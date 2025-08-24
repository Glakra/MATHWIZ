import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run():
    """
    Main function to run the Objects on a Coordinate Plane activity.
    This gets called when the subtopic is loaded from the main menu.
    """
    # Initialize session state
    if "coord_difficulty" not in st.session_state:
        st.session_state.coord_difficulty = 1  # Start at level 1
        st.session_state.coord_consecutive_correct = 0
        st.session_state.coord_consecutive_wrong = 0
        st.session_state.coord_total_score = 0
        st.session_state.coord_total_attempts = 0
    
    if "current_problem" not in st.session_state:
        generate_new_problem()
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > P. Coordinate plane**")
    st.title("📍 Objects on a Coordinate Plane")
    st.markdown("*Identify coordinates of shapes on a grid*")
    st.markdown("---")
    
    # Display current level and progress
    display_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            # Clear session state for this activity
            for key in list(st.session_state.keys()):
                if key.startswith('coord_'):
                    del st.session_state[key]
            if "current_problem" in st.session_state:
                del st.session_state.current_problem
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_coordinate_problem()
    
    # Instructions
    with st.expander("💡 **How to Read Coordinates**", expanded=False):
        st.markdown("""
        ### Remember:
        - **First number (x-coordinate)**: How far to go **right** (positive) or **left** (negative) from 0
        - **Second number (y-coordinate)**: How far to go **up** (positive) or **down** (negative) from 0
        - Coordinates are written as **(x, y)**
        
        ### Examples:
        - **(3, 5)**: 3 units right, 5 units up
        - **(-2, 4)**: 2 units left, 4 units up
        - **(0, -3)**: Stay at center horizontally, 3 units down
        
        ### Question Types:
        - **Find coordinates**: What are the coordinates of a shape?
        - **Find shape**: Which shape is at given coordinates?
        - **Multiple shapes**: Identify specific shapes among many
        
        ### Difficulty Levels:
        - **Level 1**: Small grid (0-5), single shape
        - **Level 2**: Standard grid (0-10), 1-2 shapes
        - **Level 3**: Large grid (0-20), 2-3 shapes
        - **Level 4**: Grid with negatives (-5 to 5)
        - **Level 5**: Larger negative grid (-10 to 10)
        - **Level 6**: Decimal coordinates with multiple shapes
        """)

def get_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty_settings = {
        1: {
            "min_coord": 0,
            "max_coord": 5,
            "grid_size": 5,
            "use_decimals": False,
            "num_shapes": 1,
            "input_type": "multiple_choice",
            "label": "Beginner (0-5)",
            "color": "🟢"
        },
        2: {
            "min_coord": 0,
            "max_coord": 10,
            "grid_size": 10,
            "use_decimals": False,
            "num_shapes": random.randint(1, 2),
            "input_type": random.choice(["multiple_choice", "text_input"]),
            "label": "Basic (0-10)",
            "color": "🟡"
        },
        3: {
            "min_coord": 0,
            "max_coord": 20,
            "grid_size": 20,
            "use_decimals": False,
            "num_shapes": random.randint(2, 3),
            "input_type": random.choice(["multiple_choice", "text_input"]),
            "label": "Intermediate (0-20)",
            "color": "🟠"
        },
        4: {
            "min_coord": -5,
            "max_coord": 5,
            "grid_size": 10,
            "use_decimals": False,
            "num_shapes": random.randint(1, 3),
            "input_type": "text_input",
            "label": "Advanced (-5 to 5)",
            "color": "🔴"
        },
        5: {
            "min_coord": -10,
            "max_coord": 10,
            "grid_size": 20,
            "use_decimals": False,
            "num_shapes": random.randint(2, 4),
            "input_type": "text_input",
            "label": "Expert (-10 to 10)",
            "color": "🟣"
        },
        6: {
            "min_coord": 0,
            "max_coord": 10,
            "grid_size": 10,
            "use_decimals": True,
            "num_shapes": random.randint(2, 4),
            "input_type": "text_input",
            "label": "Master (decimals + multiple)",
            "color": "⚫"
        }
    }
    return difficulty_settings.get(st.session_state.coord_difficulty, difficulty_settings[1])

