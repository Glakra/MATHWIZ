import streamlit as st
import random
import math
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np

def run():
    """
    Main function to run the Understanding Probability activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/understanding_probability.py
    """
    # Initialize session state with regular Python types
    if "probability_difficulty" not in st.session_state:
        st.session_state.probability_difficulty = 1
    
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
    st.title("🎲 Understanding Probability")
    st.markdown("*Learn about chance, likelihood, and probability*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.probability_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Likelihood",
            2: "Comparing Chances",
            3: "Fractions & Numbers",
            4: "Complex Scenarios"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
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
    with st.expander("📚 **Probability Concepts**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Likelihood Terms
            
            **Certain (100% chance)**
            - Will definitely happen
            - Example: The sun will rise tomorrow
            
            **Likely (More than 50%)**
            - Probably will happen
            - Example: Rolling 2-6 on a die
            
            **Equally Likely (50%)**
            - Same chance either way
            - Example: Flipping heads on a coin
            
            **Unlikely (Less than 50%)**
            - Probably won't happen
            - Example: Rolling a 1 on a die
            
            **Impossible (0% chance)**
            - Cannot happen
            - Example: Rolling a 7 on a standard die
            """)
        
        with col2:
            st.markdown("""
            ### 📊 How to Compare Chances
            
            **1. Count the favorable outcomes**
            - How many ways can it happen?
            
            **2. Count total possible outcomes**
            - How many total possibilities?
            
            **3. Compare the amounts**
            - More favorable = more likely
            - Equal amounts = equally likely
            - Fewer favorable = less likely
            
            ### 🔢 Probability as Numbers
            - **0** = Impossible
            - **1/2 or 0.5** = Equally likely
            - **1** = Certain
            
            **Example:** A spinner with 3 red and 1 blue
            - P(red) = 3/4 = more likely
            - P(blue) = 1/4 = less likely
            """)

def generate_new_problem():
    """Generate a new probability problem"""
    difficulty = st.session_state.probability_difficulty
    
    # Choose problem type based on difficulty
    if difficulty == 1:
        problem_types = ["spinner_basic", "dice_basic", "bag_basic", "certain_impossible"]
    elif difficulty == 2:
        problem_types = ["spinner_compare", "dice_compare", "bag_compare", "cards_basic"]
    elif difficulty == 3:
        problem_types = ["spinner_fraction", "dice_fraction", "bag_fraction", "multiple_events"]
    else:
        problem_types = ["complex_spinner", "complex_dice", "complex_bag", "real_world"]
    
    problem_type = random.choice(problem_types)
    problem_data = generate_specific_problem(problem_type)
    
    # Store problem data
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_specific_problem(problem_type):
    """Generate specific problem based on type"""
    
    if problem_type == "spinner_basic":
        return generate_spinner_basic()
    elif problem_type == "spinner_compare":
        return generate_spinner_compare()
    elif problem_type == "spinner_fraction":
        return generate_spinner_fraction()
    elif problem_type == "complex_spinner":
        return generate_complex_spinner()
    elif problem_type == "dice_basic":
        return generate_dice_basic()
    elif problem_type == "dice_compare":
        return generate_dice_compare()
    elif problem_type == "dice_fraction":
        return generate_dice_fraction()
    elif problem_type == "complex_dice":
        return generate_complex_dice()
    elif problem_type == "bag_basic":
        return generate_bag_basic()
    elif problem_type == "bag_compare":
        return generate_bag_compare()
    elif problem_type == "bag_fraction":
        return generate_bag_fraction()
    elif problem_type == "complex_bag":
        return generate_complex_bag()
    elif problem_type == "cards_basic":
        return generate_cards_basic()
    elif problem_type == "certain_impossible":
        return generate_certain_impossible()
    elif problem_type == "multiple_events":
        return generate_multiple_events()
    else:  # real_world
        return generate_real_world()

def generate_spinner_basic():
    """Generate basic spinner problem"""
    # Define configs with clear differences for basic level
    configs = [
        {"green": 3, "white": 1},   # 3/4 green, 1/4 white
        {"blue": 1, "white": 3},     # 1/4 blue, 3/4 white  
        {"red": 2, "white": 1},      # 2/3 red, 1/3 white
        {"yellow": 5, "white": 3},   # 5/8 yellow, 3/8 white
        {"purple": 1, "white": 4},   # 1/5 purple, 4/5 white
        {"orange": 3, "white": 2},   # 3/5 orange, 2/5 white
        {"pink": 4, "white": 1},     # 4/5 pink, 1/5 white
        {"brown": 1, "white": 2},    # 1/3 brown, 2/3 white
    ]
    
    config = random.choice(configs)
    colors = list(config.keys())
    color1, color2 = colors[0], colors[1]
    
    # Make sure we never have equal sections at basic level
    if config[color1] == config[color2]:
        # Adjust to ensure inequality
        config[color1] = config[color1] + 1
    
    questions = [
        f"On which colour is the spinner more likely to land?",
        f"On which colour is the spinner less likely to land?",
    ]
    
    question = random.choice(questions)
    
    if "more" in question:
        correct = color1 if config[color1] > config[color2] else color2
    else:
        correct = color1 if config[color1] < config[color2] else color2
    
    # Get the actual counts from the config that will be displayed
    actual_count1 = config[color1]
    actual_count2 = config[color2]
    total_sections = actual_count1 + actual_count2
    
    return {
        "question": question,
        "visual_type": "spinner",
        "visual_data": config,
        "options": [color1, color2],
        "correct_answer": correct,
        "explanation": f"The spinner has {actual_count1} {color1} section{'s' if actual_count1 != 1 else ''} and {actual_count2} {color2} section{'s' if actual_count2 != 1 else ''} (total: {total_sections} sections). So it's {'more' if 'more' in question else 'less'} likely to land on {correct}.",
        "problem_type": "spinner"
    }

def generate_spinner_compare():
    """Generate spinner comparison problem"""
    # Ensure spinners have different probabilities
    while True:
        spinner1 = {"red": random.randint(1, 4), "blue": random.randint(1, 4)}
        spinner2 = {"red": random.randint(1, 4), "blue": random.randint(1, 4)}
        
        prob1 = spinner1["red"] / sum(spinner1.values())
        prob2 = spinner2["red"] / sum(spinner2.values())
        
        # Make sure they're actually different
        if prob1 != prob2:
            break
    
    question = "Which spinner gives you a better chance of landing on red?"
    
    if prob1 > prob2:
        correct = "Spinner A"
    elif prob2 > prob1:
        correct = "Spinner B"
    else:
        correct = "Same chance"
    
    # Provide detailed explanation with actual values
    total1 = sum(spinner1.values())
    total2 = sum(spinner2.values())
    
    return {
        "question": question,
        "visual_type": "double_spinner",
        "visual_data": {"spinner1": spinner1, "spinner2": spinner2},
        "options": ["Spinner A", "Spinner B", "Same chance"],
        "correct_answer": correct,
        "explanation": f"Spinner A: {spinner1['red']} red out of {total1} total sections ({spinner1['red']}/{total1}). Spinner B: {spinner2['red']} red out of {total2} total sections ({spinner2['red']}/{total2}).",
        "problem_type": "spinner_compare"
    }

def generate_spinner_fraction():
    """Generate spinner with fraction answer using Python's Fraction"""
    total_sections = random.choice([4, 6, 8, 10])
    color_sections = random.randint(1, total_sections - 1)
    
    config = {
        "blue": color_sections,
        "white": total_sections - color_sections
    }
    
    question = "What is the probability of landing on blue?"
    
    # Use Python's Fraction for simplification
    frac = Fraction(color_sections, total_sections)
    correct = f"{frac.numerator}/{frac.denominator}"
    
    # Generate distractors
    options = [correct]
    
    # Unsimplified version if different
    if color_sections != frac.numerator:
        options.append(f"{color_sections}/{total_sections}")
    
    # Inverted fraction
    if frac.numerator != frac.denominator:
        options.append(f"{frac.denominator}/{frac.numerator}")
    
    # Wrong denominator
    options.append(f"{frac.numerator}/{frac.denominator + 1}")
    
    # Add more options if needed
    while len(options) < 4:
        wrong_num = random.randint(1, total_sections)
        wrong_den = random.randint(2, total_sections + 2)
        wrong_frac = Fraction(wrong_num, wrong_den)
        wrong_str = f"{wrong_frac.numerator}/{wrong_frac.denominator}"
        if wrong_str not in options:
            options.append(wrong_str)
    
    options = options[:4]
    random.shuffle(options)
    
    return {
        "question": question,
        "visual_type": "spinner",
        "visual_data": config,
        "options": options,
        "correct_answer": correct,
        "explanation": f"The spinner has {color_sections} blue section{'s' if color_sections != 1 else ''} out of {total_sections} total sections. So P(blue) = {color_sections}/{total_sections} = {correct}",
        "problem_type": "spinner_fraction"
    }

def generate_complex_spinner():
    """Generate complex spinner problem"""
    colors = ["red", "blue", "green", "yellow", "purple"]
    num_colors = random.randint(3, 4)
    selected_colors = random.sample(colors, num_colors)
    
    config = {}
    total = random.choice([8, 10, 12])
    remaining = total
    
    for i, color in enumerate(selected_colors[:-1]):
        sections = random.randint(1, remaining - (len(selected_colors) - i - 1))
        config[color] = sections
        remaining -= sections
    
    config[selected_colors[-1]] = remaining
    
    # Ask about combinations
    color1, color2 = random.sample(selected_colors, 2)
    question = f"What is the probability of landing on either {color1} or {color2}?"
    
    combined = config[color1] + config[color2]
    
    # Use Python's Fraction for simplification
    frac = Fraction(combined, total)
    correct = f"{frac.numerator}/{frac.denominator}"
    
    # Generate options
    options = [correct]
    
    # Unsimplified
    if combined != frac.numerator:
        options.append(f"{combined}/{total}")
    
    # Just one color
    single_frac = Fraction(config[color1], total)
    options.append(f"{single_frac.numerator}/{single_frac.denominator}")
    
    # Inverted
    if frac.numerator != frac.denominator:
        options.append(f"{frac.denominator}/{frac.numerator}")
    
    options = list(set(options))[:4]
    
    # Make sure we have 4 options
    while len(options) < 4:
        wrong = f"{random.randint(1, total-1)}/{total}"
        if wrong not in options:
            options.append(wrong)
    
    random.shuffle(options)
    
    return {
        "question": question,
        "visual_type": "spinner",
        "visual_data": config,
        "options": options,
        "correct_answer": correct,
        "explanation": f"{color1} has {config[color1]} sections, {color2} has {config[color2]} sections. Together: {combined}/{total} = {correct}",
        "problem_type": "complex_spinner"
    }

def generate_dice_basic():
    """Generate basic dice problem"""
    scenarios = [
        {
            "question": "What is the chance of rolling a 6 on a standard die?",
            "options": ["Likely", "Unlikely", "Equally likely", "Certain"],
            "correct": "Unlikely",
            "explanation": "Only 1 out of 6 faces shows a 6, so it's unlikely (1/6 chance)."
        },
        {
            "question": "What is the chance of rolling an even number (2, 4, or 6)?",
            "options": ["Likely", "Unlikely", "Equally likely", "Impossible"],
            "correct": "Equally likely",
            "explanation": "3 out of 6 faces are even, which is exactly half (3/6 = 1/2)."
        },
        {
            "question": "What is the chance of rolling a number less than 7?",
            "options": ["Certain", "Likely", "Unlikely", "Impossible"],
            "correct": "Certain",
            "explanation": "All numbers on a die (1-6) are less than 7, so it's certain."
        },
        {
            "question": "What is the chance of rolling a 0?",
            "options": ["Unlikely", "Impossible", "Equally likely", "Certain"],
            "correct": "Impossible",
            "explanation": "A standard die doesn't have 0, so it's impossible."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "dice",
        "visual_data": {"dice_count": 1},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "dice"
    }

def generate_dice_compare():
    """Generate dice comparison problems"""
    scenarios = [
        {
            "question": "Which is more likely when rolling a die: getting an odd number or getting a prime number (2, 3, 5)?",
            "options": ["Odd number", "Prime number", "Equally likely"],
            "correct": "Equally likely",
            "explanation": "Odd: 1, 3, 5 (3 numbers). Prime: 2, 3, 5 (3 numbers). Both have 3/6 = 1/2 probability."
        },
        {
            "question": "Which is more likely: rolling a number greater than 4 or rolling an even number?",
            "options": ["Greater than 4", "Even number", "Equally likely"],
            "correct": "Even number",
            "explanation": "Greater than 4: 5, 6 (2 numbers). Even: 2, 4, 6 (3 numbers). Even is more likely."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "dice_compare"
    }

def generate_dice_fraction():
    """Generate dice problems with fraction answers"""
    scenarios = [
        {
            "question": "What is the probability of rolling a number divisible by 3 on a standard die?",
            "options": ["1/6", "1/3", "1/2", "2/3"],
            "correct": "1/3",
            "explanation": "Numbers divisible by 3: 3 and 6. That's 2 out of 6, so 2/6 = 1/3."
        },
        {
            "question": "What is the probability of rolling at least 5 on a standard die?",
            "options": ["1/6", "1/3", "1/2", "2/3"],
            "correct": "1/3",
            "explanation": "At least 5 means 5 or 6. That's 2 out of 6, so 2/6 = 1/3."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "dice_fraction"
    }

def generate_complex_dice():
    """Generate complex dice problem"""
    scenarios = [
        {
            "question": "You roll two dice. What's the probability of getting a sum of 7?",
            "options": ["1/6", "1/12", "1/36", "5/36"],
            "correct": "1/6",
            "explanation": "There are 6 ways to get 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). That's 6/36 = 1/6."
        },
        {
            "question": "You roll a die three times. What's more likely: all three the same or all three different?",
            "options": ["All same", "All different", "Equally likely"],
            "correct": "All different",
            "explanation": "All same: 6/216. All different: 120/216. So all different is more likely."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "complex_dice"
    }

def generate_bag_basic():
    """Generate basic bag/marble problem"""
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    color1, color2 = random.sample(colors, 2)
    
    count1 = random.randint(1, 8)
    count2 = random.randint(1, 8)
    
    while count1 == count2:  # Ensure different counts for basic level
        count2 = random.randint(1, 8)
    
    question = f"A bag contains {count1} {color1} marbles and {count2} {color2} marbles. Which color are you more likely to pick?"
    
    correct = color1 if count1 > count2 else color2
    
    return {
        "question": question,
        "visual_type": "bag",
        "visual_data": {color1: count1, color2: count2},
        "options": [color1, color2],
        "correct_answer": correct,
        "explanation": f"There are more {correct} marbles ({max(count1, count2)}) than {color2 if correct == color1 else color1} marbles ({min(count1, count2)}).",
        "problem_type": "bag"
    }

def generate_bag_compare():
    """Generate bag comparison problems"""
    bag1 = {"red": random.randint(3, 7), "blue": random.randint(2, 6)}
    bag2 = {"red": random.randint(2, 6), "blue": random.randint(3, 7)}
    
    question = "Which bag gives you a better chance of picking a red marble?"
    
    prob1 = bag1["red"] / sum(bag1.values())
    prob2 = bag2["red"] / sum(bag2.values())
    
    if prob1 > prob2:
        correct = "Bag A"
    elif prob2 > prob1:
        correct = "Bag B"
    else:
        correct = "Same chance"
    
    return {
        "question": f"Bag A: {bag1['red']} red, {bag1['blue']} blue. Bag B: {bag2['red']} red, {bag2['blue']} blue. {question}",
        "visual_type": "double_bag",
        "visual_data": {"bag1": bag1, "bag2": bag2},
        "options": ["Bag A", "Bag B", "Same chance"],
        "correct_answer": correct,
        "explanation": f"Bag A: {bag1['red']}/{sum(bag1.values())} = {prob1:.2f}. Bag B: {bag2['red']}/{sum(bag2.values())} = {prob2:.2f}.",
        "problem_type": "bag_compare"
    }

def generate_bag_fraction():
    """Generate bag problems with fraction answers"""
    colors = ["red", "blue", "green", "yellow"]
    num_colors = random.randint(2, 3)
    selected = random.sample(colors, num_colors)
    
    bag = {}
    total = 0
    for color in selected:
        count = random.randint(2, 5)
        bag[color] = count
        total += count
    
    target_color = random.choice(selected)
    
    # Use Python's Fraction for simplification
    frac = Fraction(bag[target_color], total)
    correct = f"{frac.numerator}/{frac.denominator}"
    
    question = f"What is the probability of picking a {target_color} marble?"
    
    # Generate options
    options = [correct]
    
    # Unsimplified
    if bag[target_color] != frac.numerator:
        options.append(f"{bag[target_color]}/{total}")
    
    # Inverted
    if frac.numerator != frac.denominator:
        options.append(f"{frac.denominator}/{frac.numerator}")
    
    # Equal probability assumption
    options.append(f"1/{num_colors}")
    
    options = list(set(options))[:4]
    
    # Ensure 4 options
    while len(options) < 4:
        options.append(f"{random.randint(1, total-1)}/{total}")
    
    random.shuffle(options)
    
    bag_description = ", ".join([f"{v} {k}" for k, v in bag.items()])
    
    return {
        "question": f"A bag contains {bag_description} marbles. {question}",
        "visual_type": "bag",
        "visual_data": bag,
        "options": options,
        "correct_answer": correct,
        "explanation": f"{target_color}: {bag[target_color]} out of {total} total. Probability = {bag[target_color]}/{total} = {correct}",
        "problem_type": "bag_fraction"
    }

def generate_complex_bag():
    """Generate complex bag problem"""
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    num_colors = random.randint(3, 4)
    selected_colors = random.sample(colors, num_colors)
    
    bag = {}
    total = 0
    for color in selected_colors:
        count = random.randint(2, 6)
        bag[color] = count
        total += count
    
    # Ask about picking without replacement
    color = random.choice(selected_colors)
    
    question = f"You pick 2 marbles without replacement. What's the probability that both are {color}?"
    
    if bag[color] >= 2:
        # Calculate probability using Python's Fraction
        prob_num = bag[color] * (bag[color] - 1)
        prob_den = total * (total - 1)
        frac = Fraction(prob_num, prob_den)
        correct = f"{frac.numerator}/{frac.denominator}"
    else:
        correct = "0"
    
    # Generate options
    options = [correct, "0"]
    
    # Single probability
    single_frac = Fraction(bag[color], total)
    options.append(f"{single_frac.numerator}/{single_frac.denominator}")
    
    # Wrong calculation
    options.append(f"1/{total}")
    
    options = list(set(options))[:4]
    random.shuffle(options)
    
    bag_description = ", ".join([f"{v} {k}" for k, v in bag.items()])
    
    return {
        "question": f"A bag has {bag_description} marbles. {question}",
        "visual_type": "bag",
        "visual_data": bag,
        "options": options,
        "correct_answer": correct,
        "explanation": f"First {color}: {bag[color]}/{total}. Second {color}: {bag[color]-1 if bag[color] > 0 else 0}/{total-1}. Both: {correct}",
        "problem_type": "complex_bag"
    }

def generate_cards_basic():
    """Generate basic card problem"""
    scenarios = [
        {
            "question": "What is the chance of picking a red card from a standard deck?",
            "options": ["1/4", "1/2", "1/3", "3/4"],
            "correct": "1/2",
            "explanation": "Half the cards (26 out of 52) are red (hearts and diamonds)."
        },
        {
            "question": "What is the chance of picking a King from a standard deck?",
            "options": ["1/13", "1/4", "1/52", "4/13"],
            "correct": "1/13",
            "explanation": "There are 4 Kings in 52 cards, so 4/52 = 1/13."
        },
        {
            "question": "Is picking a heart more likely, less likely, or equally likely as picking a spade?",
            "options": ["More likely", "Less likely", "Equally likely"],
            "correct": "Equally likely",
            "explanation": "There are 13 hearts and 13 spades, so they're equally likely."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "cards",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "cards"
    }

def generate_certain_impossible():
    """Generate certain/impossible scenarios"""
    scenarios = [
        {
            "question": "Tomorrow will be either Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or Monday. This is:",
            "options": ["Certain", "Likely", "Unlikely", "Impossible"],
            "correct": "Certain",
            "explanation": "Tomorrow must be one of the seven days of the week."
        },
        {
            "question": "You will grow younger tomorrow. This is:",
            "options": ["Certain", "Likely", "Unlikely", "Impossible"],
            "correct": "Impossible",
            "explanation": "Time only moves forward, so you can't grow younger."
        },
        {
            "question": "If you flip a coin, it will land on heads or tails. This is:",
            "options": ["Certain", "Likely", "Unlikely", "Impossible"],
            "correct": "Certain",
            "explanation": "A coin must land on either heads or tails."
        },
        {
            "question": "You will roll an 8 on a standard six-sided die. This is:",
            "options": ["Unlikely", "Impossible", "Equally likely", "Certain"],
            "correct": "Impossible",
            "explanation": "A standard die only has numbers 1-6."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "certain_impossible"
    }

def generate_multiple_events():
    """Generate problems with multiple events"""
    scenarios = [
        {
            "question": "You roll two dice. What's more likely: getting two 6s or getting at least one 6?",
            "options": ["Two 6s", "At least one 6", "Equally likely"],
            "correct": "At least one 6",
            "explanation": "Getting two 6s has probability 1/36. Getting at least one 6 has probability 11/36."
        },
        {
            "question": "You flip two coins. What's the probability of getting two heads?",
            "options": ["1/2", "1/4", "1/3", "3/4"],
            "correct": "1/4",
            "explanation": "Each coin has 1/2 chance of heads. Both heads: 1/2 × 1/2 = 1/4."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "multiple_events"
    }

def generate_real_world():
    """Generate real-world probability scenarios"""
    scenarios = [
        {
            "question": "There are 30 students in a class. 18 like pizza, 12 like burgers. If you pick a random student, are they more likely to like pizza?",
            "options": ["Yes", "No", "Can't tell"],
            "correct": "Yes",
            "explanation": "18/30 students like pizza vs 12/30 like burgers. Pizza is more likely."
        },
        {
            "question": "In a parking lot, 15 cars are red, 10 are blue, 5 are white. What fraction of cars are NOT red?",
            "options": ["1/2", "1/3", "2/3", "3/5"],
            "correct": "1/2",
            "explanation": "Total: 30 cars. Not red: 15 cars. Fraction: 15/30 = 1/2."
        },
        {
            "question": "Weather forecast says 30% chance of rain. Is it more likely to rain or not rain?",
            "options": ["More likely to rain", "More likely not to rain", "Equally likely"],
            "correct": "More likely not to rain",
            "explanation": "30% chance of rain means 70% chance of no rain. 70% > 30%."
        }
    ]
    
    scenario = random.choice(scenarios)
    
    return {
        "question": scenario["question"],
        "visual_type": "none",
        "visual_data": {},
        "options": scenario["options"],
        "correct_answer": scenario["correct"],
        "explanation": scenario["explanation"],
        "problem_type": "real_world"
    }

def display_spinner(config):
    """Display a spinner visualization with visible sections"""
    
    # Calculate total sections
    total_sections = sum(config.values())
    labels = list(config.keys())
    
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
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Calculate angles for each individual section
    section_colors = []
    
    # Create individual sections (not just grouped by color)
    for label, count in config.items():
        for _ in range(count):
            section_colors.append(colors_map.get(label, "#CCCCCC"))
    
    # Draw the spinner with individual sections
    start_angle = 90
    angle_per_section = 360 / total_sections
    
    for i, color in enumerate(section_colors):
        # Calculate angles for this section
        theta1 = i * angle_per_section
        theta2 = (i + 1) * angle_per_section
        
        # Draw each section
        wedge = plt.matplotlib.patches.Wedge(
            center=(0, 0),
            r=1,
            theta1=theta1 + start_angle,
            theta2=theta2 + start_angle,
            facecolor=color,
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(wedge)
        
        # Add radial lines to show section boundaries
        angle_rad = math.radians(theta1 + start_angle)
        line_x = [0, math.cos(angle_rad)]
        line_y = [0, math.sin(angle_rad)]
        ax.plot(line_x, line_y, 'k-', linewidth=1.5)
    
    # Add the final divider line
    angle_rad = math.radians(start_angle)
    line_x = [0, math.cos(angle_rad)]
    line_y = [0, math.sin(angle_rad)]
    ax.plot(line_x, line_y, 'k-', linewidth=1.5)
    
    # Add spinner arrow
    arrow = plt.Arrow(0, 0, 0.3, 0.3, width=0.15, color='red', zorder=10)
    ax.add_patch(arrow)
    
    # Add center circle
    circle = plt.Circle((0, 0), 0.08, color='black', zorder=11)
    ax.add_patch(circle)
    
    # Set limits and aspect
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create a clear title showing the section counts
    title_parts = []
    for color, count in config.items():
        title_parts.append(f"{count} {color}")
    title = "Spinner with " + " and ".join(title_parts) + f" ({total_sections} Equal Sections)"
    plt.title(title, fontsize=12, fontweight='bold')
    
    # Display in Streamlit
    st.pyplot(fig)
    plt.close()
    
    # Show legend with exact counts and fractions
    legend_parts = []
    for color, sections in config.items():
        frac = Fraction(sections, total_sections)
        simplified = f"{frac.numerator}/{frac.denominator}"
        percentage = (sections / total_sections) * 100
        legend_parts.append(f"{color}: {sections}/{total_sections} = {simplified} ({percentage:.0f}%)")
    
    legend_text = " | ".join(legend_parts)
    st.info(f"**Section Details:** {legend_text}")

def display_double_spinner(data):
    """Display two spinners side by side"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Spinner A**")
        display_spinner(data["spinner1"])
    
    with col2:
        st.markdown("**Spinner B**")
        display_spinner(data["spinner2"])

def display_dice(data):
    """Display dice visualization"""
    st.markdown("### 🎲 Standard Six-Sided Die")
    st.info("A standard die has faces numbered 1 through 6")
    
    # Show dice faces using emojis
    dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    st.markdown("**Die faces:**")
    st.markdown(" ".join(dice_faces))

def display_cards():
    """Display card deck info"""
    st.markdown("### 🃏 Standard Deck of Cards")
    st.info("""
    A standard deck has:
    - 52 total cards
    - 4 suits: ♠️ Spades, ♥️ Hearts, ♦️ Diamonds, ♣️ Clubs
    - 13 cards per suit
    - 26 red cards (Hearts + Diamonds)
    - 26 black cards (Spades + Clubs)
    """)

def display_bag(config):
    """Display bag with marbles"""
    colors_map = {
        "red": "🔴",
        "blue": "🔵",
        "green": "🟢",
        "yellow": "🟡",
        "purple": "🟣",
        "orange": "🟠",
        "white": "⚪",
        "black": "⚫"
    }
    
    st.markdown("### 🎒 Bag of Marbles")
    
    # Create visual representation
    marbles = []
    for color, count in config.items():
        emoji = colors_map.get(color, "⚪")
        marbles.extend([emoji] * count)
    
    random.shuffle(marbles)
    
    # Display marbles
    marble_string = " ".join(marbles)
    st.markdown(f"**Marbles in bag:** {marble_string}")
    
    # Show counts
    counts = " | ".join([f"{color}: {count}" for color, count in config.items()])
    st.info(f"**Counts:** {counts}")

def display_double_bag(data):
    """Display two bags side by side"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Bag A**")
        display_bag(data["bag1"])
    
    with col2:
        st.markdown("**Bag B**")
        display_bag(data["bag2"])

def display_problem():
    """Display the current problem with appropriate visualization"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_problem}")
    
    # Display visualization based on type
    visual_type = data.get("visual_type", "none")
    
    if visual_type == "spinner":
        display_spinner(data["visual_data"])
    elif visual_type == "double_spinner":
        display_double_spinner(data["visual_data"])
    elif visual_type == "dice":
        display_dice(data.get("visual_data", {}))
    elif visual_type == "bag":
        display_bag(data["visual_data"])
    elif visual_type == "double_bag":
        display_double_bag(data["visual_data"])
    elif visual_type == "cards":
        display_cards()
    
    st.markdown("---")
    
    # Display answer options
    display_answer_options(data["options"])
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation buttons
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 See Explanation", type="secondary", use_container_width=True):
                show_detailed_explanation()
            
            if st.button("Next Question →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_answer_options(options):
    """Display answer options as buttons"""
    # Determine layout based on number of options
    if len(options) == 2:
        cols = st.columns(2)
    elif len(options) == 3:
        cols = st.columns(3)
    else:
        cols = st.columns(2)
        
    # Display buttons
    for i, option in enumerate(options):
        col_idx = i % len(cols)
        with cols[col_idx]:
            if st.button(
                option,
                key=f"option_{i}",
                use_container_width=True,
                disabled=st.session_state.answer_submitted
            ):
                st.session_state.user_answer = option
                check_answer()

def check_answer():
    """Check if the user's answer is correct"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    st.session_state.answer_correct = (user_answer == correct_answer)
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if st.session_state.answer_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    
    if st.session_state.answer_correct:
        st.success(f"✅ **Correct! {st.session_state.correct_answer} is right!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.probability_difficulty
            st.session_state.probability_difficulty = min(
                st.session_state.probability_difficulty + 1, 4
            )
            
            if st.session_state.probability_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Great job! Moving to Level {st.session_state.probability_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. The correct answer is {st.session_state.correct_answer}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.probability_difficulty
            st.session_state.probability_difficulty = max(
                st.session_state.probability_difficulty - 1, 1
            )
            
            if st.session_state.probability_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.probability_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_detailed_explanation():
    """Show detailed probability explanation"""
    with st.expander("📚 **Detailed Explanation**", expanded=True):
        data = st.session_state.problem_data
        problem_type = data.get("problem_type", "")
        
        st.markdown("### Understanding the Solution:")
        st.markdown(data['explanation'])
        
        # Add specific guidance based on problem type
        if "spinner" in problem_type:
            st.markdown("""
            ### 🎯 Spinner Tips:
            - Count the total sections
            - Count sections of the color in question
            - Probability = favorable sections / total sections
            - More sections = more likely
            """)
        elif "dice" in problem_type:
            st.markdown("""
            ### 🎲 Dice Tips:
            - Standard die has 6 faces (1-6)
            - Each face has equal chance (1/6)
            - Count favorable outcomes
            - Probability = favorable / 6
            """)
        elif "bag" in problem_type:
            st.markdown("""
            ### 🎒 Bag Tips:
            - Count total marbles
            - Count marbles of desired color
            - Probability = desired marbles / total marbles
            - More marbles = more likely to pick
            """)
        
        # Show probability scale
        st.markdown("---")
        st.markdown("### 📊 Probability Scale:")
        st.markdown("""
        - **0** = Impossible (will never happen)
        - **1/4** = Unlikely (probably won't happen)
        - **1/2** = Equally likely (50-50 chance)
        - **3/4** = Likely (probably will happen)
        - **1** = Certain (will definitely happen)
        """)

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