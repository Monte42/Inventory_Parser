# =======
# Imports
# =======
import os
import pandas as pd
import csv
import datetime




# =================
# Global Variables
# =================
# List of stores I need data from
store_list = [
    '1714',
    '2588',
    '2852',
    '4847',
    '4859',
    '4952',
    '6251',
    '6575',
    '6677',
    '6678',
    '6679'
]
# Todays date
date = datetime.datetime.now()
# Downloaded file from website in Downloads Folder
in_file = 'C:/Users/GDumond/Downloads/b.csv'

# Save as filename - *** UN-COMMENT the filename you want to use
    # File save as for current days locked in orders
out_file = f'C:/Users/GDumond/OneDrive - Penn Tank Lines/Documents/BENCHMARK/BB_{date.strftime("%m%d")}.csv'
    # File save as for tomorrows pending orders
# out_file = f'C:/Users/GDumond/OneDrive - Penn Tank Lines/Documents/BENCHMARK/New_{date.strftime("%m%d")}.csv'

# Read in_file, and it convert to a DataFrame
df = pd.read_csv(in_file)
# Array to store data to be written to out_file
parsed_data = []
# Number of loads for the working day
load_count = 1



# ==========
# Functions
# ==========
# takes in array and returns second value.  Will be used to sort data
def sort_array_by_second_element(arr):
    return arr[1]



# ============
# Run Program
# ============
# Collect desired data from DataFrame & store in parsed_data array
for i in range(len(df)): # iterate through each row of DataFrame
    if str(df['siteId'].loc[i]) in store_list: # check if current rows site is in store_list
        parsed_data.append(
            [ # create array of desired columns for current row (site) & add it to parsed_data
                df['orderId'].loc[i],
                df['startDeliveryTime'].loc[i],
                df['endDeliveryTime'].loc[i],
                df['siteId'].loc[i],
                df['materialId'].loc[i],
                df['quantityOrdered'].loc[i]
            ]
        )
# Sort parsed_data by each nested arrays second element (startDeliveryTime)
parsed_data.sort(key=sort_array_by_second_element)


# Convert each element of parsed_data from an array to a string
current_orderId = 0 # create a variable to store the current elements first value (order ID)
for i in range(len(parsed_data)): # iterate through parsed_data
    # Checks if current rows Order Id is equal to current_orderId or if current_orderId is equal to 0
    if current_orderId == parsed_data[i][0] or current_orderId == 0:
        #  places nested array values into a comma separated value string format into newRow variable - add new line at the end
        newRow = f'{parsed_data[i][0]},{parsed_data[i][1]},{parsed_data[i][2]},{parsed_data[i][3]},{parsed_data[i][4]},{parsed_data[i][5]}\n'
        # set current_orderId to equal this rows Order Id
        current_orderId = parsed_data[i][0]
    else: # if current_orderId is not 0 and this is a new Order Id #
        #  places nested array values into a comma separated value string format into newRow variable - add new line at the end and begining
        newRow = f'\n{parsed_data[i][0]},{parsed_data[i][1]},{parsed_data[i][2]},{parsed_data[i][3]},{parsed_data[i][4]},{parsed_data[i][5]}\n'
        # set current_orderId to equal this rows Order Id
        current_orderId = parsed_data[i][0]
        # As this is a new load not accounted for add 1 to load count
        load_count += 1
    # set current working index of parsed_data to equal newRow
    parsed_data[i] = newRow
# insert table head and total load count, done last so as not to loose in array sorting process
parsed_data.insert(0,f'Order ID, Retain, Run Out, Site ID, Product, Volume, ,Total Loads: {load_count}\n' )
# Creates and opens new file with out_file name and location and the ability to write to said file
with open(out_file, 'w') as file: # create temp local var (file) to store current working file
                                  #  Remember out_file is a string
    for row in parsed_data: # iterate through parsed_data, now an array of string with comma separated values
        # Writes row to the new file
        file.write(row)
# Delete the original downloaded file
os.remove(in_file)
