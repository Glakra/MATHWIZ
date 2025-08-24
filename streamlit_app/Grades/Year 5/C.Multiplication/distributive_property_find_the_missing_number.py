import streamlit as st
import random

def run():
    """
    Main function to run the Distributive Property: Find the Missing Number practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/distributive_property_find_missing_number.py
    """
    # Initialize session state for difficulty and game state
    if "distributive_difficulty" not in st.session_state:
        st.session_state.distributive_difficulty = 1  # Start with basic problems
    
    if "current_question_dist" not in st.session_state:
        st.session_state.current_question_dist = None
        st.session_state.correct_answer_dist = None
        st.session_state.show_feedback_dist = False
        st.session_state.answer_submitted_dist = False
        st.session_state.question_data_dist = {}
        st.session_state.distributive_score = 0
        st.session_state.total_questions_dist = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔢 Distributive Property: Find the Missing Number")
    st.markdown("*Use the distributive property to find missing numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.distributive_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Numbers", 2: "Intermediate", 3: "Advanced"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Numbers')}")
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
        if st.session_state.total_questions_dist > 0:
            accuracy = (st.session_state.distributive_score / st.session_state.total_questions_dist) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question_dist is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Distributive Property Guide**", expanded=False):
        st.markdown("""
        ### Understanding the Distributive Property:
        
        #### 🔹 **What is the Distributive Property?**
        The distributive property says that:
        **a × (b + c) = (a × b) + (a × c)**
        
        #### 🔹 **How to Read the Equation:**
        When you see: **(3 × 4) + (3 × 2) = 3 × (4 + ___)**
        - **Left side:** The expanded form - multiply each number separately
        - **Right side:** The factored form - factor out the common number
        
        #### 🔹 **Finding the Missing Number:**
        1. **Look at the left side** - identify what's being added: (3 × 4) + (3 × 2)
        2. **Find the common factor** - both terms have 3, so factor it out: 3 × (something)
        3. **What's left?** The numbers being multiplied by 3: 4 and 2
        4. **Missing number** is the second addend: 4 + **2**
        
        ### 📊 **Step-by-Step Examples:**
        
        #### **Example 1: Missing addend**
        ```
        Problem: (5 × 6) + (5 × 3) = 5 × (6 + ___)
        
        Step 1: Look at left side - (5 × 6) + (5 × 3)
        Step 2: Common factor is 5
        Step 3: Numbers being multiplied: 6 and 3  
        Step 4: So: 5 × (6 + 3)
        Step 5: Missing number = 3
        ```
        
        #### **Example 2: Missing common factor**
        ```
        Problem: (3 × 40) + (3 × 2) = ___ × 42
        
        Step 1: Calculate left side - (3 × 40) + (3 × 2) = 120 + 6 = 126
        Step 2: Look at right side - ___ × 42 = 126
        Step 3: What times 42 equals 126? → 126 ÷ 42 = 3
        Step 4: Check: Does 40 + 2 = 42? ✓
        Step 5: Missing factor = 3
        ```
        
        ### 🎯 **Different Question Types:**
        
        #### **Type 1: Missing addend in parentheses**
        - **Missing second addend:** (4 × 2) + (4 × 7) = 4 × (2 + ___)
        - **Missing first addend:** (6 × 5) + (6 × 3) = 6 × (___ + 3)
        
        #### **Type 2: Missing common factor**
        - **Missing factor:** (3 × 40) + (3 × 2) = ___ × 42
        - **Missing factor:** (9 × 2) + (9 × 5) = ___ × 7
        
        For Type 2, you need to:
        1. **Calculate the sum inside:** 40 + 2 = 42, or 2 + 5 = 7
        2. **Find what factor** was taken out from both terms
        3. **Check:** Does that factor times the sum equal the left side?
        
        ### 💡 **Tips for Success:**
        - **Find the common factor** first (the number that appears in both multiplications)
        - **Identify what's being added** inside the parentheses on the left
        - **Match the pattern** - the same numbers should appear on both sides
        - **Check your work** - substitute your answer back into the equation
        
        ### 🏆 **Why This Property Matters:**
        - **Mental math shortcuts** - makes calculations easier
        - **Algebraic thinking** - foundation for working with variables
        - **Problem solving** - breaking down complex problems
        - **Real-world applications** - calculating areas, costs, and more
        """)

def generate_new_question():
    """Generate a new distributive property question"""
    difficulty = st.session_state.distributive_difficulty
    
    # Choose question type (where the missing number appears)
    question_types = ["missing_second_addend", "missing_first_addend", "missing_common_factor"]
    question_type = random.choice(question_types)
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        # Basic: single digits, easier calculations
        factor_options = [2, 3, 4, 5, 6]
        addend_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    elif difficulty == 2:
        # Intermediate: mix of single and two digits
        factor_options = [2, 3, 4, 5, 6, 7, 8, 9]
        addend_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    else:  # difficulty == 3
        # Advanced: larger numbers
        factor_options = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        addend_options = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    # Generate the components
    common_factor = random.choice(factor_options)
    first_addend = random.choice(addend_options)
    second_addend = random.choice([x for x in addend_options if x != first_addend])
    
    # Calculate products for the left side
    first_product = common_factor * first_addend
    second_product = common_factor * second_addend
    total_sum = first_addend + second_addend
    
    if question_type == "missing_second_addend":
        # Format: (a × b) + (a × c) = a × (b + ___)
        # Missing the second addend
        missing_number = second_addend
        left_side = f"({common_factor} × {first_addend}) + ({common_factor} × {second_addend})"
        right_side = f"{common_factor} × ({first_addend} + ___)"
        position_description = "second addend"
        
    elif question_type == "missing_first_addend":
        # Format: (a × b) + (a × c) = a × (___ + c)  
        # Missing the first addend
        missing_number = first_addend
        left_side = f"({common_factor} × {first_addend}) + ({common_factor} × {second_addend})"
        right_side = f"{common_factor} × (___ + {second_addend})"
        position_description = "first addend"
        
    else:  # missing_common_factor
        # Format: (a × b) + (a × c) = ___ × (b + c)
        # Missing the common factor
        missing_number = common_factor
        left_side = f"({common_factor} × {first_addend}) + ({common_factor} × {second_addend})"
        right_side = f"___ × {total_sum}"
        position_description = "common factor"
    
    st.session_state.question_data_dist = {
        "common_factor": common_factor,
        "first_addend": first_addend,
        "second_addend": second_addend,
        "first_product": first_product,
        "second_product": second_product,
        "total_sum": total_sum,
        "left_side": left_side,
        "right_side": right_side,
        "question_type": question_type,
        "position_description": position_description
    }
    
    st.session_state.correct_answer_dist = missing_number
    st.session_state.current_question_dist = "Use the distributive property of multiplication to find the missing number."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data_dist
    
    # Display question
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question_dist}**")
    
    # Display the equation in a nice format
    st.markdown("### 📋 Equation:")
    
    # Create the equation display
    equation_html = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 30px; 
        border-radius: 10px; 
        border: 2px solid #dee2e6;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #495057;
        margin: 20px 0;
        font-family: 'Courier New', monospace;
    ">
        {data['left_side']} = {data['right_side']}
    </div>
    """
    
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Input section
    with st.form("distributive_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("**Enter the missing number:**")
            user_answer = st.number_input(
                "Missing number:",
                min_value=0,
                max_value=100,
                value=None,
                step=1,
                key="missing_number_input",
                placeholder="Enter the missing number",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer_dist = int(user_answer)
            st.session_state.show_feedback_dist = True
            st.session_state.answer_submitted_dist = True
            st.session_state.total_questions_dist += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback_dist:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted_dist:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer_dist
    correct_answer = st.session_state.correct_answer_dist
    data = st.session_state.question_data_dist
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.distributive_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions_dist % 5 == 0:  # Every 5 questions
            accuracy = st.session_state.distributive_score / st.session_state.total_questions_dist
            if accuracy >= 0.8 and st.session_state.distributive_difficulty < 3:
                old_difficulty = st.session_state.distributive_difficulty
                st.session_state.distributive_difficulty += 1
                if old_difficulty < st.session_state.distributive_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.distributive_difficulty}**")
                    if st.session_state.distributive_difficulty == 3:
                        st.balloons()
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty if struggling
        if st.session_state.total_questions_dist % 5 == 0:  # Every 5 questions
            accuracy = st.session_state.distributive_score / st.session_state.total_questions_dist
            if accuracy < 0.4 and st.session_state.distributive_difficulty > 1:
                old_difficulty = st.session_state.distributive_difficulty
                st.session_state.distributive_difficulty = max(st.session_state.distributive_difficulty - 1, 1)
                if old_difficulty > st.session_state.distributive_difficulty:
                    st.warning(f"⬇️ **Let's practice easier problems. Back to Level {st.session_state.distributive_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the distributive property solution"""
    data = st.session_state.question_data_dist
    correct_answer = st.session_state.correct_answer_dist
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Original equation:** {data['left_side']} = {data['right_side']}
        
        #### 🔍 **Step 1: Analyze the left side**
        - **First term:** {data['common_factor']} × {data['first_addend']} = {data['first_product']}
        - **Second term:** {data['common_factor']} × {data['second_addend']} = {data['second_product']}
        - **Total:** {data['first_product']} + {data['second_product']} = {data['first_product'] + data['second_product']}
        """)
        
        if data['question_type'] == "missing_common_factor":
            st.markdown(f"""
            #### 🎯 **Step 2: Apply the distributive property (factoring)**
            To factor out the common multiplier from: ({data['common_factor']} × {data['first_addend']}) + ({data['common_factor']} × {data['second_addend']})
            
            - **Look for the common factor:** Both terms have {data['common_factor']} being multiplied
            - **Factor it out:** {data['common_factor']} × ({data['first_addend']} + {data['second_addend']})
            - **Simplify inside parentheses:** {data['common_factor']} × {data['total_sum']}
            
            #### ✅ **Step 3: Find the missing factor**
            We need: ___ × {data['total_sum']} = {data['first_product'] + data['second_product']}
            
            **What number times {data['total_sum']} equals {data['first_product'] + data['second_product']}?**
            
            {data['first_product'] + data['second_product']} ÷ {data['total_sum']} = {correct_answer}
            
            **Therefore, the missing common factor is {correct_answer}.**
            """)
        else:
            st.markdown(f"""
            #### 🎯 **Step 2: Apply the distributive property**
            The distributive property says: **a × (b + c) = (a × b) + (a × c)**
            
            In our case:
            - **Common factor (a):** {data['common_factor']}
            - **First number (b):** {data['first_addend']}  
            - **Second number (c):** {data['second_addend']}
            
            #### ✅ **Step 3: Complete the factored form**
            {data['common_factor']} × ({data['first_addend']} + {data['second_addend']}) = {data['common_factor']} × {data['total_sum']} = {data['common_factor'] * data['total_sum']}
            
            **Therefore, the missing {data['position_description']} is {correct_answer}.**
            """)
        
        st.markdown(f"""
        #### 🔄 **Step 4: Verify the answer**
        **Left side:** ({data['common_factor']} × {data['first_addend']}) + ({data['common_factor']} × {data['second_addend']}) = {data['first_product']} + {data['second_product']} = {data['first_product'] + data['second_product']}
        
        **Right side:** {data['common_factor']} × {data['total_sum']} = {data['common_factor'] * data['total_sum']}
        
        ✅ **Both sides equal {data['first_product'] + data['second_product']}, so our answer is correct!**
        
        ### 💡 **Key Insight:**
        The distributive property works in **both directions**:
        - **Expanding:** a × (b + c) → (a × b) + (a × c) 
        - **Factoring:** (a × b) + (a × c) → a × (b + c)
        
        This flexibility makes it a powerful tool for mental math and algebraic thinking!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question_dist = None
    st.session_state.correct_answer_dist = None
    st.session_state.show_feedback_dist = False
    st.session_state.answer_submitted_dist = False
    st.session_state.question_data_dist = {}
    
    # Clear input values
    if "missing_number_input" in st.session_state:
        del st.session_state.missing_number_input
    if "user_answer_dist" in st.session_state:
        del st.session_state.user_answer_dist