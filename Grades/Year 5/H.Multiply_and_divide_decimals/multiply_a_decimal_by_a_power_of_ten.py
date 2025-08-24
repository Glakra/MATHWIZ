import streamlit as st
import random

def run():
    """
    Main function to run the Multiply a decimal by a power of ten activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/multiply_a_decimal_by_a_power_of_ten.py
    """
    # Initialize session state
    if "power_of_ten_problem" not in st.session_state:
        st.session_state.power_of_ten_problem = None
        st.session_state.power_of_ten_answer_submitted = False
        st.session_state.user_power_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("✖️ Multiply a Decimal by a Power of Ten")
    st.markdown("*Multiply decimals by 10, 100, or 1000*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.power_of_ten_problem is None:
        st.session_state.power_of_ten_problem = generate_problem()
        st.session_state.power_of_ten_answer_submitted = False
        st.session_state.user_power_answer = ""
    
    problem = st.session_state.power_of_ten_problem
    
    # Display the question
    st.markdown("### 📝 Multiply:")
    
    # Display the problem based on format
    if problem['format'] == 'vertical':
        # Vertical format
        st.markdown(f"""
        <div style="
            text-align: center;
            font-family: 'Courier New', monospace;
            font-size: 24px;
            margin: 30px 0;
        ">
            <div style="text-align: right; width: 150px; margin: 0 auto;">
                <div>{problem['decimal']}</div>
                <div style="border-bottom: 2px solid #333; margin: 5px 0;">× {problem['power']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Horizontal format
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 28px;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
        ">
            {problem['expression']}
        </div>
        """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_power_answer,
            key="power_answer_input",
            disabled=st.session_state.power_of_ten_answer_submitted,
            placeholder="Enter your answer",
            label_visibility="collapsed"
        )
        st.session_state.user_power_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.power_of_ten_answer_submitted):
            
            if st.session_state.user_power_answer.strip() == "":
                st.warning("⚠️ Please enter your answer.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_power_answer)
                    st.session_state.power_of_ten_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid number.")
    
    # Show feedback if answer was submitted
    if st.session_state.power_of_ten_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.power_of_ten_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.power_of_ten_problem = None
                st.session_state.power_of_ten_answer_submitted = False
                st.session_state.user_power_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Multiplying by Powers of 10:
        
        **Key Rule:** Move the decimal point to the RIGHT
        - × 10 → Move decimal 1 place right
        - × 100 → Move decimal 2 places right
        - × 1000 → Move decimal 3 places right
        
        ### Examples:
        
        **Multiply by 10:**
        - 0.5 × 10 = 5
        - 3.42 × 10 = 34.2
        - 0.067 × 10 = 0.67
        
        **Multiply by 100:**
        - 0.5 × 100 = 50
        - 3.42 × 100 = 342
        - 0.067 × 100 = 6.7
        
        **Multiply by 1000:**
        - 0.5 × 1000 = 500
        - 3.42 × 1000 = 3420
        - 0.067 × 1000 = 67
        
        ### Step by Step:
        1. **Count the zeros** in the power of 10
        2. **Move the decimal point** that many places to the right
        3. **Add zeros if needed** when you run out of digits
        
        ### Visual Example:
        ```
        0.89 × 100
        Step 1: 100 has 2 zeros
        Step 2: Move decimal 2 places right
        0.89 → 08.9 → 89.
        Answer: 89
        ```
        
        ### Remember:
        - The number gets BIGGER when multiplying by powers of 10
        - If you run out of digits, add zeros
        - You can drop the decimal point if there are no decimals left (89. = 89)
        """)

def generate_problem():
    """Generate a random multiplication by power of ten problem"""
    # Choose power of ten
    powers = [10, 100, 1000]
    power = random.choice(powers)
    
    # Choose decimal type
    decimal_types = [
        'one_decimal',      # e.g., 0.5, 3.7
        'two_decimals',     # e.g., 0.22, 4.56
        'three_decimals',   # e.g., 0.123, 2.345
        'small_decimal'     # e.g., 0.05, 0.007
    ]
    
    decimal_type = random.choice(decimal_types)
    
    if decimal_type == 'one_decimal':
        decimal = round(random.uniform(0.1, 9.9), 1)
    elif decimal_type == 'two_decimals':
        decimal = round(random.uniform(0.01, 9.99), 2)
    elif decimal_type == 'three_decimals':
        decimal = round(random.uniform(0.001, 9.999), 3)
    else:  # small_decimal
        # Generate small decimals like 0.05, 0.007
        if random.random() < 0.5:
            decimal = round(random.uniform(0.01, 0.09), 2)
        else:
            decimal = round(random.uniform(0.001, 0.009), 3)
    
    # Choose format
    format_type = random.choice(['vertical', 'horizontal'])
    
    # Calculate answer
    answer = decimal * power
    # Clean up answer (remove trailing zeros after decimal)
    if answer == int(answer):
        answer = int(answer)
    
    # Create expression for horizontal format
    if random.random() < 0.5:
        expression = f"{power} × {decimal} = ?"
    else:
        expression = f"{decimal} × {power} = ?"
    
    return {
        'decimal': decimal,
        'power': power,
        'answer': answer,
        'format': format_type,
        'expression': expression if format_type == 'horizontal' else None,
        'decimal_places': len(str(decimal).split('.')[-1]) if '.' in str(decimal) else 0
    }

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.power_of_ten_problem
    
    try:
        user_answer = float(st.session_state.user_power_answer)
        # Convert to int if it's a whole number
        if user_answer == int(user_answer):
            user_answer = int(user_answer)
        
        # Check if answer is correct
        if user_answer == problem['answer']:
            st.success("🎉 **Correct! Excellent work!**")
            
            # Show the work
            with st.expander("✅ **See how it works**", expanded=True):
                st.markdown(f"### {problem['decimal']} × {problem['power']} = {problem['answer']}")
                
                # Count zeros in power of 10
                zero_count = len(str(problem['power'])) - 1
                st.markdown(f"\n**Step 1:** Count the zeros in {problem['power']}")
                st.markdown(f"→ {problem['power']} has **{zero_count} zero{'s' if zero_count > 1 else ''}**")
                
                st.markdown(f"\n**Step 2:** Move the decimal point {zero_count} place{'s' if zero_count > 1 else ''} to the right")
                
                # Show decimal movement
                decimal_str = str(problem['decimal'])
                if '.' in decimal_str:
                    parts = decimal_str.split('.')
                    whole = parts[0]
                    decimal_part = parts[1]
                    
                    # Show step by step movement
                    st.markdown(f"→ {decimal_str}")
                    
                    # Move decimal point
                    for i in range(zero_count):
                        if i < len(decimal_part):
                            whole += decimal_part[i]
                            remaining = decimal_part[i+1:]
                            if remaining:
                                st.markdown(f"→ {whole}.{remaining}")
                            else:
                                st.markdown(f"→ {whole}")
                        else:
                            whole += "0"
                            st.markdown(f"→ {whole}")
                
                st.markdown(f"\n**Answer:** {problem['answer']}")
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{problem['answer']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"### {problem['decimal']} × {problem['power']} = ?")
                
                # Count zeros
                zero_count = len(str(problem['power'])) - 1
                st.markdown(f"\n**Rule:** When multiplying by {problem['power']}, move the decimal point {zero_count} place{'s' if zero_count > 1 else ''} to the right.")
                
                # Show the process
                st.markdown("\n**Step-by-step:**")
                decimal_str = str(problem['decimal'])
                
                # Visual representation
                st.markdown(f"1. Start with: **{decimal_str}**")
                st.markdown(f"2. Move decimal {zero_count} place{'s' if zero_count > 1 else ''} right")
                
                # Show movement
                if '.' in decimal_str:
                    result_str = decimal_str.replace('.', '')
                    decimal_pos = decimal_str.index('.')
                    new_pos = decimal_pos + zero_count
                    
                    # Add zeros if needed
                    while len(result_str) < new_pos:
                        result_str += '0'
                    
                    # Insert decimal if needed
                    if new_pos < len(result_str):
                        result_str = result_str[:new_pos] + '.' + result_str[new_pos:]
                    
                    # Clean up
                    if result_str.endswith('.'):
                        result_str = result_str[:-1]
                    if '.' in result_str:
                        result_str = result_str.rstrip('0').rstrip('.')
                    
                    st.markdown(f"3. Result: **{result_str}**")
                
                st.markdown(f"\n**Correct answer:** {problem['answer']}")
                st.markdown(f"**Your answer:** {user_answer}")
                
                # Common mistake hints
                if user_answer == problem['decimal']:
                    st.warning("💡 Remember to multiply! Don't just copy the decimal.")
                elif user_answer == problem['decimal'] * (problem['power'] / 10):
                    st.warning("💡 Check your decimal movement - you might be one place off!")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a valid number.")