import streamlit as st
import random

def run():
    """
    Main function to run the Estimate sums and differences of decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/G. Add and subtract decimals/estimate_sums_and_differences_of_decimals.py
    """
    # Initialize session state
    if "estimate_problem" not in st.session_state:
        st.session_state.estimate_problem = None
        st.session_state.estimate_answer_submitted = False
        st.session_state.user_estimate = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > G. Add and subtract decimals**")
    st.title("🎯 Estimate Sums and Differences of Decimals")
    st.markdown("*Round to the nearest whole number, then calculate*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.estimate_problem is None:
        st.session_state.estimate_problem = generate_problem()
        st.session_state.estimate_answer_submitted = False
        st.session_state.user_estimate = ""
    
    problem = st.session_state.estimate_problem
    
    # Display the question
    if problem['operation'] == 'addition':
        st.markdown("### 📝 Estimate the sum by rounding each number to the nearest whole number and then adding.")
    else:
        st.markdown("### 📝 Estimate the difference by rounding each number to the nearest whole number and then subtracting.")
    
    # Display the expression
    st.markdown(f"<h2 style='text-align: center; color: #1976d2; margin: 30px 0;'>{problem['expression']}</h2>", 
                unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create input with label
        if problem['operation'] == 'addition':
            label_text = "The sum is approximately"
        else:
            label_text = "The difference is approximately"
        
        user_input = st.text_input(
            label_text,
            value=st.session_state.user_estimate,
            key="estimate_input",
            disabled=st.session_state.estimate_answer_submitted,
            placeholder="Enter whole number"
        )
        st.session_state.user_estimate = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.estimate_answer_submitted):
            
            if st.session_state.user_estimate.strip() == "":
                st.warning("⚠️ Please enter your estimate.")
            else:
                try:
                    # Validate the input is a valid integer
                    int(st.session_state.user_estimate)
                    st.session_state.estimate_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a whole number (no decimals).")
    
    # Show feedback if answer was submitted
    if st.session_state.estimate_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.estimate_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.estimate_problem = None
                st.session_state.estimate_answer_submitted = False
                st.session_state.user_estimate = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Estimate:
        1. **Round each decimal** to the nearest whole number
        2. **Add or subtract** the rounded numbers
        3. **Enter your estimate** as a whole number
        
        ### Rounding Rules:
        - **Look at the tenths place** (first digit after decimal)
        - **If it's 5 or more:** Round up
        - **If it's less than 5:** Round down
        
        ### Examples:
        **Addition:**
        - `6.52 + 7.571`
        - Round: 6.52 → 7, and 7.571 → 8
        - Estimate: 7 + 8 = 15
        
        **Subtraction:**
        - `7.6 - 4.9`
        - Round: 7.6 → 8, and 4.9 → 5
        - Estimate: 8 - 5 = 3
        
        ### Why Estimate?
        - **Quick mental math** for shopping
        - **Check if your exact answer** makes sense
        - **Useful in real life** when you need approximate values
        
        ### Remember:
        - We want the **estimate**, not the exact answer
        - Always round **before** calculating
        - Your answer should be a **whole number**
        """)

def generate_problem():
    """Generate a random estimation problem"""
    # Choose operation type
    operation = random.choice(['addition', 'subtraction'])
    
    if operation == 'addition':
        # Decide number of addends (2 or 3)
        num_addends = random.choice([2, 3])
        
        # Generate decimal numbers
        numbers = []
        for _ in range(num_addends):
            # Generate numbers with varying decimal places
            if random.random() < 0.5:
                # One decimal place
                num = round(random.uniform(1.0, 20.0), 1)
            else:
                # Two or three decimal places
                num = round(random.uniform(1.0, 20.0), random.choice([2, 3]))
            numbers.append(num)
        
        # Create expression string
        expression = " + ".join(str(n) for n in numbers)
        
        # Calculate rounded values and answer
        rounded_numbers = [round(n) for n in numbers]
        answer = sum(rounded_numbers)
        
        return {
            'operation': 'addition',
            'numbers': numbers,
            'expression': expression,
            'rounded_numbers': rounded_numbers,
            'answer': answer,
            'explanation': f"Round: {' + '.join(f'{n} → {round(n)}' for n in numbers)}. Then add: {' + '.join(str(r) for r in rounded_numbers)} = {answer}"
        }
    
    else:  # subtraction
        # Generate two numbers where first > second to avoid negative results
        num1 = round(random.uniform(5.0, 20.0), random.choice([1, 2]))
        num2 = round(random.uniform(1.0, min(num1 - 1, 15.0)), random.choice([1, 2]))
        
        # Ensure we don't get negative estimates
        if round(num1) <= round(num2):
            num1 = num2 + random.uniform(2.0, 5.0)
            num1 = round(num1, 1)
        
        expression = f"{num1} - {num2}"
        
        # Calculate rounded values and answer
        rounded1 = round(num1)
        rounded2 = round(num2)
        answer = rounded1 - rounded2
        
        return {
            'operation': 'subtraction',
            'numbers': [num1, num2],
            'expression': expression,
            'rounded_numbers': [rounded1, rounded2],
            'answer': answer,
            'explanation': f"Round: {num1} → {rounded1}, {num2} → {rounded2}. Then subtract: {rounded1} - {rounded2} = {answer}"
        }

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.estimate_problem
    
    try:
        user_answer = int(st.session_state.user_estimate)
        
        # Check if answer is correct
        if user_answer == problem['answer']:
            st.success("🎉 **Excellent! That's the correct estimate!**")
            
            # Show the work
            with st.expander("✅ **See the complete solution**", expanded=True):
                st.markdown("### Step 1: Round each number")
                for i, (num, rounded) in enumerate(zip(problem['numbers'], problem['rounded_numbers'])):
                    st.markdown(f"- {num} → **{rounded}**")
                
                st.markdown("### Step 2: Calculate with rounded numbers")
                if problem['operation'] == 'addition':
                    calculation = " + ".join(str(r) for r in problem['rounded_numbers'])
                else:
                    calculation = f"{problem['rounded_numbers'][0]} - {problem['rounded_numbers'][1]}"
                
                st.markdown(f"{calculation} = **{problem['answer']}**")
        
        else:
            st.error(f"❌ **Not quite right.** The correct estimate is **{problem['answer']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown("### Let's work through this step by step:")
                
                # Step 1: Show rounding
                st.markdown("**Step 1: Round each number to the nearest whole number**")
                for num, rounded in zip(problem['numbers'], problem['rounded_numbers']):
                    tenths = int((num * 10) % 10)
                    if tenths >= 5:
                        st.markdown(f"- {num} → {rounded} (tenths place is {tenths}, so round up)")
                    else:
                        st.markdown(f"- {num} → {rounded} (tenths place is {tenths}, so round down)")
                
                # Step 2: Show calculation
                st.markdown("\n**Step 2: Calculate with the rounded numbers**")
                if problem['operation'] == 'addition':
                    calculation = " + ".join(str(r) for r in problem['rounded_numbers'])
                else:
                    calculation = f"{problem['rounded_numbers'][0]} - {problem['rounded_numbers'][1]}"
                
                st.markdown(f"{calculation} = **{problem['answer']}**")
                
                # Show what user calculated
                if user_answer != problem['answer']:
                    st.markdown(f"\n**Your answer:** {user_answer}")
                    st.markdown("Remember to round each number **before** calculating!")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a whole number.")

def round_to_nearest(num):
    """Round a number to the nearest integer"""
    return round(num)