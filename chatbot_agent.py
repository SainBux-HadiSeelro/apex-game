"""
ApexRPS - 24/7 Live AI Customer Concierge & Knowledge Agent
Developed by Hadi Seelro | Agentic AI Specialist

Features:
1. 24/7 Offline/Online Autonomous Execution (Zero-crash guarantee).
2. Live Application Telemetry Injection (Game score, win rate, player archetype, session history).
3. Professional Customer Support & Portfolio Representative for Hadi Seelro.
4. Explains AI algorithms, Game Theory, and handles hiring/consulting inquiries.
5. Optional LLM API integration (OpenAI/Gemini/Groq) with automatic local fallback.
"""

import os
import re
from typing import Any, Dict, List, Optional


class LiveAppTelemetry:
    """Encapsulates real-time application context for the chatbot."""
    def __init__(
        self,
        total_rounds: int = 0,
        player_score: int = 0,
        agent_score: int = 0,
        ties: int = 0,
        win_rate: float = 0.0,
        current_streak: int = 0,
        active_persona: str = "Apex Autonomous Agent",
        player_archetype: str = "Calibrating...",
        recent_moves: Optional[List[Dict[str, str]]] = None,
    ):
        self.total_rounds = total_rounds
        self.player_score = player_score
        self.agent_score = agent_score
        self.ties = ties
        self.win_rate = win_rate
        self.current_streak = current_streak
        self.active_persona = active_persona
        self.player_archetype = player_archetype
        self.recent_moves = recent_moves or []

    def format_context_block(self) -> str:
        recent_str = (
            ", ".join([f"R{m.get('round')}: P({m.get('player')}) vs A({m.get('agent')}) -> {m.get('outcome')}" for m in self.recent_moves[-3:]])
            if self.recent_moves else "No rounds played yet."
        )
        return (
            f"--- LIVE SESSION TELEMETRY ---\n"
            f"• Total Rounds: {self.total_rounds}\n"
            f"• Player Score: {self.player_score} | Agent Score: {self.agent_score} | Ties: {self.ties}\n"
            f"• Player Win Rate: {self.win_rate}%\n"
            f"• Current Streak: {self.current_streak}\n"
            f"• Active Agent Mode: {self.active_persona}\n"
            f"• Player Behavioral Archetype: {self.player_archetype}\n"
            f"• Last 3 Rounds: {recent_str}\n"
            f"-------------------------------"
        )


DEVELOPER_PROFILE = {
    "name": "Hadi Seelro",
    "role": "Agentic AI Developer & Full-Stack Systems Engineer",
    "specialties": [
        "Autonomous Multi-Agent Architecture",
        "LLM Orchestration & Prompt Optimization",
        "Game-Theoretic & Statistical Machine Learning",
        "Production Streamlit, FastAPI, and Next.js applications",
        "RAG (Retrieval-Augmented Generation) Systems",
    ],
    "portfolio_pitch": (
        "Hadi Seelro specializes in building intelligent, autonomous agent systems "
        "that move beyond basic LLM prompts to self-directed, predictive, and goal-oriented AI."
    ),
    "contact": {
        "status": "Available for Freelance Projects, AI Consulting & Full-time Engineering Roles",
        "github": "https://github.com/SainBux-HadiSeelro/apex-game",
        "linkedin": "https://linkedin.com",
    }
}


