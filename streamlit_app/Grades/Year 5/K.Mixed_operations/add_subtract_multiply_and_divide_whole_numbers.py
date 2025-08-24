import streamlit as st
import random

def run():
    """
    Main function to run the Add, subtract, multiply and divide whole numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/add_subtract_multiply_and_divide_whole_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "mixed_ops_difficulty" not in st.session_state:
        st.session_state.mixed_ops_difficulty = 1  # Start with easier problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.remainder = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("➕➖✖️➗ Add, Subtract, Multiply and Divide Whole Numbers")
    st.markdown("*Practice all four operations with whole numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mixed_ops_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Expert", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        # Progress bar (1 to 5)
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
        - **Solve each problem** using the correct operation
        - **Enter your answer** in the box provided
        - **For division:** Enter the quotient and remainder separately
        - **Check your work** before submitting
        
        ### Tips for Each Operation:
        
        **➕ Addition:**
        - Line up numbers by place value
        - Start from the ones place
        - Remember to carry when needed
        
        **➖ Subtraction:**
        - Line up numbers by place value
        - Start from the ones place
        - Borrow when needed
        
        **✖️ Multiplication:**
        - Break down into smaller steps
        - Remember to add zeros for place value
        - Check by estimating
        
        **➗ Division:**
        - Think: How many groups?
        - Use multiplication to check
        - Don't forget the remainder
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Smaller numbers, basic operations
        - **🟡 Level 3:** Medium numbers, all operations
        - **🔴 Level 4-5:** Large numbers, complex calculations
        
        ### Strategy Tips:
        - **Estimate first** to check if your answer makes sense
        - **Show your work** on paper for complex problems
        - **Double-check** by using the inverse operation
        """)

def generate_new_problem():
    """Generate a new mixed operation problem based on difficulty"""
    difficulty = st.session_state.mixed_ops_difficulty
    
    # Choose operation based on difficulty
    if difficulty == 1:
        operations = ["add", "subtract"]
    else:
        operations = ["add", "subtract", "multiply", "divide"]
    
    operation = random.choice(operations)
    
    # Generate numbers based on operation and difficulty
    if operation == "add":
        if difficulty == 1:
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
        elif difficulty == 2:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(100, 999)
        elif difficulty == 3:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(1000, 9999)
        elif difficulty == 4:
            num1 = random.randint(10000, 99999)
            num2 = random.randint(1000, 9999)
        else:  # difficulty == 5
            num1 = random.randint(10000, 99999)
            num2 = random.randint(10000, 99999)
        
        answer = num1 + num2
        problem_text = f"{num1:,} + {num2:,}"
        
    elif operation == "subtract":
        # Ensure num1 > num2 for positive result
        if difficulty == 1:
            num1 = random.randint(500, 999)
            num2 = random.randint(100, num1-1)
        elif difficulty == 2:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(100, min(999, num1-1))
        elif difficulty == 3:
            num1 = random.randint(5000, 9999)
            num2 = random.randint(1000, num1-1)
        elif difficulty == 4:
            num1 = random.randint(10000, 99999)
            num2 = random.randint(1000, min(9999, num1-1))
        else:  # difficulty == 5
            num1 = random.randint(50000, 99999)
            num2 = random.randint(10000, num1-1)
        
        answer = num1 - num2
        problem_text = f"{num1:,} - {num2:,}"
        
    elif operation == "multiply":
        if difficulty == 2:
            num1 = random.randint(10, 99)
            num2 = random.randint(2, 9)
        elif difficulty == 3:
            num1 = random.randint(100, 999)
            num2 = random.randint(2, 9)
        elif difficulty == 4:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(2, 9)
        else:  # difficulty == 5
            num1 = random.randint(10000, 99999)
            num2 = random.randint(2, 9)
        
        answer = num1 * num2
        problem_text = f"{num1:,} × {num2}"
        
    else:  # division
        # Create division problems that work nicely
        if difficulty == 2:
            divisor = random.randint(2, 9)
            quotient = random.randint(10, 99)
            remainder = random.randint(0, divisor-1)
        elif difficulty == 3:
            divisor = random.randint(2, 9)
            quotient = random.randint(100, 999)
            remainder = random.randint(0, divisor-1)
        elif difficulty == 4:
            divisor = random.randint(10, 99)
            quotient = random.randint(10, 99)
            remainder = random.randint(0, divisor-1)
        else:  # difficulty == 5
            divisor = random.randint(10, 99)
            quotient = random.randint(100, 999)
            remainder = random.randint(0, divisor-1)
        
        dividend = divisor * quotient + remainder
        answer = quotient
        problem_text = f"{dividend:,} ÷ {divisor}"
        
        st.session_state.remainder = remainder
    
    st.session_state.problem_data = {
        "operation": operation,
        "problem_text": problem_text,
        "num1": num1 if operation != "divide" else dividend,
        "num2": num2 if operation != "divide" else divisor
    }
    st.session_state.correct_answer = answer
    st.session_state.current_problem = operation

