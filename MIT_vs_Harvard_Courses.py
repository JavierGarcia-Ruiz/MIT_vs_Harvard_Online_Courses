""" Project_name: Analysis of the differences in the data between MIT and Harvard online courses """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
import openpyxl

# 1.Previsualization of the dataset:

MIT_Harvard = pd.read_csv("appendix.csv")
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

desired_width = 900  # setting up the width of the run tool window for better visualization of the data
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)

print(MIT_Harvard.head(10))
print('\n')
print(MIT_Harvard.describe().round(2))
print('\n')


# 2.Segmentation of the data:

Inst_frec_table = MIT_Harvard["Institution"].value_counts()
MIT = MIT_Harvard[MIT_Harvard["Institution"] == "MITx"].copy()
Harvard = MIT_Harvard[MIT_Harvard["Institution"] == "HarvardX"].copy()

print(Inst_frec_table)
print('\n', MIT.head(), '\n', Harvard.head())

# 3.1.1.Which course has more participants?

MIT_participants = MIT["Participants (Course Content Accessed)"].sum()
Harvard_participants = Harvard["Participants (Course Content Accessed)"].sum()

print('\n')
print("MIT total of participants:", MIT_participants)
print("Harvard total of participants:", Harvard_participants)
print("Difference between the MIT over Harvard:", MIT_participants - Harvard_participants)

'''As we can see, the institution who has more number of participants is the MIT with a difference of 247615 
participants over Harvard, between the years 2012 and 2016. We can continue asking if this difference still
when we apply more granularity over the range of years.'''

MIT["Launch Year"] = MIT["Launch Date"].str[-4:]  # Splitting the year from the 'Launch date'
Harvard["Launch Year"] = Harvard["Launch Date"].str[-4:]

# MIT:

MIT_Total_Participants_per_year = {}
for year in MIT["Launch Year"].unique():
    aggregation = MIT[MIT["Launch Year"] == year]
    participants_agg = aggregation["Participants (Course Content Accessed)"].sum()
    MIT_Total_Participants_per_year[year] = participants_agg

print('\n')
print("The total of the participants in the MIT courses per year: ", MIT_Total_Participants_per_year)

# Harvard:

Harvard_Total_Participants_per_year = {}
for year in Harvard["Launch Year"]:
    aggregation = Harvard[Harvard["Launch Year"] == year]
    participants_agg = aggregation["Participants (Course Content Accessed)"].sum()
    Harvard_Total_Participants_per_year[year] = participants_agg

print("The total of the participants in Harvard courses per year: ", Harvard_Total_Participants_per_year)

# Difference MIT - Harvard per year: Using dictionary comprehension + keys().

difference = {key: MIT_Total_Participants_per_year[key] - Harvard_Total_Participants_per_year.get(key, 0)
              for key in MIT_Total_Participants_per_year.keys()}

print("The difference is : ", difference)


'''MIT has more participants in the years 2013, 2015 and 2016, but on the other hand, Harvard has more participants
in the years 2012 and 2014.'''

# 3.1.2.How many of that participants finished the courses (Has a certified) in percentage?
# MIT percentage of people who finished their courses:

MIT_Certified_per_year = {}
for year in MIT["Launch Year"].unique():
    aggregation = MIT[MIT["Launch Year"] == year]
    certified_agg = aggregation["Certified"].sum()
    MIT_Certified_per_year[year] = certified_agg

MIT_percentage_certified = {key: round((MIT_Certified_per_year[key] / MIT_Total_Participants_per_year.get(key, 0)) * 100, 2)
                            for key in MIT_Certified_per_year.keys()}
print('\n')
print("Number of certified participants per year in the MIT Courses: ", MIT_Certified_per_year)
print("Percentage of people who finished their courses in the MIT: ", MIT_percentage_certified)

# Harvard percentage of people who finished their courses:

Harvard_Certified_per_year = {}
for year in Harvard["Launch Year"].unique():
    aggregation = Harvard[Harvard["Launch Year"] == year]
    certified_agg = aggregation["Certified"].sum()
    Harvard_Certified_per_year[year] = certified_agg

Harvard_percentage_certified = {key: round((Harvard_Certified_per_year[key] / Harvard_Total_Participants_per_year.get(key, 0)) * 100, 2)
                                for key in Harvard_Certified_per_year.keys()}
print('\n')
print("Number of certified participants per year in the Harvard Courses: ", Harvard_Certified_per_year)
print("Percentage of people who finished their courses in Harvard: ", Harvard_percentage_certified)

# 4.EXPORTING TWO DATASETS TO AN EXCEL FILE:
writer = ExcelWriter('excel.xlsx')

MIT.to_excel(writer,'Sheet1')
Harvard.to_excel(writer, 'Sheet2')

writer.save()
