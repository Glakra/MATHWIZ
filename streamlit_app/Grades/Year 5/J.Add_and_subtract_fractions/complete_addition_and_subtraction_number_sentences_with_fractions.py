import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Complete addition and subtraction number sentences with fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/complete_addition_and_subtraction_number_sentences_with_fractions.py
    """
    # Initialize session state for difficulty and score
    if "complete_fractions_difficulty" not in st.session_state:
        st.session_state.complete_fractions_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "complete_fractions_score" not in st.session_state:
        st.session_state.complete_fractions_score = 0
        st.session_state.complete_fractions_attempts = 0
    
    if "current_equation" not in st.session_state:
        st.session_state.current_equation = None
        st.session_state.missing_value = None
        st.session_state.missing_type = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🔢 Complete Addition and Subtraction Sentences")
    st.markdown("*Fill in the missing number to complete the equation*")
    st.markdown("---")
    
    # Difficulty and score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        st.markdown(f"**Difficulty:** {difficulty_names[st.session_state.complete_fractions_difficulty]}")
        st.markdown(f"**Score:** {st.session_state.complete_fractions_score}/{st.session_state.complete_fractions_attempts}")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new equation if needed
    if st.session_state.current_equation is None:
        generate_new_equation()
    
    # Display current equation
    display_equation()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **How to Solve These Problems**", expanded=False):
        st.markdown("""
        ### Types of Missing Values:
        
        **Missing Numerator:**
        - Keep the denominator the same
        - Work backwards from the result
        - Example: 3/7 + ?/7 = 5/7 → ? = 2
        
        **Missing Denominator:**
        - Look for equivalent fractions
        - Find what number makes the equation work
        - Example: 1/2 + 1/? = 3/4 → ? = 4
        
        ### Tips:
        - For **same denominators**: Just add/subtract numerators
        - For **different denominators**: Find LCD first
        - **Check your work**: Substitute back to verify
        - **Simplify**: Sometimes the answer needs to be reduced
        """)

def generate_new_equation():
    """Generate a new fraction equation with a missing value"""
    difficulty = st.session_state.complete_fractions_difficulty
    
    if difficulty == 1:  # Easy - same denominators
        # Pick a common denominator
        d = random.choice([6, 8, 10, 12, 13, 14, 15, 16, 18, 19, 20])
        
        # Pick operation
        operation = random.choice(["add", "subtract"])
        
        # Pick which value is missing
        missing_position = random.choice(["first", "second", "result"])
        
        if operation == "add":
            # Generate two numerators that sum to less than denominator
            n1 = random.randint(1, d//2)
            n2 = random.randint(1, d//2)
            result = n1 + n2
            
            if missing_position == "first":
                equation = f"?/{d} + {n2}/{d} = {result}/{d}"
                missing_value = n1
            elif missing_position == "second":
                equation = f"{n1}/{d} + ?/{d} = {result}/{d}"
                missing_value = n2
            else:  # result
                equation = f"{n1}/{d} + {n2}/{d} = ?/{d}"
                missing_value = result
        
        else:  # subtract
            # Ensure valid subtraction
            n1 = random.randint(d//2, d-1)
            n2 = random.randint(1, n1-1)
            result = n1 - n2
            
            if missing_position == "first":
                equation = f"?/{d} - {n2}/{d} = {result}/{d}"
                missing_value = n1
            elif missing_position == "second":
                equation = f"{n1}/{d} - ?/{d} = {result}/{d}"
                missing_value = n2
            else:  # result
                equation = f"{n1}/{d} - {n2}/{d} = ?/{d}"
                missing_value = result
        
        missing_type = "numerator"
    
    elif difficulty == 2:  # Medium - different denominators, simpler relationships
        # One denominator is multiple of other
        base = random.choice([2, 3, 4, 5])
        multiplier = random.choice([2, 3, 4])
        d1, d2 = sorted([base, base * multiplier])
        
        operation = random.choice(["add", "subtract"])
        missing_position = random.choice(["first_num", "second_num", "denominator"])
        
        # Generate appropriate numerators
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d2-1)
        
        if operation == "add":
            # Calculate result
            frac1 = Fraction(n1, d1)
            frac2 = Fraction(n2, d2)
            result_frac = frac1 + frac2
            
            if missing_position == "first_num":
                equation = f"?/{d1} + {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n1
                missing_type = "numerator"
            elif missing_position == "second_num":
                equation = f"{n1}/{d1} + ?/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n2
                missing_type = "numerator"
            else:  # denominator
                equation = f"{n1}/{d1} + {n2}/? = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d2
                missing_type = "denominator"
        
        else:  # subtract
            # Ensure frac1 > frac2
            if Fraction(n1, d1) < Fraction(n2, d2):
                n1, n2, d1, d2 = n2, n1, d2, d1
            
            frac1 = Fraction(n1, d1)
            frac2 = Fraction(n2, d2)
            result_frac = frac1 - frac2
            
            if missing_position == "first_num":
                equation = f"?/{d1} - {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n1
                missing_type = "numerator"
            elif missing_position == "second_num":
                equation = f"{n1}/{d1} - ?/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n2
                missing_type = "numerator"
            else:  # denominator
                equation = f"{n1}/{d1} - {n2}/? = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d2
                missing_type = "denominator"
    
    else:  # Hard - any denominators
        # Generate unrelated denominators
        d1 = random.choice([3, 4, 5, 6, 7, 8, 9])
        d2 = random.choice([d for d in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if d != d1])
        
        operation = random.choice(["add", "subtract"])
        missing_position = random.choice(["first_num", "second_num", "first_denom", "second_denom"])
        
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d2-1)
        
        if operation == "add":
            frac1 = Fraction(n1, d1)
            frac2 = Fraction(n2, d2)
            result_frac = frac1 + frac2
            
            if missing_position == "first_num":
                equation = f"?/{d1} + {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n1
                missing_type = "numerator"
            elif missing_position == "second_num":
                equation = f"{n1}/{d1} + ?/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n2
                missing_type = "numerator"
            elif missing_position == "first_denom":
                equation = f"{n1}/? + {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d1
                missing_type = "denominator"
            else:  # second_denom
                equation = f"{n1}/{d1} + {n2}/? = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d2
                missing_type = "denominator"
        
        else:  # subtract
            if Fraction(n1, d1) < Fraction(n2, d2):
                n1, n2, d1, d2 = n2, n1, d2, d1
            
            frac1 = Fraction(n1, d1)
            frac2 = Fraction(n2, d2)
            result_frac = frac1 - frac2
            
            if missing_position == "first_num":
                equation = f"?/{d1} - {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n1
                missing_type = "numerator"
            elif missing_position == "second_num":
                equation = f"{n1}/{d1} - ?/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = n2
                missing_type = "numerator"
            elif missing_position == "first_denom":
                equation = f"{n1}/? - {n2}/{d2} = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d1
                missing_type = "denominator"
            else:  # second_denom
                equation = f"{n1}/{d1} - {n2}/? = {result_frac.numerator}/{result_frac.denominator}"
                missing_value = d2
                missing_type = "denominator"
    
    st.session_state.current_equation = equation
    st.session_state.missing_value = int(missing_value)
    st.session_state.missing_type = missing_type
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_equation():
    """Display the current equation with input field"""
    st.markdown("### Fill in the missing number.")
    
    equation = st.session_state.current_equation
    
    # Create the equation display
    equation_parts = equation.split("=")
    left_side = equation_parts[0].strip()
    right_side = equation_parts[1].strip()
    
    # Style the equation - replace ? with blank
    display_equation = equation.replace("?", "___")
    
    equation_html = f"""
    <div style="
        font-size: 24px;
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
    ">
        {display_equation}
    </div>
    """
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Input form
    with st.form("equation_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.missing_type == "numerator":
                answer = st.number_input(
                    "Enter the missing numerator:",
                    min_value=0,
                    step=1,
                    key="missing_input"
                )
            else:
                answer = st.number_input(
                    "Enter the missing denominator:",
                    min_value=1,
                    step=1,
                    key="missing_input"
                )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit:
            st.session_state.user_answer = int(answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.session_state.complete_fractions_attempts += 1
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_equation()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.missing_value
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Well done!**")
        st.session_state.complete_fractions_score += 1
        
        # Increase difficulty
        old_difficulty = st.session_state.complete_fractions_difficulty
        if st.session_state.complete_fractions_score % 3 == 0:  # Every 3 correct answers
            st.session_state.complete_fractions_difficulty = min(3, old_difficulty + 1)
            if st.session_state.complete_fractions_difficulty > old_difficulty:
                st.info(f"⬆️ **Level up! Moving to {['', 'Easy', 'Medium', 'Hard'][st.session_state.complete_fractions_difficulty]} problems.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer}.**")
        
        # Decrease difficulty if struggling
        if st.session_state.complete_fractions_attempts > 0:
            accuracy = st.session_state.complete_fractions_score / st.session_state.complete_fractions_attempts
            if accuracy < 0.5 and st.session_state.complete_fractions_attempts % 5 == 0:
                old_difficulty = st.session_state.complete_fractions_difficulty
                st.session_state.complete_fractions_difficulty = max(1, old_difficulty - 1)
                if st.session_state.complete_fractions_difficulty < old_difficulty:
                    st.warning(f"⬇️ **Let's practice with {['', 'Easy', 'Medium', 'Hard'][st.session_state.complete_fractions_difficulty]} problems.**")
        
        # Show solution
        show_solution()

def show_solution():
    """Show how to solve the equation"""
    equation = st.session_state.current_equation
    correct_answer = st.session_state.missing_value
    missing_type = st.session_state.missing_type
    
    with st.expander("📖 **See How to Solve**", expanded=True):
        st.markdown("### Solution Steps:")
        
        # Show the complete equation
        complete_equation = equation.replace("?", str(correct_answer))
        st.markdown(f"The complete equation is: **{complete_equation}**")
        
        # Explain based on missing type
        if missing_type == "numerator":
            st.markdown("""
            **To find a missing numerator:**
            1. Keep the denominator the same
            2. Work backwards from the result
            3. Add or subtract as needed
            """)
        else:
            st.markdown("""
            **To find a missing denominator:**
            1. Look at the relationship between fractions
            2. Find what denominator makes the equation true
            3. Check if fractions need to be equivalent
            """)
        
        # Verify the solution
        st.markdown("### Verification:")
        st.markdown(f"Let's check: {complete_equation}")
        st.markdown("✓ The equation is balanced!")

def find_lcd(denominators):
    """Find the LCD of a list of denominators"""
    from math import gcd
    lcd = denominators[0]
    for d in denominators[1:]:
        lcd = lcd * d // gcd(lcd, d)
    return lcd

def reset_equation():
    """Reset for next equation"""
    st.session_state.current_equation = None
    st.session_state.missing_value = None
    st.session_state.missing_type = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer