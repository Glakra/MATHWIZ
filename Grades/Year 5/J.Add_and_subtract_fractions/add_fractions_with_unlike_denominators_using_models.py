import streamlit as st
import random
from fractions import Fraction
import re
import math

def run():
    """
    Main function to run the Add fractions with unlike denominators using models activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_fractions_with_unlike_denominators_using_models.py
    """
    # Initialize session state
    if "unlike_model_difficulty" not in st.session_state:
        st.session_state.unlike_model_difficulty = 1  # Start with simple problems
    
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
    st.markdown("*Use visual models to add fractions with different denominators*")
    st.markdown("---")
    
    # Display score and difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Difficulty indicator
        diff_names = ["Easy", "Medium", "Hard", "Expert"]
        diff_level = st.session_state.unlike_model_difficulty
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
        
        **Step 1: Look at the model**
        - Each fraction is shown as colored blocks
        - The blocks are divided to show the denominator
        
        **Step 2: Find equivalent fractions**
        - The model shows how to convert to the same denominator
        - Count the total parts in each fraction
        
        **Step 3: Add the fractions**
        - Once denominators are the same, add the numerators
        - Keep the common denominator
        
        ### Example: 1/2 + 1/4
        - 1/2 = 2/4 (shown in the model)
        - 2/4 + 1/4 = 3/4
        
        ### Tips:
        - Count the colored parts carefully
        - Look for the common denominator in the model
        - The answer should be simplified if possible
        """)

def generate_new_problem():
    """Generate a new unlike denominator addition problem"""
    difficulty = st.session_state.unlike_model_difficulty
    
    # Define fraction pairs by difficulty
    if difficulty == 1:
        # Easy - one denominator is multiple of the other
        fraction_pairs = [
            (Fraction(1, 2), Fraction(1, 4)),
            (Fraction(1, 2), Fraction(3, 8)),
            (Fraction(1, 3), Fraction(1, 6)),
            (Fraction(1, 4), Fraction(1, 8)),
            (Fraction(2, 3), Fraction(1, 6)),
            (Fraction(1, 2), Fraction(1, 6)),
            (Fraction(1, 3), Fraction(2, 9)),
            (Fraction(1, 5), Fraction(2, 10))
        ]
    elif difficulty == 2:
        # Medium - slightly harder relationships
        fraction_pairs = [
            (Fraction(2, 3), Fraction(1, 4)),
            (Fraction(1, 4), Fraction(2, 5)),
            (Fraction(1, 3), Fraction(3, 8)),
            (Fraction(2, 5), Fraction(1, 3)),
            (Fraction(3, 4), Fraction(1, 6)),
            (Fraction(1, 6), Fraction(3, 8)),
            (Fraction(2, 5), Fraction(1, 4)),
            (Fraction(1, 3), Fraction(2, 5))
        ]
    elif difficulty == 3:
        # Hard - more complex relationships
        fraction_pairs = [
            (Fraction(3, 4), Fraction(2, 5)),
            (Fraction(2, 3), Fraction(3, 5)),
            (Fraction(3, 5), Fraction(1, 4)),
            (Fraction(5, 6), Fraction(3, 8)),
            (Fraction(2, 7), Fraction(3, 4)),
            (Fraction(3, 8), Fraction(2, 5)),
            (Fraction(4, 5), Fraction(2, 3)),
            (Fraction(5, 8), Fraction(1, 3))
        ]
    else:
        # Expert - challenging fractions
        fraction_pairs = [
            (Fraction(3, 7), Fraction(2, 5)),
            (Fraction(4, 9), Fraction(3, 5)),
            (Fraction(5, 8), Fraction(3, 7)),
            (Fraction(2, 9), Fraction(5, 6)),
            (Fraction(3, 11), Fraction(2, 5)),
            (Fraction(5, 12), Fraction(3, 8)),
            (Fraction(7, 9), Fraction(2, 5)),
            (Fraction(4, 15), Fraction(3, 10))
        ]
    
    # Choose random fraction pair
    frac1, frac2 = random.choice(fraction_pairs)
    
    # Randomly swap order
    if random.choice([True, False]):
        frac1, frac2 = frac2, frac1
    
    # Calculate answer
    answer = frac1 + frac2
    
    # Find LCD for the model
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
    
    st.session_state.current_problem = f"Add."
    st.session_state.correct_answer = answer

def format_fraction_display(numerator, denominator):
    """Create HTML for a fraction display"""
    return f'''
    <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 5px;">
        <span style="display: block; border-bottom: 2px solid black; padding: 0 8px; font-size: 24px;">{numerator}</span>
        <span style="display: block; padding: 0 8px; font-size: 24px;">{denominator}</span>
    </span>
    '''

def create_visual_model(frac1, frac2, lcd):
    """Create visual model using colored blocks"""
    data = st.session_state.problem_data
    
    # Create model container
    st.markdown("---")
    
    # Choose colors based on problem
    if frac1.denominator == 2:
        color1 = "🟪"  # Purple for halves
        color2 = "🟩"  # Green
        empty = "⬜"
    elif frac1.denominator == 3:
        color1 = "🟦"  # Blue for thirds
        color2 = "🟨"  # Yellow
        empty = "⬜"
    else:
        color1 = "🟥"  # Red
        color2 = "🟧"  # Orange
        empty = "⬜"
    
    # First fraction visual
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"### {frac1}")
    with col2:
        # Show the fraction as blocks
        blocks1 = color1 * frac1.numerator + empty * (frac1.denominator - frac1.numerator)
        st.markdown(f"<div style='font-size: 30px; letter-spacing: 5px;'>{blocks1}</div>", unsafe_allow_html=True)
    
    # Plus sign
    st.markdown("<h2 style='text-align: center;'>+</h2>", unsafe_allow_html=True)
    
    # Second fraction visual
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"### {frac2}")
    with col2:
        # Show the fraction as blocks
        blocks2 = color2 * frac2.numerator + empty * (frac2.denominator - frac2.numerator)
        # Split into multiple rows if needed
        if frac2.denominator > 6:
            mid = frac2.denominator // 2
            blocks2_row1 = blocks2[:mid]
            blocks2_row2 = blocks2[mid:]
            st.markdown(f"<div style='font-size: 30px; letter-spacing: 5px;'>{blocks2_row1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 30px; letter-spacing: 5px;'>{blocks2_row2}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size: 30px; letter-spacing: 5px;'>{blocks2}</div>", unsafe_allow_html=True)
    
    # Line separator
    st.markdown("<hr style='border: 2px solid black; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Show equivalent fractions if helpful
    if frac1.denominator != lcd or frac2.denominator != lcd:
        st.markdown("**💡 Hint: Convert to equivalent fractions**")
        
        # Show conversions
        if frac1.denominator != lcd:
            equiv1 = data['frac1_expanded']
            st.markdown(f"{frac1} = {equiv1}")
        
        if frac2.denominator != lcd:
            equiv2 = data['frac2_expanded']
            st.markdown(f"{frac2} = {equiv2}")

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
    """Display the current problem with visual model"""
    data = st.session_state.problem_data
    
    # Display instruction
    st.markdown("### Add.")
    
    # Display the equation
    frac1_html = format_fraction_display(data['frac1'].numerator, data['frac1'].denominator)
    frac2_html = format_fraction_display(data['frac2'].numerator, data['frac2'].denominator)
    
    st.markdown(
        f"""
        <div style="font-size: 28px; margin: 20px 0; text-align: center;">
            {frac1_html} + {frac2_html} = 
            <span style="display: inline-block; width: 100px; height: 40px; 
                        border: 2px solid #1E90FF; background-color: #E6F3FF;
                        vertical-align: middle; margin-left: 10px;"></span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display the instruction
    st.markdown("**Use the model to help you.**")
    
    # Display visual model
    create_visual_model(data['frac1'], data['frac2'], data['lcd'])
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            answer_input = st.text_input(
                "Your answer (as a fraction):",
                placeholder="e.g., 3/4 or 5/8",
                key="user_answer_input",
                label_visibility="collapsed"
            )
            
            submit_button = st.form_submit_button(
                "Submit", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            # Parse the answer
            parsed_answer = parse_fraction_answer(answer_input)
            
            if parsed_answer is None:
                st.error("❌ Please enter a valid fraction (e.g., 3/4)")
            else:
                st.session_state.user_answer = parsed_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.score["attempted"] += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
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
            if success_rate >= 0.8 and st.session_state.unlike_model_difficulty < 4:
                st.session_state.unlike_model_difficulty += 1
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.unlike_model_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
        
        # Show step-by-step solution
        show_solution()
        
        # Decrease difficulty if struggling
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate < 0.5 and st.session_state.unlike_model_difficulty > 1:
                st.session_state.unlike_model_difficulty -= 1
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.unlike_model_difficulty}**")

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['frac1']} + {data['frac2']}
        
        **Step 1: Find a common denominator**
        - The denominators are {data['frac1'].denominator} and {data['frac2'].denominator}
        - The least common denominator (LCD) is {data['lcd']}
        
        **Step 2: Convert to equivalent fractions**
        - {data['frac1']} = {data['frac1_expanded']}
        - {data['frac2']} = {data['frac2_expanded']}
        
        **Step 3: Add the fractions**
        - {data['frac1_expanded']} + {data['frac2_expanded']} = {data['frac1_expanded'].numerator + data['frac2_expanded'].numerator}/{data['lcd']}
        
        **Step 4: Simplify if possible**
        - Final answer: {st.session_state.correct_answer}
        
        **💡 The model shows:** How the fractions are represented as colored blocks to help visualize the addition!
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer