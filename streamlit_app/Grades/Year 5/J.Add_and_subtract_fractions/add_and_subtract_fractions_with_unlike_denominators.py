import streamlit as st
import random
from fractions import Fraction
from math import gcd

def run():
    """
    Main function to run the Add and Subtract Fractions with Unlike Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_fractions_with_unlike_denominators.py
    """
    # Initialize session state for adaptive difficulty
    if "frac_difficulty_level" not in st.session_state:
        st.session_state.frac_difficulty_level = 1  # Start at level 1 (easiest)
    
    if "frac_streak" not in st.session_state:
        st.session_state.frac_streak = 0  # Track consecutive correct answers
    
    if "frac_mistakes" not in st.session_state:
        st.session_state.frac_mistakes = 0  # Track consecutive mistakes
    
    if "current_frac_problem" not in st.session_state:
        st.session_state.current_frac_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Add custom CSS
    st.markdown("""
    <style>
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Style the text input */
    input[type="text"] {
        font-size: 18px !important;
        text-align: center !important;
    }
    
    /* Submit button style */
    div.stButton > button[type="submit"] {
        background-color: #4CAF50;
        color: white;
    }
    
    div.stButton > button[type="submit"]:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕➖ Add and Subtract Fractions with Unlike Denominators")
    st.markdown("*Practice adding and subtracting fractions with different denominators*")
    
    # Difficulty indicator and back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Beginner", 2: "Easy", 3: "Medium", 4: "Hard", 5: "Expert"}
        difficulty_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🟣"}
        current_diff = st.session_state.frac_difficulty_level
        st.markdown(f"**Difficulty Level:** {difficulty_colors[current_diff]} {difficulty_names[current_diff]}")
        st.progress(current_diff / 5, text=f"Level {current_diff}/5")
    
    with col2:
        if st.session_state.frac_streak > 0:
            st.metric("Streak", f"🔥 {st.session_state.frac_streak}")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_frac_problem is None:
        generate_adaptive_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Adaptive Difficulty System:
        - **Level 1 (Beginner)**: Simple fractions with small denominators (2, 3, 4)
        - **Level 2 (Easy)**: Common denominators (2, 3, 4, 5, 6)
        - **Level 3 (Medium)**: Larger denominators (up to 12)
        - **Level 4 (Hard)**: Complex fractions requiring more steps
        - **Level 5 (Expert)**: Challenging problems with large denominators
        
        **Progress System:**
        - ✅ 3 correct in a row = Level up!
        - ❌ 2 mistakes in a row = Level down
        - 🔥 Build your streak!
        
        ### How to Solve:
        
        **For Addition (a/b + c/d):**
        1. Find LCD of b and d
        2. Convert both fractions: a/b = (a×k)/(b×k), c/d = (c×m)/(d×m)
        3. Add numerators: (a×k + c×m)/LCD
        4. Simplify the result
        
        **For Subtraction (a/b - c/d):**
        1. Same process but subtract numerators
        2. Make sure first fraction > second fraction
        
        ### Remember:
        - Always simplify your final answer!
        - Enter answers as fractions (e.g., 3/4) or whole numbers
        """)

def generate_adaptive_problem():
    """Generate problem based on current difficulty level"""
    level = st.session_state.frac_difficulty_level
    
    # Define denominator sets for each level
    level_denominators = {
        1: [2, 3, 4],  # Beginner
        2: [2, 3, 4, 5, 6],  # Easy
        3: [2, 3, 4, 5, 6, 8, 9, 10, 12],  # Medium
        4: [3, 4, 5, 6, 7, 8, 9, 10, 12, 15],  # Hard
        5: [6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 20]  # Expert
    }
    
    # Choose operation (50/50 chance)
    operation = random.choice(["add", "subtract"])
    
    # Get appropriate denominators for this level
    possible_denoms = level_denominators[level]
    
    # Generate fractions
    attempts = 0
    while attempts < 50:  # Prevent infinite loop
        denom1 = random.choice(possible_denoms)
        denom2 = random.choice([d for d in possible_denoms if d != denom1])
        
        # Generate numerators based on level
        if level <= 2:
            # For easier levels, keep numerators small
            num1 = random.randint(1, min(denom1 - 1, 4))
            num2 = random.randint(1, min(denom2 - 1, 4))
        else:
            # For harder levels, allow larger numerators
            num1 = random.randint(1, denom1 - 1)
            num2 = random.randint(1, denom2 - 1)
        
        frac1 = Fraction(num1, denom1)
        frac2 = Fraction(num2, denom2)
        
        # For subtraction, ensure positive result
        if operation == "subtract":
            if frac1 < frac2:
                frac1, frac2 = frac2, frac1
                num1, denom1, num2, denom2 = num2, denom2, num1, denom1
            
            result = frac1 - frac2
            if result.numerator > 0:  # Ensure positive result
                break
        else:  # addition
            result = frac1 + frac2
            # For easier levels, avoid results > 2
            if level <= 2 and result > 2:
                continue
            break
        
        attempts += 1
    
    st.session_state.current_frac_problem = {
        "operation": operation,
        "num1": num1,
        "denom1": denom1,
        "num2": num2,
        "denom2": denom2,
        "frac1": frac1,
        "frac2": frac2,
        "result": result
    }
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_problem():
    """Display the current problem"""
    problem = st.session_state.current_frac_problem
    
    # Display operation type
    if problem["operation"] == "add":
        st.markdown("### Add.")
    else:
        st.markdown("### Subtract.")
    
    # Add spacing
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Create the problem layout
    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 3])
    
    with col1:
        # First fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; line-height: 1;">
                <div style="border-bottom: 3px solid black; display: inline-block; padding: 0 20px; min-width: 60px;">
                    {problem['num1']}
                </div>
                <div style="padding: 0 20px; min-width: 60px;">
                    {problem['denom1']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        op_symbol = "+" if problem["operation"] == "add" else "−"
        st.markdown(f"<div style='text-align: center; font-size: 36px; margin-top: 25px;'>{op_symbol}</div>", 
                   unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; line-height: 1;">
                <div style="border-bottom: 3px solid black; display: inline-block; padding: 0 20px; min-width: 60px;">
                    {problem['num2']}
                </div>
                <div style="padding: 0 20px; min-width: 60px;">
                    {problem['denom2']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div style='text-align: center; font-size: 36px; margin-top: 25px;'>=</div>", 
                   unsafe_allow_html=True)
    
    with col5:
        # Answer input
        if not st.session_state.answer_submitted:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            answer = st.text_input("", placeholder="Enter answer (e.g., 3/4)", 
                                 key="answer_input", label_visibility="collapsed")
        else:
            # Show result after submission
            result_color = "green" if st.session_state.user_correct else "red"
            result_symbol = "✓" if st.session_state.user_correct else "✗"
            st.markdown(f"""
            <div style="text-align: left; margin-top: 25px;">
                <span style="font-size: 36px; color: {result_color};">
                    {result_symbol} {st.session_state.current_frac_problem['result']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Submit button
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("Next Problem →", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def check_answer():
    """Check the user's answer and update difficulty"""
    user_input = st.session_state.answer_input.strip()
    
    if not user_input:
        st.warning("Please enter an answer.")
        return
    
    try:
        # Parse user answer
        if '/' in user_input:
            parts = user_input.split('/')
            if len(parts) == 2:
                num = int(parts[0])
                denom = int(parts[1])
                if denom == 0:
                    st.error("Denominator cannot be zero.")
                    return
                user_answer = Fraction(num, denom)
            else:
                st.error("Please enter a valid fraction (e.g., 3/4).")
                return
        else:
            user_answer = Fraction(int(user_input), 1)
    
    except ValueError:
        st.error("Please enter a valid fraction (e.g., 3/4) or whole number.")
        return
    
    # Check if correct
    correct_answer = st.session_state.current_frac_problem['result']
    st.session_state.user_correct = (user_answer == correct_answer)
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    
    # Update difficulty based on performance
    if st.session_state.user_correct:
        st.session_state.frac_streak += 1
        st.session_state.frac_mistakes = 0
        
        # Level up after 3 correct in a row
        if st.session_state.frac_streak >= 3 and st.session_state.frac_difficulty_level < 5:
            st.session_state.frac_difficulty_level += 1
            st.session_state.frac_streak = 0
    else:
        st.session_state.frac_mistakes += 1
        st.session_state.frac_streak = 0
        
        # Level down after 2 mistakes in a row
        if st.session_state.frac_mistakes >= 2 and st.session_state.frac_difficulty_level > 1:
            st.session_state.frac_difficulty_level -= 1
            st.session_state.frac_mistakes = 0
    
    st.rerun()

def show_feedback():
    """Display feedback with solution"""
    problem = st.session_state.current_frac_problem
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
        if st.session_state.frac_streak == 2:
            st.info("🔥 **One more correct answer to level up!**")
        elif st.session_state.frac_streak == 0 and st.session_state.frac_difficulty_level < 5:
            st.balloons()
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.frac_difficulty_level}**")
    else:
        st.error(f"❌ **Incorrect.** The correct answer is **{problem['result']}**")
        if st.session_state.frac_mistakes == 1:
            st.warning("💡 **Tip:** Take your time and check your work.")
        elif st.session_state.frac_mistakes == 0 and st.session_state.frac_difficulty_level > 1:
            st.warning(f"⬇️ **Level decreased to {st.session_state.frac_difficulty_level}. Keep practicing!**")
        
        # Show solution
        with st.expander("📖 **See step-by-step solution**", expanded=True):
            show_solution(problem)

def show_solution(problem):
    """Show step-by-step solution"""
    frac1 = problem['frac1']
    frac2 = problem['frac2']
    result = problem['result']
    operation = problem['operation']
    op_symbol = "+" if operation == "add" else "−"
    
    # Find LCD
    lcd = abs(frac1.denominator * frac2.denominator) // gcd(frac1.denominator, frac2.denominator)
    
    # Calculate equivalent fractions
    equiv1_num = frac1.numerator * (lcd // frac1.denominator)
    equiv2_num = frac2.numerator * (lcd // frac2.denominator)
    
    st.markdown(f"""
    ### Step-by-step solution:
    
    **Step 1: Find the LCD**
    - Denominators: {frac1.denominator} and {frac2.denominator}
    - LCD = {lcd}
    
    **Step 2: Convert to equivalent fractions**
    - {frac1} = {frac1.numerator} × {lcd // frac1.denominator}/{frac1.denominator} × {lcd // frac1.denominator} = {equiv1_num}/{lcd}
    - {frac2} = {frac2.numerator} × {lcd // frac2.denominator}/{frac2.denominator} × {lcd // frac2.denominator} = {equiv2_num}/{lcd}
    
    **Step 3: {operation.capitalize()}**
    """)
    
    if operation == "add":
        st.markdown(f"- {equiv1_num}/{lcd} + {equiv2_num}/{lcd} = {equiv1_num + equiv2_num}/{lcd}")
    else:
        st.markdown(f"- {equiv1_num}/{lcd} − {equiv2_num}/{lcd} = {equiv1_num - equiv2_num}/{lcd}")
    
    st.markdown(f"""
    **Step 4: Simplify**
    - {equiv1_num + equiv2_num if operation == "add" else equiv1_num - equiv2_num}/{lcd} = **{result}**
    """)

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_frac_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_answer'):
        del st.session_state.user_answer
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct