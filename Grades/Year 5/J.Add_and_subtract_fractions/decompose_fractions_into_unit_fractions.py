import streamlit as st
import random

def run():
    """
    Main function to run the Decompose Fractions into Unit Fractions practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/decompose_fractions_into_unit_fractions.py
    """
    # Initialize session state for difficulty and game state
    if "decompose_click_difficulty" not in st.session_state:
        st.session_state.decompose_click_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_values = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🧩 Decompose Fractions into Unit Fractions")
    st.markdown("*Fill in the missing numbers to write fractions as sums of unit fractions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decompose_click_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Small fractions (denominators 3-5)",
            2: "Medium fractions (denominators 6-8)",
            3: "Larger fractions (denominators 9-12)",
            4: "Complex fractions (denominators 13-16)",
            5: "Challenge mode (all denominators)"
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
        ### How to Play:
        1. Look at the fraction on the left (e.g., 3/5)
        2. Click the number buttons below to fill in the blanks
        3. Each blank should contain a unit fraction
        4. The sum should equal the original fraction
        
        ### What are Unit Fractions?
        - A unit fraction has **1** as the numerator
        - Examples: 1/2, 1/3, 1/4, 1/5, etc.
        
        ### Examples:
        - **2/3** = 1/3 + 1/3
        - **3/4** = 1/4 + 1/4 + 1/4
        - **4/5** = 1/5 + 1/5 + 1/5 + 1/5
        - **3/7** = 1/7 + 1/7 + 1/7
        
        ### Pattern to Remember:
        - For fraction n/d, you need **n** unit fractions of 1/d
        - Example: 3/7 needs three 1/7s
        
        ### Note:
        - We start with fractions like 2/3, 3/4, etc. (not 1/2)
        - This ensures meaningful decomposition practice
        
        ### Tips:
        - The denominator stays the same
        - Count how many parts you need (look at numerator)
        - All parts should be 1/denominator
        """)

def generate_new_question():
    """Generate a new decompose fractions question"""
    difficulty = st.session_state.decompose_click_difficulty
    
    try:
        # Set denominator range based on difficulty
        # Start from 3 to ensure meaningful decomposition (2/3, 3/3, etc.)
        if difficulty == 1:
            denominator = random.randint(3, 5)
        elif difficulty == 2:
            denominator = random.randint(6, 8)
        elif difficulty == 3:
            denominator = random.randint(9, 12)
        elif difficulty == 4:
            denominator = random.randint(13, 16)
        else:  # difficulty == 5
            denominator = random.randint(3, 16)
        
        # Generate numerator
        # For meaningful decomposition, we want at least 2 unit fractions
        max_numerator = min(denominator - 1, 8)  # Cap at 8 for usability
        
        # Ensure numerator is at least 2 for proper decomposition
        if max_numerator >= 2:
            numerator = random.randint(2, max_numerator)
        else:
            # Fallback (shouldn't happen with denominator >= 3)
            numerator = max_numerator
            
    except ValueError as e:
        # Fallback to safe values if there's any issue
        denominator = 4
        numerator = 3
    
    # Create button options (include correct answer and distractors)
    options = []
    
    # Always include the correct unit fraction
    options.append(f"1/{denominator}")
    
    # Add some distractors with same denominator
    for i in range(2, min(denominator, 6)):
        if len(options) < 5:
            options.append(f"{i}/{denominator}")
    
    # Add distractors with different denominators
    distractor_denominators = [d for d in range(2, 20) if d != denominator]
    random.shuffle(distractor_denominators)
    
    for d in distractor_denominators:
        if len(options) < 5:
            options.append(f"1/{d}")
    
    # Ensure we have exactly 5 options
    while len(options) < 5:
        # Add random fractions as last resort
        rand_num = random.randint(1, 5)
        rand_denom = random.choice([d for d in range(2, 10) if d != denominator])
        rand_frac = f"{rand_num}/{rand_denom}"
        if rand_frac not in options:
            options.append(rand_frac)
    
    # Keep only 5 options
    options = options[:5]
    
    # Sort options by denominator then numerator for consistent display
    def fraction_sort_key(frac):
        parts = frac.split('/')
        return (int(parts[1]), int(parts[0]))
    
    options.sort(key=fraction_sort_key)
    
    # Initialize selected values
    st.session_state.selected_values = [""] * numerator
    
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "fraction": f"{numerator}/{denominator}",
        "options": options,
        "correct_answer": f"1/{denominator}"
    }
    st.session_state.correct_answer = [f"1/{denominator}"] * numerator
    st.session_state.current_question = f"Fill in the missing numbers to write {numerator}/{denominator} as a sum of unit fractions."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the equation with blanks
    st.markdown("### Fill in the blanks:")
    st.markdown("")  # Add space
    
    # Create container for better spacing
    equation_container = st.container()
    
    with equation_container:
        # Calculate total columns needed
        total_cols = 2 + (data["numerator"] * 2 - 1)  # fraction + = + blanks + plus signs
        cols = st.columns(total_cols)
        
        # Original fraction
        with cols[0]:
            st.markdown(f"""
            <div style="
                background-color: #f5f5f5;
                border: 3px solid #333;
                padding: 15px 25px;
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 10px;
                color: #333;
            ">{data['fraction']}</div>
            """, unsafe_allow_html=True)
        
        # Equal sign
        with cols[1]:
            st.markdown(f"""
            <div style="
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                padding: 15px;
                margin-top: 10px;
                color: #333;
            ">=</div>
            """, unsafe_allow_html=True)
        
        # Blanks and plus signs
        for i in range(data["numerator"]):
            blank_col_idx = 2 + (i * 2)
            
            # Display blank or filled value
            with cols[blank_col_idx]:
                value = st.session_state.selected_values[i] if i < len(st.session_state.selected_values) else ""
                
                if value:
                    # Filled box with better contrast
                    st.markdown(f"""
                    <div style="
                        background-color: #2196F3;
                        border: 3px solid #1976D2;
                        padding: 15px;
                        text-align: center;
                        font-size: 22px;
                        font-weight: bold;
                        border-radius: 6px;
                        margin-top: 10px;
                        min-height: 60px;
                        min-width: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                    ">{value}</div>
                    """, unsafe_allow_html=True)
                else:
                    # Empty box - more visible with light blue background
                    st.markdown(f"""
                    <div style="
                        background-color: #e6f3ff;
                        border: 3px solid #2196F3;
                        padding: 15px;
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                        border-radius: 6px;
                        margin-top: 10px;
                        min-height: 60px;
                        min-width: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                    ">&nbsp;</div>
                    """, unsafe_allow_html=True)
            
            # Plus sign (if not last blank)
            if i < data["numerator"] - 1:
                plus_col_idx = blank_col_idx + 1
                with cols[plus_col_idx]:
                    st.markdown(f"""
                    <div style="
                        text-align: center;
                        font-size: 32px;
                        font-weight: bold;
                        padding: 15px;
                        margin-top: 10px;
                        color: #333;
                    ">+</div>
                    """, unsafe_allow_html=True)
    
    # Number buttons
    st.markdown("")  # Add space
    st.markdown("### Click to select:")
    
    button_cols = st.columns(len(data["options"]))
    
    for idx, option in enumerate(data["options"]):
        with button_cols[idx]:
            # Make all buttons secondary for now to ensure visibility
            if st.button(
                option,
                key=f"option_{idx}",
                use_container_width=True,
                type="secondary"
            ):
                # Find the first empty slot
                for i in range(len(st.session_state.selected_values)):
                    if st.session_state.selected_values[i] == "":
                        st.session_state.selected_values[i] = option
                        st.rerun()
                        break
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear All", type="secondary", use_container_width=True):
            st.session_state.selected_values = [""] * data["numerator"]
            st.rerun()
    
    with col2:
        if st.button("⬅️ Remove Last", type="secondary", use_container_width=True):
            # Find the last filled slot and clear it
            for i in range(len(st.session_state.selected_values) - 1, -1, -1):
                if st.session_state.selected_values[i] != "":
                    st.session_state.selected_values[i] = ""
                    st.rerun()
                    break
    
    with col3:
        # Check if all blanks are filled
        all_filled = all(val != "" for val in st.session_state.selected_values)
        if all_filled:
            submit_button = st.button(
                "✅ Submit",
                type="primary",
                use_container_width=True
            )
            
            if submit_button:
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
        else:
            st.button(
                "✅ Submit",
                type="secondary",
                use_container_width=True,
                disabled=True
            )
    
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
    user_answer = st.session_state.selected_values
    correct_answer = st.session_state.correct_answer
    
    # Check if answer is correct
    is_correct = all(val == data["correct_answer"] for val in user_answer)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete equation
        equation = f"{data['fraction']} = " + " + ".join(correct_answer)
        st.success(f"✓ {equation}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.decompose_click_difficulty
        st.session_state.decompose_click_difficulty = min(
            st.session_state.decompose_click_difficulty + 1, 5
        )
        
        if st.session_state.decompose_click_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've mastered decomposing fractions!**")
        elif old_difficulty < st.session_state.decompose_click_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decompose_click_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        user_equation = f"{data['fraction']} = " + " + ".join(user_answer)
        st.error(f"You entered: {user_equation}")
        
        # Show the correct answer
        correct_equation = f"{data['fraction']} = " + " + ".join(correct_answer)
        st.success(f"The correct answer is: {correct_equation}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.decompose_click_difficulty
        st.session_state.decompose_click_difficulty = max(
            st.session_state.decompose_click_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decompose_click_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.decompose_click_difficulty}. Keep practicing!**")
        
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
        
        **Step 1: Understand the fraction**
        - {numerator}/{denominator} means {numerator} parts out of {denominator} equal parts
        
        **Step 2: What is a unit fraction?**
        - A unit fraction has 1 as the numerator
        - For denominator {denominator}, the unit fraction is 1/{denominator}
        
        **Step 3: How many unit fractions do we need?**
        - We need {numerator} parts
        - Each part is 1/{denominator}
        - So we need {numerator} unit fractions of 1/{denominator}
        
        **Step 4: Write the decomposition**
        {numerator}/{denominator} = {"1/" + str(denominator) + " + " + " + ".join(["1/" + str(denominator)] * (numerator - 1))}
        
        **Why does this work?**
        - When we add fractions with the same denominator, we add the numerators
        - 1/{denominator} + 1/{denominator} + ... = {numerator}/{denominator}
        - We're adding 1 exactly {numerator} times, which gives us {numerator}
        
        **Remember:**
        - The numerator tells you HOW MANY unit fractions
        - The denominator tells you WHICH unit fraction to use
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_values = []
    if "user_answer" in st.session_state:
        del st.session_state.user_answer