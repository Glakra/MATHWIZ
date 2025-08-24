import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import random

def run():
    """
    Main function to run the Follow Directions on Coordinate Plane activity.
    Interactive movement and navigation practice.
    """
    # Initialize session state
    if "direction_difficulty" not in st.session_state:
        st.session_state.direction_difficulty = 1
        st.session_state.direction_consecutive_correct = 0
        st.session_state.direction_consecutive_wrong = 0
        st.session_state.direction_total_score = 0
        st.session_state.direction_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.user_x = ""
        st.session_state.user_y = ""
    
    if "current_direction_problem" not in st.session_state:
        generate_direction_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > P. Coordinate plane**")
    st.title("🧭 Follow Directions on a Coordinate Plane")
    st.markdown("*Follow movement instructions and find where you end up*")
    st.markdown("---")
    
    # Display progress
    display_direction_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_direction_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_direction_problem()
    
    # Instructions
    with st.expander("💡 **How to Follow Directions**", expanded=False):
        st.markdown("""
        ### Movement Rules:
        - **Right**: Add to x-coordinate (move →)
        - **Left**: Subtract from x-coordinate (move ←)
        - **Up**: Add to y-coordinate (move ↑)
        - **Down**: Subtract from y-coordinate (move ↓)
        
        ### Example:
        - Start at (3, 4)
        - Move right 2 units: x becomes 3 + 2 = 5
        - End at (5, 4)
        
        ### Difficulty Levels:
        - **Level 1**: Single movements (up/down/left/right)
        - **Level 2**: Larger single movements
        - **Level 3**: Two-step movements
        - **Level 4**: Diagonal movements
        - **Level 5**: Three-step movements
        - **Level 6**: Complex paths with obstacles
        
        ### Tips:
        - Track x and y separately
        - Right/Left changes x-coordinate
        - Up/Down changes y-coordinate
        - Check your path doesn't go off the grid!
        """)

