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