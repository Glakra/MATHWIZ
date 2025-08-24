import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import random

def run():
    """
    Main function to run the Interpret Bar Graphs activity.
    Interactive bar graph interpretation with progressive difficulty.
    """
    # Initialize session state
    if "bar_graph_difficulty" not in st.session_state:
        st.session_state.bar_graph_difficulty = 1
        st.session_state.bar_graph_consecutive_correct = 0
        st.session_state.bar_graph_consecutive_wrong = 0
        st.session_state.bar_graph_total_score = 0
        st.session_state.bar_graph_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.user_answer = None
        st.session_state.answer_submitted = False
    
    if "current_bar_graph_problem" not in st.session_state:
        generate_bar_graph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📊 Interpret Bar Graphs")
    st.markdown("*Read and analyze information from bar graphs*")
    st.markdown("---")
    
    # Display progress
    display_bar_graph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_bar_graph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_bar_graph_problem()
    
    # Instructions
    with st.expander("💡 **How to Read Bar Graphs**", expanded=False):
        st.markdown("""
        ### Understanding Bar Graphs:
        - **Bars** represent different categories or items
        - **Height** of each bar shows the value or quantity
        - **X-axis** (horizontal) shows categories
        - **Y-axis** (vertical) shows values
        
        ### Types of Questions:
        1. **Read values** - Find the exact value of a bar
        2. **Compare** - Which bar is tallest/shortest?
        3. **Calculate differences** - How much more/less?
        4. **Find totals** - Add values together
        5. **Identify patterns** - What trends do you see?
        
        ### Tips:
        - Use the scale on the y-axis carefully
        - Line up with grid lines for accuracy
        - Check units (ones, tens, hundreds)
        - Double-check your reading
        - **Note**: When bars have the same height, any of them can be the correct answer!
        
        ### Difficulty Levels:
        - **Level 1**: Simple values (0-20)
        - **Level 2**: Larger values (0-50)
        - **Level 3**: Comparison questions
        - **Level 4**: Difference calculations
        - **Level 5**: Multiple operations
        - **Level 6**: Complex analysis
        """)

