import streamlit as st
import random

def run():
    """
    Main function to run the Roman Numerals practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/roman_numerals.py
    """
    # Initialize session state - SAME PATTERN AS WORKING place_values.py
    if "roman_numerals_difficulty" not in st.session_state:
        st.session_state.roman_numerals_difficulty = 100  # Start with max value 100
    
    if "roman_current_question" not in st.session_state:
        st.session_state.roman_current_question = None
        st.session_state.roman_correct_answer = None
        st.session_state.roman_show_feedback = False
        st.session_state.roman_answer_submitted = False
        st.session_state.roman_question_type = None
        st.session_state.roman_number = None
        st.session_state.roman_numeral = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🏛️ Roman Numerals")
    st.markdown("*Convert between decimal numbers and Roman numerals*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.roman_numerals_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Range:** 1 to {difficulty_level}")
        # Progress bar (20 to 1000)
        progress = (difficulty_level - 20) / (1000 - 20)  # Convert 20-1000 to 0-1
        st.progress(progress, text=f"Max value: {difficulty_level}")
    
    with col2:
        if difficulty_level <= 100:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 500:
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
    if st.session_state.roman_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Type 1:** Convert decimal numbers to Roman numerals
        - **Type 2:** Convert Roman numerals to decimal numbers
        - **Type your answer** in the text box
        
        ### Roman Numeral Basics:
        - **I** = 1, **V** = 5, **X** = 10, **L** = 50
        - **C** = 100, **D** = 500, **M** = 1000
        
        ### Important Rules:
        - **Addition:** VI = 5 + 1 = 6
        - **Subtraction:** IV = 5 - 1 = 4, IX = 10 - 1 = 9
        - **Only subtract:** I before V or X, X before L or C, C before D or M
        - **Repeat max 3 times:** III = 3, but not IIII
        
        ### Examples:
        - **4** → IV (not IIII)
        - **9** → IX (not VIIII)
        - **14** → XIV (10 + 4)
        - **19** → XIX (10 + 9)
        - **40** → XL (50 - 10)
        - **90** → XC (100 - 10)
        - **400** → CD (500 - 100)
        - **900** → CM (1000 - 100)
        
        ### Difficulty Levels:
        - **🟡 Beginner:** Numbers 1-100
        - **🟠 Intermediate:** Numbers 1-500  
        - **🔴 Advanced:** Numbers 1-1000
        
        ### Scoring:
        - ✅ **Correct answer:** Range increases
        - ❌ **Wrong answer:** Range decreases
        - 🎯 **Goal:** Master numbers up to 1000!
        """)

def int_to_roman(n):
    """Convert integer to Roman numeral"""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman = ""
    for i in range(len(val)):
        while n >= val[i]:
            roman += syms[i]
            n -= val[i]
    return roman

def roman_to_int(s):
    """Convert Roman numeral to integer"""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
                 'C': 100, 'D': 500, 'M': 1000}
    prev_value = 0
    total = 0
    for char in reversed(s.upper()):
        value = roman_map.get(char, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value
    return total

def generate_new_question():
    """Generate a new Roman numerals question"""
    max_val = st.session_state.roman_numerals_difficulty
    question_type = random.choice(["decimal_to_roman", "roman_to_decimal"])
    number = random.randint(1, max_val)
    roman = int_to_roman(number)
    
    # Store question data in session state
    st.session_state.roman_question_type = question_type
    st.session_state.roman_number = number
    st.session_state.roman_numeral = roman
    
    if question_type == "decimal_to_roman":
        # Type 1: Decimal → Roman
        question_text = f"How would you write **{number}** as a Roman numeral?"
        st.session_state.roman_correct_answer = roman
    else:
        # Type 2: Roman → Decimal
        question_text = f"What number does this Roman numeral represent?"
        st.session_state.roman_correct_answer = str(number)
    
    st.session_state.roman_current_question = question_text

def display_question():
    """Display the current question interface"""
    question_type = st.session_state.roman_question_type
    
    # Display question with nice formatting
    st.markdown("### 🏛️ Question:")
    st.markdown(st.session_state.roman_current_question)
    
    # Display the main content in a highlighted box
    if question_type == "decimal_to_roman":
        # Show the number to convert
        content = str(st.session_state.roman_number)
        placeholder_text = "e.g. XXV"
    else:
        # Show the Roman numeral to convert
        content = st.session_state.roman_numeral
        placeholder_text = "e.g. 25"
    
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #1f77b4;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Type your answer:**")
        
        user_answer = st.text_input(
            "Your answer:",
            placeholder=placeholder_text,
            key="roman_input",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer.strip():
            st.session_state.roman_user_answer = user_answer.strip()
            st.session_state.roman_show_feedback = True
            st.session_state.roman_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.roman_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.roman_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.roman_user_answer
    correct_answer = st.session_state.roman_correct_answer
    question_type = st.session_state.roman_question_type
    
    # Validate answer based on question type
    is_correct = False
    if question_type == "decimal_to_roman":
        is_correct = user_answer.upper() == correct_answer
    else:
        is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 1000)
        old_difficulty = st.session_state.roman_numerals_difficulty
        st.session_state.roman_numerals_difficulty = min(
            st.session_state.roman_numerals_difficulty + 100, 1000
        )
        
        # Show encouragement based on difficulty
        if st.session_state.roman_numerals_difficulty == 1000 and old_difficulty < 1000:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Roman numerals up to 1000!**")
        elif old_difficulty < st.session_state.roman_numerals_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now practicing with numbers up to {st.session_state.roman_numerals_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 20)
        old_difficulty = st.session_state.roman_numerals_difficulty
        st.session_state.roman_numerals_difficulty = max(
            st.session_state.roman_numerals_difficulty - 20, 20
        )
        
        if old_difficulty > st.session_state.roman_numerals_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to range 1-{st.session_state.roman_numerals_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    question_type = st.session_state.roman_question_type
    number = st.session_state.roman_number
    roman = st.session_state.roman_numeral
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "decimal_to_roman":
            st.markdown(f"""
            ### Step-by-step conversion: {number} → {roman}
            
            **Breaking down {number}:**
            """)
            
            # Break down the conversion process
            n = number
            val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
            
            breakdown = []
            for i in range(len(val)):
                count = n // val[i]
                if count > 0:
                    breakdown.append(f"**{count} × {val[i]}** = {syms[i] * count}")
                    n -= val[i] * count
            
            for item in breakdown:
                st.markdown(f"- {item}")
            
            st.markdown(f"**Result:** {roman}")
            
        else:
            st.markdown(f"""
            ### Step-by-step conversion: {roman} → {number}
            
            **Breaking down {roman}:**
            """)
            
            # Analyze the Roman numeral
            roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
            s = roman
            breakdown = []
            
            i = 0
            while i < len(s):
                if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i + 1]]:
                    # Subtraction case
                    value = roman_map[s[i + 1]] - roman_map[s[i]]
                    breakdown.append(f"**{s[i]}{s[i + 1]}** = {roman_map[s[i + 1]]} - {roman_map[s[i]]} = {value}")
                    i += 2
                else:
                    # Addition case
                    breakdown.append(f"**{s[i]}** = {roman_map[s[i]]}")
                    i += 1
            
            for item in breakdown:
                st.markdown(f"- {item}")
            
            st.markdown(f"**Total:** {number}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.roman_current_question = None
    st.session_state.roman_correct_answer = None
    st.session_state.roman_show_feedback = False
    st.session_state.roman_answer_submitted = False
    st.session_state.roman_question_type = None
    st.session_state.roman_number = None
    st.session_state.roman_numeral = None
    if "roman_user_answer" in st.session_state:
        del st.session_state.roman_user_answer
