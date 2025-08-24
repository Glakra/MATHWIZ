import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Sums and Differences practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/estimate_sums_and_differences_of_whole_numbers.py
    """
    # Initialize session state
    if "estimation_difficulty" not in st.session_state:
        st.session_state.estimation_difficulty = {"round_to": 100000}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.question_count = 0
        st.session_state.correct_count = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("📏 Estimate Sums and Differences")
    st.markdown("*Practice rounding numbers and estimating answers*")
    st.markdown("---")
    
    # Difficulty indicator
    round_to = st.session_state.estimation_difficulty["round_to"]
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Rounding:** Nearest {round_to:,}")
        if st.session_state.question_count > 0:
            accuracy = (st.session_state.correct_count / st.session_state.question_count) * 100
            st.markdown(f"**Score:** {st.session_state.correct_count}/{st.session_state.question_count} ({accuracy:.0f}%)")
        else:
            st.markdown("**Score:** Starting...")
    
    with col2:
        if round_to >= 100000:
            st.markdown("**🔴 Advanced**")
        elif round_to >= 10000:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🟡 Beginner**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Learn About Estimation and Rounding**", expanded=False):
        st.markdown("""
        ### 📏 What is Estimation?
        
        **Estimation** is finding an approximate answer that's close to the exact answer but easier to calculate. It's like making a "smart guess" using math rules!
        
        ### 🎯 Why Do We Estimate?
        - **Quick calculations:** Get answers fast without exact math
        - **Check our work:** See if exact answers make sense
        - **Real-world problems:** Often we don't need perfect precision
        - **Mental math:** Calculate in your head more easily
        
        ### 📐 How Rounding Works:
        
        #### **Rounding to the Nearest 10:**
        - Look at the **ones digit**
        - If 5 or higher → round UP
        - If 4 or lower → round DOWN
        - Example: 247 → 250, but 243 → 240
        
        #### **Rounding to the Nearest 100:**
        - Look at the **tens digit**
        - If 5 or higher → round UP
        - If 4 or lower → round DOWN  
        - Example: 1,670 → 1,700, but 1,630 → 1,600
        
        #### **Rounding to the Nearest 1,000:**
        - Look at the **hundreds digit**
        - If 5 or higher → round UP
        - If 4 or lower → round DOWN
        - Example: 45,800 → 46,000, but 45,200 → 45,000
        
        #### **Rounding to the Nearest 10,000:**
        - Look at the **thousands digit**
        - If 5 or higher → round UP
        - If 4 or lower → round DOWN
        - Example: 167,000 → 170,000, but 163,000 → 160,000
        
        #### **Rounding to the Nearest 100,000:**
        - Look at the **ten-thousands digit**
        - If 5 or higher → round UP
        - If 4 or lower → round DOWN
        - Example: 875,000 → 900,000, but 825,000 → 800,000
        
        ### 🧮 **Estimation Steps:**
        
        1. **Round each number** to the specified place value
        2. **Perform the operation** (+ or −) with the rounded numbers
        3. **Check if your answer makes sense** (is it reasonable?)
        
        ### 💭 **Example Walkthrough:**
        
        **Problem:** Estimate 143,678 + 289,543 to the nearest 10,000
        
        **Step 1:** Round each number
        - 143,678 → Look at thousands digit (3) → Round down to 140,000
        - 289,543 → Look at thousands digit (9) → Round up to 290,000
        
        **Step 2:** Add the rounded numbers
        - 140,000 + 290,000 = 430,000
        
        **Step 3:** Check reasonableness
        - Original numbers were about 140k and 290k
        - 430,000 makes sense as an estimate!
        
        ### 🎯 **Tips for Success:**
        
        - **Identify the place value** you're rounding to
        - **Look at the digit to the right** of that place value
        - **Remember the 5 rule:** 5 or higher rounds up, 4 or lower rounds down
        - **Think logically:** Does your estimate seem reasonable?
        - **Practice mental math:** Try to do the rounding in your head
        
        ### 📊 **Common Rounding Mistakes:**
        
        - **Wrong digit:** Looking at the wrong place value digit
        - **Forget to round both:** Only rounding one of the numbers
        - **Calculation errors:** Making mistakes with the rounded numbers
        - **Place value confusion:** Not understanding which digit to look at
        
        ### 🎲 **Real-World Applications:**
        
        - **Shopping:** Estimating total costs at the store
        - **Time:** Estimating how long trips will take
        - **Sports:** Estimating scores and statistics
        - **Science:** Making quick calculations in experiments
        """)

def generate_new_question():
    """Generate a new estimation question"""
    
    # Generate two large numbers
    num1 = random.randint(10000, 999999)
    num2 = random.randint(10000, 999999)
    
    # Choose operation
    operation = random.choice(["+", "-"])
    
    # Get current rounding target
    round_to = st.session_state.estimation_difficulty["round_to"]
    
    # Round both numbers
    rounded_num1 = round(num1 / round_to) * round_to
    rounded_num2 = round(num2 / round_to) * round_to
    
    # Calculate the estimated answer
    if operation == "+":
        answer = rounded_num1 + rounded_num2
        operation_name = "sum"
    else:
        # Make sure subtraction doesn't go negative
        if rounded_num1 < rounded_num2:
            rounded_num1, rounded_num2 = rounded_num2, rounded_num1
            num1, num2 = num2, num1
        answer = rounded_num1 - rounded_num2
        operation_name = "difference"
    
    st.session_state.problem_data = {
        "num1": num1,
        "num2": num2,
        "rounded_num1": rounded_num1,
        "rounded_num2": rounded_num2,
        "operation": operation,
        "operation_name": operation_name,
        "round_to": round_to,
        "answer": answer
    }
    
    st.session_state.correct_answer = str(int(answer))
    st.session_state.current_question = f"Estimate the {operation_name} by rounding each number to the nearest {round_to:,} and then calculating."

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### 📏 Estimation Challenge:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the original problem in a highlighted box
    original_problem = f"{data['num1']:,} {data['operation']} {data['num2']:,}"
    st.markdown(f"""
    <div style="
        background-color: #fff3e0; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #ff9800;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        color: #e65100;
        font-weight: bold;
    ">
        {original_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Show rounding steps
    st.markdown("### 🔄 **Step 1: Round each number**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Original:** {data['num1']:,}")
        st.markdown(f"**Rounded:** {data['rounded_num1']:,}")
    
    with col2:
        st.markdown(f"**Original:** {data['num2']:,}")
        st.markdown(f"**Rounded:** {data['rounded_num2']:,}")
    
    # Show the rounded calculation
    st.markdown("### 🧮 **Step 2: Calculate with rounded numbers**")
    rounded_problem = f"{data['rounded_num1']:,} {data['operation']} {data['rounded_num2']:,} = ?"
    st.markdown(f"**Calculate:** {rounded_problem}")
    
    # Answer input
    with st.form("estimation_form", clear_on_submit=False):
        st.markdown("**💭 What is your estimated answer?**")
        
        user_answer = st.number_input(
            "Enter your estimate:",
            min_value=0,
            step=1,
            format="%d",
            key="estimate_answer"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Estimate", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = str(int(user_answer))
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.question_count += 1
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Nice estimation!**")
        st.session_state.correct_count += 1
        
        # Increase difficulty (make rounding more precise)
        old_round_to = st.session_state.estimation_difficulty["round_to"]
        if old_round_to >= 100000:
            st.session_state.estimation_difficulty["round_to"] = max(10000, old_round_to // 2)
        elif old_round_to >= 10000:
            st.session_state.estimation_difficulty["round_to"] = max(1000, old_round_to // 2)
        else:
            st.session_state.estimation_difficulty["round_to"] = max(100, old_round_to // 2)
        
        new_round_to = st.session_state.estimation_difficulty["round_to"]
        if new_round_to < old_round_to:
            st.info(f"⬆️ **Great job! Now rounding to the nearest {new_round_to:,} for more precision**")
        
        show_solution_steps()
    else:
        st.error(f"❌ **Incorrect.** The correct estimate was **{int(correct_answer):,}**.")
        
        # Decrease difficulty (make rounding less precise)
        old_round_to = st.session_state.estimation_difficulty["round_to"]
        st.session_state.estimation_difficulty["round_to"] = min(100000, old_round_to * 2)
        
        new_round_to = st.session_state.estimation_difficulty["round_to"]
        if new_round_to > old_round_to:
            st.warning(f"⬇️ **Let's practice with easier rounding. Now rounding to the nearest {new_round_to:,}**")
        
        show_solution_steps()

def show_solution_steps():
    """Show the complete solution with steps"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See the complete solution**", expanded=True):
        st.markdown("### 🧮 **Step-by-step solution:**")
        
        # Step 1: Show rounding process
        st.markdown("**Step 1: Round each number**")
        
        # Explain rounding for first number
        st.markdown(f"• **{data['num1']:,}** rounded to nearest {data['round_to']:,}:")
        explain_rounding(data['num1'], data['round_to'], data['rounded_num1'])
        
        # Explain rounding for second number  
        st.markdown(f"• **{data['num2']:,}** rounded to nearest {data['round_to']:,}:")
        explain_rounding(data['num2'], data['round_to'], data['rounded_num2'])
        
        # Step 2: Show calculation
        st.markdown("**Step 2: Calculate with rounded numbers**")
        calculation = f"{data['rounded_num1']:,} {data['operation']} {data['rounded_num2']:,} = {data['answer']:,}"
        st.markdown(f"• **{calculation}**")
        
        # Step 3: Reasonableness check
        st.markdown("**Step 3: Check if the estimate makes sense**")
        original_range = f"between {min(data['num1'], data['num2']):,} and {max(data['num1'], data['num2']):,}"
        st.markdown(f"• Original numbers were {original_range}")
        st.markdown(f"• Our estimate of {data['answer']:,} seems reasonable! ✓")

def explain_rounding(original, round_to, rounded):
    """Explain how a specific number was rounded"""
    # Find which digit to look at for rounding
    if round_to == 100000:
        digit_place = "ten-thousands"
        look_at_digit = (original // 10000) % 10
    elif round_to == 10000:
        digit_place = "thousands"
        look_at_digit = (original // 1000) % 10
    elif round_to == 1000:
        digit_place = "hundreds"
        look_at_digit = (original // 100) % 10
    elif round_to == 100:
        digit_place = "tens"
        look_at_digit = (original // 10) % 10
    else:
        digit_place = "ones"
        look_at_digit = original % 10
    
    direction = "up" if rounded > original else "down"
    st.markdown(f"  - Look at {digit_place} digit: **{look_at_digit}**")
    st.markdown(f"  - Since {look_at_digit} is {'≥ 5' if look_at_digit >= 5 else '< 5'}, round **{direction}** to **{rounded:,}**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer