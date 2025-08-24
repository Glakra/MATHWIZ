import streamlit as st
import random

def run():
    """
    Main function to run the Compare Unit Fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/compare_unit_fractions.py
    """
    # Initialize session state
    if "fractions_level" not in st.session_state:
        st.session_state.fractions_level = 1  # Start with easier comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_fraction = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🔢 Compare Unit Fractions")
    st.markdown("*Compare unit fractions and select the correct answer*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_level
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = ["Basic comparisons", "Standard comparisons", "Advanced comparisons"][min(difficulty_level-1, 2)]
        st.markdown(f"**Current Level:** {difficulty_text}")
        progress = min(difficulty_level / 3, 1.0)
        st.progress(progress, text=difficulty_text)
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Standard**")
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
        st.markdown("### How to Play:")
        st.markdown("- **Read the question** - Which fraction is greater? or Which fraction is less?")
        st.markdown("- **Click on the correct fraction tile** to select your answer")
        st.markdown("- **Press Submit** to check your answer")
        st.markdown("- **Remember:** Unit fractions have 1 as the numerator")
        
        st.markdown("### Quick Tips:")
        st.markdown("- **For unit fractions:** Bigger denominator = Smaller fraction")
        st.markdown("- **Think visually:** 1/2 of a pizza > 1/4 of a pizza > 1/8 of a pizza")
        st.markdown("- **Compare denominators:** When numerators are both 1, just compare the bottom numbers")
        
        st.markdown("### Examples:")
        st.markdown("- **1/2 > 1/3** (2 pieces vs 3 pieces - fewer pieces means bigger pieces)")
        st.markdown("- **1/4 < 1/3** (4 pieces vs 3 pieces - more pieces means smaller pieces)")
        st.markdown("- **1/10 < 1/5** (10 pieces vs 5 pieces - much smaller pieces!)")
        
        st.markdown("### Strategy:")
        st.markdown("- When comparing unit fractions, the fraction with the **smaller denominator is greater**")
        st.markdown("- When in doubt, imagine dividing a pizza!")

def generate_new_question():
    """Generate a new unit fractions comparison question"""
    difficulty = st.session_state.fractions_level
    
    # Define denominator pools based on difficulty
    if difficulty == 1:
        # Basic: Very common fractions with clear differences
        denominators = [2, 3, 4, 5, 6, 8]
    elif difficulty == 2:
        # Standard: Include more denominators
        denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    else:
        # Advanced: Include all denominators up to 15
        denominators = list(range(2, 16))
    
    # Select two different denominators
    denom1, denom2 = random.sample(denominators, 2)
    
    # Create the fractions (unit fractions have numerator 1)
    fraction1 = (1, denom1)
    fraction2 = (1, denom2)
    
    # Randomly decide whether to ask for less or greater
    comparison_type = random.choice(["less", "greater"])
    
    # Store question data
    st.session_state.question_data = {
        "fraction1": fraction1,
        "fraction2": fraction2,
        "comparison_type": comparison_type,
        "correct_answer": None
    }
    
    # Determine correct answer
    value1 = fraction1[0] / fraction1[1]
    value2 = fraction2[0] / fraction2[1]
    
    if comparison_type == "less":
        st.session_state.question_data["correct_answer"] = fraction1 if value1 < value2 else fraction2
        st.session_state.current_question = "Which fraction is less?"
    else:
        st.session_state.question_data["correct_answer"] = fraction1 if value1 > value2 else fraction2
        st.session_state.current_question = "Which fraction is greater?"
    
    # Reset selection
    st.session_state.selected_fraction = None

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown(f"### {st.session_state.current_question}")
    
    # Add custom styling for fraction tiles
    st.markdown("""
    <style>
    /* Style for fraction buttons */
    .stButton > button {
        min-height: 70px !important;
        font-size: 28px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        white-space: nowrap !important;
    }
    
    /* Selected button style */
    .stButton > button[kind="primary"] {
        background-color: #d1e7ff !important;
        border: 2px solid #0066cc !important;
        color: #0066cc !important;
    }
    
    /* Unselected button style */
    .stButton > button[kind="secondary"] {
        background-color: #f0f2f6 !important;
        border: 2px solid #c3c7cf !important;
        color: #262730 !important;
    }
    
    /* Hover effect */
    .stButton > button:hover {
        transform: scale(1.05);
        transition: transform 0.2s;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create fraction tiles
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use columns for side-by-side tiles with better spacing
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])
    
    frac1_str = f"{data['fraction1'][0]}/{data['fraction1'][1]}"
    frac2_str = f"{data['fraction2'][0]}/{data['fraction2'][1]}"
    
    # Style the fraction display
    with col2:
        # First fraction tile
        if st.button(
            frac1_str,
            key="frac1_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac1_str else "primary",
            help=f"Click to select {frac1_str}"
        ):
            st.session_state.selected_fraction = frac1_str
            st.rerun()
    
    with col3:
        # Second fraction tile
        if st.button(
            frac2_str,
            key="frac2_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac2_str else "primary",
            help=f"Click to select {frac2_str}"
        ):
            st.session_state.selected_fraction = frac2_str
            st.rerun()
    
    # Show selection reminder if no fraction is selected
    if st.session_state.selected_fraction is None and not st.session_state.answer_submitted:
        st.info("👆 Click on a fraction to select your answer")
    elif st.session_state.selected_fraction is not None and not st.session_state.answer_submitted:
        st.success(f"✔️ You selected: **{st.session_state.selected_fraction}**")
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_disabled = st.session_state.selected_fraction is None or st.session_state.answer_submitted
        if st.button("Submit", type="primary", use_container_width=True, disabled=submit_disabled):
            # Parse the selected answer back to tuple format
            parts = st.session_state.selected_fraction.split('/')
            selected_tuple = (int(parts[0]), int(parts[1]))
            st.session_state.user_answer = selected_tuple
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data["correct_answer"]
    comparison_type = st.session_state.question_data["comparison_type"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Well done!**")
        
        # Quick explanation
        frac1 = st.session_state.question_data["fraction1"]
        frac2 = st.session_state.question_data["fraction2"]
        if comparison_type == "greater":
            larger = correct_answer
            st.info(f"**{larger[0]}/{larger[1]}** is greater because dividing by {larger[1]} gives bigger pieces than dividing by {frac1[1] if larger != frac1 else frac2[1]}.")
        else:
            smaller = correct_answer
            st.info(f"**{smaller[0]}/{smaller[1]}** is less because dividing by {smaller[1]} gives smaller pieces than dividing by {frac1[1] if smaller != frac1 else frac2[1]}.")
        
        # Increase difficulty
        old_level = st.session_state.fractions_level
        st.session_state.fractions_level = min(st.session_state.fractions_level + 1, 3)
        
        if st.session_state.fractions_level > old_level:
            if st.session_state.fractions_level == 3:
                st.balloons()
    else:
        correct_str = f"{correct_answer[0]}/{correct_answer[1]}"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_str}**.")
        
        # Decrease difficulty
        old_level = st.session_state.fractions_level
        st.session_state.fractions_level = max(st.session_state.fractions_level - 1, 1)
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    frac1 = data["fraction1"]
    frac2 = data["fraction2"]
    comparison_type = data["comparison_type"]
    correct = data["correct_answer"]
    
    with st.expander("📖 **See explanation**", expanded=True):
        st.markdown(f"**Comparing:** {frac1[0]}/{frac1[1]} and {frac2[0]}/{frac2[1]}")
        
        # Simple rule
        st.markdown("### Remember:")
        st.markdown("For unit fractions: **smaller denominator = larger fraction**")
        
        # Visual comparison
        if frac1[1] < frac2[1]:
            st.markdown(f"- {frac1[1]} parts < {frac2[1]} parts")
            st.markdown(f"- So {frac1[0]}/{frac1[1]} > {frac2[0]}/{frac2[1]}")
        else:
            st.markdown(f"- {frac1[1]} parts > {frac2[1]} parts")
            st.markdown(f"- So {frac1[0]}/{frac1[1]} < {frac2[0]}/{frac2[1]}")
        
        # Pizza example
        st.markdown("### 🍕 Think Pizza:")
        st.markdown(f"- 1 slice of a {min(frac1[1], frac2[1])}-slice pizza is **bigger**")
        st.markdown(f"- 1 slice of a {max(frac1[1], frac2[1])}-slice pizza is **smaller**")
        
        # Answer
        st.markdown("---")
        if comparison_type == "less":
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the smaller fraction")
        else:
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the larger fraction")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_fraction = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer