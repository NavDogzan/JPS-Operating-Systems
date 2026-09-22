import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk


root = tk.Tk()
root.title("JPS CSV Manager")
root.geometry("950x600")
root.minsize(650, 400)
root.configure(bg="#eef2f5")

file_path = None
headers = []
rows = []
filtered_indexes = []
selected_indexes = set()
row_cells = {}
search_text = tk.StringVar()
status_text = tk.StringVar(value="Open a CSV file to begin")
canvas = None
grid_frame = None


def refresh_table():
    global filtered_indexes, row_cells, selected_indexes
    query = search_text.get().strip().lower()
    filtered_indexes = [
        index for index, row in enumerate(rows)
        if not query or query in " ".join(row).lower()
    ]
    selected_indexes = set()
    row_cells = {}
    for widget in grid_frame.winfo_children():
        widget.destroy()

    for column, header in enumerate(headers):
        tk.Label(
            grid_frame, text=header, bg="#37474f", fg="white", relief="solid",
            borderwidth=1, padx=8, pady=7, anchor="w", width=18,
        ).grid(row=0, column=column, sticky="nsew")

    for display_row, row_index in enumerate(filtered_indexes, start=1):
        row_cells[row_index] = []
        for column, value in enumerate(rows[row_index]):
            cell = tk.Label(
                grid_frame, text=value, bg="white", fg="#263238", relief="solid",
                borderwidth=1, padx=8, pady=7, anchor="w", width=18,
            )
            cell.grid(row=display_row, column=column, sticky="nsew")
            row_cells[row_index].append(cell)
            cell.bind("<Button-1>", lambda _event, index=row_index: select_row(index))
            cell.bind("<Double-1>", lambda _event, index=row_index: edit_row(index))
    grid_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


def select_row(row_index):
    global selected_indexes
    for cells in row_cells.values():
        for cell in cells:
            cell.configure(bg="white")
    selected_indexes = {row_index}
    for cell in row_cells.get(row_index, []):
        cell.configure(bg="#b3e5fc")


def new_csv():
    global file_path, headers, rows
    file_path = None
    headers = []
    rows = []
    search_text.set("")
    refresh_table()
    status_text.set("New CSV - add columns or rows to begin")
    add_columns("First column")


def add_columns(title="Add columns"):
    global headers
    names = simpledialog.askstring(title, "Enter column names separated by commas:", parent=root)
    if not names:
        return
    new_headers = [name.strip() for name in names.split(",") if name.strip()]
    existing = set(headers)
    added = 0
    for name in new_headers:
        if name not in existing:
            headers.append(name)
            existing.add(name)
            added += 1
    for row in rows:
        row.extend([""] * (len(headers) - len(row)))
    refresh_table()
    status_text.set(f"Added {added} column(s)")


