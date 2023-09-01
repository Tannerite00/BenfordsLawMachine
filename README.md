# BenfordsLawMachine

A simple python script that takes a CSV and applies Benford's Law to it, where in any financial data typically the number 1 appears approx. 30% of the time, with a sloping distribution down to 9 that should appear approx. 5% of the time. 

The basic theory is that when someone commits fraud, they do not do it in increments of $10, $20, $100, or $200, instead they do it in $80 or $900 increments. 

This script allows one to see the distribution of numbers in a file as well as displays their percentage of the overall amount of numbers counted. 
