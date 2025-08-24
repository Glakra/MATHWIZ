import streamlit as st
import random

def run():
    """
    Main function to run the Add Fractions with Area Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/add_fractions_with_like_denominators_using_area_models.py
    """
    # Initialize session state for difficulty and game state
    if "area_model_difficulty" not in st.session_state:
        st.session_state.area_model_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_numerator = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕ Add Fractions Using Area Models")
    st.markdown("*Use the pictures to add fractions with like denominators*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.area_model_difficulty
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
        ### How to Play:
        1. Look at the two visual models showing fractions
        2. Count the shaded parts in each model
        3. Add the fractions together
        4. Enter your answer in the box
        5. Remember: the denominator stays the same!
        
        ### Visual Models:
        - **Rectangles**: Divided into equal parts horizontally or vertically
        - **Squares**: Divided into equal parts in a grid
        - **Circles**: Divided into equal pie slices
        
        ### Example:
        If you see 2/4 (2 parts shaded out of 4) + 1/4 (1 part shaded out of 4)
        - Count: 2 + 1 = 3 parts shaded total
        - Answer: 3/4
        
        ### Remember:
        - The denominator (bottom number) stays the same
        - Only add the numerators (top numbers)
        - Look at the pictures to help you count!
        """)

def generate_new_question():
    """Generate a new area model addition question"""
    difficulty = st.session_state.area_model_difficulty
    
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
    
    # Choose shape type
    shape_types = ['rectangle', 'square', 'circle']
    if difficulty <= 2:
        # For easier levels, prefer rectangles and squares
        shape_type = random.choice(['rectangle', 'rectangle', 'square', 'circle'])
    else:
        shape_type = random.choice(shape_types)
    
    # Generate numerators that don't exceed the denominator when added
    max_sum = min(denominator, denominator)  # Can't exceed the whole
    
    # Generate first numerator
    numerator1 = random.randint(1, min(denominator - 1, max_sum - 1))
    
    # Generate second numerator
    max_num2 = min(denominator - 1, max_sum - numerator1)
    numerator2 = random.randint(1, max_num2)
    
    # Calculate the sum
    sum_numerator = numerator1 + numerator2
    
    # Choose colors for the fractions
    color_pairs = [
        ('#FFB6C1', '#87CEEB'),  # Light pink and sky blue
        ('#98FB98', '#DDA0DD'),  # Pale green and plum
        ('#F0E68C', '#FFA07A'),  # Khaki and light salmon
        ('#FFD700', '#90EE90'),  # Gold and light green
        ('#FF69B4', '#00CED1'),  # Hot pink and dark turquoise
    ]
    colors = random.choice(color_pairs)
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "sum_numerator": sum_numerator,
        "shape_type": shape_type,
        "color1": colors[0],
        "color2": colors[1]
    }
    
    st.session_state.correct_answer = sum_numerator
    st.session_state.current_question = "Use the pictures to add."

def create_rectangle_svg(numerator, denominator, color, width=120, height=80):
    """Create an SVG rectangle divided into parts with some shaded"""
    svg = f'<svg width="{width}" height="{height}" style="border: 2px solid #333;">'
    
    if denominator <= 4:
        # Horizontal divisions
        part_height = height / denominator
        for i in range(denominator):
            y = i * part_height
            if i < numerator:
                svg += f'<rect x="0" y="{y}" width="{width}" height="{part_height}" fill="{color}" stroke="#333" stroke-width="1"/>'
            else:
                svg += f'<rect x="0" y="{y}" width="{width}" height="{part_height}" fill="white" stroke="#333" stroke-width="1"/>'
    else:
        # Grid layout
        cols = 2
        rows = (denominator + 1) // 2
        part_width = width / cols
        part_height = height / rows
        
        for i in range(denominator):
            row = i // cols
            col = i % cols
            x = col * part_width
            y = row * part_height
            
            if i < numerator:
                svg += f'<rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" fill="{color}" stroke="#333" stroke-width="1"/>'
            else:
                svg += f'<rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" fill="white" stroke="#333" stroke-width="1"/>'
    
    svg += '</svg>'
    return svg

def create_square_svg(numerator, denominator, color, size=100):
    """Create an SVG square divided into parts with some shaded"""
    svg = f'<svg width="{size}" height="{size}" style="border: 2px solid #333;">'
    
    # Determine grid size
    if denominator == 4:
        rows, cols = 2, 2
    elif denominator == 6:
        rows, cols = 2, 3
    elif denominator == 8:
        rows, cols = 2, 4
    elif denominator == 9:
        rows, cols = 3, 3
    elif denominator == 10:
        rows, cols = 2, 5
    elif denominator == 12:
        rows, cols = 3, 4
    else:
        # Default: try to make it as square as possible
        cols = int(denominator ** 0.5)
        rows = (denominator + cols - 1) // cols
    
    part_width = size / cols
    part_height = size / rows
    
    for i in range(denominator):
        row = i // cols
        col = i % cols
        x = col * part_width
        y = row * part_height
        
        if i < numerator:
            svg += f'<rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" fill="{color}" stroke="#333" stroke-width="1"/>'
        else:
            svg += f'<rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" fill="white" stroke="#333" stroke-width="1"/>'
    
    svg += '</svg>'
    return svg

def create_circle_svg(numerator, denominator, color, size=100):
    """Create an SVG circle divided into pie slices with some shaded"""
    radius = size / 2 - 2
    center = size / 2
    
    svg = f'<svg width="{size}" height="{size}">'
    
    # Draw pie slices
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90  # Start from top
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = start_angle * 3.14159 / 180
        end_rad = end_angle * 3.14159 / 180
        
        # Calculate points
        x1 = center + radius * (0.99 * 3.14159 / 180 * start_angle).real
        y1 = center + radius * (0.99 * 3.14159 / 180 * start_angle).imag
        x2 = center + radius * (0.99 * 3.14159 / 180 * end_angle).real
        y2 = center + radius * (0.99 * 3.14159 / 180 * end_angle).imag
        
        # Simpler calculation
        import math
        x1 = center + radius * math.cos(start_rad)
        y1 = center + radius * math.sin(start_rad)
        x2 = center + radius * math.cos(end_rad)
        y2 = center + radius * math.sin(end_rad)
        
        # Determine if we need large arc flag
        large_arc = 0 if angle_per_slice <= 180 else 1
        
        # Create path
        if i < numerator:
            fill_color = color
        else:
            fill_color = "white"
        
        path = f'M {center} {center} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z'
        svg += f'<path d="{path}" fill="{fill_color}" stroke="#333" stroke-width="2"/>'
    
    # Draw circle outline
    svg += f'<circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#333" stroke-width="2"/>'
    
    svg += '</svg>'
    return svg

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Create visual representation
    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
    
    with col1:
        # First fraction visual
        if data['shape_type'] == 'rectangle':
            svg1 = create_rectangle_svg(data['numerator1'], data['denominator'], data['color1'])
        elif data['shape_type'] == 'square':
            svg1 = create_square_svg(data['numerator1'], data['denominator'], data['color1'])
        else:  # circle
            svg1 = create_circle_svg(data['numerator1'], data['denominator'], data['color1'])
        
        st.markdown(svg1, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 25px;">
            +
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction visual
        if data['shape_type'] == 'rectangle':
            svg2 = create_rectangle_svg(data['numerator2'], data['denominator'], data['color2'])
        elif data['shape_type'] == 'square':
            svg2 = create_square_svg(data['numerator2'], data['denominator'], data['color2'])
        else:  # circle
            svg2 = create_circle_svg(data['numerator2'], data['denominator'], data['color2'])
        
        st.markdown(svg2, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 25px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 25px;">
            ?
        </div>
        """, unsafe_allow_html=True)
    
    # Show the equation with fractions
    st.markdown("")
    equation_cols = st.columns([1, 1, 1, 1, 3])
    
    with equation_cols[0]:
        st.markdown(f"""
        <div style="text-align: center; font-size: 24px;">
            <div style="border-bottom: 2px solid black; padding: 5px;">{data['numerator1']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with equation_cols[1]:
        st.markdown("""
        <div style="text-align: center; font-size: 24px; padding-top: 20px;">
            +
        </div>
        """, unsafe_allow_html=True)
    
    with equation_cols[2]:
        st.markdown(f"""
        <div style="text-align: center; font-size: 24px;">
            <div style="border-bottom: 2px solid black; padding: 5px;">{data['numerator2']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with equation_cols[3]:
        st.markdown("""
        <div style="text-align: center; font-size: 24px; padding-top: 20px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with equation_cols[4]:
        # Input area
        st.markdown("")  # Add some space
        input_col1, input_col2 = st.columns([1, 2])
        
        with input_col1:
            user_numerator = st.text_input(
                "",
                value=st.session_state.user_numerator,
                key="numerator_input",
                placeholder="?",
                label_visibility="collapsed"
            )
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; margin-top: -20px;">
                <div style="border-top: 2px solid black; padding: 5px;">{data['denominator']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Submit button
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if user_numerator.strip():
                try:
                    user_num = int(user_numerator)
                    st.session_state.user_numerator = user_numerator
                    st.session_state.user_answer = user_num
                    st.session_state.answer_submitted = True
                    st.session_state.show_feedback = True
                except ValueError:
                    st.error("Please enter a valid number")
            else:
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
        fraction1 = f"{data['numerator1']}/{data['denominator']}"
        fraction2 = f"{data['numerator2']}/{data['denominator']}"
        result = f"{correct_answer}/{data['denominator']}"
        
        st.success(f"✓ {fraction1} + {fraction2} = {result}")
        
        # Show visual explanation
        with st.expander("🎨 **See the visual explanation**", expanded=True):
            st.markdown(f"""
            **How it works:**
            - First shape: {data['numerator1']} parts shaded out of {data['denominator']}
            - Second shape: {data['numerator2']} parts shaded out of {data['denominator']}
            - Total shaded parts: {data['numerator1']} + {data['numerator2']} = {correct_answer}
            - Since both fractions have the same denominator ({data['denominator']}), we keep it the same
            - Answer: {result}
            """)
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.area_model_difficulty
        st.session_state.area_model_difficulty = min(
            st.session_state.area_model_difficulty + 1, 5
        )
        
        if st.session_state.area_model_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered adding fractions with area models!**")
        elif old_difficulty < st.session_state.area_model_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.area_model_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        user_fraction = f"{user_answer}/{data['denominator']}"
        st.error(f"You answered: {user_fraction}")
        
        # Show the correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.area_model_difficulty
        st.session_state.area_model_difficulty = max(
            st.session_state.area_model_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.area_model_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.area_model_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for adding fractions with area models"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Area Models for Adding Fractions**", expanded=True):
        st.markdown(f"""
        ### How to Add Fractions with Like Denominators
        
        **Your problem:**
        {data['numerator1']}/{data['denominator']} + {data['numerator2']}/{data['denominator']} = ?
        
        **Step 1: Count the shaded parts**
        - First fraction: {data['numerator1']} parts shaded
        - Second fraction: {data['numerator2']} parts shaded
        
        **Step 2: Add the shaded parts**
        - Total shaded: {data['numerator1']} + {data['numerator2']} = {data['sum_numerator']}
        
        **Step 3: Keep the same denominator**
        - The whole is still divided into {data['denominator']} parts
        - So the denominator stays {data['denominator']}
        
        **Answer: {data['sum_numerator']}/{data['denominator']}**
        
        ### Remember:
        - When denominators are the same, just add the numerators
        - The denominator tells us how many parts the whole is divided into
        - The numerator tells us how many parts are shaded
        - Visual models help us see what we're adding!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_numerator = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer