import streamlit as st
import random

def run():
    """
    Main function to run the Inequalities with decimal addition and subtraction activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/G. Add and subtract decimals/inequalities_with_decimal_addition_and_subtraction.py
    """
    # Initialize session state
    if "inequality_problem" not in st.session_state:
        st.session_state.inequality_problem = None
        st.session_state.inequality_answer_submitted = False
        st.session_state.selected_sign = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > G. Add and subtract decimals**")
    st.title("⚖️ Inequalities with Decimal Addition and Subtraction")
    st.markdown("*Choose the correct sign to make the statement true*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.inequality_problem is None:
        st.session_state.inequality_problem = generate_problem()
        st.session_state.inequality_answer_submitted = False
        st.session_state.selected_sign = None
    
    problem = st.session_state.inequality_problem
    
    # Display the question
    st.markdown("### 📝 Which sign makes the statement true?")
    
    # Display the inequality with a placeholder for the sign
    display_inequality(problem)
    
    # Sign selection buttons
    st.markdown("### Choose a sign:")
    col1, col2, col3 = st.columns(3)
    
    # Use actual signs for internal logic but display labels for buttons
    signs = [">", "<", "="]
    sign_labels = [">", "<", "="]
    sign_meanings = {
        ">": "greater than",
        "<": "less than", 
        "=": "equal to"
    }
    
    # Track which button was clicked
    for i, (col, sign, label) in enumerate(zip([col1, col2, col3], signs, sign_labels)):
        with col:
            # Use HTML entities for button labels to avoid rendering issues
            button_label = label
            if label == ">":
                button_label = ">"
            elif label == "<":
                button_label = "<"
                
            if st.button(
                button_label,
                key=f"sign_{i}",
                use_container_width=True,
                type="secondary" if st.session_state.selected_sign != sign else "primary",
                disabled=st.session_state.inequality_answer_submitted,
                help=sign_meanings[sign]
            ):
                st.session_state.selected_sign = sign
                st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.inequality_answer_submitted or st.session_state.selected_sign is None):
            st.session_state.inequality_answer_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.inequality_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.inequality_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.inequality_problem = None
                st.session_state.inequality_answer_submitted = False
                st.session_state.selected_sign = None
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Calculate** the value on each side of the ? mark
        - **Compare** the two values
        - **Choose** the correct sign: >, <, or =
        - **Submit** your answer to check if you're right
        
        ### Understanding the Signs:
        - **>** means "greater than" (left side is bigger)
        - **<** means "less than" (left side is smaller)
        - **=** means "equal to" (both sides are the same)
        
        ### Tips for Success:
        1. **Calculate carefully:** Work out each expression step by step
        2. **Line up decimals:** When adding or subtracting, align decimal points
        3. **Double-check:** Verify your calculations before choosing a sign
        
        ### Examples:
        - `7.4 ? 8.2 - 0.7` → Calculate: 7.4 ? 7.5 → Answer: 
        - `3.5 + 1.2 ? 4.7` → Calculate: 4.7 ? 4.7 → Answer: =
        - `5.6 - 0.3 ? 5.0` → Calculate: 5.3 ? 5.0 → Answer: >
        
        ### Remember:
        - Take your time with decimal calculations
        - Check your work by substituting the sign back in
        - Think: "Which side is bigger?"
        """)

def generate_problem():
    """Generate a random inequality problem with decimal addition or subtraction"""
    problem_types = [
        'single_vs_expression',    # a ? b + c or a ? b - c
        'expression_vs_single',    # a + b ? c or a - b ? c
        'expression_vs_expression' # a + b ? c - d
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'single_vs_expression':
        # Format: number ? (number ± number)
        left_value = round(random.uniform(0.1, 10.0), 1)
        
        if random.choice([True, False]):
            # Addition on right
            b = round(random.uniform(0.1, 8.0), 1)
            c = round(random.uniform(0.1, 5.0), 1)
            right_value = round(b + c, 1)
            right_expression = f"{b} + {c}"
        else:
            # Subtraction on right
            b = round(random.uniform(2.0, 10.0), 1)
            c = round(random.uniform(0.1, b - 0.1), 1)
            right_value = round(b - c, 1)
            right_expression = f"{b} - {c}"
        
        left_expression = str(left_value)
    
    elif problem_type == 'expression_vs_single':
        # Format: (number ± number) ? number
        right_value = round(random.uniform(0.1, 10.0), 1)
        
        if random.choice([True, False]):
            # Addition on left
            a = round(random.uniform(0.1, 8.0), 1)
            b = round(random.uniform(0.1, 5.0), 1)
            left_value = round(a + b, 1)
            left_expression = f"{a} + {b}"
        else:
            # Subtraction on left
            a = round(random.uniform(2.0, 10.0), 1)
            b = round(random.uniform(0.1, a - 0.1), 1)
            left_value = round(a - b, 1)
            left_expression = f"{a} - {b}"
        
        right_expression = str(right_value)
    
    else:  # expression_vs_expression
        # Format: (number ± number) ? (number ± number)
        # Left side
        if random.choice([True, False]):
            a = round(random.uniform(0.1, 8.0), 1)
            b = round(random.uniform(0.1, 5.0), 1)
            left_value = round(a + b, 1)
            left_expression = f"{a} + {b}"
        else:
            a = round(random.uniform(2.0, 10.0), 1)
            b = round(random.uniform(0.1, a - 0.1), 1)
            left_value = round(a - b, 1)
            left_expression = f"{a} - {b}"
        
        # Right side
        if random.choice([True, False]):
            c = round(random.uniform(0.1, 8.0), 1)
            d = round(random.uniform(0.1, 5.0), 1)
            right_value = round(c + d, 1)
            right_expression = f"{c} + {d}"
        else:
            c = round(random.uniform(2.0, 10.0), 1)
            d = round(random.uniform(0.1, c - 0.1), 1)
            right_value = round(c - d, 1)
            right_expression = f"{c} - {d}"
    
    # Determine correct sign
    if abs(left_value - right_value) < 0.01:
        correct_sign = "="
    elif left_value > right_value:
        correct_sign = ">"
    else:
        correct_sign = "<"
    
    return {
        'left_expression': left_expression,
        'right_expression': right_expression,
        'left_value': left_value,
        'right_value': right_value,
        'correct_sign': correct_sign
    }

def display_inequality(problem):
    """Display the inequality with the selected sign or placeholder"""
    if st.session_state.selected_sign:
        sign_display = st.session_state.selected_sign
        sign_color = "#2196F3"  # Blue for selected
        # Use HTML entities for display
        if sign_display == ">":
            sign_display = "&gt;"
        elif sign_display == "<":
            sign_display = "&lt;"
    else:
        sign_display = "?"
        sign_color = "#666"  # Gray for placeholder
    
    # Create the inequality display
    inequality_html = f"""
    <div style="
        text-align: center;
        margin: 40px 0;
        font-size: 32px;
        font-family: 'Courier New', monospace;
        background-color: #f5f5f5;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #ddd;
    ">
        <span style="color: #333;">{problem['left_expression']}</span>
        <span style="
            display: inline-block;
            background-color: white;
            border: 2px solid {sign_color};
            border-radius: 50%;
            width: 50px;
            height: 50px;
            line-height: 46px;
            margin: 0 20px;
            color: {sign_color};
            font-weight: bold;
        ">{sign_display}</span>
        <span style="color: #333;">{problem['right_expression']}</span>
    </div>
    """
    
    st.markdown(inequality_html, unsafe_allow_html=True)

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.inequality_problem
    selected_sign = st.session_state.selected_sign
    
    # Check if answer is correct
    is_correct = selected_sign == problem['correct_sign']
    
    if is_correct:
        st.success("🎉 **Correct! Well done!**")
        
        # Show the calculation
        st.info(f"""
        ✓ {problem['left_expression']} = {problem['left_value']}  
        ✓ {problem['right_expression']} = {problem['right_value']}  
        ✓ {problem['left_value']} {problem['correct_sign']} {problem['right_value']}
        """)
        
    else:
        st.error(f"❌ **Not quite right.** The correct sign is **{problem['correct_sign']}**")
        
        # Show detailed explanation
        with st.expander("📖 **See explanation**", expanded=True):
            st.markdown("### Let's work through this step by step:")
            
            # Calculate left side
            st.markdown(f"**Left side:** {problem['left_expression']} = **{problem['left_value']}**")
            
            # Calculate right side
            st.markdown(f"**Right side:** {problem['right_expression']} = **{problem['right_value']}**")
            
            # Compare
            st.markdown(f"**Compare:** {problem['left_value']} ? {problem['right_value']}")
            
            # Explain the correct sign
            if problem['correct_sign'] == ">":
                st.markdown(f"Since {problem['left_value']} is greater than {problem['right_value']}, we use **>**")
            elif problem['correct_sign'] == "<":
                st.markdown(f"Since {problem['left_value']} is less than {problem['right_value']}, we use **<**")
            else:
                st.markdown(f"Since {problem['left_value']} equals {problem['right_value']}, we use **=**")
            
            # Show complete statement
            st.markdown(f"**Answer:** {problem['left_expression']} **{problem['correct_sign']}** {problem['right_expression']}")