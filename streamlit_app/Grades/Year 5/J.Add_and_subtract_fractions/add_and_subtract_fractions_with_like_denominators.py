import streamlit as st
import random

def run():
    """
    Main function to run the Add and Subtract Fractions with Like Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/add_and_subtract_fractions_with_like_denominators.py
    """
    # Initialize session state for difficulty and game state
    if "add_subtract_difficulty" not in st.session_state:
        st.session_state.add_subtract_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕➖ Add and Subtract Fractions with Like Denominators")
    st.markdown("*Add or subtract fractions that have the same denominator*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.add_subtract_difficulty
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
        ### How to Add and Subtract Fractions with Like Denominators:
        
        **Rule:** When fractions have the same denominator:
        - **Addition:** Add the numerators, keep the denominator
        - **Subtraction:** Subtract the numerators, keep the denominator
        
        ### Examples:
        **Addition:** 2/5 + 3/5 = 5/5 = 1
        **Subtraction:** 7/8 - 3/8 = 4/8 = 1/2
        
        ### Steps:
        1. Check that denominators are the same ✓
        2. Add or subtract the top numbers only
        3. Keep the bottom number the same
        4. Simplify if possible
        
        ### Remember:
        - The denominator NEVER changes
        - Only work with the numerators
        - Watch for improper fractions (like 7/5)
        - Simplify your answer when possible
        """)

def generate_new_question():
    """Generate a new fraction addition or subtraction question"""
    difficulty = st.session_state.add_subtract_difficulty
    
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
    
    # Randomly choose operation
    operation = random.choice(["add", "subtract"])
    
    if operation == "add":
        # Generate addition problem
        if difficulty <= 2:
            # Keep sum less than or equal to denominator for easier levels
            numerator1 = random.randint(1, min(denominator - 1, denominator - 1))
            max_num2 = min(denominator - numerator1, denominator - 1)
            numerator2 = random.randint(1, max_num2)
        else:
            # Allow improper fractions for harder levels
            numerator1 = random.randint(1, denominator - 1)
            numerator2 = random.randint(1, denominator - 1)
        
        result = numerator1 + numerator2
    else:
        # Generate subtraction problem (ensure positive result)
        numerator1 = random.randint(2, denominator - 1)
        numerator2 = random.randint(1, numerator1 - 1)
        result = numerator1 - numerator2
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "result": result,
        "operation": operation
    }
    
    st.session_state.correct_answer = result
    st.session_state.current_question = "Add." if operation == "add" else "Subtract."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display "Add." or "Subtract." instruction
    st.markdown(f"### {st.session_state.current_question}")
    
    # Create the fraction display
    st.markdown("")
    
    # Use columns for the equation
    col1, col2, col3, col4, col5 = st.columns([1.5, 0.5, 1.5, 0.5, 2])
    
    with col1:
        # First fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 48px; line-height: 1;">
            <div style="border-bottom: 3px solid black; padding: 5px;">{data['numerator1']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col2:
        operation_symbol = "+" if data['operation'] == "add" else "−"
        st.markdown(f"""
        <div style="text-align: center; font-size: 48px; padding-top: 30px;">
            {operation_symbol}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 48px; line-height: 1;">
            <div style="border-bottom: 3px solid black; padding: 5px;">{data['numerator2']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 30px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Answer input area
        st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
        with st.form("answer_form", clear_on_submit=False):
            user_input = st.text_input(
                "",
                key="fraction_answer",
                placeholder=f"?/{data['denominator']}",
                label_visibility="collapsed"
            )
            
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit and user_input.strip():
                # Parse the answer
                if '/' in user_input:
                    try:
                        parts = user_input.split('/')
                        user_num = int(parts[0])
                        user_denom = int(parts[1])
                        
                        # Check if denominator is correct
                        if user_denom != data['denominator']:
                            st.error(f"The denominator should be {data['denominator']}")
                        else:
                            st.session_state.user_answer = user_num
                            st.session_state.answer_submitted = True
                            st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid fraction (e.g., 5/6)")
                else:
                    try:
                        # If they just entered the numerator
                        user_num = int(user_input)
                        st.session_state.user_answer = user_num
                        st.session_state.answer_submitted = True
                        st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid number")
            elif submit:
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
        st.success("🎉 **Correct! Well done!**")
        
        # Show the complete equation
        fraction1 = f"{data['numerator1']}/{data['denominator']}"
        fraction2 = f"{data['numerator2']}/{data['denominator']}"
        result = f"{correct_answer}/{data['denominator']}"
        operation_symbol = "+" if data['operation'] == "add" else "−"
        
        st.success(f"✓ {fraction1} {operation_symbol} {fraction2} = {result}")
        
        # Check for special cases
        if correct_answer == 0:
            st.info("💡 **Note:** When you subtract all the parts, you get 0!")
        elif correct_answer == data['denominator']:
            st.info("💡 **Note:** Your answer equals 1 whole!")
        elif correct_answer > data['denominator']:
            # Calculate mixed number
            whole_part = correct_answer // data['denominator']
            remainder = correct_answer % data['denominator']
            if remainder == 0:
                st.info(f"💡 **Note:** {result} = {whole_part}")
            else:
                st.info(f"💡 **Note:** {result} is an improper fraction. It equals {whole_part} {remainder}/{data['denominator']}")
        
        # Check if the result can be simplified
        from math import gcd
        if correct_answer > 0 and correct_answer != data['denominator']:
            common_divisor = gcd(correct_answer, data['denominator'])
            if common_divisor > 1:
                simplified_num = correct_answer // common_divisor
                simplified_denom = data['denominator'] // common_divisor
                if simplified_denom == 1:
                    st.info(f"💡 **Simplification:** {result} = {simplified_num}")
                else:
                    st.info(f"💡 **Simplification:** {result} = {simplified_num}/{simplified_denom}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.add_subtract_difficulty
        st.session_state.add_subtract_difficulty = min(
            st.session_state.add_subtract_difficulty + 1, 5
        )
        
        if st.session_state.add_subtract_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've reached the highest level!**")
        elif old_difficulty < st.session_state.add_subtract_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.add_subtract_difficulty}**")
    
    else:
        st.error("❌ **Not quite right. Try again!**")
        
        # Show what they entered
        user_fraction = f"{user_answer}/{data['denominator']}"
        st.error(f"You answered: {user_fraction}")
        
        # Show the correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.add_subtract_difficulty
        st.session_state.add_subtract_difficulty = max(
            st.session_state.add_subtract_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.add_subtract_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.add_subtract_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for adding or subtracting fractions"""
    data = st.session_state.question_data
    operation_name = "Addition" if data['operation'] == "add" else "Subtraction"
    operation_symbol = "+" if data['operation'] == "add" else "−"
    
    with st.expander("📖 **How to Solve This Problem**", expanded=True):
        st.markdown(f"""
        ### {operation_name} of Fractions with Like Denominators
        
        **Your Problem:**
        **{data['numerator1']}/{data['denominator']} {operation_symbol} {data['numerator2']}/{data['denominator']} = ?**
        
        ### Solution Steps:
        
        **Step 1: Check the denominators**
        - First fraction: {data['denominator']} ✓
        - Second fraction: {data['denominator']} ✓
        - They're the same! This makes it easy.
        
        **Step 2: {operation_name} the numerators**
        - {data['numerator1']} {operation_symbol} {data['numerator2']} = {data['result']}
        
        **Step 3: Keep the same denominator**
        - The denominator stays {data['denominator']}
        
        **Answer: {data['result']}/{data['denominator']}**
        
        ### Visual Example:
        """)
        
        if data['operation'] == "add":
            st.markdown(f"""
        Think of it like this:
        - You have {data['numerator1']} pieces of a pizza cut into {data['denominator']} slices
        - You get {data['numerator2']} more pieces
        - Total: {data['result']} pieces out of {data['denominator']}
        """)
        else:
            st.markdown(f"""
        Think of it like this:
        - You have {data['numerator1']} pieces of a pizza cut into {data['denominator']} slices
        - You give away {data['numerator2']} pieces
        - Remaining: {data['result']} pieces out of {data['denominator']}
        """)
        
        st.markdown(f"""
        ### Remember the Rule:
        **Same denominator → {operation_name} only the numerators!**
        
        ### Quick Check:
        - Did you keep the denominator the same? ✓
        - Did you only {operation_name.lower()} the top numbers? ✓
        - Can your answer be simplified? Check!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer