# UofA-Course-Scraper
This script generates a csv of all classes in the U of A catalouge.
It is highly recommended that you take the current csv file and use it rather than generate a new one,as doing so will take about half an hour.
The intention of the script is to use input scraped data into a SQL server, however all data is in a single file,and needs to be refactored into multiple tables to cut down on redundancy.
If doing so is proving to be hassly for me, a new script will be made generating multiple csv files.

# HOW TO RUN:
To run the script, first install BeautifulSoup4 using the command `pip install beautifulsoup4`.
Run the script python script and let it run in the background for approximately half an hour.
The slow run time is intentional, as the script sleeps every 2 seconds after making a request.
This is to prevent the UofA servers from being spammed. Please do NOT shorten/remove these constraints. 
Doing so can hypothically lead to your IP being blocked.
