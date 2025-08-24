import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Inequalities with addition and subtraction of fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/inequalities_with_addition_and_subtraction_of_fractions.py
    """
    # Initialize session state for difficulty and score
    if "inequalities_difficulty" not in st.session_state:
        st.session_state.inequalities_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "inequalities_score" not in st.session_state:
        st.session_state.inequalities_score = 0
        st.session_state.inequalities_attempts = 0
    
    if "current_inequality" not in st.session_state:
        st.session_state.current_inequality = None
        st.session_state.correct_sign = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.selected_sign = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("⚖️ Inequalities with Fractions")
    st.markdown("*Compare fractions and fraction expressions*")
    st.markdown("---")
    
    # Difficulty and score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        st.markdown(f"**Difficulty:** {difficulty_names[st.session_state.inequalities_difficulty]}")
        st.markdown(f"**Score:** {st.session_state.inequalities_score}/{st.session_state.inequalities_attempts}")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new inequality if needed
    if st.session_state.current_inequality is None:
        generate_new_inequality()
    
    # Display current inequality
    display_inequality()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **How to Compare Fraction Expressions**", expanded=False):
        st.markdown("""
        ### Steps to Compare:
        
        1. **Simplify each side** - Add or subtract fractions
        2. **Find common denominators** if needed
        3. **Compare the results**
        
        ### Examples:
        - **11/15 + 14/15 ? 1/3**
          - Left: 11/15 + 14/15 = 25/15 = 5/3
          - Right: 1/3
          - Compare: 5/3 > 1/3 ✓
        
        - **7/9 - 2/9 ? 6/9**
          - Left: 7/9 - 2/9 = 5/9
          - Right: 6/9
          - Compare: 5/9 < 6/9 ✓
        
        ### Remember:
        - **>** means "greater than"
        - **<** means "less than"  
        - **=** means "equal to"
        """)

def generate_new_inequality():
    """Generate a new fraction inequality problem with expressions"""
    difficulty = st.session_state.inequalities_difficulty
    
    if difficulty == 1:  # Easy - same denominators
        problem_types = [
            "add_same_vs_single",  # a/d + b/d vs c/d
            "sub_same_vs_single",  # a/d - b/d vs c/d
            "single_vs_add_same",  # a/d vs b/d + c/d
            "sub_same_vs_sub_same"  # a/d - b/d vs c/d - e/d
        ]
        
        problem_type = random.choice(problem_types)
        
        if problem_type == "add_same_vs_single":
            # Like: 11/15 + 14/15 vs 1/3
            d1 = random.choice([9, 10, 12, 15, 18, 20])
            n1 = random.randint(1, d1//2)
            n2 = random.randint(1, d1//2)
            
            # Make sure sum doesn't exceed denominator
            if n1 + n2 >= d1:
                n2 = d1 - n1 - 1
            
            left_expr = [(n1, d1, "+"), (n2, d1, None)]
            
            # Right side - different denominator
            d2 = random.choice([2, 3, 4, 5, 6])
            n3 = random.randint(1, d2-1)
            right_expr = [(n3, d2, None)]
            
        elif problem_type == "sub_same_vs_single":
            # Like: 7/9 - 2/9 vs 6/9
            d1 = random.choice([9, 10, 12, 15, 18])
            n1 = random.randint(d1//2, d1-1)
            n2 = random.randint(1, n1-1)
            
            left_expr = [(n1, d1, "-"), (n2, d1, None)]
            
            # Right side - same or different denominator
            if random.choice([True, False]):
                right_expr = [(random.randint(1, d1-1), d1, None)]
            else:
                d2 = random.choice([2, 3, 4, 5])
                right_expr = [(random.randint(1, d2-1), d2, None)]
        
        elif problem_type == "single_vs_add_same":
            # Like: 1/2 vs 2/12 + 1/2
            d1 = random.choice([2, 3, 4, 5, 6])
            n1 = random.randint(1, d1-1)
            left_expr = [(n1, d1, None)]
            
            # Right side
            d2 = random.choice([8, 10, 12, 15, 18])
            n2 = random.randint(1, d2//3)
            n3 = random.randint(1, d1-1)
            right_expr = [(n2, d2, "+"), (n3, d1, None)]
        
        else:  # sub_same_vs_sub_same
            # Both sides have subtraction
            d = random.choice([12, 15, 18, 20])
            n1 = random.randint(d//2, d-1)
            n2 = random.randint(1, n1//2)
            left_expr = [(n1, d, "-"), (n2, d, None)]
            
            n3 = random.randint(d//2, d-1)
            n4 = random.randint(1, n3//2)
            right_expr = [(n3, d, "-"), (n4, d, None)]
    
    elif difficulty == 2:  # Medium - mixed denominators
        problem_types = [
            "add_mixed_vs_single",
            "sub_mixed_vs_single",
            "add_vs_add_mixed",
            "mixed_three_terms"
        ]
        
        problem_type = random.choice(problem_types)
        
        if problem_type == "add_mixed_vs_single":
            # Different denominators on left, single on right
            d1 = random.choice([3, 4, 5, 6])
            d2 = random.choice([6, 8, 10, 12])
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            
            left_expr = [(n1, d1, "+"), (n2, d2, None)]
            
            d3 = random.choice([2, 3, 4, 5])
            n3 = random.randint(1, d3-1)
            right_expr = [(n3, d3, None)]
            
        elif problem_type == "sub_mixed_vs_single":
            # Subtraction with different denominators
            d1 = random.choice([3, 4, 5, 6, 8])
            d2 = random.choice([6, 8, 10, 12])
            
            # Ensure valid subtraction
            frac1 = Fraction(random.randint(2, d1-1), d1)
            frac2 = Fraction(random.randint(1, d2-1), d2)
            if frac1 < frac2:
                frac1, frac2 = frac2, frac1
            
            left_expr = [(frac1.numerator, frac1.denominator, "-"), 
                        (frac2.numerator, frac2.denominator, None)]
            
            d3 = random.choice([3, 4, 5, 6])
            n3 = random.randint(1, d3-1)
            right_expr = [(n3, d3, None)]
        
        elif problem_type == "add_vs_add_mixed":
            # Addition on both sides
            d1, d2 = random.sample([3, 4, 5, 6, 8], 2)
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            left_expr = [(n1, d1, "+"), (n2, d2, None)]
            
            d3, d4 = random.sample([3, 4, 5, 6, 8, 10], 2)
            n3 = random.randint(1, d3-1)
            n4 = random.randint(1, d4-1)
            right_expr = [(n3, d3, "+"), (n4, d4, None)]
        
        else:  # mixed_three_terms
            # Three terms total
            d1 = random.choice([4, 5, 6])
            d2 = random.choice([8, 10, 12])
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            n3 = random.randint(1, d1-1)
            
            left_expr = [(n1, d1, "+"), (n2, d2, None)]
            right_expr = [(n3, d1, None)]
    
    else:  # Hard - complex expressions
        problem_types = [
            "three_terms_left",
            "three_terms_both",
            "mixed_add_sub",
            "complex_mixed"
        ]
        
        problem_type = random.choice(problem_types)
        
        if problem_type == "three_terms_left":
            # Three terms on left side
            denominators = [3, 4, 5, 6, 8, 10, 12]
            d1, d2, d3 = random.sample(denominators, 3)
            n1 = random.randint(1, max(1, d1//3))
            n2 = random.randint(1, max(1, d2//3))
            n3 = random.randint(1, max(1, d3//3))
            
            ops = random.choice([("+", "+"), ("+", "-"), ("-", "+")])
            if "-" in ops:
                # Ensure valid subtraction
                total = Fraction(n1, d1)
                if ops[0] == "+":
                    total += Fraction(n2, d2)
                    if total < Fraction(n3, d3):
                        n3 = 1
                else:
                    if total < Fraction(n2, d2):
                        n1, n2 = n2, n1
                        d1, d2 = d2, d1
            
            left_expr = [(n1, d1, ops[0]), (n2, d2, ops[1]), (n3, d3, None)]
            
            # Simple right side
            d4 = random.choice([2, 3, 4, 5])
            n4 = random.randint(1, d4-1)
            right_expr = [(n4, d4, None)]
        
        elif problem_type == "three_terms_both":
            # Three terms total, split between sides
            if random.choice([True, False]):
                # 2 on left, 1 on right
                d1, d2 = random.sample([3, 4, 5, 6], 2)
                n1 = random.randint(1, d1-1)
                n2 = random.randint(1, d2-1)
                left_expr = [(n1, d1, "+"), (n2, d2, None)]
                
                d3 = random.choice([2, 3, 4, 5])
                n3 = random.randint(1, d3-1)
                right_expr = [(n3, d3, None)]
            else:
                # 1 on left, 2 on right
                d1 = random.choice([2, 3, 4, 5])
                n1 = random.randint(1, d1-1)
                left_expr = [(n1, d1, None)]
                
                d2, d3 = random.sample([3, 4, 5, 6, 8], 2)
                n2 = random.randint(1, d2-1)
                n3 = random.randint(1, d3-1)
                right_expr = [(n2, d2, "+"), (n3, d3, None)]
        
        elif problem_type == "mixed_add_sub":
            # Mix of addition and subtraction
            d1, d2, d3 = random.sample([3, 4, 5, 6, 8, 10], 3)
            n1 = random.randint(d1//2, d1-1)  # Start with larger number
            n2 = random.randint(1, min(n1, d2-1))
            n3 = random.randint(1, d3-1)
            
            left_expr = [(n1, d1, "-"), (n2, d2, "+"), (n3, d3, None)]
            
            d4 = random.choice([2, 3, 4, 5, 6])
            n4 = random.randint(1, d4-1)
            right_expr = [(n4, d4, None)]
        
        else:  # complex_mixed
            # Both sides have operations
            d1, d2 = random.sample([3, 4, 5, 6], 2)
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            
            op1 = random.choice(["+", "-"])
            if op1 == "-" and Fraction(n1, d1) < Fraction(n2, d2):
                n1, n2, d1, d2 = n2, n1, d2, d1
            
            left_expr = [(n1, d1, op1), (n2, d2, None)]
            
            d3, d4 = random.sample([3, 4, 5, 6, 8], 2)
            n3 = random.randint(1, d3-1)
            n4 = random.randint(1, d4-1)
            
            op2 = random.choice(["+", "-"])
            if op2 == "-" and Fraction(n3, d3) < Fraction(n4, d4):
                n3, n4, d3, d4 = n4, n3, d4, d3
            
            right_expr = [(n3, d3, op2), (n4, d4, None)]
    
    # Calculate the values
    left_value = calculate_expression(left_expr)
    right_value = calculate_expression(right_expr)
    
    # Determine correct sign
    if left_value > right_value:
        correct_sign = ">"
    elif left_value < right_value:
        correct_sign = "<"
    else:
        correct_sign = "="
    
    # Store the inequality
    st.session_state.current_inequality = {
        "left_expr": left_expr,
        "right_expr": right_expr,
        "left_value": left_value,
        "right_value": right_value
    }
    st.session_state.correct_sign = correct_sign
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.selected_sign = None

def calculate_expression(expr):
    """Calculate the value of a fraction expression"""
    result = Fraction(0)
    current_op = "+"
    
    for item in expr:
        num, denom, next_op = item
        frac = Fraction(num, denom)
        
        if current_op == "+":
            result += frac
        elif current_op == "-":
            result -= frac
        
        if next_op:
            current_op = next_op
    
    return result

def format_expression_display(expr):
    """Format expression for display"""
    parts = []
    for i, (num, denom, op) in enumerate(expr):
        parts.append(f"{num}/{denom}")
        if op:
            parts.append(op)
    return " ".join(parts)

def display_inequality():
    """Display the inequality problem with clickable buttons"""
    st.markdown("### Which sign makes the statement true?")
    
    inequality = st.session_state.current_inequality
    
    # Format expressions
    left_display = format_expression_display(inequality["left_expr"])
    right_display = format_expression_display(inequality["right_expr"])
    
    # Display the inequality with a placeholder for the sign
    col1, col2, col3 = st.columns([2.5, 1, 2.5])
    
    with col1:
        st.markdown(
            f"""<div style="text-align: right; font-size: 24px; padding: 20px;">
                {left_display}
            </div>""", 
            unsafe_allow_html=True
        )
    
    with col2:
        if st.session_state.selected_sign:
            sign_display = st.session_state.selected_sign
            if sign_display == ">":
                sign_display = "&gt;"
            elif sign_display == "<":
                sign_display = "&lt;"
            st.markdown(
                f"""<div style="text-align: center; font-size: 24px; padding: 20px; 
                    background-color: #e3f2fd; border-radius: 50%; width: 60px; 
                    height: 60px; margin: auto; display: flex; align-items: center; 
                    justify-content: center;">
                    {sign_display}
                </div>""", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """<div style="text-align: center; font-size: 24px; padding: 20px; 
                    background-color: #f5f5f5; border-radius: 50%; width: 60px; 
                    height: 60px; margin: auto; display: flex; align-items: center; 
                    justify-content: center;">
                    ?
                </div>""", 
                unsafe_allow_html=True
            )
    
    with col3:
        st.markdown(
            f"""<div style="text-align: left; font-size: 24px; padding: 20px;">
                {right_display}
            </div>""", 
            unsafe_allow_html=True
        )
    
    # Sign selection buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("**>**", key="greater", use_container_width=True, 
                    disabled=st.session_state.answer_submitted,
                    type="primary" if st.session_state.selected_sign == ">" else "secondary"):
            st.session_state.selected_sign = ">"
            st.rerun()
    
    with col2:
        if st.button("**<**", key="less", use_container_width=True,
                    disabled=st.session_state.answer_submitted,
                    type="primary" if st.session_state.selected_sign == "<" else "secondary"):
            st.session_state.selected_sign = "<"
            st.rerun()
    
    with col3:
        if st.button("**=**", key="equal", use_container_width=True,
                    disabled=st.session_state.answer_submitted,
                    type="primary" if st.session_state.selected_sign == "=" else "secondary"):
            st.session_state.selected_sign = "="
            st.rerun()
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                    disabled=st.session_state.answer_submitted or not st.session_state.selected_sign):
            if st.session_state.selected_sign:
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
                st.session_state.inequalities_attempts += 1
                st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_inequality()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    selected_sign = st.session_state.selected_sign
    correct_sign = st.session_state.correct_sign
    
    if selected_sign == correct_sign:
        st.success("🎉 **Correct! Great job!**")
        st.session_state.inequalities_score += 1
        
        # Increase difficulty
        if st.session_state.inequalities_score % 3 == 0:
            old_difficulty = st.session_state.inequalities_difficulty
            st.session_state.inequalities_difficulty = min(3, old_difficulty + 1)
            if st.session_state.inequalities_difficulty > old_difficulty:
                st.info(f"⬆️ **Level up! Moving to {['', 'Easy', 'Medium', 'Hard'][st.session_state.inequalities_difficulty]} problems.**")
    else:
        sign_display = {"<": "<", ">": ">", "=": "="}
        st.error(f"❌ **Not quite. The correct sign is {sign_display[correct_sign]}**")
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if struggling
        if st.session_state.inequalities_attempts > 0:
            accuracy = st.session_state.inequalities_score / st.session_state.inequalities_attempts
            if accuracy < 0.5 and st.session_state.inequalities_attempts % 5 == 0:
                old_difficulty = st.session_state.inequalities_difficulty
                st.session_state.inequalities_difficulty = max(1, old_difficulty - 1)
                if st.session_state.inequalities_difficulty < old_difficulty:
                    st.warning(f"⬇️ **Let's practice with {['', 'Easy', 'Medium', 'Hard'][st.session_state.inequalities_difficulty]} problems.**")

def show_explanation():
    """Show explanation for the comparison"""
    inequality = st.session_state.current_inequality
    left_value = inequality["left_value"]
    right_value = inequality["right_value"]
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        st.markdown("### Left Side:")
        left_display = format_expression_display(inequality["left_expr"])
        st.markdown(f"{left_display} = **{left_value}**")
        
        if len(inequality["left_expr"]) > 1:
            st.markdown("Working:")
            work_str = ""
            for i, (num, denom, op) in enumerate(inequality["left_expr"]):
                if i == 0:
                    work_str = f"{num}/{denom}"
                else:
                    work_str = f"({work_str}) {inequality['left_expr'][i-1][2]} {num}/{denom}"
            st.markdown(f"= {left_value}")
        
        st.markdown("### Right Side:")
        right_display = format_expression_display(inequality["right_expr"])
        st.markdown(f"{right_display} = **{right_value}**")
        
        if len(inequality["right_expr"]) > 1:
            st.markdown("Working:")
            work_str = ""
            for i, (num, denom, op) in enumerate(inequality["right_expr"]):
                if i == 0:
                    work_str = f"{num}/{denom}"
                else:
                    work_str = f"({work_str}) {inequality['right_expr'][i-1][2]} {num}/{denom}"
            st.markdown(f"= {right_value}")
        
        # Show comparison
        st.markdown("### Comparison:")
        left_decimal = float(left_value)
        right_decimal = float(right_value)
        
        st.markdown(f"""
        {left_value} = {left_decimal:.4f}  
        {right_value} = {right_decimal:.4f}
        """)
        
        if left_value > right_value:
            st.markdown(f"Since {left_decimal:.4f} > {right_decimal:.4f}, the answer is **>**")
        elif left_value < right_value:
            st.markdown(f"Since {left_decimal:.4f} < {right_decimal:.4f}, the answer is **<**")
        else:
            st.markdown(f"Since {left_decimal:.4f} = {right_decimal:.4f}, the answer is **=**")

def reset_inequality():
    """Reset for next problem"""
    st.session_state.current_inequality = None
    st.session_state.correct_sign = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.selected_sign = None