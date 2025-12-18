import sqlite3

def run_anayltics():
    conn = sqlite3.connect('hr_data.db')
    cursor = conn.cursor()

    # Sample query to find the average salary

    query = "SELECT AVG(salary) FROM employees WHERE typeof(salary) != 'text'"
    cursor.execute(query)

    # fetchone() gets the single result from the average calculation
    result = cursor.fetchone()

    print(f"The average company salary is: ${result[0]:,.2f}")

    conn.close()

if __name__ == "__main__":
    run_anayltics()