# Arabic Datasets for Alzheimer's Memory Assistant (فاكر؟)

This directory contains culturally appropriate Arabic datasets designed for the "فاكر؟" (Faker?) Alzheimer's Memory Assistant. These datasets are specifically created to provide memory prompts and cultural references that are familiar to Arabic-speaking elderly individuals, especially those with Alzheimer's disease.

## Directory Structure

```
arabic_datasets/
├── cultural_entities/        # Cultural entities that might trigger memories
│   ├── arab_entities.json    # General Arab cultural entities
│   ├── arabic_names.json     # Common Arabic names
│   ├── arabic_proverbs.json  # Traditional Arabic proverbs
│   ├── traditional_foods.json # Traditional Arabic foods
│   └── traditional_songs.json # Traditional Arabic songs and music
├── memory_prompts/           # Prompts designed to trigger memories
│   ├── family_prompts.json   # Prompts related to family
│   ├── historical_events.json # Prompts related to historical events
│   ├── places_prompts.json   # Prompts related to places
│   └── religious_prompts.json # Prompts related to religious practices
└── arabic_speech_samples/    # Directory for Arabic speech samples (empty placeholder)
```

## Dataset Descriptions

### Cultural Entities

1. **Arab Entities (`arab_entities.json`)**: 
   - Contains various cultural entities categorized by type (food, celebration, tradition, landmark, music)
   - Each entity includes Arabic and English names, descriptions, and cultural context

2. **Arabic Names (`arabic_names.json`)**: 
   - Common Arabic names for males and females
   - Includes meaning, origin, and popularity information

3. **Arabic Proverbs (`arabic_proverbs.json`)**: 
   - Traditional Arabic proverbs and sayings
   - Includes explanations and memory prompts related to each proverb

4. **Traditional Foods (`traditional_foods.json`)**: 
   - Traditional Arabic dishes from various regions
   - Includes descriptions and memory prompts related to each food

5. **Traditional Songs (`traditional_songs.json`)**: 
   - Famous Arabic songs and music that might trigger memories
   - Includes artist information, year, and memory prompts

### Memory Prompts

1. **Family Prompts (`family_prompts.json`)**: 
   - Questions about family members and family life
   - Categorized by difficulty level (easy, medium, hard)

2. **Historical Events (`historical_events.json`)**: 
   - Significant historical events in the Arab world
   - Includes year, region, and memory prompts

3. **Places Prompts (`places_prompts.json`)**: 
   - Questions about places and locations that might be familiar
   - Categorized by type (personal location, home, education, etc.)

4. **Religious Prompts (`religious_prompts.json`)**: 
   - Questions related to religious practices and memories
   - Covers both Islamic and Christian traditions

## Data Format

All datasets are provided in JSON format with bilingual content (Arabic and English). Each entry typically includes:

- Unique identifier
- Arabic text
- English translation
- Category or type
- Additional metadata specific to the entity type
- Memory prompts in both Arabic and English

## Usage

These datasets are designed to be used by the "فاكر؟" (Faker?) Alzheimer's Memory Assistant to:

1. Generate culturally appropriate conversation prompts
2. Recognize and respond to cultural references
3. Provide context-aware memory assistance
4. Support bilingual interactions

## Contributing

To expand these datasets:

1. Follow the existing JSON structure
2. Ensure all entries have both Arabic and English text
3. Include appropriate metadata for categorization
4. Add memory prompts that might help trigger recollections

## License

These datasets are part of the "فاكر؟" (Faker?) Alzheimer's Memory Assistant project and are subject to the same licensing terms as the main project. 