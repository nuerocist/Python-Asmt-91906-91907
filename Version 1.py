medications = []

def add_medication():
    name = input("Enter medication name: ")
    time = input("Enter time (HH:MM): ")
    dosage = input("Enter dosage: ")
    medication = {"name": name, "time": time, "dosage": dosage, "taken": False}
    medications.append(medication)
    print(f"{name} added to your schedule.\n")

def view_schedule():
    if not medications:
        print("No medications added yet.\n")
        return
    print("\nToday's Medication Schedule")
    print("-" * 30)
    for i, med in enumerate(medications, start=1):
        status = "Taken" if med["taken"] else "Not taken"
        print(f"{i}. {med['name']} - {med['time']} - {med['dosage']} - {status}")
    print()

def mark_taken():
    view_schedule()
    if not medications:
        return
    try:
        choice = int(input("Enter the number of the medication you have taken: "))
        if 1 <= choice <= len(medications):
            medications[choice - 1]["taken"] = True
            print(f"{medications[choice - 1]['name']} marked as taken.\n")
        else:
            print("That number does not match a medication on your list.\n")
    except ValueError:
        print("Please enter a valid number.\n")

def main():
    while True:
        print("Medication Reminder - Version 1")
        print("1. Add a medication")
        print("2. View today's schedule")
        print("3. Mark a medication as taken")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_medication()
        elif choice == "2":
            view_schedule()
        elif choice == "3":
            mark_taken()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Please choose a number between 1 and 4.\n")

main()