import streamlit as st
import random

def run():
    """
    Main function to run the Subtract Fractions with Like Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/subtract_fractions_with_like_denominators.py
    """
    # Initialize session state for difficulty and game state
    if "subtract_fractions_difficulty" not in st.session_state:
        st.session_state.subtract_fractions_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions with Like Denominators")
    st.markdown("*Subtract fractions that have the same denominator*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.subtract_fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (denominators 2-4)",
            2: "Simple (denominators 4-6)",
            3: "Medium (denominators 6-8)",
            4: "Advanced (denominators 8-10)",
            5: "Expert (denominators 10-12)"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
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
        ### How to Subtract Fractions with Like Denominators:
        
        **Rule:** When fractions have the same denominator, just subtract the numerators!
        
        ### Example:
        5/8 - 2/8 = ?
        - The denominators are the same (8)
        - Subtract the numerators: 5 - 2 = 3
        - Keep the denominator: 8
        - Answer: 3/8
        
        ### Steps:
        1. Check that denominators are the same ✓
        2. Subtract the top numbers (numerators)
        3. Keep the bottom number (denominator) the same
        4. Simplify if needed
        
        ### Remember:
        - **Same denominator = Easy!**
        - Only subtract the top numbers
        - The bottom stays the same
        - Make sure the first fraction is bigger!
        - If you get 0, that's okay - it means nothing is left
        """)

def generate_new_question():
    """Generate a new fraction subtraction question"""
    difficulty = st.session_state.subtract_fractions_difficulty
    
    # Set denominator range based on difficulty
    if difficulty == 1:
        denominator = random.choice([2, 3, 4])
    elif difficulty == 2:
        denominator = random.choice([4, 5, 6])
    elif difficulty == 3:
        denominator = random.choice([6, 7, 8])
    elif difficulty == 4:
        denominator = random.choice([8, 9, 10])
    else:  # difficulty == 5
        denominator = random.choice([10, 11, 12])
    
    # Generate numerators (ensure first > second for positive result)
    # For lower difficulties, keep it simple
    if difficulty <= 2:
        # First numerator should be at least 2 to allow subtraction
        numerator1 = random.randint(2, denominator - 1)
        # Second numerator should be less than first
        numerator2 = random.randint(1, numerator1 - 1)
    else:
        # For higher difficulties, allow more variety
        numerator1 = random.randint(2, denominator - 1)
        numerator2 = random.randint(1, numerator1 - 1)
    
    # Calculate the difference
    diff_numerator = numerator1 - numerator2
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "diff_numerator": diff_numerator
    }
    
    st.session_state.correct_answer = diff_numerator
    st.session_state.current_question = "Subtract."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display "Subtract." instruction
    st.markdown("### Subtract.")
    
    # Create the fraction subtraction display
    st.markdown("")
    
    # Use columns for the equation
    col1, col2, col3, col4, col5 = st.columns([1.5, 0.5, 1.5, 0.5, 2])
    
    with col1:
        # First fraction with visual representation
        fraction_html = f"""
        <div style="text-align: center; font-size: 48px; line-height: 1;">
            <div style="border-bottom: 3px solid black; padding: 5px;">{data['numerator1']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 30px;">
            −
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction with visual representation
        fraction_html = f"""
        <div style="text-align: center; font-size: 48px; line-height: 1;">
            <div style="border-bottom: 3px solid black; padding: 5px;">{data['numerator2']}</div>
            <div style="padding: 5px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 48px; padding-top: 30px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Answer input area
        st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
        with st.form("answer_form", clear_on_submit=False):
            user_input = st.text_input(
                "",
                key="fraction_answer",
                placeholder=f"?/{data['denominator']}",
                label_visibility="collapsed"
            )
            
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit and user_input.strip():
                # Parse the answer
                if '/' in user_input:
                    try:
                        parts = user_input.split('/')
                        user_num = int(parts[0])
                        user_denom = int(parts[1])
                        
                        # Check if denominator is correct
                        if user_denom != data['denominator']:
                            st.error(f"The denominator should be {data['denominator']}")
                        else:
                            st.session_state.user_answer = user_num
                            st.session_state.answer_submitted = True
                            st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid fraction (e.g., 3/8)")
                else:
                    try:
                        # If they just entered the numerator
                        user_num = int(user_input)
                        st.session_state.user_answer = user_num
                        st.session_state.answer_submitted = True
                        st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid number")
            elif submit:
                st.error("Please enter your answer")
    
    # Show feedback
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.question_data
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Well done!**")
        
        # Show the complete equation
        fraction1 = f"{data['numerator1']}/{data['denominator']}"
        fraction2 = f"{data['numerator2']}/{data['denominator']}"
        result = f"{correct_answer}/{data['denominator']}"
        
        st.success(f"✓ {fraction1} − {fraction2} = {result}")
        
        # Check for special cases
        if correct_answer == 0:
            st.info("💡 **Note:** When you subtract all the parts, you get 0! Nothing is left.")
        elif correct_answer == 1 and data['denominator'] > 1:
            st.info(f"💡 **Note:** {result} can be simplified to 1/{data['denominator']}")
        
        # Check if the result can be simplified
        from math import gcd
        if correct_answer > 0:
            common_divisor = gcd(correct_answer, data['denominator'])
            if common_divisor > 1:
                simplified_num = correct_answer // common_divisor
                simplified_denom = data['denominator'] // common_divisor
                if simplified_denom == 1:
                    st.info(f"💡 **Note:** {result} can be simplified to {simplified_num}")
                else:
                    st.info(f"💡 **Note:** {result} can be simplified to {simplified_num}/{simplified_denom}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.subtract_fractions_difficulty
        st.session_state.subtract_fractions_difficulty = min(
            st.session_state.subtract_fractions_difficulty + 1, 5
        )
        
        if st.session_state.subtract_fractions_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've reached the highest level!**")
        elif old_difficulty < st.session_state.subtract_fractions_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.subtract_fractions_difficulty}**")
    
    else:
        st.error("❌ **Not quite right. Try again!**")
        
        # Show what they entered
        user_fraction = f"{user_answer}/{data['denominator']}"
        st.error(f"You answered: {user_fraction}")
        
        # Show the correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.subtract_fractions_difficulty
        st.session_state.subtract_fractions_difficulty = max(
            st.session_state.subtract_fractions_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.subtract_fractions_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.subtract_fractions_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for subtracting fractions"""
    data = st.session_state.question_data
    
    with st.expander("📖 **How to Subtract Fractions with Like Denominators**", expanded=True):
        st.markdown(f"""
        ### Your Problem:
        **{data['numerator1']}/{data['denominator']} − {data['numerator2']}/{data['denominator']} = ?**
        
        ### Solution Steps:
        
        **Step 1: Check the denominators**
        - First fraction: {data['denominator']} ✓
        - Second fraction: {data['denominator']} ✓
        - They're the same! This makes it easy.
        
        **Step 2: Subtract the numerators**
        - {data['numerator1']} − {data['numerator2']} = {data['diff_numerator']}
        
        **Step 3: Keep the same denominator**
        - The denominator stays {data['denominator']}
        
        **Answer: {data['diff_numerator']}/{data['denominator']}**
        
        ### Visual Example:
        Think of it like this:
        - You have {data['numerator1']} pieces of a pizza cut into {data['denominator']} slices
        - You eat (or give away) {data['numerator2']} pieces
        - You have {data['diff_numerator']} pieces left out of {data['denominator']}
        
        ### Remember the Rule:
        **Same denominator → Subtract only the numerators!**
        
        ### Important:
        - The first fraction must be bigger than or equal to the second
        - If they're equal, the answer is 0
        - The denominator NEVER changes when subtracting
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer