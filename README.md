# BenfordsLawMachine

A simple python script that takes a CSV and applies Benford's Law to it, where in any financial data typically the number 1 appears approx. 30% of the time, with a sloping distribution down to 9 that should appear approx. 5% of the time. 

The basic theory is that when someone commits fraud, they do not do it in increments of $10, $20, $100, or $200, instead they do it in $80 or $900 increments. 

This script allows one to browse their file explorer, choose a csv file, and then process it to see the distribution of numbers in a file as well as displays their percentage of the overall amount of numbers counted. 
A graph of the numbers is also created to help the user viusalize the distribution. 

# Transaction Analysis

A simple transctional analytics tool that takes 3 variables from a csv: Which Rep bought an item, what Item was bought, and the Total amount spent on an item. if a person bought the same item multiple times, it sums them under the individual's name. 
Then a graph is shown for each different item in the csv file, with a histogram depicting how much was spent and by whome. 
