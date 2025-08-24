import streamlit as st
import random
from fractions import Fraction
import re

def run():
    """
    Main function to run the Add and subtract mixed numbers with like denominators activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_mixed_numbers_with_like_denominators.py
    """
    # Initialize session state
    if "mixed_difficulty" not in st.session_state:
        st.session_state.mixed_difficulty = 1  # Start with simple problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.score = {"correct": 0, "attempted": 0}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🔢 Add & Subtract Mixed Numbers")
    st.markdown("*Add and subtract mixed numbers with like denominators*")
    st.markdown("---")
    
    # Display score and difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Difficulty indicator
        diff_names = ["Easy", "Medium", "Hard", "Expert"]
        diff_level = st.session_state.mixed_difficulty
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
        ### How to Add/Subtract Mixed Numbers with Like Denominators:
        
        **Step-by-Step Method:**
        1. **Add/Subtract the whole numbers**
        2. **Add/Subtract the fractions** (same denominator)
        3. **Simplify if needed** (convert improper fractions)
        
        ### Example - Addition:
        **3 2/5 + 1 3/5:**
        - Whole numbers: 3 + 1 = 4
        - Fractions: 2/5 + 3/5 = 5/5 = 1
        - Result: 4 + 1 = 5
        
        ### Example - Subtraction:
        **5 1/4 - 2 3/4:**
        - Can't subtract 3/4 from 1/4
        - Borrow 1 from 5: 4 5/4 - 2 3/4
        - Now: 4 - 2 = 2 and 5/4 - 3/4 = 2/4 = 1/2
        - Result: 2 1/2
        
        ### How to Enter Your Answer:
        - **Whole number:** Just type the number (e.g., 5)
        - **Fraction:** Type as numerator/denominator (e.g., 3/4)
        - **Mixed number:** Type as whole fraction (e.g., 2 3/4 or 2 3/4)
        
        ### Remember:
        - Always simplify your final answer
        - Watch for borrowing in subtraction
        - Check if your answer makes sense!
        """)

def generate_new_problem():
    """Generate a new mixed number problem based on difficulty"""
    difficulty = st.session_state.mixed_difficulty
    
    # Define denominators by difficulty
    if difficulty == 1:
        denominators = [2, 3, 4, 5]      # Easy
        whole_range = (1, 5)
    elif difficulty == 2:
        denominators = [6, 8, 10]        # Medium
        whole_range = (2, 10)
    elif difficulty == 3:
        denominators = [12, 15, 16]      # Hard
        whole_range = (3, 15)
    else:
        denominators = [20, 24, 25]      # Expert
        whole_range = (5, 20)
    
    # Choose operation
    operation = random.choice(["add", "subtract"])
    
    # Generate mixed numbers
    denominator = random.choice(denominators)
    
    if operation == "add":
        # For addition, generate two mixed numbers
        whole1 = random.randint(whole_range[0], whole_range[1])
        num1 = random.randint(1, denominator - 1)
        
        whole2 = random.randint(whole_range[0], whole_range[1])
        num2 = random.randint(1, denominator - 1)
        
        # Calculate answer
        total_whole = whole1 + whole2
        total_num = num1 + num2
        
        # Handle improper fraction
        if total_num >= denominator:
            extra_whole = total_num // denominator
            total_whole += extra_whole
            total_num = total_num % denominator
        
        # Create answer
        if total_num == 0:
            answer_str = str(total_whole)
            answer_value = total_whole
        else:
            answer_frac = Fraction(total_num, denominator)
            answer_str = f"{total_whole} {answer_frac}"
            answer_value = total_whole + answer_frac
            
    else:  # subtract
        # For subtraction, ensure first number is larger
        whole1 = random.randint(whole_range[0] + 2, whole_range[1])
        whole2 = random.randint(whole_range[0], min(whole1 - 1, whole_range[1] - 2))
        
        # Generate fractions
        num1 = random.randint(1, denominator - 1)
        num2 = random.randint(1, denominator - 1)
        
        # Handle borrowing if needed
        if num1 < num2:
            # Need to borrow
            whole1 -= 1
            num1 += denominator
        
        # Calculate answer
        result_whole = whole1 - whole2
        result_num = num1 - num2
        
        # Create answer
        if result_num == 0:
            answer_str = str(result_whole)
            answer_value = result_whole
        else:
            answer_frac = Fraction(result_num, denominator)
            answer_str = f"{result_whole} {answer_frac}"
            answer_value = result_whole + answer_frac
    
    # Store problem data
    st.session_state.problem_data = {
        "operation": operation,
        "whole1": whole1 if operation == "add" else whole1 + (1 if num1 >= denominator else 0),
        "num1": num1 if operation == "add" else num1 % denominator,
        "whole2": whole2,
        "num2": num2,
        "denominator": denominator,
        "answer_str": answer_str,
        "answer_value": answer_value
    }
    
    # Format problem text
    mixed1 = f"{st.session_state.problem_data['whole1']} {st.session_state.problem_data['num1']}/{denominator}"
    mixed2 = f"{whole2} {num2}/{denominator}"
    
    if operation == "add":
        st.session_state.current_problem = f"Add. Write your answer as a fraction or as a whole or mixed number."
        st.session_state.problem_equation = f"{mixed1} + {mixed2}"
    else:
        st.session_state.current_problem = f"Subtract. Write your answer as a fraction or as a whole or mixed number."
        st.session_state.problem_equation = f"{mixed1} − {mixed2}"
    
    st.session_state.correct_answer = answer_str

def parse_mixed_answer(answer_str):
    """Parse various answer formats: whole number, fraction, or mixed number"""
    answer_str = answer_str.strip()
    
    # Check for whole number only
    if answer_str.isdigit():
        return int(answer_str)
    
    # Check for fraction only (e.g., "3/4")
    fraction_match = re.match(r'^(\d+)\s*/\s*(\d+)$', answer_str)
    if fraction_match:
        num = int(fraction_match.group(1))
        denom = int(fraction_match.group(2))
        if denom > 0:
            return Fraction(num, denom)
    
    # Check for mixed number (e.g., "2 3/4" or "2 3/4")
    mixed_match = re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)$', answer_str)
    if mixed_match:
        whole = int(mixed_match.group(1))
        num = int(mixed_match.group(2))
        denom = int(mixed_match.group(3))
        if denom > 0:
            return whole + Fraction(num, denom)
    
    return None

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display the instruction
    st.markdown(f"### {st.session_state.current_problem}")
    
    # Display the equation in a nice format
    equation_parts = st.session_state.problem_equation.split(" ")
    
    # Create the equation display with larger font
    st.markdown(
        f"""
        <div style="font-size: 28px; font-weight: bold; margin: 30px 0; 
                    padding: 20px; background-color: #f0f0f0; 
                    border-radius: 10px; text-align: center;">
            {st.session_state.problem_equation} = 
            <span style="display: inline-block; width: 200px; height: 40px; 
                        border-bottom: 2px solid #333; vertical-align: middle;"></span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            answer_input = st.text_input(
                "Your answer:",
                placeholder="e.g., 5 or 3/4 or 2 1/2",
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
            parsed_answer = parse_mixed_answer(answer_input)
            
            if parsed_answer is None:
                st.error("❌ Please enter a valid answer (whole number, fraction, or mixed number)")
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
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if "user_answer" not in st.session_state:
        return
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.problem_data["answer_value"]
    
    # Compare answers (handle floating point comparison for mixed numbers)
    if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
        is_correct = abs(user_answer - correct_answer) < 0.0001
    else:
        is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success("🎉 **Correct! Great job!**")
        st.session_state.score["correct"] += 1
        
        # Show the complete equation
        st.markdown(f"### ✅ {st.session_state.problem_equation} = {st.session_state.correct_answer}")
        
        # Increase difficulty if doing well
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate >= 0.8 and st.session_state.mixed_difficulty < 4:
                st.session_state.mixed_difficulty += 1
                st.info(f"⬆️ **Excellent! Moving to Level {st.session_state.mixed_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{st.session_state.correct_answer}**")
        
        # Show step-by-step solution
        show_solution()
        
        # Decrease difficulty if struggling
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate < 0.5 and st.session_state.mixed_difficulty > 1:
                st.session_state.mixed_difficulty -= 1
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.mixed_difficulty}**")

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        if data["operation"] == "add":
            st.markdown(f"""
            ### Addition of Mixed Numbers:
            
            **Problem:** {st.session_state.problem_equation}
            
            **Step 1: Add the whole numbers**
            - {data['whole1']} + {data['whole2']} = {data['whole1'] + data['whole2']}
            
            **Step 2: Add the fractions**
            - {data['num1']}/{data['denominator']} + {data['num2']}/{data['denominator']} = {data['num1'] + data['num2']}/{data['denominator']}
            
            **Step 3: Simplify if needed**
            """)
            
            total_num = data['num1'] + data['num2']
            if total_num >= data['denominator']:
                extra_whole = total_num // data['denominator']
                remainder = total_num % data['denominator']
                st.markdown(f"""
                - {total_num}/{data['denominator']} = {extra_whole} {remainder}/{data['denominator']}
                - Add the extra whole: {data['whole1'] + data['whole2']} + {extra_whole} = {data['whole1'] + data['whole2'] + extra_whole}
                """)
            
            st.markdown(f"**Final Answer:** {st.session_state.correct_answer}")
            
        else:  # subtract
            st.markdown(f"""
            ### Subtraction of Mixed Numbers:
            
            **Problem:** {st.session_state.problem_equation}
            """)
            
            # Check if borrowing was needed
            original_num1 = data['num1']
            if data['num1'] >= data['denominator']:
                # Borrowing occurred
                st.markdown(f"""
                **Step 1: Check if we can subtract the fractions**
                - We need to subtract {data['num2']}/{data['denominator']} from {original_num1 % data['denominator']}/{data['denominator']}
                - Since {original_num1 % data['denominator']} < {data['num2']}, we need to borrow
                
                **Step 2: Borrow 1 from the whole number**
                - {data['whole1']} {original_num1 % data['denominator']}/{data['denominator']} = {data['whole1'] - 1} {data['denominator'] + (original_num1 % data['denominator'])}/{data['denominator']}
                
                **Step 3: Now subtract**
                - Whole numbers: {data['whole1'] - 1} - {data['whole2']} = {data['whole1'] - 1 - data['whole2']}
                - Fractions: {data['denominator'] + (original_num1 % data['denominator'])}/{data['denominator']} - {data['num2']}/{data['denominator']} = {data['denominator'] + (original_num1 % data['denominator']) - data['num2']}/{data['denominator']}
                """)
            else:
                st.markdown(f"""
                **Step 1: Subtract the whole numbers**
                - {data['whole1']} - {data['whole2']} = {data['whole1'] - data['whole2']}
                
                **Step 2: Subtract the fractions**
                - {data['num1']}/{data['denominator']} - {data['num2']}/{data['denominator']} = {data['num1'] - data['num2']}/{data['denominator']}
                """)
            
            # Simplify final fraction if needed
            result_num = data['num1'] - data['num2']
            if result_num > 0:
                simplified = Fraction(result_num, data['denominator'])
                if simplified.denominator != data['denominator']:
                    st.markdown(f"""
                    **Step 3: Simplify the fraction**
                    - {result_num}/{data['denominator']} = {simplified}
                    """)
            
            st.markdown(f"**Final Answer:** {st.session_state.correct_answer}")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer