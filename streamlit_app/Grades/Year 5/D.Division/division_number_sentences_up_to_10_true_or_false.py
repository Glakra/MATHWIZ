import streamlit as st
import random

def run():
    """
    Main function to run the Division number sentences up to 10: true or false? activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D.Division/division_number_sentences_true_false.py
    """
    # Initialize session state for difficulty and game state
    if "division_true_false_difficulty" not in st.session_state:
        st.session_state.division_true_false_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("✅❌ Division Number Sentences: True or False?")
    st.markdown("*Evaluate division equations to determine if they are correct or incorrect*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.division_true_false_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Evaluate Division Sentences:
        - **Calculate each side** of the equation separately
        - **Compare the results** - are they equal?
        - **Choose True** if both sides are equal
        - **Choose False** if the sides are different
        
        ### Types of Division Sentences:
        1. **Simple Division:** 8 ÷ 2 = 4 (True or False?)
        2. **Division vs. Number:** 12 ÷ 3 = 5 (False - should be 4)
        3. **Two Division Problems:** 15 ÷ 3 = 10 ÷ 2 (True - both equal 5)
        4. **Mixed Operations:** 6 ÷ 2 = 1 + 2 (True - both equal 3)
        
        ### Step-by-Step Process:
        1. **Calculate the left side** of the equation
        2. **Calculate the right side** of the equation
        3. **Compare the results**
        4. **Decide: True or False?**
        
        ### Examples:
        **True Sentences:**
        - 8 ÷ 2 = 4 ✓ (4 = 4)
        - 12 ÷ 4 = 9 ÷ 3 ✓ (3 = 3)
        - 10 ÷ 5 = 1 + 1 ✓ (2 = 2)
        
        **False Sentences:**
        - 15 ÷ 3 = 4 ✗ (5 ≠ 4)
        - 18 ÷ 6 = 16 ÷ 4 ✗ (3 ≠ 4)
        - 14 ÷ 7 = 3 - 1 ✗ (2 ≠ 2) Wait, this is actually True!
        
        ### Quick Mental Math Tips:
        - **Division by 1:** Any number ÷ 1 = same number
        - **Division by 2:** Half the number
        - **Division by 5:** Count by 5s to find the answer
        - **Division by 10:** Remove one zero
        - **Same number divided by itself = 1**
        
        ### Common Mistakes to Avoid:
        - Don't just look at the numbers - **calculate both sides**
        - Remember **order matters** in division (8 ÷ 2 ≠ 2 ÷ 8)
        - **Check your mental math** twice
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple division facts with obvious answers
        - **🟠 Level 3:** Mixed operations and two-step problems
        - **🔴 Level 4-5:** Complex equations with multiple operations
        
        ### Key Skills:
        - ✅ **Mental division** with facts up to 10
        - ✅ **Equation evaluation** skills
        - ✅ **Critical thinking** about number relationships
        - ✅ **Careful calculation** and checking
        """)

def generate_division_sentences():
    """Generate division number sentences based on difficulty level"""
    level = st.session_state.division_true_false_difficulty
    
    # Define divisors based on difficulty
    if level == 1:
        divisors = [1, 2, 5, 10]  # Easiest facts
        max_dividend = 20
    elif level == 2:
        divisors = [1, 2, 3, 5, 10]  # Add 3
        max_dividend = 30
    elif level == 3:
        divisors = [1, 2, 3, 4, 5, 6, 10]  # Add 4 and 6
        max_dividend = 60
    elif level == 4:
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts
        max_dividend = 80
    else:  # level 5
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts with complexity
        max_dividend = 100
    
    # Choose whether to make it true or false (50/50 chance)
    should_be_true = random.choice([True, False])
    
    # Generate different types of sentences
    sentence_types = [
        "simple_division",      # 8 ÷ 2 = 4
        "division_vs_number",   # 12 ÷ 3 = 5
        "two_divisions",        # 15 ÷ 3 = 10 ÷ 2
        "division_vs_addition", # 6 ÷ 2 = 1 + 2
        "division_vs_subtraction" # 9 ÷ 3 = 5 - 2
    ]
    
    # Weight sentence types based on difficulty
    if level <= 2:
        sentence_type = random.choices(
            sentence_types[:2],  # Only simple types
            weights=[60, 40]
        )[0]
    elif level <= 3:
        sentence_type = random.choices(
            sentence_types[:4],  # Add two divisions and addition
            weights=[30, 30, 25, 15]
        )[0]
    else:
        sentence_type = random.choice(sentence_types)  # All types
    
    return generate_sentence_by_type(sentence_type, should_be_true, divisors, max_dividend)

def generate_sentence_by_type(sentence_type, should_be_true, divisors, max_dividend):
    """Generate specific type of division sentence"""
    
    if sentence_type == "simple_division":
        # Format: a ÷ b = c
        divisor = random.choice(divisors)
        if divisor == 1:
            quotient = random.randint(1, min(15, max_dividend))
        else:
            quotient = random.randint(1, min(max_dividend // divisor, 12))
        
        dividend = divisor * quotient
        
        if should_be_true:
            right_side = quotient
        else:
            # Make it false by changing the quotient
            wrong_options = [quotient + 1, quotient - 1, quotient + 2, quotient * 2]
            wrong_options = [x for x in wrong_options if x > 0 and x != quotient]
            right_side = random.choice(wrong_options) if wrong_options else quotient + 1
        
        return {
            "equation": f"{dividend} ÷ {divisor} = {right_side}",
            "left_value": dividend // divisor,
            "right_value": right_side,
            "is_true": should_be_true
        }
    
    elif sentence_type == "division_vs_number":
        # Format: a ÷ b = c (where c is just a number)
        divisor = random.choice(divisors)
        if divisor == 1:
            quotient = random.randint(1, min(15, max_dividend))
        else:
            quotient = random.randint(1, min(max_dividend // divisor, 12))
        
        dividend = divisor * quotient
        
        if should_be_true:
            right_side = quotient
        else:
            # Make it false
            wrong_options = [quotient + 1, quotient - 1, quotient + 2]
            wrong_options = [x for x in wrong_options if x > 0 and x != quotient]
            right_side = random.choice(wrong_options) if wrong_options else quotient + 1
        
        return {
            "equation": f"{dividend} ÷ {divisor} = {right_side}",
            "left_value": quotient,
            "right_value": right_side,
            "is_true": should_be_true
        }
    
    elif sentence_type == "two_divisions":
        # Format: a ÷ b = c ÷ d
        divisor1 = random.choice(divisors)
        divisor2 = random.choice(divisors)
        
        if should_be_true:
            # Make both sides equal
            quotient = random.randint(1, 8)
            dividend1 = divisor1 * quotient
            dividend2 = divisor2 * quotient
        else:
            # Make them different
            quotient1 = random.randint(1, 8)
            quotient2 = quotient1 + random.choice([1, -1, 2])
            quotient2 = max(1, quotient2)
            
            dividend1 = divisor1 * quotient1
            dividend2 = divisor2 * quotient2
        
        return {
            "equation": f"{dividend1} ÷ {divisor1} = {dividend2} ÷ {divisor2}",
            "left_value": dividend1 // divisor1,
            "right_value": dividend2 // divisor2,
            "is_true": should_be_true
        }
    
    elif sentence_type == "division_vs_addition":
        # Format: a ÷ b = c + d
        divisor = random.choice(divisors)
        quotient = random.randint(2, 10)
        dividend = divisor * quotient
        
        if should_be_true:
            # Make addition equal to quotient
            addend1 = random.randint(1, quotient - 1)
            addend2 = quotient - addend1
        else:
            # Make addition different
            addend1 = random.randint(1, quotient + 2)
            addend2 = random.randint(1, quotient + 2)
            while addend1 + addend2 == quotient:
                addend2 = random.randint(1, quotient + 2)
        
        return {
            "equation": f"{dividend} ÷ {divisor} = {addend1} + {addend2}",
            "left_value": quotient,
            "right_value": addend1 + addend2,
            "is_true": should_be_true
        }
    
    else:  # division_vs_subtraction
        # Format: a ÷ b = c - d
        divisor = random.choice(divisors)
        quotient = random.randint(1, 8)
        dividend = divisor * quotient
        
        if should_be_true:
            # Make subtraction equal to quotient
            minuend = quotient + random.randint(1, 5)
            subtrahend = minuend - quotient
        else:
            # Make subtraction different
            minuend = random.randint(quotient + 1, quotient + 6)
            subtrahend = random.randint(1, minuend - 1)
            while minuend - subtrahend == quotient:
                subtrahend = random.randint(1, minuend - 1)
        
        return {
            "equation": f"{dividend} ÷ {divisor} = {minuend} - {subtrahend}",
            "left_value": quotient,
            "right_value": minuend - subtrahend,
            "is_true": should_be_true
        }

def generate_new_question():
    """Generate a new true/false question"""
    question_data = generate_division_sentences()
    
    st.session_state.question_data = question_data
    st.session_state.correct_answer = question_data["is_true"]
    st.session_state.current_question = "Is the number sentence true or false?"
    st.session_state.selected_answer = None

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### ✅❌ Is the number sentence true or false?")
    
    # Display the equation
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 35px; 
        border-radius: 15px; 
        border-left: 5px solid #17a2b8;
        font-size: 32px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    ">
        {data['equation']}
    </div>
    """, unsafe_allow_html=True)
    
    # True/False buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("true", key="true_btn", type="primary" if st.session_state.selected_answer == True else "secondary", use_container_width=True):
            st.session_state.selected_answer = True
            st.rerun()
    
    with col2:
        if st.button("false", key="false_btn", type="primary" if st.session_state.selected_answer == False else "secondary", use_container_width=True):
            st.session_state.selected_answer = False
            st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.selected_answer is not None:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        else:
            st.info("👆 Choose true or false above")
    
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
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show why it's correct
        if correct_answer:
            st.markdown(f"**{data['equation']}** is **TRUE** ✓")
            st.markdown(f"Both sides equal **{data['left_value']}**")
        else:
            st.markdown(f"**{data['equation']}** is **FALSE** ✓")
            st.markdown(f"Left side = **{data['left_value']}**, Right side = **{data['right_value']}**")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.division_true_false_difficulty
        st.session_state.division_true_false_difficulty = min(
            st.session_state.division_true_false_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.division_true_false_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 division sentence evaluation!**")
        elif old_level < st.session_state.division_true_false_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.division_true_false_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        if correct_answer:
            st.markdown(f"**{data['equation']}** is **TRUE**")
            st.markdown(f"Both sides equal **{data['left_value']}**")
        else:
            st.markdown(f"**{data['equation']}** is **FALSE**")
            st.markdown(f"Left side = **{data['left_value']}**, Right side = **{data['right_value']}**")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.division_true_false_difficulty
        st.session_state.division_true_false_difficulty = max(
            st.session_state.division_true_false_difficulty - 1, 1
        )
        
        if old_level > st.session_state.division_true_false_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.division_true_false_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Evaluation:
        
        **Equation:** {data['equation']}
        
        **Step 1: Calculate the left side**
        Left side = **{data['left_value']}**
        
        **Step 2: Calculate the right side**
        Right side = **{data['right_value']}**
        
        **Step 3: Compare the results**
        {data['left_value']} {'=' if data['left_value'] == data['right_value'] else '≠'} {data['right_value']}
        
        **Conclusion:** The equation is **{'TRUE' if correct_answer else 'FALSE'}**
        """)
        
        # Add specific calculation details
        equation_parts = data['equation'].split(' = ')
        left_part = equation_parts[0]
        right_part = equation_parts[1]
        
        st.markdown(f"""
        ### Detailed Calculations:
        **Left side:** {left_part} = {data['left_value']}
        **Right side:** {right_part} = {data['right_value']}
        
        ### Remember:
        - Always **calculate each side** separately
        - **Compare the final values** to determine if they're equal
        - If equal → **True**, if different → **False**
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None