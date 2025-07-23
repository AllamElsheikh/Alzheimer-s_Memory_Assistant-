"""
Arabic Dataset Loader for فاكر؟ (Faker?) Alzheimer's Memory Assistant.

This module provides utilities for loading and accessing the Arabic datasets
used for memory prompts and cultural entity recognition.
"""

import json
import os
import random
from typing import Dict, List, Optional, Union, Any

class ArabicDatasetLoader:
    """Loader for Arabic datasets used in the Alzheimer's Memory Assistant."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the dataset loader.
        
        Args:
            data_dir: Path to the data directory. If None, uses default path.
        """
        if data_dir is None:
            # Try to find the data directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', 'arabic_datasets')
        else:
            self.data_dir = data_dir
            
        self.index_path = os.path.join(self.data_dir, 'dataset_index.json')
        self.index = self._load_index()
        self.datasets = {}
        
    def _load_index(self) -> Dict:
        """Load the dataset index file."""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading index file: {e}")
            return {"datasets": {"cultural_entities": [], "memory_prompts": []}}
    
    def _load_dataset(self, dataset_name: str) -> Dict:
        """
        Load a specific dataset by name.
        
        Args:
            dataset_name: Name of the dataset to load
            
        Returns:
            The loaded dataset as a dictionary
        """
        # Find the dataset in the index
        dataset_info = None
        for category in ['cultural_entities', 'memory_prompts']:
            for dataset in self.index['datasets'].get(category, []):
                if dataset['name'] == dataset_name:
                    dataset_info = dataset
                    break
            if dataset_info:
                break
                
        if not dataset_info:
            print(f"Dataset '{dataset_name}' not found in index")
            return {}
            
        # Load the dataset
        file_path = os.path.join(self.data_dir, dataset_info['file'])
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading dataset '{dataset_name}': {e}")
            return {}
    
    def get_dataset(self, dataset_name: str) -> Dict:
        """
        Get a dataset by name, loading it if necessary.
        
        Args:
            dataset_name: Name of the dataset to get
            
        Returns:
            The dataset as a dictionary
        """
        if dataset_name not in self.datasets:
            self.datasets[dataset_name] = self._load_dataset(dataset_name)
        return self.datasets[dataset_name]
    
    def get_random_prompt(self, dataset_name: str, category: str = None, 
                          difficulty: str = None, language: str = 'ar') -> Dict:
        """
        Get a random prompt from a memory prompt dataset.
        
        Args:
            dataset_name: Name of the dataset to get the prompt from
            category: Optional category to filter by
            difficulty: Optional difficulty level to filter by
            language: Language for the prompt ('ar' for Arabic, 'en' for English)
            
        Returns:
            A dictionary containing the prompt and its metadata
        """
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            return {}
            
        # Get the key for the prompts list (usually the dataset name)
        prompts_key = next(iter(dataset.keys()), None)
        if not prompts_key:
            return {}
            
        prompts = dataset[prompts_key]
        
        # Filter by category and difficulty if provided
        filtered_prompts = prompts
        if category:
            filtered_prompts = [p for p in filtered_prompts if p.get('category') == category]
        if difficulty:
            filtered_prompts = [p for p in filtered_prompts if p.get('difficulty') == difficulty]
            
        if not filtered_prompts:
            return {}
            
        # Select a random prompt
        prompt = random.choice(filtered_prompts)
        
        # Format the result based on the requested language
        prompt_text = prompt.get(f'prompt_{language}', prompt.get('prompt_ar', ''))
        
        return {
            'id': prompt.get('id', ''),
            'prompt': prompt_text,
            'category': prompt.get('category', ''),
            'difficulty': prompt.get('difficulty', ''),
            'original_data': prompt
        }
    
    def get_entity_by_name(self, entity_name: str, dataset_name: str = None, 
                          language: str = 'ar') -> Dict:
        """
        Find an entity by name in the cultural entities datasets.
        
        Args:
            entity_name: Name of the entity to find
            dataset_name: Optional specific dataset to search in
            language: Language of the entity name ('ar' for Arabic, 'en' for English)
            
        Returns:
            The entity data if found, empty dict otherwise
        """
        # Determine which datasets to search
        if dataset_name:
            datasets_to_search = [dataset_name]
        else:
            # Search all cultural entity datasets
            datasets_to_search = [
                dataset['name'] for dataset in 
                self.index['datasets'].get('cultural_entities', [])
            ]
        
        # Search for the entity
        name_field = f'name_{language}' if language == 'en' else 'name_ar'
        
        for ds_name in datasets_to_search:
            dataset = self.get_dataset(ds_name)
            if not dataset:
                continue
                
            # Get the key for the entities list
            entities_key = next(iter(dataset.keys()), None)
            if not entities_key:
                continue
                
            entities = dataset[entities_key]
            
            # Look for matching entity
            for entity in entities:
                if entity.get(name_field, '').lower() == entity_name.lower():
                    return entity
                    
        return {}
    
    def get_entities_by_category(self, category: str, dataset_name: str = None) -> List[Dict]:
        """
        Get entities by category.
        
        Args:
            category: Category to filter by
            dataset_name: Optional specific dataset to search in
            
        Returns:
            List of matching entities
        """
        # Determine which datasets to search
        if dataset_name:
            datasets_to_search = [dataset_name]
        else:
            # Get datasets that have this category
            datasets_to_search = []
            for dataset in self.index['datasets'].get('cultural_entities', []):
                if category in dataset.get('categories', []):
                    datasets_to_search.append(dataset['name'])
        
        results = []
        
        for ds_name in datasets_to_search:
            dataset = self.get_dataset(ds_name)
            if not dataset:
                continue
                
            # Get the key for the entities list
            entities_key = next(iter(dataset.keys()), None)
            if not entities_key:
                continue
                
            entities = dataset[entities_key]
            
            # Look for matching entities
            for entity in entities:
                entity_category = entity.get('category', '')
                if entity_category == category:
                    results.append(entity)
                    
        return results
    
    def get_random_entity(self, category: str = None, 
                         dataset_name: str = None) -> Dict:
        """
        Get a random entity, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            dataset_name: Optional specific dataset to get from
            
        Returns:
            A random entity
        """
        if category:
            entities = self.get_entities_by_category(category, dataset_name)
            if entities:
                return random.choice(entities)
            return {}
        
        # No category specified, get a random entity from any dataset
        if dataset_name:
            datasets_to_search = [dataset_name]
        else:
            datasets_to_search = [
                dataset['name'] for dataset in 
                self.index['datasets'].get('cultural_entities', [])
            ]
            
        # Shuffle the datasets for randomness
        random.shuffle(datasets_to_search)
        
        for ds_name in datasets_to_search:
            dataset = self.get_dataset(ds_name)
            if not dataset:
                continue
                
            # Get the key for the entities list
            entities_key = next(iter(dataset.keys()), None)
            if not entities_key:
                continue
                
            entities = dataset[entities_key]
            if entities:
                return random.choice(entities)
                
        return {}
    
    def get_available_datasets(self) -> Dict:
        """
        Get information about all available datasets.
        
        Returns:
            Dictionary with information about available datasets
        """
        return {
            'cultural_entities': self.index['datasets'].get('cultural_entities', []),
            'memory_prompts': self.index['datasets'].get('memory_prompts', [])
        }
    
    def get_available_categories(self) -> Dict:
        """
        Get all available categories across datasets.
        
        Returns:
            Dictionary with categories by dataset type
        """
        categories = {
            'cultural_entities': set(),
            'memory_prompts': set()
        }
        
        for dataset_type, datasets in self.index['datasets'].items():
            for dataset in datasets:
                for category in dataset.get('categories', []):
                    categories[dataset_type].add(category)
                    
        return {
            'cultural_entities': list(categories['cultural_entities']),
            'memory_prompts': list(categories['memory_prompts'])
        }


# Example usage
if __name__ == "__main__":
    loader = ArabicDatasetLoader()
    
    # Print available datasets
    print("Available datasets:")
    available = loader.get_available_datasets()
    for dataset_type, datasets in available.items():
        print(f"  {dataset_type}:")
        for dataset in datasets:
            print(f"    - {dataset['name']}: {dataset['description']} ({dataset['count']} items)")
    
    # Get a random family prompt
    family_prompt = loader.get_random_prompt('family_prompts')
    print("\nRandom family prompt:")
    print(f"  {family_prompt.get('prompt', '')}")
    
    # Get a random food entity
    food = loader.get_random_entity(category='food')
    print("\nRandom food entity:")
    if food:
        print(f"  {food.get('name_ar', '')}: {food.get('description_ar', '')}") 