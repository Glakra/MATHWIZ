import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Fractions of a Number practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/fractions_of_a_number.py
    """
    # Initialize session state for difficulty and game state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🔢 Fractions of a Number")
    st.markdown("*Find what fraction of a number equals*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Unit fractions (1/2, 1/3, 1/4...)",
            2: "Simple fractions (2/3, 3/4...)",
            3: "Improper fractions (5/4, 7/3...)",
            4: "Complex fractions (7/8, 11/12...)",
            5: "Mixed calculations"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
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
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        - **Read the fraction** and the number
        - **Multiply** the fraction by the number
        - **Simplify** if needed
        
        ### Examples:
        - **1/2 of 8** = 1/2 × 8 = 8 ÷ 2 = **4**
        - **2/3 of 9** = 2/3 × 9 = (2 × 9) ÷ 3 = 18 ÷ 3 = **6**
        - **3/4 of 12** = 3/4 × 12 = (3 × 12) ÷ 4 = 36 ÷ 4 = **9**
        
        ### Quick Method:
        1. **Divide** the number by the denominator (bottom number)
        2. **Multiply** the result by the numerator (top number)
        
        ### Example: 2/5 of 15
        1. 15 ÷ 5 = 3
        2. 3 × 2 = 6
        So 2/5 of 15 = **6**
        
        ### Difficulty Levels:
        - **🟢 Level 1:** Unit fractions (1/2, 1/3, 1/4)
        - **🟢 Level 2:** Simple fractions (2/3, 3/4)
        - **🟡 Level 3:** Improper fractions (5/4, 7/3)
        - **🔴 Level 4:** Complex fractions (7/8, 11/12)
        - **🔴 Level 5:** Mixed calculations
        """)

def generate_new_question():
    """Generate a new fractions of a number question"""
    difficulty = st.session_state.fractions_difficulty
    
    if difficulty == 1:
        # Unit fractions with easy numbers
        denominators = [2, 3, 4, 5, 6, 8, 10]
        denominator = random.choice(denominators)
        numerator = 1
        # Choose a number that's divisible by the denominator
        multiplier = random.randint(1, 12)
        number = denominator * multiplier
        
    elif difficulty == 2:
        # Simple proper fractions
        denominator = random.choice([3, 4, 5, 6, 8, 10, 12])
        numerator = random.randint(2, denominator - 1)
        # Ensure the fraction can be simplified sometimes
        if random.random() < 0.3:
            gcd = get_gcd(numerator, denominator)
            if gcd > 1:
                numerator //= gcd
                denominator //= gcd
        multiplier = random.randint(1, 15)
        number = denominator * multiplier
        
    elif difficulty == 3:
        # Include improper fractions
        denominator = random.choice([2, 3, 4, 5, 6, 8])
        numerator = random.randint(denominator + 1, denominator * 2)
        multiplier = random.randint(1, 10)
        number = denominator * multiplier
        
    elif difficulty == 4:
        # Complex fractions with larger numbers
        denominator = random.choice([7, 8, 9, 11, 12, 15, 16])
        numerator = random.randint(1, denominator - 1)
        # Sometimes use numbers that don't divide evenly
        if random.random() < 0.5:
            number = random.randint(10, 50)
        else:
            multiplier = random.randint(2, 8)
            number = denominator * multiplier
            
    else:  # difficulty == 5
        # Mixed calculations - any fraction, any number
        denominator = random.randint(2, 20)
        numerator = random.randint(1, denominator * 2)
        number = random.randint(10, 100)
    
    # Calculate the correct answer
    fraction = Fraction(numerator, denominator)
    result = fraction * number
    
    # If result is a whole number, convert it
    if result.denominator == 1:
        correct_answer = result.numerator
    else:
        correct_answer = float(result)
    
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "number": number,
        "fraction_str": f"{numerator}/{denominator}"
    }
    st.session_state.correct_answer = correct_answer if isinstance(correct_answer, int) else round(correct_answer, 2)
    st.session_state.current_question = f"What number is {numerator}/{denominator} of {number}?"

def get_gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    
    # Display the question in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #4169e1;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #2c3e50;
    ">
        What number is <span style="color: #e74c3c; font-size: 28px;">{data['fraction_str']}</span> 
        of <span style="color: #27ae60; font-size: 28px;">{data['number']}</span>?
    </div>
    """, unsafe_allow_html=True)
    
    # Visual representation for lower difficulties
    if st.session_state.fractions_difficulty <= 2:
        show_visual_representation(data)
    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Number input for answer
            user_answer = st.number_input(
                "Enter your answer:",
                min_value=0.0,
                max_value=10000.0,
                step=0.01,
                format="%.2f",
                key="fraction_answer_input",
                label_visibility="collapsed",
                placeholder="Type your answer here..."
            )
            
            # Submit button
            submit_button = st.form_submit_button(
                "✅ Submit Answer", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def show_visual_representation(data):
    """Show visual representation for easier understanding"""
    numerator = data['numerator']
    denominator = data['denominator']
    number = data['number']
    
    # Only show visual for numbers that divide evenly and are not too large
    if number % denominator == 0 and number <= 24 and denominator <= 8:
        st.markdown("#### Visual Helper:")
        
        # Create a visual representation using columns
        items_per_group = number // denominator
        
        # Show the division
        cols = st.columns(denominator)
        for i in range(denominator):
            with cols[i]:
                if i < numerator:
                    st.markdown(f"""
                    <div style="
                        background-color: #3498db;
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                        margin: 2px;
                    ">
                        {items_per_group}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        background-color: #ecf0f1;
                        color: #7f8c8d;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                        margin: 2px;
                    ">
                        {items_per_group}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.caption(f"The number {number} divided into {denominator} equal groups of {items_per_group}. We take {numerator} group(s).")

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
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Handle floating point comparison with tolerance
    if isinstance(correct_answer, float):
        # Allow for small rounding differences
        is_correct = abs(user_answer - correct_answer) < 0.01
    else:
        # For integers, also accept the exact decimal equivalent
        is_correct = (user_answer == correct_answer) or (abs(user_answer - correct_answer) < 0.01)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the calculation
        data = st.session_state.question_data
        st.info(f"✓ {data['fraction_str']} of {data['number']} = **{correct_answer}**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = min(
            st.session_state.fractions_difficulty + 1, 5
        )
        
        if st.session_state.fractions_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've reached the highest level!**")
        elif old_difficulty < st.session_state.fractions_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.fractions_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** You entered: {user_answer}")
        st.error(f"The correct answer is **{correct_answer}**")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = max(
            st.session_state.fractions_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.fractions_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.fractions_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    data = st.session_state.question_data
    numerator = data['numerator']
    denominator = data['denominator']
    number = data['number']
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **See step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Finding {numerator}/{denominator} of {number}
        
        **Method 1: Multiply fraction by number**
        
        {numerator}/{denominator} × {number} = ({numerator} × {number}) ÷ {denominator}
        
        = {numerator * number} ÷ {denominator}
        
        = **{correct_answer}**
        
        ---
        
        **Method 2: Divide then multiply**
        
        Step 1: Divide {number} by {denominator} = {number} ÷ {denominator} = {number/denominator:.2f}
        
        Step 2: Multiply by {numerator} = {number/denominator:.2f} × {numerator} = **{correct_answer}**
        
        ---
        
        **Understanding:**
        - The fraction {numerator}/{denominator} means "{numerator} parts out of {denominator} equal parts"
        - So we divide {number} into {denominator} equal parts
        - Then we take {numerator} of those parts
        """)
        
        # Visual explanation for simple cases
        if number % denominator == 0:
            part_size = number // denominator
            st.markdown(f"""
            **Visual breakdown:**
            - Each part = {number} ÷ {denominator} = {part_size}
            - We need {numerator} parts = {part_size} × {numerator} = **{correct_answer}**
            """)
        
        # Common mistakes to avoid
        st.markdown("""
        ---
        **Common Mistakes to Avoid:**
        - ❌ Don't just divide by the denominator - remember to multiply by the numerator!
        - ❌ Don't multiply the whole number by the numerator only
        - ✅ Always multiply the fraction by the number: (numerator × number) ÷ denominator
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer