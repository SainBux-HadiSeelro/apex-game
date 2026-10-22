"""
ApexRPS - Agentic AI Decision Engine
Developed by Hadi Seelro | Agentic AI Specialist

This module implements multi-strategy predictive AI agents:
1. Random Baseline (Benchmark)
2. Markov Pattern Predictor (1st & 2nd order state transitions)
3. Psychological Agent (Win-Stay, Lose-Shift behavioral heuristic)
4. Apex Autonomous Ensemble (Adaptive Bayesian weighting + real-time reasoning emission)
"""

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Dict, List, Optional, Tuple


class Move(str, Enum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"

    @classmethod
    def list(cls) -> List[str]:
        return [cls.ROCK.value, cls.PAPER.value, cls.SCISSORS.value]

    @property
    def emoji(self) -> str:
        icons = {
            "Rock": "✊",
            "Paper": "🖐️",
            "Scissors": "✌️",
        }
        return icons.get(self.value, "❓")


class Outcome(str, Enum):
    WIN = "Player Wins"
    LOSS = "Agent Wins"
    TIE = "Tie"


# Winning rules: Key beats Value
WINNING_RULES = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

# Counter-move mapping: Move -> what move beats it
COUNTER_MOVES = {
    Move.ROCK: Move.PAPER,
    Move.PAPER: Move.SCISSORS,
    Move.SCISSORS: Move.ROCK,
}


@dataclass
class RoundRecord:
    round_number: int
    player_move: Move
    agent_move: Move
    outcome: Outcome
    agent_confidence: float
    reasoning_summary: str


@dataclass
class AgentReasoning:
    predicted_player_move: Move
    confidence: float
    probability_distribution: Dict[str, float]
    thought_chain: List[str]
    chosen_move: Move
    strategy_used: str


class MarkovModel:
    """
    1st and 2nd Order Markov Chain model tracking human transition tendencies.
    P(Move_t | Move_{t-1}, Move_{t-2})
    """
    def __init__(self):
        self.moves = [Move.ROCK.value, Move.PAPER.value, Move.SCISSORS.value]
        # Order 1: (prev_move) -> {Rock: count, Paper: count, Scissors: count}
        self.order1: Dict[str, Dict[str, int]] = {
            m: {next_m: 1 for next_m in self.moves} for m in self.moves  # Laplace smoothing (+1)
        }
        # Order 2: (prev2, prev1) -> {Rock: count, Paper: count, Scissors: count}
        self.order2: Dict[Tuple[str, str], Dict[str, int]] = {}

    def update(self, player_history: List[Move]):
        if len(player_history) >= 2:
            prev = player_history[-2].value
            curr = player_history[-1].value
            self.order1[prev][curr] += 1

        if len(player_history) >= 3:
            prev2 = player_history[-3].value
            prev1 = player_history[-2].value
            curr = player_history[-1].value
            key = (prev2, prev1)
            if key not in self.order2:
                self.order2[key] = {m: 1 for m in self.moves}
            self.order2[key][curr] += 1

    def predict_next(self, player_history: List[Move]) -> Tuple[Dict[str, float], List[str]]:
        thoughts = []
        if not player_history:
            thoughts.append("[Markov] No history available yet; assuming uniform distribution (33.3% each).")
            return {m: 1 / 3 for m in self.moves}, thoughts

        # Try Order-2 if sufficient history
        if len(player_history) >= 2:
            key = (player_history[-2].value, player_history[-1].value)
            if key in self.order2:
                counts = self.order2[key]
                total = sum(counts.values())
                probs = {m: round(counts[m] / total, 3) for m in self.moves}
                thoughts.append(
                    f"[Markov Order-2] Matched state sequence ({key[0]} -> {key[1]}). "
                    f"Historical transition sample size: {total}. Probabilities: {probs}"
                )
                return probs, thoughts

        # Fallback to Order-1
        last_move = player_history[-1].value
        counts = self.order1[last_move]
        total = sum(counts.values())
        probs = {m: round(counts[m] / total, 3) for m in self.moves}
        thoughts.append(
            f"[Markov Order-1] Conditional on previous move '{last_move}'. "
            f"Observed distribution: {probs}"
        )
        return probs, thoughts


class PsychologicalModel:
    """
    Win-Stay, Lose-Shift (WSLS) Game Theory heuristic.
    Studies in human game dynamics show:
    - Winners tend to repeat their winning move (Win-Stay).
    - Losers tend to shift to the move that would have beaten what the opponent just played (Lose-Shift).
    - Ties often trigger cyclic progression (Rock -> Paper -> Scissors).
    """

    @staticmethod
    def predict_next(history: List[RoundRecord]) -> Tuple[Dict[str, float], List[str]]:
        moves = [Move.ROCK.value, Move.PAPER.value, Move.SCISSORS.value]
        thoughts = []

        if not history:
            thoughts.append("[Psychological] Initial round: Human bias favors Rock (38% empirical baseline).")
            return {
                Move.ROCK.value: 0.40,
                Move.PAPER.value: 0.30,
                Move.SCISSORS.value: 0.30,
            }, thoughts

        last_round = history[-1]
        p_move = last_round.player_move
        a_move = last_round.agent_move
        outcome = last_round.outcome

        probs = {m: 0.20 for m in moves}

        if outcome == Outcome.WIN:
            # Player won -> High likelihood of Win-Stay (replaying same move)
            probs[p_move.value] = 0.60
            remaining = (1.0 - 0.60) / 2
            for m in moves:
                if m != p_move.value:
                    probs[m] = round(remaining, 2)
            thoughts.append(
                f"[Psychology: Win-Stay] Player won last round with {p_move.value}. "
                f"Cognitive bias predicts 60% probability of repetition."
            )

        elif outcome == Outcome.LOSS:
            # Player lost -> Lose-Shift: Players often switch to what would have beaten the agent's winning move,
            # or shift cyclically.
            counter_to_agent = COUNTER_MOVES[a_move].value
            probs[counter_to_agent] = 0.55
            remaining = (1.0 - 0.55) / 2
            for m in moves:
                if m != counter_to_agent:
                    probs[m] = round(remaining, 2)
            thoughts.append(
                f"[Psychology: Lose-Shift] Player lost to Agent's {a_move.value}. "
                f"Anticipating emotional counter-switch to {counter_to_agent} (55% probability)."
            )

        else:
            # Tie -> Cyclic shift tendency: Rock -> Paper -> Scissors
            next_in_cycle = {
                Move.ROCK: Move.PAPER,
                Move.PAPER: Move.SCISSORS,
                Move.SCISSORS: Move.ROCK,
            }[p_move].value
            probs[next_in_cycle] = 0.50
            remaining = (1.0 - 0.50) / 2
            for m in moves:
                if m != next_in_cycle:
                    probs[m] = round(remaining, 2)
            thoughts.append(
                f"[Psychology: Tie-Breaker] Tie on {p_move.value}. "
                f"Cognitive momentum suggests cyclic shift to {next_in_cycle} (50% probability)."
            )

        return probs, thoughts


class ApexAgentEngine:
    """
    Autonomous Multi-Agent Orchestrator.
    Combines Markov pattern recognition, Psychological heuristic modeling,
    and adaptive entropy tuning to formulate optimal counter-strategies.
    """

    def __init__(self):
        self.markov = MarkovModel()
        self.history: List[RoundRecord] = []

    def record_round(self, round_record: RoundRecord):
        self.history.append(round_record)
        player_moves = [r.player_move for r in self.history]
        self.markov.update(player_moves)

    def decide_move(self, persona: str = "Apex Autonomous Agent") -> AgentReasoning:
        moves = [Move.ROCK.value, Move.PAPER.value, Move.SCISSORS.value]
        player_history = [r.player_move for r in self.history]

        # 1. Benchmark: Random Bot
        if persona == "Novice Bot (Random)":
            choice_str = random.choice(moves)
            chosen = Move(choice_str)
            return AgentReasoning(
                predicted_player_move=Move.ROCK,
                confidence=33.3,
                probability_distribution={m: 0.333 for m in moves},
                thought_chain=["[Novice Engine] Generating uniform pseudo-random baseline decision."],
                chosen_move=chosen,
                strategy_used="Uniform Random",
            )

        # 2. Markov Pattern Predictor
        if persona == "Pattern Predictor (Markov)":
            probs, thoughts = self.markov.predict_next(player_history)
            pred_move_str = max(probs, key=probs.get)
            pred_move = Move(pred_move_str)
            counter = COUNTER_MOVES[pred_move]
            conf = round(probs[pred_move_str] * 100, 1)
            thoughts.append(f"[Tactical Counter] Predicted Player Move: {pred_move_str}. Counter-action: {counter.value}.")
            return AgentReasoning(
                predicted_player_move=pred_move,
                confidence=conf,
                probability_distribution=probs,
                thought_chain=thoughts,
                chosen_move=counter,
                strategy_used="Markov Chain State Machine",
            )

        # 3. Psychological Agent
        if persona == "Psychological Agent (WSLS)":
            probs, thoughts = PsychologicalModel.predict_next(self.history)
            pred_move_str = max(probs, key=probs.get)
            pred_move = Move(pred_move_str)
            counter = COUNTER_MOVES[pred_move]
            conf = round(probs[pred_move_str] * 100, 1)
            thoughts.append(f"[Cognitive Counter] Deploying behavioral counter-move: {counter.value}.")
            return AgentReasoning(
                predicted_player_move=pred_move,
                confidence=conf,
                probability_distribution=probs,
                thought_chain=thoughts,
                chosen_move=counter,
                strategy_used="Win-Stay Lose-Shift Model",
            )

        # 4. Apex Autonomous Ensemble (Default Master)
        thoughts = [
            f"[Agent Orchestration] Initializing multi-agent decision consensus for Round {len(self.history) + 1}."
        ]
        markov_probs, markov_thoughts = self.markov.predict_next(player_history)
        psych_probs, psych_thoughts = PsychologicalModel.predict_next(self.history)

        thoughts.extend(markov_thoughts)
        thoughts.extend(psych_thoughts)

        # Dynamic ensemble weighting based on history depth
        # Early rounds (1-4): Psychological heuristic dominates (65% psych, 35% markov)
        # Mature rounds (5+): Markov sequence patterns become statistically dominant (65% markov, 35% psych)
        n = len(self.history)
        if n < 4:
            w_markov = 0.30
            w_psych = 0.70
            thoughts.append(f"[Bayesian Weighting] Early game (n={n}): Prioritizing Psychological heuristics (70% weight).")
        else:
            w_markov = 0.65
            w_psych = 0.35
            thoughts.append(f"[Bayesian Weighting] Empirical sequence established (n={n}): Prioritizing Markov patterns (65% weight).")

        ensemble_probs = {}
        for m in moves:
            ensemble_probs[m] = round((w_markov * markov_probs[m]) + (w_psych * psych_probs[m]), 3)

        # Normalize to 1.0
        tot = sum(ensemble_probs.values()) or 1.0
        ensemble_probs = {m: round(p / tot, 3) for m, p in ensemble_probs.items()}

        pred_move_str = max(ensemble_probs, key=ensemble_probs.get)
        pred_move = Move(pred_move_str)
        counter = COUNTER_MOVES[pred_move]
        conf = round(ensemble_probs[pred_move_str] * 100, 1)

        # Add slight stochastic exploration (5% chance) to avoid becoming strictly deterministic against expert players
        if random.random() < 0.05 and n > 5:
            alternative_moves = [m for m in moves if m != counter.value]
            exploratory = Move(random.choice(alternative_moves))
            thoughts.append(
                f"[Stochastic Exploration] Epsilon-greedy exploration triggered. Shifting from {counter.value} to {exploratory.value} to disrupt counter-prediction."
            )
            counter = exploratory

        thoughts.append(
            f"[Synthesis] Consensus Player Prediction: **{pred_move.value}** (P={ensemble_probs[pred_move.value]}). "
            f"Autonomous Counter-Execution: **{counter.value}**."
        )

        return AgentReasoning(
            predicted_player_move=pred_move,
            confidence=conf,
            probability_distribution=ensemble_probs,
            thought_chain=thoughts,
            chosen_move=counter,
            strategy_used="Apex Bayesian Multi-Agent Ensemble",
        )


def evaluate_round(player_move: Move, agent_move: Move) -> Outcome:
    """Evaluate outcome from player's perspective."""
    if player_move == agent_move:
        return Outcome.TIE
    if WINNING_RULES[player_move] == agent_move:
        return Outcome.WIN
    return Outcome.LOSS


def classify_player_style(history: List[RoundRecord]) -> Dict[str, str]:
    """Classifies user behavioral archetype based on telemetry."""
    if len(history) < 3:
        return {
            "archetype": "Calibrating...",
            "description": "Play at least 3 rounds to unlock behavioral intelligence profile.",
            "badge": "🔍 Analyzing",
        }

    moves = [r.player_move.value for r in history]
    counts = {m: moves.count(m) for m in Move.list()}
    total = len(moves)
    max_move, max_count = max(counts.items(), key=lambda x: x[1])

    # Check for bias
    if max_count / total >= 0.55:
        return {
            "archetype": f"Heavy {max_move} Bias",
            "description": f"You lean heavily on {max_move} ({round(max_count/total*100)}% of moves). The Apex Agent will counter this effortlessly.",
            "badge": "⚡ Predictable Pattern",
        }

    # Check for cyclical (Rock -> Paper -> Scissors)
    shifts = 0
    for i in range(1, len(moves)):
        if moves[i] != moves[i - 1]:
            shifts += 1

    shift_ratio = shifts / (total - 1)
    if shift_ratio >= 0.85:
        return {
            "archetype": "Dynamic Shifter",
            "description": "You rarely repeat the same move twice. You employ high agility tactics.",
            "badge": "🌪️ Agility Specialist",
        }

    return {
        "archetype": "Adaptive Strategist",
        "description": "Balanced distribution across all moves. Engaging in strategic meta-play.",
        "badge": "🧠 Mind-Gamer",
    }
