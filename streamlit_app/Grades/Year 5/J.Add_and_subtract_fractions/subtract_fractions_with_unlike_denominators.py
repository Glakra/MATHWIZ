import streamlit as st
import random
from fractions import Fraction
from math import gcd

def run():
    """
    Main function to run the Subtract Fractions with Unlike Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/subtract_fractions_with_unlike_denominators.py
    """
    # Add custom CSS for better styling
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
    
    /* Style for fraction display */
    .fraction {
        display: inline-block;
        text-align: center;
        vertical-align: middle;
    }
    
    .fraction-num {
        border-bottom: 3px solid black;
        display: block;
        padding: 0 20px;
        min-width: 60px;
    }
    
    .fraction-denom {
        display: block;
        padding: 0 20px;
        min-width: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "frac_subtract_score" not in st.session_state:
        st.session_state.frac_subtract_score = 0
        st.session_state.frac_subtract_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions with Unlike Denominators")
    st.markdown("*Practice subtracting fractions with different denominators*")
    
    # Add spacing
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Score display with back button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown("**Score**")
        st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>{st.session_state.frac_subtract_score}/{st.session_state.frac_subtract_attempts}</div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.frac_subtract_attempts > 0:
            percentage = (st.session_state.frac_subtract_score / st.session_state.frac_subtract_attempts) * 100
            st.markdown("**Accuracy**")
            st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>{percentage:.0f}%</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: right; margin-top: 20px;'></div>", unsafe_allow_html=True)
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Add vertical spacing
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section at the bottom
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Subtract Fractions with Unlike Denominators:
        
        **Step 1: Find the LCD (Least Common Denominator)**
        - Find the smallest number that both denominators divide into evenly
        - Example: For 1/4 and 1/6, LCD = 12
        
        **Step 2: Convert to Equivalent Fractions**
        - Multiply both numerator and denominator to get the LCD
        - 1/4 = 3/12 (multiply by 3/3)
        - 1/6 = 2/12 (multiply by 2/2)
        
        **Step 3: Subtract the Numerators**
        - Keep the common denominator
        - 3/12 - 2/12 = 1/12
        
        **Step 4: Simplify if Possible**
        - Find the GCD of numerator and denominator
        - Divide both by the GCD
        
        ### Examples:
        - **11/12 - 1/4 = ?**
          - LCD = 12
          - 11/12 - 3/12 = 8/12 = 2/3
        
        - **3/4 - 5/8 = ?**
          - LCD = 8
          - 6/8 - 5/8 = 1/8
        
        - **7/10 - 2/5 = ?**
          - LCD = 10
          - 7/10 - 4/10 = 3/10
        
        ### Remember:
        - ✅ Always find the LCD first
        - ✅ Convert both fractions before subtracting
        - ✅ Simplify your final answer
        - ❌ Never subtract denominators
        """)

def generate_new_problem():
    """Generate a new fraction subtraction problem"""
    # Problem sets with varying difficulty
    problem_sets = [
        # Easy - small denominators
        [(3, 4), (1, 2)],
        [(5, 6), (1, 3)],
        [(7, 8), (1, 4)],
        [(2, 3), (1, 6)],
        [(5, 6), (1, 2)],
        [(3, 4), (1, 8)],
        [(11, 12), (1, 4)],
        [(3, 4), (5, 8)],
        [(7, 10), (2, 5)],
        [(4, 5), (1, 10)],
        
        # Medium - larger denominators
        [(7, 8), (3, 4)],
        [(5, 6), (2, 3)],
        [(9, 10), (3, 5)],
        [(11, 12), (3, 4)],
        [(7, 9), (2, 3)],
        [(8, 9), (1, 3)],
        [(5, 8), (1, 2)],
        [(13, 15), (2, 5)],
        [(11, 14), (3, 7)],
        [(9, 10), (4, 5)],
        
        # Harder - more complex
        [(11, 12), (5, 8)],
        [(13, 15), (3, 5)],
        [(17, 20), (3, 4)],
        [(19, 24), (5, 8)],
        [(23, 30), (2, 5)],
        [(17, 18), (5, 9)],
        [(21, 28), (5, 7)],
        [(19, 21), (4, 7)],
        [(25, 30), (7, 10)],
        [(29, 35), (3, 7)]
    ]
    
    # Select a random problem
    problem = random.choice(problem_sets)
    num1, denom1 = problem[0]
    num2, denom2 = problem[1]
    
    # Create fractions
    frac1 = Fraction(num1, denom1)
    frac2 = Fraction(num2, denom2)
    
    # Ensure we get a positive result
    if frac1 < frac2:
        frac1, frac2 = frac2, frac1
        num1, denom1, num2, denom2 = num2, denom2, num1, denom1
    
    result = frac1 - frac2
    
    st.session_state.current_problem = {
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
    """Display the current subtraction problem"""
    problem = st.session_state.current_problem
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Display the problem in a clean format
    st.markdown("### Subtract.")
    
    # Add more spacing
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Create the problem layout with better proportions
    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 3])
    
    with col1:
        # First fraction with larger font
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
        st.markdown("<div style='text-align: center; font-size: 36px; margin-top: 25px;'>−</div>", unsafe_allow_html=True)
    
    with col3:
        # Second fraction with larger font
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
        st.markdown("<div style='text-align: center; font-size: 36px; margin-top: 25px;'>=</div>", unsafe_allow_html=True)
    
    with col5:
        # Answer input box with better styling
        if not st.session_state.answer_submitted:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            answer = st.text_input("", placeholder="Enter answer as fraction (e.g., 3/4)", 
                                 key="answer_input", label_visibility="collapsed")
        else:
            # Show the correct answer after submission
            result_color = "green" if st.session_state.user_correct else "red"
            result_symbol = "✓" if st.session_state.user_correct else "✗"
            st.markdown(f"""
            <div style="text-align: left; margin-top: 25px;">
                <span style="font-size: 36px; color: {result_color};">
                    {result_symbol} {st.session_state.current_problem['result']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Add spacing before submit button
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Submit button with custom styling
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            # Custom styled submit button
            submit_html = """
            <style>
            div.stButton > button {
                background-color: #FF5252;
                color: white;
                font-size: 16px;
                font-weight: 500;
                padding: 10px 24px;
                border: none;
                border-radius: 4px;
                width: 100%;
            }
            div.stButton > button:hover {
                background-color: #E53935;
            }
            </style>
            """
            st.markdown(submit_html, unsafe_allow_html=True)
            
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
    
    # Show feedback
    if st.session_state.show_feedback:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
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
    """Check the user's answer"""
    user_input = st.session_state.answer_input.strip()
    
    if not user_input:
        st.warning("Please enter an answer.")
        return
    
    try:
        # Parse the user's answer as a fraction
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
            # Try to parse as a whole number
            user_answer = Fraction(int(user_input), 1)
    
    except ValueError:
        st.error("Please enter a valid fraction (e.g., 3/4) or whole number.")
        return
    
    # Check if the answer is correct
    correct_answer = st.session_state.current_problem['result']
    st.session_state.user_correct = (user_answer == correct_answer)
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.frac_subtract_attempts += 1
    
    if st.session_state.user_correct:
        st.session_state.frac_subtract_score += 1
    
    st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.current_problem
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
    else:
        st.error(f"❌ **Incorrect.** The correct answer is **{problem['result']}**")
        
        # Add spacing before solution
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Show step-by-step solution
        with st.expander("📖 **See step-by-step solution**", expanded=True):
            show_solution(problem)

def show_solution(problem):
    """Show step-by-step solution"""
    frac1 = problem['frac1']
    frac2 = problem['frac2']
    result = problem['result']
    
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
    
    **Step 3: Subtract**
    - {equiv1_num}/{lcd} − {equiv2_num}/{lcd} = {equiv1_num - equiv2_num}/{lcd}
    
    **Step 4: Simplify**
    - {equiv1_num - equiv2_num}/{lcd} = **{result}**
    """)
    
    # Show work if they entered wrong answer
    if hasattr(st.session_state, 'user_answer') and not st.session_state.user_correct:
        st.markdown("---")
        st.markdown(f"**Your answer:** {st.session_state.user_answer}")
        
        # Common mistakes feedback
        if st.session_state.user_answer == Fraction(problem['num1'] - problem['num2'], problem['denom1']):
            st.warning("⚠️ **Common mistake:** You subtracted the numerators without finding a common denominator first!")
        elif st.session_state.user_answer.denominator != result.denominator:
            st.info("💡 **Tip:** Remember to simplify your answer to lowest terms.")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_answer'):
        del st.session_state.user_answer
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct