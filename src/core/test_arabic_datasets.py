"""
Test script for the Arabic dataset loader.
"""

import sys
import os
import json
from arabic_dataset_loader import ArabicDatasetLoader

def test_dataset_loader():
    """Test the Arabic dataset loader functionality."""
    print("Testing Arabic Dataset Loader...")
    
    # Initialize the loader
    loader = ArabicDatasetLoader()
    
    # Test 1: Check if datasets are available
    print("\n1. Checking available datasets...")
    available_datasets = loader.get_available_datasets()
    if not available_datasets['cultural_entities'] or not available_datasets['memory_prompts']:
        print("❌ No datasets found!")
        return False
    
    print("✅ Found datasets:")
    for dataset_type, datasets in available_datasets.items():
        print(f"  {dataset_type}: {len(datasets)} datasets")
        for dataset in datasets:
            print(f"    - {dataset['name']}")
    
    # Test 2: Load a specific dataset
    print("\n2. Loading 'family_prompts' dataset...")
    family_prompts = loader.get_dataset('family_prompts')
    if not family_prompts:
        print("❌ Failed to load family_prompts dataset!")
        return False
    
    # Check if the dataset has the expected structure
    if 'family_prompts' not in family_prompts:
        print("❌ Dataset has unexpected structure!")
        return False
    
    print(f"✅ Successfully loaded dataset with {len(family_prompts['family_prompts'])} prompts")
    
    # Test 3: Get random prompts
    print("\n3. Testing random prompt retrieval...")
    # Get a random family prompt
    prompt = loader.get_random_prompt('family_prompts')
    if not prompt:
        print("❌ Failed to get random family prompt!")
        return False
    
    print("✅ Random family prompt:")
    print(f"  ID: {prompt.get('id')}")
    print(f"  Prompt: {prompt.get('prompt')}")
    print(f"  Category: {prompt.get('category')}")
    print(f"  Difficulty: {prompt.get('difficulty')}")
    
    # Test 4: Get prompts with filters
    print("\n4. Testing filtered prompt retrieval...")
    # Get a random family prompt with medium difficulty
    prompt = loader.get_random_prompt('family_prompts', difficulty='medium')
    if not prompt or prompt.get('difficulty') != 'medium':
        print("❌ Failed to get filtered prompt by difficulty!")
        return False
    
    print("✅ Filtered prompt by difficulty 'medium':")
    print(f"  ID: {prompt.get('id')}")
    print(f"  Prompt: {prompt.get('prompt')}")
    print(f"  Difficulty: {prompt.get('difficulty')}")
    
    # Test 5: Get entity by category
    print("\n5. Testing entity retrieval by category...")
    # Get food entities
    food_entities = loader.get_entities_by_category('food')
    if not food_entities:
        print("❌ Failed to get food entities!")
        return False
    
    print(f"✅ Found {len(food_entities)} food entities")
    if food_entities:
        print(f"  Example: {food_entities[0].get('name_ar')} - {food_entities[0].get('description_ar')}")
    
    # Test 6: Get random entity
    print("\n6. Testing random entity retrieval...")
    # Get a random food entity
    entity = loader.get_random_entity(category='food')
    if not entity:
        print("❌ Failed to get random food entity!")
        return False
    
    print("✅ Random food entity:")
    print(f"  Name: {entity.get('name_ar')}")
    print(f"  Description: {entity.get('description_ar')}")
    
    # Test 7: Get entity by name
    print("\n7. Testing entity retrieval by name...")
    # Get an entity by name (using a name we know exists)
    entity_name = entity.get('name_ar')  # Use the name from the previous test
    found_entity = loader.get_entity_by_name(entity_name)
    if not found_entity:
        print(f"❌ Failed to find entity by name '{entity_name}'!")
        return False
    
    print(f"✅ Found entity by name '{entity_name}'")
    
    # Test 8: Get available categories
    print("\n8. Testing available categories retrieval...")
    categories = loader.get_available_categories()
    if not categories['cultural_entities'] or not categories['memory_prompts']:
        print("❌ Failed to get available categories!")
        return False
    
    print("✅ Available categories:")
    print(f"  Cultural entities: {', '.join(categories['cultural_entities'])}")
    print(f"  Memory prompts: {', '.join(categories['memory_prompts'])}")
    
    # All tests passed
    print("\n✅ All tests passed successfully!")
    return True

def main():
    """Main function to run the tests."""
    success = test_dataset_loader()
    if not success:
        print("\n❌ Some tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main() 