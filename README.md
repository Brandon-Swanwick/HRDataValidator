HR Data Validation & Analytics Pipeline
=======================================

This project implements a robust, configuration-driven ETL (Extract, Transform, Load) pipeline designed to process messy HR employee records. It validates incoming data against strict business rules, cleans common data-entry errors, and provides high-level analytics from a structured SQLite database.

🚀 Features
-----------

*   **Automated Data Cleaning**: Handles "human" data entry like "Seventy-K" or "$85,000" and converts them into standard floats.
    
*   **Strict Validation Engine**: Enforces rules for Employee IDs, Phone Numbers, Emails, and Salaries.
    
*   **Advanced Date Logic**: Distinguishes between formatting errors (e.g., 12/25/2024) and calendar logic errors (e.g., 2023-02-30).
    
*   **Multi-Format Audit Logs**: Generates detailed error reports in **CSV**, **JSON**, and **Parquet** for cross-departmental review.
    
*   **SQLite Integration**: Automatically populates a clean relational database for downstream analytics.
    
*   **Config-Driven**: Validation thresholds (min/max salary, date formats) are managed via config.json for easy updates without changing code.
    

🛠 Project Structure
--------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   .  ├── Source/  │   ├── validator.py       # Core validation and database logic  │   ├── query_data.py      # Analytics and reporting script  │   ├── employees.csv      # Source data (messy)  │   └── config.json        # Validation rules and thresholds  ├── hr_data.db             # Generated SQLite database (Ignored by Git)  ├── validation_errors.csv  # Audit report of failed records  └── README.md   `

🧪 Edge Case Handling
---------------------

The pipeline is hardened against several common data integrity issues:

Case

Input Example

Pipeline Action

**Salary Strings**

Seventy-K

Normalized to 70000.0

**Salary Bounds**

999999

Rejected (Exceeds $150k limit in config)

**Invalid Dates**

2023-02-30

Caught as "Non-existent calendar date"

**Date Format**

12/25/2023

Caught as "Format mismatch" (Expected YYYY-MM-DD)

**Phone Length**

12345

Rejected (Requires exactly 7 digits per config)

**Multiple Errors**

ID and Email bad

Row failed; both errors logged to the audit report

⚙️ Setup & Usage
----------------

### 1\. Requirements

Ensure you have Python 3.8+ and the following installed:

*   pandas and pyarrow (optional, for Parquet reports)
    

### 2\. Run the Validator

Processes employees.csv and populates the database.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python Source/validator.py   `

### 3\. Run Analytics

Generates a report on average salary, top earners, and average tenure.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python Source/query_data.py   `

📊 Sample Analytics Output
--------------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   The average company salary is: $92,730.78  The 1st earner is EMP0028 with a salary of $149,000.00  The Average Tenure of employees is: 4.08 years   `

📝 Configuration
----------------

Modify Source/config.json to update business rules:

*   Change salary\_rules to adjust pay scales.
    
*   Update date\_rules if the source file format changes.