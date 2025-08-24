import streamlit as st
import random

def run():
    """
    Main function to run the Add, subtract, multiply and divide decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/add_subtract_multiply_and_divide_decimals.py
    """
    # Initialize session state
    if "decimal_difficulty" not in st.session_state:
        st.session_state.decimal_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("🔢 Add, Subtract, Multiply and Divide Decimals")
    st.markdown("*Master decimal operations with precision*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Tenths", "Hundredths", "Mixed Places", "Complex", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_decimal_problem()
    
    # Display current problem
    display_decimal_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Decimal Operations Guide**", expanded=False):
        st.markdown("""
        ### Key Rules for Decimal Operations:
        
        **➕ Addition & ➖ Subtraction:**
        - **Line up the decimal points** vertically
        - Add zeros to make equal decimal places
        - Add/subtract as with whole numbers
        - Keep decimal point in the same position
        
        **Example:**
        ```
          4.99
        + 0.55
        ------
          5.54
        ```
        
        **✖️ Multiplication:**
        - Multiply ignoring decimal points
        - Count total decimal places in both numbers
        - Place decimal point that many places from right
        
        **Example:**
        ```
        0.1 × 6 = ?
        1 × 6 = 6
        1 decimal place total
        Answer: 0.6
        ```
        
        **➗ Division:**
        - Move decimal in divisor to make whole number
        - Move decimal in dividend same number of places
        - Divide as normal
        - Place decimal point directly above in quotient
        
        **Example:**
        ```
        263.1 ÷ 10 = 26.31
        (Move decimal 1 place left)
        ```
        
        ### Decimal Place Values:
        - **Tenths:** 0.1, 0.2, 0.3...
        - **Hundredths:** 0.01, 0.02, 0.03...
        - **Thousandths:** 0.001, 0.002, 0.003...
        
        ### Tips:
        - Always estimate first to check reasonableness
        - Use zeros as placeholders when needed
        - Check by using inverse operation
        """)

def generate_new_decimal_problem():
    """Generate a new decimal problem based on difficulty"""
    difficulty = st.session_state.decimal_difficulty
    
    # Choose operation
    if difficulty == 1:
        operations = ["add", "subtract"]
    else:
        operations = ["add", "subtract", "multiply", "divide"]
    
    operation = random.choice(operations)
    
    # Generate numbers based on operation and difficulty
    if operation == "add":
        if difficulty == 1:  # Tenths
            num1 = round(random.uniform(0.1, 9.9), 1)
            num2 = round(random.uniform(0.1, 9.9), 1)
        elif difficulty == 2:  # Hundredths
            num1 = round(random.uniform(0.01, 9.99), 2)
            num2 = round(random.uniform(0.01, 9.99), 2)
        elif difficulty == 3:  # Mixed places
            num1 = round(random.uniform(10, 99.99), 2)
            num2 = round(random.uniform(0.1, 9.99), random.randint(1, 2))
        elif difficulty == 4:  # Complex
            num1 = round(random.uniform(10, 999.999), 3)
            num2 = round(random.uniform(0.01, 99.99), 2)
        else:  # Master
            num1 = round(random.uniform(100, 9999.999), 3)
            num2 = round(random.uniform(0.001, 999.999), 3)
        
        answer = round(num1 + num2, 6)  # Keep precision
        
    elif operation == "subtract":
        if difficulty == 1:  # Tenths
            num1 = round(random.uniform(5, 99.9), 1)
            num2 = round(random.uniform(0.1, num1-0.1), 1)
        elif difficulty == 2:  # Hundredths
            num1 = round(random.uniform(10, 99.99), 2)
            num2 = round(random.uniform(0.01, num1-0.01), 2)
        elif difficulty == 3:  # Mixed places
            num1 = round(random.uniform(50, 999.9), 1)
            num2 = round(random.uniform(0.01, min(num1-0.1, 99.99)), 2)
        elif difficulty == 4:  # Complex
            num1 = round(random.uniform(100, 999.999), 3)
            num2 = round(random.uniform(0.001, min(num1-0.1, 99.999)), 3)
        else:  # Master
            num1 = round(random.uniform(1000, 9999.999), 3)
            num2 = round(random.uniform(0.001, min(num1-1, 999.999)), 3)
        
        answer = round(num1 - num2, 6)
        
    elif operation == "multiply":
        if difficulty == 2:  # Start with simple
            num1 = round(random.uniform(0.1, 9.9), 1)
            num2 = random.randint(2, 9)
        elif difficulty == 3:  # Decimal × whole
            num1 = round(random.uniform(0.01, 99.99), 2)
            num2 = random.randint(2, 99)
        elif difficulty == 4:  # Decimal × decimal
            num1 = round(random.uniform(0.1, 99.9), 1)
            num2 = round(random.uniform(0.1, 9.9), 1)
        else:  # Master
            num1 = round(random.uniform(0.01, 999.99), 2)
            num2 = round(random.uniform(0.01, 99.99), 2)
        
        answer = round(num1 * num2, 6)
        
    else:  # division
        if difficulty == 2:  # Divide by 10, 100
            dividend = round(random.uniform(10, 999.9), 1)
            divisor = random.choice([10, 100])
            num1 = dividend
            num2 = divisor
        elif difficulty == 3:  # Simple decimal division
            divisor = random.randint(2, 9)
            result = round(random.uniform(0.1, 99.9), 1)
            num1 = round(divisor * result, 1)
            num2 = divisor
        elif difficulty == 4:  # Decimal ÷ decimal
            num2 = round(random.uniform(0.1, 9.9), 1)
            result = round(random.uniform(1, 99), 1)
            num1 = round(num2 * result, 2)
        else:  # Master
            num2 = round(random.uniform(0.01, 9.99), 2)
            result = round(random.uniform(10, 999), 2)
            num1 = round(num2 * result, 3)
        
        answer = round(num1 / num2, 6)
    
    # Clean up answer (remove trailing zeros)
    answer = float(f"{answer:.6f}".rstrip('0').rstrip('.'))
    
    st.session_state.problem_data = {
        "operation": operation,
        "num1": num1,
        "num2": num2
    }
    st.session_state.correct_answer = answer
    st.session_state.current_problem = operation

def display_decimal_problem():
    """Display the current decimal problem"""
    data = st.session_state.problem_data
    operation = data["operation"]
    num1 = data["num1"]
    num2 = data["num2"]
    
    # Display operation type
    operation_names = {
        "add": "Add",
        "subtract": "Subtract",
        "multiply": "Multiply",
        "divide": "Divide"
    }
    operation_symbols = {
        "add": "+",
        "subtract": "-",
        "multiply": "×",
        "divide": "÷"
    }
    
    st.markdown(f"### {operation_names[operation]}:")
    
    # Display the problem based on operation
    if operation in ["add", "subtract"]:
        # Vertical format for addition/subtraction
        display_vertical_decimal_problem(num1, num2, operation_symbols[operation])
    else:
        # Horizontal format for multiplication/division
        display_horizontal_decimal_problem(num1, num2, operation_symbols[operation])
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        user_answer = st.number_input(
            "Your answer:",
            min_value=-99999.0,
            max_value=99999.0,
            step=0.001,
            format="%.6f",
            key="decimal_answer_input"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            # Clean up user answer (remove trailing zeros)
            cleaned_answer = float(f"{user_answer:.6f}".rstrip('0').rstrip('.'))
            st.session_state.user_answer = cleaned_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_vertical_decimal_problem(num1, num2, operator):
    """Display vertical format for addition/subtraction"""
    # Format numbers to align decimal points
    str1 = f"{num1:.6f}".rstrip('0').rstrip('.')
    str2 = f"{num2:.6f}".rstrip('0').rstrip('.')
    
    # Find decimal positions
    dec1 = str1.find('.')
    dec2 = str2.find('.')
    
    # Calculate padding
    if dec1 == -1:
        str1 += ".0"
        dec1 = str1.find('.')
    if dec2 == -1:
        str2 += ".0"
        dec2 = str2.find('.')
    
    # Get integer and decimal parts
    int1, frac1 = str1.split('.')
    int2, frac2 = str2.split('.')
    
    # Pad to align
    max_int = max(len(int1), len(int2))
    max_frac = max(len(frac1), len(frac2))
    
    str1_padded = f"{int1:>{max_int}}.{frac1:<{max_frac}}"
    str2_padded = f"{int2:>{max_int}}.{frac2:<{max_frac}}"
    
    st.markdown(f"""
    <div style="
        font-family: 'Courier New', monospace;
        font-size: 28px;
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 10px;
        display: inline-block;
        margin: 20px 0;
        border: 2px solid #dee2e6;
    ">
        <div style="text-align: right;">
            <div style="margin-bottom: 5px;">{str1_padded}</div>
            <div style="margin-bottom: 5px;">{operator} {str2_padded}</div>
            <div style="border-top: 3px solid #333; margin-top: 10px; padding-top: 10px;">
                <span style="color: transparent;">{'_' * (max_int + max_frac + 1)}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_horizontal_decimal_problem(num1, num2, operator):
    """Display horizontal format for multiplication/division"""
    # Format numbers nicely
    str1 = f"{num1:.6f}".rstrip('0').rstrip('.')
    str2 = f"{num2:.6f}".rstrip('0').rstrip('.')
    
    if operator == "÷" and num2 >= 10:
        # Long division format
        st.markdown(f"""
        <div style="
            font-family: 'Courier New', monospace;
            font-size: 28px;
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            display: inline-block;
            margin: 20px 0;
            border: 2px solid #dee2e6;
        ">
            <div>
                <span style="margin-right: 10px;">{str2}</span>
                <span style="border-left: 3px solid #333; border-top: 3px solid #333; padding-left: 10px;">
                    {str1}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Standard horizontal format
        st.markdown(f"""
        <div style="
            font-family: 'Courier New', monospace;
            font-size: 32px;
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            display: inline-block;
            margin: 20px 0;
            border: 2px solid #dee2e6;
        ">
            <div>
                {str1} {operator} {str2} = ?
            </div>
        </div>
        """, unsafe_allow_html=True)

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    operation = st.session_state.problem_data["operation"]
    
    # Check if answer is correct (with small tolerance for decimal precision)
    is_correct = abs(user_answer - correct_answer) < 0.0001
    
    # Format answers for display
    correct_display = f"{correct_answer:.6f}".rstrip('0').rstrip('.')
    user_display = f"{user_answer:.6f}".rstrip('0').rstrip('.')
    
    if is_correct:
        st.success(f"🎉 **Excellent! {correct_display} is correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.decimal_difficulty
        st.session_state.decimal_difficulty = min(
            st.session_state.decimal_difficulty + 1, 5
        )
        
        if st.session_state.decimal_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've mastered decimal operations!**")
        elif old_difficulty < st.session_state.decimal_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decimal_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_display}**")
        st.error(f"You answered: {user_display}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.decimal_difficulty
        st.session_state.decimal_difficulty = max(
            st.session_state.decimal_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimal_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.decimal_difficulty}. Keep practicing!**")
        
        # Show solution
        show_decimal_solution()

def show_decimal_solution():
    """Show detailed solution for decimal operations"""
    data = st.session_state.problem_data
    operation = data["operation"]
    num1 = data["num1"]
    num2 = data["num2"]
    answer = st.session_state.correct_answer
    
    with st.expander("📖 **Solution Explained**", expanded=True):
        if operation == "add":
            st.markdown("""
            ### Addition with Decimals:
            
            **Step 1:** Line up the decimal points
            **Step 2:** Add zeros if needed to make equal decimal places
            **Step 3:** Add as normal
            **Step 4:** Place decimal point in the answer
            """)
            
            # Show aligned addition
            show_aligned_calculation(num1, num2, "+", answer)
            
        elif operation == "subtract":
            st.markdown("""
            ### Subtraction with Decimals:
            
            **Step 1:** Line up the decimal points
            **Step 2:** Add zeros if needed
            **Step 3:** Subtract as normal
            **Step 4:** Place decimal point in the answer
            """)
            
            # Show aligned subtraction
            show_aligned_calculation(num1, num2, "-", answer)
            
        elif operation == "multiply":
            st.markdown(f"""
            ### Multiplication with Decimals:
            
            **Original problem:** {num1} × {num2}
            
            **Step 1:** Count decimal places
            - {num1} has {count_decimal_places(num1)} decimal place(s)
            - {num2} has {count_decimal_places(num2)} decimal place(s)
            - Total: {count_decimal_places(num1) + count_decimal_places(num2)} decimal place(s)
            
            **Step 2:** Multiply ignoring decimals
            - {int(num1 * 10**count_decimal_places(num1))} × {int(num2 * 10**count_decimal_places(num2))} = {int(num1 * 10**count_decimal_places(num1)) * int(num2 * 10**count_decimal_places(num2))}
            
            **Step 3:** Place decimal point
            - Count {count_decimal_places(num1) + count_decimal_places(num2)} places from right
            - Answer: **{answer}**
            """)
            
        else:  # division
            st.markdown(f"""
            ### Division with Decimals:
            
            **Original problem:** {num1} ÷ {num2}
            """)
            
            if num2 == 10 or num2 == 100 or num2 == 1000:
                st.markdown(f"""
                **Special case:** Dividing by {num2}
                - Move decimal point {len(str(int(num2))) - 1} place(s) to the left
                - {num1} → **{answer}**
                """)
            else:
                st.markdown(f"""
                **Method:** Direct division
                - {num1} ÷ {num2} = **{answer}**
                
                **Check:** {num2} × {answer} = {round(num2 * answer, 6)}
                """)

def show_aligned_calculation(num1, num2, operator, answer):
    """Show aligned calculation for addition/subtraction"""
    # Format numbers
    str1 = f"{num1:.6f}".rstrip('0').rstrip('.')
    str2 = f"{num2:.6f}".rstrip('0').rstrip('.')
    str_ans = f"{answer:.6f}".rstrip('0').rstrip('.')
    
    st.markdown(f"""
    ```
      {str1}
    {operator} {str2}
    ────────
      {str_ans}
    ```
    """)

def count_decimal_places(num):
    """Count decimal places in a number"""
    str_num = f"{num:.6f}".rstrip('0').rstrip('.')
    if '.' not in str_num:
        return 0
    return len(str_num.split('.')[1])

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer