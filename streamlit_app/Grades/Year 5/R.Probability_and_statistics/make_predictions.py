import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fractions import Fraction
import math

def run():
    """
    Main function to run the Make Predictions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/make_predictions.py
    """
    # Initialize session state
    if "prediction_difficulty" not in st.session_state:
        st.session_state.prediction_difficulty = 1
    
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
    
    # Page header
    st.markdown("**📚 Year 5 > R. Probability and statistics**")
    st.title("🎯 Make Predictions")
    st.markdown("*Use probability to predict outcomes over multiple trials*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.prediction_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Predictions",
            2: "Compound Events",
            3: "Complex Scenarios",
            4: "Advanced Problems"
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
    
    # Instructions
    st.markdown("---")
    with st.expander("📚 **How to Make Predictions**", expanded=False):
        st.markdown("""
        ### 🎲 Expected Value Formula
        
        **Expected number = Probability × Number of trials**
        
        ### 📊 Examples:
        
        **Flipping a coin 10 times:**
        - P(Heads) = 1/2
        - Expected heads = 1/2 × 10 = 5
        
        **Rolling a die 12 times:**
        - P(Getting a 6) = 1/6
        - Expected 6s = 1/6 × 12 = 2
        
        **Bag with 3 red and 2 blue marbles (5 picks with replacement):**
        - P(Red) = 3/5
        - Expected red = 3/5 × 5 = 3
        
        ### 💡 Important Notes:
        - These are **predictions**, not guarantees
        - Actual results may vary due to randomness
        - The prediction is the most likely outcome
        - Round to the nearest whole number when needed
        """)

def generate_new_problem():
    """Generate a new prediction problem"""
    difficulty = st.session_state.prediction_difficulty
    
    if difficulty == 1:
        problem_types = [
            "marble_simple", "spinner_simple", "dice_simple",
            "coin_simple", "cards_simple", "number_wheel"
        ]
    elif difficulty == 2:
        problem_types = [
            "marble_compound", "spinner_compound", "dice_compound",
            "coin_compound", "cards_compound", "dart_board"
        ]
    elif difficulty == 3:
        problem_types = [
            "marble_not", "spinner_complex", "dice_sum",
            "weather_forecast", "sports_prediction", "game_show"
        ]
    else:
        problem_types = [
            "multiple_events", "conditional_prediction", "sampling",
            "quality_control", "election_poll", "medical_test"
        ]
    
    problem_type = random.choice(problem_types)
    problem_data = generate_specific_problem(problem_type)
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_specific_problem(problem_type):
    """Generate specific prediction problem"""
    
    if problem_type == "marble_simple":
        # Generate marble configuration
        colors = ["purple", "green", "orange", "blue", "red", "yellow"]
        color1 = random.choice(colors[:3])
        color2 = random.choice(colors[3:])
        
        count1 = random.randint(2, 5)
        count2 = random.randint(2, 5)
        total = count1 + count2
        
        # Number of trials
        trials = random.choice([4, 5, 6, 7, 8, 9, 10, 11, 12])
        
        # Choose which color to ask about
        target_color = random.choice([color1, color2])
        target_count = count1 if target_color == color1 else count2
        
        # Calculate expected value
        probability = target_count / total
        expected = probability * trials
        answer = round(expected)
        
        question = f"You select a marble without looking and then put it back. If you do this {trials} times, what is the best prediction possible for the number of times you will pick a {target_color} marble?"
        
        return {
            "question": question,
            "visual_type": "marbles",
            "visual_data": {color1: count1, color2: count2},
            "correct_answer": answer,
            "explanation": f"P({target_color}) = {target_count}/{total}. Expected = {target_count}/{total} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "spinner_simple":
        # Generate spinner configuration
        total_sections = random.choice([4, 5, 6, 8, 10])
        colors = ["pink", "blue", "yellow", "green", "red", "purple"]
        
        if random.random() < 0.5:
            # Two colors
            color1 = random.choice(colors[:3])
            color2 = random.choice(colors[3:])
            sections1 = random.randint(1, total_sections - 1)
            sections2 = total_sections - sections1
            config = {color1: sections1, color2: sections2}
            target_color = random.choice([color1, color2])
            target_sections = config[target_color]
        else:
            # Single color
            color = random.choice(colors)
            colored_sections = random.randint(1, total_sections - 1)
            config = {color: colored_sections, "white": total_sections - colored_sections}
            target_color = color
            target_sections = colored_sections
        
        trials = random.choice([5, 6, 7, 8, 9, 10, 12])
        
        probability = target_sections / total_sections
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you spin the spinner {trials} times, what is the best prediction possible for the number of times it will land on {target_color}?"
        
        return {
            "question": question,
            "visual_type": "spinner",
            "visual_data": config,
            "correct_answer": answer,
            "explanation": f"P({target_color}) = {target_sections}/{total_sections}. Expected = {target_sections}/{total_sections} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "dice_simple":
        trials = random.choice([6, 12, 18, 24, 30, 36])
        
        scenarios = [
            {
                "desc": "roll a 6",
                "favorable": 1,
                "total": 6
            },
            {
                "desc": "roll an even number",
                "favorable": 3,
                "total": 6
            },
            {
                "desc": "roll a number greater than 4",
                "favorable": 2,
                "total": 6
            },
            {
                "desc": "roll a prime number (2, 3, or 5)",
                "favorable": 3,
                "total": 6
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you roll a standard die {trials} times, what is the best prediction for the number of times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "dice",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/6. Expected = {scenario['favorable']}/6 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "coin_simple":
        trials = random.choice([10, 20, 30, 40, 50, 100])
        
        target = random.choice(["heads", "tails"])
        probability = 0.5
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you flip a fair coin {trials} times, what is the best prediction for the number of {target}?"
        
        return {
            "question": question,
            "visual_type": "coin",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P({target}) = 1/2. Expected = 1/2 × {trials} = {expected:.0f}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "cards_simple":
        trials = random.choice([13, 26, 52])
        
        scenarios = [
            {
                "desc": "draw a heart",
                "favorable": 13,
                "total": 52
            },
            {
                "desc": "draw a face card",
                "favorable": 12,
                "total": 52
            },
            {
                "desc": "draw an Ace",
                "favorable": 4,
                "total": 52
            },
            {
                "desc": "draw a red card",
                "favorable": 26,
                "total": 52
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you draw a card from a standard deck (with replacement) {trials} times, what is the best prediction for how many times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "cards",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/52. Expected = {scenario['favorable']}/52 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "number_wheel":
        # Number wheel from 1 to N
        max_num = random.choice([8, 10, 12])
        trials = random.choice([8, 10, 12, 15, 20])
        
        scenarios = [
            {
                "desc": f"spin an even number",
                "favorable": max_num // 2,
                "total": max_num
            },
            {
                "desc": f"spin a number less than {max_num // 2 + 1}",
                "favorable": max_num // 2,
                "total": max_num
            },
            {
                "desc": f"spin a multiple of 3",
                "favorable": max_num // 3,
                "total": max_num
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"A wheel has numbers 1 to {max_num}. If you spin it {trials} times, what is the best prediction for how many times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "number_wheel",
            "visual_data": {"max": max_num},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/{max_num}. Expected = {scenario['favorable']}/{max_num} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "marble_compound":
        # Three or more colors
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        num_colors = random.choice([3, 4])
        selected_colors = random.sample(colors, num_colors)
        
        counts = {}
        total = 0
        for color in selected_colors:
            count = random.randint(2, 5)
            counts[color] = count
            total += count
        
        # Ask about two colors combined
        target_colors = random.sample(selected_colors, 2)
        target_count = counts[target_colors[0]] + counts[target_colors[1]]
        
        trials = random.choice([8, 10, 12, 15, 20])
        
        probability = target_count / total
        expected = probability * trials
        answer = round(expected)
        
        question = f"You select a marble without looking and then put it back. If you do this {trials} times, what is the best prediction for the number of times you will pick a {target_colors[0]} or {target_colors[1]} marble?"
        
        return {
            "question": question,
            "visual_type": "marbles",
            "visual_data": counts,
            "correct_answer": answer,
            "explanation": f"P({target_colors[0]} or {target_colors[1]}) = {target_count}/{total}. Expected = {target_count}/{total} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "spinner_compound":
        # Spinner with 3+ colors
        colors = ["red", "blue", "green", "yellow", "purple"]
        num_colors = random.choice([3, 4])
        selected_colors = random.sample(colors, num_colors)
        
        total_sections = random.choice([8, 10, 12])
        sections = {}
        remaining = total_sections
        
        for i, color in enumerate(selected_colors[:-1]):
            s = random.randint(1, remaining - (num_colors - i - 1))
            sections[color] = s
            remaining -= s
        sections[selected_colors[-1]] = remaining
        
        # Ask about multiple colors
        num_target = random.choice([2, 3])
        target_colors = random.sample(selected_colors, num_target)
        target_sections = sum(sections[c] for c in target_colors)
        
        trials = random.choice([10, 12, 15, 18, 20])
        
        probability = target_sections / total_sections
        expected = probability * trials
        answer = round(expected)
        
        colors_text = " or ".join(target_colors)
        question = f"If you spin the spinner {trials} times, what is the best prediction for the number of times it will land on {colors_text}?"
        
        return {
            "question": question,
            "visual_type": "spinner",
            "visual_data": sections,
            "correct_answer": answer,
            "explanation": f"P({colors_text}) = {target_sections}/{total_sections}. Expected = {target_sections}/{total_sections} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "dice_compound":
        trials = random.choice([12, 18, 24, 30, 36])
        
        scenarios = [
            {
                "desc": "roll a 2 or a 5",
                "favorable": 2,
                "total": 6
            },
            {
                "desc": "roll a 1, 3, or 5 (odd numbers)",
                "favorable": 3,
                "total": 6
            },
            {
                "desc": "roll a number less than 4",
                "favorable": 3,
                "total": 6
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you roll a die {trials} times, what is the best prediction for how many times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "dice",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/6. Expected = {scenario['favorable']}/6 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "coin_compound":
        # Multiple coins or multiple outcomes
        num_coins = random.choice([2, 3])
        trials = random.choice([8, 16, 24, 32])
        
        if num_coins == 2:
            scenarios = [
                {
                    "desc": "get two heads",
                    "favorable": 1,
                    "total": 4
                },
                {
                    "desc": "get at least one head",
                    "favorable": 3,
                    "total": 4
                },
                {
                    "desc": "get exactly one tail",
                    "favorable": 2,
                    "total": 4
                }
            ]
        else:  # 3 coins
            scenarios = [
                {
                    "desc": "get all heads",
                    "favorable": 1,
                    "total": 8
                },
                {
                    "desc": "get exactly two heads",
                    "favorable": 3,
                    "total": 8
                },
                {
                    "desc": "get at least one tail",
                    "favorable": 7,
                    "total": 8
                }
            ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you flip {num_coins} coins together {trials} times, what is the best prediction for how many times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "coin",
            "visual_data": {"num_coins": num_coins},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/{scenario['total']}. Expected = {scenario['favorable']}/{scenario['total']} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "cards_compound":
        trials = random.choice([26, 52])
        
        scenarios = [
            {
                "desc": "draw a red face card",
                "favorable": 6,
                "total": 52
            },
            {
                "desc": "draw a black Ace or King",
                "favorable": 4,
                "total": 52
            },
            {
                "desc": "draw a card that is not a heart",
                "favorable": 39,
                "total": 52
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"Drawing cards with replacement {trials} times, what is the best prediction for how many times you will {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "cards",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/52. Expected = {scenario['favorable']}/52 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "dart_board":
        # Dartboard with colored regions
        regions = {
            "red": random.randint(20, 40),
            "blue": random.randint(15, 30),
            "yellow": random.randint(10, 25),
            "green": random.randint(10, 20)
        }
        
        # Normalize to 100
        total = sum(regions.values())
        for color in regions:
            regions[color] = round(regions[color] * 100 / total)
        
        # Adjust to exactly 100
        diff = 100 - sum(regions.values())
        regions["red"] += diff
        
        target_color = random.choice(list(regions.keys()))
        trials = random.choice([20, 25, 30, 40, 50])
        
        probability = regions[target_color] / 100
        expected = probability * trials
        answer = round(expected)
        
        question = f"A dartboard has regions: {', '.join([f'{v}% {k}' for k, v in regions.items()])}. If you throw {trials} darts randomly, what is the best prediction for how many will hit {target_color}?"
        
        return {
            "question": question,
            "visual_type": "dartboard",
            "visual_data": regions,
            "correct_answer": answer,
            "explanation": f"P({target_color}) = {regions[target_color]}/100. Expected = {regions[target_color]}/100 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "marble_not":
        # NOT a certain color
        colors = ["purple", "orange", "blue", "green"]
        num_colors = random.choice([2, 3])
        selected_colors = random.sample(colors, num_colors)
        
        counts = {}
        total = 0
        for color in selected_colors:
            count = random.randint(2, 6)
            counts[color] = count
            total += count
        
        exclude_color = random.choice(selected_colors)
        favorable = total - counts[exclude_color]
        
        trials = random.choice([10, 12, 15, 18, 20])
        
        probability = favorable / total
        expected = probability * trials
        answer = round(expected)
        
        question = f"You select a marble without looking and then put it back. If you do this {trials} times, what is the best prediction for the number of times you will pick a marble that is not {exclude_color}?"
        
        return {
            "question": question,
            "visual_type": "marbles",
            "visual_data": counts,
            "correct_answer": answer,
            "explanation": f"P(not {exclude_color}) = {favorable}/{total}. Expected = {favorable}/{total} × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "spinner_complex":
        # Complex spinner conditions
        total_sections = 12
        sections = {
            "red": random.randint(2, 4),
            "blue": random.randint(2, 4),
            "yellow": random.randint(2, 4),
            "green": random.randint(2, 4)
        }
        
        # Adjust to total 12
        current_total = sum(sections.values())
        diff = total_sections - current_total
        sections["red"] += diff
        
        # Create complex condition
        conditions = [
            ("primary color (red, blue, or yellow)", ["red", "blue", "yellow"]),
            ("warm color (red or yellow)", ["red", "yellow"]),
            ("cool color (blue or green)", ["blue", "green"])
        ]
        
        condition_text, target_colors = random.choice(conditions)
        target_sections = sum(sections[c] for c in target_colors if c in sections)
        
        trials = random.choice([24, 36, 48, 60])
        
        probability = target_sections / total_sections
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you spin the spinner {trials} times, what is the best prediction for how many times it will land on a {condition_text}?"
        
        return {
            "question": question,
            "visual_type": "spinner",
            "visual_data": sections,
            "correct_answer": answer,
            "explanation": f"P({condition_text}) = {target_sections}/12. Expected = {target_sections}/12 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "dice_sum":
        # Two dice sum predictions
        trials = random.choice([36, 72, 108])
        
        scenarios = [
            {
                "desc": "sum of 7",
                "favorable": 6,
                "total": 36
            },
            {
                "desc": "sum of 12",
                "favorable": 1,
                "total": 36
            },
            {
                "desc": "sum less than 5",
                "favorable": 6,  # (1,1), (1,2), (2,1), (1,3), (3,1), (2,2)
                "total": 36
            },
            {
                "desc": "doubles",
                "favorable": 6,
                "total": 36
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * trials
        answer = round(expected)
        
        question = f"If you roll two dice {trials} times, what is the best prediction for how many times you will get {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "dice",
            "visual_data": {"num_dice": 2},
            "correct_answer": answer,
            "explanation": f"P({scenario['desc']}) = {scenario['favorable']}/36. Expected = {scenario['favorable']}/36 × {trials} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": trials
        }
    
    elif problem_type == "weather_forecast":
        # Weather predictions
        rain_chance = random.choice([20, 30, 40, 60, 70])
        days = random.choice([10, 20, 30])
        
        probability = rain_chance / 100
        expected = probability * days
        answer = round(expected)
        
        question = f"If there's a {rain_chance}% chance of rain each day, what is the best prediction for the number of rainy days in the next {days} days?"
        
        return {
            "question": question,
            "visual_type": "weather",
            "visual_data": {"rain_chance": rain_chance},
            "correct_answer": answer,
            "explanation": f"P(rain) = {rain_chance}/100. Expected = {rain_chance}/100 × {days} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": days
        }
    
    elif problem_type == "sports_prediction":
        # Sports scenarios
        scenarios = [
            {
                "sport": "basketball",
                "desc": "free throws",
                "success_rate": 75,
                "attempts": random.choice([20, 40, 60])
            },
            {
                "sport": "soccer",
                "desc": "penalty kicks",
                "success_rate": 80,
                "attempts": random.choice([10, 15, 20])
            },
            {
                "sport": "baseball",
                "desc": "hits",
                "success_rate": 30,
                "attempts": random.choice([30, 40, 50])
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["success_rate"] / 100
        expected = probability * scenario["attempts"]
        answer = round(expected)
        
        question = f"A {scenario['sport']} player has a {scenario['success_rate']}% success rate for {scenario['desc']}. In {scenario['attempts']} attempts, what is the best prediction for successful {scenario['desc']}?"
        
        return {
            "question": question,
            "visual_type": "sports",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"P(success) = {scenario['success_rate']}/100. Expected = {scenario['success_rate']}/100 × {scenario['attempts']} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": scenario["attempts"]
        }
    
    elif problem_type == "game_show":
        # Game show scenarios
        doors = random.choice([3, 4, 5])
        winning_doors = random.choice([1, 2])
        plays = random.choice([15, 20, 30])
        
        probability = winning_doors / doors
        expected = probability * plays
        answer = round(expected)
        
        question = f"In a game show with {doors} doors where {winning_doors} hide prizes, if you play {plays} times, what is the best prediction for how many times you'll win?"
        
        return {
            "question": question,
            "visual_type": "doors",
            "visual_data": {"total": doors, "winning": winning_doors},
            "correct_answer": answer,
            "explanation": f"P(win) = {winning_doors}/{doors}. Expected = {winning_doors}/{doors} × {plays} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": plays
        }
    
    # Level 4 problems
    elif problem_type == "multiple_events":
        # Complex multi-stage events
        scenarios = [
            {
                "desc": "A bag has 5 red and 3 blue marbles. You pick one, note the color, return it, then pick again.",
                "question_end": "both picks are the same color",
                "favorable": 34,  # RR: 25, BB: 9
                "total": 64,
                "trials": random.choice([32, 64, 96])
            },
            {
                "desc": "You flip a coin and roll a die.",
                "question_end": "you get heads AND an even number",
                "favorable": 1,
                "total": 4,
                "trials": random.choice([24, 36, 48])
            }
        ]
        
        scenario = random.choice(scenarios)
        probability = scenario["favorable"] / scenario["total"]
        expected = probability * scenario["trials"]
        answer = round(expected)
        
        question = f"{scenario['desc']} If you do this {scenario['trials']} times, predict how many times {scenario['question_end']}."
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P(event) = {scenario['favorable']}/{scenario['total']}. Expected = {probability:.3f} × {scenario['trials']} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": scenario["trials"]
        }
    
    elif problem_type == "conditional_prediction":
        # Conditional probability predictions
        scenarios = [
            {
                "setup": "In a class, 60% of students play sports. Of those who play sports, 75% also play music.",
                "question": "how many play both sports and music",
                "probability": 0.45,  # 0.60 × 0.75
                "trials": random.choice([40, 60, 80])
            },
            {
                "setup": "A factory has 80% good items. Of the good items, 90% pass the final test.",
                "question": "how many items are good AND pass the test",
                "probability": 0.72,  # 0.80 × 0.90
                "trials": random.choice([50, 100, 150])
            }
        ]
        
        scenario = random.choice(scenarios)
        expected = scenario["probability"] * scenario["trials"]
        answer = round(expected)
        
        question = f"{scenario['setup']} Out of {scenario['trials']} students/items, predict {scenario['question']}."
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P(both) = {scenario['probability']:.2f}. Expected = {scenario['probability']:.2f} × {scenario['trials']} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": scenario["trials"]
        }
    
    elif problem_type == "sampling":
        # Sampling and surveys
        scenarios = [
            {
                "context": "A survey shows 35% of people prefer chocolate ice cream.",
                "question": "In a sample of",
                "probability": 0.35,
                "trials": random.choice([100, 200, 500])
            },
            {
                "context": "Studies show 28% of teenagers have a part-time job.",
                "question": "In a group of",
                "probability": 0.28,
                "trials": random.choice([50, 100, 150])
            }
        ]
        
        scenario = random.choice(scenarios)
        expected = scenario["probability"] * scenario["trials"]
        answer = round(expected)
        
        question = f"{scenario['context']} {scenario['question']} {scenario['trials']} people, how many would you predict prefer this/have this?"
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {},
            "correct_answer": answer,
            "explanation": f"P = {scenario['probability']:.2f}. Expected = {scenario['probability']:.2f} × {scenario['trials']} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": scenario["trials"]
        }
    
    elif problem_type == "quality_control":
        # Manufacturing/quality scenarios
        defect_rate = random.choice([2, 3, 5, 8, 10])
        items = random.choice([100, 200, 500, 1000])
        
        probability = defect_rate / 100
        expected = probability * items
        answer = round(expected)
        
        question = f"A factory has a {defect_rate}% defect rate. In a batch of {items} items, how many defects would you predict?"
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {"defect_rate": defect_rate},
            "correct_answer": answer,
            "explanation": f"P(defect) = {defect_rate}/100. Expected = {defect_rate}/100 × {items} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": items
        }
    
    elif problem_type == "election_poll":
        # Voting/polling predictions
        support_rate = random.choice([45, 52, 58, 65])
        voters = random.choice([500, 1000, 2000])
        
        probability = support_rate / 100
        expected = probability * voters
        answer = round(expected)
        
        question = f"A poll shows {support_rate}% support for a proposal. In a group of {voters} voters, how many would you predict to support it?"
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {"support": support_rate},
            "correct_answer": answer,
            "explanation": f"P(support) = {support_rate}/100. Expected = {support_rate}/100 × {voters} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": voters
        }
    
    elif problem_type == "medical_test":
        # Medical/testing scenarios
        positive_rate = random.choice([5, 10, 15, 20])
        tests = random.choice([100, 200, 500])
        
        probability = positive_rate / 100
        expected = probability * tests
        answer = round(expected)
        
        question = f"A medical test has a {positive_rate}% positive rate in the population. Out of {tests} tests, how many positives would you predict?"
        
        return {
            "question": question,
            "visual_type": "text",
            "visual_data": {"positive_rate": positive_rate},
            "correct_answer": answer,
            "explanation": f"P(positive) = {positive_rate}/100. Expected = {positive_rate}/100 × {tests} = {expected:.1f} ≈ {answer}",
            "problem_type": problem_type,
            "trials": tests
        }
    
    # Default fallback
    return generate_specific_problem("marble_simple")

def display_problem():
    """Display the current problem with visualization"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Question {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Display visualization
    visual_type = data.get("visual_type", "text")
    
    if visual_type == "marbles":
        display_marbles(data["visual_data"])
    elif visual_type == "spinner":
        display_spinner(data["visual_data"])
    elif visual_type == "dice":
        display_dice_visual(data.get("visual_data", {}))
    elif visual_type == "coin":
        display_coin_visual(data.get("visual_data", {}))
    elif visual_type == "cards":
        display_cards_visual()
    elif visual_type == "number_wheel":
        display_number_wheel(data["visual_data"])
    elif visual_type == "dartboard":
        display_dartboard(data["visual_data"])
    elif visual_type == "weather":
        display_weather(data["visual_data"])
    elif visual_type == "sports":
        display_sports(data["visual_data"])
    elif visual_type == "doors":
        display_doors(data["visual_data"])
    elif visual_type == "text":
        # No visual needed, just context
        pass
    
    st.markdown("---")
    
    # Input form
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Your prediction:",
            placeholder="Enter number of times",
            disabled=st.session_state.answer_submitted,
            key="prediction_input",
            label_visibility="visible"
        )
        st.caption("times")
    
    with col2:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                try:
                    user_answer = int(user_input)
                    if user_answer >= 0:
                        st.session_state.user_answer = user_answer
                        check_answer()
                    else:
                        st.error("Please enter a non-negative number.")
                except ValueError:
                    st.error("Please enter a whole number.")
            else:
                st.warning("Please enter your prediction.")
    
    with col3:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 See Calculation", type="secondary", use_container_width=True):
                show_detailed_calculation()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_marbles(config):
    """Display marble visualization"""
    colors_map = {
        "red": "#FF6B6B",
        "blue": "#4DABF7",
        "green": "#51CF66",
        "yellow": "#FFD43B",
        "purple": "#9775FA",
        "orange": "#FF922B",
        "white": "#F8F9FA",
        "pink": "#FFB6C1",
        "brown": "#8B4513",
        "black": "#212529"
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Calculate positions
    total_marbles = sum(config.values())
    cols = min(10, total_marbles)
    rows = (total_marbles + cols - 1) // cols
    
    # Draw marbles
    marble_index = 0
    for color, count in config.items():
        for _ in range(count):
            row = marble_index // cols
            col = marble_index % cols
            
            circle = plt.Circle(
                (col * 1.2 + 0.6, rows - row - 0.5),
                0.4,
                color=colors_map.get(color, "#CCCCCC"),
                ec='black',
                linewidth=2
            )
            ax.add_patch(circle)
            marble_index += 1
    
    # Set limits and aspect
    ax.set_xlim(0, cols * 1.2)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title with counts
    title_parts = [f"{count} {color}" for color, count in config.items()]
    title = " | ".join(title_parts)
    plt.title(f"Marbles: {title}", fontsize=12, fontweight='bold')
    
    st.pyplot(fig)
    plt.close()

def display_spinner(config):
    """Display spinner visualization"""
    colors_map = {
        "red": "#FF6B6B",
        "blue": "#4DABF7",
        "green": "#51CF66",
        "yellow": "#FFD43B",
        "purple": "#9775FA",
        "orange": "#FF922B",
        "white": "#F8F9FA",
        "pink": "#FFB6C1",
        "brown": "#8B4513"
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Calculate angles
    total = sum(config.values())
    sizes = list(config.values())
    colors = [colors_map.get(c, "#CCCCCC") for c in config.keys()]
    labels = [f"{c}\n({v} sections)" for c, v in config.items()]
    
    # Draw pie chart as spinner
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='',
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 2}
    )
    
    # Add center circle to make it look like a spinner
    centre_circle = plt.Circle((0, 0), 0.1, fc='black')
    ax.add_artist(centre_circle)
    
    # Add arrow
    ax.arrow(0, 0, 0.3, 0.3, head_width=0.15, head_length=0.1, fc='red', ec='red', linewidth=2)
    
    ax.set_aspect('equal')
    plt.title(f"Spinner with {total} equal sections", fontsize=12, fontweight='bold')
    
    st.pyplot(fig)
    plt.close()

def display_dice_visual(data):
    """Display dice visualization"""
    num_dice = data.get("num_dice", 1)
    
    if num_dice == 1:
        st.info("🎲 **Standard 6-sided die** (faces: 1, 2, 3, 4, 5, 6)")
    else:
        st.info(f"🎲🎲 **{num_dice} standard dice** (36 possible outcomes)")

def display_coin_visual(data):
    """Display coin visualization"""
    num_coins = data.get("num_coins", 1)
    
    if num_coins == 1:
        st.info("🪙 **Fair coin** (Heads or Tails)")
    else:
        st.info(f"🪙 × {num_coins} **{num_coins} fair coins** ({2**num_coins} possible outcomes)")

def display_cards_visual():
    """Display cards info"""
    st.info("🃏 **Standard 52-card deck** (4 suits × 13 ranks, with replacement)")

def display_number_wheel(data):
    """Display number wheel"""
    max_num = data["max"]
    st.info(f"🎯 **Number wheel** with numbers 1 to {max_num}")

def display_dartboard(data):
    """Display dartboard with regions"""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    colors_map = {
        "red": "#FF6B6B",
        "blue": "#4DABF7",
        "yellow": "#FFD43B",
        "green": "#51CF66"
    }
    
    sizes = list(data.values())
    colors = [colors_map.get(c, "#CCCCCC") for c in data.keys()]
    labels = [f"{c}\n{v}%" for c, v in data.items()]
    
    ax.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
    ax.set_aspect('equal')
    plt.title("Dartboard Regions", fontsize=12, fontweight='bold')
    
    st.pyplot(fig)
    plt.close()

def display_weather(data):
    """Display weather prediction"""
    rain_chance = data["rain_chance"]
    st.info(f"☔ **Weather Forecast:** {rain_chance}% chance of rain each day")

def display_sports(data):
    """Display sports scenario"""
    icons = {
        "basketball": "🏀",
        "soccer": "⚽",
        "baseball": "⚾"
    }
    icon = icons.get(data["sport"], "🏃")
    st.info(f"{icon} **{data['sport'].title()} Player:** {data['success_rate']}% success rate for {data['desc']}")

def display_doors(data):
    """Display game show doors"""
    st.info(f"🚪 **Game Show:** {data['total']} doors, {data['winning']} with prizes")

def check_answer():
    """Check the user's prediction"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Allow for reasonable rounding differences
    st.session_state.answer_correct = (user_answer == correct_answer)
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if st.session_state.answer_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback"""
    data = st.session_state.problem_data
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The best prediction was **{data['correct_answer']} times**")
        st.markdown(f"📚 {data['explanation']}")
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {data['correct_answer']} times is the best prediction!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.prediction_difficulty
            st.session_state.prediction_difficulty = min(
                st.session_state.prediction_difficulty + 1, 4
            )
            
            if st.session_state.prediction_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.prediction_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. You predicted {st.session_state.user_answer}, but the best prediction is {data['correct_answer']} times.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.prediction_difficulty
            st.session_state.prediction_difficulty = max(
                st.session_state.prediction_difficulty - 1, 1
            )
            
            if st.session_state.prediction_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.prediction_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_detailed_calculation():
    """Show detailed calculation steps"""
    with st.expander("📚 **Step-by-Step Calculation**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### How to Calculate the Prediction:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        st.markdown("### The Formula:")
        st.markdown("**Expected Value = Probability × Number of Trials**")
        
        st.markdown("### Why This Works:")
        st.markdown("""
        The expected value tells us the **average** number of times we'd expect 
        the event to occur if we repeated the experiment many times. While the 
        actual result in any single experiment might be different, this gives 
        us the best prediction based on probability.
        """)
        
        # Show percentage interpretation
        trials = data.get("trials", 1)
        answer = data["correct_answer"]
        percentage = (answer / trials) * 100 if trials > 0 else 0
        
        st.markdown("---")
        st.markdown(f"### Interpretation:")
        st.markdown(f"Out of {trials} trials, we expect about **{percentage:.1f}%** to be successful.")

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