# HR Data Validation Tool

A lightweight, configuration-driven Python utility designed to audit and validate HR employee records. This tool identifies formatting errors, range violations, and missing data in CSV exports.

## Project Structure

* **`validator.py`**: The core execution script that processes the data.
* **`config.json`**: A JSON configuration file defining the validation rules.
* **`employees.csv`**: The input source file containing raw employee records.
* **`validation_errors.csv`**: The output report listing all discovered inconsistencies(in CSV format).
* **`validation_errors.json`**: The output report listing all discovered inconsistencies (in JSON format).

## Setup and Usage

1. **Configure Rules**: Open `config.json` to define your specific data requirements.
2. **Prepare Data**: Ensure your input file is named `employees.csv`.
3. **Execute**:
```bash
python validator.py

```


4. **Review Results**: Open `validation_errors.csv` for the error report.