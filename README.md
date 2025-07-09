# Alzheimer-s_Memory_Assistant
## 🎯 About
The Alzheimer's Memory Assistant is a privacy-first, offline-capable application that uses AI to help individuals with Alzheimer's disease and dementia maintain their daily routines, remember important people, and stay connected with their families. Built with empathy and designed for simplicity.
### Why This Project Matters

25+ million people worldwide live with Alzheimer's disease
Simple technology can significantly improve quality of life
Privacy and dignity are fundamental rights for all patients
Offline functionality ensures reliability when it matters most

## ✨ Features
### 🏠 Core Memory Features

Personal Memory Cards - Photo-based reminders of family and friends
Face Recognition - Identify people in photos automatically
Voice-Activated Recall - "Who is this person?" voice commands
Smart Reminders - Medication, appointments, and daily tasks

### 🧩 Daily Living Support

Daily Routine Assistant - Step-by-step guidance for daily activities
Emergency Contact System - Quick access to family and emergency contacts
Home Navigation - Visual map of home with room labels
Item Finder - Remember where common items are placed

### 🔒 Privacy & Security

100% Offline AI - Uses local Llama 3 model for privacy
Encrypted Storage - All personal data encrypted locally
No Data Collection - Your memories stay on your device
HIPAA Considerations - Designed with medical privacy in mind

## 🚀 Getting Started
### Prerequisites

Python 3.8 or higher
4GB RAM minimum (8GB recommended)
10GB free storage space
Microphone and speakers/headphones
Webcam (optional, for face recognition)

### Quick Start
```
bash# Clone the repository
git clone https://github.com/yourusername/alzheimer-memory-assistant.git
cd alzheimer-memory-assistant

# Run the setup script
python scripts/setup_environment.py

# Install dependencies
pip install -r requirements/requirements.txt

# Download offline AI models
python scripts/download_models.py

# Launch the application
python src/main.py
```
## Project structure 
```
alzheimer-memory-assistant/
├── README.md
├── LICENSE
|
├── src/
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── database_config.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── memory_engine.py
│   │   ├── reminder_system.py
│   │   ├── voice_processor.py
│   │   └── image_recognition.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── memory_cards.py
│   │   ├── reminder_interface.py
│   │   └── simple_interface.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llama_integration.py
│   │   ├── offline_nlp.py
│   │   └── context_manager.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── backup_manager.py
│   │   └── export_handler.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── audio_utils.py
│   │   ├── image_utils.py
│   │   ├── date_time_helpers.py
│   │   └── accessibility_helpers.py
│   │
│   └── security/
│       ├── __init__.py
│       ├── encryption.py
│       └── privacy_manager.py
│
├── tests/
│   ├── __init__.py
│   ├── test_memory_engine.py
│   ├── test_reminder_system.py
│   ├── test_ai_integration.py
│   ├── test_ui_components.py
│   └── test_data_handling.py
│
├── data/
│   ├── sample_data/
│   │   ├── sample_memories.json
│   │   ├── sample_reminders.json
│   │   └── sample_photos/
│   │
│   ├── templates/
│   │   ├── memory_card_template.json
│   │   ├── reminder_template.json
│   │   └── person_profile_template.json
│   │
│   └── models/
│       ├── offline_nlp_model/
│       └── image_recognition_model/
│
├── resources/
│   ├── icons/
│   ├── sounds/
│   │   ├── notification_sounds/
│   │   └── voice_prompts/
│   ├── images/
│   │   ├── ui_elements/
│   │   └── memory_aids/
│   └── fonts/
│
├── scripts/
│   ├── setup_environment.py
│   ├── install_dependencies.py
│   ├── backup_data.py
│   └── migrate_data.py
│
├── config/
│   ├── app_config.yaml
│   ├── ai_model_config.yaml
│   └── accessibility_config.yaml
│
├── requirements/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── requirements-offline.txt
│
├── deployment/
│   ├── installer/
│   │   ├── windows_installer.nsi
│   │   ├── mac_installer.py
│   │   └── linux_installer.sh
│   │
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── distribution/
│       ├── build_release.py
│       └── package_app.py
│
├── medical/
│   ├── guidelines/
│   │   ├── alzheimer_considerations.md
│   │   ├── memory_techniques.md
│   │   └── caregiver_best_practices.md
│   │
│   └── research/
│       ├── memory_studies.md
│       └── assistive_technology_research.md
│
└── examples/
    ├── basic_usage.py
    ├── caregiver_setup.py
    ├── memory_card_creation.py
    └── reminder_configuration.py
```
## 📦 Installation
For Patients and Families (Easy Installation)
Download the installer from our Releases page
Run the installer and follow the simple setup wizard
Launch the app from your desktop or start menu

### For Developers
```
# Development setup
git clone https://github.com/AllamElsheikh/alzheimer-memory-assistant.git
cd alzheimer-memory-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements/requirements-dev.txt

# Run tests
python -m pytest tests/

# Start development server
python src/main.py --dev
```
## 🎯 Usage
### First-Time Setup

Launch the application
Choose your interface style (Simple, Standard, or Caregiver)
Add family photos to create memory cards
Set up daily reminders for medications and appointments
Record voice notes about important people and places

### Daily Use
python# Example: Adding a memory card
from src.core.memory_engine import MemoryEngine

memory = MemoryEngine()
memory.add_person_card(
    name="Sarah Johnson",
    relationship="Daughter",
    photo_path="photos/sarah.jpg",
    notes="Lives in Chicago, has two children"
)
### Voice Commands

"Who is this person?" - Identify someone in a photo
"Remind me to take medicine" - Set a medication reminder
"Call my daughter" - Quick access to emergency contacts
"What's my schedule today?" - Review daily reminders

## 👨‍⚕️ For Caregivers
### Caregiver Dashboard
Access the caregiver dashboard to:

Monitor daily app usage
Update memory cards remotely
Adjust reminder schedules
View emergency contact logs
Export memory data for medical visits

### Setup Guide

Install the app on the patient's device
Create caregiver account with secure access code
Upload family photos and create memory cards
Configure daily reminders for medications and activities
Set up emergency contacts with photos and phone numbers
Test voice commands and adjust sensitivity

### Best Practices

Keep it simple - Less is more for cognitive accessibility
Regular updates - Add new photos and update information
Routine-based - Integrate with existing daily routines
Patient-centered - Let the patient guide the interaction
Privacy first - Never share personal data without consent

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
  <p><strong>Built with ❤️ for the Alzheimer's community</strong></p>
  <p>Made by developers who believe technology should serve humanity's most vulnerable</p>
</div>
