import streamlit as st
import random

def run():
    """
    Main function to run the Multiplication Facts: Find the Missing Factor practice activity.
    This gets called when the subtopic is loaded from the main navigation.
    """
    # Initialize session state for difficulty and game state
    if "missing_factor_difficulty" not in st.session_state:
        st.session_state.missing_factor_difficulty = 5  # Start with factors up to 5
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔍 Multiplication Facts up to 10: Find the Missing Factor")
    st.markdown("*Find the missing number in multiplication equations*")
    st.markdown("---")
    
    # Difficulty indicator
    max_factor = st.session_state.missing_factor_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** Factors up to {max_factor}")
        # Progress bar (5 to 10)
        progress = (max_factor - 5) / 5  # Convert 5-10 to 0-1
        st.progress(progress, text=f"Up to {max_factor}×{max_factor}")
    
    with col2:
        if max_factor <= 6:
            st.markdown("**🟡 Beginner**")
        elif max_factor <= 8:
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
        - **Look at the multiplication equation**
        - **Find the missing factor** (the unknown number)
        - **Type your answer** in the input box
        - **Think:** What number makes the equation true?
        
        ### Strategies to Find Missing Factors:
        
        #### Method 1: Use Division
        - **If you see: 4 × ? = 24**
        - **Think: 24 ÷ 4 = ?**
        - **Answer: 6** (because 4 × 6 = 24)
        
        #### Method 2: Count Up by the Known Factor
        - **If you see: 3 × ? = 15**
        - **Count by 3s: 3, 6, 9, 12, 15**
        - **That's 5 jumps, so 3 × 5 = 15**
        
        #### Method 3: Use Known Facts
        - **If you know: 7 × 8 = 56**
        - **Then you also know: ? × 8 = 56 means ? = 7**
        - **And: 7 × ? = 56 means ? = 8**
        
        ### Special Cases:
        - **× 1 = same number:** Any number × 1 equals itself
        - **× 0 = 0:** Any number × 0 equals 0
        - **Same factors:** 6 × 6 = 36 (perfect squares)
        
        ### Examples:
        - **5 × ? = 35** → Think: 35 ÷ 5 = 7
        - **? × 4 = 28** → Think: 28 ÷ 4 = 7  
        - **9 × ? = 81** → Think: 9 × 9 = 81, so ? = 9
        
        ### Difficulty Levels:
        - **🟡 Level 5-6:** Easier factors (1-6)
        - **🟠 Level 7-8:** Medium factors (1-8)
        - **🔴 Level 9-10:** All factors (1-10)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder factors
        - ❌ **Wrong answer:** Practice easier factors
        - 🎯 **Goal:** Master all factors up to 10!
        """)

def generate_new_question():
    """Generate a new missing factor question"""
    max_factor = st.session_state.missing_factor_difficulty
    
    # Generate two factors and their product
    factor1 = random.randint(1, max_factor)
    factor2 = random.randint(1, max_factor)
    product = factor1 * factor2
    
    # Randomly decide which factor to hide
    hide_first = random.choice([True, False])
    
    if hide_first:
        # Hide the first factor: ? × factor2 = product
        missing_factor = factor1
        known_factor = factor2
        position = "first"
        equation_display = f"? × {known_factor} = {product}"
    else:
        # Hide the second factor: factor1 × ? = product
        missing_factor = factor2
        known_factor = factor1
        position = "second"
        equation_display = f"{known_factor} × ? = {product}"
    
    st.session_state.question_data = {
        "equation_display": equation_display,
        "missing_factor": missing_factor,
        "known_factor": known_factor,
        "product": product,
        "position": position
    }
    st.session_state.correct_answer = missing_factor
    st.session_state.current_question = "Fill in the missing number."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display instruction
    st.markdown("### 🔍 Fill in the missing number.")
    
    # Create the equation display similar to the images
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display the equation with input box in a clean format
        equation_parts = data["equation_display"].split("?")
        
        if data["position"] == "first":
            # ? × known = product format
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 30px; 
                border-radius: 15px; 
                border: 2px solid #28a745;
                text-align: center;
                margin: 30px 0;
                font-family: 'Courier New', monospace;
            ">
                <div style="font-size: 36px; font-weight: bold; color: #28a745; margin-bottom: 20px;">
                    <span style="display: inline-block; margin: 0 10px;">⬜</span>
                    <span style="margin: 0 10px;">×</span>
                    <span style="margin: 0 10px;">{data['known_factor']}</span>
                    <span style="margin: 0 10px;">=</span>
                    <span style="margin: 0 10px;">{data['product']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # known × ? = product format
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 30px; 
                border-radius: 15px; 
                border: 2px solid #28a745;
                text-align: center;
                margin: 30px 0;
                font-family: 'Courier New', monospace;
            ">
                <div style="font-size: 36px; font-weight: bold; color: #28a745; margin-bottom: 20px;">
                    <span style="margin: 0 10px;">{data['known_factor']}</span>
                    <span style="margin: 0 10px;">×</span>
                    <span style="display: inline-block; margin: 0 10px;">⬜</span>
                    <span style="margin: 0 10px;">=</span>
                    <span style="margin: 0 10px;">{data['product']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_answer = st.number_input(
                "Enter the missing number:",
                min_value=0,
                max_value=10,
                value=None,
                step=1,
                key="missing_factor_input",
                placeholder="?"
            )
        
        # Submit button with matching style
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "Submit", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = int(user_answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show thinking help
    if not st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="
                background-color: #e8f4fd; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center;
                margin: 15px 0;
                border: 1px dashed #1f77b4;
            ">
                <div style="font-size: 14px; color: #666;">💭 Think: {data['product']} ÷ {data['known_factor']} = ?</div>
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Well done!**")
        
        # Show the complete equation
        complete_equation = data["equation_display"].replace("?", str(correct_answer))
        st.info(f"✨ **Complete equation:** {complete_equation}")
        
        # Increase difficulty (max factor 10)
        old_max = st.session_state.missing_factor_difficulty
        st.session_state.missing_factor_difficulty = min(
            st.session_state.missing_factor_difficulty + 1, 10
        )
        
        # Show encouragement based on difficulty
        if st.session_state.missing_factor_difficulty == 10 and old_max < 10:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered finding missing factors up to 10!**")
        elif old_max < st.session_state.missing_factor_difficulty:
            new_max = st.session_state.missing_factor_difficulty
            st.info(f"⬆️ **Level up! Now working with factors up to {new_max}**")
        
        # Show the division connection
        st.markdown(f"**🔗 Remember:** {data['product']} ÷ {data['known_factor']} = {correct_answer}")
    
    else:
        st.error(f"❌ **Not quite right.** The missing factor is **{correct_answer}**.")
        
        # Show the correct equation
        complete_equation = data["equation_display"].replace("?", str(correct_answer))
        st.info(f"✨ **Correct equation:** {complete_equation}")
        
        # Decrease difficulty (min factor 5)
        old_max = st.session_state.missing_factor_difficulty
        st.session_state.missing_factor_difficulty = max(
            st.session_state.missing_factor_difficulty - 1, 5
        )
        
        if old_max > st.session_state.missing_factor_difficulty:
            new_max = st.session_state.missing_factor_difficulty
            st.warning(f"⬇️ **Let's practice with easier factors. Now working up to {new_max}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for finding the missing factor"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here to learn how to find missing factors**", expanded=True):
        st.markdown(f"""
        ### How to solve: {data['equation_display']}
        
        **Answer: {correct_answer}**
        
        ### Method 1: Use Division
        - **We know:** {data['known_factor']} × ? = {data['product']}
        - **Think:** What times {data['known_factor']} equals {data['product']}?
        - **Divide:** {data['product']} ÷ {data['known_factor']} = **{correct_answer}**
        - **Check:** {data['known_factor']} × {correct_answer} = {data['product']} ✓
        
        ### Method 2: Skip Counting
        Count by {data['known_factor']}s until you reach {data['product']}:
        """)
        
        # Show skip counting sequence
        if data['known_factor'] <= 6 and correct_answer <= 8:  # Only for reasonable sizes
            sequence = []
            for i in range(1, correct_answer + 1):
                sequence.append(f"{data['known_factor']} × {i} = {data['known_factor'] * i}")
            
            for step in sequence:
                if step.endswith(f"= {data['product']}"):
                    st.markdown(f"- **{step}** ← This is our answer!")
                else:
                    st.markdown(f"- {step}")
        
        st.markdown(f"""
        ### Why This Works:
        - **Multiplication and division are opposites**
        - **If a × b = c, then c ÷ a = b and c ÷ b = a**
        - **{data['known_factor']} × {correct_answer} = {data['product']}**
        - **{data['product']} ÷ {data['known_factor']} = {correct_answer}**
        
        ### Quick Check:
        **{data['known_factor']} × {correct_answer} = {data['known_factor'] * correct_answer}** ✓
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer