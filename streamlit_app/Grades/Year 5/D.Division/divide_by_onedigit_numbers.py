import streamlit as st
import random

def run():
    """
    Main function to run the Divide by One-Digit Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_by_one_digit_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "divide_difficulty" not in st.session_state:
        st.session_state.divide_difficulty = 2  # Start with 2-digit dividends
    
    if "current_division" not in st.session_state:
        st.session_state.current_division = None
        st.session_state.correct_quotient = None
        st.session_state.correct_remainder = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.division_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("➗ Divide by One-Digit Numbers")
    st.markdown("*Practice dividing numbers by single digits*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if difficulty_level == 2:
            st.markdown("**Current Difficulty:** 2-digit ÷ 1-digit")
        elif difficulty_level == 3:
            st.markdown("**Current Difficulty:** 3-digit ÷ 1-digit")
        elif difficulty_level == 4:
            st.markdown("**Current Difficulty:** 4-digit ÷ 1-digit")
        else:
            st.markdown("**Current Difficulty:** Large numbers ÷ 1-digit")
        
        # Progress bar (2 to 5 digits)
        progress = (difficulty_level - 2) / 3  # Convert 2-5 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
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
    if st.session_state.current_division is None:
        generate_new_division()
    
    # Display current question
    display_division_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Division:
        - **Look at the division problem** in the format: divisor) dividend
        - **Divide step by step** using long division
        - **Enter your answer** in the quotient box
        - **If there's a remainder**, enter it in the remainder box
        
        ### Long Division Steps:
        1. **Divide:** How many times does the divisor go into the first digit(s)?
        2. **Multiply:** Multiply the quotient digit by the divisor
        3. **Subtract:** Subtract from the dividend
        4. **Bring down:** Bring down the next digit
        5. **Repeat:** Continue until done
        
        ### Examples:
        - **84 ÷ 4 = 21** (no remainder)
        - **85 ÷ 4 = 21 R 1** (quotient: 21, remainder: 1)
        - **156 ÷ 3 = 52** (no remainder)
        - **157 ÷ 3 = 52 R 1** (quotient: 52, remainder: 1)
        
        ### Tips:
        - **Check your work:** quotient × divisor + remainder = dividend
        - **Remainder must be smaller** than the divisor
        - **Take your time** with each step
        
        ### Difficulty Levels:
        - **🟡 2-digit numbers:** (10-99) ÷ (2-9)
        - **🟠 3-digit numbers:** (100-999) ÷ (2-9)  
        - **🔴 4+ digit numbers:** (1000+) ÷ (2-9)
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 4+ digit division!
        """)

def generate_new_division():
    """Generate a new division problem"""
    difficulty = st.session_state.divide_difficulty
    
    # Generate dividend based on difficulty
    if difficulty == 2:
        dividend = random.randint(20, 99)
    elif difficulty == 3:
        dividend = random.randint(100, 999)
    elif difficulty == 4:
        dividend = random.randint(1000, 9999)
    else:
        dividend = random.randint(10000, 99999)
    
    # Generate divisor (1-digit, 2-9)
    divisor = random.randint(2, 9)
    
    # Calculate correct answer
    quotient = dividend // divisor
    remainder = dividend % divisor
    
    st.session_state.division_data = {
        "dividend": dividend,
        "divisor": divisor
    }
    st.session_state.correct_quotient = quotient
    st.session_state.correct_remainder = remainder
    st.session_state.current_division = f"{dividend} ÷ {divisor}"

def display_division_question():
    """Display the current division question interface"""
    data = st.session_state.division_data
    dividend = data["dividend"]
    divisor = data["divisor"]
    
    # Display question header
    st.markdown("### ➗ Division Problem:")
    
    # Create the long division layout
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 40px; 
        border-radius: 15px; 
        border: 2px solid #dee2e6;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #333;
    ">
        <div style="margin-bottom: 20px; font-size: 20px; color: #666;">
            Solve this division problem:
        </div>
        <div style="font-size: 36px; color: #1f77b4;">
            {divisor}) {dividend:,}
        </div>
        <div style="margin-top: 20px; font-size: 18px; color: #666;">
            {dividend:,} ÷ {divisor} = ?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("division_form", clear_on_submit=False):
        st.markdown("**Enter your answer:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            quotient_input = st.number_input(
                "Quotient (answer):",
                min_value=0,
                step=1,
                key="quotient_input",
                help="The main answer (how many times it goes in)"
            )
        
        with col2:
            remainder_input = st.number_input(
                "Remainder:",
                min_value=0,
                max_value=divisor-1,
                step=1,
                key="remainder_input",
                help=f"What's left over (must be less than {divisor})"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_quotient = int(quotient_input) if quotient_input is not None else 0
            st.session_state.user_remainder = int(remainder_input) if remainder_input is not None else 0
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
    user_quotient = st.session_state.user_quotient
    user_remainder = st.session_state.user_remainder
    correct_quotient = st.session_state.correct_quotient
    correct_remainder = st.session_state.correct_remainder
    
    # Check if answer is correct
    quotient_correct = user_quotient == correct_quotient
    remainder_correct = user_remainder == correct_remainder
    
    if quotient_correct and remainder_correct:
        st.success("🎉 **Excellent! That's completely correct!**")
        
        # Show the complete answer
        if correct_remainder == 0:
            st.info(f"✅ **{st.session_state.division_data['dividend']} ÷ {st.session_state.division_data['divisor']} = {correct_quotient}** (no remainder)")
        else:
            st.info(f"✅ **{st.session_state.division_data['dividend']} ÷ {st.session_state.division_data['divisor']} = {correct_quotient} R {correct_remainder}**")
        
        # Increase difficulty (max 5 levels)
        old_difficulty = st.session_state.divide_difficulty
        st.session_state.divide_difficulty = min(st.session_state.divide_difficulty + 1, 5)
        
        if st.session_state.divide_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered division with large numbers!**")
        elif old_difficulty < st.session_state.divide_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.divide_difficulty}-digit numbers**")
    
    else:
        # Show what was wrong
        if not quotient_correct and not remainder_correct:
            st.error(f"❌ **Both answers are incorrect.**")
        elif not quotient_correct:
            st.error(f"❌ **Quotient is incorrect.** You said {user_quotient}, but it should be {correct_quotient}.")
        else:
            st.error(f"❌ **Remainder is incorrect.** You said {user_remainder}, but it should be {correct_remainder}.")
        
        # Show correct answer
        if correct_remainder == 0:
            st.info(f"**Correct answer:** {correct_quotient} (no remainder)")
        else:
            st.info(f"**Correct answer:** {correct_quotient} R {correct_remainder}")
        
        # Decrease difficulty (min level 2)
        old_difficulty = st.session_state.divide_difficulty
        st.session_state.divide_difficulty = max(st.session_state.divide_difficulty - 1, 2)
        
        if old_difficulty > st.session_state.divide_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.divide_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation of the division"""
    dividend = st.session_state.division_data["dividend"]
    divisor = st.session_state.division_data["divisor"]
    quotient = st.session_state.correct_quotient
    remainder = st.session_state.correct_remainder
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Long Division: {dividend} ÷ {divisor}
        
        **Problem:** {divisor}) {dividend}
        """)
        
        # Show step-by-step breakdown
        st.markdown("### Step-by-step solution:")
        
        # Convert to string to work with digits
        dividend_str = str(dividend)
        current_number = 0
        quotient_digits = []
        
        st.markdown("```")
        st.markdown(f"    {quotient}")
        st.markdown(f"{divisor}) {dividend}")
        
        # Simulate long division steps
        remainder_check = dividend
        temp_quotient = quotient
        
        # Show verification
        st.markdown("```")
        
        st.markdown(f"""
        ### Verification:
        - **Check:** {quotient} × {divisor} + {remainder} = {quotient * divisor + remainder}
        - **Original number:** {dividend}
        - **✅ Correct!** {quotient * divisor + remainder} = {dividend}
        
        ### Key Points:
        - **Quotient:** {quotient} (how many times {divisor} goes into {dividend})
        - **Remainder:** {remainder} (what's left over)
        - **Rule:** Remainder must be less than divisor ({remainder} < {divisor})
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_division = None
    st.session_state.correct_quotient = None
    st.session_state.correct_remainder = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.division_data = {}
    if "user_quotient" in st.session_state:
        del st.session_state.user_quotient
    if "user_remainder" in st.session_state:
        del st.session_state.user_remainder