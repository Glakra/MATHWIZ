import streamlit as st
import random

def run():
    """
    Main function to run the Use One Multiplication Fact to Complete Another practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/use_one_multiplication_fact_to_complete_another.py
    """
    # Initialize session state for difficulty and game state
    if "mult_fact_difficulty" not in st.session_state:
        st.session_state.mult_fact_difficulty = 1  # Start with basic problems
    
    if "current_question_fact" not in st.session_state:
        st.session_state.current_question_fact = None
        st.session_state.correct_answer_fact = None
        st.session_state.show_feedback_fact = False
        st.session_state.answer_submitted_fact = False
        st.session_state.question_data_fact = {}
        st.session_state.mult_fact_score = 0
        st.session_state.total_questions_fact = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔗 Use One Multiplication Fact to Complete Another")
    st.markdown("*Build on known facts to solve new problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mult_fact_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Facts", 2: "Intermediate", 3: "Advanced"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Facts')}")
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
        if st.session_state.total_questions_fact > 0:
            accuracy = (st.session_state.mult_fact_score / st.session_state.total_questions_fact) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question_fact is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Multiplication Fact Strategies**", expanded=False):
        st.markdown("""
        ### How to Use Known Facts to Find New Ones:
        
        #### 🔹 **The Strategy:**
        When you know one multiplication fact, you can use it to find related facts:
        - **If you know:** 12 × 20 = 240
        - **You can find:** 12 × 19 = ?
        
        #### 🔹 **The Pattern:**
        - **Going down by 1:** If the second number decreases by 1, subtract the first number
        - **Going up by 1:** If the second number increases by 1, add the first number
        
        #### 🔹 **Why This Works:**
        Think about what multiplication really means:
        - **12 × 20** means "12 groups of 20" = 240
        - **12 × 19** means "12 groups of 19" = 12 groups of (20 - 1) = (12 × 20) - (12 × 1) = 240 - 12 = 228
        
        ### 📊 **Step-by-Step Examples:**
        
        #### **Example 1: Subtracting**
        ```
        Known fact: 50 × 90 = 4500
        Find: 50 × 89 = ?
        
        Think: 89 = 90 - 1
        So: 50 × 89 = 50 × (90 - 1) = (50 × 90) - (50 × 1) = 4500 - 50 = 4450
        ```
        
        #### **Example 2: Adding**
        ```
        Known fact: 7 × 30 = 210
        Find: 7 × 31 = ?
        
        Think: 31 = 30 + 1  
        So: 7 × 31 = 7 × (30 + 1) = (7 × 30) + (7 × 1) = 210 + 7 = 217
        ```
        
        #### **Example 3: Bigger Changes**
        ```
        Known fact: 6 × 40 = 240
        Find: 6 × 37 = ?
        
        Think: 37 = 40 - 3
        So: 6 × 37 = 6 × (40 - 3) = (6 × 40) - (6 × 3) = 240 - 18 = 222
        ```
        
        ### 🎯 **Different Question Types:**
        - **One less:** 15 × 20 = 300, so 15 × 19 = ___
        - **One more:** 8 × 60 = 480, so 8 × 61 = ___
        - **Few less:** 9 × 50 = 450, so 9 × 47 = ___
        - **Few more:** 4 × 80 = 320, so 4 × 83 = ___
        
        ### 💡 **Mental Math Tips:**
        - **Identify the change** first (how much bigger or smaller is the second number?)
        - **Multiply the change** by the first number
        - **Add or subtract** from the known fact
        - **Check reasonableness** - does your answer make sense?
        
        ### 🏆 **Why This Strategy Matters:**
        - **Builds number sense** - understand relationships between numbers
        - **Mental math fluency** - solve problems quickly without paper
        - **Pattern recognition** - see mathematical connections
        - **Problem-solving skills** - use what you know to find what you don't know
        """)

def generate_new_question():
    """Generate a new multiplication fact relationship question"""
    difficulty = st.session_state.mult_fact_difficulty
    
    # Choose the type of relationship
    relationship_types = ["subtract_1", "add_1", "subtract_few", "add_few"]
    
    # Adjust complexity based on difficulty
    if difficulty == 1:
        # Basic: simple relationships, easier numbers
        relationship_type = random.choice(["subtract_1", "add_1"])
        first_factor_options = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        second_factor_options = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    elif difficulty == 2:
        # Intermediate: include small changes
        relationship_type = random.choice(relationship_types)
        first_factor_options = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15]
        second_factor_options = [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90]
    else:  # difficulty == 3
        # Advanced: larger numbers and bigger changes
        relationship_type = random.choice(relationship_types)
        first_factor_options = [12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
        second_factor_options = [20, 25, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Generate the base multiplication
    first_factor = random.choice(first_factor_options)
    second_factor = random.choice(second_factor_options)
    known_product = first_factor * second_factor
    
    # Generate the related multiplication based on relationship type
    if relationship_type == "subtract_1":
        new_second_factor = second_factor - 1
        change_amount = -1
        operation = "subtract"
    elif relationship_type == "add_1":
        new_second_factor = second_factor + 1
        change_amount = 1
        operation = "add"
    elif relationship_type == "subtract_few":
        change_amount = -random.choice([2, 3, 4, 5])
        new_second_factor = second_factor + change_amount
        operation = "subtract"
    else:  # add_few
        change_amount = random.choice([2, 3, 4, 5])
        new_second_factor = second_factor + change_amount
        operation = "add"
    
    # Calculate the correct answer
    correct_answer = first_factor * new_second_factor
    
    # Alternative calculation using the relationship
    if operation == "add":
        alt_answer = known_product + (first_factor * abs(change_amount))
    else:
        alt_answer = known_product - (first_factor * abs(change_amount))
    
    st.session_state.question_data_fact = {
        "first_factor": first_factor,
        "second_factor": second_factor,
        "known_product": known_product,
        "new_second_factor": new_second_factor,
        "change_amount": change_amount,
        "operation": operation,
        "relationship_type": relationship_type
    }
    
    st.session_state.correct_answer_fact = correct_answer
    st.session_state.current_question_fact = "Find the missing number."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data_fact
    
    # Display question
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question_fact}**")
    
    # Display the known fact and the question
    fact_display = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        border: 2px solid #dee2e6;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #495057;
        margin: 20px 0;
        font-family: 'Courier New', monospace;
        line-height: 1.8;
    ">
        {data['first_factor']} × {data['second_factor']} = {data['known_product']}, so {data['first_factor']} × {data['new_second_factor']} = <span style="color: #007bff;">____</span>
    </div>
    """
    
    st.markdown(fact_display, unsafe_allow_html=True)
    
    # Input section
    with st.form("multiplication_fact_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_answer = st.number_input(
                f"{data['first_factor']} × {data['new_second_factor']} =",
                min_value=0,
                max_value=100000,
                value=None,
                step=1,
                key="fact_answer_input",
                placeholder="Enter your answer",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer_fact = int(user_answer)
            st.session_state.show_feedback_fact = True
            st.session_state.answer_submitted_fact = True
            st.session_state.total_questions_fact += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback_fact:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted_fact:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer_fact
    correct_answer = st.session_state.correct_answer_fact
    data = st.session_state.question_data_fact
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.mult_fact_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions_fact % 5 == 0:  # Every 5 questions
            accuracy = st.session_state.mult_fact_score / st.session_state.total_questions_fact
            if accuracy >= 0.8 and st.session_state.mult_fact_difficulty < 3:
                old_difficulty = st.session_state.mult_fact_difficulty
                st.session_state.mult_fact_difficulty += 1
                if old_difficulty < st.session_state.mult_fact_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.mult_fact_difficulty}**")
                    if st.session_state.mult_fact_difficulty == 3:
                        st.balloons()
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty if struggling
        if st.session_state.total_questions_fact % 5 == 0:  # Every 5 questions
            accuracy = st.session_state.mult_fact_score / st.session_state.total_questions_fact
            if accuracy < 0.4 and st.session_state.mult_fact_difficulty > 1:
                old_difficulty = st.session_state.mult_fact_difficulty
                st.session_state.mult_fact_difficulty = max(st.session_state.mult_fact_difficulty - 1, 1)
                if old_difficulty > st.session_state.mult_fact_difficulty:
                    st.warning(f"⬇️ **Let's practice easier problems. Back to Level {st.session_state.mult_fact_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the multiplication fact relationship"""
    data = st.session_state.question_data_fact
    correct_answer = st.session_state.correct_answer_fact
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        change = abs(data['change_amount'])
        change_text = f"{change}" if change > 1 else "1"
        
        if data['operation'] == "add":
            direction = "increased"
            math_operation = "add"
            symbol = "+"
        else:
            direction = "decreased"
            math_operation = "subtract"
            symbol = "-"
        
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Known fact:** {data['first_factor']} × {data['second_factor']} = {data['known_product']}
        **Find:** {data['first_factor']} × {data['new_second_factor']} = ?
        
        #### 🔍 **Step 1: Identify the change**
        The second factor changed from {data['second_factor']} to {data['new_second_factor']}
        - **Change:** {data['second_factor']} → {data['new_second_factor']} (the number {direction} by {change_text})
        
        #### 🧮 **Step 2: Apply the relationship**
        When the second factor {direction} by {change_text}, we {math_operation} {change_text} group(s) of the first factor.
        
        **Method 1 - Using the relationship:**
        {data['first_factor']} × {data['new_second_factor']} = {data['known_product']} {symbol} ({data['first_factor']} × {change})
        = {data['known_product']} {symbol} {data['first_factor'] * change}
        = **{correct_answer}**
        
        **Method 2 - Direct calculation:**
        {data['first_factor']} × {data['new_second_factor']} = **{correct_answer}**
        
        #### ✅ **Step 3: Verify the answer**
        Both methods give us the same answer: **{correct_answer}**
        
        ### 💡 **Why This Works:**
        Multiplication represents **groups of objects**:
        - {data['first_factor']} × {data['second_factor']} = {data['first_factor']} groups of {data['second_factor']} = {data['known_product']}
        - {data['first_factor']} × {data['new_second_factor']} = {data['first_factor']} groups of {data['new_second_factor']} = {correct_answer}
        
        The difference between these is exactly {data['first_factor']} × {change} = {data['first_factor'] * change}.
        
        ### 🎯 **The Pattern:**
        - **When the second factor goes up by n:** Add n × (first factor) to the original product
        - **When the second factor goes down by n:** Subtract n × (first factor) from the original product
        
        This pattern helps you use known multiplication facts to quickly find new ones!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question_fact = None
    st.session_state.correct_answer_fact = None
    st.session_state.show_feedback_fact = False
    st.session_state.answer_submitted_fact = False
    st.session_state.question_data_fact = {}
    
    # Clear input values
    if "fact_answer_input" in st.session_state:
        del st.session_state.fact_answer_input
    if "user_answer_fact" in st.session_state:
        del st.session_state.user_answer_fact