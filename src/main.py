import sys
import os

# Ensure the project root is in the system path to allow for correct module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ui.main_window import MainWindow

if __name__ == "__main__":
    try:
        print("Initializing the application...")
        app = MainWindow()  # MainWindow is the root CTk window
        print("Starting the main event loop...")
        app.mainloop()      # This call blocks and runs the application
        print("Application has been closed.")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred during application startup: {e}")
        traceback.print_exc()
