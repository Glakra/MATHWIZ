import streamlit as st
import random

def run():
    """
    Main function to run the Inequalities with multiplication activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C.Multiplication/inequalities_with_multiplication.py
    """
    # Initialize session state for difficulty and game state
    if "inequalities_mult_difficulty" not in st.session_state:
        st.session_state.inequalities_mult_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_sign = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("⚖️ Inequalities with Multiplication")
    st.markdown("*Compare multiplication expressions with numbers using >, <, or =*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.inequalities_mult_difficulty
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
        ### How to Compare:
        - **Calculate the multiplication** on the left side
        - **Compare with the number** on the right side
        - **Choose the correct sign:**
          - **>** means "greater than"
          - **<** means "less than" 
          - **=** means "equal to"
        
        ### Quick Strategies:
        1. **Mental Math:** Calculate the product quickly
        2. **Estimation:** Round numbers for quick comparison
        3. **Number Sense:** Use known facts to help
        
        ### Examples:
        - **7 × 8 ? 50** → 7 × 8 = 56, so 56 > 50 → **>**
        - **4 × 9 ? 40** → 4 × 9 = 36, so 36 < 40 → **<**
        - **6 × 5 ? 30** → 6 × 5 = 30, so 30 = 30 → **=**
        
        ### Estimation Tips:
        - **Round to nearest 10:** 23 × 4 ≈ 20 × 4 = 80
        - **Break apart:** 15 × 6 = (10 × 6) + (5 × 6) = 60 + 30 = 90
        - **Use doubles:** 8 × 7 = 8 × 6 + 8 = 48 + 8 = 56
        
        ### Remember:
        - **>** The left side is **bigger**
        - **<** The left side is **smaller**
        - **=** Both sides are **the same**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Single digit × single digit vs. small numbers
        - **🟠 Level 3:** Single digit × double digit vs. medium numbers
        - **🔴 Level 4-5:** Double digit × double digit vs. large numbers
        
        ### Key Skills:
        - ✅ **Mental multiplication** - calculating products quickly
        - ✅ **Estimation** - approximating to compare faster
        - ✅ **Number comparison** - understanding >, <, =
        - ✅ **Math reasoning** - using logic to eliminate choices
        """)

def generate_new_question():
    """Generate a new inequality question"""
    level = st.session_state.inequalities_mult_difficulty
    
    # Determine ranges based on difficulty
    if level == 1:
        # Single digit × single digit, compare with small numbers
        factor1_range = (2, 9)
        factor2_range = (2, 9)
        comparison_offset = (-15, 15)
    elif level == 2:
        # Single digit × single digit, compare with medium numbers
        factor1_range = (3, 9)
        factor2_range = (3, 9)
        comparison_offset = (-25, 25)
    elif level == 3:
        # Single × double digit, compare with medium numbers
        factor1_range = (2, 9)
        factor2_range = (10, 25)
        comparison_offset = (-40, 40)
    elif level == 4:
        # Larger single × double digit
        factor1_range = (4, 9)
        factor2_range = (15, 35)
        comparison_offset = (-60, 60)
    else:  # level 5
        # Double × double digit
        factor1_range = (10, 25)
        factor2_range = (10, 35)
        comparison_offset = (-100, 100)
    
    # Generate the multiplication factors
    factor1 = random.randint(*factor1_range)
    factor2 = random.randint(*factor2_range)
    
    # Calculate the actual product
    actual_product = factor1 * factor2
    
    # Decide what type of comparison we want
    comparison_types = ['greater', 'less', 'equal']
    desired_comparison = random.choice(comparison_types)
    
    if desired_comparison == 'equal':
        # Make them equal
        comparison_number = actual_product
        correct_sign = '='
    elif desired_comparison == 'greater':
        # Make the product greater than the comparison number
        min_offset, max_offset = comparison_offset
        offset = random.randint(min_offset, -1)  # Negative offset makes comparison smaller
        comparison_number = max(1, actual_product + offset)
        correct_sign = '>'
    else:  # 'less'
        # Make the product less than the comparison number
        min_offset, max_offset = comparison_offset
        offset = random.randint(1, max_offset)  # Positive offset makes comparison larger
        comparison_number = actual_product + offset
        correct_sign = '<'
    
    # Sometimes adjust for more interesting numbers
    if random.random() < 0.3:
        # Make comparison number a "nice" number (multiple of 5 or 10)
        if comparison_number > 10:
            if desired_comparison == 'greater':
                comparison_number = (comparison_number // 10) * 10  # Round down to nearest 10
                if comparison_number >= actual_product:
                    comparison_number -= 10
            elif desired_comparison == 'less':
                comparison_number = ((comparison_number // 10) + 1) * 10  # Round up to nearest 10
                if comparison_number <= actual_product:
                    comparison_number += 10
    
    # Ensure the comparison makes sense
    if comparison_number <= 0:
        comparison_number = 1
    
    # Recalculate correct sign based on final numbers
    if actual_product > comparison_number:
        correct_sign = '>'
    elif actual_product < comparison_number:
        correct_sign = '<'
    else:
        correct_sign = '='
    
    st.session_state.question_data = {
        "factor1": factor1,
        "factor2": factor2,
        "comparison_number": comparison_number,
        "actual_product": actual_product
    }
    st.session_state.correct_answer = correct_sign
    st.session_state.current_question = "Which sign makes the statement true?"
    st.session_state.selected_sign = None

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### ⚖️ Question:")
    st.markdown("**Which sign makes the statement true?**")
    
    # Display the inequality expression
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
        {data['factor1']} × {data['factor2']} ? {data['comparison_number']}
    </div>
    """, unsafe_allow_html=True)
    
    # Sign selection buttons with HTML entities
    st.markdown("**Choose the correct sign:**")
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col2:
        # Greater than button
        button_style = "primary" if st.session_state.selected_sign == ">" else "secondary"
        if st.button("**>**", key="greater", type=button_style, use_container_width=True):
            st.session_state.selected_sign = ">"
            st.rerun()
    
    with col3:
        # Less than button  
        button_style = "primary" if st.session_state.selected_sign == "<" else "secondary"
        if st.button("**<**", key="less", type=button_style, use_container_width=True):
            st.session_state.selected_sign = "<"
            st.rerun()
    
    with col4:
        # Equal button
        button_style = "primary" if st.session_state.selected_sign == "=" else "secondary"
        if st.button("**=**", key="equal", type=button_style, use_container_width=True):
            st.session_state.selected_sign = "="
            st.rerun()
    
    # Show selected statement
    if st.session_state.selected_sign:
        st.markdown("---")
        st.markdown("**Your answer:**")
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd; 
            padding: 20px; 
            border-radius: 10px; 
            font-size: 24px;
            text-align: center;
            margin: 15px 0;
            font-weight: bold;
            color: #1976d2;
            font-family: 'Courier New', monospace;
        ">
            {data['factor1']} × {data['factor2']} {st.session_state.selected_sign} {data['comparison_number']}
        </div>
        """, unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.selected_sign:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        else:
            st.info("👆 Choose a sign (>, <, or =) above")
    
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
    user_answer = st.session_state.selected_sign
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the calculation
        st.markdown(f"**{data['factor1']} × {data['factor2']} = {data['actual_product']}**")
        st.markdown(f"**{data['actual_product']} {correct_answer} {data['comparison_number']}** ✓")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.inequalities_mult_difficulty
        st.session_state.inequalities_mult_difficulty = min(
            st.session_state.inequalities_mult_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.inequalities_mult_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 multiplication inequalities!**")
        elif old_level < st.session_state.inequalities_mult_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.inequalities_mult_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they chose vs. correct
        st.markdown(f"You chose: **{data['factor1']} × {data['factor2']} {user_answer} {data['comparison_number']}**")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.inequalities_mult_difficulty
        st.session_state.inequalities_mult_difficulty = max(
            st.session_state.inequalities_mult_difficulty - 1, 1
        )
        
        if old_level > st.session_state.inequalities_mult_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.inequalities_mult_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Step 1: Calculate the multiplication**
        {data['factor1']} × {data['factor2']} = {data['actual_product']}
        
        **Step 2: Compare the result**
        {data['actual_product']} ? {data['comparison_number']}
        """)
        
        # Explain the comparison
        if correct_answer == '>':
            st.markdown(f"""
            **Step 3: Determine the relationship**
            {data['actual_product']} is **greater than** {data['comparison_number']}
            
            So: **{data['factor1']} × {data['factor2']} > {data['comparison_number']}** ✓
            
            **Remember:** > means "greater than" (the left side is bigger)
            """)
        elif correct_answer == '<':
            st.markdown(f"""
            **Step 3: Determine the relationship**
            {data['actual_product']} is **less than** {data['comparison_number']}
            
            So: **{data['factor1']} × {data['factor2']} < {data['comparison_number']}** ✓
            
            **Remember:** < means "less than" (the left side is smaller)
            """)
        else:  # equal
            st.markdown(f"""
            **Step 3: Determine the relationship**
            {data['actual_product']} is **equal to** {data['comparison_number']}
            
            So: **{data['factor1']} × {data['factor2']} = {data['comparison_number']}** ✓
            
            **Remember:** = means "equal to" (both sides are the same)
            """)
        
        # Show estimation strategy if helpful
        if data['actual_product'] > 50:
            st.markdown(f"""
            ### Quick Estimation Strategy:
            **{data['factor1']} × {data['factor2']}** can be estimated as:
            """)
            
            # Round to nearest 10 for estimation
            rounded1 = round(data['factor1'] / 10) * 10
            rounded2 = round(data['factor2'] / 10) * 10
            if rounded1 == 0:
                rounded1 = 10
            if rounded2 == 0:
                rounded2 = 10
            
            estimated = rounded1 * rounded2
            st.markdown(f"- Round: {rounded1} × {rounded2} = {estimated}")
            st.markdown(f"- This is close to our exact answer of {data['actual_product']}")
        
        # Memory tips for signs
        st.markdown(f"""
        ### Memory Tips:
        - **>** Think of an arrow pointing right → (greater)
        - **<** Think of an arrow pointing left ← (less)  
        - **=** Both sides are balanced ⚖️ (equal)
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_sign = None