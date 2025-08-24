import streamlit as st
import random
from fractions import Fraction
from math import gcd

def run():
    """
    Main function to run the Add and Subtract Mixed Numbers with Unlike Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_mixed_numbers_with_unlike_denominators.py
    """
    # Initialize session state for adaptive difficulty
    if "mixed_difficulty_level" not in st.session_state:
        st.session_state.mixed_difficulty_level = 1
    
    if "mixed_streak" not in st.session_state:
        st.session_state.mixed_streak = 0
    
    if "mixed_mistakes" not in st.session_state:
        st.session_state.mixed_mistakes = 0
    
    if "current_mixed_problem" not in st.session_state:
        st.session_state.current_mixed_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Style text input */
    input[type="text"] {
        font-size: 18px !important;
        text-align: center !important;
    }
    
    /* Mixed number display */
    .mixed-number {
        display: inline-block;
        font-size: 36px;
        margin: 0 10px;
    }
    
    .whole-part {
        display: inline-block;
        margin-right: 8px;
    }
    
    .fraction-part {
        display: inline-block;
        text-align: center;
        vertical-align: middle;
    }
    
    .numerator {
        border-bottom: 3px solid black;
        padding: 0 8px;
    }
    
    .denominator {
        padding: 0 8px;
    }
    
    /* Submit button */
    div.stButton > button[type="submit"] {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🔢 Add and Subtract Mixed Numbers with Unlike Denominators")
    st.markdown("*Practice with mixed numbers (whole numbers and fractions)*")
    
    # Difficulty and progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        level_names = {1: "Starter", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Master"}
        level_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🟣"}
        level = st.session_state.mixed_difficulty_level
        st.markdown(f"**Level:** {level_colors[level]} {level_names[level]}")
        st.progress(level / 5, text=f"Progress: Level {level}/5")
    
    with col2:
        if st.session_state.mixed_streak > 0:
            st.metric("Streak", f"🔥 {st.session_state.mixed_streak}")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    st.markdown("---")
    
    # Generate new problem if needed
    if st.session_state.current_mixed_problem is None:
        generate_mixed_problem()
    
    # Display problem
    display_mixed_problem()
    
    # Instructions
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **How to Add/Subtract Mixed Numbers**", expanded=False):
        st.markdown("""
        ### Method 1: Convert to Improper Fractions
        **Example: 2 3/4 + 1 1/2**
        1. Convert to improper fractions:
           - 2 3/4 = 11/4
           - 1 1/2 = 3/2
        2. Find LCD: LCD of 4 and 2 = 4
        3. Convert: 3/2 = 6/4
        4. Add: 11/4 + 6/4 = 17/4
        5. Convert back: 17/4 = 4 1/4
        
        ### Method 2: Add/Subtract Parts Separately
        **Example: 2 3/4 + 1 1/2**
        1. Add whole numbers: 2 + 1 = 3
        2. Add fractions: 3/4 + 1/2 = 3/4 + 2/4 = 5/4 = 1 1/4
        3. Combine: 3 + 1 1/4 = 4 1/4
        
        ### For Subtraction:
        - If the first fraction is smaller, borrow 1 from the whole number
        - Example: 3 1/4 - 1 3/4
          - Can't do 1/4 - 3/4
          - Borrow: 3 1/4 = 2 5/4
          - Now: 2 5/4 - 1 3/4 = 1 2/4 = 1 1/2
        
        ### Difficulty Levels:
        - **Level 1**: Simple fractions (halves, quarters)
        - **Level 2**: Common denominators (2, 3, 4, 6)
        - **Level 3**: More denominators (up to 12)
        - **Level 4**: Larger numbers and fractions
        - **Level 5**: Complex problems requiring regrouping
        """)

def generate_mixed_problem():
    """Generate an adaptive mixed number problem"""
    level = st.session_state.mixed_difficulty_level
    
    # Parameters by level
    level_params = {
        1: {
            "whole_range": (1, 3),
            "denominators": [2, 4],
            "allow_regrouping": False
        },
        2: {
            "whole_range": (1, 5),
            "denominators": [2, 3, 4, 6],
            "allow_regrouping": False
        },
        3: {
            "whole_range": (1, 8),
            "denominators": [2, 3, 4, 5, 6, 8, 10, 12],
            "allow_regrouping": True
        },
        4: {
            "whole_range": (2, 12),
            "denominators": [3, 4, 5, 6, 8, 9, 10, 12],
            "allow_regrouping": True
        },
        5: {
            "whole_range": (3, 15),
            "denominators": [4, 5, 6, 8, 9, 10, 12, 15, 16],
            "allow_regrouping": True
        }
    }
    
    params = level_params[level]
    operation = random.choice(["add", "subtract"])
    
    # Generate mixed numbers
    attempts = 0
    while attempts < 50:
        # Generate whole parts
        whole1 = random.randint(*params["whole_range"])
        whole2 = random.randint(*params["whole_range"])
        
        # Generate fractions
        denom1 = random.choice(params["denominators"])
        denom2 = random.choice([d for d in params["denominators"] if d != denom1])
        
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)
        
        # Create mixed numbers as improper fractions for calculation
        mixed1 = Fraction(whole1 * denom1 + num1, denom1)
        mixed2 = Fraction(whole2 * denom2 + num2, denom2)
        
        # For subtraction, ensure positive result
        if operation == "subtract":
            if mixed1 < mixed2:
                mixed1, mixed2 = mixed2, mixed1
                whole1, whole2 = whole2, whole1
                num1, denom1, num2, denom2 = num2, denom2, num1, denom1
            
            result = mixed1 - mixed2
            
            # Check if regrouping is needed
            frac1 = Fraction(num1, denom1)
            frac2 = Fraction(num2, denom2)
            needs_regrouping = frac1 < frac2
            
            # For lower levels, avoid regrouping
            if not params["allow_regrouping"] and needs_regrouping:
                continue
                
            # For higher levels, ensure some problems need regrouping
            if level >= 3 and random.random() < 0.3 and not needs_regrouping:
                continue
        else:
            result = mixed1 + mixed2
            # For easier levels, keep results reasonable
            if level <= 2 and result > 10:
                continue
        
        # Ensure positive result
        if result > 0:
            break
        
        attempts += 1
    
    st.session_state.current_mixed_problem = {
        "operation": operation,
        "whole1": whole1,
        "num1": num1,
        "denom1": denom1,
        "whole2": whole2,
        "num2": num2,
        "denom2": denom2,
        "mixed1": mixed1,
        "mixed2": mixed2,
        "result": result
    }
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_mixed_problem():
    """Display the current mixed number problem"""
    problem = st.session_state.current_mixed_problem
    
    # Display operation type
    if problem["operation"] == "add":
        st.markdown("### Add. Write your answer as a fraction or as a whole or mixed number.")
    else:
        st.markdown("### Subtract. Write your answer as a fraction or as a whole or mixed number.")
    
    # Add spacing
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Create the problem layout
    col1, col2, col3, col4, col5 = st.columns([2, 0.5, 2, 0.5, 3])
    
    with col1:
        # First mixed number
        st.markdown(f"""
        <div class="mixed-number">
            <span class="whole-part">{problem['whole1']}</span>
            <span class="fraction-part">
                <sup>{problem['num1']}</sup>⁄<sub>{problem['denom1']}</sub>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        op_symbol = "+" if problem["operation"] == "add" else "−"
        st.markdown(f"<div style='text-align: center; font-size: 36px; margin-top: 5px;'>{op_symbol}</div>", 
                   unsafe_allow_html=True)
    
    with col3:
        # Second mixed number
        st.markdown(f"""
        <div class="mixed-number">
            <span class="whole-part">{problem['whole2']}</span>
            <span class="fraction-part">
                <sup>{problem['num2']}</sup>⁄<sub>{problem['denom2']}</sub>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div style='text-align: center; font-size: 36px; margin-top: 5px;'>=</div>", 
                   unsafe_allow_html=True)
    
    with col5:
        # Answer input
        if not st.session_state.answer_submitted:
            answer = st.text_input("", placeholder="Answer", 
                                 key="answer_input", label_visibility="collapsed")
        else:
            # Show result
            result_str = format_mixed_number(problem['result'])
            result_color = "green" if st.session_state.user_correct else "red"
            result_symbol = "✓" if st.session_state.user_correct else "✗"
            st.markdown(f"""
            <div style="font-size: 36px; color: {result_color}; margin-top: 5px;">
                {result_symbol} {result_str}
            </div>
            """, unsafe_allow_html=True)
    
    # Submit button
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Problem →", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def format_mixed_number(fraction):
    """Format a fraction as a mixed number string"""
    if fraction.denominator == 1:
        return str(fraction.numerator)
    elif fraction.numerator < fraction.denominator:
        return f"{fraction.numerator}/{fraction.denominator}"
    else:
        whole = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        if remainder == 0:
            return str(whole)
        else:
            return f"{whole} {remainder}/{fraction.denominator}"

