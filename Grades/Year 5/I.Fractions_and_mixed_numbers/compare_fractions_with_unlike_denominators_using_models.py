import streamlit as st
import random
import math

def run():
    """
    Main function to run the Compare Fractions with Unlike Denominators Using Models activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/compare_fractions_with_unlike_denominators_using_models.py
    """
    # Initialize session state
    if "compare_fractions_score" not in st.session_state:
        st.session_state.compare_fractions_score = 0
        st.session_state.compare_fractions_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.selected_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Compare Fractions with Unlike Denominators Using Models")
    st.markdown("*Use visual models to compare fractions with different denominators*")
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.session_state.compare_fractions_attempts > 0:
            accuracy = (st.session_state.compare_fractions_score / st.session_state.compare_fractions_attempts) * 100
            st.metric("Score", f"{st.session_state.compare_fractions_score}/{st.session_state.compare_fractions_attempts}", 
                     f"{accuracy:.0f}%")
        else:
            st.metric("Score", "0/0", "Start practicing!")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the visual models** showing two fractions
        - **Compare the shaded portions** to see which is larger or smaller
        - **Click on the fraction** that answers the question
        - **Submit your answer** to check if you're correct
        
        ### Visual Models:
        - **⭕ Circles:** Pizza-like circles divided into slices
        - **🔺 Triangles:** Triangular shapes with divisions
        - **⬜ Grids:** Squares arranged in rows and columns
        - **📊 Bars:** Rectangular bars divided into sections
        
        ### Tips for Success:
        - **Look at the shaded parts:** More shading = larger fraction
        - **Same numerators:** When top numbers match, smaller bottom = larger fraction
        - **Think of pizza:** Which slice gives you more pizza?
        - **Use benchmarks:** Compare to 1/2 to help decide
        
        ### Examples:
        - **1/2 vs 1/4:** Half a pizza is more than a quarter
        - **3/4 vs 3/8:** 3 out of 4 pieces is more than 3 out of 8
        - **2/3 vs 2/5:** 2 out of 3 is more than 2 out of 5
        
        ### Remember:
        - The **denominator** tells how many equal parts
        - The **numerator** tells how many parts are taken
        - Visual models help you see the actual size!
        """)

def generate_new_problem():
    """Generate a new fraction comparison problem with visual models"""
    
    # Equal distribution of shape types
    circle_problems = [
        {
            "fraction1": (3, 4),
            "fraction2": (2, 8),
            "model_type": "circle",
            "question": "Which fraction is greater?",
            "correct_answer": (3, 4),
            "explanation": "3/4 is greater than 2/8 (which equals 1/4)"
        },
        {
            "fraction1": (5, 8),
            "fraction2": (1, 2),
            "model_type": "circle",
            "question": "Which fraction is less?",
            "correct_answer": (1, 2),
            "explanation": "1/2 (4/8) is less than 5/8"
        },
        {
            "fraction1": (1, 4),
            "fraction2": (3, 8),
            "model_type": "circle",
            "question": "Which fraction is less?",
            "correct_answer": (1, 4),
            "explanation": "1/4 (2/8) is less than 3/8"
        },
        {
            "fraction1": (2, 3),
            "fraction2": (3, 4),
            "model_type": "circle",
            "question": "Which fraction is less?",
            "correct_answer": (2, 3),
            "explanation": "2/3 is less than 3/4"
        },
    ]
    
    triangle_problems = [
        {
            "fraction1": (1, 6),
            "fraction2": (1, 3),
            "model_type": "triangle",
            "question": "Which fraction is greater?",
            "correct_answer": (1, 3),
            "explanation": "1/3 is greater because each third is larger than each sixth"
        },
        {
            "fraction1": (2, 3),
            "fraction2": (2, 6),
            "model_type": "triangle",
            "question": "Which fraction is greater?",
            "correct_answer": (2, 3),
            "explanation": "2/3 is greater than 2/6 (which equals 1/3)"
        },
        {
            "fraction1": (1, 3),
            "fraction2": (2, 6),
            "model_type": "triangle",
            "question": "Which fraction is less?",
            "correct_answer": (1, 3),
            "explanation": "1/3 and 2/6 are equal"
        },
        {
            "fraction1": (2, 3),
            "fraction2": (1, 6),
            "model_type": "triangle",
            "question": "Which fraction is greater?",
            "correct_answer": (2, 3),
            "explanation": "2/3 is greater than 1/6"
        },
    ]
    
    grid_problems = [
        {
            "fraction1": (3, 4),
            "fraction2": (3, 8),
            "model_type": "grid",
            "question": "Which fraction is greater?",
            "correct_answer": (3, 4),
            "explanation": "3/4 is greater because fourths are larger than eighths"
        },
        {
            "fraction1": (2, 5),
            "fraction2": (3, 10),
            "model_type": "grid",
            "question": "Which fraction is greater?",
            "correct_answer": (2, 5),
            "explanation": "2/5 (4/10) is greater than 3/10"
        },
        {
            "fraction1": (3, 5),
            "fraction2": (5, 8),
            "model_type": "grid",
            "question": "Which fraction is less?",
            "correct_answer": (3, 5),
            "explanation": "3/5 is less than 5/8"
        },
        {
            "fraction1": (1, 2),
            "fraction2": (3, 5),
            "model_type": "grid",
            "question": "Which fraction is less?",
            "correct_answer": (1, 2),
            "explanation": "1/2 (5/10) is less than 3/5 (6/10)"
        },
    ]
    
    bar_problems = [
        {
            "fraction1": (5, 8),
            "fraction2": (1, 4),
            "model_type": "bar",
            "question": "Which fraction is greater?",
            "correct_answer": (5, 8),
            "explanation": "5/8 is greater than 1/4 (2/8)"
        },
        {
            "fraction1": (2, 3),
            "fraction2": (2, 5),
            "model_type": "bar",
            "question": "Which fraction is less?",
            "correct_answer": (2, 5),
            "explanation": "2/5 is less because fifths are smaller than thirds"
        },
        {
            "fraction1": (3, 4),
            "fraction2": (2, 3),
            "model_type": "bar",
            "question": "Which fraction is greater?",
            "correct_answer": (3, 4),
            "explanation": "3/4 is greater than 2/3"
        },
        {
            "fraction1": (1, 4),
            "fraction2": (2, 7),
            "model_type": "bar",
            "question": "Which fraction is less?",
            "correct_answer": (1, 4),
            "explanation": "1/4 is less than 2/7"
        },
    ]
    
    # Combine all problems for equal distribution
    all_problems = circle_problems + triangle_problems + grid_problems + bar_problems
    
    st.session_state.current_problem = random.choice(all_problems)
    st.session_state.selected_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def create_svg_circle(numerator, denominator, color):
    """Create SVG circle fraction model"""
    cx, cy, r = 100, 100, 80
    
    svg_parts = [f'<svg width="200" height="200" viewBox="0 0 200 200">']
    
    # Draw background circle
    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="black" stroke-width="2"/>')
    
    # Draw pie slices
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        
        # Determine if we need a large arc
        large_arc = 1 if angle_per_slice > 180 else 0
        
        # Create the path
        if i < numerator:
            path = f'M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2} Z'
            svg_parts.append(f'<path d="{path}" fill="{color}" opacity="0.8" stroke="black" stroke-width="1"/>')
        
        # Add division lines
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x1}" y2="{y1}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_svg_triangle(numerator, denominator, color):
    """Create SVG triangle fraction model with proper divisions"""
    
    svg_parts = ['<svg width="200" height="200" viewBox="0 0 200 200">']
    
    # Define triangle vertices
    top_x, top_y = 100, 30
    left_x, left_y = 30, 170
    right_x, right_y = 170, 170
    
    # Draw triangle outline
    svg_parts.append(f'<path d="M {top_x} {top_y} L {left_x} {left_y} L {right_x} {right_y} Z" fill="white" stroke="black" stroke-width="2"/>')
    
    if denominator == 3:
        # Divide into thirds from center point
        center_x = 100
        center_y = 123  # Centroid of triangle
        
        # Create three sections from center to each vertex
        sections = [
            (f'M {center_x} {center_y} L {top_x} {top_y} L {left_x} {left_y} Z', 0),
            (f'M {center_x} {center_y} L {left_x} {left_y} L {right_x} {right_y} Z', 1),
            (f'M {center_x} {center_y} L {right_x} {right_y} L {top_x} {top_y} Z', 2)
        ]
        
        # Shade the appropriate sections
        for path, index in sections:
            if index < numerator:
                svg_parts.append(f'<path d="{path}" fill="{color}" opacity="0.8" stroke="black" stroke-width="1"/>')
        
        # Add division lines from center to vertices
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{top_x}" y2="{top_y}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{left_x}" y2="{left_y}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{right_x}" y2="{right_y}" stroke="black" stroke-width="2"/>')
    
    elif denominator == 6:
        # Divide into sixths - create 6 smaller triangles
        center_x = 100
        center_y = 123
        
        # Midpoints of each side
        mid_top_left = ((top_x + left_x) / 2, (top_y + left_y) / 2)
        mid_top_right = ((top_x + right_x) / 2, (top_y + right_y) / 2)
        mid_bottom = ((left_x + right_x) / 2, left_y)
        
        sections = [
            f'M {top_x} {top_y} L {mid_top_left[0]} {mid_top_left[1]} L {center_x} {center_y} Z',
            f'M {top_x} {top_y} L {center_x} {center_y} L {mid_top_right[0]} {mid_top_right[1]} Z',
            f'M {mid_top_left[0]} {mid_top_left[1]} L {left_x} {left_y} L {center_x} {center_y} Z',
            f'M {center_x} {center_y} L {left_x} {left_y} L {mid_bottom[0]} {mid_bottom[1]} Z',
            f'M {center_x} {center_y} L {mid_bottom[0]} {mid_bottom[1]} L {right_x} {right_y} Z',
            f'M {mid_top_right[0]} {mid_top_right[1]} L {center_x} {center_y} L {right_x} {right_y} Z'
        ]
        
        # Shade the appropriate sections
        for i in range(min(numerator, len(sections))):
            svg_parts.append(f'<path d="{sections[i]}" fill="{color}" opacity="0.8" stroke="black" stroke-width="1"/>')
        
        # Add all division lines
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{top_x}" y2="{top_y}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{left_x}" y2="{left_y}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{right_x}" y2="{right_y}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{mid_top_left[0]}" y2="{mid_top_left[1]}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{mid_top_right[0]}" y2="{mid_top_right[1]}" stroke="black" stroke-width="2"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{mid_bottom[0]}" y2="{mid_bottom[1]}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def display_problem():
    """Display the current fraction comparison problem"""
    
    problem = st.session_state.current_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Get fractions
    frac1 = problem['fraction1']
    frac2 = problem['fraction2']
    
    # Choose colors based on model type
    colors = {
        "circle": ("#4CAF50", "#9C27B0"),
        "triangle": ("#4CAF50", "#9C27B0"),
        "grid": ("#FFC107", "#00BCD4"),
        "bar": ("#FF9800", "#2196F3")
    }
    
    color1, color2 = colors.get(problem['model_type'], ("#4CAF50", "#FF9800"))
    
    # Create two columns for the fractions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h2 style='text-align: center;'>{frac1[0]}/{frac1[1]}</h2>", unsafe_allow_html=True)
        
        if problem['model_type'] == 'circle':
            svg = create_svg_circle(frac1[0], frac1[1], color1)
            st.markdown(f'<div style="text-align: center;">{svg}</div>', unsafe_allow_html=True)
        elif problem['model_type'] == 'triangle':
            svg = create_svg_triangle(frac1[0], frac1[1], color1)
            st.markdown(f'<div style="text-align: center;">{svg}</div>', unsafe_allow_html=True)
        elif problem['model_type'] == 'grid':
            # Grid model
            display_grid_model(frac1[0], frac1[1], color1)
        else:  # bar
            # Bar model
            display_bar_model(frac1[0], frac1[1], color1)
    
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{frac2[0]}/{frac2[1]}</h2>", unsafe_allow_html=True)
        
        if problem['model_type'] == 'circle':
            svg = create_svg_circle(frac2[0], frac2[1], color2)
            st.markdown(f'<div style="text-align: center;">{svg}</div>', unsafe_allow_html=True)
        elif problem['model_type'] == 'triangle':
            svg = create_svg_triangle(frac2[0], frac2[1], color2)
            st.markdown(f'<div style="text-align: center;">{svg}</div>', unsafe_allow_html=True)
        elif problem['model_type'] == 'grid':
            # Grid model
            display_grid_model(frac2[0], frac2[1], color2)
        else:  # bar
            # Bar model
            display_bar_model(frac2[0], frac2[1], color2)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create clickable options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{frac1[0]}/{frac1[1]}", key="frac1_btn", 
                    type="primary" if st.session_state.selected_answer == frac1 else "secondary",
                    use_container_width=True):
            st.session_state.selected_answer = frac1
            st.rerun()
    
    with col2:
        if st.button(f"{frac2[0]}/{frac2[1]}", key="frac2_btn",
                    type="primary" if st.session_state.selected_answer == frac2 else "secondary",
                    use_container_width=True):
            st.session_state.selected_answer = frac2
            st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True, 
                    disabled=st.session_state.answer_submitted):
            if st.session_state.selected_answer:
                check_answer()
            else:
                st.warning("Please select an answer before submitting!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.current_problem = None
                st.rerun()

def display_grid_model(numerator, denominator, color):
    """Display grid model using Streamlit components"""
    
    # Determine grid dimensions
    if denominator == 4:
        rows, cols = 2, 2
    elif denominator == 8:
        rows, cols = 2, 4
    elif denominator == 10:
        rows, cols = 2, 5
    elif denominator == 5:
        rows, cols = 1, 5
    elif denominator == 6:
        rows, cols = 2, 3
    else:
        cols = min(denominator, 5)
        rows = (denominator + cols - 1) // cols
    
    # Create the grid using Streamlit columns
    cell_count = 0
    for r in range(rows):
        grid_cols = st.columns(cols)
        for c in range(cols):
            if cell_count < denominator:
                with grid_cols[c]:
                    if cell_count < numerator:
                        st.markdown(
                            f'<div style="width: 40px; height: 40px; background-color: {color}; '
                            f'border: 2px solid black; margin: 1px;"></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div style="width: 40px; height: 40px; background-color: white; '
                            'border: 2px solid black; margin: 1px;"></div>',
                            unsafe_allow_html=True
                        )
                    cell_count += 1

def display_bar_model(numerator, denominator, color):
    """Display horizontal bar model using Streamlit"""
    
    # Create the bar using columns
    bar_cols = st.columns(denominator)
    
    for i in range(denominator):
        with bar_cols[i]:
            if i < numerator:
                st.markdown(
                    f'<div style="width: 100%; height: 60px; background-color: {color}; '
                    f'border: 1px solid black; border-right: {"none" if i < denominator-1 else "1px solid black"};"></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div style="width: 100%; height: 60px; background-color: white; '
                    f'border: 1px solid black; border-right: {"none" if i < denominator-1 else "1px solid black"};"></div>',
                    unsafe_allow_html=True
                )

def check_answer():
    """Check if the selected answer is correct"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    st.session_state.answer_submitted = True
    st.session_state.compare_fractions_attempts += 1
    
    if st.session_state.selected_answer == correct_answer:
        st.session_state.compare_fractions_score += 1
    
    st.session_state.show_feedback = True

def show_feedback():
    """Display feedback for the submitted answer"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    if st.session_state.selected_answer == correct_answer:
        st.success(f"🎉 **Correct! {problem['explanation']}**")
        
        # Add visual celebration for streaks
        if st.session_state.compare_fractions_score % 5 == 0:
            st.balloons()
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer[0]}/{correct_answer[1]}**")
        st.info(f"💡 **{problem['explanation']}**")
        
        # Additional tips
        with st.expander("📚 **Learn More**", expanded=True):
            st.markdown("""
            ### How to Compare Fractions:
            
            1. **Look at the visual models** - Which has more shaded area?
            2. **Compare to benchmarks** - Is each fraction more or less than 1/2?
            3. **Find common denominators** - Convert to make denominators the same
            4. **Cross multiply** - Multiply diagonally and compare products
            
            ### Quick Tips:
            - **Same numerators?** Smaller denominator = larger fraction
            - **Same denominators?** Larger numerator = larger fraction
            - **Different everything?** Look at the shaded parts!
            
            ### Example:
            To compare 3/4 and 2/3:
            - 3/4 = 9/12 (multiply by 3)
            - 2/3 = 8/12 (multiply by 4)
            - 9/12 > 8/12, so 3/4 > 2/3
            """)