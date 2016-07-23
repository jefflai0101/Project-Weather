###########################################################################################################################
import os
import csv
import sys
import datetime
import requests
###########################################################################################################################
#Assign folderPath to other modules
folderPath = os.path.dirname(os.path.abspath(__file__))
###########################################################################################################################
#Obtain Date values
today = str(datetime.date.today())
thisDay = today[8:]
thisMonth = today[5:7]
thisYear = today[0:4]
###########################################################################################################################
def checkWeather(year):

	with open(os.path.join(folderPath, 'Data', str(year) + '.csv'), 'w+', newline='', encoding='utf-8') as csvfile:
		csvwriter = csv.writer(csvfile)
		buff = ['Month', 'Day', 'hPa', 'Max Temp', 'Mean Temp', 'Min Temp', 'Mean Dew Point', 'Relative Humidity(%)', 'Mean Amount of Cloud(%)', 'Total Rainfall (mm)', 'Total Bright Sunshine (hours)', 'Prevailing Wind Direction (Degrees)', 'Mean Wind Speed (km/h)']
		csvwriter.writerow(buff)

		lastMonth = int(thisMonth) if (year == thisYear) else 12

		for i in range (0, lastMonth):
			#currentMonth = ('0' + str(lastMonth)) if ((i == int(thisMonth)-1) and (year == thisYear)) else ''
			#link = 'http://www.hko.gov.hk/cis/dailyExtract/dailyExtract_' + str(year) + currentMonth + '.xml'
			link = 'http://www.hko.gov.hk/cis/dailyExtract/dailyExtract_' + str(year) + '.xml'
			response = requests.get(link)
			response.raise_for_status() # raise exception if invalid response
			days = response.json()['stn']['data'][i]['dayData']
			days = days[:-2]
			
			for day in days:
				day.insert(0, i+1)
				csvwriter.writerow(day)

###########################################################################################################################
def obtainArchive():
	for i in range (1884, int(thisYear)):
		print ('Working on: ', str(i))
		checkWeather(str(i))

###########################################################################################################################
def obtainCurrent():
	print ('Working on: ', str(thisYear))
	checkWeather(str(thisYear))

###########################################################################################################################
def main()
	aMode = False
	cMode = False
	for mode in sys.argv[1:]:
		if ((mode.lower() == 'a' or mode.lower() == 'archive') and aMode == False):
			obtainArchive()
			aMode = True
		if ((mode.lower() == 'c' or mode.lower() == 'current') and cMode == False):
			obtainCurrent()
			cMode = True

###########################################################################################################################
main()

###########################################################################################################################