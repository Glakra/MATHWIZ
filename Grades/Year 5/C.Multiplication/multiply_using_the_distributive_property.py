import streamlit as st
import random

def run():
    """
    Main function to run the Multiply using the Distributive Property practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_using_the_distributive_property.py
    """
    # Initialize session state for difficulty and game state
    if "multiply_dist_difficulty" not in st.session_state:
        st.session_state.multiply_dist_difficulty = 1  # Start with basic problems
    
    if "current_question_mult" not in st.session_state:
        st.session_state.current_question_mult = None
        st.session_state.correct_answers_mult = {}
        st.session_state.show_feedback_mult = False
        st.session_state.answer_submitted_mult = False
        st.session_state.question_data_mult = {}
        st.session_state.multiply_dist_score = 0
        st.session_state.total_questions_mult = 0
        st.session_state.user_answers_mult = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🧮 Multiply Using the Distributive Property")
    st.markdown("*Break down complex multiplications into simpler parts*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiply_dist_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Problems", 2: "Intermediate", 3: "Advanced"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Problems')}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
        
        # Show score
        if st.session_state.total_questions_mult > 0:
            accuracy = (st.session_state.multiply_dist_score / st.session_state.total_questions_mult) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question_mult is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Distributive Property Strategy**", expanded=False):
        st.markdown("""
        ### How to Multiply Using the Distributive Property:
        
        #### 🔹 **The Strategy:**
        When you have a difficult multiplication like **6 × 34**, break it down:
        1. **Split the larger number** into easier parts: 34 = 30 + 4
        2. **Multiply each part** separately: 6 × 30 and 6 × 4  
        3. **Add the results** together: (6 × 30) + (6 × 4)
        
        #### 🔹 **Why This Works:**
        The **distributive property** says: **a × (b + c) = (a × b) + (a × c)**
        - So: 6 × (30 + 4) = (6 × 30) + (6 × 4)
        - This turns one hard problem into two easy ones!
        
        #### 🔹 **Step-by-Step Process:**
        1. **First:** Calculate the simpler multiplications
        2. **Then:** Use those answers to solve the main problem
        3. **Finally:** Add the partial products together
        
        ### 📊 **Complete Example:**
        
        #### **Problem: 7 × 25**
        ```
        Step 1: Break down 25 = 20 + 5
        
        Step 2: Calculate parts:
        • 7 × 20 = 140
        • 7 × 5 = 35
        
        Step 3: Use distributive property:
        7 × 25 = 7 × (20 + 5) = (7 × 20) + (7 × 5) = 140 + 35 = 175
        ```
        
        ### 🎯 **Common Breakdowns:**
        - **Two-digit numbers:** 23 = 20 + 3, 47 = 40 + 7, 56 = 50 + 6
        - **Larger numbers:** 123 = 100 + 20 + 3, 245 = 200 + 40 + 5
        - **Strategic splits:** 48 = 40 + 8 or 48 = 50 - 2 (whichever is easier)
        
        ### 💡 **Tips for Success:**
        - **Choose friendly numbers** - use multiples of 10 when possible
        - **Check your work** - does the breakdown add up to the original number?
        - **Practice mental math** - these partial products should be easy to calculate
        - **Verify your answer** - add the partial products carefully
        
        ### 🏆 **Why This Method Helps:**
        - **Mental math skills** - solve problems without paper and pencil
        - **Number sense** - understand how numbers break apart and combine
        - **Flexibility** - multiple ways to solve the same problem
        - **Foundation for algebra** - understanding how expressions expand
        """)

def generate_new_question():
    """Generate a new multiply using distributive property question"""
    difficulty = st.session_state.multiply_dist_difficulty
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        # Basic: single digit × two-digit (ending in friendly numbers)
        multiplier_options = [2, 3, 4, 5, 6, 7, 8, 9]
        tens_options = [20, 30, 40, 50, 60, 70, 80, 90]
        ones_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    elif difficulty == 2:
        # Intermediate: single digit × larger two-digit
        multiplier_options = [2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
        tens_options = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        ones_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:  # difficulty == 3
        # Advanced: two-digit × two-digit (simplified)
        multiplier_options = [11, 12, 13, 14, 15, 16, 17, 18, 19]
        tens_options = [20, 30, 40, 50, 60]
        ones_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Generate the problem
    multiplier = random.choice(multiplier_options)
    tens_part = random.choice(tens_options)
    ones_part = random.choice(ones_options)
    target_number = tens_part + ones_part
    
    # Calculate all the answers
    first_product = multiplier * ones_part      # easier multiplication
    second_product = multiplier * tens_part     # easier multiplication  
    final_product = first_product + second_product  # final answer
    
    st.session_state.question_data_mult = {
        "multiplier": multiplier,
        "target_number": target_number,
        "tens_part": tens_part,
        "ones_part": ones_part,
        "first_product": first_product,
        "second_product": second_product,
        "final_product": final_product,
        "breakdown": f"{target_number} = {tens_part} + {ones_part}"
    }
    
    st.session_state.correct_answers_mult = {
        "first": first_product,
        "second": second_product,
        "final": final_product
    }
    
    st.session_state.current_question_mult = f"Multiply using the distributive property:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data_mult
    
    # Display question header
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question_mult}**")
    
    with st.form("multiply_distributive_form", clear_on_submit=False):
        # Step 1: Simple multiplications
        st.markdown("### 📝 **Multiply:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_input = st.number_input(
                f"{data['multiplier']} × {data['ones_part']} =",
                min_value=0,
                max_value=1000,
                value=st.session_state.user_answers_mult.get("first", None) if "user_answers_mult" in st.session_state else None,
                step=1,
                key="first_mult_input",
                placeholder="Enter answer"
            )
        
        with col2:
            second_input = st.number_input(
                f"{data['multiplier']} × {data['tens_part']} =",
                min_value=0,
                max_value=10000,
                value=st.session_state.user_answers_mult.get("second", None) if "user_answers_mult" in st.session_state else None,
                step=1,
                key="second_mult_input",
                placeholder="Enter answer"
            )
        
        # Step 2: Distributive property application
        st.markdown("### 🧠 **Now multiply the following, using your answers from above and the distributive property of multiplication:**")
        
        # Show the breakdown hint
        st.markdown(f"**Hint:** {data['breakdown']}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            final_input = st.number_input(
                f"{data['multiplier']} × {data['target_number']} =",
                min_value=0,
                max_value=50000,
                value=st.session_state.user_answers_mult.get("final", None) if "user_answers_mult" in st.session_state else None,
                step=1,
                key="final_mult_input",
                placeholder="Enter final answer"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            # Collect all answers
            st.session_state.user_answers_mult = {
                "first": first_input if first_input is not None else 0,
                "second": second_input if second_input is not None else 0,
                "final": final_input if final_input is not None else 0
            }
            st.session_state.show_feedback_mult = True
            st.session_state.answer_submitted_mult = True
            st.session_state.total_questions_mult += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback_mult:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted_mult:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answers = st.session_state.user_answers_mult
    correct_answers = st.session_state.correct_answers_mult
    data = st.session_state.question_data_mult
    
    # Check each part
    first_correct = user_answers["first"] == correct_answers["first"]
    second_correct = user_answers["second"] == correct_answers["second"]
    final_correct = user_answers["final"] == correct_answers["final"]
    
    # Feedback for partial products
    st.markdown("### 📊 **Step-by-Step Check:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if first_correct:
            st.success(f"✅ **{data['multiplier']} × {data['ones_part']} = {correct_answers['first']}** ✓")
        else:
            st.error(f"❌ **{data['multiplier']} × {data['ones_part']}** = {user_answers['first']} ≠ {correct_answers['first']}")
    
    with col2:
        if second_correct:
            st.success(f"✅ **{data['multiplier']} × {data['tens_part']} = {correct_answers['second']}** ✓")
        else:
            st.error(f"❌ **{data['multiplier']} × {data['tens_part']}** = {user_answers['second']} ≠ {correct_answers['second']}")
    
    # Feedback for final answer
    st.markdown("### 🎯 **Final Answer Check:**")
    if final_correct:
        st.success(f"✅ **{data['multiplier']} × {data['target_number']} = {correct_answers['final']}** ✓")
    else:
        st.error(f"❌ **{data['multiplier']} × {data['target_number']}** = {user_answers['final']} ≠ {correct_answers['final']}")
    
    # Overall scoring and feedback
    parts_correct = sum([first_correct, second_correct])
    
    if first_correct and second_correct and final_correct:
        st.success("🏆 **Perfect! All parts correct!**")
        st.session_state.multiply_dist_score += 1
        st.balloons()
    elif final_correct and (first_correct or second_correct):
        st.info("🌟 **Great job! You got the final answer right!**")
        st.markdown("💡 *Double-check your partial products for even better understanding.*")
    elif parts_correct == 2 and not final_correct:
        st.warning("👍 **Good work on the partial products!**")
        st.markdown(f"💡 *Remember to add them: {correct_answers['first']} + {correct_answers['second']} = {correct_answers['final']}*")
    elif parts_correct == 1:
        st.info("💪 **You're getting there! Keep practicing the multiplication facts.**")
    else:
        st.warning("🎯 **Let's review the steps together.**")
    
    # Show the complete breakdown
    st.markdown("### 📋 **Complete Solution:**")
    st.markdown(f"""
    **Using the distributive property:**
    
    {data['multiplier']} × {data['target_number']} = {data['multiplier']} × ({data['tens_part']} + {data['ones_part']})
    
    = ({data['multiplier']} × {data['tens_part']}) + ({data['multiplier']} × {data['ones_part']})
    
    = {correct_answers['second']} + {correct_answers['first']} = **{correct_answers['final']}**
    """)
    
    # Adjust difficulty based on performance
    if st.session_state.total_questions_mult % 4 == 0:  # Every 4 questions
        accuracy = st.session_state.multiply_dist_score / st.session_state.total_questions_mult
        if accuracy >= 0.75 and st.session_state.multiply_dist_difficulty < 3:
            old_difficulty = st.session_state.multiply_dist_difficulty
            st.session_state.multiply_dist_difficulty += 1
            if old_difficulty < st.session_state.multiply_dist_difficulty:
                st.success(f"⬆️ **Level Up! Now at Level {st.session_state.multiply_dist_difficulty}**")
        elif accuracy < 0.4 and st.session_state.multiply_dist_difficulty > 1:
            old_difficulty = st.session_state.multiply_dist_difficulty
            st.session_state.multiply_dist_difficulty = max(st.session_state.multiply_dist_difficulty - 1, 1)
            if old_difficulty > st.session_state.multiply_dist_difficulty:
                st.warning(f"⬇️ **Let's practice easier problems. Back to Level {st.session_state.multiply_dist_difficulty}**")
    
    # Show detailed explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the distributive property multiplication"""
    data = st.session_state.question_data_mult
    correct_answers = st.session_state.correct_answers_mult
    
    with st.expander("📖 **Click here for complete explanation**", expanded=True):
        st.markdown(f"""
        ### Why the Distributive Property Works:
        
        **Problem:** {data['multiplier']} × {data['target_number']}
        
        #### 🔍 **Step 1: Break down the number**
        {data['target_number']} = {data['tens_part']} + {data['ones_part']}
        
        *We choose this breakdown because multiples of 10 are easier to multiply!*
        
        #### 🧮 **Step 2: Apply the distributive property**
        {data['multiplier']} × {data['target_number']} = {data['multiplier']} × ({data['tens_part']} + {data['ones_part']})
        
        **The distributive property says:** a × (b + c) = (a × b) + (a × c)
        
        So: {data['multiplier']} × ({data['tens_part']} + {data['ones_part']}) = ({data['multiplier']} × {data['tens_part']}) + ({data['multiplier']} × {data['ones_part']})
        
        #### ✅ **Step 3: Calculate each part**
        - **First part:** {data['multiplier']} × {data['tens_part']} = {correct_answers['second']}
        - **Second part:** {data['multiplier']} × {data['ones_part']} = {correct_answers['first']}
        
        #### 🎯 **Step 4: Add the results**
        {correct_answers['second']} + {correct_answers['first']} = **{correct_answers['final']}**
        
        ### 💡 **Alternative Breakdowns:**
        You could also break down {data['target_number']} differently:
        - {data['target_number']} = {data['target_number'] - 10} + 10
        - {data['target_number']} = {data['target_number'] + 10} - 10
        
        The distributive property is flexible - choose the breakdown that makes mental math easiest!
        
        ### 🏆 **Mental Math Tip:**
        This method helps you multiply large numbers in your head:
        1. **Break into friendly parts** (usually multiples of 10)
        2. **Multiply each part separately** 
        3. **Add the results together**
        
        With practice, you can do this entire calculation mentally!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question_mult = None
    st.session_state.correct_answers_mult = {}
    st.session_state.show_feedback_mult = False
    st.session_state.answer_submitted_mult = False
    st.session_state.question_data_mult = {}
    st.session_state.user_answers_mult = {}
    
    # Clear input values
    for key in ["first_mult_input", "second_mult_input", "final_mult_input"]:
        if key in st.session_state:
            del st.session_state[key]