import streamlit as st
import random
import re
from fractions import Fraction

def run():
    """
    Main function to run the Find the Probability activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/find_the_probability.py
    """
    # Initialize session state with regular Python types
    if "prob_difficulty" not in st.session_state:
        st.session_state.prob_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > R. Probability and statistics**")
    st.title("🎯 Find the Probability")
    st.markdown("*Calculate probabilities and express them as fractions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.prob_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Events",
            2: "Compound Events", 
            3: "Multi-Step Problems",
            4: "Advanced Scenarios"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Simple')}")
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level}/4")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level == 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Calculate Probability**", expanded=False):
        st.markdown("""
        ### 📐 Probability Formula
        
        **Probability = Number of favorable outcomes / Total number of possible outcomes**
        
        ### ✍️ How to Enter Your Answer
        - Enter fractions using forward slash: **1/2**, **3/4**, **2/3**
        - Simplify your fractions: **2/4** should be **1/2**
        - For impossible events, enter **0**
        - For certain events, enter **1**
        
        ### 📊 Common Examples
        
        **Coin Flip:**
        - P(Heads) = 1/2
        - P(Tails) = 1/2
        
        **Six-Sided Die:**
        - P(Any specific number) = 1/6
        - P(Even number) = 3/6 = 1/2
        - P(Number > 4) = 2/6 = 1/3
        
        **Deck of Cards (52 cards):**
        - P(Red card) = 26/52 = 1/2
        - P(King) = 4/52 = 1/13
        - P(Heart) = 13/52 = 1/4
        
        ### 🎯 Tips
        1. Count all favorable outcomes
        2. Count total possible outcomes
        3. Write as a fraction
        4. Simplify to lowest terms
        """)

