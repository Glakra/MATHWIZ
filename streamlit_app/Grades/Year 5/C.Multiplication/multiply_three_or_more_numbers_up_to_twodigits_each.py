import streamlit as st
import random

def run():
    """
    Main function to run the Multiply three or more numbers up to two digits each activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C.Multiplication/multiply_three_or_more_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "mult_three_difficulty" not in st.session_state:
        st.session_state.mult_three_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔢 Multiply Three or More Numbers")
    st.markdown("*Master multiplication with multiple factors up to two digits each*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mult_three_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Multiply Multiple Numbers:
        - **Work from left to right** - multiply the first two numbers, then multiply that result by the next number
        - **Use the associative property** - you can group numbers in different ways
        - **Look for patterns** - numbers like 2, 5, 10 can make calculations easier
        - **Break down larger numbers** if needed
        
        ### Strategies:
        1. **Left to Right Method:**
           - 4 × 3 × 5 = (4 × 3) × 5 = 12 × 5 = 60
        
        2. **Look for Easy Pairs:**
           - 8 × 5 × 2 = 8 × (5 × 2) = 8 × 10 = 80
           - 4 × 7 × 25 = (4 × 25) × 7 = 100 × 7 = 700
        
        3. **Use Properties:**
           - 6 × 2 × 9 × 5 = (6 × 9) × (2 × 5) = 54 × 10 = 540
        
        ### Helpful Patterns:
        - **2 × 5 = 10** (easy to work with)
        - **4 × 25 = 100** (makes calculations simple)
        - **8 × 125 = 1000** (for advanced problems)
        - **Any number × 1 = same number**
        - **Any number × 10 = add a zero**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** 3 numbers, mostly single digits
        - **🟠 Level 3:** 3-4 numbers, mix of single and double digits
        - **🔴 Level 4-5:** 4-5 numbers, up to two digits each
        
        ### Examples:
        - **Easy:** 2 × 3 × 4 = 24
        - **Medium:** 5 × 6 × 2 × 3 = 180
        - **Hard:** 12 × 4 × 5 × 3 = 720
        """)

def generate_new_question():
    """Generate a new multiplication question with 3+ numbers"""
    level = st.session_state.mult_three_difficulty
    
    # Determine number of factors and their ranges based on difficulty
    if level == 1:
        num_factors = 3
        ranges = [(1, 5), (1, 6), (1, 4)]  # Very small numbers
    elif level == 2:
        num_factors = 3
        ranges = [(2, 8), (2, 7), (1, 5)]  # Small numbers
    elif level == 3:
        num_factors = random.choice([3, 4])
        if num_factors == 3:
            ranges = [(3, 12), (2, 10), (1, 8)]
        else:
            ranges = [(2, 8), (2, 6), (1, 5), (2, 4)]
    elif level == 4:
        num_factors = random.choice([3, 4, 4])  # Favor 4 factors
        if num_factors == 3:
            ranges = [(5, 15), (3, 12), (2, 10)]
        else:
            ranges = [(3, 10), (2, 8), (2, 7), (1, 6)]
    else:  # level 5
        num_factors = random.choice([4, 4, 5])  # Favor 4-5 factors
        if num_factors == 4:
            ranges = [(4, 20), (3, 15), (2, 12), (2, 8)]
        else:
            ranges = [(2, 12), (2, 10), (2, 8), (1, 6), (2, 5)]
    
    # Generate factors
    factors = []
    for i in range(num_factors):
        min_val, max_val = ranges[i] if i < len(ranges) else (1, 10)
        factor = random.randint(min_val, max_val)
        factors.append(factor)
    
    # Sometimes include strategic numbers for easier calculation
    if level >= 3 and random.random() < 0.3:
        # Replace one factor with a "nice" number
        nice_numbers = [2, 5, 10, 4, 25] if level >= 4 else [2, 5, 10]
        replace_index = random.randint(0, len(factors) - 1)
        factors[replace_index] = random.choice(nice_numbers)
    
    # Calculate the correct answer
    correct_answer = 1
    for factor in factors:
        correct_answer *= factor
    
    # Generate the question expression
    expression = " × ".join(map(str, factors))
    
    st.session_state.question_data = {
        "factors": factors,
        "expression": expression,
        "num_factors": num_factors
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Calculate: {expression}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🔢 Multiply:")
    
    # Display the multiplication expression in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 35px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        font-size: 36px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    ">
        {data['expression']} = ?
    </div>
    """, unsafe_allow_html=True)
    
    # Input field for answer
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_input = st.number_input(
                "Enter your answer:",
                min_value=0,
                max_value=999999,
                step=1,
                key="answer_input",
                label_visibility="collapsed",
                placeholder="Type your answer here..."
            )
            
            # Submit button
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            if user_input is not None and user_input > 0:
                st.session_state.user_answer = int(user_input)
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            else:
                st.warning("Please enter a valid answer.")
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the calculation
        st.markdown(f"**{data['expression']} = {correct_answer:,}**")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.mult_three_difficulty
        st.session_state.mult_three_difficulty = min(
            st.session_state.mult_three_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.mult_three_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 multi-factor multiplication!**")
        elif old_level < st.session_state.mult_three_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.mult_three_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer:,}**.")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.mult_three_difficulty
        st.session_state.mult_three_difficulty = max(
            st.session_state.mult_three_difficulty - 1, 1
        )
        
        if old_level > st.session_state.mult_three_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.mult_three_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    factors = data['factors']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['expression']} = ?
        
        #### Method 1: Left to Right
        """)
        
        # Show step-by-step left to right calculation
        result = factors[0]
        steps = [f"Start with: **{factors[0]}**"]
        
        for i in range(1, len(factors)):
            old_result = result
            result *= factors[i]
            steps.append(f"{old_result} × {factors[i]} = **{result}**")
        
        for step in steps:
            st.markdown(f"- {step}")
        
        st.markdown(f"**Final Answer: {correct_answer:,}**")
        
        # Show alternative grouping if beneficial
        if len(factors) >= 4 or any(f in [2, 4, 5, 8, 10, 25] for f in factors):
            st.markdown("#### Method 2: Smart Grouping")
            show_smart_grouping(factors, correct_answer)
        
        # Show patterns if present
        show_patterns(factors)

