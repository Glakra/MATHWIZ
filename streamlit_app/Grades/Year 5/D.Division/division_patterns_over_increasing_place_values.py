import streamlit as st
import random

def run():
    """
    Main function to run the Division Patterns Over Increasing Place Values practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/division_patterns_over_increasing_place_values.py
    """
    # Initialize session state for difficulty and game state
    if "pattern_difficulty" not in st.session_state:
        st.session_state.pattern_difficulty = 1  # Start with simple patterns
    
    if "current_pattern_problem" not in st.session_state:
        st.session_state.current_pattern_problem = None
        st.session_state.correct_pattern_answers = []
        st.session_state.show_pattern_feedback = False
        st.session_state.pattern_answer_submitted = False
        st.session_state.pattern_problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("📈 Division Patterns Over Increasing Place Values")
    st.markdown("*Discover patterns when place values change in division*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.pattern_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic patterns (simple numbers)",
            2: "Intermediate patterns (larger numbers)", 
            3: "Advanced patterns (complex relationships)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_pattern_problem is None:
        generate_new_pattern_problem()
    
    # Display current question
    display_pattern_problem()
    
    # Instructions section
    show_pattern_instructions()

def show_pattern_instructions():
    """Display the instructions in an expandable section"""
    with st.expander("💡 **Understanding Division Patterns**", expanded=False):
        st.markdown("""
        ### What are Division Patterns?
        Division patterns show how answers change in predictable ways when we multiply or divide numbers by powers of 10.
        
        ### Key Pattern Rules:
        
        **Rule 1: When the dividend increases by powers of 10, the quotient increases by the same amount**
        - 24 ÷ 3 = 8
        - 240 ÷ 3 = 80 (dividend × 10, quotient × 10)
        - 2,400 ÷ 3 = 800 (dividend × 100, quotient × 100)
        
        **Rule 2: When both dividend and divisor increase by the same power of 10, the quotient stays the same**
        - 35 ÷ 5 = 7
        - 350 ÷ 50 = 7 (both × 10)
        - 3,500 ÷ 500 = 7 (both × 100)
        
        **Rule 3: When the divisor increases by powers of 10, the quotient decreases by the same amount**
        - 420 ÷ 6 = 70
        - 420 ÷ 60 = 7 (divisor × 10, quotient ÷ 10)
        - 420 ÷ 600 = 0.7 (divisor × 100, quotient ÷ 100)
        
        ### Pattern Types You Will See:
        
        **Type 1: Missing Dividend**
        - __ ÷ 4 = 6
        - __ ÷ 4 = 60,000
        - __ ÷ 4 = 600,000
        
        **Type 2: Missing Quotient**
        - 35 ÷ 7 = __
        - 350,000 ÷ 7 = __
        - 35,000,000 ÷ 7 = __
        
        **Type 3: Missing Divisor**
        - 48 ÷ __ = 8
        - 480 ÷ __ = 80
        - 4,800 ÷ __ = 800
        
        ### How to Solve Pattern Problems:
        
        **Step 1: Look at the first equation**
        - Find the basic fact (like 24 ÷ 3 = 8)
        
        **Step 2: Identify the pattern**
        - Are numbers getting 10 times bigger? 100 times bigger?
        - Which numbers are changing?
        
        **Step 3: Apply the pattern rule**
        - If dividend × 10, then quotient × 10
        - If both dividend and divisor × 10, quotient stays same
        - If divisor × 10, then quotient ÷ 10
        
        **Step 4: Check your answer**
        - Does the pattern make sense?
        - Try multiplying: quotient × divisor = dividend
        
        ### Quick Pattern Tricks:
        
        **Adding Zeros:**
        - When dividend gets more zeros, quotient gets same number of zeros
        - 72 ÷ 8 = 9, so 7,200 ÷ 8 = 900
        
        **Moving Zeros:**
        - When divisor gets zeros, quotient loses zeros
        - 560 ÷ 7 = 80, so 560 ÷ 70 = 8
        
        **Keeping the Same:**
        - When both get same zeros, quotient stays same
        - 45 ÷ 9 = 5, so 4,500 ÷ 900 = 5
        
        ### Remember:
        - Look for the basic division fact first
        - Count how many zeros are added or moved
        - Apply the same change to find the missing number
        - Check by multiplying to verify your answer
        """)

def generate_new_pattern_problem():
    """Generate a new division pattern problem based on difficulty"""
    difficulty = st.session_state.pattern_difficulty
    
    # Basic division facts to build patterns from
    basic_facts = [
        (24, 3, 8), (35, 5, 7), (48, 6, 8), (56, 7, 8), (63, 9, 7),
        (72, 8, 9), (81, 9, 9), (64, 8, 8), (42, 6, 7), (54, 6, 9),
        (28, 4, 7), (36, 4, 9), (45, 5, 9), (32, 4, 8), (49, 7, 7)
    ]
    
    # Choose a random basic fact
    dividend_base, divisor_base, quotient_base = random.choice(basic_facts)
    
    # Define pattern types
    pattern_types = ["missing_dividend", "missing_quotient", "missing_divisor"]
    pattern_type = random.choice(pattern_types)
    
    # Define place value multipliers based on difficulty
    if difficulty == 1:
        multipliers = [1, 10, 100]
        place_names = ["ones", "tens", "hundreds"]
    elif difficulty == 2:
        multipliers = [1, 100, 10000]
        place_names = ["ones", "hundreds", "ten thousands"]
    else:
        multipliers = [1, 1000, 1000000]
        place_names = ["ones", "thousands", "millions"]
    
    # Generate the pattern based on type
    equations = []
    correct_answers = []
    missing_positions = []
    
    for i, mult in enumerate(multipliers):
        if pattern_type == "missing_dividend":
            # Pattern: __ ÷ divisor = quotient (quotient increases)
            dividend = dividend_base * mult
            divisor = divisor_base
            quotient = quotient_base * mult
            equations.append(f"÷ {divisor:,} = {quotient:,}")
            correct_answers.append(dividend)
            missing_positions.append("dividend")
            
        elif pattern_type == "missing_quotient":
            # Pattern: dividend ÷ divisor = __ (dividend increases)
            dividend = dividend_base * mult
            divisor = divisor_base
            quotient = quotient_base * mult
            equations.append(f"{dividend:,} ÷ {divisor:,} = ")
            correct_answers.append(quotient)
            missing_positions.append("quotient")
            
        else:  # missing_divisor
            # Pattern: dividend ÷ __ = quotient (both dividend and quotient increase)
            dividend = dividend_base * mult
            divisor = divisor_base
            quotient = quotient_base * mult
            equations.append(f"{dividend:,} ÷ = {quotient:,}")
            correct_answers.append(divisor)
            missing_positions.append("divisor")
    
    st.session_state.pattern_problem_data = {
        "equations": equations,
        "pattern_type": pattern_type,
        "multipliers": multipliers,
        "place_names": place_names,
        "basic_fact": (dividend_base, divisor_base, quotient_base),
        "missing_positions": missing_positions
    }
    st.session_state.correct_pattern_answers = correct_answers
    st.session_state.current_pattern_problem = "Complete the pattern:"

def display_pattern_problem():
    """Display the current pattern problem interface"""
    data = st.session_state.pattern_problem_data
    
    # Display question header
    st.markdown("### 📈 Complete the Pattern:")
    
    # Display the pattern explanation
    pattern_explanations = {
        "missing_dividend": "Find the missing dividends in this pattern:",
        "missing_quotient": "Find the missing quotients in this pattern:",
        "missing_divisor": "Find the missing divisors in this pattern:"
    }
    
    st.markdown(f"*{pattern_explanations[data['pattern_type']]}*")
    
    # Display the equations with input fields
    with st.form("pattern_form", clear_on_submit=False):
        user_answers = []
        
        for i, equation in enumerate(data['equations']):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if data['pattern_type'] == "missing_dividend":
                    # Show input box ÷ divisor = quotient
                    parts = equation.split(' = ')
                    divisor_part = parts[0].replace('÷ ', '')
                    quotient_part = parts[1]
                    
                    input_col, eq_col = st.columns([1, 2])
                    with input_col:
                        answer = st.number_input(
                            f"Equation {i+1}:",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed"
                        )
                        user_answers.append(int(answer) if answer else 0)
                    
                    with eq_col:
                        st.markdown(f"÷ {divisor_part} = {quotient_part}")
                
                elif data['pattern_type'] == "missing_quotient":
                    # Show dividend ÷ divisor = input box
                    parts = equation.split(' = ')
                    dividend_divisor_part = parts[0]
                    
                    eq_col, input_col = st.columns([2, 1])
                    with eq_col:
                        st.markdown(f"{dividend_divisor_part} = ")
                    
                    with input_col:
                        answer = st.number_input(
                            f"Equation {i+1}:",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed"
                        )
                        user_answers.append(int(answer) if answer else 0)
                
                else:  # missing_divisor
                    # Show dividend ÷ input box = quotient
                    parts = equation.split(' = ')
                    dividend_part = parts[0].split(' ÷')[0]
                    quotient_part = parts[1]
                    
                    left_col, input_col, right_col = st.columns([1, 1, 1])
                    with left_col:
                        st.markdown(f"{dividend_part} ÷")
                    
                    with input_col:
                        answer = st.number_input(
                            f"Equation {i+1}:",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed"
                        )
                        user_answers.append(int(answer) if answer else 0)
                    
                    with right_col:
                        st.markdown(f"= {quotient_part}")
        
        # Submit button
        if st.form_submit_button("✅ Submit Pattern", type="primary", use_container_width=True):
            st.session_state.user_pattern_answers = user_answers
            st.session_state.show_pattern_feedback = True
            st.session_state.pattern_answer_submitted = True
    
    # Show feedback and next button
    handle_pattern_feedback_and_next()

def handle_pattern_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_pattern_feedback:
        show_pattern_feedback()
    
    # Next question button
    if st.session_state.pattern_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Pattern", type="secondary", use_container_width=True):
                reset_pattern_question_state()
                st.rerun()

def show_pattern_feedback():
    """Display feedback for the submitted pattern answers"""
    user_answers = st.session_state.user_pattern_answers
    correct_answers = st.session_state.correct_pattern_answers
    data = st.session_state.pattern_problem_data
    
    # Check how many are correct
    correct_count = sum(1 for u, c in zip(user_answers, correct_answers) if u == c)
    total_count = len(correct_answers)
    
    if correct_count == total_count:
        st.success("🎉 **Perfect! You found the complete pattern!**")
        
        # Show the correct answers
        answer_display = ", ".join([f"{ans:,}" for ans in correct_answers])
        st.info(f"✅ **Correct answers:** {answer_display}")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.pattern_difficulty
        st.session_state.pattern_difficulty = min(st.session_state.pattern_difficulty + 1, 3)
        
        if st.session_state.pattern_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You have mastered division patterns!**")
        elif old_difficulty < st.session_state.pattern_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working on Level {st.session_state.pattern_difficulty} patterns**")
    
    elif correct_count > 0:
        st.warning(f"📊 **Partially correct!** You got {correct_count} out of {total_count} answers right.")
        
        # Show which ones were right/wrong
        for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers)):
            if user_ans == correct_ans:
                st.success(f"✅ **Equation {i+1}:** {correct_ans:,} is correct!")
            else:
                st.error(f"❌ **Equation {i+1}:** You said {user_ans:,}, but it should be {correct_ans:,}")
        
        # Show explanation
        show_pattern_explanation()
    
    else:
        st.error("❌ **Not quite right.** Let's look at the pattern together.")
        
        # Show all correct answers
        for i, correct_ans in enumerate(correct_answers):
            st.info(f"**Equation {i+1}:** {correct_ans:,}")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.pattern_difficulty
        st.session_state.pattern_difficulty = max(st.session_state.pattern_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.pattern_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.pattern_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_pattern_explanation()

def show_pattern_explanation():
    """Show step-by-step explanation of the pattern"""
    data = st.session_state.pattern_problem_data
    correct_answers = st.session_state.correct_pattern_answers
    basic_dividend, basic_divisor, basic_quotient = data['basic_fact']
    
    with st.expander("📖 **Click here for pattern explanation**", expanded=True):
        st.markdown(f"""
        ### Pattern Analysis:
        
        **Basic division fact:** {basic_dividend} ÷ {basic_divisor} = {basic_quotient}
        
        **Pattern type:** {data['pattern_type'].replace('_', ' ').title()}
        
        ### Step-by-step pattern:
        """)
        
        for i, (mult, place_name, answer) in enumerate(zip(data['multipliers'], data['place_names'], correct_answers)):
            if data['pattern_type'] == "missing_dividend":
                dividend = answer
                quotient = basic_quotient * mult
                st.markdown(f"""
                **Step {i+1} ({place_name}):**
                - Quotient: {basic_quotient} × {mult:,} = {quotient:,}
                - Since quotient × {mult:,}, dividend must also × {mult:,}
                - **Answer: {dividend:,}** ÷ {basic_divisor} = {quotient:,}
                """)
                
            elif data['pattern_type'] == "missing_quotient":
                dividend = basic_dividend * mult
                quotient = answer
                st.markdown(f"""
                **Step {i+1} ({place_name}):**
                - Dividend: {basic_dividend} × {mult:,} = {dividend:,}
                - Since dividend × {mult:,}, quotient also × {mult:,}
                - **Answer:** {dividend:,} ÷ {basic_divisor} = {quotient:,}
                """)
                
            else:  # missing_divisor
                dividend = basic_dividend * mult
                quotient = basic_quotient * mult
                divisor = answer
                st.markdown(f"""
                **Step {i+1} ({place_name}):**
                - Dividend: {basic_dividend} × {mult:,} = {dividend:,}
                - Quotient: {basic_quotient} × {mult:,} = {quotient:,}
                - **Answer:** {dividend:,} ÷ {divisor} = {quotient:,}
                """)
        
        st.markdown(f"""
        ### Pattern Rule:
        When place values increase by powers of 10, division results follow predictable patterns.
        
        ### Key Insight:
        - **Multiplying by 10** adds one zero
        - **Multiplying by 100** adds two zeros
        - **Multiplying by 1,000** adds three zeros
        
        ### Verification:
        Check each answer by multiplying: quotient × divisor = dividend
        """)

def reset_pattern_question_state():
    """Reset the question state for next question"""
    st.session_state.current_pattern_problem = None
    st.session_state.correct_pattern_answers = []
    st.session_state.show_pattern_feedback = False
    st.session_state.pattern_answer_submitted = False
    st.session_state.pattern_problem_data = {}
    if "user_pattern_answers" in st.session_state:
        del st.session_state.user_pattern_answers