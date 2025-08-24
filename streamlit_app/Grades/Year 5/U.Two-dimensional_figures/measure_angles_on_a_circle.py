import streamlit as st
import random
import math

def run():
    """
    Main function to run the Measure Angles on a Circle activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/measure_angles_on_a_circle.py
    """
    # Initialize session state
    if "angle_difficulty" not in st.session_state:
        st.session_state.angle_difficulty = 1  # 1=easy (multiples of 45°), 2=medium (multiples of 15°), 3=hard (any 5° multiple)
    
    if "current_angle" not in st.session_state:
        st.session_state.current_angle = None
        st.session_state.angle_data = {}
        st.session_state.show_feedback = False
        st.session_state.selected_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Measure Angles on a Circle")
    st.markdown("*Identify the measure of angles shown on a circle with 15° markings*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (45° multiples)",
            2: "Medium (15° multiples)", 
            3: "Hard (5° multiples)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.angle_difficulty]}")
        progress = (st.session_state.angle_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.angle_difficulty}/3")
    
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
    
    # Display the angle problem
    display_angle_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Measure Angles on a Circle:
        1. **Look at the shaded angle** shown in green
        2. **Count the dashes** - each dash represents 15°
        3. **Major marks** are at 0°, 90°, 180°, and 270°
        4. **Click the correct angle measurement** from the options
        
        ### Angle Types:
        - **Acute angle:** Less than 90°
        - **Right angle:** Exactly 90°
        - **Obtuse angle:** Between 90° and 180°
        - **Straight angle:** Exactly 180°
        - **Reflex angle:** Between 180° and 360°
        
        ### Tips for Counting:
        - Each small dash = 15°
        - From one major mark to the next = 90°
        - Half circle = 180°
        - Full circle = 360°
        
        ### Quick Reference:
        - 1 dash = 15°
        - 2 dashes = 30°
        - 3 dashes = 45°
        - 4 dashes = 60°
        - 5 dashes = 75°
        - 6 dashes = 90° (right angle)
        
        ### Difficulty Levels:
        - **Easy:** Angles at 45° intervals (0°, 45°, 90°, 135°, etc.)
        - **Medium:** Angles at 15° intervals (15°, 30°, 45°, 60°, etc.)
        - **Hard:** Angles at 5° intervals (5°, 10°, 15°, 20°, etc.)
        """)

def generate_new_angle():
    """Generate a new angle based on difficulty level"""
    difficulty = st.session_state.angle_difficulty
    
    # Define angle pools based on difficulty
    if difficulty == 1:  # Easy - multiples of 45°
        angle_pool = [45, 90, 135, 180, 225, 270, 315]
    elif difficulty == 2:  # Medium - multiples of 15°
        angle_pool = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 
                     195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345]
    else:  # Hard - multiples of 5°
        angle_pool = list(range(5, 360, 5))
    
    # Choose angle
    angle_measure = random.choice(angle_pool)
    
    # Randomly choose starting position (where the angle starts from)
    # For variety, don't always start from 0°
    start_positions = [0, 90, 180, 270]
    if difficulty >= 2:
        start_positions.extend([45, 135, 225, 315])
    if difficulty == 3:
        start_positions = list(range(0, 360, 15))
    
    start_angle = random.choice(start_positions)
    end_angle = (start_angle + angle_measure) % 360
    
    # Determine angle type for educational labeling
    if angle_measure < 90:
        angle_type = "acute"
    elif angle_measure == 90:
        angle_type = "right"
    elif angle_measure < 180:
        angle_type = "obtuse"
    elif angle_measure == 180:
        angle_type = "straight"
    elif angle_measure < 360:
        angle_type = "reflex"
    else:
        angle_type = "full"
    
    # Generate answer options (including the correct answer)
    options = generate_answer_options(angle_measure, difficulty)
    
    st.session_state.angle_data = {
        'angle_measure': angle_measure,
        'start_angle': start_angle,
        'end_angle': end_angle,
        'angle_type': angle_type,
        'options': options
    }
    st.session_state.current_angle = angle_measure

def generate_answer_options(correct_angle, difficulty):
    """Generate multiple choice options"""
    options = [correct_angle]
    
    # Generate plausible distractors
    if difficulty == 1:
        # For easy, use other 45° multiples
        candidates = [45, 90, 135, 180, 225, 270, 315]
    elif difficulty == 2:
        # For medium, use nearby 15° multiples
        candidates = list(range(15, 360, 15))
    else:
        # For hard, use nearby 5° multiples
        candidates = list(range(5, 360, 5))
    
    # Remove correct answer from candidates
    candidates = [c for c in candidates if c != correct_angle]
    
    # Add some close distractors
    for offset in [-30, -15, 15, 30]:
        distractor = correct_angle + offset
        if 0 < distractor < 360 and distractor in candidates:
            if distractor not in options:
                options.append(distractor)
    
    # Add random distractors if needed
    while len(options) < 6:
        distractor = random.choice(candidates)
        if distractor not in options:
            options.append(distractor)
    
    # Take first 6 options and shuffle
    options = options[:6]
    random.shuffle(options)
    
    return options

def display_angle_problem():
    """Display the angle measurement problem"""
    data = st.session_state.angle_data
    
    # Question text
    angle_type_text = f" ({data['angle_type']} angle)" if not st.session_state.show_feedback else ""
    st.markdown(f"### What is the measure of this angle{angle_type_text}? The dashes are 15° apart.")
    
    # Create and display the angle visualization
    create_angle_visualization(data['start_angle'], data['end_angle'], data['angle_measure'])
    
    # Display answer options as clickable tiles
    st.markdown("### Select your answer:")
    
    # Create 2 rows of 3 tiles each
    options = data['options']
    
    for row in range(2):
        cols = st.columns(3)
        for col_idx in range(3):
            option_idx = row * 3 + col_idx
            if option_idx < len(options):
                with cols[col_idx]:
                    option = options[option_idx]
                    # Create button for each option
                    button_key = f"option_{option}_{st.session_state.total_attempted}"
                    
                    # Style based on feedback state
                    if st.session_state.show_feedback:
                        if option == data['angle_measure']:
                            button_type = "primary"  # Correct answer in green
                            label = f"✅ {option}°"
                        elif option == st.session_state.selected_answer:
                            button_type = "secondary"  # Wrong selected answer
                            label = f"❌ {option}°"
                        else:
                            button_type = "secondary"
                            label = f"{option}°"
                        disabled = True
                    else:
                        button_type = "secondary"
                        label = f"{option}°"
                        disabled = False
                    
                    if st.button(label, key=button_key, type=button_type, 
                                disabled=disabled, use_container_width=True):
                        if not st.session_state.show_feedback:
                            submit_answer(option)
                            st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_angle_visualization(start_angle, end_angle, angle_measure):
    """Create and display the angle on a circle using Streamlit components"""
    import streamlit.components.v1 as components
    
    # Convert angles to radians for calculations
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Calculate arc path
    large_arc = 1 if angle_measure > 180 else 0
    
    # Calculate start and end points on circle (radius = 120)
    start_x = 200 + 120 * math.cos(start_rad)
    start_y = 200 - 120 * math.sin(start_rad)
    end_x = 200 + 120 * math.cos(end_rad)
    end_y = 200 - 120 * math.sin(end_rad)
    
    # Create dash marks every 15 degrees
    dash_marks = []
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        x1 = 200 + 110 * math.cos(rad)
        y1 = 200 - 110 * math.sin(rad)
        x2 = 200 + 120 * math.cos(rad)
        y2 = 200 - 120 * math.sin(rad)
        
        # Major marks at 0, 90, 180, 270
        if deg % 90 == 0:
            stroke_width = 2
            x1 = 200 + 105 * math.cos(rad)
            y1 = 200 - 105 * math.sin(rad)
        else:
            stroke_width = 1
        
        dash_marks.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#666" stroke-width="{stroke_width}"/>')
    
    # Create complete HTML with SVG
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 400px;
            }}
        </style>
    </head>
    <body>
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Background circle -->
            <circle cx="200" cy="200" r="120" fill="white" stroke="#ccc" stroke-width="2"/>
            
            <!-- Angle sector (filled) -->
            <path d="M 200 200 L {start_x} {start_y} A 120 120 0 {large_arc} 0 {end_x} {end_y} Z"
                  fill="#4CAF50" fill-opacity="0.3" stroke="#4CAF50" stroke-width="2"/>
            
            <!-- Center point -->
            <circle cx="200" cy="200" r="4" fill="#333"/>
            
            <!-- Dash marks -->
            {"".join(dash_marks)}
            
            <!-- Angle rays -->
            <line x1="200" y1="200" x2="{start_x}" y2="{start_y}" stroke="#4CAF50" stroke-width="3"/>
            <line x1="200" y1="200" x2="{end_x}" y2="{end_y}" stroke="#4CAF50" stroke-width="3"/>
            
            <!-- Angle arc for small angles -->
            {f'<path d="M {200 + 30 * math.cos(start_rad)} {200 - 30 * math.sin(start_rad)} A 30 30 0 {large_arc} 0 {200 + 30 * math.cos(end_rad)} {200 - 30 * math.sin(end_rad)}" fill="none" stroke="#4CAF50" stroke-width="2"/>' if angle_measure <= 90 else ''}
            
            <!-- Cardinal direction labels -->
            <text x="330" y="205" text-anchor="start" font-size="14" fill="#666">0°</text>
            <text x="195" y="75" text-anchor="middle" font-size="14" fill="#666">90°</text>
            <text x="70" y="205" text-anchor="end" font-size="14" fill="#666">180°</text>
            <text x="195" y="335" text-anchor="middle" font-size="14" fill="#666">270°</text>
        </svg>
    </body>
    </html>
    '''
    
    # Use Streamlit components to render the HTML
    components.html(html_content, height=420, scrolling=False)

def submit_answer(selected_angle):
    """Process the submitted answer"""
    st.session_state.selected_answer = selected_angle
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_angle = st.session_state.angle_data['angle_measure']
    
    if selected_angle == correct_angle:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.angle_difficulty < 3:
            st.session_state.angle_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 2 wrong in recent attempts
        if st.session_state.angle_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.angle_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.angle_data
    selected = st.session_state.selected_answer
    correct = data['angle_measure']
    
    if selected == correct:
        st.success(f"🎉 **Correct!** The angle measures {correct}°.")
        
        # Add educational note about angle type
        angle_type_info = {
            'acute': "This is an acute angle (less than 90°).",
            'right': "This is a right angle (exactly 90°).",
            'obtuse': "This is an obtuse angle (between 90° and 180°).",
            'straight': "This is a straight angle (exactly 180°).",
            'reflex': "This is a reflex angle (between 180° and 360°)."
        }
        
        if data['angle_type'] in angle_type_info:
            st.info(f"📐 {angle_type_info[data['angle_type']]}")
        
        # Check for difficulty increase
        if st.session_state.consecutive_correct == 0 and st.session_state.angle_difficulty == 3:
            st.balloons()
            st.info("🏆 **Excellent work at the highest difficulty level!**")
    else:
        st.error(f"❌ **Not quite.** You selected {selected}°, but the correct answer is {correct}°.")
        
        # Provide helpful explanation
        with st.expander("📖 **See explanation**", expanded=True):
            st.markdown(f"""
            ### How to find {correct}°:
            
            1. **Starting ray:** The angle starts from the {data['start_angle']}° position
            2. **Ending ray:** The angle ends at the {data['end_angle']}° position
            3. **Calculation:** The angle measure is the difference between these positions
            
            **Counting method:**
            - Each dash mark represents 15°
            - From the starting ray to the ending ray, there are {correct // 15} dashes {f"(and {correct % 15}° more)" if correct % 15 != 0 else ""}
            - {f"{correct // 15} × 15°" if correct % 15 == 0 else f"{correct // 15} × 15° + {correct % 15}°"} = {correct}°
            
            **Angle type:** This is {'an' if data['angle_type'] in ['acute', 'obtuse'] else 'a'} **{data['angle_type']} angle**
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_angle = None
    st.session_state.angle_data = {}
    st.session_state.show_feedback = False
    st.session_state.selected_answer = None