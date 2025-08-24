import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np
import random

def run():
    """
    Main function to run the Coordinate Planes as Maps activity.
    Interactive map exploration with locations and coordinates.
    """
    # Initialize session state
    if "map_difficulty" not in st.session_state:
        st.session_state.map_difficulty = 1
        st.session_state.map_consecutive_correct = 0
        st.session_state.map_consecutive_wrong = 0
        st.session_state.map_total_score = 0
        st.session_state.map_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.selected_answer = None
    
    if "current_map_problem" not in st.session_state:
        generate_map_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > P. Coordinate plane**")
    st.title("🗺️ Coordinate Planes as Maps")
    st.markdown("*Find locations using coordinates on the map*")
    st.markdown("---")
    
    # Display progress
    display_map_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_map_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_map_problem()
    
    # Instructions
    with st.expander("💡 **How to Use Map Coordinates**", expanded=False):
        st.markdown("""
        ### Reading Map Coordinates:
        1. **First number (x)**: Count spaces to the RIGHT from 0
        2. **Second number (y)**: Count spaces UP from 0
        3. **Example**: (3, 2) means 3 right, 2 up
        
        ### Question Types:
        - **"What is at (x, y)?"** - Find what's at those coordinates
        - **"Where is the [place]?"** - Click the coordinates where it's located
        
        ### Difficulty Levels:
        - **Level 1**: 4-5 locations, small grid (0-5)
        - **Level 2**: 5-6 locations, medium grid (0-7)
        - **Level 3**: 6-8 locations, coordinates given
        - **Level 4**: 8-10 locations, find coordinates
        - **Level 5**: 10-12 locations, mixed questions
        - **Level 6**: 12+ locations, city districts
        
        ### Tips:
        - Always start counting from (0, 0) at bottom-left
        - Check both x and y coordinates carefully
        - Icons help identify different types of locations
        """)

def get_map_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.map_difficulty
    
    settings = {
        1: {
            "grid_size": 5,
            "num_locations": random.randint(4, 5),
            "question_type": "what_is_at",  # Only "What is at?" questions
            "label": "Beginner Map",
            "color": "🟢"
        },
        2: {
            "grid_size": 7,
            "num_locations": random.randint(5, 6),
            "question_type": "what_is_at",  # Still only "What is at?"
            "label": "Basic Map",
            "color": "🟡"
        },
        3: {
            "grid_size": 7,
            "num_locations": random.randint(6, 8),
            "question_type": "mixed",  # Mix of both question types
            "label": "Town Map",
            "color": "🟠"
        },
        4: {
            "grid_size": 8,
            "num_locations": random.randint(8, 10),
            "question_type": "where_is",  # Focus on "Where is?" questions
            "label": "City Map",
            "color": "🔴"
        },
        5: {
            "grid_size": 10,
            "num_locations": random.randint(10, 12),
            "question_type": "mixed",
            "label": "Large City",
            "color": "🟣"
        },
        6: {
            "grid_size": 10,
            "num_locations": random.randint(12, 15),
            "question_type": "mixed",
            "label": "Metropolis",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_map_progress():
    """Display current level and progress"""
    settings = get_map_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.map_difficulty}/6")
    
    with col2:
        st.metric("Map Type", settings['label'])
    
    with col3:
        if st.session_state.map_total_attempts > 0:
            accuracy = (st.session_state.map_total_score / st.session_state.map_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.map_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.map_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Metropolis Navigator")

def generate_map_problem():
    """Generate a new map coordinate problem"""
    settings = get_map_difficulty_settings()
    
    # Define location types with emojis
    location_types = [
        ("🏪", "grocery store"),
        ("🏦", "bank"),
        ("🐾", "pet store"),
        ("🎨", "art supply store"),
        ("🚲", "bicycle shop"),
        ("🎭", "theatre"),
        ("🏥", "hospital"),
        ("📚", "library"),
        ("☕", "coffee shop"),
        ("🍕", "pizza place"),
        ("🏫", "school"),
        ("⛽", "gas station"),
        ("🏬", "shopping mall"),
        ("🎮", "game store"),
        ("💊", "pharmacy"),
        ("🚗", "car dealership"),
        ("📮", "post office"),
        ("🎨", "art gallery"),
        ("🎪", "toy store"),
        ("🏢", "office building"),
        ("🎬", "cinema"),
        ("🏪", "convenience store"),
        ("🏛️", "museum"),
        ("⚽", "sports store"),
        ("🎵", "music shop"),
        ("📡", "radio tower"),
        ("⚓", "harbour"),
        ("✨", "magic shop"),
        ("🗑️", "tip"),
        ("🎉", "party supply store")
    ]
    
    # Randomly select locations
    selected_locations = random.sample(location_types, settings["num_locations"])
    
    # Generate random positions for locations
    positions = []
    location_map = {}
    
    for emoji, name in selected_locations:
        while True:
            x = random.randint(0, settings["grid_size"])
            y = random.randint(0, settings["grid_size"])
            if (x, y) not in positions:
                positions.append((x, y))
                location_map[(x, y)] = (emoji, name)
                break
    
    # Decide question type
    if settings["question_type"] == "what_is_at":
        question_type = "what_is_at"
    elif settings["question_type"] == "where_is":
        question_type = "where_is"
    else:  # mixed
        question_type = random.choice(["what_is_at", "where_is"])
    
    # Generate question and answer
    if question_type == "what_is_at":
        # Pick a location that exists
        target_pos = random.choice(positions)
        question = f"What is at ({target_pos[0]}, {target_pos[1]})?"
        correct_answer = location_map[target_pos][1]
        
        # Generate wrong answers
        other_locations = [loc[1] for pos, loc in location_map.items() if pos != target_pos]
        wrong_answers = random.sample(other_locations, min(3, len(other_locations)))
        
        # If we need more wrong answers, add some that aren't on the map
        all_location_names = [loc[1] for _, loc in location_types]
        used_names = [loc[1] for _, loc in location_map.values()]
        unused_names = [name for name in all_location_names if name not in used_names]
        
        while len(wrong_answers) < 3 and unused_names:
            wrong_answers.append(random.choice(unused_names))
            unused_names.remove(wrong_answers[-1])
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
    else:  # where_is
        # Pick a location to find
        target_pos = random.choice(positions)
        target_location = location_map[target_pos]
        question = f"Where is the {target_location[1]}?"
        correct_answer = f"({target_pos[0]}, {target_pos[1]})"
        
        # Generate coordinate options (some real, some not on map)
        options = [correct_answer]
        
        # Add some other real positions
        other_positions = [pos for pos in positions if pos != target_pos]
        for pos in random.sample(other_positions, min(2, len(other_positions))):
            options.append(f"({pos[0]}, {pos[1]})")
        
        # Add a fake position
        while len(options) < 4:
            fake_x = random.randint(0, settings["grid_size"])
            fake_y = random.randint(0, settings["grid_size"])
            fake_option = f"({fake_x}, {fake_y})"
            if fake_option not in options:
                options.append(fake_option)
        
        random.shuffle(options)
    
    problem_data = {
        "settings": settings,
        "location_map": location_map,
        "question": question,
        "question_type": question_type,
        "correct_answer": correct_answer,
        "options": options[:4],  # Ensure exactly 4 options
        "target_position": target_pos if question_type == "what_is_at" else None
    }
    
    st.session_state.current_map_problem = problem_data
    st.session_state.show_result = False
    st.session_state.selected_answer = None

def display_map_problem():
    """Display the map and question interface"""
    problem = st.session_state.current_map_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Create two columns - map and answer options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display the map
        create_map_visualization(problem)
    
    with col2:
        st.markdown("### Select Answer")
        
        if not st.session_state.show_result:
            # Display answer options as buttons
            for i, option in enumerate(problem['options']):
                if st.button(
                    option, 
                    key=f"option_{i}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_answer == option else "secondary"
                ):
                    st.session_state.selected_answer = option
                    st.rerun()
            
            # Submit button
            st.markdown("---")
            if st.button("Submit", type="primary", use_container_width=True, 
                        disabled=st.session_state.selected_answer is None):
                check_map_answer()
                st.rerun()
        else:
            # Show which answer was selected
            for option in problem['options']:
                if option == st.session_state.selected_answer:
                    if option == problem['correct_answer']:
                        st.success(f"✅ {option}")
                    else:
                        st.error(f"❌ {option}")
                elif option == problem['correct_answer']:
                    st.info(f"✓ {option}")
                else:
                    st.caption(option)
    
    # Show feedback
    if st.session_state.show_result:
        display_map_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                generate_map_problem()
                st.rerun()

def create_map_visualization(problem):
    """Create the map visualization with locations"""
    settings = problem['settings']
    location_map = problem['location_map']
    
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
    
    # Add locations to the map
    for (x, y), (emoji, name) in location_map.items():
        # Add emoji/icon
        ax.text(x, y, emoji, fontsize=24, ha='center', va='center',
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='white', edgecolor='gray', alpha=0.8))
        
        # Add label below if not too crowded
        if settings['num_locations'] <= 8:
            ax.text(x, y - 0.3, name, fontsize=8, ha='center', va='top', 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow', alpha=0.7))
    
    # Highlight target position if showing result
    if st.session_state.show_result:
        if problem['question_type'] == 'what_is_at' and problem['target_position']:
            # Highlight the position asked about
            x, y = problem['target_position']
            circle = plt.Circle((x, y), 0.4, color='green', fill=False, linewidth=3)
            ax.add_patch(circle)
        elif problem['question_type'] == 'where_is':
            # Highlight the correct location
            for (x, y), (emoji, name) in location_map.items():
                if name == problem['correct_answer'].replace("the ", ""):
                    # Find position from answer
                    correct_pos = None
                    for pos, loc in location_map.items():
                        if loc[1] == problem['correct_answer'].replace("Where is the ", "").replace("?", ""):
                            correct_pos = pos
                            break
                    
                    # Extract coordinates from correct answer string
                    if "(" in problem['correct_answer']:
                        coords = problem['correct_answer'].strip("()").split(", ")
                        x, y = int(coords[0]), int(coords[1])
                        circle = plt.Circle((x, y), 0.4, color='green', fill=False, linewidth=3)
                        ax.add_patch(circle)
    
    # Add title
    ax.set_title(f"{settings['label']} - Grid Size: {settings['grid_size']}x{settings['grid_size']}", 
                fontsize=16, pad=20)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Show legend
    with st.expander("📍 Location Legend", expanded=False):
        cols = st.columns(3)
        for i, ((x, y), (emoji, name)) in enumerate(location_map.items()):
            with cols[i % 3]:
                st.caption(f"{emoji} {name} at ({x}, {y})")

def check_map_answer():
    """Check if the selected answer is correct"""
    problem = st.session_state.current_map_problem
    selected = st.session_state.selected_answer
    correct = problem['correct_answer']
    
    # Update statistics
    st.session_state.map_total_attempts += 1
    
    if selected == correct:
        st.session_state.map_total_score += 1
        st.session_state.map_consecutive_correct += 1
        st.session_state.map_consecutive_wrong = 0
        st.session_state.current_map_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.map_consecutive_correct >= 3 and 
            st.session_state.map_difficulty < 6):
            st.session_state.map_difficulty += 1
            st.session_state.map_consecutive_correct = 0
    else:
        st.session_state.map_consecutive_wrong += 1
        st.session_state.map_consecutive_correct = 0
        st.session_state.current_map_problem["result"] = "incorrect"
        
        # Check for level down
        if (st.session_state.map_consecutive_wrong >= 3 and 
            st.session_state.map_difficulty > 1):
            st.session_state.map_difficulty -= 1
            st.session_state.map_consecutive_wrong = 0
    
    st.session_state.show_result = True

def display_map_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_map_problem
    
    if problem.get("result") == "correct":
        st.success("✅ Excellent! That's the right answer!")
        
        if st.session_state.map_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Great navigation! {st.session_state.map_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.map_consecutive_correct == 0:  # Just leveled up
            st.success(f"🎉 Level Up! Welcome to {get_map_difficulty_settings()['label']}!")
    else:
        st.error(f"❌ Not quite. The correct answer was: {problem['correct_answer']}")
        
        # Provide explanation
        with st.expander("📍 See explanation"):
            if problem['question_type'] == 'what_is_at':
                st.markdown(f"**At position {problem['target_position']}:**")
                emoji, name = problem['location_map'][problem['target_position']]
                st.markdown(f"You'll find the {emoji} **{name}**")
                st.info("Remember: Count right for x, then up for y!")
            else:
                st.markdown(f"**To find the {problem['correct_answer']}:**")
                st.markdown("Look for its icon on the map, then read its coordinates")
                st.info("Remember: First number is x (horizontal), second is y (vertical)")
        
        # Level down message
        if st.session_state.map_consecutive_wrong == 0:  # Just leveled down
            st.warning(f"📉 Moving to an easier map: {get_map_difficulty_settings()['label']}")

def clear_map_state():
    """Clear all map-related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('map_') or key in ['current_map_problem', 'show_result', 'selected_answer']:
            del st.session_state[key]