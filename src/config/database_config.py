import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

# Assuming settings.py is in the same directory
from .settings import Settings

class DatabaseConfig:
    """Database configuration and setup"""

    def __init__(self, settings: Settings):
        """
        Initializes the DatabaseConfig object.

        Args:
            settings (Settings): The application settings object.
        """
        self.settings = settings
        self.db_path = Path(self.settings.get_data_directory()) / 'memory_assistant.db'
        self._ensure_db_directory_exists()
        self.connection = self.get_connection()
        self.create_tables()

    def _ensure_db_directory_exists(self):
        """Ensures that the directory for the database file exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self):
        """Establishes and returns a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Access columns by name
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def create_tables(self):
        """Creates the necessary database tables if they don't already exist."""
        if not self.connection:
            return

        cursor = self.connection.cursor()
        try:
            # Table for storing information about people (Memory Cards)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS person_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                relationship TEXT,
                photo_path TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Table for storing reminders
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TIMESTAMP NOT NULL,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()

    def setup_encryption(self):
        """
        Placeholder for setting up database encryption.
        NOTE: Standard sqlite3 does not support encryption out-of-the-box.
              This would require a library like SQLCipher.
        """
        print("Encryption setup is not implemented in this version.")
        pass

    def backup_database(self):
        """Creates a timestamped backup of the database file."""
        if not self.db_path.exists():
            print("Database file not found. Cannot create backup.")
            return

        backup_dir = Path(self.settings.get_data_directory()) / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.db"

        try:
            shutil.copy2(self.db_path, backup_file)
            print(f"Database backup created at {backup_file}")
            return str(backup_file)
        except IOError as e:
            print(f"Error creating backup: {e}")
            return None

    def close_connection(self):
        """Closes the database connection if it's open."""
        if self.connection:
            self.connection.close()
