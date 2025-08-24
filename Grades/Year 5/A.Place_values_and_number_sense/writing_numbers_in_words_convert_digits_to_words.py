import streamlit as st
import random

def run():
    """
    Main function to run the Convert Digits to Words practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/writing_numbers_in_words_convert_digits_to_words.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "digits_to_words_difficulty" not in st.session_state:
        st.session_state.digits_to_words_difficulty = 3  # Start with 3-digit numbers
    
    if "digits_to_words_current_question" not in st.session_state:
        st.session_state.digits_to_words_current_question = None
        st.session_state.digits_to_words_correct_answer = None
        st.session_state.digits_to_words_show_feedback = False
        st.session_state.digits_to_words_answer_submitted = False
        st.session_state.digits_to_words_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📝 Convert Digits to Words")
    st.markdown("*Read number digits and write them as words*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.digits_to_words_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (2 to 6 digits)
        progress = (difficulty_level - 2) / 4  # Convert 2-6 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level <= 3:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 4:
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
    if st.session_state.digits_to_words_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the number written in digits**
        - **Choose the correct word form** from the options
        - **Think about place values** - thousands, hundreds, tens, ones
        
        ### Tips for Success:
        - **Break it down:** 2,300 = "two thousand three hundred"
        - **Watch for zero:** 2,005 = "two thousand five" (not "two thousand and five")
        - **No "and":** 205 = "two hundred five" not "two hundred and five"
        
        ### Examples:
        - **47** → "forty-seven"
        - **312** → "three hundred twelve"  
        - **2,006** → "two thousand six"
        - **15,400** → "fifteen thousand four hundred"
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** (10s - 100s)
        - **🟠 4-5 digit numbers:** (1,000s - 10,000s)  
        - **🔴 6 digit numbers:** (100,000s)
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 6-digit numbers!
        """)

def number_to_words(n):
    """Convert a number to its word representation"""
    if n == 0:
        return "zero"
    
    # Define word mappings
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
            "seventeen", "eighteen", "nineteen"]
    
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def convert_hundreds(num):
        result = ""
        
        # Handle hundreds
        if num >= 100:
            result += ones[num // 100] + " hundred"
            num %= 100
            if num > 0:
                result += " "
        
        # Handle tens and ones
        if num >= 20:
            result += tens[num // 10]
            if num % 10 != 0:
                result += "-" + ones[num % 10]
        elif num > 0:
            result += ones[num]
        
        return result
    
    if n < 1000:
        return convert_hundreds(n)
    elif n < 1000000:
        thousands = n // 1000
        remainder = n % 1000
        result = convert_hundreds(thousands) + " thousand"
        if remainder > 0:
            result += " " + convert_hundreds(remainder)
        return result
    else:
        # Handle up to millions (for difficulty level 6)
        millions = n // 1000000
        remainder = n % 1000000
        result = convert_hundreds(millions) + " million"
        if remainder >= 1000:
            thousands = remainder // 1000
            result += " " + convert_hundreds(thousands) + " thousand"
            remainder %= 1000
        if remainder > 0:
            result += " " + convert_hundreds(remainder)
        return result

def generate_new_question():
    """Generate a new digits to words question"""
    digits = st.session_state.digits_to_words_difficulty
    
    # Generate a random number with the specified number of digits
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    correct_number = random.randint(min_val, max_val)
    
    # Convert to words
    correct_word_form = number_to_words(correct_number)
    
    # Generate smart distractors (wrong word forms)
    options = [correct_word_form]
    attempts = 0
    while len(options) < 4 and attempts < 20:  # Prevent infinite loop
        # Create variations by generating similar numbers
        variation = random.choice([
            random.randint(-50, 50),  # Small variations
            random.randint(-500, 500),  # Medium variations
            correct_number // 10,  # Remove a digit
            correct_number * 10 % (10**digits),  # Add a digit (if within range)
        ])
        
        wrong_number = correct_number + variation
        
        # Make sure wrong number is valid and unique
        if (wrong_number != correct_number and 
            min_val <= wrong_number < max_val and
            wrong_number > 0):
            wrong_word_form = number_to_words(wrong_number)
            if wrong_word_form not in options:
                options.append(wrong_word_form)
        
        attempts += 1
    
    # If we couldn't generate enough distractors, add some simple ones
    while len(options) < 4:
        wrong_number = random.randint(min_val, max_val)
        wrong_word_form = number_to_words(wrong_number)
        if wrong_word_form not in options:
            options.append(wrong_word_form)
    
    # Shuffle the options
    random.shuffle(options)
    
    st.session_state.digits_to_words_question_data = {
        "digit_form": correct_number,
        "options": options
    }
    st.session_state.digits_to_words_correct_answer = correct_word_form
    st.session_state.digits_to_words_current_question = f"How do you write this number in words?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.digits_to_words_question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.digits_to_words_current_question}**")
    
    # Display the digit form in a highlighted box
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
        {data['digit_form']:,}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Choose the correct word form:**")
        
        # Create radio button options
        user_answer = st.radio(
            "Select your answer:",
            options=data['options'],
            key="digits_to_words_choice",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.digits_to_words_user_answer = user_answer
            st.session_state.digits_to_words_show_feedback = True
            st.session_state.digits_to_words_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.digits_to_words_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.digits_to_words_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.digits_to_words_user_answer
    correct_answer = st.session_state.digits_to_words_correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 6 digits)
        old_difficulty = st.session_state.digits_to_words_difficulty
        st.session_state.digits_to_words_difficulty = min(
            st.session_state.digits_to_words_difficulty + 1, 6
        )
        
        # Show encouragement based on difficulty
        if st.session_state.digits_to_words_difficulty == 6 and old_difficulty < 6:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 6-digit number conversion!**")
        elif old_difficulty < st.session_state.digits_to_words_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.digits_to_words_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.digits_to_words_difficulty
        st.session_state.digits_to_words_difficulty = max(
            st.session_state.digits_to_words_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.digits_to_words_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.digits_to_words_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_number = st.session_state.digits_to_words_question_data['digit_form']
    correct_word_form = st.session_state.digits_to_words_correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step conversion:
        
        **Digit form:** {correct_number:,}
        **Word form:** {correct_word_form}
        
        ### How to break it down:
        """)
        
        # Break down the number by place value
        breakdown = []
        temp = correct_number
        
        if temp >= 1000000:
            millions = temp // 1000000
            breakdown.append(f"**{millions * 1000000:,}** = {millions} million")
            temp %= 1000000
            
        if temp >= 1000:
            thousands = temp // 1000
            breakdown.append(f"**{thousands * 1000:,}** = {thousands} thousand")
            temp %= 1000
            
        if temp >= 100:
            hundreds = temp // 100
            breakdown.append(f"**{hundreds * 100}** = {hundreds} hundred")
            temp %= 100
            
        if temp > 0:
            breakdown.append(f"**{temp}** = {number_to_words(temp)}")
        
        for item in breakdown:
            st.markdown(f"- {item}")
        
        if len(breakdown) > 1:
            st.markdown(f"**Combined:** {correct_word_form}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.digits_to_words_current_question = None
    st.session_state.digits_to_words_correct_answer = None
    st.session_state.digits_to_words_show_feedback = False
    st.session_state.digits_to_words_answer_submitted = False
    st.session_state.digits_to_words_question_data = {}
    if "digits_to_words_user_answer" in st.session_state:
        del st.session_state.digits_to_words_user_answer