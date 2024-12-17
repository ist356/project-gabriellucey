# Reflection

Student Name:  Gabriel Lucey
Student Email:  gplucey@syr.edu

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`

I had some troubles with this project, but overall it was a great experience to work on web scraping and API skills. The first big issue I came across was trying to web scrape the correct stats for every NFL team. I had no trouble looping through and scraping each team, but I struggled with which specific statistics I wanted to pull from the NFL website. The NFL website lists every team’s stats with an <li> element for each statistic. Since every list element had the same class attribute, I had to create a list of unwanted indices for statistics I did not want in my data.

After this, I had trouble with the Google API call, which was used to gather information about the stadiums' locations. I found that searching just the team name would not always work, so I added the keyword "Stadium" into the query for every API call. This worked for every team except for one, so I made a fallback query in case the team name plus the keyword "Stadium" did not work. After this, I noticed that one NFL team had the wrong coordinates from the Google API, so I had to manually alter these coordinates in the dataframe at the end of main_functions.py.

Some new functions that I explored were, first, the Fraction function. The Fraction function allowed me to change the statistics where there was a string fraction into a float decimal percentage. This allowed me to have consistent and clean data for analysis. I also used a new function, enumerate, which allowed me to loop through lists and keep track of the index and the value. I used this to obtain the longitude and latitude of each stadium. Another new function I used was the AntPath function. This allowed me to create a path between two teams by providing the longitude and latitude for both teams. The last new function I used was MagicMock. I used MagicMock for my testing as it allowed me to simulate Playwright scraping to test my scraping function.