def get_direction_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.direction_difficulty
    
    settings = {
        1: {
            "grid_size": 10,
            "num_steps": 1,
            "max_distance": 4,
            "movement_types": ["horizontal", "vertical"],
            "start_range": (1, 8),  # Keep away from edges
            "label": "Single Step",
            "color": "🟢"
        },
        2: {
            "grid_size": 10,
            "num_steps": 1,
            "max_distance": 8,
            "movement_types": ["horizontal", "vertical"],
            "start_range": (0, 9),
            "label": "Longer Steps",
            "color": "🟡"
        },
        3: {
            "grid_size": 12,
            "num_steps": 2,
            "max_distance": 5,
            "movement_types": ["horizontal", "vertical"],
            "start_range": (2, 9),
            "label": "Two Steps",
            "color": "🟠"
        },
        4: {
            "grid_size": 12,
            "num_steps": 2,
            "max_distance": 6,
            "movement_types": ["horizontal", "vertical", "diagonal"],
            "start_range": (2, 9),
            "label": "With Diagonals",
            "color": "🔴"
        },
        5: {
            "grid_size": 15,
            "num_steps": 3,
            "max_distance": 5,
            "movement_types": ["horizontal", "vertical", "diagonal"],
            "start_range": (3, 11),
            "label": "Three Steps",
            "color": "🟣"
        },
        6: {
            "grid_size": 15,
            "num_steps": 4,
            "max_distance": 6,
            "movement_types": ["horizontal", "vertical", "diagonal", "complex"],
            "start_range": (3, 11),
            "label": "Complex Paths",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_direction_progress():
    """Display current level and progress"""
    settings = get_direction_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.direction_difficulty}/6")
    
    with col2:
        st.metric("Movement Type", settings['label'])
    
    with col3:
        if st.session_state.direction_total_attempts > 0:
            accuracy = (st.session_state.direction_total_score / st.session_state.direction_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.direction_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.direction_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Master Navigator")

def generate_direction_problem():
    """Generate a new direction following problem"""
    settings = get_direction_difficulty_settings()
    
    # Generate starting position
    start_x = random.randint(settings["start_range"][0], settings["start_range"][1])
    start_y = random.randint(settings["start_range"][0], settings["start_range"][1])
    
    # Generate movements
    movements = []
    current_x, current_y = start_x, start_y
    
    for _ in range(settings["num_steps"]):
        # Choose movement type
        if "diagonal" in settings["movement_types"] and random.random() < 0.3:
            movement_type = "diagonal"
        else:
            movement_type = random.choice(["horizontal", "vertical"])
        
        # Generate movement
        if movement_type == "horizontal":
            # Ensure we stay on grid
            max_right = min(settings["max_distance"], settings["grid_size"] - current_x)
            max_left = min(settings["max_distance"], current_x)
            
            if max_right > 0 and (max_left == 0 or random.random() < 0.5):
                # Move right
                distance = random.randint(1, max_right)
                movements.append(("right", distance))
                current_x += distance
            else:
                # Move left
                distance = random.randint(1, max_left)
                movements.append(("left", distance))
                current_x -= distance
                
        elif movement_type == "vertical":
            # Ensure we stay on grid
            max_up = min(settings["max_distance"], settings["grid_size"] - current_y)
            max_down = min(settings["max_distance"], current_y)
            
            if max_up > 0 and (max_down == 0 or random.random() < 0.5):
                # Move up
                distance = random.randint(1, max_up)
                movements.append(("up", distance))
                current_y += distance
            else:
                # Move down
                distance = random.randint(1, max_down)
                movements.append(("down", distance))
                current_y -= distance
                
        else:  # diagonal
            # Simple diagonal movements
            directions = []
            if current_x < settings["grid_size"] - 2 and current_y < settings["grid_size"] - 2:
                directions.append(("northeast", 1, 1))
            if current_x > 2 and current_y < settings["grid_size"] - 2:
                directions.append(("northwest", -1, 1))
            if current_x < settings["grid_size"] - 2 and current_y > 2:
                directions.append(("southeast", 1, -1))
            if current_x > 2 and current_y > 2:
                directions.append(("southwest", -1, -1))
            
            if directions:
                direction = random.choice(directions)
                distance = random.randint(1, min(3, settings["max_distance"]))
                movements.append((direction[0], distance))
                current_x += direction[1] * distance
                current_y += direction[2] * distance
    
    # Create question text
    question_parts = [f"You start at ({start_x}, {start_y})."]
    
    for i, (direction, distance) in enumerate(movements):
        if i > 0:
            question_parts.append("Then you")
        else:
            question_parts.append("You")
            
        if distance == 1:
            question_parts.append(f"move {direction} {distance} unit.")
        else:
            question_parts.append(f"move {direction} {distance} units.")
    
    question_parts.append("Where do you end?")
    question = " ".join(question_parts)
    
    problem_data = {
        "settings": settings,
        "start_position": (start_x, start_y),
        "movements": movements,
        "end_position": (current_x, current_y),
        "question": question,
        "path": [(start_x, start_y)]  # Store path for visualization
    }
    
    # Calculate full path
    x, y = start_x, start_y
    for direction, distance in movements:
        if direction == "right":
            x += distance
        elif direction == "left":
            x -= distance
        elif direction == "up":
            y += distance
        elif direction == "down":
            y -= distance
        elif direction == "northeast":
            x += distance
            y += distance
        elif direction == "northwest":
            x -= distance
            y += distance
        elif direction == "southeast":
            x += distance
            y -= distance
        elif direction == "southwest":
            x -= distance
            y -= distance
        problem_data["path"].append((x, y))
    
    st.session_state.current_direction_problem = problem_data
    st.session_state.show_result = False
    st.session_state.user_x = ""
    st.session_state.user_y = ""

def display_direction_problem():
    """Display the direction problem interface"""
    problem = st.session_state.current_direction_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Create two columns - grid and input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display the coordinate grid
        create_direction_visualization(problem)
    
    with col2:
        st.markdown("### Your Answer")
        
        if not st.session_state.show_result:
            # Input fields for coordinates
            st.markdown("Where do you end?")
            
            # Create input fields in a row
            input_col1, input_col2 = st.columns(2)
            
            with input_col1:
                user_x = st.text_input(
                    "x",
                    value=st.session_state.user_x,
                    key="x_input",
                    placeholder="?",
                    max_chars=2
                )
                st.session_state.user_x = user_x
            
            with input_col2:
                user_y = st.text_input(
                    "y", 
                    value=st.session_state.user_y,
                    key="y_input",
                    placeholder="?",
                    max_chars=2
                )
                st.session_state.user_y = user_y
            
            # Show coordinate format
            st.caption(f"Answer: ({user_x or '?'}, {user_y or '?'})")
            
            # Submit button
            st.markdown("---")
            if st.button("Submit", type="primary", use_container_width=True):
                if user_x and user_y:
                    try:
                        int(user_x)
                        int(user_y)
                        check_direction_answer()
                        st.rerun()
                    except ValueError:
                        st.error("Please enter valid numbers")
                else:
                    st.error("Please enter both coordinates")
        else:
            # Show submitted answer
            st.markdown("Your answer:")
            st.info(f"({st.session_state.user_x}, {st.session_state.user_y})")
            
            st.markdown("Correct answer:")
            if (int(st.session_state.user_x), int(st.session_state.user_y)) == problem['end_position']:
                st.success(f"{problem['end_position']}")
            else:
                st.error(f"{problem['end_position']}")
    
    # Show feedback
    if st.session_state.show_result:
        display_direction_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="primary", use_container_width=True):
                generate_direction_problem()
                st.rerun()

def create_direction_visualization(problem):
    """Create the coordinate grid with movement visualization"""
    settings = problem['settings']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Set up the grid
    ax.set_xlim(-0.5, settings['grid_size'] + 0.5)
    ax.set_ylim(-0.5, settings['grid_size'] + 0.5)
    ax.set_aspect('equal')
    
    # Draw grid
    ax.grid(True, linestyle='-', color='lightgray', alpha=0.7)
    
    # Set ticks
    ax.set_xticks(range(0, settings['grid_size'] + 1))
    ax.set_yticks(range(0, settings['grid_size'] + 1))
    
    # Add axis labels
    ax.set_xlabel('x', fontsize=14, labelpad=10)
    ax.set_ylabel('y', fontsize=14, labelpad=10)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Draw starting point
    start_x, start_y = problem['start_position']
    ax.plot(start_x, start_y, 'go', markersize=15, label='Start')
    ax.text(start_x + 0.2, start_y + 0.2, 'START', fontsize=10, color='green', weight='bold')
    
    # If showing result, draw the path
    if st.session_state.show_result:
        # Draw path
        path = problem['path']
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            
            # Draw arrow
            arrow = FancyArrowPatch(
                (x1, y1), (x2, y2),
                arrowstyle='->', 
                mutation_scale=20,
                linewidth=3,
                color='blue',
                alpha=0.7
            )
            ax.add_patch(arrow)
            
            # Add step number
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.3, f"Step {i + 1}", 
                   fontsize=9, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
        
        # Draw end point
        end_x, end_y = problem['end_position']
        ax.plot(end_x, end_y, 'ro', markersize=15, label='End')
        ax.text(end_x + 0.2, end_y + 0.2, 'END', fontsize=10, color='red', weight='bold')
        
        # Draw user's answer if incorrect
        try:
            user_x = int(st.session_state.user_x)
            user_y = int(st.session_state.user_y)
            if (user_x, user_y) != (end_x, end_y):
                ax.plot(user_x, user_y, 'ko', markersize=15, alpha=0.5)
                ax.text(user_x + 0.2, user_y - 0.3, 'Your Answer', 
                       fontsize=9, color='black', alpha=0.7)
        except:
            pass
    else:
        # Just show starting point with a question mark for end
        ax.text(settings['grid_size'] / 2, settings['grid_size'] - 1, '?', 
               fontsize=30, ha='center', color='gray', alpha=0.5)
    
    # Add title
    ax.set_title("Follow the Directions", fontsize=16, pad=20)
    
    # Add legend if showing result
    if st.session_state.show_result:
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.tight_layout()
    st.pyplot(fig)

def check_direction_answer():
    """Check if the submitted answer is correct"""
    problem = st.session_state.current_direction_problem
    
    try:
        user_x = int(st.session_state.user_x)
        user_y = int(st.session_state.user_y)
        user_answer = (user_x, user_y)
    except ValueError:
        return
    
    correct_answer = problem['end_position']
    
    # Update statistics
    st.session_state.direction_total_attempts += 1
    
    if user_answer == correct_answer:
        st.session_state.direction_total_score += 1
        st.session_state.direction_consecutive_correct += 1
        st.session_state.direction_consecutive_wrong = 0
        st.session_state.current_direction_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.direction_consecutive_correct >= 3 and 
            st.session_state.direction_difficulty < 6):
            st.session_state.direction_difficulty += 1
            st.session_state.direction_consecutive_correct = 0
    else:
        st.session_state.direction_consecutive_wrong += 1
        st.session_state.direction_consecutive_correct = 0
        st.session_state.current_direction_problem["result"] = "incorrect"
        
        # Check for level down
        if (st.session_state.direction_consecutive_wrong >= 3 and 
            st.session_state.direction_difficulty > 1):
            st.session_state.direction_difficulty -= 1
            st.session_state.direction_consecutive_wrong = 0
    
    st.session_state.show_result = True

