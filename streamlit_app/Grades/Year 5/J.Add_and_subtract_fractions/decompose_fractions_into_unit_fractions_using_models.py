import streamlit as st
import random

def run():
    """
    Main function to run the Decompose Fractions into Unit Fractions practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/decompose_fractions_into_unit_fractions_using_models.py
    """
    # Initialize session state for difficulty and game state
    if "decompose_difficulty" not in st.session_state:
        st.session_state.decompose_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🧩 Decompose Fractions into Unit Fractions")
    st.markdown("*Break down fractions into sums of unit fractions using visual models*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decompose_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Small denominators (2-6)",
            2: "Medium denominators (7-10)",
            3: "Larger denominators (11-15)",
            4: "Complex denominators (16-20)",
            5: "Challenge mode (mixed)"
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
        ### What are Unit Fractions?
        A **unit fraction** has 1 as the numerator (top number).
        Examples: 1/2, 1/3, 1/4, 1/5, etc.
        
        ### How to Decompose:
        Any fraction can be written as a sum of unit fractions.
        
        **Example:** 3/5 = 1/5 + 1/5 + 1/5
        - We need 3 parts
        - Each part is 1/5
        - So we add 1/5 three times
        
        ### More Examples:
        - **2/3** = 1/3 + 1/3
        - **4/7** = 1/7 + 1/7 + 1/7 + 1/7
        - **5/8** = 1/8 + 1/8 + 1/8 + 1/8 + 1/8
        
        ### Visual Understanding:
        - Look at the fraction strip
        - Count how many parts are shaded
        - Each shaded part represents one unit fraction
        
        ### Remember:
        The number of unit fractions = the numerator of the original fraction
        """)

def generate_new_question():
    """Generate a new decompose fractions question"""
    difficulty = st.session_state.decompose_difficulty
    
    # Set denominator range based on difficulty
    if difficulty == 1:
        denominator = random.randint(2, 6)
    elif difficulty == 2:
        denominator = random.randint(7, 10)
    elif difficulty == 3:
        denominator = random.randint(11, 15)
    elif difficulty == 4:
        denominator = random.randint(16, 20)
    else:  # difficulty == 5
        denominator = random.randint(2, 20)
    
    # Generate numerator (always less than denominator for proper fractions)
    max_numerator = min(denominator - 1, 12)  # Cap at 12 for readability
    numerator = random.randint(1, max_numerator)
    
    # Create the correct decomposition
    unit_fraction = f"1/{denominator}"
    correct_parts = [unit_fraction] * numerator
    
    # Generate wrong answers (distractors)
    options = []
    
    # Correct answer
    options.append(correct_parts)
    
    # Wrong answer 1: One too few unit fractions
    if numerator > 1:
        wrong1 = [unit_fraction] * (numerator - 1)
        options.append(wrong1)
    
    # Wrong answer 2: One too many unit fractions
    if numerator < denominator - 1:
        wrong2 = [unit_fraction] * (numerator + 1)
        options.append(wrong2)
    
    # Wrong answer 3: Different unit fraction (if possible)
    if denominator > 2:
        wrong_denominator = denominator - 1 if numerator < denominator - 1 else denominator + 1
        wrong3 = [f"1/{wrong_denominator}"] * numerator
        options.append(wrong3)
    
    # Wrong answer 4: Mixed denominators
    if numerator > 2:
        wrong4 = [unit_fraction] * (numerator - 2) + [f"2/{denominator}"]
        options.append(wrong4)
    
    # Ensure we have exactly 4 options
    while len(options) < 4:
        # Add a random wrong decomposition
        random_num = random.randint(1, max(numerator, denominator - 1))
        random_denom = random.choice([d for d in range(2, 21) if d != denominator])
        wrong_option = [f"1/{random_denom}"] * random_num
        if wrong_option not in options:
            options.append(wrong_option)
    
    # Keep only 4 options
    options = options[:4]
    
    # Shuffle options
    random.shuffle(options)
    
    # Find the index of the correct answer
    correct_index = options.index(correct_parts)
    
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "fraction": f"{numerator}/{denominator}",
        "options": options,
        "correct_index": correct_index
    }
    st.session_state.correct_answer = correct_index
    st.session_state.current_question = f"How do you write {numerator}/{denominator} as a sum of unit fractions?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("Use the fraction strips to help.")
    
    # Draw the visual fraction model
    draw_fraction_model(data["numerator"], data["denominator"])
    
    # Display options
    st.markdown("### Choose your answer:")
    
    with st.form("answer_form", clear_on_submit=False):
        # Create radio buttons for each option
        option_strings = []
        for i, option in enumerate(data["options"]):
            option_str = " + ".join(option)
            option_strings.append(option_str)
        
        user_choice = st.radio(
            "Select the correct decomposition:",
            options=range(len(option_strings)),
            format_func=lambda x: option_strings[x],
            key="decompose_choice",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "✅ Submit Answer", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            st.session_state.user_answer = user_choice
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def draw_fraction_model(numerator, denominator):
    """Draw a visual fraction strip model"""
    # Create the whole bar (1)
    st.markdown("""
    <div style="
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        font-size: 20px;
        font-weight: bold;
        border-radius: 5px;
    ">1</div>
    """, unsafe_allow_html=True)
    
    # Create the fraction bar divided into parts
    cols = st.columns(denominator)
    
    for i in range(denominator):
        with cols[i]:
            if i < numerator:
                # Shaded part
                st.markdown(f"""
                <div style="
                    background-color: #cfe2ff;
                    border: 1px solid #084298;
                    padding: 20px 5px;
                    text-align: center;
                    margin: 2px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #084298;
                    border-radius: 3px;
                ">1<br>—<br>{denominator}</div>
                """, unsafe_allow_html=True)
            else:
                # Unshaded part
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    padding: 20px 5px;
                    text-align: center;
                    margin: 2px;
                    font-size: 14px;
                    color: #6c757d;
                    border-radius: 3px;
                ">1<br>—<br>{denominator}</div>
                """, unsafe_allow_html=True)
    
    # Add caption
    st.caption(f"The fraction {numerator}/{denominator} is shown with {numerator} shaded parts out of {denominator} equal parts.")

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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the correct decomposition
        correct_decomposition = " + ".join(data["options"][correct_answer])
        st.success(f"✓ {data['fraction']} = {correct_decomposition}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.decompose_difficulty
        st.session_state.decompose_difficulty = min(
            st.session_state.decompose_difficulty + 1, 5
        )
        
        if st.session_state.decompose_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decomposing fractions!**")
        elif old_difficulty < st.session_state.decompose_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decompose_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they selected
        user_decomposition = " + ".join(data["options"][user_answer])
        st.error(f"You selected: {user_decomposition}")
        
        # Show the correct answer
        correct_decomposition = " + ".join(data["options"][correct_answer])
        st.success(f"The correct answer is: {data['fraction']} = {correct_decomposition}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.decompose_difficulty
        st.session_state.decompose_difficulty = max(
            st.session_state.decompose_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decompose_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.decompose_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    data = st.session_state.question_data
    numerator = data["numerator"]
    denominator = data["denominator"]
    
    with st.expander("📖 **Understanding the Answer**", expanded=True):
        st.markdown(f"""
        ### Decomposing {numerator}/{denominator} into Unit Fractions
        
        **What does {numerator}/{denominator} mean?**
        - The denominator ({denominator}) tells us the fraction bar is divided into {denominator} equal parts
        - The numerator ({numerator}) tells us we have {numerator} of those parts
        
        **Unit Fraction:**
        - Each part is 1/{denominator} (one part out of {denominator})
        - This is called a unit fraction because the numerator is 1
        
        **Decomposition:**
        - Since we have {numerator} parts
        - And each part is 1/{denominator}
        - We write: {numerator}/{denominator} = {"1/" + str(denominator) + " + " + " + ".join(["1/" + str(denominator)] * (numerator - 1))}
        
        **Visual Understanding:**
        - Look at the fraction strip above
        - Count the shaded parts: there are {numerator}
        - Each shaded part represents 1/{denominator}
        - So we add 1/{denominator} exactly {numerator} times
        
        **Remember:**
        To decompose any fraction a/b into unit fractions:
        - Write 1/b (the unit fraction)
        - Add it 'a' times (as many times as the numerator)
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