import streamlit as st
import random

def run():
    """
    Main function to run the Estimate products of whole numbers and decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/estimate_products_of_whole_numbers_and_decimals.py
    """
    # Initialize session state
    if "estimate_product_problem" not in st.session_state:
        st.session_state.estimate_product_problem = None
        st.session_state.estimate_product_answer_submitted = False
        st.session_state.user_product_estimate = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("🎯 Estimate Products of Whole Numbers and Decimals")
    st.markdown("*Round to the greatest place value, then multiply*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.estimate_product_problem is None:
        st.session_state.estimate_product_problem = generate_problem()
        st.session_state.estimate_product_answer_submitted = False
        st.session_state.user_product_estimate = ""
    
    problem = st.session_state.estimate_product_problem
    
    # Display the question
    st.markdown("### 📝 Estimate the product. Round each number to its greatest place value, then multiply.")
    
    # Display the expression
    st.markdown(f"<h2 style='text-align: center; color: #1976d2; margin: 30px 0;'>{problem['expression']}</h2>", 
                unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create input with label
        user_input = st.text_input(
            "The product is approximately",
            value=st.session_state.user_product_estimate,
            key="product_estimate_input",
            disabled=st.session_state.estimate_product_answer_submitted,
            placeholder="Enter your estimate"
        )
        st.session_state.user_product_estimate = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.estimate_product_answer_submitted):
            
            if st.session_state.user_product_estimate.strip() == "":
                st.warning("⚠️ Please enter your estimate.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_product_estimate)
                    st.session_state.estimate_product_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid number.")
    
    # Show feedback if answer was submitted
    if st.session_state.estimate_product_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.estimate_product_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.estimate_product_problem = None
                st.session_state.estimate_product_answer_submitted = False
                st.session_state.user_product_estimate = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Estimate Products:
        1. **Round each number to its greatest place value**
        2. **Multiply the rounded numbers**
        3. **Enter your estimate**
        
        ### Rounding to Greatest Place Value:
        - **47** → Round to nearest ten → **50**
        - **382** → Round to nearest hundred → **400**
        - **1.1** → Round to nearest whole number → **1**
        - **0.89** → Round to nearest whole number → **1**
        - **5.7** → Round to nearest whole number → **6**
        - **12.3** → Round to nearest ten → **10**
        
        ### Examples:
        - **47 × 1.1**
          - Round: 47 → 50 (nearest ten)
          - Round: 1.1 → 1 (nearest whole)
          - Estimate: 50 × 1 = 50
        
        - **23 × 4.8**
          - Round: 23 → 20 (nearest ten)
          - Round: 4.8 → 5 (nearest whole)
          - Estimate: 20 × 5 = 100
        
        - **156 × 2.3**
          - Round: 156 → 200 (nearest hundred)
          - Round: 2.3 → 2 (nearest whole)
          - Estimate: 200 × 2 = 400
        
        ### Why Estimate Products?
        - **Quick mental math** for shopping (price × quantity)
        - **Check if your exact answer** is reasonable
        - **Useful for budgeting** and planning
        
        ### Remember:
        - Round to the **greatest (leftmost) place value**
        - For decimals less than 10, round to the nearest whole number
        - The estimate helps you check if your exact answer makes sense
        """)

def generate_problem():
    """Generate a random product estimation problem"""
    problem_types = [
        'two_digit_decimal',      # e.g., 47 × 1.1
        'three_digit_decimal',    # e.g., 234 × 2.7
        'decimal_whole',          # e.g., 3.4 × 28
        'two_decimals'           # e.g., 4.7 × 8.2
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'two_digit_decimal':
        # Two-digit whole number × decimal
        num1 = random.randint(11, 99)
        num2 = round(random.uniform(0.1, 9.9), 1)
        
    elif problem_type == 'three_digit_decimal':
        # Three-digit whole number × decimal
        num1 = random.randint(101, 999)
        num2 = round(random.uniform(0.1, 9.9), 1)
        
    elif problem_type == 'decimal_whole':
        # Decimal × whole number
        num1 = round(random.uniform(0.1, 9.9), 1)
        num2 = random.randint(11, 99)
        
    else:  # two_decimals
        # Two decimals
        num1 = round(random.uniform(1.1, 9.9), 1)
        num2 = round(random.uniform(1.1, 9.9), 1)
    
    # Create expression
    expression = f"{num1} × {num2}"
    
    # Round each number to its greatest place value
    rounded1 = round_to_greatest_place_value(num1)
    rounded2 = round_to_greatest_place_value(num2)
    
    # Calculate answer
    answer = rounded1 * rounded2
    
    return {
        'numbers': [num1, num2],
        'expression': expression,
        'rounded_numbers': [rounded1, rounded2],
        'answer': int(answer) if answer == int(answer) else answer,
        'place_values': [get_place_value_name(num1), get_place_value_name(num2)]
    }

def round_to_greatest_place_value(num):
    """Round a number to its greatest place value"""
    if num < 1:
        # For decimals less than 1, round to 1
        return 1
    elif num < 10:
        # For numbers less than 10, round to nearest whole number
        return round(num)
    elif num < 100:
        # Round to nearest ten
        return round(num / 10) * 10
    elif num < 1000:
        # Round to nearest hundred
        return round(num / 100) * 100
    else:
        # Round to nearest thousand
        return round(num / 1000) * 1000

def get_place_value_name(num):
    """Get the name of the greatest place value for rounding"""
    if num < 1:
        return "whole number (1)"
    elif num < 10:
        return "whole number"
    elif num < 100:
        return "ten"
    elif num < 1000:
        return "hundred"
    else:
        return "thousand"

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.estimate_product_problem
    
    try:
        user_answer = float(st.session_state.user_product_estimate)
        # Convert to int if it's a whole number
        if user_answer == int(user_answer):
            user_answer = int(user_answer)
        
        # Check if answer is correct
        if user_answer == problem['answer']:
            st.success("🎉 **Excellent! That's the correct estimate!**")
            
            # Show the work
            with st.expander("✅ **See the complete solution**", expanded=True):
                st.markdown("### Step 1: Round each number to its greatest place value")
                
                for i, (num, rounded, place) in enumerate(zip(
                    problem['numbers'], 
                    problem['rounded_numbers'],
                    problem['place_values']
                )):
                    st.markdown(f"- {num} → **{rounded}** (round to nearest {place})")
                
                st.markdown("### Step 2: Multiply the rounded numbers")
                st.markdown(f"{problem['rounded_numbers'][0]} × {problem['rounded_numbers'][1]} = **{problem['answer']}**")
        
        else:
            st.error(f"❌ **Not quite right.** The correct estimate is **{problem['answer']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown("### Let's work through this step by step:")
                
                # Step 1: Show rounding
                st.markdown("**Step 1: Round each number to its greatest place value**")
                
                for num, rounded, place in zip(
                    problem['numbers'], 
                    problem['rounded_numbers'],
                    problem['place_values']
                ):
                    st.markdown(f"- {num} → **{rounded}** (round to nearest {place})")
                    
                    # Explain the rounding
                    if num >= 10:
                        if place == "ten":
                            ones = int(num % 10)
                            if ones >= 5:
                                st.markdown(f"  *(ones digit is {ones}, so round up)*")
                            else:
                                st.markdown(f"  *(ones digit is {ones}, so round down)*")
                        elif place == "hundred":
                            tens = int((num % 100) / 10)
                            if tens >= 5:
                                st.markdown(f"  *(tens digit is {tens}, so round up)*")
                            else:
                                st.markdown(f"  *(tens digit is {tens}, so round down)*")
                
                # Step 2: Show calculation
                st.markdown("\n**Step 2: Multiply the rounded numbers**")
                st.markdown(f"{problem['rounded_numbers'][0]} × {problem['rounded_numbers'][1]} = **{problem['answer']}**")
                
                # Show what user calculated
                if user_answer != problem['answer']:
                    st.markdown(f"\n**Your answer:** {user_answer}")
                    st.markdown("Remember to round to the **greatest place value** before multiplying!")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a valid number.")