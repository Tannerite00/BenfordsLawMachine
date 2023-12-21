# Benfords Law

A simple python script that takes a CSV and applies Benford's Law to it, where in any financial data typically the leading number 1 appears approx. 30% of the time, with a sloping distribution down to 9 that should appear approx. 5% of the time. 

The basic theory is that when someone commits fraud, they do not do it in increments of $10, $20, $100, or $200, instead they do it in $80 or $900 increments. Therefor, if the higher numbers appear more often than the large number average distribution, there is a chance fraud is at play. 

This script allows one to browse their file explorer, choose a csv file, and then process it to see the distribution of numbers in a file as well as displays their percentage of the overall amount of numbers counted. 
A graph of the numbers is also created to help the user viusalize the distribution. 

# Gaussian Distribution

Gives a normal distribution based on the total spent on each Item by each Rep. If there is an abnormally large or small transaction it is made clearly visible for the user to see. WIP: Plots a normal distribution for each item group, with first and second std dev lines plotted to easily pick out outliers. 

Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item). 

Click the checkbox to exclude all negative values to see how bthe distribution may change. 

# Transaction Analysis

A transctional analytics tool that takes 3 variables from a csv: Which Rep bought an item, what Item was bought, and the Total amount spent on an item. if a person bought the same item multiple times, the graph will sum them but also show a partition to display the different transactions. 
The graph is interactive, so specific items can be viewed together with others or on their own, and the graph can be zoomed in and out to see all parts of the data or just specific parts the user wants to focus on.

Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item). 

# Finding Duplicates

Finds duplicate transactions in the data based off of if the 3 columns chosen by the user match with any of the other data, renders it in an excel-like grid in a separate modal and saves them to a new csv. 

# Showing the CSV in the App

Renders the csv file chosen as an excel-like sheet in a separate modal. 

# Info
This brings up a separate modal that contains most of this read me to explain what the various techniques are doing and to give more in-depth instructions. 

# Field Statistics 
Automatic stats that run when the file is selected such as: number of records, largest value, smallest value, 
Coming soon: largest negative value, number of valid values, earliest/latest dates, and more!

# Training Data
Added ability to add the selected csv file to a training data csv to have historical records to check analysis against in the future. Currently limited to the max size of an excel sheet (1 million x 1 million). 
Coming soon: ability to add/exclude specific columns and headers

# Other Features
This program is able to handle Advanced Record Definition Editor, AS400, dBASE, M. Access, M. Excel, ODBC, Print Report and Adobe PDF, SAP/AIS, Text, and XML documents as long as they are in table format.

# What Are We Playing With In The Sandbox?

Trying to create a modal that allows us to make our own audit templates and store them as JSON files. Add and Delete steps in the audit template and save it. can also load existing ones! 

Currently trying to get the save function to work! 





