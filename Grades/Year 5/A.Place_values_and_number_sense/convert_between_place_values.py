import streamlit as st
import random

def run():
    """
    Main function to run the Convert Between Place Values practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/convert_between_place_values.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "convert_place_values_difficulty" not in st.session_state:
        st.session_state.convert_place_values_difficulty = 2  # Start with level 2
    
    if "convert_place_values_current_question" not in st.session_state:
        st.session_state.convert_place_values_current_question = None
        st.session_state.convert_place_values_correct_answer = None
        st.session_state.convert_place_values_show_feedback = False
        st.session_state.convert_place_values_answer_submitted = False
        st.session_state.convert_place_values_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Convert Between Place Values")
    st.markdown("*Convert numbers between different place value units*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.convert_place_values_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** Level {difficulty_level}")
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
    if st.session_state.convert_place_values_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the place value conversion problem**
        - **Fill in the missing number** to make the equation correct
        - **Think about place value relationships**
        
        ### Place Value Chart:
        | Unit | Value |
        |------|-------|
        | **Ones** | 1 |
        | **Tens** | 10 |
        | **Hundreds** | 100 |
        | **Thousands** | 1,000 |
        | **Ten thousands** | 10,000 |
        | **Hundred thousands** | 100,000 |
        | **Millions** | 1,000,000 |
        
        ### Conversion Tips:
        - **To convert to smaller units:** Multiply
        - **To convert to larger units:** Divide
        - **Count the zeros** to find the relationship
        
        ### Examples:
        - **5 thousands = 50 hundreds** (5 × 10 = 50)
        - **3 hundreds = 30 tens** (3 × 10 = 30)
        - **400 ones = 4 hundreds** (400 ÷ 100 = 4)
        - **6 ten thousands = 60 thousands** (6 × 10 = 60)
        
        ### Common Conversions:
        - **1 ten = 10 ones**
        - **1 hundred = 10 tens = 100 ones**
        - **1 thousand = 10 hundreds = 100 tens = 1,000 ones**
        - **1 ten thousand = 10 thousands**
        - **1 hundred thousand = 100 thousands**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Basic conversions (ones, tens, hundreds)
        - **🟠 Level 3:** Intermediate (thousands, ten thousands)
        - **🔴 Level 4-5:** Advanced (hundred thousands, millions)
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master all place value conversions!
        """)

def get_place_value_name(value):
    """Get the place value name for a given value"""
    place_names = {
        1: "ones",
        10: "tens", 
        100: "hundreds",
        1000: "thousands",
        10000: "ten thousands",
        100000: "hundred thousands",
        1000000: "millions"
    }
    return place_names.get(value, str(value))

def generate_new_question():
    """Generate a new place value conversion question"""
    difficulty = st.session_state.convert_place_values_difficulty
    
    # Define place values available for each difficulty level
    if difficulty == 1:
        place_values = [1, 10, 100]
    elif difficulty == 2:
        place_values = [1, 10, 100, 1000]
    elif difficulty == 3:
        place_values = [10, 100, 1000, 10000]
    elif difficulty == 4:
        place_values = [100, 1000, 10000, 100000]
    else:  # difficulty 5
        place_values = [1000, 10000, 100000, 1000000]
    
    # Choose two different place values
    from_place = random.choice(place_values)
    to_place = random.choice([pv for pv in place_values if pv != from_place])
    
    # Generate a reasonable coefficient (1-9 for most cases)
    if from_place > to_place:
        # Converting to smaller units (multiply)
        coefficient = random.randint(1, 9)
        result = coefficient * (from_place // to_place)
        question_type = "multiply"
    else:
        # Converting to larger units (divide)
        # Make sure we get a whole number result
        multiplier = to_place // from_place
        result = random.randint(1, 9)
        coefficient = result * multiplier
        question_type = "divide"
    
    # Randomly decide if we're solving for the coefficient or the result
    solve_for = random.choice(["coefficient", "result"])
    
    from_name = get_place_value_name(from_place)
    to_name = get_place_value_name(to_place)
    
    if solve_for == "coefficient":
        # Solve: ? [from_name] = [result] [to_name]
        question_text = f"**? {from_name} = {result:,} {to_name}**"
        correct_answer = str(coefficient)
        blank_position = "left"
    else:
        # Solve: [coefficient] [from_name] = ? [to_name]
        question_text = f"**{coefficient} {from_name} = ? {to_name}**"
        correct_answer = str(result)
        blank_position = "right"
    
    st.session_state.convert_place_values_question_data = {
        "coefficient": coefficient,
        "from_place": from_place,
        "to_place": to_place,
        "from_name": from_name,
        "to_name": to_name,
        "result": result,
        "solve_for": solve_for,
        "blank_position": blank_position,
        "question_text": question_text
    }
    st.session_state.convert_place_values_correct_answer = correct_answer
    st.session_state.convert_place_values_current_question = "Fill in the missing number:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.convert_place_values_question_data
    
    # Display question with nice formatting
    st.markdown("### 🔄 Question:")
    st.markdown(st.session_state.convert_place_values_current_question)
    
    # Display the conversion equation in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        font-size: 24px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #1f77b4;
    ">
        {data['question_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Type your answer:**")
        
        user_answer = st.text_input(
            "Your answer:",
            placeholder="Enter the missing number",
            key="convert_place_values_input",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer.strip():
            st.session_state.convert_place_values_user_answer = user_answer.strip()
            st.session_state.convert_place_values_show_feedback = True
            st.session_state.convert_place_values_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.convert_place_values_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.convert_place_values_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.convert_place_values_user_answer
    correct_answer = st.session_state.convert_place_values_correct_answer
    
    # Clean user input (remove commas and spaces)
    cleaned_user_answer = user_answer.replace(",", "").replace(" ", "")
    
    if cleaned_user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.convert_place_values_difficulty
        st.session_state.convert_place_values_difficulty = min(
            st.session_state.convert_place_values_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.convert_place_values_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered all place value conversions!**")
        elif old_difficulty < st.session_state.convert_place_values_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now at Level {st.session_state.convert_place_values_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{int(correct_answer):,}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.convert_place_values_difficulty
        st.session_state.convert_place_values_difficulty = max(
            st.session_state.convert_place_values_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.convert_place_values_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.convert_place_values_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.convert_place_values_question_data
    correct_answer = int(st.session_state.convert_place_values_correct_answer)
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if data['solve_for'] == "coefficient":
            st.markdown(f"""
            ### Step-by-step conversion: ? {data['from_name']} = {data['result']:,} {data['to_name']}
            """)
        else:
            st.markdown(f"""
            ### Step-by-step conversion: {data['coefficient']} {data['from_name']} = ? {data['to_name']}
            """)
        
        # Explain the conversion process
        from_place = data['from_place']
        to_place = data['to_place']
        
        st.markdown(f"""
        **Understanding the relationship:**
        - **1 {data['from_name']}** = {from_place:,} ones
        - **1 {data['to_name']}** = {to_place:,} ones
        """)
        
        if from_place > to_place:
            # Converting to smaller units
            factor = from_place // to_place
            st.markdown(f"""
            **Conversion factor:** 1 {data['from_name']} = {factor} {data['to_name']}
            """)
            
            if data['solve_for'] == "coefficient":
                st.markdown(f"""
                **Working backwards:**
                - {data['result']:,} {data['to_name']} ÷ {factor} = {correct_answer} {data['from_name']}
                """)
            else:
                st.markdown(f"""
                **Multiply to convert to smaller units:**
                - {data['coefficient']} × {factor} = {correct_answer:,} {data['to_name']}
                """)
        else:
            # Converting to larger units
            factor = to_place // from_place
            st.markdown(f"""
            **Conversion factor:** {factor} {data['from_name']} = 1 {data['to_name']}
            """)
            
            if data['solve_for'] == "coefficient":
                st.markdown(f"""
                **Working backwards:**
                - {data['result']:,} {data['to_name']} × {factor} = {correct_answer:,} {data['from_name']}
                """)
            else:
                st.markdown(f"""
                **Divide to convert to larger units:**
                - {data['coefficient']:,} ÷ {factor} = {correct_answer} {data['to_name']}
                """)
        
        st.markdown(f"**Final answer:** {correct_answer:,}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.convert_place_values_current_question = None
    st.session_state.convert_place_values_correct_answer = None
    st.session_state.convert_place_values_show_feedback = False
    st.session_state.convert_place_values_answer_submitted = False
    st.session_state.convert_place_values_question_data = {}
    if "convert_place_values_user_answer" in st.session_state:
        del st.session_state.convert_place_values_user_answer