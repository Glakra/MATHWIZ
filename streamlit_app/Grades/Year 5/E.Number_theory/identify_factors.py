import streamlit as st
import random

def run():
    """
    Main function to run the Identify Factors activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/identify_factors.py
    """
    # Initialize session state
    if "factors_difficulty" not in st.session_state:
        st.session_state.factors_difficulty = 1
    
    if "current_factors_problem" not in st.session_state:
        st.session_state.current_factors_problem = None
        st.session_state.factors_answer = None
        st.session_state.factors_feedback = False
        st.session_state.factors_submitted = False
        st.session_state.factors_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🔢 Identify Factors")
    st.markdown("*Find which numbers divide evenly into the given number*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.factors_difficulty
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
    if st.session_state.current_factors_problem is None:
        generate_factors_problem()
    
    # Display current question
    display_factors_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is a Factor?
        A **factor** of a number is a whole number that divides evenly into it (with no remainder).
        
        ### How to Find Factors:
        **To check if a number is a factor:**
        1. **Divide** the target number by the potential factor
        2. **Check the remainder** - if it's 0, then it's a factor!
        3. **If there's a remainder**, it's not a factor
        
        ### Example: Factors of 18
        - **18 ÷ 1 = 18 R 0** ✅ So 1 is a factor
        - **18 ÷ 2 = 9 R 0** ✅ So 2 is a factor  
        - **18 ÷ 3 = 6 R 0** ✅ So 3 is a factor
        - **18 ÷ 4 = 4 R 2** ❌ So 4 is NOT a factor
        - **18 ÷ 6 = 3 R 0** ✅ So 6 is a factor
        
        **All factors of 18:** 1, 2, 3, 6, 9, 18
        
        ### Quick Tips:
        - **1 is always a factor** of any number
        - **The number itself** is always a factor
        - **Even numbers** are always divisible by 2
        - **Numbers ending in 0 or 5** are always divisible by 5
        - **Use multiplication facts** - if 3 × 6 = 18, then both 3 and 6 are factors of 18
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Small numbers (10-30)
        - **🟠 Level 3:** Medium numbers (30-60)
        - **🔴 Level 4-5:** Larger numbers (60-100)
        
        ### Strategy:
        Think about multiplication tables - which numbers multiply to give your target?
        """)

def generate_factors_problem():
    """Generate a factors problem based on difficulty level"""
    difficulty = st.session_state.factors_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple numbers with clear factors
        problems = [
            {"target": 18, "options": [8, 4, 7, 6], "correct": 6},  # From your image
            {"target": 12, "options": [5, 3, 7, 8], "correct": 3},  # 12÷3=4
            {"target": 15, "options": [4, 5, 7, 8], "correct": 5},  # 15÷5=3
            {"target": 20, "options": [3, 4, 7, 9], "correct": 4},  # 20÷4=5
            {"target": 24, "options": [5, 6, 7, 9], "correct": 6},  # 24÷6=4
            {"target": 16, "options": [3, 8, 5, 7], "correct": 8},  # 16÷8=2
            {"target": 21, "options": [4, 7, 5, 8], "correct": 7},  # 21÷7=3
            {"target": 28, "options": [5, 7, 9, 6], "correct": 7},  # 28÷7=4
            {"target": 30, "options": [4, 6, 7, 8], "correct": 6},  # 30÷6=5
            {"target": 25, "options": [4, 5, 6, 7], "correct": 5},  # 25÷5=5
        ]
    elif difficulty == 2:
        # Level 2: Slightly larger numbers
        problems = [
            {"target": 32, "options": [6, 8, 7, 9], "correct": 8},   # 32÷8=4
            {"target": 36, "options": [5, 9, 7, 8], "correct": 9},   # 36÷9=4
            {"target": 42, "options": [5, 6, 8, 9], "correct": 6},   # 42÷6=7
            {"target": 45, "options": [7, 9, 8, 6], "correct": 9},   # 45÷9=5
            {"target": 48, "options": [7, 8, 9, 5], "correct": 8},   # 48÷8=6
            {"target": 35, "options": [6, 7, 8, 9], "correct": 7},   # 35÷7=5
            {"target": 40, "options": [6, 8, 7, 9], "correct": 8},   # 40÷8=5
            {"target": 54, "options": [7, 9, 8, 5], "correct": 9},   # 54÷9=6
            {"target": 49, "options": [6, 7, 8, 9], "correct": 7},   # 49÷7=7
            {"target": 56, "options": [6, 8, 9, 5], "correct": 8},   # 56÷8=7
        ]
    elif difficulty == 3:
        # Level 3: Medium difficulty with multiple factors
        problems = [
            {"target": 60, "options": [8, 12, 7, 11], "correct": 12}, # 60÷12=5
            {"target": 72, "options": [11, 12, 13, 14], "correct": 12}, # 72÷12=6
            {"target": 84, "options": [11, 12, 13, 14], "correct": 12}, # 84÷12=7
            {"target": 63, "options": [8, 9, 11, 13], "correct": 9},   # 63÷9=7
            {"target": 81, "options": [8, 9, 11, 13], "correct": 9},   # 81÷9=9
            {"target": 64, "options": [7, 8, 9, 11], "correct": 8},    # 64÷8=8
            {"target": 75, "options": [8, 15, 11, 13], "correct": 15}, # 75÷15=5
            {"target": 88, "options": [9, 11, 13, 15], "correct": 11}, # 88÷11=8
            {"target": 96, "options": [11, 12, 13, 14], "correct": 12}, # 96÷12=8
            {"target": 77, "options": [9, 11, 13, 15], "correct": 11}, # 77÷11=7
        ]
    elif difficulty == 4:
        # Level 4: Larger numbers with less obvious factors
        problems = [
            {"target": 91, "options": [12, 13, 11, 15], "correct": 13}, # 91÷13=7
            {"target": 65, "options": [12, 13, 11, 15], "correct": 13}, # 65÷13=5
            {"target": 78, "options": [12, 13, 11, 15], "correct": 13}, # 78÷13=6
            {"target": 85, "options": [14, 17, 13, 16], "correct": 17}, # 85÷17=5
            {"target": 68, "options": [14, 17, 13, 16], "correct": 17}, # 68÷17=4
            {"target": 87, "options": [14, 29, 13, 16], "correct": 29}, # 87÷29=3
            {"target": 95, "options": [18, 19, 17, 21], "correct": 19}, # 95÷19=5
            {"target": 76, "options": [18, 19, 17, 21], "correct": 19}, # 76÷19=4
            {"target": 93, "options": [14, 31, 13, 16], "correct": 31}, # 93÷31=3
            {"target": 69, "options": [14, 23, 13, 16], "correct": 23}, # 69÷23=3
        ]
    else:  # difficulty == 5
        # Level 5: Complex numbers requiring good factor sense
        problems = [
            {"target": 119, "options": [16, 17, 19, 21], "correct": 17}, # 119÷17=7
            {"target": 133, "options": [16, 17, 19, 21], "correct": 19}, # 133÷19=7
            {"target": 161, "options": [22, 23, 19, 21], "correct": 23}, # 161÷23=7
            {"target": 143, "options": [10, 11, 13, 12], "correct": 11}, # 143÷11=13
            {"target": 187, "options": [10, 11, 13, 12], "correct": 11}, # 187÷11=17
            {"target": 169, "options": [12, 13, 15, 17], "correct": 13}, # 169÷13=13
            {"target": 121, "options": [10, 11, 13, 12], "correct": 11}, # 121÷11=11
            {"target": 209, "options": [10, 11, 13, 12], "correct": 11}, # 209÷11=19
            {"target": 221, "options": [12, 13, 15, 17], "correct": 13}, # 221÷13=17
            {"target": 247, "options": [12, 13, 15, 17], "correct": 13}, # 247÷13=19
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    st.session_state.factors_data = problem
    st.session_state.factors_answer = problem["correct"]
    st.session_state.current_factors_problem = f"Which number is a factor of {problem['target']}?"

def display_factors_problem():
    """Display the current factors problem interface"""
    data = st.session_state.factors_data
    target = data["target"]
    options = data["options"]
    
    # Display the question
    st.markdown(f"### 🎯 {st.session_state.current_factors_problem}")
    
    # Display options in a clean grid using columns
    st.markdown("**Choose your answer:**")
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]
    
    # Display each option in its own column with styling
    for i, option in enumerate(options):
        with columns[i]:
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 10px 0;
                font-size: 24px;
                font-weight: bold;
                color: #333;
            ">
                {option}
            </div>
            """, unsafe_allow_html=True)
    
    # Single form for answer selection
    with st.form("factors_form", clear_on_submit=False):
        # Radio button selection
        selected_option = st.radio(
            "Select your answer:",
            options=[str(opt) for opt in options],
            key="factor_choice",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        # Handle form submission
        if submit_button:
            if selected_option:
                selected_number = int(selected_option)
                st.session_state.factors_user_answer = selected_number
                st.session_state.factors_feedback = True
                st.session_state.factors_submitted = True
            else:
                st.error("Please select an answer")
    
    # Show feedback and next button
    handle_factors_feedback()

def handle_factors_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("factors_feedback", False):
        show_factors_feedback()
    
    if st.session_state.get("factors_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_factors_state()
                st.rerun()

def show_factors_feedback():
    """Display feedback for the factors problem"""
    user_answer = st.session_state.get("factors_user_answer")
    correct_answer = st.session_state.get("factors_answer")
    data = st.session_state.get("factors_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    target = data["target"]
    
    if user_answer == correct_answer:
        # Check the division to show in feedback
        quotient = target // correct_answer
        st.success(f"🎉 **Excellent!** {correct_answer} is a factor of {target} because {target} ÷ {correct_answer} = {quotient} with no remainder!")
        
        # Increase difficulty
        old_difficulty = st.session_state.factors_difficulty
        st.session_state.factors_difficulty = min(
            st.session_state.factors_difficulty + 1, 5
        )
        
        if st.session_state.factors_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered identifying factors!**")
        elif old_difficulty < st.session_state.factors_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.factors_difficulty}**")
        
        show_factors_explanation(correct=True)
    
    else:
        # Check what happens when we divide by the wrong answer
        if target % user_answer == 0:
            quotient = target // user_answer
            st.warning(f"🤔 **Actually, {user_answer} IS a factor!** {target} ÷ {user_answer} = {quotient}. But the intended answer was {correct_answer}.")
        else:
            remainder = target % user_answer
            quotient = target // user_answer
            st.error(f"❌ **Not quite.** {user_answer} is not a factor of {target} because {target} ÷ {user_answer} = {quotient} R {remainder}.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.factors_difficulty
        st.session_state.factors_difficulty = max(
            st.session_state.factors_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.factors_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.factors_difficulty}. Keep practicing!**")
        
        show_factors_explanation(correct=False)

def show_factors_explanation(correct=True):
    """Show explanation for the factors problem"""
    data = st.session_state.get("factors_data", {})
    correct_answer = st.session_state.get("factors_answer")
    user_answer = st.session_state.get("factors_user_answer")
    
    if not data or correct_answer is None:
        return
        
    target = data["target"]
    options = data["options"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for step-by-step explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Factor Check:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Question: Which number is a factor of {target}?
        ### Options: {', '.join(map(str, options))}
        
        ### Let's check each option:
        """)
        
        # Check each option
        for option in options:
            quotient = target // option
            remainder = target % option
            
            if remainder == 0:
                status = "✅ **IS a factor**"
                explanation = f"{target} ÷ {option} = {quotient} (no remainder)"
                if option == correct_answer:
                    explanation += " ← **Correct answer!**"
            else:
                status = "❌ **NOT a factor**"
                explanation = f"{target} ÷ {option} = {quotient} R {remainder} (has remainder)"
            
            st.markdown(f"- **{option}:** {explanation} {status}")
        
        # Find ALL factors of the target number
        all_factors = []
        for i in range(1, target + 1):
            if target % i == 0:
                all_factors.append(i)
        
        st.markdown(f"""
        ### Complete list of factors of {target}:
        **{', '.join(map(str, all_factors))}**
        
        ### Remember:
        - A factor divides evenly (remainder = 0)
        - 1 and {target} are always factors of {target}
        - Factors come in pairs: if {correct_answer} is a factor, then {target // correct_answer} is also a factor
        """)

def reset_factors_state():
    """Reset the state for next problem"""
    st.session_state.current_factors_problem = None
    st.session_state.factors_answer = None
    st.session_state.factors_feedback = False
    st.session_state.factors_submitted = False
    st.session_state.factors_data = {}
    
    if "factors_user_answer" in st.session_state:
        del st.session_state.factors_user_answer