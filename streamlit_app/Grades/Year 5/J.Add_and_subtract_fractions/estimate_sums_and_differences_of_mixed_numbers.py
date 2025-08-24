import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Estimate sums and differences of mixed numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/estimate_sums_and_differences_of_mixed_numbers.py
    """
    # Initialize session state for difficulty and score
    if "estimate_difficulty" not in st.session_state:
        st.session_state.estimate_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "estimate_score" not in st.session_state:
        st.session_state.estimate_score = 0
        st.session_state.estimate_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.operation = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🎯 Estimate Sums and Differences of Mixed Numbers")
    st.markdown("*Round to the nearest whole number, then calculate*")
    st.markdown("---")
    
    # Difficulty and score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        st.markdown(f"**Difficulty:** {difficulty_names[st.session_state.estimate_difficulty]}")
        st.markdown(f"**Score:** {st.session_state.estimate_score}/{st.session_state.estimate_attempts}")
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
    with st.expander("💡 **Estimation Tips**", expanded=False):
        st.markdown("""
        ### How to Estimate with Mixed Numbers:
        
        1. **Round each mixed number** to the nearest whole number
        2. **Apply the operation** (add or subtract) to the rounded numbers
        3. **Check your work** - is your estimate reasonable?
        
        ### Rounding Rules:
        - If fraction ≥ 1/2, round UP
        - If fraction < 1/2, round DOWN
        
        ### Examples:
        - **3 3/4** → rounds to **4** (3/4 > 1/2)
        - **5 1/3** → rounds to **5** (1/3 < 1/2)
        - **2 1/2** → rounds to **3** (1/2 = 1/2, round up)
        - **8 5/6** → rounds to **9** (5/6 > 1/2)
        
        ### Quick Fraction Comparisons to 1/2:
        - 1/3, 1/4, 2/5 are **less than 1/2**
        - 2/3, 3/4, 3/5, 4/5 are **greater than 1/2**
        - 2/4, 3/6, 4/8 **equal 1/2**
        """)

def generate_new_problem():
    """Generate a new estimation problem"""
    difficulty = st.session_state.estimate_difficulty
    operation = random.choice(["add", "subtract"])
    
    if difficulty == 1:  # Easy - smaller numbers, clear rounding
        if operation == "add":
            # Generate mixed numbers with clear rounding cases
            whole1 = random.randint(1, 20)
            whole2 = random.randint(1, 20)
            
            # Choose fractions that clearly round up or down
            clear_fractions = [
                (1, 4), (1, 3), (1, 5), (1, 6),  # Clearly < 1/2
                (3, 4), (2, 3), (4, 5), (5, 6),  # Clearly > 1/2
                (1, 2), (2, 4), (3, 6)            # Exactly 1/2
            ]
            
            num1, denom1 = random.choice(clear_fractions)
            num2, denom2 = random.choice(clear_fractions)
            
        else:  # subtract
            # Ensure valid subtraction
            whole1 = random.randint(10, 30)
            whole2 = random.randint(1, whole1 - 1)
            
            clear_fractions = [(1, 4), (3, 4), (1, 3), (2, 3), (1, 5), (4, 5)]
            num1, denom1 = random.choice(clear_fractions)
            num2, denom2 = random.choice(clear_fractions)
    
    elif difficulty == 2:  # Medium - larger numbers, mixed rounding
        if operation == "add":
            whole1 = random.randint(20, 100)
            whole2 = random.randint(10, 100)
            
            # More varied fractions
            fractions = [
                (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
                (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8), (1, 10), (7, 10), (9, 10)
            ]
            
            num1, denom1 = random.choice(fractions)
            num2, denom2 = random.choice(fractions)
            
        else:  # subtract
            whole1 = random.randint(50, 200)
            whole2 = random.randint(10, whole1 - 10)
            
            fractions = [
                (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
                (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8)
            ]
            num1, denom1 = random.choice(fractions)
            num2, denom2 = random.choice(fractions)
    
    else:  # Hard - very large numbers, tricky fractions
        if operation == "add":
            whole1 = random.randint(100, 500)
            whole2 = random.randint(50, 500)
            
            # Include harder to judge fractions
            hard_fractions = [
                (3, 7), (4, 7), (2, 7), (5, 7),  # Sevenths
                (3, 8), (5, 8), (7, 8),          # Eighths
                (4, 9), (5, 9), (7, 9),          # Ninths
                (3, 11), (5, 11), (7, 11),       # Elevenths
                (5, 12), (7, 12), (11, 12)       # Twelfths
            ]
            
            num1, denom1 = random.choice(hard_fractions)
            num2, denom2 = random.choice(hard_fractions)
            
        else:  # subtract
            whole1 = random.randint(200, 500)
            whole2 = random.randint(50, whole1 - 50)
            
            hard_fractions = [
                (3, 7), (4, 7), (2, 7), (5, 7),
                (3, 8), (5, 8), (7, 8),
                (4, 9), (5, 9), (7, 9),
                (3, 11), (5, 11), (7, 11),
                (5, 12), (7, 12), (11, 12)
            ]
            num1, denom1 = random.choice(hard_fractions)
            num2, denom2 = random.choice(hard_fractions)
    
    # Create mixed numbers
    mixed1 = {"whole": whole1, "num": num1, "denom": denom1}
    mixed2 = {"whole": whole2, "num": num2, "denom": denom2}
    
    # Calculate rounded values
    rounded1 = round_mixed_number(mixed1)
    rounded2 = round_mixed_number(mixed2)
    
    # Calculate correct answer
    if operation == "add":
        correct_answer = rounded1 + rounded2
    else:
        correct_answer = rounded1 - rounded2
    
    # Store problem
    st.session_state.current_problem = {
        "mixed1": mixed1,
        "mixed2": mixed2,
        "rounded1": rounded1,
        "rounded2": rounded2
    }
    st.session_state.operation = operation
    st.session_state.correct_answer = correct_answer
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def round_mixed_number(mixed):
    """Round a mixed number to the nearest whole number"""
    fraction_value = mixed["num"] / mixed["denom"]
    if fraction_value >= 0.5:
        return mixed["whole"] + 1
    else:
        return mixed["whole"]

def format_mixed_number(mixed):
    """Format mixed number for display (text version)"""
    if mixed["num"] == 0:
        return str(mixed["whole"])
    return f"{mixed['whole']} {mixed['num']}/{mixed['denom']}"

def display_problem():
    """Display the current estimation problem"""
    problem = st.session_state.current_problem
    operation = st.session_state.operation
    
    # Choose appropriate text
    if operation == "add":
        instruction = "Estimate the sum. Round each number to the nearest whole number, then add."
        result_text = "The sum is approximately"
    else:
        instruction = "Estimate the difference. Round each number to the nearest whole number, then subtract."
        result_text = "The difference is approximately"
    
    # Display instruction
    st.markdown(f"### {instruction}")
    
    # Create the problem display using columns for proper fraction formatting
    st.markdown("")  # Add some space
    
    # Create a container for the problem
    problem_container = st.container()
    with problem_container:
        # Use columns to center the problem
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            # Display the problem using LaTeX for proper fraction rendering
            mixed1 = problem["mixed1"]
            mixed2 = problem["mixed2"]
            
            # Format as LaTeX
            if mixed1["num"] == 0:
                latex1 = f"{mixed1['whole']}"
            else:
                latex1 = f"{mixed1['whole']}\\frac{{{mixed1['num']}}}{{{mixed1['denom']}}}"
            
            if mixed2["num"] == 0:
                latex2 = f"{mixed2['whole']}"
            else:
                latex2 = f"{mixed2['whole']}\\frac{{{mixed2['num']}}}{{{mixed2['denom']}}}"
            
            operation_symbol = "+" if operation == "add" else "-"
            
            # Display using LaTeX
            st.latex(f"{latex1} {operation_symbol} {latex2}")
    
    st.markdown("")  # Add some space
    
    # Answer input
    with st.form("estimate_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            answer = st.number_input(
                f"{result_text}",
                min_value=-1000,
                max_value=1000,
                step=1,
                key="estimate_input"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit:
            st.session_state.user_answer = int(answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.session_state.estimate_attempts += 1
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Great estimation!**")
        st.session_state.estimate_score += 1
        
        # Increase difficulty
        if st.session_state.estimate_score % 3 == 0:
            old_difficulty = st.session_state.estimate_difficulty
            st.session_state.estimate_difficulty = min(3, old_difficulty + 1)
            if st.session_state.estimate_difficulty > old_difficulty:
                st.info(f"⬆️ **Level up! Moving to {['', 'Easy', 'Medium', 'Hard'][st.session_state.estimate_difficulty]} problems.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer}.**")
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if struggling
        if st.session_state.estimate_attempts > 0:
            accuracy = st.session_state.estimate_score / st.session_state.estimate_attempts
            if accuracy < 0.5 and st.session_state.estimate_attempts % 5 == 0:
                old_difficulty = st.session_state.estimate_difficulty
                st.session_state.estimate_difficulty = max(1, old_difficulty - 1)
                if st.session_state.estimate_difficulty < old_difficulty:
                    st.warning(f"⬇️ **Let's practice with {['', 'Easy', 'Medium', 'Hard'][st.session_state.estimate_difficulty]} problems.**")

def show_explanation():
    """Show explanation for the estimation"""
    problem = st.session_state.current_problem
    operation = st.session_state.operation
    
    with st.expander("📖 **See How to Estimate**", expanded=True):
        st.markdown("### Step 1: Round each mixed number")
        
        # First number
        mixed1 = problem["mixed1"]
        frac1_value = mixed1["num"] / mixed1["denom"]
        
        st.markdown(f"**{format_mixed_number(mixed1)}**")
        st.markdown(f"- Fraction part: {mixed1['num']}/{mixed1['denom']} = {frac1_value:.3f}")
        st.markdown(f"- Is {mixed1['num']}/{mixed1['denom']} ≥ 1/2? **{'Yes' if frac1_value >= 0.5 else 'No'}**")
        st.markdown(f"- Rounds to: **{problem['rounded1']}**")
        
        st.markdown("")
        
        # Second number
        mixed2 = problem["mixed2"]
        frac2_value = mixed2["num"] / mixed2["denom"]
        
        st.markdown(f"**{format_mixed_number(mixed2)}**")
        st.markdown(f"- Fraction part: {mixed2['num']}/{mixed2['denom']} = {frac2_value:.3f}")
        st.markdown(f"- Is {mixed2['num']}/{mixed2['denom']} ≥ 1/2? **{'Yes' if frac2_value >= 0.5 else 'No'}**")
        st.markdown(f"- Rounds to: **{problem['rounded2']}**")
        
        # Step 2: Calculate
        st.markdown("### Step 2: Calculate with rounded numbers")
        if operation == "add":
            st.markdown(f"{problem['rounded1']} + {problem['rounded2']} = **{st.session_state.correct_answer}**")
        else:
            st.markdown(f"{problem['rounded1']} − {problem['rounded2']} = **{st.session_state.correct_answer}**")
        
        # Estimation tip
        st.markdown("""
        ### Remember:
        - Round **before** calculating
        - This gives an **estimate**, not the exact answer
        - Estimates help check if exact answers are reasonable
        """)

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.operation = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer