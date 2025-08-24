import streamlit as st
import random

def run():
    """
    Main function to run the Evaluate numerical expressions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/evaluate_numerical_expressions.py
    """
    # Initialize session state
    if "evaluate_difficulty" not in st.session_state:
        st.session_state.evaluate_difficulty = 1
    
    if "current_expression" not in st.session_state:
        st.session_state.current_expression = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.expression_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("🧮 Evaluate Numerical Expressions")
    st.markdown("*Calculate expressions using order of operations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.evaluate_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Two Operations", "Mixed Operations", "With Parentheses", "Complex", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new expression if needed
    if st.session_state.current_expression is None:
        generate_new_expression()
    
    # Display current expression
    display_expression()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Order of Operations Guide (PEMDAS)**", expanded=False):
        st.markdown("""
        ### Remember: PEMDAS / BODMAS
        
        **P**arentheses / **B**rackets
        **E**xponents / **O**rders
        **M**ultiplication and **D**ivision (left to right)
        **A**ddition and **S**ubtraction (left to right)
        
        ### Step-by-Step Process:
        
        1️⃣ **Parentheses First**
        - Always do operations inside ( ) first
        - Example: 2 + (3 × 4) = 2 + 12 = 14
        
        2️⃣ **Multiplication & Division** (left to right)
        - These have equal priority
        - Do them from left to right
        - Example: 10 ÷ 2 × 3 = 5 × 3 = 15
        
        3️⃣ **Addition & Subtraction** (left to right)
        - These have equal priority
        - Do them from left to right
        - Example: 8 - 3 + 2 = 5 + 2 = 7
        
        ### Common Mistakes to Avoid:
        
        ❌ **Wrong:** 2 + 3 × 4 = 5 × 4 = 20
        ✅ **Right:** 2 + 3 × 4 = 2 + 12 = 14
        
        ❌ **Wrong:** 12 ÷ 3 × 2 = 12 ÷ 6 = 2
        ✅ **Right:** 12 ÷ 3 × 2 = 4 × 2 = 8
        
        ### Examples:
        
        **Example 1:** 5 + 5 × 2
        - First: 5 × 2 = 10
        - Then: 5 + 10 = 15
        
        **Example 2:** (4 + 6) ÷ 2
        - First: 4 + 6 = 10
        - Then: 10 ÷ 2 = 5
        
        **Example 3:** 3 × 5 ÷ 3
        - Left to right: 3 × 5 = 15
        - Then: 15 ÷ 3 = 5
        
        ### Tips:
        - **Underline** or **circle** operations you'll do first
        - Work step by step
        - Check your work by redoing the calculation
        """)

def generate_expression_templates():
    """Generate expression templates for different difficulty levels"""
    return {
        1: [  # Two operations - simple
            # Addition and subtraction only
            "{a} + {b} - {c}",
            "{a} - {b} + {c}",
            # Multiplication with addition/subtraction
            "{a} × {b} + {c}",
            "{a} + {b} × {c}",
            "{a} × {b} - {c}",
            "{a} - {b} × {c}",
            # Division with addition/subtraction
            "{a} ÷ {b} + {c}",
            "{a} + {b} ÷ {c}",
            "{a} ÷ {b} - {c}",
            "{a} - {b} ÷ {c}",
        ],
        
        2: [  # Mixed operations - no parentheses
            # Three operations
            "{a} + {b} × {c} - {d}",
            "{a} × {b} + {c} - {d}",
            "{a} × {b} ÷ {c} + {d}",
            "{a} + {b} ÷ {c} × {d}",
            "{a} × {b} + {c} × {d}",
            "{a} ÷ {b} + {c} ÷ {d}",
            # Chains of same precedence
            "{a} × {b} × {c}",
            "{a} ÷ {b} × {c}",
            "{a} × {b} ÷ {c}",
            "{a} + {b} - {c} + {d}",
        ],
        
        3: [  # With parentheses
            "({a} + {b}) × {c}",
            "{a} × ({b} + {c})",
            "({a} - {b}) × {c}",
            "{a} × ({b} - {c})",
            "({a} + {b}) ÷ {c}",
            "{a} ÷ ({b} + {c})",
            "({a} - {b}) ÷ {c}",
            "({a} × {b}) + {c}",
            "({a} × {b}) - {c}",
            "({a} ÷ {b}) + {c}",
            "{a} + ({b} × {c})",
            "{a} - ({b} × {c})",
            "({a} + {b}) × ({c} - {d})",
        ],
        
        4: [  # Complex expressions
            "{a} × {b} + {c} × {d} - {e}",
            "({a} + {b}) × {c} - {d} ÷ {e}",
            "{a} × ({b} + {c}) ÷ {d}",
            "({a} - {b}) × ({c} + {d})",
            "{a} + {b} × {c} ÷ {d}",
            "({a} × {b} - {c}) ÷ {d}",
            "{a} × {b} - ({c} + {d}) × {e}",
            "({a} + {b} × {c}) ÷ {d}",
        ],
        
        5: [  # Master level - nested parentheses and complex
            "(({a} + {b}) × {c} - {d}) ÷ {e}",
            "{a} × ({b} + {c} × {d}) - {e}",
            "({a} + {b}) × ({c} - {d}) ÷ {e}",
            "{a} × {b} + ({c} - {d}) × ({e} + {f})",
            "(({a} - {b}) × {c} + {d}) ÷ ({e} - {f})",
            "{a} + {b} × ({c} + {d} ÷ {e})",
            "({a} × {b} - {c} × {d}) + {e} ÷ {f}",
        ]
    }

def generate_new_expression():
    """Generate a new expression based on difficulty"""
    difficulty = st.session_state.evaluate_difficulty
    templates = generate_expression_templates()
    
    # Choose a template
    template = random.choice(templates[difficulty])
    
    # Generate appropriate numbers
    if difficulty == 1:
        # Simple numbers for level 1
        numbers = {
            'a': random.randint(1, 10),
            'b': random.randint(1, 10),
            'c': random.randint(1, 10),
            'd': random.randint(1, 10),
        }
    elif difficulty == 2:
        # Slightly larger numbers
        numbers = {
            'a': random.randint(2, 15),
            'b': random.randint(2, 12),
            'c': random.randint(1, 10),
            'd': random.randint(1, 10),
        }
    elif difficulty == 3:
        # Mix of numbers
        numbers = {
            'a': random.randint(3, 20),
            'b': random.randint(2, 15),
            'c': random.randint(2, 12),
            'd': random.randint(2, 10),
        }
    elif difficulty == 4:
        # Larger range
        numbers = {
            'a': random.randint(5, 25),
            'b': random.randint(3, 20),
            'c': random.randint(2, 15),
            'd': random.randint(2, 12),
            'e': random.randint(2, 10),
        }
    else:  # difficulty == 5
        # Complex numbers
        numbers = {
            'a': random.randint(5, 30),
            'b': random.randint(3, 25),
            'c': random.randint(2, 20),
            'd': random.randint(2, 15),
            'e': random.randint(2, 12),
            'f': random.randint(2, 10),
        }
    
    # Special handling for division - ensure clean results
    expression = template
    for var in ['a', 'b', 'c', 'd', 'e', 'f']:
        if f'{{{var}}}' in expression:
            # Check if this variable is used in division
            if f'÷ {{{var}}}' in expression or f'{{{var}}} ÷' in expression:
                # For divisors, use smaller numbers
                if f'÷ {{{var}}}' in expression:
                    numbers[var] = random.randint(2, 6)
                # For dividends, make them multiples
                elif f'{{{var}}} ÷' in expression and var in numbers:
                    next_var = chr(ord(var) + 1)
                    if f'÷ {{{next_var}}}' in expression and next_var in numbers:
                        divisor = numbers[next_var]
                        numbers[var] = divisor * random.randint(2, 8)
    
    # Build the expression
    for var, value in numbers.items():
        expression = expression.replace(f'{{{var}}}', str(value))
    
    # Calculate the correct answer
    try:
        # Replace × and ÷ with * and / for eval
        eval_expr = expression.replace('×', '*').replace('÷', '/')
        correct_answer = eval(eval_expr)
        
        # Round if necessary (for division results)
        if isinstance(correct_answer, float):
            if correct_answer == int(correct_answer):
                correct_answer = int(correct_answer)
            else:
                correct_answer = round(correct_answer, 2)
    except:
        # Fallback to a simple expression if evaluation fails
        expression = "5 + 3 × 2"
        correct_answer = 11
    
    st.session_state.expression_data = {
        "expression": expression,
        "template": template,
        "numbers": numbers
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_expression = expression

def display_expression():
    """Display the current expression to evaluate"""
    st.markdown("### Evaluate the expression.")
    
    # Display expression in a card
    st.markdown(f"""
    <div style="
        background-color: #f5f5f5;
        border: 3px solid #333;
        border-radius: 15px;
        padding: 40px;
        margin: 30px auto;
        max-width: 500px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <div style="
            font-size: 32px;
            font-weight: bold;
            color: #333;
            letter-spacing: 3px;
        ">
            {st.session_state.current_expression}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        user_answer = st.number_input(
            "Your answer:",
            min_value=-9999,
            max_value=9999,
            step=1,
            key="evaluate_answer"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
                reset_expression_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Handle floating point comparison
    if isinstance(correct_answer, float):
        is_correct = abs(user_answer - correct_answer) < 0.01
    else:
        is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success(f"🎉 **Correct! The answer is {correct_answer}!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.evaluate_difficulty
        st.session_state.evaluate_difficulty = min(
            st.session_state.evaluate_difficulty + 1, 5
        )
        
        if st.session_state.evaluate_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered order of operations!**")
        elif old_difficulty < st.session_state.evaluate_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.evaluate_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer}.**")
        st.error(f"You answered: {user_answer}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.evaluate_difficulty
        st.session_state.evaluate_difficulty = max(
            st.session_state.evaluate_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.evaluate_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.evaluate_difficulty}. Keep practicing!**")
        
        # Show step-by-step solution
        show_step_by_step_solution()

def show_step_by_step_solution():
    """Show detailed step-by-step solution"""
    expression = st.session_state.current_expression
    answer = st.session_state.correct_answer
    
    with st.expander("📖 **Step-by-Step Solution**", expanded=True):
        st.markdown(f"### Let's evaluate: {expression}")
        
        # Create a working copy of the expression
        work_expr = expression
        steps = []
        
        # Step 1: Handle parentheses
        while '(' in work_expr:
            # Find innermost parentheses
            start = -1
            for i, char in enumerate(work_expr):
                if char == '(':
                    start = i
                elif char == ')' and start != -1:
                    # Evaluate what's inside
                    inner = work_expr[start+1:i]
                    inner_eval = inner.replace('×', '*').replace('÷', '/')
                    try:
                        result = eval(inner_eval)
                        if isinstance(result, float) and result == int(result):
                            result = int(result)
                        steps.append(f"Evaluate inside parentheses: ({inner}) = {result}")
                        work_expr = work_expr[:start] + str(result) + work_expr[i+1:]
                        break
                    except:
                        break
        
        # Step 2: Handle multiplication and division (left to right)
        while '×' in work_expr or '÷' in work_expr:
            # Find the leftmost × or ÷
            mult_pos = work_expr.find('×')
            div_pos = work_expr.find('÷')
            
            if mult_pos == -1:
                pos = div_pos
                op = '÷'
            elif div_pos == -1:
                pos = mult_pos
                op = '×'
            else:
                if mult_pos < div_pos:
                    pos = mult_pos
                    op = '×'
                else:
                    pos = div_pos
                    op = '÷'
            
            if pos != -1:
                # Find the numbers around the operation
                left_num, right_num, left_start, right_end = extract_numbers_around_op(work_expr, pos)
                
                if op == '×':
                    result = left_num * right_num
                    steps.append(f"Multiply: {left_num} × {right_num} = {result}")
                else:
                    result = left_num / right_num
                    if result == int(result):
                        result = int(result)
                    else:
                        result = round(result, 2)
                    steps.append(f"Divide: {left_num} ÷ {right_num} = {result}")
                
                work_expr = work_expr[:left_start] + str(result) + work_expr[right_end:]
        
        # Step 3: Handle addition and subtraction (left to right)
        while '+' in work_expr or ('-' in work_expr and not work_expr.startswith('-')):
            # Find the leftmost + or -
            add_pos = work_expr.find('+')
            # Find subtraction (not negative numbers)
            sub_pos = -1
            for i in range(1, len(work_expr)):
                if work_expr[i] == '-':
                    sub_pos = i
                    break
            
            if add_pos == -1 and sub_pos == -1:
                break
            elif add_pos == -1:
                pos = sub_pos
                op = '-'
            elif sub_pos == -1:
                pos = add_pos
                op = '+'
            else:
                if add_pos < sub_pos:
                    pos = add_pos
                    op = '+'
                else:
                    pos = sub_pos
                    op = '-'
            
            if pos != -1:
                # Find the numbers around the operation
                left_num, right_num, left_start, right_end = extract_numbers_around_op(work_expr, pos)
                
                if op == '+':
                    result = left_num + right_num
                    steps.append(f"Add: {left_num} + {right_num} = {result}")
                else:
                    result = left_num - right_num
                    steps.append(f"Subtract: {left_num} - {right_num} = {result}")
                
                work_expr = work_expr[:left_start] + str(result) + work_expr[right_end:]
        
        # Display all steps
        st.markdown("### Order of Operations (PEMDAS):")
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"**Step {i}:** {step}")
        
        st.markdown(f"\n### Final Answer: **{answer}**")
        
        # Add a visual representation
        st.markdown("\n### Remember:")
        st.markdown("""
        1️⃣ **P**arentheses first
        2️⃣ **M**ultiplication and **D**ivision (left to right)
        3️⃣ **A**ddition and **S**ubtraction (left to right)
        """)

def extract_numbers_around_op(expr, op_pos):
    """Extract numbers around an operation"""
    # Find left number
    left_start = op_pos - 1
    while left_start > 0 and (expr[left_start-1].isdigit() or expr[left_start-1] == '.'):
        left_start -= 1
    if left_start > 0 and expr[left_start-1] == '-':
        left_start -= 1
    
    # Find right number
    right_end = op_pos + 1
    if right_end < len(expr) and expr[right_end] == '-':
        right_end += 1
    while right_end < len(expr) and (expr[right_end].isdigit() or expr[right_end] == '.'):
        right_end += 1
    
    left_num_str = expr[left_start:op_pos].strip()
    right_num_str = expr[op_pos+1:right_end].strip()
    
    try:
        left_num = float(left_num_str) if '.' in left_num_str else int(left_num_str)
        right_num = float(right_num_str) if '.' in right_num_str else int(right_num_str)
    except:
        left_num = 0
        right_num = 1
    
    return left_num, right_num, left_start, right_end

def reset_expression_state():
    """Reset the expression state for next question"""
    st.session_state.current_expression = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.expression_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer