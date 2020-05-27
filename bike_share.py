#Udacity Project 2: Bike Share Data Analysis
#Author: Jon Niskanen
#Date: 4/30/2020
import pandas as pd
import csv
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
import datetime
from datetime import datetime
import statistics
from statistics import mode
import os
import time
import numpy as np
import random

def most_common_time(List, time_unit): 
	date_list = pd.to_datetime(List)#convert series to dateimes
	if(time_unit == 'month'):
		return(mode(date_list.dt.month))#return mode of month
	elif(time_unit == 'day'): 
		return(mode(date_list.dt.dayofweek))#return mode of DOW
	elif(time_unit == 'hour'):
		return(mode(date_list.dt.hour))#return mode of hour
	else:
		print('invalid time unit error in most most_common_time function')#error catch
		return 1
#function to find the most common station in a given list
def most_common_station(List):
	station_list = List
	return(mode(station_list))

def most_common_route(start, end):
	route = list(zip(start, end))
	return(mode(route))

chicago_df = pd.read_csv('chicago.csv') #loading data frame for chicago
newyork_df = pd.read_csv('new_york_city.csv') #loading data frame for NYC
washington_df = pd.read_csv('washington.csv') #loading data frame for washington

chicago_df.columns = ['Index','Start Time', 'End Time', 'Trip Duration', 
'Start Station', 'End Station', 'User Type','Gender','Birth Year'] #loading column names for chicago
newyork_df.columns = ['Index','Start Time', 'End Time', 'Trip Duration', 
'Start Station', 'End Station', 'User Type','Gender','Birth Year'] #loading column names for NYC
washington_df.columns = ['Index','Start Time', 'End Time', 'Trip Duration', 
'Start Station','End Station','User Type'] #loading column names for washington

week_days = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') #defining week days
months = ('January', 'February', 'March','April','May','June','July','August','September','October','November','December') #defining months
clock = {0: '12:00AM', 1: '1:00AM', 2:'2:00AM', 3:'3:00AM', 4:'4:00AM', 5:'5:00AM', 6:'6:00AM', 7:'7:00AM', 8:'8:00AM', 9:'9:00AM', 10:'10:00AM',
11: '11:00AM', 12: '12:00PM', 13:'1:00PM', 14:'2:00PM', 15:'3:00PM', 16:'4:00PM', 17:'5:00PM', 18:'6:00PM', 19:'7:00PM', 20:'8:00PM', 21:'9:00PM',
22:'10:00PM', 23:'11:00PM', 24:'12:00AM'
}#defining dicitonary for times

