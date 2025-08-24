import streamlit as st
import random
from fractions import Fraction
import re
import math

def run():
    """
    Main function to run the Add fractions with unlike denominators activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_fractions_with_unlike_denominators.py
    """
    # Initialize session state
    if "unlike_difficulty" not in st.session_state:
        st.session_state.unlike_difficulty = 1  # Start with simple problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.score = {"correct": 0, "attempted": 0}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕ Add Fractions with Unlike Denominators")
    st.markdown("*Add fractions with different denominators*")
    st.markdown("---")
    
    # Display score and difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Difficulty indicator
        diff_names = ["Easy", "Medium", "Hard", "Expert"]
        diff_level = st.session_state.unlike_difficulty
        st.markdown(f"**Difficulty:** {diff_names[diff_level-1]}")
        
        # Progress bar
        progress = (diff_level - 1) / 3
        st.progress(progress, text=f"Level {diff_level}/4")
    
    with col2:
        # Score display
        score = st.session_state.score
        if score["attempted"] > 0:
            percentage = (score["correct"] / score["attempted"]) * 100
            st.metric("Score", f"{score['correct']}/{score['attempted']}", f"{percentage:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Help & Tips**", expanded=False):
        st.markdown("""
        ### How to Add Fractions with Unlike Denominators:
        
        **Step 1: Find the Least Common Denominator (LCD)**
        - Find the smallest number that both denominators divide into evenly
        - Example: For 1/2 + 1/3, LCD = 6
        
        **Step 2: Convert to Equivalent Fractions**
        - Multiply numerator and denominator to get the LCD
        - 1/2 = 3/6 (multiply by 3/3)
        - 1/3 = 2/6 (multiply by 2/2)
        
        **Step 3: Add the Fractions**
        - Now that denominators are the same, add the numerators
        - 3/6 + 2/6 = 5/6
        
        **Step 4: Simplify if Possible**
        - Reduce the fraction to lowest terms
        - Check if numerator and denominator have common factors
        
        ### Quick LCD Tips:
        - For 2 and 4: LCD = 4
        - For 3 and 6: LCD = 6
        - For 4 and 6: LCD = 12
        - For 5 and 10: LCD = 10
        
        ### Remember:
        - Always simplify your final answer
        - The LCD is often (but not always) the product of the denominators
        """)

