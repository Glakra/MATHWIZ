import streamlit as st
import random
from fractions import Fraction
from math import floor

def run():
    """
    Main function for Add and subtract money amounts activity.
    Uses Python's Fraction for exact decimal arithmetic.
    """
    # Initialize session state
    if "money_difficulty" not in st.session_state:
        st.session_state.money_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("💰 Add and Subtract Money Amounts")
    st.markdown("*Practice adding and subtracting money with regrouping*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.money_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (no regrouping)",
            2: "Medium (with regrouping)", 
            3: "Advanced (large amounts)"
        }
        st.markdown(f"**Current Level:** {difficulty_text[difficulty_level]}")
        progress = (difficulty_level - 1) / 2
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
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
        generate_new_problem()
    
    # Display the problem
    display_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Enter each digit** in the boxes provided
        - **Work from right to left** (start with cents)
        - **Remember regrouping** when needed
        
        ### Money Rules:
        - **100 cents = $1.00**
        - **Regroup when cents ≥ 10**
        - **Borrow $1 = 100 cents** when subtracting
        
        ### Tips:
        - **Line up decimal points** vertically
        - **Add/subtract cents first**, then dollars
        - **Check your work** by estimation
        
        ### Difficulty Levels:
        - **🟢 Easy:** No regrouping needed
        - **🟡 Medium:** Regrouping required
        - **🔴 Hard:** Large amounts with multiple regroupings
        """)

def generate_new_problem():
    """Generate a new money problem"""
    difficulty = st.session_state.money_difficulty
    
    if difficulty == 1:  # Easy - no regrouping
        if random.choice([True, False]):  # Addition
            # Generate amounts that won't require regrouping
            dollars1 = random.randint(1, 20)
            cents1 = random.randint(0, 49)
            dollars2 = random.randint(1, 20)
            cents2 = random.randint(0, 50 - cents1)  # Ensure no regrouping
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "add"
        else:  # Subtraction
            # Ensure no borrowing needed
            dollars1 = random.randint(10, 30)
            cents1 = random.randint(50, 99)
            dollars2 = random.randint(1, dollars1 - 1)
            cents2 = random.randint(0, cents1)
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "subtract"
    
    elif difficulty == 2:  # Medium - with regrouping
        if random.choice([True, False]):  # Addition
            # Generate amounts that will require regrouping
            dollars1 = random.randint(10, 50)
            cents1 = random.randint(60, 99)
            dollars2 = random.randint(10, 50)
            cents2 = random.randint(60, 99)
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "add"
        else:  # Subtraction with borrowing
            dollars1 = random.randint(20, 60)
            cents1 = random.randint(0, 40)
            dollars2 = random.randint(5, dollars1 - 5)
            cents2 = random.randint(cents1 + 10, 99)
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "subtract"
    
    else:  # Hard - large amounts
        if random.choice([True, False]):  # Addition
            dollars1 = random.randint(100, 500)
            cents1 = random.randint(0, 99)
            dollars2 = random.randint(100, 500)
            cents2 = random.randint(0, 99)
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "add"
        else:  # Subtraction
            dollars1 = random.randint(200, 800)
            cents1 = random.randint(0, 99)
            dollars2 = random.randint(50, min(dollars1 - 10, 400))
            cents2 = random.randint(0, 99)
            
            amount1 = dollars1 + cents1 / 100
            amount2 = dollars2 + cents2 / 100
            operation = "subtract"
    
    # Calculate exact result
    if operation == "add":
        result = amount1 + amount2
    else:
        result = amount1 - amount2
    
    # Convert to dollars and cents for display
    result_dollars = int(result)
    result_cents = round((result - result_dollars) * 100)
    
    # Extract components
    amount1_dollars = int(amount1)
    amount1_cents = round((amount1 - amount1_dollars) * 100)
    amount2_dollars = int(amount2)
    amount2_cents = round((amount2 - amount2_dollars) * 100)
    
    st.session_state.problem_data = {
        'amount1': amount1,
        'amount2': amount2,
        'operation': operation,
        'result': result,
        'result_dollars': result_dollars,
        'result_cents': result_cents,
        'amount1_dollars': amount1_dollars,
        'amount1_cents': amount1_cents,
        'amount2_dollars': amount2_dollars,
        'amount2_cents': amount2_cents
    }
    st.session_state.current_problem = f"{'Add' if operation == 'add' else 'Subtract'} these money amounts:"

def display_problem():
    """Display the money problem with interactive digit boxes"""
    data = st.session_state.problem_data
    
    st.markdown(f"### {st.session_state.current_problem}")
    
    # Create the visual problem layout
    operation_symbol = "+" if data['operation'] == 'add' else "-"
    
    # Format amounts with proper spacing
    amount1_str = f"${data['amount1_dollars']}.{data['amount1_cents']:02d}"
    amount2_str = f"${data['amount2_dollars']}.{data['amount2_cents']:02d}"
    
    # Create columns for alignment
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Display the problem
        st.markdown(f"""
        <div style="font-family: monospace; font-size: 28px; text-align: right; margin: 20px 0;">
            <div style="margin-bottom: 10px;">&nbsp;&nbsp;{amount1_str}</div>
            <div style="margin-bottom: 10px;">{operation_symbol} {amount2_str}</div>
            <div style="border-top: 3px solid black; margin-top: 10px; padding-top: 10px;">
                $ <span id="answer-display"></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create input boxes for the answer
        st.markdown("### Enter your answer:")
        
        # Determine number of dollar digits needed
        max_dollars = max(data['result_dollars'], 999)  # At least 3 digits
        num_dollar_digits = len(str(max_dollars))
        
        # Create the input grid
        total_cols = num_dollar_digits + 3  # +3 for $, decimal point and 2 cent digits
        cols = st.columns(total_cols)
        
        # Dollar sign
        with cols[0]:
            st.markdown("**$**", help="Dollar sign")
        
        # Dollar digits
        for i in range(1, num_dollar_digits):
            with cols[i]:
                digit = st.text_input(
                    f"Dollar digit {i}",
                    max_chars=1,
                    key=f"dollar_{i-1}",
                    placeholder="0",
                    label_visibility="collapsed"
                )
                if digit and not digit.isdigit():
                    st.error("Numbers only!")
                st.session_state.user_answers[f"dollar_{i-1}"] = digit
        
        # Decimal point
        with cols[num_dollar_digits]:
            st.markdown("**.**", help="Decimal point")
        
        # Cent digits (always 2)
        for i in range(2):
            with cols[num_dollar_digits + 1 + i]:
                digit = st.text_input(
                    f"Cent digit {i}",
                    max_chars=1,
                    key=f"cent_{i}",
                    placeholder="0",
                    label_visibility="collapsed"
                )
                if digit and not digit.isdigit():
                    st.error("Numbers only!")
                st.session_state.user_answers[f"cent_{i}"] = digit
        
        # Submit button
        st.markdown("")
        if st.button("✅ Submit Answer", type="primary", use_container_width=True):
            check_answer()
        
        # Show feedback
        if st.session_state.show_feedback:
            show_feedback()
        
        # Next question button
        if st.session_state.answer_submitted:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def check_answer():
    """Check the user's answer"""
    data = st.session_state.problem_data
    
    # Collect user's answer
    try:
        # Get dollar digits
        num_dollar_digits = len(str(max(data['result_dollars'], 999))) - 1
        dollar_str = ""
        for i in range(num_dollar_digits):
            digit = st.session_state.user_answers.get(f"dollar_{i}", "0")
            if not digit:
                digit = "0"
            dollar_str += digit
        
        # Get cent digits
        cent_str = ""
        for i in range(2):
            digit = st.session_state.user_answers.get(f"cent_{i}", "0")
            if not digit:
                digit = "0"
            cent_str += digit
        
        # Convert to number
        user_dollars = int(dollar_str) if dollar_str else 0
        user_cents = int(cent_str) if cent_str else 0
        user_answer = user_dollars + user_cents / 100
        
    except:
        st.error("Please enter valid numbers!")
        return
    
    # Check if correct (with small tolerance for floating point)
    correct = abs(user_answer - data['result']) < 0.001
    
    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True
    st.session_state.user_correct = correct
    
    # Update difficulty
    if correct:
        st.session_state.consecutive_correct += 1
        if st.session_state.consecutive_correct >= 3:
            st.session_state.money_difficulty = min(st.session_state.money_difficulty + 1, 3)
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        if st.session_state.money_difficulty > 1:
            st.session_state.money_difficulty -= 1

def show_feedback():
    """Display feedback"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.money_difficulty < 3:
            st.info("⬆️ **Level up! Problems are getting harder.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is ${data['result_dollars']}.{data['result_cents']:02d}**")
        
        # Show step-by-step solution
        with st.expander("📖 **See the solution**", expanded=True):
            st.markdown("### Step-by-step solution:")
            
            if data['operation'] == 'add':
                st.markdown(f"""
                **Step 1: Add the cents**
                - {data['amount1_cents']} cents + {data['amount2_cents']} cents = {data['amount1_cents'] + data['amount2_cents']} cents
                """)
                
                total_cents = data['amount1_cents'] + data['amount2_cents']
                if total_cents >= 100:
                    st.markdown(f"""
                **Step 2: Regroup cents to dollars**
                - {total_cents} cents = {total_cents // 100} dollar(s) and {total_cents % 100} cents
                """)
                    
                    st.markdown(f"""
                **Step 3: Add the dollars (including regrouped)**
                - ${data['amount1_dollars']} + ${data['amount2_dollars']} + ${total_cents // 100} = ${data['result_dollars']}
                """)
                else:
                    st.markdown(f"""
                **Step 2: Add the dollars**
                - ${data['amount1_dollars']} + ${data['amount2_dollars']} = ${data['result_dollars']}
                """)
                
            else:  # Subtraction
                if data['amount1_cents'] < data['amount2_cents']:
                    st.markdown(f"""
                **Step 1: Borrow from dollars**
                - Can't subtract {data['amount2_cents']} cents from {data['amount1_cents']} cents
                - Borrow $1 = 100 cents
                - {data['amount1_cents']} + 100 = {data['amount1_cents'] + 100} cents
                """)
                    
                    st.markdown(f"""
                **Step 2: Subtract cents**
                - {data['amount1_cents'] + 100} cents - {data['amount2_cents']} cents = {data['result_cents']} cents
                """)
                    
                    st.markdown(f"""
                **Step 3: Subtract dollars (remember we borrowed 1)**
                - ${data['amount1_dollars'] - 1} - ${data['amount2_dollars']} = ${data['result_dollars']}
                """)
                else:
                    st.markdown(f"""
                **Step 1: Subtract cents**
                - {data['amount1_cents']} cents - {data['amount2_cents']} cents = {data['result_cents']} cents
                """)
                    
                    st.markdown(f"""
                **Step 2: Subtract dollars**
                - ${data['amount1_dollars']} - ${data['amount2_dollars']} = ${data['result_dollars']}
                """)
            
            st.markdown(f"""
            **Final answer: ${data['result_dollars']}.{data['result_cents']:02d}**
            """)

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}