def parse_mixed_number(input_str):
    """Parse user input as a mixed number"""
    input_str = input_str.strip()
    
    # Try to parse as mixed number (e.g., "2 3/4")
    if ' ' in input_str:
        parts = input_str.split(' ', 1)
        if len(parts) == 2:
            try:
                whole = int(parts[0])
                if '/' in parts[1]:
                    frac_parts = parts[1].split('/')
                    if len(frac_parts) == 2:
                        num = int(frac_parts[0])
                        denom = int(frac_parts[1])
                        if denom == 0:
                            return None, "Denominator cannot be zero"
                        return Fraction(whole * denom + num, denom), None
            except ValueError:
                pass
    
    # Try to parse as fraction (e.g., "3/4")
    if '/' in input_str:
        parts = input_str.split('/')
        if len(parts) == 2:
            try:
                num = int(parts[0])
                denom = int(parts[1])
                if denom == 0:
                    return None, "Denominator cannot be zero"
                return Fraction(num, denom), None
            except ValueError:
                pass
    
    # Try to parse as whole number
    try:
        whole = int(input_str)
        return Fraction(whole, 1), None
    except ValueError:
        pass
    
    return None, "Invalid format. Use: whole number (5), fraction (3/4), or mixed (2 1/2)"

def check_answer():
    """Check answer and update difficulty"""
    user_input = st.session_state.answer_input
    
    if not user_input:
        st.warning("Please enter an answer.")
        return
    
    # Parse user answer
    user_answer, error = parse_mixed_number(user_input)
    
    if error:
        st.error(error)
        return
    
    # Check if correct
    correct_answer = st.session_state.current_mixed_problem['result']
    st.session_state.user_correct = (user_answer == correct_answer)
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    
    # Update difficulty
    if st.session_state.user_correct:
        st.session_state.mixed_streak += 1
        st.session_state.mixed_mistakes = 0
        
        if st.session_state.mixed_streak >= 3 and st.session_state.mixed_difficulty_level < 5:
            st.session_state.mixed_difficulty_level += 1
            st.session_state.mixed_streak = 0
    else:
        st.session_state.mixed_mistakes += 1
        st.session_state.mixed_streak = 0
        
        if st.session_state.mixed_mistakes >= 2 and st.session_state.mixed_difficulty_level > 1:
            st.session_state.mixed_difficulty_level -= 1
            st.session_state.mixed_mistakes = 0
    
    st.rerun()

def show_feedback():
    """Display feedback with solution"""
    problem = st.session_state.current_mixed_problem
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Excellent work!**")
        if st.session_state.mixed_streak == 2:
            st.info("🔥 **One more correct answer to level up!**")
        elif st.session_state.mixed_streak == 0 and st.session_state.mixed_difficulty_level < 5:
            st.balloons()
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.mixed_difficulty_level}**")
    else:
        correct_str = format_mixed_number(problem['result'])
        st.error(f"❌ **Not quite. The correct answer is {correct_str}**")
        
        if st.session_state.mixed_mistakes == 1:
            st.warning("💡 **Tip:** Try converting to improper fractions first.")
        
        # Show solution
        with st.expander("📖 **See step-by-step solution**", expanded=True):
            show_solution(problem)

def show_solution(problem):
    """Show step-by-step solution"""
    st.markdown("### Step-by-step solution:")
    
    # Method 1: Convert to improper fractions
    st.markdown("**Method: Convert to Improper Fractions**")
    
    # Step 1: Convert mixed to improper
    improper1 = problem['whole1'] * problem['denom1'] + problem['num1']
    improper2 = problem['whole2'] * problem['denom2'] + problem['num2']
    
    st.markdown(f"""
    **Step 1: Convert to improper fractions**
    - {problem['whole1']} {problem['num1']}/{problem['denom1']} = {improper1}/{problem['denom1']}
    - {problem['whole2']} {problem['num2']}/{problem['denom2']} = {improper2}/{problem['denom2']}
    """)
    
    # Step 2: Find LCD
    lcd = abs(problem['denom1'] * problem['denom2']) // gcd(problem['denom1'], problem['denom2'])
    
    st.markdown(f"""
    **Step 2: Find LCD**
    - LCD of {problem['denom1']} and {problem['denom2']} = {lcd}
    """)
    
    # Step 3: Convert to equivalent fractions
    equiv1 = improper1 * (lcd // problem['denom1'])
    equiv2 = improper2 * (lcd // problem['denom2'])
    
    st.markdown(f"""
    **Step 3: Convert to equivalent fractions**
    - {improper1}/{problem['denom1']} = {equiv1}/{lcd}
    - {improper2}/{problem['denom2']} = {equiv2}/{lcd}
    """)
    
    # Step 4: Calculate
    op_symbol = "+" if problem['operation'] == "add" else "−"
    if problem['operation'] == "add":
        result_num = equiv1 + equiv2
    else:
        result_num = equiv1 - equiv2
    
    st.markdown(f"""
    **Step 4: {problem['operation'].capitalize()}**
    - {equiv1}/{lcd} {op_symbol} {equiv2}/{lcd} = {result_num}/{lcd}
    """)
    
    # Step 5: Simplify and convert to mixed
    result_simplified = Fraction(result_num, lcd)
    result_str = format_mixed_number(result_simplified)
    
    st.markdown(f"""
    **Step 5: Simplify and convert to mixed number**
    - {result_num}/{lcd} = **{result_str}**
    """)
    
    # Show regrouping note for subtraction if needed
    if problem['operation'] == 'subtract':
        frac1 = Fraction(problem['num1'], problem['denom1'])
        frac2 = Fraction(problem['num2'], problem['denom2'])
        if frac1 < frac2:
            st.info("💡 **Note:** This problem required regrouping (borrowing) from the whole number.")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_mixed_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_answer'):
        del st.session_state.user_answer
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct