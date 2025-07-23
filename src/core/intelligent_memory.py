import os
import json
import random
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MemoryItem:
    """Data class to represent a memory item"""
    memory_id: str
    content: str
    source: str  # 'conversation', 'photo', 'user_input', etc.
    timestamp: datetime.datetime
    importance: float  # 0.0 to 1.0
    tags: List[str]
    metadata: Dict[str, Any]
    last_accessed: Optional[datetime.datetime] = None
    access_count: int = 0

class IntelligentMemoryRetrieval:
    """
    Advanced memory management system for Alzheimer's patients using Gemma 3n.
    Provides intelligent memory retrieval, association, and reinforcement.
    """
    
    def __init__(self, gemma_integration=None, memory_file='data/intelligent_memories.json'):
        """Initialize the intelligent memory system"""
        self.gemma_integration = gemma_integration
        self.memory_file = memory_file
        self.memories = self._load_memories()
        self.memory_graph = {}  # For associative memory connections
        self.working_memory = []  # Recently accessed memories
        self.working_memory_size = 10
        self._build_memory_graph()
        
    def _load_memories(self) -> List[MemoryItem]:
        """Load memories from JSON file"""
        memories = []
        if not os.path.exists(self.memory_file):
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            return memories
            
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
                
            for item in memory_data:
                memory = MemoryItem(
                    memory_id=item['memory_id'],
                    content=item['content'],
                    source=item['source'],
                    timestamp=datetime.datetime.fromisoformat(item['timestamp']),
                    importance=item['importance'],
                    tags=item['tags'],
                    metadata=item['metadata'],
                    last_accessed=datetime.datetime.fromisoformat(item['last_accessed']) if item.get('last_accessed') else None,
                    access_count=item.get('access_count', 0)
                )
                memories.append(memory)
                
            return memories
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error loading memories: {e}")
            return []
    
    def _save_memories(self):
        """Save memories to JSON file"""
        memory_data = []
        for memory in self.memories:
            memory_dict = {
                'memory_id': memory.memory_id,
                'content': memory.content,
                'source': memory.source,
                'timestamp': memory.timestamp.isoformat(),
                'importance': memory.importance,
                'tags': memory.tags,
                'metadata': memory.metadata,
                'last_accessed': memory.last_accessed.isoformat() if memory.last_accessed else None,
                'access_count': memory.access_count
            }
            memory_data.append(memory_dict)
            
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=4)
    
    def _build_memory_graph(self):
        """Build associative memory graph for faster retrieval"""
        self.memory_graph = {}
        
        # Create nodes for each memory
        for memory in self.memories:
            self.memory_graph[memory.memory_id] = {
                'memory': memory,
                'connections': []
            }
        
        # Create connections between related memories
        for i, memory1 in enumerate(self.memories):
            for j, memory2 in enumerate(self.memories):
                if i != j:
                    # Calculate connection strength based on tag similarity
                    common_tags = set(memory1.tags).intersection(set(memory2.tags))
                    if common_tags:
                        connection_strength = len(common_tags) / max(len(memory1.tags), len(memory2.tags))
                        
                        # Add temporal proximity factor
                        time_diff = abs((memory1.timestamp - memory2.timestamp).total_seconds())
                        time_factor = 1.0 / (1.0 + (time_diff / (24 * 3600)))  # Normalize to 0-1 range
                        
                        # Combined strength
                        strength = 0.7 * connection_strength + 0.3 * time_factor
                        
                        if strength > 0.2:  # Only keep strong connections
                            self.memory_graph[memory1.memory_id]['connections'].append({
                                'target_id': memory2.memory_id,
                                'strength': strength
                            })
    
    def add_memory(self, content: str, source: str, tags: List[str], 
                  importance: float = 0.5, metadata: Dict[str, Any] = None) -> str:
        """
        Add a new memory to the system
        
        Args:
            content: The memory content
            source: Source of the memory (conversation, photo, etc.)
            tags: List of tags for categorization
            importance: Importance score (0.0 to 1.0)
            metadata: Additional metadata
            
        Returns:
            memory_id: ID of the created memory
        """
        # Generate unique ID
        memory_id = f"mem_{len(self.memories)}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create memory item
        memory = MemoryItem(
            memory_id=memory_id,
            content=content,
            source=source,
            timestamp=datetime.datetime.now(),
            importance=importance,
            tags=tags,
            metadata=metadata or {},
            last_accessed=None,
            access_count=0
        )
        
        # Add to memory collection
        self.memories.append(memory)
        
        # Update memory graph
        self.memory_graph[memory_id] = {
            'memory': memory,
            'connections': []
        }
        
        # Create connections with existing memories
        for existing_memory in self.memories:
            if existing_memory.memory_id != memory_id:
                # Calculate connection strength based on tag similarity
                common_tags = set(memory.tags).intersection(set(existing_memory.tags))
                if common_tags:
                    connection_strength = len(common_tags) / max(len(memory.tags), len(existing_memory.tags))
                    
                    if connection_strength > 0.2:  # Only keep strong connections
                        self.memory_graph[memory_id]['connections'].append({
                            'target_id': existing_memory.memory_id,
                            'strength': connection_strength
                        })
                        
                        # Add reverse connection
                        self.memory_graph[existing_memory.memory_id]['connections'].append({
                            'target_id': memory_id,
                            'strength': connection_strength
                        })
        
        # Save to disk
        self._save_memories()
        
        return memory_id
    
    def retrieve_memories(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """
        Retrieve memories based on query using Gemma 3n for semantic search
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of relevant memory items
        """
        # If Gemma integration is available, use it for semantic search
        if self.gemma_integration:
            try:
                # Create a prompt for Gemma to find relevant memories
                prompt = f"""
                أنا أبحث عن ذكريات متعلقة بالاستفسار التالي: "{query}"
                
                من فضلك قم بتقييم الذكريات التالية وحدد أيها أكثر صلة بالاستفسار:
                
                {self._format_memories_for_prompt(self.memories[:20])}
                
                أعطني أرقام الذكريات الأكثر صلة (حتى {limit} ذكريات) مرتبة حسب الأهمية.
                أجب بأرقام فقط، مفصولة بفواصل.
                """
                
                # Get response from Gemma
                response = self.gemma_integration.generate_response(prompt)
                
                # Parse response to get memory indices
                try:
                    # Extract numbers from response
                    import re
                    numbers = re.findall(r'\d+', response)
                    indices = [int(num) - 1 for num in numbers if 0 <= int(num) - 1 < len(self.memories)]
                    
                    # Get memories by indices
                    relevant_memories = [self.memories[i] for i in indices[:limit]]
                    
                    # Update access stats
                    for memory in relevant_memories:
                        self._update_access_stats(memory)
                    
                    return relevant_memories
                except Exception as e:
                    print(f"Error parsing Gemma response: {e}")
                    # Fall back to keyword search
            except Exception as e:
                print(f"Error using Gemma for memory retrieval: {e}")
                # Fall back to keyword search
        
        # Fallback: Simple keyword matching
        query_lower = query.lower()
        scored_memories = []
        
        for memory in self.memories:
            score = 0
            # Check content
            if query_lower in memory.content.lower():
                score += 0.6
            
            # Check tags
            for tag in memory.tags:
                if query_lower in tag.lower():
                    score += 0.3
                    break
            
            # Check metadata
            for key, value in memory.metadata.items():
                if isinstance(value, str) and query_lower in value.lower():
                    score += 0.1
                    break
            
            # Apply importance factor
            score *= (0.5 + 0.5 * memory.importance)
            
            if score > 0:
                scored_memories.append((memory, score))
        
        # Sort by score and get top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        results = [item[0] for item in scored_memories[:limit]]
        
        # Update access stats
        for memory in results:
            self._update_access_stats(memory)
        
        return results
    
    def _format_memories_for_prompt(self, memories: List[MemoryItem]) -> str:
        """Format memories for inclusion in a prompt"""
        formatted = []
        for i, memory in enumerate(memories):
            formatted.append(f"{i+1}. {memory.content} [Tags: {', '.join(memory.tags)}]")
        return "\n".join(formatted)
    
    def _update_access_stats(self, memory: MemoryItem):
        """Update memory access statistics"""
        memory.last_accessed = datetime.datetime.now()
        memory.access_count += 1
        
        # Add to working memory
        if memory not in self.working_memory:
            self.working_memory.append(memory)
            # Trim working memory if needed
            if len(self.working_memory) > self.working_memory_size:
                self.working_memory.pop(0)
        
        # Save changes
        self._save_memories()
    
    def get_associated_memories(self, memory_id: str, limit: int = 3) -> List[MemoryItem]:
        """
        Get memories associated with a given memory through the memory graph
        
        Args:
            memory_id: ID of the memory to find associations for
            limit: Maximum number of results
            
        Returns:
            List of associated memories
        """
        if memory_id not in self.memory_graph:
            return []
        
        # Get connections sorted by strength
        connections = sorted(
            self.memory_graph[memory_id]['connections'],
            key=lambda x: x['strength'],
            reverse=True
        )
        
        # Get associated memories
        associated_memories = []
        for conn in connections[:limit]:
            target_id = conn['target_id']
            for memory in self.memories:
                if memory.memory_id == target_id:
                    associated_memories.append(memory)
                    break
        
        return associated_memories
    
    def generate_memory_prompt(self, context: str = "", person_name: str = "") -> Tuple[str, MemoryItem]:
        """
        Generate a memory prompt for stimulating recall
        
        Args:
            context: Current conversation context
            person_name: Name of person to focus on (optional)
            
        Returns:
            prompt: The generated prompt
            memory: The memory item being prompted
        """
        # Strategy 1: Use working memory (recently accessed)
        if self.working_memory and random.random() < 0.3:
            memory = random.choice(self.working_memory)
            prompt = f"هل تتذكر {memory.content}؟"
            return prompt, memory
        
        # Strategy 2: Use person-specific memory if provided
        if person_name:
            person_memories = [m for m in self.memories if 
                              person_name.lower() in m.content.lower() or
                              'person' in m.tags and person_name.lower() in str(m.metadata).lower()]
            
            if person_memories:
                memory = random.choice(person_memories)
                prompt = f"هل تتذكر عندما كنت مع {person_name}؟ {memory.content}"
                return prompt, memory
        
        # Strategy 3: Use important memories
        important_memories = sorted(self.memories, key=lambda m: m.importance, reverse=True)
        if important_memories:
            memory = random.choice(important_memories[:5])  # Choose from top 5 important memories
            prompt = f"أريد أن أسألك عن ذكرى مهمة: {memory.content}"
            return prompt, memory
        
        # Fallback
        if self.memories:
            memory = random.choice(self.memories)
            prompt = f"هل يمكنك أن تخبرني عن {memory.content}؟"
            return prompt, memory
        
        # No memories available
        return "هل يمكنك أن تخبرني عن ذكرياتك القديمة؟", None
    
    def analyze_memory_response(self, memory_id: str, response: str) -> Dict[str, Any]:
        """
        Analyze patient's response to a memory prompt
        
        Args:
            memory_id: ID of the prompted memory
            response: Patient's response
            
        Returns:
            Analysis results
        """
        # Find the memory
        memory = None
        for m in self.memories:
            if m.memory_id == memory_id:
                memory = m
                break
        
        if not memory:
            return {"error": "Memory not found"}
        
        # If Gemma integration is available, use it for analysis
        if self.gemma_integration:
            try:
                # Create a prompt for Gemma to analyze the response
                prompt = f"""
                تحليل استجابة المريض للذكرى:
                
                الذكرى: {memory.content}
                استجابة المريض: "{response}"
                
                قم بتحليل الاستجابة وتقييم:
                1. هل تذكر المريض الذكرى بشكل صحيح؟ (نعم/جزئيًا/لا)
                2. مستوى التفاصيل في الاستجابة (منخفض/متوسط/عالي)
                3. الحالة العاطفية للمريض (إيجابية/محايدة/سلبية)
                4. أي علامات على الارتباك أو القلق
                
                قدم تقييمك بتنسيق JSON.
                """
                
                # Get response from Gemma
                analysis_response = self.gemma_integration.generate_response(prompt)
                
                # Try to extract JSON
                try:
                    import re
                    # Find JSON pattern in response
                    json_match = re.search(r'\{.*\}', analysis_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        analysis = json.loads(json_str)
                        return analysis
                except Exception as e:
                    print(f"Error parsing analysis response: {e}")
                    # Fall back to simple analysis
            except Exception as e:
                print(f"Error using Gemma for response analysis: {e}")
                # Fall back to simple analysis
        
        # Fallback: Simple analysis
        recall_success = memory.content.lower() in response.lower()
        detail_level = "low"
        if len(response.split()) > 20:
            detail_level = "medium"
        if len(response.split()) > 50:
            detail_level = "high"
        
        return {
            "recall_success": "yes" if recall_success else "no",
            "detail_level": detail_level,
            "emotional_state": "neutral",
            "confusion_signs": "unknown"
        }
    
    def reinforce_memory(self, memory_id: str, success: bool):
        """
        Reinforce memory based on recall success
        
        Args:
            memory_id: ID of the memory
            success: Whether recall was successful
        """
        for memory in self.memories:
            if memory.memory_id == memory_id:
                # Update importance based on recall success
                if success:
                    # Successful recall - slightly decrease importance (less need to reinforce)
                    memory.importance = max(0.1, memory.importance - 0.05)
                else:
                    # Failed recall - increase importance (needs more reinforcement)
                    memory.importance = min(1.0, memory.importance + 0.1)
                
                # Save changes
                self._save_memories()
                break
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        if not self.memories:
            return {
                "total_memories": 0,
                "avg_importance": 0,
                "most_common_tags": [],
                "memory_sources": {}
            }
        
        # Calculate statistics
        total = len(self.memories)
        avg_importance = sum(m.importance for m in self.memories) / total
        
        # Count tags
        tag_counts = {}
        for memory in self.memories:
            for tag in memory.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count sources
        source_counts = {}
        for memory in self.memories:
            source_counts[memory.source] = source_counts.get(memory.source, 0) + 1
        
        # Get most common tags
        most_common_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_memories": total,
            "avg_importance": avg_importance,
            "most_common_tags": [tag for tag, count in most_common_tags],
            "memory_sources": source_counts
        }
    
    def clear_all_memories(self):
        """Clear all memories (use with caution)"""
        self.memories = []
        self.memory_graph = {}
        self.working_memory = []
        self._save_memories()

# Example usage
if __name__ == "__main__":
    # This would typically use the actual GemmaIntegration
    from ..ai.gemma_integration import GemmaIntegration
    
    # For testing
    gemma = GemmaIntegration()
    memory_system = IntelligentMemoryRetrieval(gemma)
    
    # Add sample memory
    memory_id = memory_system.add_memory(
        content="زيارة حديقة الأزهر مع العائلة",
        source="conversation",
        tags=["family", "outdoors", "happy"],
        importance=0.8,
        metadata={"location": "Cairo", "people": ["Ahmed", "Fatima"]}
    )
    
    # Retrieve memories
    memories = memory_system.retrieve_memories("عائلة")
    for memory in memories:
        print(f"Found memory: {memory.content}")
    
    # Generate prompt
    prompt, memory = memory_system.generate_memory_prompt(person_name="Ahmed")
    print(f"Memory prompt: {prompt}")
