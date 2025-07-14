import json
import os
from datetime import datetime

class ReminderManager:
    """Manages reminders, including loading, saving, and checking their status."""

    def __init__(self, reminders_file='data/reminders.json'):
        """Initializes the ReminderManager and loads existing reminders."""
        self.reminders_file = reminders_file
        self.reminders = self._load_reminders()

    def _load_reminders(self):
        """Loads reminders from the JSON file."""
        if not os.path.exists(self.reminders_file):
            return []
        try:
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_reminders(self):
        """Saves the current list of reminders to the JSON file."""
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
        with open(self.reminders_file, 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, indent=4)

    def add_reminder(self, text, time_str, recurrence='daily'):
        """Adds a new reminder to the list.

        Args:
            text (str): The reminder message.
            time_str (str): The time for the reminder in 'HH:MM' format.
            recurrence (str): How often the reminder should repeat (e.g., 'daily').
        """
        new_reminder = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'text': text,
            'time': time_str,
            'recurrence': recurrence,
            'last_triggered': None
        }
        self.reminders.append(new_reminder)
        self.save_reminders()

    def delete_reminder(self, reminder_id):
        """Deletes a reminder by its ID."""
        self.reminders = [r for r in self.reminders if r.get('id') != reminder_id]
        self.save_reminders()

    def get_due_reminders(self):
        """Checks for and returns any reminders that are currently due."""
        now = datetime.now()
        due_reminders = []
        today_str = now.strftime('%Y-%m-%d')

        for reminder in self.reminders:
            reminder_time = datetime.strptime(reminder['time'], '%H:%M').time()
            
            # Check if it's time for the reminder
            if now.time() >= reminder_time:
                # For daily reminders, check if it has already been triggered today
                if reminder.get('recurrence') == 'daily':
                    last_triggered_date = reminder.get('last_triggered')
                    if last_triggered_date != today_str:
                        due_reminders.append(reminder)
        
        return due_reminders

    def mark_as_triggered(self, reminder_id):
        """Marks a reminder as triggered for the current day."""
        today_str = datetime.now().strftime('%Y-%m-%d')
        for reminder in self.reminders:
            if reminder.get('id') == reminder_id:
                reminder['last_triggered'] = today_str
                break
        self.save_reminders()