def generate_new_problem():
    """Generate a new unlike denominator addition problem"""
    difficulty = st.session_state.unlike_difficulty
    
    # Define fraction pairs by difficulty
    if difficulty == 1:
        # Easy - simple denominators, one often divides the other
        fraction_pairs = [
            (Fraction(1, 2), Fraction(1, 4)),
            (Fraction(1, 3), Fraction(1, 6)),
            (Fraction(1, 2), Fraction(1, 6)),
            (Fraction(1, 4), Fraction(1, 8)),
            (Fraction(2, 3), Fraction(1, 6)),
            (Fraction(3, 4), Fraction(1, 8)),
            (Fraction(1, 5), Fraction(1, 10)),
            (Fraction(1, 3), Fraction(2, 9)),
            (Fraction(5, 12), Fraction(1, 6)),
            (Fraction(1, 2), Fraction(3, 8))
        ]
    elif difficulty == 2:
        # Medium - require finding LCD
        fraction_pairs = [
            (Fraction(2, 3), Fraction(1, 4)),
            (Fraction(3, 4), Fraction(2, 5)),
            (Fraction(1, 3), Fraction(3, 8)),
            (Fraction(3, 5), Fraction(1, 3)),
            (Fraction(3, 4), Fraction(1, 6)),
            (Fraction(2, 5), Fraction(3, 10)),
            (Fraction(5, 6), Fraction(1, 4)),
            (Fraction(3, 8), Fraction(1, 6)),
            (Fraction(2, 7), Fraction(1, 3)),
            (Fraction(3, 10), Fraction(1, 2))
        ]
    elif difficulty == 3:
        # Hard - larger denominators
        fraction_pairs = [
            (Fraction(3, 7), Fraction(2, 5)),
            (Fraction(4, 9), Fraction(1, 6)),
            (Fraction(5, 8), Fraction(2, 7)),
            (Fraction(3, 11), Fraction(2, 5)),
            (Fraction(7, 12), Fraction(3, 8)),
            (Fraction(5, 9), Fraction(2, 3)),
            (Fraction(4, 15), Fraction(1, 6)),
            (Fraction(7, 10), Fraction(3, 8)),
            (Fraction(5, 12), Fraction(7, 18)),
            (Fraction(8, 15), Fraction(2, 9))
        ]
    else:
        # Expert - challenging denominators
        fraction_pairs = [
            (Fraction(5, 14), Fraction(3, 8)),
            (Fraction(7, 15), Fraction(4, 9)),
            (Fraction(11, 18), Fraction(5, 12)),
            (Fraction(8, 21), Fraction(5, 14)),
            (Fraction(13, 20), Fraction(7, 15)),
            (Fraction(9, 16), Fraction(5, 12)),
            (Fraction(11, 24), Fraction(7, 20)),
            (Fraction(17, 30), Fraction(11, 25)),
            (Fraction(13, 28), Fraction(9, 21)),
            (Fraction(19, 35), Fraction(11, 30))
        ]
    
    # Choose random fraction pair
    frac1, frac2 = random.choice(fraction_pairs)
    
    # Randomly swap order
    if random.choice([True, False]):
        frac1, frac2 = frac2, frac1
    
    # Calculate answer
    answer = frac1 + frac2
    
    # Find LCD
    lcd = frac1.denominator * frac2.denominator // math.gcd(frac1.denominator, frac2.denominator)
    
    # Store problem data
    st.session_state.problem_data = {
        "frac1": frac1,
        "frac2": frac2,
        "answer": answer,
        "lcd": lcd,
        "frac1_expanded": Fraction(frac1.numerator * (lcd // frac1.denominator), lcd),
        "frac2_expanded": Fraction(frac2.numerator * (lcd // frac2.denominator), lcd)
    }
    
    st.session_state.current_problem = "Add."
    st.session_state.correct_answer = answer

def format_fraction_display(numerator, denominator):
    """Create HTML for a fraction display"""
    return f'''
    <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 8px;">
        <span style="display: block; border-bottom: 2px solid black; padding: 2px 10px; font-size: 24px; line-height: 1;">{numerator}</span>
        <span style="display: block; padding: 2px 10px; font-size: 24px; line-height: 1;">{denominator}</span>
    </span>
    '''

def parse_fraction_answer(answer_str):
    """Parse a fraction answer"""
    answer_str = answer_str.strip()
    
    # Check for whole number
    if answer_str.isdigit():
        return Fraction(int(answer_str), 1)
    
    # Check for fraction (e.g., "3/4")
    match = re.match(r'^(\d+)\s*/\s*(\d+)$', answer_str)
    if match:
        num = int(match.group(1))
        denom = int(match.group(2))
        if denom > 0:
            return Fraction(num, denom)
    
    # Check for mixed number (e.g., "1 1/2")
    mixed_match = re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)$', answer_str)
    if mixed_match:
        whole = int(mixed_match.group(1))
        num = int(mixed_match.group(2))
        denom = int(mixed_match.group(3))
        if denom > 0:
            return Fraction(whole * denom + num, denom)
    
    return None

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display instruction
    st.markdown("### Add.")
    
    # Create the problem display
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
    
    with col1:
        # First fraction
        st.markdown(
            format_fraction_display(data['frac1'].numerator, data['frac1'].denominator),
            unsafe_allow_html=True
        )
    
    with col2:
        # Plus sign
        st.markdown("<h2 style='text-align: center; margin-top: 15px;'>+</h2>", unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        st.markdown(
            format_fraction_display(data['frac2'].numerator, data['frac2'].denominator),
            unsafe_allow_html=True
        )
    
    with col4:
        # Equals sign
        st.markdown("<h2 style='text-align: center; margin-top: 15px;'>=</h2>", unsafe_allow_html=True)
    
    with col5:
        # Answer input box
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        answer_input = st.text_input(
            "Answer",
            placeholder="e.g., 5/6",
            key="user_answer_input",
            label_visibility="collapsed"
        )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True):
            if answer_input:
                # Parse the answer
                parsed_answer = parse_fraction_answer(answer_input)
                
                if parsed_answer is None:
                    st.error("❌ Please enter a valid fraction (e.g., 3/4)")
                else:
                    st.session_state.user_answer = parsed_answer
                    st.session_state.show_feedback = True
                    st.session_state.answer_submitted = True
                    st.session_state.score["attempted"] += 1
            else:
                st.warning("Please enter an answer")
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if "user_answer" not in st.session_state:
        return
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.problem_data
    
    # Compare answers (both simplified)
    is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.score["correct"] += 1
        
        # Show the complete equation
        st.markdown(f"### ✅ {data['frac1']} + {data['frac2']} = {correct_answer}")
        
        # Increase difficulty if doing well
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate >= 0.8 and st.session_state.unlike_difficulty < 4:
                st.session_state.unlike_difficulty += 1
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.unlike_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
        
        # Show step-by-step solution
        show_solution()
        
        # Decrease difficulty if struggling
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate < 0.5 and st.session_state.unlike_difficulty > 1:
                st.session_state.unlike_difficulty -= 1
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.unlike_difficulty}**")

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        st.markdown(f"""
        ### Adding Fractions with Unlike Denominators:
        
        **Problem:** {data['frac1']} + {data['frac2']}
        
        **Step 1: Find the Least Common Denominator (LCD)**
        - Denominators: {data['frac1'].denominator} and {data['frac2'].denominator}
        - LCD = {data['lcd']}
        
        **Step 2: Convert to Equivalent Fractions**
        - {data['frac1']} = {data['frac1'].numerator} × {data['lcd'] // data['frac1'].denominator}/{data['frac1'].denominator} × {data['lcd'] // data['frac1'].denominator} = {data['frac1_expanded']}
        - {data['frac2']} = {data['frac2'].numerator} × {data['lcd'] // data['frac2'].denominator}/{data['frac2'].denominator} × {data['lcd'] // data['frac2'].denominator} = {data['frac2_expanded']}
        
        **Step 3: Add the Fractions**
        - {data['frac1_expanded']} + {data['frac2_expanded']} = {data['frac1_expanded'].numerator + data['frac2_expanded'].numerator}/{data['lcd']}
        
        **Step 4: Simplify**
        - {data['frac1_expanded'].numerator + data['frac2_expanded'].numerator}/{data['lcd']} = **{st.session_state.correct_answer}**
        
        ### Remember:
        - Always find the LCD first
        - Convert both fractions to have the LCD
        - Add the numerators, keep the denominator
        - Simplify your final answer
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    st.session_state.user_answer_input = ""  # Clear the input
    if "user_answer" in st.session_state:
        del st.session_state.user_answer