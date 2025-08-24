import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Round Mixed Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I.Fractions and mixed numbers/round_mixed_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "round_mixed_difficulty" not in st.session_state:
        st.session_state.round_mixed_difficulty = 1  # Start with simple mixed numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🎯 Round Mixed Numbers")
    st.markdown("*Round mixed numbers to the nearest whole number*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.round_mixed_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple fractions (1/2, 1/4, 3/4)",
            2: "Common fractions (thirds, fifths, sixths)",
            3: "Improper mixed numbers",
            4: "Complex fractions (sevenths, ninths)",
            5: "Advanced rounding challenges"
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
        ### Rounding Rules for Mixed Numbers:
        
        **Look at the fraction part:**
        - If fraction = 1/2 or more → **Round UP** ⬆️
        - If fraction < 1/2 → **Round DOWN** ⬇️
        
        ### Examples:
        - **3 1/4** → Fraction is 1/4 (less than 1/2) → Round down to **3**
        - **5 3/4** → Fraction is 3/4 (more than 1/2) → Round up to **6**
        - **2 1/2** → Fraction is exactly 1/2 → Round up to **3**
        - **7 2/5** → Is 2/5 less than 1/2? Yes (2/5 = 0.4) → Round down to **7**
        - **4 5/8** → Is 5/8 more than 1/2? Yes (5/8 = 0.625) → Round up to **5**
        
        ### Quick Comparison to 1/2:
        To compare a fraction to 1/2, cross multiply:
        - For a/b vs 1/2: Check if 2a vs b
        - Example: Is 3/7 > 1/2? Check: 2×3 = 6, and 6 < 7, so NO
        
        ### Special Cases:
        - **Improper mixed numbers** like 4 6/5 = 5 1/5 (simplify first!)
        - **Exactly 1/2** always rounds UP
        
        ### Difficulty Levels:
        - **🟢 Level 1:** Easy fractions (1/2, 1/4, 3/4)
        - **🟢 Level 2:** Common fractions (1/3, 2/3, 1/5, etc.)
        - **🟡 Level 3:** Improper mixed numbers
        - **🔴 Level 4:** Complex fractions
        - **🔴 Level 5:** Advanced challenges
        """)

def generate_new_question():
    """Generate a new round mixed numbers question"""
    difficulty = st.session_state.round_mixed_difficulty
    
    if difficulty == 1:
        # Level 1: Simple fractions that are easy to compare to 1/2
        whole_part = random.randint(1, 10)
        fractions = [
            (1, 4),  # Less than 1/2
            (3, 4),  # Greater than 1/2
            (1, 2),  # Exactly 1/2
            (1, 3),  # Less than 1/2
            (2, 3),  # Greater than 1/2
        ]
        numerator, denominator = random.choice(fractions)
        
    elif difficulty == 2:
        # Level 2: Common fractions with various denominators
        whole_part = random.randint(1, 15)
        denominators = [3, 4, 5, 6, 8, 10]
        denominator = random.choice(denominators)
        numerator = random.randint(1, denominator - 1)
        
    elif difficulty == 3:
        # Level 3: Include improper mixed numbers
        whole_part = random.randint(2, 20)
        denominator = random.choice([2, 3, 4, 5, 6, 8])
        # Sometimes create improper fractions
        if random.random() < 0.5:
            # Improper fraction
            numerator = random.randint(denominator, denominator * 2)
        else:
            # Proper fraction
            numerator = random.randint(1, denominator - 1)
            
    elif difficulty == 4:
        # Level 4: Complex fractions with larger denominators
        whole_part = random.randint(5, 30)
        denominator = random.choice([7, 8, 9, 11, 12, 15, 16])
        numerator = random.randint(1, denominator - 1)
        
    else:  # difficulty == 5
        # Level 5: Advanced challenges including larger numbers
        whole_part = random.randint(10, 50)
        denominator = random.randint(2, 20)
        # Mix of proper and improper fractions
        if random.random() < 0.3:
            numerator = random.randint(denominator, int(denominator * 1.5))
        else:
            numerator = random.randint(1, denominator - 1)
    
    # Simplify the fraction if it's improper
    if numerator >= denominator:
        extra_wholes = numerator // denominator
        numerator = numerator % denominator
        whole_part += extra_wholes
        # Format the improper mixed number for display
        original_improper_num = numerator + extra_wholes * denominator
        fraction_display = f"{whole_part - extra_wholes} {original_improper_num}/{denominator}"
        if numerator > 0:
            simplified_display = f"{whole_part} {numerator}/{denominator}"
        else:
            simplified_display = str(whole_part)
    else:
        fraction_display = f"{whole_part} {numerator}/{denominator}"
        simplified_display = None
    
    # Calculate the correct answer
    # Compare fraction to 1/2
    if numerator == 0:
        correct_answer = whole_part
    elif numerator * 2 >= denominator:  # fraction >= 1/2
        correct_answer = whole_part + 1
    else:  # fraction < 1/2
        correct_answer = whole_part
    
    st.session_state.question_data = {
        "whole_part": whole_part,
        "numerator": numerator,
        "denominator": denominator,
        "mixed_number": fraction_display,
        "simplified": simplified_display,
        "fraction_value": numerator / denominator if numerator > 0 else 0
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"What is {fraction_display} rounded to the nearest whole number?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    
    # Display the question in a highlighted box
    # Escape any special HTML characters in the mixed number
    safe_mixed_number = data['mixed_number'].replace('<', '&lt;').replace('>', '&gt;')
    
    st.markdown(f"""
    <div style="
        background-color: #fff3cd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #ffc107;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #856404;
    ">
        What is <span style="color: #dc3545; font-size: 32px;">{safe_mixed_number}</span> 
        rounded to the nearest whole number?
    </div>
    """, unsafe_allow_html=True)
    
    # Show simplified version if applicable
    if data['simplified']:
        st.info(f"💡 **Hint:** First simplify the improper mixed number: {data['mixed_number']} = {data['simplified']}")
    

    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Number input for answer
            user_answer = st.number_input(
                "Enter the whole number:",
                min_value=0,
                max_value=100,
                step=1,
                key="round_mixed_answer_input",
                label_visibility="collapsed",
                placeholder="Type your answer..."
            )
            
            # Submit button
            submit_button = st.form_submit_button(
                "✅ Submit Answer", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            st.session_state.user_answer = int(user_answer)
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
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.success(f"✓ {data['mixed_number']} rounds to **{correct_answer}**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.round_mixed_difficulty
        st.session_state.round_mixed_difficulty = min(
            st.session_state.round_mixed_difficulty + 1, 5
        )
        
        if st.session_state.round_mixed_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've mastered rounding mixed numbers!**")
        elif old_difficulty < st.session_state.round_mixed_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.round_mixed_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** You answered: {user_answer}")
        st.error(f"The correct answer is **{correct_answer}**")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.round_mixed_difficulty
        st.session_state.round_mixed_difficulty = max(
            st.session_state.round_mixed_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.round_mixed_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.round_mixed_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    data = st.session_state.question_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **See step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Rounding {data['mixed_number']} to the nearest whole number
        """)
        
        # If it was an improper mixed number, show simplification
        if data['simplified']:
            st.markdown(f"""
        **Step 1: Simplify the improper mixed number**
        
        {data['mixed_number']} = {data['simplified']}
        
        (The fraction part was improper, so we converted it to a proper mixed number)
        """)
            
        # Main rounding explanation
        if data['numerator'] == 0:
            st.markdown(f"""
        **The fraction part is 0**
        
        Since there's no fraction part, the number is already whole.
        
        **Answer: {correct_answer}**
        """)
        else:
            st.markdown(f"""
        **Step 2: Compare the fraction part to 1/2**
        
        Fraction part: {data['numerator']}/{data['denominator']}
        
        To compare to 1/2, we can cross multiply:
        - {data['numerator']}/{data['denominator']} vs 1/2
        - {data['numerator']} × 2 vs {data['denominator']} × 1
        - {data['numerator'] * 2} vs {data['denominator']}
        
        Since {data['numerator'] * 2} {"≥" if data['numerator'] * 2 >= data['denominator'] else "<"} {data['denominator']}, 
        the fraction {data['numerator']}/{data['denominator']} is {"≥" if data['numerator'] * 2 >= data['denominator'] else "<"} 1/2
        
        **Step 3: Apply the rounding rule**
        
        {"• Fraction ≥ 1/2 → Round UP ⬆️" if data['numerator'] * 2 >= data['denominator'] else "• Fraction < 1/2 → Round DOWN ⬇️"}
        
        Whole number part: {data['whole_part']}
        {"Round up to: " + str(data['whole_part'] + 1) if data['numerator'] * 2 >= data['denominator'] else "Round down to: " + str(data['whole_part'])}
        
        **Answer: {correct_answer}**
        """)
        
        # Visual number line
        st.markdown("""
        ---
        ### Visual Representation:
        """)
        
        position = "right" if data['fraction_value'] >= 0.5 else "left"
        st.markdown(f"""
        The mixed number {data['mixed_number']} is on the **{position}** side of {data['whole_part']}½
        
        Number line:
        ```
        {data['whole_part']} ←----------|----------→ {data['whole_part'] + 1}
                               ↑                
                            {data['whole_part']}½           
        ```
        
        Since the fraction part is {"greater than or equal to" if data['fraction_value'] >= 0.5 else "less than"} 1/2,
        we round {"UP" if position == "right" else "DOWN"} to **{correct_answer}**
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