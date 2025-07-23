"""
Test script for the integration of Arabic cultural datasets with the intelligent memory system.
"""

import sys
import os
import random
from intelligent_memory import IntelligentMemoryRetrieval

def test_cultural_integration():
    """Test the integration of cultural datasets with the memory system."""
    print("Testing Cultural Integration with Intelligent Memory System...")
    
    # Initialize the memory system without Gemma integration for testing
    memory_system = IntelligentMemoryRetrieval(gemma_integration=None)
    
    # Test 1: Generate memory prompts using cultural datasets
    print("\n1. Testing cultural memory prompts...")
    for _ in range(5):
        prompt, memory = memory_system.generate_memory_prompt(use_cultural_prompts=True)
        print(f"  Prompt: {prompt}")
        print(f"  Memory returned: {'Yes' if memory else 'No (using cultural dataset)'}")
        print("  ---")
    
    # Test 2: Generate entity-specific cultural prompts
    print("\n2. Testing entity-specific cultural prompts...")
    entity_types = ['food', 'music', 'proverb']
    for entity_type in entity_types:
        prompt = memory_system.get_cultural_entity_prompt(entity_type=entity_type)
        print(f"  {entity_type.capitalize()} prompt: {prompt}")
    
    # Test 3: Test random entity prompt
    print("\n3. Testing random cultural entity prompt...")
    prompt = memory_system.get_cultural_entity_prompt()
    print(f"  Random entity prompt: {prompt}")
    
    # Test 4: Test analyzing cultural responses
    print("\n4. Testing cultural response analysis...")
    test_responses = [
        "نعم، أتذكر هذه الأغنية جيداً. كنت أستمع إليها كثيراً في شبابي.",
        "لا، لا أعرف هذا المثل.",
        "أحب هذا الطعام كثيراً، كانت والدتي تطبخه لنا في المناسبات الخاصة."
    ]
    
    for response in test_responses:
        analysis = memory_system.analyze_cultural_response("سؤال ثقافي", response)
        print(f"  Response: {response[:30]}...")
        print(f"  Analysis: {analysis}")
        print("  ---")
    
    # Test 5: Check dataset statistics
    print("\n5. Testing dataset statistics...")
    stats = memory_system.get_dataset_statistics()
    print(f"  Cultural entities datasets: {stats['cultural_entities']['datasets']}")
    print(f"  Memory prompts datasets: {stats['memory_prompts']['datasets']}")
    print(f"  Cultural entity categories: {stats['cultural_entities']['available_categories']}")
    print(f"  Memory prompt categories: {stats['memory_prompts']['available_categories']}")
    
    # All tests passed
    print("\n✅ All tests completed!")
    return True

def main():
    """Main function to run the tests."""
    success = test_cultural_integration()
    if not success:
        print("\n❌ Some tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main() 