def open_csv():
    global file_path, headers, rows
    path = filedialog.askopenfilename(
        title="Open CSV file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not path:
        return
    try:
        with open(path, "r", newline="", encoding="utf-8-sig") as file:
            data = list(csv.reader(file))
        if not data:
            raise ValueError("The file is empty")
        if not any(data[0]):
            raise ValueError("The CSV has no column names")
        headers = data[0]
        rows = [(row + [""] * len(headers))[:len(headers)] for row in data[1:]]
        file_path = path
        search_text.set("")
        refresh_table()
        status_text.set(f"Loaded {os.path.basename(path)} - {len(rows)} rows")
    except (OSError, csv.Error, ValueError) as error:
        messagebox.showerror("Could not open CSV", str(error), parent=root)


def save_csv(save_as=False):
    global file_path
    if not headers:
        messagebox.showinfo("Nothing to save", "Add at least one column first.", parent=root)
        return
    if save_as or not file_path:
        file_path = filedialog.asksaveasfilename(
            title="Save CSV file", defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not file_path:
            return
    try:
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
        status_text.set(f"Saved {os.path.basename(file_path)} - {len(rows)} rows")
    except OSError as error:
        messagebox.showerror("Could not save CSV", str(error), parent=root)


def add_row():
    if not headers:
        add_columns("First column")
    if headers:
        values = ask_for_row([""] * len(headers), "Add row")
        if values is not None:
            rows.append(values)
            refresh_table()
            status_text.set(f"Added row - {len(rows)} total")


def edit_row(row_index=None):
    if row_index is None:
        if len(selected_indexes) != 1:
            messagebox.showinfo("Select one row", "Select exactly one row to edit.", parent=root)
            return
        row_index = next(iter(selected_indexes))
    values = ask_for_row(rows[row_index], "Edit row")
    if values is not None:
        rows[row_index] = values
        refresh_table()


def delete_row():
    if not selected_indexes:
        messagebox.showinfo("Select rows", "Select one or more rows to delete.", parent=root)
        return
    if not messagebox.askyesno("Delete row", "Delete the selected row?", parent=root):
        return
    for row_index in sorted(selected_indexes, reverse=True):
        del rows[row_index]
    refresh_table()
    status_text.set(f"Deleted row - {len(rows)} remaining")


def ask_for_row(values, title):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.transient(root)
    dialog.grab_set()
    entries = []
    for index, header in enumerate(headers):
        tk.Label(dialog, text=header, anchor="w").grid(row=index, column=0, padx=10, pady=5, sticky="w")
        entry = ttk.Entry(dialog, width=45)
        entry.insert(0, values[index] if index < len(values) else "")
        entry.grid(row=index, column=1, padx=10, pady=5)
        entries.append(entry)
    result = []

    def accept():
        result.extend(entry.get() for entry in entries)
        dialog.destroy()

    def cancel():
        dialog.destroy()

    buttons = tk.Frame(dialog)
    buttons.grid(row=len(headers), column=0, columnspan=2, pady=10)
    ttk.Button(buttons, text="Cancel", command=cancel).pack(side="left", padx=5)
    ttk.Button(buttons, text="OK", command=accept).pack(side="left", padx=5)
    dialog.bind("<Return>", lambda _event: accept())
    dialog.bind("<Escape>", lambda _event: cancel())
    entries[0].focus_set()
    root.wait_window(dialog)
    return result or None


def build_ui():
    global canvas, grid_frame
    toolbar = tk.Frame(root, bg="#263238", padx=8, pady=8)
    toolbar.pack(fill="x")
    button_style = {
        "bg": "#37474f", "fg": "white", "activebackground": "#546e7a",
        "activeforeground": "white", "relief": "flat", "font": ("Segoe UI", 10),
        "cursor": "hand2",
    }
    for label, command in [("New", new_csv), ("Open", open_csv), ("Save", save_csv)]:
        tk.Button(toolbar, text=label, command=command, **button_style).pack(side="left", padx=5)
    tk.Button(toolbar, text="Add columns", command=add_columns, **button_style).pack(side="left", padx=(18, 5))
    tk.Button(toolbar, text="Add row", command=add_row, **button_style).pack(side="left", padx=(18, 5))
    tk.Button(toolbar, text="Edit row", command=edit_row, **button_style).pack(side="left", padx=5)
    tk.Button(toolbar, text="Delete row", command=delete_row, **button_style).pack(side="left", padx=5)

    search_frame = tk.Frame(root, bg="#d7e0e5", padx=10, pady=8)
    search_frame.pack(fill="x")
    tk.Label(search_frame, text="Search", bg="#d7e0e5", fg="#263238").pack(side="left")
    ttk.Entry(search_frame, textvariable=search_text, width=35).pack(side="left", padx=(8, 0))
    ttk.Button(search_frame, text="Clear", command=lambda: search_text.set("")).pack(side="left", padx=8)

    table_frame = tk.Frame(root, bg="white")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    canvas = tk.Canvas(table_frame, bg="#b0bec5", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    grid_frame = tk.Frame(canvas, bg="#b0bec5")
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")
    grid_frame.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
    vertical_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    horizontal_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)
    vertical_scroll.pack(side="right", fill="y")
    horizontal_scroll.pack(side="bottom", fill="x")
    tk.Label(root, textvariable=status_text, anchor="w", bg="#d7e0e5", fg="#455a64", padx=10).pack(fill="x")


build_ui()
search_text.trace_add("write", lambda *_args: refresh_table())
root.bind("<Control-o>", lambda _event: open_csv())
root.bind("<Control-s>", lambda _event: save_csv())
root.bind("<Control-n>", lambda _event: new_csv())
root.mainloop()
