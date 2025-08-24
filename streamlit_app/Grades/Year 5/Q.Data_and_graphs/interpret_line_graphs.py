import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime

def run():
    """
    Main function to run the Interpret Line Graphs activity.
    Interactive line graph reading with progressive difficulty.
    """
    # Initialize session state
    if "graph_difficulty" not in st.session_state:
        st.session_state.graph_difficulty = 1
        st.session_state.graph_consecutive_correct = 0
        st.session_state.graph_consecutive_wrong = 0
        st.session_state.graph_total_score = 0
        st.session_state.graph_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.selected_answer = None
        st.session_state.user_input = ""
    
    if "current_graph_problem" not in st.session_state:
        generate_graph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📈 Interpret Line Graphs")
    st.markdown("*Read and analyze information from line graphs*")
    st.markdown("---")
    
    # Display progress
    display_graph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_graph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_graph_problem()
    
    # Instructions
    with st.expander("💡 **How to Read Line Graphs**", expanded=False):
        st.markdown("""
        ### Line Graph Reading Tips:
        1. **Read the title** - Understand what the graph shows
        2. **Check axes labels** - X-axis (horizontal) and Y-axis (vertical)
        3. **Follow the line** - Trace from x-value to the line, then to y-value
        4. **Look for patterns** - Increasing, decreasing, peaks, valleys
        
        ### Question Types:
        - **Direct reading**: Find value at specific point
        - **Find specific value**: When did something reach a certain level?
        - **Identify trends**: Highest, lowest, changes
        - **Compare values**: Between different points
        - **Patterns**: Repeated behaviors
        
        ### Difficulty Levels:
        - **Level 1**: Simple graphs, whole numbers, direct reading
        - **Level 2**: More data points, finding specific values
        - **Level 3**: Identifying trends and patterns
        - **Level 4**: Complex patterns, multiple comparisons
        - **Level 5**: Detailed analysis, calculations
        - **Level 6**: Advanced interpretation, predictions
        """)

