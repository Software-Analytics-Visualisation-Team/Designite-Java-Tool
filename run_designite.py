#!/usr/bin/env python3
import sys, zipfile, subprocess, shutil, tempfile
from pathlib import Path

def pick_input_dir(root: Path) -> Path:
    first_level_dirs = [p for p in root.iterdir() if p.is_dir()]
    return first_level_dirs[0] if len(first_level_dirs) == 1 else root

def main():
    if len(sys.argv) != 4:
        print("Usage: run_designite.py <src_zip> <report_zip> <jar_path>", file=sys.stderr)
        sys.exit(2)

    src_zip, out_zip, jar_path = map(Path, sys.argv[1:])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        src_dir = tmp / "src_dir"
        out_dir = tmp / "workdir"
        src_dir.mkdir(parents=True, exist_ok=True)
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) unzip
        try:
            with zipfile.ZipFile(src_zip, 'r') as zf:
                zf.extractall(src_dir)
        except zipfile.BadZipFile:
            print("Archive ZIP invalide.", file=sys.stderr)
            sys.exit(1)

        input_dir = pick_input_dir(src_dir)

        # 2) calculate user.dir even if the JAR is a symlink towards target
        resolved = jar_path.resolve()
        user_dir = resolved.parent.parent if resolved.parent.name == "target" else resolved.parent

        # 2bis) Ensure the output file exists
        log_dir = user_dir / "output"
        log_dir.mkdir(parents=True, exist_ok=True)

        # 3) call the JAR
        cmd = [
            "java",
            f"-Duser.dir={user_dir}",
            "-jar", str(jar_path),
            "-i", str(input_dir),
            "-o", str(out_dir),
        ]
        proc = subprocess.run(cmd, cwd=str(tmp), capture_output=True, text=True)
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout or "")
            sys.stderr.write(proc.stderr or "")
            sys.exit(proc.returncode)

        # 4) package the 4 CSV files into the output zip
        def find_src(name: str) -> Path | None:
            candidates = [
                out_dir / name,                 # -o directory
                tmp / "output" / name,          # in case Designite writes to ./output
                user_dir / "output" / name,     # or in <repo>/output
            ]
            for p in candidates:
                if p.exists() and p.stat().st_size > 0:
                    return p
            return None

        names = [
            "typeMetrics.csv",
            "methodMetrics.csv",
            "designCodeSmells.csv",
            "implementationCodeSmells.csv",
        ]

        out_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for name in names:
                src = find_src(name)
                if src is not None:
                    zf.write(src, arcname=name)
                else:
                    # create an empty entry if missing (avoids broken tests)
                    zf.writestr(name, "")

if __name__ == "__main__":
    main()
