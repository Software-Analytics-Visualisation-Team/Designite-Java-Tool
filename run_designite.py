#!/usr/bin/env python3
import sys
import zipfile
import subprocess
import tempfile
from pathlib import Path

def unzip(src_zip: Path, dest_dir: Path) -> None:
    with zipfile.ZipFile(src_zip, 'r') as zf:
        zf.extractall(dest_dir)

def pick_input_dir(root: Path) -> Path:
    # If the zip contains a single root folder, use it, otherwise use the root
    first_level_dirs = [p for p in root.iterdir() if p.is_dir()]
    return first_level_dirs[0] if len(first_level_dirs) == 1 else root

def zip_dir(src_dir: Path, out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in src_dir.rglob("*"):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(src_dir))

def main():
    if len(sys.argv) != 4:
        print("Usage: run_designite.py <src_zip> <report_zip> <jar_path>", file=sys.stderr)
        sys.exit(2)

    src_zip = Path(sys.argv[1])
    report_zip = Path(sys.argv[2])
    jar_path = Path(sys.argv[3])

    if not src_zip.exists():
        print(f"Archive introuvable: {src_zip}", file=sys.stderr)
        sys.exit(1)
    if not jar_path.exists():
        print(f"JAR introuvable: {jar_path}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        src_dir = tmp / "src"
        out_dir = tmp / "out"
        src_dir.mkdir()
        out_dir.mkdir()

        # 1) unzip input
        try:
            unzip(src_zip, src_dir)
        except zipfile.BadZipFile:
            print("Archive ZIP invalide.", file=sys.stderr)
            sys.exit(1)

        input_dir = pick_input_dir(src_dir)

        # 2) launch DesigniteJava
        cmd = [
            "java",
            "-jar", str(jar_path),
            "-i", str(input_dir),
            "-o", str(out_dir),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        # Relay output for easier debugging in Galaxy
        if proc.stdout:
            print(proc.stdout, file=sys.stdout, end="")
        if proc.stderr:
            print(proc.stderr, file=sys.stderr, end="")
        if proc.returncode != 0:
            sys.exit(proc.returncode)

        # 3) zip all produced files
        # If nothing was written (unlikely case), create an empty zip instead of failing
        if any(out_dir.iterdir()):
            zip_dir(out_dir, report_zip)
        else:
            with zipfile.ZipFile(report_zip, "w"):
                pass

if __name__ == "__main__":
    main()
