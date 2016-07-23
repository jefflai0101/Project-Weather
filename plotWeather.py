###########################################################################################################################
import os
import csv
import sys
import pandas
import numpy
import datetime
import requests
import matplotlib.pyplot as plt
###########################################################################################################################
#Assign folderPath to other modules
folderPath = os.path.dirname(os.path.abspath(__file__))
###########################################################################################################################
#Obtain Date values
today = str(datetime.date.today())
thisDay = int(today[8:])
thisMonth = int(today[5:7])
thisYear = int(today[0:4])
###########################################################################################################################
#Data heading
namesList = [
			'Month',
			'Day',
			'hPa',
			'Max Temp',
			'Mean Temp',
			'Min Temp', 'Mean Dew Point',
			'Relative Humidity(%)',
			'Mean Amount of Cloud(%)',
			'Total Rainfall (mm)',
			'Total Bright Sunshine (hours)',
			'Prevailing Wind Direction (Degrees)',
			'Mean Wind Speed (km/h)'
			]
###########################################################################################################################
#Obtaining data for the year from HKO
def checkWeather(year):

	with open(os.path.join(folderPath, 'Data', str(year) + '.csv'), 'w+', newline='', encoding='utf-8') as csvfile:
		csvwriter = csv.writer(csvfile)
		
		csvwriter.writerow(namesList)

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
#Call function to obtain data starting from 1884 to the year prior to current year
def obtainArchive():
	for i in range (1884, int(thisYear)):
		print ('Working on: ', str(i))
		checkWeather(str(i))

###########################################################################################################################
#Call function to obtain data of current year
def obtainCurrent():
	print ('Working on: ', str(thisYear))
	checkWeather(str(thisYear))

###########################################################################################################################
#Plotting data for all years with available data
def plotWeather():

	dirpath = []
	subDir = []
	filenames  = []
	minYear = thisYear
	maxYear = thisYear
	x = []
	y = []

	#Determine the year ranges
	for dirpath, subDir, filenames in os.walk(os.path.join(folderPath, 'Data')):
		for f in filenames:
			if (f != '.DS_Store'):
				fYear = int(f.split('/')[-1].split('.')[0])
				if (minYear > fYear): minYear = fYear

	#Read in data between min and max year range
	for i in range (minYear, maxYear):
		listData = pandas.read_csv(os.path.join(folderPath, 'Data', str(i) + '.csv'), header=0, names=namesList)
		#Calculate average temperature with available data
		try:
			if (len(listData['Mean Temp']) != 0):
				tAverage = numpy.mean((listData[listData['Month'] == 7]['Max Temp']))
				#tAverage = numpy.mean(listData['Mean Temp'])
				#X-axis takes years with record, Y-axis takes the average temperature for the correspondent year
				y.append(tAverage)
				x.append(i)
		except TypeError:
			pass

#	plt.title('Average Temperature of Hong Kong\n(1884 - 2015)')
#	plt.plot(x, y)
#	plt.plot(x, numpy.poly1d(numpy.polyfit(x, y, 1))(x))
#	plt.show()

	#Merging data into DataFrame
	plotData = pandas.DataFrame({'Year':x, 'Temp':y})
	#plot chars
	plotData.plot(x='Year', y='Temp')
	x = plotData['Year']
	y = plotData['Temp']
	#Set chart title
	plt.title('Average Temperature of Hong Kong\n(1884 - 2015)')
	#line of best-fit
	plt.plot(x, numpy.poly1d(numpy.polyfit(x, y, 1))(x))
	plt.show()

	#Gives formula
	#print (numpy.poly1d(numpy.polyfit(x, y, 1)))
	#Projection for 2020 mean temperature
	#print (numpy.poly1d(numpy.polyfit(x, y, 1))(2020))

###########################################################################################################################
#Calling different functions according to mode
def main():
	aMode = False
	cMode = False
	pMode = False
	for mode in sys.argv[1:]:
		if ((mode.lower() == 'a' or mode.lower() == 'archive') and aMode == False):
			obtainArchive()
			aMode = True
		if ((mode.lower() == 'c' or mode.lower() == 'current') and cMode == False):
			obtainCurrent()
			cMode = True
		if ((mode.lower() == 'p' or mode.lower() == 'plot') and pMode == False):
			plotWeather()
			pMode = True

###########################################################################################################################
main()

###########################################################################################################################