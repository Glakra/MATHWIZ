import streamlit as st
import random

def run():
    """
    Main function to run the Understanding Decimals Expressed in Words practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/understanding_decimals_expressed_in_words.py
    """
    # Initialize session state for difficulty and game state
    if "decimals_words_difficulty" not in st.session_state:
        st.session_state.decimals_words_difficulty = 1  # Start with simple 2-decimal places
    
    if "current_decimals_question" not in st.session_state:
        st.session_state.current_decimals_question = None
        st.session_state.decimals_correct_answer = None
        st.session_state.decimals_show_feedback = False
        st.session_state.decimals_answer_submitted = False
        st.session_state.decimals_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Understanding Decimals Expressed in Words")
    st.markdown("*Read decimal numbers and choose how to write them in words*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimals_words_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** Level {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
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
    if st.session_state.current_decimals_question is None:
        generate_new_decimals_question()
    
    # Display current question
    display_decimals_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Two question types:** Decimal↔Words conversion in both directions
        - **Multiple choice:** Choose the correct words for a decimal number
        - **Text input:** Type the decimal number for given words
        - **Think about place values** - tenths, hundredths, thousandths
        
        ### Tips for Success:
        
        #### **Reading Decimals (Number → Words):**
        - **Say "point"** instead of "decimal point"
        - **Read each digit after the point separately**: 0.92 = "zero point nine two"
        - **Don't say "and"**: We say "zero point five" not "zero and five tenths"
        - **Include zero**: Always start with "zero" for decimals less than 1
        
        #### **Writing Decimals (Words → Number):**
        - **"point" = decimal point (.)**
        - **Each word after "point" = one digit**
        - **"zero" = 0, "one" = 1**, etc.
        - **Keep leading zero**: "zero point five" = 0.5 (not .5)
        
        ### Examples:
        - **0.7** ↔ "zero point seven"
        - **0.25** ↔ "zero point two five"  
        - **0.08** ↔ "zero point zero eight"
        - **1.5** ↔ "one point five"
        - **12.75** ↔ "twelve point seven five"
        
        ### Common Mistakes to Avoid:
        - ❌ Don't say "zero point ninety-two" for 0.92
        - ✅ Say "zero point nine two" for 0.92
        - ❌ Don't write .5 for "zero point five"  
        - ✅ Write 0.5 for "zero point five"
        - ❌ Don't say "point five" for 0.5
        - ✅ Say "zero point five" for 0.5
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple decimals (0.7, 0.25)
        - **🟠 Level 3:** With zeros (0.05, 0.30)  
        - **🔴 Level 4-5:** Whole numbers + decimals (2.45, 15.8)
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master Level 5!
        """)

def decimal_to_words(decimal_str):
    """Convert a decimal number string to its word representation"""
    # Split into whole and decimal parts
    if '.' in decimal_str:
        whole_part, decimal_part = decimal_str.split('.')
    else:
        whole_part = decimal_str
        decimal_part = ""
    
    # Number word mappings
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
            "seventeen", "eighteen", "nineteen"]
    
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def convert_whole_number(num_str):
        """Convert whole number to words"""
        num = int(num_str)
        if num == 0:
            return "zero"
        
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
                result += " " + ones[num % 10]
        elif num > 0:
            result += ones[num]
        
        return result
    
    # Convert whole part
    whole_words = convert_whole_number(whole_part) if whole_part != "0" else "zero"
    
    # Convert decimal part if it exists
    if decimal_part:
        decimal_words = " point"
        for digit in decimal_part:
            if digit == "0":
                decimal_words += " zero"
            elif digit == "1":
                decimal_words += " one"
            elif digit == "2":
                decimal_words += " two"
            elif digit == "3":
                decimal_words += " three"
            elif digit == "4":
                decimal_words += " four"
            elif digit == "5":
                decimal_words += " five"
            elif digit == "6":
                decimal_words += " six"
            elif digit == "7":
                decimal_words += " seven"
            elif digit == "8":
                decimal_words += " eight"
            elif digit == "9":
                decimal_words += " nine"
        
        return whole_words + decimal_words
    else:
        return whole_words

def generate_new_decimals_question():
    """Generate a new decimal question (either decimal→words or words→decimal)"""
    difficulty = st.session_state.decimals_words_difficulty
    
    # Randomly choose question type (50/50 split)
    question_type = random.choice(["decimal_to_words", "words_to_decimal"])
    
    # Generate decimal based on difficulty level
    if difficulty == 1:
        # Level 1: Simple one decimal place (0.1 to 0.9)
        decimal_num = random.randint(1, 9) / 10
        decimal_str = f"{decimal_num:.1f}"
        
    elif difficulty == 2:
        # Level 2: Two decimal places, no zeros (0.12 to 0.99, avoiding x.x0)
        whole = 0
        decimal_part = random.randint(11, 99)
        # Avoid numbers ending in 0 for this level
        while decimal_part % 10 == 0:
            decimal_part = random.randint(11, 99)
        decimal_str = f"0.{decimal_part:02d}"
        
    elif difficulty == 3:
        # Level 3: Two decimal places including zeros (0.05, 0.30, etc.)
        decimal_options = []
        # Numbers with zero in tenths place
        for i in range(1, 10):
            decimal_options.append(f"0.0{i}")
        # Numbers with zero in hundredths place  
        for i in range(1, 10):
            decimal_options.append(f"0.{i}0")
        # Some regular two-digit decimals
        for i in range(10, 100):
            decimal_options.append(f"0.{i:02d}")
        
        decimal_str = random.choice(decimal_options)
        
    elif difficulty == 4:
        # Level 4: Whole numbers with one decimal place (1.5, 12.7, etc.)
        whole = random.randint(1, 20)
        decimal_part = random.randint(1, 9)
        decimal_str = f"{whole}.{decimal_part}"
        
    else:  # difficulty == 5
        # Level 5: Whole numbers with two decimal places (2.45, 15.08, etc.)
        whole = random.randint(1, 50)
        decimal_part = random.randint(1, 99)
        decimal_str = f"{whole}.{decimal_part:02d}"
    
    # Convert to words
    decimal_words = decimal_to_words(decimal_str)
    
    if question_type == "decimal_to_words":
        # Decimal → Words (multiple choice)
        distractors = generate_word_distractors(decimal_str, decimal_words)
        options = [decimal_words] + distractors
        random.shuffle(options)
        
        st.session_state.decimals_question_data = {
            "question_type": "decimal_to_words",
            "decimal_number": decimal_str,
            "decimal_words": decimal_words,
            "options": options
        }
        st.session_state.decimals_correct_answer = decimal_words
        st.session_state.current_decimals_question = f"How do you write {decimal_str} in words?"
        
    else:  # words_to_decimal
        # Words → Decimal (text input)
        st.session_state.decimals_question_data = {
            "question_type": "words_to_decimal",
            "decimal_number": decimal_str,
            "decimal_words": decimal_words,
            "options": None
        }
        st.session_state.decimals_correct_answer = decimal_str
        st.session_state.current_decimals_question = f"Write {decimal_words} as a decimal number."

def generate_word_distractors(decimal_str, correct_words):
    """Generate plausible wrong answers for decimal→words questions"""
    distractors = []
    
    # Split decimal for manipulation
    if '.' in decimal_str:
        whole_part, decimal_part = decimal_str.split('.')
    else:
        whole_part = decimal_str
        decimal_part = ""
    
    # Common mistake patterns
    
    # 1. Missing "zero" at the beginning (for decimals starting with 0)
    if decimal_str.startswith("0."):
        distractor1 = correct_words.replace("zero point", "point")
        if distractor1 != correct_words and distractor1 not in distractors:
            distractors.append(distractor1)
    
    # 2. Reading decimal digits as whole numbers (0.92 → "zero point ninety-two")
    if decimal_part and len(decimal_part) == 2:
        tens_digit = int(decimal_part[0])
        ones_digit = int(decimal_part[1])
        
        if tens_digit >= 2:  # Can make "twenty", "thirty", etc.
            tens_words = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
            ones_words = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
            
            if ones_digit == 0:
                number_word = tens_words[tens_digit]
            else:
                number_word = tens_words[tens_digit] + " " + ones_words[ones_digit]
            
            whole_words = "zero" if whole_part == "0" else decimal_to_words(whole_part)
            distractor2 = f"{whole_words} point {number_word}"
            if distractor2 not in distractors:
                distractors.append(distractor2)
    
    # 3. Wrong digit substitutions
    if decimal_part:
        # Change one digit in the decimal part
        decimal_list = list(decimal_part)
        if len(decimal_list) > 0:
            # Change first decimal digit
            original_digit = decimal_list[0]
            new_digit = str((int(original_digit) + 1) % 10)
            decimal_list[0] = new_digit
            new_decimal = ''.join(decimal_list)
            new_decimal_str = f"{whole_part}.{new_decimal}"
            distractor3 = decimal_to_words(new_decimal_str)
            if distractor3 not in distractors:
                distractors.append(distractor3)
        
        if len(decimal_list) > 1:
            # Change second decimal digit
            decimal_list = list(decimal_part)  # Reset
            original_digit = decimal_list[1]
            new_digit = str((int(original_digit) + 2) % 10)
            decimal_list[1] = new_digit
            new_decimal = ''.join(decimal_list)
            new_decimal_str = f"{whole_part}.{new_decimal}"
            distractor4 = decimal_to_words(new_decimal_str)
            if distractor4 not in distractors:
                distractors.append(distractor4)
    
    # 4. Wrong whole number part (for decimals with whole numbers)
    if whole_part != "0":
        wrong_whole = str(int(whole_part) + random.choice([1, 2, -1, -2]))
        if int(wrong_whole) > 0:
            wrong_decimal_str = f"{wrong_whole}.{decimal_part}" if decimal_part else wrong_whole
            distractor5 = decimal_to_words(wrong_decimal_str)
            if distractor5 not in distractors:
                distractors.append(distractor5)
    
    # Ensure we have exactly 3 distractors
    while len(distractors) < 3:
        # Generate additional random distractors if needed
        random_digits = [str(random.randint(0, 9)) for _ in range(len(decimal_part) if decimal_part else 1)]
        random_decimal_part = ''.join(random_digits)
        random_decimal_str = f"{whole_part}.{random_decimal_part}"
        random_distractor = decimal_to_words(random_decimal_str)
        if random_distractor not in distractors and random_distractor != correct_words:
            distractors.append(random_distractor)
    
    return distractors[:3]  # Return exactly 3 distractors

def display_decimals_question():
    """Display the current question interface"""
    data = st.session_state.decimals_question_data
    question_type = data["question_type"]
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_decimals_question}**")
    
    if question_type == "decimal_to_words":
        # Decimal → Words: Show decimal number, multiple choice answers
        
        # Display the decimal number in a highlighted box
        st.markdown(f"""
        <div style="
            background-color: #e8f4fd; 
            padding: 40px; 
            border-radius: 15px; 
            border-left: 5px solid #1f77b4;
            font-size: 48px;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            color: #1f77b4;
            font-family: 'Courier New', monospace;
        ">
            {data['decimal_number']}
        </div>
        """, unsafe_allow_html=True)
        
        # Answer selection
        with st.form("decimals_answer_form", clear_on_submit=False):
            st.markdown("**Choose the correct way to write this in words:**")
            
            # Create radio button options
            user_answer = st.radio(
                "Select your answer:",
                options=data['options'],
                key="decimals_choice",
                label_visibility="collapsed"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_answer:
                st.session_state.decimals_user_answer = user_answer
                st.session_state.decimals_show_feedback = True
                st.session_state.decimals_answer_submitted = True
    
    else:  # words_to_decimal
        # Words → Decimal: Show words, text input for decimal
        
        # Display the words in a highlighted box
        st.markdown(f"""
        <div style="
            background-color: #fff3e0; 
            padding: 40px; 
            border-radius: 15px; 
            border-left: 5px solid #ff9800;
            font-size: 32px;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            color: #e65100;
        ">
            {data['decimal_words']}
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        with st.form("decimals_input_form", clear_on_submit=False):
            st.markdown("**Enter the decimal number:**")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                user_input = st.text_input(
                    "Decimal number:",
                    placeholder="Enter decimal (e.g., 0.8)",
                    key="decimals_input",
                    label_visibility="collapsed"
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_input.strip():
                st.session_state.decimals_user_answer = user_input.strip()
                st.session_state.decimals_show_feedback = True
                st.session_state.decimals_answer_submitted = True
    
    # Show feedback and next button
    handle_decimals_feedback_and_next()

def handle_decimals_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.decimals_show_feedback:
        show_decimals_feedback()
    
    # Next question button
    if st.session_state.decimals_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_decimals_question_state()
                st.rerun()

def show_decimals_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.decimals_user_answer
    correct_answer = st.session_state.decimals_correct_answer
    data = st.session_state.decimals_question_data
    question_type = data["question_type"]
    
    # Check if answer is correct
    is_correct = False
    
    if question_type == "decimal_to_words":
        # Exact match for multiple choice
        is_correct = user_answer == correct_answer
    else:  # words_to_decimal
        # For decimal input, allow flexible formats
        is_correct = check_decimal_answer(user_answer, correct_answer)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 5 levels)
        old_difficulty = st.session_state.decimals_words_difficulty
        st.session_state.decimals_words_difficulty = min(
            st.session_state.decimals_words_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.decimals_words_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal word conversion!**")
        elif old_difficulty < st.session_state.decimals_words_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decimals_words_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.decimals_words_difficulty
        st.session_state.decimals_words_difficulty = max(
            st.session_state.decimals_words_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimals_words_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.decimals_words_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_decimals_explanation()

def check_decimal_answer(user_input, correct_decimal):
    """Check if user's decimal input is correct (allowing for format variations)"""
    try:
        # Remove any extra spaces
        user_input = user_input.strip()
        
        # Convert both to float for comparison
        user_float = float(user_input)
        correct_float = float(correct_decimal)
        
        # Check if they're equal (within small tolerance for floating point)
        return abs(user_float - correct_float) < 0.0001
        
    except (ValueError, TypeError):
        # Invalid input format
        return False

def show_decimals_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.decimals_correct_answer
    user_answer = st.session_state.decimals_user_answer
    data = st.session_state.decimals_question_data
    question_type = data["question_type"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "decimal_to_words":
            decimal_number = data['decimal_number']
            st.markdown(f"""
            ### Step-by-step conversion (Decimal → Words):
            
            **Decimal number:** {decimal_number}
            **Correct words:** {correct_answer}
            **Your answer:** {user_answer}
            
            ### How to read decimals in words:
            """)
            
            # Break down the decimal
            if '.' in decimal_number:
                whole_part, decimal_part = decimal_number.split('.')
                
                st.markdown(f"""
                **Step 1:** Read the whole number part
                - **{whole_part}** = "{decimal_to_words(whole_part)}"
                
                **Step 2:** Say "point"
                
                **Step 3:** Read each decimal digit separately
                """)
                
                for i, digit in enumerate(decimal_part):
                    digit_word = {
                        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
                    }[digit]
                    position = "tenths" if i == 0 else "hundredths" if i == 1 else "thousandths"
                    st.markdown(f"- **{digit}** in {position} place = \"{digit_word}\"")
                
                st.markdown(f"**Final answer:** \"{correct_answer}\"")
            
            # Common mistakes explanation
            st.markdown("### ❌ **Common Mistakes to Avoid:**")
            if decimal_number.startswith("0."):
                st.markdown("- Don't skip the \"zero\" at the beginning")
                st.markdown("- Don't read decimal digits as whole numbers (like \"ninety-two\" for .92)")
            
            st.markdown("- Always say each digit separately after \"point\"")
            st.markdown("- Include \"zero\" for any 0 digits in the decimal part")
            
        else:  # words_to_decimal
            decimal_words = data['decimal_words']
            decimal_number = data['decimal_number']
            
            st.markdown(f"""
            ### Step-by-step conversion (Words → Decimal):
            
            **Words:** {decimal_words}
            **Correct decimal:** {correct_answer}
            **Your answer:** {user_answer}
            
            ### How to convert words to decimal:
            """)
            
            # Break down the words
            if 'point' in decimal_words:
                parts = decimal_words.split(' point ')
                whole_words = parts[0]
                decimal_words_part = parts[1] if len(parts) > 1 else ""
                
                st.markdown(f"""
                **Step 1:** Convert the whole number part
                - **"{whole_words}"** = {decimal_number.split('.')[0]}
                
                **Step 2:** The word "point" means decimal point (.)
                
                **Step 3:** Convert each word after "point" to a digit
                """)
                
                if decimal_words_part:
                    decimal_digits = decimal_words_part.split()
                    decimal_part = ""
                    for word in decimal_digits:
                        digit = {
                            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
                            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
                        }.get(word, '?')
                        decimal_part += digit
                        st.markdown(f"- **\"{word}\"** = {digit}")
                    
                    st.markdown(f"**Final answer:** {decimal_number.split('.')[0]}.{decimal_part} = **{correct_answer}**")
            
            st.markdown("### ✅ **Remember:**")
            st.markdown("- \"point\" = decimal point (.)")  
            st.markdown("- Each word after \"point\" becomes one digit")
            st.markdown("- \"zero\" becomes 0, \"one\" becomes 1, etc.")
            st.markdown("- Don't forget the leading zero for decimals less than 1")

def reset_decimals_question_state():
    """Reset the question state for next question"""
    st.session_state.current_decimals_question = None
    st.session_state.decimals_correct_answer = None
    st.session_state.decimals_show_feedback = False
    st.session_state.decimals_answer_submitted = False
    st.session_state.decimals_question_data = {}
    if "decimals_user_answer" in st.session_state:
        del st.session_state.decimals_user_answer