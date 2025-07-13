import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
import os

# ---------------------------
# Calculate + Save BMI
# ---------------------------
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if height <= 0 or weight <= 0:
            raise ValueError

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"BMI: {bmi}\nCategory: {category}")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("bmi_records.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, weight, height, bmi, category])

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")

# ---------------------------
# View BMI History
# ---------------------------
def view_history():
    if not os.path.exists("bmi_records.csv"):
        messagebox.showinfo("No Data", "No records found.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("500x300")

    tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show="headings")
    tree.heading("Date", text="Date & Time")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (m)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")

    with open("bmi_records.csv", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

# ---------------------------
# Setup GUI
# ---------------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("350x320")
root.resizable(False, False)

tk.Label(root, text="Enter your weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)

tk.Label(root, text="Enter your height (m):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack(pady=5)

tk.Button(root, text="Calculate and Save", command=calculate_bmi).pack(pady=10)
tk.Button(root, text="View History", command=view_history).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
