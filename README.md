# sqlalchemy-challenge
The hawaii-sqlite database is used to provide data on years-long temperature and precipitation measurements at various observation stations. The analysis is then graphed with a line graph to show precipitation over time.

The station analysis portion counts the number of stations, shows which station is the most active, and then runs a histogram of the frequency of temperature observations at that particular station.

The bonus section of the notebook file contains a converted DataFrame that takes the date and converts it to a datetime object. From there, I created two DataFrames to pull out all dates for the months of June and December to run T-Tests on that data.

In app.py, the created route has pages for precipitation, stations, observed temperatures, and two functionalities that take user input. The first tool is where a user can input a start date in YYYY-MM-DD format and the return is the min, max, and average temperature for all stations starting from that point to the end of the available data. The second tool takes in a start and end date in YYYY-MM-DD format to return min, max, and average temperature for all stations beginning with the input start date and ending with the input end date.