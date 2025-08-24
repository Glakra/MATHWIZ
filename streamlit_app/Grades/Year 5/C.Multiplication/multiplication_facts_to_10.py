import streamlit as st
import random

def run():
    """
    Main function to run the Multiplication Facts practice activity.
    This gets called when the subtopic is loaded from the main navigation.
    """
    # Initialize session state for difficulty and game state
    if "multiplication_facts_max_factor" not in st.session_state:
        st.session_state.multiplication_facts_max_factor = 5  # Start with factors up to 5
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("✖️ Multiplication Facts to 10")
    st.markdown("*Master your multiplication tables with instant practice*")
    st.markdown("---")
    
    # Difficulty indicator
    max_factor = st.session_state.multiplication_facts_max_factor
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** Times tables up to {max_factor}")
        # Progress bar (5 to 10)
        progress = (max_factor - 5) / 5  # Convert 5-10 to 0-1
        st.progress(progress, text=f"Up to {max_factor} × {max_factor}")
    
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
        - **Solve the multiplication problem** as quickly as you can
        - **Type your answer** in the input box
        - **Press Submit** to check your answer
        - **Build up your times tables** from 5×5 up to 10×10!
        
        ### Tips for Success:
        - **Memorize patterns:** 2×8 = 16, so 8×2 = 16 too!
        - **Use known facts:** If you know 5×6 = 30, then 6×5 = 30
        - **Count by groups:** 7×4 means 7+7+7+7 = 28
        - **Practice daily:** A few minutes each day builds strong recall
        
        ### Common Patterns to Remember:
        - **×2 facts:** Double the number (6×2 = 12)
        - **×5 facts:** Always end in 0 or 5 (7×5 = 35)
        - **×9 facts:** Fingers trick or (10×n - n)
        - **×10 facts:** Just add a zero (8×10 = 80)
        
        ### Times Tables Progression:
        - **🟡 Level 5-6:** Basic facts (1-6 times tables)
        - **🟠 Level 7-8:** Intermediate facts (1-8 times tables)
        - **🔴 Level 9-10:** Advanced facts (1-10 times tables)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder times tables
        - ❌ **Wrong answer:** Practice easier times tables
        - 🎯 **Goal:** Master all tables up to 10×10!
        
        ### Memory Tips:
        - **6×7 = 42:** "Six-seven, forty-two"
        - **6×8 = 48:** "Six times eight, forty-eight"
        - **7×8 = 56:** "Seven times eight, fifty-six"
        - **9×9 = 81:** "Nine times nine, eighty-one"
        """)

def generate_new_question():
    """Generate a new multiplication facts question"""
    max_factor = st.session_state.multiplication_facts_max_factor
    
    # Generate two random factors within the current difficulty level
    a = random.randint(1, max_factor)
    b = random.randint(1, max_factor)
    correct_answer = a * b
    
    st.session_state.question_data = {
        "factor_a": a,
        "factor_b": b
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"{a} × {b}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with large, clear formatting
    st.markdown("### ✖️ Multiply:")
    
    # Display the multiplication problem in a large, centered format
    factor_a = data['factor_a']
    factor_b = data['factor_b']
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 40px; 
        border-radius: 20px; 
        border: 3px solid #28a745;
        text-align: center;
        margin: 30px 0;
        font-family: 'Courier New', monospace;
    ">
        <div style="font-size: 48px; font-weight: bold; color: #28a745; margin-bottom: 10px;">
            {factor_a} × {factor_b} = ?
        </div>
        <div style="font-size: 16px; color: #6c757d;">
            What is {factor_a} times {factor_b}?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual representation for smaller numbers (up to 6)
    if factor_a <= 6 and factor_b <= 6:
        show_visual_representation(factor_a, factor_b)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_answer = st.number_input(
                "Your answer:",
                min_value=0,
                max_value=100,
                value=None,
                step=1,
                key="multiplication_input",
                placeholder="Enter your answer"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = int(user_answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def show_visual_representation(a, b):
    """Show visual dots representation for smaller multiplication problems"""
    if a * b <= 36:  # Only show for reasonable sizes
        st.markdown("**Visual representation:**")
        
        # Create a grid of dots
        visual_html = "<div style='text-align: center; margin: 20px 0;'>"
        
        for row in range(a):
            visual_html += "<div style='margin: 5px 0;'>"
            for col in range(b):
                visual_html += "<span style='font-size: 20px; margin: 2px; color: #007bff;'>●</span>"
            visual_html += f" <span style='color: #6c757d; font-size: 14px;'>({b} dots)</span>" if row == 0 else ""
            visual_html += "</div>"
        
        visual_html += f"<div style='margin-top: 10px; font-weight: bold; color: #28a745;'>{a} groups of {b} = {a * b}</div>"
        visual_html += "</div>"
        
        st.markdown(visual_html, unsafe_allow_html=True)

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
        
        # Increase difficulty (max factor 10)
        old_max = st.session_state.multiplication_facts_max_factor
        st.session_state.multiplication_facts_max_factor = min(
            st.session_state.multiplication_facts_max_factor + 1, 10
        )
        
        # Show encouragement based on difficulty
        if st.session_state.multiplication_facts_max_factor == 10 and old_max < 10:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered all multiplication tables up to 10×10!**")
        elif old_max < st.session_state.multiplication_facts_max_factor:
            new_max = st.session_state.multiplication_facts_max_factor
            st.info(f"⬆️ **Level up! Now practicing times tables up to {new_max}×{new_max}**")
        
        # Show additional encouragement
        factor_a, factor_b = data['factor_a'], data['factor_b']
        if factor_a == factor_b:
            st.info(f"💡 **Great!** {factor_a}×{factor_b} = {correct_answer} is a perfect square!")
        elif factor_a == 9 or factor_b == 9:
            st.info("💡 **Tip:** 9 times tables have a cool finger trick!")
    
    else:
        st.error(f"❌ **Not quite right.** {data['factor_a']} × {data['factor_b']} = **{correct_answer}**")
        
        # Decrease difficulty (min factor 5)
        old_max = st.session_state.multiplication_facts_max_factor
        st.session_state.multiplication_facts_max_factor = max(
            st.session_state.multiplication_facts_max_factor - 1, 5
        )
        
        if old_max > st.session_state.multiplication_facts_max_factor:
            new_max = st.session_state.multiplication_facts_max_factor
            st.warning(f"⬇️ **Let's practice easier tables. Now working on tables up to {new_max}×{new_max}**")
        
        # Show helpful explanation
        show_explanation()

def show_explanation():
    """Show explanation and memory tips for the multiplication fact"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    factor_a, factor_b = data['factor_a'], data['factor_b']
    
    with st.expander("📖 **Click here for help remembering this fact**", expanded=True):
        st.markdown(f"### {factor_a} × {factor_b} = {correct_answer}")
        
        # Provide different explanation strategies
        explanations = []
        
        # Commutative property
        if factor_a != factor_b:
            explanations.append(f"**Flip it:** {factor_b} × {factor_a} = {correct_answer} (same answer!)")
        
        # Skip counting
        if factor_a <= factor_b:
            skip_sequence = [factor_a * i for i in range(1, factor_b + 1)]
            explanations.append(f"**Count by {factor_a}s:** {' → '.join(map(str, skip_sequence))}")
        
        # Addition method
        if factor_b <= 5:
            addition_parts = [str(factor_a)] * factor_b
            explanations.append(f"**Add {factor_b} groups:** {' + '.join(addition_parts)} = {correct_answer}")
        
        # Special patterns
        if factor_a == 2 or factor_b == 2:
            explanations.append("**Doubling:** Multiply by 2 means double the number!")
        elif factor_a == 5 or factor_b == 5:
            explanations.append("**Times 5 pattern:** Count by 5s, answers end in 0 or 5!")
        elif factor_a == 9 or factor_b == 9:
            other_factor = factor_b if factor_a == 9 else factor_a
            explanations.append(f"**Times 9 trick:** (10 × {other_factor}) - {other_factor} = {10 * other_factor} - {other_factor} = {correct_answer}")
        elif factor_a == 10 or factor_b == 10:
            explanations.append("**Times 10:** Just add a zero to the end!")
        
        # Display explanations
        for explanation in explanations:
            st.markdown(f"- {explanation}")
        
        # Memory device for tricky ones
        if (factor_a, factor_b) in [(6, 7), (7, 6)]:
            st.markdown("🧠 **Memory trick:** *'Six times seven, lucky forty-two!'*")
        elif (factor_a, factor_b) in [(6, 8), (8, 6)]:
            st.markdown("🧠 **Memory trick:** *'Six times eight, I won't be late, forty-eight!'*")
        elif (factor_a, factor_b) in [(7, 8), (8, 7)]:
            st.markdown("🧠 **Memory trick:** *'Seven times eight, fifty-six!'*")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer