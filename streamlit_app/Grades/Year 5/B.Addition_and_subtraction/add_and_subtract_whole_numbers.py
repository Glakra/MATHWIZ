import streamlit as st
import random

def run():
    """
    Main function to run the Add and Subtract Whole Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B.Addition and subtraction/add_and_subtract_whole_numbers.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "add_subtract_whole_numbers_difficulty" not in st.session_state:
        st.session_state.add_subtract_whole_numbers_difficulty = 3  # Start with 3-digit numbers
    
    if "add_subtract_whole_numbers_current_question" not in st.session_state:
        st.session_state.add_subtract_whole_numbers_current_question = None
        st.session_state.add_subtract_whole_numbers_correct_answer = None
        st.session_state.add_subtract_whole_numbers_show_feedback = False
        st.session_state.add_subtract_whole_numbers_answer_submitted = False
        st.session_state.add_subtract_whole_numbers_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("➕➖ Add and Subtract Whole Numbers")
    st.markdown("*Practice addition and subtraction with multi-digit numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.add_subtract_whole_numbers_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit base numbers")
        # Progress bar (2 to 6 digits)
        progress = (difficulty_level - 2) / 4  # Convert 2-6 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level <= 3:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 4:
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
    if st.session_state.add_subtract_whole_numbers_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the vertical arithmetic problem**
        - **Calculate the answer** using addition or subtraction
        - **Type your answer** in the text box
        
        ### Addition Tips:
        - **Start from the rightmost column** (ones place)
        - **Add digits column by column**
        - **Remember to carry** when the sum is 10 or more
        - **Write carried digits** above the next column
        
        ### Subtraction Tips:
        - **Start from the rightmost column** (ones place)
        - **Subtract digits column by column**
        - **Borrow from the next column** when needed
        - **Cross out and reduce** the borrowed-from digit
        
        ### Examples:
        **Addition:**
        ```
           1,234
        +    567
        -------
           1,801
        ```
        
        **Subtraction:**
        ```
           5,432
        -  1,789
        -------
           3,643
        ```
        
        ### Strategy Tips:
        - **Estimate first:** Round numbers to check if your answer makes sense
        - **Double-check:** Use the inverse operation to verify
        - **Practice place values:** Know your thousands, hundreds, tens, ones
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** Basic practice
        - **🟠 4-5 digit numbers:** Intermediate
        - **🔴 6 digit numbers:** Advanced
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 6-digit arithmetic!
        """)

def generate_new_question():
    """Generate a new addition or subtraction question"""
    base_digits = st.session_state.add_subtract_whole_numbers_difficulty
    
    # Choose operation type
    q_type = random.choice(["add", "sub"])
    
    # Generate numbers with variable digit lengths
    digits_a = random.randint(base_digits, base_digits + 2)
    digits_b = random.randint(base_digits, base_digits + 1)
    
    a = random.randint(10**(digits_a - 1), 10**digits_a - 1)
    b = random.randint(10**(digits_b - 1), 10**digits_b - 1)
    
    if q_type == "add":
        answer = a + b
        label = "Add."
        symbol = "+"
        operation = "addition"
    else:
        # Ensure no negative results
        if b > a:
            a, b = b, a
        answer = a - b
        label = "Subtract."
        symbol = "−"  # Using minus sign, not hyphen
        operation = "subtraction"
    
    # Format numbers for vertical display
    max_len = max(len(str(a)), len(str(b)), len(str(answer)))
    top_formatted = str(a).rjust(max_len)
    bottom_formatted = str(b).rjust(max_len)
    
    st.session_state.add_subtract_whole_numbers_question_data = {
        "a": a,
        "b": b,
        "answer": answer,
        "label": label,
        "symbol": symbol,
        "operation": operation,
        "top_formatted": top_formatted,
        "bottom_formatted": bottom_formatted,
        "max_len": max_len
    }
    st.session_state.add_subtract_whole_numbers_correct_answer = str(answer)
    st.session_state.add_subtract_whole_numbers_current_question = label

