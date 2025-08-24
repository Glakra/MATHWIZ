import streamlit as st
import random

def run():
    """
    Main function for Perimeter of Rectangles practice.
    Students calculate the perimeter of rectangles and squares with labeled dimensions.
    """
    
    # Initialize session state
    if "perimeter_difficulty" not in st.session_state:
        st.session_state.perimeter_difficulty = 1  # Start with simple numbers
    
    if "current_perimeter_problem" not in st.session_state:
        st.session_state.current_perimeter_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("📏 Perimeter of Rectangles")
    st.markdown("*Calculate the perimeter by adding all sides of the rectangle*")
    st.markdown("---")
    
    # Difficulty indicator and progress
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple (whole numbers < 10)",
            2: "Medium (whole numbers 10-50)",
            3: "Large (whole numbers 50-100)",
            4: "Mixed units & decimals"
        }
        st.markdown(f"**Difficulty Level:** {difficulty_names[st.session_state.perimeter_difficulty]}")
        progress = st.session_state.perimeter_difficulty / 4
        st.progress(progress)
    
    with col2:
        if st.session_state.total_attempted > 0:
            accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_perimeter_problem is None:
        generate_perimeter_problem()
    
    # Display the problem
    display_perimeter_problem()
    
    # Instructions
    with st.expander("💡 **How to Calculate Perimeter**", expanded=False):
        st.markdown("""
        ### What is Perimeter?
        The **perimeter** is the total distance around the outside of a shape.
        
        ### For Rectangles:
        **Method 1:** Add all four sides
        - Perimeter = length + width + length + width
        - Perimeter = top + right + bottom + left
        
        **Method 2:** Use the formula
        - Perimeter = 2 × (length + width)
        - Or: Perimeter = 2 × length + 2 × width
        
        ### For Squares:
        - All four sides are equal
        - Perimeter = 4 × side length
        
        ### Examples:
        - Rectangle 5m × 3m: Perimeter = 5 + 3 + 5 + 3 = 16m
        - Square 4cm × 4cm: Perimeter = 4 × 4 = 16cm
        
        ### Remember:
        - ✅ Include the unit (m, cm, etc.) in your answer
        - ✅ Add ALL four sides
        - ✅ Check: opposite sides of a rectangle are equal
        """)

def generate_perimeter_problem():
    """Generate a perimeter problem based on difficulty"""
    
    difficulty = st.session_state.perimeter_difficulty
    
    if difficulty == 1:
        # Simple: whole numbers < 10
        shapes = [
            {"type": "rectangle", "length": 5, "width": 3, "unit": "m"},
            {"type": "rectangle", "length": 7, "width": 4, "unit": "cm"},
            {"type": "square", "side": 6, "unit": "m"},
            {"type": "rectangle", "length": 8, "width": 2, "unit": "cm"},
            {"type": "square", "side": 5, "unit": "m"},
            {"type": "rectangle", "length": 9, "width": 6, "unit": "cm"},
        ]
        
    elif difficulty == 2:
        # Medium: whole numbers 10-50
        shapes = [
            {"type": "rectangle", "length": 12, "width": 11, "unit": "m"},
            {"type": "rectangle", "length": 25, "width": 15, "unit": "cm"},
            {"type": "square", "side": 18, "unit": "m"},
            {"type": "rectangle", "length": 34, "width": 22, "unit": "cm"},
            {"type": "rectangle", "length": 45, "width": 30, "unit": "m"},
            {"type": "square", "side": 27, "unit": "cm"},
        ]
        
    elif difficulty == 3:
        # Large: whole numbers 50-100
        shapes = [
            {"type": "rectangle", "length": 75, "width": 50, "unit": "m"},
            {"type": "rectangle", "length": 88, "width": 62, "unit": "cm"},
            {"type": "square", "side": 65, "unit": "m"},
            {"type": "rectangle", "length": 95, "width": 70, "unit": "cm"},
            {"type": "rectangle", "length": 100, "width": 85, "unit": "m"},
            {"type": "square", "side": 73, "unit": "cm"},
        ]
        
    else:  # difficulty == 4
        # Mixed units and decimals
        shapes = [
            {"type": "rectangle", "length": 12.5, "width": 8.5, "unit": "m"},
            {"type": "rectangle", "length": 15.2, "width": 10.8, "unit": "cm"},
            {"type": "square", "side": 9.6, "unit": "m"},
            {"type": "rectangle", "length": 24.75, "width": 18.25, "unit": "cm"},
            {"type": "rectangle", "length": 7.4, "width": 5.6, "unit": "km"},
            {"type": "square", "side": 11.5, "unit": "mm"},
        ]
    
    # Select a random shape
    shape = random.choice(shapes)
    
    # Calculate the correct perimeter
    if shape["type"] == "square":
        perimeter = 4 * shape["side"]
        shape["length"] = shape["side"]
        shape["width"] = shape["side"]
    else:
        perimeter = 2 * (shape["length"] + shape["width"])
    
    # Round if necessary for decimal answers
    if isinstance(perimeter, float):
        perimeter = round(perimeter, 2)
    
    st.session_state.current_perimeter_problem = {
        "shape": shape,
        "correct_answer": perimeter,
        "unit": shape["unit"]
    }

def display_perimeter_problem():
    """Display the current perimeter problem"""
    
    if st.session_state.current_perimeter_problem is None:
        return
    
    problem = st.session_state.current_perimeter_problem
    shape = problem["shape"]
    
    # Display the question
    st.markdown("### What is the perimeter of the rectangle?")
    
    # Draw the rectangle with labeled dimensions using a simpler approach
    draw_rectangle_simple(shape)
    
    # Answer input section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Use form to handle Enter key submission
        with st.form("answer_form", clear_on_submit=False):
            user_input = st.text_input(
                "Enter your answer:",
                value=st.session_state.user_answer,
                disabled=st.session_state.answer_submitted,
                placeholder=f"Type your answer here"
            )
            
            # Unit display
            unit_text = get_unit_text(problem["unit"])
            st.markdown(f"**Unit: {unit_text}**")
            
            submitted = st.form_submit_button(
                "Submit",
                type="primary",
                disabled=st.session_state.answer_submitted
            )
            
            if submitted and user_input:
                st.session_state.user_answer = user_input
                check_answer()
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def draw_rectangle_simple(shape):
    """Draw a rectangle with labeled dimensions using a simpler HTML/CSS approach"""
    
    # Format dimension labels
    def format_dimension(value):
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            else:
                return str(value)
        return str(value)
    
    length_label = f"{format_dimension(shape['length'])} {shape['unit']}"
    width_label = f"{format_dimension(shape['width'])} {shape['unit']}"
    
    # Choose color based on difficulty
    colors = {
        1: "#DDA0DD",  # Plum (matching your first image)
        2: "#B19CD9",  # Light purple (matching your second image)
        3: "#90EE90",  # Light green (matching your third image)
        4: "#87CEEB"   # Sky blue (matching your fourth image)
    }
    fill_color = colors.get(st.session_state.perimeter_difficulty, "#87CEEB")
    
    # Calculate display dimensions
    max_width = 300
    max_height = 200
    
    # Calculate aspect ratio
    if shape["length"] >= shape["width"]:
        display_width = max_width
        display_height = int(max_width * shape["width"] / shape["length"])
        display_height = max(display_height, 80)  # Minimum height
    else:
        display_height = max_height
        display_width = int(max_height * shape["length"] / shape["width"])
        display_width = max(display_width, 100)  # Minimum width
    
    # Create the rectangle display using HTML/CSS
    rectangle_html = f"""
    <style>
        .perimeter-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 30px 0;
            position: relative;
        }}
        .rectangle-wrapper {{
            position: relative;
            display: inline-block;
        }}
        .rectangle {{
            width: {display_width}px;
            height: {display_height}px;
            background-color: {fill_color};
            border: 2px solid #333;
            position: relative;
        }}
        .dimension-label {{
            position: absolute;
            font-weight: bold;
            font-size: 14px;
            color: #333;
        }}
        .top-label {{
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
        }}
        .bottom-label {{
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
        }}
        .left-label {{
            left: -60px;
            top: 50%;
            transform: translateY(-50%);
        }}
        .right-label {{
            right: -60px;
            top: 50%;
            transform: translateY(-50%);
        }}
    </style>
    
    <div class="perimeter-container">
        <div class="rectangle-wrapper">
            <div class="dimension-label top-label">{length_label}</div>
            <div class="dimension-label bottom-label">{length_label}</div>
            <div class="dimension-label left-label">{width_label}</div>
            <div class="dimension-label right-label">{width_label}</div>
            <div class="rectangle"></div>
        </div>
    </div>
    """
    
    st.markdown(rectangle_html, unsafe_allow_html=True)

def get_unit_text(unit):
    """Get the full text for units"""
    unit_map = {
        "m": "metres",
        "cm": "centimetres",
        "mm": "millimetres",
        "km": "kilometres",
        "ft": "feet",
        "in": "inches"
    }
    return unit_map.get(unit, unit)

def check_answer():
    """Check if the user's answer is correct"""
    
    problem = st.session_state.current_perimeter_problem
    correct_answer = problem["correct_answer"]
    
    try:
        # Parse user answer (handle both integer and decimal inputs)
        user_answer = float(st.session_state.user_answer.strip())
        
        # Check if answer is correct (allow small tolerance for decimals)
        if abs(user_answer - correct_answer) < 0.01:
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            is_correct = True
            
            # Increase difficulty after 3 consecutive correct
            if st.session_state.consecutive_correct >= 3:
                if st.session_state.perimeter_difficulty < 4:
                    st.session_state.perimeter_difficulty += 1
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            is_correct = False
            
            # Decrease difficulty after 2 wrong
            if st.session_state.total_attempted > st.session_state.total_correct + 1:
                if st.session_state.perimeter_difficulty > 1:
                    st.session_state.perimeter_difficulty -= 1
        
        st.session_state.answer_submitted = True
        st.session_state.show_feedback = True
        st.session_state.total_attempted += 1
        
    except (ValueError, AttributeError):
        st.error("Please enter a valid number")
        st.session_state.user_answer = ""

def show_feedback():
    """Display feedback for the answer"""
    
    problem = st.session_state.current_perimeter_problem
    correct_answer = problem["correct_answer"]
    shape = problem["shape"]
    
    try:
        user_answer = float(st.session_state.user_answer.strip())
        
        if abs(user_answer - correct_answer) < 0.01:
            st.success(f"🎉 **Correct! The perimeter is {correct_answer} {problem['unit']}**")
            
            if st.session_state.consecutive_correct == 2:
                st.info("🔥 One more correct answer to level up!")
        else:
            st.error(f"❌ **Not quite right. The correct answer is {correct_answer} {problem['unit']}**")
            
            # Show detailed solution
            with st.expander("📖 **See the solution**", expanded=True):
                st.markdown("### Step-by-step solution:")
                
                if shape["type"] == "square":
                    st.markdown(f"""
                    This is a **square** with all sides equal to **{shape['side']} {shape['unit']}**
                    
                    **Method 1: Add all four sides**
                    - Perimeter = {shape['side']} + {shape['side']} + {shape['side']} + {shape['side']}
                    - Perimeter = {correct_answer} {shape['unit']}
                    
                    **Method 2: Use the square formula**
                    - Perimeter = 4 × side
                    - Perimeter = 4 × {shape['side']}
                    - Perimeter = {correct_answer} {shape['unit']}
                    """)
                else:
                    sum_two_sides = shape['length'] + shape['width']
                    st.markdown(f"""
                    This is a **rectangle** with:
                    - Length = **{shape['length']} {shape['unit']}**
                    - Width = **{shape['width']} {shape['unit']}**
                    
                    **Method 1: Add all four sides**
                    - Perimeter = {shape['length']} + {shape['width']} + {shape['length']} + {shape['width']}
                    - Perimeter = {correct_answer} {shape['unit']}
                    
                    **Method 2: Use the rectangle formula**
                    - Perimeter = 2 × (length + width)
                    - Perimeter = 2 × ({shape['length']} + {shape['width']})
                    - Perimeter = 2 × {sum_two_sides}
                    - Perimeter = {correct_answer} {shape['unit']}
                    """)
                
                st.markdown(f"""
                ### Your answer: {user_answer} {shape['unit']}
                ### Correct answer: {correct_answer} {shape['unit']}
                
                **Remember:** Always add ALL four sides of the rectangle!
                """)
                
    except (ValueError, AttributeError):
        pass

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_perimeter_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""