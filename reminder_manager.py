
import json
from datetime import datetime

class ReminderManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.reminders = self.load_reminders()

    def load_reminders(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_reminders(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.reminders, f, indent=4)

    def add_reminder(self, date_str, reminder):
        if date_str not in self.reminders:
            self.reminders[date_str] = []
        self.reminders[date_str].append(reminder)
        self.save_reminders()

    def update_reminder(self, date_str, index, updated_reminder):
        if date_str in self.reminders and 0 <= index < len(self.reminders[date_str]):
            self.reminders[date_str][index] = updated_reminder
            self.save_reminders()

    def delete_reminder(self, date_str, index):
        if date_str in self.reminders and 0 <= index < len(self.reminders[date_str]):
            del self.reminders[date_str][index]
            if not self.reminders[date_str]:
                del self.reminders[date_str]
            self.save_reminders()

    def get_reminders_for_date(self, date_str):
        return self.reminders.get(date_str, [])

    def get_all_reminders(self):
        return self.reminders

    def delete_all_for_date(self, date_str):
        if date_str in self.reminders:
            del self.reminders[date_str]
            self.save_reminders()
