import streamlit as st
import random
import math

def run():
    """
    Main function to run the Measure Angles with a Protractor activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/measure_angles_with_a_protractor.py
    """
    # Initialize session state
    if "protractor_difficulty" not in st.session_state:
        st.session_state.protractor_difficulty = 1  # 1=easy (10° multiples), 2=medium (5° multiples), 3=hard (any degree)
    
    if "current_protractor_angle" not in st.session_state:
        st.session_state.current_protractor_angle = None
        st.session_state.protractor_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Measure Angles with a Protractor")
    st.markdown("*Read angle measurements using a protractor*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (10° multiples)",
            2: "Medium (5° multiples)", 
            3: "Hard (any degree)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.protractor_difficulty]}")
        progress = (st.session_state.protractor_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.protractor_difficulty}/3")
    
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
    if st.session_state.current_protractor_angle is None:
        generate_new_protractor_angle()
    
    # Display the protractor problem
    display_protractor_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Read a Protractor:
        
        1. **Place the center point** of the protractor at the vertex of the angle
        2. **Align one ray** with the 0° line (baseline) of the protractor
        3. **Read the measurement** where the other ray crosses the protractor scale
        4. **Use the correct scale** - protractors have two scales (inner and outer)
        
        ### Reading Tips:
        - **Inner scale:** Starts from 0° on the right side
        - **Outer scale:** Starts from 0° on the left side
        - **Choose the scale** where one ray aligns with 0°
        - **Count by 10s** using the major marks
        - **Count by 1s** using the small marks
        
        ### Common Angles to Remember:
        - **0°:** Rays point in the same direction
        - **90°:** Right angle (perpendicular rays)
        - **180°:** Straight angle (opposite directions)
        - **45°:** Half of a right angle
        - **135°:** One and a half right angles
        
        ### Angle Types:
        - **Acute:** 0° < angle < 90°
        - **Right:** Exactly 90°
        - **Obtuse:** 90° < angle < 180°
        - **Straight:** Exactly 180°
        
        ### Common Mistakes to Avoid:
        - ❌ Reading from the wrong scale
        - ❌ Not aligning the vertex properly
        - ❌ Confusing 50° with 130° (or similar)
        - ✅ Always check: Does your answer make sense for the angle type?
        """)

def generate_new_protractor_angle():
    """Generate a new protractor angle based on difficulty level"""
    difficulty = st.session_state.protractor_difficulty
    
    # Define angle pools based on difficulty
    if difficulty == 1:  # Easy - multiples of 10°
        angle_pool = list(range(10, 180, 10))
    elif difficulty == 2:  # Medium - multiples of 5°
        angle_pool = list(range(5, 180, 5))
    else:  # Hard - any degree from 1° to 179°
        angle_pool = list(range(1, 180))
    
    # Choose angle
    angle_measure = random.choice(angle_pool)
    
    # Randomly decide if angle opens to right or left
    # This determines which scale to read from
    opens_right = random.choice([True, False])
    
    # Determine angle type
    if angle_measure < 90:
        angle_type = "acute"
    elif angle_measure == 90:
        angle_type = "right"
    elif angle_measure < 180:
        angle_type = "obtuse"
    else:
        angle_type = "straight"
    
    st.session_state.protractor_data = {
        'angle_measure': angle_measure,
        'opens_right': opens_right,
        'angle_type': angle_type
    }
    st.session_state.current_protractor_angle = angle_measure

def display_protractor_problem():
    """Display the protractor measurement problem"""
    data = st.session_state.protractor_data
    
    # Question text
    st.markdown(f"### What is the measurement of this angle?")
    
    # Create and display the protractor visualization
    create_protractor_visualization(data['angle_measure'], data['opens_right'])
    
    # Input field for answer
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create input field with submit button
        if not st.session_state.show_feedback:
            user_input = st.text_input(
                "Enter the angle measurement:",
                key="angle_input",
                placeholder="Type your answer in degrees",
                label_visibility="collapsed"
            )
            
            # Add degree symbol hint
            st.caption("Enter the number only (the ° symbol will be added automatically)")
            
            if st.button("Submit", type="primary", use_container_width=True):
                if user_input:
                    try:
                        answer = int(user_input)
                        if 0 <= answer <= 180:
                            submit_answer(answer)
                            st.rerun()
                        else:
                            st.error("Please enter an angle between 0° and 180°")
                    except ValueError:
                        st.error("Please enter a valid number")
                else:
                    st.warning("Please enter your answer")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_protractor_visualization(angle_measure, opens_right):
    """Create and display the protractor with angle - COMPLETELY MINIMAL VERSION"""
    import streamlit.components.v1 as components
    
    # Calculate angle positions
    if opens_right:
        # Angle opens to the right (use inner scale, starting from right)
        angle_rad = math.radians(angle_measure)
        end_x = 400 + 200 * math.cos(angle_rad)
        end_y = 350 - 200 * math.sin(angle_rad)
        baseline_end_x = 600
        baseline_end_y = 350
        arrow_angle = angle_rad
    else:
        # Angle opens to the left (use outer scale, starting from left)
        angle_rad = math.radians(180 - angle_measure)
        end_x = 400 + 200 * math.cos(angle_rad)
        end_y = 350 - 200 * math.sin(angle_rad)
        baseline_end_x = 200
        baseline_end_y = 350
        arrow_angle = math.radians(180 - angle_measure)
    
    # Create tick marks for the protractor
    tick_marks = []
    numbers_inner = []
    numbers_outer = []
    
    for deg in range(0, 181):
        rad = math.radians(deg)
        
        # Determine tick properties based on degree
        if deg % 10 == 0:
            # Major ticks (every 10 degrees)
            inner_radius = 170
            outer_radius = 195
            tick_width = 2
            tick_color = "#000"
        elif deg % 5 == 0:
            # Medium ticks (every 5 degrees)
            inner_radius = 180
            outer_radius = 195
            tick_width = 1.5
            tick_color = "#333"
        else:
            # Minor ticks (every degree)
            inner_radius = 188
            outer_radius = 195
            tick_width = 0.7
            tick_color = "#666"
        
        # Create tick mark
        x1 = 400 + inner_radius * math.cos(rad)
        y1 = 350 - inner_radius * math.sin(rad)
        x2 = 400 + outer_radius * math.cos(rad)
        y2 = 350 - outer_radius * math.sin(rad)
        
        tick_marks.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{tick_color}" stroke-width="{tick_width}"/>')
        
        # Add numbers for major marks (every 10 degrees)
        if deg % 10 == 0:
            # Inner scale numbers (0 on right)
            num_x_inner = 400 + 150 * math.cos(rad)
            num_y_inner = 350 - 150 * math.sin(rad)
            font_size = 16 if deg % 30 == 0 else 14
            font_weight = "bold" if deg == 0 or deg == 90 or deg == 180 else "normal"
            numbers_inner.append(f'<text x="{num_x_inner}" y="{num_y_inner + 5}" text-anchor="middle" font-size="{font_size}" font-weight="{font_weight}" fill="#333">{deg}</text>')
            
            # Outer scale numbers (0 on left)
            num_x_outer = 400 + 215 * math.cos(rad)
            num_y_outer = 350 - 215 * math.sin(rad)
            numbers_outer.append(f'<text x="{num_x_outer}" y="{num_y_outer + 5}" text-anchor="middle" font-size="{font_size}" font-weight="{font_weight}" fill="#666">{180 - deg}</text>')
    
    # Create complete HTML with SVG - NO FILLS OR BACKGROUNDS
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
        </style>
    </head>
    <body>
        <svg width="800" height="450" viewBox="0 0 800 450">
            <!-- White background -->
            <rect width="800" height="450" fill="white"/>
            
            <!-- Baseline (thicker and darker) -->
            <line x1="180" y1="350" x2="620" y2="350" stroke="#000" stroke-width="3"/>
            
            <!-- Center mark -->
            <line x1="400" y1="340" x2="400" y2="360" stroke="#000" stroke-width="3"/>
            <line x1="390" y1="350" x2="410" y2="350" stroke="#000" stroke-width="3"/>
            
            <!-- Tick marks -->
            {"".join(tick_marks)}
            
            <!-- Degree labels -->
            <g font-family="Arial, sans-serif">
                <!-- Inner scale numbers -->
                {"".join(numbers_inner)}
                
                <!-- Outer scale numbers -->
                {"".join(numbers_outer)}
            </g>
            
            <!-- Scale labels -->
            <text x="400" y="320" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Inner Scale</text>
            <text x="400" y="110" text-anchor="middle" font-size="13" fill="#666" font-weight="bold">Outer Scale</text>
            
            <!-- Angle rays (bold black lines) -->
            <line x1="400" y1="350" x2="{baseline_end_x}" y2="{baseline_end_y}" 
                  stroke="#000" stroke-width="4" stroke-linecap="round"/>
            <line x1="400" y1="350" x2="{end_x}" y2="{end_y}" 
                  stroke="#000" stroke-width="4" stroke-linecap="round"/>
            
            <!-- Arrow heads on rays -->
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="10" 
                        refX="9" refY="3" orient="auto">
                    <polygon points="0 0, 10 3, 0 6" fill="#000"/>
                </marker>
            </defs>
            
            <!-- Apply arrows to lines -->
            <line x1="400" y1="350" x2="{baseline_end_x - 5}" y2="{baseline_end_y}" 
                  stroke="none" stroke-width="4" marker-end="url(#arrowhead)"/>
            <line x1="400" y1="350" x2="{end_x - 5 * math.cos(arrow_angle)}" y2="{end_y + 5 * math.sin(arrow_angle)}" 
                  stroke="none" stroke-width="4" marker-end="url(#arrowhead)"/>
            
            <!-- Center point (placed last to be on top) -->
            <circle cx="400" cy="350" r="6" fill="#000"/>
        </svg>
    </body>
    </html>
    '''
    
    # Use Streamlit components to render the HTML
    components.html(html_content, height=470, scrolling=False)

def submit_answer(user_angle):
    """Process the submitted answer"""
    st.session_state.user_answer = user_angle
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_angle = st.session_state.protractor_data['angle_measure']
    
    # Allow for small margin of error at higher difficulties
    tolerance = 0 if st.session_state.protractor_difficulty == 1 else 1
    
    if abs(user_angle - correct_angle) <= tolerance:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.protractor_difficulty < 3:
            st.session_state.protractor_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.protractor_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.protractor_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.protractor_data
    user_answer = st.session_state.user_answer
    correct = data['angle_measure']
    
    tolerance = 0 if st.session_state.protractor_difficulty == 1 else 1
    
    if abs(user_answer - correct) <= tolerance:
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
        
        # Check for difficulty increase
        if st.session_state.consecutive_correct == 0 and st.session_state.protractor_difficulty == 3:
            st.balloons()
            st.info("🏆 **Excellent work! You're reading protractors like a pro!**")
    else:
        st.error(f"❌ **Not quite.** You answered {user_answer}°, but the correct answer is {correct}°.")
        
        # Provide helpful explanation
        with st.expander("📖 **See how to read this angle**", expanded=True):
            scale_used = "inner (bottom)" if data['opens_right'] else "outer (top)"
            baseline_side = "right" if data['opens_right'] else "left"
            
            st.markdown(f"""
            ### How to read this protractor:
            
            1. **Identify the baseline:** One ray lies along the baseline (horizontal line)
            2. **Find the 0° mark:** The baseline ray points to the {baseline_side}, so use the **{scale_used} scale**
            3. **Read the measurement:** Follow the other ray to where it crosses the protractor
            4. **The angle measures:** **{correct}°**
            
            ### Reading tip:
            - When the angle opens to the **{baseline_side}**, use the **{scale_used}** numbers
            - Count by 10s using the bold marks: {(correct // 10) * 10}°
            - Then add the remaining degrees: {correct % 10}°
            - Total: {(correct // 10) * 10}° + {correct % 10}° = **{correct}°**
            
            ### Common mistake to avoid:
            - If you got {180 - correct}°, you may have read from the wrong scale!
            - Always check: Does your answer match the angle type you see?
            - This angle looks {data['angle_type']}, and {correct}° is indeed {data['angle_type']}.
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_protractor_angle = None
    st.session_state.protractor_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_answer = None