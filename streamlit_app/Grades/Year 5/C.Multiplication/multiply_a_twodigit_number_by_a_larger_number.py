import streamlit as st
import random

def run():
    """
    Main function to run the Multiply Two-Digit by Larger Number practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/D. Multiplication/multiply_two_digit_by_larger.py
    """
    # Initialize session state for difficulty and game state
    if "multiply_difficulty" not in st.session_state:
        st.session_state.multiply_difficulty = 1  # Start with level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > D. Multiplication**")
    st.title("🔢 Multiply Two-Digit by Larger Number")
    st.markdown("*Calculate the product of two numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiply_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Easy Start (2-digit × 2-digit)",
            2: "Building Up (2-digit × larger 2-digit)",
            3: "Standard Practice (2-digit × 3-digit)",
            4: "Getting Harder (larger numbers)",
            5: "Expert Challenge (complex multiplication)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
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
    with st.expander("💡 **Instructions & Multiplication Tips**", expanded=False):
        st.markdown("""
        ### How to Multiply Large Numbers:
        
        When multiplying a two-digit number by a larger number, you can use several strategies:
        
        #### Strategy 1: Traditional Algorithm
        Break the multiplication into partial products:
        
        **Example: 23 × 45**
        ```
            2 3
        ×   4 5
        -------
          1 1 5  ← 23 × 5
        + 9 2 0  ← 23 × 40
        -------
        1 0 3 5
        ```
        
        #### Strategy 2: Mental Math Tricks
        - **Break apart numbers:** 23 × 45 = 23 × (40 + 5) = (23 × 40) + (23 × 5)
        - **Use doubles:** If multiplying by even numbers, consider doubling
        - **Round and adjust:** 23 × 45 ≈ 25 × 45 = 1125, then subtract 2 × 45 = 90
        
        #### Strategy 3: Estimation First
        - **Round both numbers:** 23 × 45 ≈ 20 × 50 = 1000
        - **Check if your answer is reasonable**
        
        ### Tips for Success:
        - **Start with estimation** to check your final answer
        - **Work systematically** through the algorithm
        - **Double-check your calculation** by working backwards
        - **Practice your multiplication facts** for speed
        
        ### What to Expect:
        - **Level 1:** Simple 2-digit × 2-digit (12-50 × 11-25)
        - **Level 2:** Larger 2-digit numbers (25-99 × 25-50)
        - **Level 3:** 2-digit × 3-digit (15-99 × 100-199)
        - **Level 4:** More challenging combinations
        - **Level 5:** Expert level with large numbers
        
        ### Remember:
        - **Take your time** - accuracy is more important than speed
        - **Show your work** mentally by breaking down the steps
        - **Use estimation** to verify your answer makes sense
        """)

def generate_new_question():
    """Generate a new multiplication question based on difficulty"""
    difficulty = st.session_state.multiply_difficulty
    
    if difficulty == 1:
        # Level 1: Easy start (2-digit × 2-digit, smaller numbers)
        first_options = list(range(12, 51))
        second_options = list(range(11, 26))
        
    elif difficulty == 2:
        # Level 2: Building up (2-digit × larger 2-digit)
        first_options = list(range(25, 100))
        second_options = list(range(25, 51))
        
    elif difficulty == 3:
        # Level 3: Standard practice (2-digit × 3-digit)
        first_options = list(range(15, 100))
        second_options = list(range(100, 200))
        
    elif difficulty == 4:
        # Level 4: Getting harder
        first_options = list(range(35, 100))
        second_options = list(range(150, 300))
        
    else:  # Level 5
        # Level 5: Expert challenge
        first_options = list(range(45, 100))
        second_options = list(range(200, 500))
    
    # Generate the two numbers
    num1 = random.choice(first_options)
    num2 = random.choice(second_options)
    
    # Calculate the correct answer
    correct_answer = num1 * num2
    
    # Store question data
    st.session_state.question_data = {
        "num1": num1,
        "num2": num2,
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Multiply: {num1} × {num2}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question title
    st.markdown(f"### {st.session_state.current_question}")
    st.markdown("*Calculate the product and enter your answer below.*")
    
    # Create the visual multiplication layout
    create_multiplication_display(data)
    
    # Answer input
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Your Answer:")
        user_answer = st.number_input("", min_value=0, max_value=999999, value=None, 
                                    key="multiplication_answer", placeholder="Enter your answer",
                                    label_visibility="collapsed", help="Enter the product")
        st.session_state.user_answer = user_answer
    
    # Submit button
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("✅ Submit Answer", type="primary", use_container_width=True, key="submit_multiply"):
            # Validate input is provided
            if st.session_state.user_answer is None:
                st.error("Please enter your answer before submitting!")
                return
            
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_multiplication_display(data):
    """Create the visual multiplication problem display"""
    
    num1 = data["num1"]
    num2 = data["num2"]
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Display the multiplication problem in traditional format
        st.markdown(f"""
        <div style="text-align: center; font-family: monospace; font-size: 24px; line-height: 1.4; margin: 30px 0;">
            <div style="text-align: right; margin-bottom: 5px; width: 150px; margin-left: auto; margin-right: auto;">
                <span style="font-weight: bold;">{num1}</span>
            </div>
            <div style="text-align: right; margin-bottom: 15px; width: 150px; margin-left: auto; margin-right: auto;">
                <span style="margin-right: 15px;">×</span><span style="font-weight: bold;">{num2}</span>
            </div>
            <div style="border-bottom: 3px solid black; margin: 10px 0; width: 150px; margin-left: auto; margin-right: auto;"></div>
            <div style="margin-top: 20px; color: #666; font-size: 18px;">
                ?
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    num1 = st.session_state.question_data["num1"]
    num2 = st.session_state.question_data["num2"]
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete answer
        st.info(f"**{num1} × {num2} = {correct_answer}** ✓")
        
        # Track consecutive correct answers
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3 and st.session_state.multiply_difficulty < 5:
            old_difficulty = st.session_state.multiply_difficulty
            st.session_state.multiply_difficulty += 1
            st.session_state.consecutive_correct = 0
            
            if st.session_state.multiply_difficulty == 5:
                st.balloons()
                st.info("🏆 **Outstanding! You've reached Expert Level!**")
            else:
                st.info(f"⬆️ **Level Up! Now on Level {st.session_state.multiply_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**.")
        
        # Show what they entered vs correct
        st.markdown(f"**You entered:** {user_answer}")
        st.markdown(f"**Correct answer:** {num1} × {num2} = {correct_answer}")
        
        # Reset consecutive correct counter
        st.session_state.consecutive_correct = 0
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if wrong
        if st.session_state.multiply_difficulty > 1:
            st.session_state.multiply_difficulty -= 1
            st.warning(f"⬇️ **Moving to Level {st.session_state.multiply_difficulty} for more practice.**")

def show_explanation():
    """Show step-by-step explanation"""
    num1 = st.session_state.question_data["num1"]
    num2 = st.session_state.question_data["num2"]
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **See the solution method**", expanded=True):
        st.markdown(f"### How to solve {num1} × {num2}")
        
        # Show estimation first
        rounded_num1 = round(num1, -1)  # Round to nearest 10
        rounded_num2 = round(num2, -1)  # Round to nearest 10
        estimate = rounded_num1 * rounded_num2
        
        st.markdown(f"**Step 1: Estimate**")
        st.markdown(f"- Round {num1} to {rounded_num1}")
        st.markdown(f"- Round {num2} to {rounded_num2}")
        st.markdown(f"- Estimate: {rounded_num1} × {rounded_num2} = {estimate}")
        
        st.markdown(f"**Step 2: Calculate exactly**")
        
        # Show partial products if it's a reasonable size to break down
        if num2 < 100:
            # Two-digit second number
            tens_digit = num2 // 10
            ones_digit = num2 % 10
            
            if tens_digit > 0 and ones_digit > 0:
                partial1 = num1 * ones_digit
                partial2 = num1 * (tens_digit * 10)
                
                st.markdown(f"- {num1} × {ones_digit} = {partial1}")
                st.markdown(f"- {num1} × {tens_digit * 10} = {partial2}")
                st.markdown(f"- {partial1} + {partial2} = {correct_answer}")
            else:
                st.markdown(f"- {num1} × {num2} = {correct_answer}")
        else:
            # For larger numbers, just show the result
            st.markdown(f"- {num1} × {num2} = {correct_answer}")
        
        st.markdown(f"**Step 3: Check**")
        st.markdown(f"- Our estimate was {estimate}")
        st.markdown(f"- Our answer is {correct_answer}")
        if abs(correct_answer - estimate) / estimate < 0.3:  # Within 30%
            st.markdown(f"- ✅ This is close to our estimate, so it looks correct!")
        else:
            st.markdown(f"- The exact answer is quite different from the estimate")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = None
    
    # Clear input field value
    if "multiplication_answer" in st.session_state:
        del st.session_state["multiplication_answer"]