def display_direction_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_direction_problem
    
    if problem.get("result") == "correct":
        st.success("✅ Excellent! You found the correct ending position!")
        
        if st.session_state.direction_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Great navigation! {st.session_state.direction_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.direction_consecutive_correct == 0:  # Just leveled up
            st.success(f"🎉 Level Up! Now tackling: {get_direction_difficulty_settings()['label']}!")
    else:
        st.error("❌ Not quite right. Check the path on the grid.")
        
        # Provide step-by-step explanation
        with st.expander("📐 See step-by-step solution"):
            problem = st.session_state.current_direction_problem
            st.markdown(f"**Starting position:** {problem['start_position']}")
            
            x, y = problem['start_position']
            for i, (direction, distance) in enumerate(problem['movements']):
                st.markdown(f"\n**Step {i + 1}:** Move {direction} {distance} unit(s)")
                
                if direction == "right":
                    st.markdown(f"- x: {x} + {distance} = {x + distance}")
                    st.markdown(f"- y: stays {y}")
                    x += distance
                elif direction == "left":
                    st.markdown(f"- x: {x} - {distance} = {x - distance}")
                    st.markdown(f"- y: stays {y}")
                    x -= distance
                elif direction == "up":
                    st.markdown(f"- x: stays {x}")
                    st.markdown(f"- y: {y} + {distance} = {y + distance}")
                    y += distance
                elif direction == "down":
                    st.markdown(f"- x: stays {x}")
                    st.markdown(f"- y: {y} - {distance} = {y - distance}")
                    y -= distance
                
                st.markdown(f"- New position: ({x}, {y})")
            
            st.markdown(f"\n**Final position:** ({x}, {y})")
            
            st.info("""
            Remember:
            - Right/Left changes the x-coordinate
            - Up/Down changes the y-coordinate
            - Track each change carefully!
            """)
        
        # Level down message
        if st.session_state.direction_consecutive_wrong == 0:  # Just leveled down
            st.warning(f"📉 Moving to easier problems: {get_direction_difficulty_settings()['label']}")

def clear_direction_state():
    """Clear all direction-related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('direction_') or key in ['current_direction_problem', 'show_result', 'user_x', 'user_y']:
            del st.session_state[key]