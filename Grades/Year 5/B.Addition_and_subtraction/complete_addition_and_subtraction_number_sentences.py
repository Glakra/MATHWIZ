import streamlit as st
import random

def run():
    """
    Main function to run the Complete Number Sentences practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/complete_addition_and_subtraction_sentences.py
    """
    # Initialize session state for difficulty and game state
    if "number_sentence_difficulty" not in st.session_state:
        st.session_state.number_sentence_difficulty = {"digits": 3}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("🔢 Complete Number Sentences")
    st.markdown("*Fill in the missing numbers in addition and subtraction problems*")
    st.markdown("---")
    
    # Difficulty indicator
    current_digits = st.session_state.number_sentence_difficulty["digits"]
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {current_digits}-digit numbers")
        # Progress bar (2 to 5 digits)
        progress = (current_digits - 2) / 3  # Convert 2-5 to 0-1
        st.progress(progress, text=f"{current_digits}-digit numbers")
    
    with col2:
        if current_digits <= 3:
            st.markdown("**🟡 Beginner**")
        elif current_digits == 4:
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
        - **Look at the vertical equation** shown below
        - **One number is missing** (either the top number or bottom number)
        - **Type the missing number** to complete the equation
        - **Check your work** by doing the math in your head or on paper
        
        ### Problem-Solving Strategy:
        1. **Identify the operation:** Is it addition (+) or subtraction (−)?
        2. **Look at what's missing:** Top number or bottom number?
        3. **Work backwards:** Use the result to find the missing number
        4. **Check your answer:** Does the completed equation make sense?
        
        ### Mathematical Thinking:
        - **For addition:** If ? + 45 = 123, then ? = 123 − 45
        - **For subtraction:** If ? − 45 = 78, then ? = 78 + 45
        - **For subtraction:** If 123 − ? = 78, then ? = 123 − 78
        
        ### Tips for Success:
        - **Estimate first:** Does your answer seem reasonable?
        - **Double-check:** Plug your answer back into the equation
        - **Practice mental math:** Try to solve some steps in your head
        - **Use place values:** Break larger numbers into parts if needed
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** Building foundation skills
        - **🟠 4 digit numbers:** Developing fluency
        - **🔴 5 digit numbers:** Mastery level
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger and more challenging
        - ❌ **Wrong answer:** Numbers get smaller for more practice
        - 🎯 **Goal:** Master 5-digit number sentences!
        """)

def generate_new_question():
    """Generate a new number sentence completion problem"""
    digits = st.session_state.number_sentence_difficulty["digits"]
    
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
    
    # Choose which number to hide
    missing = random.choice(["top", "bottom"])
    
    st.session_state.problem_data = {
        "top": top,
        "bottom": bottom,
        "result": result,
        "operation": operation,
        "missing": missing
    }
    
    st.session_state.correct_answer = str(top if missing == "top" else bottom)
    st.session_state.current_question = "Fill in the missing number to complete the equation:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### 🔢 Complete this equation:")
    
    # Create the vertical equation display
    display_vertical_equation()
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**🤔 What is the missing number?**")
        
        # Input for the missing number
        user_answer = st.number_input(
            f"Enter the missing {'top' if data['missing'] == 'top' else 'bottom'} number:",
            min_value=0,
            step=1,
            format="%d",
            key="missing_number"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = str(int(user_answer))
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_vertical_equation():
    """Display the equation in vertical format with proper alignment"""
    data = st.session_state.problem_data
    
    # Get the numbers as strings for formatting
    top_str = str(data["top"])
    bottom_str = str(data["bottom"])
    result_str = str(data["result"])
    
    # Find the maximum width needed for alignment
    max_width = max(len(top_str), len(bottom_str), len(result_str))
    
    # Right-align all numbers
    top_aligned = top_str.rjust(max_width)
    bottom_aligned = bottom_str.rjust(max_width)
    result_aligned = result_str.rjust(max_width)
    
    # Create the display with missing number replaced by question marks
    if data["missing"] == "top":
        top_display = "?" * len(top_str)
        top_display = top_display.rjust(max_width)
        bottom_display = bottom_aligned
    else:
        top_display = top_aligned
        bottom_display = "?" * len(bottom_str)
        bottom_display = bottom_display.rjust(max_width)
    
    # Create horizontal line
    line = "─" * max_width
    
    # Display the equation in a code block for monospace font
    equation_html = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #007bff;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        text-align: center;
        margin: 30px 0;
        line-height: 1.8;
        color: #2c3e50;
    ">
        <div style="margin-bottom: 10px;">{top_display}</div>
        <div style="margin-bottom: 10px;">{data['operation']} {bottom_display}</div>
        <div style="margin-bottom: 10px; border-top: 2px solid #333; padding-top: 10px;">{result_aligned}</div>
    </div>
    """
    
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Add a hint about which number is missing
    missing_hint = "top number" if data["missing"] == "top" else "bottom number"
    st.markdown(f"<div style='text-align: center; color: #666; font-style: italic; margin-top: -15px;'>Find the missing {missing_hint}</div>", unsafe_allow_html=True)

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
        
        # Increase difficulty (max 5 digits)
        old_difficulty = st.session_state.number_sentence_difficulty["digits"]
        st.session_state.number_sentence_difficulty["digits"] = min(
            st.session_state.number_sentence_difficulty["digits"] + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.number_sentence_difficulty["digits"] == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 5-digit number sentences!**")
        elif old_difficulty < st.session_state.number_sentence_difficulty["digits"]:
            st.info(f"⬆️ **Great progress! Now working with {st.session_state.number_sentence_difficulty['digits']}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.number_sentence_difficulty["digits"]
        st.session_state.number_sentence_difficulty["digits"] = max(
            st.session_state.number_sentence_difficulty["digits"] - 1, 2
        )
        
        if old_difficulty > st.session_state.number_sentence_difficulty["digits"]:
            st.warning(f"⬇️ **Let's practice with {st.session_state.number_sentence_difficulty['digits']}-digit numbers for now**")
        
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
        
        # Explain the logic
        if data["missing"] == "top":
            if operation == "+":
                st.markdown(f"**Logic:** If ? + {bottom_str} = {result_str}, then ? = {result_str} − {bottom_str}")
                st.markdown(f"**Calculation:** {result_str} − {bottom_str} = {correct_answer}")
            else:  # subtraction
                st.markdown(f"**Logic:** If ? − {bottom_str} = {result_str}, then ? = {result_str} + {bottom_str}")
                st.markdown(f"**Calculation:** {result_str} + {bottom_str} = {correct_answer}")
        else:  # missing bottom
            if operation == "+":
                st.markdown(f"**Logic:** If {top_str} + ? = {result_str}, then ? = {result_str} − {top_str}")
                st.markdown(f"**Calculation:** {result_str} − {top_str} = {correct_answer}")
            else:  # subtraction
                st.markdown(f"**Logic:** If {top_str} − ? = {result_str}, then ? = {top_str} − {result_str}")
                st.markdown(f"**Calculation:** {top_str} − {result_str} = {correct_answer}")
        
        # Verification
        st.markdown("### ✅ **Verification:**")
        verification = f"{top_str} {operation} {bottom_str} = {result_str}"
        st.markdown(f"**Check:** {verification} ✓")
        
        # Strategy tip
        st.markdown("### 💡 **Remember:**")
        if operation == "+":
            st.markdown("- **Addition problems:** Use subtraction to find the missing number")
            st.markdown("- **Think:** What do I add to get the result?")
        else:
            st.markdown("- **Subtraction problems:** Use addition or subtraction to find the missing number")
            st.markdown("- **Think:** What was the original amount, or what was taken away?")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer