import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HRDataValidator:
    def __init__(self, data_list: list):
        self.raw_data = data_list
        self.errors = 0
    
    def validate_employee_id(self, employee_id: str) -> bool:
        if len(employee_id) == 0: # if Employe ID is field is Empty we have an error
            logging.error(f"Employee ID is empty/null.")
            self.errors = self.errors + 1
            return False
        else:
            if len(employee_id) == 7: # if Employe ID is field len 7 no error
                return True
            else:
                logging.error(f"Employee ID is not 7 chars long.")
                self.errors = self.errors + 1
                return False

    def validate_salary(self, salary) -> bool:
        try:
            salary = float(salary) # casting slary to a float wrapped in a try statement
            if salary < 0: # if salary is a float but less than 0 we have an error
                logging.error(f"Salary '{salary}' failed non-negative check.")
                self.errors = self.errors + 1
                return False
            else:           # No errors here salary was correct and non negative
                return True
        except (ValueError,TypeError):   # failed to cast to float we have an error in the data
            logging.error(f"Salary '{salary}' failed type conversion. Not numeric.")
            self.errors = self.errors + 1
            return False

if __name__ == "__main__":
    test_data = [
        {"id": "EMP1234", "salary": 75000.00},  # Should PASS
        {"id": "SHORT", "salary": 90000},      # Should FAIL (ID length)
        {"id": "EMP1234", "salary": "ABC"},    # Should FAIL (Salary type)
        {"id": "", "salary": 50000},           # Should FAIL (Empty ID)
    ]

    validator = HRDataValidator(test_data)

    for record in test_data:
        # Call the methods you defined on the 'validator' object
        id_valid = validator.validate_employee_id(record["id"])
        salary_valid = validator.validate_salary(record["salary"])

        # Optional: Print the status for that record
        print(f"ID: {record['id']} | Salary: {record['salary']} | Valid ID: {id_valid} | Valid Salary: {salary_valid}")
    
    print(f"\n--- Final Validation Summary ---")
    print(f"Total records processed: {len(test_data)}")
    print(f"Total Errors Recorded: {validator.errors}")
