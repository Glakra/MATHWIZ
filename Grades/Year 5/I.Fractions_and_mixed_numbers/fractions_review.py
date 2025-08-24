import streamlit as st
import random
import math

def run():
    """
    Main function to run the Fractions review activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/fractions_review.py
    """
    # Initialize session state
    if "fractions_review_problem" not in st.session_state:
        st.session_state.fractions_review_problem = None
        st.session_state.fractions_review_submitted = False
        st.session_state.user_fraction_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🥧 Fractions Review")
    st.markdown("*Identify fractions from visual representations*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.fractions_review_problem is None:
        st.session_state.fractions_review_problem = generate_fraction_problem()
        st.session_state.fractions_review_submitted = False
        st.session_state.user_fraction_answer = ""
    
    problem = st.session_state.fractions_review_problem
    
    # Display the question
    st.markdown(f"### 📝 {problem['question']}")
    
    # Display the visual representation
    st.markdown(problem['svg'], unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("**Use a forward slash ( / ) to separate the numerator and denominator.**")
        
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_fraction_answer,
            key="fraction_answer_input",
            disabled=st.session_state.fractions_review_submitted,
            placeholder="e.g., 3/4",
            label_visibility="collapsed"
        )
        st.session_state.user_fraction_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.fractions_review_submitted):
            
            if st.session_state.user_fraction_answer.strip() == "":
                st.warning("⚠️ Please enter your answer as a fraction (e.g., 3/4).")
            else:
                st.session_state.fractions_review_submitted = True
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.fractions_review_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.fractions_review_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.fractions_review_problem = None
                st.session_state.fractions_review_submitted = False
                st.session_state.user_fraction_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Write Fractions:
        - **Numerator:** The number on top (how many parts)
        - **Denominator:** The number on bottom (total parts)
        - **Format:** numerator/denominator (e.g., 3/4)
        
        ### Types of Questions:
        1. **Colored parts:** What fraction of the shape is colored?
        2. **Shape counting:** What fraction of the shapes are circles/triangles/etc.?
        3. **Property questions:** What fraction are NOT something?
        
        ### Examples:
        - If 3 out of 4 parts are colored → **3/4**
        - If 2 out of 5 shapes are circles → **2/5**
        - If 4 out of 6 squares are NOT blue → **4/6** (can simplify to 2/3)
        
        ### Tips:
        - **Count carefully:** Count the colored/matching parts (numerator)
        - **Count total:** Count all parts or shapes (denominator)
        - **Check your work:** Make sure numerator ≤ denominator
        - **Simplify if asked:** But usually write what you see first
        """)

def format_number(num):
    """Format a number to avoid scientific notation and ensure valid SVG values"""
    # Round to 2 decimal places and format as string
    formatted = f"{float(num):.2f}"
    # Remove trailing zeros and decimal point if not needed
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    return formatted

def generate_fraction_problem():
    """Generate a random fraction visualization problem"""
    problem_types = [
        'circle_sectors',
        'grid_squares',
        'shape_collection',
        'divided_rectangle',
        'pie_chart',
        'diamond_sections'
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'circle_sectors':
        # Circle divided into equal sectors
        total_sectors = random.choice([4, 6, 8, 10, 12])
        colored_sectors = random.randint(1, total_sectors - 1)
        color = random.choice(['pink', 'blue', 'green', 'orange', 'purple'])
        
        # Create SVG
        svg = create_circle_sectors_svg(total_sectors, colored_sectors, color)
        
        return {
            'type': 'circle_sectors',
            'question': f'What fraction of the shape is {color}?',
            'svg': svg,
            'answer': f'{colored_sectors}/{total_sectors}',
            'numerator': colored_sectors,
            'denominator': total_sectors
        }
    
    elif problem_type == 'grid_squares':
        # Grid of squares
        rows = random.choice([2, 3, 4])
        cols = random.choice([2, 3, 4])
        total_squares = rows * cols
        colored_squares = random.randint(1, total_squares - 1)
        color = random.choice(['pink', 'blue', 'green', 'orange', 'purple'])
        
        # Create SVG
        svg = create_grid_svg(rows, cols, colored_squares, color)
        
        return {
            'type': 'grid_squares',
            'question': f'What fraction of the shape is {color}?',
            'svg': svg,
            'answer': f'{colored_squares}/{total_squares}',
            'numerator': colored_squares,
            'denominator': total_squares
        }
    
    elif problem_type == 'shape_collection':
        # Collection of different shapes
        shapes = []
        shape_types = ['square', 'circle', 'triangle', 'star', 'rectangle']
        total_shapes = random.randint(4, 8)
        
        # Generate random shapes
        for _ in range(total_shapes):
            shapes.append(random.choice(shape_types))
        
        # Choose question type
        question_types = [
            ('circles', lambda s: s == 'circle'),
            ('triangles', lambda s: s == 'triangle'),
            ('rectangles or squares', lambda s: s in ['rectangle', 'square']),
            ('triangles or rectangles', lambda s: s in ['triangle', 'rectangle']),
            ('not circles', lambda s: s != 'circle'),
            ('not squares', lambda s: s != 'square')
        ]
        
        question_text, condition = random.choice(question_types)
        matching = sum(1 for s in shapes if condition(s))
        
        # Create SVG
        svg = create_shapes_collection_svg(shapes)
        
        return {
            'type': 'shape_collection',
            'question': f'What fraction of the shapes are {question_text}?',
            'svg': svg,
            'answer': f'{matching}/{total_shapes}',
            'numerator': matching,
            'denominator': total_shapes
        }
    
    elif problem_type == 'divided_rectangle':
        # Rectangle divided into equal parts
        divisions = random.choice([3, 4, 5, 6, 8])
        colored_parts = random.randint(1, divisions - 1)
        color = random.choice(['pink', 'blue', 'green', 'orange', 'purple'])
        
        # Create SVG
        svg = create_divided_rectangle_svg(divisions, colored_parts, color)
        
        return {
            'type': 'divided_rectangle',
            'question': f'What fraction of the shape is {color}?',
            'svg': svg,
            'answer': f'{colored_parts}/{divisions}',
            'numerator': colored_parts,
            'denominator': divisions
        }
    
    elif problem_type == 'pie_chart':
        # Pie chart style circle
        total_parts = random.choice([3, 4, 5, 6, 8])
        colored_parts = random.randint(1, total_parts - 1)
        color = random.choice(['green', 'blue', 'red', 'yellow', 'purple'])
        
        # Create SVG
        svg = create_pie_chart_svg(total_parts, colored_parts, color)
        
        return {
            'type': 'pie_chart',
            'question': f'What fraction of the shape is {color}?',
            'svg': svg,
            'answer': f'{colored_parts}/{total_parts}',
            'numerator': colored_parts,
            'denominator': total_parts
        }
    
    else:  # diamond_sections
        # Diamond (rotated square) with triangular sections
        colored_sections = random.randint(1, 3)
        color = random.choice(['orange', 'blue', 'green', 'red', 'purple'])
        
        # Create SVG
        svg = create_diamond_svg(colored_sections, color)
        
        return {
            'type': 'diamond_sections',
            'question': f'What fraction of the shape is {color}?',
            'svg': svg,
            'answer': f'{colored_sections}/4',
            'numerator': colored_sections,
            'denominator': 4
        }

def create_circle_sectors_svg(total_sectors, colored_sectors, color):
    """Create an SVG of a circle divided into sectors"""
    angle_per_sector = 360 / total_sectors
    
    # Randomly select which sectors to color
    colored_indices = random.sample(range(total_sectors), colored_sectors)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="200" height="200" viewBox="0 0 200 200">')
    
    for i in range(total_sectors):
        start_angle = i * angle_per_sector - 90  # Start from top
        end_angle = (i + 1) * angle_per_sector - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = 100 + 80 * math.cos(start_rad)
        y1 = 100 + 80 * math.sin(start_rad)
        x2 = 100 + 80 * math.cos(end_rad)
        y2 = 100 + 80 * math.sin(end_rad)
        
        # Format numbers to avoid scientific notation
        x1_str = format_number(x1)
        y1_str = format_number(y1)
        x2_str = format_number(x2)
        y2_str = format_number(y2)
        
        # Determine if this sector should be colored
        fill_color = color if i in colored_indices else 'white'
        
        # Create sector path
        large_arc = 0 if angle_per_sector <= 180 else 1
        path = f'M 100 100 L {x1_str} {y1_str} A 80 80 0 {large_arc} 1 {x2_str} {y2_str} Z'
        svg_parts.append(f'<path d="{path}" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_grid_svg(rows, cols, colored_squares, color):
    """Create an SVG of a grid with some squares colored"""
    total_squares = rows * cols
    colored_indices = random.sample(range(total_squares), colored_squares)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="200" height="200" viewBox="0 0 200 200">')
    
    square_size = 180 / max(rows, cols)
    start_x = (200 - cols * square_size) / 2
    start_y = (200 - rows * square_size) / 2
    
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            x = start_x + col * square_size
            y = start_y + row * square_size
            
            fill_color = color if index in colored_indices else 'white'
            
            x_str = format_number(x)
            y_str = format_number(y)
            size_str = format_number(square_size)
            
            svg_parts.append(f'<rect x="{x_str}" y="{y_str}" width="{size_str}" height="{size_str}" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_shapes_collection_svg(shapes):
    """Create an SVG with a collection of different shapes"""
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="400" height="100" viewBox="0 0 400 100">')
    
    shape_width = 350 / len(shapes)
    start_x = 25
    
    colors = ['green', 'orange', 'blue', 'purple', 'red', 'yellow']
    
    for i, shape in enumerate(shapes):
        x = start_x + i * shape_width + shape_width / 2
        y = 50
        color = random.choice(colors)
        
        x_str = format_number(x)
        y_str = format_number(y)
        
        if shape == 'circle':
            svg_parts.append(f'<circle cx="{x_str}" cy="{y_str}" r="20" fill="{color}" stroke="black" stroke-width="2"/>')
        elif shape == 'square':
            x_rect = format_number(x - 20)
            y_rect = format_number(y - 20)
            svg_parts.append(f'<rect x="{x_rect}" y="{y_rect}" width="40" height="40" fill="{color}" stroke="black" stroke-width="2"/>')
        elif shape == 'triangle':
            p1 = f"{x_str},{format_number(y-25)}"
            p2 = f"{format_number(x-22)},{format_number(y+20)}"
            p3 = f"{format_number(x+22)},{format_number(y+20)}"
            svg_parts.append(f'<polygon points="{p1} {p2} {p3}" fill="{color}" stroke="black" stroke-width="2"/>')
        elif shape == 'star':
            # Simple 5-pointed star
            star_points = []
            for j in range(10):
                angle = (j * 36 - 90) * math.pi / 180
                r = 25 if j % 2 == 0 else 10
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                star_points.append(f"{format_number(px)},{format_number(py)}")
            svg_parts.append(f'<polygon points="{" ".join(star_points)}" fill="{color}" stroke="black" stroke-width="2"/>')
        elif shape == 'rectangle':
            x_rect = format_number(x - 25)
            y_rect = format_number(y - 15)
            svg_parts.append(f'<rect x="{x_rect}" y="{y_rect}" width="50" height="30" fill="{color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_divided_rectangle_svg(divisions, colored_parts, color):
    """Create an SVG of a rectangle divided into equal vertical parts"""
    colored_indices = random.sample(range(divisions), colored_parts)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="300" height="150" viewBox="0 0 300 150">')
    
    part_width = 240 / divisions
    start_x = 30
    
    for i in range(divisions):
        x = start_x + i * part_width
        fill_color = color if i in colored_indices else 'white'
        
        x_str = format_number(x)
        width_str = format_number(part_width)
        
        svg_parts.append(f'<rect x="{x_str}" y="25" width="{width_str}" height="100" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_pie_chart_svg(total_parts, colored_parts, color):
    """Create a pie chart style circle"""
    angle_per_part = 360 / total_parts
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="200" height="200" viewBox="0 0 200 200">')
    
    for i in range(total_parts):
        start_angle = i * angle_per_part - 90
        end_angle = (i + 1) * angle_per_part - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = 100 + 80 * math.cos(start_rad)
        y1 = 100 + 80 * math.sin(start_rad)
        x2 = 100 + 80 * math.cos(end_rad)
        y2 = 100 + 80 * math.sin(end_rad)
        
        # Format numbers
        x1_str = format_number(x1)
        y1_str = format_number(y1)
        x2_str = format_number(x2)
        y2_str = format_number(y2)
        
        fill_color = color if i < colored_parts else 'white'
        
        large_arc = 0 if angle_per_part <= 180 else 1
        path = f'M 100 100 L {x1_str} {y1_str} A 80 80 0 {large_arc} 1 {x2_str} {y2_str} Z'
        svg_parts.append(f'<path d="{path}" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_diamond_svg(colored_sections, color):
    """Create a diamond (rotated square) with 4 triangular sections"""
    colored_indices = random.sample(range(4), colored_sections)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="200" height="200" viewBox="0 0 200 200">')
    
    # Use a simple diamond shape without rotation transform
    # Center point
    cx, cy = 100, 100
    # Diamond vertices
    vertices = [
        (cx, cy - 50),  # Top
        (cx + 50, cy),  # Right
        (cx, cy + 50),  # Bottom
        (cx - 50, cy)   # Left
    ]
    
    # Create 4 triangular sections
    for i in range(4):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 4]
        
        fill_color = color if i in colored_indices else 'white'
        
        path = f'M {cx} {cy} L {v1[0]} {v1[1]} L {v2[0]} {v2[1]} Z'
        svg_parts.append(f'<path d="{path}" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    # Add diamond outline
    outline_points = ' '.join([f'{v[0]},{v[1]}' for v in vertices])
    svg_parts.append(f'<polygon points="{outline_points}" fill="none" stroke="black" stroke-width="3"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.fractions_review_problem
    user_answer = st.session_state.user_fraction_answer.strip()
    
    # Parse user answer
    try:
        if '/' not in user_answer:
            st.error("❌ Please enter your answer as a fraction using / (e.g., 3/4)")
            return
        
        parts = user_answer.split('/')
        if len(parts) != 2:
            st.error("❌ Please use exactly one / to separate numerator and denominator")
            return
        
        user_num = int(parts[0].strip())
        user_den = int(parts[1].strip())
        
        # Check if fraction is valid
        if user_den == 0:
            st.error("❌ The denominator cannot be zero")
            return
        
        # Check if answer is correct
        correct_num = problem['numerator']
        correct_den = problem['denominator']
        
        # Check for exact match or equivalent fraction
        is_exact_match = (user_num == correct_num and user_den == correct_den)
        is_equivalent = (user_num * correct_den == correct_num * user_den)
        
        if is_exact_match:
            st.success(f"🎉 **Correct! {user_answer} is right!**")
            
        elif is_equivalent:
            st.success(f"🎉 **Correct! {user_answer} is equivalent to {problem['answer']}**")
            st.info(f"Both fractions equal {user_num/user_den:.2f}")
            
        else:
            st.error(f"❌ **Not quite right. The correct answer is {problem['answer']}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"**Counting the parts:**")
                
                if problem['type'] in ['circle_sectors', 'grid_squares', 'divided_rectangle', 'pie_chart', 'diamond_sections']:
                    st.markdown(f"- Colored parts: **{correct_num}**")
                    st.markdown(f"- Total parts: **{correct_den}**")
                    st.markdown(f"- Fraction: **{correct_num}/{correct_den}**")
                else:  # shape_collection
                    st.markdown(f"- Matching shapes: **{correct_num}**")
                    st.markdown(f"- Total shapes: **{correct_den}**")
                    st.markdown(f"- Fraction: **{correct_num}/{correct_den}**")
                
                st.markdown(f"\n**Your answer:** {user_answer}")
                
    except ValueError:
        st.error("❌ Please enter whole numbers for the numerator and denominator (e.g., 3/4)")
    except Exception as e:
        st.error("❌ Invalid input. Please enter your answer as a fraction (e.g., 3/4)")