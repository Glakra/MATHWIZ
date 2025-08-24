import streamlit as st
import random

def run():
    """
    Main function to run the Convert Words to Digits practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/writing_numbers_in_words_convert_words_to_digits.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "words_to_digits_difficulty" not in st.session_state:
        st.session_state.words_to_digits_difficulty = 3  # Start with 3-digit numbers
    
    if "words_to_digits_current_question" not in st.session_state:
        st.session_state.words_to_digits_current_question = None
        st.session_state.words_to_digits_correct_answer = None
        st.session_state.words_to_digits_show_feedback = False
        st.session_state.words_to_digits_answer_submitted = False
        st.session_state.words_to_digits_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📝 Convert Words to Digits")
    st.markdown("*Read number words and write them as digits*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.words_to_digits_difficulty
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
    if st.session_state.words_to_digits_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the number written in words**
        - **Choose the correct digit form** from the options
        - **Think about place values** - thousands, hundreds, tens, ones
        
        ### Tips for Success:
        - **Break it down:** "two thousand three hundred" = 2,000 + 300 = 2,300
        - **Watch for zero:** "two thousand five" = 2,005 (not 2,5)
        - **No "and":** We say "two hundred five" not "two hundred and five"
        
        ### Examples:
        - **"forty-seven"** → 47
        - **"three hundred twelve"** → 312  
        - **"two thousand six"** → 2,006
        - **"fifteen thousand four hundred"** → 15,400
        
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
    """Generate a new words to digits question"""
    digits = st.session_state.words_to_digits_difficulty
    
    # Generate a random number with the specified number of digits
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    correct_number = random.randint(min_val, max_val)
    
    # Convert to words
    word_form = number_to_words(correct_number)
    
    # Generate smart distractors (wrong answers close to the correct one)
    options = [correct_number]
    attempts = 0
    while len(options) < 4 and attempts < 20:  # Prevent infinite loop
        # Create variations by adding/subtracting small amounts
        variation = random.choice([
            random.randint(-50, 50),  # Small variations
            random.randint(-500, 500),  # Medium variations
            correct_number // 10,  # Remove a digit
            correct_number * 10 % (10**digits),  # Add a digit (if within range)
        ])
        
        wrong = correct_number + variation
        
        # Make sure wrong answer is valid and unique
        if (wrong != correct_number and 
            wrong not in options and 
            min_val <= wrong < max_val and
            wrong > 0):
            options.append(wrong)
        
        attempts += 1
    
    # If we couldn't generate enough distractors, add some simple ones
    while len(options) < 4:
        wrong = random.randint(min_val, max_val)
        if wrong not in options:
            options.append(wrong)
    
    # Shuffle the options
    random.shuffle(options)
    
    st.session_state.words_to_digits_question_data = {
        "word_form": word_form,
        "options": options
    }
    st.session_state.words_to_digits_correct_answer = correct_number
    st.session_state.words_to_digits_current_question = f"How do you write this number using digits?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.words_to_digits_question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.words_to_digits_current_question}**")
    
    # Display the word form in a highlighted box
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
        {data['word_form']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Choose the correct digit form:**")
        
        # Create options in a grid layout
        cols = st.columns(2)
        for i, option in enumerate(data['options']):
            col_index = i % 2
            with cols[col_index]:
                # Create radio button options
                if i == 0:
                    user_answer = st.radio(
                        "Select your answer:",
                        options=[f"{opt:,}" for opt in data['options']],
                        key="words_to_digits_choice",
                        label_visibility="collapsed"
                    )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Convert back to integer for comparison
            selected_number = int(user_answer.replace(",", ""))
            st.session_state.words_to_digits_user_answer = selected_number
            st.session_state.words_to_digits_show_feedback = True
            st.session_state.words_to_digits_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.words_to_digits_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.words_to_digits_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.words_to_digits_user_answer
    correct_answer = st.session_state.words_to_digits_correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 6 digits)
        old_difficulty = st.session_state.words_to_digits_difficulty
        st.session_state.words_to_digits_difficulty = min(
            st.session_state.words_to_digits_difficulty + 1, 6
        )
        
        # Show encouragement based on difficulty
        if st.session_state.words_to_digits_difficulty == 6 and old_difficulty < 6:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 6-digit number conversion!**")
        elif old_difficulty < st.session_state.words_to_digits_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.words_to_digits_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer:,}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.words_to_digits_difficulty
        st.session_state.words_to_digits_difficulty = max(
            st.session_state.words_to_digits_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.words_to_digits_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.words_to_digits_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.words_to_digits_correct_answer
    word_form = st.session_state.words_to_digits_question_data['word_form']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step conversion:
        
        **Word form:** {word_form}
        **Digit form:** {correct_answer:,}
        
        ### How to break it down:
        """)
        
        # Break down the number by place value
        breakdown = []
        temp = correct_answer
        
        if temp >= 1000000:
            millions = temp // 1000000
            breakdown.append(f"**{millions} million** = {millions * 1000000:,}")
            temp %= 1000000
            
        if temp >= 1000:
            thousands = temp // 1000
            breakdown.append(f"**{thousands} thousand** = {thousands * 1000:,}")
            temp %= 1000
            
        if temp >= 100:
            hundreds = temp // 100
            breakdown.append(f"**{hundreds} hundred** = {hundreds * 100}")
            temp %= 100
            
        if temp > 0:
            breakdown.append(f"**{temp}** = {temp}")
        
        for item in breakdown:
            st.markdown(f"- {item}")
        
        if len(breakdown) > 1:
            st.markdown(f"**Total:** {' + '.join([str(correct_answer // 1000000 * 1000000) if correct_answer >= 1000000 else '', str((correct_answer % 1000000) // 1000 * 1000) if correct_answer >= 1000 else '', str(correct_answer % 1000)]).strip(' + ')} = **{correct_answer:,}**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.words_to_digits_current_question = None
    st.session_state.words_to_digits_correct_answer = None
    st.session_state.words_to_digits_show_feedback = False
    st.session_state.words_to_digits_answer_submitted = False
    st.session_state.words_to_digits_question_data = {}
    if "words_to_digits_user_answer" in st.session_state:
        del st.session_state.words_to_digits_user_answer