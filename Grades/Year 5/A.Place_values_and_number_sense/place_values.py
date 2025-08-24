import streamlit as st
import random

def run():
    """
    Main function to run the Place Values practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/place_values.py
    """
    # Initialize session state for difficulty and game state
    if "convert_place_value_difficulty" not in st.session_state:
        st.session_state.convert_place_value_difficulty = 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Place Values")
    st.markdown("*Learn to convert between different place values*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.convert_place_value_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}/3")
        # Progress bar
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        level_names = ["🟡 Beginner", "🟠 Intermediate", "🔴 Advanced"]
        st.markdown(f"**{level_names[difficulty_level-1]}**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question in a card-like container
    with st.container():
        st.markdown("### 📝 Question:")
        
        # Question display with nice formatting
        question_container = st.container()
        with question_container:
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f2f6; 
                    padding: 20px; 
                    border-radius: 10px; 
                    border-left: 5px solid #1f77b4;
                    font-size: 24px;
                    text-align: center;
                    margin: 20px 0;
                ">
                    <strong>{st.session_state.current_question}</strong>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    # Create form for answer input
    with st.form("answer_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.text_input(
                "Your answer:", 
                key="answer_input",
                placeholder="Enter your answer here",
                label_visibility="collapsed"
            )
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.user_answer = user_answer.strip()
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Fill in the missing number** to complete the place value equation
        - **Example:** ___ tens = 50 ones → Answer: 5 (because 5 × 10 = 50)
        
        ### Levels:
        - **🟡 Level 1:** Convert tens to ones (1 ten = 10 ones)
        - **🟠 Level 2:** Convert hundreds to ones (1 hundred = 100 ones)  
        - **🔴 Level 3:** Convert thousands to ones (1 thousand = 1000 ones)
        
        ### Scoring:
        - ✅ **Correct answer:** Move up a level
        - ❌ **Wrong answer:** Move down a level
        - 🎯 **Goal:** Reach and maintain Level 3!
        """)

def generate_new_question():
    """Generate a new place value conversion question based on current difficulty"""
    levels = [
        (10, "tens"),
        (100, "hundreds"), 
        (1000, "thousands")
    ]
    
    difficulty = st.session_state.convert_place_value_difficulty
    level_index = min(difficulty - 1, 2)
    multiplier, unit = levels[level_index]
    
    base_units = random.randint(2, 9)
    total = base_units * multiplier
    
    question_html = f"___ {unit} = {total:,} ones"
    answer = str(base_units)
    
    st.session_state.current_question = question_html
    st.session_state.correct_answer = answer

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 3)
        old_level = st.session_state.convert_place_value_difficulty
        st.session_state.convert_place_value_difficulty = min(
            st.session_state.convert_place_value_difficulty + 1, 3
        )
        
        # Show encouragement based on level
        if st.session_state.convert_place_value_difficulty == 3 and old_level < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've reached the highest level!**")
        elif old_level < st.session_state.convert_place_value_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.convert_place_value_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.convert_place_value_difficulty
        st.session_state.convert_place_value_difficulty = max(
            st.session_state.convert_place_value_difficulty - 1, 1
        )
        
        if old_level > st.session_state.convert_place_value_difficulty:
            st.warning(f"⬇️ **Level down to Level {st.session_state.convert_place_value_difficulty}. Don't worry, you've got this!**")
        
        # Show explanation
        show_explanation(correct_answer)

def show_explanation(correct_answer):
    """Show explanation for the correct answer"""
    levels = [(10, "tens"), (100, "hundreds"), (1000, "thousands")]
    difficulty = st.session_state.convert_place_value_difficulty
    level_index = min(difficulty, 2)  # Use current level for explanation
    multiplier, unit = levels[level_index]
    
    total_value = int(correct_answer) * multiplier
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution:
        
        **Remember:** 1 {unit[:-1]} = {multiplier:,} ones
        
        **So:** {correct_answer} {unit} = {correct_answer} × {multiplier:,} = **{total_value:,} ones**
        
        **Tip:** Think of it like this - if you have {correct_answer} groups of {multiplier:,}, 
        you have {total_value:,} individual items total!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
