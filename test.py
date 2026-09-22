import csv 
import tkinter as tk

root = tk.Tk()
root.geometry("1000x600")
def add_col():
    global col
    header = csv_data[0][col] if col < len(csv_data[0]) else f"Column {col + 1}"
    if col >= len(csv_data[0]):
        csv_data[0].append(header)
        for data_row in csv_data[1:]:
            data_row.append("")
    column_frame = tk.Frame(ViewFrame, bg="white", bd=1, relief="solid")
    column_frame.grid(column=col, row=0, padx=3, pady=3, sticky="nsew")
    tk.Label(column_frame, text=header, bg="#37474f", fg="white", width=16).pack(fill="x")
    for data_row in csv_data[1:]:
        entry = tk.Entry(column_frame, width=18)
        entry.insert(0, data_row[col])
        entry.pack(padx=4, pady=2)
    columns.append(column_frame)
    ViewFrame.columnconfigure(col, weight=1)
    col+=1

def add_row():
    global row
    if not columns:
        add_col()
    new_row = [""] * len(columns)
    csv_data.append(new_row)
    for column_frame in columns:
        tk.Entry(column_frame, width=18).pack(padx=4, pady=2)
    row += 1


csv_data = [
    ["Name", "Age", "City"],
    ["Alice", "28", "New York"],
    ["Bob", "34", "Los Angeles"],
    ["Charlie", "22", "Chicago"],
]

col = 0
row = len(csv_data) - 1
columns = []

C = tk.Button(root,text="Add coloumn",width=10, command=add_col).pack(side="top")
R = tk.Button(root,text="Add row",width=10, command=add_row).pack(side="top")

ViewFrame = tk.Frame(root, bg="Light Grey", height=1000)
ViewFrame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

for _ in csv_data[0]:
    add_col()

root.mainloop()