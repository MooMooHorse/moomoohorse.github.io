import datetime
import pytz

# set the timezone to CST
timezone = pytz.timezone('US/Central')

# get the current time in CST timezone
now = datetime.datetime.now(timezone)

# format the date and time as a string
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S %z')

# print the formatted date and time
print(formatted_date)