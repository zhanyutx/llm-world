#!/usr/bin/env python3
"""
Interactive Storytelling Platform - Python Implementation
A complete implementation using Streamlit for UI and OpenAI for LLM integration
"""

import streamlit as st
import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, asdict
from enum import Enum
import openai
import os

# Configure page
st.set_page_config(
    page_title="Interactive Storytelling Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    .narrator-message {
        background: linear-gradient(135deg, #8360c3 0%, #2ebf91 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-style: italic;
        border-left: 4px solid #9C27B0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF5722;
    }
    
    .world-state {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .typing-indicator {
        color: #4CAF50;
        font-weight: bold;
        animation: pulse 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { opacity: 1; }
        to { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# Data Classes
@dataclass
class Agent:
    id: str
    name: str
    role: str
    avatar: str
    personality: str
    background: str
    goals: List[str]
    is_typing: bool = False
    preferred_model: str = "gpt-3.5-turbo"

@dataclass
class Message:
    id: str
    speaker: str
    content: str
    timestamp: datetime
    message_type: Literal["dialogue", "narration", "intervention", "system"]
    metadata: Dict = None

@dataclass
class WorldState:
    location: str
    time_of_day: str
    weather: str
    mood: str
    active_events: List[str]
    lore: Dict[str, str]
    rules: List[str]

class LLMProvider:
    """Pluggable LLM Provider Interface"""
    
    def __init__(self, provider_name: str = "openai"):
        self.provider_name = provider_name
        self.setup_provider()
    
    def setup_provider(self):
        """Setup the LLM provider (OpenAI, Anthropic, etc.)"""
        if self.provider_name == "openai":
            # OpenAI setup
            openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
        elif self.provider_name == "mock":
            # Mock provider for testing
            pass
    
    async def generate_response(self, prompt: str, agent: Agent) -> str:
        """Generate response from LLM"""
        if self.provider_name == "mock":
            return await self._mock_response(agent)
        elif self.provider_name == "openai":
            return await self._openai_response(prompt, agent)
        else:
            raise ValueError(f"Unknown provider: {self.provider_name}")
    
    async def _mock_response(self, agent: Agent) -> str:
        """Mock responses for demonstration"""
        await asyncio.sleep(random.uniform(1, 3))  # Simulate API delay
        
        responses = {
            "Elara": [
                "The ancient magic still flows through these ruins, whispering secrets of forgotten times.",
                "I sense a presence here... something watching us from the shadows.",
                "My elven senses detect traces of old enchantments woven into these stones.",
                "The moonlight reveals runes that speak of a great battle fought here long ago.",
                "Perhaps we should tread carefully - the spirits of this place seem restless."
            ],
            "Marcus": [
                "My sword arm grows tense. There's danger lurking in these halls.",
                "I've faced many foes, but something about this place chills my warrior's heart.",
                "The shadows move strangely here. We should stay alert and ready for battle.",
                "These ruins have seen too much bloodshed. I can feel the weight of history.",
                "Whatever evil once dwelt here may yet linger. We must be prepared."
            ]
        }
        
        agent_responses = responses.get(agent.name, ["I'm not sure how to respond."])
        return random.choice(agent_responses)
    
    async def _openai_response(self, prompt: str, agent: Agent) -> str:
        """Generate response using OpenAI API"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=agent.preferred_model,
                messages=[
                    {"role": "system", "content": f"You are {agent.name}, {agent.role}. {agent.personality}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

class StorytellingEngine:
    """Core engine managing the storytelling session"""
    
    def __init__(self):
        self.agents: List[Agent] = []
        self.messages: List[Message] = []
        self.world_state: WorldState = None
        self.llm_provider: LLMProvider = None
        self.session_active: bool = False
        self.auto_play: bool = False
        
        self.initialize_default_setup()
    
    def initialize_default_setup(self):
        """Initialize with default agents and world"""
        # Default Agents
        self.agents = [
            Agent(
                id="agent_1",
                name="Elara",
                role="Elven Mage",
                avatar="🧝‍♀️",
                personality="Wise, mystical, and cautious. Speaks with ancient wisdom and notices magical phenomena.",
                background="A centuries-old elf who has studied the arcane arts in the hidden libraries of Rivendell.",
                goals=["Uncover ancient secrets", "Protect magical artifacts", "Guide companions safely"]
            ),
            Agent(
                id="agent_2", 
                name="Marcus",
                role="Human Warrior",
                avatar="⚔️",
                personality="Brave, direct, and protective. Values honor and loyalty above all else.",
                background="A seasoned knight who has defended the realm against countless threats.",
                goals=["Protect the innocent", "Defeat evil", "Maintain honor"]
            )
        ]
        
        # Default World State
        self.world_state = WorldState(
            location="Ancient Ruins of Eldermoor",
            time_of_day="Night",
            weather="Clear, moonlit sky",
            mood="Tense and mysterious",
            active_events=["Mysterious shadows moving", "Ancient magic stirring"],
            lore={
                "Eldermoor": "Once a great city, now ruins filled with forgotten magic",
                "The Temple": "Said to house an artifact of immense power",
                "The Curse": "Legend speaks of a curse that befell the city centuries ago"
            },
            rules=[
                "Magic is unpredictable in these ruins",
                "The dead do not rest easy here",
                "Ancient traps still function"
            ]
        )
        
        # Initialize LLM Provider
        self.llm_provider = LLMProvider("mock")  # Change to "openai" for real API
        
        # Add initial narrator message
        self.add_message(
            speaker="Narrator",
            content="Welcome to the Ancient Ruins of Eldermoor. Two adventurers stand at the entrance of a mysterious temple, moonlight casting eerie shadows across crumbling stone pillars...",
            message_type="narration"
        )
    
    def add_message(self, speaker: str, content: str, message_type: str, metadata: Dict = None):
        """Add a new message to the conversation"""
        message = Message(
            id=f"msg_{len(self.messages)}_{int(time.time())}",
            speaker=speaker,
            content=content,
            timestamp=datetime.now(),
            message_type=message_type,
            metadata=metadata or {}
        )
        self.messages.append(message)
    
    def get_conversation_context(self, limit: int = 10) -> str:
        """Get recent conversation context for LLM"""
        recent_messages = self.messages[-limit:]
        context_parts = []
        
        # Add world state context
        context_parts.append(f"Current Location: {self.world_state.location}")
        context_parts.append(f"Time: {self.world_state.time_of_day}")
        context_parts.append(f"Mood: {self.world_state.mood}")
        context_parts.append(f"Active Events: {', '.join(self.world_state.active_events)}")
        context_parts.append("---")
        
        # Add recent conversation
        for msg in recent_messages:
            if msg.message_type != "system":
                context_parts.append(f"{msg.speaker}: {msg.content}")
        
        return "\n".join(context_parts)
    
    async def generate_agent_response(self, agent_id: str) -> Optional[str]:
        """Generate response for a specific agent"""
        agent = next((a for a in self.agents if a.id == agent_id), None)
        if not agent:
            return None
        
        # Set typing indicator
        agent.is_typing = True
        
        try:
            # Build context
            context = self.get_conversation_context()
            prompt = f"""
            Context: {context}
            
            You are {agent.name}. Respond as your character would in this situation.
            Keep your response to 1-2 sentences and stay in character.
            """
            
            response = await self.llm_provider.generate_response(prompt, agent)
            
            # Add response to conversation
            self.add_message(
                speaker=agent.name,
                content=response,
                message_type="dialogue",
                metadata={"agent_id": agent_id}
            )
            
            return response
            
        finally:
            agent.is_typing = False
    
    def update_world_state(self, updates: Dict):
        """Update world state with new information"""
        for key, value in updates.items():
            if hasattr(self.world_state, key):
                setattr(self.world_state, key, value)
    
    def get_next_agent(self) -> Optional[Agent]:
        """Determine which agent should respond next"""
        if not self.messages:
            return self.agents[0]
        
        last_speaker = self.messages[-1].speaker
        
        # Find agents that didn't speak last
        available_agents = [a for a in self.agents if a.name != last_speaker]
        
        if available_agents:
            return random.choice(available_agents)
        
        return None

# Streamlit App
def main():
    # Initialize session state
    if 'engine' not in st.session_state:
        st.session_state.engine = StorytellingEngine()
    
    engine = st.session_state.engine
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">📚 Interactive Storytelling Platform</h1>
        <p style="color: #E8E8E8; margin: 0;">Collaborative AI-powered storytelling with dynamic world-building</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Control Panel
    with st.sidebar:
        st.header("🎮 Control Panel")
        
        # Session Controls
        st.subheader("Session Controls")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start" if not engine.session_active else "⏸️ Pause"):
                engine.session_active = not engine.session_active
                status = "started" if engine.session_active else "paused"
                engine.add_message("System", f"Session {status}.", "system")
                st.rerun()
        
        with col2:
            if st.button("💾 Save"):
                # In a real app, save to database/file
                st.success("Session saved!")
        
        # Auto-play toggle
        engine.auto_play = st.toggle("🤖 Auto-play", value=engine.auto_play)
        
        # Agent trigger
        if st.button("🎭 Trigger Next Agent"):
            if engine.session_active:
                next_agent = engine.get_next_agent()
                if next_agent:
                    # Use asyncio to run the async function
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(engine.generate_agent_response(next_agent.id))
                    loop.close()
                    st.rerun()
        
        st.divider()
        
        # LLM Settings
        st.subheader("🔧 LLM Settings")
        provider = st.selectbox(
            "Provider",
            ["mock", "openai", "anthropic"],
            index=0
        )
        
        if provider != engine.llm_provider.provider_name:
            engine.llm_provider = LLMProvider(provider)
        
        if provider == "openai":
            api_key = st.text_input("OpenAI API Key", type="password")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        st.divider()
        
        # Agent Status
        st.subheader("🤖 Agent Status")
        for agent in engine.agents:
            with st.container():
                st.markdown(f"""
                <div class="agent-card">
                    <h4>{agent.avatar} {agent.name}</h4>
                    <p><strong>Role:</strong> {agent.role}</p>
                    <p><strong>Status:</strong> {'🤔 Thinking...' if agent.is_typing else '💭 Ready'}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # World State Display
        st.subheader("🌍 World State")
        with st.container():
            st.markdown(f"""
            <div class="world-state">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div><strong>📍 Location:</strong> {engine.world_state.location}</div>
                    <div><strong>🕐 Time:</strong> {engine.world_state.time_of_day}</div>
                    <div><strong>🌤️ Weather:</strong> {engine.world_state.weather}</div>
                    <div><strong>😐 Mood:</strong> {engine.world_state.mood}</div>
                </div>
                <div style="margin-top: 1rem;">
                    <strong>📅 Active Events:</strong> {', '.join(engine.world_state.active_events)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Chat Messages
        st.subheader("💬 Story Timeline")
        
        # Messages container
        messages_container = st.container()
        with messages_container:
            for message in engine.messages:
                timestamp = message.timestamp.strftime("%H:%M:%S")
                
                if message.message_type == "narration":
                    st.markdown(f"""
                    <div class="narrator-message">
                        <strong>📖 {message.speaker}</strong> <small>({timestamp})</small><br>
                        {message.content}
                    </div>
                    """, unsafe_allow_html=True)
                
                elif message.message_type == "dialogue":
                    agent = next((a for a in engine.agents if a.name == message.speaker), None)
                    avatar = agent.avatar if agent else "💬"
                    
                    st.markdown(f"""
                    <div class="agent-card">
                        <strong>{avatar} {message.speaker}</strong> <small>({timestamp})</small><br>
                        "{message.content}"
                    </div>
                    """, unsafe_allow_html=True)
                
                elif message.message_type == "intervention":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👑 {message.speaker}</strong> <small>({timestamp})</small><br>
                        {message.content}
                    </div>
                    """, unsafe_allow_html=True)
                
                elif message.message_type == "system":
                    st.info(f"🔧 {message.content}")
        
        # User Input Area
        st.subheader("🎬 Director Controls")
        
        # Intervention mode
        intervention_mode = st.selectbox(
            "Intervention Mode",
            ["narrator", "character", "director"],
            help="Choose how you want to contribute to the story"
        )
        
        # Input form
        with st.form("user_input_form"):
            user_input = st.text_area(
                "Your Input",
                placeholder=f"Enter as {intervention_mode}... (e.g., 'A mysterious figure emerges from the shadows')",
                height=100
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submit = st.form_submit_button("📤 Send")
            with col2:
                world_update = st.form_submit_button("🌍 Update World")
            
            if submit and user_input.strip():
                speaker = "Narrator" if intervention_mode == "narrator" else "Director"
                msg_type = "narration" if intervention_mode == "narrator" else "intervention"
                
                engine.add_message(speaker, user_input, msg_type)
                st.rerun()
            
            if world_update and user_input.strip():
                # Parse world updates (simple format: "location: New Place")
                if "location:" in user_input.lower():
                    new_location = user_input.split("location:")[-1].strip()
                    engine.update_world_state({"location": new_location})
                    engine.add_message("System", f"Location changed to: {new_location}", "system")
                
                if "mood:" in user_input.lower():
                    new_mood = user_input.split("mood:")[-1].strip()
                    engine.update_world_state({"mood": new_mood})
                    engine.add_message("System", f"Mood changed to: {new_mood}", "system")
                
                st.rerun()
    
    with col2:
        # World Building Tools
        st.subheader("🏗️ World Builder")
        
        # Quick world updates
        with st.expander("Quick Updates"):
            new_location = st.text_input("Change Location")
            new_mood = st.text_input("Change Mood")
            new_event = st.text_input("Add Event")
            
            if st.button("Apply Changes"):
                updates = {}
                if new_location: updates["location"] = new_location
                if new_mood: updates["mood"] = new_mood
                if new_event: 
                    current_events = engine.world_state.active_events.copy()
                    current_events.append(new_event)
                    updates["active_events"] = current_events
                
                if updates:
                    engine.update_world_state(updates)
                    engine.add_message("System", "World state updated.", "system")
                    st.rerun()
        
        # Lore Display
        with st.expander("📜 World Lore"):
            for key, value in engine.world_state.lore.items():
                st.write(f"**{key}:** {value}")
        
        # Rules Display
        with st.expander("⚖️ World Rules"):
            for i, rule in enumerate(engine.world_state.rules, 1):
                st.write(f"{i}. {rule}")
        
        # Export/Import
        with st.expander("💾 Data Management"):
            if st.button("📥 Export Session"):
                session_data = {
                    "messages": [asdict(msg) for msg in engine.messages],
                    "world_state": asdict(engine.world_state),
                    "agents": [asdict(agent) for agent in engine.agents]
                }
                st.download_button(
                    "Download Session Data",
                    json.dumps(session_data, indent=2, default=str),
                    file_name=f"story_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Auto-refresh for real-time updates
    if engine.auto_play and engine.session_active:
        time.sleep(5)  # Wait 5 seconds
        next_agent = engine.get_next_agent()
        if next_agent:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(engine.generate_agent_response(next_agent.id))
            loop.close()
            st.rerun()

if __name__ == "__main__":
    main()