def display_question():
    """Display the current question interface"""
    data = st.session_state.add_subtract_whole_numbers_question_data
    
    # Display question with nice formatting
    st.markdown("### ➕➖ Question:")
    st.markdown(data["label"])
    
    # Display the vertical arithmetic problem in a highlighted box
    vertical_problem = f"  {data['top_formatted']}\n{data['symbol']} {data['bottom_formatted']}\n{'─' * (data['max_len'] + 2)}"
    
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        font-family: 'Courier New', monospace;
        font-size: 20px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #1f77b4;
        white-space: pre-line;
    ">
{vertical_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Type your answer:**")
        
        user_answer = st.text_input(
            "Your answer:",
            placeholder="Enter your answer",
            key="add_subtract_whole_numbers_input",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer.strip():
            st.session_state.add_subtract_whole_numbers_user_answer = user_answer.strip()
            st.session_state.add_subtract_whole_numbers_show_feedback = True
            st.session_state.add_subtract_whole_numbers_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.add_subtract_whole_numbers_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.add_subtract_whole_numbers_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.add_subtract_whole_numbers_user_answer
    correct_answer = st.session_state.add_subtract_whole_numbers_correct_answer
    
    # Clean user input (remove commas and spaces, strip leading zeros)
    cleaned_user_answer = user_answer.replace(",", "").replace(" ", "").lstrip("0")
    if not cleaned_user_answer:  # Handle case where user enters just "0"
        cleaned_user_answer = "0"
    
    if cleaned_user_answer == correct_answer:
        st.success("🎉 **Correct! Nice work!**")
        
        # Increase difficulty (max 6 digits)
        old_difficulty = st.session_state.add_subtract_whole_numbers_difficulty
        st.session_state.add_subtract_whole_numbers_difficulty = min(
            st.session_state.add_subtract_whole_numbers_difficulty + 1, 6
        )
        
        # Show encouragement based on difficulty
        if st.session_state.add_subtract_whole_numbers_difficulty == 6 and old_difficulty < 6:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 6-digit arithmetic!**")
        elif old_difficulty < st.session_state.add_subtract_whole_numbers_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.add_subtract_whole_numbers_difficulty}-digit base numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{int(correct_answer):,}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.add_subtract_whole_numbers_difficulty
        st.session_state.add_subtract_whole_numbers_difficulty = max(
            st.session_state.add_subtract_whole_numbers_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.add_subtract_whole_numbers_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.add_subtract_whole_numbers_difficulty}-digit base numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.add_subtract_whole_numbers_question_data
    a, b, answer = data['a'], data['b'], data['answer']
    operation = data['operation']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step {operation}:
        """)
        
        # Show the problem again
        vertical_problem = f"  {data['top_formatted']}\n{data['symbol']} {data['bottom_formatted']}\n{'─' * (data['max_len'] + 2)}\n  {str(answer).rjust(data['max_len'])}"
        
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa; 
            padding: 20px; 
            border-radius: 10px; 
            font-family: 'Courier New', monospace;
            font-size: 16px;
            text-align: center;
            margin: 20px 0;
            color: #333;
            white-space: pre-line;
        ">
{vertical_problem}
        </div>
        """, unsafe_allow_html=True)
        
        if operation == "addition":
            st.markdown(f"""
            **Breaking it down:**
            - **{a:,}** + **{b:,}** = **{answer:,}**
            - Start from the rightmost column (ones place)
            - Add each column, carrying when the sum ≥ 10
            - Work your way left through tens, hundreds, thousands, etc.
            """)
        else:
            st.markdown(f"""
            **Breaking it down:**
            - **{a:,}** − **{b:,}** = **{answer:,}**
            - Start from the rightmost column (ones place)  
            - Subtract each column, borrowing when needed
            - Work your way left through tens, hundreds, thousands, etc.
            """)
        
        # Verification tip
        if operation == "addition":
            st.info(f"💡 **Check your work:** {answer:,} − {b:,} = {a:,} ✓")
        else:
            st.info(f"💡 **Check your work:** {answer:,} + {b:,} = {a:,} ✓")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.add_subtract_whole_numbers_current_question = None
    st.session_state.add_subtract_whole_numbers_correct_answer = None
    st.session_state.add_subtract_whole_numbers_show_feedback = False
    st.session_state.add_subtract_whole_numbers_answer_submitted = False
    st.session_state.add_subtract_whole_numbers_question_data = {}
    if "add_subtract_whole_numbers_user_answer" in st.session_state:
        del st.session_state.add_subtract_whole_numbers_user_answer