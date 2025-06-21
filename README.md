# WebScraping


Project Structure
This project is composed of four core components:

1. Web Scraping
Uses Selenium to scrape historical data (stats, events, yearly summaries) from a public website. The scraper handles pagination, missing elements, and user-agent headers, saving results into CSV files for later use.

2. Database Import
Cleans and standardizes the scraped data, then imports it into a structured SQLite database. Column names are normalized and tables are clearly organized for querying and visualization.

3. Query CLI Tool
A command-line interface that lets users run custom SQL queries on the dataset. Supports filtering by year, stat type, events, and includes examples like joins between tables. Results are printed in a readable table format with error handling.

4. Streamlit Dashboard
A web-based interactive dashboard featuring multiple visualizations:

Stat Records by Year — reveals data coverage over time.

Top Players by Stat Count — ranks the most prominent players.

World Series Winners — a pie chart showing title distribution over selected years. Dropdowns and sliders let users filter the data on the fly.

Preview
attached screenshots


Web Scraping and Dashboard Project
1. Goal - automatically extract historical data from the Major League Baseball(MLB) History Website using Selenium, organize it into structured DataFrames, and save the cleaned data as CSV files.
1. Web Scraping Program
Goal: Scrape data from Major League Baseball History.
Steps:
Use Selenium to retrieve the data.
Extract relevant details (year, event names, statistics).
Save the raw data into CSV format for each dataset.
Handle challenges such as:
Pagination
Missing tags
User-agent headers for mimicking a browser request.

2. Database Import Program
Goal: Import the CSV files into a SQLite database.
Steps:
Create a program that imports each CSV as a separate table in the database.
Ensure proper data types (numeric, date, etc.) during the import.
Check for errors during the import process.

3. Database Query Program
Goal: Query the database via the command line.
Steps:
Allow users to run queries, including at least joins (e.g., combining player stats with event data).
Ensure the program can handle flexible querying, allowing for filtering by year, event, or player statistics.
Handle errors and display results appropriately.

4. Dashboard Program
Goal: Build an interactive dashboard using Streamlit or Dash.
Steps:
Display insights from the data using at least three visualizations.
Implement interactive features like:
Dropdowns to select years or event categories.
Sliders to adjust the data view.
Dynamically update the visualizations based on user input.
Deploy the dashboard on Render or Streamlit.io for public access.

Web Scraping
Uses Selenium to retrieve data from the web.
Handles common scraping challenges like missing tags, pagination, and user-agent headers.
Saves raw data as a CSV.
Avoids scraping duplication or redundant requests.
Data Cleaning & Transformation
Loads raw data into a Pandas DataFrame.
Cleans missing, duplicate, or malformed entries effectively.
Applies appropriate transformations, groupings, or filters.
Shows before/after stages of cleaning or reshaping.
Data Visualization
Includes at least three visualizations using Streamlit or Dash.
Visuals are relevant, well-labeled, and support the data story.
User interactions such as dropdowns or sliders are implemented.
Visualizations respond correctly to user input or filters.
Dashboard / App Functionality
Built with Streamlit or Dash to display data and insights.
Features clean layout and responsive components.
Allows users to explore different aspects of the data.
Provides clear titles, instructions, and descriptions for user guidance.
Code Quality & Documentation
Code is well-organized and split into logical sections or functions.
Inline comments or markdown cells explain major steps or choices.
All dependencies are listed and environment setup is reproducible.
Comments or markdown cells explain logic.
README.md includes summary, setup steps, and a screenshot.