def display_progress():
    """Display current level and progress"""
    settings = get_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.coord_difficulty}/6")
    
    with col2:
        st.metric("Difficulty", settings['label'])
    
    with col3:
        if st.session_state.coord_total_attempts > 0:
            accuracy = (st.session_state.coord_total_score / st.session_state.coord_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.coord_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.coord_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Master Level")

def generate_new_problem():
    """Generate a new coordinate plane problem based on difficulty"""
    settings = get_difficulty_settings()
    
    # Shape types
    shape_types = [
        {"name": "circle", "symbol": "●", "color": "blue", "matplotlib_color": "#2196F3"},
        {"name": "triangle", "symbol": "▲", "color": "green", "matplotlib_color": "#4CAF50"},
        {"name": "square", "symbol": "■", "color": "red", "matplotlib_color": "#FF5722"},
        {"name": "star", "symbol": "★", "color": "purple", "matplotlib_color": "#9C27B0"},
        {"name": "pentagon", "symbol": "⬟", "color": "orange", "matplotlib_color": "#FF9800"},
        {"name": "hexagon", "symbol": "⬢", "color": "brown", "matplotlib_color": "#795548"},
        {"name": "diamond", "symbol": "♦", "color": "pink", "matplotlib_color": "#E91E63"},
    ]
    
    # Generate multiple shapes without overlap
    shapes = []
    occupied_positions = set()
    
    for i in range(settings["num_shapes"]):
        shape = random.choice(shape_types)
        
        # Find a position that doesn't overlap
        attempts = 0
        while attempts < 50:
            if settings["use_decimals"]:
                x_coord = random.randint(settings["min_coord"] * 2, settings["max_coord"] * 2) / 2
                y_coord = random.randint(settings["min_coord"] * 2, settings["max_coord"] * 2) / 2
            else:
                x_coord = random.randint(settings["min_coord"], settings["max_coord"])
                y_coord = random.randint(settings["min_coord"], settings["max_coord"])
            
            # Check if position is occupied (with buffer zone)
            position_clear = True
            for ox, oy in occupied_positions:
                if abs(ox - x_coord) < 1.5 and abs(oy - y_coord) < 1.5:
                    position_clear = False
                    break
            
            if position_clear:
                occupied_positions.add((x_coord, y_coord))
                shapes.append({
                    "shape": shape.copy(),
                    "x": x_coord,
                    "y": y_coord
                })
                break
            
            attempts += 1
    
    # Determine question type
    question_types = ["find_coordinate", "find_shape", "which_shape_at"]
    if settings["num_shapes"] == 1:
        question_type = "find_coordinate"
    else:
        question_type = random.choice(question_types)
    
    # Select target shape
    target_shape_idx = random.randint(0, len(shapes) - 1)
    target_shape = shapes[target_shape_idx]
    
    # Generate question based on type
    if question_type == "find_coordinate":
        ask_for = random.choice(['x', 'y', 'both'])
        correct_answer = {
            'x': target_shape['x'],
            'y': target_shape['y'],
            'both': (target_shape['x'], target_shape['y'])
        }[ask_for]
    elif question_type == "find_shape":
        ask_for = "shape_at_coord"
        correct_answer = target_shape['shape']['name']
    else:  # which_shape_at
        ask_for = "which_shape"
        correct_answer = target_shape['shape']['name']
    
    # Generate options for multiple choice
    options = []
    if settings["input_type"] == "multiple_choice":
        if question_type == "find_coordinate":
            if ask_for == 'both':
                # Generate coordinate pair options
                options = [(target_shape['x'], target_shape['y'])]
                for shape in shapes:
                    if shape != target_shape:
                        options.append((shape['x'], shape['y']))
                # Add some random options
                while len(options) < 4:
                    rx = random.randint(settings["min_coord"], settings["max_coord"])
                    ry = random.randint(settings["min_coord"], settings["max_coord"])
                    if (rx, ry) not in options:
                        options.append((rx, ry))
            else:
                # Single coordinate options
                coord_value = target_shape['x'] if ask_for == 'x' else target_shape['y']
                other_coord = target_shape['y'] if ask_for == 'x' else target_shape['x']
                options = generate_distractors(coord_value, other_coord, ask_for, settings)
                options = [coord_value] + options
        else:
            # Shape name options
            options = [shape['shape']['name'] for shape in shapes]
            all_shape_names = [st['name'] for st in shape_types]
            while len(options) < 4:
                random_shape = random.choice(all_shape_names)
                if random_shape not in options:
                    options.append(random_shape)
        
        random.shuffle(options)
    
    st.session_state.current_problem = {
        "shapes": shapes,
        "target_shape": target_shape,
        "target_idx": target_shape_idx,
        "question_type": question_type,
        "ask_for": ask_for,
        "options": options,
        "correct_answer": correct_answer,
        "answered": False,
        "settings": settings,
        "input_type": settings["input_type"]
    }

def generate_distractors(correct_answer, other_coord, ask_for, settings):
    """Generate plausible wrong answers"""
    distractors = []
    
    # Common mistakes
    if settings["use_decimals"]:
        # For decimals, include common rounding errors
        distractors.append(int(correct_answer))  # Rounded down
        if correct_answer != int(correct_answer):
            distractors.append(int(correct_answer) + 1)  # Rounded up
    
    # Off-by-one errors
    if correct_answer + 1 <= settings["max_coord"]:
        distractors.append(correct_answer + 1)
    if correct_answer - 1 >= settings["min_coord"]:
        distractors.append(correct_answer - 1)
    
    # Coordinate confusion - use the other coordinate
    if other_coord != correct_answer:
        distractors.append(other_coord)
    
    # Sign errors for negative coordinates
    if settings["min_coord"] < 0 and correct_answer != 0:
        distractors.append(-correct_answer)
    
    # Remove duplicates and limit to 3 distractors
    distractors = list(set(distractors))
    distractors = [d for d in distractors if d != correct_answer]
    
    # If we don't have enough distractors, add random ones
    while len(distractors) < 3:
        if settings["use_decimals"]:
            random_distractor = random.randint(settings["min_coord"] * 2, settings["max_coord"] * 2) / 2
        else:
            random_distractor = random.randint(settings["min_coord"], settings["max_coord"])
        
        if random_distractor != correct_answer and random_distractor not in distractors:
            distractors.append(random_distractor)
    
    return distractors[:3]

def display_coordinate_problem():
    """Display the coordinate plane with shape(s)"""
    problem = st.session_state.current_problem
    target_shape = problem["target_shape"]
    
    # Generate question based on type
    if problem["question_type"] == "find_coordinate":
        shape_info = target_shape['shape']
        if problem["settings"]["num_shapes"] > 1:
            # Add ordinal indicator
            ordinal = ["first", "second", "third", "fourth"][problem["target_idx"]]
            shape_desc = f"the {ordinal} {shape_info['color']} {shape_info['name']}"
        else:
            shape_desc = f"the {shape_info['color']} {shape_info['name']}"
        
        if problem["ask_for"] == "both":
            question = f"### What are the coordinates of {shape_desc} {shape_info['symbol']}?"
        else:
            question = f"### What is the {problem['ask_for']}-coordinate of {shape_desc} {shape_info['symbol']}?"
    elif problem["question_type"] == "find_shape":
        coords = f"({format_coord(target_shape['x'])}, {format_coord(target_shape['y'])})"
        question = f"### Which shape is at coordinates {coords}?"
    else:  # which_shape_at
        question = f"### Which {target_shape['shape']['color']} shape is on the grid?"
    
    st.markdown(question)
    
    # Create coordinate plane with matplotlib
    fig = create_coordinate_plane_plot(problem)
    st.pyplot(fig)
    
    # Handle input based on type
    if not problem.get("answered", False):
        if problem["input_type"] == "multiple_choice":
            display_multiple_choice(problem)
        else:
            display_text_input(problem)
    
    # Show feedback if answered
    if problem.get("answered", False):
        display_feedback(problem)

def display_multiple_choice(problem):
    """Display multiple choice options"""
    st.markdown("**Choose your answer:**")
    
    # Create a 2x2 grid for options
    col1, col2 = st.columns(2)
    
    for i, option in enumerate(problem["options"]):
        col = col1 if i % 2 == 0 else col2
        with col:
            # Format the option display
            if isinstance(option, tuple):
                option_text = f"({format_coord(option[0])}, {format_coord(option[1])})"
            elif isinstance(option, (int, float)):
                option_text = format_coord(option)
            else:
                option_text = option.title()
            
            if st.button(option_text, key=f"option_{i}", use_container_width=True):
                check_answer(option)

def display_text_input(problem):
    """Display text input field(s)"""
    st.markdown("**Enter your answer:**")
    
    if problem["ask_for"] == "both":
        col1, col2 = st.columns(2)
        with col1:
            x_input = st.text_input("x-coordinate:", key="x_input")
        with col2:
            y_input = st.text_input("y-coordinate:", key="y_input")
        
        if st.button("Submit Answer", type="primary", use_container_width=True):
            try:
                x_val = float(x_input) if x_input else None
                y_val = float(y_input) if y_input else None
                if x_val is not None and y_val is not None:
                    check_answer((x_val, y_val))
                else:
                    st.error("Please enter both coordinates.")
            except ValueError:
                st.error("Please enter valid numbers.")
    
    elif problem["question_type"] == "find_coordinate":
        coord_input = st.text_input(f"Enter the {problem['ask_for']}-coordinate:", key="coord_input")
        if st.button("Submit Answer", type="primary", use_container_width=True):
            try:
                coord_val = float(coord_input) if coord_input else None
                if coord_val is not None:
                    check_answer(coord_val)
                else:
                    st.error("Please enter a coordinate.")
            except ValueError:
                st.error("Please enter a valid number.")
    
    else:  # shape name
        shape_input = st.text_input("Enter the shape name:", key="shape_input")
        if st.button("Submit Answer", type="primary", use_container_width=True):
            if shape_input:
                check_answer(shape_input.lower().strip())
            else:
                st.error("Please enter a shape name.")

def display_feedback(problem):
    """Display feedback after answer"""
    target_shape = problem["target_shape"]
    shape_info = target_shape['shape']
    
    if problem.get("correct", False):
        st.success("✅ Excellent! That's correct!")
        
        # Show complete information
        if problem["question_type"] == "find_coordinate":
            st.info(f"The {shape_info['color']} {shape_info['name']} is at ({format_coord(target_shape['x'])}, {format_coord(target_shape['y'])})")
        
        # Show encouragement for streaks
        if st.session_state.coord_consecutive_correct >= 3:
            st.balloons()
            st.info(f"🎉 Amazing streak of {st.session_state.coord_consecutive_correct} correct answers!")
    else:
        st.error("❌ Not quite right.")
        
        # Show correct answer
        if problem["question_type"] == "find_coordinate":
            if problem["ask_for"] == "both":
                st.info(f"The correct coordinates are ({format_coord(target_shape['x'])}, {format_coord(target_shape['y'])})")
            else:
                st.info(f"The correct {problem['ask_for']}-coordinate is {format_coord(problem['correct_answer'])}")
        else:
            st.info(f"The correct answer is: {problem['correct_answer']}")
        
        # Show hint
        with st.expander("💡 Need help understanding?"):
            if problem["question_type"] == "find_coordinate":
                st.markdown("""
                **How to find coordinates:**
                1. Start at the origin (0, 0)
                2. Count right (positive) or left (negative) for the x-coordinate
                3. Count up (positive) or down (negative) for the y-coordinate
                4. Write as (x, y)
                """)
            else:
                st.markdown("""
                **Shape identification tips:**
                - Circle: Round shape ●
                - Triangle: 3 sides ▲
                - Square: 4 equal sides ■
                - Star: Pointed shape ★
                - Pentagon: 5 sides ⬟
                - Hexagon: 6 sides ⬢
                - Diamond: 4 sides in diamond shape ♦
                """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next Problem", type="primary", use_container_width=True):
            generate_new_problem()
            st.rerun()

def format_coord(value):
    """Format coordinate value for display"""
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    elif isinstance(value, float):
        return f"{value:.1f}"
    return str(value)

def create_coordinate_plane_plot(problem):
    """Create matplotlib figure with coordinate plane and shapes"""
    settings = problem["settings"]
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Set up the grid based on difficulty
    margin = 0.5
    ax.set_xlim(settings["min_coord"] - margin, settings["max_coord"] + margin)
    ax.set_ylim(settings["min_coord"] - margin, settings["max_coord"] + margin)
    ax.set_aspect('equal')
    
    # Draw grid
    ax.grid(True, linestyle='-', color='lightgray', alpha=0.7)
    
    # Set up axes
    ax.axhline(y=0, color='black', linewidth=2)
    ax.axvline(x=0, color='black', linewidth=2)
    
    # Remove box
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add axis labels
    ax.set_xlabel('x', fontsize=14, labelpad=10)
    ax.set_ylabel('y', fontsize=14, labelpad=10)
    
    # Set ticks based on grid size
    if settings["grid_size"] <= 10:
        step = 1
    elif settings["grid_size"] <= 20:
        step = 2
    else:
        step = 5
    
    if settings["use_decimals"]:
        # Show decimal ticks
        ticks = np.arange(settings["min_coord"], settings["max_coord"] + 0.5, 0.5)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
    else:
        ax.set_xticks(range(settings["min_coord"], settings["max_coord"] + 1, step))
        ax.set_yticks(range(settings["min_coord"], settings["max_coord"] + 1, step))
    
    # Add arrowheads
    ax.annotate('', xy=(settings["max_coord"] + margin, 0), xytext=(settings["max_coord"] + margin - 0.2, 0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(0, settings["max_coord"] + margin), xytext=(0, settings["max_coord"] + margin - 0.2),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Draw all shapes
    for i, shape_data in enumerate(problem["shapes"]):
        shape = shape_data["shape"]
        x, y = shape_data["x"], shape_data["y"]
        color = shape["matplotlib_color"]
        
        # Highlight target shape if showing feedback
        if problem.get("answered", False) and i == problem["target_idx"]:
            # Add a yellow highlight circle behind the target shape
            highlight = plt.Circle((x, y), 0.5, color='yellow', alpha=0.5, zorder=4)
            ax.add_patch(highlight)
        
        # Adjust shape size based on grid size
        shape_size = 0.3 if settings["grid_size"] <= 10 else 0.5
        
        if shape["name"] == "circle":
            circle = plt.Circle((x, y), shape_size, color=color, zorder=5)
            ax.add_patch(circle)
        
        elif shape["name"] == "square":
            square = plt.Rectangle((x - shape_size, y - shape_size), shape_size * 2, shape_size * 2, 
                                  color=color, zorder=5)
            ax.add_patch(square)
        
        elif shape["name"] == "triangle":
            triangle = patches.Polygon([(x, y + shape_size), (x - shape_size, y - shape_size), 
                                       (x + shape_size, y - shape_size)], 
                                      closed=True, color=color, zorder=5)
            ax.add_patch(triangle)
        
        elif shape["name"] == "star":
            # Create star shape
            angles = np.linspace(0, 2 * np.pi, 10, endpoint=False) - np.pi/2
            radii = np.array([shape_size, shape_size/2] * 5)
            star_x = x + radii * np.cos(angles)
            star_y = y + radii * np.sin(angles)
            star = patches.Polygon(list(zip(star_x, star_y)), closed=True, color=color, zorder=5)
            ax.add_patch(star)
        
        elif shape["name"] == "pentagon":
            # Create pentagon shape
            angles = np.linspace(0, 2 * np.pi, 5, endpoint=False) - np.pi/2
            pent_x = x + shape_size * np.cos(angles)
            pent_y = y + shape_size * np.sin(angles)
            pentagon = patches.Polygon(list(zip(pent_x, pent_y)), closed=True, color=color, zorder=5)
            ax.add_patch(pentagon)
        
        elif shape["name"] == "hexagon":
            # Create hexagon shape
            angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
            hex_x = x + shape_size * np.cos(angles)
            hex_y = y + shape_size * np.sin(angles)
            hexagon = patches.Polygon(list(zip(hex_x, hex_y)), closed=True, color=color, zorder=5)
            ax.add_patch(hexagon)
        
        elif shape["name"] == "diamond":
            # Create diamond shape
            diamond = patches.Polygon([(x, y + shape_size), (x + shape_size, y), 
                                      (x, y - shape_size), (x - shape_size, y)], 
                                     closed=True, color=color, zorder=5)
            ax.add_patch(diamond)
        
        # Add number labels for multiple shapes
        if settings["num_shapes"] > 1 and not problem.get("answered", False):
            ax.text(x, y - shape_size - 0.3, str(i + 1), 
                   fontsize=10, ha='center', va='top', weight='bold')
    
    plt.tight_layout()
    return fig

def check_answer(user_answer):
    """Check if the answer is correct and update difficulty"""
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    st.session_state.coord_total_attempts += 1
    
    # Check answer based on type
    is_correct = False
    if isinstance(correct_answer, tuple) and isinstance(user_answer, tuple):
        # Compare coordinate pairs
        is_correct = (abs(user_answer[0] - correct_answer[0]) < 0.01 and 
                     abs(user_answer[1] - correct_answer[1]) < 0.01)
    elif isinstance(correct_answer, (int, float)) and isinstance(user_answer, (int, float)):
        # Compare single coordinates
        is_correct = abs(user_answer - correct_answer) < 0.01
    elif isinstance(correct_answer, str) and isinstance(user_answer, str):
        # Compare shape names
        is_correct = user_answer.lower() == correct_answer.lower()
    
    if is_correct:
        st.session_state.coord_total_score += 1
        st.session_state.coord_consecutive_correct += 1
        st.session_state.coord_consecutive_wrong = 0
        problem["correct"] = True
        
        # Check for level up
        if st.session_state.coord_consecutive_correct >= 3 and st.session_state.coord_difficulty < 6:
            st.session_state.coord_difficulty += 1
            st.session_state.coord_consecutive_correct = 0
            st.success(f"🎉 Level Up! You've reached Level {st.session_state.coord_difficulty}!")
    else:
        st.session_state.coord_consecutive_wrong += 1
        st.session_state.coord_consecutive_correct = 0
        problem["correct"] = False
        problem["user_answer"] = user_answer
        
        # Check for level down
        if st.session_state.coord_consecutive_wrong >= 3 and st.session_state.coord_difficulty > 1:
            st.session_state.coord_difficulty -= 1
            st.session_state.coord_consecutive_wrong = 0
            st.warning(f"📉 Difficulty decreased to Level {st.session_state.coord_difficulty}. Keep practicing!")
    
    problem["answered"] = True