"""
Conversation Flow Manager for Alzheimer's Memory Assistant
Manages therapeutic conversations with context awareness and adaptive responses.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

class ConversationState(Enum):
    """Current state of the conversation"""
    GREETING = "greeting"
    ASSESSMENT = "assessment"
    MEMORY_EXERCISE = "memory_exercise"
    EMOTIONAL_SUPPORT = "emotional_support"
    COGNITIVE_TRAINING = "cognitive_training"
    MEDICATION_REMINDER = "medication_reminder"
    FAMILY_INTERACTION = "family_interaction"
    CRISIS_INTERVENTION = "crisis_intervention"
    CLOSING = "closing"

class ResponseType(Enum):
    """Type of AI response"""
    THERAPEUTIC = "therapeutic"
    INFORMATIONAL = "informational"
    ENCOURAGING = "encouraging"
    REDIRECTING = "redirecting"
    EMERGENCY = "emergency"

@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    timestamp: datetime
    speaker: str  # "patient" or "assistant"
    content: str
    audio_path: Optional[str]
    image_path: Optional[str]
    emotional_tone: str
    cognitive_load: float  # 0-1, complexity of the interaction
    response_time: float  # seconds
    confidence: float  # AI confidence in understanding

@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    patient_id: str
    turns: List[ConversationTurn]
    states_visited: List[ConversationState]
    assessment_scores: Dict[str, float]
    goals_achieved: List[str]
    therapeutic_outcomes: Dict[str, Any]

class ConversationFlowManager:
    """
    Manages therapeutic conversation flows with adaptive AI responses
    """
    
    def __init__(self, gemma_integration=None, memory_retrieval=None, assessment_engine=None):
        self.gemma_integration = gemma_integration
        self.memory_retrieval = memory_retrieval
        self.assessment_engine = assessment_engine
        
        self.current_session = None
        self.conversation_history = []
        self.conversation_templates = self._load_conversation_templates()
        self.therapeutic_goals = self._initialize_therapeutic_goals()
        self.state_transitions = self._define_state_transitions()
        
    def start_conversation_session(self, patient_id: str) -> str:
        """Start a new conversation session"""
        
        session_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{patient_id}"
        
        self.current_session = ConversationSession(
            session_id=session_id,
            start_time=datetime.now(),
            end_time=None,
            patient_id=patient_id,
            turns=[],
            states_visited=[ConversationState.GREETING],
            assessment_scores={},
            goals_achieved=[],
            therapeutic_outcomes={}
        )
        
        # Generate opening greeting
        opening_message = self._generate_contextual_greeting(patient_id)
        
        # Add opening turn
        opening_turn = ConversationTurn(
            timestamp=datetime.now(),
            speaker="assistant",
            content=opening_message,
            audio_path=None,
            image_path=None,
            emotional_tone="warm",
            cognitive_load=0.1,
            response_time=0.0,
            confidence=1.0
        )
        
        self.current_session.turns.append(opening_turn)
        
        print(f"Started conversation session: {session_id}")
        return session_id

    def process_patient_input(self, input_text: str, audio_path: str = None, 
                            image_path: str = None) -> Dict[str, Any]:
        """
        Process patient input and generate appropriate AI response
        """
        
        if not self.current_session:
            raise ValueError("No active conversation session")
        
        start_time = datetime.now()
        
        # Analyze patient input
        input_analysis = self._analyze_patient_input(input_text, audio_path, image_path)
        
        # Update conversation state if needed
        new_state = self._determine_conversation_state(input_analysis)
        if new_state != self._get_current_state():
            self.current_session.states_visited.append(new_state)
        
        # Add patient turn to conversation
        patient_turn = ConversationTurn(
            timestamp=start_time,
            speaker="patient",
            content=input_text,
            audio_path=audio_path,
            image_path=image_path,
            emotional_tone=input_analysis.get("emotional_tone", "neutral"),
            cognitive_load=input_analysis.get("cognitive_load", 0.5),
            response_time=0.0,  # Not applicable for patient input
            confidence=input_analysis.get("understanding_confidence", 0.8)
        )
        
        self.current_session.turns.append(patient_turn)
        
        # Generate AI response
        ai_response = self._generate_adaptive_response(input_analysis, new_state)
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Add AI turn to conversation
        ai_turn = ConversationTurn(
            timestamp=datetime.now(),
            speaker="assistant",
            content=ai_response["content"],
            audio_path=ai_response.get("suggested_audio"),
            image_path=ai_response.get("suggested_image"),
            emotional_tone=ai_response.get("emotional_tone", "supportive"),
            cognitive_load=ai_response.get("cognitive_load", 0.3),
            response_time=response_time,
            confidence=ai_response.get("confidence", 0.8)
        )
        
        self.current_session.turns.append(ai_turn)
        
        # Update therapeutic outcomes
        self._update_therapeutic_outcomes(input_analysis, ai_response)
        
        return {
            "response": ai_response["content"],
            "conversation_state": new_state.value,
            "therapeutic_suggestions": ai_response.get("therapeutic_suggestions", []),
            "memory_triggers": ai_response.get("memory_triggers", []),
            "assessment_updates": ai_response.get("assessment_updates", {}),
            "emotion_detected": input_analysis.get("emotional_tone"),
            "cognitive_load": input_analysis.get("cognitive_load"),
            "session_progress": self._calculate_session_progress()
        }

    def _analyze_patient_input(self, input_text: str, audio_path: str = None, 
                             image_path: str = None) -> Dict[str, Any]:
        """
        Analyze patient input using Gemma 3n multimodal capabilities
        """
        
        analysis_prompt = f"""
        تحليل مدخلات المريض في جلسة علاجية:
        
        النص: {input_text}
        وسائط إضافية: {'صوت' if audio_path else 'لا'}, {'صورة' if image_path else 'لا'}
        
        حلل:
        1. الحالة العاطفية (إيجابي، سلبي، قلق، حزن، فرح، غضب)
        2. مستوى الوضوح المعرفي (0-1)
        3. علامات الارتباك أو التشويش
        4. المواضيع المذكورة
        5. طلبات المساعدة
        6. علامات الضيق أو الأزمة
        7. الذكريات المشار إليها
        8. مستوى المشاركة (0-1)
        
        اكتب تحليلاً مفصلاً:
        """
        
        analysis = {}
        
        if self.gemma_integration:
            try:
                # Use multimodal analysis if media is available
                if audio_path or image_path:
                    ai_analysis = self.gemma_integration._generate_multimodal_response(
                        text=analysis_prompt,
                        image_path=image_path,
                        audio_path=audio_path
                    )
                else:
                    ai_analysis = self.gemma_integration.generate_response(analysis_prompt)
                
                analysis = self._parse_patient_analysis(ai_analysis, input_text)
                
            except Exception as e:
                print(f"Patient input analysis error: {e}")
                analysis = self._fallback_input_analysis(input_text)
        else:
            analysis = self._fallback_input_analysis(input_text)
        
        return analysis

    def _parse_patient_analysis(self, ai_analysis: str, input_text: str) -> Dict[str, Any]:
        """Parse AI analysis into structured data"""
        
        # Extract emotional tone
        emotional_indicators = {
            "positive": ["إيجابي", "سعيد", "مرتاح", "positive", "happy", "comfortable"],
            "negative": ["سلبي", "حزين", "مكتئب", "negative", "sad", "depressed"],
            "anxious": ["قلق", "متوتر", "خائف", "anxious", "worried", "fearful"],
            "confused": ["مرتبك", "مشوش", "confused", "disoriented"],
            "angry": ["غاضب", "منزعج", "angry", "frustrated"],
            "neutral": ["محايد", "عادي", "neutral", "normal"]
        }
        
        emotional_tone = "neutral"
        for emotion, indicators in emotional_indicators.items():
            if any(indicator in ai_analysis.lower() for indicator in indicators):
                emotional_tone = emotion
                break
        
        # Extract cognitive clarity (look for numerical indicators)
        import re
        clarity_match = re.search(r'وضوح.*?([0-9]*\.?[0-9]+)', ai_analysis)
        cognitive_clarity = 0.7  # Default
        if clarity_match:
            try:
                cognitive_clarity = float(clarity_match.group(1))
                if cognitive_clarity > 1:
                    cognitive_clarity = cognitive_clarity / 10  # Handle 0-10 scale
            except ValueError:
                pass
        
        # Detect crisis indicators
        crisis_indicators = [
            "أزمة", "مساعدة", "خطر", "ألم", "crisis", "help", "emergency", "pain",
            "لا أستطيع", "أريد أن أموت", "can't", "want to die"
        ]
        
        crisis_detected = any(indicator in input_text.lower() or indicator in ai_analysis.lower() 
                            for indicator in crisis_indicators)
        
        # Extract mentioned topics
        topics = []
        topic_indicators = {
            "family": ["عائلة", "أسرة", "زوج", "زوجة", "أطفال", "family", "spouse", "children"],
            "health": ["صحة", "دواء", "طبيب", "مرض", "health", "medicine", "doctor", "illness"],
            "memory": ["ذاكرة", "تذكر", "نسيان", "memory", "remember", "forget"],
            "daily_activities": ["أكل", "نوم", "استحمام", "eat", "sleep", "shower", "daily"],
            "emotions": ["مشاعر", "حزن", "فرح", "emotions", "feelings", "sad", "happy"]
        }
        
        for topic, indicators in topic_indicators.items():
            if any(indicator in input_text.lower() for indicator in indicators):
                topics.append(topic)
        
        # Calculate engagement level
        engagement_level = min(1.0, len(input_text.split()) / 20)  # Based on response length
        if any(word in input_text.lower() for word in ["نعم", "أريد", "yes", "want", "like"]):
            engagement_level += 0.2
        
        return {
            "emotional_tone": emotional_tone,
            "cognitive_clarity": cognitive_clarity,
            "cognitive_load": 1.0 - cognitive_clarity,  # Higher confusion = higher load
            "crisis_detected": crisis_detected,
            "topics_mentioned": topics,
            "engagement_level": min(1.0, engagement_level),
            "understanding_confidence": 0.8,  # Default confidence
            "ai_analysis": ai_analysis
        }

    def _fallback_input_analysis(self, input_text: str) -> Dict[str, Any]:
        """Fallback analysis when AI is not available"""
        
        # Simple keyword-based analysis
        emotional_keywords = {
            "positive": ["سعيد", "جيد", "ممتاز", "رائع", "happy", "good", "great", "wonderful"],
            "negative": ["حزين", "سيء", "تعب", "sad", "bad", "tired", "difficult"],
            "anxious": ["قلق", "خائف", "متوتر", "worried", "afraid", "nervous"],
            "confused": ["مرتبك", "لا أعرف", "confused", "don't know"]
        }
        
        emotional_tone = "neutral"
        for emotion, keywords in emotional_keywords.items():
            if any(keyword in input_text.lower() for keyword in keywords):
                emotional_tone = emotion
                break
        
        # Simple engagement calculation
        word_count = len(input_text.split())
        engagement_level = min(1.0, word_count / 15)
        
        # Simple cognitive load (based on complexity indicators)
        complexity_indicators = ["لا أستطيع", "صعب", "مشكلة", "can't", "difficult", "problem"]
        cognitive_load = 0.7 if any(indicator in input_text.lower() for indicator in complexity_indicators) else 0.3
        
        return {
            "emotional_tone": emotional_tone,
            "cognitive_clarity": 1.0 - cognitive_load,
            "cognitive_load": cognitive_load,
            "crisis_detected": False,
            "topics_mentioned": [],
            "engagement_level": engagement_level,
            "understanding_confidence": 0.6,
            "ai_analysis": "Fallback analysis used"
        }

    def _determine_conversation_state(self, input_analysis: Dict[str, Any]) -> ConversationState:
        """Determine the appropriate conversation state based on input analysis"""
        
        current_state = self._get_current_state()
        
        # Crisis detection takes priority
        if input_analysis.get("crisis_detected", False):
            return ConversationState.CRISIS_INTERVENTION
        
        # Check for specific topic-based state transitions
        topics = input_analysis.get("topics_mentioned", [])
        
        if "memory" in topics and current_state != ConversationState.MEMORY_EXERCISE:
            return ConversationState.MEMORY_EXERCISE
        
        if "emotions" in topics and input_analysis.get("emotional_tone") in ["negative", "anxious"]:
            return ConversationState.EMOTIONAL_SUPPORT
        
        if "health" in topics:
            return ConversationState.MEDICATION_REMINDER
        
        if "family" in topics:
            return ConversationState.FAMILY_INTERACTION
        
        # Check cognitive load for assessment needs
        if input_analysis.get("cognitive_load", 0) > 0.7:
            return ConversationState.ASSESSMENT
        
        # Default state transitions based on current state
        state_progression = {
            ConversationState.GREETING: ConversationState.ASSESSMENT,
            ConversationState.ASSESSMENT: ConversationState.COGNITIVE_TRAINING,
            ConversationState.COGNITIVE_TRAINING: ConversationState.MEMORY_EXERCISE,
            ConversationState.MEMORY_EXERCISE: ConversationState.EMOTIONAL_SUPPORT,
            ConversationState.EMOTIONAL_SUPPORT: ConversationState.CLOSING
        }
        
        # Check if we should progress to next state
        if len(self.current_session.turns) > 6:  # After some interaction
            return state_progression.get(current_state, current_state)
        
        return current_state

    def _get_current_state(self) -> ConversationState:
        """Get the current conversation state"""
        if self.current_session and self.current_session.states_visited:
            return self.current_session.states_visited[-1]
        return ConversationState.GREETING

    def _generate_adaptive_response(self, input_analysis: Dict[str, Any], 
                                  new_state: ConversationState) -> Dict[str, Any]:
        """
        Generate adaptive AI response based on input analysis and conversation state
        """
        
        # Prepare response context
        response_context = {
            "current_state": new_state,
            "emotional_tone": input_analysis.get("emotional_tone", "neutral"),
            "cognitive_load": input_analysis.get("cognitive_load", 0.5),
            "topics": input_analysis.get("topics_mentioned", []),
            "session_length": len(self.current_session.turns),
            "previous_responses": [turn.content for turn in self.current_session.turns[-3:] if turn.speaker == "assistant"]
        }
        
        # Generate response using Gemma 3n
        if self.gemma_integration:
            response = self._generate_ai_response(input_analysis, response_context)
        else:
            response = self._generate_template_response(response_context)
        
        # Add therapeutic enhancements
        response = self._enhance_therapeutic_response(response, input_analysis, new_state)
        
        return response

    def _generate_ai_response(self, input_analysis: Dict[str, Any], 
                            response_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using Gemma 3n AI"""
        
        # Get conversation history for context
        recent_turns = self.current_session.turns[-4:] if len(self.current_session.turns) > 4 else self.current_session.turns
        conversation_context = "\n".join([
            f"{'المريض' if turn.speaker == 'patient' else 'المساعد'}: {turn.content}"
            for turn in recent_turns
        ])
        
        # Retrieve relevant memories if available
        memory_context = ""
        if self.memory_retrieval and input_analysis.get("topics_mentioned"):
            try:
                patient_input = self.current_session.turns[-1].content if self.current_session.turns else ""
                relevant_memories = self.memory_retrieval.retrieve_contextual_memories(
                    patient_input, "therapeutic", max_results=2
                )
                if relevant_memories:
                    memory_context = "\n\nذكريات ذات صلة:\n" + "\n".join([
                        f"- {memory.content[:100]}..." for memory in relevant_memories
                    ])
            except Exception as e:
                print(f"Memory retrieval error: {e}")
        
        # Generate response prompt
        response_prompt = f"""
        أنت مساعد ذكي متخصص في رعاية مرضى الزهايمر. تفاعل بشكل علاجي ومفيد.
        
        السياق:
        حالة المحادثة: {response_context['current_state'].value}
        الحالة العاطفية للمريض: {response_context['emotional_tone']}
        مستوى الضغط المعرفي: {response_context['cognitive_load']:.1f}
        المواضيع المذكورة: {', '.join(response_context['topics'])}
        
        المحادثة الحديثة:
        {conversation_context}
        {memory_context}
        
        اكتب رداً علاجياً مناسباً:
        - كن دافئاً ومتفهماً
        - استخدم لغة بسيطة وواضحة
        - قدم الدعم العاطفي المناسب
        - اقترح أنشطة أو تمارين مفيدة إذا كان مناسباً
        - تجنب المعلومات المعقدة أو المربكة
        """
        
        try:
            ai_response = self.gemma_integration.generate_response(response_prompt)
            
            return {
                "content": ai_response,
                "emotional_tone": "supportive",
                "cognitive_load": 0.3,
                "confidence": 0.8,
                "generation_method": "ai"
            }
            
        except Exception as e:
            print(f"AI response generation error: {e}")
            return self._generate_template_response(response_context)

    def _generate_template_response(self, response_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using predefined templates"""
        
        state = response_context["current_state"]
        emotional_tone = response_context["emotional_tone"]
        
        # State-specific response templates
        templates = {
            ConversationState.GREETING: [
                "أهلاً وسهلاً! كيف حالك اليوم؟",
                "مرحباً! أتمنى أن تكون في حالة جيدة.",
                "صباح الخير! كيف تشعر اليوم؟"
            ],
            ConversationState.EMOTIONAL_SUPPORT: [
                "أفهم مشاعرك. هذا طبيعي تماماً.",
                "أنت لست وحدك في هذا. نحن هنا لمساعدتك.",
                "مشاعرك مهمة ومفهومة. دعنا نتحدث عنها."
            ],
            ConversationState.MEMORY_EXERCISE: [
                "دعنا نتذكر شيئاً جميلاً من الماضي.",
                "هل تتذكر مكاناً كان يجعلك سعيداً؟",
                "حدثني عن ذكرى جميلة تحتفظ بها."
            ],
            ConversationState.COGNITIVE_TRAINING: [
                "دعنا نقوم بتمرين بسيط للذهن.",
                "ما رأيك في لعبة صغيرة لتحفيز الذاكرة؟",
                "هل تريد أن نمارس بعض التمارين المفيدة؟"
            ]
        }
        
        # Emotional tone adjustments
        if emotional_tone == "negative":
            response_prefix = "أعلم أن الأمور قد تبدو صعبة أحياناً. "
        elif emotional_tone == "anxious":
            response_prefix = "لا تقلق، كل شيء سيكون بخير. "
        elif emotional_tone == "positive":
            response_prefix = "يسعدني أن أراك في حالة جيدة! "
        else:
            response_prefix = ""
        
        # Select appropriate template
        state_templates = templates.get(state, ["كيف يمكنني مساعدتك اليوم؟"])
        selected_template = np.random.choice(state_templates)
        
        final_response = response_prefix + selected_template
        
        return {
            "content": final_response,
            "emotional_tone": "supportive",
            "cognitive_load": 0.2,
            "confidence": 0.6,
            "generation_method": "template"
        }

    def _enhance_therapeutic_response(self, response: Dict[str, Any], 
                                    input_analysis: Dict[str, Any],
                                    conversation_state: ConversationState) -> Dict[str, Any]:
        """Add therapeutic enhancements to the response"""
        
        # Add memory triggers if relevant
        memory_triggers = []
        if conversation_state == ConversationState.MEMORY_EXERCISE:
            memory_triggers = [
                "عائلتك",
                "منزل طفولتك",
                "عملك السابق",
                "أصدقاء قدامى",
                "مناسبات سعيدة"
            ]
        
        # Add therapeutic suggestions
        therapeutic_suggestions = []
        
        if input_analysis.get("emotional_tone") == "negative":
            therapeutic_suggestions.extend([
                "تمارين التنفس العميق",
                "الاستماع للموسيقى المفضلة",
                "النظر إلى الصور العائلية"
            ])
        
        if input_analysis.get("cognitive_load", 0) > 0.6:
            therapeutic_suggestions.extend([
                "أخذ استراحة قصيرة",
                "شرب كوب من الماء",
                "التركيز على التنفس"
            ])
        
        # Add assessment updates if relevant
        assessment_updates = {}
        if conversation_state == ConversationState.ASSESSMENT:
            assessment_updates = {
                "engagement_level": input_analysis.get("engagement_level", 0.5),
                "emotional_state": input_analysis.get("emotional_tone", "neutral"),
                "cognitive_clarity": input_analysis.get("cognitive_clarity", 0.7)
            }
        
        # Enhance the response
        response.update({
            "memory_triggers": memory_triggers,
            "therapeutic_suggestions": therapeutic_suggestions,
            "assessment_updates": assessment_updates,
            "conversation_state": conversation_state.value
        })
        
        return response

    def _generate_contextual_greeting(self, patient_id: str) -> str:
        """Generate personalized greeting based on patient history"""
        
        # Check time of day
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_greeting = "صباح الخير"
        elif current_hour < 17:
            time_greeting = "مساء الخير"
        else:
            time_greeting = "مساء الخير"
        
        # Basic personalized greeting
        greetings = [
            f"{time_greeting}! كيف حالك اليوم؟",
            f"{time_greeting}! أتمنى أن تكون في أحسن حال.",
            f"{time_greeting}! كيف تشعر اليوم؟"
        ]
        
        return np.random.choice(greetings)

    def _update_therapeutic_outcomes(self, input_analysis: Dict[str, Any], 
                                   ai_response: Dict[str, Any]):
        """Update therapeutic outcomes based on the interaction"""
        
        if not self.current_session:
            return
        
        # Update assessment scores
        self.current_session.assessment_scores.update(
            ai_response.get("assessment_updates", {})
        )
        
        # Track therapeutic goals
        if input_analysis.get("engagement_level", 0) > 0.7:
            if "patient_engagement" not in self.current_session.goals_achieved:
                self.current_session.goals_achieved.append("patient_engagement")
        
        if input_analysis.get("emotional_tone") == "positive":
            if "positive_emotional_state" not in self.current_session.goals_achieved:
                self.current_session.goals_achieved.append("positive_emotional_state")
        
        # Update therapeutic outcomes
        outcomes = self.current_session.therapeutic_outcomes
        
        # Emotional progression
        if "emotional_progression" not in outcomes:
            outcomes["emotional_progression"] = []
        outcomes["emotional_progression"].append({
            "timestamp": datetime.now().isoformat(),
            "emotional_tone": input_analysis.get("emotional_tone", "neutral")
        })
        
        # Cognitive clarity tracking
        if "cognitive_clarity" not in outcomes:
            outcomes["cognitive_clarity"] = []
        outcomes["cognitive_clarity"].append({
            "timestamp": datetime.now().isoformat(),
            "clarity_score": input_analysis.get("cognitive_clarity", 0.5)
        })
        
        # Engagement tracking
        if "engagement_levels" not in outcomes:
            outcomes["engagement_levels"] = []
        outcomes["engagement_levels"].append({
            "timestamp": datetime.now().isoformat(),
            "engagement": input_analysis.get("engagement_level", 0.5)
        })

    def _calculate_session_progress(self) -> Dict[str, Any]:
        """Calculate progress metrics for the current session"""
        
        if not self.current_session or not self.current_session.turns:
            return {}
        
        # Calculate session duration
        duration = (datetime.now() - self.current_session.start_time).total_seconds() / 60  # minutes
        
        # Calculate average emotional tone
        emotional_tones = [turn.emotional_tone for turn in self.current_session.turns if turn.speaker == "patient"]
        positive_emotions = sum(1 for tone in emotional_tones if tone in ["positive", "happy"])
        emotional_positivity = positive_emotions / len(emotional_tones) if emotional_tones else 0
        
        # Calculate engagement
        engagement_scores = [turn.cognitive_load for turn in self.current_session.turns if turn.speaker == "patient"]
        average_engagement = 1 - np.mean(engagement_scores) if engagement_scores else 0.5  # Lower cognitive load = higher engagement
        
        # Calculate conversation flow
        states_count = len(set(self.current_session.states_visited))
        conversation_flow_score = min(1.0, states_count / 5)  # Normalized by expected number of states
        
        return {
            "session_duration_minutes": duration,
            "total_turns": len(self.current_session.turns),
            "emotional_positivity": emotional_positivity,
            "average_engagement": average_engagement,
            "conversation_flow_score": conversation_flow_score,
            "goals_achieved": len(self.current_session.goals_achieved),
            "states_visited": [state.value for state in self.current_session.states_visited]
        }

    def end_conversation_session(self) -> Dict[str, Any]:
        """End the current conversation session and return summary"""
        
        if not self.current_session:
            return {"error": "No active session to end"}
        
        self.current_session.end_time = datetime.now()
        
        # Generate session summary
        session_summary = {
            "session_id": self.current_session.session_id,
            "duration_minutes": (self.current_session.end_time - self.current_session.start_time).total_seconds() / 60,
            "total_turns": len(self.current_session.turns),
            "states_visited": [state.value for state in self.current_session.states_visited],
            "goals_achieved": self.current_session.goals_achieved,
            "final_assessment_scores": self.current_session.assessment_scores,
            "therapeutic_outcomes": self.current_session.therapeutic_outcomes,
            "session_progress": self._calculate_session_progress()
        }
        
        # Save session to history
        self.conversation_history.append(self.current_session)
        self._save_conversation_session(self.current_session)
        
        # Clear current session
        self.current_session = None
        
        print(f"Conversation session ended. Duration: {session_summary['duration_minutes']:.1f} minutes")
        
        return session_summary

    def _save_conversation_session(self, session: ConversationSession):
        """Save conversation session to persistent storage"""
        
        session_dir = "data/conversations"
        os.makedirs(session_dir, exist_ok=True)
        
        session_file = os.path.join(session_dir, f"{session.session_id}.json")
        
        try:
            # Prepare session data for serialization
            session_data = {
                "session_id": session.session_id,
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "patient_id": session.patient_id,
                "turns": [
                    {
                        "timestamp": turn.timestamp.isoformat(),
                        "speaker": turn.speaker,
                        "content": turn.content,
                        "audio_path": turn.audio_path,
                        "image_path": turn.image_path,
                        "emotional_tone": turn.emotional_tone,
                        "cognitive_load": turn.cognitive_load,
                        "response_time": turn.response_time,
                        "confidence": turn.confidence
                    }
                    for turn in session.turns
                ],
                "states_visited": [state.value for state in session.states_visited],
                "assessment_scores": session.assessment_scores,
                "goals_achieved": session.goals_achieved,
                "therapeutic_outcomes": session.therapeutic_outcomes
            }
            
            # Write to file
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            print(f"Conversation session saved: {session_file}")
            
        except Exception as e:
            print(f"Error saving conversation session: {e}")

    def _load_conversation_templates(self) -> Dict[str, Any]:
        """Load conversation templates for different scenarios"""
        
        return {
            "greeting_templates": [
                "أهلاً وسهلاً! كيف حالك اليوم؟",
                "مرحباً! أتمنى أن تكون في حالة جيدة.",
                "صباح الخير! كيف تشعر اليوم؟"
            ],
            "encouragement_templates": [
                "أنت تقوم بعمل رائع!",
                "أعلم أن هذا ليس سهلاً، لكنك قوي.",
                "خطوة بخطوة، سنتقدم معاً."
            ],
            "memory_prompts": [
                "هل تتذكر...",
                "حدثني عن...",
                "ما رأيك في أن نتذكر..."
            ],
            "closing_templates": [
                "كان من الرائع التحدث معك اليوم.",
                "أتطلع لرؤيتك مرة أخرى قريباً.",
                "اعتني بنفسك حتى نلتقي مرة أخرى."
            ]
        }

    def _initialize_therapeutic_goals(self) -> List[str]:
        """Initialize therapeutic goals for sessions"""
        
        return [
            "patient_engagement",
            "positive_emotional_state",
            "memory_stimulation",
            "cognitive_exercise_completion",
            "social_interaction",
            "medication_compliance",
            "family_connection",
            "emotional_regulation",
            "reality_orientation",
            "self_care_awareness"
        ]

    def _define_state_transitions(self) -> Dict[ConversationState, List[ConversationState]]:
        """Define valid state transitions"""
        
        return {
            ConversationState.GREETING: [
                ConversationState.ASSESSMENT,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.MEMORY_EXERCISE
            ],
            ConversationState.ASSESSMENT: [
                ConversationState.COGNITIVE_TRAINING,
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.MEMORY_EXERCISE
            ],
            ConversationState.MEMORY_EXERCISE: [
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.COGNITIVE_TRAINING,
                ConversationState.FAMILY_INTERACTION
            ],
            ConversationState.EMOTIONAL_SUPPORT: [
                ConversationState.MEMORY_EXERCISE,
                ConversationState.FAMILY_INTERACTION,
                ConversationState.CLOSING
            ],
            ConversationState.COGNITIVE_TRAINING: [
                ConversationState.MEMORY_EXERCISE,
                ConversationState.ASSESSMENT,
                ConversationState.CLOSING
            ],
            ConversationState.MEDICATION_REMINDER: [
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.CLOSING
            ],
            ConversationState.FAMILY_INTERACTION: [
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.CLOSING
            ],
            ConversationState.CRISIS_INTERVENTION: [
                ConversationState.EMOTIONAL_SUPPORT,
                ConversationState.MEDICATION_REMINDER
            ],
            ConversationState.CLOSING: []
        }

    def get_conversation_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics for recent conversations"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            session for session in self.conversation_history
            if session.start_time >= cutoff_date
        ]
        
        if not recent_sessions:
            return {"message": "No recent conversations found"}
        
        # Calculate analytics
        total_sessions = len(recent_sessions)
        total_duration = sum(
            (session.end_time - session.start_time).total_seconds() / 60
            for session in recent_sessions if session.end_time
        )
        
        # Average session metrics
        avg_duration = total_duration / total_sessions if total_sessions > 0 else 0
        avg_turns = np.mean([len(session.turns) for session in recent_sessions])
        
        # Most common states
        all_states = []
        for session in recent_sessions:
            all_states.extend([state.value for state in session.states_visited])
        
        from collections import Counter
        state_frequency = Counter(all_states)
        
        # Goal achievement rates
        all_goals = []
        for session in recent_sessions:
            all_goals.extend(session.goals_achieved)
        
        goal_frequency = Counter(all_goals)
        
        return {
            "period_days": days,
            "total_sessions": total_sessions,
            "total_duration_minutes": total_duration,
            "average_duration_minutes": avg_duration,
            "average_turns_per_session": avg_turns,
            "most_common_states": dict(state_frequency.most_common(5)),
            "goal_achievement_frequency": dict(goal_frequency.most_common(10)),
            "session_frequency": total_sessions / days if days > 0 else 0
        }
