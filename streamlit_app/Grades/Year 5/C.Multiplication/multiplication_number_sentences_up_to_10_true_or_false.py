import streamlit as st
import random

def run():
    """
    Main function to run the Multiplication Number Sentences: True or False practice activity.
    This gets called when the subtopic is loaded from the main navigation.
    """
    # Initialize session state for difficulty and game state
    if "multiplication_true_false_difficulty" not in st.session_state:
        st.session_state.multiplication_true_false_difficulty = 5  # Start with factors up to 5
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("✅❌ Multiplication Number Sentences up to 10: True or False?")
    st.markdown("*Determine if multiplication equations are true or false*")
    st.markdown("---")
    
    # Difficulty indicator
    max_factor = st.session_state.multiplication_true_false_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** Factors up to {max_factor}")
        # Progress bar (5 to 10)
        progress = (max_factor - 5) / 5  # Convert 5-10 to 0-1
        st.progress(progress, text=f"Up to {max_factor}")
    
    with col2:
        if max_factor <= 6:
            st.markdown("**🟡 Beginner**")
        elif max_factor <= 8:
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
        ### How to Play:
        - **Look at the number sentence** (equation)
        - **Calculate both sides** of the equation
        - **Compare the results** - are they equal?
        - **Click "true"** if both sides are equal
        - **Click "false"** if the sides are different
        
        ### Types of Equations You'll See:
        
        #### Type 1: Multiplication vs. Multiplication
        - **Example: 2 × 6 = 3 × 4**
        - **Left side:** 2 × 6 = 12
        - **Right side:** 3 × 4 = 12
        - **Answer:** TRUE (both equal 12)
        
        #### Type 2: Multiplication vs. Number
        - **Example: 4 × 7 = 28**
        - **Left side:** 4 × 7 = 28
        - **Right side:** 28
        - **Answer:** TRUE (28 = 28)
        
        #### Type 3: False Equations
        - **Example: 5 × 3 = 4 × 4**
        - **Left side:** 5 × 3 = 15
        - **Right side:** 4 × 4 = 16
        - **Answer:** FALSE (15 ≠ 16)
        
        ### Strategy Tips:
        - **Calculate step by step:** Don't rush!
        - **Double-check your math:** Multiply carefully
        - **Look for patterns:** Sometimes you can spot answers quickly
        - **Use known facts:** 2×5=10, 3×3=9, etc.
        
        ### Quick Mental Math Tips:
        - **×2:** Double the number (6×2 = 12)
        - **×5:** Half the number, then multiply by 10 (6×5 = 30)
        - **×9:** Multiply by 10, then subtract the number (7×9 = 70-7 = 63)
        - **×10:** Add a zero (8×10 = 80)
        
        ### Common Patterns:
        - **Commutative property:** 3×4 = 4×3 (same answer)
        - **Equal products:** Different factors can give same results (2×6 = 3×4 = 12)
        - **Perfect squares:** 6×6 = 36, 7×7 = 49
        
        ### Difficulty Levels:
        - **🟡 Level 5-6:** Easier factors (1-6)
        - **🟠 Level 7-8:** Medium factors (1-8)
        - **🔴 Level 9-10:** All factors (1-10)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder factors
        - ❌ **Wrong answer:** Practice easier factors
        - 🎯 **Goal:** Master true/false recognition with all factors!
        """)

def generate_new_question():
    """Generate a new true/false multiplication equation"""
    max_factor = st.session_state.multiplication_true_false_difficulty
    
    # 60% chance of true equations, 40% chance of false
    make_true = random.random() < 0.6
    
    # Choose equation type randomly
    equation_types = ["mult_vs_mult", "mult_vs_number", "complex_mult"]
    equation_type = random.choice(equation_types)
    
    if equation_type == "mult_vs_mult":
        # Format: a × b = c × d
        if make_true:
            # Create true equation with same product
            base_product = random.randint(6, max_factor * max_factor)
            # Find factor pairs for the same product
            factors1 = get_factor_pairs(base_product, max_factor)
            factors2 = get_factor_pairs(base_product, max_factor)
            
            if factors1 and factors2:
                a, b = random.choice(factors1)
                c, d = random.choice(factors2)
                # Make sure it's not the exact same multiplication
                if (a, b) == (c, d) or (a, b) == (d, c):
                    if len(factors1) > 1:
                        pairs = [p for p in factors1 if p != (a, b) and p != (b, a)]
                        if pairs:
                            c, d = random.choice(pairs)
                
                equation = f"{a} × {b} = {c} × {d}"
                is_true = True
            else:
                # Fallback to simpler equation
                a, b = random.randint(2, max_factor), random.randint(2, max_factor)
                equation = f"{a} × {b} = {a * b}"
                is_true = True
        else:
            # Create false equation
            a, b = random.randint(2, max_factor), random.randint(2, max_factor)
            c, d = random.randint(2, max_factor), random.randint(2, max_factor)
            # Ensure they're actually different
            while a * b == c * d:
                c, d = random.randint(2, max_factor), random.randint(2, max_factor)
            
            equation = f"{a} × {b} = {c} × {d}"
            is_true = False
    
    elif equation_type == "mult_vs_number":
        # Format: a × b = number
        a, b = random.randint(1, max_factor), random.randint(1, max_factor)
        correct_product = a * b
        
        if make_true:
            equation = f"{a} × {b} = {correct_product}"
            is_true = True
        else:
            # Create a false number (off by 1-5)
            offset = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            false_number = correct_product + offset
            if false_number <= 0:
                false_number = correct_product + abs(offset)
            
            equation = f"{a} × {b} = {false_number}"
            is_true = False
    
    else:  # complex_mult
        # Format: a × b × c = d × e or similar
        if make_true:
            a, b = random.randint(2, min(4, max_factor)), random.randint(2, min(4, max_factor))
            c = random.randint(2, max_factor)
            product = a * b * c
            
            # Find factors of the product
            d, e = random.randint(2, max_factor), random.randint(2, max_factor)
            if d * e == product:
                equation = f"{a} × {b} × {c} = {d} × {e}"
                is_true = True
            else:
                # Simpler true equation
                equation = f"{a} × {b} = {a * b}"
                is_true = True
        else:
            a, b = random.randint(2, min(4, max_factor)), random.randint(2, min(4, max_factor))
            c, d = random.randint(2, max_factor), random.randint(2, max_factor)
            while a * b == c * d:
                c, d = random.randint(2, max_factor), random.randint(2, max_factor)
            
            equation = f"{a} × {b} = {c} × {d}"
            is_true = False
    
    st.session_state.question_data = {
        "equation": equation,
        "equation_type": equation_type
    }
    st.session_state.correct_answer = is_true
    st.session_state.current_question = "Is the number sentence true or false?"

def get_factor_pairs(number, max_factor):
    """Get all factor pairs of a number within the max_factor limit"""
    pairs = []
    for i in range(1, min(max_factor + 1, int(number**0.5) + 1)):
        if number % i == 0:
            j = number // i
            if j <= max_factor:
                pairs.append((i, j))
    return pairs

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### ❓ Is the number sentence true or false?")
    
    # Display the equation in a large, centered format
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa; 
            padding: 40px; 
            border-radius: 15px; 
            border: 2px solid #6c757d;
            text-align: center;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
        ">
            <div style="font-size: 32px; font-weight: bold; color: #495057;">
                {data['equation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # True/False buttons
    if not st.session_state.show_feedback:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 0.5, 1, 1])
        
        with col2:
            if st.button("true", key="true_btn", use_container_width=True, type="primary" if st.session_state.selected_answer == True else "secondary"):
                st.session_state.selected_answer = True
        
        with col4:
            if st.button("false", key="false_btn", use_container_width=True, type="primary" if st.session_state.selected_answer == False else "secondary"):
                st.session_state.selected_answer = False
        
        # Submit button
        if st.session_state.selected_answer is not None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Submit", type="primary", use_container_width=True):
                    st.session_state.user_answer = st.session_state.selected_answer
                    st.session_state.show_feedback = True
                    st.session_state.answer_submitted = True
        
        # Show hint about selected answer
        if st.session_state.selected_answer is not None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                answer_text = "TRUE" if st.session_state.selected_answer else "FALSE"
                st.markdown(f"""
                <div style="
                    background-color: #e8f4fd; 
                    padding: 10px; 
                    border-radius: 8px; 
                    text-align: center;
                    margin: 10px 0;
                    font-size: 14px;
                    color: #1f77b4;
                ">
                    Selected: <strong>{answer_text}</strong>
                </div>
                """, unsafe_allow_html=True)
    
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct!**")
        
        # Show why it's correct
        answer_text = "TRUE" if correct_answer else "FALSE"
        st.info(f"✨ **The equation is {answer_text}**")
        
        # Increase difficulty (max factor 10)
        old_max = st.session_state.multiplication_true_false_difficulty
        st.session_state.multiplication_true_false_difficulty = min(
            st.session_state.multiplication_true_false_difficulty + 1, 10
        )
        
        # Show encouragement based on difficulty
        if st.session_state.multiplication_true_false_difficulty == 10 and old_max < 10:
            st.balloons()
            st.info("🏆 **Excellent! You've mastered true/false equations with all factors up to 10!**")
        elif old_max < st.session_state.multiplication_true_false_difficulty:
            new_max = st.session_state.multiplication_true_false_difficulty
            st.info(f"⬆️ **Level up! Now working with factors up to {new_max}**")
    
    else:
        correct_text = "TRUE" if correct_answer else "FALSE"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_text}**.")
        
        # Decrease difficulty (min factor 5)
        old_max = st.session_state.multiplication_true_false_difficulty
        st.session_state.multiplication_true_false_difficulty = max(
            st.session_state.multiplication_true_false_difficulty - 1, 5
        )
        
        if old_max > st.session_state.multiplication_true_false_difficulty:
            new_max = st.session_state.multiplication_true_false_difficulty
            st.warning(f"⬇️ **Let's practice with easier factors. Now working up to {new_max}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show detailed explanation of why the equation is true or false"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    equation = data['equation']
    
    with st.expander("📖 **Click here to see the detailed explanation**", expanded=True):
        st.markdown(f"### Equation: {equation}")
        
        # Parse and evaluate the equation
        parts = equation.split(' = ')
        left_side = parts[0].strip()
        right_side = parts[1].strip()
        
        # Calculate left side
        left_value = calculate_expression(left_side)
        right_value = calculate_expression(right_side)
        
        st.markdown(f"""
        ### Step-by-step calculation:
        
        **Left side:** {left_side}
        """)
        
        if '×' in left_side:
            # Show multiplication steps
            factors = [int(x.strip()) for x in left_side.split('×')]
            if len(factors) == 2:
                st.markdown(f"- {factors[0]} × {factors[1]} = **{left_value}**")
            else:
                # Multiple factors
                result = factors[0]
                calculation = str(factors[0])
                for i in range(1, len(factors)):
                    result *= factors[i]
                    calculation += f" × {factors[i]}"
                st.markdown(f"- {calculation} = **{left_value}**")
        else:
            st.markdown(f"- **{left_value}**")
        
        st.markdown(f"""
        **Right side:** {right_side}
        """)
        
        if '×' in right_side:
            # Show multiplication steps
            factors = [int(x.strip()) for x in right_side.split('×')]
            if len(factors) == 2:
                st.markdown(f"- {factors[0]} × {factors[1]} = **{right_value}**")
            else:
                # Multiple factors
                result = factors[0]
                calculation = str(factors[0])
                for i in range(1, len(factors)):
                    result *= factors[i]
                    calculation += f" × {factors[i]}"
                st.markdown(f"- {calculation} = **{right_value}**")
        else:
            st.markdown(f"- **{right_value}**")
        
        # Show comparison
        if left_value == right_value:
            st.markdown(f"""
            ### Comparison:
            **{left_value} = {right_value}** ✅
            
            **Answer: TRUE** - Both sides are equal!
            """)
        else:
            st.markdown(f"""
            ### Comparison:
            **{left_value} ≠ {right_value}** ❌
            
            **Answer: FALSE** - The sides are not equal.
            """)

def calculate_expression(expression):
    """Calculate the value of a multiplication expression"""
    if '×' not in expression:
        return int(expression.strip())
    
    factors = [int(x.strip()) for x in expression.split('×')]
    result = 1
    for factor in factors:
        result *= factor
    return result

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer