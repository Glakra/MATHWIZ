import streamlit as st
import random

def run():
    """
    Main function to run the Complete Missing Steps multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/D. Multiplication/multiply_two_digit_by_larger_complete_missing_steps.py
    """
    # Initialize session state for difficulty and game state
    if "missing_steps_difficulty" not in st.session_state:
        st.session_state.missing_steps_difficulty = 1  # Start with level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.user_inputs = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > D. Multiplication**")
    st.title("🔢 Complete the Missing Steps")
    st.markdown("*Fill in the missing numbers in the multiplication algorithm*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.missing_steps_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Easy Start (×10s, ×20s)",
            2: "Building Up (×30s, ×40s)",
            3: "Standard Practice (×50s-×70s)",
            4: "Getting Harder (×80s-×99s)",
            5: "Expert Challenge (3-digit numbers)"
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
    with st.expander("💡 **Instructions & Multiplication Steps Guide**", expanded=False):
        st.markdown("""
        ### How Multi-Digit Multiplication Works:
        
        When multiplying a 2-digit number by a larger number, we break it into **partial products**:
        
        #### Example: 23 × 45
        
        **Step 1:** Set up the problem
        ```
            2 3
        ×   4 5
        -------
        ```
        
        **Step 2:** Multiply by the ones digit (5)
        - 3 × 5 = 15 (write 5, carry 1)
        - 2 × 5 = 10, plus carry 1 = 11 (write 11)
        - Result: 115
        
        **Step 3:** Multiply by the tens digit (4)
        - 3 × 4 = 12 (write 2, carry 1)  
        - 2 × 4 = 8, plus carry 1 = 9 (write 9)
        - Result: 920 (shifted one place left)
        
        **Step 4:** Add the partial products
        ```
            2 3
        ×   4 5
        -------
          1 1 5  ← 23 × 5
        + 9 2 0  ← 23 × 40
        -------
        1 0 3 5
        ```
        
        ### What You'll Practice:
        - **Fill in missing numbers** in each step
        - **Understand carrying** in multiplication
        - **Add partial products** correctly
        - **See the complete algorithm** in action
        
        ### Tips for Success:
        - **Work systematically** - complete one step at a time
        - **Remember to carry** when products are ≥ 10
        - **Check your work** by estimating the final answer
        - **Line up place values** correctly when adding
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Easy start (×10s, ×20s)
        - **🟡 Level 2:** Building up (×30s, ×40s)
        - **🟠 Level 3:** Standard practice (×50s-×70s)
        - **🔴 Level 4:** Getting harder (×80s-×99s)
        - **🔴 Level 5:** Expert challenge (3-digit numbers)
        """)

def generate_new_question():
    """Generate a new missing steps multiplication question based on difficulty"""
    difficulty = st.session_state.missing_steps_difficulty
    
    if difficulty == 1:
        # Level 1: Easy start (×10s, ×20s)
        first_options = list(range(12, 50))
        second_options = [10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25]
        
    elif difficulty == 2:
        # Level 2: Building up (×30s, ×40s)
        first_options = list(range(15, 60))
        second_options = list(range(30, 50))
        
    elif difficulty == 3:
        # Level 3: Standard practice
        first_options = list(range(20, 80))
        second_options = list(range(50, 80))
        
    elif difficulty == 4:
        # Level 4: Getting harder
        first_options = list(range(25, 99))
        second_options = list(range(80, 100))
        
    else:  # Level 5
        # Level 5: Expert challenge (3-digit multiplier)
        first_options = list(range(30, 99))
        second_options = list(range(100, 150))
    
    # Generate the two numbers
    num1 = random.choice(first_options)
    num2 = random.choice(second_options)
    
    # Calculate the full multiplication breakdown
    multiplication_data = calculate_multiplication_steps(num1, num2)
    
    # Generate missing positions (randomly select which numbers to hide)
    missing_positions = generate_missing_positions(multiplication_data, difficulty)
    
    # Store question data
    st.session_state.question_data = {
        "num1": num1,
        "num2": num2,
        "multiplication_data": multiplication_data,
        "missing_positions": missing_positions
    }
    
    # Store correct answers for missing positions
    st.session_state.correct_answers = {}
    for pos in missing_positions:
        st.session_state.correct_answers[pos] = multiplication_data[pos]
    
    st.session_state.current_question = f"Fill in the missing numbers in the multiplication steps"

def calculate_multiplication_steps(num1, num2):
    """Calculate all the steps in the multiplication algorithm"""
    # Convert numbers to digit lists
    num1_str = str(num1)
    num2_str = str(num2)
    
    # Get individual digits
    if len(num2_str) == 2:
        # Two-digit multiplier
        ones_digit = int(num2_str[-1])
        tens_digit = int(num2_str[-2])
        
        # Calculate partial products
        partial1 = num1 * ones_digit
        partial2 = num1 * tens_digit * 10  # Shifted for tens place
        
        final_result = partial1 + partial2
        
        return {
            "num1": num1,
            "num2": num2,
            "ones_digit": ones_digit,
            "tens_digit": tens_digit,
            "partial1": partial1,
            "partial2": partial2,
            "final_result": final_result,
            "multiplier_type": "two_digit"
        }
    
    else:
        # Three-digit multiplier (Level 5)
        ones_digit = int(num2_str[-1])
        tens_digit = int(num2_str[-2])
        hundreds_digit = int(num2_str[-3])
        
        # Calculate partial products
        partial1 = num1 * ones_digit
        partial2 = num1 * tens_digit * 10
        partial3 = num1 * hundreds_digit * 100
        
        final_result = partial1 + partial2 + partial3
        
        return {
            "num1": num1,
            "num2": num2,
            "ones_digit": ones_digit,
            "tens_digit": tens_digit,
            "hundreds_digit": hundreds_digit,
            "partial1": partial1,
            "partial2": partial2,
            "partial3": partial3,
            "final_result": final_result,
            "multiplier_type": "three_digit"
        }

def generate_missing_positions(multiplication_data, difficulty):
    """Generate which positions should be missing based on difficulty"""
    all_positions = []
    
    if multiplication_data["multiplier_type"] == "two_digit":
        all_positions = ["partial1", "partial2", "final_result"]
    else:
        all_positions = ["partial1", "partial2", "partial3", "final_result"]
    
    # Determine how many to hide based on difficulty
    if difficulty <= 2:
        num_missing = min(2, len(all_positions) - 1)  # Hide 1-2 numbers
    elif difficulty <= 3:
        num_missing = min(3, len(all_positions))      # Hide 2-3 numbers
    else:
        num_missing = len(all_positions)              # Hide most numbers
    
    # Randomly select positions to hide
    missing_positions = random.sample(all_positions, num_missing)
    
    return missing_positions

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    multiplication_data = data["multiplication_data"]
    missing_positions = data["missing_positions"]
    
    # Display question title
    st.markdown(f"### {st.session_state.current_question}")
    st.markdown("*Look at the multiplication algorithm below and fill in the missing numbers.*")
    
    # Create the visual multiplication layout
    create_multiplication_visual(multiplication_data, missing_positions)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True, key="submit_missing_steps"):
            # Validate all inputs are provided
            user_inputs = st.session_state.get('user_inputs', {})
            
            # Check if all missing positions have inputs
            missing_inputs = [pos for pos in missing_positions if user_inputs.get(pos) is None]
            
            if missing_inputs:
                st.error("Please fill in all missing numbers before submitting!")
                return
            
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_multiplication_visual(multiplication_data, missing_positions):
    """Create the visual multiplication algorithm with input boxes"""
    
    # Create the multiplication layout
    st.markdown("### 🔢 Multiplication Steps:")
    
    # Main multiplication setup
    num1 = multiplication_data["num1"]
    num2 = multiplication_data["num2"]
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display the multiplication problem setup with proper traditional alignment
        st.markdown(f"""
        <div style="text-align: center; font-family: monospace; font-size: 20px; line-height: 1.4;">
            <div style="text-align: right; margin-bottom: 5px; width: 120px; margin-left: auto; margin-right: auto;">
                <span style="font-weight: bold;">{num1}</span>
            </div>
            <div style="text-align: right; margin-bottom: 15px; width: 120px; margin-left: auto; margin-right: auto;">
                <span style="margin-right: 15px;">×</span><span style="font-weight: bold;">{num2}</span>
            </div>
            <div style="border-bottom: 2px solid black; margin: 10px 0; width: 120px; margin-left: auto; margin-right: auto;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create input fields for partial products
        if multiplication_data["multiplier_type"] == "two_digit":
            create_two_digit_inputs(multiplication_data, missing_positions)
        else:
            create_three_digit_inputs(multiplication_data, missing_positions)

def create_two_digit_inputs(multiplication_data, missing_positions):
    """Create input layout for two-digit multiplier"""
    
    # Extract data
    ones_digit = multiplication_data["ones_digit"]
    tens_digit = multiplication_data["tens_digit"]
    partial1 = multiplication_data["partial1"]
    partial2 = multiplication_data["partial2"]
    final_result = multiplication_data["final_result"]
    
    # Create single column context for proper sequencing
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # First partial product
        if "partial1" in missing_positions:
            partial1_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                           key="partial1_input", placeholder="?",
                                           label_visibility="collapsed", help="First partial product")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["partial1"] = partial1_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 18px; font-weight: bold; margin: 10px 0;'>{partial1}</div>", 
                       unsafe_allow_html=True)
        
        # Second partial product - always show + sign
        if "partial2" in missing_positions:
            partial2_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                           key="partial2_input", placeholder="?",
                                           label_visibility="collapsed", help="Second partial product")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["partial2"] = partial2_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 18px; font-weight: bold; margin: 10px 0;'>+ {partial2}</div>", 
                       unsafe_allow_html=True)
        
        # Line separator - within the column context, before final result
        st.markdown("""
        <div style="border-bottom: 2px solid black; margin: 15px auto; width: 120px;"></div>
        """, unsafe_allow_html=True)
        
        # Final result - after the line separator
        if "final_result" in missing_positions:
            final_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                        key="final_input", placeholder="?",
                                        label_visibility="collapsed", help="Final answer")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["final_result"] = final_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 20px; font-weight: bold; color: #2E7D32; margin: 10px 0;'>{final_result}</div>", 
                       unsafe_allow_html=True)

def create_three_digit_inputs(multiplication_data, missing_positions):
    """Create input layout for three-digit multiplier"""
    
    # Extract data
    ones_digit = multiplication_data["ones_digit"]
    tens_digit = multiplication_data["tens_digit"]
    hundreds_digit = multiplication_data["hundreds_digit"]
    partial1 = multiplication_data["partial1"]
    partial2 = multiplication_data["partial2"]
    partial3 = multiplication_data["partial3"]
    final_result = multiplication_data["final_result"]
    
    # Create single column context for proper sequencing
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # First partial product
        if "partial1" in missing_positions:
            partial1_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                           key="partial1_input", placeholder="?",
                                           label_visibility="collapsed")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["partial1"] = partial1_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 18px; font-weight: bold; margin: 10px 0;'>{partial1}</div>", 
                       unsafe_allow_html=True)
        
        # Second partial product
        if "partial2" in missing_positions:
            partial2_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                           key="partial2_input", placeholder="?",
                                           label_visibility="collapsed")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["partial2"] = partial2_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 18px; font-weight: bold; margin: 10px 0;'>+ {partial2}</div>", 
                       unsafe_allow_html=True)
        
        # Third partial product
        if "partial3" in missing_positions:
            partial3_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                           key="partial3_input", placeholder="?",
                                           label_visibility="collapsed")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["partial3"] = partial3_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 18px; font-weight: bold; margin: 10px 0;'>+ {partial3}</div>", 
                       unsafe_allow_html=True)
        
        # Line separator - within the column context, before final result
        st.markdown("""
        <div style="border-bottom: 2px solid black; margin: 15px auto; width: 120px;"></div>
        """, unsafe_allow_html=True)
        
        # Final result - after the line separator
        if "final_result" in missing_positions:
            final_input = st.number_input("", min_value=0, max_value=99999, value=None, 
                                        key="final_input", placeholder="?",
                                        label_visibility="collapsed")
            st.session_state.user_inputs = st.session_state.get('user_inputs', {})
            st.session_state.user_inputs["final_result"] = final_input
        else:
            st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 20px; font-weight: bold; color: #2E7D32; margin: 10px 0;'>{final_result}</div>", 
                       unsafe_allow_html=True)

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
    """Display feedback for the submitted answers"""
    user_inputs = st.session_state.get('user_inputs', {})
    correct_answers = st.session_state.correct_answers
    missing_positions = st.session_state.question_data["missing_positions"]
    
    # Check each missing position
    all_correct = True
    feedback_data = {}
    
    for pos in missing_positions:
        user_answer = user_inputs.get(pos)
        correct_answer = correct_answers[pos]
        
        is_correct = user_answer == correct_answer
        feedback_data[pos] = {
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        }
        
        if not is_correct:
            all_correct = False
    
    # Display feedback for each position
    cols = st.columns(len(missing_positions))
    for i, pos in enumerate(missing_positions):
        with cols[i]:
            feedback = feedback_data[pos]
            if feedback["is_correct"]:
                st.success(f"✅ {pos.replace('_', ' ').title()}: {feedback['correct_answer']}")
            else:
                st.error(f"❌ {pos.replace('_', ' ').title()}: {feedback['correct_answer']} (you put {feedback['user_answer']})")
    
    # Overall feedback
    if all_correct:
        st.success("🎉 **Perfect! You completed all the missing steps correctly!**")
        
        # Track consecutive correct answers
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3 and st.session_state.missing_steps_difficulty < 5:
            old_difficulty = st.session_state.missing_steps_difficulty
            st.session_state.missing_steps_difficulty += 1
            st.session_state.consecutive_correct = 0
            
            if st.session_state.missing_steps_difficulty == 5:
                st.balloons()
                st.info("🏆 **Outstanding! You've reached Expert Level!**")
            else:
                st.info(f"⬆️ **Level Up! Now on Level {st.session_state.missing_steps_difficulty}**")
    
    else:
        # Reset consecutive correct counter
        st.session_state.consecutive_correct = 0
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if multiple wrong
        wrong_count = sum([not feedback["is_correct"] for feedback in feedback_data.values()])
        if wrong_count >= 2 and st.session_state.missing_steps_difficulty > 1:
            st.session_state.missing_steps_difficulty -= 1
            st.warning(f"⬇️ **Moving to Level {st.session_state.missing_steps_difficulty} for more practice.**")

def show_explanation():
    """Show step-by-step explanation"""
    multiplication_data = st.session_state.question_data["multiplication_data"]
    
    with st.expander("📖 **Step-by-step solution**", expanded=True):
        num1 = multiplication_data["num1"]
        num2 = multiplication_data["num2"]
        
        st.markdown(f"### Complete Solution for {num1} × {num2}")
        
        if multiplication_data["multiplier_type"] == "two_digit":
            ones_digit = multiplication_data["ones_digit"]
            tens_digit = multiplication_data["tens_digit"]
            partial1 = multiplication_data["partial1"]
            partial2 = multiplication_data["partial2"]
            final_result = multiplication_data["final_result"]
            
            st.markdown("#### Step-by-step breakdown:")
            st.markdown(f"1. **{num1} × {ones_digit} = {partial1}** (multiply by ones digit)")
            st.markdown(f"2. **{num1} × {tens_digit}0 = {partial2}** (multiply by tens digit, shifted)")
            st.markdown(f"3. **{partial1} + {partial2} = {final_result}** (add partial products)")
            
        else:
            ones_digit = multiplication_data["ones_digit"]
            tens_digit = multiplication_data["tens_digit"]
            hundreds_digit = multiplication_data["hundreds_digit"]
            partial1 = multiplication_data["partial1"]
            partial2 = multiplication_data["partial2"]
            partial3 = multiplication_data["partial3"]
            final_result = multiplication_data["final_result"]
            
            st.markdown("#### Step-by-step breakdown:")
            st.markdown(f"1. **{num1} × {ones_digit} = {partial1}** (multiply by ones digit)")
            st.markdown(f"2. **{num1} × {tens_digit}0 = {partial2}** (multiply by tens digit)")
            st.markdown(f"3. **{num1} × {hundreds_digit}00 = {partial3}** (multiply by hundreds digit)")
            st.markdown(f"4. **{partial1} + {partial2} + {partial3} = {final_result}** (add all partial products)")
        
        st.markdown(f"**Final Answer:** {num1} × {num2} = {final_result} ✓")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_inputs = {}
    
    # Clear input field values
    input_keys = ["partial1_input", "partial2_input", "partial3_input", "final_input"]
    for key in input_keys:
        if key in st.session_state:
            del st.session_state[key]