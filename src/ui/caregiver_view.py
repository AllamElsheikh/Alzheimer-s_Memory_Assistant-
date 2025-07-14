import customtkinter as ctk
from tkinter import simpledialog, messagebox, filedialog
from datetime import datetime
from src.core.prompt_manager import PromptManager
from src.core.reminder_manager import ReminderManager
from src.core.memory_engine import MemoryEngine
from src.ai.context_manager import ContextManager

class CaregiverView(ctk.CTkFrame):
    """The caregiver-facing view for managing the app."""

    def __init__(self, parent, controller):
        """Initializes the CaregiverView frame."""
        super().__init__(parent)
        self.controller = controller
        self.prompt_manager = PromptManager()
        self.reminder_manager = ReminderManager()
        self.memory_engine = MemoryEngine()
        self.context_manager = ContextManager()

        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Caregiver Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.settings_tab = self.tab_view.add("Settings")
        self.prompts_tab = self.tab_view.add("Memory Prompts")
        self.reminders_tab = self.tab_view.add("Reminders")
        self.reports_tab = self.tab_view.add("Reports")
        self.memory_tab = self.tab_view.add("Memory Cards")

        self.create_settings_tab()
        self.create_prompts_tab()
        self.create_reminders_tab()
        self.create_reports_tab()
        self.create_memory_tab()

    def create_settings_tab(self):
        label = ctk.CTkLabel(self.settings_tab, text="Application settings will be configured here.")
        label.pack(padx=20, pady=20)

    def create_prompts_tab(self):
        self.prompts_tab.grid_columnconfigure(0, weight=1)
        self.prompts_tab.grid_rowconfigure(0, weight=1)

        self.prompts_frame = ctk.CTkScrollableFrame(self.prompts_tab, label_text="Current Prompts")
        self.prompts_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        add_prompt_button = ctk.CTkButton(self.prompts_tab, text="Add New Prompt", command=self.add_prompt_dialog)
        add_prompt_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.refresh_prompts_list()

    def refresh_prompts_list(self):
        for widget in self.prompts_frame.winfo_children():
            widget.destroy()

        prompts = self.prompt_manager.get_prompts()
        for i, prompt in enumerate(prompts):
            prompt_text = prompt.get('text', 'No text')
            frame = ctk.CTkFrame(self.prompts_frame)
            frame.pack(fill="x", pady=5, padx=5)
            label = ctk.CTkLabel(frame, text=f"{i+1}. {prompt_text}")
            label.pack(side="left", padx=10)
            del_button = ctk.CTkButton(frame, text="Delete", width=60, command=lambda i=i: self.delete_prompt(i))
            del_button.pack(side="right", padx=10)

    def add_prompt_dialog(self):
        dialog = ctk.CTkInputDialog(text="Enter the prompt question:", title="Add New Prompt")
        prompt_text = dialog.get_input()

        if prompt_text:
            image_path = filedialog.askopenfilename(title="Select an image file (optional)")
            audio_path = filedialog.askopenfilename(title="Select an audio file (optional)")

            new_prompt = {
                "text": prompt_text,
                "image_path": image_path if image_path else None,
                "audio_path": audio_path if audio_path else None
            }
            self.prompt_manager.add_prompt(new_prompt)
            self.refresh_prompts_list()

    def delete_prompt(self, index):
        self.prompt_manager.delete_prompt(index)
        self.refresh_prompts_list()

    def create_reminders_tab(self):
        """Creates the UI components for the Reminders tab."""
        self.reminders_tab.grid_columnconfigure(0, weight=1)
        self.reminders_tab.grid_rowconfigure(0, weight=1)

        self.reminders_frame = ctk.CTkScrollableFrame(self.reminders_tab, label_text="Scheduled Reminders")
        self.reminders_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        add_reminder_button = ctk.CTkButton(self.reminders_tab, text="Add New Reminder", command=self.add_reminder_dialog)
        add_reminder_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.refresh_reminders_list()

    def refresh_reminders_list(self):
        """Clears and reloads the list of reminders from the ReminderManager."""
        for widget in self.reminders_frame.winfo_children():
            widget.destroy()

        reminders = self.reminder_manager.reminders
        for reminder in reminders:
            reminder_id = reminder.get('id')
            text = f"{reminder.get('time', 'N/A')} - {reminder.get('text', 'No text')}"
            
            frame = ctk.CTkFrame(self.reminders_frame)
            frame.pack(fill="x", pady=5, padx=5)
            label = ctk.CTkLabel(frame, text=text)
            label.pack(side="left", padx=10, expand=True, fill="x")
            del_button = ctk.CTkButton(frame, text="Delete", width=60, command=lambda r_id=reminder_id: self.delete_reminder(r_id))
            del_button.pack(side="right", padx=10)

    def add_reminder_dialog(self):
        """Opens dialogs to get reminder text and time from the user."""
        text_dialog = ctk.CTkInputDialog(text="What is the reminder for?", title="New Reminder")
        text = text_dialog.get_input()
        if not text:
            return

        time_dialog = ctk.CTkInputDialog(text="What time should the reminder be? (HH:MM format)", title="Reminder Time")
        time_str = time_dialog.get_input()
        if time_str:  # Basic validation, could be improved
            try:
                datetime.strptime(time_str, '%H:%M')
                self.reminder_manager.add_reminder(text, time_str)
                self.refresh_reminders_list()
            except ValueError:
                messagebox.showerror("Invalid Format", "Please enter the time in HH:MM format.")

    def delete_reminder(self, reminder_id):
        """Deletes a reminder and refreshes the list."""
        self.reminder_manager.delete_reminder(reminder_id)
        self.refresh_reminders_list()

    def create_reports_tab(self):
        """Enhanced reports tab with session analytics"""
        reports_frame = ctk.CTkScrollableFrame(self.reports_tab)
        reports_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(reports_frame, text="Patient Interaction Reports", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)
        
        # Generate report button
        generate_button = ctk.CTkButton(reports_frame, text="Generate Latest Report", 
                                       command=self.generate_session_report)
        generate_button.pack(pady=10)
        
        # Report display area
        self.report_text = ctk.CTkTextbox(reports_frame, height=300)
        self.report_text.pack(fill="both", expand=True, pady=10)
        
        # Load last report if available
        self.load_latest_report()

    def generate_session_report(self):
        """Generate a comprehensive session report"""
        try:
            # Get the latest session report from context manager
            report = self.context_manager.get_session_report()
            
            report_text = f"""
=== Daily Interaction Report ===
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Session Summary:
- Duration: {report.get('duration', 0)} minutes
- Total Conversations: {report.get('interaction_summary', {}).get('total_conversations', 0)}
- Engagement Level: {report.get('interaction_summary', {}).get('engagement_level', 'Unknown')}

Topics Discussed:
{chr(10).join(f"- {topic}" for topic in report.get('interaction_summary', {}).get('topics_discussed', []))}

Memory Assessment:
- Status: {report.get('memory_assessment', {}).get('status', 'No data')}
- Success Rate: {report.get('memory_assessment', {}).get('success_rate', 0):.0%}

Mood Assessment:
- Overall Mood: {report.get('mood_assessment', {}).get('overall_mood', 'Neutral')}
- Mood Changes: {report.get('mood_assessment', {}).get('mood_changes', 0)}

Recommendations:
{chr(10).join(f"- {rec}" for rec in report.get('recommendations', []))}

=== End Report ===
            """
            
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", report_text)
            
        except Exception as e:
            error_text = f"Error generating report: {str(e)}"
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", error_text)

    def load_latest_report(self):
        """Load the most recent report"""
        placeholder_text = """
=== Patient Interaction Reports ===

This section will display:
- Daily interaction summaries
- Memory performance trends
- Mood and engagement analysis
- Caregiver recommendations

Click 'Generate Latest Report' to see the most recent session data.
        """
        self.report_text.insert("1.0", placeholder_text)

    def create_memory_tab(self):
        """Creates the UI components for the Memory Cards tab."""
        self.memory_tab.grid_columnconfigure(0, weight=1)
        self.memory_tab.grid_rowconfigure(0, weight=1)

        self.memory_frame = ctk.CTkScrollableFrame(self.memory_tab, label_text="Person Memory Cards")
        self.memory_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        add_memory_button = ctk.CTkButton(self.memory_tab, text="Add Person Card", command=self.add_memory_card_dialog)
        add_memory_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.refresh_memory_cards()

    def refresh_memory_cards(self):
        """Refresh the list of memory cards"""
        for widget in self.memory_frame.winfo_children():
            widget.destroy()

        cards = self.memory_engine.get_all_cards()
        for card in cards:
            card_frame = ctk.CTkFrame(self.memory_frame)
            card_frame.pack(fill="x", pady=5, padx=5)
            
            info_text = f"{card['name']} - {card.get('relationship', 'Unknown')}"
            if card.get('access_count', 0) > 0:
                info_text += f" (Accessed {card['access_count']} times)"
            
            label = ctk.CTkLabel(card_frame, text=info_text)
            label.pack(side="left", padx=10, expand=True, fill="x")
            
            edit_button = ctk.CTkButton(card_frame, text="Edit", width=60, 
                                       command=lambda c=card: self.edit_memory_card(c))
            edit_button.pack(side="right", padx=5)
            
            del_button = ctk.CTkButton(card_frame, text="Delete", width=60,
                                      command=lambda c=card: self.delete_memory_card(c['id']))
            del_button.pack(side="right", padx=5)

    def add_memory_card_dialog(self):
        """Dialog to add a new memory card"""
        name_dialog = ctk.CTkInputDialog(text="Person's name:", title="Add Memory Card")
        name = name_dialog.get_input()
        if not name:
            return

        relationship_dialog = ctk.CTkInputDialog(text="Relationship (e.g., daughter, son, friend):", title="Relationship")
        relationship = relationship_dialog.get_input()
        if not relationship:
            relationship = "Unknown"

        photo_path = filedialog.askopenfilename(
            title="Select a photo of this person (optional)",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )

        notes_dialog = ctk.CTkInputDialog(text="Additional notes about this person:", title="Notes")
        notes = notes_dialog.get_input() or ""

        # Add the memory card
        card_id = self.memory_engine.add_person_card(name, relationship, photo_path, notes)
        messagebox.showinfo("Success", f"Memory card for {name} has been added!")
        self.refresh_memory_cards()

    def edit_memory_card(self, card):
        """Edit an existing memory card"""
        messagebox.showinfo("Edit", f"Edit functionality for {card['name']} will be implemented")
        # TODO: Implement edit dialog

    def delete_memory_card(self, card_id):
        """Delete a memory card"""
        if messagebox.askyesno("Delete", "Are you sure you want to delete this memory card?"):
            if self.memory_engine.delete_person_card(card_id):
                messagebox.showinfo("Deleted", "Memory card has been deleted")
                self.refresh_memory_cards()
            else:
                messagebox.showerror("Error", "Failed to delete memory card")
