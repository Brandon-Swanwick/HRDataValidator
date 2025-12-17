import pytest
import sys
import os

# 1. This snippet ensures the 'source' folder is visible to the test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

# 2. Import the classes from your validator file
# (Assuming your file is named validator.py and contains these classes)
from validator import HRDataValidator, ErrorReporter

@pytest.fixture
def reporter():
    """Fixture to provide a clean reporter for every test."""
    return ErrorReporter('test_output')

@pytest.fixture
def validator(reporter):
    """Fixture to provide a validator instance with default settings."""
    # We pass an empty list and a dummy path to avoid loading real files
    return HRDataValidator([], reporter, 'non_existent_config.json')

def test_salary_low_bound(validator, reporter):
    """Verify that a salary below 30,000 triggers an error."""
    record = {"id": "EMP001", "salary": "25000"}
    
    # Act
    result = validator.validate_salary(0, record, record["salary"])
    
    # Assert
    assert result is False
    assert len(reporter.errors) == 1
    assert "out of bounds" in reporter.errors[0]['error_message']

def test_email_missing_at_symbol(validator, reporter):
    """Verify that an email without '@' triggers an error."""
    record = {"id": "EMP002", "email": "bademail.com"}
    
    result = validator.validate_email(0, record, record["email"])
    
    assert result is False
    assert "@" in reporter.errors[0]['error_message']