def generate_new_problem():
    """Generate a new probability problem"""
    difficulty = st.session_state.prob_difficulty
    
    # Choose problem type based on difficulty
    if difficulty == 1:
        problem_types = [
            "die_single", "coin_single", "spinner_simple", 
            "bag_simple", "cards_simple", "number_simple"
        ]
    elif difficulty == 2:
        problem_types = [
            "die_compound", "coin_multiple", "spinner_compound",
            "bag_compound", "cards_compound", "school_events"
        ]
    elif difficulty == 3:
        problem_types = [
            "die_multiple", "without_replacement", "conditional",
            "geometric", "sports", "weather"
        ]
    else:
        problem_types = [
            "complex_compound", "tree_diagram", "combination",
            "real_world_complex", "game_theory", "multiple_stage"
        ]
    
    problem_type = random.choice(problem_types)
    problem_data = generate_specific_problem(problem_type)
    
    # Store problem data
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_specific_problem(problem_type):
    """Generate specific problem based on type"""
    
    if problem_type == "die_single":
        scenarios = [
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling an even number?",
                "favorable": 3,  # 2, 4, 6
                "total": 6,
                "explanation": "Even numbers on a die: 2, 4, 6 (3 outcomes out of 6 possible)"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a 3?",
                "favorable": 1,
                "total": 6,
                "explanation": "Only one face shows 3 out of 6 possible faces"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a number greater than 4?",
                "favorable": 2,  # 5, 6
                "total": 6,
                "explanation": "Numbers greater than 4: 5 and 6 (2 outcomes out of 6)"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling an odd number?",
                "favorable": 3,  # 1, 3, 5
                "total": 6,
                "explanation": "Odd numbers: 1, 3, 5 (3 outcomes out of 6)"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a prime number?",
                "favorable": 3,  # 2, 3, 5
                "total": 6,
                "explanation": "Prime numbers on a die: 2, 3, 5 (3 outcomes out of 6)"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "coin_single":
        scenarios = [
            {
                "question": "If you flip a coin, what is the probability that it will land on heads?",
                "favorable": 1,
                "total": 2,
                "explanation": "A coin has 2 sides: heads and tails. Heads is 1 out of 2"
            },
            {
                "question": "If you flip a coin, what is the probability that it will land on tails?",
                "favorable": 1,
                "total": 2,
                "explanation": "A coin has 2 sides: heads and tails. Tails is 1 out of 2"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "spinner_simple":
        # Generate random spinner configuration
        total_sections = random.choice([4, 5, 6, 8, 10])
        color = random.choice(["red", "blue", "green", "yellow", "purple"])
        favorable_sections = random.randint(1, total_sections - 1)
        
        question = f"A spinner has {total_sections} equal sections. {favorable_sections} sections are {color}. What is the probability of landing on {color}?"
        
        answer = Fraction(favorable_sections, total_sections)
        
        return {
            "question": question,
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": f"{color} sections: {favorable_sections} out of {total_sections} total sections",
            "problem_type": problem_type
        }
    
    elif problem_type == "bag_simple":
        # Generate random bag configuration
        color1 = random.choice(["red", "blue", "green", "yellow", "white"])
        color2 = random.choice(["black", "purple", "orange", "pink", "brown"])
        
        count1 = random.randint(2, 8)
        count2 = random.randint(2, 8)
        total = count1 + count2
        
        target_color = random.choice([color1, color2])
        favorable = count1 if target_color == color1 else count2
        
        question = f"A bag contains {count1} {color1} marbles and {count2} {color2} marbles. What is the probability of picking a {target_color} marble?"
        
        answer = Fraction(favorable, total)
        
        return {
            "question": question,
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": f"{target_color} marbles: {favorable} out of {total} total marbles",
            "problem_type": problem_type
        }
    
    elif problem_type == "cards_simple":
        scenarios = [
            {
                "question": "What is the probability of drawing a heart from a standard deck of 52 cards?",
                "favorable": 13,
                "total": 52,
                "explanation": "There are 13 hearts in a deck of 52 cards"
            },
            {
                "question": "What is the probability of drawing a King from a standard deck of 52 cards?",
                "favorable": 4,
                "total": 52,
                "explanation": "There are 4 Kings (one of each suit) in 52 cards"
            },
            {
                "question": "What is the probability of drawing a red card from a standard deck of 52 cards?",
                "favorable": 26,
                "total": 52,
                "explanation": "There are 26 red cards (13 hearts + 13 diamonds) in 52 cards"
            },
            {
                "question": "What is the probability of drawing an Ace from a standard deck of 52 cards?",
                "favorable": 4,
                "total": 52,
                "explanation": "There are 4 Aces (one of each suit) in 52 cards"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "number_simple":
        # Random number selection problems
        start = 1
        end = random.choice([10, 12, 15, 20])
        
        scenarios = [
            {
                "desc": "even",
                "check": lambda x: x % 2 == 0
            },
            {
                "desc": "odd",
                "check": lambda x: x % 2 == 1
            },
            {
                "desc": "greater than " + str(end // 2),
                "check": lambda x: x > end // 2
            },
            {
                "desc": "less than " + str((end // 2) + 1),
                "check": lambda x: x < (end // 2) + 1
            }
        ]
        
        scenario = random.choice(scenarios)
        favorable = sum(1 for i in range(start, end + 1) if scenario["check"](i))
        total = end - start + 1
        
        question = f"If you randomly pick a number from 1 to {end}, what is the probability of picking an {scenario['desc']} number?"
        
        answer = Fraction(favorable, total)
        
        return {
            "question": question,
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": f"Numbers that are {scenario['desc']}: {favorable} out of {total} total numbers",
            "problem_type": problem_type
        }
    
    elif problem_type == "die_compound":
        scenarios = [
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a 2 or a 5?",
                "favorable": 2,
                "total": 6,
                "explanation": "Favorable outcomes: 2, 5 (2 out of 6)"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a number less than 3?",
                "favorable": 2,  # 1, 2
                "total": 6,
                "explanation": "Numbers less than 3: 1, 2 (2 out of 6)"
            },
            {
                "question": "If you roll a 6-sided die, what is the probability of rolling a 1, 3, or 5?",
                "favorable": 3,
                "total": 6,
                "explanation": "Favorable outcomes: 1, 3, 5 (3 out of 6)"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "coin_multiple":
        num_flips = random.choice([2, 3])
        
        if num_flips == 2:
            scenarios = [
                {
                    "question": "If you flip 2 coins, what is the probability of getting 2 heads?",
                    "favorable": 1,  # HH
                    "total": 4,  # HH, HT, TH, TT
                    "explanation": "Outcomes: HH, HT, TH, TT. Only HH has 2 heads (1 out of 4)"
                },
                {
                    "question": "If you flip 2 coins, what is the probability of getting at least 1 head?",
                    "favorable": 3,  # HH, HT, TH
                    "total": 4,
                    "explanation": "Outcomes: HH, HT, TH, TT. Three have at least 1 head (3 out of 4)"
                },
                {
                    "question": "If you flip 2 coins, what is the probability of getting exactly 1 tail?",
                    "favorable": 2,  # HT, TH
                    "total": 4,
                    "explanation": "Outcomes: HH, HT, TH, TT. HT and TH have exactly 1 tail (2 out of 4)"
                }
            ]
        else:  # 3 flips
            scenarios = [
                {
                    "question": "If you flip 3 coins, what is the probability of getting all heads?",
                    "favorable": 1,  # HHH
                    "total": 8,
                    "explanation": "There are 2³ = 8 total outcomes. Only HHH has all heads (1 out of 8)"
                },
                {
                    "question": "If you flip 3 coins, what is the probability of getting exactly 2 heads?",
                    "favorable": 3,  # HHT, HTH, THH
                    "total": 8,
                    "explanation": "8 total outcomes. HHT, HTH, THH have exactly 2 heads (3 out of 8)"
                }
            ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "spinner_compound":
        # Spinner with multiple colors
        colors = ["red", "blue", "green", "yellow"]
        num_colors = random.choice([3, 4])
        selected_colors = random.sample(colors, num_colors)
        
        total_sections = random.choice([8, 10, 12])
        
        # Distribute sections among colors
        sections = {}
        remaining = total_sections
        for i, color in enumerate(selected_colors[:-1]):
            s = random.randint(1, remaining - (num_colors - i - 1))
            sections[color] = s
            remaining -= s
        sections[selected_colors[-1]] = remaining
        
        # Create question about two colors
        target_colors = random.sample(selected_colors, 2)
        favorable = sections[target_colors[0]] + sections[target_colors[1]]
        
        sections_desc = ", ".join([f"{v} {k}" for k, v in sections.items()])
        question = f"A spinner has {sections_desc} sections. What is the probability of landing on {target_colors[0]} or {target_colors[1]}?"
        
        answer = Fraction(favorable, total_sections)
        
        return {
            "question": question,
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": f"{target_colors[0]}: {sections[target_colors[0]]}, {target_colors[1]}: {sections[target_colors[1]]}. Total: {favorable} out of {total_sections}",
            "problem_type": problem_type
        }
    
    elif problem_type == "bag_compound":
        # Bag with three colors
        colors = ["red", "blue", "green", "yellow", "white", "black"]
        selected = random.sample(colors, 3)
        
        counts = {}
        total = 0
        for color in selected:
            c = random.randint(2, 6)
            counts[color] = c
            total += c
        
        # Ask about NOT a specific color
        exclude_color = random.choice(selected)
        favorable = total - counts[exclude_color]
        
        counts_desc = ", ".join([f"{v} {k}" for k, v in counts.items()])
        question = f"A bag contains {counts_desc} marbles. What is the probability of NOT picking a {exclude_color} marble?"
        
        answer = Fraction(favorable, total)
        
        return {
            "question": question,
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": f"Not {exclude_color}: {favorable} out of {total} total marbles",
            "problem_type": problem_type
        }
    
    elif problem_type == "cards_compound":
        scenarios = [
            {
                "question": "What is the probability of drawing a face card (Jack, Queen, or King) from a standard deck?",
                "favorable": 12,  # 3 face cards × 4 suits
                "total": 52,
                "explanation": "Face cards: 3 per suit × 4 suits = 12 out of 52 cards"
            },
            {
                "question": "What is the probability of drawing a black King from a standard deck?",
                "favorable": 2,  # King of Spades and King of Clubs
                "total": 52,
                "explanation": "Black Kings: King of Spades and King of Clubs (2 out of 52)"
            },
            {
                "question": "What is the probability of drawing a red face card from a standard deck?",
                "favorable": 6,  # 3 face cards × 2 red suits
                "total": 52,
                "explanation": "Red face cards: 3 per suit × 2 red suits = 6 out of 52"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "school_events":
        scenarios = [
            {
                "question": "In a class of 30 students, 18 play soccer and 12 play basketball. If all students play at least one sport, what is the probability a randomly selected student plays soccer?",
                "favorable": 18,
                "total": 30,
                "explanation": "18 out of 30 students play soccer"
            },
            {
                "question": "A jar contains 15 red pens, 10 blue pens, and 5 black pens. What is the probability of picking a blue pen?",
                "favorable": 10,
                "total": 30,
                "explanation": "10 blue pens out of 30 total pens"
            },
            {
                "question": "In a box of 24 chocolates, 8 are dark chocolate, 10 are milk chocolate, and 6 are white chocolate. What is the probability of picking a dark chocolate?",
                "favorable": 8,
                "total": 24,
                "explanation": "8 dark chocolates out of 24 total"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "die_multiple":
        scenarios = [
            {
                "question": "If you roll two dice, what is the probability of getting a sum of 7?",
                "favorable": 6,  # (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
                "total": 36,
                "explanation": "Ways to get 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). That's 6 out of 36 outcomes"
            },
            {
                "question": "If you roll two dice, what is the probability of getting a sum of 12?",
                "favorable": 1,  # (6,6)
                "total": 36,
                "explanation": "Only way to get 12: (6,6). That's 1 out of 36 outcomes"
            },
            {
                "question": "If you roll two dice, what is the probability of getting the same number on both?",
                "favorable": 6,  # (1,1), (2,2), (3,3), (4,4), (5,5), (6,6)
                "total": 36,
                "explanation": "Doubles: (1,1), (2,2), (3,3), (4,4), (5,5), (6,6). That's 6 out of 36"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "without_replacement":
        # Pick without replacement
        colors = ["red", "blue", "green"]
        color = random.choice(colors)
        
        if color == "red":
            count = 5
            other = 7
        elif color == "blue":
            count = 4
            other = 8
        else:
            count = 6
            other = 6
        
        total = count + other
        
        # Probability of picking 2 of the same color
        if count >= 2:
            favorable = count * (count - 1)
            total_outcomes = total * (total - 1)
            
            question = f"A bag has {count} {color} and {other} other marbles. If you pick 2 marbles without replacement, what is the probability both are {color}?"
            
            answer = Fraction(favorable, total_outcomes)
            
            return {
                "question": question,
                "correct_answer": answer,
                "correct_string": f"{answer.numerator}/{answer.denominator}",
                "explanation": f"First {color}: {count}/{total}. Second {color}: {count-1}/{total-1}. Both: {favorable}/{total_outcomes}",
                "problem_type": problem_type
            }
    
    elif problem_type == "conditional":
        scenarios = [
            {
                "question": "A jar has 20 candies: 12 are fruit-flavored (8 red, 4 green) and 8 are mint. If you pick a fruit candy, what's the probability it's red?",
                "favorable": 8,
                "total": 12,
                "explanation": "Given it's fruit-flavored, there are 8 red out of 12 fruit candies"
            },
            {
                "question": "In a deck of cards, if you draw a face card, what's the probability it's a Queen?",
                "favorable": 4,
                "total": 12,
                "explanation": "12 face cards total (J, Q, K of each suit). 4 are Queens"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "geometric":
        # Geometric probability
        scenarios = [
            {
                "question": "A dartboard has a radius of 10 inches with a bullseye of radius 2 inches. What's the probability of hitting the bullseye?",
                "favorable": 4,  # π × 2² = 4π
                "total": 100,  # π × 10² = 100π
                "explanation": "Bullseye area: π × 2² = 4π. Total area: π × 10² = 100π. Ratio: 4π/100π = 4/100 = 1/25"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "sports":
        scenarios = [
            {
                "question": "A basketball player makes 75% of free throws. Express this probability as a simplified fraction.",
                "favorable": 3,
                "total": 4,
                "explanation": "75% = 75/100 = 3/4"
            },
            {
                "question": "In a tennis match, a player wins 60% of first serves. Express this as a simplified fraction.",
                "favorable": 3,
                "total": 5,
                "explanation": "60% = 60/100 = 3/5"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "weather":
        scenarios = [
            {
                "question": "Weather forecast shows 40% chance of rain. Express this probability as a simplified fraction.",
                "favorable": 2,
                "total": 5,
                "explanation": "40% = 40/100 = 2/5"
            },
            {
                "question": "There's a 25% chance of snow tomorrow. Express this as a simplified fraction.",
                "favorable": 1,
                "total": 4,
                "explanation": "25% = 25/100 = 1/4"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    # Level 4 problems
    elif problem_type == "complex_compound":
        scenarios = [
            {
                "question": "You have a standard deck of 52 cards. What's the probability of drawing a card that is either a heart OR a face card?",
                "favorable": 22,  # 13 hearts + 12 face cards - 3 heart face cards
                "total": 52,
                "explanation": "Hearts: 13, Face cards: 12, Heart face cards: 3. Using inclusion-exclusion: 13 + 12 - 3 = 22"
            },
            {
                "question": "In a bag of 30 marbles (10 red, 12 blue, 8 green), what's the probability of picking either red or green?",
                "favorable": 18,
                "total": 30,
                "explanation": "Red or green: 10 + 8 = 18 out of 30 total marbles"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "tree_diagram":
        scenarios = [
            {
                "question": "You flip a coin then roll a die. What's the probability of getting heads AND rolling a 6?",
                "favorable": 1,
                "total": 12,  # 2 × 6
                "explanation": "P(Heads) = 1/2, P(6) = 1/6. Both: 1/2 × 1/6 = 1/12"
            },
            {
                "question": "You spin two spinners: one with 3 equal sections (red, blue, green), another with 4 equal sections (1, 2, 3, 4). What's the probability of getting blue AND 3?",
                "favorable": 1,
                "total": 12,  # 3 × 4
                "explanation": "P(Blue) = 1/3, P(3) = 1/4. Both: 1/3 × 1/4 = 1/12"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "combination":
        scenarios = [
            {
                "question": "From a group of 5 students (Alice, Bob, Carol, David, Eve), what's the probability that a randomly selected pair includes Alice?",
                "favorable": 4,  # Alice paired with each of the other 4
                "total": 10,  # C(5,2) = 10
                "explanation": "Total pairs: C(5,2) = 10. Pairs with Alice: 4 (Alice with each other person)"
            },
            {
                "question": "You have 4 red balls and 2 blue balls. If you pick 2 balls, what's the probability both are red?",
                "favorable": 6,  # C(4,2) = 6
                "total": 15,  # C(6,2) = 15
                "explanation": "Ways to pick 2 red from 4: C(4,2) = 6. Total ways to pick 2 from 6: C(6,2) = 15"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "real_world_complex":
        scenarios = [
            {
                "question": "In a parking lot with 60 cars: 24 are sedans, 18 are SUVs, 18 are trucks. If 1/3 of sedans are white, what's the probability a randomly selected sedan is white?",
                "favorable": 1,
                "total": 3,
                "explanation": "Given it's a sedan, probability of white is 1/3"
            },
            {
                "question": "A factory produces 100 items daily: 60 pass all tests, 30 have minor defects, 10 have major defects. What's the probability an item passes all tests?",
                "favorable": 3,
                "total": 5,
                "explanation": "60 out of 100 items pass all tests. 60/100 = 3/5"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "game_theory":
        scenarios = [
            {
                "question": "In rock-paper-scissors, what's the probability of winning if both players choose randomly?",
                "favorable": 1,
                "total": 3,
                "explanation": "Each choice wins against 1 option, loses to 1, ties with 1. P(win) = 1/3"
            },
            {
                "question": "You roll a die. You win if you roll 4 or higher. What's the probability of winning?",
                "favorable": 1,
                "total": 2,
                "explanation": "Winning numbers: 4, 5, 6. That's 3 out of 6 = 1/2"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "multiple_stage":
        scenarios = [
            {
                "question": "You draw 2 cards from a deck with replacement. What's the probability both are Aces?",
                "favorable": 1,
                "total": 169,
                "explanation": "P(First Ace) = 4/52 = 1/13, P(Second Ace) = 4/52 = 1/13. Both: 1/13 × 1/13 = 1/169"
            },
            {
                "question": "A game has 3 rounds. You win a round with probability 1/2. What's the probability of winning all 3 rounds?",
                "favorable": 1,
                "total": 8,
                "explanation": "P(Win all 3) = 1/2 × 1/2 × 1/2 = 1/8"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = Fraction(scenario["favorable"], scenario["total"])
        
        return {
            "question": scenario["question"],
            "correct_answer": answer,
            "correct_string": f"{answer.numerator}/{answer.denominator}",
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    # Default fallback
    return generate_specific_problem("die_single")

def parse_fraction_input(user_input):
    """Parse user input to extract fraction"""
    if not user_input:
        return None
    
    # Clean the input
    cleaned = user_input.strip()
    
    # Handle special cases
    if cleaned == "0":
        return Fraction(0)
    if cleaned == "1":
        return Fraction(1)
    
    # Try to parse as fraction (e.g., "1/2", "3/4")
    fraction_pattern = r'^(\d+)\s*/\s*(\d+)$'
    match = re.match(fraction_pattern, cleaned)
    
    if match:
        try:
            numerator = int(match.group(1))
            denominator = int(match.group(2))
            if denominator == 0:
                return None
            return Fraction(numerator, denominator)
        except:
            return None
    
    # Try to parse as decimal
    try:
        # Convert decimal to fraction
        decimal_val = float(cleaned)
        # Use Python's Fraction to convert
        return Fraction(decimal_val).limit_denominator(1000)
    except:
        pass
    
    # Try to parse as percentage (e.g., "50%")
    if cleaned.endswith('%'):
        try:
            percent = float(cleaned[:-1])
            return Fraction(int(percent), 100)
        except:
            pass
    
    return None

def display_problem():
    """Display the current problem with input field"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Question {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Add visual hint based on problem type
    problem_type = data.get("problem_type", "")
    
    if "die" in problem_type:
        st.info("🎲 **Hint:** A standard die has 6 faces numbered 1 through 6")
    elif "coin" in problem_type:
        st.info("🪙 **Hint:** A coin has 2 sides: heads and tails")
    elif "cards" in problem_type:
        st.info("🃏 **Hint:** A standard deck has 52 cards: 4 suits × 13 cards each")
    elif "spinner" in problem_type:
        st.info("🎯 **Hint:** Count the favorable sections and total sections")
    elif "bag" in problem_type or "marble" in problem_type:
        st.info("🎒 **Hint:** Count the favorable marbles and total marbles")
    
    st.markdown("---")
    
    # Input form
    st.markdown("**Write your answer as a fraction or a whole number. With fractions, use a forward slash (/) to separate the numerator and denominator.**")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Your answer:",
            placeholder="Examples: 1/2, 3/4, 0, 1",
            disabled=st.session_state.answer_submitted,
            key="answer_input"
        )
    
    with col2:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                parsed = parse_fraction_input(user_input)
                if parsed is not None:
                    st.session_state.user_answer = parsed
                    check_answer()
                else:
                    st.error("Invalid input. Please enter a fraction (e.g., 1/2) or whole number.")
            else:
                st.warning("Please enter an answer.")
    
    with col3:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation buttons
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 See Solution", type="secondary", use_container_width=True):
                show_detailed_solution()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def check_answer():
    """Check if the user's answer is correct"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Compare fractions
    st.session_state.answer_correct = (user_answer == correct_answer)
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if st.session_state.answer_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The correct answer was **{data['correct_string']}**")
        st.markdown(f"📚 {data['explanation']}")
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {data['correct_string']} is right!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.prob_difficulty
            st.session_state.prob_difficulty = min(
                st.session_state.prob_difficulty + 1, 4
            )
            
            if st.session_state.prob_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Great job! Moving to Level {st.session_state.prob_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        user_str = f"{st.session_state.user_answer.numerator}/{st.session_state.user_answer.denominator}"
        st.error(f"❌ **Not quite. You entered {user_str}, but the correct answer is {data['correct_string']}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.prob_difficulty
            st.session_state.prob_difficulty = max(
                st.session_state.prob_difficulty - 1, 1
            )
            
            if st.session_state.prob_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.prob_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_detailed_solution():
    """Show detailed solution with step-by-step calculation"""
    with st.expander("📚 **Step-by-Step Solution**", expanded=True):
        data = st.session_state.problem_data
        answer = data['correct_answer']
        
        st.markdown("### Solution Process:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        st.markdown("### Calculation:")
        
        # Get the original fraction before simplification
        # We need to extract this from the explanation or problem type
        original_num = answer.numerator
        original_den = answer.denominator
        
        # For some problems, the explanation contains the original values
        import re
        numbers = re.findall(r'\d+', data['explanation'])
        if len(numbers) >= 2:
            try:
                # Try to find the actual counts from the explanation
                for i in range(len(numbers) - 1):
                    test_frac = Fraction(int(numbers[i]), int(numbers[i+1]))
                    if test_frac == answer:
                        original_num = int(numbers[i])
                        original_den = int(numbers[i+1])
                        break
            except:
                pass
        
        # Show the fraction calculation
        st.markdown(f"**Favorable outcomes:** {original_num}")
        st.markdown(f"**Total possible outcomes:** {original_den}")
        
        # Show the exact fraction
        st.markdown(f"**Probability = {original_num}/{original_den}**")
        
        # Show simplified form if different
        if original_num != answer.numerator or original_den != answer.denominator:
            st.markdown(f"**Simplified: {answer.numerator}/{answer.denominator}**")
        
        # Show decimal equivalent
        decimal = float(answer)
        st.markdown(f"**Decimal equivalent:** {decimal:.4f}")
        
        # Show percentage
        percentage = decimal * 100
        st.markdown(f"**Percentage:** {percentage:.1f}%")
        
        # Show probability interpretation
        st.markdown("---")
        st.markdown("### Interpretation:")
        if percentage == 0:
            st.markdown("This event is **impossible** - it will never happen.")
        elif percentage == 100:
            st.markdown("This event is **certain** - it will always happen.")
        elif percentage == 50:
            st.markdown("This event is **equally likely** - 50/50 chance.")
        elif percentage < 50:
            st.markdown(f"This event is **unlikely** - less than 50% chance ({percentage:.1f}%).")
        else:
            st.markdown(f"This event is **likely** - more than 50% chance ({percentage:.1f}%).")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct