import streamlit as st
import random

def run():
    """
    Main function to run the Relate Multiplication and Division practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 3/R. Properties/relate_multiplication_and_division.py
    """
    # Initialize session state for difficulty and game state
    if "relate_mult_div_difficulty" not in st.session_state:
        st.session_state.relate_mult_div_difficulty = 1  # Start with basic facts
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 3 > R. Properties**")
    st.title("🔗 Relate Multiplication and Division")
    st.markdown("*Understand how multiplication and division are inverse operations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.relate_mult_div_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Basic Facts (1-5)", 2: "Medium Facts (1-8)", 3: "Advanced Facts (1-12)"}
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
        - **Read the given fact** (multiplication or division)
        - **Find the missing number** in the related fact
        - **Remember:** Multiplication and division are inverse operations
        
        ### Understanding the Relationship:
        - **If 6 × 4 = 24, then 24 ÷ 6 = 4 and 24 ÷ 4 = 6**
        - **If 35 ÷ 7 = 5, then 7 × 5 = 35 and 5 × 7 = 35**
        
        ### Question Types:
        1. **Division → Multiplication:** "If 20 ÷ 4 = 5, then 4 × ? = 20"
        2. **Division → Missing Factor:** "If 18 ÷ 3 = 6, then 3 × ? = 18"
        3. **Multiplication → Division:** "If 7 × 8 = 56, then 56 ÷ ? = 8"
        
        ### Tips for Success:
        - **Think in fact families:** 3, 4, and 12 go together
        - **Use what you know:** If 3 × 4 = 12, then 12 ÷ 3 = 4
        - **Check your work:** Multiply to check division, divide to check multiplication
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Basic facts (numbers 1-5)
        - **🟠 Level 2:** Medium facts (numbers 1-8)  
        - **🔴 Level 3:** Advanced facts (numbers 1-12)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder facts
        - ❌ **Wrong answer:** Practice easier facts
        - 🎯 **Goal:** Master all fact families!
        """)

def generate_new_question():
    """Generate a new relate multiplication and division question"""
    difficulty = st.session_state.relate_mult_div_difficulty
    
    # Set number ranges based on difficulty
    if difficulty == 1:
        max_factor = 5
    elif difficulty == 2:
        max_factor = 8
    else:
        max_factor = 12
    
    # Generate two factors
    factor1 = random.randint(1, max_factor)
    factor2 = random.randint(1, max_factor)
    product = factor1 * factor2
    
    # Choose question type
    question_types = [
        "div_to_mult",      # If 20 ÷ 4 = 5, then 4 × ? = 20
        "div_to_mult_alt",  # If 20 ÷ 4 = 5, then ? × 4 = 20  
        "mult_to_div",      # If 4 × 5 = 20, then 20 ÷ ? = 5
        "mult_to_div_alt"   # If 4 × 5 = 20, then ? ÷ 4 = 5
    ]
    
    question_type = random.choice(question_types)
    
    if question_type == "div_to_mult":
        # If 20 ÷ 4 = 5, then 4 × ? = 20
        given_dividend = product
        given_divisor = factor1
        given_quotient = factor2
        question_text = f"If {given_dividend} ÷ {given_divisor} = {given_quotient}, then..."
        incomplete_text = f"{given_divisor} × ? = {given_dividend}"
        correct_answer = given_quotient
        
    elif question_type == "div_to_mult_alt":
        # If 20 ÷ 4 = 5, then ? × 4 = 20
        given_dividend = product
        given_divisor = factor1
        given_quotient = factor2
        question_text = f"If {given_dividend} ÷ {given_divisor} = {given_quotient}, then..."
        incomplete_text = f"? × {given_divisor} = {given_dividend}"
        correct_answer = given_quotient
        
    elif question_type == "mult_to_div":
        # If 4 × 5 = 20, then 20 ÷ ? = 5
        question_text = f"If {factor1} × {factor2} = {product}, then..."
        incomplete_text = f"{product} ÷ ? = {factor2}"
        correct_answer = factor1
        
    else:  # mult_to_div_alt
        # If 4 × 5 = 20, then ? ÷ 4 = 5
        question_text = f"If {factor1} × {factor2} = {product}, then..."
        incomplete_text = f"? ÷ {factor1} = {factor2}"
        correct_answer = product
    
    st.session_state.question_data = {
        "question_text": question_text,
        "incomplete_text": incomplete_text,
        "question_type": question_type
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Find the missing number:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🔗 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the given fact in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #1f77b4;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #1f77b4;
    ">
        {data['question_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display the incomplete equation with input box
    incomplete_parts = data['incomplete_text'].split('?')
    
    st.markdown("**Complete this equation:**")
    
    # Create a custom HTML layout with the input box
    st.markdown(f"""
    <div style="
        background-color: #fff8dc; 
        padding: 25px; 
        border-radius: 10px; 
        border: 2px solid #ffa500;
        font-size: 28px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #333;
    ">
        {incomplete_parts[0]}<span style="color: #ff6b6b;">___</span>{incomplete_parts[1] if len(incomplete_parts) > 1 else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.number_input(
                "Enter the missing number:",
                min_value=0,
                max_value=200,
                value=None,
                step=1,
                key="missing_number",
                help="Type the number that goes in the blank"
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
        old_difficulty = st.session_state.relate_mult_div_difficulty
        st.session_state.relate_mult_div_difficulty = min(
            st.session_state.relate_mult_div_difficulty + 1, 3
        )
        
        # Show encouragement based on difficulty
        if st.session_state.relate_mult_div_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered multiplication and division relationships!**")
        elif old_difficulty < st.session_state.relate_mult_div_difficulty:
            st.info(f"⬆️ **Level up! Now working with harder fact families**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.relate_mult_div_difficulty
        st.session_state.relate_mult_div_difficulty = max(
            st.session_state.relate_mult_div_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.relate_mult_div_difficulty:
            st.warning(f"⬇️ **Let's practice easier facts first. Keep going!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    question_type = data['question_type']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step explanation:
        
        **Given:** {data['question_text']}
        **Complete:** {data['incomplete_text'].replace('?', str(correct_answer))}
        
        ### Why this works:
        """)
        
        if question_type in ["div_to_mult", "div_to_mult_alt"]:
            # Extract numbers from the given division fact
            given_text = data['question_text']
            parts = given_text.replace("If ", "").replace(", then...", "").split(" = ")
            division_part = parts[0]
            quotient = parts[1]
            dividend, divisor = division_part.split(" ÷ ")
            
            st.markdown(f"""
            - **Division fact:** {dividend} ÷ {divisor} = {quotient}
            - **This means:** {divisor} groups of {quotient} makes {dividend}
            - **So multiplication:** {divisor} × {quotient} = {dividend}
            - **Or:** {quotient} × {divisor} = {dividend}
            
            **Remember:** Division and multiplication are inverse operations!
            """)
            
        else:  # mult_to_div or mult_to_div_alt
            # Extract numbers from the given multiplication fact
            given_text = data['question_text']
            parts = given_text.replace("If ", "").replace(", then...", "").split(" = ")
            multiplication_part = parts[0]
            product = parts[1]
            factor1, factor2 = multiplication_part.split(" × ")
            
            st.markdown(f"""
            - **Multiplication fact:** {factor1} × {factor2} = {product}
            - **This means:** {factor1} groups of {factor2} makes {product}
            - **So we can divide:** {product} ÷ {factor1} = {factor2}
            - **Or:** {product} ÷ {factor2} = {factor1}
            
            **Remember:** If you know one fact, you know the whole family!
            """)
        
        # Show the complete fact family
        if question_type in ["div_to_mult", "div_to_mult_alt"]:
            given_text = data['question_text']
            parts = given_text.replace("If ", "").replace(", then...", "").split(" = ")
            division_part = parts[0]
            quotient = parts[1]
            dividend, divisor = division_part.split(" ÷ ")
            
            st.markdown(f"""
            ### Complete Fact Family:
            - **{divisor} × {quotient} = {dividend}**
            - **{quotient} × {divisor} = {dividend}**
            - **{dividend} ÷ {divisor} = {quotient}**
            - **{dividend} ÷ {quotient} = {divisor}**
            """)
        else:
            given_text = data['question_text']
            parts = given_text.replace("If ", "").replace(", then...", "").split(" = ")
            multiplication_part = parts[0]
            product = parts[1]
            factor1, factor2 = multiplication_part.split(" × ")
            
            st.markdown(f"""
            ### Complete Fact Family:
            - **{factor1} × {factor2} = {product}**
            - **{factor2} × {factor1} = {product}**
            - **{product} ÷ {factor1} = {factor2}**
            - **{product} ÷ {factor2} = {factor1}**
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