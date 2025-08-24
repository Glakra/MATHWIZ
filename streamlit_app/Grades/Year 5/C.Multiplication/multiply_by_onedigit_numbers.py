import streamlit as st
import random

def run():
    """
    Main function to run the Multiply by One-Digit Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_by_onedigit_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "onedigit_mult_difficulty" not in st.session_state:
        st.session_state.onedigit_mult_difficulty = 2  # Start with 2-digit numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("✖️ Multiply by One-Digit Numbers")
    st.markdown("*Practice the standard multiplication algorithm*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.onedigit_mult_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (2 to 4 digits)
        progress = (difficulty_level - 2) / 2  # Convert 2-4 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level == 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 3:
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
        ### How to Multiply by One-Digit Numbers:
        - **Line up** the numbers properly (ones under ones, tens under tens)
        - **Start from the right** (ones place) and work left
        - **Multiply each digit** by the one-digit number
        - **Carry over** when needed (write small numbers above)
        - **Add up** all the partial products
        
        ### Example: 234 × 6
        ```
            2 3 4
        ×       6
        -------
          1,404
        ```
        
        **Step by step:**
        1. **6 × 4 = 24** → Write 4, carry 2
        2. **6 × 3 = 18** → 18 + 2 = 20 → Write 0, carry 2  
        3. **6 × 2 = 12** → 12 + 2 = 14 → Write 14
        4. **Result: 1,404**
        
        ### Tips for Success:
        - **Remember your times tables** (1-9)
        - **Carry carefully** - write small numbers above
        - **Check your work** by estimating
        - **Line up digits** in the correct place values
        - **Practice regrouping** (carrying over)
        
        ### Difficulty Levels:
        - **🟡 2-digit × 1-digit:** (23 × 4)
        - **🟠 3-digit × 1-digit:** (234 × 6)  
        - **🔴 4-digit × 1-digit:** (2345 × 7)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder problems
        - ❌ **Wrong answer:** Practice more at this level
        - 🎯 **Goal:** Master 4-digit multiplication!
        """)

def generate_new_question():
    """Generate a new one-digit multiplication question"""
    digits = st.session_state.onedigit_mult_difficulty
    
    # Generate multi-digit number and single digit multiplier
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    # Ensure interesting numbers (not too many zeros, some carrying required)
    multi_digit = random.randint(min_val, max_val)
    while str(multi_digit).count('0') > 1:  # Avoid too many zeros
        multi_digit = random.randint(min_val, max_val)
    
    single_digit = random.randint(2, 9)  # Avoid 0 and 1 for more interesting problems
    
    # Calculate the answer
    correct_answer = multi_digit * single_digit
    
    # Create question data
    st.session_state.question_data = {
        "multi_digit": multi_digit,
        "single_digit": single_digit,
        "correct_answer": correct_answer,
        "num_digits_answer": len(str(correct_answer))
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Multiply."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### ✖️ Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Create form for the answer
    with st.form("multiplication_form"):
        # Create the multiplication layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Display the multiplication problem in vertical format
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 30px; 
                border-radius: 15px; 
                border: 2px solid #dee2e6;
                font-family: 'Courier New', monospace;
                font-size: 28px;
                text-align: right;
                margin: 20px 0;
                line-height: 1.8;
            ">
                <div style="margin-bottom: 15px; padding-right: 30px;">
                    {data['multi_digit']:,}
                </div>
                <div style="margin-bottom: 15px; padding-right: 30px;">
                    ×&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data['single_digit']}
                </div>
                <div style="border-bottom: 3px solid #000; margin: 10px 0;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Enter your answer:**")
            
            # Create input field for the answer
            st.markdown("""
            <style>
            .answer-container {
                background-color: #ffffff;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                padding: 25px;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="answer-container">', unsafe_allow_html=True)
            
            # Single input field for the complete answer
            answer_cols = st.columns([1, 3, 1])
            with answer_cols[1]:
                user_answer = st.number_input(
                    "Answer:",
                    min_value=0,
                    step=1,
                    key="final_answer",
                    label_visibility="collapsed",
                    help=f"What is {data['multi_digit']:,} × {data['single_digit']}?",
                    placeholder="Enter your answer"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
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
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's the correct answer!**")
        
        # Increase difficulty (max 4 digits)
        old_difficulty = st.session_state.onedigit_mult_difficulty
        st.session_state.onedigit_mult_difficulty = min(
            st.session_state.onedigit_mult_difficulty + 1, 4
        )
        
        if st.session_state.onedigit_mult_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 4-digit multiplication!**")
        elif old_difficulty < st.session_state.onedigit_mult_difficulty:
            st.info(f"⬆️ **Great work! Moving up to {st.session_state.onedigit_mult_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.onedigit_mult_difficulty
        st.session_state.onedigit_mult_difficulty = max(
            st.session_state.onedigit_mult_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.onedigit_mult_difficulty:
            st.warning(f"⬇️ **Let's practice more with {st.session_state.onedigit_mult_difficulty}-digit numbers**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    data = st.session_state.question_data
    multi_digit = data['multi_digit']
    single_digit = data['single_digit']
    correct_answer = data['correct_answer']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution for {multi_digit:,} × {single_digit}:
        """)
        
        # Break down the multiplication process
        multi_str = str(multi_digit)
        steps = []
        carry = 0
        result_digits = []
        
        # Work from right to left
        for i in range(len(multi_str) - 1, -1, -1):
            digit = int(multi_str[i])
            product = digit * single_digit + carry
            
            if product >= 10:
                result_digit = product % 10
                carry = product // 10
                steps.append(f"**Step {len(steps) + 1}:** {single_digit} × {digit} = {digit * single_digit}, plus carry {carry if len(steps) > 0 else 0} = {product} → Write {result_digit}, carry {carry}")
            else:
                result_digit = product
                carry = 0
                steps.append(f"**Step {len(steps) + 1}:** {single_digit} × {digit} = {product} → Write {result_digit}")
            
            result_digits.insert(0, str(result_digit))
        
        if carry > 0:
            result_digits.insert(0, str(carry))
            steps.append(f"**Final step:** Write the final carry {carry}")
        
        for step in steps:
            st.markdown(step)
        
        st.markdown(f"""
        ### Visual breakdown:
        ```
            {multi_digit:,}
        ×       {single_digit}
        -------
          {correct_answer:,}
        ```
        
        **Final Answer: {multi_digit:,} × {single_digit} = {correct_answer:,}**
        """)
        
        # Add a tip about estimation
        estimated = round_to_nearest_hundred(multi_digit) * single_digit
        st.markdown(f"""
        💡 **Estimation check:** 
        {multi_digit:,} is about {round_to_nearest_hundred(multi_digit):,}, so {round_to_nearest_hundred(multi_digit):,} × {single_digit} ≈ {estimated:,}
        Our answer of {correct_answer:,} is close to this estimate! ✓
        """)

def round_to_nearest_hundred(n):
    """Round number to nearest hundred for estimation"""
    if n < 100:
        return round(n, -1)  # Round to nearest 10
    else:
        return round(n, -2)  # Round to nearest 100

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""