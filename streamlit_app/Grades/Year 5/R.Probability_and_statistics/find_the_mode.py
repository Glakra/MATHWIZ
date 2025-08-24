import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter
import numpy as np

def run():
    """
    Main function to run the Find the Mode activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/find_the_mode.py
    """
    # Initialize session state
    if "mode_difficulty" not in st.session_state:
        st.session_state.mode_difficulty = 1
    
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
    st.title("📊 Find the Mode")
    st.markdown("*Find the most frequently occurring value in a dataset*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mode_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Small Sets (5-8 numbers)",
            2: "Medium Sets (8-12 numbers)",
            3: "Large Sets with Context",
            4: "Multiple Modes & No Mode",
            5: "Real-World Applications"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 3:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level == 4:
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
    with st.expander("📚 **Understanding the Mode**", expanded=False):
        st.markdown("""
        ### 📊 What is the Mode?
        
        **The mode is the value that appears MOST OFTEN in a dataset.**
        
        ### 📝 How to Find the Mode:
        
        1. **Count** how many times each value appears
        2. **Find** the value that appears most frequently
        3. **That's** your mode!
        
        ### 🎯 Examples:
        
        **Example 1:** 3, 5, 3, 7, 3, 9
        - 3 appears 3 times
        - 5 appears 1 time
        - 7 appears 1 time
        - 9 appears 1 time
        - **Mode = 3** ✓
        
        **Example 2:** 2, 4, 4, 6, 6, 6, 8
        - 2 appears 1 time
        - 4 appears 2 times
        - 6 appears 3 times
        - 8 appears 1 time
        - **Mode = 6** ✓
        
        ### 💡 Special Cases:
        
        - **No Mode:** When all values appear the same number of times
        - **Multiple Modes (Bimodal):** When two or more values tie for most frequent
        - **Real-World Use:** Most popular item, common shoe size, favorite color
        
        ### 🔑 Key Tips:
        - Make a frequency table to organize your counting
        - Circle or highlight as you count
        - Double-check your counting!
        """)

def generate_new_problem():
    """Generate a new mode problem based on difficulty"""
    difficulty = st.session_state.mode_difficulty
    
    if difficulty == 1:
        # Level 1: Small sets with clear mode
        problem_data = generate_simple_mode_problem()
    elif difficulty == 2:
        # Level 2: Medium sets with clear mode
        problem_data = generate_medium_mode_problem()
    elif difficulty == 3:
        # Level 3: Large sets with context
        problem_data = generate_context_mode_problem()
    elif difficulty == 4:
        # Level 4: Multiple modes or no mode
        problem_data = generate_special_mode_problem()
    else:
        # Level 5: Real-world applications
        problem_data = generate_real_world_mode_problem()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_simple_mode_problem():
    """Generate Level 1 problems - small clear datasets"""
    scenarios = [
        {
            "type": "numbers",
            "size": random.randint(5, 7)
        },
        {
            "type": "colors",
            "size": random.randint(6, 8)
        },
        {
            "type": "shapes",
            "size": random.randint(5, 7)
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if scenario["type"] == "numbers":
        # Create dataset with clear mode
        mode_value = random.randint(1, 10)
        mode_frequency = random.randint(3, 4)
        
        # Generate the dataset
        dataset = [mode_value] * mode_frequency
        
        # Add other values
        other_values = [x for x in range(1, 11) if x != mode_value]
        remaining_spots = scenario["size"] - mode_frequency
        
        for _ in range(remaining_spots):
            dataset.append(random.choice(other_values))
        
        random.shuffle(dataset)
        
        return {
            "question": "What is the mode?",
            "dataset": dataset,
            "display_type": "numbers",
            "correct_answer": str(mode_value),
            "explanation": f"The number {mode_value} appears {mode_frequency} times, more than any other number.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    elif scenario["type"] == "colors":
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        mode_color = random.choice(colors[:4])
        mode_frequency = random.randint(3, 4)
        
        dataset = [mode_color] * mode_frequency
        other_colors = [c for c in colors if c != mode_color]
        
        remaining_spots = scenario["size"] - mode_frequency
        for _ in range(remaining_spots):
            dataset.append(random.choice(other_colors))
        
        random.shuffle(dataset)
        
        return {
            "question": "What color appears most often?",
            "dataset": dataset,
            "display_type": "colors",
            "correct_answer": mode_color,
            "explanation": f"The color {mode_color} appears {mode_frequency} times, more than any other color.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    else:  # shapes
        shapes = ["circle", "square", "triangle", "star", "heart"]
        mode_shape = random.choice(shapes[:3])
        mode_frequency = random.randint(3, 4)
        
        dataset = [mode_shape] * mode_frequency
        other_shapes = [s for s in shapes if s != mode_shape]
        
        remaining_spots = scenario["size"] - mode_frequency
        for _ in range(remaining_spots):
            dataset.append(random.choice(other_shapes))
        
        random.shuffle(dataset)
        
        return {
            "question": "What shape appears most often?",
            "dataset": dataset,
            "display_type": "shapes",
            "correct_answer": mode_shape,
            "explanation": f"The {mode_shape} appears {mode_frequency} times, more than any other shape.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }

def generate_medium_mode_problem():
    """Generate Level 2 problems - medium datasets"""
    scenarios = [
        "dice_rolls",
        "test_scores",
        "ages",
        "shoe_sizes"
    ]
    
    scenario = random.choice(scenarios)
    
    if scenario == "dice_rolls":
        mode_value = random.randint(1, 6)
        mode_frequency = random.randint(4, 5)
        dataset_size = random.randint(10, 12)
        
        dataset = [mode_value] * mode_frequency
        remaining = dataset_size - mode_frequency
        
        for _ in range(remaining):
            value = random.randint(1, 6)
            if value != mode_value:
                dataset.append(value)
            else:
                dataset.append(random.choice([x for x in range(1, 7) if x != mode_value]))
        
        random.shuffle(dataset)
        
        return {
            "question": "A die was rolled multiple times. What number came up most often?",
            "dataset": dataset,
            "display_type": "dice",
            "correct_answer": str(mode_value),
            "explanation": f"The number {mode_value} was rolled {mode_frequency} times, more than any other number.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    elif scenario == "test_scores":
        scores = [6, 7, 8, 9, 10]
        mode_score = random.choice(scores)
        mode_frequency = random.randint(4, 5)
        dataset_size = random.randint(10, 12)
        
        dataset = [mode_score] * mode_frequency
        remaining = dataset_size - mode_frequency
        
        other_scores = [s for s in scores if s != mode_score]
        for _ in range(remaining):
            dataset.append(random.choice(other_scores))
        
        random.shuffle(dataset)
        
        return {
            "question": "Students took a quiz worth 10 points. What was the most common score?",
            "dataset": dataset,
            "display_type": "scores",
            "correct_answer": str(mode_score),
            "explanation": f"The score {mode_score} appeared {mode_frequency} times, more than any other score.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    elif scenario == "ages":
        ages = list(range(8, 13))
        mode_age = random.choice(ages)
        mode_frequency = random.randint(4, 5)
        dataset_size = random.randint(10, 12)
        
        dataset = [mode_age] * mode_frequency
        remaining = dataset_size - mode_frequency
        
        other_ages = [a for a in ages if a != mode_age]
        for _ in range(remaining):
            dataset.append(random.choice(other_ages))
        
        random.shuffle(dataset)
        
        return {
            "question": "What is the most common age in this group of students?",
            "dataset": dataset,
            "display_type": "ages",
            "correct_answer": str(mode_age),
            "explanation": f"Age {mode_age} appears {mode_frequency} times, more than any other age.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    else:  # shoe_sizes
        sizes = [3, 3.5, 4, 4.5, 5, 5.5, 6]
        mode_size = random.choice(sizes[1:5])
        mode_frequency = random.randint(4, 5)
        dataset_size = random.randint(10, 12)
        
        dataset = [mode_size] * mode_frequency
        remaining = dataset_size - mode_frequency
        
        other_sizes = [s for s in sizes if s != mode_size]
        for _ in range(remaining):
            dataset.append(random.choice(other_sizes))
        
        random.shuffle(dataset)
        
        return {
            "question": "What is the most common shoe size in the class?",
            "dataset": dataset,
            "display_type": "shoe_sizes",
            "correct_answer": str(mode_size),
            "explanation": f"Size {mode_size} appears {mode_frequency} times, more than any other size.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }

def generate_context_mode_problem():
    """Generate Level 3 problems - larger datasets with context"""
    scenarios = [
        {
            "context": "A candy store tracked which flavors customers bought today",
            "items": ["chocolate", "strawberry", "vanilla", "mint", "caramel", "orange"],
            "dataset_size": 15
        },
        {
            "context": "Students voted for their favorite sport",
            "items": ["soccer", "basketball", "tennis", "swimming", "running"],
            "dataset_size": 18
        },
        {
            "context": "A survey asked people their favorite day of the week",
            "items": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "dataset_size": 20
        },
        {
            "context": "Children chose their favorite pizza topping",
            "items": ["cheese", "pepperoni", "mushroom", "sausage", "pineapple"],
            "dataset_size": 16
        }
    ]
    
    scenario = random.choice(scenarios)
    mode_item = random.choice(scenario["items"][:4])
    mode_frequency = random.randint(6, 8)
    
    dataset = [mode_item] * mode_frequency
    remaining = scenario["dataset_size"] - mode_frequency
    
    # Distribute remaining items
    other_items = [item for item in scenario["items"] if item != mode_item]
    for _ in range(remaining):
        dataset.append(random.choice(other_items))
    
    random.shuffle(dataset)
    
    return {
        "question": f"{scenario['context']}. What was the most popular choice?",
        "dataset": dataset,
        "display_type": "context",
        "correct_answer": mode_item,
        "explanation": f"{mode_item.capitalize()} was chosen {mode_frequency} times, more than any other option.",
        "visual_data": {
            "values": dataset,
            "frequency": Counter(dataset),
            "context": scenario["context"]
        }
    }

def generate_special_mode_problem():
    """Generate Level 4 problems - multiple modes or no mode"""
    problem_types = ["no_mode", "bimodal", "trimodal"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "no_mode":
        # All values appear same number of times
        values = random.sample(range(1, 20), 4)
        frequency = 2
        dataset = []
        for value in values:
            dataset.extend([value] * frequency)
        random.shuffle(dataset)
        
        return {
            "question": "What is the mode? (Type 'none' if there is no mode)",
            "dataset": dataset,
            "display_type": "numbers",
            "correct_answer": "none",
            "explanation": f"All values appear exactly {frequency} times, so there is no mode.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    elif problem_type == "bimodal":
        # Two modes
        mode1 = random.randint(1, 5)
        mode2 = random.randint(6, 10)
        mode_frequency = random.randint(4, 5)
        
        dataset = [mode1] * mode_frequency + [mode2] * mode_frequency
        
        # Add other values with lower frequency
        other_values = [x for x in range(1, 11) if x not in [mode1, mode2]]
        for _ in range(4):
            dataset.append(random.choice(other_values))
        
        random.shuffle(dataset)
        modes = sorted([mode1, mode2])
        
        return {
            "question": "What are the modes? (Enter smaller number first, separated by comma)",
            "dataset": dataset,
            "display_type": "numbers",
            "correct_answer": f"{modes[0]},{modes[1]}",
            "explanation": f"Both {modes[0]} and {modes[1]} appear {mode_frequency} times. This dataset is bimodal.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }
    
    else:  # trimodal
        modes = random.sample(range(1, 10), 3)
        mode_frequency = 3
        
        dataset = []
        for mode in modes:
            dataset.extend([mode] * mode_frequency)
        
        # Add a few other values
        other_values = [x for x in range(1, 10) if x not in modes]
        for _ in range(3):
            dataset.append(random.choice(other_values))
        
        random.shuffle(dataset)
        modes_sorted = sorted(modes)
        
        return {
            "question": "What are the modes? (Enter all, separated by commas, smallest first)",
            "dataset": dataset,
            "display_type": "numbers",
            "correct_answer": f"{modes_sorted[0]},{modes_sorted[1]},{modes_sorted[2]}",
            "explanation": f"The values {modes_sorted[0]}, {modes_sorted[1]}, and {modes_sorted[2]} all appear {mode_frequency} times.",
            "visual_data": {
                "values": dataset,
                "frequency": Counter(dataset)
            }
        }

def generate_real_world_mode_problem():
    """Generate Level 5 problems - real-world applications"""
    scenarios = [
        {
            "context": "A clothing store wants to know which size to stock most of",
            "data_type": "T-shirt sizes",
            "values": ["XS", "S", "M", "L", "XL"],
            "question": "Based on last month's sales, which size should they order the most of?"
        },
        {
            "context": "A school cafeteria is planning next week's menu",
            "data_type": "lunch choices",
            "values": ["pizza", "burger", "salad", "pasta", "sandwich"],
            "question": "Based on this week's choices, what should be the main option?"
        },
        {
            "context": "A game developer is analyzing player levels",
            "data_type": "player levels",
            "values": list(range(1, 11)),
            "question": "What level are most players currently at?"
        },
        {
            "context": "A bus company is optimizing their schedule",
            "data_type": "boarding times",
            "values": ["7am", "8am", "9am", "10am", "11am", "noon"],
            "question": "When do most passengers board the bus?"
        },
        {
            "context": "A library is deciding which genre to expand",
            "data_type": "book checkouts",
            "values": ["fiction", "mystery", "science", "history", "art", "sports"],
            "question": "Which genre is borrowed most often?"
        }
    ]
    
    scenario = random.choice(scenarios)
    mode_value = random.choice(scenario["values"][:len(scenario["values"])//2])
    mode_frequency = random.randint(8, 12)
    dataset_size = random.randint(25, 30)
    
    dataset = [mode_value] * mode_frequency
    remaining = dataset_size - mode_frequency
    
    # Create realistic distribution
    other_values = [v for v in scenario["values"] if v != mode_value]
    
    # Add second most common
    if remaining > 5:
        second_value = random.choice(other_values)
        second_frequency = random.randint(4, 6)
        dataset.extend([second_value] * second_frequency)
        remaining -= second_frequency
        other_values = [v for v in other_values if v != second_value]
    
    # Distribute rest
    for _ in range(remaining):
        dataset.append(random.choice(other_values))
    
    random.shuffle(dataset)
    
    return {
        "question": f"{scenario['context']}. {scenario['question']}",
        "dataset": dataset,
        "display_type": "real_world",
        "correct_answer": str(mode_value),
        "explanation": f"{mode_value} appears {mode_frequency} times out of {dataset_size} total. This is the mode and should guide the decision.",
        "visual_data": {
            "values": dataset,
            "frequency": Counter(dataset),
            "context": scenario["context"],
            "data_type": scenario["data_type"]
        }
    }

def display_problem():
    """Display the current problem with appropriate visualization"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Display dataset based on type
    display_type = data.get("display_type", "numbers")
    
    if display_type == "numbers":
        display_numbers(data["dataset"])
    elif display_type == "colors":
        display_colors(data["dataset"])
    elif display_type == "shapes":
        display_shapes(data["dataset"])
    elif display_type == "dice":
        display_dice(data["dataset"])
    elif display_type == "scores":
        display_scores(data["dataset"])
    elif display_type == "ages":
        display_ages(data["dataset"])
    elif display_type == "shoe_sizes":
        display_shoe_sizes(data["dataset"])
    elif display_type == "context":
        display_context_data(data["dataset"])
    elif display_type == "real_world":
        display_real_world_data(data)
    
    st.markdown("---")
    
    # Input form
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Check if this is a special case problem
        if "none" in str(data.get("correct_answer", "")).lower() or "," in str(data.get("correct_answer", "")):
            placeholder = "Enter answer (use comma for multiple)"
        else:
            placeholder = "Enter the mode"
        
        user_input = st.text_input(
            "Your answer:",
            placeholder=placeholder,
            disabled=st.session_state.answer_submitted,
            key="mode_input"
        )
    
    with col2:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                st.session_state.user_answer = user_input.strip().lower()
                check_answer()
            else:
                st.warning("Please enter your answer.")
    
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
            if st.button("📊 Show Frequency Table", type="secondary", use_container_width=True):
                show_frequency_table()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_numbers(dataset):
    """Display numbers in a grid"""
    # Create colored boxes for numbers
    colors = ['#FFE5E5', '#E5F2FF', '#E5FFE5', '#FFF5E5', '#F5E5FF', '#E5FFF5']
    
    # Group numbers for coloring
    unique_values = list(set(dataset))
    color_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_values)}
    
    # Display in rows
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, val in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        background-color: {color_map[val]};
                        padding: 15px;
                        border-radius: 10px;
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                        margin: 2px;
                    ">{val}</div>""",
                    unsafe_allow_html=True
                )

def display_colors(dataset):
    """Display color blocks"""
    color_codes = {
        "red": "#FF6B6B",
        "blue": "#4DABF7",
        "green": "#51CF66",
        "yellow": "#FFD93D",
        "purple": "#9775FA",
        "orange": "#FFA94D"
    }
    
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, color in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        background-color: {color_codes.get(color, '#888')};
                        padding: 20px;
                        border-radius: 10px;
                        margin: 2px;
                        border: 2px solid #ddd;
                    ">&nbsp;</div>""",
                    unsafe_allow_html=True
                )

def display_shapes(dataset):
    """Display shapes"""
    shape_emojis = {
        "circle": "⭕",
        "square": "⬜",
        "triangle": "🔺",
        "star": "⭐",
        "heart": "❤️"
    }
    
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, shape in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        text-align: center;
                        font-size: 30px;
                        padding: 10px;
                    ">{shape_emojis.get(shape, '?')}</div>""",
                    unsafe_allow_html=True
                )

def display_dice(dataset):
    """Display dice values"""
    dice_faces = {
        1: "⚀", 2: "⚁", 3: "⚂",
        4: "⚃", 5: "⚄", 6: "⚅"
    }
    
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    st.markdown("**Dice rolls:**")
    for row in rows:
        cols = st.columns(len(row))
        for i, val in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        text-align: center;
                        font-size: 40px;
                        padding: 5px;
                    ">{dice_faces.get(val, str(val))}</div>""",
                    unsafe_allow_html=True
                )

def display_scores(dataset):
    """Display test scores"""
    st.markdown("**Test Scores (out of 10):**")
    
    # Create a visual bar for each score
    score_str = ""
    for i, score in enumerate(dataset):
        if i > 0:
            score_str += ", "
        if i % 10 == 0 and i > 0:
            score_str += "\n"
        score_str += f"**{score}**"
    
    st.markdown(score_str)

def display_ages(dataset):
    """Display ages"""
    st.markdown("**Ages of students:**")
    
    # Display as cards
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, age in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        background-color: #E8F4FD;
                        padding: 10px;
                        border-radius: 8px;
                        text-align: center;
                        font-weight: bold;
                        border: 1px solid #B8E0FF;
                    ">{age} yrs</div>""",
                    unsafe_allow_html=True
                )

def display_shoe_sizes(dataset):
    """Display shoe sizes"""
    st.markdown("**Shoe sizes in the class:**")
    
    # Display as shoe icons with sizes
    items_per_row = 8
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, size in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""<div style="
                        background-color: #FFF0E5;
                        padding: 10px;
                        border-radius: 8px;
                        text-align: center;
                        font-weight: bold;
                        border: 1px solid #FFD4B3;
                    ">👟<br>{size}</div>""",
                    unsafe_allow_html=True
                )

def display_context_data(dataset):
    """Display context data as a list"""
    st.markdown("**Responses:**")
    
    # Group and display
    items_per_row = 6
    rows = [dataset[i:i+items_per_row] for i in range(0, len(dataset), items_per_row)]
    
    for row in rows:
        row_text = " | ".join([f"**{item}**" for item in row])
        st.markdown(row_text)

def display_real_world_data(data):
    """Display real-world scenario data"""
    dataset = data["dataset"]
    visual_data = data["visual_data"]
    
    st.info(f"📊 **{visual_data['data_type'].title()} Data** ({len(dataset)} entries)")
    
    # Create a simple bar chart
    freq = visual_data["frequency"]
    
    if len(freq) <= 8:
        fig, ax = plt.subplots(figsize=(10, 4))
        items = list(freq.keys())
        counts = list(freq.values())
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(items)))
        bars = ax.bar(items, counts, color=colors)
        
        ax.set_xlabel(visual_data["data_type"].title())
        ax.set_ylabel("Frequency")
        ax.set_title("Data Distribution")
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}',
                   ha='center', va='bottom')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        # For large datasets, show as text
        display_context_data(dataset)

def check_answer():
    """Check the user's answer"""
    user_answer = st.session_state.user_answer
    correct_answer = str(st.session_state.correct_answer).lower()
    
    # Handle different answer formats
    if "," in correct_answer:
        # Multiple modes
        correct_values = [x.strip() for x in correct_answer.split(",")]
        user_values = [x.strip() for x in user_answer.split(",")]
        is_correct = set(correct_values) == set(user_values)
    else:
        # Single mode or "none"
        is_correct = user_answer == correct_answer
    
    st.session_state.answer_correct = is_correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if is_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The correct answer was: **{data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {data['correct_answer']} is the mode!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.mode_difficulty
            st.session_state.mode_difficulty = min(
                st.session_state.mode_difficulty + 1, 5
            )
            
            if st.session_state.mode_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Great job! Moving to Level {st.session_state.mode_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. You said {st.session_state.user_answer}, but the correct answer is {data['correct_answer']}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.mode_difficulty
            st.session_state.mode_difficulty = max(
                st.session_state.mode_difficulty - 1, 1
            )
            
            if st.session_state.mode_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.mode_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_frequency_table():
    """Show frequency table for the dataset"""
    with st.expander("📊 **Frequency Table**", expanded=True):
        data = st.session_state.problem_data
        freq = data["visual_data"]["frequency"]
        
        st.markdown("### How many times each value appears:")
        
        # Create frequency table
        sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        # Display as table
        table_data = []
        for value, count in sorted_items:
            table_data.append({
                "Value": str(value),
                "Frequency": count,
                "Visual": "█" * count
            })
        
        st.table(table_data)
        
        # Highlight the mode
        max_freq = sorted_items[0][1]
        modes = [str(item[0]) for item in sorted_items if item[1] == max_freq]
        
        if len(modes) == 1:
            st.success(f"**The mode is {modes[0]}** (appears {max_freq} times)")
        elif len(modes) == len(freq):
            st.info("**No mode** - all values appear the same number of times")
        else:
            st.success(f"**Multiple modes: {', '.join(modes)}** (each appears {max_freq} times)")

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