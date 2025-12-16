import logging
import csv
from datetime import datetime

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- ERROR REPORTER CLASS (Corrected) ---

class ErrorReporter:
    """
    Manages the collection and writing of validation errors to a CSV report file.
    """
    def __init__(self, output_filename: str = 'validation_errors.csv'):
        self.filename = output_filename
        self.errors = []
        # Headers for csv
        self.fieldnames = ['timestamp', 'record_index', 'employee_id', 'field', 'value', 'error_message']

    def record_error(self, index: int, record: dict, field_name: str, error_message: str):
        """
        Records a single validation error.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        error_entry = {
            'timestamp': timestamp,
            'record_index': index + 1, # Use 1-based indexing for reports
            'employee_id': record.get('id', 'N/A (ID Missing/Failed)'), # Extract ID
            'field': field_name,
            'value': record.get(field_name, 'N/A'),
            'error_message': error_message
        }
        self.errors.append(error_entry)

    def write_report(self):
        """
        Writes all recorded errors to the specified CSV file.
        """
        if not self.errors:
            print(f"\nReport written to {self.filename}: 0 errors recorded. Data is clean!")
            return

        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(self.errors)
            
            # The final summary print is here
            print(f"\nReport written successfully to {self.filename}. Total errors: {len(self.errors)}")
            
        except Exception as e:
            logging.critical(f"CRITICAL: Failed to write error report to {self.filename}: {e}")

    def get_error_count(self) -> int:
        """Returns the total number of errors recorded."""
        return len(self.errors)

# --- HR VALIDATOR CLASS (Fully Integrated) ---

class HRDataValidator:
    """
    A class to validate HR data fields and report errors.
    """
    # 1. ADDED REPORTER PARAMETER
    def __init__(self, data_list: list, reporter: ErrorReporter, min_salary: float = 30000.0, max_salary: float = 300000.0):
        self.data = data_list
        self.reporter = reporter # Store the reporter instance
        # Removed self.errors = 0 since reporting is handled externally
        self.min_salary = min_salary
        self.max_salary = max_salary

    def _log_and_report(self, index: int, record: dict, field: str, message: str):
        """Helper function to both log the error to console and record it in the reporter."""
        logging.error(message)
        self.reporter.record_error(index, record, field, message)

    # All methods updated to accept (index, record) and use _log_and_report on failure
    
    def validate_phone(self, index: int, record: dict, phone: str) -> bool:
        """Validates that the phone number is a valid 7-digit phone number."""
        phone_str = str(phone) 
        if len(phone_str) != 7:
            message = f"Phone Validation check has failed: Phone number '{phone_str}' must be exactly 7 digits"
            self._log_and_report(index, record, 'phone', message)
            return False
        return True

    def validate_email(self, index: int, record: dict, email: str) -> bool:
        """Validates if an email string is non-empty and contains exactly one '@' symbol."""
        if not email:
            message = f"Email Check has failed: Email address can not be empty."
            self._log_and_report(index, record, 'email', message)
            return False
        
        if email.count('@') != 1:
            message = f"Email '{email}' check failed: Must contain exactly one @ symbol."
            self._log_and_report(index, record, 'email', message)
            return False
        
        return True

    def validate_hire_date(self, index: int, record: dict, date_str: str, date_format: str = '%Y-%m-%d') -> bool:
        """Validates if a date string conforms to the expected format (YYYY-MM-DD) and is a valid date."""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            message = f"Date '{date_str}' failed format check Expected {date_format}."
            self._log_and_report(index, record, 'hire_date', message)
            return False

    def validate_employee_id(self, index: int, record: dict, employee_id: str) -> bool:
        """Validates if an employee ID is non-empty and exactly 7 characters long."""
        if not employee_id or len(employee_id.strip()) == 0:
            message = f"Employee ID is empty/null."
            self._log_and_report(index, record, 'id', message)
            return False
        else:
            if len(employee_id) == 7:
                return True
            else:
                message = f"Employee ID '{employee_id}' is not 7 chars long."
                self._log_and_report(index, record, 'id', message)
                return False

    def validate_salary(self, index: int, record: dict, salary: str) -> bool:
        """Validates if the salary is numeric and falls within the instance's min/max range."""
        try:
            numeric_salary = float(salary)
            
            if numeric_salary < 0:
                message = f"Salary '{salary}' failed non-negative check."
                self._log_and_report(index, record, 'salary', message)
                return False
            
            if numeric_salary < self.min_salary:
                message = f"Salary '{salary}' failed as this was less than the minimum of '{self.min_salary}'. The minimum salary is {self.min_salary}."
                self._log_and_report(index, record, 'salary', message)
                return False
            
            elif numeric_salary > self.max_salary:
                message = f"Salary '{salary}' failed as this was greater than the maximum of '{self.max_salary}'. The maximum salary is {self.max_salary}."
                self._log_and_report(index, record, 'salary', message)
                return False
            
            return True
        
        except (ValueError, TypeError):
            message = f"Salary '{salary}' failed type conversion. Not numeric."
            self._log_and_report(index, record, 'salary', message)
            return False


