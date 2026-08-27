import json
import os
import tkinter as tk

# File used to store medication data
DATA_FILE = "medications.json"


class Medication:
    # Shows a single medication with its schedule details
    def __init__(self, name, time, dosage, taken=False):
        self.name = name
        self.time = time
        self.dosage = dosage
        self.taken = taken # defaults to False when a medication is first created

    def mark_as_taken(self):
         # Updates this medication's status once the user confirms they took it
        self.taken = True

    def to_dict(self):
        # Converts this object into a plain dictionary so it can be saved as JSON
        return {"name": self.name, "time": self.time, "dosage": self.dosage, "taken": self.taken}

    def __str__(self):
        # Controls how a Medication looks when displayed in the schedule list
        status = "Taken" if self.taken else "Not taken"
        return f"{self.name} - {self.time} - {self.dosage} - {status}"

def load_medications():
    # Loads saved medications from file when the program starts
    if not os.path.exists(DATA_FILE):
         # No file yet means this is the first time the program has run
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
        # Handles a missing field or a corrupted/unreadable file
        print("Could not read saved data. Starting with an empty schedule.")
        return []

def save_medications(medications):
    # Writes the current list of medications to file, overwriting the old save
    data = []
    for medication in medications:
        data.append(medication.to_dict())
    file = open(DATA_FILE, "w")
    json.dump(data, file, indent=2)
    file.close()

def is_valid_time(time_str):
    # Checks the time is in HH:MM format with real hour and minute values
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
     # Checks the dosage starts with a whole number greater than 0
    parts = dosage_str.split()
    if len(parts) == 0:
        return False
    number_part = parts[0]
    if not number_part.isdigit():
        return False
    return int(number_part) > 0

medications = load_medications()

# All of the windows and widgets
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

# Shows validation error messages to the user
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

tk.Label(window, text="Today's Schedule").pack(pady=(10, 0))
schedule_list = tk.Listbox(window, width=50)
schedule_list.pack(pady=5)

def refresh_schedule():
     # Redraws the schedule list from the current medications list
    schedule_list.delete(0, tk.END)
    for medication in medications:
        schedule_list.insert(tk.END, str(medication))

def add_medication():
    # Reads the form, validates it, and adds a new medication if everything is valid
    name = name_entry.get()
    time = time_entry.get()
    dosage = dosage_entry.get()

    if name == "":
        error_label.config(text="Enter a medication name.")
        return
    if not is_valid_time(time):
        error_label.config(text="Time must be in HH:MM format, e.g. 08:00.")
        return
    if not is_valid_dosage(dosage):
        error_label.config(text="Dosage must start with a number greater than 0.")
        return

    medications.append(Medication(name, time, dosage))
    save_medications(medications)

# Clear the form ready for the next entry
    name_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    dosage_entry.delete(0, tk.END)
    error_label.config(text="")
    refresh_schedule()

def mark_taken():
    # Marks whichever medication is selected in the list as taken
    selection = schedule_list.curselection()
    if not selection:
        error_label.config(text="Select a medication first.")
        return
    index = selection[0]
    medications[index].mark_as_taken()
    save_medications(medications)
    refresh_schedule()

tk.Button(window, text="Add medication", command=add_medication).pack(pady=5)
tk.Button(window, text="Mark selected as taken", command=mark_taken).pack(pady=5)

refresh_schedule()
window.mainloop()