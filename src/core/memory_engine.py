import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class MemoryEngine:
    """Core memory management system for person cards and memories"""
    
    def __init__(self, data_file='data/person_cards.json'):
        """Initialize memory engine with data storage"""
        self.data_file = data_file
        self.person_cards = self._load_data()
        self.next_id = max([card.get('id', 0) for card in self.person_cards], default=0) + 1
        
    def _load_data(self) -> List[Dict]:
        """Load person cards from JSON file"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self):
        """Save person cards to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.person_cards, f, ensure_ascii=False, indent=4)
    
    def add_person_card(self, name: str, relationship: str, photo_path: str, notes: str = "") -> int:
        """Add a new person memory card"""
        person_card = {
            'id': self.next_id,
            'name': name,
            'relationship': relationship,
            'photo_path': photo_path,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'last_accessed': None,
            'access_count': 0
        }
        self.person_cards.append(person_card)
        self.next_id += 1
        self._save_data()
        return person_card['id']
    
    def get_person_by_name(self, name: str) -> Optional[Dict]:
        """Retrieve person by name"""
        for card in self.person_cards:
            if card['name'].lower() == name.lower():
                # Update access tracking
                card['last_accessed'] = datetime.now().isoformat()
                card['access_count'] = card.get('access_count', 0) + 1
                self._save_data()
                return card
        return None
    
    def get_person_by_id(self, person_id: int) -> Optional[Dict]:
        """Retrieve person by ID"""
        for card in self.person_cards:
            if card['id'] == person_id:
                return card
        return None
    
    def update_person_card(self, person_id: int, updates: Dict) -> bool:
        """Update existing person card"""
        for card in self.person_cards:
            if card['id'] == person_id:
                card.update(updates)
                card['updated_at'] = datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def delete_person_card(self, person_id: int) -> bool:
        """Delete person card"""
        original_length = len(self.person_cards)
        self.person_cards = [card for card in self.person_cards if card['id'] != person_id]
        if len(self.person_cards) < original_length:
            self._save_data()
            return True
        return False
    
    def search_memories(self, query: str) -> List[Dict]:
        """Search through memory cards"""
        query_lower = query.lower()
        results = []
        for card in self.person_cards:
            if (query_lower in card['name'].lower() or 
                query_lower in card.get('relationship', '').lower() or
                query_lower in card.get('notes', '').lower()):
                results.append(card)
        return results
    
    def get_all_cards(self) -> List[Dict]:
        """Get all person cards"""
        return self.person_cards.copy()
    
    def get_memory_suggestions(self, context: str = "") -> List[Dict]:
        """Get AI-powered memory suggestions based on recent interactions"""
        # Sort by recent access and access count for suggestions
        sorted_cards = sorted(
            self.person_cards,
            key=lambda x: (x.get('access_count', 0), x.get('last_accessed', '')),
            reverse=True
        )
        return sorted_cards[:5]  # Return top 5 suggestions
