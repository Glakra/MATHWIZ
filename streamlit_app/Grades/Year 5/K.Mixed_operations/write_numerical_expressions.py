import streamlit as st
import random

def run():
    """
    Main function to run the Write numerical expressions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/write_numerical_expressions.py
    """
    # Initialize session state
    if "expression_difficulty" not in st.session_state:
        st.session_state.expression_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("✏️ Write Numerical Expressions")
    st.markdown("*Convert words to mathematical expressions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.expression_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Simple", "Standard", "Complex", "Multi-operation", "Advanced"]
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
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_expression_problem()
    
    # Display current problem
    display_expression_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Expression Writing Guide**", expanded=False):
        st.markdown("""
        ### How to Write Expressions:
        
        **Operation Symbols:**
        - **Addition:** Use + (plus sign)
        - **Subtraction:** Use - (minus sign)  
        - **Multiplication:** Use × (multiplication sign)
        - **Division:** Use ÷ (division sign)
        
        ### Key Words to Operations:
        
        **➕ Addition Words:**
        - plus, add, sum of
        - increased by, more than
        - combined, total of
        - and (when adding)
        
        **➖ Subtraction Words:**
        - minus, subtract, difference
        - decreased by, less than
        - take away, reduced by
        - from (subtract from)
        
        **✖️ Multiplication Words:**
        - multiply, times, product of
        - by (multiply by)
        - groups of, sets of
        - double, triple, quadruple
        
        **➗ Division Words:**
        - divide, divided by, quotient
        - split into, share equally
        - per, each
        - half of, third of
        
        ### Examples:
        - "6 plus 8" → **6 + 8**
        - "multiply 5 by 9" → **5 × 9**
        - "20 divided by 4" → **20 ÷ 4**
        - "subtract 7 from 15" → **15 - 7**
        
        ### Important Notes:
        - **Do NOT simplify** the expression
        - **Do NOT calculate** the answer
        - Write expressions **exactly** as described
        - Pay attention to **order** (especially for subtraction and division)
        
        ### Order Matters:
        - "subtract 5 from 12" → **12 - 5** (not 5 - 12)
        - "divide 20 by 4" → **20 ÷ 4** (not 4 ÷ 20)
        """)

def generate_expression_templates():
    """Generate diverse expression templates"""
    return {
        "addition": [
            {"template": "{num1} plus {num2}", "expression": "{num1} + {num2}"},
            {"template": "add {num1} and {num2}", "expression": "{num1} + {num2}"},
            {"template": "the sum of {num1} and {num2}", "expression": "{num1} + {num2}"},
            {"template": "{num1} increased by {num2}", "expression": "{num1} + {num2}"},
            {"template": "{num2} more than {num1}", "expression": "{num1} + {num2}"},
            {"template": "{num1} combined with {num2}", "expression": "{num1} + {num2}"},
            {"template": "the total of {num1} and {num2}", "expression": "{num1} + {num2}"},
        ],
        
        "subtraction": [
            {"template": "{num1} minus {num2}", "expression": "{num1} - {num2}"},
            {"template": "subtract {num2} from {num1}", "expression": "{num1} - {num2}"},
            {"template": "{num1} take away {num2}", "expression": "{num1} - {num2}"},
            {"template": "the difference between {num1} and {num2}", "expression": "{num1} - {num2}"},
            {"template": "{num1} decreased by {num2}", "expression": "{num1} - {num2}"},
            {"template": "{num1} less {num2}", "expression": "{num1} - {num2}"},
            {"template": "{num1} reduced by {num2}", "expression": "{num1} - {num2}"},
            {"template": "{num2} less than {num1}", "expression": "{num1} - {num2}"},
        ],
        
        "multiplication": [
            {"template": "multiply {num1} by {num2}", "expression": "{num1} × {num2}"},
            {"template": "{num1} times {num2}", "expression": "{num1} × {num2}"},
            {"template": "the product of {num1} and {num2}", "expression": "{num1} × {num2}"},
            {"template": "{num1} multiplied by {num2}", "expression": "{num1} × {num2}"},
            {"template": "{num2} groups of {num1}", "expression": "{num1} × {num2}"},
            {"template": "{num2} sets of {num1}", "expression": "{num1} × {num2}"},
        ],
        
        "division": [
            {"template": "{num1} divided by {num2}", "expression": "{num1} ÷ {num2}"},
            {"template": "divide {num1} by {num2}", "expression": "{num1} ÷ {num2}"},
            {"template": "the quotient of {num1} and {num2}", "expression": "{num1} ÷ {num2}"},
            {"template": "{num1} split into {num2} equal parts", "expression": "{num1} ÷ {num2}"},
            {"template": "{num1} shared equally among {num2}", "expression": "{num1} ÷ {num2}"},
            {"template": "how many {num2}s are in {num1}", "expression": "{num1} ÷ {num2}"},
        ],
        
        "special": [
            {"template": "double {num1}", "expression": "{num1} × 2", "operation": "multiplication"},
            {"template": "triple {num1}", "expression": "{num1} × 3", "operation": "multiplication"},
            {"template": "quadruple {num1}", "expression": "{num1} × 4", "operation": "multiplication"},
            {"template": "half of {num1}", "expression": "{num1} ÷ 2", "operation": "division"},
            {"template": "a third of {num1}", "expression": "{num1} ÷ 3", "operation": "division"},
            {"template": "a quarter of {num1}", "expression": "{num1} ÷ 4", "operation": "division"},
        ]
    }