class ChatbotConciergeAgent:
    """
    24/7 Autonomous Concierge Agent with deep domain knowledge and live state awareness.
    Guaranteed 100% uptime with smart local generation + optional cloud LLM expansion.
    """

    def __init__(self, api_key: Optional[str] = None, provider: str = "local"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.provider = provider

    def generate_response(self, user_query: str, telemetry: LiveAppTelemetry) -> str:
        """Processes user message and yields an authoritative, contextual response."""
        query_clean = user_query.strip().lower()

        # If user explicitly configured an OpenAI key and requested cloud LLM
        if self.api_key and self.provider == "openai":
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                system_prompt = (
                    f"You are the 24/7 Live AI Concierge for ApexRPS, developed by Hadi Seelro. "
                    f"You have complete awareness of the application, game theory mechanisms, and the developer's portfolio.\n\n"
                    f"{telemetry.format_context_block()}\n\n"
                    f"Developer Details: {DEVELOPER_PROFILE}\n"
                    f"Tone: Ultra-professional, sharp, engaging, articulate. Handle customer inquiries, "
                    f"explain AI game algorithms, review live scores, and represent Hadi Seelro for client inquiries."
                )
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query},
                    ],
                    max_tokens=450,
                    temperature=0.7,
                )
                return res.choices[0].message.content.strip()
            except Exception as e:
                # Fall back gracefully to local engine
                pass

        # Robust Autonomous Local Engine (Guarantees 24/7 uptime without external dependencies)
        return self._local_intent_router(query_clean, user_query, telemetry)

    def _local_intent_router(self, query_clean: str, raw_query: str, telemetry: LiveAppTelemetry) -> str:
        """High-precision heuristic and semantic knowledge router."""

        # 1. Score & Live Telemetry Inquiries
        if any(w in query_clean for w in ["score", "stats", "winning", "win rate", "streak", "record", "match"]):
            if telemetry.total_rounds == 0:
                return (
                    "📊 **Current Live Telemetry:**\n\n"
                    "No rounds have been played in this session yet! Choose **Rock**, **Paper**, or **Scissors** above "
                    "to engage the Agentic Arena. Once you start, I'll track your win rate, psychological patterns, and counter-play!"
                )
            
            lead_status = (
                "🎉 You are currently leading the match!"
                if telemetry.player_score > telemetry.agent_score
                else "🤖 The AI Agent currently holds the lead."
                if telemetry.agent_score > telemetry.player_score
                else "⚖️ The match is currently tied!"
            )

            return (
                f"📊 **Live Match Telemetry (Round {telemetry.total_rounds}):**\n\n"
                f"• **Scoreboard:** Player: **{telemetry.player_score}** | Agent: **{telemetry.agent_score}** | Ties: **{telemetry.ties}**\n"
                f"• **Your Win Rate:** **{telemetry.win_rate}%**\n"
                f"• **Streak Status:** **{telemetry.current_streak}**\n"
                f"• **Behavioral Archetype:** `{telemetry.player_archetype}`\n"
                f"• **Active Opponent:** `{telemetry.active_persona}`\n\n"
                f"_{lead_status}_ What move do you plan to challenge the agent with next?"
            )

        # 2. How the AI Agent works / Predicts moves
        if any(w in query_clean for w in ["how", "predict", "algorithm", "markov", "cheat", "ai work", "thinking", "reasoning", "game theory"]):
            return (
                "🧠 **How the Apex Agentic AI System Works:**\n\n"
                "Unlike conventional games that use naive `random.choice()`, this platform deploys a **Multi-Agent Decision Architecture**:\n\n"
                "1. **Markov Transition Matrix (1st & 2nd Order):**\n"
                "   Calculates $P(Move_t \\mid Move_{t-1}, Move_{t-2})$. It tracks your historical move sequences and calculates transition probabilities.\n\n"
                "2. **Win-Stay, Lose-Shift (WSLS) Cognitive Engine:**\n"
                "   Implements empirical human behavioral game theory. When humans win, they have a 60%+ bias to repeat; when they lose, they shift cyclically.\n\n"
                "3. **Bayesian Ensemble Consensus:**\n"
                "   Dynamically shifts weights: early rounds rely on psychological heuristics, while late rounds leverage high-order Markov data.\n\n"
                "4. **Real-time Introspection:**\n"
                "   Look at the **Agent Reasoning Stream** in the Arena to view probability distributions and confidence metrics before each counter-move!"
            )

        # 3. Developer / Hadi Seelro Portfolio Inquiries
        if any(w in query_clean for w in ["developer", "hadi", "seelro", "who made", "creator", "portfolio", "author"]):
            specialties = "\n".join([f"• {s}" for s in DEVELOPER_PROFILE["specialties"]])
            return (
                f"👨‍💻 **Meet the Developer: Hadi Seelro**\n\n"
                f"**Role:** {DEVELOPER_PROFILE['role']}\n\n"
                f"{DEVELOPER_PROFILE['portfolio_pitch']}\n\n"
                f"**Core Expertise:**\n{specialties}\n\n"
                f"**Professional Availability:**\n"
                f"• {DEVELOPER_PROFILE['contact']['status']}\n\n"
                f"Want to collaborate or discuss an AI automation system for your business? Just ask me how to get in touch!"
            )

        # 4. Hiring / Commercial / Freelance Inquiries
        if any(w in query_clean for w in ["hire", "contact", "freelance", "business", "project", "quote", "cost", "collaborate", "email"]):
            return (
                "💼 **Work With Hadi Seelro:**\n\n"
                "Looking to integrate Agentic AI, custom autonomous workflows, or modern intelligent web apps into your business?\n\n"
                "**Services Offered:**\n"
                "1. **Custom Autonomous Agents** (Self-reflective task execution, multi-agent systems)\n"
                "2. **Production RAG & Vector Pipelines** (Enterprise doc search & automated workflows)\n"
                "3. **Full-Stack AI Interfaces** (High-performance Streamlit, FastAPI, React dashboards)\n"
                "4. **Predictive Statistical Engines** (Game theory, decision intelligence)\n\n"
                "💬 Let's schedule a technical discovery call! You can leave your project scope here or reach out directly via Hadi's portfolio links."
            )

        # 5. Game Rules / RPS Explanation
        if any(w in query_clean for w in ["rule", "play", "help", "guide", "tie"]):
            return (
                "🎮 **Rules & Strategic Mechanics:**\n\n"
                "• **Rock (✊)** crushes Scissors (✌️)\n"
                "• **Scissors (✌️)** cuts Paper (🖐️)\n"
                "• **Paper (🖐️)** covers Rock (✊)\n\n"
                "**Pro Strategy Against Apex Agent:**\n"
                "To counter the AI, deliberately randomize your rhythm or alternate between Win-Stay and cyclic shifts to dilute the Markov transition matrix!"
            )

        # 6. Reset or Troubleshoot
        if any(w in query_clean for w in ["reset", "restart", "clear", "error", "bug"]):
            return (
                "🔄 **Session Management:**\n\n"
                "You can reset the game session, wipe the Markov transition memory, and start a fresh match at any time using the **'Reset Match'** button in the sidebar!\n"
                "If you want to preserve your telemetry, click **'Export Session JSON'** before resetting."
            )

        # 7. Greetings
        if any(w in query_clean for w in ["hi", "hello", "hey", "salam", "aoa", "greetings"]):
            return (
                f"👋 **Greetings! I am the Apex 24/7 Concierge Agent.**\n\n"
                f"I have live telemetry on your current game session ({telemetry.player_score}-{telemetry.agent_score} scoreline), "
                f"full technical knowledge of our AI decision engine, and can assist you with developer inquiries regarding **Hadi Seelro**.\n\n"
                f"How can I assist you right now?"
            )

        # Default Intelligent Fallback
        return (
            f"🤖 **Apex AI Concierge Assistant:**\n\n"
            f"I received your inquiry: *\"{raw_query}\"*\n\n"
            f"Here is what I can assist you with 24/7:\n"
            f"• 📊 **Match Telemetry:** Ask about your current win rate, scores, or streak.\n"
            f"• 🧠 **AI Architecture:** Inquire how our Markov and Psychological agents predict moves.\n"
            f"• 👨‍💻 **Developer Portfolio:** Learn about **Hadi Seelro**'s background in Agentic AI systems.\n"
            f"• 💼 **Hiring & Consulting:** Explore collaboration on custom AI projects.\n\n"
            f"Feel free to ask any specific question!"
        )
