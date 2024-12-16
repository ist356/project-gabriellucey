import pytest
import os
import pandas as pd

# Path to the generated CSV file
FILE = "cache/nfl_team_stats.csv"

# Test 1: Simple test that always passes
def test_should_pass():
    print("\nThis test always passes!")
    assert True

# Test 2: Check if the CSV file is created
def test_nfl_team_stats_csv_exists():
    print(f"Expecting {FILE} to exist!")
    assert os.path.exists(FILE), f"File {FILE} does not exist."

# Test 3: Check the structure of the CSV file
def test_nfl_team_stats_csv_structure():
    print(f"Checking structure of {FILE}")
    df = pd.read_csv(FILE)
    
    # Expected number of rows and columns
    expected_columns = [
        "TOTAL FIRST DOWNS", "THIRD DOWN CONVERSIONS", "FOURTH DOWN CONVERSIONS",
        "TOTAL OFFENSIVE YARDS", "TOTAL RUSHING YARDS", "TOTAL PASSING YARDS",
        "SACKS", "FIELD GOALS", "TOUCHDOWNS", "TURNOVER RATIO", "team", "latitude", "longitude"
    ]
    expected_num_columns = len(expected_columns)
    min_expected_rows = 32 
    
    # Check the columns
    assert list(df.columns) == expected_columns, "CSV columns do not match expected structure."

    # Check the number of rows and columns
    print(f"We expect at least {min_expected_rows} rows and {expected_num_columns} columns.")
    assert df.shape[1] == expected_num_columns, "Column count mismatch."
    assert df.shape[0] >= min_expected_rows, "Not enough rows in the CSV."

    print("CSV structure and data validation passed!")
