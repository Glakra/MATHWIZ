import streamlit as st
import random

def run():
    """
    Main function to run the Divide by powers of ten activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/divide_by_powers_of_ten.py
    """
    # Initialize session state
    if "divide_power_problem" not in st.session_state:
        st.session_state.divide_power_problem = None
        st.session_state.divide_power_submitted = False
        st.session_state.user_divide_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("➗ Divide by Powers of Ten")
    st.markdown("*Divide by 10, 100, or 1000*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.divide_power_problem is None:
        st.session_state.divide_power_problem = generate_problem()
        st.session_state.divide_power_submitted = False
        st.session_state.user_divide_answer = ""
    
    problem = st.session_state.divide_power_problem
    
    # Display the question
    st.markdown("### 📝 Divide:")
    
    # Display the problem based on format
    if problem['format'] == 'horizontal':
        # Horizontal format
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 32px;
            margin: 40px 0;
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            padding: 30px;
            border-radius: 10px;
        ">
            {problem['expression']}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Vertical format (long division)
        display_vertical_division(problem)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_divide_answer,
            key="divide_answer_input",
            disabled=st.session_state.divide_power_submitted,
            placeholder="Enter your answer",
            label_visibility="collapsed"
        )
        st.session_state.user_divide_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.divide_power_submitted):
            
            if st.session_state.user_divide_answer.strip() == "":
                st.warning("⚠️ Please enter your answer.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_divide_answer)
                    st.session_state.divide_power_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid number.")
    
    # Show feedback if answer was submitted
    if st.session_state.divide_power_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.divide_power_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.divide_power_problem = None
                st.session_state.divide_power_submitted = False
                st.session_state.user_divide_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Dividing by Powers of 10:
        
        **Key Rule:** Move the decimal point to the LEFT
        - ÷ 10 → Move decimal 1 place left
        - ÷ 100 → Move decimal 2 places left
        - ÷ 1000 → Move decimal 3 places left
        
        ### Examples:
        
        **Divide by 10:**
        - 50 ÷ 10 = 5
        - 8 ÷ 10 = 0.8
        - 345 ÷ 10 = 34.5
        - 0.6 ÷ 10 = 0.06
        
        **Divide by 100:**
        - 900 ÷ 100 = 9
        - 45 ÷ 100 = 0.45
        - 7 ÷ 100 = 0.07
        - 2,340 ÷ 100 = 23.4
        
        **Divide by 1000:**
        - 5000 ÷ 1000 = 5
        - 250 ÷ 1000 = 0.25
        - 8 ÷ 1000 = 0.008
        - 45,600 ÷ 1000 = 45.6
        
        ### Step by Step:
        1. **Count the zeros** in the power of 10
        2. **Move the decimal point** that many places to the left
        3. **Add zeros if needed** after the decimal point
        
        ### Visual Example:
        ```
        345 ÷ 100
        Step 1: 100 has 2 zeros
        Step 2: Move decimal 2 places left
        345. → 34.5 → 3.45
        Answer: 3.45
        ```
        
        ### Remember:
        - The number gets SMALLER when dividing by powers of 10
        - Always move decimal LEFT (opposite of multiplication)
        - Add zeros after decimal point if needed (0.08, 0.007)
        """)

def generate_problem():
    """Generate a random division by power of ten problem"""
    # Choose power of ten
    powers = [10, 100, 1000]
    power = random.choice(powers)
    
    # Choose dividend type
    dividend_types = [
        'whole_small',      # e.g., 9, 45
        'whole_medium',     # e.g., 234, 567
        'whole_large',      # e.g., 2345, 8900
        'decimal',          # e.g., 23.5, 456.78
        'special'           # Nice round numbers that divide evenly
    ]
    
    dividend_type = random.choice(dividend_types)
    
    if dividend_type == 'whole_small':
        dividend = random.randint(1, 99)
    elif dividend_type == 'whole_medium':
        dividend = random.randint(100, 999)
    elif dividend_type == 'whole_large':
        dividend = random.randint(1000, 9999)
    elif dividend_type == 'decimal':
        # Generate decimals
        if random.random() < 0.5:
            dividend = round(random.uniform(10, 999), random.choice([1, 2]))
        else:
            dividend = round(random.uniform(0.1, 9.9), random.choice([1, 2]))
    else:  # special - numbers that divide evenly
        if power == 10:
            dividend = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200])
        elif power == 100:
            dividend = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500])
        else:  # 1000
            dividend = random.choice([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000])
    
    # Choose format
    format_type = random.choice(['horizontal', 'vertical'])
    
    # Calculate answer
    answer = dividend / power
    
    # Format answer nicely (remove unnecessary trailing zeros)
    if answer == int(answer):
        answer = int(answer)
    else:
        # Round to avoid floating point issues
        answer = round(answer, 10)  # High precision first
        # Convert to string and back to remove trailing zeros
        answer_str = f"{answer:.10f}".rstrip('0').rstrip('.')
        answer = float(answer_str)
    
    return {
        'dividend': dividend,
        'divisor': power,
        'answer': answer,
        'format': format_type,
        'expression': f"{dividend} ÷ {power} = ?"
    }

def display_vertical_division(problem):
    """Display division in vertical format"""
    dividend_str = str(problem['dividend'])
    divisor_str = str(problem['divisor'])
    
    # Create the long division display
    division_html = f"""
    <div style="
        display: flex;
        justify-content: center;
        margin: 40px 0;
    ">
        <div style="
            font-family: 'Courier New', monospace;
            font-size: 28px;
            text-align: left;
            background-color: #f5f5f5;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #ddd;
        ">
            <div style="position: relative;">
                <div style="
                    position: absolute;
                    left: -10px;
                    top: 15px;
                    padding-right: 15px;
                ">{divisor_str}</div>
                <div style="
                    border-left: 3px solid #333;
                    border-top: 3px solid #333;
                    padding-left: 20px;
                    padding-top: 5px;
                    margin-left: {len(divisor_str) * 15 + 10}px;
                    min-width: {max(100, len(dividend_str) * 20)}px;
                ">{dividend_str}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(division_html, unsafe_allow_html=True)

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.divide_power_problem
    
    try:
        user_answer = float(st.session_state.user_divide_answer)
        
        # Check if answer is correct (with small tolerance for floating point)
        if abs(user_answer - problem['answer']) < 0.0001:
            st.success("🎉 **Correct! Excellent work!**")
            
            # Show the work
            with st.expander("✅ **See how it works**", expanded=True):
                st.markdown(f"### {problem['dividend']} ÷ {problem['divisor']} = {problem['answer']}")
                
                # Count zeros in power of 10
                zero_count = len(str(problem['divisor'])) - 1
                st.markdown(f"\n**Step 1:** Count the zeros in {problem['divisor']}")
                st.markdown(f"→ {problem['divisor']} has **{zero_count} zero{'s' if zero_count > 1 else ''}**")
                
                st.markdown(f"\n**Step 2:** Move the decimal point {zero_count} place{'s' if zero_count > 1 else ''} to the left")
                
                # Show decimal movement
                dividend_str = str(problem['dividend'])
                if '.' not in dividend_str:
                    dividend_str += '.'
                
                # Show step by step movement
                st.markdown(f"→ Start: {dividend_str}")
                
                # Calculate decimal position
                decimal_pos = dividend_str.index('.')
                new_decimal_pos = decimal_pos - zero_count
                
                # Show the movement
                if new_decimal_pos <= 0:
                    # Need to add zeros after decimal point
                    zeros_needed = abs(new_decimal_pos)
                    result = "0." + "0" * zeros_needed + dividend_str.replace('.', '')
                    st.markdown(f"→ Add zeros: {result}")
                else:
                    # Just move decimal
                    digits = dividend_str.replace('.', '')
                    result = digits[:new_decimal_pos] + '.' + digits[new_decimal_pos:]
                    st.markdown(f"→ Result: {result}")
                
                # Clean up result
                result = result.rstrip('0').rstrip('.') if '.' in result else result
                st.markdown(f"\n**Answer:** {problem['answer']}")
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{problem['answer']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"### {problem['dividend']} ÷ {problem['divisor']} = ?")
                
                # Count zeros
                zero_count = len(str(problem['divisor'])) - 1
                st.markdown(f"\n**Rule:** When dividing by {problem['divisor']}, move the decimal point {zero_count} place{'s' if zero_count > 1 else ''} to the left.")
                
                # Show the process
                st.markdown("\n**Step-by-step:**")
                st.markdown(f"1. Start with: **{problem['dividend']}**")
                st.markdown(f"2. Move decimal {zero_count} place{'s' if zero_count > 1 else ''} left")
                
                # Show visual representation
                dividend_str = str(problem['dividend'])
                if '.' not in dividend_str:
                    st.markdown(f"   - Think of {problem['dividend']} as {problem['dividend']}.0")
                
                st.markdown(f"3. Result: **{problem['answer']}**")
                
                st.markdown(f"\n**Correct answer:** {problem['answer']}")
                st.markdown(f"**Your answer:** {user_answer}")
                
                # Common mistake hints
                if abs(user_answer - problem['dividend'] * problem['divisor']) < 0.1:
                    st.warning("💡 You multiplied instead of dividing!")
                elif abs(user_answer - problem['dividend']) < 0.0001:
                    st.warning("💡 Remember to divide! Don't just copy the number.")
                elif abs(user_answer * 10 - problem['answer']) < 0.0001 or abs(user_answer / 10 - problem['answer']) < 0.0001:
                    st.warning("💡 Check your decimal movement - you might be one place off!")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a valid number.")