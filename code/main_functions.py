import os
import pandas as pd
import requests
from playwright.sync_api import sync_playwright
from fractions import Fraction

#create variables to use for functions
NFL_TEAMS_URL = "https://www.nfl.com/teams/"
STATS_KEYS = [
    "TOTAL FIRST DOWNS", "THIRD DOWN CONVERSIONS", "FOURTH DOWN CONVERSIONS",
    "TOTAL OFFENSIVE YARDS", "TOTAL RUSHING YARDS", "TOTAL PASSING YARDS",
    "SACKS", "FIELD GOALS", "TOUCHDOWNS", "TURNOVER RATIO"
]
API_URL = "https://cent.ischool-iot.net/api/google/places/textsearch"
API_KEY = "7bd02b43bf977d8cfeb68449"
HEADERS = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}

def scrape_nfl_teams():
    '''
    Go to nfl teams url and scrape team names 
    '''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(NFL_TEAMS_URL)
        team_elements = page.query_selector_all(
            "h4.d3-o-media-object__roofline.nfl-c-custom-promo__headline > p"
        )
        teams = [team.inner_text().strip() for team in team_elements]
        browser.close()
        return teams


def scrape_team_stats(team, page):
    '''
    Loop through the list of teams buy formattign teams names and scrape stats from stat keys list.
    Create lsit of unwanted indices and filter out unwanted stats
    Use Fraction Function to convert stats to decimal if needed then rename those columns to include (%)
    '''
    url = f"https://www.nfl.com/teams/{team.lower().replace(' ', '-')}/stats"
    page.goto(url)
    stats_list = page.query_selector("ul.nfl-o-team-h2h-stats__list")
    list_items = stats_list.query_selector_all("li") if stats_list else []

    #filter out unwanted indices
    unwanted_indices = {1, 5, 7, 9, 13}  #indices of unwanted stats
    filtered_items = [item for i, item in enumerate(list_items) if i not in unwanted_indices]

    team_stats = {}
    for item in filtered_items:
        label = item.query_selector(".nfl-o-team-h2h-stats__label")
        value = item.query_selector(".nfl-o-team-h2h-stats__value")
        if label and value:
            key = label.inner_text().strip().upper()
            value_text = value.inner_text().strip()
            if '/' in value_text:
                decimal_value = float(Fraction(value_text))
                value_text = f"{decimal_value:.4f}"
                key = f"{key} (%)"
            if key in STATS_KEYS or key.endswith(" (%)"):
                team_stats[key] = value_text

    team_stats["team"] = team
    return team_stats


def get_stadium_coordinates(query):
    """
    Fetch latitude and longitude for a given query using the API.
    Falls back to using just the team name if the 'stadium' query fails.
    If no fallback is available, raises a ValueError.
    """
    params = {"query": query}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    #check if results are available
    if "results" in data and len(data["results"]) > 0:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        #create fallbaack query for failed searches with google api
        fallback_query = " ".join(query.split()[:-1])
        print(f"Retrying with fallback query: {fallback_query}")
        
        params["query"] = fallback_query
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            raise ValueError(f"No location found for query: {query} or fallback: {fallback_query}")

#main function to scrape all teams and stadiums
def scrape_all_teams_and_stadiums():
    '''
    main function to scrape all teams and stadiums
    use playwright to scrape team stats and google api to get stadium coordinates
    use enumerate to loop through teams and format team names
    '''
    teams = scrape_nfl_teams()
    formatted_teams = [team.lower().replace(" ", "-") for team in teams]
    stadium_names = [team + " Stadium" for team in teams]

    all_team_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, team in enumerate(teams):
            print(f"Scraping stats for {team}...")
            team_stats = scrape_team_stats(team, page)

            print(f"Fetching coordinates for {stadium_names[i]}...")
            latitude, longitude = get_stadium_coordinates(stadium_names[i])

            team_stats["latitude"] = latitude
            team_stats["longitude"] = longitude
            all_team_data.append(team_stats)

        browser.close()

    #save to cache folder
    os.makedirs("cache", exist_ok=True)
    output_path = os.path.join("cache", "nfl_team_stats.csv")
    df = pd.DataFrame(all_team_data)

    #manually add Detroit Lions coordinates due to issues with google api search
    detroit_index = df[df['team'] == "Detroit Lions"].index
    df.at[detroit_index[0], "latitude"] = 42.3407
    df.at[detroit_index[0], "longitude"] = -83.0456

    df.to_csv(output_path, index=False)

#main script to run all functions
if __name__ == "__main__":
    scrape_all_teams_and_stadiums()
