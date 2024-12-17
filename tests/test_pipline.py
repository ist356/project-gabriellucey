import pytest
import os
import sys
import pandas as pd
from unittest.mock import MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))

from code.main_functions import get_stadium_coordinates, scrape_team_stats, scrape_all_teams_and_stadiums

# Sample DataFrame
TEST_DF = pd.DataFrame({
    "team": ["Arizona Cardinals", "Atlanta Falcons"],
    "TOTAL FIRST DOWNS": [283, 269]
})
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
    
    # Expected columns and accounting for columns with percentages
    expected_columns = [
        "TOTAL FIRST DOWNS", "THIRD DOWN CONVERSIONS (%)", "FOURTH DOWN CONVERSIONS (%)",
        "TOTAL OFFENSIVE YARDS", "TOTAL RUSHING YARDS", "TOTAL PASSING YARDS",
        "SACKS", "FIELD GOALS (%)", "TOUCHDOWNS", "TURNOVER RATIO", "team", "latitude", "longitude"
    ]
    expected_num_columns = len(expected_columns)
    min_expected_rows = 32

    # Clean up columns with percentages
    percentage_columns = ["THIRD DOWN CONVERSIONS (%)", "FOURTH DOWN CONVERSIONS (%)", "FIELD GOALS (%)"]
    for col in percentage_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.rstrip('%').astype(float)  # Remove '%' and convert to float

    # Check the columns
    assert list(df.columns) == expected_columns, "CSV columns do not match expected structure."

    # Check the number of rows and columns
    print(f"We expect at least {min_expected_rows} rows and {expected_num_columns} columns.")
    assert df.shape[1] == expected_num_columns, "Column count mismatch."
    assert df.shape[0] >= min_expected_rows, "Not enough rows in the CSV."

    print("CSV structure and data validation passed!")

def test_get_stadium_coordinates():
    latitude, longitude = get_stadium_coordinates("Arizona Cardinals Stadium")
    assert isinstance(latitude, float) and isinstance(longitude, float), "Coordinates are not valid floats."


#use magic mock to mock the page object and its methods
def test_scrape_team_stats():
    mock_page = MagicMock()
    mock_stats_list = MagicMock()
    mock_list_items = [
        MagicMock(query_selector=MagicMock(side_effect=[MagicMock(inner_text=lambda: "TOTAL FIRST DOWNS"), 
                                                        MagicMock(inner_text=lambda: "283")]))
    ]
    
    mock_page.query_selector.return_value = mock_stats_list
    mock_stats_list.query_selector_all.return_value = mock_list_items

    stats = scrape_team_stats("Arizona Cardinals", mock_page)
    assert "TOTAL FIRST DOWNS" in stats
    assert stats["TOTAL FIRST DOWNS"] == "283"

