# Function to load and display CSV in Treeview
def load_csv(mode=0):
    # Ask the user to select a CSV file
    if mode == 0:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    elif mode == 1:
        file_path = "C:/Users/manol/Desktop/New folder/c1.csv"
    
    if not file_path:
        return

    # Clear existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Open the CSV file and read it
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the headers from the first row

        # Clear existing columns in the Treeview
        tree["columns"] = headers

        # Define columns and headings
        for header in headers:
            if header == 'File Name':
                tree.heading(header, text=header)
                tree.column(header, width=400)
            else:
                tree.heading(header, text=header)
                tree.column(header, width=100)

        # Add rows to the Treeview
        for row in reader:
            tree.insert("", tk.END, values=row)

# Function to handle double-click event and print file name
def on_double_click(event):
    global added_song, added_song_name
    # Get the item selected by the user
    selected_item = tree.selection()
    if selected_item:
        # Get the values of the selected row
        item_values = tree.item(selected_item, 'values')
        # Assuming the file name is in the first column
        file_name = item_values[0]  # Adjust the index if file name is in another column
        added_song = file_name
        added_song_name = file_name
        print(f"File Name: {file_name}")