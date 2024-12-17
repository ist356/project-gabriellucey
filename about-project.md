# About My Project

Student Name:  Gabriel Lucey
Student Email:  gplucey@syr.edu

### What it does
This project is a user interface that allows users to choose two separate NFL teams from two dropdown bars. Once the two teams are selected, you can click a "generate stats" button to view how the two teams compare based on a statistic—Touchdowns, Sacks, etc. This statistic can be changed to another statistic from a dropdown below the first button. Once everything is selected, a bar chart will appear showing how the two teams compare. It will also show the NFL average for the stat as well as the NFL-leading team for the stat. Below the bar chart, a map of the two teams' stadiums will appear with a line drawn between them to emphasize their length.

This project uses web scraping to obtain the names and statistics for NFL teams and uses the Google Text Search API to find the team stadium location.
This project also uses Streamlit with Plotly Express and Folium for visualizations.
### How you run my project

1. Feel free to pip install the requirements.txt.

2. Run the main_functions.py file. This will do all the web scraping and API calls that are needed to create the CSV. This may take a minute or two as there is a lot of scraping. You will know it is done once the terminal no longer shows any teams being scraped.

3. Run the tests with test_pipeline.py to check that the CSV is ready for Streamlit and that the functions performed correctly.

4. Run user_interface.py with Streamlit. From here, you can mess around and explore different statistics with different NFL teams.
***Note**: At first, the markers on the map may not display with the correct icon, but they seemed to load in correctly for me after a minute or two.

### Other things you need to know

1. I would like to acknowledge the use of AI for this project. GitHub Copilot and ChatGPT were used to help write code and explain concepts. All new concepts that AI taught me were understood and will be covered in the reflection.

2. I would like to acknowledge that I manually entered the coordinates for one NFL stadium at the bottom of main_functions.py. For some reason, the Google API was getting coordinates for a different stadium, so the fallback would not work. This will also be covered in the reflection.