def get_bar_graph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.bar_graph_difficulty
    
    settings = {
        1: {
            "value_range": (0, 20),
            "num_bars": 4,
            "question_types": ["read_value", "find_highest", "find_lowest"],
            "label": "Simple Reading",
            "color": "🟢",
            "y_max": 25,
            "y_step": 5,
            "allow_decimals": False
        },
        2: {
            "value_range": (0, 50),
            "num_bars": 5,
            "question_types": ["read_value", "find_highest", "find_lowest", "compare_two"],
            "label": "Basic Graphs",
            "color": "🟡",
            "y_max": 60,
            "y_step": 10,
            "allow_decimals": False
        },
        3: {
            "value_range": (0, 100),
            "num_bars": 5,
            "question_types": ["compare_two", "find_difference", "how_many_more"],
            "label": "Comparisons",
            "color": "🟠",
            "y_max": 110,
            "y_step": 10,
            "allow_decimals": False
        },
        4: {
            "value_range": (0, 100),
            "num_bars": 6,
            "question_types": ["find_difference", "find_total", "how_many_between"],
            "label": "Calculations",
            "color": "🔴",
            "y_max": 110,
            "y_step": 10,
            "allow_decimals": False
        },
        5: {
            "value_range": (0, 200),
            "num_bars": 6,
            "question_types": ["find_total", "find_average", "complex_comparison"],
            "label": "Advanced Analysis",
            "color": "🟣",
            "y_max": 220,
            "y_step": 20,
            "allow_decimals": False
        },
        6: {
            "value_range": (0, 1000),
            "num_bars": 7,
            "question_types": ["complex_comparison", "multi_step", "pattern_analysis"],
            "label": "Expert Level",
            "color": "⚫",
            "y_max": 1100,
            "y_step": 100,
            "allow_decimals": True
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_bar_graph_progress():
    """Display current level and progress"""
    settings = get_bar_graph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.bar_graph_difficulty}/6")
    
    with col2:
        st.metric("Question Type", settings['label'])
    
    with col3:
        if st.session_state.bar_graph_total_attempts > 0:
            accuracy = (st.session_state.bar_graph_total_score / st.session_state.bar_graph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.bar_graph_consecutive_correct}")

def generate_bar_graph_data(settings):
    """Generate data for the bar graph based on difficulty"""
    contexts = [
        {
            "title": "Books Read Last Week",
            "x_label": "Day",
            "y_label": "Number of Books",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "unit": "books"
        },
        {
            "title": "Students in Different Classes",
            "x_label": "Class",
            "y_label": "Number of Students",
            "categories": ["Class A", "Class B", "Class C", "Class D", "Class E"],
            "unit": "students"
        },
        {
            "title": "Pets Owned by Students",
            "x_label": "Type of Pet",
            "y_label": "Number of Pets",
            "categories": ["Dogs", "Cats", "Birds", "Fish", "Rabbits"],
            "unit": "pets"
        },
        {
            "title": "Miles Driven Each Day",
            "x_label": "Day",
            "y_label": "Miles",
            "categories": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "unit": "miles"
        },
        {
            "title": "Swimming Team Times",
            "x_label": "Swimmer",
            "y_label": "Time (seconds)",
            "categories": ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan"],
            "unit": "seconds"
        },
        {
            "title": "Kilometers Walked",
            "x_label": "Day",
            "y_label": "Kilometers",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday"],
            "unit": "kilometers"
        },
        {
            "title": "Chess Tournament Wins",
            "x_label": "Player",
            "y_label": "Games Won",
            "categories": ["Alex", "Sarah", "Mike", "Lisa", "Tom"],
            "unit": "games"
        },
        {
            "title": "Lawn Mowers Sold",
            "x_label": "Model",
            "y_label": "Units Sold",
            "categories": ["EcoMow", "PowerCut", "GreenBlade", "TurboTrim"],
            "unit": "mowers"
        },
        {
            "title": "Fruit Sold at Market",
            "x_label": "Fruit",
            "y_label": "Kilograms",
            "categories": ["Apples", "Oranges", "Bananas", "Grapes", "Pears"],
            "unit": "kg"
        },
        {
            "title": "Points Scored in Games",
            "x_label": "Game",
            "y_label": "Points",
            "categories": ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5"],
            "unit": "points"
        }
    ]
    
    # Select context based on difficulty
    context = random.choice(contexts)
    
    # Adjust number of categories based on settings
    categories = context["categories"][:settings["num_bars"]]
    
    # Generate values
    values = []
    min_val, max_val = settings["value_range"]
    
    # Create realistic patterns
    if st.session_state.bar_graph_difficulty <= 2:
        # Random values for easier levels
        for _ in categories:
            val = random.randint(min_val + 5, max_val - 5)
            # Round to step
            val = round(val / settings["y_step"]) * settings["y_step"]
            values.append(val)
    else:
        # More structured patterns for harder levels
        pattern = random.choice(["random", "increasing", "decreasing", "peak", "valley"])
        
        if pattern == "random":
            for _ in categories:
                val = random.randint(min_val + 10, max_val - 10)
                val = round(val / settings["y_step"]) * settings["y_step"]
                values.append(val)
        elif pattern == "increasing":
            start = random.randint(min_val + 10, min_val + 30)
            step = (max_val - start - 20) / len(categories)
            for i in range(len(categories)):
                val = start + int(i * step) + random.randint(-5, 5)
                val = round(val / settings["y_step"]) * settings["y_step"]
                values.append(val)
        elif pattern == "decreasing":
            start = random.randint(max_val - 30, max_val - 10)
            step = (start - min_val - 20) / len(categories)
            for i in range(len(categories)):
                val = start - int(i * step) + random.randint(-5, 5)
                val = round(val / settings["y_step"]) * settings["y_step"]
                values.append(val)
        elif pattern == "peak":
            mid = len(categories) // 2
            peak_val = random.randint(max_val - 20, max_val - 5)
            for i in range(len(categories)):
                if i == mid:
                    val = peak_val
                else:
                    distance = abs(i - mid)
                    val = peak_val - distance * random.randint(10, 20)
                val = max(min_val, round(val / settings["y_step"]) * settings["y_step"])
                values.append(val)
        else:  # valley
            mid = len(categories) // 2
            valley_val = random.randint(min_val + 5, min_val + 20)
            for i in range(len(categories)):
                if i == mid:
                    val = valley_val
                else:
                    distance = abs(i - mid)
                    val = valley_val + distance * random.randint(10, 20)
                val = min(max_val, round(val / settings["y_step"]) * settings["y_step"])
                values.append(val)
    
    return {
        "context": context,
        "categories": categories,
        "values": values
    }

def generate_category_options(correct_answer, all_categories):
    """Generate randomized options for category-based questions"""
    # Start with the correct answer
    options = [correct_answer]
    
    # Get other categories (excluding the correct one)
    other_categories = [cat for cat in all_categories if cat != correct_answer]
    
    # Randomly select 3 other options (or all if less than 3 available)
    num_others = min(3, len(other_categories))
    other_options = random.sample(other_categories, num_others)
    
    options.extend(other_options)
    
    # Ensure we have exactly 4 options if possible
    while len(options) < 4 and len(options) < len(all_categories):
        # Add more categories if available
        remaining = [cat for cat in all_categories if cat not in options]
        if remaining:
            options.append(random.choice(remaining))
    
    # IMPORTANT: Randomize the final order
    random.shuffle(options)
    
    return options

def generate_numerical_options(correct_answer, settings):
    """Generate randomized options for numerical questions"""
    options = [correct_answer]
    
    # Generate plausible wrong answers
    attempts = 0
    while len(options) < 4 and attempts < 20:
        attempts += 1
        
        # Create variations
        if random.random() < 0.5:
            # Add/subtract steps
            offset = random.choice([-2, -1, 1, 2]) * settings["y_step"]
        else:
            # Add/subtract smaller amounts for variety
            offset = random.randint(-30, 30)
            if offset == 0:
                offset = settings["y_step"]
        
        wrong = correct_answer + offset
        
        # Make sure it's positive and different
        wrong = max(0, wrong)
        
        # Round to appropriate precision
        if settings.get("allow_decimals", False):
            wrong = round(wrong, 1)
        else:
            wrong = int(wrong)
        
        # Add if unique
        if wrong not in options:
            options.append(wrong)
    
    # If we still don't have enough options, add some based on common mistakes
    while len(options) < 4:
        if len(options) == 1:
            # Add double and half
            options.append(correct_answer * 2)
            options.append(max(1, correct_answer // 2))
        else:
            # Add random values in range
            min_val, max_val = settings["value_range"]
            wrong = random.randint(min_val, max_val)
            if wrong not in options:
                options.append(wrong)
    
    # Take only 4 options and shuffle
    options = options[:4]
    random.shuffle(options)
    
    return options

def generate_question(data, settings):
    """Generate a question based on the data and difficulty"""
    question_type = random.choice(settings["question_types"])
    categories = data["categories"]
    values = data["values"]
    context = data["context"]
    
    if question_type == "read_value":
        # Simple value reading
        idx = random.randint(0, len(categories) - 1)
        question = f"How many {context['unit']} for {categories[idx]}?"
        correct_answer = values[idx]
        correct_answers = [correct_answer]  # Single answer
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "find_highest":
        # Find the highest bar - handle ties
        max_val = max(values)
        max_indices = [i for i, v in enumerate(values) if v == max_val]
        # ALL categories with max value are correct
        correct_answers = [categories[i] for i in max_indices]
        
        # For display purposes, pick one as the "primary" answer
        correct_answer = correct_answers[0]
        question = f"Which has the most {context['unit']}?"
        options = generate_category_options(correct_answer, categories)
        
    elif question_type == "find_lowest":
        # Find the lowest bar - handle ties
        min_val = min(values)
        min_indices = [i for i, v in enumerate(values) if v == min_val]
        # ALL categories with min value are correct
        correct_answers = [categories[i] for i in min_indices]
        
        # For display purposes, pick one as the "primary" answer
        correct_answer = correct_answers[0]
        question = f"Which has the fewest {context['unit']}?"
        options = generate_category_options(correct_answer, categories)
        
    elif question_type == "compare_two":
        # Compare two specific bars
        idx1, idx2 = random.sample(range(len(categories)), 2)
        if values[idx1] > values[idx2]:
            question = f"How many more {context['unit']} does {categories[idx1]} have than {categories[idx2]}?"
            correct_answer = values[idx1] - values[idx2]
        else:
            question = f"How many more {context['unit']} does {categories[idx2]} have than {categories[idx1]}?"
            correct_answer = values[idx2] - values[idx1]
        correct_answers = [correct_answer]
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "find_difference":
        # Find difference between highest and lowest
        max_val = max(values)
        min_val = min(values)
        question = f"What is the difference between the highest and lowest {context['unit']}?"
        correct_answer = max_val - min_val
        correct_answers = [correct_answer]
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "find_total":
        # Find total of all bars or subset
        if len(categories) <= 4:
            question = f"What is the total number of {context['unit']}?"
            correct_answer = sum(values)
        else:
            # Select 2-3 categories
            num_selected = random.randint(2, 3)
            indices = random.sample(range(len(categories)), num_selected)
            selected_cats = [categories[i] for i in indices]
            selected_vals = [values[i] for i in indices]
            
            if num_selected == 2:
                question = f"What is the total {context['unit']} for {selected_cats[0]} and {selected_cats[1]}?"
            else:
                question = f"What is the total {context['unit']} for {selected_cats[0]}, {selected_cats[1]}, and {selected_cats[2]}?"
            correct_answer = sum(selected_vals)
        correct_answers = [correct_answer]
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "how_many_more":
        # How many more to reach a target
        idx = random.randint(0, len(categories) - 1)
        target = values[idx] + random.randint(1, 5) * settings["y_step"]
        question = f"How many more {context['unit']} would {categories[idx]} need to reach {target}?"
        correct_answer = target - values[idx]
        correct_answers = [correct_answer]
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "how_many_between":
        # Count bars between two values
        threshold1 = random.randint(min(values), max(values) - settings["y_step"])
        threshold2 = threshold1 + random.randint(1, 3) * settings["y_step"]
        count = sum(1 for v in values if threshold1 <= v <= threshold2)
        question = f"How many have between {threshold1} and {threshold2} {context['unit']}?"
        correct_answer = count
        correct_answers = [correct_answer]
        options = [count, count-1 if count > 0 else count+1, count+1, count+2]
        options = list(set([max(0, o) for o in options]))[:4]
        random.shuffle(options)
        
    elif question_type == "find_average":
        # Find average (rounded)
        avg = sum(values) / len(values)
        correct_answer = round(avg / settings["y_step"]) * settings["y_step"]
        correct_answers = [correct_answer]
        question = f"What is the average number of {context['unit']} (rounded to nearest {settings['y_step']})?"
        options = generate_numerical_options(correct_answer, settings)
        
    elif question_type == "complex_comparison":
        # Complex comparisons
        if random.random() < 0.5:
            # Combined vs individual
            idx1, idx2, idx3 = random.sample(range(len(categories)), 3)
            combined = values[idx1] + values[idx2]
            question = f"Is {categories[idx1]} + {categories[idx2]} greater than {categories[idx3]}?"
            correct_answer = "Yes" if combined > values[idx3] else "No"
            correct_answers = [correct_answer]
            options = ["Yes", "No"]
        else:
            # Ratio question
            idx1, idx2 = random.sample(range(len(categories)), 2)
            if values[idx2] > 0 and values[idx1] % values[idx2] == 0:
                ratio = values[idx1] // values[idx2]
                question = f"How many times greater is {categories[idx1]} than {categories[idx2]}?"
                correct_answer = ratio
                correct_answers = [correct_answer]
                options = [ratio, ratio-1 if ratio > 1 else ratio+1, ratio+1, ratio+2]
                random.shuffle(options)
            else:
                # Fall back to difference
                question = f"What is the difference between {categories[idx1]} and {categories[idx2]}?"
                correct_answer = abs(values[idx1] - values[idx2])
                correct_answers = [correct_answer]
                options = generate_numerical_options(correct_answer, settings)
                
    elif question_type == "multi_step":
        # Multi-step problems
        problem_type = random.choice(["double_compare", "percentage", "distribution"])
        
        if problem_type == "double_compare":
            idx1, idx2 = random.sample(range(len(categories)), 2)
            target = values[idx1] * 2
            question = f"If {categories[idx1]} doubles their {context['unit']}, will they have more than {categories[idx2]}?"
            correct_answer = "Yes" if target > values[idx2] else "No"
            correct_answers = [correct_answer]
            options = ["Yes", "No"]
            
        elif problem_type == "percentage":
            idx = random.randint(0, len(categories) - 1)
            total = sum(values)
            if total > 0:
                percentage = round((values[idx] / total) * 100)
                question = f"What percentage of the total {context['unit']} does {categories[idx]} have?"
                correct_answer = percentage
                correct_answers = [correct_answer]
                options = [percentage, percentage-5, percentage+5, percentage+10]
                options = list(set([max(0, min(100, o)) for o in options]))[:4]
                random.shuffle(options)
            else:
                # Fallback
                question = f"How many {context['unit']} does {categories[idx]} have?"
                correct_answer = values[idx]
                correct_answers = [correct_answer]
                options = generate_numerical_options(correct_answer, settings)
                
        else:  # distribution
            avg = sum(values) / len(values)
            above_avg = sum(1 for v in values if v > avg)
            question = f"How many have above average {context['unit']}?"
            correct_answer = above_avg
            correct_answers = [correct_answer]
            options = list(range(max(0, above_avg-1), min(len(categories)+1, above_avg+3)))
            random.shuffle(options)
            
    else:  # pattern_analysis
        # Analyze patterns
        diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
        
        if len(set(diffs)) == 1:  # Constant difference
            question = f"By how much does each bar increase/decrease from the previous?"
            correct_answer = abs(diffs[0])
            correct_answers = [correct_answer]
            options = generate_numerical_options(correct_answer, settings)
        else:
            # Find biggest jump
            max_diff_idx = diffs.index(max(diffs, key=abs))
            question = f"Between which two consecutive items is the biggest change?"
            correct_answer = f"{categories[max_diff_idx]} to {categories[max_diff_idx+1]}"
            correct_answers = [correct_answer]
            # Generate wrong options
            options = [correct_answer]
            for _ in range(3):
                idx = random.randint(0, len(categories)-2)
                opt = f"{categories[idx]} to {categories[idx+1]}"
                if opt not in options:
                    options.append(opt)
            random.shuffle(options)
    
    return {
        "question": question,
        "correct_answer": correct_answer,
        "correct_answers": correct_answers,  # List of all acceptable answers
        "options": options,
        "question_type": question_type
    }

def generate_bar_graph_problem():
    """Generate a new bar graph problem"""
    settings = get_bar_graph_difficulty_settings()
    
    # Generate data
    data = generate_bar_graph_data(settings)
    
    # Generate question
    question_data = generate_question(data, settings)
    
    problem_data = {
        "settings": settings,
        "data": data,
        "question": question_data["question"],
        "correct_answer": question_data["correct_answer"],
        "correct_answers": question_data["correct_answers"],
        "options": question_data["options"],
        "question_type": question_data["question_type"]
    }
    
    st.session_state.current_bar_graph_problem = problem_data
    st.session_state.user_answer = None
    st.session_state.answer_submitted = False
    st.session_state.show_result = False

def display_bar_graph_problem():
    """Display the bar graph problem interface"""
    problem = st.session_state.current_bar_graph_problem
    data = problem["data"]
    context = data["context"]
    
    # Display context
    st.markdown(f"### {context['title']}")
    
    # Create two columns for table and graph
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display data table
        display_data_table(data)
    
    with col2:
        # Display bar graph
        create_bar_graph(data, problem["settings"])
    
    # Display question
    st.markdown("---")
    st.markdown(f"### ❓ {problem['question']}")
    
    # Answer options
    if not st.session_state.answer_submitted:
        if isinstance(problem["correct_answer"], str) and problem["correct_answer"] in ["Yes", "No"]:
            # Yes/No question
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Yes", use_container_width=True, type="primary"):
                    st.session_state.user_answer = "Yes"
                    check_bar_graph_answer()
                    st.rerun()
            with col2:
                if st.button("No", use_container_width=True, type="primary"):
                    st.session_state.user_answer = "No"
                    check_bar_graph_answer()
                    st.rerun()
        else:
            # Multiple choice with proper randomization
            # Use selectbox for category questions, buttons for numerical
            if isinstance(problem["correct_answer"], str) and problem["correct_answer"] not in ["Yes", "No"]:
                # Category-based question - use selectbox
                st.markdown("**Select your answer:**")
                
                # Create a placeholder option
                options_with_placeholder = ["Select an answer..."] + problem["options"]
                
                selected = st.selectbox(
                    "Choose one:",
                    options_with_placeholder,
                    index=0,
                    label_visibility="collapsed"
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Submit Answer", type="primary", use_container_width=True, 
                                disabled=(selected == "Select an answer...")):
                        st.session_state.user_answer = selected
                        check_bar_graph_answer()
                        st.rerun()
            else:
                # Numerical question - use buttons in grid
                st.markdown("**Choose your answer:**")
                cols = st.columns(2)
                for i, option in enumerate(problem["options"]):
                    with cols[i % 2]:
                        # Format numerical options nicely
                        if isinstance(option, (int, float)):
                            if option == int(option):
                                display_text = f"{int(option)}"
                            else:
                                display_text = f"{option:.1f}"
                        else:
                            display_text = str(option)
                        
                        if st.button(
                            display_text, 
                            key=f"option_{i}",
                            use_container_width=True,
                            type="primary"
                        ):
                            st.session_state.user_answer = option
                            check_bar_graph_answer()
                            st.rerun()
    
    # Show feedback
    if st.session_state.show_result:
        display_bar_graph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                generate_bar_graph_problem()
                st.rerun()

def display_data_table(data):
    """Display the data table"""
    context = data["context"]
    
    # Create DataFrame
    df = pd.DataFrame({
        context["x_label"]: data["categories"],
        context["y_label"]: data["values"]
    })
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=min(400, 50 + len(data["categories"]) * 35)
    )

def create_bar_graph(data, settings):
    """Create and display the bar graph"""
    context = data["context"]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create bars
    x_pos = np.arange(len(data["categories"]))
    colors = plt.cm.Set3(np.linspace(0, 1, len(data["categories"])))
    
    bars = ax.bar(x_pos, data["values"], color=colors, edgecolor='black', linewidth=1)
    
    # Customize the plot
    ax.set_xlabel(context["x_label"], fontsize=12)
    ax.set_ylabel(context["y_label"], fontsize=12)
    ax.set_title(context["title"], fontsize=14, fontweight='bold')
    
    # Set x-axis labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(data["categories"], rotation=45 if len(data["categories"]) > 5 else 0, ha='right')
    
    # Set y-axis
    ax.set_ylim(0, settings["y_max"])
    ax.set_yticks(range(0, settings["y_max"] + 1, settings["y_step"]))
    
    # Add grid
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars for easier levels
    if st.session_state.bar_graph_difficulty <= 3:
        for bar, value in zip(bars, data["values"]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + settings["y_step"]/10,
                   f'{int(value)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def check_bar_graph_answer():
    """Check if the answer is correct"""
    problem = st.session_state.current_bar_graph_problem
    
    # Update statistics
    st.session_state.bar_graph_total_attempts += 1
    
    # Check answer - now handles multiple correct answers
    correct_answers = problem.get("correct_answers", [problem["correct_answer"]])
    is_correct = st.session_state.user_answer in correct_answers
    
    if is_correct:
        st.session_state.bar_graph_total_score += 1
        st.session_state.bar_graph_consecutive_correct += 1
        st.session_state.bar_graph_consecutive_wrong = 0
        
        # Check for level up
        if (st.session_state.bar_graph_consecutive_correct >= 3 and 
            st.session_state.bar_graph_difficulty < 6):
            st.session_state.bar_graph_difficulty += 1
            st.session_state.bar_graph_consecutive_correct = 0
    else:
        st.session_state.bar_graph_consecutive_wrong += 1
        st.session_state.bar_graph_consecutive_correct = 0
        
        # Check for level down
        if (st.session_state.bar_graph_consecutive_wrong >= 3 and 
            st.session_state.bar_graph_difficulty > 1):
            st.session_state.bar_graph_difficulty -= 1
            st.session_state.bar_graph_consecutive_wrong = 0
    
    st.session_state.answer_submitted = True
    st.session_state.show_result = True

def display_bar_graph_feedback():
    """Display feedback after answer submission"""
    problem = st.session_state.current_bar_graph_problem
    user_answer = st.session_state.user_answer
    correct_answers = problem.get("correct_answers", [problem["correct_answer"]])
    
    if user_answer in correct_answers:
        st.success("✅ Correct! Well done!")
        
        # If there were multiple correct answers, mention it
        if len(correct_answers) > 1 and problem["question_type"] in ["find_highest", "find_lowest"]:
            tied_answers = ", ".join(correct_answers)
            st.info(f"Note: {tied_answers} all have the same value, so any of these answers would be correct!")
        
        if st.session_state.bar_graph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Amazing! {st.session_state.bar_graph_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.bar_graph_consecutive_correct == 0:
            settings = get_bar_graph_difficulty_settings()
            st.success(f"🎉 Level Up! Now on: {settings['label']}!")
    else:
        # Show all correct answers if there are ties
        if len(correct_answers) > 1:
            correct_text = " or ".join([f"**{ans}**" for ans in correct_answers])
            st.error(f"❌ Not quite. The correct answer is: {correct_text}")
            
            # Explain about ties
            if problem["question_type"] in ["find_highest", "find_lowest"]:
                data = problem["data"]
                context = data["context"]
                
                # Find the tied values
                if problem["question_type"] == "find_highest":
                    target_val = max(data["values"])
                    st.info(f"These all have {target_val} {context['unit']}, which is the highest value.")
                else:
                    target_val = min(data["values"])
                    st.info(f"These all have {target_val} {context['unit']}, which is the lowest value.")
        else:
            st.error(f"❌ Not quite. The correct answer is: **{correct_answers[0]}**")
        
        # Show explanation
        show_explanation(problem)
        
        # Level down message
        if st.session_state.bar_graph_consecutive_wrong == 0:
            settings = get_bar_graph_difficulty_settings()
            st.warning(f"📉 Moving to easier questions: {settings['label']}")

def show_explanation(problem):
    """Show detailed explanation for the answer"""
    with st.expander("📖 See explanation", expanded=True):
        data = problem["data"]
        context = data["context"]
        question_type = problem["question_type"]
        
        if question_type == "read_value":
            st.markdown("**How to read a value from the bar graph:**")
            st.markdown("1. Find the bar for the category mentioned")
            st.markdown("2. Look at the top of the bar")
            st.markdown("3. Follow across to the y-axis to read the value")
            st.markdown(f"4. The scale shows {context['unit']} in steps of {problem['settings']['y_step']}")
            
        elif question_type in ["find_highest", "find_lowest"]:
            st.markdown("**How to find the highest/lowest bar:**")
            st.markdown("1. Look at all the bars")
            st.markdown("2. Compare their heights visually")
            st.markdown("3. The tallest bar has the highest value")
            st.markdown("4. The shortest bar has the lowest value")
            st.markdown("5. **Important**: If multiple bars have the same height, they are all correct!")
            
        elif question_type in ["compare_two", "find_difference"]:
            st.markdown("**How to compare values:**")
            st.markdown("1. Find the values for both bars")
            st.markdown("2. Subtract the smaller from the larger")
            st.markdown("3. The difference tells you 'how many more'")
            
        elif question_type == "find_total":
            st.markdown("**How to find the total:**")
            st.markdown("1. Read the value of each bar mentioned")
            st.markdown("2. Add all the values together")
            st.markdown("3. Check your addition carefully")
            
        elif question_type == "find_average":
            st.markdown("**How to find the average:**")
            st.markdown("1. Add up all the values")
            st.markdown("2. Divide by the number of bars")
            st.markdown("3. Round to the nearest step on the scale")
        
        # Show the specific values involved
        st.markdown("---")
        st.markdown("**Values in this problem:**")
        for cat, val in zip(data["categories"], data["values"]):
            st.markdown(f"- {cat}: {val} {context['unit']}")

def clear_bar_graph_state():
    """Clear all bar graph related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('bar_graph_') or key in ['current_bar_graph_problem', 'user_answer', 
                                                    'answer_submitted', 'show_result']:
            del st.session_state[key]