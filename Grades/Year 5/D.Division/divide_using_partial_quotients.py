import streamlit as st
import random

def run():
    """
    Main function to run the Long Division practice activity.
    """
    # Initialize session state for difficulty and game state
    if "long_division_difficulty" not in st.session_state:
        st.session_state.long_division_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("➗ Long Division")
    st.markdown("*Step-by-step traditional division method*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.long_division_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Simple", 2: "Intermediate", 3: "Advanced", 4: "Expert"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Simple**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
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
        ### How to Do Long Division:
        
        **Example: 44 ÷ 2 = 22**
        
        1. **Fill quotient boxes** at the top
        2. **Divide step by step** from left to right  
        3. **Multiply and subtract** for each step
        4. **Show your work** in the boxes below
        
        ### The Process:
        - Look at first digits of dividend
        - How many times does divisor go into it?
        - Write that number in quotient box
        - Multiply quotient × divisor
        - Subtract from working number
        - Bring down next digit and repeat
        
        ### Tips:
        - Start from the left
        - Estimate carefully
        - Always multiply then subtract
        - Line up numbers properly
        - Check your work
        """)

def generate_new_problem():
    """Generate a new long division problem"""
    difficulty = st.session_state.long_division_difficulty
    
    if difficulty == 1:
        divisors = [2, 3, 4, 5]
        quotient_range = (10, 25)
    elif difficulty == 2:
        divisors = [2, 3, 4, 5, 6, 7, 8, 9]
        quotient_range = (15, 50)
    elif difficulty == 3:
        divisors = [3, 4, 5, 6, 7, 8, 9]
        quotient_range = (50, 150)
    else:
        divisors = [6, 7, 8, 9, 11, 12]
        quotient_range = (100, 300)
    
    divisor = random.choice(divisors)
    quotient = random.randint(*quotient_range)
    has_remainder = random.random() < (difficulty - 1) * 0.15
    remainder = random.randint(1, divisor - 1) if has_remainder else 0
    dividend = quotient * divisor + remainder
    
    st.session_state.problem_data = {
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "remainder": remainder
    }
    st.session_state.current_problem = f"Solve {dividend} ÷ {divisor} using long division."

def display_problem():
    """Display the current problem interface"""
    data = st.session_state.problem_data
    
    st.markdown("### ➗ Problem:")
    st.markdown(f"**{st.session_state.current_problem}**")
    st.markdown("---")
    
    with st.form("long_division_form", clear_on_submit=False):
        create_division_layout(data)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            check_answers()
    
    handle_feedback_and_next()

def create_division_layout(data):
    """Create a clean long division layout with proper alignment"""
    dividend = data["dividend"]
    divisor = data["divisor"]
    quotient = data["quotient"]
    remainder = data["remainder"]
    
    quotient_str = str(quotient)
    dividend_str = str(dividend)
    
    # Simplified CSS for clean layout
    st.markdown("""
    <style>
    .quotient-area {
        margin-left: 50px;
        margin-bottom: 20px;
    }
    .division-symbol {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 30px 0;
        font-size: 32px;
        font-weight: bold;
    }
    .divisor-num {
        color: #1976D2;
        margin-right: 20px;
        font-size: 36px;
    }
    .dividend-container {
        border-top: 4px solid #333;
        border-left: 4px solid #333;
        padding: 15px 20px;
        background: white;
    }
    .dividend-num {
        color: #C2185B;
        font-size: 36px;
        letter-spacing: 8px;
        font-weight: bold;
    }
    .work-area {
        margin-left: 180px;
        margin-top: 20px;
        width: 180px;
    }
    .step-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 15px 0;
        font-size: 24px;
    }
    .minus-sign {
        color: #d32f2f;
        font-weight: bold;
        font-size: 28px;
    }
    .step-line {
        border-bottom: 3px solid #333;
        width: 150px;
        margin: 10px 0;
    }
    .step-result {
        font-size: 28px;
        font-weight: bold;
        color: #333;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Start clean container
    st.markdown('<div class="clean-division">', unsafe_allow_html=True)
    
    # Simple quotient input without decorative container
    st.markdown("**Fill in the quotient digits:**")
    
    # Quotient input boxes aligned with division symbol
    quotient_cols = st.columns([1, 1, 1, 1, 2])  # Left-aligned layout
    user_quotient_inputs = []
    
    for i, digit in enumerate(quotient_str):
        with quotient_cols[i + 1]:
            q_input = st.number_input(
                f"Digit {i+1}",
                min_value=0,
                max_value=9,
                value=0,
                key=f"quotient_{i}",
                label_visibility="collapsed"
            )
            user_quotient_inputs.append(q_input)
    
    # Division symbol
    st.markdown(f"""
    <div class="division-symbol">
        <span class="divisor-num">{divisor}</span>
        <div class="dividend-container">
            <span class="dividend-num">{dividend_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Work steps aligned under the dividend
    st.markdown('<div class="work-area">', unsafe_allow_html=True)
    
    division_steps = calculate_long_division_steps(dividend, divisor)
    user_work_inputs = []
    work_steps = division_steps['work_steps']
    
    for i, step in enumerate(work_steps):
        if step['type'] == 'multiply_subtract':
            # Simple input row aligned under dividend
            col1, col2, col3, col4 = st.columns([0.5, 1.5, 0.5, 2])
            
            with col1:
                st.markdown('<span class="minus-sign">−</span>', unsafe_allow_html=True)
            
            with col2:
                subtract_input = st.number_input(
                    f"Work step {i+1}",
                    min_value=0,
                    max_value=9999,
                    value=0,
                    key=f"work_{i}",
                    label_visibility="collapsed"
                )
                user_work_inputs.append(subtract_input)
            
            with col3:
                st.markdown("**←**")
            
            with col4:
                st.markdown(f"**{step['quotient_digit']} × {divisor}**")
            
            # Division line
            st.markdown('<div class="step-line"></div>', unsafe_allow_html=True)
            
            # Result
            st.markdown(f'<div class="step-result">{step["remainder"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close work-area
    st.markdown('</div>', unsafe_allow_html=True)  # Close clean-division
    
    # Store user inputs
    st.session_state.user_quotient_inputs = user_quotient_inputs
    st.session_state.user_work_inputs = user_work_inputs

def calculate_long_division_steps(dividend, divisor):
    """Calculate steps for long division"""
    steps = []
    quotient_digits = []
    dividend_str = str(dividend)
    working_number = 0
    
    for i, digit in enumerate(dividend_str):
        working_number = working_number * 10 + int(digit)
        
        if working_number >= divisor:
            q_digit = working_number // divisor
            quotient_digits.append(q_digit)
            product = q_digit * divisor
            remainder = working_number - product
            
            steps.append({
                'type': 'multiply_subtract',
                'quotient_digit': q_digit,
                'working_number': working_number,
                'product': product,
                'remainder': remainder
            })
            
            working_number = remainder
        else:
            if quotient_digits:
                quotient_digits.append(0)
        
        if i < len(dividend_str) - 1 and working_number > 0:
            steps.append({
                'type': 'bring_down',
                'digit': dividend_str[i + 1],
                'new_working_number': working_number * 10 + int(dividend_str[i + 1])
            })
    
    return {
        'quotient_digits': quotient_digits,
        'work_steps': steps,
        'final_remainder': working_number
    }

def check_answers():
    """Check if answers are correct"""
    data = st.session_state.problem_data
    user_quotient_inputs = st.session_state.user_quotient_inputs
    user_work_inputs = st.session_state.user_work_inputs
    
    # Check quotient
    correct_quotient_digits = [int(d) for d in str(data["quotient"])]
    quotient_correct = len(user_quotient_inputs) == len(correct_quotient_digits) and all(
        user == correct for user, correct in zip(user_quotient_inputs, correct_quotient_digits)
    )
    
    # Check work steps
    division_steps = calculate_long_division_steps(data["dividend"], data["divisor"])
    correct_work = []
    for step in division_steps['work_steps']:
        if step['type'] == 'multiply_subtract':
            correct_work.append(step['product'])
    
    work_correct = len(user_work_inputs) == len(correct_work) and all(
        user == correct for user, correct in zip(user_work_inputs, correct_work)
    )
    
    st.session_state.answer_correct = quotient_correct and work_correct
    st.session_state.quotient_correct = quotient_correct
    st.session_state.work_correct = work_correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def handle_feedback_and_next():
    """Handle feedback and next button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback"""
    data = st.session_state.problem_data
    
    if st.session_state.answer_correct:
        st.success("🎉 **Perfect! Your long division is correct!**")
        
        quotient_display = "".join(map(str, st.session_state.user_quotient_inputs))
        st.markdown(f"**{data['dividend']} ÷ {data['divisor']} = {quotient_display}**")
        
        if data["remainder"] > 0:
            st.markdown(f"**with remainder {data['remainder']}**")
        
        # Increase difficulty
        old_difficulty = st.session_state.long_division_difficulty
        st.session_state.long_division_difficulty = min(
            st.session_state.long_division_difficulty + 1, 4
        )
        
        if st.session_state.long_division_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered long division!**")
        elif old_difficulty < st.session_state.long_division_difficulty:
            difficulty_names = {1: "Simple", 2: "Intermediate", 3: "Advanced", 4: "Expert"}
            st.info(f"⬆️ **Great work! Moving to {difficulty_names[st.session_state.long_division_difficulty]} level**")
    
    else:
        st.error("❌ **Let's check your work step by step.**")
        
        if not st.session_state.quotient_correct:
            correct_quotient = str(data["quotient"])
            user_quotient = "".join(map(str, st.session_state.user_quotient_inputs))
            st.markdown(f"**Quotient:** You entered {user_quotient}, correct is {correct_quotient}")
        
        if not st.session_state.work_correct:
            st.markdown("**Work steps:** Some subtraction steps need correction.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.long_division_difficulty
        st.session_state.long_division_difficulty = max(
            st.session_state.long_division_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.long_division_difficulty:
            difficulty_names = {1: "Simple", 2: "Intermediate", 3: "Advanced", 4: "Expert"}
            st.warning(f"⬇️ **Let's practice {difficulty_names[st.session_state.long_division_difficulty]} problems**")
        
        show_solution()

def show_solution():
    """Show complete solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **Complete Solution**", expanded=True):
        st.markdown(f"### Solution for {data['dividend']} ÷ {data['divisor']}:")
        st.markdown(f"**Quotient:** {data['quotient']}")
        if data['remainder'] > 0:
            st.markdown(f"**Remainder:** {data['remainder']}")
        
        verification = data['quotient'] * data['divisor'] + data['remainder']
        st.markdown(f"**Check:** {data['quotient']} × {data['divisor']} + {data['remainder']} = {verification} ✓")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    
    # Clear user inputs
    keys_to_delete = []
    for key in st.session_state.keys():
        if key.startswith(("user_quotient_inputs", "user_work_inputs", "answer_correct", "quotient_correct", "work_correct")):
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del st.session_state[key]