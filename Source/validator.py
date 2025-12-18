import logging, json, csv, sqlite3, os
from datetime import datetime

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ErrorReporter:
    #Manages the collection and writing of validation errors to multiple formats.
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
        # Writing any entries with erros that do not follow config rules to CSV, JSON, Parquet
        if not self.errors:
            print(f"\nReport: 0 errors recorded. Data is clean!")
            return
        
        # 1. CSV Report
        try:
            with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(self.errors)
                logging.info(f"CSV Report written: {self.csv_filename}")
        except Exception as e:
            logging.critical(f"CRITICAL: Failed to write CSV report: {e}")

        # 2. JSON Report
        try:
            with open(self.json_filename, mode='w', encoding='utf-8') as file:
                json.dump(self.errors, file, indent=4)
                logging.info(f"JSON Report written: {self.json_filename}")
        except Exception as e:
            logging.error(f"Failed to write JSON report: {e}")

        # 3. Parquet Report
        try:
            import pandas as pd
            df = pd.DataFrame(self.errors)
            df.to_parquet(self.parquet_filename)
            logging.info(f"Parquet Report written: {self.parquet_filename}")
        except ImportError:
            logging.warning("Skipping Parquet: pandas/pyarrow not installed.")

    def get_error_count(self) -> int:
        return len(self.errors)

class HRDataValidator:
    # Validates HR data and saves successful entries (that follow config rules) to a SQL database.
    def __init__(self, reporter: ErrorReporter, config_filepath: str):
        self.reporter = reporter
        self.db_path = 'hr_data.db'
        
        # Defaults as a fall back if config file is not found/provided
        self.rules = {
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
                self.rules.update({
                    "min_salary": config['salary_rules']['min'],
                    "max_salary": config['salary_rules']['max'],
                    "id_len": config['id_rules']['required_length'],
                    "date_format": config['date_rules']['format'],
                    "phone_len": config['phone_rules']['required_length'],
                    "email_symbol": config['email_rules']['required_symbol']
                })
                logging.info(f"Configuration loaded from {config_filepath}.")
        except Exception as e:
            logging.warning(f"Using fallback defaults: {e}")

        self._init_db()

    def _init_db(self):
        # Initializes a fresh database table for clean data.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS employees")
        cursor.execute('''
            CREATE TABLE employees (
                id TEXT PRIMARY KEY,
                salary REAL,
                hire_date TEXT,
                email TEXT,
                phone TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_clean_record(self, record: dict):
        # Saves a single validated record to the database.
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (id, salary, hire_date, email, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (record['id'], record['salary'], record['hire_date'], record['email'], record['phone']))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Database Insert Error: {e}")

    def _log_and_report(self, index: int, record: dict, field: str, message: str):
        logging.error(message)
        self.reporter.record_error(index, record, field, message)

    def validate_salary(self, index: int, record: dict) -> bool:
        raw_val = record.get("salary", "")
        # Clean the data: handle 'seventy-k', '$', and commas
        s = str(raw_val).lower().strip().replace('$', '').replace(',', '')
        
        # Real-world transformation
        if s == 'seventy-k': clean_val = 70000.0
        elif s.endswith('k'):
            try: clean_val = float(s.replace('k', '')) * 1000
            except: clean_val = 0.0
        else:
            try: clean_val = float(s)
            except: clean_val = -1.0

        if clean_val < self.rules['min_salary'] or clean_val > self.rules['max_salary']:
            msg = f"Salary {raw_val} failed validation."
            self._log_and_report(index, record, 'salary', msg)
            return False
        
        # Update record with the cleaned numeric value for the database
        record['salary'] = clean_val
        return True

    def validate_phone(self, index: int, record: dict) -> bool:
        val = str(record.get("phone", ""))
        if len(val) != self.rules['phone_len']:
            self._log_and_report(index, record, 'phone', f"Must be {self.rules['phone_len']} digits.")
            return False
        return True

    def validate_email(self, index: int, record: dict) -> bool:
        val = record.get("email", "")
        if val.count(self.rules['email_symbol']) != 1:
            self._log_and_report(index, record, 'email', "Invalid email format.")
            return False
        return True

    def validate_hire_date(self, index: int, record: dict) -> bool:
        val = record.get("hire_date", "")
        try:
            datetime.strptime(val, self.rules['date_format'])
            return True
        except:
            self._log_and_report(index, record, 'hire_date', f"Date {val} is invalid.")
            return False

    def validate_id(self, index: int, record: dict) -> bool:
        val = str(record.get("id", "")).strip()
        if len(val) != self.rules['id_len']:
            self._log_and_report(index, record, 'id', f"ID must be {self.rules['id_len']} chars.")
            return False
        return True

def load_csv(filepath: str) -> list:
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader: data.append(row)
        logging.info(f"Loaded {len(data)} records.")
    except Exception as e:
        logging.error(f"Failed to load CSV: {e}")
    return data

if __name__ == "__main__":
    data = load_csv('employees.csv')
    
    if data:
        reporter = ErrorReporter('validation_errors')
        validator = HRDataValidator(reporter, 'config.json')
        
        clean_count = 0
        print("\n--- Starting Data Pipeline ---")
        
        for i, record in enumerate(data):
            # Track if ALL validations pass for this row
            results = [
                validator.validate_id(i, record),
                validator.validate_salary(i, record),
                validator.validate_hire_date(i, record),
                validator.validate_email(i, record),
                validator.validate_phone(i, record)
            ]
            
            # If every result in the list is True
            if all(results):
                validator.save_clean_record(record)
                clean_count += 1

        print(f"\n--- Pipeline Summary ---")
        print(f"Total Rows Processed: {len(data)}")
        print(f"Successful (Saved to DB): {clean_count}")
        print(f"Failed (Logged to Reports): {reporter.get_error_count()}")
        
        reporter.write_report()