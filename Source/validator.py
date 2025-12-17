import logging, json, csv
from datetime import datetime

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ErrorReporter:
    """Manages the collection and writing of validation errors to a CSV report file."""
    def __init__(self, output_filename: str = 'validation_errors'):
        self.csv_filename = f"{output_filename}.csv"
        self.json_filename = f"{output_filename}.json"
        self.parquet_filename = f"{output_filename}.parquet"
        self.errors = []
        self.fieldnames = ['timestamp', 'record_index', 'employee_id', 'field', 'value', 'error_message']

    def record_error(self, index: int, record: dict, field_name: str, error_message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_entry = {
            'timestamp': timestamp,
            'record_index': index + 1,
            'employee_id': record.get('id', 'N/A'),
            'field': field_name,
            'value': record.get(field_name, 'N/A'),
            'error_message': error_message
        }
        self.errors.append(error_entry)

    def write_report(self):
        if not self.errors:
            print(f"\nReport: 0 errors recorded. Data is clean!")
            return
        
        # Write to CSV Report
        try:
            with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(self.errors)
            print(f"\nReport written successfully to {self.csv_filename}. Total errors: {len(self.errors)}")
        except Exception as e:
            logging.critical(f"CRITICAL: Failed to write error report: {e}")

        # Write to JSON report
        try:
            with open(self.json_filename, mode='w', encoding='utf-8') as file:
                json.dump(self.errors, file, indent=4)
                logging.info(f"JSON Report written: {self.json_filename}")
        except Exception as e:
            logging.error(f"Failed to write JSON report: {e}")

        # Write to Parquet (requires Pandas) 
        try:
            # keeping pandas usage limited incase a system running this does not have pandas it will avoid a top level structure crash and ensures CSV and JSON still work
            import pandas as pd
            df = pd.DataFrame(self.errors)
            df.to_parquet(f"{self.parquet_filename}")
        except ImportError:
            logging.warning(f"skipping Parquet: pandas/pyarrow not installed.")
        
        logging.info(f"Both CSV, and JSON outputs are logged, total of {len(self.errors)}")

    def get_error_count(self) -> int:
        return len(self.errors)

class HRDataValidator:
    """A class to validate HR data fields using external configuration rules."""
    def __init__(self, data_list: list, reporter: ErrorReporter, config_filepath: str):
        self.data = data_list
        self.reporter = reporter
        
        # Centralized system defaults if JSON loading fails
        defaults = {
            "min_salary": 30000.0,
            "max_salary": 150000.0,
            "id_len": 7,
            "phone_len": 7,
            "date_format": "%Y-%m-%d",
            "email_symbol": "@"
        }

        try:
            with open(config_filepath, 'r') as file:
                config = json.load(file)
                self.min_salary = config['salary_rules']['min']
                self.max_salary = config['salary_rules']['max']
                self.id_len = config['id_rules']['required_length']
                self.date_format = config['date_rules']['format']
                self.phone_len = config['phone_rules']['required_length']
                self.email_symbol = config['email_rules']['required_symbol']
                logging.info("Configuration loaded successfully from JSON.")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logging.warning(f"Config issues ({e}). Using system fallback defaults.")
            self.min_salary = defaults["min_salary"]
            self.max_salary = defaults["max_salary"]
            self.id_len = defaults["id_len"]
            self.phone_len = defaults["phone_len"]
            self.date_format = defaults["date_format"]
            self.email_symbol = defaults["email_symbol"]

    def _log_and_report(self, index: int, record: dict, field: str, message: str):
        logging.error(message)
        self.reporter.record_error(index, record, field, message)

    def validate_phone(self, index: int, record: dict, phone: str) -> bool:
        phone_str = str(phone) 
        if len(phone_str) != self.phone_len:
            msg = f"Phone check failed: '{phone_str}' must be exactly {self.phone_len} digits."
            self._log_and_report(index, record, 'phone', msg)
            return False
        return True

    def validate_email(self, index: int, record: dict, email: str) -> bool:
        if not email or email.count(self.email_symbol) != 1:
            msg = f"Email check failed: '{email}' must contain exactly one '{self.email_symbol}'."
            self._log_and_report(index, record, 'email', msg)
            return False
        return True

    def validate_hire_date(self, index: int, record: dict, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, self.date_format)
            return True
        except (ValueError, TypeError):
            msg = f"Date check failed: '{date_str}' expected format {self.date_format}."
            self._log_and_report(index, record, 'hire_date', msg)
            return False

    def validate_employee_id(self, index: int, record: dict, employee_id: str) -> bool:
        clean_id = str(employee_id).strip()
        if not clean_id or len(clean_id) != self.id_len:
            msg = f"ID check failed: '{employee_id}' must be {self.id_len} chars."
            self._log_and_report(index, record, 'id', msg)
            return False
        return True

    def validate_salary(self, index: int, record: dict, salary: str) -> bool:
        try:
            val = float(salary)
            if val < self.min_salary or val > self.max_salary:
                msg = f"Salary {val} out of bounds ({self.min_salary}-{self.max_salary})."
                self._log_and_report(index, record, 'salary', msg)
                return False
            return True
        except (ValueError, TypeError):
            msg = f"Salary '{salary}' failed: Not a numeric value."
            self._log_and_report(index, record, 'salary', msg)
            return False

def load_csv_from_file(filepath: str) -> list:
    """Reads the CSV file and converts it into a list of dictionaries."""
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        logging.info(f"Successfully loaded {len(data)} records from {filepath}.")
    except FileNotFoundError:
        logging.error(f"The file {filepath} was not found.")
    return data

if __name__ == "__main__":
    # File paths
    CONFIG_PATH = 'config.json'
    REPORT_PATH = 'validation_errors'
    EMPLOYEES_PATH = 'employees.csv'

    # Load data
    data = load_csv_from_file(EMPLOYEES_PATH)
    
    if data:
        reporter = ErrorReporter(REPORT_PATH)
        validator = HRDataValidator(data, reporter, CONFIG_PATH)
        
        print("\n--- Starting Data Validation ---")
        for i, record in enumerate(data):
            validator.validate_employee_id(i, record, record.get("id", ""))
            validator.validate_salary(i, record, record.get("salary", ""))
            validator.validate_hire_date(i, record, record.get("hire_date", ""))
            validator.validate_email(i, record, record.get("email", ""))
            validator.validate_phone(i, record, record.get("phone", ""))

        print(f"\n--- Final Summary ---")
        print(f"Total Records: {len(data)} | Total Errors: {reporter.get_error_count()}")
        reporter.write_report()
    else:
        print("\nError: No data loaded. Check if employees.csv exists.")