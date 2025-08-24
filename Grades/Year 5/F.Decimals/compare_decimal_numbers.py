import streamlit as st
import random

def run():
    """
    Main function to run the Compare Decimal Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimal_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "compare_decimal_difficulty" not in st.session_state:
        st.session_state.compare_decimal_difficulty = 1  # Start with simple decimals
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_comparison = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Compare Decimal Numbers")
    st.markdown("*Compare decimal numbers and choose the correct sign*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_decimal_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple decimals (tenths)",
            2: "Hundredths comparisons", 
            3: "Mixed decimal places",
            4: "Close value comparisons",
            5: "Advanced decimal challenges"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
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
        ### How to Play:
        - **Look at the two decimal numbers** displayed
        - **Compare their values** using place value
        - **Choose the correct comparison sign** (>, <, or =)
        - **Click on your answer** to submit
        
        ### Comparison Signs:
        - **>** means "greater than" (left number is bigger)
        - **<** means "less than" (left number is smaller)  
        - **=** means "equal to" (both numbers are the same)
        
        ### How to Compare Decimals:
        1. **Compare whole number parts first**
        2. **If whole numbers are equal, compare tenths**
        3. **If tenths are equal, compare hundredths**
        4. **Continue until you find a difference**
        
        ### Examples:
        - **9.3 vs 9.1:** Same whole number (9), but 3 tenths > 1 tenth, so 9.3 > 9.1
        - **2.45 vs 2.5:** Same whole number (2), same tenths (4 vs 5), so 2.45 < 2.5
        - **0.8 vs 0.80:** These are equal! 0.8 = 0.80
        - **15.6 vs 8.9:** 15 > 8, so 15.6 > 8.9
        
        ### Place Value Tips:
        - **Tenths place:** First digit after decimal point (0.7 = 7 tenths)
        - **Hundredths place:** Second digit after decimal point (0.07 = 7 hundredths)
        - **7 tenths = 70 hundredths:** So 0.7 = 0.70
        - **More digits doesn't mean bigger:** 0.5 > 0.499
        
        ### Strategies:
        - **Line up decimal points** mentally
        - **Add zeros** to make same length: 2.5 becomes 2.50
        - **Think about money:** $9.30 vs $9.10
        - **Use number lines** - which is further right?
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple tenths (1.2 vs 1.5)
        - **🟡 Level 2:** Hundredths (3.45 vs 3.42)
        - **🟠 Level 3:** Mixed places (0.8 vs 0.75)
        - **🔴 Level 4:** Close values (7.89 vs 7.9)
        - **🔴 Level 5:** Advanced challenges
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all comparison levels!
        """)

def generate_new_question():
    """Generate a new decimal comparison question based on difficulty level"""
    difficulty = st.session_state.compare_decimal_difficulty
    
    if difficulty == 1:
        # Simple tenths comparisons
        whole_parts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        tenths = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        decimal1 = random.choice(whole_parts) + random.choice(tenths) / 10
        decimal2 = random.choice(whole_parts) + random.choice(tenths) / 10
        
        # Ensure they're different
        while decimal1 == decimal2:
            decimal2 = random.choice(whole_parts) + random.choice(tenths) / 10
            
    elif difficulty == 2:
        # Hundredths comparisons
        decimal1 = round(random.uniform(1, 10), 2)
        decimal2 = round(random.uniform(1, 10), 2)
        
        # Ensure they're different
        while abs(decimal1 - decimal2) < 0.01:
            decimal2 = round(random.uniform(1, 10), 2)
            
    elif difficulty == 3:
        # Mixed decimal places - one tenths, one hundredths
        if random.choice([True, False]):
            decimal1 = round(random.uniform(1, 10), 1)  # tenths
            decimal2 = round(random.uniform(1, 10), 2)  # hundredths
        else:
            decimal1 = round(random.uniform(1, 10), 2)  # hundredths
            decimal2 = round(random.uniform(1, 10), 1)  # tenths
            
    elif difficulty == 4:
        # Close value comparisons
        base = round(random.uniform(1, 20), 2)
        variation = random.choice([0.01, 0.02, 0.03, 0.1, 0.2])
        
        if random.choice([True, False]):
            decimal1 = base
            decimal2 = round(base + variation, 2)
        else:
            decimal1 = round(base + variation, 2)
            decimal2 = base
            
    else:  # difficulty == 5
        # Advanced challenges including equal decimals
        if random.random() < 0.3:  # 30% chance of equal decimals
            base = round(random.uniform(1, 20), 2)
            if random.choice([True, False]):
                decimal1 = round(base, 1)  # 2.5
                decimal2 = round(base, 2)  # 2.50
            else:
                decimal1 = base
                decimal2 = base
        else:
            # Very close comparisons
            decimal1 = round(random.uniform(0.1, 50), 3)
            decimal2 = round(decimal1 + random.choice([-0.001, -0.01, 0.001, 0.01]), 3)
    
    # Determine correct comparison
    if decimal1 > decimal2:
        correct_answer = ">"
    elif decimal1 < decimal2:
        correct_answer = "<"
    else:
        correct_answer = "="
    
    # Store question data
    st.session_state.question_data = {
        "decimal1": decimal1,
        "decimal2": decimal2
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Which sign makes the statement true?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question text
    question_text = st.session_state.current_question
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #007acc;
        font-size: 18px;
        margin: 20px 0;
        color: #333;
        text-align: center;
    ">
        {question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Display the comparison with question mark (like the image)
    decimal1 = data["decimal1"]
    decimal2 = data["decimal2"]
    
    st.markdown(f"""
    <div style="
        text-align: center; 
        font-size: 36px; 
        font-weight: bold; 
        margin: 40px 0;
        color: #333;
        letter-spacing: 10px;
    ">
        {decimal1} ? {decimal2}
    </div>
    """, unsafe_allow_html=True)
    
    # Comparison buttons (clickable tiles like the image)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col2:
        if st.button("Greater\n(>)", key="greater_btn", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            st.session_state.selected_comparison = ">"
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    with col3:
        if st.button("Less\n(<)", key="less_btn", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            st.session_state.selected_comparison = "<"
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    with col4:
        if st.button("Equal\n(=)", key="equal_btn", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            st.session_state.selected_comparison = "="
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show selected answer
    if st.session_state.selected_comparison:
        st.markdown(f"""
        <div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; color: #007acc;">
            Your answer: {decimal1} {st.session_state.selected_comparison} {decimal2}
        </div>
        """, unsafe_allow_html=True)
    
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
    user_answer = st.session_state.selected_comparison
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.compare_decimal_difficulty
        st.session_state.compare_decimal_difficulty = min(
            st.session_state.compare_decimal_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.compare_decimal_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal number comparisons!**")
        elif old_difficulty < st.session_state.compare_decimal_difficulty:
            difficulty_names = {
                2: "hundredths comparisons",
                3: "mixed decimal places", 
                4: "close value comparisons",
                5: "advanced decimal challenges"
            }
            next_level = difficulty_names.get(st.session_state.compare_decimal_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        decimal1 = st.session_state.question_data["decimal1"]
        decimal2 = st.session_state.question_data["decimal2"]
        st.error(f"❌ **Not quite right.** The correct answer is **{decimal1} {correct_answer} {decimal2}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    decimal1 = data["decimal1"]
    decimal2 = data["decimal2"]
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step comparison:
        
        **Comparing:** {decimal1} {correct_answer} {decimal2}
        
        ### How to solve:
        """)
        
        # Break down the comparison step by step
        whole1 = int(decimal1)
        whole2 = int(decimal2)
        
        if whole1 != whole2:
            st.markdown(f"""
            **Step 1: Compare whole number parts**
            - {decimal1} has whole number **{whole1}**
            - {decimal2} has whole number **{whole2}**
            - Since **{whole1} {">" if whole1 > whole2 else "<"} {whole2}**, we have **{decimal1} {correct_answer} {decimal2}**
            """)
        else:
            # Same whole number, compare decimal parts
            dec_part1 = decimal1 - whole1
            dec_part2 = decimal2 - whole2
            
            st.markdown(f"""
            **Step 1: Compare whole number parts**
            - Both numbers have the same whole number part: **{whole1}**
            
            **Step 2: Compare decimal parts**
            - {decimal1} has decimal part **{dec_part1:.3f}**
            - {decimal2} has decimal part **{dec_part2:.3f}**
            """)
            
            # Compare tenths place
            tenths1 = int((decimal1 * 10) % 10)
            tenths2 = int((decimal2 * 10) % 10)
            
            if tenths1 != tenths2:
                st.markdown(f"""
            **Step 3: Compare tenths place**
            - {decimal1} has **{tenths1}** in the tenths place
            - {decimal2} has **{tenths2}** in the tenths place
            - Since **{tenths1} {">" if tenths1 > tenths2 else "<"} {tenths2}**, we have **{decimal1} {correct_answer} {decimal2}**
                """)
            else:
                # Compare hundredths if needed
                hundredths1 = int((decimal1 * 100) % 10)
                hundredths2 = int((decimal2 * 100) % 10)
                
                if hundredths1 != hundredths2:
                    st.markdown(f"""
            **Step 3: Compare hundredths place**
            - {decimal1} has **{hundredths1}** in the hundredths place
            - {decimal2} has **{hundredths2}** in the hundredths place
            - Since **{hundredths1} {">" if hundredths1 > hundredths2 else "<"} {hundredths2}**, we have **{decimal1} {correct_answer} {decimal2}**
                    """)
                else:
                    st.markdown(f"""
            **Step 3: Numbers are equal**
            - All decimal places are the same
            - Therefore **{decimal1} = {decimal2}**
                    """)
        
        # Add helpful tip based on the comparison
        if correct_answer == ">":
            st.markdown("💡 **Remember:** The number on the left is larger than the number on the right!")
        elif correct_answer == "<":
            st.markdown("💡 **Remember:** The number on the left is smaller than the number on the right!")
        else:
            st.markdown("💡 **Remember:** These decimal numbers represent the same value!")
        
        st.markdown("""
        ### 💡 Comparison tips:
        - **Start with whole numbers** - compare these first
        - **Then compare decimal places** from left to right
        - **Think about place value** - tenths, hundredths, thousandths
        - **Use real examples** - think about money ($9.30 vs $9.10)
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_comparison = None