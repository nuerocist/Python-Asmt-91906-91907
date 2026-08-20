import json
import os
import tkinter as tk

DATA_FILE = "medications.json"


class Medication:
    def __init__(self, name, time, dosage, taken=False):
        self.name = name
        self.time = time
        self.dosage = dosage
        self.taken = taken

    def mark_as_taken(self):
        self.taken = True

    def to_dict(self):
        return {"name": self.name, "time": self.time, "dosage": self.dosage, "taken": self.taken}

    def __str__(self):
        status = "Taken" if self.taken else "Not taken"
        return f"{self.name} - {self.time} - {self.dosage} - {status}"

def load_medications():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        file = open(DATA_FILE, "r")
        data = json.load(file)
        file.close()
        medications = []
        for m in data:
            medications.append(Medication(m["name"], m["time"], m["dosage"], m["taken"]))
        return medications
    except (json.JSONDecodeError, KeyError):
        print("Could not read saved data. Starting with an empty schedule.")
        return []

def save_medications(medications):
    data = []
    for medication in medications:
        data.append(medication.to_dict())
    file = open(DATA_FILE, "w")
    json.dump(data, file, indent=2)
    file.close()

def is_valid_time(time_str):
    parts = time_str.split(":")
    if len(parts) != 2:
        return False
    hours, minutes = parts
    if not (hours.isdigit() and minutes.isdigit()):
        return False
    hours = int(hours)
    minutes = int(minutes)
    if hours < 0 or hours > 23:
        return False
    if minutes < 0 or minutes > 59:
        return False
    return True

def is_valid_dosage(dosage_str):
    parts = dosage_str.split()
    if len(parts) == 0:
        return False
    number_part = parts[0]
    if not number_part.isdigit():
        return False
    return int(number_part) > 0

medications = load_medications()

window = tk.Tk()
window.title("Medication Reminder - Version 3")
window.geometry("400x450")

tk.Label(window, text="Medication name").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Time (HH:MM)").pack()
time_entry = tk.Entry(window)
time_entry.pack()

tk.Label(window, text="Dosage").pack()
dosage_entry = tk.Entry(window)
dosage_entry.pack()

error_label = tk.Label(window, text="", fg="red")
error_label.pack()

tk.Label(window, text="Today's Schedule").pack(pady=(10, 0))
schedule_list = tk.Listbox(window, width=50)
schedule_list.pack(pady=5)

def refresh_schedule():
    schedule_list.delete(0, tk.END)
    for medication in medications:
        schedule_list.insert(tk.END, str(medication))