def generate_new_expression_problem():
    """Generate a new expression problem based on difficulty"""
    difficulty = st.session_state.expression_difficulty
    templates = generate_expression_templates()
    
    # Choose operation type based on difficulty
    if difficulty == 1:
        # Simple: basic addition and subtraction
        operations = ["addition", "subtraction"]
        use_special = False
    elif difficulty == 2:
        # Standard: all four operations
        operations = ["addition", "subtraction", "multiplication", "division"]
        use_special = False
    elif difficulty == 3:
        # Complex: include special phrases
        operations = ["addition", "subtraction", "multiplication", "division"]
        use_special = True
    else:
        # Multi-operation and Advanced
        operations = ["addition", "subtraction", "multiplication", "division"]
        use_special = True
    
    # For levels 4-5, we might create compound expressions
    if difficulty >= 4 and random.random() < 0.5:
        generate_compound_expression()
        return
    
    # Regular single operation
    if use_special and random.random() < 0.3:
        template_data = random.choice(templates["special"])
        operation = template_data["operation"]
    else:
        operation = random.choice(operations)
        template_data = random.choice(templates[operation])
    
    # Generate numbers based on difficulty
    if difficulty == 1:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
    elif difficulty == 2:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
    elif difficulty == 3:
        num1 = random.randint(10, 100)
        num2 = random.randint(2, 20)
    else:
        num1 = random.randint(10, 500)
        num2 = random.randint(2, 100)
    
    # Ensure sensible division
    if operation == "division":
        # Make sure division is clean for easier checking
        num2 = random.randint(2, 12)
        num1 = num2 * random.randint(2, 20)
    
    # Format the problem and answer
    problem_text = template_data["template"].replace("{num1}", str(num1)).replace("{num2}", str(num2))
    correct_expression = template_data["expression"].replace("{num1}", str(num1)).replace("{num2}", str(num2))
    
    # For special templates that only use num1
    if "{num2}" not in template_data["template"]:
        problem_text = template_data["template"].replace("{num1}", str(num1))
        correct_expression = template_data["expression"].replace("{num1}", str(num1))
    
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "operation": operation,
        "num1": num1,
        "num2": num2 if "{num2}" in template_data["template"] else None
    }
    st.session_state.correct_answer = correct_expression
    st.session_state.current_problem = problem_text

def generate_compound_expression():
    """Generate compound expressions for higher difficulty"""
    difficulty = st.session_state.expression_difficulty
    
    compound_templates = [
        # Two operations
        {
            "template": "add {num1} and {num2}, then multiply by {num3}",
            "expression": "({num1} + {num2}) × {num3}",
            "nums": 3
        },
        {
            "template": "multiply {num1} by {num2}, then add {num3}",
            "expression": "{num1} × {num2} + {num3}",
            "nums": 3
        },
        {
            "template": "subtract {num2} from {num1}, then divide by {num3}",
            "expression": "({num1} - {num2}) ÷ {num3}",
            "nums": 3
        },
        {
            "template": "the sum of {num1} and the product of {num2} and {num3}",
            "expression": "{num1} + {num2} × {num3}",
            "nums": 3
        },
        {
            "template": "divide the sum of {num1} and {num2} by {num3}",
            "expression": "({num1} + {num2}) ÷ {num3}",
            "nums": 3
        },
        {
            "template": "{num1} plus {num2} minus {num3}",
            "expression": "{num1} + {num2} - {num3}",
            "nums": 3
        },
        {
            "template": "the difference between {num1} and the product of {num2} and {num3}",
            "expression": "{num1} - {num2} × {num3}",
            "nums": 3
        }
    ]
    
    if difficulty == 5:
        # Add more complex templates for level 5
        compound_templates.extend([
            {
                "template": "add {num1} and {num2}, multiply by {num3}, then subtract {num4}",
                "expression": "({num1} + {num2}) × {num3} - {num4}",
                "nums": 4
            },
            {
                "template": "the product of {num1} and {num2} divided by the sum of {num3} and {num4}",
                "expression": "{num1} × {num2} ÷ ({num3} + {num4})",
                "nums": 4
            }
        ])
    
    template = random.choice(compound_templates)
    
    # Generate appropriate numbers
    if template["nums"] == 3:
        nums = {
            "num1": random.randint(10, 50),
            "num2": random.randint(5, 30),
            "num3": random.randint(2, 10)
        }
    else:  # 4 numbers
        nums = {
            "num1": random.randint(10, 30),
            "num2": random.randint(5, 20),
            "num3": random.randint(2, 8),
            "num4": random.randint(1, 15)
        }
    
    # Format problem and answer
    problem_text = template["template"]
    correct_expression = template["expression"]
    
    for key, value in nums.items():
        problem_text = problem_text.replace(f"{{{key}}}", str(value))
        correct_expression = correct_expression.replace(f"{{{key}}}", str(value))
    
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "operation": "compound",
        "nums": nums
    }
    st.session_state.correct_answer = correct_expression
    st.session_state.current_problem = problem_text

