import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HRDataValidator:
    def __init__(self, data_list: list):
        self.raw_data = data_list
        self.errors = 0

    def validate_phone(self, phone:str) -> bool:
        # Validating that the phone number is a valid 7 digit phone number
        if len(phone) != 7:
            logging.error(f"Phone Validation check has failed: Phone number must be exactly 7 digits")
            self.errors += 1
            return False
        return True

    def validate_email(self, email: str) -> bool:
        # Validates if an email string is non-empty and contains exactly one '@' symbol to conform to the proper format
        if not email:
            logging.error(f"Email Check has failed: Email address can not be empty.")
            self.errors += 1
            return False
        
        # Rule 2: Must contain exactly one '@'
        if email.count('@') != 1:
            logging.error(f"Email '{email}' check failed: Must contain exactly one @ symbol")
            self.errors += 1
            return False
        
        # Both checks bassed
        return True

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
        # 0. PASS: All 5 fields are valid
        {"id": "EMP1234", "salary": 75000.00, "hire_date": "2023-10-25", "email": "joe.smith@corp.com", "phone": "5551234"},
        
        # 1. FAIL (ID length)
        {"id": "SHORT", "salary": 90000, "hire_date": "2022-01-15", "email": "pass@test.com", "phone": "5559876"},
        
        # 2. FAIL (Salary Type)
        {"id": "EMP1234", "salary": "ABC", "hire_date": "2024-03-01", "email": "pass@test.com", "phone": "1234567"},
        
        # 3. FAIL (Empty ID)
        {"id": "", "salary": 50000, "hire_date": "2021-11-09", "email": "pass@test.com", "phone": "9990000"},
        
        # 4. FAIL (Date Format)
        {"id": "EMP9999", "salary": 55000, "hire_date": "10/25/2023", "email": "pass@test.com", "phone": "1112222"},
        
        # 5. FAIL (Invalid Date Value)
        {"id": "EMP0000", "salary": 65000, "hire_date": "2024-02-30", "email": "pass@test.com", "phone": "7776666"},

        # 6. FAIL (Email - missing '@')
        {"id": "EMP7777", "salary": 45000, "hire_date": "2023-05-01", "email": "invalid.email.com", "phone": "8887777"},
        
        # 7. FAIL (Email - empty string)
        {"id": "EMP8888", "salary": 80000, "hire_date": "2022-12-12", "email": "", "phone": "1002003"},

        # 8. NEW TEST: FAIL (Phone - too short)
        {"id": "EMP5000", "salary": 60000, "hire_date": "2023-11-11", "email": "valid@email.com", "phone": "123"},
        
        # 9. NEW TEST: FAIL (Phone - too long)
        {"id": "EMP6000", "salary": 70000, "hire_date": "2024-01-01", "email": "valid@email.com", "phone": "1234567890"},
    ]

    validator = HRDataValidator(test_data)
    
    # --- Simplified and Unified Loop ---
    for record in test_data:
        # Now we can call all validations without checking for the key, 
        # as we ensured all records have all keys above!
        id_valid = validator.validate_employee_id(record["id"])
        salary_valid = validator.validate_salary(record["salary"])
        date_valid = validator.validate_hire_date(record["hire_date"])
        email_valid = validator.validate_email(record["email"]) # NEW CALL
        phone_valid = validator.validate_phone(record["phone"])

        # Print the status, including the new email check
        print(f"ID: {record['id']} | Salary: {record['salary']} | Date: {record['hire_date']} | Email: {record['email']} | Phone: {record['phone']} | Valid ID: {id_valid} | Valid Salary: {salary_valid} | Valid Date: {date_valid} | Valid Email: {email_valid} | Valid Phone: {phone_valid}")
    
    # Final print statement...
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(test_data)}")
    print(f"Total Errors Recorded: {validator.errors}") 
    # EXPECTED ERRORS: 7 (ID, Salary, ID, Date, Date, Email, Email)

    validator = HRDataValidator(test_data)

    for record in test_data:
        # Call the methods you defined on the 'validator' object
        id_valid = validator.validate_employee_id(record["id"])
        salary_valid = validator.validate_salary(record["salary"])
        email_valid = validator.validate_email(record["email"])
        date_valid = validator.validate_hire_date(record["hire_date"])
        phone_valid = validator.validate_phone(record["phone"])

        # Optional: Print the status for that record
        print(f"ID: {record['id']} | Salary: {record['salary']} | Date: {record['hire_date']} | Email: {record['email']} | Phone: {record['phone']} | Valid ID: {id_valid} | Valid Salary: {salary_valid} | Valid Date: {date_valid} | Valid Email: {email_valid} | Valid Phone: {phone_valid}")
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(test_data)}")
    print(f"Total Errors Recorded: {validator.errors}")
