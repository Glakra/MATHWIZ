import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Add three or more fractions practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/add_three_or_more_fractions.py
    """
    # Initialize session state for the activity
    if "add_fractions_score" not in st.session_state:
        st.session_state.add_fractions_score = 0
        st.session_state.add_fractions_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕ Add Three or More Fractions")
    st.markdown("*Add fractions with different denominators*")
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Score:** {st.session_state.add_fractions_score}/{st.session_state.add_fractions_attempts}")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Add Fractions:
        1. **Find the LCD** (Least Common Denominator)
        2. **Convert each fraction** to have the LCD
        3. **Add the numerators**
        4. **Keep the same denominator**
        5. **Simplify if possible**
        
        ### Example:
        1/2 + 1/3 + 1/6
        - LCD of 2, 3, and 6 is 6
        - 1/2 = 3/6, 1/3 = 2/6, 1/6 = 1/6
        - 3/6 + 2/6 + 1/6 = 6/6 = 1
        
        ### Tips:
        - List multiples to find LCD
        - Always simplify your final answer
        - Check your work by estimating
        """)

def generate_new_problem():
    """Generate a new fraction addition problem"""
    # Problem sets with varying difficulty
    problem_sets = [
        # Easy: Common denominators
        {"fractions": [Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)], "difficulty": "easy"},
        {"fractions": [Fraction(1, 10), Fraction(1, 2), Fraction(1, 10)], "difficulty": "easy"},
        {"fractions": [Fraction(3, 8), Fraction(1, 4), Fraction(1, 2)], "difficulty": "easy"},
        
        # Medium: Need to find LCD
        {"fractions": [Fraction(5, 12), Fraction(1, 4), Fraction(1, 6)], "difficulty": "medium"},
        {"fractions": [Fraction(1, 3), Fraction(1, 6), Fraction(1, 9)], "difficulty": "medium"},
        {"fractions": [Fraction(2, 5), Fraction(1, 10), Fraction(3, 20)], "difficulty": "medium"},
        {"fractions": [Fraction(1, 4), Fraction(2, 3), Fraction(1, 6)], "difficulty": "medium"},
        
        # Hard: Larger denominators or 4 fractions
        {"fractions": [Fraction(2, 7), Fraction(3, 14), Fraction(1, 2)], "difficulty": "hard"},
        {"fractions": [Fraction(5, 6), Fraction(1, 3), Fraction(1, 4)], "difficulty": "hard"},
        {"fractions": [Fraction(3, 10), Fraction(2, 5), Fraction(1, 15)], "difficulty": "hard"},
        {"fractions": [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 6)], "difficulty": "hard"},
        {"fractions": [Fraction(1, 5), Fraction(2, 15), Fraction(1, 3), Fraction(1, 10)], "difficulty": "hard"},
    ]
    
    # Select random problem
    problem = random.choice(problem_sets)
    fractions = problem["fractions"]
    
    # Calculate correct answer
    correct_answer = sum(fractions)
    
    st.session_state.current_problem = fractions
    st.session_state.correct_answer = correct_answer
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_problem():
    """Display the current fraction addition problem"""
    fractions = st.session_state.current_problem
    
    # Display the problem
    st.markdown("### Add.")
    
    # Create fraction display
    problem_text = ""
    for i, frac in enumerate(fractions):
        if i > 0:
            problem_text += " + "
        problem_text += f"{frac.numerator}/{frac.denominator}"
    
    # Display in a nice box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 20px; 
        border-radius: 10px; 
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
    ">
        {problem_text} = ?
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**Enter your answer as a fraction:**")
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                numerator = st.number_input("Numerator", min_value=0, step=1, key="num_input")
            with subcol2:
                denominator = st.number_input("Denominator", min_value=1, step=1, key="denom_input")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit:
            st.session_state.user_answer = Fraction(numerator, denominator)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.session_state.add_fractions_attempts += 1
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Great job!**")
        st.session_state.add_fractions_score += 1
        
        # Show if they simplified
        if user_answer.denominator < sum(f.denominator for f in st.session_state.current_problem):
            st.info("✨ Excellent! You also simplified the fraction.")
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer}**")
        
        # Show step-by-step solution
        show_solution()

def show_solution():
    """Show step-by-step solution"""
    fractions = st.session_state.current_problem
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        # Find LCD
        denominators = [f.denominator for f in fractions]
        lcd = find_lcd(denominators)
        
        st.markdown("### Step 1: Find the LCD")
        st.markdown(f"Denominators: {', '.join(map(str, denominators))}")
        st.markdown(f"**LCD = {lcd}**")
        
        # Convert fractions
        st.markdown("### Step 2: Convert each fraction")
        converted = []
        for frac in fractions:
            multiplier = lcd // frac.denominator
            new_num = frac.numerator * multiplier
            converted.append(new_num)
            st.markdown(f"- {frac} = {frac.numerator} × {multiplier}/{frac.denominator} × {multiplier} = **{new_num}/{lcd}**")
        
        # Add numerators
        st.markdown("### Step 3: Add the numerators")
        sum_text = " + ".join(map(str, converted))
        total = sum(converted)
        st.markdown(f"{sum_text} = **{total}**")
        
        # Result
        st.markdown("### Step 4: Write the result")
        result = Fraction(total, lcd)
        st.markdown(f"**{total}/{lcd}**")
        
        # Simplify if needed
        if result != st.session_state.correct_answer:
            st.markdown("### Step 5: Simplify")
            st.markdown(f"{result} = **{st.session_state.correct_answer}**")

def find_lcd(denominators):
    """Find the LCD of a list of denominators"""
    from math import gcd
    lcd = denominators[0]
    for d in denominators[1:]:
        lcd = lcd * d // gcd(lcd, d)
    return lcd

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer