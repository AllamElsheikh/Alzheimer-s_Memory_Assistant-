import customtkinter as ctk
from src.core.reminder_manager import ReminderManager
from tkinter import messagebox
from src.ai.asr_service import ASRService
from src.ai.gemma_integration import GemmaIntegration

class MainWindow(ctk.CTk):
    """Main application window for the Faker? app."""

    def __init__(self):
        """Initializes the main window and sets up the UI components."""
        super().__init__()

        self.title("Faker? - AI Memory Assistant")
        self.geometry("800x600")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize services
        print("Initializing ReminderManager...")
        self.reminder_manager = ReminderManager()
        print("Initializing ASRService...")
        self.asr_service = ASRService()
        print("Initializing GemmaIntegration...")
        self.gemma_integration = GemmaIntegration()

        # Navigation Frame
        self.nav_frame = ctk.CTkFrame(self, height=50)
        self.nav_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.create_navigation()

        # Container for views
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.setup_views()

        self.show_frame("PatientView")
        self._current_frame = "PatientView"

        # Start the reminder checking loop
        self.check_reminders()

    def check_reminders(self):
        """Checks for due reminders and displays a notification for each.
        This method reschedules itself to run every 60 seconds."""
        try:
            due_reminders = self.reminder_manager.get_due_reminders()
            for reminder in due_reminders:
                messagebox.showinfo("Reminder", reminder.get('text', 'You have a reminder.'))
                self.reminder_manager.mark_as_triggered(reminder.get('id'))
        except Exception as e:
            print(f"Error checking reminders: {e}")
        
        # Schedule the next check
        self.after(60000, self.check_reminders)

    def create_navigation(self):
        """Creates the navigation buttons."""
        patient_button = ctk.CTkButton(self.nav_frame, text="Patient View", command=lambda: self.show_frame("PatientView"))
        patient_button.pack(side="left", padx=10)

        caregiver_button = ctk.CTkButton(self.nav_frame, text="Caregiver Dashboard", command=lambda: self.show_frame("CaregiverView"))
        caregiver_button.pack(side="left", padx=10)

        report_button = ctk.CTkButton(self.nav_frame, text="Reports", command=lambda: self.show_frame("ReportView"))
        report_button.pack(side="left", padx=10)

    def setup_views(self):
        """Creates and stores instances of the different view frames."""
        # Import views here to avoid circular dependencies
        from .patient_view import PatientView
        from .caregiver_view import CaregiverView
        from .report_view import ReportView

        views = {
            "PatientView": PatientView,
            "CaregiverView": CaregiverView,
            "ReportView": ReportView
        }

        for name, F in views.items():
            if name == "PatientView":
                # Pass the initialized services to PatientView
                frame = F(self.container, self, self.asr_service, self.gemma_integration)
            else:
                frame = F(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Shows the specified frame/view."""
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            
            # End session when switching away from patient view
            if hasattr(self, '_current_frame') and self._current_frame == "PatientView":
                patient_frame = self.frames.get("PatientView")
                if patient_frame and hasattr(patient_frame, 'end_session'):
                    patient_frame.end_session()
            
            self._current_frame = page_name
        else:
            print(f"Error: Frame '{page_name}' not found.")

    def run(self):
        """Starts the main application loop."""
        self.mainloop()

# To test the main window independently
if __name__ == "__main__":
    app = MainWindow()
    app.run()
