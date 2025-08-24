import streamlit as st
import random
import math
import streamlit.components.v1 as components

def run():
    """
    Main function to run the Reflection, Rotation and Translation activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/reflection_rotation_translation.py
    """
    # Initialize session state
    if "transform_difficulty" not in st.session_state:
        st.session_state.transform_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_problems = []  # Track recent problems to avoid repetition
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔄 Reflection, Rotation and Translation")
    st.markdown("*Identify which transformation has been applied to the shape*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (Simple shapes & emojis)",
            2: "Medium (Complex shapes)", 
            3: "Hard (Irregular & tricky)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.transform_difficulty]}")
        progress = (st.session_state.transform_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.transform_difficulty}/3")
    
    with col2:
        if st.session_state.total_attempted > 0:
            accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
        else:
            st.metric("Accuracy", "---")
    
    with col3:
        st.metric("Streak", st.session_state.consecutive_correct)
    
    with col4:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display the transformation problem
    display_transformation_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Three Types of Transformations:
        
        **🔄 Translation (Slide)**
        - Shape moves to a new position
        - Same size, same orientation
        - Like sliding a book across a table
        - Every point moves the same distance and direction
        
        **🪞 Reflection (Flip)**
        - Creates a mirror image
        - Flips across a line (vertical, horizontal, or diagonal)
        - Like seeing yourself in a mirror
        - Orientation changes but size stays the same
        
        **🔃 Rotation (Turn)**
        - Shape turns around a point
        - Common angles: 90°, 180°, 270°
        - Like turning a steering wheel
        - Size stays same, position and orientation change
        
        ### How to Identify:
        
        **Translation Test:**
        - Can you slide the shape without turning or flipping?
        - Are all angles and orientations the same?
        - Did it just move position?
        
        **Reflection Test:**
        - Is it a mirror image?
        - Did it flip over a line?
        - Are left and right (or top and bottom) swapped?
        
        **Rotation Test:**
        - Did the shape turn?
        - Is it at a different angle?
        - Can you rotate it back to the original?
        
        ### Quick Recognition:
        
        📍 **Translation** → Same exact shape, different location
        🪞 **Reflection** → Mirror image, flipped
        🔃 **Rotation** → Turned at an angle
        
        ### Common Angles:
        - **90° rotation** = Quarter turn (↱)
        - **180° rotation** = Half turn (↕)
        - **270° rotation** = Three-quarter turn (↰)
        
        ### Tips:
        - Look at distinctive features (corners, edges, orientation)
        - For emojis, check which way they're facing
        - Imagine moving the shape yourself
        """)

def generate_new_problem():
    """Generate a new transformation problem"""
    difficulty = st.session_state.transform_difficulty
    
    # Define transformation types
    transformations = ["translation", "reflection", "rotation"]
    
    # Choose a random transformation to ask about
    target_transformation = random.choice(transformations)
    
    # Decide whether to use emoji or polygon shape
    use_emoji = random.choice([True, False]) if difficulty <= 2 else random.choice([False, False, True])
    
    if use_emoji:
        shape = generate_emoji_shape(difficulty)
    else:
        shape = generate_polygon_shape(difficulty)
    
    # Generate the three options (one correct, two incorrect)
    if shape["type"] == "emoji":
        options = generate_emoji_transformation_options(shape, target_transformation)
    else:
        options = generate_polygon_transformation_options(shape, target_transformation)
    
    # Store problem data
    st.session_state.problem_data = {
        "original_shape": shape,
        "target_transformation": target_transformation,
        "options": options,
        "correct_answer": next(i for i, opt in enumerate(options) if opt["is_correct"])
    }
    st.session_state.current_problem = f"{shape['name']}_{target_transformation}"

def generate_emoji_shape(difficulty):
    """Generate emoji-based shapes for transformations"""
    if difficulty == 1:  # Easy - simple emojis
        emojis = [
            {"name": "arrow_right", "emoji": "➡️", "has_direction": True},
            {"name": "arrow_up", "emoji": "⬆️", "has_direction": True},
            {"name": "triangle", "emoji": "🔺", "has_direction": True},
            {"name": "diamond", "emoji": "🔷", "has_direction": False},
            {"name": "heart", "emoji": "❤️", "has_direction": True},
            {"name": "star", "emoji": "⭐", "has_direction": False},
            {"name": "house", "emoji": "🏠", "has_direction": True},
            {"name": "tree", "emoji": "🌳", "has_direction": True},
            {"name": "car", "emoji": "🚗", "has_direction": True},
            {"name": "airplane", "emoji": "✈️", "has_direction": True},
            {"name": "rocket", "emoji": "🚀", "has_direction": True},
            {"name": "fish", "emoji": "🐠", "has_direction": True},
            {"name": "butterfly", "emoji": "🦋", "has_direction": True},
            {"name": "flower", "emoji": "🌸", "has_direction": False},
            {"name": "sun", "emoji": "☀️", "has_direction": False},
            {"name": "moon", "emoji": "🌙", "has_direction": True}
        ]
    elif difficulty == 2:  # Medium - more complex emojis
        emojis = [
            {"name": "hexagon", "emoji": "⬡", "has_direction": False},
            {"name": "octagon", "emoji": "🛑", "has_direction": False},
            {"name": "bird", "emoji": "🦅", "has_direction": True},
            {"name": "cat", "emoji": "🐈", "has_direction": True},
            {"name": "dog", "emoji": "🐕", "has_direction": True},
            {"name": "horse", "emoji": "🐎", "has_direction": True},
            {"name": "bicycle", "emoji": "🚲", "has_direction": True},
            {"name": "ship", "emoji": "🚢", "has_direction": True},
            {"name": "helicopter", "emoji": "🚁", "has_direction": True},
            {"name": "crab", "emoji": "🦀", "has_direction": True},
            {"name": "lobster", "emoji": "🦞", "has_direction": True},
            {"name": "snail", "emoji": "🐌", "has_direction": True},
            {"name": "turtle", "emoji": "🐢", "has_direction": True},
            {"name": "penguin", "emoji": "🐧", "has_direction": True},
            {"name": "whale", "emoji": "🐋", "has_direction": True}
        ]
    else:  # Hard - complex/abstract emojis
        emojis = [
            {"name": "spiral", "emoji": "🌀", "has_direction": True},
            {"name": "yin_yang", "emoji": "☯️", "has_direction": True},
            {"name": "snowflake", "emoji": "❄️", "has_direction": False},
            {"name": "gear", "emoji": "⚙️", "has_direction": False},
            {"name": "atom", "emoji": "⚛️", "has_direction": False},
            {"name": "compass", "emoji": "🧭", "has_direction": True},
            {"name": "anchor", "emoji": "⚓", "has_direction": True},
            {"name": "key", "emoji": "🗝️", "has_direction": True},
            {"name": "scissors", "emoji": "✂️", "has_direction": True},
            {"name": "hammer", "emoji": "🔨", "has_direction": True},
            {"name": "wrench", "emoji": "🔧", "has_direction": True},
            {"name": "microscope", "emoji": "🔬", "has_direction": True},
            {"name": "telescope", "emoji": "🔭", "has_direction": True},
            {"name": "hourglass", "emoji": "⏳", "has_direction": True}
        ]
    
    selected = random.choice(emojis)
    return {
        "name": selected["name"],
        "emoji": selected["emoji"],
        "type": "emoji",
        "has_direction": selected["has_direction"],
        "color": None
    }

def generate_polygon_shape(difficulty):
    """Generate polygon-based shapes for transformations"""
    if difficulty == 1:  # Easy - simple shapes
        shapes = [
            {
                "name": "right_triangle",
                "points": [(1, 1), (4, 1), (1, 3)],
                "color": "#4FC3F7"
            },
            {
                "name": "square",
                "points": [(1, 1), (3, 1), (3, 3), (1, 3)],
                "color": "#9C27B0"
            },
            {
                "name": "L_shape",
                "points": [(1, 1), (3, 1), (3, 2), (2, 2), (2, 4), (1, 4)],
                "color": "#4CAF50"
            },
            {
                "name": "rectangle",
                "points": [(1, 1), (4, 1), (4, 2), (1, 2)],
                "color": "#FF9800"
            },
            {
                "name": "diamond",
                "points": [(2.5, 1), (4, 2.5), (2.5, 4), (1, 2.5)],
                "color": "#E91E63"
            },
            {
                "name": "arrow_right",
                "points": [(1, 2), (3, 2), (3, 1), (4, 2.5), (3, 4), (3, 3), (1, 3)],
                "color": "#F44336"
            },
            {
                "name": "parallelogram",
                "points": [(1, 1), (3, 1), (4, 3), (2, 3)],
                "color": "#00BCD4"
            },
            {
                "name": "isosceles_triangle",
                "points": [(2.5, 1), (4, 3), (1, 3)],
                "color": "#FF5722"
            },
            {
                "name": "right_angle_L",
                "points": [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)],
                "color": "#8BC34A"
            },
            {
                "name": "small_plus",
                "points": [(2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2)],
                "color": "#FFC107"
            },
            {
                "name": "chevron",
                "points": [(1, 2), (2, 1), (3, 2), (3, 3), (2, 4), (1, 3)],
                "color": "#3F51B5"
            },
            {
                "name": "house",
                "points": [(1, 1), (3, 1), (3, 2), (4, 2), (2.5, 3.5), (1, 2)],
                "color": "#795548"
            }
        ]
    
    elif difficulty == 2:  # Medium - more complex shapes
        shapes = [
            {
                "name": "pentagon",
                "points": [(2, 1), (4, 1), (5, 2.5), (3, 4), (1, 2.5)],
                "color": "#E91E63"
            },
            {
                "name": "T_shape",
                "points": [(1, 3), (1, 4), (4, 4), (4, 3), (3, 3), (3, 1), (2, 1), (2, 3)],
                "color": "#FFC107"
            },
            {
                "name": "trapezoid",
                "points": [(1, 1), (4, 1), (3, 3), (2, 3)],
                "color": "#009688"
            },
            {
                "name": "hexagon",
                "points": [(1, 2), (2, 1), (4, 1), (5, 2), (4, 3), (2, 3)],
                "color": "#3F51B5"
            },
            {
                "name": "complex_arrow",
                "points": [(1, 2.5), (2, 2.5), (2, 1), (4, 3), (2, 5), (2, 3.5), (1, 3.5)],
                "color": "#FF6F00"
            },
            {
                "name": "star_5point",
                "points": [(3, 1), (3.5, 2), (4.5, 2), (3.7, 2.8), (4, 3.8), (3, 3.2), (2, 3.8), (2.3, 2.8), (1.5, 2), (2.5, 2)],
                "color": "#9C27B0"
            },
            {
                "name": "cross",
                "points": [(2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2)],
                "color": "#00BCD4"
            },
            {
                "name": "kite",
                "points": [(2.5, 1), (4, 2), (2.5, 4), (1, 2)],
                "color": "#4CAF50"
            },
            {
                "name": "octagon",
                "points": [(2, 1), (3, 1), (4, 2), (4, 3), (3, 4), (2, 4), (1, 3), (1, 2)],
                "color": "#FF5722"
            },
            {
                "name": "Z_shape",
                "points": [(1, 3), (1, 4), (3, 4), (3, 3), (2, 3), (2, 2), (3, 2), (3, 1), (1, 1), (1, 2), (2, 2), (2, 3)],
                "color": "#CDDC39"
            },
            {
                "name": "lightning_bolt",
                "points": [(2, 1), (3, 2), (2.5, 2), (3.5, 3.5), (2, 3), (2.5, 3), (1.5, 4)],
                "color": "#FFEB3B"
            },
            {
                "name": "bowtie",
                "points": [(1, 1), (2, 2), (1, 3), (3, 3), (4, 2), (3, 1)],
                "color": "#E91E63"
            }
        ]
    
    else:  # Hard - complex and irregular shapes
        shapes = [
            {
                "name": "irregular_pentagon",
                "points": [(1, 1), (4, 1), (5, 2), (3, 4), (1, 3)],
                "color": "#673AB7"
            },
            {
                "name": "complex_L",
                "points": [(1, 1), (4, 1), (4, 2), (2, 2), (2, 4), (3, 4), (3, 3), (1, 3)],
                "color": "#FF6F00"
            },
            {
                "name": "spiral_shape",
                "points": [(2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2)],
                "color": "#1A237E"
            },
            {
                "name": "complex_star",
                "points": [(3, 0.5), (3.3, 1.5), (4.3, 1.5), (3.5, 2.2), (4, 3.2), (3, 2.5), (2, 3.2), (2.5, 2.2), (1.7, 1.5), (2.7, 1.5)],
                "color": "#D32F2F"
            },
            {
                "name": "irregular_hexagon",
                "points": [(1, 1.5), (2, 1), (4, 1), (4.5, 2), (3.5, 3.5), (1.5, 3)],
                "color": "#00E676"
            },
            {
                "name": "abstract_shape",
                "points": [(1, 1), (2, 1.5), (2, 1), (3, 1), (4, 2), (3.5, 3), (4, 4), (2.5, 3.5), (1.5, 4), (1, 3)],
                "color": "#FF9800"
            },
            {
                "name": "double_L",
                "points": [(1, 1), (2, 1), (2, 2), (3, 2), (3, 1), (4, 1), (4, 3), (3, 3), (3, 4), (2, 4), (2, 3), (1, 3)],
                "color": "#9C27B0"
            },
            {
                "name": "maze_shape",
                "points": [(1, 1), (3, 1), (3, 1.5), (2, 1.5), (2, 2.5), (3, 2.5), (3, 2), (4, 2), (4, 3), (2, 3), (2, 3.5), (3, 3.5), (3, 4), (1, 4)],
                "color": "#00BCD4"
            },
            {
                "name": "irregular_octagon",
                "points": [(1.5, 1), (3, 1), (4, 1.5), (4.5, 2.5), (4, 3.5), (2.5, 4), (1.5, 3.5), (1, 2.5)],
                "color": "#4CAF50"
            },
            {
                "name": "complex_polygon",
                "points": [(1, 1), (2, 1), (2.5, 1.5), (3, 1), (3.5, 2), (3, 2.5), (3.5, 3), (2.5, 3.5), (2, 3), (1.5, 3.5), (1, 2.5), (1.5, 2)],
                "color": "#FFC107"
            },
            {
                "name": "jagged_shape",
                "points": [(1, 1), (1.5, 1.5), (1, 2), (1.5, 2.5), (1, 3), (2, 3.5), (3, 3), (3.5, 3.5), (4, 3), (3.5, 2.5), (4, 2), (3.5, 1.5), (4, 1), (3, 1.5), (2, 1)],
                "color": "#E91E63"
            },
            {
                "name": "gear_shape",
                "points": [(2, 1), (2.5, 1.2), (3, 1), (3.2, 1.5), (3.5, 1.5), (3.7, 2), (4, 2), (3.8, 2.5), (4, 3), (3.5, 3.2), (3.5, 3.5), (3, 3.7), (3, 4), (2.5, 3.8), (2, 4), (1.8, 3.5), (1.5, 3.5), (1.3, 3), (1, 3), (1.2, 2.5), (1, 2), (1.5, 1.8), (1.5, 1.5)],
                "color": "#795548"
            }
        ]
    
    selected = random.choice(shapes)
    selected["type"] = "polygon"
    return selected

def generate_emoji_transformation_options(shape, target_transformation):
    """Generate transformation options for emoji shapes"""
    options = []
    
    # Create positions for grid display
    positions = [(2, 2), (5, 2), (2, 5), (5, 5), (3, 3), (4, 4)]
    random.shuffle(positions)
    
    if target_transformation == "translation":
        # Correct: Translation (same orientation, different position)
        options.append({
            "emoji": shape["emoji"],
            "position": positions[0],
            "transformation": "translation",
            "is_correct": True,
            "rotation": 0,
            "flip": False
        })
        
        # Incorrect: Reflection
        options.append({
            "emoji": shape["emoji"],
            "position": positions[1],
            "transformation": "reflection",
            "is_correct": False,
            "rotation": 0,
            "flip": True
        })
        
        # Incorrect: Rotation
        options.append({
            "emoji": shape["emoji"],
            "position": positions[2],
            "transformation": "rotation",
            "is_correct": False,
            "rotation": 90,
            "flip": False
        })
    
    elif target_transformation == "reflection":
        # Correct: Reflection
        options.append({
            "emoji": shape["emoji"],
            "position": positions[0],
            "transformation": "reflection",
            "is_correct": True,
            "rotation": 0,
            "flip": True
        })
        
        # Incorrect: Translation
        options.append({
            "emoji": shape["emoji"],
            "position": positions[1],
            "transformation": "translation",
            "is_correct": False,
            "rotation": 0,
            "flip": False
        })
        
        # Incorrect: Rotation
        options.append({
            "emoji": shape["emoji"],
            "position": positions[2],
            "transformation": "rotation",
            "is_correct": False,
            "rotation": 180,
            "flip": False
        })
    
    else:  # rotation
        # Correct: Rotation
        angle = random.choice([90, 180, 270])
        options.append({
            "emoji": shape["emoji"],
            "position": positions[0],
            "transformation": "rotation",
            "is_correct": True,
            "rotation": angle,
            "flip": False
        })
        
        # Incorrect: Translation
        options.append({
            "emoji": shape["emoji"],
            "position": positions[1],
            "transformation": "translation",
            "is_correct": False,
            "rotation": 0,
            "flip": False
        })
        
        # Incorrect: Reflection
        options.append({
            "emoji": shape["emoji"],
            "position": positions[2],
            "transformation": "reflection",
            "is_correct": False,
            "rotation": 0,
            "flip": True
        })
    
    random.shuffle(options)
    return options

def generate_polygon_transformation_options(shape, target_transformation):
    """Generate transformation options for polygon shapes"""
    options = []
    
    if target_transformation == "translation":
        # Translate the shape
        dx, dy = random.choice([(2, 1), (-1, 2), (3, -1)])
        transformed_points = [(x + dx, y + dy) for x, y in shape["points"]]
        options.append({
            "points": transformed_points,
            "transformation": "translation",
            "is_correct": True
        })
        
        # Add incorrect options
        reflected_points = reflect_shape(shape["points"], "vertical")
        options.append({
            "points": reflected_points,
            "transformation": "reflection",
            "is_correct": False
        })
        
        rotated_points = rotate_shape(shape["points"], 90)
        options.append({
            "points": rotated_points,
            "transformation": "rotation",
            "is_correct": False
        })
    
    elif target_transformation == "reflection":
        # Reflect the shape
        axis = random.choice(["vertical", "horizontal"])
        reflected_points = reflect_shape(shape["points"], axis)
        options.append({
            "points": reflected_points,
            "transformation": "reflection",
            "is_correct": True
        })
        
        # Add incorrect options
        dx, dy = random.choice([(2, 1), (-1, 2)])
        translated_points = [(x + dx, y + dy) for x, y in shape["points"]]
        options.append({
            "points": translated_points,
            "transformation": "translation",
            "is_correct": False
        })
        
        rotated_points = rotate_shape(shape["points"], 180)
        options.append({
            "points": rotated_points,
            "transformation": "rotation",
            "is_correct": False
        })
    
    else:  # rotation
        # Rotate the shape
        angle = random.choice([90, 180, 270])
        rotated_points = rotate_shape(shape["points"], angle)
        options.append({
            "points": rotated_points,
            "transformation": "rotation",
            "is_correct": True
        })
        
        # Add incorrect options
        dx, dy = random.choice([(2, 1), (-1, 2)])
        translated_points = [(x + dx, y + dy) for x, y in shape["points"]]
        options.append({
            "points": translated_points,
            "transformation": "translation",
            "is_correct": False
        })
        
        reflected_points = reflect_shape(shape["points"], "horizontal")
        options.append({
            "points": reflected_points,
            "transformation": "reflection",
            "is_correct": False
        })
    
    random.shuffle(options)
    return options

def reflect_shape(points, axis="vertical"):
    """Reflect shape across an axis"""
    cx = sum(x for x, y in points) / len(points)
    cy = sum(y for x, y in points) / len(points)
    
    reflected = []
    if axis == "vertical":
        for x, y in points:
            new_x = 2 * cx - x
            reflected.append((new_x, y))
    else:  # horizontal
        for x, y in points:
            new_y = 2 * cy - y
            reflected.append((x, new_y))
    
    return reflected

def rotate_shape(points, angle):
    """Rotate shape around its center"""
    cx = sum(x for x, y in points) / len(points)
    cy = sum(y for x, y in points) / len(points)
    
    theta = math.radians(angle)
    
    rotated = []
    for x, y in points:
        x_shifted = x - cx
        y_shifted = y - cy
        
        x_rotated = x_shifted * math.cos(theta) - y_shifted * math.sin(theta)
        y_rotated = x_shifted * math.sin(theta) + y_shifted * math.cos(theta)
        
        x_final = x_rotated + cx + 3
        y_final = y_rotated + cy
        
        rotated.append((x_final, y_final))
    
    return rotated

def display_transformation_problem():
    """Display the transformation problem"""
    data = st.session_state.problem_data
    transformation = data["target_transformation"]
    
    transformation_emojis = {
        "translation": "➡️",
        "reflection": "🪞",
        "rotation": "🔃"
    }
    
    st.markdown(f"### Look at this shape:")
    
    # Display original shape
    if data["original_shape"]["type"] == "emoji":
        display_emoji_shape(data["original_shape"]["emoji"], "original", 0, False)
    else:
        create_shape_display(data["original_shape"]["points"], data["original_shape"]["color"], "original")
    
    # Ask the appropriate question
    st.markdown(f"### Which image shows a {transformation}? {transformation_emojis[transformation]}")
    
    # Display the three options
    cols = st.columns(3)
    for i, (col, option) in enumerate(zip(cols, data["options"])):
        with col:
            st.markdown(f"**{chr(65 + i)}**")  # A, B, C
            if data["original_shape"]["type"] == "emoji":
                display_emoji_shape(
                    option["emoji"], 
                    f"option_{i}", 
                    option.get("rotation", 0),
                    option.get("flip", False)
                )
            else:
                create_shape_display(option["points"], data["original_shape"]["color"], f"option_{i}")
    
    # Display answer buttons
    if not st.session_state.show_feedback:
        st.markdown("---")
        cols = st.columns(3)
        selected = None
        
        for i, col in enumerate(cols):
            with col:
                if st.button(chr(65 + i), key=f"btn_{i}", use_container_width=True):
                    selected = i
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                if selected is not None:
                    submit_answer(selected)
                    st.rerun()
                elif "selected_answer" in st.session_state:
                    submit_answer(st.session_state.selected_answer)
                    st.rerun()
                else:
                    st.warning("Please select A, B, or C")
        
        if selected is not None:
            st.session_state.selected_answer = selected
            st.rerun()
        
        if "selected_answer" in st.session_state:
            answer_text = chr(65 + st.session_state.selected_answer)
            st.info(f"Selected: **{answer_text}**")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def display_emoji_shape(emoji, identifier, rotation=0, flip=False):
    """Display emoji on a grid with transformations"""
    transform_style = ""
    if rotation != 0:
        transform_style += f"rotate({rotation}deg) "
    if flip:
        transform_style += "scaleX(-1) "
    
    html_content = f'''
    <div style="display: flex; justify-content: center; margin: 10px 0;">
        <div style="
            width: 140px;
            height: 140px;
            background: white;
            border: 1px solid #ddd;
            position: relative;
            background-image: repeating-linear-gradient(0deg, #e0e0e0, #e0e0e0 1px, transparent 1px, transparent 20px),
                            repeating-linear-gradient(90deg, #e0e0e0, #e0e0e0 1px, transparent 1px, transparent 20px);
        ">
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) {transform_style};
                font-size: 60px;
            ">
                {emoji}
            </div>
        </div>
    </div>
    '''
    
    components.html(html_content, height=160)

def create_shape_display(points, color, identifier):
    """Create and display a shape on a grid using HTML component"""
    scale = 20
    offset = 10
    
    svg_points = []
    for x, y in points:
        svg_x = x * scale + offset
        svg_y = (6 - y) * scale + offset
        svg_points.append(f"{svg_x},{svg_y}")
    
    polygon_points = " ".join(svg_points)
    
    html_content = f'''
    <div style="display: flex; justify-content: center; margin: 10px 0;">
        <svg width="140" height="140" style="background: white; border: 1px solid #ddd;">
            <!-- Grid lines -->
            <defs>
                <pattern id="grid_{identifier}" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="0.5"/>
                </pattern>
            </defs>
            <rect width="140" height="140" fill="url(#grid_{identifier})"/>
            
            <!-- Grid border lines -->
            <g stroke="#ccc" stroke-width="0.5">
                {"".join([f'<line x1="0" y1="{i}" x2="140" y2="{i}"/>' for i in range(20, 140, 20)])}
                {"".join([f'<line x1="{i}" y1="0" x2="{i}" y2="140"/>' for i in range(20, 140, 20)])}
            </g>
            
            <!-- Shape -->
            <polygon points="{polygon_points}" 
                     fill="{color}" 
                     stroke="darker" 
                     stroke-width="1.5" 
                     opacity="0.7"/>
        </svg>
    </div>
    '''
    
    components.html(html_content, height=160)

def submit_answer(user_answer):
    """Process the submitted answer"""
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_answer = st.session_state.problem_data["correct_answer"]
    
    if user_answer == correct_answer:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        if st.session_state.consecutive_correct >= 3 and st.session_state.transform_difficulty < 3:
            st.session_state.transform_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        if st.session_state.transform_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.transform_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    correct_answer = data["correct_answer"]
    transformation = data["target_transformation"]
    
    transformation_names = {
        "translation": "Translation (Slide)",
        "reflection": "Reflection (Flip)",
        "rotation": "Rotation (Turn)"
    }
    
    if user_answer == correct_answer:
        st.success(f"✅ **Correct!** Option {chr(65 + correct_answer)} shows a {transformation_names[transformation]}!")
        
        explanations = {
            "translation": "The shape has been moved to a new position without changing its orientation or size.",
            "reflection": "The shape has been flipped to create a mirror image.",
            "rotation": "The shape has been turned around a point."
        }
        st.info(f"📐 **Explanation:** {explanations[transformation]}")
        
        if st.session_state.consecutive_correct == 3:
            st.balloons()
            st.info("🏆 **Excellent streak! Moving to the next level!**")
    else:
        st.error(f"❌ **Not quite.** The correct answer was Option {chr(65 + correct_answer)}.")
        
        user_option = data["options"][user_answer]
        st.warning(f"You selected Option {chr(65 + user_answer)}, which shows a {transformation_names[user_option['transformation']]}.")
        
        with st.expander("📖 **Understanding the transformations**", expanded=True):
            st.markdown(f"""
            ### What we were looking for: {transformation_names[transformation]}
            
            **Option {chr(65 + correct_answer)} is correct because:**
            """)
            
            if transformation == "translation":
                st.markdown("""
                - The shape moved position
                - Orientation is exactly the same
                - No flipping or turning occurred
                """)
            elif transformation == "reflection":
                st.markdown("""
                - The shape is a mirror image
                - It has been flipped over a line
                - Orientation is reversed
                """)
            else:  # rotation
                st.markdown("""
                - The shape has been turned
                - It's at a different angle
                - Size is same but orientation changed
                """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_answer = None
    if "selected_answer" in st.session_state:
        del st.session_state.selected_answer