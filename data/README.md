# Data Directory Structure

## Overview
This directory contains all data files required for the Alzheimer's Memory Assistant application.

## Structure

```
data/
├── patients/              # Patient profiles and information
├── images/
│   ├── family_photos/     # Patient family and friends photos
│   └── memory_prompts/    # Images used for memory stimulation
├── audio/
│   ├── recordings/        # Patient voice recordings
│   └── samples/          # Audio samples for testing
├── conversations/         # Conversation history and context
├── medical/              # Medical schedules and notes
└── person_cards.json     # Family/friend relationship data
```

## Required Files

### patients/
- `patient_profile.json` - Patient basic information
- `medical_history.json` - Medical background and current status

### conversations/
- `conversation_context.json` - Session history and context
- `cognitive_assessments.json` - Memory performance tracking

### medical/
- `medication_schedule.json` - Daily medication reminders
- `daily_routine.json` - Patient's daily schedule

## Data Privacy
All patient data must be:
- Anonymized for demo purposes
- Compliant with healthcare privacy regulations
- Stored locally (no cloud storage)
