import json
import os

class PromptManager:
    """Manages the creation, storage, and retrieval of memory prompts."""

    def __init__(self, prompts_file='data/memory_prompts.json'):
        """Initializes the PromptManager.

        Args:
            prompts_file (str): The path to the JSON file where prompts are stored.
        """
        self.prompts_file = prompts_file
        self.prompts = self.load_prompts()

    def load_prompts(self):
        """Loads prompts from the JSON file."""
        if not os.path.exists(self.prompts_file):
            # Create the data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.prompts_file), exist_ok=True)
            return []
        
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_prompts(self):
        """Saves the current list of prompts to the JSON file."""
        with open(self.prompts_file, 'w', encoding='utf-8') as f:
            json.dump(self.prompts, f, ensure_ascii=False, indent=4)

    def add_prompt(self, prompt_data):
        """Adds a new prompt and saves it.

        Args:
            prompt_data (dict): A dictionary containing the prompt's details,
                              e.g., {'text': '...', 'image_path': '...', 'audio_path': '...'}
        """
        self.prompts.append(prompt_data)
        self.save_prompts()

    def get_prompts(self):
        """Returns all prompts."""
        return self.prompts

    def delete_prompt(self, index):
        """Deletes a prompt by its index."""
        if 0 <= index < len(self.prompts):
            del self.prompts[index]
            self.save_prompts()
