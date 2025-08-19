# DesigniteJava Galaxy Tool

This Galaxy tool wraps [DesigniteJava](https://www.designite-tools.com/) to detect code smells and compute metrics for Java projects.

---

## What is DesigniteJava?

DesigniteJava analyzes Java source code to detect code smells and calculate various software metrics. This tool integrates DesigniteJava into Galaxy, allowing you to run analyses on zipped Java projects and receive results as CSV files.

---

## Inputs

- **Input:** ZIP archive of a Java project (e.g., created with `git archive` or `zip`).

---

## Outputs

The output is a ZIP archive containing CSV files with metrics and detected smells.  
The exact files depend on your DesigniteJava version:

### Community Version

- `typeMetrics.csv`
- `methodMetrics.csv`
- `designCodeSmells.csv`
- `implementationCodeSmells.csv`

### Professional Version

- `TypeMetrics.csv`
- `MethodMetrics.csv`
- `DesignSmells.csv`
- `ImplementationSmells.csv`
- `ArchitectureSmells.csv`
- `TestSmells.csv`
- `TestabilitySmells.csv`
- `DesigniteLog<date>.txt`

> **Note:** You need a licence key to access the Professional Version

---

## How It Works

1. **Unzips** your Java project.
2. **Runs** DesigniteJava:
   ```
   java -jar DesigniteJava.jar -i <input_dir> -o <output_dir>
   ```
3. **Packages** the resulting CSVs into a ZIP for Galaxy output.

---

## Usage Example

1. Upload a ZIP of your Java project.
2. Run the tool.
3. Download and extract the output ZIP to access the CSV reports.

---

## Troubleshooting

- If you see missing output files, check that your input ZIP contains valid Java source code.
- For Professional features, ensure your license is registered.

