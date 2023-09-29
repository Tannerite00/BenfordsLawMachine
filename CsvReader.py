import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm
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
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        entry_file_path.delete(0, tk.END)  # Clear the entry field
        entry_file_path.insert(0, file_path)  # Set the selected file path

        # Get the list of columns from the CSV file
        with open(file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)  # Read the header row
            column_names = header  # Get column names from the header row

        # Call a function to handle the retrieved column names
        handle_column_names(column_names)

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
    

    # Grid layout for labels and dropdown menus
    label_menu1.grid(row=5, column=0, padx=10, pady=5)
    dropdown_menu1.grid(row=5, column=1, padx=10, pady=5)
    label_menu2.grid(row=6, column=0, padx=10, pady=5)
    dropdown_menu2.grid(row=6, column=1, padx=10, pady=5)
    label_menu3.grid(row=7, column=0, padx=10, pady=5)
    dropdown_menu3.grid(row=7, column=1, padx=10, pady=5)


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
        col3 = var_col2.get()

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

#Function to find duplicates in the data
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
            # Display the duplicate rows
            print("Duplicate Rows:")
            print(duplicate_rows)

            # Save the duplicate rows to a new CSV file
            duplicate_rows.to_csv('duplicate_rows.csv', index=False)

            print(f"Duplicate rows saved to 'duplicate_rows.csv'.")
        else:
            print("No duplicate rows found in the CSV file.")

    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

def show_first_10_rows_as_excel(csv_file_path):
    try:
        # Load the first 10 rows of the CSV file into a DataFrame
        data = pd.read_csv(csv_file_path).head(10)

        # Create an ExcelWriter object
        writer = pd.ExcelWriter('first_10_rows.xlsx', engine='openpyxl')

        # Write the data to the ExcelWriter object
        data.to_excel(writer, index=False, sheet_name='Sheet1')

        # Save the data to a temporary Excel file
        writer.update()

        # Show the Excel-like data in a modal dialog
        display_data_as_modal(data)

    except FileNotFoundError:
        print("CSV file not found. Please select a valid CSV file.")

def display_data_as_modal(data):
    # Create a new tkinter window (modal dialog)
    modal = tk.Toplevel()
    modal.title("Data Viewer")

    # Create a Treeview widget to display the data
    tree = ttk.Treeview(modal)

    # Set the column names based on the DataFrame columns
    columns = list(data.columns)
    tree["columns"] = columns
    tree.heading("#0", text="Row")  # Create a row number column

    for col in columns:
        tree.heading(col, text=col)

    # Insert data into the Treeview widget
    for i, row in data.iterrows():
        tree.insert("", i, text=i, values=list(row))

    # Add a scrollbar to the Treeview widget
    scrollbar = ttk.Scrollbar(modal, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    tree.pack(fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    modal.mainloop()


# Create and configure widgets
label_instruction = tk.Label(root, text="Select a CSV file:")
entry_file_path = tk.Entry(root, width=40)
button_browse = tk.Button(root, text="Browse", command=browse_file)
button_process_benfords_law = tk.Button(root, text="Run Benford's Law", command=process_benfords_law)
button_process_gaussian = tk.Button(root, text="Run Gaussian Distribution", command=lambda: process_gaussian_distribution(entry_file_path.get(), var_col1.get(), var_col3.get()))
button_process_transaction_analysis = tk.Button(root, text="Run Transaction Analysis", command=lambda: analyze_transactions_from_csv(entry_file_path.get(), var_col1.get(), var_col2.get(), var_col3.get()))
button_show_first_10_rows = tk.Button(root, text="Show First 10 Rows", command=lambda: show_first_10_rows_as_excel(entry_file_path.get()))
button_find_duplicate_rows = tk.Button(root, text="Find Duplicates", command=lambda: find_duplicate_rows(entry_file_path.get(), var_col1.get(), var_col2.get(), var_col3.get()))

# Arrange widgets in the layout using grid
label_instruction.grid(row=0, column=0, columnspan=2, pady=10)
entry_file_path.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
button_browse.grid(row=1, column=2, padx=10, pady=5)
button_process_benfords_law.grid(row=3, column=0, padx=10, pady=5)
button_process_gaussian.grid(row=3, column=1, padx=10, pady=5)
button_process_transaction_analysis.grid(row=3, column=2, padx=10, pady=5)
button_find_duplicate_rows.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
button_show_first_10_rows.grid(row=4, column=2, padx=10, pady=5)


# Start the Tkinter main loop
root.mainloop()
