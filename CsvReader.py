import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm
import wx
import wx.grid 
import pandas as pd
import plotly.express as px
import re

# Initialize a dictionary to count digits from 1 to 9
digit_counts = {str(i): 0 for i in range(1, 10)}

# Initialize a variable to count the total number of digits
total_digit_count = 0
# Create the main application window
root = tk.Tk()
root.title("CSV File Processor")

# Initialize Tkinter variables for selected column names as globals
var_col1 = tk.StringVar()
var_col2 = tk.StringVar()
var_col3 = tk.StringVar()

# Function to handle the file selection
def browse_file():
    global var_col1, var_col2, var_col3  # Declare them as global
    file_path = filedialog.askopenfilename(filetypes=[
        ("CSV Files", "*.csv"),
        ("Advanced Record Definition Editor Files", "*.are"),
        ("AS400 Files", "*.as400"),
        ("dBASE Files", "*.dbf"),
        ("Microsoft Access Files", "*.mdb *.accdb"),
        ("Microsoft Excel Files", "*.xls *.xlsx"),
        ("ODBC Files", "*.odbc"),
        ("Print Report Files", "*.pr"),
        ("Adobe PDF Files", "*.pdf"),
        ("SAP/AIS Files", "*.sap"),
        ("Text Files", "*.txt"),
        ("XML Files", "*.xml"),
    ])
    
    if file_path:
        entry_file_path.delete(0, tk.END)  # Clear the entry field
        entry_file_path.insert(0, file_path)  # Set the selected file path

        # Get the list of columns based on the file type
        if file_path.endswith((".csv", ".txt", ".xml")):
            with open(file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                header = next(csvreader)  # Read the header row
                column_names = header  # Get column names from the header row
        
        # Call a function to handle the retrieved column names
        handle_column_names(column_names)


# Function to create dropdown menus for column names
def handle_column_names(column_names):
    global var_col1, var_col2, var_col3  # Access the global variables

    # Create dropdown menus for each column
    dropdown_menu1 = tk.OptionMenu(root, var_col1, *column_names)
    dropdown_menu2 = tk.OptionMenu(root, var_col2, *column_names)
    dropdown_menu3 = tk.OptionMenu(root, var_col3, *column_names)

    # Label each dropdown menu
    label_menu1 = tk.Label(root, text="Account Description:")
    label_menu2 = tk.Label(root, text="Transaction Description:")
    label_menu3 = tk.Label(root, text="Transactions:")
    label_column_instructions1 = tk.Label(root, text="Select 3 columns to run analysis on. The first column is the category you want the data separated by.")
    label_column_instructions2 = tk.Label(root, text="The second is who/what bought the item/service and the last should be the transactions")

    # Grid layout for labels and dropdown menus
    label_column_instructions1.grid(row=7, column=0, columnspan=2, pady=1)
    label_column_instructions2.grid(row=8, column=0, columnspan=2, pady=1)
    label_menu1.grid(row=9, column=0, padx=1, pady=5)
    dropdown_menu1.grid(row=9, column=1, padx=1, pady=5)
    label_menu2.grid(row=10, column=0, padx=1, pady=5)
    dropdown_menu2.grid(row=10, column=1, padx=1, pady=5)
    label_menu3.grid(row=11, column=0, padx=1, pady=5)
    dropdown_menu3.grid(row=11, column=1, padx=1, pady=5)


# Define a function to clean and convert 'Total' values to float
def clean_and_convert_total(total_str_or_float):
    if isinstance(total_str_or_float, str):
        total_str = total_str_or_float.replace('$', '').replace(',', '').strip()
        # Handle negative numbers enclosed in parentheses
        if total_str.startswith('(') and total_str.endswith(')'):
            total_str = '-' + total_str[1:-1]
        try:
            return float(total_str)
        except ValueError:
            return np.nan
    elif isinstance(total_str_or_float, float):
        # If it's already a float, return it as is
        return total_str_or_float
    else:
        # If it's neither a string nor a float, return NaN
        return np.nan

def process_gaussian_distribution(csv_file_path, col1, col3):
    try:
        # Load transaction data from the selected CSV file
        data = pd.read_csv(csv_file_path)
        col1 = var_col1.get()
        col3 = var_col3.get()

        # Clean and convert the entire col3 column to float
        data[col3] = data[col3].apply(clean_and_convert_total)

        # Group transactions by 'Item'
        grouped_data = data.groupby([col1])
        
        # Plot Gaussian distributions for each selected column
        for i, group_data in grouped_data:
            # Fit a normal distribution to the data for the current column
            mu, std = norm.fit(group_data[col3])

            # Create a histogram
            plt.figure(figsize=(10, 6))
            plt.hist(group_data[col3], bins=30, density=True, alpha=0.6, color='blue')

            # Create a range of values for the x-axis based on the normal distribution
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mu, std)

            # Plot the fitted normal distribution
            plt.plot(x, p, 'k', linewidth=2)
            title = f"Fit results for {i}: mu = {mu:.2f}, std = {std:.2f}"
            plt.title(title)

            plt.xlabel('Dollars Spent (Total)')
            plt.ylabel('')

            # Calculate and plot the first standard deviation lines
            std1_left = mu - std
            std1_right = mu + std
            plt.axvline(x=std1_left, color='k', linestyle='--', label='1st std dev', linewidth=2)
            plt.axvline(x=std1_right, color='k', linestyle='--', linewidth=2)

            # Calculate and plot the second standard deviation lines
            std2_left = mu - 2 * std
            std2_right = mu + 2 * std
            plt.axvline(x=std2_left, color='r', linestyle='--', label='2nd std dev', linewidth=2)
            plt.axvline(x=std2_right, color='r', linestyle='--', linewidth=2)

            # Force y-axis ticks to display whole numbers
            yint = range(min([int(val) for val in plt.yticks()[0]]), max([int(val) for val in plt.yticks()[0]]) + 1)
            plt.yticks(yint)
            plt.show()
    except ValueError as e:
        print(f"Error processing data for item {i}: {e}")
            
    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

# Function to process the selected CSV file and run Benford's Law analysis
def process_benfords_law():
    global total_digit_count  # Declare total_digit_count as a global variable
    global digit_counts  # Declare digit_counts as a global variable

    try:
        csv_file_path = entry_file_path.get()
        if csv_file_path:
            # Clear the previous counts
            digit_counts = {str(i): 0 for i in range(1, 10)}
            total_digit_count = 0

            # Open the CSV file and read its contents
            with open(csv_file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    # Join the elements in each row to form a single string
                    row_str = ''.join(row)

                    # Use regular expressions to find all leading digits in the row
                    leading_digits = re.findall(r'\b[1-9]\d*', row_str)

                    # Iterate through the leading digits
                    for digit_str in leading_digits:
                        digit = digit_str[0]  # Get the first character (leading digit)
                        digit_counts[digit] += 1
                        total_digit_count += 1

            # Calculate percentages for each digit
            digit_percentages = {digit: (count / total_digit_count) * 100 if total_digit_count > 0 else 0 for digit, count in digit_counts.items()}

            # Calculate expected Benford's Law percentages
            expected_percentages = {str(digit): np.log10(1 + 1 / digit) * 100 for digit in range(1, 10)}

            # Plot the bar chart
            digits = list(digit_percentages.keys())
            percentages = list(digit_percentages.values())
            expected_percentages_values = list(expected_percentages.values())

            # Determine bar colors based on alignment with Benford's Law
            bar_colors = ['blue' if abs(percentage - expected_percentages[digit]) <= 5 else
                        'yellow' if abs(percentage - expected_percentages[digit]) <= 7.5 else
                        'orange' if abs(percentage - expected_percentages[digit]) <= 10 else
                        'red' for digit, percentage in digit_percentages.items()]

            # Plot the bars with colors
            plt.bar(digits, percentages, color=bar_colors, label='Actual Percentages')

            # Plot the expected Benford's Law line (red)
            plt.plot(digits, expected_percentages_values, 'r', label='Benford\'s Law')

            plt.xlabel('Leading Digit')
            plt.ylabel('Percentage (%)')
            plt.title('Leading Digit Percentages vs. Benford\'s Law')
            plt.legend()
            plt.show()
    
    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

# Function to run transaction analysis 
def analyze_transactions_from_csv(csv_file_path, col1, col2, col3):
    try:
        # Load transaction data from the selected CSV file
        data = pd.read_csv(csv_file_path)
        col1 = var_col1.get()
        col2 = var_col2.get()
        col3 = var_col3.get()

        # Clean and convert 'Total' column values
        data[col3] = data[col3].apply(clean_and_convert_total)

        # Create an interactive horizontal histogram using Plotly
        fig = px.bar(data, x=data[col3], y=data[col2], color=data[col1], orientation='h',
                     title='Total Spending by Rep',
                     labels={'Total': 'Dollars Spent (Total)', 'Rep': 'Rep'})

        # Show the interactive plot
        fig.show()


    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

# Class that creates the Duplicates modal to display duplicates found in the csv
class DuplicateViewer(wx.Frame):
    def __init__(self, duplicate_rows):
        super().__init__(None, title="Duplicate Rows Viewer", size=(800, 600))
        self.panel = wx.Panel(self)

        # Create a grid
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(len(duplicate_rows) + 1, duplicate_rows.shape[1])  # Create a grid with one extra row for headers

        # Set column labels from DataFrame
        for col, col_label in enumerate(duplicate_rows.columns):
            self.grid.SetCellValue(0, col, col_label)

        # Populate the grid with data
        for row, (_, row_data) in enumerate(duplicate_rows.iterrows()):
            for col, cell_value in enumerate(row_data):
                self.grid.SetCellValue(row + 1, col, str(cell_value))  # Use str() to convert values to strings

        # Auto-size columns
        for col in range(duplicate_rows.shape[1]):
            self.grid.AutoSizeColumn(col)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.Show()

# Function to find duplicates in the data
def find_duplicate_rows(csv_file_path, col1, col2, col3):
    try:
        # Load transaction data from the selected CSV file
        data = pd.read_csv(csv_file_path)
        col1 = var_col1.get()
        col2 = var_col2.get()
        col3 = var_col3.get()

        # Identify duplicate rows based on 'Item', 'Rep', and 'Total' columns
        duplicate_rows = data[data.duplicated(subset=[col1, col2, col3], keep=False)]

        if not duplicate_rows.empty:
            # Create a wxPython application
            app = wx.App()
            DuplicateViewer(duplicate_rows)
            app.MainLoop()

            # Save the duplicate rows to a new CSV file
            duplicate_rows.to_csv('duplicate_rows.csv', index=False)

            print(f"Duplicate rows saved to 'duplicate_rows.csv'.")
        else:
            print("No duplicate rows found in the CSV file.")

    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

# Class that creates the file view modal to display the csv file in an excel-like format
class DataViewer(wx.Frame):
    def __init__(self, data):
        super(DataViewer, self).__init__(None, title="Data Viewer")
        self.panel = wx.Panel(self)
        
        # Create a grid to display the data
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(data.shape[0], data.shape[1])
        
        # Set column labels
        for col, col_label in enumerate(data.columns):
            self.grid.SetColLabelValue(col, col_label)
        
        # Populate the grid with data
        for row, row_data in data.iterrows():
            for col, value in enumerate(row_data):
                self.grid.SetCellValue(row, col, str(value))
        
        # Create a sizer to manage layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        self.Show()

# Function that loads the csv file data into the DataViewer class
def show_excel_file(csv_file_path):
    try:
        # Load the first 10 rows of the CSV file into a DataFrame
        data = pd.read_csv(csv_file_path)

        # Open the data in a wxPython frame
        app = wx.App(False)
        frame = DataViewer(data)
        app.MainLoop()

    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

def open_info_dialog():
    # Explanation text
    explanation_text = """
    Benford's Law Analysis:
    
        A simple python script that takes a CSV and applies Benford's Law to it, where in any financial data typically the leading number 1 appears approx. 30 percent of the time, with a sloping distribution down to 9 that should appear approx. 5 percent of the time.
    
        The basic theory is that when someone commits fraud, they do not do it in increments of $10, $20, $100, or $200, instead they do it in $80 or $900 increments. Therefor, if the higher numbers appear more often than the large number average distribution, there is a chance fraud is at play.
    
    Gaussian Distribution Analysis:

        Gives a normal distribution based on the total spent on each Item by each Rep. If there is an abnormally large or small transaction it is made clearly visible for the user to see. WIP: Plots a normal distribution for each item group, with first and second std dev lines plotted to easily pick out outliers.
    
        Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item).

    Transaction Analysis:

     A transctional analytics tool that takes 3 variables from a csv: Which Rep bought an item, what Item was bought, and the Total amount spent on an item. if a person bought the same item multiple times, the graph will sum them but also show a partition to display the different transactions. The graph is interactive, so specific items can be viewed together with others or on their own, and the graph can be zoomed in and out to see all parts of the data or just specific parts the user wants to focus on.
    
        Select 3 columns from the drop down menus, an account description (or item category), the transaction description (what item/service was purchased) and the transaction column (total spent on item).

    Finding Duplicates:

        Finds duplicate transactions in the data based off of if the 3 columns chosen by the user match with any of the other data, renders it in an excel-like grid in a seperate modal and saves them to a new csv.
    """

    messagebox.showinfo("Analysis Explanations", explanation_text)


# Create and configure widgets
label_instruction = tk.Label(root, text="Select a CSV file:")
entry_file_path = tk.Entry(root, width=60)
button_browse = tk.Button(root, text="Browse Files", command=browse_file)
button_process_benfords_law = tk.Button(root, text="Run Benford's Law", command=process_benfords_law)
button_process_gaussian = tk.Button(root, text="Run Gaussian Distribution", command=lambda: process_gaussian_distribution(entry_file_path.get(), var_col1.get(), var_col3.get()))
button_process_transaction_analysis = tk.Button(root, text="Run Transaction Analysis", command=lambda: analyze_transactions_from_csv(entry_file_path.get(), var_col1.get(), var_col2.get(), var_col3.get()))
button_show_excel_file = tk.Button(root, text="Show Excel File", command=lambda: show_excel_file(entry_file_path.get()))
button_find_duplicate_rows = tk.Button(root, text="Find Duplicates", command=lambda: find_duplicate_rows(entry_file_path.get(), var_col1.get(), var_col2.get(), var_col3.get()))
info_button = tk.Button(root, text="Info", command=open_info_dialog)

# Arrange widgets in the layout using grid
label_instruction.grid(row=0, column=0, columnspan=2, pady=10)
entry_file_path.grid(row=1, column=0, columnspan=2, padx=1, pady=1)
button_browse.grid(row=1, column=2, padx=1, pady=1)
button_process_benfords_law.grid(row=2, column=2, padx=1, pady=1)
button_process_gaussian.grid(row=3, column=2, padx=1, pady=1)
button_process_transaction_analysis.grid(row=4, column=2, padx=1, pady=1)
button_find_duplicate_rows.grid(row=5, column=2, columnspan=2, padx=1, pady=1)
button_show_excel_file.grid(row=6, column=2, padx=1, pady=1)
info_button.grid(row=0, column=2, padx=1, pady=1)

# Start the Tkinter main loop
root.mainloop()
