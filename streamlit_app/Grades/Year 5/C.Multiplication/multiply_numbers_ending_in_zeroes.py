import streamlit as st
import random

def run():
    """
    Main function to run the Multiply Numbers Ending in Zeroes practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_numbers_ending_in_zeroes.py
    """
    # Initialize session state for difficulty and game state
    if "zeroes_mult_difficulty" not in st.session_state:
        st.session_state.zeroes_mult_difficulty = 1  # Start with basic problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔢 Multiply Numbers Ending in Zeroes")
    st.markdown("*Learn the shortcut for multiplying with zeros*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.zeroes_mult_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Tens & Hundreds", "Thousands", "Large Numbers"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level - 1]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
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
        ### The Zero Shortcut Method:
        
        **🎯 Step 1: Ignore the zeros temporarily**
        **🎯 Step 2: Multiply the non-zero digits** 
        **🎯 Step 3: Count and add back the zeros**
        
        ### Examples:
        
        **Example 1: 8000 × 4**
        1. **Ignore zeros:** 8 × 4 = 32
        2. **Count zeros:** 8000 has 3 zeros
        3. **Add zeros back:** 32,000 ✅
        
        **Example 2: 3 × 500** 
        1. **Ignore zeros:** 3 × 5 = 15
        2. **Count zeros:** 500 has 2 zeros
        3. **Add zeros back:** 1,500 ✅
        
        **Example 3: 60 × 700**
        1. **Ignore zeros:** 6 × 7 = 42  
        2. **Count zeros:** 60 has 1 zero, 700 has 2 zeros = 3 total zeros
        3. **Add zeros back:** 42,000 ✅
        
        ### Key Rules:
        - **Count ALL zeros** from both numbers
        - **Multiply the non-zero parts** first
        - **Add the total number of zeros** to your answer
        - **Check your answer** - does it make sense?
        
        ### Common Patterns:
        - **× 10** → Add 1 zero
        - **× 100** → Add 2 zeros  
        - **× 1000** → Add 3 zeros
        - **60 × 700** → (6 × 7) + (1 + 2) zeros = 42,000
        
        ### Tips for Success:
        - **Write down the non-zero multiplication** first
        - **Count zeros carefully** - don't miss any!
        - **Practice with smaller numbers** first
        - **Use estimation** to check if your answer is reasonable
        
        ### Types of Problems:
        - **🔢 Large × Single:** 8000 × 4
        - **🔢 Single × Large:** 3 × 500  
        - **🔢 Both with Zeros:** 60 × 700
        - **🔢 Multiple Zeros:** 4000 × 60
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Tens and hundreds (10, 20, 100, 200)
        - **🟠 Level 2:** Thousands (1000, 2000, 3000)
        - **🔴 Level 3:** Large numbers with many zeros
        
        ### Mental Math Trick:
        **Instead of:** 800 × 6 = 800 + 800 + 800 + 800 + 800 + 800  
        **Think:** 8 × 6 = 48, then add 2 zeros = 4,800 ⚡
        """)

def generate_new_question():
    """Generate a new multiplication problem with numbers ending in zeros"""
    difficulty = st.session_state.zeroes_mult_difficulty
    
    # Different types of zero problems
    problem_types = [
        "large_times_single",    # 8000 × 4
        "single_times_large",    # 3 × 500  
        "both_with_zeros",       # 60 × 700
        "multiple_zeros"         # 4000 × 60
    ]
    
    problem_type = random.choice(problem_types)
    
    if difficulty == 1:
        # Level 1: Tens and hundreds
        if problem_type == "large_times_single":
            # Numbers like 80, 300, 600 × single digit
            base = random.randint(2, 9)
            zeros = random.choice([1, 2])  # 10s or 100s
            factor1 = base * (10 ** zeros)
            factor2 = random.randint(2, 9)
            
        elif problem_type == "single_times_large":
            # Single digit × numbers like 80, 300, 600
            factor1 = random.randint(2, 9)
            base = random.randint(2, 9)
            zeros = random.choice([1, 2])  # 10s or 100s
            factor2 = base * (10 ** zeros)
            
        elif problem_type == "both_with_zeros":
            # Both numbers have zeros, but smaller
            base1 = random.randint(2, 9)
            base2 = random.randint(2, 9)
            factor1 = base1 * 10  # Like 20, 30, 40
            factor2 = base2 * 10  # Like 20, 30, 40
            
        else:  # multiple_zeros
            # One number with multiple zeros
            base = random.randint(2, 9)
            factor1 = base * 100  # Like 200, 300, 400
            factor2 = random.randint(2, 9)
    
    elif difficulty == 2:
        # Level 2: Thousands
        if problem_type == "large_times_single":
            # Numbers like 2000, 5000 × single digit
            base = random.randint(2, 9)
            zeros = random.choice([3, 4])  # 1000s or 10000s
            factor1 = base * (10 ** zeros)
            factor2 = random.randint(2, 9)
            
        elif problem_type == "single_times_large":
            # Single digit × numbers like 2000, 5000
            factor1 = random.randint(2, 9)
            base = random.randint(2, 9)
            zeros = random.choice([3, 4])  # 1000s or 10000s
            factor2 = base * (10 ** zeros)
            
        elif problem_type == "both_with_zeros":
            # Both numbers have zeros
            base1 = random.randint(2, 9)
            base2 = random.randint(2, 9)
            factor1 = base1 * random.choice([10, 100])  # 10s or 100s
            factor2 = base2 * random.choice([100, 1000])  # 100s or 1000s
            
        else:  # multiple_zeros
            # Larger numbers with more zeros
            base = random.randint(2, 9)
            factor1 = base * random.choice([1000, 10000])
            factor2 = random.randint(2, 9) * 10
    
    else:
        # Level 3: Large numbers with many zeros
        if problem_type == "large_times_single":
            # Very large numbers × single digit
            base = random.randint(2, 9)
            zeros = random.choice([4, 5, 6])  # 10000s, 100000s, 1000000s
            factor1 = base * (10 ** zeros)
            factor2 = random.randint(2, 9)
            
        elif problem_type == "single_times_large":
            # Single digit × very large numbers
            factor1 = random.randint(2, 9)
            base = random.randint(2, 9)
            zeros = random.choice([4, 5, 6])  # 10000s, 100000s, 1000000s
            factor2 = base * (10 ** zeros)
            
        elif problem_type == "both_with_zeros":
            # Both numbers have many zeros
            base1 = random.randint(2, 9)
            base2 = random.randint(2, 9)
            factor1 = base1 * random.choice([100, 1000])
            factor2 = base2 * random.choice([1000, 10000])
            
        else:  # multiple_zeros
            # Complex problems with many zeros
            base = random.randint(2, 9)
            factor1 = base * random.choice([10000, 100000])
            factor2 = random.randint(2, 9) * random.choice([100, 1000])
    
    # Calculate the correct answer
    correct_answer = factor1 * factor2
    
    # Store question data
    st.session_state.question_data = {
        'factor1': factor1,
        'factor2': factor2,
        'correct_answer': correct_answer,
        'problem_type': problem_type,
        'difficulty': difficulty
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Multiply:"

def display_question():
    """Display the current multiplication question"""
    data = st.session_state.question_data
    
    # Create form for the answer
    with st.form("zeroes_multiplication_form"):
        # Display the question in a clean format
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Display "Multiply:" header
            st.markdown("### ✖️ Multiply:")
            
            # Create the equation layout with inline input
            eq_cols = st.columns([3, 1, 3, 1, 4])
            
            with eq_cols[0]:
                st.markdown(f"<div style='font-size: 24px; text-align: right; margin-top: 12px; font-family: monospace;'>{data['factor1']:,}</div>", unsafe_allow_html=True)
            
            with eq_cols[1]:
                st.markdown("<div style='font-size: 24px; text-align: center; margin-top: 12px;'>×</div>", unsafe_allow_html=True)
            
            with eq_cols[2]:
                st.markdown(f"<div style='font-size: 24px; text-align: right; margin-top: 12px; font-family: monospace;'>{data['factor2']:,}</div>", unsafe_allow_html=True)
            
            with eq_cols[3]:
                st.markdown("<div style='font-size: 24px; text-align: center; margin-top: 12px;'>=</div>", unsafe_allow_html=True)
            
            with eq_cols[4]:
                user_answer = st.number_input(
                    "Answer",
                    min_value=0,
                    step=1,
                    key="answer_input",
                    label_visibility="collapsed",
                    help=f"What is {data['factor1']:,} × {data['factor2']:,}?",
                    placeholder="Enter answer"
                )
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! {correct_answer:,} is correct!**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.zeroes_mult_difficulty
        st.session_state.zeroes_mult_difficulty = min(
            st.session_state.zeroes_mult_difficulty + 1, 3
        )
        
        if st.session_state.zeroes_mult_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered multiplying with zeros!**")
        elif old_difficulty < st.session_state.zeroes_mult_difficulty:
            st.info(f"⬆️ **Great work! Moving up to Level {st.session_state.zeroes_mult_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.zeroes_mult_difficulty
        st.session_state.zeroes_mult_difficulty = max(
            st.session_state.zeroes_mult_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.zeroes_mult_difficulty:
            st.warning(f"⬇️ **Let's practice more at Level {st.session_state.zeroes_mult_difficulty}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation using the zero shortcut method"""
    data = st.session_state.question_data
    factor1 = data['factor1']
    factor2 = data['factor2']
    correct_answer = data['correct_answer']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Zero Shortcut Method for {factor1:,} × {factor2:,}:
        """)
        
        # Count zeros in each number
        zeros_factor1 = count_trailing_zeros(factor1)
        zeros_factor2 = count_trailing_zeros(factor2)
        total_zeros = zeros_factor1 + zeros_factor2
        
        # Get non-zero parts
        non_zero1 = factor1 // (10 ** zeros_factor1) if zeros_factor1 > 0 else factor1
        non_zero2 = factor2 // (10 ** zeros_factor2) if zeros_factor2 > 0 else factor2
        
        basic_product = non_zero1 * non_zero2
        
        st.markdown(f"""
        **Step 1: Identify the non-zero parts** 🔍
        - {factor1:,} = {non_zero1} with {zeros_factor1} zero{'s' if zeros_factor1 != 1 else ''}
        - {factor2:,} = {non_zero2} with {zeros_factor2} zero{'s' if zeros_factor2 != 1 else ''}
        
        **Step 2: Multiply the non-zero parts** ✖️
        - {non_zero1} × {non_zero2} = {basic_product}
        
        **Step 3: Count total zeros** 📊
        - Total zeros = {zeros_factor1} + {zeros_factor2} = {total_zeros}
        
        **Step 4: Add the zeros back** ➕
        - {basic_product} + {total_zeros} zero{'s' if total_zeros != 1 else ''} = **{correct_answer:,}**
        
        ### Visual breakdown:
        ```
        {factor1:,} × {factor2:,}
        = {non_zero1} × {non_zero2} × 10^{total_zeros}
        = {basic_product} × {"1" + "0" * total_zeros}
        = {correct_answer:,}
        ```
        
        💡 **Quick check:** {basic_product} with {total_zeros} zero{'s' if total_zeros != 1 else ''} added = {correct_answer:,} ✓
        """)

def count_trailing_zeros(n):
    """Count the number of trailing zeros in a number"""
    if n == 0:
        return 1
    count = 0
    while n % 10 == 0:
        count += 1
        n //= 10
    return count

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""