import streamlit as st
import random

def run():
    """
    Main function to run the Choose Numbers with a Particular Quotient activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/choose_numbers_with_a_particular_quotient.py
    """
    # Initialize session state
    if "quotient_difficulty" not in st.session_state:
        st.session_state.quotient_difficulty = 1
    
    if "current_quotient_problem" not in st.session_state:
        st.session_state.current_quotient_problem = None
        st.session_state.quotient_answer = None
        st.session_state.quotient_feedback = False
        st.session_state.quotient_submitted = False
        st.session_state.quotient_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("🎯 Choose Numbers with a Particular Quotient")
    st.markdown("*Find two numbers that create the given quotient when divided*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.quotient_difficulty
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
    if st.session_state.current_quotient_problem is None:
        generate_quotient_problem()
    
    # Display current question
    display_quotient_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Find Numbers with a Particular Quotient:
        
        **What is a quotient?** The quotient is the answer when you divide one number by another.
        
        **Strategy:**
        1. **Look at the target quotient** (the answer you need)
        2. **Check each pair of numbers** from the box
        3. **Try both ways:** A ÷ B and B ÷ A
        4. **Find the pair** that gives the target quotient
        
        ### Example:
        **Numbers:** 2, 8, 10, 15  
        **Target quotient:** 5
        
        **Try different combinations:**
        - 10 ÷ 2 = 5 ✅ (This works!)
        - 8 ÷ 2 = 4 (Not 5)
        - 15 ÷ 3 = 5 (But 3 isn't in the box)
        
        **Answer:** 10 and 2
        
        ### Tips:
        - **Work systematically** - try each number as the dividend
        - **Remember division facts** - they help you spot answers quickly
        - **Check your work** - multiply your answer back
        - **Both orders matter** - A ÷ B might not equal B ÷ A
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple quotients (2, 3, 4, 5)
        - **🟠 Level 3:** Medium quotients (6, 7, 8, 9)
        - **🔴 Level 4-5:** Larger quotients and more numbers
        """)

def generate_quotient_problem():
    """Generate a quotient problem based on difficulty level"""
    difficulty = st.session_state.quotient_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple quotients with 4 numbers
        problems = [
            {"numbers": [2, 6, 8, 12], "quotient": 3, "answer": (6, 2), "alt_answer": (12, 4)},  # 6÷2=3 or 12÷4=3
            {"numbers": [3, 8, 12, 15], "quotient": 4, "answer": (12, 3), "alt_answer": None},  # 12÷3=4
            {"numbers": [2, 4, 10, 14], "quotient": 5, "answer": (10, 2), "alt_answer": None},  # 10÷2=5
            {"numbers": [2, 6, 14, 16], "quotient": 2, "answer": (6, 3), "alt_answer": (14, 7)},  # Multiple solutions
            {"numbers": [3, 9, 15, 21], "quotient": 3, "answer": (9, 3), "alt_answer": (15, 5)},  # 9÷3=3
            {"numbers": [4, 8, 16, 20], "quotient": 4, "answer": (16, 4), "alt_answer": (20, 5)},  # 16÷4=4
        ]
    elif difficulty == 2:
        # Level 2: Slightly harder quotients
        problems = [
            {"numbers": [2, 18, 53, 78], "quotient": 9, "answer": (18, 2), "alt_answer": None},  # From your image
            {"numbers": [2, 8, 10, 15], "quotient": 5, "answer": (10, 2), "alt_answer": None},  # From your image
            {"numbers": [3, 7, 21, 28], "quotient": 7, "answer": (21, 3), "alt_answer": (28, 4)},  # 21÷3=7
            {"numbers": [4, 6, 24, 30], "quotient": 6, "answer": (24, 4), "alt_answer": (30, 5)},  # 24÷4=6
            {"numbers": [5, 8, 40, 45], "quotient": 8, "answer": (40, 5), "alt_answer": None},  # 40÷5=8
            {"numbers": [2, 9, 18, 36], "quotient": 9, "answer": (18, 2), "alt_answer": (36, 4)},  # 18÷2=9
        ]
    elif difficulty == 3:
        # Level 3: More numbers and medium quotients
        problems = [
            {"numbers": [3, 5, 7, 35, 42], "quotient": 7, "answer": (35, 5), "alt_answer": (42, 6)},  # 35÷5=7
            {"numbers": [2, 4, 6, 48, 54], "quotient": 8, "answer": (48, 6), "alt_answer": None},  # 48÷6=8
            {"numbers": [3, 6, 8, 54, 72], "quotient": 9, "answer": (54, 6), "alt_answer": (72, 8)},  # 54÷6=9
            {"numbers": [4, 5, 7, 28, 35], "quotient": 7, "answer": (28, 4), "alt_answer": (35, 5)},  # 28÷4=7
            {"numbers": [2, 8, 9, 72, 81], "quotient": 9, "answer": (72, 8), "alt_answer": (81, 9)},  # 72÷8=9
            {"numbers": [3, 4, 6, 24, 36], "quotient": 6, "answer": (24, 4), "alt_answer": (36, 6)},  # 24÷4=6
        ]
    elif difficulty == 4:
        # Level 4: Larger quotients and more complex
        problems = [
            {"numbers": [3, 5, 8, 11, 88], "quotient": 11, "answer": (88, 8), "alt_answer": None},  # 88÷8=11
            {"numbers": [2, 4, 12, 15, 60], "quotient": 12, "answer": (60, 5), "alt_answer": None},  # 60÷5=12  
            {"numbers": [3, 7, 9, 13, 91], "quotient": 13, "answer": (91, 7), "alt_answer": None},  # 91÷7=13
            {"numbers": [4, 6, 8, 14, 84], "quotient": 14, "answer": (84, 6), "alt_answer": None},  # 84÷6=14
            {"numbers": [2, 5, 10, 16, 80], "quotient": 16, "answer": (80, 5), "alt_answer": None},  # 80÷5=16
            {"numbers": [3, 6, 9, 15, 90], "quotient": 15, "answer": (90, 6), "alt_answer": None},  # 90÷6=15
        ]
    else:  # difficulty == 5
        # Level 5: Very challenging with 6 numbers
        problems = [
            {"numbers": [2, 6, 8, 12, 17, 102], "quotient": 17, "answer": (102, 6), "alt_answer": None},  # 102÷6=17
            {"numbers": [3, 5, 7, 19, 21, 95], "quotient": 19, "answer": (95, 5), "alt_answer": None},  # 95÷5=19
            {"numbers": [4, 6, 9, 18, 23, 92], "quotient": 23, "answer": (92, 4), "alt_answer": None},  # 92÷4=23
            {"numbers": [2, 8, 11, 16, 29, 232], "quotient": 29, "answer": (232, 8), "alt_answer": None},  # 232÷8=29
            {"numbers": [3, 7, 9, 31, 93, 124], "quotient": 31, "answer": (93, 3), "alt_answer": (124, 4)},  # 93÷3=31
            {"numbers": [5, 6, 13, 37, 65, 185], "quotient": 37, "answer": (185, 5), "alt_answer": None},  # 185÷5=37
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    st.session_state.quotient_data = problem
    st.session_state.quotient_answer = problem["answer"]
    st.session_state.current_quotient_problem = f"Choose two numbers that have a quotient of {problem['quotient']}"

def display_quotient_problem():
    """Display the current quotient problem interface"""
    data = st.session_state.quotient_data
    numbers = data["numbers"]
    quotient = data["quotient"]
    
    # Display instruction
    st.markdown("### 🎯 Choose two numbers from the box to complete the sentence:")
    
    # Display the number box
    numbers_html = ""
    for num in numbers:
        numbers_html += f'<span style="background-color: #e8d5f2; padding: 8px 15px; margin: 5px; border-radius: 8px; font-size: 18px; font-weight: bold; color: #6f42c1;">{num}</span>'
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 20px 0;
    ">
        {numbers_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Create the sentence completion interface
    with st.form("quotient_form", clear_on_submit=False):
        # Randomly choose which format to display
        format_type = random.choice(["sentence", "equation"]) if "format_type" not in st.session_state else st.session_state.get("format_type", "sentence")
        
        if format_type == "sentence":
            # Format like "__ and __ have a quotient of 9"
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            
            with col1:
                first_number = st.selectbox("", [""] + numbers, key="first_select", label_visibility="collapsed")
            with col2:
                st.markdown("<div style='padding-top: 8px;'>and</div>", unsafe_allow_html=True)
            with col3:
                second_number = st.selectbox("", [""] + numbers, key="second_select", label_visibility="collapsed")
            with col4:
                st.markdown("<div style='padding-top: 8px;'>have a</div>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<div style='padding-top: 8px;'>quotient of <strong>{quotient}</strong>.</div>", unsafe_allow_html=True)
        
        else:
            # Format like "__ ÷ __ = 5"
            col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 1])
            
            with col1:
                first_number = st.selectbox("", [""] + numbers, key="first_select", label_visibility="collapsed")
            with col2:
                st.markdown("<div style='padding-top: 8px; text-align: center;'>÷</div>", unsafe_allow_html=True)
            with col3:
                second_number = st.selectbox("", [""] + numbers, key="second_select", label_visibility="collapsed")
            with col4:
                st.markdown("<div style='padding-top: 8px; text-align: center;'>=</div>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<div style='padding-top: 8px; text-align: center; font-weight: bold;'>{quotient}</div>", unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            if first_number and second_number and first_number != second_number:
                st.session_state.quotient_user_answer = (first_number, second_number)
                st.session_state.quotient_feedback = True
                st.session_state.quotient_submitted = True
            elif not first_number or not second_number:
                st.error("Please select two numbers")
            elif first_number == second_number:
                st.error("Please select two different numbers")
    
    # Show feedback and next button
    handle_quotient_feedback()

def handle_quotient_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.quotient_feedback:
        show_quotient_feedback()
    
    if st.session_state.quotient_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_quotient_state()
                st.rerun()

def show_quotient_feedback():
    """Display feedback for the quotient problem"""
    user_answer = st.session_state.quotient_user_answer
    correct_answer = st.session_state.quotient_answer
    data = st.session_state.quotient_data
    
    # Check if the user's answer is correct (either order)
    user_first, user_second = user_answer
    correct_first, correct_second = correct_answer
    
    # Check both possible correct answers
    is_correct = False
    division_check = ""
    
    # Try the main answer
    if (user_first == correct_first and user_second == correct_second) or \
       (user_first == correct_second and user_second == correct_first):
        is_correct = True
        if user_first > user_second:
            division_check = f"{user_first} ÷ {user_second} = {user_first // user_second}"
        else:
            division_check = f"{user_second} ÷ {user_first} = {user_second // user_first}"
    
    # Try alternative answer if exists
    elif data.get("alt_answer"):
        alt_first, alt_second = data["alt_answer"]
        if (user_first == alt_first and user_second == alt_second) or \
           (user_first == alt_second and user_second == alt_first):
            is_correct = True
            if user_first > user_second:
                division_check = f"{user_first} ÷ {user_second} = {user_first // user_second}"
            else:
                division_check = f"{user_second} ÷ {user_first} = {user_second // user_first}"
    
    # Also check if user found a valid quotient with their numbers
    if not is_correct:
        try:
            if user_first % user_second == 0 and user_first // user_second == data["quotient"]:
                is_correct = True
                division_check = f"{user_first} ÷ {user_second} = {data['quotient']}"
            elif user_second % user_first == 0 and user_second // user_first == data["quotient"]:
                is_correct = True
                division_check = f"{user_second} ÷ {user_first} = {data['quotient']}"
        except:
            pass
    
    if is_correct:
        st.success(f"🎉 **Excellent!** {division_check}")
        
        # Increase difficulty
        old_difficulty = st.session_state.quotient_difficulty
        st.session_state.quotient_difficulty = min(
            st.session_state.quotient_difficulty + 1, 5
        )
        
        if st.session_state.quotient_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered finding quotients!**")
        elif old_difficulty < st.session_state.quotient_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.quotient_difficulty}**")
        
        show_quotient_explanation(correct=True)
    
    else:
        # Show what their division actually gives
        actual_quotients = []
        if user_second != 0 and user_first % user_second == 0:
            actual_quotients.append(f"{user_first} ÷ {user_second} = {user_first // user_second}")
        if user_first != 0 and user_second % user_first == 0:
            actual_quotients.append(f"{user_second} ÷ {user_first} = {user_second // user_first}")
        
        if actual_quotients:
            st.error(f"❌ **Not quite.** {', '.join(actual_quotients)}, but we need a quotient of {data['quotient']}.")
        else:
            st.error(f"❌ **Not quite.** {user_first} and {user_second} don't divide evenly to give {data['quotient']}.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.quotient_difficulty
        st.session_state.quotient_difficulty = max(
            st.session_state.quotient_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.quotient_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.quotient_difficulty}. Keep trying!**")
        
        show_quotient_explanation(correct=False)

def show_quotient_explanation(correct=True):
    """Show explanation for the quotient problem"""
    data = st.session_state.quotient_data
    correct_answer = st.session_state.quotient_answer
    quotient = data["quotient"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Finding the Correct Quotient:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Available numbers: {', '.join(map(str, data['numbers']))}
        ### Target quotient: {quotient}
        
        ### Let's check all possibilities:
        """)
        
        # Show all possible divisions
        numbers = data["numbers"]
        found_solutions = []
        
        for i, num1 in enumerate(numbers):
            for j, num2 in enumerate(numbers):
                if i != j and num2 != 0 and num1 % num2 == 0:
                    div_result = num1 // num2
                    if div_result == quotient:
                        found_solutions.append(f"✅ **{num1} ÷ {num2} = {quotient}**")
                    else:
                        st.markdown(f"- {num1} ÷ {num2} = {div_result}")
        
        # Show the correct solutions
        for solution in found_solutions:
            st.markdown(solution)
        
        if not found_solutions:
            st.markdown("❌ No valid solutions found in systematic check")
        
        st.markdown(f"""
        ### Strategy tip:
        - **Think about multiples:** What numbers multiply by {quotient} to give one of our available numbers?
        - **Work backwards:** If quotient = {quotient}, then dividend = quotient × divisor
        - **Check systematically:** Try each number as dividend, then as divisor
        """)

def reset_quotient_state():
    """Reset the state for next problem"""
    st.session_state.current_quotient_problem = None
    st.session_state.quotient_answer = None
    st.session_state.quotient_feedback = False
    st.session_state.quotient_submitted = False
    st.session_state.quotient_data = {}
    if "quotient_user_answer" in st.session_state:
        del st.session_state.quotient_user_answer