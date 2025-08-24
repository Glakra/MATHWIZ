import streamlit as st
import random
import math

def run():
    """
    Main function to run the Estimate Angle Measurements activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/estimate_angle_measurements.py
    """
    # Initialize session state
    if "estimate_difficulty" not in st.session_state:
        st.session_state.estimate_difficulty = 1  # 1=easy (common angles), 2=medium (varied), 3=hard (close options)
    
    if "current_angle" not in st.session_state:
        st.session_state.current_angle = None
        st.session_state.angle_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_choice = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Estimate Angle Measurements")
    st.markdown("*Look at the angle and choose the best estimate*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (Common angles)",
            2: "Medium (Varied angles)", 
            3: "Hard (Close options)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.estimate_difficulty]}")
        progress = (st.session_state.estimate_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.estimate_difficulty}/3")
    
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
    
    # Generate new angle if needed
    if st.session_state.current_angle is None:
        generate_new_angle()
    
    # Display the angle estimation problem
    display_angle_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Estimate Angles:
        
        1. **Look at the angle** shown in the diagram
        2. **Compare to reference angles** you know
        3. **Choose the best estimate** from the options
        4. **Click Submit** to check your answer
        
        ### Reference Angles to Remember:
        - **0°:** Rays point in the same direction
        - **30°:** About 1/3 of a right angle
        - **45°:** Half of a right angle (diagonal)
        - **60°:** About 2/3 of a right angle
        - **90°:** Right angle (perpendicular, L-shape)
        - **120°:** Wider than a right angle (90° + 30°)
        - **135°:** One and a half right angles (90° + 45°)
        - **150°:** Almost a straight line (180° - 30°)
        - **180°:** Straight angle (opposite directions)
        
        ### Estimation Tips:
        - **Acute angles:** Less than 90° (sharp)
        - **Right angle:** Exactly 90° (square corner)
        - **Obtuse angles:** Between 90° and 180° (wide)
        - **Straight angle:** Exactly 180° (straight line)
        
        ### Quick Checks:
        - Is it smaller or larger than a right angle?
        - Is it closer to 0° or 180°?
        - Compare to halfway points (45°, 90°, 135°)
        
        ### Visual Tricks:
        - 📐 Imagine a square corner for 90°
        - ✂️ Imagine scissors opening for different angles
        - 🕐 Think of clock hands for common angles
        """)

def generate_new_angle():
    """Generate a new angle for estimation"""
    difficulty = st.session_state.estimate_difficulty
    
    if difficulty == 1:  # Easy - common angles
        # Common angles that are easy to recognize
        angle_pool = [30, 45, 60, 90, 120, 135, 150]
        actual_angle = random.choice(angle_pool)
        
        # Generate options with clear differences
        if actual_angle <= 45:
            wrong_options = [actual_angle + 30, actual_angle + 60, actual_angle + 90]
        elif actual_angle == 90:
            wrong_options = [30, 60, 120]
        else:
            wrong_options = [actual_angle - 30, actual_angle - 60, 90]
        
    elif difficulty == 2:  # Medium - varied angles
        # More varied angles
        angle_pool = [15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165]
        actual_angle = random.choice(angle_pool)
        
        # Generate options with moderate differences
        offset_pool = [-30, -20, -15, 15, 20, 30]
        wrong_options = []
        for _ in range(3):
            offset = random.choice(offset_pool)
            wrong = actual_angle + offset
            if 10 <= wrong <= 170 and wrong != actual_angle and wrong not in wrong_options:
                wrong_options.append(wrong)
            offset_pool.remove(offset)
        
        # Ensure we have 3 wrong options
        while len(wrong_options) < 3:
            wrong = random.randint(10, 170)
            if wrong != actual_angle and wrong not in wrong_options:
                wrong_options.append(wrong)
    
    else:  # Hard - close options
        # Any angle, with close distractors
        actual_angle = random.randint(15, 165)
        
        # Generate options with small differences
        offsets = [-15, -10, -5, 5, 10, 15]
        wrong_options = []
        used_offsets = []
        
        for _ in range(3):
            offset = random.choice([o for o in offsets if o not in used_offsets])
            wrong = actual_angle + offset
            if 10 <= wrong <= 170:
                wrong_options.append(wrong)
                used_offsets.append(offset)
        
        # Ensure we have 3 wrong options
        while len(wrong_options) < 3:
            wrong = actual_angle + random.choice([-20, 20, 25, -25])
            if 10 <= wrong <= 170 and wrong not in wrong_options:
                wrong_options.append(wrong)
    
    # Create options list and shuffle
    options = [actual_angle] + wrong_options[:3]
    random.shuffle(options)
    
    # Determine angle type
    if actual_angle < 90:
        angle_type = "acute"
    elif actual_angle == 90:
        angle_type = "right"
    elif actual_angle < 180:
        angle_type = "obtuse"
    else:
        angle_type = "straight"
    
    # Store angle data
    st.session_state.angle_data = {
        'actual_angle': actual_angle,
        'options': options,
        'angle_type': angle_type
    }
    st.session_state.current_angle = actual_angle

def display_angle_problem():
    """Display the angle estimation problem"""
    data = st.session_state.angle_data
    
    # Question text
    st.markdown("### What is the measure of this angle? Choose the best estimate.")
    
    # Create the angle visualization
    create_angle_visualization(data['actual_angle'])
    
    # Display options as clickable tiles
    if not st.session_state.show_feedback:
        st.markdown("### Select your answer:")
        
        # Create a 2x2 grid for options
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2]
        
        selected = None
        for i, option in enumerate(data['options']):
            col_index = i % 2
            row_offset = i // 2
            
            with cols[col_index] if row_offset == 0 else cols[col_index + 2]:
                # Create a button for each option
                button_key = f"option_{i}"
                if st.button(
                    f"{option}°",
                    key=button_key,
                    use_container_width=True,
                    help=f"Click to select {option}°"
                ):
                    selected = option
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                if selected is not None:
                    submit_answer(selected)
                    st.rerun()
                else:
                    # Check if any option was selected in session state
                    if "selected_angle" in st.session_state:
                        submit_answer(st.session_state.selected_angle)
                        st.rerun()
                    else:
                        st.warning("Please select an answer first")
        
        # Store selected value if clicked
        if selected is not None:
            st.session_state.selected_angle = selected
            st.rerun()
        
        # Highlight selected option
        if "selected_angle" in st.session_state:
            st.success(f"Selected: {st.session_state.selected_angle}°")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_angle_visualization(angle_degrees):
    """Create a visual representation of the angle"""
    import streamlit.components.v1 as components
    
    # Convert angle to radians
    angle_rad = math.radians(angle_degrees)
    
    # Calculate end point of second ray
    ray_length = 150
    end_x = 200 + ray_length * math.cos(angle_rad)
    end_y = 200 - ray_length * math.sin(angle_rad)
    
    # Determine color based on angle type
    if angle_degrees == 90:
        angle_color = "#4CAF50"  # Green for right angle
    elif angle_degrees < 90:
        angle_color = "#2196F3"  # Blue for acute
    else:
        angle_color = "#FF9800"  # Orange for obtuse
    
    # Create SVG visualization
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                background: white;
                font-family: Arial, sans-serif;
            }}
            svg {{
                background: #fafafa;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Background grid for reference -->
            <defs>
                <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f0f0" stroke-width="1"/>
                </pattern>
            </defs>
            <rect width="400" height="400" fill="url(#grid)"/>
            
            <!-- Angle arc (for visualization) -->
            <path d="M 200 200 L 350 200 A 50 50 0 {1 if angle_degrees > 180 else 0} 0 {200 + 50 * math.cos(angle_rad)} {200 - 50 * math.sin(angle_rad)} Z"
                  fill="{angle_color}" fill-opacity="0.2" stroke="none"/>
            
            <!-- Small arc to show the angle -->
            <path d="M 250 200 A 50 50 0 {1 if angle_degrees > 180 else 0} 0 {200 + 50 * math.cos(angle_rad)} {200 - 50 * math.sin(angle_rad)}"
                  fill="none" stroke="{angle_color}" stroke-width="2" stroke-dasharray="3,3"/>
            
            <!-- First ray (horizontal) -->
            <line x1="200" y1="200" x2="350" y2="200" 
                  stroke="#000" stroke-width="3" stroke-linecap="round"/>
            
            <!-- Arrow on first ray -->
            <polygon points="345,195 345,205 355,200" fill="#000"/>
            
            <!-- Second ray -->
            <line x1="200" y1="200" x2="{end_x}" y2="{end_y}" 
                  stroke="#000" stroke-width="3" stroke-linecap="round"/>
            
            <!-- Arrow on second ray -->
            <polygon points="{end_x - 5 * math.cos(angle_rad) - 5 * math.sin(angle_rad)},{end_y + 5 * math.sin(angle_rad) - 5 * math.cos(angle_rad)} 
                           {end_x - 5 * math.cos(angle_rad) + 5 * math.sin(angle_rad)},{end_y + 5 * math.sin(angle_rad) + 5 * math.cos(angle_rad)} 
                           {end_x + 5 * math.cos(angle_rad)},{end_y - 5 * math.sin(angle_rad)}" 
                     fill="#000"/>
            
            <!-- Vertex point -->
            <circle cx="200" cy="200" r="5" fill="#000"/>
            
            <!-- Right angle square (if applicable) -->
            {f'<path d="M 220 200 L 220 180 L 200 180" fill="none" stroke="#000" stroke-width="2"/>' if angle_degrees == 90 else ''}
            
            <!-- Question mark in the angle -->
            <text x="{200 + 30 * math.cos(angle_rad/2)}" y="{200 - 30 * math.sin(angle_rad/2)}" 
                  text-anchor="middle" font-size="24" font-weight="bold" fill="{angle_color}">?</text>
        </svg>
    </body>
    </html>
    '''
    
    # Display the angle
    components.html(html_content, height=440, scrolling=False)

def submit_answer(selected_angle):
    """Process the submitted answer"""
    st.session_state.user_choice = selected_angle
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_angle = st.session_state.angle_data['actual_angle']
    
    if selected_angle == correct_angle:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.estimate_difficulty < 3:
            st.session_state.estimate_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.estimate_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.estimate_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.angle_data
    user_choice = st.session_state.user_choice
    correct = data['actual_angle']
    
    if user_choice == correct:
        st.success(f"🎉 **Correct!** The angle measures {correct}°.")
        
        # Add educational note about angle type
        angle_type_info = {
            'acute': "This is an acute angle (less than 90°).",
            'right': "This is a right angle (exactly 90°).",
            'obtuse': "This is an obtuse angle (between 90° and 180°).",
            'straight': "This is a straight angle (exactly 180°)."
        }
        
        if data['angle_type'] in angle_type_info:
            st.info(f"📐 {angle_type_info[data['angle_type']]}")
        
        # Special recognition for perfect streaks
        if st.session_state.consecutive_correct == 3:
            st.balloons()
            st.info("🏆 **Great streak! Moving to the next level!**")
    else:
        difference = abs(user_choice - correct)
        st.error(f"❌ **Not quite.** You chose {user_choice}°, but the angle is {correct}°.")
        
        # Provide helpful explanation
        with st.expander("📖 **Understanding this angle**", expanded=True):
            st.markdown(f"""
            ### Angle Analysis:
            
            **Actual angle:** {correct}°
            **Your estimate:** {user_choice}°
            **Difference:** {difference}°
            
            ### How to recognize {correct}°:
            """)
            
            # Provide specific tips based on the angle
            if correct == 90:
                st.markdown("""
                - **Right angle** - forms a perfect square corner
                - Like the corner of a book or paper
                - Two perpendicular lines
                - Think of an "L" shape
                """)
            elif correct < 30:
                st.markdown(f"""
                - **Very acute angle** - quite narrow
                - Much less than half of a right angle
                - Think of a slightly opened door
                - About {correct/30:.1f} times a 30° angle
                """)
            elif correct < 60:
                st.markdown(f"""
                - **Acute angle** - less than 2/3 of a right angle
                - About {correct/45:.1f} times a 45° angle
                - Think of scissors slightly opened
                """)
            elif correct < 90:
                st.markdown(f"""
                - **Acute angle** - close to but less than a right angle
                - About {correct/90:.1%} of a right angle
                - Think of a door mostly opened
                """)
            elif correct < 120:
                st.markdown(f"""
                - **Obtuse angle** - wider than a right angle
                - {correct - 90}° more than a right angle
                - Think of an opened book
                """)
            elif correct < 150:
                st.markdown(f"""
                - **Obtuse angle** - much wider than a right angle
                - About {correct/90:.1f} times a right angle
                - Think of scissors widely opened
                """)
            else:
                st.markdown(f"""
                - **Very obtuse angle** - almost a straight line
                - Only {180 - correct}° away from a straight angle
                - Think of a door almost fully opened
                """)
            
            # Visual comparison tip
            st.markdown(f"""
            ### Visual tip:
            Compare your estimate ({user_choice}°) with the actual angle ({correct}°):
            - Your estimate was {difference}° {"too large" if user_choice > correct else "too small"}
            - {"Good estimate!" if difference <= 15 else "Try to visualize reference angles like 45°, 90°, and 135°"}
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_angle = None
    st.session_state.angle_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_choice = None
    if "selected_angle" in st.session_state:
        del st.session_state.selected_angle