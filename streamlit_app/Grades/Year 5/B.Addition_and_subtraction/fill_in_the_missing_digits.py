import streamlit as st
import random

def run():
    """
    Main function to run the Fill Missing Digits practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/fill_in_the_missing_digits.py
    """
    # Initialize session state for difficulty and game state
    if "fill_missing_digit_difficulty" not in st.session_state:
        st.session_state.fill_missing_digit_difficulty = {"digits": 3}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("🔍 Fill in the Missing Digits")
    st.markdown("*Find the missing digit in addition and subtraction problems*")
    st.markdown("---")
    
    # Difficulty indicator
    current_digits = st.session_state.fill_missing_digit_difficulty["digits"]
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {current_digits}-digit numbers")
        # Progress bar (2 to 6 digits)
        progress = (current_digits - 2) / 4  # Convert 2-6 to 0-1
        st.progress(progress, text=f"{current_digits}-digit numbers")
    
    with col2:
        if current_digits <= 3:
            st.markdown("**🟡 Beginner**")
        elif current_digits <= 4:
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
        - **Look at the vertical equation** with one missing digit (shown as ⬜)
        - **Type the single digit** (0-9) that belongs in the empty box
        - **Use place value knowledge** to figure out what digit makes the equation correct
        - **Check your work** by verifying the complete equation
        
        ### Problem-Solving Strategy:
        1. **Look at the position:** Is the missing digit in the ones, tens, hundreds place?
        2. **Work column by column:** Start from the ones place and work left
        3. **Consider carrying/borrowing:** Does this column need to carry or borrow?
        4. **Use logic:** What digit would make this equation work?
        
        ### Place Value Thinking:
        - **Ones place:** Units (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
        - **Tens place:** Groups of 10 (10, 20, 30, 40, 50, 60, 70, 80, 90)
        - **Hundreds place:** Groups of 100 (100, 200, 300, 400, 500, 600, 700, 800, 900)
        - **And so on...**
        
        ### Addition Tips:
        - **Look at the result:** What digit + other digit = result digit?
        - **Remember carrying:** If the sum is 10 or more, you carry 1 to the next column
        - **Check neighboring columns:** Did a carry affect this digit?
        
        ### Subtraction Tips:
        - **Look at the result:** What digit - other digit = result digit?
        - **Remember borrowing:** If you can't subtract, you borrow from the next column
        - **Check if borrowing occurred:** Was 10 added to this column?
        
        ### Examples:
        - **1⬜3 + 245 = 398** → Missing digit is 5 (153 + 245 = 398)
        - **567 - 2⬜4 = 283** → Missing digit is 8 (567 - 284 = 283)
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** Learn the basics
        - **🟠 4 digit numbers:** Build confidence  
        - **🔴 5-6 digit numbers:** Master level
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger and more challenging
        - ❌ **Wrong answer:** Numbers get smaller for more practice
        - 🎯 **Goal:** Master 6-digit missing digit problems!
        """)

def generate_new_question():
    """Generate a new missing digit problem"""
    digits = st.session_state.fill_missing_digit_difficulty["digits"]
    
    # Choose operation randomly
    operation = random.choice(["+", "-"])
    
    # Generate numbers with specified digits
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    top = random.randint(min_val, max_val)
    bottom = random.randint(min_val, max_val)
    
    # Make sure subtraction doesn't go negative
    if operation == "-" and bottom > top:
        top, bottom = bottom, top
    
    # Calculate result
    result = top + bottom if operation == "+" else top - bottom
    
    # Choose which digit to hide (from the top number)
    top_str = str(top).rjust(digits)
    missing_index = random.randint(0, digits - 1)
    
    # Create display version with missing digit
    top_display = list(top_str)
    correct_digit = top_display[missing_index]
    top_display[missing_index] = "⬜"
    
    st.session_state.problem_data = {
        "top": top,
        "bottom": bottom,
        "result": result,
        "operation": operation,
        "top_display": top_display,
        "correct_digit": correct_digit,
        "missing_index": missing_index,
        "digits": digits
    }
    
    st.session_state.correct_answer = correct_digit
    st.session_state.current_question = "Type the missing digit:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### 🔍 Find the missing digit:")
    
    # Create the vertical equation display with missing digit
    display_vertical_equation_with_missing_digit()
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**🤔 What digit goes in the empty box?**")
        
        # Input for the missing digit (only 0-9)
        user_answer = st.selectbox(
            "Choose the missing digit:",
            options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            index=0,
            key="missing_digit"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = str(user_answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_vertical_equation_with_missing_digit():
    """Display the equation in vertical format with one missing digit"""
    data = st.session_state.problem_data
    
    # Get the numbers as strings for formatting
    top_display = "".join(data["top_display"])
    bottom_str = str(data["bottom"]).rjust(data["digits"])
    result_str = str(data["result"]).rjust(data["digits"])
    
    # Create the display with highlighted missing digit
    equation_html = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #dc3545;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        line-height: 1.8;
        color: #2c3e50;
    ">
        <div style="margin-bottom: 10px; letter-spacing: 8px;">{top_display}</div>
        <div style="margin-bottom: 10px; letter-spacing: 8px;">{data['operation']} {bottom_str}</div>
        <div style="margin-bottom: 10px; border-top: 2px solid #333; padding-top: 10px; letter-spacing: 8px;">{result_str}</div>
    </div>
    """
    
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Add context about place values
    place_names = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
    if data["missing_index"] < len(place_names):
        place_name = place_names[data["digits"] - 1 - data["missing_index"]]
        st.markdown(f"<div style='text-align: center; color: #666; font-style: italic; margin-top: -15px;'>The missing digit is in the <strong>{place_name} place</strong></div>", unsafe_allow_html=True)

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
        st.success("🎉 **Excellent! That's the correct digit!**")
        
        # Increase difficulty (max 6 digits)
        old_difficulty = st.session_state.fill_missing_digit_difficulty["digits"]
        st.session_state.fill_missing_digit_difficulty["digits"] = min(
            st.session_state.fill_missing_digit_difficulty["digits"] + 1, 6
        )
        
        # Show encouragement based on difficulty
        if st.session_state.fill_missing_digit_difficulty["digits"] == 6 and old_difficulty < 6:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 6-digit missing digit problems!**")
        elif old_difficulty < st.session_state.fill_missing_digit_difficulty["digits"]:
            st.info(f"⬆️ **Great work! Now working with {st.session_state.fill_missing_digit_difficulty['digits']}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct digit was **{correct_answer}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.fill_missing_digit_difficulty["digits"]
        st.session_state.fill_missing_digit_difficulty["digits"] = max(
            st.session_state.fill_missing_digit_difficulty["digits"] - 1, 2
        )
        
        if old_difficulty > st.session_state.fill_missing_digit_difficulty["digits"]:
            st.warning(f"⬇️ **Let's practice with {st.session_state.fill_missing_digit_difficulty['digits']}-digit numbers for now**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.problem_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### 🧮 Step-by-step solution:")
        
        # Show the complete equation
        top_str = str(data["top"])
        bottom_str = str(data["bottom"])
        result_str = str(data["result"])
        operation = data["operation"]
        
        st.markdown(f"**Complete equation:** {top_str} {operation} {bottom_str} = {result_str}")
        
        # Explain place value
        place_names = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
        if data["missing_index"] < len(place_names):
            place_name = place_names[data["digits"] - 1 - data["missing_index"]]
            st.markdown(f"**Missing digit location:** {place_name} place")
        
        # Show the logic
        missing_pos = data["digits"] - 1 - data["missing_index"]
        place_value = 10**missing_pos
        
        st.markdown(f"**Place value:** {place_value:,}")
        st.markdown(f"**Correct digit:** {correct_answer}")
        st.markdown(f"**This represents:** {correct_answer} × {place_value:,} = {int(correct_answer) * place_value:,}")
        
        # Show column-by-column verification for simpler cases
        if data["digits"] <= 4:
            st.markdown("### 🔍 **Column-by-column check:**")
            
            # Break down by place value
            top_digits = [int(d) for d in str(data["top"]).rjust(data["digits"])]
            bottom_digits = [int(d) for d in str(data["bottom"]).rjust(data["digits"])]
            result_digits = [int(d) for d in str(data["result"]).rjust(data["digits"])]
            
            # Show the missing column
            col_index = data["missing_index"]
            top_digit = top_digits[col_index]
            bottom_digit = bottom_digits[col_index]
            result_digit = result_digits[col_index]
            
            if operation == "+":
                st.markdown(f"**In this column:** {top_digit} + {bottom_digit} = ?")
                if top_digit + bottom_digit >= 10:
                    st.markdown(f"**Calculation:** {top_digit} + {bottom_digit} = {top_digit + bottom_digit} (carries 1 to next column)")
                    st.markdown(f"**Result digit:** {(top_digit + bottom_digit) % 10}")
                else:
                    st.markdown(f"**Calculation:** {top_digit} + {bottom_digit} = {top_digit + bottom_digit}")
            else:
                st.markdown(f"**In this column:** {top_digit} - {bottom_digit} = {result_digit}")
        
        # Strategy tip
        st.markdown("### 💡 **Remember:**")
        st.markdown("- **Check place values:** Each position represents a different value")
        st.markdown("- **Work systematically:** Consider carrying (addition) or borrowing (subtraction)")
        st.markdown("- **Verify your answer:** Plug the digit back in to check if the equation works")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer