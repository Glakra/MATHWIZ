import streamlit as st
import random

def run():
    """
    Main function to run the Choose the Multiples activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/choose_the_multiples_of_a_given_number_up_to_12.py
    """
    # Initialize session state
    if "multiples_difficulty" not in st.session_state:
        st.session_state.multiples_difficulty = 1
    
    if "current_multiples_problem" not in st.session_state:
        st.session_state.current_multiples_problem = None
        st.session_state.multiples_answers = None
        st.session_state.multiples_feedback = False
        st.session_state.multiples_submitted = False
        st.session_state.multiples_data = {}
    
    # Initialize selected options
    if "multiples_selected_options" not in st.session_state:
        st.session_state.multiples_selected_options = set()
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🎯 Choose the Multiples")
    st.markdown("*Select all numbers that are multiples of the given number*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiples_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_multiples_problem is None:
        generate_multiples_problem()
    
    # Display current question
    display_multiples_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Multiples**", expanded=False):
        st.markdown("""
        ### What are Multiples?
        
        **Multiples** of a number are what you get when you **multiply that number by whole numbers** (1, 2, 3, 4, 5...).
        
        ### Example: Multiples of 6
        - **6 × 1 = 6** → 6 is a multiple of 6
        - **6 × 2 = 12** → 12 is a multiple of 6  
        - **6 × 3 = 18** → 18 is a multiple of 6
        - **6 × 4 = 24** → 24 is a multiple of 6
        - **6 × 5 = 30** → 30 is a multiple of 6
        
        **So multiples of 6 are: 6, 12, 18, 24, 30, 36, 42, 48, 54, 60...**
        
        ### How to Check if a Number is a Multiple:
        
        #### **Method 1: Division Test**
        - **Divide the number by the given number**
        - **If there's no remainder, it's a multiple**
        
        **Example:** Is 48 a multiple of 6?
        - 48 ÷ 6 = 8 (exactly, no remainder)
        - **✅ Yes, 48 is a multiple of 6**
        
        **Example:** Is 50 a multiple of 6?
        - 50 ÷ 6 = 8 remainder 2
        - **❌ No, 50 is not a multiple of 6**
        
        #### **Method 2: Skip Counting**
        - **Count by the given number**
        - **See if you land on the target number**
        
        **Example:** Multiples of 4
        - 4, 8, 12, 16, 20, 24, 28, 32, 36, 40...
        - Is 28 a multiple of 4? ✅ Yes (it appears in the list)
        - Is 30 a multiple of 4? ❌ No (it doesn't appear)
        
        ### Quick Reference - Multiples up to 60:
        
        **Multiples of 2:** 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30...  
        **Multiples of 3:** 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45...  
        **Multiples of 4:** 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60...  
        **Multiples of 5:** 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60...  
        **Multiples of 6:** 6, 12, 18, 24, 30, 36, 42, 48, 54, 60...  
        **Multiples of 7:** 7, 14, 21, 28, 35, 42, 49, 56...  
        **Multiples of 8:** 8, 16, 24, 32, 40, 48, 56...  
        **Multiples of 9:** 9, 18, 27, 36, 45, 54...  
        **Multiples of 10:** 10, 20, 30, 40, 50, 60...  
        **Multiples of 11:** 11, 22, 33, 44, 55...  
        **Multiples of 12:** 12, 24, 36, 48, 60...  
        
        ### Tips for Success:
        - **Remember your times tables** (very helpful!)
        - **Use division to check** when unsure
        - **Look for patterns** (multiples of 5 end in 0 or 5)
        - **Multiple answers possible** - select ALL correct options
        - **Even numbers** are always multiples of 2
        
        ### Common Mistakes:
        - ❌ Forgetting that a number is a multiple of itself
        - ❌ Selecting only one answer when multiple are correct
        - ❌ Confusing multiples with factors
        - ❌ Not checking all options carefully
        """)

def generate_multiples_problem():
    """Generate unlimited multiples problems using algorithmic generation"""
    difficulty = st.session_state.multiples_difficulty
    
    # Choose base number based on difficulty
    if difficulty == 1:
        # Level 1: Easy multiples (2, 3, 5, 10)
        base_number = random.choice([2, 3, 5, 10])
        max_multiple = random.randint(8, 15)  # Keep multiples reasonable
        max_range = 60
    elif difficulty == 2:
        # Level 2: Medium multiples (4, 6, 8)
        base_number = random.choice([4, 6, 8])
        max_multiple = random.randint(8, 18)
        max_range = 80
    elif difficulty == 3:
        # Level 3: All numbers 2-10
        base_number = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        max_multiple = random.randint(10, 20)
        max_range = 100
    elif difficulty == 4:
        # Level 4: Include 11, 12 and larger ranges
        base_number = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        max_multiple = random.randint(10, 25)
        max_range = 150
    else:  # difficulty == 5
        # Level 5: All numbers with challenging ranges
        base_number = random.choice([4, 5, 6, 7, 8, 9, 10, 11, 12])
        max_multiple = random.randint(15, 30)
        max_range = 200
    
    # Generate multiples of the base number
    possible_multiples = [base_number * i for i in range(1, max_multiple + 1) if base_number * i <= max_range]
    
    # Decide how many correct answers to include (1-3)
    num_correct = random.choice([1, 1, 2, 2, 3])  # Weighted toward 1-2 correct answers
    
    # Select correct answers (multiples)
    correct_answers = random.sample(possible_multiples, min(num_correct, len(possible_multiples)))
    
    # Generate non-multiples (wrong answers)
    num_wrong = 4 - num_correct
    wrong_answers = []
    
    attempts = 0
    while len(wrong_answers) < num_wrong and attempts < 50:
        # Generate a number that's NOT a multiple
        if difficulty <= 2:
            candidate = random.randint(1, max_range)
        else:
            candidate = random.randint(1, max_range)
        
        # Make sure it's not a multiple and not already used
        if (candidate % base_number != 0 and 
            candidate not in correct_answers and 
            candidate not in wrong_answers):
            wrong_answers.append(candidate)
        
        attempts += 1
    
    # If we couldn't generate enough wrong answers, create some systematically
    while len(wrong_answers) < num_wrong:
        # Create near-misses (add/subtract 1-3 from multiples)
        base_multiple = random.choice(possible_multiples)
        offset = random.choice([-3, -2, -1, 1, 2, 3])
        candidate = base_multiple + offset
        
        if (candidate > 0 and 
            candidate % base_number != 0 and 
            candidate not in correct_answers and 
            candidate not in wrong_answers):
            wrong_answers.append(candidate)
        else:
            # Last resort: just pick a random non-multiple
            candidate = random.randint(1, max_range)
            if candidate % base_number != 0 and candidate not in correct_answers + wrong_answers:
                wrong_answers.append(candidate)
    
    # Combine and shuffle all options
    all_options = correct_answers + wrong_answers
    random.shuffle(all_options)
    
    # Ensure we have exactly 4 options
    all_options = all_options[:4]
    
    # Determine which of the final 4 are correct
    final_correct = [num for num in all_options if num % base_number == 0]
    
    st.session_state.multiples_data = {
        "base_number": base_number,
        "options": all_options,
        "correct_answers": final_correct
    }
    st.session_state.multiples_answers = set(final_correct)
    st.session_state.current_multiples_problem = f"Which of the following numbers are multiples of {base_number}?"

def display_multiples_problem():
    """Display the current multiples problem with clickable tiles"""
    data = st.session_state.multiples_data
    base_number = data["base_number"]
    options = data["options"]
    
    # Display the question with clear formatting
    st.markdown("### 🎯 Question:")
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #2c3e50;
    ">
        Which of the following numbers are multiples of {base_number}?
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**💡 Tip:** You can select multiple answers - click all that apply!")
    st.markdown("")
    
    # Create clickable tiles in a 2x2 grid
    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")
    columns = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    # Display each option as a clickable tile
    for i, option in enumerate(options):
        with columns[i]:
            # Determine if this tile is selected
            is_selected = option in st.session_state.multiples_selected_options
            
            # Create button with conditional styling
            button_type = "primary" if is_selected else "secondary"
            button_text = f"✅ {option}" if is_selected else str(option)
            
            if st.button(
                button_text,
                key=f"mult_tile_{i}",
                use_container_width=True,
                type=button_type,
                help=f"Click to select/deselect: {option}"
            ):
                # Toggle selection
                if option in st.session_state.multiples_selected_options:
                    st.session_state.multiples_selected_options.remove(option)
                else:
                    st.session_state.multiples_selected_options.add(option)
                st.rerun()
    
    # Show current selections
    st.markdown("")
    if st.session_state.multiples_selected_options:
        selected_list = sorted(list(st.session_state.multiples_selected_options))
        st.success(f"**Selected:** {', '.join(map(str, selected_list))}")
    else:
        st.info("👆 **Click on the tiles to select your answers**")
    
    # Submit section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button(
            "✅ Submit", 
            type="primary", 
            use_container_width=True,
            disabled=len(st.session_state.multiples_selected_options) == 0
        )
    
    # Handle submission
    if submit_button and len(st.session_state.multiples_selected_options) > 0:
        st.session_state.multiples_user_answers = st.session_state.multiples_selected_options.copy()
        st.session_state.multiples_feedback = True
        st.session_state.multiples_submitted = True
        st.rerun()
    
    # Show feedback and next button
    handle_multiples_feedback()