def display_expression_problem():
    """Display the current expression problem"""
    # Display the problem
    st.markdown("### Write an expression for the operation described below.")
    
    # Problem text in a card
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff;
        border: 2px solid #4169e1;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        font-size: 20px;
        text-align: center;
        font-weight: bold;
    ">
        {st.session_state.current_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions reminder
    st.markdown("""
    <div style="
        background-color: #fffacd;
        border-left: 4px solid #ffd700;
        padding: 15px;
        margin: 20px 0;
        font-style: italic;
    ">
        Type × if you want to use a multiplication sign. Type ÷ if you want to use a division sign. 
        Do not simplify the expression.
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        user_answer = st.text_input(
            "Your expression:",
            key="expression_input",
            placeholder="Enter your expression here..."
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            if user_answer.strip():
                st.session_state.user_answer = user_answer.strip()
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            else:
                st.warning("Please enter an expression before submitting.")
    
    # Show feedback and next button
    handle_feedback_and_next()

def normalize_expression(expr):
    """Normalize an expression for comparison"""
    # Remove all spaces
    expr = expr.replace(" ", "")
    # Replace various multiplication symbols
    expr = expr.replace("*", "×")
    expr = expr.replace("x", "×")
    expr = expr.replace("X", "×")
    # Replace various division symbols
    expr = expr.replace("/", "÷")
    # Remove outer parentheses if they encompass the whole expression
    if expr.startswith("(") and expr.endswith(")"):
        # Check if these are the outermost parentheses
        count = 0
        for i, char in enumerate(expr):
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1
            if count == 0 and i < len(expr) - 1:
                break
        if i == len(expr) - 1:
            expr = expr[1:-1]
    return expr

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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Normalize both answers for comparison
    normalized_user = normalize_expression(user_answer)
    normalized_correct = normalize_expression(correct_answer)
    
    # Check if correct
    is_correct = normalized_user == normalized_correct
    
    # Also check for equivalent forms (e.g., a+b vs b+a for addition/multiplication)
    if not is_correct:
        operation = st.session_state.problem_data.get("operation", "")
        if operation in ["addition", "multiplication"]:
            # Check commutative property
            parts = normalized_correct.split("×" if operation == "multiplication" else "+")
            if len(parts) == 2:
                reversed_expr = f"{parts[1]}{'×' if operation == 'multiplication' else '+'}{parts[0]}"
                if normalized_user == reversed_expr:
                    is_correct = True
    
    if is_correct:
        st.success(f"🎉 **Correct! {correct_answer} is the right expression!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.expression_difficulty
        st.session_state.expression_difficulty = min(
            st.session_state.expression_difficulty + 1, 5
        )
        
        if st.session_state.expression_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Excellent! You've mastered writing expressions!**")
        elif old_difficulty < st.session_state.expression_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.expression_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct expression is: {correct_answer}**")
        st.error(f"You wrote: {user_answer}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.expression_difficulty
        st.session_state.expression_difficulty = max(
            st.session_state.expression_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.expression_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.expression_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_expression_explanation()

def show_expression_explanation():
    """Show explanation for the expression"""
    problem_text = st.session_state.current_problem
    correct_answer = st.session_state.correct_answer
    data = st.session_state.problem_data
    
    with st.expander("📖 **Understanding the Expression**", expanded=True):
        st.markdown("### Let's break it down:")
        
        operation = data.get("operation", "")
        
        if operation == "compound":
            st.markdown(f"""
            **Problem:** {problem_text}
            
            This requires multiple operations. Let's identify each step:
            
            **Correct expression:** {correct_answer}
            
            ### Tips for compound expressions:
            - Read carefully from left to right
            - Use parentheses to show what happens first
            - "then" usually means the previous result is used
            - Pay attention to order of operations
            """)
        else:
            # Identify key words
            key_words = {
                "addition": ["plus", "add", "sum", "increased", "more", "combined", "total"],
                "subtraction": ["minus", "subtract", "difference", "decreased", "less", "from", "reduced"],
                "multiplication": ["multiply", "times", "product", "by", "groups", "double", "triple"],
                "division": ["divide", "divided", "quotient", "split", "shared", "half", "third"]
            }
            
            found_words = []
            for word in key_words.get(operation, []):
                if word in problem_text.lower():
                    found_words.append(word)
            
            st.markdown(f"""
            **Problem:** {problem_text}
            
            **Key words found:** {', '.join(found_words) if found_words else 'None'}
            
            **Operation:** {operation.capitalize()}
            
            **Symbol to use:** {'+' if operation == 'addition' else '-' if operation == 'subtraction' else '×' if operation == 'multiplication' else '÷'}
            
            **Correct expression:** {correct_answer}
            """)
            
            # Special notes for order-sensitive operations
            if operation == "subtraction" and "from" in problem_text.lower():
                st.markdown("""
                ### ⚠️ Order matters!
                "Subtract A from B" means **B - A** (not A - B)
                The number after "from" goes first!
                """)
            
            if operation == "division":
                st.markdown("""
                ### ⚠️ Order matters!
                "Divide A by B" means **A ÷ B**
                The first number is being divided.
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