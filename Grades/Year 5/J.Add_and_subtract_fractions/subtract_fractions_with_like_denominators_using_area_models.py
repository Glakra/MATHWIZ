import streamlit as st
import random

def run():
    """
    Main function to run the Subtract Fractions with Area Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/subtract_fractions_with_like_denominators_using_area_models.py
    """
    # Initialize session state for difficulty and game state
    if "subtract_area_difficulty" not in st.session_state:
        st.session_state.subtract_area_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions Using Area Models")
    st.markdown("*Use the pictures to subtract*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.subtract_area_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (denominators 2-4)",
            2: "Simple (denominators 4-6)", 
            3: "Medium (denominators 6-8)",
            4: "Advanced (denominators 8-10)",
            5: "Expert (denominators 10-12)"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Subtract Fractions Using Pictures:
        
        1. **Look at the first shape** - Count the shaded parts
        2. **Look at the second shape** - This shows what to take away
        3. **Imagine removing** - Take away the second amount from the first
        4. **Count what's left** - That's your answer!
        
        ### Example:
        - First shape: 5/6 shaded (5 parts colored)
        - Second shape: 2/6 shaded (2 parts to remove)
        - Subtract: 5 - 2 = 3 parts left
        - Answer: 3/6
        
        ### Remember:
        - The shapes are divided into the same number of parts
        - Only subtract the shaded amounts
        - The denominator (bottom number) stays the same
        """)

def generate_new_question():
    """Generate a new area model subtraction question"""
    difficulty = st.session_state.subtract_area_difficulty
    
    # Set denominator range based on difficulty
    if difficulty == 1:
        denominator = random.choice([2, 3, 4])
    elif difficulty == 2:
        denominator = random.choice([4, 5, 6])
    elif difficulty == 3:
        denominator = random.choice([6, 7, 8])
    elif difficulty == 4:
        denominator = random.choice([8, 9, 10])
    else:  # difficulty == 5
        denominator = random.choice([10, 11, 12])
    
    # Generate numerators (ensure first > second for positive result)
    numerator1 = random.randint(2, denominator - 1)
    numerator2 = random.randint(1, numerator1 - 1)
    
    # Calculate the difference
    diff_numerator = numerator1 - numerator2
    
    # Choose shape type
    shapes = ["circle", "rectangle", "square", "hexagon"]
    if difficulty >= 3:
        shapes.extend(["triangle", "pentagon"])
    shape_type = random.choice(shapes)
    
    # Choose color
    colors = [
        ("#FF6B6B", "#FFE0E0", "pink"),
        ("#4ECDC4", "#E0F7F7", "teal"),
        ("#45B7D1", "#E0F2F7", "blue"),
        ("#96CEB4", "#E8F5E8", "green"),
        ("#FECA57", "#FFF5E0", "yellow"),
        ("#9B59B6", "#F0E6F5", "purple"),
        ("#FF9FF3", "#FFE6F9", "magenta"),
        ("#54A0FF", "#E6F0FF", "sky blue")
    ]
    color_scheme = random.choice(colors)
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "diff_numerator": diff_numerator,
        "shape_type": shape_type,
        "fill_color": color_scheme[0],
        "empty_color": color_scheme[1],
        "color_name": color_scheme[2]
    }
    
    st.session_state.correct_answer = diff_numerator
    st.session_state.current_question = "Use the pictures to subtract."

def create_shape_svg(shape_type, numerator, denominator, fill_color, empty_color):
    """Create an SVG shape with fractional shading"""
    if shape_type == "circle":
        return create_circle_svg(numerator, denominator, fill_color, empty_color)
    elif shape_type == "rectangle":
        return create_rectangle_svg(numerator, denominator, fill_color, empty_color)
    elif shape_type == "square":
        return create_square_svg(numerator, denominator, fill_color, empty_color)
    elif shape_type == "hexagon":
        return create_hexagon_svg(numerator, denominator, fill_color, empty_color)
    elif shape_type == "triangle":
        return create_triangle_svg(numerator, denominator, fill_color, empty_color)
    elif shape_type == "pentagon":
        return create_pentagon_svg(numerator, denominator, fill_color, empty_color)

def create_circle_svg(numerator, denominator, fill_color, empty_color):
    """Create a circle (pie chart) with fractional shading"""
    svg = '<svg width="150" height="150" viewBox="0 0 150 150">'
    
    # Calculate angles
    angle_per_slice = 360 / denominator
    
    # Draw each slice
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90  # Start from top
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = start_angle * 3.14159 / 180
        end_rad = end_angle * 3.14159 / 180
        
        # Calculate points
        x1 = 75 + 60 * float(f"{float(f'{start_rad:.3f}'):g}")
        y1 = 75 + 60 * float(f"{float(f'{start_rad:.3f}'):g}")
        x2 = 75 + 60 * float(f"{float(f'{end_rad:.3f}'):g}")
        y2 = 75 + 60 * float(f"{float(f'{end_rad:.3f}'):g}")
        
        # Use simple calculation for coordinates
        import math
        x1 = 75 + 60 * math.cos(start_rad)
        y1 = 75 + 60 * math.sin(start_rad)
        x2 = 75 + 60 * math.cos(end_rad)
        y2 = 75 + 60 * math.sin(end_rad)
        
        # Determine if large arc
        large_arc = 0 if angle_per_slice <= 180 else 1
        
        # Choose color
        color = fill_color if i < numerator else empty_color
        
        # Create path
        path = f'<path d="M 75 75 L {x1:.1f} {y1:.1f} A 60 60 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z" '
        path += f'fill="{color}" stroke="#333" stroke-width="2"/>'
        svg += path
    
    svg += '</svg>'
    return svg

def create_rectangle_svg(numerator, denominator, fill_color, empty_color):
    """Create a rectangle divided into equal parts"""
    svg = '<svg width="150" height="100" viewBox="0 0 150 100">'
    
    # Determine grid layout
    if denominator <= 4:
        cols = denominator
        rows = 1
    elif denominator <= 6:
        cols = 3
        rows = 2
    elif denominator <= 8:
        cols = 4
        rows = 2
    elif denominator <= 9:
        cols = 3
        rows = 3
    else:
        cols = 4
        rows = 3
    
    # Calculate cell dimensions
    cell_width = 120 / cols
    cell_height = 80 / rows
    
    # Draw cells
    cell_count = 0
    for row in range(rows):
        for col in range(cols):
            if cell_count < denominator:
                x = 15 + col * cell_width
                y = 10 + row * cell_height
                color = fill_color if cell_count < numerator else empty_color
                
                rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" '
                rect += f'fill="{color}" stroke="#333" stroke-width="2"/>'
                svg += rect
                
                cell_count += 1
    
    svg += '</svg>'
    return svg

def create_square_svg(numerator, denominator, fill_color, empty_color):
    """Create a square divided into equal parts"""
    svg = '<svg width="120" height="120" viewBox="0 0 120 120">'
    
    # Determine grid layout
    if denominator == 4:
        size = 2
    elif denominator <= 9:
        size = 3
    else:
        size = 4
    
    cell_size = 100 / size
    
    # Draw cells
    cell_count = 0
    for row in range(size):
        for col in range(size):
            if cell_count < denominator:
                x = 10 + col * cell_size
                y = 10 + row * cell_size
                color = fill_color if cell_count < numerator else empty_color
                
                rect = f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                rect += f'fill="{color}" stroke="#333" stroke-width="2"/>'
                svg += rect
                
                cell_count += 1
    
    svg += '</svg>'
    return svg

def create_hexagon_svg(numerator, denominator, fill_color, empty_color):
    """Create a hexagon divided into triangular sections"""
    svg = '<svg width="150" height="150" viewBox="0 0 150 150">'
    
    # Draw triangular sections from center
    angle_per_section = 360 / denominator
    
    for i in range(denominator):
        angle = i * angle_per_section
        next_angle = (i + 1) * angle_per_section
        
        # Convert to radians
        import math
        angle_rad = angle * math.pi / 180
        next_angle_rad = next_angle * math.pi / 180
        
        # Calculate points (adjusted for hexagon vertices)
        x1 = 75 + 55 * math.cos(angle_rad - math.pi/2)
        y1 = 75 + 55 * math.sin(angle_rad - math.pi/2)
        x2 = 75 + 55 * math.cos(next_angle_rad - math.pi/2)
        y2 = 75 + 55 * math.sin(next_angle_rad - math.pi/2)
        
        color = fill_color if i < numerator else empty_color
        
        path = f'<path d="M 75 75 L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} Z" '
        path += f'fill="{color}" stroke="#333" stroke-width="2"/>'
        svg += path
    
    svg += '</svg>'
    return svg

def create_triangle_svg(numerator, denominator, fill_color, empty_color):
    """Create a triangle divided into horizontal strips"""
    svg = '<svg width="150" height="130" viewBox="0 0 150 130">'
    
    # Draw horizontal strips
    strip_height = 100 / denominator
    
    for i in range(denominator):
        y_top = 20 + i * strip_height
        y_bottom = y_top + strip_height
        
        # Calculate x coordinates based on triangle shape
        x_left_top = 75 - (50 * (denominator - i) / denominator)
        x_right_top = 75 + (50 * (denominator - i) / denominator)
        x_left_bottom = 75 - (50 * (denominator - i - 1) / denominator)
        x_right_bottom = 75 + (50 * (denominator - i - 1) / denominator)
        
        color = fill_color if i < numerator else empty_color
        
        if i == denominator - 1:  # Top piece
            path = f'<path d="M 75 20 L {x_left_bottom:.1f} {y_bottom:.1f} L {x_right_bottom:.1f} {y_bottom:.1f} Z" '
        else:
            path = f'<path d="M {x_left_top:.1f} {y_top:.1f} L {x_left_bottom:.1f} {y_bottom:.1f} '
            path += f'L {x_right_bottom:.1f} {y_bottom:.1f} L {x_right_top:.1f} {y_top:.1f} Z" '
        
        path += f'fill="{color}" stroke="#333" stroke-width="2"/>'
        svg += path
    
    svg += '</svg>'
    return svg

def create_pentagon_svg(numerator, denominator, fill_color, empty_color):
    """Create a pentagon divided into sections"""
    svg = '<svg width="150" height="150" viewBox="0 0 150 150">'
    
    # Similar to hexagon but with 5 sides
    angle_per_section = 360 / denominator
    
    for i in range(denominator):
        angle = i * angle_per_section
        next_angle = (i + 1) * angle_per_section
        
        import math
        angle_rad = angle * math.pi / 180
        next_angle_rad = next_angle * math.pi / 180
        
        x1 = 75 + 55 * math.cos(angle_rad - math.pi/2)
        y1 = 75 + 55 * math.sin(angle_rad - math.pi/2)
        x2 = 75 + 55 * math.cos(next_angle_rad - math.pi/2)
        y2 = 75 + 55 * math.sin(next_angle_rad - math.pi/2)
        
        color = fill_color if i < numerator else empty_color
        
        path = f'<path d="M 75 75 L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} Z" '
        path += f'fill="{color}" stroke="#333" stroke-width="2"/>'
        svg += path
    
    svg += '</svg>'
    return svg

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display instruction
    st.markdown("### Use the pictures to subtract.")
    
    # Create visual display
    col1, col2, col3, col4, col5 = st.columns([1.5, 0.5, 1.5, 0.5, 1])
    
    with col1:
        # First shape
        shape_svg1 = create_shape_svg(
            data['shape_type'], 
            data['numerator1'], 
            data['denominator'],
            data['fill_color'],
            data['empty_color']
        )
        st.markdown(shape_svg1, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 40px;">
            −
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second shape
        shape_svg2 = create_shape_svg(
            data['shape_type'],
            data['numerator2'],
            data['denominator'],
            data['fill_color'],
            data['empty_color']
        )
        st.markdown(shape_svg2, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 40px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 40px;">
            ?
        </div>
        """, unsafe_allow_html=True)
    
    # Display fraction equation below
    st.markdown("")
    st.markdown("")
    
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
    
    with col1:
        # First fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 36px; line-height: 1;">
            <div style="border-bottom: 2px solid black; padding: 3px;">{data['numerator1']}</div>
            <div style="padding: 3px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 15px;">
            −
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 36px; line-height: 1;">
            <div style="border-bottom: 2px solid black; padding: 3px;">{data['numerator2']}</div>
            <div style="padding: 3px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 15px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Answer input
        with st.form("answer_form", clear_on_submit=False):
            user_input = st.text_input(
                "",
                key="fraction_answer",
                placeholder=f"?/{data['denominator']}",
                label_visibility="collapsed"
            )
            
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit and user_input.strip():
                # Parse the answer
                if '/' in user_input:
                    try:
                        parts = user_input.split('/')
                        user_num = int(parts[0])
                        user_denom = int(parts[1])
                        
                        if user_denom != data['denominator']:
                            st.error(f"The denominator should be {data['denominator']}")
                        else:
                            st.session_state.user_answer = user_num
                            st.session_state.answer_submitted = True
                            st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid fraction")
                else:
                    try:
                        user_num = int(user_input)
                        st.session_state.user_answer = user_num
                        st.session_state.answer_submitted = True
                        st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid number")
            elif submit:
                st.error("Please enter your answer")
    
    # Show feedback
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.question_data
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete equation
        st.success(f"✓ {data['numerator1']}/{data['denominator']} − {data['numerator2']}/{data['denominator']} = {correct_answer}/{data['denominator']}")
        
        # Visual explanation
        with st.expander("🎯 **How the pictures show the answer**", expanded=True):
            st.markdown(f"""
            **Visual explanation:**
            - First shape: {data['numerator1']} parts shaded ({data['color_name']})
            - Second shape: {data['numerator2']} parts to take away
            - Result: {data['numerator1']} − {data['numerator2']} = {correct_answer} parts left
            
            The pictures help you see subtraction as "taking away" parts!
            """)
        
        # Increase difficulty
        old_difficulty = st.session_state.subtract_area_difficulty
        st.session_state.subtract_area_difficulty = min(
            st.session_state.subtract_area_difficulty + 1, 5
        )
        
        if st.session_state.subtract_area_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered subtracting fractions with pictures!**")
        elif old_difficulty < st.session_state.subtract_area_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.subtract_area_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        st.error(f"You answered: {user_answer}/{data['denominator']}")
        
        # Show correct answer
        st.success(f"The correct answer is: {correct_answer}/{data['denominator']}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.subtract_area_difficulty
        st.session_state.subtract_area_difficulty = max(
            st.session_state.subtract_area_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.subtract_area_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.subtract_area_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for subtracting with area models"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Subtraction with Pictures**", expanded=True):
        st.markdown(f"""
        ### Your Problem:
        **{data['numerator1']}/{data['denominator']} − {data['numerator2']}/{data['denominator']} = ?**
        
        ### How to Use the Pictures:
        
        **Step 1: Count the first shape**
        - {data['numerator1']} parts are shaded ({data['color_name']})
        - This represents {data['numerator1']}/{data['denominator']}
        
        **Step 2: Look at the second shape**
        - {data['numerator2']} parts are shaded
        - This shows what to subtract: {data['numerator2']}/{data['denominator']}
        
        **Step 3: Subtract**
        - Start with {data['numerator1']} shaded parts
        - Take away {data['numerator2']} parts
        - {data['numerator1']} − {data['numerator2']} = {data['diff_numerator']}
        
        **Answer: {data['diff_numerator']}/{data['denominator']}**
        
        ### Remember:
        - The shapes are divided into {data['denominator']} equal parts
        - Subtraction means "taking away"
        - The denominator stays the same!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer