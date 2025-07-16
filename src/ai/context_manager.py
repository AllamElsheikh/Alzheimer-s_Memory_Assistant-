import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ContextManager:
    """Manage AI conversation context and interaction history"""
    
    def __init__(self, context_file='data/conversation_context.json'):
        """Initialize context manager with multimodal support"""
        self.context_file = context_file
        self.current_session = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'start_time': datetime.now().isoformat(),
            'interactions': [],
            'mood_indicators': [],
            'memory_performance': {},
            'topics_discussed': [],
            # 🏆 MULTIMODAL ENHANCEMENTS
            'multimodal_interactions': [],
            'image_analyses': [],
            'audio_analyses': [],
            'cognitive_assessments': [],
            'context_continuity': []
        }
        self.conversation_history = self._load_conversation_history()
        
        # Context tracking
        self.working_memory = {}
        self.long_term_patterns = {}
        self.session_metrics = {
            'response_times': [],
            'engagement_scores': [],
            'memory_recall_success': [],
            'multimodal_usage': 0
        }
    
    def _load_conversation_history(self) -> List[Dict]:
        """Load conversation history from file"""
        if not os.path.exists(self.context_file):
            os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
            return []
        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_context(self):
        """Save context to file"""
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)
    
    def add_context(self, context_type: str, data: Any):
        """Add context information"""
        context_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': context_type,
            'data': data
        }
        
        if context_type == 'user_input':
            self.current_session['interactions'].append({
                'timestamp': context_entry['timestamp'],
                'user_input': data,
                'response_generated': False
            })
        elif context_type == 'ai_response':
            # Update the last interaction with AI response
            if self.current_session['interactions']:
                self.current_session['interactions'][-1]['ai_response'] = data
                self.current_session['interactions'][-1]['response_generated'] = True
        elif context_type == 'memory_recall':
            self.current_session['memory_performance'][context_entry['timestamp']] = data
        elif context_type == 'mood_indicator':
            self.current_session['mood_indicators'].append(context_entry)
        elif context_type == 'topic':
            if data not in self.current_session['topics_discussed']:
                self.current_session['topics_discussed'].append(data)
    
    def get_current_context(self) -> Dict:
        """Get current conversation context"""
        return {
            'session_info': self.current_session,
            'recent_topics': self.current_session['topics_discussed'][-5:],
            'mood_trend': self._analyze_mood_trend(),
            'memory_performance': self._analyze_memory_performance(),
            'interaction_count': len(self.current_session['interactions'])
        }
    
    def update_context(self, new_context: Dict):
        """Update conversation context"""
        self.current_session.update(new_context)
    
    def clear_context(self):
        """Clear current session context"""
        # Save current session to history before clearing
        self.save_context_to_memory()
        
        # Start new session
        self.current_session = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'start_time': datetime.now().isoformat(),
            'interactions': [],
            'mood_indicators': [],
            'memory_performance': {},
            'topics_discussed': []
        }
    
    def save_context_to_memory(self):
        """Save current session context to long-term memory"""
        # Add session end time
        self.current_session['end_time'] = datetime.now().isoformat()
        
        # Calculate session summary
        self.current_session['summary'] = {
            'duration_minutes': self._calculate_session_duration(),
            'total_interactions': len(self.current_session['interactions']),
            'topics_count': len(self.current_session['topics_discussed']),
            'mood_summary': self._summarize_mood(),
            'memory_performance_summary': self._summarize_memory_performance()
        }
        
        # Add to conversation history
        self.conversation_history.append(self.current_session.copy())
        
        # Keep only last 50 sessions to prevent file from getting too large
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        
        self._save_context()
    
    def retrieve_relevant_context(self, query: str) -> Dict:
        """Retrieve relevant context for query"""
        relevant_context = {
            'recent_interactions': self.current_session['interactions'][-3:],
            'related_topics': [],
            'previous_mentions': []
        }
        
        query_lower = query.lower()
        
        # Search through topics discussed
        for topic in self.current_session['topics_discussed']:
            if query_lower in topic.lower():
                relevant_context['related_topics'].append(topic)
        
        # Search through conversation history for mentions
        for session in self.conversation_history[-10:]:  # Last 10 sessions
            for interaction in session.get('interactions', []):
                user_input = interaction.get('user_input', '').lower()
                ai_response = interaction.get('ai_response', '').lower()
                if query_lower in user_input or query_lower in ai_response:
                    relevant_context['previous_mentions'].append({
                        'session_id': session['session_id'],
                        'interaction': interaction
                    })
        
        return relevant_context
    
    def _analyze_mood_trend(self) -> str:
        """Analyze mood trend from indicators"""
        if not self.current_session['mood_indicators']:
            return "neutral"
        
        recent_moods = [indicator['data'] for indicator in self.current_session['mood_indicators'][-3:]]
        positive_count = sum(1 for mood in recent_moods if mood in ['happy', 'content', 'engaged'])
        negative_count = sum(1 for mood in recent_moods if mood in ['sad', 'confused', 'frustrated'])
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _analyze_memory_performance(self) -> Dict:
        """Analyze memory performance from session"""
        performance = self.current_session['memory_performance']
        if not performance:
            return {"status": "no_data"}
        
        correct_recalls = sum(1 for recall in performance.values() if recall.get('correct', False))
        total_recalls = len(performance)
        
        return {
            "status": "good" if correct_recalls / total_recalls > 0.7 else "needs_attention",
            "success_rate": correct_recalls / total_recalls if total_recalls > 0 else 0,
            "total_attempts": total_recalls
        }
    
    def _calculate_session_duration(self) -> int:
        """Calculate session duration in minutes"""
        start = datetime.fromisoformat(self.current_session['start_time'])
        end = datetime.now()
        return int((end - start).total_seconds() / 60)
    
    def _summarize_mood(self) -> str:
        """Summarize mood for the session"""
        return self._analyze_mood_trend()
    
    def _summarize_memory_performance(self) -> str:
        """Summarize memory performance for the session"""
        perf = self._analyze_memory_performance()
        return perf.get("status", "no_data")
    
    def get_session_report(self) -> Dict:
        """Generate a comprehensive session report for caregivers"""
        return {
            'session_id': self.current_session['session_id'],
            'duration': self._calculate_session_duration(),
            'interaction_summary': {
                'total_conversations': len(self.current_session['interactions']),
                'topics_discussed': self.current_session['topics_discussed'],
                'engagement_level': self._assess_engagement()
            },
            'memory_assessment': self._analyze_memory_performance(),
            'mood_assessment': {
                'overall_mood': self._analyze_mood_trend(),
                'mood_changes': len(self.current_session['mood_indicators'])
            },
            'recommendations': self._generate_recommendations()
        }
    
    def _assess_engagement(self) -> str:
        """Assess user engagement level"""
        interaction_count = len(self.current_session['interactions'])
        duration = self._calculate_session_duration()
        
        if duration == 0:
            return "minimal"
        
        interactions_per_minute = interaction_count / duration
        
        if interactions_per_minute > 2:
            return "high"
        elif interactions_per_minute > 1:
            return "moderate"
        else:
            return "low"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on session data"""
        recommendations = []
        
        mood = self._analyze_mood_trend()
        memory_perf = self._analyze_memory_performance()
        engagement = self._assess_engagement()
        
        if mood == "negative":
            recommendations.append("Consider shorter, more positive interactions")
        
        if memory_perf.get("status") == "needs_attention":
            recommendations.append("Focus on simpler memory exercises")
        
        if engagement == "low":
            recommendations.append("Try using more visual or audio prompts")
        
        return recommendations

    def add_multimodal_interaction(self, interaction_type: str, content: Dict[str, Any]):
        """
        Track multimodal interactions for better context understanding
        """
        multimodal_entry = {
            'timestamp': self._get_timestamp(),
            'type': interaction_type,
            'content': content,
            'session_id': self.current_session['session_id']
        }
        
        self.current_session['multimodal_interactions'].append(multimodal_entry)
        self.session_metrics['multimodal_usage'] += 1

    def get_multimodal_context(self, lookback_minutes: int = 10) -> Dict[str, Any]:
        """
        Get recent multimodal context for AI responses
        """
        recent_context = {
            'recent_images': [],
            'recent_audio': [],
            'conversation_themes': [],
            'memory_performance': self.current_session.get('memory_performance', {}),
            'working_memory': getattr(self, 'working_memory', {})
        }
        
        return recent_context