def handle_multiples_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("multiples_feedback", False):
        show_multiples_feedback()
    
    if st.session_state.get("multiples_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_multiples_state()
                st.rerun()

def show_multiples_feedback():
    """Display feedback for the multiples problem"""
    user_answers = st.session_state.get("multiples_user_answers", set())
    correct_answers = st.session_state.get("multiples_answers", set())
    data = st.session_state.get("multiples_data", {})
    
    if not data or correct_answers is None:
        return
    
    base_number = data["base_number"]
    options = data["options"]
    
    # Check if answers are exactly correct
    is_perfect = user_answers == correct_answers
    
    if is_perfect:
        if len(correct_answers) == 1:
            st.success(f"🎉 **Perfect!** You found the multiple of {base_number}.")
        else:
            st.success(f"🎉 **Excellent!** You found all {len(correct_answers)} multiples of {base_number}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.multiples_difficulty
        st.session_state.multiples_difficulty = min(
            st.session_state.multiples_difficulty + 1, 5
        )
        
        if st.session_state.multiples_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered identifying multiples!**")
        elif old_difficulty < st.session_state.multiples_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.multiples_difficulty}**")
        
        show_multiples_explanation(correct=True)
    
    else:
        # Provide specific feedback
        missed = correct_answers - user_answers
        incorrect = user_answers - correct_answers
        
        feedback_parts = []
        if missed:
            feedback_parts.append(f"missed {', '.join(map(str, sorted(missed)))}")
        if incorrect:
            feedback_parts.append(f"incorrectly selected {', '.join(map(str, sorted(incorrect)))}")
        
        feedback_text = " and ".join(feedback_parts)
        st.error(f"❌ **Not quite.** You {feedback_text}.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.multiples_difficulty
        st.session_state.multiples_difficulty = max(
            st.session_state.multiples_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.multiples_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.multiples_difficulty}. Keep practicing!**")
        
        show_multiples_explanation(correct=False)

def show_multiples_explanation(correct=True):
    """Show explanation for the multiples problem"""
    data = st.session_state.get("multiples_data", {})
    correct_answers = st.session_state.get("multiples_answers", set())
    user_answers = st.session_state.get("multiples_user_answers", set())
    
    if not data or correct_answers is None:
        return
        
    base_number = data["base_number"]
    options = data["options"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Multiples of {base_number} Explanation:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Base Number: {base_number}
        ### Correct Answers: {', '.join(map(str, sorted(correct_answers))) if correct_answers else 'None'}
        
        ### Analysis of each option:
        """)
        
        # Analyze each option
        for option in options:
            quotient = option // base_number
            remainder = option % base_number
            is_multiple = remainder == 0
            
            if option in correct_answers:
                st.markdown(f"- **{option}** ✅ **MULTIPLE**: {option} ÷ {base_number} = {quotient} (exactly, no remainder)")
                st.markdown(f"  - *Check: {base_number} × {quotient} = {base_number * quotient}*")
            else:
                st.markdown(f"- **{option}** ❌ **NOT a multiple**: {option} ÷ {base_number} = {quotient} remainder {remainder}")
                if remainder == 1:
                    st.markdown(f"  - *{option} is 1 more than {base_number * quotient}*")
                elif remainder == base_number - 1:
                    st.markdown(f"  - *{option} is 1 less than {base_number * (quotient + 1)}*")
        
        # Show multiplication table section for reference
        st.markdown(f"""
        ### 📚 Multiplication table for {base_number}:
        """)
        
        # Show first 10-12 multiples
        multiples_list = []
        for i in range(1, 13):
            multiple = base_number * i
            if multiple <= 200:  # Don't show too large numbers
                multiples_list.append(f"{base_number} × {i} = {multiple}")
            if len(multiples_list) >= 10:
                break
        
        # Display in two columns
        col1, col2 = st.columns(2)
        mid_point = len(multiples_list) // 2
        
        with col1:
            for item in multiples_list[:mid_point]:
                st.markdown(f"- {item}")
        
        with col2:
            for item in multiples_list[mid_point:]:
                st.markdown(f"- {item}")
        
        # Quick check method
        st.markdown(f"""
        ### 🔍 Quick Check Method:
        **To check if a number is a multiple of {base_number}:**
        1. **Divide the number by {base_number}**
        2. **If there's no remainder, it's a multiple**
        3. **If there's a remainder, it's not a multiple**
        
        **Example:** Is 42 a multiple of {base_number}?
        - 42 ÷ {base_number} = {42 // base_number} remainder {42 % base_number}
        - **Answer:** {'✅ Yes' if 42 % base_number == 0 else '❌ No'}
        """)

def reset_multiples_state():
    """Reset the state for next problem"""
    st.session_state.current_multiples_problem = None
    st.session_state.multiples_answers = None
    st.session_state.multiples_feedback = False
    st.session_state.multiples_submitted = False
    st.session_state.multiples_data = {}
    st.session_state.multiples_selected_options = set()  # Reset selections
    
    if "multiples_user_answers" in st.session_state:
        del st.session_state.multiples_user_answers