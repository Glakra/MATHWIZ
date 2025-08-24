import streamlit as st
import random

def run():
    """
    Main function to run the Division facts to 10 activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D.Division/division_facts_to_10.py
    """
    # Initialize session state for difficulty and game state
    if "division_facts_difficulty" not in st.session_state:
        st.session_state.division_facts_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("➗ Division Facts to 10")
    st.markdown("*Master basic division facts with divisors up to 10*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.division_facts_difficulty
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
        ### How Division Works:
        - **Division** is the opposite of multiplication
        - **8 ÷ 2 = 4** means "8 divided into 2 equal groups gives 4 in each group"
        - **Think multiplication:** If 2 × 4 = 8, then 8 ÷ 2 = 4
        
        ### Two Question Formats:
        1. **Standard Format:** 8 ÷ 8 = ? (Find the quotient)
        2. **Long Division Format:** The quotient (answer) goes in the box on top
           ```
              ⬜
           ____
         5 ) 20
           ```
        
        ### Quick Strategies:
        1. **Use Related Multiplication Facts:**
           - If 3 × 4 = 12, then 12 ÷ 3 = 4 and 12 ÷ 4 = 3
        
        2. **Special Division Rules:**
           - **Any number ÷ 1 = same number** (7 ÷ 1 = 7)
           - **Any number ÷ itself = 1** (5 ÷ 5 = 1)
           - **0 ÷ any number = 0** (0 ÷ 4 = 0)
        
        3. **Think "How Many Groups?"**
           - 15 ÷ 3 = ? means "How many 3s are in 15?"
           - Count: 3, 6, 9, 12, 15 = five 3s, so 15 ÷ 3 = 5
        
        ### Key Division Facts to Remember:
        - **÷1:** 7÷1=7, 9÷1=9 (dividing by 1 doesn't change the number)
        - **÷2:** 8÷2=4, 10÷2=5, 14÷2=7 (half the number)
        - **÷5:** 15÷5=3, 20÷5=4, 25÷5=5 (count by 5s)
        - **÷10:** 30÷10=3, 60÷10=6 (remove one zero)
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Division by 1, 2, 5, 10 (easier facts)
        - **🟠 Level 3:** Division by 3, 4, 6 (medium facts)
        - **🔴 Level 4-5:** All division facts 1-10 (harder combinations)
        
        ### Examples:
        - **6 ÷ 2 = 3** (because 2 × 3 = 6)
        - **8 ÷ 4 = 2** (because 4 × 2 = 8)
        - **9 ÷ 3 = 3** (because 3 × 3 = 9)
        
        ### Key Skills:
        - ✅ **Memorize division facts** up to 10
        - ✅ **Connect to multiplication** facts
        - ✅ **Recognize patterns** in division
        - ✅ **Use mental math** strategies
        """)

def generate_division_facts():
    """Generate division facts based on difficulty level"""
    level = st.session_state.division_facts_difficulty
    
    # Define which divisors to use based on difficulty
    if level == 1:
        divisors = [1, 2, 5, 10]  # Easiest facts
        max_dividend = 20
    elif level == 2:
        divisors = [1, 2, 3, 5, 10]  # Add 3
        max_dividend = 30
    elif level == 3:
        divisors = [1, 2, 3, 4, 5, 6, 10]  # Add 4 and 6
        max_dividend = 60
    elif level == 4:
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts
        max_dividend = 90
    else:  # level 5
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts, larger numbers
        max_dividend = 100
    
    # Choose a random divisor
    divisor = random.choice(divisors)
    
    # Generate appropriate quotients
    if divisor == 1:
        quotient = random.randint(1, min(10, max_dividend))
    else:
        max_quotient = min(10, max_dividend // divisor)
        quotient = random.randint(1, max_quotient)
    
    # Calculate dividend
    dividend = divisor * quotient
    
    return dividend, divisor, quotient

def generate_new_question():
    """Generate a new division question"""
    dividend, divisor, quotient = generate_division_facts()
    
    # Choose question format (standard or long division)
    format_type = random.choice(["standard", "long_division"])
    
    st.session_state.question_data = {
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "format_type": format_type
    }
    st.session_state.correct_answer = quotient
    st.session_state.current_question = "Solve the division problem:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question header
    st.markdown("### ➗ Divide:")
    
    if data["format_type"] == "standard":
        # Standard format: a ÷ b = ?
        display_standard_format(data)
    else:
        # Long division format: ?)a
        display_long_division_format(data)
    
    # Input and submit
    display_input_and_submit()

def display_standard_format(data):
    """Display standard division format"""
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
        {data['dividend']} ÷ {data['divisor']} = ⬜
    </div>
    """, unsafe_allow_html=True)

def display_long_division_format(data):
    """Display long division format with quotient on top"""
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 40px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    ">
        <div style="margin-bottom: 8px; margin-left: 80px;">
            <span style="
                border: 2px solid #2c3e50; 
                padding: 8px 16px; 
                font-size: 24px;
            ">⬜</span>
        </div>
        <div style="font-size: 28px;">
            <span style="margin-right: 15px;">{data['divisor']}</span>
            <span style="margin-right: 15px;">)</span>
            <span style="
                border-top: 3px solid #2c3e50; 
                padding-top: 8px;
                display: inline-block;
            ">{data['dividend']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_input_and_submit():
    """Display input field and submit button"""
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_input = st.number_input(
                "Enter your answer:",
                min_value=0,
                max_value=100,
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
        st.markdown(f"**{data['dividend']} ÷ {data['divisor']} = {correct_answer}** ✓")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.division_facts_difficulty
        st.session_state.division_facts_difficulty = min(
            st.session_state.division_facts_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.division_facts_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 division facts!**")
        elif old_level < st.session_state.division_facts_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.division_facts_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.division_facts_difficulty
        st.session_state.division_facts_difficulty = max(
            st.session_state.division_facts_difficulty - 1, 1
        )
        
        if old_level > st.session_state.division_facts_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.division_facts_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    dividend = data['dividend']
    divisor = data['divisor']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {dividend} ÷ {divisor} = ?
        
        **Method 1: Think Multiplication**
        - What number times {divisor} equals {dividend}?
        - {divisor} × ? = {dividend}
        - {divisor} × **{correct_answer}** = {dividend} ✓
        """)
        
        # Show different strategies based on the divisor
        if divisor == 1:
            st.markdown(f"""
            **Method 2: Division by 1 Rule**
            - Any number divided by 1 equals itself
            - {dividend} ÷ 1 = {dividend}
            """)
        elif divisor == dividend:
            st.markdown(f"""
            **Method 2: Number Divided by Itself**
            - Any number divided by itself equals 1
            - {dividend} ÷ {dividend} = 1
            """)
        elif divisor == 2:
            st.markdown(f"""
            **Method 2: Division by 2 (Finding Half)**
            - {dividend} ÷ 2 means "half of {dividend}"
            - Half of {dividend} = {correct_answer}
            """)
        elif divisor == 5:
            st.markdown(f"""
            **Method 2: Count by 5s**
            - How many 5s make {dividend}?
            - Count: 5, 10, 15, 20, 25, 30...
            - {correct_answer} groups of 5 make {dividend}
            """)
        elif divisor == 10:
            st.markdown(f"""
            **Method 2: Division by 10 Rule**
            - Remove one zero from the end
            - {dividend} ÷ 10 = {correct_answer}
            """)
        else:
            st.markdown(f"""
            **Method 2: Count Groups**
            - How many groups of {divisor} fit into {dividend}?
            - Start counting: {divisor}, {divisor*2}, {divisor*3}...
            - {correct_answer} groups of {divisor} = {dividend}
            """)
        
        st.markdown(f"""
        **Final Answer:** {dividend} ÷ {divisor} = **{correct_answer}**
        
        **Check Your Work:**
        {correct_answer} × {divisor} = {dividend} ✓
        """)
        
        # Memory tip
        memory_tips = {
            1: "Dividing by 1 never changes the number!",
            2: "Dividing by 2 gives you half the number.",
            5: "Count by 5s to find how many groups.",
            10: "Dividing by 10 removes one zero from the end."
        }
        
        if divisor in memory_tips:
            st.markdown(f"**💡 Memory Tip:** {memory_tips[divisor]}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer