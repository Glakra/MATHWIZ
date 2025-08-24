import streamlit as st
import random

def run():
    """
    Main function to run the Inequalities with decimal multiplication activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/inequalities_with_decimal_multiplication.py
    """
    # Initialize session state
    if "multiplication_inequality_problem" not in st.session_state:
        st.session_state.multiplication_inequality_problem = None
        st.session_state.multiplication_inequality_submitted = False
        st.session_state.selected_multiplication_sign = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("⚖️ Inequalities with Decimal Multiplication")
    st.markdown("*Calculate the product, then choose the correct sign*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.multiplication_inequality_problem is None:
        st.session_state.multiplication_inequality_problem = generate_problem()
        st.session_state.multiplication_inequality_submitted = False
        st.session_state.selected_multiplication_sign = None
    
    problem = st.session_state.multiplication_inequality_problem
    
    # Display the question
    st.markdown("### 📝 Which sign makes the statement true?")
    
    # Display the inequality with a placeholder for the sign
    display_inequality(problem)
    
    # Sign selection buttons
    st.markdown("### Choose a sign:")
    col1, col2, col3 = st.columns(3)
    
    # Use text representations for buttons
    signs = [">", "<", "="]
    button_labels = [">", "<", "="]
    sign_meanings = {
        ">": "greater than",
        "<": "less than", 
        "=": "equal to"
    }
    
    # Track which button was clicked
    with col1:
        if st.button(
            button_labels[0],
            key="mult_sign_0",
            use_container_width=True,
            type="secondary" if st.session_state.selected_multiplication_sign != signs[0] else "primary",
            disabled=st.session_state.multiplication_inequality_submitted,
            help=sign_meanings[signs[0]]
        ):
            st.session_state.selected_multiplication_sign = signs[0]
            st.rerun()
    
    with col2:
        if st.button(
            button_labels[1],
            key="mult_sign_1",
            use_container_width=True,
            type="secondary" if st.session_state.selected_multiplication_sign != signs[1] else "primary",
            disabled=st.session_state.multiplication_inequality_submitted,
            help=sign_meanings[signs[1]]
        ):
            st.session_state.selected_multiplication_sign = signs[1]
            st.rerun()
    
    with col3:
        if st.button(
            button_labels[2],
            key="mult_sign_2",
            use_container_width=True,
            type="secondary" if st.session_state.selected_multiplication_sign != signs[2] else "primary",
            disabled=st.session_state.multiplication_inequality_submitted,
            help=sign_meanings[signs[2]]
        ):
            st.session_state.selected_multiplication_sign = signs[2]
            st.rerun()
    
    # Alternative radio button option
    st.markdown("#### Or select from these options:")
    options = [
        ("greater than (>)", ">"),
        ("less than (<)", "<"),
        ("equal to (=)", "=")
    ]
    
    selected_option = st.radio(
        "Select comparison:",
        options=[opt[1] for opt in options],
        format_func=lambda x: next(opt[0] for opt in options if opt[1] == x),
        horizontal=True,
        key="mult_sign_radio",
        disabled=st.session_state.multiplication_inequality_submitted,
        label_visibility="collapsed"
    )
    
    if selected_option and not st.session_state.multiplication_inequality_submitted:
        st.session_state.selected_multiplication_sign = selected_option
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.multiplication_inequality_submitted or 
                     st.session_state.selected_multiplication_sign is None):
            st.session_state.multiplication_inequality_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.multiplication_inequality_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.multiplication_inequality_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.multiplication_inequality_problem = None
                st.session_state.multiplication_inequality_submitted = False
                st.session_state.selected_multiplication_sign = None
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Calculate** the multiplication
        2. **Compare** the result with the other number
        3. **Choose** the correct sign: >, <, or =
        
        ### Understanding the Signs:
        - **>** means "greater than" (left side is bigger)
        - **<** means "less than" (left side is smaller)
        - **=** means "equal to" (both sides are the same)
        
        ### Examples:
        - `9 × 0.2 ? 2`
          - Calculate: 9 × 0.2 = 1.8
          - Compare: 1.8 ? 2
          - Since 1.8 < 2, answer is 
        
        - `10 ? 4.5 × 2`
          - Calculate: 4.5 × 2 = 9
          - Compare: 10 ? 9
          - Since 10 > 9, answer is >
        
        ### Tips for Decimal Multiplication:
        - **Count decimal places** in the decimal factor
        - **Multiply** as if there's no decimal
        - **Place the decimal** in your answer
        
        ### Remember:
        - Calculate the product first
        - Then compare the two values
        - Double-check your multiplication
        """)

def generate_problem():
    """Generate a random multiplication inequality problem"""
    problem_types = [
        'product_left',     # (whole × decimal) ? number
        'product_right',    # number ? (decimal × whole)
        'both_products'     # (whole × decimal) ? (whole × decimal)
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'product_left':
        # Format: (whole × decimal) ? number
        whole = random.randint(2, 20)
        decimal = round(random.uniform(0.1, 0.9), 1)
        product = round(whole * decimal, 2)
        
        # Generate comparison number
        # Sometimes make it equal, sometimes different
        if random.random() < 0.2:  # 20% chance of equality
            compare_num = product
        else:
            # Make it close but different
            offset = random.uniform(-3, 3)
            compare_num = round(product + offset, 1)
            if compare_num < 0:
                compare_num = round(random.uniform(0.5, 5), 1)
        
        left_expression = f"{whole} × {decimal}"
        right_expression = str(compare_num)
        left_value = product
        right_value = compare_num
        
    elif problem_type == 'product_right':
        # Format: number ? (decimal × whole)
        decimal = round(random.uniform(0.1, 5.9), 1)
        whole = random.randint(2, 12)
        product = round(decimal * whole, 2)
        
        # Generate comparison number
        if random.random() < 0.2:  # 20% chance of equality
            compare_num = product
        else:
            offset = random.uniform(-5, 5)
            compare_num = round(product + offset, 1)
            if compare_num < 0:
                compare_num = round(random.uniform(1, 10), 1)
        
        left_expression = str(compare_num)
        right_expression = f"{decimal} × {whole}"
        left_value = compare_num
        right_value = product
        
    else:  # both_products
        # Format: (whole × decimal) ? (whole × decimal)
        whole1 = random.randint(2, 15)
        decimal1 = round(random.uniform(0.1, 2.9), 1)
        product1 = round(whole1 * decimal1, 2)
        
        whole2 = random.randint(2, 15)
        decimal2 = round(random.uniform(0.1, 2.9), 1)
        product2 = round(whole2 * decimal2, 2)
        
        left_expression = f"{whole1} × {decimal1}"
        right_expression = f"{whole2} × {decimal2}"
        left_value = product1
        right_value = product2
    
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
        'correct_sign': correct_sign,
        'type': problem_type
    }

def display_inequality(problem):
    """Display the inequality with the selected sign or placeholder"""
    if st.session_state.selected_multiplication_sign:
        sign_display = st.session_state.selected_multiplication_sign
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
    problem = st.session_state.multiplication_inequality_problem
    selected_sign = st.session_state.selected_multiplication_sign
    
    # Check if answer is correct
    is_correct = selected_sign == problem['correct_sign']
    
    # Format signs for display
    sign_display = {
        ">": "greater than (>)",
        "<": "less than (<)",
        "=": "equal to (=)"
    }
    
    if is_correct:
        st.success("🎉 **Correct! Well done!**")
        
        # Show the calculation
        st.info(f"""
        ✓ {problem['left_expression']} = {problem['left_value']}  
        ✓ {problem['right_expression']} = {problem['right_value']}  
        ✓ {problem['left_value']} is {sign_display[problem['correct_sign']]} {problem['right_value']}
        """)
        
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{sign_display[problem['correct_sign']]}**")
        
        # Show detailed explanation
        with st.expander("📖 **See explanation**", expanded=True):
            st.markdown("### Let's work through this step by step:")
            
            # Calculate and show left side
            if '×' in problem['left_expression']:
                st.markdown(f"**Left side:** {problem['left_expression']}")
                parts = problem['left_expression'].split(' × ')
                st.markdown(f"Calculate: {parts[0]} × {parts[1]} = **{problem['left_value']}**")
            else:
                st.markdown(f"**Left side:** {problem['left_expression']} = **{problem['left_value']}**")
            
            # Calculate and show right side
            if '×' in problem['right_expression']:
                st.markdown(f"\n**Right side:** {problem['right_expression']}")
                parts = problem['right_expression'].split(' × ')
                st.markdown(f"Calculate: {parts[0]} × {parts[1]} = **{problem['right_value']}**")
            else:
                st.markdown(f"\n**Right side:** {problem['right_expression']} = **{problem['right_value']}**")
            
            # Compare
            st.markdown(f"\n**Compare:** {problem['left_value']} ? {problem['right_value']}")
            
            # Explain the correct sign
            if problem['correct_sign'] == ">":
                st.markdown(f"Since {problem['left_value']} is greater than {problem['right_value']}, we use **greater than (>)**")
            elif problem['correct_sign'] == "<":
                st.markdown(f"Since {problem['left_value']} is less than {problem['right_value']}, we use **less than (<)**")
            else:
                st.markdown(f"Since {problem['left_value']} equals {problem['right_value']}, we use **equal to (=)**")
            
            # Show complete statement
            st.markdown(f"\n**Answer:** {problem['left_expression']} is **{sign_display[problem['correct_sign']]}** {problem['right_expression']}")