import streamlit as st
import random
import math

def run():
    """
    Main function to run the Compare Unit Fractions Using Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/compare_unit_fractions_using_models.py
    """
    # Initialize session state for difficulty and game state
    if "compare_fractions_difficulty" not in st.session_state:
        st.session_state.compare_fractions_difficulty = 1  # Start with simple comparisons
    
    if "question_type" not in st.session_state:
        st.session_state.question_type = None  # "greater" or "less"
        
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Compare Unit Fractions Using Models")
    st.markdown("*Compare unit fractions using visual models*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (2-6 parts)",
            2: "Medium (2-8 parts)",
            3: "Advanced (2-10 parts)",
            4: "Expert (2-12 parts)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 4)
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Medium**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the two shapes** showing unit fractions
        - **Compare the shaded parts** of each shape
        - **Choose which fraction is greater or less** as asked
        
        ### Shape Variety:
        - **Circles:** Divided into pie slices
        - **Squares:** Divided into grids or strips
        - **Rectangles:** Divided into horizontal strips
        - **Hexagons:** Divided into triangular sections
        - **Triangles:** Divided into sections
        - **Bars:** Divided into vertical sections
        
        ### Understanding Unit Fractions:
        - **Unit fraction** = fraction with numerator 1 (like 1/2, 1/3, 1/4)
        - **Key rule:** The larger the denominator, the smaller the fraction
        - **Visual tip:** More pieces = smaller pieces
        - **Works for any shape!** The principle is the same
        
        ### Comparison Rules:
        - **1/2 > 1/3** because halves are bigger than thirds
        - **1/4 < 1/3** because fourths are smaller than thirds
        - **1/8 < 1/4** because eighths are smaller than fourths
        
        ### Visual Clues:
        - **Bigger piece = Greater fraction**
        - **Smaller piece = Lesser fraction**
        - **More divisions = Smaller pieces**
        
        ### Think of Pizza! 🍕
        - Would you rather have 1/2 of a pizza or 1/8?
        - 1/2 is bigger because it's cut into fewer pieces!
        
        ### Quick Strategy:
        1. Count the total parts in each circle
        2. Remember: More parts = smaller pieces
        3. The fraction with fewer parts is greater
        
        ### Examples with Different Shapes:
        - **Circle 1/2 vs Square 1/4:** Circle with 2 parts has bigger pieces than square with 4 parts
        - **Bar 1/3 vs Triangle 1/6:** Bar with 3 parts has bigger pieces than triangle with 6 parts
        - **Rectangle 1/5 vs Hexagon 1/10:** Rectangle with 5 parts has bigger pieces than hexagon with 10 parts
        
        ### Common Patterns:
        - Halves > Thirds > Fourths > Fifths > Sixths...
        - Each time you add more divisions, pieces get smaller
        - This is true for ANY shape!
        
        ### Difficulty Levels:
        - **🟢 Basic:** Compare 2-6 parts
        - **🟡 Medium:** Compare 2-8 parts
        - **🟠 Advanced:** Compare 2-10 parts
        - **🔴 Expert:** Compare 2-12 parts
        """)

def generate_new_problem():
    """Generate a new comparison problem"""
    difficulty = st.session_state.compare_fractions_difficulty
    
    # Define denominator ranges based on difficulty
    if difficulty == 1:  # Basic
        denominators = [2, 3, 4, 5, 6]
    elif difficulty == 2:  # Medium
        denominators = [2, 3, 4, 5, 6, 7, 8]
    elif difficulty == 3:  # Advanced
        denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    else:  # Expert
        denominators = list(range(2, 13))  # 2 to 12
    
    # Choose two different denominators
    denom1, denom2 = random.sample(denominators, 2)
    
    # Randomly choose question type
    question_type = random.choice(["greater", "less"])
    st.session_state.question_type = question_type
    
    # Determine correct answer
    if question_type == "greater":
        # Smaller denominator means greater fraction
        correct_answer = f"1/{min(denom1, denom2)}"
    else:
        # Larger denominator means lesser fraction
        correct_answer = f"1/{max(denom1, denom2)}"
    
    # Choose colors for the fractions
    colors = ['#ff9ff3', '#54a0ff', '#48dbfb', '#1dd1a1', '#feca57', '#ff6b6b', 
              '#4834d4', '#00d2d3', '#ee5a24', '#f368e0', '#0abde3', '#10ac84']
    
    color1 = random.choice(colors)
    color2 = random.choice([c for c in colors if c != color1])
    
    # Choose shape types (can be same or different)
    shapes = ['circle', 'square', 'rectangle', 'hexagon', 'triangle', 'bar']
    shape1 = random.choice(shapes)
    shape2 = random.choice(shapes)
    
    # Store problem data
    st.session_state.problem_data = {
        "fraction1": f"1/{denom1}",
        "denominator1": denom1,
        "fraction2": f"1/{denom2}",
        "denominator2": denom2,
        "color1": color1,
        "color2": color2,
        "shape1": shape1,
        "shape2": shape2
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_problem = f"Which fraction is {question_type}?"

def create_fraction_shape_svg(shape_type, denominator, color, size=150):
    """Create SVG for various shapes divided into equal parts with one part shaded"""
    if shape_type == 'circle':
        return create_fraction_circle_svg(denominator, color, size)
    elif shape_type == 'square':
        return create_fraction_square_svg(denominator, color, size)
    elif shape_type == 'rectangle':
        return create_fraction_rectangle_svg(denominator, color, size)
    elif shape_type == 'hexagon':
        return create_fraction_hexagon_svg(denominator, color, size)
    elif shape_type == 'triangle':
        return create_fraction_triangle_svg(denominator, color, size)
    else:  # bar
        return create_fraction_bar_svg(denominator, color, size)

def create_fraction_circle_svg(denominator, color, size=150):
    """Create SVG for a circle divided into equal parts with one part shaded"""
    radius = size // 2
    center = radius
    
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 10px;">')
    
    # Create pie slices
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = center + radius * 0.95 * math.cos(start_rad)
        y1 = center + radius * 0.95 * math.sin(start_rad)
        x2 = center + radius * 0.95 * math.cos(end_rad)
        y2 = center + radius * 0.95 * math.sin(end_rad)
        
        # Determine if we need a large arc
        large_arc = 1 if angle_per_slice > 180 else 0
        
        # Create path
        path = f'M {center} {center} L {x1} {y1} A {radius*0.95} {radius*0.95} 0 {large_arc} 1 {x2} {y2} Z'
        
        # Only shade the first slice (unit fraction)
        fill = color if i == 0 else 'white'
        svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    # Add outer circle
    svg_parts.append(f'<circle cx="{center}" cy="{center}" r="{radius*0.95}" fill="none" stroke="#333" stroke-width="3"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_fraction_square_svg(denominator, color, size=150):
    """Create SVG for a square divided into equal parts"""
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 10px;">')
    
    # Special cases for common denominators
    if denominator == 4:
        # 2x2 grid
        cell_size = size // 2
        for i in range(4):
            row = i // 2
            col = i % 2
            x = col * cell_size
            y = row * cell_size
            fill = color if i == 0 else 'white'
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                           f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    elif denominator == 9:
        # 3x3 grid
        cell_size = size // 3
        for i in range(9):
            row = i // 3
            col = i % 3
            x = col * cell_size
            y = row * cell_size
            fill = color if i == 0 else 'white'
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                           f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    else:
        # Vertical strips
        strip_width = size / denominator
        for i in range(denominator):
            x = i * strip_width
            fill = color if i == 0 else 'white'
            svg_parts.append(f'<rect x="{x}" y="0" width="{strip_width}" height="{size}" '
                           f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_fraction_rectangle_svg(denominator, color, size=150):
    """Create SVG for a rectangle divided into equal parts"""
    width = size * 1.3
    height = size * 0.7
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" style="margin: 10px;">')
    
    # Horizontal strips
    strip_height = height / denominator
    for i in range(denominator):
        y = i * strip_height
        fill = color if i == 0 else 'white'
        svg_parts.append(f'<rect x="0" y="{y}" width="{width}" height="{strip_height}" '
                       f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_fraction_hexagon_svg(denominator, color, size=150):
    """Create SVG for a hexagon divided into equal parts"""
    center = size // 2
    radius = size // 2 - 5
    
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 10px;">')
    
    # Create triangular slices from center
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # For hexagon vertices (when denominator is 6)
        if denominator == 6:
            # Use hexagon shape
            vertices = []
            for j in range(6):
                angle = math.radians(60 * j - 90)
                x = center + radius * math.cos(angle)
                y = center + radius * math.sin(angle)
                vertices.append((x, y))
            
            # Draw triangular slice
            vertex_index = i
            next_vertex = (i + 1) % 6
            path = f'M {center} {center} L {vertices[vertex_index][0]} {vertices[vertex_index][1]} '
            path += f'L {vertices[next_vertex][0]} {vertices[next_vertex][1]} Z'
        else:
            # Regular radial slices
            x1 = center + radius * math.cos(start_rad)
            y1 = center + radius * math.sin(start_rad)
            x2 = center + radius * math.cos(end_rad)
            y2 = center + radius * math.sin(end_rad)
            
            path = f'M {center} {center} L {x1} {y1} A {radius} {radius} 0 0 1 {x2} {y2} Z'
        
        fill = color if i == 0 else 'white'
        svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    # Add hexagon outline
    if denominator == 6:
        hex_path = 'M '
        for j in range(6):
            angle = math.radians(60 * j - 90)
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            hex_path += f'{x} {y} '
        hex_path += 'Z'
        svg_parts.append(f'<path d="{hex_path}" fill="none" stroke="#333" stroke-width="3"/>')
    else:
        svg_parts.append(f'<circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#333" stroke-width="3"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_fraction_triangle_svg(denominator, color, size=150):
    """Create SVG for a triangle divided into equal parts"""
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 10px;">')
    
    # Equilateral triangle points
    height = size * 0.866  # height of equilateral triangle
    top_x, top_y = size // 2, 10
    left_x, left_y = 10, height
    right_x, right_y = size - 10, height
    
    if denominator == 2:
        # Vertical split
        mid_bottom_x = (left_x + right_x) / 2
        # First half (shaded)
        path1 = f'M {top_x} {top_y} L {left_x} {left_y} L {mid_bottom_x} {left_y} Z'
        svg_parts.append(f'<path d="{path1}" fill="{color}" stroke="#333" stroke-width="2"/>')
        # Second half
        path2 = f'M {top_x} {top_y} L {mid_bottom_x} {left_y} L {right_x} {right_y} Z'
        svg_parts.append(f'<path d="{path2}" fill="white" stroke="#333" stroke-width="2"/>')
        
    elif denominator == 3:
        # Three equal parts from center
        center_x = (top_x + left_x + right_x) / 3
        center_y = (top_y + left_y + right_y) / 3
        mid_left_x = (top_x + left_x) / 2
        mid_left_y = (top_y + left_y) / 2
        mid_right_x = (top_x + right_x) / 2
        mid_right_y = (top_y + right_y) / 2
        mid_bottom_x = (left_x + right_x) / 2
        
        # First slice (shaded)
        path1 = f'M {center_x} {center_y} L {top_x} {top_y} L {mid_left_x} {mid_left_y} Z'
        svg_parts.append(f'<path d="{path1}" fill="{color}" stroke="#333" stroke-width="2"/>')
        # Second slice
        path2 = f'M {center_x} {center_y} L {mid_left_x} {mid_left_y} L {left_x} {left_y} L {mid_bottom_x} {left_y} Z'
        svg_parts.append(f'<path d="{path2}" fill="white" stroke="#333" stroke-width="2"/>')
        # Third slice
        path3 = f'M {center_x} {center_y} L {mid_bottom_x} {left_y} L {right_x} {right_y} L {mid_right_x} {mid_right_y} Z'
        svg_parts.append(f'<path d="{path3}" fill="white" stroke="#333" stroke-width="2"/>')
        
    else:
        # Horizontal strips for other denominators
        strip_height = (height - 10) / denominator
        for i in range(denominator):
            y_top = top_y + i * strip_height
            y_bottom = y_top + strip_height
            
            # Calculate trapezoid width at each level
            ratio_top = i / denominator
            ratio_bottom = (i + 1) / denominator
            
            left_x_top = top_x - (top_x - left_x) * ratio_top
            right_x_top = top_x + (right_x - top_x) * ratio_top
            left_x_bottom = top_x - (top_x - left_x) * ratio_bottom
            right_x_bottom = top_x + (right_x - top_x) * ratio_bottom
            
            path = f'M {left_x_top} {y_top} L {right_x_top} {y_top} L {right_x_bottom} {y_bottom} L {left_x_bottom} {y_bottom} Z'
            
            fill = color if i == 0 else 'white'
            svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    # Add triangle outline
    triangle_path = f'M {top_x} {top_y} L {left_x} {left_y} L {right_x} {right_y} Z'
    svg_parts.append(f'<path d="{triangle_path}" fill="none" stroke="#333" stroke-width="3"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_fraction_bar_svg(denominator, color, size=150):
    """Create SVG for a horizontal bar divided into equal parts"""
    width = size * 1.8
    height = size * 0.4
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" style="margin: 10px;">')
    
    # Vertical divisions
    section_width = width / denominator
    for i in range(denominator):
        x = i * section_width
        fill = color if i == 0 else 'white'
        svg_parts.append(f'<rect x="{x}" y="0" width="{section_width}" height="{height}" '
                       f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    question_type = st.session_state.question_type
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_problem}")
    
    # Create two columns for the circles
    col1, col2 = st.columns(2)
    
    with col1:
        # Display first fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="margin-bottom: 10px;">{data['fraction1']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display first shape with adjusted size
        shape_size = 150 if data['shape1'] not in ['bar', 'rectangle'] else 120
        shape1_svg = create_fraction_shape_svg(data['shape1'], data['denominator1'], data['color1'], shape_size)
        st.markdown(f"""
        <div style="text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center;">
            {shape1_svg}
        </div>
        <div style="text-align: center; font-size: 14px; color: #666; margin-top: -10px;">
            {data['shape1'].capitalize()}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display second fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <h2 style="margin-bottom: 10px;">{data['fraction2']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display second shape with adjusted size
        shape_size = 150 if data['shape2'] not in ['bar', 'rectangle'] else 120
        shape2_svg = create_fraction_shape_svg(data['shape2'], data['denominator2'], data['color2'], shape_size)
        st.markdown(f"""
        <div style="text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center;">
            {shape2_svg}
        </div>
        <div style="text-align: center; font-size: 14px; color: #666; margin-top: -10px;">
            {data['shape2'].capitalize()}
        </div>
        """, unsafe_allow_html=True)
    
    # Answer selection buttons
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Select your answer:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            button1 = st.form_submit_button(
                data['fraction1'],
                use_container_width=True,
                type="secondary"
            )
        
        with col2:
            button2 = st.form_submit_button(
                data['fraction2'],
                use_container_width=True,
                type="secondary"
            )
        
        if button1:
            st.session_state.submitted_answer = data['fraction1']
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
        elif button2:
            st.session_state.submitted_answer = data['fraction2']
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Submit button alternative (green button)
    if not st.session_state.answer_submitted:
        st.info("👆 Click on the fraction you think is " + question_type)
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    submitted = st.session_state.submitted_answer
    correct = st.session_state.correct_answer
    question_type = st.session_state.question_type
    
    if submitted == correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.compare_fractions_difficulty
        st.session_state.compare_fractions_difficulty = min(
            st.session_state.compare_fractions_difficulty + 1, 4
        )
        
        # Show encouragement based on difficulty
        if st.session_state.compare_fractions_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered comparing unit fractions!**")
        elif old_difficulty < st.session_state.compare_fractions_difficulty:
            difficulty_names = {2: "Medium", 3: "Advanced", 4: "Expert"}
            st.info(f"⬆️ **Level up! Now at {difficulty_names[st.session_state.compare_fractions_difficulty]} level**")
        
        # Show quick explanation
        show_explanation(correct=True)
        
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.compare_fractions_difficulty
        st.session_state.compare_fractions_difficulty = max(
            st.session_state.compare_fractions_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.compare_fractions_difficulty:
            difficulty_names = {1: "Basic", 2: "Medium", 3: "Advanced"}
            st.warning(f"⬇️ **Difficulty decreased to {difficulty_names[st.session_state.compare_fractions_difficulty]} level. Keep practicing!**")
        
        # Show explanation
        show_explanation(correct=False)

def show_explanation(correct=False):
    """Show explanation for the comparison"""
    data = st.session_state.problem_data
    question_type = st.session_state.question_type
    
    # Extract denominators
    denom1 = data['denominator1']
    denom2 = data['denominator2']
    
    with st.expander("📖 **Understanding the comparison**", expanded=not correct):
        st.markdown(f"""
        ### Comparing {data['fraction1']} and {data['fraction2']}
        
        **Key Concept:** With unit fractions, the larger the denominator, the smaller the fraction.
        
        **Visual Understanding:**
        - The left {data['shape1']} is divided into **{denom1} equal parts**
        - The right {data['shape2']} is divided into **{denom2} equal parts**
        - Each colored piece represents **one part** of the whole
        
        **Shape Note:** Whether it's a {data['shape1']}, {data['shape2']}, or any other shape, 
        the fraction comparison works the same way!
        """)
        
        if denom1 < denom2:
            st.markdown(f"""
        **Comparison:**
        - {data['fraction1']} has **fewer, larger pieces** ({denom1} parts)
        - {data['fraction2']} has **more, smaller pieces** ({denom2} parts)
        - Therefore: **{data['fraction1']} > {data['fraction2']}**
        """)
        else:
            st.markdown(f"""
        **Comparison:**
        - {data['fraction1']} has **more, smaller pieces** ({denom1} parts)
        - {data['fraction2']} has **fewer, larger pieces** ({denom2} parts)
        - Therefore: **{data['fraction1']} < {data['fraction2']}**
        """)
        
        # Pizza analogy
        st.markdown("""
        **🍕 Pizza Example:**
        Think of sharing a pizza:
        - 1/2 means you get half the pizza (1 out of 2 pieces)
        - 1/8 means you get only one slice when cut into 8 pieces
        - Which would you rather have? The 1/2 is much bigger!
        
        This works the same whether your "pizza" is round, square, or any other shape!
        """)
        
        # Show number line if helpful
        if not correct:
            st.markdown("""
        **Remember the pattern:**
        ```
        1/2 > 1/3 > 1/4 > 1/5 > 1/6 > 1/7 > 1/8 > ...
        ```
        As denominators increase, fractions decrease!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    st.session_state.question_type = None
    if "submitted_answer" in st.session_state:
        del st.session_state.submitted_answer