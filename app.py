"""
ApexRPS - Autonomous Agentic Rock Paper Scissors Arena & 24/7 Live AI Concierge
Engineered by Hadi Seelro | Agentic AI Specialist
"""

import json
from datetime import datetime
import streamlit as st
import pandas as pd

from agent_engine import (
    ApexAgentEngine,
    Move,
    Outcome,
    RoundRecord,
    evaluate_round,
    classify_player_style,
)
from chatbot_agent import (
    ChatbotConciergeAgent,
    LiveAppTelemetry,
    DEVELOPER_PROFILE,
)

# ---------------------------------------------------------
# Page Configuration & Metadata
# ---------------------------------------------------------
st.set_page_config(
    page_title="ApexRPS | Autonomous Agentic Arena",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Ultra-Modern Cyberpunk / Glassmorphism UI Theme
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Global Imports & Base Theme */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', -apple-system, sans-serif;
}

/* Glassmorphism containers */
.glass-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 16px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

/* Hero Badge */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 9999px;
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
    border: 1px solid rgba(168, 85, 247, 0.4);
    font-size: 0.82rem;
    font-weight: 600;
    color: #c084fc;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Metric Display Boxes */
.metric-container {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* Confrontation Showdown Arena */
.showdown-box {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: radial-gradient(circle at center, rgba(30, 27, 75, 0.8), rgba(15, 23, 42, 0.95));
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 28px 16px;
    margin: 16px 0;
}
.fighter-card {
    text-align: center;
    padding: 10px;
}
.fighter-icon {
    font-size: 4rem;
    filter: drop-shadow(0 0 16px rgba(99, 102, 241, 0.4));
    animation: float 3s ease-in-out infinite;
}
.vs-badge {
    font-size: 1.5rem;
    font-weight: 900;
    color: #ef4444;
    text-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
    background: rgba(0,0,0,0.4);
    padding: 8px 14px;
    border-radius: 50%;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

/* Agent Reasoning Box */
.reasoning-box {
    background: #090d16;
    border-left: 4px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    color: #cbd5e1;
    margin-top: 10px;
    line-height: 1.6;
}

/* Outcome Banners */
.outcome-win {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
    border: 1px solid #10b981;
    color: #34d399;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: 700;
    font-size: 1.1rem;
}
.outcome-loss {
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.2), rgba(185, 28, 28, 0.1));
    border: 1px solid #ef4444;
    color: #f87171;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: 700;
    font-size: 1.1rem;
}
.outcome-tie {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.2), rgba(180, 83, 9, 0.1));
    border: 1px solid #f59e0b;
    color: #fbbf24;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: 700;
    font-size: 1.1rem;
}

/* Buttons styling */
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.2s ease;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = ApexAgentEngine()

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotConciergeAgent()

if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "agent_score" not in st.session_state:
    st.session_state.agent_score = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome to ApexRPS!** I am your 24/7 Live AI Concierge. "
                "I am fully synchronized with your live match telemetry, understand the AI's predictive game theory, "
                "and can answer any questions about the platform or its developer, **Hadi Seelro**.\n\n"
                "Play a round or ask me anything!"
            ),
        }
    ]
if "last_reasoning" not in st.session_state:
    st.session_state.last_reasoning = None
if "last_round" not in st.session_state:
    st.session_state.last_round = None


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def get_telemetry() -> LiveAppTelemetry:
    total = len(st.session_state.history)
    win_rate = (
        round((st.session_state.player_score / total) * 100, 1) if total > 0 else 0.0
    )
    style_info = classify_player_style(st.session_state.history)
    recent = [
        {
            "round": r.round_number,
            "player": r.player_move.value,
            "agent": r.agent_move.value,
            "outcome": r.outcome.value,
        }
        for r in st.session_state.history[-5:]
    ]
    return LiveAppTelemetry(
        total_rounds=total,
        player_score=st.session_state.player_score,
        agent_score=st.session_state.agent_score,
        ties=st.session_state.ties,
        win_rate=win_rate,
        current_streak=st.session_state.streak,
        active_persona=st.session_state.get("selected_persona", "Apex Autonomous Agent"),
        player_archetype=style_info["archetype"],
        recent_moves=recent,
    )


def handle_player_move(choice_str: str):
    player_move = Move(choice_str)
    persona = st.session_state.get("selected_persona", "Apex Autonomous Agent")

    # Agent deliberates and decides
    reasoning = st.session_state.engine.decide_move(persona=persona)
    agent_move = reasoning.chosen_move

    # Determine outcome
    outcome = evaluate_round(player_move, agent_move)

    # Update scores & streaks
    if outcome == Outcome.WIN:
        st.session_state.player_score += 1
        st.session_state.streak = (
            st.session_state.streak + 1 if st.session_state.streak > 0 else 1
        )
    elif outcome == Outcome.LOSS:
        st.session_state.agent_score += 1
        st.session_state.streak = (
            st.session_state.streak - 1 if st.session_state.streak < 0 else -1
        )
    else:
        st.session_state.ties += 1

    round_record = RoundRecord(
        round_number=len(st.session_state.history) + 1,
        player_move=player_move,
        agent_move=agent_move,
        outcome=outcome,
        agent_confidence=reasoning.confidence,
        reasoning_summary=f"Predicted {reasoning.predicted_player_move.value} with {reasoning.confidence}% confidence.",
    )

    # Commit to engine memory
    st.session_state.engine.record_round(round_record)
    st.session_state.history.append(round_record)
    st.session_state.last_reasoning = reasoning
    st.session_state.last_round = round_record


def reset_session():
    st.session_state.engine = ApexAgentEngine()
    st.session_state.player_score = 0
    st.session_state.agent_score = 0
    st.session_state.ties = 0
    st.session_state.streak = 0
    st.session_state.history = []
    st.session_state.last_reasoning = None
    st.session_state.last_round = None
    st.toast("Match reset. Agent neural memory refreshed!", icon="🔄")


# ---------------------------------------------------------
# Sidebar Configuration & Telemetry
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="hero-badge">⚡ Agentic AI Platform</div>', unsafe_allow_html=True)
    st.title("ApexRPS")
    st.caption("Predictive Game Theory & Live Autonomous AI Agent")

    st.markdown("---")
    st.subheader("🤖 Opponent Agent Personality")
    persona_options = [
        "Apex Autonomous Agent",
        "Pattern Predictor (Markov)",
        "Psychological Agent (WSLS)",
        "Novice Bot (Random)",
    ]
    st.session_state.selected_persona = st.selectbox(
        "Choose AI Engine:",
        persona_options,
        index=0,
        help="Apex Autonomous Agent uses Bayesian weighting of Markov chains + behavioral psychology.",
    )

    persona_badges = {
        "Apex Autonomous Agent": "🔥 Adaptive Bayesian Multi-Agent Ensemble",
        "Pattern Predictor (Markov)": "📈 1st & 2nd Order Transition Matrices",
        "Psychological Agent (WSLS)": "🧠 Win-Stay Lose-Shift Behavioral Heuristic",
        "Novice Bot (Random)": "🎲 Uniform Baseline Benchmark",
    }
    st.info(persona_badges[st.session_state.selected_persona])

    st.markdown("---")
    st.subheader("⚡ Live Match HUD")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            f'<div class="metric-container"><div class="metric-value">{st.session_state.player_score}</div><div class="metric-label">Player</div></div>',
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            f'<div class="metric-container"><div class="metric-value">{st.session_state.agent_score}</div><div class="metric-label">Agent</div></div>',
            unsafe_allow_html=True,
        )

    col_s3, col_s4 = st.columns(2)
    total_rounds = len(st.session_state.history)
    win_pct = round((st.session_state.player_score / total_rounds) * 100, 1) if total_rounds > 0 else 0.0
    with col_s3:
        st.markdown(
            f'<div class="metric-container"><div class="metric-value">{st.session_state.ties}</div><div class="metric-label">Ties</div></div>',
            unsafe_allow_html=True,
        )
    with col_s4:
        st.markdown(
            f'<div class="metric-container"><div class="metric-value">{win_pct}%</div><div class="metric-label">Win Rate</div></div>',
            unsafe_allow_html=True,
        )

    streak_txt = (
        f"🔥 Player +{st.session_state.streak}"
        if st.session_state.streak > 0
        else f"❄️ Agent +{abs(st.session_state.streak)}"
        if st.session_state.streak < 0
        else "⚖️ Even"
    )
    st.caption(f"**Streak Momentum:** {streak_txt}")

    st.markdown("---")
    st.subheader("⚙️ Session Controls")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Reset Match", use_container_width=True):
            reset_session()
            st.rerun()
    with c2:
        if st.session_state.history:
            export_data = [
                {
                    "round": r.round_number,
                    "player": r.player_move.value,
                    "agent": r.agent_move.value,
                    "outcome": r.outcome.value,
                    "confidence": r.agent_confidence,
                }
                for r in st.session_state.history
            ]
            st.download_button(
                label="📥 Export JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"apex_rps_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

    st.markdown("---")
    st.markdown(
        f"**Developer:** [{DEVELOPER_PROFILE['name']}](https://github.com/SainBux-HadiSeelro)  \n"
        f"*{DEVELOPER_PROFILE['role']}*"
    )


# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
col_h1, col_h2 = st.columns([0.7, 0.3])
with col_h1:
    st.markdown('<div class="hero-badge">⚡ Autonomous Agentic Game Engine</div>', unsafe_allow_html=True)
    st.title("APEX-RPS: Predictive AI Arena")
    st.markdown(
        "Play Rock-Paper-Scissors against an autonomous agent driven by **Markov Chain pattern analysis**, "
        "**behavioral game theory**, and real-time **chain-of-thought introspection**."
    )
with col_h2:
    st.markdown(
        """
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px 16px; text-align: right;">
            <div style="font-size: 0.8rem; color: #94a3b8;">PORTFOLIO SHOWCASE</div>
            <div style="font-weight: 700; color: #38bdf8;">Hadi Seelro</div>
            <div style="font-size: 0.75rem; color: #cbd5e1;">Agentic AI & Systems Specialist</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Tabbed Navigation
# ---------------------------------------------------------
tab_arena, tab_telemetry, tab_chatbot, tab_specs = st.tabs(
    ["⚔️ Battle Arena", "📊 Telemetry & Analytics", "💬 24/7 AI Concierge", "🧠 Architecture & Specs"]
)

# =========================================================
# TAB 1: BATTLE ARENA
# =========================================================
with tab_arena:
    st.markdown("### 🎮 Select Your Move")
    st.write("Deploy your gesture to engage the autonomous predictive engine:")

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("✊ Rock", key="btn_rock", use_container_width=True, type="primary"):
            handle_player_move(Move.ROCK.value)
            st.rerun()
    with col_btn2:
        if st.button("🖐️ Paper", key="btn_paper", use_container_width=True, type="primary"):
            handle_player_move(Move.PAPER.value)
            st.rerun()
    with col_btn3:
        if st.button("✌️ Scissors", key="btn_scissors", use_container_width=True, type="primary"):
            handle_player_move(Move.SCISSORS.value)
            st.rerun()

    # Showdown Display
    if st.session_state.last_round:
        lr = st.session_state.last_round
        st.markdown("---")
        
        # Showdown Arena Box
        st.markdown(
            f"""
            <div class="showdown-box">
                <div class="fighter-card">
                    <div style="font-size: 0.9rem; color: #94a3b8; font-weight: 600;">YOU</div>
                    <div class="fighter-icon">{lr.player_move.emoji}</div>
                    <div style="font-weight: 700; color: #f8fafc; font-size: 1.2rem;">{lr.player_move.value}</div>
                </div>
                <div>
                    <div class="vs-badge">VS</div>
                </div>
                <div class="fighter-card">
                    <div style="font-size: 0.9rem; color: #94a3b8; font-weight: 600;">AGENT ({st.session_state.selected_persona.split()[0]})</div>
                    <div class="fighter-icon">{lr.agent_move.emoji}</div>
                    <div style="font-weight: 700; color: #f8fafc; font-size: 1.2rem;">{lr.agent_move.value}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Outcome Badge
        if lr.outcome == Outcome.WIN:
            st.markdown('<div class="outcome-win">🎉 VICTORY! Your move outsmarted the Agent!</div>', unsafe_allow_html=True)
            st.balloons()
        elif lr.outcome == Outcome.LOSS:
            st.markdown('<div class="outcome-loss">🤖 DEFEAT! The Agent accurately anticipated your move!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="outcome-tie">⚖️ DRAW! Minds in synchronized equilibrium.</div>', unsafe_allow_html=True)

        # Real-time Agent Reasoning Stream
        if st.session_state.last_reasoning:
            reas = st.session_state.last_reasoning
            st.markdown("#### 🧠 Agent Real-Time Chain-of-Thought (Telemetry)")
            with st.container():
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span style="font-weight: 700; color: #818cf8;">STRATEGY: {reas.strategy_used}</span>
                            <span style="background: rgba(99, 102, 241, 0.2); border: 1px solid #6366f1; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; color: #c7d2fe;">
                                Confidence: {reas.confidence}%
                            </span>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Probabilities breakdown
                col_p1, col_p2, col_p3 = st.columns(3)
                probs = reas.probability_distribution
                with col_p1:
                    st.metric("P(Rock)", f"{round(probs.get('Rock', 0.33) * 100, 1)}%")
                    st.progress(probs.get('Rock', 0.33))
                with col_p2:
                    st.metric("P(Paper)", f"{round(probs.get('Paper', 0.33) * 100, 1)}%")
                    st.progress(probs.get('Paper', 0.33))
                with col_p3:
                    st.metric("P(Scissors)", f"{round(probs.get('Scissors', 0.33) * 100, 1)}%")
                    st.progress(probs.get('Scissors', 0.33))

                # Step-by-step thoughts
                st.markdown("**Deliberation Steps:**")
                thoughts_html = "<br>".join([f"› {t}" for t in reas.thought_chain])
                st.markdown(f'<div class="reasoning-box">{thoughts_html}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👆 Make your first move above to initiate the Agentic predictive engine!")


# =========================================================
# TAB 2: TELEMETRY & ANALYTICS
# =========================================================
with tab_telemetry:
    st.markdown("### 📊 Game Telemetry & Cognitive Profiling")
    
    if not st.session_state.history:
        st.warning("No telemetry recorded yet. Play a few rounds in the Battle Arena to generate behavioral analytics.")
    else:
        # Behavioral Archetype
        style = classify_player_style(st.session_state.history)
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="font-size: 1.5rem;">{style['badge']}</span>
                    <h3 style="margin: 0; color: #38bdf8;">Player Cognitive Archetype: {style['archetype']}</h3>
                </div>
                <p style="color: #cbd5e1; margin: 0;">{style['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_g1, col_g2 = st.columns(2)
        
        # Move Distribution
        with col_g1:
            st.markdown("#### Move Frequency Distribution")
            p_moves = [r.player_move.value for r in st.session_state.history]
            a_moves = [r.agent_move.value for r in st.session_state.history]
            
            df_dist = pd.DataFrame({
                "Player": [p_moves.count("Rock"), p_moves.count("Paper"), p_moves.count("Scissors")],
                "Agent": [a_moves.count("Rock"), a_moves.count("Paper"), a_moves.count("Scissors")],
            }, index=["Rock", "Paper", "Scissors"])
            
            st.bar_chart(df_dist)

        # Outcome Breakdown
        with col_g2:
            st.markdown("#### Match Outcome Proportions")
            outcomes = [r.outcome.value for r in st.session_state.history]
            df_outcomes = pd.DataFrame({
                "Count": [
                    outcomes.count(Outcome.WIN.value),
                    outcomes.count(Outcome.LOSS.value),
                    outcomes.count(Outcome.TIE.value),
                ]
            }, index=["Player Wins", "Agent Wins", "Ties"])
            st.bar_chart(df_outcomes)

        # Detailed Round Log Table
        st.markdown("#### Match Telemetry Ledger")
        records = [
            {
                "Round": r.round_number,
                "Player Choice": f"{r.player_move.emoji} {r.player_move.value}",
                "Agent Choice": f"{r.agent_move.emoji} {r.agent_move.value}",
                "Outcome": r.outcome.value,
                "Agent Confidence": f"{r.agent_confidence}%",
                "Deliberation Summary": r.reasoning_summary,
            }
            for r in reversed(st.session_state.history)
        ]
        st.dataframe(pd.DataFrame(records), use_container_width=True)


# =========================================================
# TAB 3: 24/7 LIVE AI CONCIERGE CHATBOT
# =========================================================
with tab_chatbot:
    st.markdown("### 💬 24/7 Live AI Customer Concierge")
    st.caption(
        "Always online. Context-aware. Equipped with real-time match telemetry, algorithm documentation, and developer portfolio info."
    )

    # Quick Prompt Chips
    st.markdown("**Quick Inquiries:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    with qc1:
        if st.button("🧠 How does AI predict?", key="q1", use_container_width=True):
            quick_query = "How does this AI predict my moves and what algorithms are running?"
    with qc2:
        if st.button("📊 My current live stats?", key="q2", use_container_width=True):
            quick_query = "What is my current live score, win rate, and streak?"
    with qc3:
        if st.button("👨‍💻 About Hadi Seelro", key="q3", use_container_width=True):
            quick_query = "Tell me about developer Hadi Seelro and his Agentic AI background."
    with qc4:
        if st.button("💼 Hire Hadi for a project", key="q4", use_container_width=True):
            quick_query = "How can I hire Hadi Seelro for building custom AI agents or web apps?"

    # Chat display container
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle user message input
    user_input = st.chat_input("Ask about the AI algorithms, live scores, or hiring Hadi Seelro...")
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        # Generate Contextual Agent Response
        telemetry = get_telemetry()
        response_text = st.session_state.chatbot.generate_response(prompt_to_send, telemetry)

        # Display assistant response
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
            st.rerun()


# =========================================================
# TAB 4: SPECIFICATIONS & WHITEPAPER
# =========================================================
with tab_specs:
    st.markdown("### 📜 System Architecture & Technical Specifications")
    
    st.markdown(
        r"""
        <div class="glass-card">
            <h4 style="color: #818cf8; margin-top: 0;">1. System Overview</h4>
            <p>
                <strong>ApexRPS</strong> elevates the traditional childhood game into a high-performance demonstration of 
                <strong>Statistical Machine Learning</strong>, <strong>Behavioral Game Theory</strong>, and 
                <strong>Multi-Agent Orchestration</strong>.
            </p>
            <ul>
                <li><strong>Markov Transition Prediction:</strong> 1st and 2nd Order state transition matrices calculate empirical conditional probabilities \( P(Move_t \mid Move_{t-1}, Move_{t-2}) \).</li>
                <li><strong>Win-Stay, Lose-Shift (WSLS) Cognitive Engine:</strong> Encodes human psychological heuristics discovered in behavioral economics (Wang et al., 2014).</li>
                <li><strong>Bayesian Consensus Ensemble:</strong> Dynamically transitions weights between cognitive heuristics in early samples (\(n < 4\)) to high-order Markov chains in mature samples.</li>
                <li><strong>24/7 Context-Injected Concierge Agent:</strong> Autonomous support agent possessing real-time telemetry awareness and full technical knowledge of developer Hadi Seelro.</li>
            </ul>
        </div>

        <div class="glass-card">
            <h4 style="color: #38bdf8; margin-top: 0;">2. Game-Theoretic Foundations</h4>
            <p>
                Under classical Nash Equilibrium, optimal Rock-Paper-Scissors strategy dictates a uniform mixed strategy:
                \[
                \sigma^* = \left(\frac{1}{3}, \frac{1}{3}, \frac{1}{3}\right)
                \]
                However, human players consistently exhibit <strong>bounded rationality</strong>:
            </p>
            <ul>
                <li><strong>Opening Bias:</strong> Humans disproportionately choose Rock (38%+) in inaugural rounds.</li>
                <li><strong>Win-Stay Heuristic:</strong> Victorious players exhibit a statistically significant tendency to repeat the winning gesture.</li>
                <li><strong>Lose-Shift Heuristic:</strong> Defeated players gravitate toward the gesture that would have overcome the opponent's previous winning action.</li>
            </ul>
        </div>

        <div class="glass-card">
            <h4 style="color: #34d399; margin-top: 0;">3. Developer & Engineering Profile</h4>
            <p>
                <strong>Engineered by:</strong> Hadi Seelro<br>
                <strong>Domain:</strong> Agentic AI, Autonomous Workflows, Full-Stack Intelligent Platforms.<br>
                <strong>Production Readiness:</strong> Fault-tolerant offline fallback, modular OOP separation of concerns, reactive Streamlit state management.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
f_col1, f_col2 = st.columns([0.7, 0.3])
with f_col1:
    st.markdown("⚡ **ApexRPS v2.0 - Autonomous Agentic Intelligence Suite**")
    st.caption("Designed & Developed by **Hadi Seelro** | Agentic AI Specialist")
with f_col2:
    st.markdown(
        """
        <div style="text-align: right;">
            <a href="https://github.com/SainBux-HadiSeelro/apex-game" target="_blank" style="text-decoration: none; color: #818cf8; font-weight: 600;">GitHub</a> • 
            <a href="https://linkedin.com" target="_blank" style="text-decoration: none; color: #38bdf8; font-weight: 600;">LinkedIn</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
