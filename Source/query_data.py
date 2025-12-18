import sqlite3

def run_anayltics_avg_salary():
    # Finds the avg salary of employees in the company (working on cleaned datbasse info only)
    conn = sqlite3.connect('hr_data.db')
    cursor = conn.cursor()

    # Query to find the average salary
    query = "SELECT AVG(salary) FROM employees"
    cursor.execute(query)

    # fetchone() gets the single result from the average calculation
    result = cursor.fetchone()

    if result and result[0] is not None:
        print(f"The average company salary is: ${result[0]:,.2f}")
    else:
        print(f"Average Salary: No data found.")

    conn.close()

def get_ordinal(n) -> str:
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    else:
        temp = (n % 10)
        if temp == 1:
            return f"{n}st"
        elif temp == 2:
            return f"{n}nd"
        elif temp == 3:
            return f"{n}rd"
    return f"{n}th"


def run_anayltics_n_highest_earner(count = 1):
    # Finds the single higest earner in the company (working on cleaned database info only)
    conn = sqlite3.connect('hr_data.db')
    cursor = conn.cursor()

    # Query to find the highest earner
    query = "SELECT id, salary FROM employees ORDER BY salary DESC LIMIT ?"
    cursor.execute(query, [count])

    # fetall() gets list of tuples containing all rows of a query result set
    result = cursor.fetchall()

    if result:
         for i, value in enumerate(result):
            print(f"The {get_ordinal(i+1)} earner is {value[0]} with a salary of ${value[1]:,.2f}")  
            #print(f"The top {i+1} earner is {value[0]} with a salary of ${value[1]:,.2f}")  
    else:
        print(f"Highest Salary: No data found.")

    conn.close()

def run_anayltics_avg_employee_tenure():
    # Finds the avg tenure of employees in the company (working on cleaned database info only)
    conn = sqlite3.connect('hr_data.db')
    cursor = conn.cursor()

    # Query to find avg tenure of each employee first in days using built in SQL tool JULIANDAY
    query = "SELECT AVG(JULIANDAY('now') - JULIANDAY(hire_date)) /365.25 from employees"
    cursor.execute(query)

    # fetchone()
    result = cursor.fetchone()

    if result and result[0] is not None:
        print(f"The Average Tenure of employees in the datbase is: {result[0]:.2f} years")
    else:
        print(f"Average Tenure: No data found.")
    conn.close()

if __name__ == "__main__":
    # By default show the top 5 earners 
    NTOP_EARNERS = 1000
    print(f"\n--- Company Analytics Report ---")
    
    run_anayltics_avg_salary()
    print(f"--------------------------------")
    
    run_anayltics_avg_employee_tenure()
    print(f"--------------------------------")
    
    run_anayltics_n_highest_earner(NTOP_EARNERS)
    print(f"--------------------------------")