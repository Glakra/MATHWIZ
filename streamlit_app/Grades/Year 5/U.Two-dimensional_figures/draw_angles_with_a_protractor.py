import streamlit as st
import random
import math

def run():
    """
    Main function to run the Draw Angles with a Protractor activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/draw_angles_with_a_protractor.py
    """
    # Initialize session state
    if "draw_angle_difficulty" not in st.session_state:
        st.session_state.draw_angle_difficulty = 1  # 1=easy (10° multiples), 2=medium (5° multiples), 3=hard (any degree)
    
    if "target_angle" not in st.session_state:
        st.session_state.target_angle = None
        st.session_state.angle_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_angle = 0
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Draw Angles with a Protractor")
    st.markdown("*Use the protractor to create angles of specific measurements*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (10° multiples, ±3° tolerance)",
            2: "Medium (5° multiples, ±2° tolerance)", 
            3: "Hard (any degree, ±1° tolerance)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.draw_angle_difficulty]}")
        progress = (st.session_state.draw_angle_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.draw_angle_difficulty}/3")
    
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
    if st.session_state.target_angle is None:
        generate_new_target_angle()
    
    # Display the angle drawing problem
    display_angle_drawing_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Draw Angles with a Protractor:
        
        1. **Read the target angle** shown at the top
        2. **Drag the blue/red dot** along the protractor arc
        3. **Watch the angle measurement** update as you drag
        4. **Note the angle shown** above the protractor
        5. **Enter it in the box** below (it should auto-fill)
        6. **Click Submit** to check your answer
        
        ### Drawing Tips:
        - **Start from the baseline** (horizontal line)
        - **Drag slowly** for precise control
        - **Use the tick marks** as guides
        - **Count by 10s** for the major marks
        - **Fine-tune** using the small marks
        
        ### Accuracy Requirements:
        - **Easy mode:** Within ±3° of target
        - **Medium mode:** Within ±2° of target
        - **Hard mode:** Within ±1° of target
        
        ### Common Angles to Practice:
        - **45°:** Half of a right angle
        - **90°:** Right angle (vertical)
        - **135°:** One and a half right angles
        - **180°:** Straight angle (opposite direction)
        
        ### Pro Tips:
        - 🎯 Look for the nearest 10° mark first
        - 📏 Then count the smaller divisions
        - 🔄 You can adjust multiple times before submitting
        - ✨ The angle updates automatically as you drag!
        """)

def generate_new_target_angle():
    """Generate a new target angle based on difficulty level"""
    difficulty = st.session_state.draw_angle_difficulty
    
    # Define angle pools based on difficulty
    if difficulty == 1:  # Easy - multiples of 10°
        angle_pool = list(range(10, 180, 10))
    elif difficulty == 2:  # Medium - multiples of 5°
        angle_pool = list(range(5, 180, 5))
    else:  # Hard - any degree from 1° to 179°
        angle_pool = list(range(1, 180))
    
    # Choose angle
    target_angle = random.choice(angle_pool)
    
    # Randomly decide if arrow starts from right or left
    starts_from_right = random.choice([True, False])
    
    # Determine angle type for educational purposes
    if target_angle < 90:
        angle_type = "acute"
    elif target_angle == 90:
        angle_type = "right"
    elif target_angle < 180:
        angle_type = "obtuse"
    else:
        angle_type = "straight"
    
    st.session_state.angle_data = {
        'target_angle': target_angle,
        'starts_from_right': starts_from_right,
        'angle_type': angle_type
    }
    st.session_state.target_angle = target_angle

def display_angle_drawing_problem():
    """Display the interactive angle drawing problem"""
    data = st.session_state.angle_data
    
    # Question text
    st.markdown(f"### Use the protractor to make a {data['target_angle']}° angle.")
    
    # Create and display the interactive protractor
    create_interactive_protractor(data['target_angle'], data['starts_from_right'])
    
    # Input field for the angle
    if not st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### What angle did you draw?")
            
            # Number input for the angle
            user_input = st.number_input(
                "Enter the angle shown on the protractor:",
                min_value=0,
                max_value=180,
                value=0,
                step=1,
                key="angle_input",
                help="Look at the angle displayed above the protractor and enter it here"
            )
            
            # Show feedback based on current input
            if user_input > 0:
                target = data['target_angle']
                diff = abs(user_input - target)
                
                # Determine tolerance
                if st.session_state.draw_angle_difficulty == 1:
                    tolerance = 3
                elif st.session_state.draw_angle_difficulty == 2:
                    tolerance = 2
                else:
                    tolerance = 1
                
                # Visual feedback
                if diff <= tolerance:
                    st.success(f"🟢 **Perfect! You're within tolerance!**")
                elif diff <= tolerance * 2:
                    st.warning(f"🟡 **Close! Adjust by {diff - tolerance}° more**")
                else:
                    st.info(f"🔴 **Keep adjusting! Off by {diff}°**")
            
            # Submit button
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if user_input > 0:
                    submit_answer(user_input)
                    st.rerun()
                else:
                    st.warning("Please draw an angle first and enter its measurement")
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_interactive_protractor(target_angle, starts_from_right):
    """Create an interactive protractor with draggable arrow"""
    import streamlit.components.v1 as components
    
    # Determine which side the fixed ray is on
    if starts_from_right:
        arrow_color = "#2196F3"  # Blue arrow for right side
    else:
        arrow_color = "#F44336"  # Red arrow for left side
    
    # Create HTML with interactive JavaScript
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                background: white;
                font-family: Arial, sans-serif;
            }}
            #protractor-container {{
                position: relative;
                cursor: pointer;
            }}
            .draggable {{
                cursor: move;
            }}
            #current-angle {{
                font-size: 28px;
                font-weight: bold;
                color: {arrow_color};
                margin-bottom: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div id="current-angle">Current Angle: 0°</div>
        <div id="protractor-container">
            <svg width="800" height="450" viewBox="0 0 800 450" id="protractor-svg">
                <!-- White background -->
                <rect width="800" height="450" fill="white"/>
                
                <!-- Protractor outline (subtle) -->
                <path d="M 200 350 A 200 200 0 0 0 600 350 Z"
                      fill="none" stroke="#ddd" stroke-width="2" opacity="0.5"/>
                
                <!-- Baseline -->
                <line x1="180" y1="350" x2="620" y2="350" stroke="#000" stroke-width="3"/>
                
                <!-- Center marks -->
                <line x1="400" y1="340" x2="400" y2="360" stroke="#000" stroke-width="3"/>
                <line x1="390" y1="350" x2="410" y2="350" stroke="#000" stroke-width="3"/>
                
                <!-- Tick marks will be added here -->
                <g id="tick-marks"></g>
                
                <!-- Numbers will be added here -->
                <g id="numbers" font-family="Arial, sans-serif"></g>
                
                <!-- Scale labels -->
                <text x="400" y="320" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">Inner Scale</text>
                <text x="400" y="110" text-anchor="middle" font-size="13" fill="#666" font-weight="bold">Outer Scale</text>
                
                <!-- Fixed ray (baseline) -->
                <line x1="400" y1="350" 
                      x2="{600 if starts_from_right else 200}" 
                      y2="350" 
                      stroke="#000" stroke-width="4" stroke-linecap="round"/>
                
                <!-- Arrow on fixed ray -->
                <polygon points="{595 if starts_from_right else 205},345 {595 if starts_from_right else 205},355 {605 if starts_from_right else 195},350" 
                         fill="#000"/>
                
                <!-- Draggable ray -->
                <line id="draggable-ray" 
                      x1="400" y1="350" 
                      x2="{600 if starts_from_right else 200}" 
                      y2="350" 
                      stroke="{arrow_color}" stroke-width="4" stroke-linecap="round"
                      class="draggable"/>
                
                <!-- Arrow indicator -->
                <circle id="drag-handle" 
                        cx="{600 if starts_from_right else 200}" 
                        cy="350" 
                        r="12" 
                        fill="{arrow_color}" 
                        stroke="white" 
                        stroke-width="2"
                        class="draggable"
                        style="cursor: move;">
                    <title>Drag me!</title>
                </circle>
                
                <!-- Center point -->
                <circle cx="400" cy="350" r="6" fill="#000"/>
                
                <!-- Live angle display on the protractor -->
                <text id="live-angle" x="400" y="280" text-anchor="middle" 
                      font-size="24" font-weight="bold" fill="{arrow_color}">0°</text>
            </svg>
        </div>
        
        <script>
            let currentAngle = 0;
            let isDragging = false;
            let startsFromRight = {str(starts_from_right).lower()};
            let targetAngle = {target_angle};
            
            // Create tick marks and numbers
            function createProtractorMarks() {{
                const tickGroup = document.getElementById('tick-marks');
                const numberGroup = document.getElementById('numbers');
                
                for (let deg = 0; deg <= 180; deg++) {{
                    const rad = deg * Math.PI / 180;
                    let innerRadius, outerRadius, strokeWidth, strokeColor;
                    
                    // Determine tick properties
                    if (deg % 10 === 0) {{
                        innerRadius = 170;
                        outerRadius = 195;
                        strokeWidth = 2;
                        strokeColor = '#000';
                        
                        // Add numbers for major marks - Inner scale
                        const numX = 400 + 150 * Math.cos(rad);
                        const numY = 350 - 150 * Math.sin(rad);
                        
                        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                        text.setAttribute('x', numX);
                        text.setAttribute('y', numY + 5);
                        text.setAttribute('text-anchor', 'middle');
                        text.setAttribute('font-size', deg % 30 === 0 ? '16' : '14');
                        text.setAttribute('font-weight', (deg === 0 || deg === 90 || deg === 180) ? 'bold' : 'normal');
                        text.setAttribute('fill', '#333');
                        text.textContent = deg;
                        numberGroup.appendChild(text);
                        
                        // Add numbers for major marks - Outer scale
                        const numX2 = 400 + 215 * Math.cos(rad);
                        const numY2 = 350 - 215 * Math.sin(rad);
                        
                        const text2 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                        text2.setAttribute('x', numX2);
                        text2.setAttribute('y', numY2 + 5);
                        text2.setAttribute('text-anchor', 'middle');
                        text2.setAttribute('font-size', deg % 30 === 0 ? '16' : '14');
                        text2.setAttribute('font-weight', (deg === 0 || deg === 90 || deg === 180) ? 'bold' : 'normal');
                        text2.setAttribute('fill', '#666');
                        text2.textContent = 180 - deg;
                        numberGroup.appendChild(text2);
                    }} else if (deg % 5 === 0) {{
                        innerRadius = 180;
                        outerRadius = 195;
                        strokeWidth = 1.5;
                        strokeColor = '#333';
                    }} else {{
                        innerRadius = 188;
                        outerRadius = 195;
                        strokeWidth = 0.7;
                        strokeColor = '#666';
                    }}
                    
                    // Create tick mark
                    const x1 = 400 + innerRadius * Math.cos(rad);
                    const y1 = 350 - innerRadius * Math.sin(rad);
                    const x2 = 400 + outerRadius * Math.cos(rad);
                    const y2 = 350 - outerRadius * Math.sin(rad);
                    
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', x1);
                    line.setAttribute('y1', y1);
                    line.setAttribute('x2', x2);
                    line.setAttribute('y2', y2);
                    line.setAttribute('stroke', strokeColor);
                    line.setAttribute('stroke-width', strokeWidth);
                    tickGroup.appendChild(line);
                }}
            }}
            
            // Update the draggable ray position
            function updateRay(angle) {{
                const ray = document.getElementById('draggable-ray');
                const handle = document.getElementById('drag-handle');
                const liveAngle = document.getElementById('live-angle');
                const currentAngleDisplay = document.getElementById('current-angle');
                
                // Calculate actual angle based on starting side
                let actualAngle = angle;
                if (!startsFromRight) {{
                    actualAngle = 180 - angle;
                }}
                
                const rad = actualAngle * Math.PI / 180;
                const x = 400 + 200 * Math.cos(rad);
                const y = 350 - 200 * Math.sin(rad);
                
                ray.setAttribute('x2', x);
                ray.setAttribute('y2', y);
                handle.setAttribute('cx', x);
                handle.setAttribute('cy', y);
                
                currentAngle = Math.round(angle);
                liveAngle.textContent = currentAngle + '°';
                currentAngleDisplay.textContent = 'Current Angle: ' + currentAngle + '°';
                
                // Add visual feedback based on proximity to target
                const diff = Math.abs(currentAngle - targetAngle);
                if (diff <= 1) {{
                    currentAngleDisplay.style.color = '#4CAF50'; // Green
                }} else if (diff <= 3) {{
                    currentAngleDisplay.style.color = '#FF9800'; // Orange
                }} else {{
                    currentAngleDisplay.style.color = '{arrow_color}'; // Default
                }}
            }}
            
            // Handle mouse/touch events
            function handleStart(e) {{
                isDragging = true;
                e.preventDefault();
            }}
            
            function handleMove(e) {{
                if (!isDragging) return;
                
                const svg = document.getElementById('protractor-svg');
                const pt = svg.createSVGPoint();
                
                if (e.touches) {{
                    pt.x = e.touches[0].clientX;
                    pt.y = e.touches[0].clientY;
                }} else {{
                    pt.x = e.clientX;
                    pt.y = e.clientY;
                }}
                
                const cursorPoint = pt.matrixTransform(svg.getScreenCTM().inverse());
                
                // Calculate angle from center
                const dx = cursorPoint.x - 400;
                const dy = 350 - cursorPoint.y;
                let angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                // Ensure angle is positive and within 0-180
                if (angle < 0) angle = 0;
                if (angle > 180) angle = 180;
                
                // Adjust for starting side
                if (!startsFromRight) {{
                    angle = 180 - angle;
                }}
                
                updateRay(angle);
            }}
            
            function handleEnd(e) {{
                isDragging = false;
            }}
            
            // Initialize
            createProtractorMarks();
            
            // Add event listeners
            const handle = document.getElementById('drag-handle');
            const svg = document.getElementById('protractor-svg');
            
            // Mouse events
            handle.addEventListener('mousedown', handleStart);
            svg.addEventListener('mousemove', handleMove);
            svg.addEventListener('mouseup', handleEnd);
            svg.addEventListener('mouseleave', handleEnd);
            
            // Touch events for mobile
            handle.addEventListener('touchstart', handleStart);
            svg.addEventListener('touchmove', handleMove);
            svg.addEventListener('touchend', handleEnd);
            
            // Also allow clicking anywhere on the protractor to set angle
            svg.addEventListener('click', function(e) {{
                if (e.target === handle) return; // Don't double-process handle clicks
                
                const pt = svg.createSVGPoint();
                pt.x = e.clientX;
                pt.y = e.clientY;
                const cursorPoint = pt.matrixTransform(svg.getScreenCTM().inverse());
                
                // Calculate angle from center
                const dx = cursorPoint.x - 400;
                const dy = 350 - cursorPoint.y;
                let angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                // Ensure angle is positive and within 0-180
                if (angle < 0) angle = 0;
                if (angle > 180) angle = 180;
                
                // Adjust for starting side
                if (!startsFromRight) {{
                    angle = 180 - angle;
                }}
                
                updateRay(angle);
            }});
        </script>
    </body>
    </html>
    '''
    
    # Display the interactive component (no return value expected)
    components.html(html_content, height=550, scrolling=False)

def submit_answer(user_input):
    """Process the submitted answer"""
    st.session_state.user_angle = user_input
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    target_angle = st.session_state.angle_data['target_angle']
    
    # Determine tolerance based on difficulty
    if st.session_state.draw_angle_difficulty == 1:
        tolerance = 3  # Easy - within 3 degrees
    elif st.session_state.draw_angle_difficulty == 2:
        tolerance = 2  # Medium - within 2 degrees
    else:
        tolerance = 1  # Hard - within 1 degree
    
    if abs(user_input - target_angle) <= tolerance:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.draw_angle_difficulty < 3:
            st.session_state.draw_angle_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.draw_angle_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.draw_angle_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.angle_data
    user_angle = st.session_state.user_angle
    target = data['target_angle']
    
    # Determine tolerance based on difficulty
    if st.session_state.draw_angle_difficulty == 1:
        tolerance = 3
    elif st.session_state.draw_angle_difficulty == 2:
        tolerance = 2
    else:
        tolerance = 1
    
    difference = abs(user_angle - target)
    
    if difference <= tolerance:
        st.success(f"🎉 **Excellent!** You drew a {user_angle}° angle. Target was {target}°.")
        
        if difference == 0:
            st.balloons()
            st.info("🎯 **PERFECT! Exactly on target!**")
        elif difference == 1:
            st.info("🎯 **Almost perfect! Just 1° off!**")
        
        # Add educational note about angle type
        angle_type_info = {
            'acute': "You successfully drew an acute angle (less than 90°)!",
            'right': "Perfect! You drew a right angle (exactly 90°)!",
            'obtuse': "Great job! You drew an obtuse angle (between 90° and 180°)!",
            'straight': "Excellent! You drew a straight angle (exactly 180°)!"
        }
        
        if data['angle_type'] in angle_type_info:
            st.info(f"📐 {angle_type_info[data['angle_type']]}")
        
        # Check for difficulty increase
        if st.session_state.consecutive_correct == 0 and st.session_state.draw_angle_difficulty == 3:
            st.info("🏆 **Amazing! You're drawing angles with perfect precision!**")
    else:
        st.error(f"❌ **Not quite.** You drew {user_angle}°, but the target was {target}°. (Off by {difference}°)")
        
        # Provide helpful guidance
        with st.expander("📖 **Tips for drawing angles accurately**", expanded=True):
            direction = "right" if user_angle < target else "left"
            
            st.markdown(f"""
            ### How to draw {target}° accurately:
            
            1. **Find the nearest 10° mark:** {(target // 10) * 10}°
            2. **Count the additional degrees:** {target % 10}°
            3. **Total:** {(target // 10) * 10}° + {target % 10}° = {target}°
            
            ### Your attempt:
            - You drew: **{user_angle}°**
            - Target was: **{target}°**
            - Difference: **{difference}°** too {'small' if user_angle < target else 'large'}
            
            ### To improve:
            - Move the arrow **{difference}° to the {direction}**
            - {"You were very close! Just a tiny adjustment needed." if difference <= 5 else "Take your time and use the tick marks as guides."}
            - Each small tick = 1°
            - Each medium tick = 5°
            - Each large tick with number = 10°
            
            ### Angle type:
            - Target angle ({target}°) is {'an' if data['angle_type'] in ['acute', 'obtuse'] else 'a'} **{data['angle_type']} angle**
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.target_angle = None
    st.session_state.angle_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_angle = 0