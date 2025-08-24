import streamlit as st
import random
from decimal import Decimal

def run():
    """
    Main function to run the Add and Subtract Decimal Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/G. Add and subtract decimals/add_and_subtract_decimal_numbers.py
    """
    # Initialize session state
    if "decimal_difficulty" not in st.session_state:
        st.session_state.decimal_difficulty = 1  # Start with simple decimals
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_inputs = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > G. Add and subtract decimals**")
    st.title("➕➖ Add and Subtract Decimal Numbers")
    st.markdown("*Practice adding and subtracting decimals with proper place value alignment*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["One decimal place", "Two decimal places", "Mixed decimals", "Challenging"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level - 1]}")
        # Progress bar
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level} of 4")
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the problem** (addition or subtraction)
        - **Enter each digit** of your answer in the boxes
        - **Remember the decimal point** - it's already placed for you
        - **Submit your answer** to check if it's correct
        
        ### Tips for Success:
        - **Line up decimal points** vertically
        - **Add zeros if needed** to make equal decimal places
        - **Start from the right** and work left
        - **Regroup/borrow** just like with whole numbers
        
        ### Examples:
        - **Addition:** 3.4 + 2.5 = 5.9
        - **Addition with regrouping:** 6.7 + 4.8 = 11.5
        - **Subtraction:** 8.6 - 3.2 = 5.4
        - **Subtraction with borrowing:** 10.3 - 6.7 = 3.6
        
        ### Difficulty Levels:
        - **🟢 Basic:** One decimal place (tenths)
        - **🟡 Intermediate:** Two decimal places (hundredths)
        - **🟠 Advanced:** Mixed decimal places
        - **🔴 Expert:** Larger numbers with regrouping/borrowing
        """)

def generate_new_question():
    """Generate a new addition or subtraction question based on difficulty"""
    level = st.session_state.decimal_difficulty
    operation = random.choice(['add', 'subtract'])
    
    if level == 1:  # One decimal place
        if operation == 'add':
            # Simple addition
            num1 = round(random.uniform(0.1, 9.9), 1)
            num2 = round(random.uniform(0.1, 9.9), 1)
        else:
            # Simple subtraction (ensure positive result)
            num1 = round(random.uniform(5.0, 19.9), 1)
            num2 = round(random.uniform(0.1, num1 - 0.1), 1)
    
    elif level == 2:  # Two decimal places
        if operation == 'add':
            num1 = round(random.uniform(0.01, 99.99), 2)
            num2 = round(random.uniform(0.01, 99.99), 2)
        else:
            num1 = round(random.uniform(10.00, 99.99), 2)
            num2 = round(random.uniform(0.01, num1 - 0.01), 2)
    
    elif level == 3:  # Mixed decimal places
        if operation == 'add':
            # Mix of 1 and 2 decimal places
            if random.choice([True, False]):
                num1 = round(random.uniform(0.1, 99.9), 1)
                num2 = round(random.uniform(0.01, 99.99), 2)
            else:
                num1 = round(random.uniform(0.01, 99.99), 2)
                num2 = round(random.uniform(0.1, 99.9), 1)
        else:
            num1 = round(random.uniform(10.0, 199.99), random.choice([1, 2]))
            num2 = round(random.uniform(0.01, num1 - 0.01), random.choice([1, 2]))
    
    else:  # Expert - larger numbers
        if operation == 'add':
            num1 = round(random.uniform(0.01, 999.99), 2)
            num2 = round(random.uniform(0.01, 999.99), 2)
        else:
            num1 = round(random.uniform(100.00, 999.99), 2)
            num2 = round(random.uniform(0.01, num1 - 0.01), 2)
    
    # Calculate answer
    if operation == 'add':
        answer = Decimal(str(num1)) + Decimal(str(num2))
        operation_symbol = '+'
        operation_word = 'Add'
    else:
        answer = Decimal(str(num1)) - Decimal(str(num2))
        operation_symbol = '-'
        operation_word = 'Subtract'
    
    # Convert answer to string to handle decimal places properly
    answer_str = str(answer)
    
    st.session_state.question_data = {
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'operation_symbol': operation_symbol,
        'operation_word': operation_word,
        'answer': float(answer),
        'answer_str': answer_str
    }
    st.session_state.correct_answer = float(answer)
    st.session_state.current_question = f"{operation_word}."
    st.session_state.user_inputs = {}

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📊 {data['operation_word']}.")
    
    # Format numbers for display
    num1_str = f"{data['num1']:.2f}" if '.' in str(data['num1']) else str(data['num1'])
    num2_str = f"{data['num2']:.2f}" if '.' in str(data['num2']) else str(data['num2'])
    
    # Remove trailing zeros
    num1_str = num1_str.rstrip('0').rstrip('.') if '.' in num1_str else num1_str
    num2_str = num2_str.rstrip('0').rstrip('.') if '.' in num2_str else num2_str
    
    # Get answer structure
    answer_str = data['answer_str']
    if '.' in answer_str:
        whole_part, decimal_part = answer_str.split('.')
    else:
        whole_part = answer_str
        decimal_part = ""
    
    # Parse numbers to align properly
    num1_parts = num1_str.split('.') if '.' in num1_str else [num1_str, '']
    num2_parts = num2_str.split('.') if '.' in num2_str else [num2_str, '']
    
    # Determine maximum digits
    max_whole_digits = max(len(num1_parts[0]), len(num2_parts[0]), len(whole_part))
    max_decimal_digits = max(len(num1_parts[1]) if len(num1_parts) > 1 else 0,
                            len(num2_parts[1]) if len(num2_parts) > 1 else 0,
                            len(decimal_part))
    
    # Pad numbers for alignment
    num1_whole = num1_parts[0].rjust(max_whole_digits)
    num2_whole = num2_parts[0].rjust(max_whole_digits)
    
    num1_decimal = num1_parts[1].ljust(max_decimal_digits) if len(num1_parts) > 1 else ''
    num2_decimal = num2_parts[1].ljust(max_decimal_digits) if len(num2_parts) > 1 else ''
    
    # Create HTML for the math problem
    problem_html = f"""
    <div style='display: flex; justify-content: center; margin: 20px 0;'>
        <div style='font-family: Consolas, monospace; font-size: 32px; text-align: right;'>
            <div style='margin-bottom: 5px;'>
                <span style='letter-spacing: 0.3em;'>{num1_whole}</span>{f"<span>.</span><span style='letter-spacing: 0.3em;'>{num1_decimal}</span>" if num1_decimal else ""}
            </div>
            <div style='border-bottom: 3px solid black; padding-bottom: 5px; margin-bottom: 10px; position: relative;'>
                <span style='position: absolute; left: -40px;'>{data['operation_symbol']}</span>
                <span style='letter-spacing: 0.3em;'>{num2_whole}</span>{f"<span>.</span><span style='letter-spacing: 0.3em;'>{num2_decimal}</span>" if num2_decimal else ""}
            </div>
        </div>
    </div>
    """
    st.markdown(problem_html, unsafe_allow_html=True)
    
    # Create input boxes with precise alignment
    input_html = """
    <style>
    .digit-input {
        width: 45px !important;
        height: 45px !important;
        font-size: 24px !important;
        text-align: center !important;
        margin: 0 2px !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 5px !important;
        font-family: Consolas, monospace !important;
    }
    .decimal-point {
        font-size: 32px;
        font-weight: bold;
        margin: 0 5px;
        font-family: Consolas, monospace;
    }
    </style>
    """
    st.markdown(input_html, unsafe_allow_html=True)
    
    # Create container for inputs
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create a container with fixed width for alignment
        input_container = st.container()
        
        with input_container:
            # Calculate total width needed
            total_positions = max_whole_digits + (1 + max_decimal_digits if max_decimal_digits > 0 else 0)
            
            # Create columns with specific ratios for better alignment
            if max_decimal_digits > 0:
                # With decimal point
                col_widths = []
                for i in range(max_whole_digits):
                    col_widths.append(1)
                col_widths.append(0.5)  # Decimal point column
                for i in range(max_decimal_digits):
                    col_widths.append(1)
                
                input_cols = st.columns(col_widths)
            else:
                # Without decimal point
                input_cols = st.columns(max_whole_digits)
            
            # Place input boxes
            col_index = 0
            
            # Whole number part
            for i in range(max_whole_digits):
                with input_cols[col_index]:
                    key = f"digit_{i}"
                    value = st.text_input(
                        "",
                        max_chars=1,
                        key=key,
                        label_visibility="collapsed",
                        placeholder=""
                    )
                    st.session_state.user_inputs[key] = value
                col_index += 1
            
            # Decimal point and decimal part
            if max_decimal_digits > 0:
                # Decimal point
                with input_cols[col_index]:
                    st.markdown(
                        "<div style='text-align: center; margin-top: 8px;'><span class='decimal-point'>.</span></div>",
                        unsafe_allow_html=True
                    )
                col_index += 1
                
                # Decimal digits
                for i in range(max_decimal_digits):
                    with input_cols[col_index]:
                        key = f"decimal_{i}"
                        value = st.text_input(
                            "",
                            max_chars=1,
                            key=key,
                            label_visibility="collapsed",
                            placeholder=""
                        )
                        st.session_state.user_inputs[key] = value
                    col_index += 1
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            # Construct user answer from inputs
            user_answer = construct_user_answer()
            if user_answer is not None:
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
            else:
                st.warning("Please fill in all the answer boxes!")
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def construct_user_answer():
    """Construct the user's answer from individual digit inputs"""
    data = st.session_state.question_data
    answer_str = data['answer_str']
    
    # Determine expected structure
    if '.' in answer_str:
        whole_part, decimal_part = answer_str.split('.')
    else:
        whole_part = answer_str
        decimal_part = ""
    
    # Parse numbers to get max digits
    num1_str = str(data['num1'])
    num2_str = str(data['num2'])
    
    num1_parts = num1_str.split('.') if '.' in num1_str else [num1_str, '']
    num2_parts = num2_str.split('.') if '.' in num2_str else [num2_str, '']
    
    max_whole_digits = max(len(num1_parts[0]), len(num2_parts[0]), len(whole_part))
    max_decimal_digits = max(len(num1_parts[1]) if len(num1_parts) > 1 else 0,
                            len(num2_parts[1]) if len(num2_parts) > 1 else 0,
                            len(decimal_part))
    
    # Collect whole part digits
    whole_digits = []
    for i in range(max_whole_digits):
        key = f"digit_{i}"
        value = st.session_state.user_inputs.get(key, "")
        if value == "":
            value = "0"  # Treat empty as 0
        whole_digits.append(value)
    
    # Construct whole part (remove leading zeros)
    whole_answer = ''.join(whole_digits).lstrip('0') or '0'
    
    # Collect decimal part if present
    if max_decimal_digits > 0:
        decimal_digits = []
        for i in range(max_decimal_digits):
            key = f"decimal_{i}"
            value = st.session_state.user_inputs.get(key, "")
            if value == "":
                value = "0"  # Treat empty decimal places as 0
            decimal_digits.append(value)
        
        # Remove trailing zeros from decimal part
        decimal_answer = ''.join(decimal_digits).rstrip('0')
        if decimal_answer:
            user_answer_str = f"{whole_answer}.{decimal_answer}"
        else:
            user_answer_str = whole_answer
    else:
        user_answer_str = whole_answer
    
    try:
        return float(user_answer_str)
    except:
        return None

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = construct_user_answer()
    correct_answer = st.session_state.correct_answer
    
    if user_answer is None:
        st.error("❌ **Invalid answer format. Please enter digits only.**")
        return
    
    # Check if answer is correct (with small tolerance for floating point)
    if abs(user_answer - correct_answer) < 0.001:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.decimal_difficulty
        st.session_state.decimal_difficulty = min(
            st.session_state.decimal_difficulty + 1, 4
        )
        
        if st.session_state.decimal_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal operations!**")
        elif old_difficulty < st.session_state.decimal_difficulty:
            st.info(f"⬆️ **Level up! Now working with {['', 'one decimal place', 'two decimal places', 'mixed decimals', 'challenging problems'][st.session_state.decimal_difficulty]}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{st.session_state.question_data['answer_str']}**")
        st.markdown(f"Your answer: **{user_answer}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.decimal_difficulty
        st.session_state.decimal_difficulty = max(
            st.session_state.decimal_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimal_difficulty:
            st.warning(f"⬇️ **Level adjusted. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Step-by-step solution:")
        
        if data['operation'] == 'add':
            st.markdown(f"""
            **Addition:** {data['num1']} + {data['num2']}
            
            1. **Line up the decimal points**
            2. **Add from right to left**
            3. **Regroup if needed** (carry over)
            4. **Place the decimal point** in the same position
            
            **Answer:** {data['answer_str']}
            """)
        else:
            st.markdown(f"""
            **Subtraction:** {data['num1']} - {data['num2']}
            
            1. **Line up the decimal points**
            2. **Subtract from right to left**
            3. **Borrow if needed** (from the next place value)
            4. **Place the decimal point** in the same position
            
            **Answer:** {data['answer_str']}
            """)
        
        # Show visual alignment
        st.code(f"""
  {str(data['num1']):>8}
{data['operation_symbol']} {str(data['num2']):>8}
---------
  {data['answer_str']:>8}
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_inputs = {}