term_loop = True #keep program running while true variable
while(term_loop):
	print('Welcome to the bike share data analysis project!')
	input_flag = True#first loop gets the location the user would like to investigate and combines data if needed
	while(input_flag):
		city = input('What city would you like to investigate?(Washington, New York, Chicago, All Data):\n:')
		if (city == 'Washington'):
			city_df = washington_df
			input_flag = False
		elif(city == 'New York'):
			city_df = newyork_df
			input_flag = False
		elif(city == 'Chicago'):
			city_df = chicago_df
			input_flag = False
		elif (city =='All Data'):
			city_df = pd.concat([washington_df,newyork_df,chicago_df])#comnbine all data
			input_flag = False
		else: 
			print("Your input did not match one of the listed cities, try again\n")
			input_flag = True
	input_flag = True #second loop identifies the type of data the user would like to see
	while(input_flag):
		print("\nWhat data would you like to retrieve?")
		data_group = input('1:Popular travel times\n2:Popular stations and routes\n3:Trip duration\n4:User info\n5:Raw data\n:')
		if(data_group == '1'):
			t1 = time.time()
			os.system('clear')
			date_list = city_df['Start Time']
			print('Retrieving popular travel time data for',city,':')
			print('Most common month:',months[most_common_time(date_list,'month')])#return month indexed by output of most_common function
			print('Most common day of week:',week_days[most_common_time(date_list,'day')])#return day indexed by output of most_common function
			print('Most common hour:',clock[most_common_time(date_list,'hour')])#return time indexed by output of most_common function
			t2 = time.time()	
			print('Calculation time:',t2-t1)		
			input_flag = False
		elif(data_group == '2'):
			t1 = time.time()
			os.system('clear')
			station_start = city_df['Start Station']
			station_end = city_df['End Station']
			print('Retrieving popular station data for',city,':')
			print('Most popular start station:',most_common_station(station_start))
			print('Most popular end station:',most_common_station(station_end))
			route = most_common_route(station_start,station_end)
			print('Most popular route:', route[0], 'to', route[1])
			t2 = time.time()
			print('Calculation time:',t2-t1)
			input_flag = False
		elif(data_group == '3'):
			t1 = time.time()
			os.system('clear')
			total_time = round((city_df['Trip Duration'].sum())/(60*60),2)
			avg_time = round((city_df['Trip Duration'].mean())/(60),2)
			print('Retrieving trip duration data for',city,':')
			print('Total travel time:',total_time, 'hours')
			print('Average travel time:',avg_time, 'minutes')
			t2 = time.time()
			print('Calculation time:',t2-t1)
			input_flag = False
		elif(data_group == '4'):
			t1 = time.time()
			os.system('clear')
			print('Retrieving user data for',city,':')
			user_count = city_df['User Type'].value_counts()
			print('Number of Subscriber trips:',user_count[0])
			print('Number of Customer trips:',user_count[1])			
			if(city in ['New York','Chicago','All Data']):#ignore washington in this analysis
				gender_count = city_df['Gender'].value_counts()#get gender instance counts
				birth_list = city_df['Birth Year'].dropna()#remove na from series
				birth_list = birth_list.astype(int)#convert to int, mode run about 4x faster on int than float
				print('Number of males:', gender_count[0])
				print('Number of females:',gender_count[1])
				print('Oldest user birth year:',int(city_df['Birth Year'].min()))
				print('Youngest user birth year:', int(city_df['Birth Year'].max()))
				print('Most common birth year:', mode(birth_list))
			input_flag = False
			t2 = time.time()
			print('Calculation time:',t2-t1)
		elif(data_group == '5'):
			input_flag_2 = True
			while(input_flag_2):
				interval= input('How many lines of raw data would you like retrieved?\n:')
				interval = int(interval) #turn string into int
				if(interval <= (len(city_df)-1)):
					input_flag_2 = False
				else:
					print('lines requested is too large or wrong format, try again')
					input_flag_2 = True
			raw_data = True
			print('Retrieving raw data for',city)	
			print('*Maximize terminal window for column readability*')	
			pd.set_option('display.max_rows', None)
			pd.set_option('display.max_columns', None)
			pd.set_option('display.width', None)
			row_count = 0
			print(row_count, len(city_df)-1)
			while(raw_data):
				if((row_count+interval) < (len(city_df)-1)):
					print(city_df[row_count:(row_count+interval)])
					row_count += interval
				elif((row_count+interval) == (len(city_df)-1)):
					print(city_df[row_count:(row_count+interval)])
					row_count = 0
					print('End of data...')
				elif((row_count+interval) > (len(city_df)-1)):
					last_interval = interval -((row_count+interval)-len(city_df)-1)
					print(row_count, last_interval)
					print(city_df[row_count:(row_count+last_interval)])
					row_count = 0
					print('End of data...')
				input_flag_2 = True
				while(input_flag_2):
					print('Would you like to view', interval,'more rows?',end = '')
					more_raw = input('(y/n)\n:')
					if(more_raw == 'y'):
						raw_data = True
						input_flag_2 = False
					elif(more_raw == 'n'):
						raw_data = False
						input_flag_2 = False
					else:
						print('input did not match, try again.')
						input_flag_2 = True
			input_flag = False
		else:
			print("Your input did not match one of the data codes (1, 2, 3 or 4) try again\n")
			input_flag = True
	input_flag = True #after running ask the user to run again
	while(input_flag):
		repeat_loop = input("\nWould you like to retrieve more data(y/n)?\n:")	
		if(repeat_loop == 'y'):
			os.system('clear')
			term_loop = True
			input_flag = False
		elif(repeat_loop == 'n'):
			print("Goodbye...")
			term_loop = False
			input_flag = False
		else:
			print('Input was not recognized, try again.')
			input_flag = True