import streamlit as st
import random

def run():
    """
    Main function to run the Divide using Arrays practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 3/L. Division/divide_two_digit_numbers_by_one_digit_numbers_using_arrays.py
    """
    # Initialize session state for difficulty and game state
    if "divide_arrays_difficulty" not in st.session_state:
        st.session_state.divide_arrays_difficulty = 1  # Start with basic division
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 3 > L. Division**")
    st.title("🔢 Divide Using Arrays")
    st.markdown("*Use visual models to understand division with remainders*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_arrays_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Simple (10-25 ÷ 2-5)", 2: "Medium (20-50 ÷ 3-7)", 3: "Advanced (30-99 ÷ 4-9)"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/3")
    
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
        ### How to Play:
        - **Look at the array model** showing circles arranged in rows
        - **Count complete rows** - this gives you the quotient
        - **Count leftover circles** - this gives you the remainder
        - **Complete the division sentence** using what you see
        
        ### Understanding Arrays:
        - **Each row has the same number of items** (the divisor)
        - **Complete rows = quotient** (how many groups we can make)
        - **Leftover items = remainder** (what's left over)
        
        ### Example:
        - **22 ÷ 4:** We can make 5 complete rows of 4, with 2 left over
        - **Answer:** 22 ÷ 4 = 5 R2
        
        ### Question Types:
        1. **Find the quotient:** "21 ÷ 4 = ? R1"
        2. **Find the remainder:** "22 ÷ 4 = 5 R?"
        3. **Mixed practice** with different numbers
        
        ### Tips for Success:
        - **Count carefully:** Make sure you see all the rows
        - **Check remainders:** Remainder must be less than the divisor
        - **Use the model:** Let the visual help you understand
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple division (10-25 ÷ 2-5)
        - **🟠 Level 2:** Medium division (20-50 ÷ 3-7)  
        - **🔴 Level 3:** Advanced division (30-99 ÷ 4-9)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder problems
        - ❌ **Wrong answer:** Practice easier problems
        - 🎯 **Goal:** Master division with visual models!
        """)

def generate_new_question():
    """Generate a new divide using arrays question"""
    difficulty = st.session_state.divide_arrays_difficulty
    
    # Set number ranges based on difficulty
    if difficulty == 1:
        dividend = random.randint(10, 25)
        divisor = random.randint(2, 5)
    elif difficulty == 2:
        dividend = random.randint(20, 50)
        divisor = random.randint(3, 7)
    else:
        dividend = random.randint(30, 99)
        divisor = random.randint(4, 9)
    
    # Calculate quotient and remainder
    quotient = dividend // divisor
    remainder = dividend % divisor
    
    # Choose what to ask for (quotient or remainder)
    question_types = ["quotient", "remainder"]
    question_type = random.choice(question_types)
    
    # Choose circle color
    colors = ["#FFD700", "#32CD32", "#FF6347", "#4169E1", "#FF69B4", "#00CED1"]
    circle_color = random.choice(colors)
    
    if question_type == "quotient":
        equation_text = f"{dividend} ÷ {divisor} = ? R{remainder}"
        correct_answer = quotient
        asking_for = "quotient"
    else:
        equation_text = f"{dividend} ÷ {divisor} = {quotient} R?"
        correct_answer = remainder
        asking_for = "remainder"
    
    st.session_state.question_data = {
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "remainder": remainder,
        "equation_text": equation_text,
        "asking_for": asking_for,
        "circle_color": circle_color
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Use the model to complete the division number sentence."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🔢 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("---")
    
    # Create the visual array model
    create_array_visual(data)
    
    # Display the equation
    st.markdown("### Complete the division sentence:")
    
    # Create equation with input box
    equation_parts = data['equation_text'].split('?')
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        border: 2px solid #007bff;
        font-size: 32px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #333;
    ">
        {equation_parts[0]}<span style="color: #dc3545; background-color: #fff3cd; padding: 5px 15px; border-radius: 5px;">___</span>{equation_parts[1] if len(equation_parts) > 1 else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if data['asking_for'] == "quotient":
                help_text = "Count the number of complete rows"
                max_val = 50
            else:
                help_text = "Count the leftover circles"
                max_val = data['divisor'] - 1
            
            user_answer = st.number_input(
                f"Enter the missing {data['asking_for']}:",
                min_value=0,
                max_value=max_val,
                value=None,
                step=1,
                key="division_answer",
                help=help_text
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_array_visual(data):
    """Create the visual array model using HTML/CSS"""
    dividend = data['dividend']
    divisor = data['divisor']
    quotient = data['quotient']
    remainder = data['remainder']
    color = data['circle_color']
    
    # Calculate layout - circles in complete rows plus remainder
    complete_circles = quotient * divisor
    
    # Create the complete rows section
    rows_html = ""
    for row in range(quotient):
        row_html = ""
        for col in range(divisor):
            row_html += f'<span style="display: inline-block; width: 40px; height: 40px; background-color: {color}; border-radius: 50%; margin: 4px; border: 2px solid #333;"></span>'
        rows_html += f'<div style="margin: 8px 0; text-align: center;">{row_html}</div>'
    
    # Create remainder section if needed
    remainder_html = ""
    if remainder > 0:
        remainder_circles = ""
        for i in range(remainder):
            remainder_circles += f'<span style="display: inline-block; width: 40px; height: 40px; background-color: {color}; border-radius: 50%; margin: 4px; border: 2px solid #333;"></span>'
        remainder_html = f'<div style="margin: 20px 0; text-align: center;"><div style="margin: 8px 0;">{remainder_circles}</div></div>'
    
    # Display the visual array (circles only)
    html_content = f"""
    <div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 15px;">
        <div style="margin-bottom: 20px;">
            <h4 style="color: #333; margin-bottom: 15px;">Complete Rows:</h4>
            {rows_html}
        </div>
        {f'<div><h4 style="color: #333; margin-bottom: 15px;">Leftover:</h4>{remainder_html}</div>' if remainder > 0 else ''}
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Use Streamlit components for the summary text instead of HTML
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"""
        **📊 Array Summary:**
        
        🔵 **{complete_circles} circles** in **{quotient} complete rows** of **{divisor}**
        {f'➕ **{remainder} leftover circle{"s" if remainder != 1 else ""}**' if remainder > 0 else ''}
        
        🟰 **Total: {dividend} circles**
        """)
    st.markdown("---")

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
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 3)
        old_difficulty = st.session_state.divide_arrays_difficulty
        st.session_state.divide_arrays_difficulty = min(
            st.session_state.divide_arrays_difficulty + 1, 3
        )
        
        # Show encouragement based on difficulty
        if st.session_state.divide_arrays_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered division using arrays!**")
        elif old_difficulty < st.session_state.divide_arrays_difficulty:
            st.info(f"⬆️ **Level up! Now working with harder division problems**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.divide_arrays_difficulty
        st.session_state.divide_arrays_difficulty = max(
            st.session_state.divide_arrays_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.divide_arrays_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Keep going!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        dividend = data['dividend']
        divisor = data['divisor']
        quotient = data['quotient']
        remainder = data['remainder']
        asking_for = data['asking_for']
        
        st.markdown(f"""
        ### Step-by-step explanation:
        
        **Division:** {dividend} ÷ {divisor} = {quotient} R{remainder}
        
        ### How to read the array model:
        """)
        
        if asking_for == "quotient":
            st.markdown(f"""
            - **Count the complete rows:** Each row has {divisor} circles
            - **Number of complete rows:** {quotient}
            - **This is the quotient:** {quotient}
            - **Leftover circles:** {remainder} (shown separately)
            
            **Answer:** {dividend} ÷ {divisor} = **{quotient}** R{remainder}
            """)
        else:
            st.markdown(f"""
            - **Complete rows:** {quotient} rows of {divisor} = {quotient * divisor} circles
            - **Leftover circles:** Count the circles not in complete rows
            - **Number of leftover circles:** {remainder}
            - **This is the remainder:** {remainder}
            
            **Answer:** {dividend} ÷ {divisor} = {quotient} R**{remainder}**
            """)
        
        st.markdown(f"""
        ### Understanding division:
        - **{dividend} ÷ {divisor}** means "How many groups of {divisor} can we make from {dividend}?"
        - **We can make {quotient} complete groups** (rows)
        - **With {remainder} item{"s" if remainder != 1 else ""} left over**
        
        ### Check your work:
        - **{quotient} × {divisor} + {remainder} = {quotient * divisor} + {remainder} = {dividend}** ✓
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