def show_smart_grouping(factors, correct_answer):
    """Show smart grouping strategies"""
    # Look for beneficial pairs
    pairs_found = []
    
    # Check for 2×5=10, 4×25=100, etc.
    special_pairs = {
        (2, 5): 10,
        (5, 2): 10,
        (4, 25): 100,
        (25, 4): 100,
        (8, 125): 1000,
        (125, 8): 1000
    }
    
    factors_copy = factors.copy()
    for (a, b), product in special_pairs.items():
        if a in factors_copy and b in factors_copy:
            pairs_found.append(f"**{a} × {b} = {product}** (easy to work with)")
            factors_copy.remove(a)
            factors_copy.remove(b)
            factors_copy.append(product)
            break
    
    if pairs_found:
        st.markdown("Look for helpful pairs:")
        for pair in pairs_found:
            st.markdown(f"- {pair}")
        
        # Show the simplified calculation
        remaining = " × ".join(map(str, sorted(factors_copy, reverse=True)))
        st.markdown(f"- Now calculate: {remaining} = **{correct_answer:,}**")
    
    # Check for multiples of 10
    tens_count = str(correct_answer).count('0')
    if tens_count > 0 and any(f % 10 == 0 or f in [2, 5] for f in factors):
        st.markdown(f"- Notice the answer ends in {tens_count} zero(s) - this often happens with factors of 2, 5, and 10!")

def show_patterns(factors):
    """Show mathematical patterns in the factors"""
    patterns = []
    
    # Check for 1's
    if 1 in factors:
        patterns.append("**Multiplying by 1** doesn't change the value")
    
    # Check for 10's or multiples of 10
    tens = [f for f in factors if f % 10 == 0]
    if tens:
        patterns.append(f"**Multiplying by {tens[0]}** adds zero(s) to the result")
    
    # Check for even numbers
    even_count = sum(1 for f in factors if f % 2 == 0)
    if even_count >= 2:
        patterns.append("**Multiple even numbers** guarantee an even result")
    
    # Check for 5's
    if 5 in factors and any(f % 2 == 0 for f in factors):
        patterns.append("**5 times an even number** always ends in 0")
    
    if patterns:
        st.markdown("#### Helpful Patterns:")
        for pattern in patterns:
            st.markdown(f"- {pattern}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer