import streamlit as st
import random

def run():
    """
    Main function to run the Relationship between Decimal Place Values practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/relationship_between_decimal_place_values.py
    """
    # Initialize session state for difficulty and game state
    if "decimal_relationship_difficulty" not in st.session_state:
        st.session_state.decimal_relationship_difficulty = 1  # Start with simple relationships
    
    if "current_relationship_question" not in st.session_state:
        st.session_state.current_relationship_question = None
        st.session_state.relationship_correct_answer = None
        st.session_state.relationship_show_feedback = False
        st.session_state.relationship_answer_submitted = False
        st.session_state.relationship_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Relationship between Decimal Place Values")
    st.markdown("*Understand how decimal place values relate to each other*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_relationship_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_relationship_question is None:
        generate_new_relationship_question()
    
    # Display current question
    display_relationship_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Decimal Place Value Relationships**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Complete the sentence** about place value relationships
        - **Type the missing number** in the text box
        - **Think about 10× and 1/10 relationships** between place values
        
        ### Key Concept: The "×10" and "÷10" Pattern
        
        #### **Moving Left = ×10 (10 times as much)**
        ```
        0.006 → 0.06 → 0.6 → 6 → 60
         ×10     ×10    ×10   ×10
        ```
        
        #### **Moving Right = ÷10 (1/10 as much)**
        ```
        60 → 6 → 0.6 → 0.06 → 0.006
         ÷10   ÷10    ÷10     ÷10
        ```
        
        ### Understanding the Relationships:
        
        #### **"10 times as much" Examples:**
        - **6** is 10 times as much as **0.6**
        - **0.6** is 10 times as much as **0.06**
        - **60** is 10 times as much as **6**
        - **0.05** is 10 times as much as **0.005**
        
        #### **"1/10 as much" Examples:**
        - **0.6** is 1/10 as much as **6**
        - **0.06** is 1/10 as much as **0.6**
        - **6** is 1/10 as much as **60**
        - **0.005** is 1/10 as much as **0.05**
        
        ### Place Value Chart:
        ```
        Hundreds | Tens | Ones | . | Tenths | Hundredths | Thousandths
           100     10     1    .    0.1       0.01        0.001
        ```
        **Each place is 10× the place to its right**
        
        ### Tips for Success:
        
        #### **For "10 times as much":**
        - **Move the decimal point LEFT one place**
        - **0.6 → 6** (move left = ×10)
        - **0.06 → 0.6** (move left = ×10)
        
        #### **For "1/10 as much":**
        - **Move the decimal point RIGHT one place**
        - **6 → 0.6** (move right = ÷10)
        - **0.6 → 0.06** (move right = ÷10)
        
        #### **Quick Check Method:**
        - **Multiply by 10:** Add a zero OR move decimal left
        - **Divide by 10:** Remove a zero OR move decimal right
        
        ### Common Patterns:
        - **Whole number × 10 = bigger whole number** (6 → 60)
        - **Decimal × 10 = decimal or whole** (0.6 → 6)
        - **Number ÷ 10 = smaller number** (6 → 0.6)
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple relationships (0.6 ↔ 6)
        - **🟠 Level 3:** Multiple decimal places (0.06 ↔ 0.6)  
        - **🔴 Level 4-5:** Complex numbers (12.5 ↔ 125)
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master Level 5!
        """)

def generate_new_relationship_question():
    """Generate a new place value relationship question"""
    difficulty = st.session_state.decimal_relationship_difficulty
    
    # Choose relationship type
    relationship_types = ["10_times_as_much", "one_tenth_as_much"]
    relationship_type = random.choice(relationship_types)
    
    # Generate base number based on difficulty
    if difficulty == 1:
        # Level 1: Simple tenths relationships (0.1-0.9 ↔ 1-9)
        base_numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
    elif difficulty == 2:
        # Level 2: Tenths and ones (0.1-0.9 ↔ 1-9, 1-9 ↔ 10-90)
        base_numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                       1, 2, 3, 4, 5, 6, 7, 8, 9]
        
    elif difficulty == 3:
        # Level 3: Include hundredths (0.01-0.99)
        base_numbers = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
                       0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                       1, 2, 3, 4, 5, 6, 7, 8, 9]
        
    elif difficulty == 4:
        # Level 4: Include larger numbers and thousandths
        base_numbers = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
                       1, 2, 5, 10, 20, 50]
        
    else:  # difficulty == 5
        # Level 5: Complex decimal numbers
        base_numbers = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5,
                       1.5, 2.5, 12.5, 25, 125, 250]
    
    base_number = random.choice(base_numbers)
    
    if relationship_type == "10_times_as_much":
        # Answer is 10 times the given number
        given_number = base_number
        answer = base_number * 10
        
        # Format numbers properly
        given_str = format_number(given_number)
        answer_str = format_number(answer)
        
        question_text = f"Complete the sentence."
        sentence_text = f"is 10 times as much as {given_str}."
        
    else:  # one_tenth_as_much
        # Answer is 1/10 of the given number
        given_number = base_number * 10  # So the answer will be the base_number
        answer = base_number
        
        # Format numbers properly
        given_str = format_number(given_number)
        answer_str = format_number(answer)
        
        question_text = f"Complete the sentence."
        sentence_text = f"is 1/10 as much as {given_str}."
    
    st.session_state.relationship_question_data = {
        "relationship_type": relationship_type,
        "given_number": given_str,
        "answer": answer_str,
        "sentence_text": sentence_text,
        "question_text": question_text
    }
    st.session_state.relationship_correct_answer = answer_str
    st.session_state.current_relationship_question = question_text

def format_number(num):
    """Format number to remove unnecessary trailing zeros"""
    if num == int(num):
        return str(int(num))
    else:
        # Remove trailing zeros from decimal
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        return formatted

def display_relationship_question():
    """Display the current question interface"""
    data = st.session_state.relationship_question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{data['question_text']}**")
    
    # Display the sentence with input box
    sentence_parts = data['sentence_text'].split(' ', 1)  # Split after first word
    remaining_text = sentence_parts[0] if len(sentence_parts) > 0 else ""
    
    # Create the sentence completion interface
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create columns for the sentence layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Input and submit in a form
        with st.form("relationship_form", clear_on_submit=False):
            # Create the sentence with input box
            cols = st.columns([2, 5])
            
            with cols[0]:
                user_input = st.text_input(
                    "Answer:",
                    placeholder="Enter number",
                    label_visibility="collapsed",
                    key="relationship_input"
                )
            
            with cols[1]:
                st.markdown(f"""
                <div style="
                    padding: 8px 0;
                    font-size: 18px;
                    line-height: 1.6;
                ">
                    {data['sentence_text']}
                </div>
                """, unsafe_allow_html=True)
            
            # Submit button
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit_button and user_input.strip():
                st.session_state.relationship_user_answer = user_input.strip()
                st.session_state.relationship_show_feedback = True
                st.session_state.relationship_answer_submitted = True
    
    # Show feedback and next button
    handle_relationship_feedback_and_next()

def handle_relationship_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.relationship_show_feedback:
        show_relationship_feedback()
    
    # Next question button
    if st.session_state.relationship_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_relationship_state()
                st.rerun()

def show_relationship_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.relationship_user_answer
    correct_answer = st.session_state.relationship_correct_answer
    data = st.session_state.relationship_question_data
    
    # Check if answer is correct (allow for different valid formats)
    is_correct = check_number_answer(user_answer, correct_answer)
    
    st.markdown("---")
    st.markdown("### 📋 Results:")
    
    if is_correct:
        st.success("🎉 **Perfect! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.decimal_relationship_difficulty
        st.session_state.decimal_relationship_difficulty = min(
            st.session_state.decimal_relationship_difficulty + 1, 5
        )
        
        if st.session_state.decimal_relationship_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decimal place value relationships!**")
        elif old_difficulty < st.session_state.decimal_relationship_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decimal_relationship_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.decimal_relationship_difficulty
        st.session_state.decimal_relationship_difficulty = max(
            st.session_state.decimal_relationship_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimal_relationship_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.decimal_relationship_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_relationship_explanation(is_correct)

def check_number_answer(user_input, correct_answer):
    """Check if user's number input is correct (allowing for format variations)"""
    try:
        # Convert both to float for comparison
        user_float = float(user_input)
        correct_float = float(correct_answer)
        
        # Check if they're equal (within small tolerance for floating point)
        return abs(user_float - correct_float) < 0.000001
        
    except (ValueError, TypeError):
        # Invalid input format
        return False

def show_relationship_explanation(correct=True):
    """Show detailed explanation"""
    data = st.session_state.relationship_question_data
    user_answer = st.session_state.relationship_user_answer
    correct_answer = st.session_state.relationship_correct_answer
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Understanding the Relationship:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        relationship_type = data["relationship_type"]
        given_number = data["given_number"]
        
        st.markdown(f"""
        ### 🔢 **Question Analysis:**
        - **Given number:** {given_number}
        - **Correct answer:** {correct_answer}
        - **Your answer:** {user_answer}
        """)
        
        if relationship_type == "10_times_as_much":
            st.markdown(f"""
            ### 📈 **"10 times as much" means ×10:**
            
            **Method 1: Multiplication**
            - {given_number} × 10 = **{correct_answer}**
            
            **Method 2: Decimal Point Movement**
            - Move decimal point **LEFT one place** to multiply by 10
            - {given_number} → **{correct_answer}**
            
            ### 🎯 **Why this works:**
            - Each place value is **10 times** the place to its right
            - Moving left = making the number **10 times bigger**
            """)
            
            # Show place value visualization
            show_place_value_movement(given_number, correct_answer, "multiply")
            
        else:  # one_tenth_as_much
            st.markdown(f"""
            ### 📉 **"1/10 as much" means ÷10:**
            
            **Method 1: Division**
            - {given_number} ÷ 10 = **{correct_answer}**
            
            **Method 2: Decimal Point Movement**
            - Move decimal point **RIGHT one place** to divide by 10
            - {given_number} → **{correct_answer}**
            
            ### 🎯 **Why this works:**
            - Each place value is **1/10** the place to its left
            - Moving right = making the number **10 times smaller**
            """)
            
            # Show place value visualization
            show_place_value_movement(given_number, correct_answer, "divide")
        
        st.markdown("""
        ### 💡 **Quick Memory Tips:**
        - **×10:** Decimal moves **LEFT** (number gets bigger)
        - **÷10:** Decimal moves **RIGHT** (number gets smaller)
        - **Think:** LEFT = Larger, RIGHT = tinieR
        """)

def show_place_value_movement(start_num, end_num, operation):
    """Show visual representation of decimal point movement"""
    st.markdown("#### 🔄 **Decimal Point Movement:**")
    
    if operation == "multiply":
        arrow = "←"
        description = "Move LEFT to multiply by 10"
    else:
        arrow = "→"
        description = "Move RIGHT to divide by 10"
    
    st.markdown(f"""
    ```
    {start_num}  {arrow}  {end_num}
    ```
    **{description}**
    """)
    
    # Show the pattern
    if operation == "multiply":
        st.markdown(f"""
        ### 📊 **The ×10 Pattern:**
        - {start_num} × 10 = {end_num}
        - Notice how the digits stay the same, but move to higher place values
        """)
    else:
        st.markdown(f"""
        ### 📊 **The ÷10 Pattern:**
        - {start_num} ÷ 10 = {end_num}
        - Notice how the digits stay the same, but move to lower place values
        """)

def reset_relationship_state():
    """Reset state for next question"""
    st.session_state.current_relationship_question = None
    st.session_state.relationship_correct_answer = None
    st.session_state.relationship_show_feedback = False
    st.session_state.relationship_answer_submitted = False
    st.session_state.relationship_question_data = {}
    
    # Clear any stored answers
    if "relationship_user_answer" in st.session_state:
        del st.session_state.relationship_user_answer