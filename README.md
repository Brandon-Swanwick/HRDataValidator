**HR Data Validation & Analytics Pipeline**
===========================================

This project implements a robust, configuration-driven ETL (Extract, Transform, Load) pipeline designed to process messy HR employee records. It validates incoming data against strict business rules, cleans common data-entry errors, and provides high-level analytics from a structured SQLite database.

**🚀 Features**
---------------

*   **Automated Data Cleaning**: Handles "human" data entry like "Seventy-K" or "$85,000" and converts them into standard floats.
    
*   **Strict Validation Engine**: Enforces rules for Employee IDs, Phone Numbers, Emails, and Salaries.
    
*   **Advanced Date Logic**: Distinguishes between formatting errors (e.g., 12/25/2024) and calendar logic errors (e.g., 2023-02-30).
    
*   **Multi-Format Audit Logs**: Generates detailed error reports in **CSV**, **JSON**, and **Parquet** for cross-departmental review.
    
*   **SQLite Integration**: Automatically populates a clean relational database for downstream analytics.
    
*   **Config-Driven**: Validation thresholds (min/max salary, date formats) are managed via config.json for easy updates without changing code.
    

## 🛠 Project Structure

```text
.
├── Source/
│   ├── validator.py            # Core validation and database logic
│   ├── query_data.py           # Analytics and reporting script
│   ├── employees.csv           # Source data (messy)
│   ├── config.json             # Validation rules and thresholds
│   ├── hr_data.db              # Generated SQLite database (Ignored by Git)
│   ├── validation_errors.csv   # Audit report of failed records
└── README.md                   # Project documentation
```

**🧪 Edge Case Handling**
-------------------------

The pipeline is hardened against several common data integrity issues:

| Case | Input Example | Pipeline Action |

| Salary Strings | Seventy-K | Normalized to 70000.0 |

| Salary Bounds | 999999 | Rejected (Exceeds $150k limit in config) |

| Invalid Dates | 2023-02-30 | Caught as "Non-existent calendar date" |

| Date Format | 12/25/2023 | Caught as "Format mismatch" (Expected YYYY-MM-DD) |

| Phone Length | 12345 | Rejected (Requires exactly 7 digits per config) |

| Multiple Errors | ID and Email bad | Row failed; both errors logged to the audit report |

**⚙️ Setup & Usage**
--------------------

### **1\. Requirements**

Ensure you have Python 3.8+ and the following installed:

*   pandas and pyarrow (optional, for Parquet reports)
    

### **2\. Run the Validator**

Processes employees.csv and populates the database.

python Source/validator.py

### **3\. Run Analytics**

Generates a report on average salary, top earners, and average tenure.

python Source/query\_data.py

**📊 Sample Analytics Output**
------------------------------

*   The Average company salary is: $92,730.78
*   The 1st earner is EMP0028 with a salary of $149,000.00
*   The Average Tenure of employees is: 4.08 years

**📝 Configuration**
--------------------

Modify Source/config.json to update business rules:

*   Change salary\_rules to adjust pay scales.
    
*   Update date\_rules if the source file format changes.

*   Change id\_rules if the id length format changes

*   Change phone\_rules if the phone length changes

**⚙️ Program Flow For Validator**
------------------------------

It's a classic **ETL (Extract, Transform, Load)** pattern. Here is the play-by-play of what happens from the moment you hit "Enter" until the clean data hits your database.

### Phase 1: The Initialization (The "Setup")

1. **Loading the Blueprint:** The `HRDataValidator` starts by reading your `config.json`. It updates its internal `self.rules` dictionary so it knows exactly what the "salary cap" is and what "date format" to look for.
2. **Database Provisioning:** It runs `_init_db()`. This is a "destructive" setup; it drops the old table and creates a fresh one with the correct schema (`id`, `salary`, `hire_date`, etc.).
3. **The Reporter:** It hooks into the `ErrorReporter` class, which initializes empty lists to catch any "bad" records.

### Phase 2: The Extraction (The "E")

4. **Reading the CSV:** `load_csv()` opens the file and turns every row into a Python **Dictionary**. At this stage, everything—including the salary—is just a string (e.g., `"$80,000"`).

### Phase 3: The Validation & Transformation (The "T")

This is the "Brain" of the script. For every single row in your CSV:

5. **The Gauntlet:** The script runs a list of checks (`validate_id`, `validate_salary`, `validate_hire_date`, etc.).
* **Transformation (Salary):** In `validate_salary`, it doesn't just check the value; it **cleans** it. It strips the `$`, removes the commas, and handles the "K" notation (like `Seventy-K`). If it passes, it **overwrites** the messy string in the record with a clean float.
* **Logic Check (Date):** It tries to force the date string into a `datetime` object. If `datetime.strptime` screams (because the format is wrong or it's Feb 30th), the script catches that error and asks the `ErrorReporter` to write down exactly what went wrong.



### Phase 4: The Decision (The "Gatekeeper")

6. **The `all(results)` check:**
* **IF ALL PASS:** If every function returned `True`, the row is considered "Clean."
* **IF ANY FAIL:** The row is flagged. It is **not** sent to the database. Instead, the `failed_row_count` goes up by one.



### Phase 5: The Loading (The "L")

7. **Database Insertion:** Only the "Clean" records are sent to `save_clean_record()`. It executes an `INSERT` statement into `hr_data.db`. Because we cleaned the data in Phase 3, the database gets a perfect number (e.g., `80000.0`) instead of `$80,000`.

### Phase 6: The Audit (The "Post-Mortem")

8. **Reporting:** Once the loop finishes, the `ErrorReporter` takes all those collected errors and writes them out to three different files (CSV, JSON, Parquet).
9. **Summary:** The script prints the final tally to your console so you can see at a glance if the "CEO salary" or the "Feb 30th" date actually got caught.

**In short:** It extracts messy strings  scrubs them into clean numbers/dates  saves the winners to the DB  logs the losers to the reports.