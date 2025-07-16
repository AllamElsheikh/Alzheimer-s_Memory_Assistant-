"""
Intelligent Memory Retrieval System for Alzheimer's Memory Assistant
Uses Gemma 3n multimodal capabilities for contextual memory assistance.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from collections import defaultdict
import hashlib

@dataclass
class MemoryNode:
    """Represents a single memory with multimodal data"""
    id: str
    timestamp: datetime
    content: str
    memory_type: str  # episodic, semantic, procedural
    confidence: float
    tags: List[str]
    associated_media: Dict[str, str]  # image_path, audio_path, etc.
    emotional_context: str
    importance_score: float
    retrieval_count: int
    last_accessed: datetime

@dataclass
class MemoryCluster:
    """Group of related memories"""
    id: str
    name: str
    memories: List[MemoryNode]
    central_theme: str
    created: datetime
    strength: float  # how strongly memories are connected

class IntelligentMemoryRetrieval:
    """
    Memory retrieval system using Gemma 3n multimodal processing
    """
    
    def __init__(self, gemma_integration=None):
        self.gemma_integration = gemma_integration
        self.memory_database = {}  # id -> MemoryNode
        self.memory_clusters = {}  # id -> MemoryCluster
        self.association_graph = defaultdict(list)  # memory_id -> list of related memory_ids
        self.context_history = []
        self.retrieval_patterns = defaultdict(int)
        
        # Load existing memories
        self._load_memory_database()

    def store_multimodal_memory(self, content: str, memory_type: str = "episodic",
                               image_path: str = None, audio_path: str = None,
                               emotional_context: str = "neutral",
                               tags: List[str] = None) -> str:
        """
        Store a new memory with multimodal data
        """
        
        memory_id = self._generate_memory_id(content)
        
        # Use Gemma 3n to analyze and enhance the memory
        content, importance_score = self._analyze_memory_importance(
            content, image_path, audio_path, emotional_context
        )
        
        # Create memory node
        memory_node = MemoryNode(
            id=memory_id,
            timestamp=datetime.now(),
            content=content,
            memory_type=memory_type,
            confidence=1.0,  # Initial confidence
            tags=tags or [],
            associated_media={
                "image_path": image_path,
                "audio_path": audio_path
            },
            emotional_context=emotional_context,
            importance_score=importance_score,
            retrieval_count=0,
            last_accessed=datetime.now()
        )
        
        # Store in database
        self.memory_database[memory_id] = memory_node
        
        # Find and create associations
        self._create_memory_associations(memory_node)
        
        # Update clusters
        self._update_memory_clusters(memory_node)
        
        # Save to persistent storage
        self._save_memory_database()
        
        print(f"Memory stored: {memory_id} (importance: {importance_score:.2f})")
        return memory_id

    def retrieve_contextual_memories(self, query: str, context_type: str = "general",
                                   max_results: int = 5,
                                   include_multimodal: bool = True) -> List[MemoryNode]:
        """
        Retrieve memories based on contextual query using Gemma 3n
        """
        
        print(f"Retrieving memories for query: '{query}'")
        
        # Use Gemma 3n to understand the query context
        query_analysis = self._analyze_query_context(query, context_type)
        
        # Get candidate memories
        candidates = self._get_candidate_memories(query_analysis)
        
        # Score and rank memories
        scored_memories = []
        for memory in candidates:
            relevance_score = self._calculate_memory_relevance(
                memory, query, query_analysis, include_multimodal
            )
            scored_memories.append((memory, relevance_score))
        
        # Sort by relevance and recency
        scored_memories.sort(key=lambda x: (x[1], x[0].timestamp), reverse=True)
        
        # Select top results
        selected_memories = [memory for memory, score in scored_memories[:max_results]]
        
        # Update retrieval statistics
        for memory in selected_memories:
            memory.retrieval_count += 1
            memory.last_accessed = datetime.now()
            self.retrieval_patterns[memory.id] += 1
        
        # Update context history
        self.context_history.append({
            "timestamp": datetime.now(),
            "query": query,
            "context_type": context_type,
            "retrieved_memories": [m.id for m in selected_memories]
        })
        
        return selected_memories

    def _analyze_memory_importance(self, content: str, image_path: str = None,
                                 audio_path: str = None, emotional_context: str = "neutral") -> Tuple[str, float]:
        """
        Use Gemma 3n to analyze memory importance and enhance content
        """
        
        analysis_prompt = f"""
        تحليل أهمية الذكرى للمريض:
        
        المحتوى: {content}
        السياق العاطفي: {emotional_context}
        وسائط مرفقة: {'صورة' if image_path else 'لا'}, {'صوت' if audio_path else 'لا'}
        
        قم بتقييم:
        1. الأهمية العاطفية (0-1)
        2. الأهمية للحياة اليومية (0-1)
        3. القابلية للتذكر (0-1)
        4. الارتباط بذكريات أخرى (0-1)
        
        اكتب تحليلاً مختصراً وأعط درجة أهمية إجمالية:
        """
        
        if self.gemma_integration:
            try:
                # Use multimodal analysis if media is available
                if image_path or audio_path:
                    analysis = self.gemma_integration._generate_multimodal_response(
                        text=analysis_prompt,
                        image_path=image_path,
                        audio_path=audio_path
                    )
                else:
                    analysis = self.gemma_integration.generate_response(analysis_prompt)
                
                # Extract importance score from analysis
                importance_score = self._extract_importance_score(analysis)
                content = f"{content}\n\nتحليل الذكرى: {analysis}"
                
                return content, importance_score
                
            except Exception as e:
                print(f"Memory analysis error: {e}")
        
        # Fallback to simple heuristics
        importance_score = self._calculate_simple_importance(content, emotional_context)
        return content, importance_score

    def _extract_importance_score(self, analysis: str) -> float:
        """Extract numerical importance score from AI analysis"""
        
        # Look for numerical patterns in the analysis
        import re
        
        # Look for patterns like "درجة أهمية: 0.8" or "importance: 0.85"
        score_patterns = [
            r'درجة أهمية[:\s]+([0-9]*\.?[0-9]+)',
            r'أهمية إجمالية[:\s]+([0-9]*\.?[0-9]+)',
            r'importance[:\s]+([0-9]*\.?[0-9]+)',
            r'score[:\s]+([0-9]*\.?[0-9]+)'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, analysis, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1))
                    return min(1.0, max(0.0, score))  # Clamp to [0, 1]
                except ValueError:
                    continue
        
        # Fallback: analyze text for emotional and importance keywords
        importance_keywords = [
            'مهم', 'هام', 'أساسي', 'ضروري', 'حيوي', 'أولوية',
            'important', 'essential', 'critical', 'vital', 'significant'
        ]
        
        emotional_keywords = [
            'سعيد', 'حزين', 'فرح', 'غضب', 'خوف', 'حب', 'كره',
            'happy', 'sad', 'joy', 'anger', 'fear', 'love', 'emotional'
        ]
        
        score = 0.5  # Base score
        
        for keyword in importance_keywords:
            if keyword in analysis.lower():
                score += 0.1
        
        for keyword in emotional_keywords:
            if keyword in analysis.lower():
                score += 0.05
        
        return min(1.0, score)

    def _calculate_simple_importance(self, content: str, emotional_context: str) -> float:
        """Simple heuristic-based importance calculation"""
        
        score = 0.5  # Base score
        
        # Emotional context weighting
        emotion_weights = {
            "جداً إيجابي": 0.3,
            "إيجابي": 0.2,
            "محايد": 0.0,
            "سلبي": 0.1,
            "جداً سلبي": 0.2,
            "very_positive": 0.3,
            "positive": 0.2,
            "neutral": 0.0,
            "negative": 0.1,
            "very_negative": 0.2
        }
        
        score += emotion_weights.get(emotional_context, 0.0)
        
        # Content length and detail weighting
        if len(content) > 100:
            score += 0.1
        if len(content) > 200:
            score += 0.1
        
        # Important keywords
        important_words = [
            'عائلة', 'أسرة', 'زوج', 'زوجة', 'أطفال', 'والدين',
            'family', 'spouse', 'children', 'parents',
            'عمل', 'وظيفة', 'مهنة', 'work', 'job', 'career',
            'صحة', 'مرض', 'دواء', 'health', 'medicine', 'doctor'
        ]
        
        for word in important_words:
            if word in content.lower():
                score += 0.05
        
        return min(1.0, max(0.1, score))

    def _generate_memory_id(self, content: str) -> str:
        """Generate unique ID for memory"""
        
        timestamp = datetime.now().isoformat()
        content_hash = hashlib.md5(f"{content}{timestamp}".encode('utf-8')).hexdigest()
        return f"mem_{content_hash[:12]}"

    def _analyze_query_context(self, query: str, context_type: str) -> Dict[str, Any]:
        """
        Analyze query to understand what type of memories to retrieve
        """
        
        context_prompt = f"""
        تحليل استعلام البحث عن الذكريات:
        
        الاستعلام: {query}
        نوع السياق: {context_type}
        
        حدد:
        1. نوع الذكرى المطلوبة (شخصية، عملية، عامة)
        2. الإطار الزمني المحتمل
        3. الكلمات المفتاحية المهمة
        4. السياق العاطفي المطلوب
        5. نوع الوسائط المفيدة (صور، صوت)
        
        اكتب تحليلاً مختصراً:
        """
        
        if self.gemma_integration:
            try:
                analysis = self.gemma_integration.generate_response(context_prompt)
                return self._parse_query_analysis(analysis, query)
            except Exception as e:
                print(f"Query analysis error: {e}")
        
        # Fallback to simple keyword analysis
        return self._simple_query_analysis(query, context_type)

    def _parse_query_analysis(self, analysis: str, original_query: str) -> Dict[str, Any]:
        """Parse AI analysis of query into structured data"""
        
        # Extract keywords from original query
        keywords = [word.strip() for word in original_query.split() if len(word.strip()) > 2]
        
        # Determine memory types based on analysis
        memory_types = []
        if any(word in analysis.lower() for word in ['شخصية', 'عائلة', 'personal', 'family']):
            memory_types.append('episodic')
        if any(word in analysis.lower() for word in ['عملية', 'مهارة', 'procedural', 'skill']):
            memory_types.append('procedural')
        if any(word in analysis.lower() for word in ['عامة', 'معلومات', 'semantic', 'general']):
            memory_types.append('semantic')
        
        if not memory_types:
            memory_types = ['episodic', 'semantic', 'procedural']
        
        return {
            "keywords": keywords,
            "memory_types": memory_types,
            "analysis": analysis,
            "emotional_context": self._extract_emotional_context(analysis),
            "time_frame": self._extract_time_frame(analysis),
            "media_preference": self._extract_media_preference(analysis)
        }

    def _simple_query_analysis(self, query: str, context_type: str) -> Dict[str, Any]:
        """Simple fallback query analysis"""
        
        keywords = [word.strip() for word in query.split() if len(word.strip()) > 2]
        
        # Default memory types based on context
        context_memory_mapping = {
            "personal": ["episodic"],
            "family": ["episodic"],
            "work": ["procedural", "semantic"],
            "general": ["episodic", "semantic", "procedural"],
            "health": ["semantic", "episodic"]
        }
        
        memory_types = context_memory_mapping.get(context_type, ["episodic", "semantic"])
        
        return {
            "keywords": keywords,
            "memory_types": memory_types,
            "analysis": f"Simple analysis for: {query}",
            "emotional_context": "neutral",
            "time_frame": "any",
            "media_preference": "any"
        }

    def _extract_emotional_context(self, analysis: str) -> str:
        """Extract emotional context from analysis"""
        
        emotional_indicators = {
            "positive": ["إيجابي", "سعيد", "فرح", "positive", "happy", "joy"],
            "negative": ["سلبي", "حزين", "غضب", "negative", "sad", "anger"],
            "neutral": ["محايد", "عادي", "neutral", "normal"]
        }
        
        for emotion, indicators in emotional_indicators.items():
            if any(indicator in analysis.lower() for indicator in indicators):
                return emotion
        
        return "neutral"

    def _extract_time_frame(self, analysis: str) -> str:
        """Extract time frame from analysis"""
        
        time_indicators = {
            "recent": ["حديث", "مؤخراً", "recent", "lately", "recently"],
            "old": ["قديم", "سابق", "old", "past", "previous"],
            "childhood": ["طفولة", "صغر", "childhood", "young"],
            "any": ["أي", "كل", "any", "all"]
        }
        
        for timeframe, indicators in time_indicators.items():
            if any(indicator in analysis.lower() for indicator in indicators):
                return timeframe
        
        return "any"

    def _extract_media_preference(self, analysis: str) -> str:
        """Extract media preference from analysis"""
        
        if any(word in analysis.lower() for word in ["صورة", "صور", "image", "photo", "visual"]):
            return "image"
        elif any(word in analysis.lower() for word in ["صوت", "أصوات", "audio", "sound", "voice"]):
            return "audio"
        else:
            return "any"

    def _get_candidate_memories(self, query_analysis: Dict[str, Any]) -> List[MemoryNode]:
        """Get candidate memories based on query analysis"""
        
        candidates = []
        keywords = query_analysis["keywords"]
        memory_types = query_analysis["memory_types"]
        
        for memory in self.memory_database.values():
            # Filter by memory type
            if memory.memory_type not in memory_types:
                continue
            
            # Check keyword matches
            keyword_match = False
            for keyword in keywords:
                if (keyword.lower() in memory.content.lower() or 
                    any(keyword.lower() in tag.lower() for tag in memory.tags)):
                    keyword_match = True
                    break
            
            if keyword_match or not keywords:  # Include if keywords match or no specific keywords
                candidates.append(memory)
        
        return candidates

    def _calculate_memory_relevance(self, memory: MemoryNode, query: str,
                                  query_analysis: Dict[str, Any],
                                  include_multimodal: bool) -> float:
        """Calculate relevance score for a memory"""
        
        score = 0.0
        
        # Keyword relevance
        keywords = query_analysis["keywords"]
        if keywords:
            keyword_matches = sum(1 for keyword in keywords 
                                if keyword.lower() in memory.content.lower())
            score += (keyword_matches / len(keywords)) * 0.4
        
        # Tag relevance
        if memory.tags:
            tag_matches = sum(1 for keyword in keywords 
                            for tag in memory.tags
                            if keyword.lower() in tag.lower())
            score += min(tag_matches * 0.1, 0.2)
        
        # Importance score
        score += memory.importance_score * 0.3
        
        # Recency (more recent = slightly higher score)
        days_old = (datetime.now() - memory.timestamp).days
        recency_score = max(0, 1 - (days_old / 365))  # Decay over a year
        score += recency_score * 0.1
        
        # Retrieval frequency (frequently accessed = higher relevance)
        frequency_score = min(memory.retrieval_count / 10, 1.0)
        score += frequency_score * 0.1
        
        # Multimodal bonus
        if include_multimodal and (memory.associated_media.get("image_path") or 
                                 memory.associated_media.get("audio_path")):
            score += 0.1
        
        # Emotional context match
        if query_analysis["emotional_context"] == memory.emotional_context:
            score += 0.1
        
        return score

    def _create_memory_associations(self, new_memory: MemoryNode):
        """Create associations between the new memory and existing memories"""
        
        for existing_id, existing_memory in self.memory_database.items():
            if existing_id == new_memory.id:
                continue
            
            # Calculate association strength
            association_strength = self._calculate_association_strength(new_memory, existing_memory)
            
            if association_strength > 0.3:  # Threshold for creating association
                self.association_graph[new_memory.id].append(existing_id)
                self.association_graph[existing_id].append(new_memory.id)

    def _calculate_association_strength(self, memory1: MemoryNode, memory2: MemoryNode) -> float:
        """Calculate association strength between two memories"""
        
        strength = 0.0
        
        # Common tags
        if memory1.tags and memory2.tags:
            common_tags = set(memory1.tags) & set(memory2.tags)
            strength += len(common_tags) * 0.2
        
        # Similar emotional context
        if memory1.emotional_context == memory2.emotional_context:
            strength += 0.3
        
        # Temporal proximity
        time_diff = abs((memory1.timestamp - memory2.timestamp).days)
        if time_diff < 7:  # Within a week
            strength += 0.3
        elif time_diff < 30:  # Within a month
            strength += 0.2
        elif time_diff < 365:  # Within a year
            strength += 0.1
        
        # Content similarity (simple word overlap)
        words1 = set(memory1.content.lower().split())
        words2 = set(memory2.content.lower().split())
        common_words = words1 & words2
        if words1 and words2:
            content_similarity = len(common_words) / max(len(words1), len(words2))
            strength += content_similarity * 0.3
        
        return min(strength, 1.0)

    def _update_memory_clusters(self, new_memory: MemoryNode):
        """Update memory clusters with the new memory"""
        
        # Find best cluster for the memory
        best_cluster = None
        best_fit_score = 0.0
        
        for cluster in self.memory_clusters.values():
            fit_score = self._calculate_cluster_fit(new_memory, cluster)
            if fit_score > best_fit_score and fit_score > 0.5:  # Threshold for cluster membership
                best_fit_score = fit_score
                best_cluster = cluster
        
        if best_cluster:
            # Add to existing cluster
            best_cluster.memories.append(new_memory)
            best_cluster.strength = self._recalculate_cluster_strength(best_cluster)
        else:
            # Create new cluster
            cluster_id = f"cluster_{len(self.memory_clusters)}"
            new_cluster = MemoryCluster(
                id=cluster_id,
                name=self._generate_cluster_name(new_memory),
                memories=[new_memory],
                central_theme=new_memory.content[:50] + "...",
                created=datetime.now(),
                strength=1.0
            )
            self.memory_clusters[cluster_id] = new_cluster

    def _calculate_cluster_fit(self, memory: MemoryNode, cluster: MemoryCluster) -> float:
        """Calculate how well a memory fits into a cluster"""
        
        if not cluster.memories:
            return 0.0
        
        fit_scores = []
        for cluster_memory in cluster.memories:
            association_strength = self._calculate_association_strength(memory, cluster_memory)
            fit_scores.append(association_strength)
        
        return np.mean(fit_scores)

    def _recalculate_cluster_strength(self, cluster: MemoryCluster) -> float:
        """Recalculate the strength of connections within a cluster"""
        
        if len(cluster.memories) < 2:
            return 1.0
        
        total_strength = 0.0
        pair_count = 0
        
        for i, memory1 in enumerate(cluster.memories):
            for memory2 in cluster.memories[i+1:]:
                strength = self._calculate_association_strength(memory1, memory2)
                total_strength += strength
                pair_count += 1
        
        return total_strength / pair_count if pair_count > 0 else 0.0

    def _generate_cluster_name(self, representative_memory: MemoryNode) -> str:
        """Generate a descriptive name for a memory cluster"""
        
        # Use first few words of the memory content
        words = representative_memory.content.split()[:3]
        name = " ".join(words)
        
        # Add memory type if relevant
        if representative_memory.memory_type != "episodic":
            name += f" ({representative_memory.memory_type})"
        
        return name

    def get_memory_suggestions(self, context: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
        """Get memory suggestions based on current context"""
        
        suggestion_prompt = f"""
        اقتراح ذكريات مفيدة للسياق الحالي:
        
        السياق: {context}
        
        ما هي الذكريات التي قد تكون مفيدة أو ذات صلة؟
        فكر في:
        - الأنشطة المشابهة
        - الأشخاص المرتبطين
        - الأماكن ذات الصلة
        - المهارات المطلوبة
        """
        
        # Get AI suggestions if available
        if self.gemma_integration:
            try:
                ai_suggestions = self.gemma_integration.generate_response(suggestion_prompt)
                # Parse AI suggestions and match with stored memories
                return self._match_ai_suggestions_with_memories(ai_suggestions, context)
            except Exception as e:
                print(f"AI suggestion error: {e}")
        
        # Fallback to similarity-based suggestions
        return self._get_similarity_based_suggestions(context, max_suggestions)

    def _match_ai_suggestions_with_memories(self, ai_suggestions: str, context: str) -> List[Dict[str, Any]]:
        """Match AI suggestions with actual stored memories"""
        
        suggestions = []
        
        # Extract keywords from AI suggestions
        suggestion_keywords = []
        for line in ai_suggestions.split('\n'):
            if line.strip():
                words = [word.strip('.,!?:') for word in line.split() if len(word.strip('.,!?:')) > 2]
                suggestion_keywords.extend(words)
        
        # Find memories that match the suggested themes
        for memory in self.memory_database.values():
            relevance_score = 0.0
            
            # Check keyword matches
            for keyword in suggestion_keywords:
                if keyword.lower() in memory.content.lower():
                    relevance_score += 0.1
            
            # Check tag matches
            for tag in memory.tags:
                if any(keyword.lower() in tag.lower() for keyword in suggestion_keywords):
                    relevance_score += 0.2
            
            if relevance_score > 0.3:
                suggestions.append({
                    "memory": memory,
                    "relevance_score": relevance_score,
                    "suggestion_reason": "Matches AI analysis of current context"
                })
        
        # Sort by relevance and return top suggestions
        suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
        return suggestions[:3]

    def _get_similarity_based_suggestions(self, context: str, max_suggestions: int) -> List[Dict[str, Any]]:
        """Get suggestions based on content similarity"""
        
        context_words = set(context.lower().split())
        suggestions = []
        
        for memory in self.memory_database.values():
            memory_words = set(memory.content.lower().split())
            
            # Calculate word overlap
            overlap = len(context_words & memory_words)
            similarity = overlap / max(len(context_words), len(memory_words)) if context_words or memory_words else 0
            
            if similarity > 0.1:  # Minimum similarity threshold
                suggestions.append({
                    "memory": memory,
                    "relevance_score": similarity,
                    "suggestion_reason": f"Content similarity: {similarity:.2f}"
                })
        
        # Sort by similarity and return top suggestions
        suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
        return suggestions[:max_suggestions]

    def _load_memory_database(self):
        """Load existing memories from persistent storage"""
        
        memory_file = "data/memories/memory_database.json"
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruct memory nodes
                for memory_id, memory_data in data.get("memories", {}).items():
                    memory_node = MemoryNode(
                        id=memory_data["id"],
                        timestamp=datetime.fromisoformat(memory_data["timestamp"]),
                        content=memory_data["content"],
                        memory_type=memory_data["memory_type"],
                        confidence=memory_data["confidence"],
                        tags=memory_data["tags"],
                        associated_media=memory_data["associated_media"],
                        emotional_context=memory_data["emotional_context"],
                        importance_score=memory_data["importance_score"],
                        retrieval_count=memory_data["retrieval_count"],
                        last_accessed=datetime.fromisoformat(memory_data["last_accessed"])
                    )
                    self.memory_database[memory_id] = memory_node
                
                # Reconstruct association graph
                self.association_graph = defaultdict(list, data.get("associations", {}))
                
                # Reconstruct memory clusters
                for cluster_id, cluster_data in data.get("clusters", {}).items():
                    cluster_memories = [
                        self.memory_database[mem_id] 
                        for mem_id in cluster_data["memory_ids"] 
                        if mem_id in self.memory_database
                    ]
                    
                    cluster = MemoryCluster(
                        id=cluster_data["id"],
                        name=cluster_data["name"],
                        memories=cluster_memories,
                        central_theme=cluster_data["central_theme"],
                        created=datetime.fromisoformat(cluster_data["created"]),
                        strength=cluster_data["strength"]
                    )
                    self.memory_clusters[cluster_id] = cluster
                
                print(f"Loaded {len(self.memory_database)} memories from database")
                
            except Exception as e:
                print(f"Error loading memory database: {e}")

    def _save_memory_database(self):
        """Save memory database to persistent storage"""
        
        memory_dir = "data/memories"
        os.makedirs(memory_dir, exist_ok=True)
        
        memory_file = os.path.join(memory_dir, "memory_database.json")
        
        try:
            # Prepare data for serialization
            data = {
                "memories": {},
                "associations": dict(self.association_graph),
                "clusters": {}
            }
            
            # Serialize memory nodes
            for memory_id, memory in self.memory_database.items():
                data["memories"][memory_id] = {
                    "id": memory.id,
                    "timestamp": memory.timestamp.isoformat(),
                    "content": memory.content,
                    "memory_type": memory.memory_type,
                    "confidence": memory.confidence,
                    "tags": memory.tags,
                    "associated_media": memory.associated_media,
                    "emotional_context": memory.emotional_context,
                    "importance_score": memory.importance_score,
                    "retrieval_count": memory.retrieval_count,
                    "last_accessed": memory.last_accessed.isoformat()
                }
            
            # Serialize memory clusters
            for cluster_id, cluster in self.memory_clusters.items():
                data["clusters"][cluster_id] = {
                    "id": cluster.id,
                    "name": cluster.name,
                    "memory_ids": [memory.id for memory in cluster.memories],
                    "central_theme": cluster.central_theme,
                    "created": cluster.created.isoformat(),
                    "strength": cluster.strength
                }
            
            # Write to file
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("Memory database saved successfully")
            
        except Exception as e:
            print(f"Error saving memory database: {e}")

    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get statistics about the memory database"""
        
        if not self.memory_database:
            return {"message": "No memories stored"}
        
        # Memory type distribution
        type_distribution = defaultdict(int)
        for memory in self.memory_database.values():
            type_distribution[memory.memory_type] += 1
        
        # Emotional context distribution
        emotion_distribution = defaultdict(int)
        for memory in self.memory_database.values():
            emotion_distribution[memory.emotional_context] += 1
        
        # Importance score statistics
        importance_scores = [memory.importance_score for memory in self.memory_database.values()]
        
        # Retrieval statistics
        retrieval_counts = [memory.retrieval_count for memory in self.memory_database.values()]
        
        return {
            "total_memories": len(self.memory_database),
            "memory_types": dict(type_distribution),
            "emotional_contexts": dict(emotion_distribution),
            "clusters": len(self.memory_clusters),
            "associations": sum(len(associations) for associations in self.association_graph.values()) // 2,
            "importance_stats": {
                "mean": np.mean(importance_scores),
                "std": np.std(importance_scores),
                "min": np.min(importance_scores),
                "max": np.max(importance_scores)
            },
            "retrieval_stats": {
                "mean": np.mean(retrieval_counts),
                "total_retrievals": sum(retrieval_counts),
                "most_accessed": max(retrieval_counts) if retrieval_counts else 0
            }
        }
