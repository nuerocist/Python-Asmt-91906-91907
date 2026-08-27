import json
import os

# File used to store medication data
DATA_FILE = "medications.json"

class Medication:
    def __init__(self, name, time, dosage, taken=False):
        self.name = name
        self.time = time
        self.dosage = dosage
        self.taken = taken

    def mark_as_taken(self):
        # Updates this medication's status once the user confirms they took it
        self.taken = True

    def to_dict(self):
        # Converts this object into a plain dictionary so it can be saved as JSON
        return {
            "name": self.name,
            "time": self.time,
            "dosage": self.dosage,
            "taken": self.taken,
        }

    def __str__(self):
        # Controls how a Medication looks when printed
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
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        print("Could not read saved data. Starting with an empty schedule.")
        return []

def save_medications(medications):
    # Writes the current list of medications to file, overwriting the old save
    data = [medication.to_dict() for medication in medications]
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

def add_medication(medications):
    # Prompts the user for details and adds a new medication to the list
    name = input("Enter medication name: ")
    time = input("Enter time (HH:MM): ")
    dosage = input("Enter dosage: ")
    medications.append(Medication(name, time, dosage))
    save_medications(medications)
    print(f"{name} added and saved to your schedule.\n")

def view_schedule(medications):
    # Displays every medication currently stored, with its status
    if not medications:
        print("No medications added yet.\n")
        return
    print("\nToday's Medication Schedule")
    print("-" * 30)
    for i, medication in enumerate(medications, start=1):
        print(f"{i}. {medication}")
    print()

def mark_taken(medications):
    # Lets the user select a medication from the schedule and mark it as taken
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

def main():
    medications = load_medications()
    while True:
        print("Medication Reminder - Version 2")
        print("1. Add a medication")
        print("2. View today's schedule")
        print("3. Mark a medication as taken")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_medication(medications)
        elif choice == "2":
            view_schedule(medications)
        elif choice == "3":
            mark_taken(medications)
        elif choice == "4":
            print("Your schedule has been saved. Goodbye.")
            break
        else:
            print("Please choose a number between 1 and 4.\n")


main()