import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Quotients practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/estimate_quotients.py
    """
    # Initialize session state for difficulty and game state
    if "estimate_difficulty" not in st.session_state:
        st.session_state.estimate_difficulty = 1  # Start with simple problems
    
    if "current_estimate_problem" not in st.session_state:
        st.session_state.current_estimate_problem = None
        st.session_state.correct_estimate_answer = None
        st.session_state.show_estimate_feedback = False
        st.session_state.estimate_answer_submitted = False
        st.session_state.estimate_problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("🎯 Estimate Quotients")
    st.markdown("*Practice estimating division answers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.estimate_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple estimation (2-3 digit ÷ 1 digit)",
            2: "Intermediate estimation (4-5 digit ÷ 1 digit)", 
            3: "Advanced estimation (Comparisons & choices)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_estimate_problem is None:
        generate_new_estimate_problem()
    
    # Display current question
    display_estimate_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Estimation Strategies**", expanded=False):
        st.markdown("""
        ### Why Estimate Quotients?
        **Estimation helps you:**
        - **Check if your exact answer is reasonable**
        - **Solve problems quickly** when exact answers aren't needed
        - **Compare** which division results are larger or smaller
        - **Spot errors** in calculations
        
        ### Estimation Strategies:
        
        #### **Strategy 1: Round to Compatible Numbers**
        Make the division easier by rounding to numbers that divide nicely.
        
        **Example:** 284 ÷ 7
        - Round 284 to 280 (compatible with 7)
        - 280 ÷ 7 = 40
        - **Estimate: About 40**
        
        #### **Strategy 2: Round to the Nearest Ten/Hundred**
        Round the dividend to make calculation easier.
        
        **Example:** 1,847 ÷ 6
        - Round 1,847 to 1,800
        - 1,800 ÷ 6 = 300
        - **Estimate: About 300**
        
        #### **Strategy 3: Use Benchmark Divisions**
        Think of easy divisions you know.
        
        **Example:** 456 ÷ 8
        - I know 400 ÷ 8 = 50
        - 456 is close to 400
        - **Estimate: About 50-60**
        
        #### **Strategy 4: Front-End Estimation**
        Use only the front digits.
        
        **Example:** 3,428 ÷ 7
        - Think: 3,400 ÷ 7
        - 3,500 ÷ 7 = 500 (since 35 ÷ 7 = 5)
        - **Estimate: About 500**
        
        ### Comparison Problems:
        When comparing estimates like **36,528 ? 82,782 ÷ 5**:
        
        **Step 1:** Estimate each side
        - Left side: 36,528 (already a number)
        - Right side: 82,782 ÷ 5 ≈ 80,000 ÷ 5 = 16,000
        
        **Step 2:** Compare
        - 36,528 vs 16,000
        - 36,528 > 16,000
        - **Answer: >**
        
        ### Quick Mental Math Tips:
        - **÷ 5:** Multiply by 2, then ÷ 10 (or ÷ 10, then × 2)
        - **÷ 25:** Think quarters (25¢), or ÷ 100 then × 4
        - **÷ 2:** Half the number
        - **÷ 4:** Half, then half again
        
        ### Common Estimation Ranges:
        - **Hundreds ÷ single digit** → Tens
        - **Thousands ÷ single digit** → Hundreds  
        - **Ten thousands ÷ single digit** → Thousands
        
        ### Remember:
        - **Estimation should be quick** - don't spend too long calculating
        - **Close is good enough** - estimates don't need to be exact
        - **Check reasonableness** - does your estimate make sense?
        """)

def generate_new_estimate_problem():
    """Generate a new estimation problem based on difficulty"""
    difficulty = st.session_state.estimate_difficulty
    
    if difficulty == 1:
        # Simple estimation problems
        problem_types = ["direct_estimate", "multiple_choice"]
        problem_type = random.choice(problem_types)
        
        if problem_type == "direct_estimate":
            # Direct estimation: "Estimate 284 ÷ 7"
            dividend = random.randint(150, 999)
            divisor = random.randint(3, 9)
            exact_quotient = dividend / divisor
            
            # Create reasonable estimate range
            lower_bound = int(exact_quotient * 0.8)
            upper_bound = int(exact_quotient * 1.2)
            
            problem_text = f"Estimate: {dividend:,} ÷ {divisor}"
            question_type = "direct_estimate"
            correct_answer = round(exact_quotient / 10) * 10  # Round to nearest 10
            
        else:
            # Multiple choice estimation
            dividend = random.randint(200, 899)
            divisor = random.randint(4, 8)
            exact_quotient = dividend / divisor
            
            # Create multiple choice options
            correct_estimate = round(exact_quotient / 10) * 10
            options = [
                correct_estimate,
                correct_estimate + random.choice([10, 20, 30]),
                correct_estimate - random.choice([10, 20, 30]),
                correct_estimate + random.choice([40, 50])
            ]
            options = sorted(list(set(options)))[:4]  # Remove duplicates and limit to 4
            random.shuffle(options)
            
            problem_text = f"Which is the best estimate for {dividend:,} ÷ {divisor}?"
            question_type = "multiple_choice"
            correct_answer = correct_estimate
            
    elif difficulty == 2:
        # Intermediate - larger numbers
        problem_types = ["direct_estimate", "multiple_choice"]
        problem_type = random.choice(problem_types)
        
        if problem_type == "direct_estimate":
            dividend = random.randint(1500, 9999)
            divisor = random.randint(3, 9)
            exact_quotient = dividend / divisor
            
            problem_text = f"Estimate: {dividend:,} ÷ {divisor}"
            question_type = "direct_estimate"
            correct_answer = round(exact_quotient / 100) * 100  # Round to nearest 100
            
        else:
            dividend = random.randint(2000, 8999)
            divisor = random.randint(4, 8)
            exact_quotient = dividend / divisor
            
            correct_estimate = round(exact_quotient / 100) * 100
            options = [
                correct_estimate,
                correct_estimate + random.choice([100, 200, 300]),
                correct_estimate - random.choice([100, 200, 300]),
                correct_estimate + random.choice([400, 500])
            ]
            options = sorted(list(set([opt for opt in options if opt > 0])))[:4]
            random.shuffle(options)
            
            problem_text = f"Which is the best estimate for {dividend:,} ÷ {divisor}?"
            question_type = "multiple_choice"
            correct_answer = correct_estimate
    
    else:
        # Advanced - comparison problems
        problem_types = ["comparison", "advanced_multiple_choice"]
        problem_type = random.choice(problem_types)
        
        if problem_type == "comparison":
            # Create comparison like the example: number ? division
            number1 = random.randint(15000, 45000)
            dividend2 = random.randint(50000, 90000)
            divisor2 = random.choice([3, 4, 5, 6, 7, 8, 9])
            
            quotient2 = dividend2 / divisor2
            
            if number1 > quotient2:
                correct_answer = ">"
            else:
                correct_answer = "<"
            
            problem_text = f"Estimate. Which sign makes the statement true?"
            question_type = "comparison"
            
        else:
            # Advanced multiple choice with larger numbers
            dividend = random.randint(15000, 50000)
            divisor = random.randint(6, 9)
            exact_quotient = dividend / divisor
            
            correct_estimate = round(exact_quotient / 1000) * 1000
            options = [
                correct_estimate,
                correct_estimate + random.choice([1000, 2000]),
                correct_estimate - random.choice([1000, 2000]),
                correct_estimate + random.choice([3000, 4000])
            ]
            options = sorted(list(set([opt for opt in options if opt > 0])))[:4]
            random.shuffle(options)
            
            problem_text = f"Which is the best estimate for {dividend:,} ÷ {divisor}?"
            question_type = "multiple_choice"
            correct_answer = correct_estimate
    
    st.session_state.estimate_problem_data = {
        "problem_text": problem_text,
        "question_type": question_type,
        "dividend": dividend if 'dividend' in locals() else None,
        "divisor": divisor if 'divisor' in locals() else None,
        "number1": number1 if 'number1' in locals() else None,
        "dividend2": dividend2 if 'dividend2' in locals() else None,
        "divisor2": divisor2 if 'divisor2' in locals() else None,
        "options": options if 'options' in locals() else None,
        "exact_quotient": exact_quotient if 'exact_quotient' in locals() else None
    }
    st.session_state.correct_estimate_answer = correct_answer
    st.session_state.current_estimate_problem = problem_text

def display_estimate_problem():
    """Display the current estimation problem interface"""
    data = st.session_state.estimate_problem_data
    question_type = data["question_type"]
    
    # Display question header
    st.markdown("### 🎯 Estimation Problem:")
    
    # Display the problem based on type
    if question_type == "comparison":
        # Comparison problem like the example
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa; 
            padding: 30px; 
            border-radius: 15px; 
            border-left: 5px solid #17a2b8;
            font-size: 18px;
            line-height: 1.6;
            margin: 20px 0;
            color: #333;
            text-align: center;
        ">
            {data['problem_text']}
        </div>
        """, unsafe_allow_html=True)
        
        # Show the comparison expression
        st.markdown(f"""
        <div style="
            background-color: #e8f4fd; 
            padding: 25px; 
            border-radius: 12px; 
            border: 2px solid #1976d2;
            font-family: 'Courier New', monospace;
            font-size: 24px;
            text-align: center;
            margin: 25px 0;
            font-weight: bold;
            color: #1976d2;
        ">
            {data['number1']:,} ? {data['dividend2']:,} ÷ {data['divisor2']}
        </div>
        """, unsafe_allow_html=True)
        
        # Show comparison options visually
        st.markdown("**Choose the correct sign:**")
        st.markdown(f"""
        <div style="text-align: center; margin: 15px 0;">
            <p style="font-size: 16px; color: #666;">
                Is <strong>{data['number1']:,}</strong> greater than or less than <strong>{data['dividend2']:,} ÷ {data['divisor2']}</strong>?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create clear button options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"👆 {data['number1']:,} is GREATER", use_container_width=True, type="secondary", key="greater_than_btn"):
                st.session_state.user_estimate_answer = ">"
                st.session_state.show_estimate_feedback = True
                st.session_state.estimate_answer_submitted = True
                st.rerun()
        
        with col2:
            if st.button(f"👇 {data['number1']:,} is LESS", use_container_width=True, type="secondary", key="less_than_btn"):
                st.session_state.user_estimate_answer = "<"
                st.session_state.show_estimate_feedback = True
                st.session_state.estimate_answer_submitted = True
                st.rerun()
    
    elif question_type == "multiple_choice":
        # Multiple choice problem
        st.markdown(f"""
        <div style="
            background-color: #f0f8ff; 
            padding: 30px; 
            border-radius: 15px; 
            border-left: 5px solid #4682b4;
            font-size: 18px;
            line-height: 1.6;
            margin: 20px 0;
            color: #333;
        ">
            {data['problem_text']}
        </div>
        """, unsafe_allow_html=True)
        
        # Show the division expression
        st.markdown(f"""
        <div style="
            background-color: #f3e5f5; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 4px solid #9c27b0;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            color: #333;
        ">
            {data['dividend']:,} ÷ {data['divisor']}
        </div>
        """, unsafe_allow_html=True)
        
        # Multiple choice options
        st.markdown("**Choose the best estimate:**")
        
        cols = st.columns(2)
        for i, option in enumerate(data['options']):
            col_index = i % 2
            with cols[col_index]:
                if st.button(f"{option:,}", use_container_width=True, type="secondary", key=f"option_{i}"):
                    st.session_state.user_estimate_answer = option
                    st.session_state.show_estimate_feedback = True
                    st.session_state.estimate_answer_submitted = True
                    st.rerun()
    
    else:
        # Direct estimation problem
        st.markdown(f"""
        <div style="
            background-color: #fff8e1; 
            padding: 30px; 
            border-radius: 15px; 
            border-left: 5px solid #ff9800;
            font-size: 18px;
            line-height: 1.6;
            margin: 20px 0;
            color: #333;
        ">
            {data['problem_text']}
        </div>
        """, unsafe_allow_html=True)
        
        # Show the division expression
        st.markdown(f"""
        <div style="
            background-color: #fff3e0; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 4px solid #ff9800;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            color: #333;
        ">
            {data['dividend']:,} ÷ {data['divisor']}
        </div>
        """, unsafe_allow_html=True)
        
        # Direct input
        with st.form("direct_estimate_form", clear_on_submit=False):
            st.markdown("**Enter your estimate:**")
            
            user_answer = st.number_input(
                "Your estimate:",
                min_value=1,
                step=1,
                key="direct_estimate_input",
                help="Enter a reasonable estimate (doesn't need to be exact)"
            )
            
            # Submit button
            if st.form_submit_button("✅ Submit Estimate", type="primary", use_container_width=True):
                st.session_state.user_estimate_answer = int(user_answer) if user_answer is not None else 0
                st.session_state.show_estimate_feedback = True
                st.session_state.estimate_answer_submitted = True
    
    # Show feedback and next button
    handle_estimate_feedback_and_next()

def handle_estimate_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_estimate_feedback:
        show_estimate_feedback()
    
    # Next question button
    if st.session_state.estimate_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_estimate_question_state()
                st.rerun()

def show_estimate_feedback():
    """Display feedback for the submitted estimation answer"""
    user_answer = st.session_state.user_estimate_answer
    correct_answer = st.session_state.correct_estimate_answer
    data = st.session_state.estimate_problem_data
    
    if data["question_type"] == "comparison":
        # Comparison feedback
        if user_answer == correct_answer:
            st.success("🎉 **Excellent! You chose the correct sign!**")
            
            # Show the estimation work
            quotient2 = data['dividend2'] / data['divisor2']
            st.info(f"✅ **{data['number1']:,} {correct_answer} {quotient2:,.0f}** (approximately)")
            
        else:
            st.error(f"❌ **Not quite right.** The correct sign is **{correct_answer}**.")
            show_comparison_explanation()
    
    elif data["question_type"] == "direct_estimate":
        # Direct estimation feedback - check if within reasonable range
        exact_quotient = data['exact_quotient']
        error_percentage = abs(user_answer - exact_quotient) / exact_quotient
        
        if error_percentage <= 0.25:  # Within 25% is good estimation
            st.success("🎉 **Great estimation! You're very close!**")
            st.info(f"✅ **Your estimate: {user_answer:,}** | **Exact answer: {exact_quotient:.0f}**")
        else:
            st.warning(f"📊 **Your estimate could be closer.** Try again!")
            st.info(f"**Your estimate: {user_answer:,}** | **Exact answer: {exact_quotient:.0f}**")
            show_estimation_explanation()
    
    else:
        # Multiple choice feedback
        if user_answer == correct_answer:
            st.success("🎉 **Perfect! That's the best estimate!**")
            exact_quotient = data['exact_quotient']
            st.info(f"✅ **Your estimate: {user_answer:,}** | **Exact answer: {exact_quotient:.0f}**")
        else:
            st.error(f"❌ **Not the best estimate.** The best estimate is **{correct_answer:,}**.")
            show_estimation_explanation()
    
    # Update difficulty based on performance
    if user_answer == correct_answer or (data["question_type"] == "direct_estimate" and error_percentage <= 0.25):
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.estimate_difficulty
        st.session_state.estimate_difficulty = min(st.session_state.estimate_difficulty + 1, 3)
        
        if st.session_state.estimate_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered estimation skills!**")
        elif old_difficulty < st.session_state.estimate_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working on Level {st.session_state.estimate_difficulty} problems**")
    else:
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.estimate_difficulty
        st.session_state.estimate_difficulty = max(st.session_state.estimate_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.estimate_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.estimate_difficulty}. Keep practicing!**")

def show_comparison_explanation():
    """Show explanation for comparison problems"""
    data = st.session_state.estimate_problem_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        quotient2 = data['dividend2'] / data['divisor2']
        
        st.markdown(f"""
        ### Comparison Analysis:
        
        **Left side:** {data['number1']:,}
        
        **Right side:** {data['dividend2']:,} ÷ {data['divisor2']}
        - Estimate: {data['dividend2']:,} ÷ {data['divisor2']} ≈ {quotient2:,.0f}
        
        ### Step-by-step estimation:
        - Round {data['dividend2']:,} to make division easier
        - Think: {round(data['dividend2']/1000)*1000:,} ÷ {data['divisor2']} = {round(data['dividend2']/1000)*1000//data['divisor2']:,.0f}
        
        ### Comparison:
        - {data['number1']:,} vs {quotient2:,.0f}
        - **Answer: {st.session_state.correct_estimate_answer}**
        """)

def show_estimation_explanation():
    """Show explanation for estimation problems"""
    data = st.session_state.estimate_problem_data
    
    with st.expander("📖 **Click here for estimation strategies**", expanded=True):
        exact_quotient = data['exact_quotient']
        dividend = data['dividend']
        divisor = data['divisor']
        
        st.markdown(f"""
        ### Estimation Strategies for {dividend:,} ÷ {divisor}:
        
        **Strategy 1: Round to compatible numbers**
        - Think of numbers close to {dividend:,} that divide easily by {divisor}
        - Example: {round(dividend/100)*100:,} ÷ {divisor} = {round(dividend/100)*100//divisor:,}
        
        **Strategy 2: Front-end estimation**
        - Use the front digits: {str(dividend)[0]}{str(dividend)[1] if len(str(dividend)) > 1 else ''}000 ÷ {divisor}
        - This gives approximately {int(str(dividend)[0] + str(dividend)[1] if len(str(dividend)) > 1 else str(dividend)[0] + '0') * 100 // divisor * 10:,}
        
        **Exact answer:** {exact_quotient:.0f}
        **Good estimates would be:** {round(exact_quotient/10)*10:,} to {round(exact_quotient/10)*10 + 20:,}
        
        ### Remember:
        - Estimation should be **quick and easy**
        - **Close is good enough** - you don't need the exact answer
        - Use **round numbers** that are easy to divide
        """)

def reset_estimate_question_state():
    """Reset the question state for next question"""
    st.session_state.current_estimate_problem = None
    st.session_state.correct_estimate_answer = None
    st.session_state.show_estimate_feedback = False
    st.session_state.estimate_answer_submitted = False
    st.session_state.estimate_problem_data = {}
    if "user_estimate_answer" in st.session_state:
        del st.session_state.user_estimate_answer