import json
import os

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
        return {
            "name": self.name,
            "time": self.time,
            "dosage": self.dosage,
            "taken": self.taken,
        }

    def __str__(self):
        status = "Taken" if self.taken else "Not taken"
        return f"{self.name} - {self.time} - {self.dosage} - {status}"

def load_medications():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        return [Medication(m["name"], m["time"], m["dosage"], m["taken"]) for m in data]
    except (json.JSONDecodeError, KeyError):
        print("Could not read saved data. Starting with an empty schedule.\n")
        return []

def save_medications(medications):
    data = [medication.to_dict() for medication in medications]
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

def add_medication(medications):
    name = input("Enter medication name: ")
    time = input("Enter time (HH:MM): ")
    dosage = input("Enter dosage: ")
    medications.append(Medication(name, time, dosage))
    save_medications(medications)
    print(f"{name} added and saved to your schedule.\n")

def view_schedule(medications):
    if not medications:
        print("No medications added yet.\n")
        return
    print("\nToday's Medication Schedule")
    print("-" * 30)
    for i, medication in enumerate(medications, start=1):
        print(f"{i}. {medication}")
    print()

def mark_taken(medications):
    view_schedule(medications)
    if not medications:
        return
    try:
        choice = int(input("Enter the number of the medication you have taken: "))
        if 1 <= choice <= len(medications):
            medications[choice - 1].mark_as_taken()
            save_medications(medications)
            print(f"{medications[choice - 1].name} marked as taken and saved.\n")
        else:
            print("That number does not match a medication on your list.\n")
    except ValueError:
        print("Please enter a valid number.\n")