def display_problem():
    """Display the current problem interface"""
    data = st.session_state.problem_data
    operation = data["operation"]
    
    # Display operation type
    operation_names = {
        "add": "➕ Addition",
        "subtract": "➖ Subtraction", 
        "multiply": "✖️ Multiplication",
        "divide": "➗ Division"
    }
    
    st.markdown(f"### {operation_names[operation]}")
    
    # Display the problem in a nice format based on operation
    if operation == "add":
        display_vertical_problem(data["num1"], data["num2"], "+")
    elif operation == "subtract":
        display_vertical_problem(data["num1"], data["num2"], "-")
    elif operation == "multiply":
        display_vertical_problem(data["num1"], data["num2"], "×")
    else:  # division
        display_division_problem(data["num1"], data["num2"])
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        if operation == "divide":
            col1, col2 = st.columns(2)
            with col1:
                quotient = st.number_input(
                    "Quotient:",
                    min_value=0,
                    step=1,
                    key="quotient_input"
                )
            with col2:
                remainder = st.number_input(
                    "Remainder:",
                    min_value=0,
                    step=1,
                    key="remainder_input"
                )
            user_answer = (quotient, remainder)
        else:
            user_answer = st.number_input(
                "Your answer:",
                min_value=0,
                step=1,
                key="answer_input"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            if operation == "divide":
                st.session_state.user_answer = user_answer[0]
                st.session_state.user_remainder = user_answer[1]
            else:
                st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_vertical_problem(num1, num2, operator):
    """Display a vertical math problem"""
    # Format numbers with proper spacing
    max_digits = max(len(str(num1)), len(str(num2)) + 1)  # +1 for operator
    
    st.markdown(f"""
    <div style="
        font-family: monospace;
        font-size: 24px;
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        display: inline-block;
        margin: 20px 0;
    ">
        <div style="text-align: right;">
            <div>{num1:>{max_digits},}</div>
            <div>{operator} {num2:>{max_digits-2},}</div>
            <div style="border-top: 2px solid #333; margin-top: 5px; padding-top: 5px;">
                <input style="
                    width: {max_digits * 15}px;
                    text-align: right;
                    font-family: monospace;
                    font-size: 24px;
                    border: none;
                    background: transparent;
                    color: #666;
                " disabled>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_division_problem(dividend, divisor):
    """Display a division problem with long division format"""
    st.markdown(f"""
    <div style="
        font-family: monospace;
        font-size: 24px;
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        display: inline-block;
        margin: 20px 0;
    ">
        <div>
            <span style="margin-right: 10px;">{divisor}</span>
            <span style="border-left: 2px solid #333; border-top: 2px solid #333; padding-left: 10px;">
                {dividend:,}
            </span>
        </div>
        <div style="margin-top: 20px;">
            <span style="color: #666;">Quotient = ?</span>
            <span style="margin-left: 30px; color: #666;">Remainder = ?</span>
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
    operation = st.session_state.problem_data["operation"]
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Check answer based on operation
    if operation == "divide":
        user_remainder = st.session_state.user_remainder
        correct_remainder = st.session_state.remainder
        is_correct = (user_answer == correct_answer and user_remainder == correct_remainder)
    else:
        is_correct = (user_answer == correct_answer)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.mixed_ops_difficulty
        st.session_state.mixed_ops_difficulty = min(
            st.session_state.mixed_ops_difficulty + 1, 5
        )
        
        if st.session_state.mixed_ops_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've reached Master level!**")
        elif old_difficulty < st.session_state.mixed_ops_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.mixed_ops_difficulty}**")
    
    else:
        if operation == "divide":
            st.error(f"❌ **Not quite. The correct answer was {correct_answer} R {st.session_state.remainder}**")
        else:
            st.error(f"❌ **Not quite. The correct answer was {correct_answer:,}**")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.mixed_ops_difficulty
        st.session_state.mixed_ops_difficulty = max(
            st.session_state.mixed_ops_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.mixed_ops_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.mixed_ops_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.problem_data
    operation = data["operation"]
    
    with st.expander("📖 **See solution**", expanded=True):
        if operation == "add":
            st.markdown(f"""
            ### Addition Solution:
            
            ```
               {data['num1']:,}
            +  {data['num2']:,}
            --------
               {st.session_state.correct_answer:,}
            ```
            
            **Steps:**
            1. Line up the numbers by place value
            2. Add from right to left
            3. Carry over when sum ≥ 10
            """)
            
        elif operation == "subtract":
            st.markdown(f"""
            ### Subtraction Solution:
            
            ```
               {data['num1']:,}
            -  {data['num2']:,}
            --------
               {st.session_state.correct_answer:,}
            ```
            
            **Steps:**
            1. Line up the numbers by place value
            2. Subtract from right to left
            3. Borrow when needed
            """)
            
        elif operation == "multiply":
            st.markdown(f"""
            ### Multiplication Solution:
            
            ```
               {data['num1']:,}
            ×      {data['num2']}
            --------
               {st.session_state.correct_answer:,}
            ```
            
            **Quick method:**
            {data['num1']:,} × {data['num2']} = {st.session_state.correct_answer:,}
            """)
            
        else:  # division
            quotient = st.session_state.correct_answer
            remainder = st.session_state.remainder
            divisor = data['num2']
            dividend = data['num1']
            
            st.markdown(f"""
            ### Division Solution:
            
            {dividend:,} ÷ {divisor} = **{quotient} R {remainder}**
            
            **Check:** {divisor} × {quotient} + {remainder} = {divisor * quotient + remainder:,} ✓
            
            **Steps:**
            1. How many times does {divisor} go into {dividend:,}?
            2. {divisor} × {quotient} = {divisor * quotient:,}
            3. Remainder = {dividend:,} - {divisor * quotient:,} = {remainder}
            """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.remainder = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
    if "user_remainder" in st.session_state:
        del st.session_state.user_remainder