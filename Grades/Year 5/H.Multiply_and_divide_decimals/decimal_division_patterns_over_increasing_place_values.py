import streamlit as st
import random

def run():
    """
    Main function to run the Decimal division patterns over increasing place values activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/decimal_division_patterns_over_increasing_place_values.py
    """
    # Initialize session state
    if "pattern_problem" not in st.session_state:
        st.session_state.pattern_problem = None
        st.session_state.pattern_submitted = False
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("🔢 Decimal Division Patterns Over Increasing Place Values")
    st.markdown("*Complete patterns with powers of 10*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.pattern_problem is None:
        st.session_state.pattern_problem = generate_pattern_problem()
        st.session_state.pattern_submitted = False
        st.session_state.user_answers = {}
    
    problem = st.session_state.pattern_problem
    
    # Display the question
    st.markdown("### 📝 Complete the pattern:")
    
    # Create the pattern display
    display_pattern_improved(problem)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.pattern_submitted):
            
            # Check if all fields are filled
            all_filled = True
            for i in range(len(problem['answers'])):
                if problem['blanks'][i]:
                    answer_key = f"answer_{i}"
                    if st.session_state.user_answers.get(answer_key, "").strip() == "":
                        all_filled = False
                        break
                
                # Check for left blanks in mixed patterns
                if problem['type'] in ['mixed_multiply', 'mixed_divide']:
                    if problem.get('blank_positions', [])[i] == 'left':
                        left_key = f"left_answer_{i}"
                        if st.session_state.user_answers.get(left_key, "").strip() == "":
                            all_filled = False
                            break
            
            if not all_filled:
                st.warning("⚠️ Please fill in all the blank fields.")
            else:
                # Validate all inputs are numbers
                try:
                    for i in range(len(problem['answers'])):
                        if problem['blanks'][i]:
                            float(st.session_state.user_answers[f"answer_{i}"])
                        if problem['type'] in ['mixed_multiply', 'mixed_divide']:
                            if problem.get('blank_positions', [])[i] == 'left':
                                float(st.session_state.user_answers[f"left_answer_{i}"])
                    st.session_state.pattern_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter valid numbers in all fields.")
    
    # Show feedback if answer was submitted
    if st.session_state.pattern_submitted:
        show_feedback_improved()
    
    # Next question button
    if st.session_state.pattern_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Pattern", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.pattern_problem = None
                st.session_state.pattern_submitted = False
                st.session_state.user_answers = {}
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Understanding Patterns with Powers of 10:
        
        **Division Patterns (÷):**
        - ÷ 10 → Move decimal 1 place LEFT
        - ÷ 100 → Move decimal 2 places LEFT
        - ÷ 1000 → Move decimal 3 places LEFT
        - ÷ 10000 → Move decimal 4 places LEFT
        
        **Multiplication Patterns (×):**
        - × 10 → Move decimal 1 place RIGHT
        - × 100 → Move decimal 2 places RIGHT
        - × 1000 → Move decimal 3 places RIGHT
        - × 10000 → Move decimal 4 places RIGHT
        
        ### Example Patterns:
        
        **Division Pattern:**
        ```
        6.991 ÷ 10 = 0.6991
        6.991 ÷ 100 = 0.06991
        6.991 ÷ 1000 = 0.006991
        6.991 ÷ 10000 = 0.0006991
        ```
        
        **Multiplication Pattern:**
        ```
        0.284 × 10 = 2.84
        0.284 × 100 = 28.4
        0.284 × 1000 = 284
        0.284 × 10000 = 2840
        ```
        
        ### Tips:
        - **Look at the first example** to understand the pattern
        - **Count the zeros** in the power of 10
        - **Move the decimal** that many places
        - **Add zeros** if needed
        - **Check:** Each answer should be 10 times larger (×) or smaller (÷) than the previous
        """)

def generate_pattern_problem():
    """Generate a random pattern problem"""
    pattern_types = [
        'multiply_pattern',     # Start with decimal, multiply by powers of 10
        'divide_pattern',       # Start with number, divide by powers of 10
        'mixed_multiply',       # Mixed order multiplication
        'mixed_divide'          # Mixed order division
    ]
    
    pattern_type = random.choice(pattern_types)
    
    if pattern_type == 'multiply_pattern':
        # Start with a decimal, multiply by increasing powers of 10
        start_num = round(random.uniform(0.001, 0.999), random.choice([3, 4]))
        powers = [10, 100, 1000, 10000]
        
        equations = []
        answers = []
        blanks = []
        
        for i, power in enumerate(powers):
            result = start_num * power
            # Format result nicely
            if result >= 1000:
                result = int(result) if result == int(result) else result
            
            equations.append(f"{start_num} × {power}")
            answers.append(result)
            blanks.append(random.choice([True, False]) if i > 0 else False)  # First one is always shown
        
        return {
            'type': 'multiply',
            'equations': equations,
            'answers': answers,
            'blanks': blanks,
            'pattern_description': 'multiplication by powers of 10'
        }
    
    elif pattern_type == 'divide_pattern':
        # Start with a number, divide by increasing powers of 10
        start_num = random.choice([
            round(random.uniform(1, 9.999), 3),
            random.randint(10, 99),
            random.randint(100, 999)
        ])
        powers = [10, 100, 1000, 10000]
        
        equations = []
        answers = []
        blanks = []
        
        for i, power in enumerate(powers):
            result = start_num / power
            # Format result to avoid floating point issues
            result = round(result, 10)
            result_str = f"{result:.10f}".rstrip('0').rstrip('.')
            result = float(result_str)
            
            equations.append(f"{start_num} ÷ {power}")
            answers.append(result)
            blanks.append(random.choice([True, False]) if i > 0 else False)
        
        return {
            'type': 'divide',
            'equations': equations,
            'answers': answers,
            'blanks': blanks,
            'pattern_description': 'division by powers of 10'
        }
    
    elif pattern_type == 'mixed_multiply':
        # Mixed order multiplication (fill in the blanks on left side)
        base_num = round(random.uniform(0.001, 99.999), random.choice([3, 4]))
        powers = [10, 100, 1000, 10000]
        
        equations = []
        answers = []
        blanks = []
        blank_positions = []
        
        for i, power in enumerate(powers):
            result = base_num * power
            if result >= 1000:
                result = int(result) if result == int(result) else result
            
            # Decide if this should have a blank
            if i == 0:
                # First one is always complete
                equations.append(f"{base_num} × {power}")
                blank_positions.append(None)
                blanks.append(False)
            else:
                # Randomly choose what to blank
                choice = random.choice(['left', 'right', 'none'])
                if choice == 'left':
                    equations.append(f"? × {power}")
                    blank_positions.append('left')
                    blanks.append(False)  # Right side is shown
                elif choice == 'right':
                    equations.append(f"{base_num} × {power}")
                    blank_positions.append('right')
                    blanks.append(True)  # Right side is blank
                else:
                    equations.append(f"{base_num} × {power}")
                    blank_positions.append(None)
                    blanks.append(False)
            
            answers.append(result)
        
        return {
            'type': 'mixed_multiply',
            'equations': equations,
            'answers': answers,
            'blanks': blanks,
            'blank_positions': blank_positions,
            'base_num': base_num,
            'pattern_description': 'finding missing numbers in multiplication patterns'
        }
    
    else:  # mixed_divide
        # Generate a base number
        base_num = random.choice([
            round(random.uniform(1, 9.999), 3),
            random.randint(10, 99),
            random.randint(100, 999)
        ])
        powers = [10, 100, 1000, 10000]
        
        equations = []
        answers = []
        blanks = []
        blank_positions = []
        
        for i, power in enumerate(powers):
            result = base_num / power
            result = round(result, 10)
            result_str = f"{result:.10f}".rstrip('0').rstrip('.')
            result = float(result_str)
            
            if i == 0:
                equations.append(f"{base_num} ÷ {power}")
                blank_positions.append(None)
                blanks.append(False)
            else:
                choice = random.choice(['left', 'right', 'none'])
                if choice == 'left':
                    equations.append(f"? ÷ {power}")
                    blank_positions.append('left')
                    blanks.append(False)
                elif choice == 'right':
                    equations.append(f"{base_num} ÷ {power}")
                    blank_positions.append('right')
                    blanks.append(True)
                else:
                    equations.append(f"{base_num} ÷ {power}")
                    blank_positions.append(None)
                    blanks.append(False)
            
            answers.append(result)
        
        return {
            'type': 'mixed_divide',
            'equations': equations,
            'answers': answers,
            'blanks': blanks,
            'blank_positions': blank_positions,
            'base_num': base_num,
            'pattern_description': 'finding missing numbers in division patterns'
        }

def display_pattern_improved(problem):
    """Display the pattern with proper formatting"""
    # Create a container for better layout
    pattern_container = st.container()
    
    with pattern_container:
        for i, equation in enumerate(problem['equations']):
            # Create columns for each row
            if problem['type'] in ['mixed_multiply', 'mixed_divide'] and problem.get('blank_positions', [])[i] == 'left':
                # Handle left blank case
                col1, col2, col3, col4, col5 = st.columns([1.5, 0.5, 1, 0.5, 1.5])
                
                with col1:
                    user_input = st.text_input(
                        f"Left {i+1}",
                        key=f"left_answer_{i}",
                        disabled=st.session_state.pattern_submitted,
                        placeholder="Enter number",
                        label_visibility="collapsed"
                    )
                    st.session_state.user_answers[f"left_answer_{i}"] = user_input
                
                with col2:
                    operator = "×" if "×" in equation else "÷"
                    st.markdown(f"<div style='text-align: center; font-size: 20px; padding-top: 5px;'>{operator}</div>", 
                              unsafe_allow_html=True)
                
                with col3:
                    power = equation.split(' ')[-1]
                    st.markdown(f"<div style='text-align: center; font-size: 20px; padding-top: 5px;'>{power}</div>", 
                              unsafe_allow_html=True)
                
                with col4:
                    st.markdown("<div style='text-align: center; font-size: 20px; padding-top: 5px;'>=</div>", 
                              unsafe_allow_html=True)
                
                with col5:
                    # Always show the answer for left blank patterns
                    st.markdown(f"<div style='font-size: 20px; padding: 8px; background-color: #f0f0f0; border-radius: 5px; text-align: center;'>{problem['answers'][i]}</div>", 
                              unsafe_allow_html=True)
                    
            else:
                # Normal case or right blank
                col1, col2, col3 = st.columns([2, 0.5, 1.5])
                
                with col1:
                    st.markdown(f"<div style='font-size: 20px; padding: 8px;'>{equation}</div>", 
                              unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='text-align: center; font-size: 20px; padding-top: 5px;'>=</div>", 
                              unsafe_allow_html=True)
                
                with col3:
                    if problem['blanks'][i]:
                        user_input = st.text_input(
                            f"Answer {i+1}",
                            key=f"answer_{i}",
                            disabled=st.session_state.pattern_submitted,
                            placeholder="Enter answer",
                            label_visibility="collapsed"
                        )
                        st.session_state.user_answers[f"answer_{i}"] = user_input
                    else:
                        st.markdown(f"<div style='font-size: 20px; padding: 8px; background-color: #f0f0f0; border-radius: 5px; text-align: center;'>{problem['answers'][i]}</div>", 
                                  unsafe_allow_html=True)

def show_feedback_improved():
    """Display feedback for the submitted answers"""
    problem = st.session_state.pattern_problem
    all_correct = True
    
    st.markdown("### Results:")
    
    for i, equation in enumerate(problem['equations']):
        # Check left blank if applicable
        if problem['type'] in ['mixed_multiply', 'mixed_divide'] and problem.get('blank_positions', [])[i] == 'left':
            try:
                user_left = float(st.session_state.user_answers.get(f"left_answer_{i}", ""))
                correct_left = problem['base_num']
                
                if abs(user_left - correct_left) < 0.0001:
                    st.success(f"✅ {correct_left} {equation[1:]} = {problem['answers'][i]}")
                else:
                    st.error(f"❌ {correct_left} {equation[1:]} = {problem['answers'][i]} (You entered: {user_left})")
                    all_correct = False
                    
            except (ValueError, KeyError):
                st.error(f"❌ {correct_left} {equation[1:]} = {problem['answers'][i]} (Invalid input)")
                all_correct = False
        
        # Check right blank if applicable
        elif problem['blanks'][i]:
            try:
                user_answer = float(st.session_state.user_answers[f"answer_{i}"])
                correct_answer = problem['answers'][i]
                
                if abs(user_answer - correct_answer) < 0.0001:
                    st.success(f"✅ {equation} = {correct_answer}")
                else:
                    st.error(f"❌ {equation} = {correct_answer} (You entered: {user_answer})")
                    all_correct = False
                    
            except (ValueError, KeyError):
                st.error(f"❌ {equation} = {correct_answer} (Invalid input)")
                all_correct = False
    
    # Overall feedback
    if all_correct:
        st.balloons()
        st.success("🎉 **Perfect! You completed the pattern correctly!**")
    else:
        st.info("💡 **Review the pattern and try again. Remember to move the decimal point based on the number of zeros.**")
    
    # Show pattern explanation
    with st.expander("📖 **Understanding the Pattern**", expanded=True):
        if problem['type'] in ['multiply', 'mixed_multiply']:
            st.markdown("### Multiplication Pattern")
            st.markdown("When multiplying by powers of 10:")
            st.markdown("- × 10 → Move decimal 1 place RIGHT")
            st.markdown("- × 100 → Move decimal 2 places RIGHT")
            st.markdown("- × 1000 → Move decimal 3 places RIGHT")
            st.markdown("- × 10000 → Move decimal 4 places RIGHT")
        else:
            st.markdown("### Division Pattern")
            st.markdown("When dividing by powers of 10:")
            st.markdown("- ÷ 10 → Move decimal 1 place LEFT")
            st.markdown("- ÷ 100 → Move decimal 2 places LEFT")
            st.markdown("- ÷ 1000 → Move decimal 3 places LEFT")
            st.markdown("- ÷ 10000 → Move decimal 4 places LEFT")