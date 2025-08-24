import streamlit as st
import random

def run():
    """
    Main function to run the Division facts up to 10: find the missing number activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D.Division/division_facts_find_missing_number.py
    """
    # Initialize session state for difficulty and game state
    if "division_missing_difficulty" not in st.session_state:
        st.session_state.division_missing_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("🔍 Division Facts: Find the Missing Number")
    st.markdown("*Complete division equations by finding the missing dividend, divisor, or quotient*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.division_missing_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Three Types of Missing Numbers:
        1. **Missing Dividend:** ⬜ ÷ 5 = 2 (What number divided by 5 equals 2?)
        2. **Missing Divisor:** 15 ÷ ⬜ = 3 (15 divided by what number equals 3?)
        3. **Missing Quotient:** 12 ÷ 4 = ⬜ (12 divided by 4 equals what?)
        
        ### How to Find Each Type:
        
        **Finding Missing Dividend:**
        - Think: "What × divisor = dividend?"
        - Example: ⬜ ÷ 5 = 2 → 2 × 5 = **10**
        
        **Finding Missing Divisor:**
        - Think: "Dividend ÷ what = quotient?"
        - Example: 15 ÷ ⬜ = 3 → 15 ÷ 3 = **5**
        
        **Finding Missing Quotient:**
        - Think: "Dividend ÷ divisor = ?"
        - Example: 12 ÷ 4 = **3**
        
        ### Key Strategy - Use Multiplication:
        **Remember:** Division and multiplication are opposites!
        - If **a ÷ b = c**, then **c × b = a**
        - If **a ÷ b = c**, then **a ÷ c = b**
        
        ### Quick Methods:
        1. **For Missing Dividend:** Multiply quotient × divisor
        2. **For Missing Divisor:** Divide dividend ÷ quotient  
        3. **For Missing Quotient:** Divide dividend ÷ divisor
        
        ### Examples:
        - **⬜ ÷ 3 = 4** → 4 × 3 = **12**
        - **18 ÷ ⬜ = 6** → 18 ÷ 6 = **3**
        - **20 ÷ 5 = ⬜** → 20 ÷ 5 = **4**
        
        ### Check Your Work:
        Always verify by substituting your answer back into the original equation!
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Division by 1, 2, 5, 10 with smaller numbers
        - **🟠 Level 3:** Division by 3, 4, 6 with medium numbers
        - **🔴 Level 4-5:** All division facts 1-10 with larger numbers
        
        ### Key Skills:
        - ✅ **Understand the relationship** between multiplication and division
        - ✅ **Identify which number** is missing (dividend, divisor, or quotient)
        - ✅ **Apply the correct strategy** for each type
        - ✅ **Verify answers** using the opposite operation
        """)

def generate_missing_number_problem():
    """Generate division problems with missing numbers"""
    level = st.session_state.division_missing_difficulty
    
    # Define which divisors to use based on difficulty
    if level == 1:
        divisors = [2, 5, 10]  # Easiest facts
        max_quotient = 8
    elif level == 2:
        divisors = [1, 2, 3, 5, 10]  # Add 1 and 3
        max_quotient = 10
    elif level == 3:
        divisors = [2, 3, 4, 5, 6, 10]  # Add 4 and 6
        max_quotient = 12
    elif level == 4:
        divisors = [2, 3, 4, 5, 6, 7, 8, 9, 10]  # Add 7, 8, 9
        max_quotient = 12
    else:  # level 5
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts
        max_quotient = 15
    
    # Choose a random divisor and quotient
    divisor = random.choice(divisors)
    
    # Generate appropriate quotient
    if divisor == 1:
        quotient = random.randint(1, min(20, max_quotient))
    else:
        quotient = random.randint(1, max_quotient)
    
    # Calculate dividend
    dividend = divisor * quotient
    
    # Choose which number to hide (dividend, divisor, or quotient)
    missing_types = ["dividend", "divisor", "quotient"]
    
    # Weight the choices based on difficulty
    if level <= 2:
        # Focus more on missing quotient and dividend (easier)
        missing_type = random.choices(
            missing_types, 
            weights=[40, 30, 30]  # dividend, divisor, quotient
        )[0]
    else:
        # More balanced distribution for higher levels
        missing_type = random.choices(
            missing_types,
            weights=[35, 35, 30]
        )[0]
    
    return {
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "missing_type": missing_type
    }

def generate_new_question():
    """Generate a new missing number question"""
    question_data = generate_missing_number_problem()
    
    # Determine the correct answer based on what's missing
    if question_data["missing_type"] == "dividend":
        correct_answer = question_data["dividend"]
        equation = f"⬜ ÷ {question_data['divisor']} = {question_data['quotient']}"
    elif question_data["missing_type"] == "divisor":
        correct_answer = question_data["divisor"]
        equation = f"{question_data['dividend']} ÷ ⬜ = {question_data['quotient']}"
    else:  # missing quotient
        correct_answer = question_data["quotient"]
        equation = f"{question_data['dividend']} ÷ {question_data['divisor']} = ⬜"
    
    st.session_state.question_data = {
        **question_data,
        "equation": equation
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Fill in the missing number."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the instruction
    st.markdown("### 🔍 Fill in the missing number.")
    
    # Display the equation with the missing number
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 35px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        font-size: 32px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    ">
        {data['equation']}
    </div>
    """, unsafe_allow_html=True)
    
    # Input and submit
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_input = st.number_input(
                "Enter the missing number:",
                min_value=0,
                max_value=200,
                step=1,
                key="answer_input",
                label_visibility="collapsed",
                placeholder="Type your answer here..."
            )
            
            # Submit button
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            if user_input is not None and user_input >= 0:
                st.session_state.user_answer = int(user_input)
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            else:
                st.warning("Please enter a valid answer.")
    
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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete equation
        complete_equation = data['equation'].replace('⬜', str(correct_answer))
        st.markdown(f"**{complete_equation}** ✓")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.division_missing_difficulty
        st.session_state.division_missing_difficulty = min(
            st.session_state.division_missing_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.division_missing_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 missing number division!**")
        elif old_level < st.session_state.division_missing_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.division_missing_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.division_missing_difficulty
        st.session_state.division_missing_difficulty = max(
            st.session_state.division_missing_difficulty - 1, 1
        )
        
        if old_level > st.session_state.division_missing_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.division_missing_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    missing_type = data['missing_type']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['equation']}
        **Missing:** {missing_type.title()}
        """)
        
        if missing_type == "dividend":
            st.markdown(f"""
            **Strategy: Find the Dividend**
            - We know: ⬜ ÷ {data['divisor']} = {data['quotient']}
            - Think: "What number divided by {data['divisor']} equals {data['quotient']}?"
            - Use multiplication: {data['quotient']} × {data['divisor']} = ?
            
            **Solution:**
            {data['quotient']} × {data['divisor']} = **{correct_answer}**
            
            **Check:** {correct_answer} ÷ {data['divisor']} = {data['quotient']} ✓
            """)
            
        elif missing_type == "divisor":
            st.markdown(f"""
            **Strategy: Find the Divisor**
            - We know: {data['dividend']} ÷ ⬜ = {data['quotient']}
            - Think: "{data['dividend']} divided by what number equals {data['quotient']}?"
            - Use division: {data['dividend']} ÷ {data['quotient']} = ?
            
            **Solution:**
            {data['dividend']} ÷ {data['quotient']} = **{correct_answer}**
            
            **Check:** {data['dividend']} ÷ {correct_answer} = {data['quotient']} ✓
            """)
            
        else:  # missing quotient
            st.markdown(f"""
            **Strategy: Find the Quotient**
            - We know: {data['dividend']} ÷ {data['divisor']} = ⬜
            - Think: "{data['dividend']} divided by {data['divisor']} equals what?"
            - Use division: {data['dividend']} ÷ {data['divisor']} = ?
            
            **Solution:**
            {data['dividend']} ÷ {data['divisor']} = **{correct_answer}**
            
            **Check:** {correct_answer} × {data['divisor']} = {data['dividend']} ✓
            """)
        
        st.markdown(f"""
        **Final Answer:** {correct_answer}
        
        ### Remember:
        **Division and multiplication are opposites!**
        - If a ÷ b = c, then c × b = a
        - If a ÷ b = c, then a ÷ c = b
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer