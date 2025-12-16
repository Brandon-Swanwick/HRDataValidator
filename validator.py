import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HRDataValidator:
    def __init__(self, data_list: list):
        self.raw_data = data_list
        self.errors = 0
    
    def validate_hire_date(self, date_str: str, date_format: str = '%Y-%m-%d') -> bool:
        # Validates if a date string conforms to the expected format (YYYY-MM-DD).
        try:
            # Attempt to parse the date string using the expected format
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            # If parsing fails, then its not a valid date format
            logging.error(f"Date '{date_str}' failed format check Expected {date_format}.")
            self.errors += 1
            return False

    def validate_employee_id(self, employee_id: str) -> bool:
        if len(employee_id) == 0: # if Employe ID is field is Empty we have an error
            logging.error(f"Employee ID is empty/null.")
            self.errors += 1
            return False
        else:
            if len(employee_id) == 7: # if Employe ID is field len 7 no error
                return True
            else:
                logging.error(f"Employee ID is not 7 chars long.")
                self.errors += 1
                return False

    def validate_salary(self, salary) -> bool:
        try:
            salary = float(salary) # casting slary to a float wrapped in a try statement
            if salary < 0: # if salary is a float but less than 0 we have an error
                logging.error(f"Salary '{salary}' failed non-negative check.")
                self.errors += 1
                return False
            else:           # No errors here salary was correct and non negative
                return True
        except (ValueError,TypeError):   # failed to cast to float we have an error in the data
            logging.error(f"Salary '{salary}' failed type conversion. Not numeric.")
            self.errors += 1
            return False

if __name__ == "__main__":
    test_data = [
        # 0. PASS: All original checks pass + valid date format (YYYY-MM-DD)
        {"id": "EMP1234", "salary": 75000.00, "hire_date": "2023-10-25"},
        
        # 1. FAIL (ID length), PASS (Salary), PASS (Date)
        {"id": "SHORT", "salary": 90000, "hire_date": "2022-01-15"},
        
        # 2. FAIL (Salary type), PASS (ID), PASS (Date)
        {"id": "EMP1234", "salary": "ABC", "hire_date": "2024-03-01"},
        
        # 3. FAIL (Empty ID), PASS (Salary), PASS (Date)
        {"id": "", "salary": 50000, "hire_date": "2021-11-09"},
        
        # 4. NEW TEST: PASS (ID/Salary), FAIL (Date Format - using MM/DD/YYYY)
        {"id": "EMP9999", "salary": 55000, "hire_date": "10/25/2023"},
        
        # 5. NEW TEST: PASS (ID/Salary), FAIL (Invalid Date - Feb 30th)
        {"id": "EMP0000", "salary": 65000, "hire_date": "2024-02-30"},
    ]

    validator = HRDataValidator(test_data)

    for record in test_data:
        # Call the methods you defined on the 'validator' object
        id_valid = validator.validate_employee_id(record["id"])
        salary_valid = validator.validate_salary(record["salary"])
        date_valid = None

        if "hire_date" in record:
            date_valid = validator.validate_hire_date(record["hire_date"])

        # Optional: Print the status for that record
        print(f"ID: {record['id']} | Salary: {record['salary']} | Date: {record.get('hire_date', 'N/A')} | Valid ID: {id_valid} | Valid Salary: {salary_valid} | Valid Date: {date_valid}\n")
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(test_data)}")
    print(f"Total Errors Recorded: {validator.errors}")
