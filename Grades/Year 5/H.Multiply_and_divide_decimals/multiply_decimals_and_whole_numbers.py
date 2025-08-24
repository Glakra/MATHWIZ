import streamlit as st
import random

def run():
    """
    Main function to run the Multiply decimals and whole numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/multiply_decimals_and_whole_numbers.py
    """
    # Initialize session state
    if "multiply_decimal_problem" not in st.session_state:
        st.session_state.multiply_decimal_problem = None
        st.session_state.multiply_decimal_answer_submitted = False
        st.session_state.user_multiply_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("✖️ Multiply Decimals and Whole Numbers")
    st.markdown("*Multiply decimal numbers by whole numbers*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.multiply_decimal_problem is None:
        st.session_state.multiply_decimal_problem = generate_problem()
        st.session_state.multiply_decimal_answer_submitted = False
        st.session_state.user_multiply_answer = ""
    
    problem = st.session_state.multiply_decimal_problem
    
    # Display the question
    st.markdown("### 📝 Multiply:")
    
    # Display the problem in vertical format
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: center;
        margin: 40px 0;
    ">
        <div style="
            font-family: 'Courier New', monospace;
            font-size: 28px;
            text-align: right;
            background-color: #f5f5f5;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #ddd;
        ">
            <div style="margin-bottom: 5px;">{problem['decimal']}</div>
            <div style="border-bottom: 3px solid #333; padding-bottom: 5px;">
                × <span style="margin-left: 20px;">{problem['whole']}</span>
            </div>
            <div style="margin-top: 15px;">
                <input type="text" style="
                    width: 150px;
                    height: 40px;
                    font-size: 24px;
                    text-align: right;
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                    padding: 5px 10px;
                    background-color: white;
                " readonly placeholder="?" />
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_multiply_answer,
            key="multiply_answer_input",
            disabled=st.session_state.multiply_decimal_answer_submitted,
            placeholder="Enter your answer",
            label_visibility="collapsed"
        )
        st.session_state.user_multiply_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.multiply_decimal_answer_submitted):
            
            if st.session_state.user_multiply_answer.strip() == "":
                st.warning("⚠️ Please enter your answer.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_multiply_answer)
                    st.session_state.multiply_decimal_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid number.")
    
    # Show feedback if answer was submitted
    if st.session_state.multiply_decimal_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.multiply_decimal_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.multiply_decimal_problem = None
                st.session_state.multiply_decimal_answer_submitted = False
                st.session_state.user_multiply_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Multiply Decimals by Whole Numbers:
        
        **Method 1: Standard Algorithm**
        1. **Multiply** as if there's no decimal point
        2. **Count** decimal places in the decimal number
        3. **Place** the decimal point in your answer
        
        **Method 2: Think of it as repeated addition**
        - 2.5 × 3 = 2.5 + 2.5 + 2.5 = 7.5
        
        ### Examples:
        
        **Example 1:** 8.8 × 6
        ```
            8.8
          ×   6
          -----
           52.8
        ```
        - Multiply: 88 × 6 = 528
        - Count decimals: 8.8 has 1 decimal place
        - Place decimal: 52.8
        
        **Example 2:** 3.45 × 7
        ```
           3.45
         ×    7
         ------
          24.15
        ```
        - Multiply: 345 × 7 = 2415
        - Count decimals: 3.45 has 2 decimal places
        - Place decimal: 24.15
        
        **Example 3:** 0.6 × 4
        ```
            0.6
          ×   4
          -----
            2.4
        ```
        - Multiply: 6 × 4 = 24
        - Count decimals: 0.6 has 1 decimal place
        - Place decimal: 2.4
        
        ### Remember:
        - The number of decimal places in the answer equals the number of decimal places in the decimal factor
        - Check your answer by estimating: 8.8 × 6 ≈ 9 × 6 = 54
        - You can verify by adding: 8.8 + 8.8 + 8.8 + 8.8 + 8.8 + 8.8 = 52.8
        """)

def generate_problem():
    """Generate a random decimal × whole number multiplication problem"""
    # Choose problem difficulty
    problem_types = [
        'one_decimal_small',      # e.g., 2.4 × 3
        'one_decimal_large',      # e.g., 8.7 × 6
        'two_decimals_small',     # e.g., 3.45 × 2
        'two_decimals_large',     # e.g., 7.89 × 4
        'decimal_less_than_one', # e.g., 0.8 × 5
        'three_decimals'         # e.g., 2.345 × 3
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'one_decimal_small':
        # One decimal place, smaller numbers
        decimal = round(random.uniform(1.1, 4.9), 1)
        whole = random.randint(2, 5)
        
    elif problem_type == 'one_decimal_large':
        # One decimal place, larger numbers
        decimal = round(random.uniform(5.1, 9.9), 1)
        whole = random.randint(2, 9)
        
    elif problem_type == 'two_decimals_small':
        # Two decimal places, smaller numbers
        decimal = round(random.uniform(1.01, 4.99), 2)
        whole = random.randint(2, 5)
        
    elif problem_type == 'two_decimals_large':
        # Two decimal places, larger numbers
        decimal = round(random.uniform(5.01, 9.99), 2)
        whole = random.randint(2, 9)
        
    elif problem_type == 'decimal_less_than_one':
        # Decimal less than 1
        decimal = round(random.uniform(0.1, 0.9), random.choice([1, 2]))
        whole = random.randint(2, 9)
        
    else:  # three_decimals
        # Three decimal places
        decimal = round(random.uniform(1.001, 9.999), 3)
        whole = random.randint(2, 5)
    
    # Calculate answer
    answer = round(decimal * whole, len(str(decimal).split('.')[-1]))
    
    # Sometimes swap order for variety
    if random.random() < 0.3:
        return {
            'decimal': whole,  # Actually whole number on top
            'whole': decimal,  # Actually decimal on bottom
            'answer': answer,
            'decimal_places': len(str(decimal).split('.')[-1]) if '.' in str(decimal) else 0
        }
    else:
        return {
            'decimal': decimal,
            'whole': whole,
            'answer': answer,
            'decimal_places': len(str(decimal).split('.')[-1]) if '.' in str(decimal) else 0
        }

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.multiply_decimal_problem
    
    try:
        user_answer = float(st.session_state.user_multiply_answer)
        
        # Check if answer is correct
        if abs(user_answer - problem['answer']) < 0.0001:  # Small tolerance for floating point
            st.success("🎉 **Correct! Great job!**")
            
            # Show the work
            with st.expander("✅ **See the solution**", expanded=True):
                st.markdown(f"### {problem['decimal']} × {problem['whole']} = {problem['answer']}")
                
                # Show the multiplication process
                st.markdown("\n**Step-by-step:**")
                
                # Remove decimal for multiplication
                decimal_str = str(problem['decimal'])
                if '.' in decimal_str:
                    decimal_places = len(decimal_str.split('.')[-1])
                    no_decimal = int(decimal_str.replace('.', ''))
                    
                    st.markdown(f"1. **Ignore the decimal:** {no_decimal} × {problem['whole']}")
                    
                    # Do the multiplication
                    product_no_decimal = no_decimal * problem['whole']
                    st.markdown(f"2. **Multiply:** {no_decimal} × {problem['whole']} = {product_no_decimal}")
                    
                    # Place the decimal
                    st.markdown(f"3. **Count decimal places:** {problem['decimal']} has {decimal_places} decimal place{'s' if decimal_places > 1 else ''}")
                    st.markdown(f"4. **Place the decimal:** {product_no_decimal} → {problem['answer']}")
                else:
                    # Whole number × decimal
                    st.markdown(f"Calculate: {problem['decimal']} × {problem['whole']} = {problem['answer']}")
                
                # Show verification by repeated addition for small whole numbers
                if problem['whole'] <= 5 and problem['whole'] == int(problem['whole']):
                    st.markdown(f"\n**Verify by addition:**")
                    addition_parts = [str(problem['decimal']) for _ in range(int(problem['whole']))]
                    st.markdown(f"{' + '.join(addition_parts)} = {problem['answer']}")
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{problem['answer']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"### {problem['decimal']} × {problem['whole']} = ?")
                
                # Detailed step-by-step
                decimal_str = str(problem['decimal'])
                if '.' in decimal_str:
                    decimal_places = len(decimal_str.split('.')[-1])
                    no_decimal = int(decimal_str.replace('.', ''))
                    
                    st.markdown("\n**Step 1: Multiply without the decimal**")
                    st.markdown(f"Think of {problem['decimal']} as {no_decimal}")
                    st.markdown(f"{no_decimal} × {problem['whole']} = {no_decimal * problem['whole']}")
                    
                    st.markdown(f"\n**Step 2: Count decimal places**")
                    st.markdown(f"{problem['decimal']} has **{decimal_places}** decimal place{'s' if decimal_places > 1 else ''}")
                    
                    st.markdown(f"\n**Step 3: Place the decimal in your answer**")
                    st.markdown(f"Move the decimal point {decimal_places} place{'s' if decimal_places > 1 else ''} from the right")
                    st.markdown(f"{no_decimal * problem['whole']} → **{problem['answer']}**")
                
                st.markdown(f"\n**Your answer:** {user_answer}")
                st.markdown(f"**Correct answer:** {problem['answer']}")
                
                # Common mistakes
                if user_answer == problem['decimal']:
                    st.warning("💡 Remember to multiply! Don't just copy the decimal number.")
                elif abs(user_answer - (problem['decimal'] + problem['whole'])) < 0.0001:
                    st.warning("💡 You added instead of multiplying. Use × not +")
                elif abs(user_answer * 10 - problem['answer']) < 0.0001:
                    st.warning("💡 Check your decimal placement - you're off by one decimal place!")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a valid number.")