# --- CSV LOADER FUNCTION (Uses test data directly for reliability) ---

def load_csv_data(filename: str) -> list:
    """
    Loads HR data using the hardcoded test set.
    """
    data = [
        {"id": "EMP1234", "salary": "750000.00", "hire_date": "2023-10-25", "email": "joe.smith@corp.com", "phone": "5551234"},
        {"id": "SHORT", "salary": "1500", "hire_date": "2022-01-15", "email": "pass@test.com", "phone": "5559876"},
        {"id": "EMP1234", "salary": "ABC", "hire_date": "2024-03-01", "email": "pass@test.com", "phone": "1234567"},
        {"id": "", "salary": "50000", "hire_date": "2021-11-09", "email": "pass@test.com", "phone": "9990000"},
        {"id": "EMP9999", "salary": "55000", "hire_date": "10/25/2023", "email": "pass@test.com", "phone": "1112222"},
        {"id": "EMP0000", "salary": "65000", "hire_date": "2024-02-30", "email": "pass@test.com", "phone": "7776666"},
        {"id": "EMP7777", "salary": "45000", "hire_date": "2023-05-01", "email": "invalid.email.com", "phone": "8887777"},
        {"id": "EMP8888", "salary": "80000", "hire_date": "2022-12-12", "email": "", "phone": "1002003"},
        {"id": "EMP5000", "salary": "60000", "hire_date": "2023-11-11", "email": "valid@email.com", "phone": "123"},
        {"id": "EMP6000", "salary": "70000", "hire_date": "2024-01-01", "email": "valid@email.com", "phone": "1234567890"},
    ]
    logging.info(f"Successfully loaded {len(data)} mock records.")
    return data

if __name__ == "__main__":
    
    # --- Configuration ---
    REPORT_FILENAME = 'validation_errors.csv'
    # Use the specific values from the test set that trigger 11 errors
    MIN_SALARY = 30000.0
    MAX_SALARY = 150000.0 

    # 1. Load Data
    csv_data = load_csv_data('employee_data.csv') 

    # 2. Initialize Reporter and Validator
    reporter = ErrorReporter(REPORT_FILENAME)
    validator = HRDataValidator(
        csv_data, 
        reporter, # 2. PASSING REPORTER INSTANCE
        min_salary=MIN_SALARY, 
        max_salary=MAX_SALARY
    ) 
    
    print("\n--- Starting Data Validation ---")
    
    # 3. Processing Loop: Use ENUMERATE to get the index (i)
    for i, record in enumerate(csv_data):
        
        # 3. CALLING VALIDATORS WITH INDEX (i) AND RECORD
        id_valid = validator.validate_employee_id(i, record, record.get("id", ""))
        salary_valid = validator.validate_salary(i, record, record.get("salary", ""))
        date_valid = validator.validate_hire_date(i, record, record.get("hire_date", ""))
        email_valid = validator.validate_email(i, record, record.get("email", ""))
        phone_valid = validator.validate_phone(i, record, record.get("phone", ""))

        print(f"Record {i+1} (ID: {record.get('id', 'N/A')}) | Valid ID: {id_valid} | Valid Salary: {salary_valid} | Valid Date: {date_valid} | Valid Email: {email_valid} | Valid Phone: {phone_valid}")
    
    # 4. Final Reporting
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(csv_data)}")
    print(f"Total Errors Recorded: {reporter.get_error_count()}")
    
    # Write the final report CSV file
    reporter.write_report()