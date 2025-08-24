import streamlit as st
import random

def run():
    """
    Main function to run the Even or Odd Arithmetic Rules practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/even_or_odd_arithmetic_rules.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "even_odd_arithmetic_difficulty" not in st.session_state:
        st.session_state.even_odd_arithmetic_difficulty = 2  # Start with 2-digit numbers
    
    if "even_odd_arithmetic_current_question" not in st.session_state:
        st.session_state.even_odd_arithmetic_current_question = None
        st.session_state.even_odd_arithmetic_correct_answer = None
        st.session_state.even_odd_arithmetic_show_feedback = False
        st.session_state.even_odd_arithmetic_answer_submitted = False
        st.session_state.even_odd_arithmetic_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("⚖️ Even or Odd: Arithmetic Rules")
    st.markdown("*Determine if arithmetic expressions result in even or odd numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.even_odd_arithmetic_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (1 to 4 digits)
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
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
    if st.session_state.even_odd_arithmetic_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the arithmetic expression**
        - **Determine if the result** will be even or odd
        - **Choose your answer** without calculating the exact number
        
        ### Even and Odd Rules:
        **Even numbers:** End in 0, 2, 4, 6, 8 (divisible by 2)
        **Odd numbers:** End in 1, 3, 5, 7, 9 (not divisible by 2)
        
        ### Addition Rules:
        - **Even + Even = Even** (e.g., 4 + 6 = 10)
        - **Odd + Odd = Even** (e.g., 3 + 5 = 8)
        - **Even + Odd = Odd** (e.g., 4 + 3 = 7)
        - **Odd + Even = Odd** (e.g., 5 + 2 = 7)
        
        ### Subtraction Rules:
        - **Even - Even = Even** (e.g., 8 - 4 = 4)
        - **Odd - Odd = Even** (e.g., 7 - 3 = 4)
        - **Even - Odd = Odd** (e.g., 8 - 3 = 5)
        - **Odd - Even = Odd** (e.g., 7 - 2 = 5)
        
        ### Quick Tips:
        - **Look at the last digit** of each number
        - **Apply the rules** without full calculation
        - **Same types (even+even, odd+odd) = Even**
        - **Different types (even+odd, odd+even) = Odd**
        
        ### Examples:
        - **246 + 138** → Even + Even = **Even**
        - **357 - 129** → Odd - Odd = **Even**
        - **482 + 35** → Even + Odd = **Odd**
        - **73 - 26** → Odd - Even = **Odd**
        
        ### Difficulty Levels:
        - **🟡 1-2 digit numbers:** Basic practice
        - **🟠 3 digit numbers:** Intermediate  
        - **🔴 4 digit numbers:** Advanced
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 4-digit arithmetic rules!
        """)

def generate_new_question():
    """Generate a new even/odd arithmetic question"""
    digits = st.session_state.even_odd_arithmetic_difficulty
    
    # Generate two random numbers with the specified number of digits
    if digits == 1:
        min_val, max_val = 1, 9
    else:
        min_val = 10**(digits - 1)
        max_val = 10**digits - 1
    
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    op = random.choice(["+", "-"])
    
    # Calculate result and determine even/odd
    if op == "+":
        result = a + b
        expression = f"{a:,} + {b:,}"
    else:
        result = a - b
        expression = f"{a:,} - {b:,}"
    
    correct_answer = "even" if result % 2 == 0 else "odd"
    
    st.session_state.even_odd_arithmetic_question_data = {
        "a": a,
        "b": b,
        "operation": op,
        "expression": expression,
        "result": result
    }
    st.session_state.even_odd_arithmetic_correct_answer = correct_answer
    st.session_state.even_odd_arithmetic_current_question = f"Is **{expression}** even or odd?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.even_odd_arithmetic_question_data
    
    # Display question with nice formatting
    st.markdown("### ⚖️ Question:")
    st.markdown(st.session_state.even_odd_arithmetic_current_question)
    
    # Display the expression in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #1f77b4;
    ">
        {data['expression']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Choose your answer:**")
        
        # Create radio button options with visual styling
        col1, col2 = st.columns(2)
        with col1:
            even_selected = st.radio(
                "Select:",
                ["Even", "Odd"],
                key="even_odd_arithmetic_choice",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.even_odd_arithmetic_user_answer = even_selected.lower()
            st.session_state.even_odd_arithmetic_show_feedback = True
            st.session_state.even_odd_arithmetic_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.even_odd_arithmetic_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.even_odd_arithmetic_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.even_odd_arithmetic_user_answer
    correct_answer = st.session_state.even_odd_arithmetic_correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 4 digits)
        old_difficulty = st.session_state.even_odd_arithmetic_difficulty
        st.session_state.even_odd_arithmetic_difficulty = min(
            st.session_state.even_odd_arithmetic_difficulty + 1, 4
        )
        
        # Show encouragement based on difficulty
        if st.session_state.even_odd_arithmetic_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 4-digit arithmetic rules!**")
        elif old_difficulty < st.session_state.even_odd_arithmetic_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.even_odd_arithmetic_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 1 digit)
        old_difficulty = st.session_state.even_odd_arithmetic_difficulty
        st.session_state.even_odd_arithmetic_difficulty = max(
            st.session_state.even_odd_arithmetic_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.even_odd_arithmetic_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.even_odd_arithmetic_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.even_odd_arithmetic_question_data
    a, b, op = data['a'], data['b'], data['operation']
    result = data['result']
    correct_answer = st.session_state.even_odd_arithmetic_correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step analysis: {data['expression']} = {result:,}
        """)
        
        # Determine if each number is even or odd
        a_type = "even" if a % 2 == 0 else "odd"
        b_type = "even" if b % 2 == 0 else "odd"
        
        st.markdown(f"""
        **Breaking it down:**
        - **{a:,}** is **{a_type}** (last digit: {a % 10})
        - **{b:,}** is **{b_type}** (last digit: {b % 10})
        """)
        
        # Apply the rules
        if op == "+":
            if a_type == b_type:
                st.markdown(f"- **Rule:** {a_type.title()} + {b_type.title()} = **Even**")
            else:
                st.markdown(f"- **Rule:** {a_type.title()} + {b_type.title()} = **Odd**")
        else:  # subtraction
            if a_type == b_type:
                st.markdown(f"- **Rule:** {a_type.title()} - {b_type.title()} = **Even**")
            else:
                st.markdown(f"- **Rule:** {a_type.title()} - {b_type.title()} = **Odd**")
        
        st.markdown(f"""
        **Verification:** {data['expression']} = {result:,}
        
        **Result:** {result:,} is **{correct_answer}** ✓
        """)
        
        # Add rule reminder
        if correct_answer == "even":
            st.info("💡 **Remember:** Same types or different types follow the pattern!")
        else:
            st.info("💡 **Remember:** Different types (even+odd or odd+even) always give odd results!")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.even_odd_arithmetic_current_question = None
    st.session_state.even_odd_arithmetic_correct_answer = None
    st.session_state.even_odd_arithmetic_show_feedback = False
    st.session_state.even_odd_arithmetic_answer_submitted = False
    st.session_state.even_odd_arithmetic_question_data = {}
    if "even_odd_arithmetic_user_answer" in st.session_state:
        del st.session_state.even_odd_arithmetic_user_answer