HR Data Validation & Analytics Tool
===================================

A lightweight, configuration-driven Python utility designed to audit, clean, and analyze HR employee records. This tool identifies formatting errors, cleans messy data, saves validated records to a SQLite database, and provides automated financial insights.

Project Structure
-----------------

*   **Source/validator.py**: The core execution script that validates data and builds the clean database.
    
*   **Source/query\_data.py**: The analytics script that runs SQL calculations against the validated data.
    
*   **Source/config.json**: A JSON configuration file defining validation and salary rules.
    
*   **Source/employees.csv**: The input source file containing raw employee records.
    
*   **hr\_data.db**: The SQLite database containing all successfully validated records.
    
*   **validation\_errors.**: The output report listing all discovered inconsistencies.
    

Database Integration
--------------------

The tool now features an automated database pipeline. When validator.py is executed, it performs the following:

*   **Data Cleaning**: Converts textual salary representations (e.g., "Seventy-K") into numeric values.
    
*   **DB Persistence**: Successfully validated and cleaned records are automatically written to a table in hr\_data.db.
    
*   **Schema Management**: The script handles the creation of the employees table, ensuring the database is always ready for querying.
    

Querying and Calculations
-------------------------

Running Source/query\_data.py interacts directly with the SQLite database to provide high-level HR metrics without manual spreadsheet work:

*   **Average Salary**: Calculates the mean salary across all validated employees.
    
*   **Top Earners**: Identifies the highest-paid individuals currently in the database.
    
*   **Department Statistics**: Aggregates data to show salary distributions by team.
    
*   **Query Efficiency**: Uses optimized SQL queries to provide instant feedback on large datasets.
    

Setup and Usage
---------------

1.  **Configure Rules**: Open Source/config.json to define your specific data requirements.
    
2.  python Source/validator.py
    
3.  python Source/query\_data.py
    

Reviewing Results
-----------------

*   **Clean Data**: Open hr\_data.db using a SQLite browser to see records that passed all checks.
    
*   **Error Logs**: Review validation\_errors.csv to see why specific records were rejected.