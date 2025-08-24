import streamlit as st
import random

def run():
    """
    Main function to run the Compare Fractions with Like Denominators activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/compare_fractions_with_like_denominators.py
    """
    # Initialize session state
    if "like_fractions_tiles_level" not in st.session_state:
        st.session_state.like_fractions_tiles_level = 1  # Start with easier comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_fraction = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🔢 Compare Fractions with Like Denominators")
    st.markdown("*Compare fractions that have the same denominator*")
    st.markdown("---")
    
    # Add custom CSS for button styling
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
    
    # Difficulty indicator
    difficulty_level = st.session_state.like_fractions_tiles_level
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = ["Simple comparisons", "Standard comparisons", "Challenging comparisons"][min(difficulty_level-1, 2)]
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
        st.markdown("- **Look at the two fractions** with the same denominator")
        st.markdown("- **Click on the correct fraction** to select your answer")
        st.markdown("- **Press Submit** to check your answer")
        
        st.markdown("### The Simple Rule:")
        st.markdown("When fractions have the **same denominator** (bottom number):")
        st.markdown("- **Just compare the numerators** (top numbers)")
        st.markdown("- **Bigger numerator = Bigger fraction**")
        st.markdown("- **Smaller numerator = Smaller fraction**")
        
        st.markdown("### Examples:")
        st.markdown("- **3/8 vs 5/8:** Since 5 > 3, then 5/8 > 3/8")
        st.markdown("- **2/6 vs 4/6:** Since 2 < 4, then 2/6 < 4/6")
        st.markdown("- **7/10 vs 3/10:** Since 7 > 3, then 7/10 > 3/10")
        
        st.markdown("### Why it works:")
        st.markdown("- Same denominator means same-sized pieces")
        st.markdown("- More pieces of the same size = larger amount")
        st.markdown("- It's like comparing 3 cookies vs 5 cookies - 5 is more!")

def generate_new_question():
    """Generate a new like denominators comparison question"""
    difficulty = st.session_state.like_fractions_tiles_level
    
    # Define denominator ranges based on difficulty
    if difficulty == 1:
        # Basic: Small denominators, clear differences
        denominators = [3, 4, 5, 6]
        min_diff = 2  # Minimum difference between numerators
    elif difficulty == 2:
        # Standard: Medium denominators
        denominators = [5, 6, 8, 10]
        min_diff = 1
    else:
        # Advanced: Larger denominators, any difference
        denominators = [8, 10, 12, 15, 20]
        min_diff = 1
    
    # Select a denominator
    denominator = random.choice(denominators)
    
    # Generate two different numerators
    possible_numerators = list(range(1, denominator))
    
    # For basic level, ensure clear differences
    if difficulty == 1 and len(possible_numerators) >= 4:
        # Pick numerators with at least min_diff difference
        num1 = random.choice(possible_numerators[:-min_diff])
        num2 = random.choice([n for n in possible_numerators if abs(n - num1) >= min_diff])
    else:
        # For other levels, any two different numerators
        if len(possible_numerators) >= 2:
            num1, num2 = random.sample(possible_numerators, 2)
        else:
            num1, num2 = 1, 2  # Fallback
    
    # Create the fractions
    fraction1 = (num1, denominator)
    fraction2 = (num2, denominator)
    
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
    if comparison_type == "less":
        st.session_state.question_data["correct_answer"] = fraction1 if num1 < num2 else fraction2
        st.session_state.current_question = "Which fraction is less?"
    else:
        st.session_state.question_data["correct_answer"] = fraction1 if num1 > num2 else fraction2
        st.session_state.current_question = "Which fraction is greater?"
    
    # Reset selection
    st.session_state.selected_fraction = None

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown(f"### {st.session_state.current_question}")
    
    # Add custom styling for fraction tiles if not already selected
    st.markdown("""
    <style>
    /* Ensure fractions display nicely */
    .fraction-text {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create fraction tiles
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use columns for side-by-side tiles with better spacing
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])
    
    frac1_str = f"{data['fraction1'][0]}/{data['fraction1'][1]}"
    frac2_str = f"{data['fraction2'][0]}/{data['fraction2'][1]}"
    
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
        st.success("🎉 **Correct! Excellent work!**")
        
        # Quick explanation
        frac1 = st.session_state.question_data["fraction1"]
        frac2 = st.session_state.question_data["fraction2"]
        st.info(f"When denominators are the same ({correct_answer[1]}), just compare numerators: "
                f"{frac1[0]} and {frac2[0]}. Since {correct_answer[0]} is "
                f"{'less' if comparison_type == 'less' else 'greater'}, "
                f"{correct_answer[0]}/{correct_answer[1]} is the answer!")
        
        # Increase difficulty
        old_level = st.session_state.like_fractions_tiles_level
        st.session_state.like_fractions_tiles_level = min(st.session_state.like_fractions_tiles_level + 1, 3)
        
        if st.session_state.like_fractions_tiles_level > old_level:
            if st.session_state.like_fractions_tiles_level == 3:
                st.balloons()
    else:
        correct_str = f"{correct_answer[0]}/{correct_answer[1]}"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_str}**.")
        
        # Decrease difficulty
        st.session_state.like_fractions_tiles_level = max(st.session_state.like_fractions_tiles_level - 1, 1)
        
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
        
        # The rule
        st.markdown("### Remember the rule:")
        st.markdown(f"When denominators are the same (**{frac1[1]}**), just compare the numerators!")
        
        # Show comparison
        st.markdown("### Compare the top numbers:")
        st.markdown(f"- First fraction: **{frac1[0]}**/{frac1[1]}")
        st.markdown(f"- Second fraction: **{frac2[0]}**/{frac2[1]}")
        
        # Which is bigger/smaller
        if frac1[0] > frac2[0]:
            st.markdown(f"Since **{frac1[0]} > {frac2[0]}**, we know **{frac1[0]}/{frac1[1]} > {frac2[0]}/{frac2[1]}**")
        else:
            st.markdown(f"Since **{frac1[0]} < {frac2[0]}**, we know **{frac1[0]}/{frac1[1]} < {frac2[0]}/{frac2[1]}**")
        
        # Visual analogy
        st.markdown("### Think of it like this:")
        st.markdown(f"- Both fractions have pieces of the same size (/{frac1[1]})")
        st.markdown(f"- One has {frac1[0]} pieces, the other has {frac2[0]} pieces")
        st.markdown(f"- {max(frac1[0], frac2[0])} pieces > {min(frac1[0], frac2[0])} pieces")
        
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