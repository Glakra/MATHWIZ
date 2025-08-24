import streamlit as st
import random
import math

def run():
    """
    Main function to run the Mixed Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/mixed_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "mixed_numbers_difficulty" not in st.session_state:
        st.session_state.mixed_numbers_difficulty = 1  # Start with simple mixed numbers
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_whole = None
        st.session_state.correct_numerator = None
        st.session_state.correct_denominator = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Mixed Numbers")
    st.markdown("*Write mixed numbers from visual representations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mixed_numbers_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (halves, thirds, fourths)",
            2: "Medium (+ fifths, sixths)",
            3: "Advanced (+ eighths, tenths)",
            4: "Expert (all denominators)"
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
        - **Count the whole shapes** that are completely filled
        - **Look at the partial shape** to find the fraction part
        - **Write the mixed number** as: whole number + fraction
        
        ### Understanding Mixed Numbers:
        - **Mixed number** = whole number + proper fraction
        - Example: 2 3/4 means "2 wholes and 3 fourths"
        
        ### How to Count:
        1. **Count whole shapes:** How many are completely filled?
        2. **Count parts in partial shape:** How many parts are filled?
        3. **Count total parts:** How many parts make one whole?
        4. **Write as:** whole number + numerator/denominator
        
        ### Examples:
        - **3 full circles + 1/2 circle** = 3 1/2
        - **2 full squares + 3/4 square** = 2 3/4
        - **4 full rectangles + 2/3 rectangle** = 4 2/3
        - **1 full shape + 5/6 shape** = 1 5/6
        
        ### Visual Clues:
        - **Squares:** Often divided into 4 parts (fourths)
        - **Circles:** Can be halves, thirds, fourths, etc.
        - **Rectangles:** Often thirds, fourths, or fifths
        
        ### Remember:
        - The **whole number** comes first
        - The **fraction** should be in lowest terms
        - Count carefully - every part matters!
        
        ### Difficulty Levels:
        - **🟢 Basic:** Halves, thirds, and fourths
        - **🟡 Medium:** Plus fifths and sixths
        - **🟠 Advanced:** Plus eighths and tenths
        - **🔴 Expert:** All possible denominators
        """)

def generate_new_problem():
    """Generate a new mixed number visual problem"""
    difficulty = st.session_state.mixed_numbers_difficulty
    
    # Define denominators based on difficulty
    if difficulty == 1:  # Basic
        denominators = [2, 3, 4]
    elif difficulty == 2:  # Medium
        denominators = [2, 3, 4, 5, 6]
    elif difficulty == 3:  # Advanced
        denominators = [2, 3, 4, 5, 6, 8, 10]
    else:  # Expert
        denominators = [2, 3, 4, 5, 6, 8, 9, 10, 12]
    
    # Choose a denominator
    denominator = random.choice(denominators)
    
    # Generate whole number part (1-5 based on difficulty)
    max_whole = min(2 + difficulty, 5)
    whole = random.randint(1, max_whole)
    
    # Generate numerator (must be less than denominator)
    numerator = random.randint(1, denominator - 1)
    
    # Simplify the fraction if needed
    gcd_value = math.gcd(numerator, denominator)
    if gcd_value > 1:
        numerator //= gcd_value
        denominator //= gcd_value
    
    # Choose shape type and color
    shapes = ['circle', 'square', 'rectangle']
    shape = random.choice(shapes)
    
    colors = {
        'circle': ['#9C88FF', '#5758BB', '#3498db', '#2ecc71'],
        'square': ['#ff9ff3', '#ee5a6f', '#f368e0', '#48dbfb'],
        'rectangle': ['#54a0ff', '#48dbfb', '#0abde3', '#006ba6']
    }
    
    color = random.choice(colors[shape])
    
    # Store the problem data
    st.session_state.problem_data = {
        "whole": whole,
        "numerator": numerator,
        "denominator": denominator,
        "shape": shape,
        "color": color,
        "original_denominator": denominator * gcd_value,  # For visual display
        "original_numerator": numerator * gcd_value
    }
    
    st.session_state.correct_whole = whole
    st.session_state.correct_numerator = numerator
    st.session_state.correct_denominator = denominator
    st.session_state.current_problem = f"Write the mixed number:"

def create_shape_svg(shape_type, denominator, filled_parts, color, size=80):
    """Create SVG for a shape with given divisions and filled parts"""
    if shape_type == 'circle':
        return create_circle_svg(denominator, filled_parts, color, size)
    elif shape_type == 'square':
        return create_square_svg(denominator, filled_parts, color, size)
    else:  # rectangle
        return create_rectangle_svg(denominator, filled_parts, color, size)

def create_circle_svg(denominator, filled_parts, color, size):
    """Create SVG for a divided circle"""
    radius = size // 2
    center = radius
    
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 5px;">')
    
    # Create pie slices
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = center + radius * math.cos(start_rad)
        y1 = center + radius * math.sin(start_rad)
        x2 = center + radius * math.cos(end_rad)
        y2 = center + radius * math.sin(end_rad)
        
        # Determine if we need a large arc
        large_arc = 1 if angle_per_slice > 180 else 0
        
        # Create path
        path = f'M {center} {center} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z'
        
        fill = color if i < filled_parts else 'white'
        svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_square_svg(denominator, filled_parts, color, size):
    """Create SVG for a divided square"""
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" style="margin: 5px;">')
    
    # Common square divisions
    if denominator == 4:
        # 2x2 grid
        cell_size = size // 2
        for i in range(4):
            row = i // 2
            col = i % 2
            x = col * cell_size
            y = row * cell_size
            fill = color if i < filled_parts else 'white'
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
            fill = color if i < filled_parts else 'white'
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                           f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    else:
        # Vertical strips for other denominators
        strip_width = size / denominator
        for i in range(denominator):
            x = i * strip_width
            fill = color if i < filled_parts else 'white'
            svg_parts.append(f'<rect x="{x}" y="0" width="{strip_width}" height="{size}" '
                           f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_rectangle_svg(denominator, filled_parts, color, size):
    """Create SVG for a divided rectangle"""
    width = size * 1.5  # Make rectangles wider
    height = size * 0.67
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" style="margin: 5px;">')
    
    # Vertical strips
    strip_width = width / denominator
    for i in range(denominator):
        x = i * strip_width
        fill = color if i < filled_parts else 'white'
        svg_parts.append(f'<rect x="{x}" y="0" width="{strip_width}" height="{height}" '
                       f'fill="{fill}" stroke="#333" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_problem}**")
    st.markdown(f"*(for example, 2 2/3):*")
    
    # Display the visual representation
    st.markdown("""
    <div style="
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    ">
    """, unsafe_allow_html=True)
    
    # Create shapes HTML
    shapes_html = '<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">'
    
    # Add whole shapes
    for i in range(data['whole']):
        shape_svg = create_shape_svg(
            data['shape'], 
            data['original_denominator'], 
            data['original_denominator'],  # Fully filled
            data['color']
        )
        shapes_html += shape_svg
    
    # Add partial shape
    shape_svg = create_shape_svg(
        data['shape'], 
        data['original_denominator'], 
        data['original_numerator'],
        data['color']
    )
    shapes_html += shape_svg
    
    shapes_html += '</div></div>'
    
    st.markdown(shapes_html, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Enter your answer:**")
        
        # Create input layout: whole number + fraction
        col1, col2, col3, col4 = st.columns([1.5, 0.5, 1.5, 2])
        
        with col1:
            user_whole = st.number_input(
                "Whole number",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key="user_whole",
                label_visibility="collapsed",
                placeholder="Whole"
            )
        
        with col2:
            st.markdown("""
            <div style="text-align: center; margin-top: 5px; font-size: 24px;">
                <strong>and</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Fraction inputs (stacked)
            user_numerator = st.number_input(
                "Numerator",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
                key="user_num_mixed",
                label_visibility="collapsed",
                placeholder="Top"
            )
            
            st.markdown("""
            <div style="margin: -15px 0;">
                <hr style="border: none; border-top: 2px solid #333;">
            </div>
            """, unsafe_allow_html=True)
            
            user_denominator = st.number_input(
                "Denominator",
                min_value=1,
                max_value=20,
                value=1,
                step=1,
                key="user_den_mixed",
                label_visibility="collapsed",
                placeholder="Bottom"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.submitted_whole = user_whole
            st.session_state.submitted_numerator = user_numerator
            st.session_state.submitted_denominator = user_denominator
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_whole = st.session_state.submitted_whole
    user_num = st.session_state.submitted_numerator
    user_den = st.session_state.submitted_denominator
    correct_whole = st.session_state.correct_whole
    correct_num = st.session_state.correct_numerator
    correct_den = st.session_state.correct_denominator
    
    # Check if the answer is correct
    user_correct = (user_whole == correct_whole and 
                   user_num == correct_num and 
                   user_den == correct_den)
    
    # Also check if fraction part is equivalent
    fraction_equivalent = False
    if user_den != 0 and correct_den != 0 and user_num != 0:
        fraction_equivalent = (user_num * correct_den == user_den * correct_num)
    
    if user_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.mixed_numbers_difficulty
        st.session_state.mixed_numbers_difficulty = min(
            st.session_state.mixed_numbers_difficulty + 1, 4
        )
        
        # Show encouragement based on difficulty
        if st.session_state.mixed_numbers_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've reached Expert level!**")
        elif old_difficulty < st.session_state.mixed_numbers_difficulty:
            difficulty_names = {2: "Medium", 3: "Advanced", 4: "Expert"}
            st.info(f"⬆️ **Level up! Now at {difficulty_names[st.session_state.mixed_numbers_difficulty]} level**")
    
    elif user_whole == correct_whole and fraction_equivalent and user_num != correct_num:
        st.warning(f"🤔 **Almost there!** The fraction part should be in lowest terms.")
        st.info(f"The correct answer is **{correct_whole} {correct_num}/{correct_den}**")
        show_explanation()
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_whole} {correct_num}/{correct_den}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.mixed_numbers_difficulty
        st.session_state.mixed_numbers_difficulty = max(
            st.session_state.mixed_numbers_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.mixed_numbers_difficulty:
            difficulty_names = {1: "Basic", 2: "Medium", 3: "Advanced"}
            st.warning(f"⬇️ **Difficulty decreased to {difficulty_names[st.session_state.mixed_numbers_difficulty]} level. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show detailed explanation for the correct answer"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### How to find the mixed number:
        
        **Step 1: Count the whole shapes**
        - Number of completely filled {data['shape']}s: **{data['whole']}**
        
        **Step 2: Count the partial shape**
        - Parts filled: **{data['original_numerator']}**
        - Total parts in one {data['shape']}: **{data['original_denominator']}**
        - Fraction: {data['original_numerator']}/{data['original_denominator']}
        """)
        
        # If fraction needs simplification
        if data['original_numerator'] != data['numerator']:
            gcd_value = math.gcd(data['original_numerator'], data['original_denominator'])
            st.markdown(f"""
        **Step 3: Simplify the fraction**
        - {data['original_numerator']}/{data['original_denominator']} ÷ {gcd_value}/{gcd_value} = **{data['numerator']}/{data['denominator']}**
        """)
        
        st.markdown(f"""
        **Answer: {data['whole']} {data['numerator']}/{data['denominator']}**
        
        This means "{data['whole']} whole {data['shape']}{'s' if data['whole'] > 1 else ''} and {data['numerator']} out of {data['denominator']} parts"
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_whole = None
    st.session_state.correct_numerator = None
    st.session_state.correct_denominator = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "submitted_whole" in st.session_state:
        del st.session_state.submitted_whole
    if "submitted_numerator" in st.session_state:
        del st.session_state.submitted_numerator
    if "submitted_denominator" in st.session_state:
        del st.session_state.submitted_denominator