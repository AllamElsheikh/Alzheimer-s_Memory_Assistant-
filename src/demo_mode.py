"""
Interactive Demo Mode for فاكر؟ (Faker?) Alzheimer's Memory Assistant

This module provides a guided demonstration of the system's capabilities
without requiring full setup, making it easy for judges to evaluate.
"""

import os
import sys
import time
import random
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from core.arabic_dataset_loader import ArabicDatasetLoader
from core.intelligent_memory import IntelligentMemoryRetrieval
from ai.gemma_integration import GemmaIntegration

class DemoMode:
    """Interactive demo mode for the Alzheimer's Memory Assistant."""
    
    def __init__(self):
        """Initialize the demo mode."""
        self.print_welcome()
        
        # Initialize components with progress indicators
        print("🔄 Initializing Gemma 3n model...")
        try:
            self.gemma = GemmaIntegration(mock_mode=True)  # Use mock mode for demo
            print("✅ Gemma 3n model initialized (mock mode)")
        except Exception as e:
            print(f"⚠️ Gemma initialization error: {e}")
            print("⚠️ Continuing in mock mode")
            self.gemma = None
        
        print("🔄 Loading Arabic datasets...")
        self.dataset_loader = ArabicDatasetLoader()
        print("✅ Arabic datasets loaded")
        
        print("🔄 Initializing memory system...")
        self.memory_system = IntelligentMemoryRetrieval(self.gemma)
        print("✅ Memory system initialized")
        
        # Add some sample memories
        self._add_sample_memories()
        
        print("\n🚀 Demo mode ready! Let's begin the demonstration.\n")
        
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "=" * 80)
        print("""
        🧠 فاكر؟ (Faker?) - AI Memory Assistant
        
        Interactive Demo Mode
        
        Developed by 2survivors for the Google Gemma 3n Hackathon
        """)
        print("=" * 80 + "\n")
    
    def _add_sample_memories(self):
        """Add sample memories for demonstration."""
        # Add family memories
        self.memory_system.add_memory(
            content="زيارة حديقة الأزهر مع العائلة في الصيف الماضي",
            source="conversation",
            tags=["family", "outdoors", "summer"],
            importance=0.8,
            metadata={"location": "Cairo", "people": ["Ahmed", "Fatima", "Layla"]}
        )
        
        self.memory_system.add_memory(
            content="الاحتفال بعيد ميلاد الحفيد محمد الخامس",
            source="photo",
            tags=["family", "birthday", "grandson"],
            importance=0.9,
            metadata={"location": "home", "people": ["Mohamed", "family"]}
        )
        
        self.memory_system.add_memory(
            content="رحلة إلى الإسكندرية في عام 2010",
            source="conversation",
            tags=["travel", "alexandria", "vacation"],
            importance=0.7,
            metadata={"location": "Alexandria", "people": ["family"]}
        )
        
        print("📝 Added 3 sample memories for demonstration")
    
    def run_demo(self):
        """Run the interactive demo."""
        while True:
            print("\n" + "-" * 50)
            print("📋 Demo Menu:")
            print("1️⃣ Memory Prompt Demonstration")
            print("2️⃣ Cultural Entity Recognition")
            print("3️⃣ Memory Retrieval System")
            print("4️⃣ Conversation Simulation")
            print("5️⃣ Dataset Exploration")
            print("0️⃣ Exit Demo")
            print("-" * 50)
            
            choice = input("👉 Enter your choice (0-5): ")
            
            if choice == '0':
                print("\n👋 Thank you for exploring فاكر؟ (Faker?) - AI Memory Assistant!")
                break
            elif choice == '1':
                self.demo_memory_prompts()
            elif choice == '2':
                self.demo_cultural_entities()
            elif choice == '3':
                self.demo_memory_retrieval()
            elif choice == '4':
                self.demo_conversation()
            elif choice == '5':
                self.demo_dataset_exploration()
            else:
                print("⚠️ Invalid choice. Please try again.")
    
    def demo_memory_prompts(self):
        """Demonstrate memory prompts."""
        print("\n🧠 Memory Prompt Demonstration")
        print("This feature helps stimulate memories through culturally appropriate prompts.")
        
        # Show different types of prompts
        print("\n👨‍👩‍👧‍👦 Family Prompts:")
        for _ in range(3):
            prompt_data = self.dataset_loader.get_random_prompt('family_prompts')
            print(f"  🇪🇬 {prompt_data.get('prompt', '')}")
            print(f"  🇺🇸 {prompt_data.get('original_data', {}).get('prompt_en', '')}")
            print()
            time.sleep(1)
        
        print("\n🕌 Religious Prompts:")
        for _ in range(2):
            prompt_data = self.dataset_loader.get_random_prompt('religious_prompts')
            print(f"  🇪🇬 {prompt_data.get('prompt', '')}")
            print(f"  🇺🇸 {prompt_data.get('original_data', {}).get('prompt_en', '')}")
            print()
            time.sleep(1)
        
        print("\n🏛️ Historical Event Prompts:")
        prompt_data = self.dataset_loader.get_random_prompt('historical_events')
        print(f"  🇪🇬 {prompt_data.get('prompt', '')}")
        print(f"  🇺🇸 {prompt_data.get('original_data', {}).get('prompt_en', '')}")
        print()
        
        input("\nPress Enter to return to the main menu...")
    
    def demo_cultural_entities(self):
        """Demonstrate cultural entity recognition."""
        print("\n🍽️ Cultural Entity Recognition")
        print("This feature helps recognize and discuss culturally significant items.")
        
        # Show different types of entities
        print("\n🍲 Traditional Foods:")
        food = self.dataset_loader.get_random_entity(dataset_name='traditional_foods')
        print(f"  🇪🇬 {food.get('name_ar', '')}: {food.get('description_ar', '')}")
        print(f"  🇺🇸 {food.get('name_en', '')}: {food.get('description_en', '')}")
        print(f"  📍 Region: {', '.join(food.get('region', []))}")
        print(f"  💬 Prompt: {food.get('memory_prompt_ar', '')}")
        print()
        time.sleep(1)
        
        print("\n🎵 Traditional Songs:")
        song = self.dataset_loader.get_random_entity(dataset_name='traditional_songs')
        print(f"  🇪🇬 {song.get('title_ar', '')} - {song.get('artist', '')}")
        print(f"  🇺🇸 {song.get('title_en', '')} - {song.get('artist_en', '')}")
        print(f"  📍 Country: {song.get('country', '')}")
        print(f"  📅 Year: {song.get('year', 'Traditional')}")
        print(f"  💬 Prompt: {song.get('memory_prompt_ar', '')}")
        print()
        time.sleep(1)
        
        print("\n📜 Arabic Proverbs:")
        proverb = self.dataset_loader.get_random_entity(dataset_name='arabic_proverbs')
        print(f"  🇪🇬 {proverb.get('proverb_ar', '')}")
        print(f"  🇺🇸 {proverb.get('proverb_en', '')}")
        print(f"  📝 Explanation: {proverb.get('explanation_ar', '')}")
        print(f"  💬 Prompt: {proverb.get('memory_prompt_ar', '')}")
        print()
        
        input("\nPress Enter to return to the main menu...")
    
    def demo_memory_retrieval(self):
        """Demonstrate memory retrieval system."""
        print("\n🔍 Memory Retrieval System")
        print("This feature helps retrieve relevant memories based on context.")
        
        # Show the sample memories
        print("\n📝 Sample Memories:")
        for i, memory in enumerate(self.memory_system.memories):
            print(f"  {i+1}. {memory.content}")
            print(f"     Tags: {', '.join(memory.tags)}")
            print(f"     Importance: {memory.importance:.1f}")
            print()
        
        # Demonstrate memory retrieval
        print("\n🔎 Memory Retrieval Examples:")
        
        print("\n1️⃣ Searching for 'عائلة' (family):")
        memories = self.memory_system.retrieve_memories("عائلة")
        for memory in memories:
            print(f"  ✅ Found: {memory.content}")
            print(f"     Tags: {', '.join(memory.tags)}")
            print()
        
        print("\n2️⃣ Searching for 'رحلة' (trip):")
        memories = self.memory_system.retrieve_memories("رحلة")
        for memory in memories:
            print(f"  ✅ Found: {memory.content}")
            print(f"     Tags: {', '.join(memory.tags)}")
            print()
        
        # Demonstrate memory prompt generation
        print("\n3️⃣ Generating Memory Prompt:")
        prompt, memory = self.memory_system.generate_memory_prompt()
        if memory:
            print(f"  💬 Prompt: {prompt}")
            print(f"  📝 Based on memory: {memory.content}")
        else:
            print(f"  💬 Cultural prompt: {prompt}")
        
        input("\nPress Enter to return to the main menu...")
    
    def demo_conversation(self):
        """Demonstrate conversation simulation."""
        print("\n💬 Conversation Simulation")
        print("This feature demonstrates how the system converses with patients.")
        
        # Simulate a conversation
        print("\n🤖 Starting conversation simulation...")
        print("\n" + "~" * 50)
        
        print("🤖 فاكر؟: السلام عليكم! كيف حالك اليوم؟")
        user_input = input("👤 أنت: ")
        
        print("\n🤖 فاكر؟: الحمد لله. هل تسمح لي أن أسألك بعض الأسئلة لتنشيط الذاكرة؟")
        user_input = input("👤 أنت: ")
        
        # Get a random cultural prompt
        prompt_data = self.dataset_loader.get_random_prompt('family_prompts')
        print(f"\n🤖 فاكر؟: {prompt_data.get('prompt', '')}")
        user_input = input("👤 أنت: ")
        
        # Analyze the response
        print("\n🔄 Analyzing response...")
        time.sleep(1)
        print("✅ Analysis complete")
        
        print("\n🤖 فاكر؟: شكراً لمشاركتك هذه الذكريات. هل تحب أن أريك صورة عائلتك؟")
        user_input = input("👤 أنت: ")
        
        print("\n🤖 فاكر؟: حسناً، سأعرض لك صورة من الألبوم العائلي.")
        print("📸 [Displaying family photo simulation]")
        time.sleep(1)
        
        print("\n🤖 فاكر؟: هل تتذكر هذه الصورة؟ إنها من رحلتكم إلى الإسكندرية في عام 2010.")
        user_input = input("👤 أنت: ")
        
        print("\n🤖 فاكر؟: نعم، كانت رحلة جميلة! هل تتذكر الطعام الذي تناولتموه هناك؟")
        
        # Get a random food entity
        food = self.dataset_loader.get_random_entity(dataset_name='traditional_foods')
        print(f"\n🤖 فاكر؟: هل أكلتم {food.get('name_ar', '')} هناك؟")
        user_input = input("👤 أنت: ")
        
        print("\n🤖 فاكر؟: شكراً لمشاركتك هذه الذكريات الجميلة. سأذكرك بموعد الدواء بعد قليل.")
        print("\n" + "~" * 50)
        
        input("\nPress Enter to return to the main menu...")
    
    def demo_dataset_exploration(self):
        """Demonstrate dataset exploration."""
        print("\n📊 Dataset Exploration")
        print("This feature allows exploration of the Arabic cultural datasets.")
        
        # Show dataset statistics
        stats = self.memory_system.get_dataset_statistics()
        
        print("\n📈 Dataset Statistics:")
        print(f"  Cultural Entities Datasets: {stats['cultural_entities']['datasets']}")
        print(f"  Memory Prompts Datasets: {stats['memory_prompts']['datasets']}")
        
        print("\n📋 Cultural Entity Categories:")
        for category in stats['cultural_entities']['available_categories']:
            print(f"  - {category}")
        
        print("\n📋 Memory Prompt Categories:")
        for category in stats['memory_prompts']['available_categories']:
            print(f"  - {category}")
        
        # Allow exploration of specific datasets
        print("\n🔍 Explore Specific Dataset:")
        print("1️⃣ Traditional Foods")
        print("2️⃣ Traditional Songs")
        print("3️⃣ Arabic Proverbs")
        print("4️⃣ Family Prompts")
        print("5️⃣ Religious Prompts")
        print("0️⃣ Return to Main Menu")
        
        choice = input("\n👉 Enter your choice (0-5): ")
        
        dataset_mapping = {
            '1': 'traditional_foods',
            '2': 'traditional_songs',
            '3': 'arabic_proverbs',
            '4': 'family_prompts',
            '5': 'religious_prompts'
        }
        
        if choice in dataset_mapping:
            dataset_name = dataset_mapping[choice]
            dataset = self.dataset_loader.get_dataset(dataset_name)
            
            # Get the key for the items list
            items_key = next(iter(dataset.keys()), None)
            if items_key and dataset[items_key]:
                print(f"\n📂 {dataset_name} ({len(dataset[items_key])} items):")
                
                # Show 3 random items
                items = random.sample(dataset[items_key], min(3, len(dataset[items_key])))
                for item in items:
                    print("\n" + "-" * 40)
                    for key, value in item.items():
                        if isinstance(value, list):
                            print(f"  {key}: {', '.join(value)}")
                        else:
                            print(f"  {key}: {value}")
        
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    demo = DemoMode()
    demo.run_demo() 