# Benfords Law

A simple python script that takes a CSV and applies Benford's Law to it, where in any financial data typically the leading number 1 appears approx. 30% of the time, with a sloping distribution down to 9 that should appear approx. 5% of the time. 

The basic theory is that when someone commits fraud, they do not do it in increments of $10, $20, $100, or $200, instead they do it in $80 or $900 increments. Therefor, if the higher numbers appear more often than the large number average distribution, there is a chance fraud is at play. 

This script allows one to browse their file explorer, choose a csv file, and then process it to see the distribution of numbers in a file as well as displays their percentage of the overall amount of numbers counted. 
A graph of the numbers is also created to help the user viusalize the distribution. 

# Gaussian Distribution

Gives a normal distribution based on the total spent on each Item by each Rep. If there is an abnormally large or small transaction it is made clearly visible for the user to see. WIP: Plots a normal distribution for each item group, with first and second std dev lines plotted to easily pick out outliers. 

Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item). 


# Transaction Analysis

A transctional analytics tool that takes 3 variables from a csv: Which Rep bought an item, what Item was bought, and the Total amount spent on an item. if a person bought the same item multiple times, the graph will sum them but also show a partition to display the different transactions. 
The graph is interactive, so specific items can be viewed together with others or on their own, and the graph can be zoomed in and out to see all parts of the data or just specific parts the user wants to focus on.

Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item). 

# Finding Duplicates

Finds duplicate transactions in the data based off of if the 3 columns chosen by the user match with any of the other data and prints them to a new csv. 

# Showing the CSV in the App

Renders the csv file chosen as an excel-like sheet in a seperate modal. 