def get_graph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.graph_difficulty
    
    settings = {
        1: {
            "data_points": 5,
            "question_types": ["direct_read"],
            "value_range": (1, 10),
            "grid": True,
            "label": "Simple Graphs",
            "color": "🟢"
        },
        2: {
            "data_points": 6,
            "question_types": ["direct_read", "find_value"],
            "value_range": (2, 12),
            "grid": True,
            "label": "Basic Reading",
            "color": "🟡"
        },
        3: {
            "data_points": 8,
            "question_types": ["find_value", "highest", "lowest"],
            "value_range": (0, 15),
            "grid": True,
            "label": "Trends & Patterns",
            "color": "🟠"
        },
        4: {
            "data_points": 10,
            "question_types": ["find_value", "compare", "pattern"],
            "value_range": (0, 20),
            "grid": True,
            "label": "Complex Analysis",
            "color": "🔴"
        },
        5: {
            "data_points": 12,
            "question_types": ["calculate", "pattern", "compare"],
            "value_range": (0, 100),
            "grid": True,
            "label": "Detailed Analysis",
            "color": "🟣"
        },
        6: {
            "data_points": 15,
            "question_types": ["complex", "predict", "analyze"],
            "value_range": (0, 200),
            "grid": True,
            "label": "Advanced Graphs",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_graph_progress():
    """Display current level and progress"""
    settings = get_graph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.graph_difficulty}/6")
    
    with col2:
        st.metric("Graph Type", settings['label'])
    
    with col3:
        if st.session_state.graph_total_attempts > 0:
            accuracy = (st.session_state.graph_total_score / st.session_state.graph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.graph_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.graph_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Graph Master")

def generate_graph_data(settings):
    """Generate line graph data based on difficulty"""
    graph_themes = [
        {
            "title": "Games won by the Bradford baseball team",
            "context": "Fans of the Bradford baseball team compared the number of games won by their team each year.",
            "x_label": "Year",
            "y_label": "Games won",
            "x_type": "year",
            "y_unit": "games",
            "color": "#FF4444"
        },
        {
            "title": "U.S. first class postal rate",
            "context": "A stamp collector carefully recorded the postal rates of the stamps in his collection.",
            "x_label": "Year",
            "y_label": "Price (cents)",
            "x_type": "year_historic",
            "y_unit": "cents",
            "color": "#00CED1"
        },
        {
            "title": "Snowball the puppy's weight",
            "context": "During monthly visits to the veterinarian, Snowball's weight was recorded.",
            "x_label": "Month",
            "y_label": "Weight (kg)",
            "x_type": "month",
            "y_unit": "kilograms",
            "color": "#4169E1"
        },
        {
            "title": "Emails Olivia received",
            "context": "Olivia kept a tally of the number of emails she received each day for a week.",
            "x_label": "Day",
            "y_label": "Emails",
            "x_type": "day",
            "y_unit": "emails",
            "color": "#9370DB"
        },
        {
            "title": "Average monthly rainfall in Miami",
            "context": "Meteorology students in Miami recorded the rainfall in their city.",
            "x_label": "Month",
            "y_label": "Rainfall (in)",
            "x_type": "month_subset",
            "y_unit": "inches",
            "color": "#FF8C00"
        },
        {
            "title": "Montana grey wolf population",
            "context": "A team of biologists monitored the number of grey wolves in Montana.",
            "x_label": "Year",
            "y_label": "Wolves",
            "x_type": "year_historic",
            "y_unit": "wolves",
            "color": "#FF8C00"
        },
        {
            "title": "Times Lily was late to school",
            "context": "Lily's parents kept track of the number of times the attendance office called to report that she had been late for school.",
            "x_label": "Month",
            "y_label": "Number of times",
            "x_type": "school_months",
            "y_unit": "times",
            "color": "#FF6347"
        },
        {
            "title": "Olympic medals won by Finland",
            "context": "In a report about the history of the Olympics, Rhianna reported the number of Olympic medals won by several countries, including Finland.",
            "x_label": "Year",
            "y_label": "Medals",
            "x_type": "olympic_years",
            "y_unit": "medals",
            "color": "#00CED1"
        }
    ]
    
    theme = random.choice(graph_themes)
    
    # Generate x-axis values based on type
    if theme["x_type"] == "year":
        start_year = 2016
        x_values = [start_year + i for i in range(settings["data_points"])]
    elif theme["x_type"] == "year_historic":
        if "postal" in theme["title"]:
            x_values = [1950, 1955, 1960, 1965, 1970][:settings["data_points"]]
        elif "wolf" in theme["title"]:
            x_values = [1979, 1980, 1981, 1982, 1983][:settings["data_points"]]
        else:
            start_year = 1990
            x_values = [start_year + i * 5 for i in range(settings["data_points"])]
    elif theme["x_type"] == "olympic_years":
        x_values = [1988, 1992, 1996, 2000, 2004][:settings["data_points"]]
    elif theme["x_type"] == "month":
        months = ["February", "March", "April", "May", "June", "July", "August"]
        x_values = months[:settings["data_points"]]
    elif theme["x_type"] == "month_subset":
        months = ["July", "August", "September", "October", "November"]
        x_values = months[:settings["data_points"]]
    elif theme["x_type"] == "school_months":
        months = ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        x_values = months[:settings["data_points"]]
    elif theme["x_type"] == "day":
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        x_values = days[:settings["data_points"]]
    else:
        x_values = list(range(settings["data_points"]))
    
    # Generate y-values with realistic patterns
    min_val, max_val = settings["value_range"]
    
    # Create different patterns based on theme
    if "baseball" in theme["title"]:
        # Up and down pattern for wins
        y_values = []
        for i in range(len(x_values)):
            if i == 0:
                y_values.append(random.randint(min_val, min_val + 3))
            elif i % 3 == 0:
                y_values.append(random.randint(min_val, min_val + 3))
            elif i % 3 == 1:
                y_values.append(random.randint(max_val - 3, max_val))
            else:
                y_values.append(random.randint(min_val + 2, max_val - 2))
    elif "postal" in theme["title"]:
        # Generally increasing
        y_values = [3, 3, 4, 5, 6][:len(x_values)]
    elif "weight" in theme["title"]:
        # Growth curve
        y_values = []
        base = 1
        for i in range(len(x_values)):
            if i < len(x_values) // 2:
                y_values.append(base + i * 2)
            else:
                y_values.append(y_values[-1] - (i - len(x_values) // 2))
    elif "email" in theme["title"]:
        # Decreasing pattern
        y_values = []
        start = 10
        for i in range(len(x_values)):
            if i < 3:
                y_values.append(start - i)
            else:
                y_values.append(3)
    elif "rainfall" in theme["title"]:
        # Peak in middle
        y_values = [6, 7, 8, 6, 3][:len(x_values)]
    elif "late" in theme["title"]:
        # Variable pattern
        patterns = [
            [7, 3, 1, 0, 3, 10, 5, 3, 8, 5],
            [5, 2, 0, 1, 4, 9, 3, 2, 7, 4],
            [8, 4, 2, 0, 2, 10, 6, 4, 9, 6]
        ]
        y_values = random.choice(patterns)[:len(x_values)]
    elif "medals" in theme["title"]:
        # Finland Olympics pattern
        y_values = [4, 5, 4, 4, 2][:len(x_values)]
    else:
        # Random pattern
        y_values = [random.randint(min_val, max_val) for _ in x_values]
    
    return {
        "theme": theme,
        "x_values": x_values,
        "y_values": y_values
    }

def generate_question(data, settings):
    """Generate a question based on the graph data"""
    question_type = random.choice(settings["question_types"])
    theme = data["theme"]
    x_values = data["x_values"]
    y_values = data["y_values"]
    
    if question_type == "direct_read":
        # Direct reading question
        idx = random.randint(0, len(x_values) - 1)
        x_val = x_values[idx]
        y_val = y_values[idx]
        
        if theme["x_type"] in ["year", "year_historic", "olympic_years"]:
            question = f"How many {theme['y_unit']} did the {theme['title'].lower().replace('games won by the ', '').replace('olympic medals won by ', '')} win in {x_val}?"
        elif theme["x_type"] in ["month", "month_subset", "school_months"]:
            if "weight" in theme["title"]:
                question = f"How much did Snowball weigh in {x_val}?"
            elif "late" in theme["title"]:
                # Find ALL occurrences of this value
                all_occurrences = [(i, x_values[i]) for i in range(len(y_values)) if y_values[i] == y_val]
                
                if len(all_occurrences) > 1:
                    # Multiple occurrences - pick one randomly
                    selected_idx, selected_x = random.choice(all_occurrences)
                    question = f"In which month was Lily late to school exactly {y_val} times?"
                    correct_answer = selected_x
                else:
                    question = f"In which month was Lily late to school exactly {y_val} times?"
                    correct_answer = x_val
                
                answer_type = "choice"
                options = random.sample(x_values, min(4, len(x_values)))
                if correct_answer not in options:
                    options[0] = correct_answer
                random.shuffle(options)
                return {
                    "question": question,
                    "correct_answer": correct_answer,
                    "answer_type": answer_type,
                    "options": options,
                    "target_value": y_val,
                    "target_x": correct_answer
                }
            else:
                question = f"What was the {theme['y_label'].lower()} in {x_val}?"
        else:  # days
            # Find ALL occurrences of this value for emails
            all_occurrences = [(i, x_values[i]) for i in range(len(y_values)) if y_values[i] == y_val]
            
            if len(all_occurrences) > 1:
                # Multiple occurrences - pick one randomly
                selected_idx, selected_x = random.choice(all_occurrences)
                question = f"On which day did Olivia receive {y_val} emails?"
                correct_answer = selected_x
            else:
                question = f"On which day did Olivia receive {y_val} emails?"
                correct_answer = x_val
            
            answer_type = "choice"
            options = random.sample(x_values, min(4, len(x_values)))
            if correct_answer not in options:
                options[0] = correct_answer
            random.shuffle(options)
            return {
                "question": question,
                "correct_answer": correct_answer,
                "answer_type": answer_type,
                "options": options,
                "target_value": y_val,
                "target_x": correct_answer
            }
        
        correct_answer = str(y_val)
        answer_type = "number"
        
    elif question_type == "find_value":
        # Find when a specific value was reached
        # Get ALL occurrences of each value
        unique_values = list(set(y_values))
        
        # Choose a value that exists
        target_value = random.choice(unique_values)
        
        # Find ALL indices where this value occurs
        all_indices = [i for i, v in enumerate(y_values) if v == target_value]
        
        # Randomly select one of the occurrences
        selected_idx = random.choice(all_indices)
        x_val = x_values[selected_idx]
        
        if "postal" in theme["title"]:
            question = f"In which year did the postal rate reach {target_value} cents?"
        elif "wolf" in theme["title"]:
            if target_value == 1:
                question = f"In which year did 1 grey wolf live in Montana?"
            else:
                question = f"In which year did {target_value} grey wolves live in Montana?"
        elif "rainfall" in theme["title"]:
            question = f"In which month is the average rainfall {target_value} inches?"
        elif "medals" in theme["title"]:
            question = f"In which year on the graph did Finland win {target_value} medals?"
        else:
            question = f"When did the value reach {target_value}?"
        
        correct_answer = str(x_val)
        answer_type = "choice"
        options = random.sample([str(x) for x in x_values], min(4, len(x_values)))
        if correct_answer not in options:
            options[0] = correct_answer
        random.shuffle(options)
        
        return {
            "question": question,
            "correct_answer": correct_answer,
            "answer_type": answer_type,
            "options": options,
            "target_value": target_value,
            "target_x": x_val
        }
        
    elif question_type == "highest":
        # Find highest value
        max_val = max(y_values)
        # Get ALL indices with max value
        max_indices = [i for i, v in enumerate(y_values) if v == max_val]
        # Randomly select one
        max_idx = random.choice(max_indices)
        
        question = f"In which {theme['x_label'].lower()} was the {theme['y_label'].lower()} highest?"
        correct_answer = str(x_values[max_idx])
        answer_type = "choice"
        options = random.sample([str(x) for x in x_values], min(4, len(x_values)))
        if correct_answer not in options:
            options[0] = correct_answer
        random.shuffle(options)
        
    elif question_type == "lowest":
        # Find lowest value
        min_val = min(y_values)
        # Get ALL indices with min value
        min_indices = [i for i, v in enumerate(y_values) if v == min_val]
        # Randomly select one
        min_idx = random.choice(min_indices)
        
        question = f"In which {theme['x_label'].lower()} was the {theme['y_label'].lower()} lowest?"
        correct_answer = str(x_values[min_idx])
        answer_type = "choice"
        options = random.sample([str(x) for x in x_values], min(4, len(x_values)))
        if correct_answer not in options:
            options[0] = correct_answer
        random.shuffle(options)
        
    else:  # compare, pattern, complex
        # Comparison question
        idx1, idx2 = random.sample(range(len(x_values)), 2)
        diff = abs(y_values[idx1] - y_values[idx2])
        
        question = f"What is the difference in {theme['y_unit']} between {x_values[idx1]} and {x_values[idx2]}?"
        correct_answer = str(diff)
        answer_type = "number"
        options = None
        
        return {
            "question": question,
            "correct_answer": correct_answer,
            "answer_type": answer_type,
            "options": options,
            "compare_indices": (idx1, idx2),
            "compare_values": (y_values[idx1], y_values[idx2])
        }
    
    return {
        "question": question,
        "correct_answer": correct_answer,
        "answer_type": answer_type,
        "options": options if answer_type == "choice" else None
    }

def generate_graph_problem():
    """Generate a new line graph interpretation problem"""
    settings = get_graph_difficulty_settings()
    
    # Generate graph data
    data = generate_graph_data(settings)
    
    # Generate question
    question_data = generate_question(data, settings)
    
    problem_data = {
        "settings": settings,
        "data": data,
        "question": f"{data['theme']['context']}\n\n{question_data['question']}",
        "correct_answer": question_data["correct_answer"],
        "answer_type": question_data["answer_type"],
        "options": question_data["options"],
        "question_details": question_data  # Store full question details for feedback
    }
    
    st.session_state.current_graph_problem = problem_data
    st.session_state.show_result = False
    st.session_state.selected_answer = None
    st.session_state.user_input = ""

def display_graph_problem():
    """Display the graph and question interface"""
    problem = st.session_state.current_graph_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Display the graph
    create_line_graph(problem)
    
    # Answer interface
    st.markdown("---")
    
    if problem["answer_type"] == "choice":
        # Multiple choice buttons
        st.markdown("### Select your answer:")
        
        # Create button grid
        cols = st.columns(min(len(problem["options"]), 4))
        
        if not st.session_state.show_result:
            for i, option in enumerate(problem["options"]):
                with cols[i % len(cols)]:
                    if st.button(
                        option,
                        key=f"option_{i}",
                        use_container_width=True,
                        type="primary" if st.session_state.selected_answer == option else "secondary"
                    ):
                        st.session_state.selected_answer = option
                        st.rerun()
            
            # Submit button
            if st.button("Submit", type="primary", disabled=st.session_state.selected_answer is None):
                check_graph_answer()
                st.rerun()
        else:
            # Show results
            for i, option in enumerate(problem["options"]):
                with cols[i % len(cols)]:
                    if option == st.session_state.selected_answer:
                        if option == problem["correct_answer"]:
                            st.success(f"✅ {option}")
                        else:
                            st.error(f"❌ {option}")
                    elif option == problem["correct_answer"]:
                        st.info(f"✓ {option}")
                    else:
                        st.caption(option)
    
    else:  # number input
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if not st.session_state.show_result:
                # Get the unit from the data
                unit = problem['data']['theme']['y_unit']
                
                user_input = st.text_input(
                    f"Enter your answer ({unit}):",
                    value=st.session_state.user_input,
                    key="number_input"
                )
                st.session_state.user_input = user_input
                
                if st.button("Submit", type="primary", use_container_width=True):
                    if user_input:
                        try:
                            int(user_input)
                            st.session_state.selected_answer = user_input
                            check_graph_answer()
                            st.rerun()
                        except ValueError:
                            st.error("Please enter a valid number")
                    else:
                        st.error("Please enter an answer")
            else:
                # Show result
                unit = problem['data']['theme']['y_unit']
                st.markdown("Your answer:")
                if st.session_state.selected_answer == problem["correct_answer"]:
                    st.success(f"✅ {st.session_state.selected_answer} {unit}")
                else:
                    st.error(f"❌ {st.session_state.selected_answer} {unit}")
                    st.info(f"✓ Correct: {problem['correct_answer']} {unit}")
    
    # Show feedback
    if st.session_state.show_result:
        display_graph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                generate_graph_problem()
                st.rerun()

def create_line_graph(problem):
    """Create and display the line graph"""
    data = problem['data']
    theme = data['theme']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Convert x_values for plotting
    if theme["x_type"] in ["month", "month_subset", "school_months", "day"]:
        x_positions = range(len(data['x_values']))
        ax.plot(x_positions, data['y_values'], 
                color=theme['color'], linewidth=2, marker='o', markersize=8)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(data['x_values'], rotation=45, ha='right')
    else:
        ax.plot(data['x_values'], data['y_values'], 
                color=theme['color'], linewidth=2, marker='o', markersize=8)
    
    # Set labels and title
    ax.set_xlabel(theme['x_label'], fontsize=12)
    ax.set_ylabel(theme['y_label'], fontsize=12)
    ax.set_title(theme['title'], fontsize=14, fontweight='bold', pad=20)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='-')
    
    # Set y-axis to start at 0 and add some padding
    y_min, y_max = 0, max(data['y_values']) * 1.1
    ax.set_ylim(y_min, y_max)
    
    # Add value labels on points if difficulty is low
    if st.session_state.graph_difficulty <= 2:
        if theme["x_type"] in ["month", "month_subset", "school_months", "day"]:
            for i, (x, y) in enumerate(zip(x_positions, data['y_values'])):
                ax.text(x, y + 0.5, str(y), ha='center', va='bottom', fontsize=10)
        else:
            for x, y in zip(data['x_values'], data['y_values']):
                ax.text(x, y + 0.5, str(y), ha='center', va='bottom', fontsize=10)
    
    # Highlight answer point if showing result
    if st.session_state.show_result:
        details = problem.get("question_details", {})
        
        # Highlight based on question type
        if "target_value" in details and "target_x" in details:
            # Find the point for "find value" or "direct read" questions
            target_x = details["target_x"]
            target_y = details["target_value"]
            
            if theme["x_type"] in ["month", "month_subset", "school_months", "day"]:
                # Find x position
                if target_x in data['x_values']:
                    x_pos = data['x_values'].index(target_x)
                    ax.plot(x_pos, target_y, 'go', markersize=15, alpha=0.5)
                    ax.annotate(f'({target_x}, {target_y})', 
                              xy=(x_pos, target_y), 
                              xytext=(x_pos, target_y + 1),
                              ha='center', fontsize=10,
                              bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen'))
            else:
                ax.plot(target_x, target_y, 'go', markersize=15, alpha=0.5)
                ax.annotate(f'({target_x}, {target_y})', 
                          xy=(target_x, target_y), 
                          xytext=(target_x, target_y + 1),
                          ha='center', fontsize=10,
                          bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen'))
        
        elif "compare_indices" in details:
            # Highlight comparison points
            idx1, idx2 = details["compare_indices"]
            val1, val2 = details["compare_values"]
            
            if theme["x_type"] in ["month", "month_subset", "school_months", "day"]:
                ax.plot([idx1, idx2], [val1, val2], 'ro', markersize=12, alpha=0.5)
                # Draw connecting line
                ax.plot([idx1, idx2], [val1, val2], 'r--', alpha=0.3, linewidth=2)
            else:
                x1, x2 = data['x_values'][idx1], data['x_values'][idx2]
                ax.plot([x1, x2], [val1, val2], 'ro', markersize=12, alpha=0.5)
                # Draw connecting line
                ax.plot([x1, x2], [val1, val2], 'r--', alpha=0.3, linewidth=2)
    
    plt.tight_layout()
    st.pyplot(fig)

def check_graph_answer():
    """Check if the submitted answer is correct"""
    problem = st.session_state.current_graph_problem
    selected = st.session_state.selected_answer
    correct = problem['correct_answer']
    
    # Update statistics
    st.session_state.graph_total_attempts += 1
    
    if str(selected) == str(correct):
        st.session_state.graph_total_score += 1
        st.session_state.graph_consecutive_correct += 1
        st.session_state.graph_consecutive_wrong = 0
        st.session_state.current_graph_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.graph_consecutive_correct >= 3 and 
            st.session_state.graph_difficulty < 6):
            st.session_state.graph_difficulty += 1
            st.session_state.graph_consecutive_correct = 0
    else:
        st.session_state.graph_consecutive_wrong += 1
        st.session_state.graph_consecutive_correct = 0
        st.session_state.current_graph_problem["result"] = "incorrect"
        
        # Check for level down
        if (st.session_state.graph_consecutive_wrong >= 3 and 
            st.session_state.graph_difficulty > 1):
            st.session_state.graph_difficulty -= 1
            st.session_state.graph_consecutive_wrong = 0
    
    st.session_state.show_result = True

def display_graph_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_graph_problem
    
    if problem.get("result") == "correct":
        st.success("✅ Excellent! You read the graph correctly!")
        
        if st.session_state.graph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Great graph reading! {st.session_state.graph_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.graph_consecutive_correct == 0:  # Just leveled up
            st.success(f"🎉 Level Up! Now working with: {get_graph_difficulty_settings()['label']}!")
    else:
        st.error("❌ Not quite right. Check the graph again.")
        
        # Provide step-by-step explanation
        with st.expander("📈 See step-by-step solution"):
            data = problem['data']
            theme = data['theme']
            details = problem.get("question_details", {})
            
            st.markdown("### Step-by-Step Solution:")
            
            if problem["answer_type"] == "number":
                if "compare_indices" in details:
                    # Comparison question
                    idx1, idx2 = details["compare_indices"]
                    val1, val2 = details["compare_values"]
                    x1, x2 = data['x_values'][idx1], data['x_values'][idx2]
                    
                    st.markdown(f"**Step 1:** Find the value for {x1}")
                    st.markdown(f"- Look at {x1} on the x-axis")
                    st.markdown(f"- Go up to the line")
                    st.markdown(f"- Read the y-value: **{val1} {theme['y_unit']}**")
                    
                    st.markdown(f"\n**Step 2:** Find the value for {x2}")
                    st.markdown(f"- Look at {x2} on the x-axis")
                    st.markdown(f"- Go up to the line")
                    st.markdown(f"- Read the y-value: **{val2} {theme['y_unit']}**")
                    
                    st.markdown(f"\n**Step 3:** Calculate the difference")
                    st.markdown(f"- |{val1} - {val2}| = **{abs(val1 - val2)}**")
                    
                else:
                    # Direct reading
                    st.markdown("**Step 1:** Find the x-value on the horizontal axis")
                    st.markdown("**Step 2:** Move straight up to the line")
                    st.markdown("**Step 3:** Move left to read the y-value on the vertical axis")
                    st.markdown(f"**Answer:** {problem['correct_answer']} {theme['y_unit']}")
            
            else:  # Multiple choice
                if "target_value" in details:
                    target_val = details["target_value"]
                    target_x = details["target_x"]
                    
                    st.markdown(f"**Step 1:** Find where the line reaches {target_val} on the y-axis")
                    st.markdown(f"- Look for {target_val} on the vertical axis")
                    st.markdown(f"- Move right until you hit the line")
                    st.markdown(f"- Move down to read the x-value")
                    
                    # Show all occurrences
                    all_occurrences = []
                    for i, y in enumerate(data['y_values']):
                        if y == target_val:
                            all_occurrences.append(data['x_values'][i])
                    
                    if len(all_occurrences) > 1:
                        st.markdown(f"\n**Note:** The value {target_val} appears at multiple points:")
                        for x in all_occurrences:
                            if str(x) == str(target_x):
                                st.markdown(f"- **{x}** ✓ (correct answer)")
                            else:
                                st.markdown(f"- {x}")
                    else:
                        st.markdown(f"\n**Answer:** {target_x}")
                else:
                    # Highest/lowest
                    st.markdown("**Step 1:** Look at all points on the line")
                    st.markdown("**Step 2:** Find the highest/lowest point")
                    st.markdown("**Step 3:** Read the x-value for that point")
                    st.markdown(f"**Answer:** {problem['correct_answer']}")
            
            st.info("""
            💡 **Graph Reading Tips:**
            - Always start from the axis mentioned in the question
            - Use the grid lines to help you read values accurately
            - Double-check by tracing your path on the graph
            """)
        
        # Level down message
        if st.session_state.graph_consecutive_wrong == 0:  # Just leveled down
            st.warning(f"📉 Moving to easier graphs: {get_graph_difficulty_settings()['label']}")

def clear_graph_state():
    """Clear all graph-related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('graph_') or key in ['current_graph_problem', 'show_result', 'selected_answer', 'user_input']:
            del st.session_state[key]