# DesigniteJava Galaxy Tool

This tool wraps [DesigniteJava](https://github.com/tushartushar/DesigniteJava) for use in Galaxy, enabling automated detection of code smells and computation of metrics for Java projects.

## Setup

1. **Clone DesigniteJava**  
   Clone the official repository inside the `designite_java` directory:
   ```sh
   git clone https://github.com/tushartushar/DesigniteJava.git
   ```

2. **Build the JAR**  
   Build the `DesigniteJava.jar` using Maven:
   ```sh
   cd DesigniteJava
   mvn -U clean package -DskipTests
   ```

3. **Symlink the JAR**  
   In the `designite_java` directory, create a symlink to the built JAR:
   ```sh
   ln -s DesigniteJava/target/DesigniteJava.jar DesigniteJava.jar
   ```

4. **Test or Serve with Planemo**  
   - To run tests and update test data:
     ```sh
     planemo test designite_java.xml --update_test_data
     ```
   - Or to serve locally:
     ```sh
     planemo serve
     ```
   - Expected outputs are in `test-data/expected`.

## Usage

- **Input:** ZIP archive of a Java project (e.g., from `git archive`)
- **Output:** ZIP archive containing four CSV files with metrics:
  - `typeMetrics.csv`
  - `methodMetrics.csv`
  - `designCodeSmells.csv`
  - `implementationCodeSmells.csv`

## How It Works

1. The tool unzips the input Java project.
2. It calculates the correct `user.dir` (required by DesigniteJava for proper file resolution).
3. It launches the JAR with:
   ```
   java -Duser.dir=<DesigniteJava directory> -jar DesigniteJava.jar -i <input_dir> -o <output_dir>
   ```
   > **Note:** The `-Duser.dir` flag is essential. If omitted or set incorrectly, DesigniteJava may fail with misleading "input file invalid" errors, even if the input path is correct.
4. The tool collects the output CSVs (by default, written to `DesigniteJava/output`), and packages them into a single ZIP for Galaxy output.

## Troubleshooting

- If you encounter errors about invalid input files, ensure that:
  - The `-Duser.dir` property is set to the directory containing the DesigniteJava JAR.
  - You are not running the JAR from outside the expected directory structure.

## References

- [DesigniteJava GitHub](https://github.com/tushartushar/DesigniteJava#readme)