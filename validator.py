import logging
from datetime import datetime

# Set up basic logging configuration
# This format ensures a clean output without extra newlines.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HRDataValidator:
    #A class to validate HR data fields according to predefined rules (Day 1 Complete).
  
    def __init__(self, data_list: list, min_salary: float = 30000.0, max_salary: float = 300000.0):
        self.data = data_list
        self.errors = 0
        # Storing the parameters
        self.min_salary = min_salary
        self.max_salary = max_salary

    def validate_phone(self, phone: str) -> bool:
     
        # Validates that the phone number is a valid 7-digit phone number.
     
        if len(phone) != 7:
            logging.error(f"Phone Validation check has failed: Phone number must be exactly 7 digits")
            self.errors += 1
            return False
        return True

    def validate_email(self, email: str) -> bool:
       
        #Validates if an email string is non-empty and contains exactly one '@' symbol.
    
        if not email:
            logging.error(f"Email Check has failed: Email address can not be empty.")
            self.errors += 1
            return False
        
        # Rule 2: Must contain exactly one '@'
        if email.count('@') != 1:
            logging.error(f"Email '{email}' check failed: Must contain exactly one @ symbol.")
            self.errors += 1
            return False
        
        return True

    def validate_hire_date(self, date_str: str, date_format: str = '%Y-%m-%d') -> bool:
      
        #Validates if a date string conforms to the expected format (YYYY-MM-DD) and is a valid date.
   
        try:
            # Attempt to parse the date string using the expected format
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            logging.error(f"Date '{date_str}' failed format check Expected {date_format}.")
            self.errors += 1
            return False

    def validate_employee_id(self, employee_id: str) -> bool:
      
        # Validates if an employee ID is non-empty and exactly 7 characters long.
       
        if len(employee_id) == 0:
            logging.error(f"Employee ID is empty/null.")
            self.errors += 1
            return False
        else:
            if len(employee_id) == 7:
                return True
            else:
                logging.error(f"Employee ID is not 7 chars long.")
                self.errors += 1
                return False

    def validate_salary(self, salary, min_salary: float, max_salary: float) -> bool:
    
        # Validates if the salary is numeric and falls within the provided min/max range.
     
        try:
            numeric_salary = float(salary)
            
            if numeric_salary < 0:
                logging.error(f"Salary '{salary}' failed non-negative check.")
                self.errors += 1
                return False
            
            # Bounds checks
            if numeric_salary < min_salary:
                logging.error(f"Salary '{salary}' failed as this was less than the minimum of '{min_salary}'.")
                self.errors += 1
                return False
            elif numeric_salary > max_salary:
                logging.error(f"Salary '{salary}' failed as this was greater than the maximum of '{max_salary}'.")
                self.errors += 1
                return False
            
            return True
        
        except (ValueError, TypeError):
            logging.error(f"Salary '{salary}' failed type conversion. Not numeric.")
            self.errors += 1
            return False

if __name__ == "__main__":
    test_data = [
        # 0. FAIL (Max Salary)
        {"id": "EMP1234", "salary": 750000.00, "hire_date": "2023-10-25", "email": "joe.smith@corp.com", "phone": "5551234"},
        
        # 1. FAIL (ID length, Min Salary)
        {"id": "SHORT", "salary": 1500, "hire_date": "2022-01-15", "email": "pass@test.com", "phone": "5559876"},
        
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

        # 8. FAIL (Phone - too short)
        {"id": "EMP5000", "salary": 60000, "hire_date": "2023-11-11", "email": "valid@email.com", "phone": "123"},
        
        # 9. FAIL (Phone - too long)
        {"id": "EMP6000", "salary": 70000, "hire_date": "2024-01-01", "email": "valid@email.com", "phone": "1234567890"},
    ]

    validator = HRDataValidator(test_data)
    print("\n")
    
    # --- Processing Loop ---
    for record in test_data:
        id_valid = validator.validate_employee_id(record["id"])
        date_valid = validator.validate_hire_date(record["hire_date"])
        email_valid = validator.validate_email(record["email"])
        phone_valid = validator.validate_phone(record["phone"])

        # Overriding the default min/max check in the loop call for testing
        salary_valid = validator.validate_salary(record["salary"], min_salary=30000, max_salary= 150000)

        # Print the status (Cleaned up print statement)
        print(f"ID: {record['id']} | Salary: {record['salary']} | Date: {record['hire_date']} | Email: {record['email']} | Phone: {record['phone']} | Valid ID: {id_valid} | Valid Salary: {salary_valid} | Valid Date: {date_valid} | Valid Email: {email_valid} | Valid Phone: {phone_valid}\n")
    
    # Final print statement
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(test_data)}")
    print(f"Total Errors Recorded: {validator.errors}")