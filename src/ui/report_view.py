import customtkinter as ctk

class ReportView(ctk.CTkFrame):
    """The view for displaying patient reports."""

    def __init__(self, parent, controller):
        """Initializes the ReportView frame."""
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Patient Reports", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Placeholder for report content
        self.report_content_label = ctk.CTkLabel(self, text="Interaction logs and analysis will be displayed here.", font=ctk.CTkFont(size=16))
        self.report_content_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
