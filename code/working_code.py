from playwright.sync_api import sync_playwright
import streamlit as st

def scrape_nfl_teams():
    url = "https://www.nfl.com/teams/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Select all team names based on their class
        team_elements = page.query_selector_all(
            "h4.d3-o-media-object__roofline.nfl-c-custom-promo__headline > p"
        )
        team_names = [team.inner_text().strip() for team in team_elements]

        browser.close()

        return team_names

# Fetch the team names
teams = scrape_nfl_teams()
print(teams)


formatted_teams = [team.lower().replace(" ", "-") for team in teams]
print(formatted_teams)