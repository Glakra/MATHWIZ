import streamlit as st
import random

def run():
    """
    Main function to run the Divide Numbers Ending in Zeroes practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_numbers_ending_in_zeroes.py
    """
    # Initialize session state for difficulty and game state
    if "divide_zeroes_difficulty" not in st.session_state:
        st.session_state.divide_zeroes_difficulty = 1  # Start with easier problems
    
    if "current_divide_question" not in st.session_state:
        st.session_state.current_divide_question = None
        st.session_state.divide_correct_answer = None
        st.session_state.divide_show_feedback = False
        st.session_state.divide_answer_submitted = False
        st.session_state.divide_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("➗ Divide Numbers Ending in Zeroes")
    st.markdown("*Practice dividing large numbers that end with zeros*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_zeroes_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
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
    if st.session_state.current_divide_question is None:
        generate_divide_question()
    
    # Display current question
    display_divide_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Divide Numbers Ending in Zeroes:
        
        **Strategy:** Remove zeros, divide, then add zeros back!
        
        ### Step-by-Step Method:
        1. **Count the zeros** at the end of the dividend
        2. **Remove the zeros** and divide the remaining numbers
        3. **Add the zeros back** to your answer
        
        ### Examples:
        - **4,500 ÷ 5** → Remove zeros: 45 ÷ 5 = 9 → Add zeros back: **900**
        - **24,000 ÷ 3** → Remove zeros: 24 ÷ 3 = 8 → Add zeros back: **8,000**
        - **360,000 ÷ 6** → Remove zeros: 36 ÷ 6 = 6 → Add zeros back: **60,000**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Thousands with single-digit divisors
        - **🟠 Level 3:** Hundreds of thousands
        - **🔴 Level 4-5:** Millions with two-digit divisors
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder problems
        - ❌ **Wrong answer:** Get easier problems for practice
        - 🎯 **Goal:** Master division with millions!
        """)

def generate_divide_question():
    """Generate a new division question based on difficulty level"""
    difficulty = st.session_state.divide_zeroes_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple thousands, single digit divisors
        problems = [
            {"dividend_base": 24, "zeros": 3, "divisor": 3},  # 24,000 ÷ 3 = 8,000
            {"dividend_base": 35, "zeros": 3, "divisor": 7},  # 35,000 ÷ 7 = 5,000
            {"dividend_base": 48, "zeros": 3, "divisor": 6},  # 48,000 ÷ 6 = 8,000
            {"dividend_base": 56, "zeros": 3, "divisor": 8},  # 56,000 ÷ 8 = 7,000
            {"dividend_base": 42, "zeros": 3, "divisor": 7},  # 42,000 ÷ 7 = 6,000
            {"dividend_base": 36, "zeros": 3, "divisor": 4},  # 36,000 ÷ 4 = 9,000
        ]
    elif difficulty == 2:
        # Level 2: Tens of thousands, single digit divisors
        problems = [
            {"dividend_base": 24, "zeros": 4, "divisor": 3},  # 240,000 ÷ 3 = 80,000
            {"dividend_base": 45, "zeros": 4, "divisor": 5},  # 450,000 ÷ 5 = 90,000
            {"dividend_base": 72, "zeros": 4, "divisor": 9},  # 720,000 ÷ 9 = 80,000
            {"dividend_base": 64, "zeros": 4, "divisor": 8},  # 640,000 ÷ 8 = 80,000
            {"dividend_base": 81, "zeros": 4, "divisor": 9},  # 810,000 ÷ 9 = 90,000
            {"dividend_base": 63, "zeros": 4, "divisor": 7},  # 630,000 ÷ 7 = 90,000
        ]
    elif difficulty == 3:
        # Level 3: Hundreds of thousands
        problems = [
            {"dividend_base": 48, "zeros": 5, "divisor": 6},  # 4,800,000 ÷ 6 = 800,000
            {"dividend_base": 35, "zeros": 5, "divisor": 7},  # 3,500,000 ÷ 7 = 500,000
            {"dividend_base": 72, "zeros": 5, "divisor": 9},  # 7,200,000 ÷ 9 = 800,000
            {"dividend_base": 56, "zeros": 5, "divisor": 8},  # 5,600,000 ÷ 8 = 700,000
            {"dividend_base": 42, "zeros": 5, "divisor": 6},  # 4,200,000 ÷ 6 = 700,000
            {"dividend_base": 45, "zeros": 5, "divisor": 5},  # 4,500,000 ÷ 5 = 900,000
        ]
    elif difficulty == 4:
        # Level 4: Millions with two-digit divisors
        problems = [
            {"dividend_base": 84, "zeros": 4, "divisor": 12},  # 840,000 ÷ 12 = 70,000
            {"dividend_base": 96, "zeros": 5, "divisor": 16},  # 9,600,000 ÷ 16 = 600,000
            {"dividend_base": 75, "zeros": 4, "divisor": 15},  # 750,000 ÷ 15 = 50,000
            {"dividend_base": 88, "zeros": 5, "divisor": 11},  # 8,800,000 ÷ 11 = 800,000
            {"dividend_base": 144, "zeros": 4, "divisor": 18}, # 1,440,000 ÷ 18 = 80,000
            {"dividend_base": 120, "zeros": 5, "divisor": 24}, # 12,000,000 ÷ 24 = 500,000
        ]
    else:  # difficulty == 5
        # Level 5: Large numbers with challenging divisors
        problems = [
            {"dividend_base": 32, "zeros": 7, "divisor": 4},   # 320,000,000 ÷ 4 = 80,000,000
            {"dividend_base": 150, "zeros": 4, "divisor": 25}, # 1,500,000 ÷ 25 = 60,000
            {"dividend_base": 240, "zeros": 5, "divisor": 48}, # 24,000,000 ÷ 48 = 500,000
            {"dividend_base": 156, "zeros": 5, "divisor": 26}, # 15,600,000 ÷ 26 = 600,000
            {"dividend_base": 210, "zeros": 6, "divisor": 42}, # 210,000,000 ÷ 42 = 5,000,000
            {"dividend_base": 180, "zeros": 5, "divisor": 36}, # 18,000,000 ÷ 36 = 500,000
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    # Calculate the numbers
    dividend = problem["dividend_base"] * (10 ** problem["zeros"])
    divisor = problem["divisor"]
    correct_answer = dividend // divisor
    
    st.session_state.divide_question_data = {
        "dividend": dividend,
        "divisor": divisor,
        "dividend_base": problem["dividend_base"],
        "zeros": problem["zeros"]
    }
    st.session_state.divide_correct_answer = correct_answer
    st.session_state.current_divide_question = f"What is {dividend:,} ÷ {divisor:,}?"

def display_divide_question():
    """Display the current division question interface"""
    data = st.session_state.divide_question_data
    dividend = data["dividend"]
    divisor = data["divisor"]
    
    # Display question with nice formatting
    st.markdown("### ➗ Division Problem:")
    
    # Display the division problem in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 40px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        text-align: center;
        margin: 30px 0;
    ">
        <div style="font-size: 24px; color: #1f77b4; margin-bottom: 20px;">
            <strong>Divide:</strong>
        </div>
        <div style="font-size: 36px; font-weight: bold; color: #1f77b4; font-family: 'Courier New', monospace;">
            {dividend:,} ÷ {divisor:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("divide_answer_form", clear_on_submit=False):
        st.markdown("**Enter your answer:**")
        
        user_answer = st.text_input(
            "Answer:", 
            key="divide_user_input",
            placeholder="Enter numbers only (e.g., 8000)",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Clean the input
            cleaned_input = user_answer.replace(",", "").replace(" ", "").strip()
            
            try:
                user_number = int(cleaned_input)
                st.session_state.divide_user_answer = user_number
                st.session_state.divide_show_feedback = True
                st.session_state.divide_answer_submitted = True
            except ValueError:
                st.error("Please enter a valid number (digits only)")
    
    # Show feedback and next button
    handle_divide_feedback_and_next()

def handle_divide_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.divide_show_feedback:
        show_divide_feedback()
    
    # Next question button
    if st.session_state.divide_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_divide_question_state()
                st.rerun()

def show_divide_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.divide_user_answer
    correct_answer = st.session_state.divide_correct_answer
    data = st.session_state.divide_question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.divide_zeroes_difficulty
        st.session_state.divide_zeroes_difficulty = min(
            st.session_state.divide_zeroes_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.divide_zeroes_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered division with zeros!**")
        elif old_difficulty < st.session_state.divide_zeroes_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.divide_zeroes_difficulty}**")
        
        # Show the strategy
        show_divide_strategy(correct=True)
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer:,}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.divide_zeroes_difficulty
        st.session_state.divide_zeroes_difficulty = max(
            st.session_state.divide_zeroes_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.divide_zeroes_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.divide_zeroes_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_divide_strategy(correct=False)

def show_divide_strategy(correct=True):
    """Show explanation for the division strategy"""
    data = st.session_state.divide_question_data
    correct_answer = st.session_state.divide_correct_answer
    dividend = data["dividend"]
    divisor = data["divisor"]
    dividend_base = data["dividend_base"]
    zeros = data["zeros"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Division Strategy:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Step-by-step solution:
        
        **Problem:** {dividend:,} ÷ {divisor:,}
        
        **Step 1:** Count the zeros at the end of {dividend:,}
        - There are **{zeros} zeros** at the end
        
        **Step 2:** Remove the zeros and divide
        - {dividend:,} becomes **{dividend_base}**
        - Now divide: {dividend_base} ÷ {divisor} = **{dividend_base // divisor}**
        
        **Step 3:** Add the zeros back
        - Take the result **{dividend_base // divisor}** and add **{zeros} zeros**
        - Final answer: **{correct_answer:,}**
        
        ### Why this works:
        When we divide a number ending in zeros by a number without zeros, 
        we can "factor out" the zeros, do the simpler division, then put the zeros back!
        """)

def reset_divide_question_state():
    """Reset the question state for next question"""
    st.session_state.current_divide_question = None
    st.session_state.divide_correct_answer = None
    st.session_state.divide_show_feedback = False
    st.session_state.divide_answer_submitted = False
    st.session_state.divide_question_data = {}
    if "divide_user_answer" in st.session_state:
        del st.session_state.divide_user_answer