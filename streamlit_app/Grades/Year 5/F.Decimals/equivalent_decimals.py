import streamlit as st
import random

def run():
    """
    Main function to run the Equivalent Decimals practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/equivalent_decimals.py
    """
    # Initialize session state for difficulty and game state
    if "equivalent_decimals_difficulty" not in st.session_state:
        st.session_state.equivalent_decimals_difficulty = 1  # Start with simple equivalents
    
    if "current_equivalent_question" not in st.session_state:
        st.session_state.current_equivalent_question = None
        st.session_state.equivalent_correct_answer = None
        st.session_state.equivalent_show_feedback = False
        st.session_state.equivalent_answer_submitted = False
        st.session_state.equivalent_question_data = {}
        st.session_state.selected_equivalent_tile = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Equivalent Decimals")
    st.markdown("*Identify decimals that represent the same value*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.equivalent_decimals_difficulty
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
    if st.session_state.current_equivalent_question is None:
        generate_new_equivalent_question()
    
    # Display current question
    display_equivalent_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Equivalent Decimals**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Two question types:** Find equivalent decimals or compare two decimals
        - **Click the correct tile** to select your answer
        - **Think about trailing zeros** and decimal place values
        
        ### What are Equivalent Decimals?
        
        #### **Definition:**
        Equivalent decimals are **different ways of writing the same number value**. They look different but represent exactly the same amount.
        
        #### **Key Rule: Trailing Zeros**
        **Adding or removing zeros at the END of a decimal doesn't change its value:**
        - **0.5 = 0.50 = 0.500** (all equal five tenths)
        - **3.2 = 3.20 = 3.200** (all equal three and two tenths)
        - **35.25 = 35.250 = 35.2500** (all equal thirty-five and twenty-five hundredths)
        
        ### Examples of Equivalent Decimals:
        
        #### **Basic Examples:**
        - **0.8 = 0.80 = 0.800** (eight tenths)
        - **0.5 = 0.50** (five tenths)
        - **1.4 = 1.40** (one and four tenths)
        - **7.0 = 7.00 = 7** (seven)
        
        #### **More Complex Examples:**
        - **12.30 = 12.3** (twelve and three tenths)
        - **35.250 = 35.25** (thirty-five and twenty-five hundredths)
        - **100.0 = 100** (one hundred)
        - **0.060 = 0.06** (six hundredths)
        
        ### What Makes Decimals Equivalent?
        
        #### **✅ These ARE Equivalent:**
        - **Same digits, extra zeros at end:** 4.5 and 4.50
        - **Same value, different decimal places:** 0.8 and 0.80
        - **Whole numbers with zeros:** 25 and 25.0
        
        #### **❌ These are NOT Equivalent:**
        - **Different digits:** 4.5 and 4.6
        - **Zeros in wrong places:** 4.5 and 4.05 (zero in middle changes value)
        - **Missing important digits:** 4.25 and 4.2 (different values)
        
        ### Tips for Success:
        
        #### **For "Find the Equivalent" Questions:**
        - **Look for the same digits** in the same positions
        - **Ignore trailing zeros** at the end
        - **Check decimal point placement**
        - **Convert to same number of decimal places** mentally
        
        #### **For "Are These Equivalent?" Questions:**
        - **Line up the decimal points** mentally
        - **Add zeros to make same length:** 0.8 → 0.80
        - **Compare digit by digit** from left to right
        - **Remember: trailing zeros don't matter**
        
        ### Mental Strategies:
        
        #### **The "Add Zeros" Method:**
        - 0.8 vs 0.80 → Add zero: 0.80 vs 0.80 ✅ Equal
        - 1.5 vs 1.50 → Add zero: 1.50 vs 1.50 ✅ Equal
        - 2.3 vs 2.30 → Add zero: 2.30 vs 2.30 ✅ Equal
        
        #### **The "Remove Zeros" Method:**
        - 4.50 vs 4.5 → Remove zero: 4.5 vs 4.5 ✅ Equal
        - 12.000 vs 12 → Remove zeros: 12 vs 12 ✅ Equal
        
        ### Common Mistakes to Avoid:
        - ❌ **Don't confuse 0.8 and 0.08** (different place values)
        - ❌ **Don't think 4.5 = 4.05** (zero in middle matters)
        - ❌ **Don't ignore the decimal point position**
        - ✅ **Remember: only TRAILING zeros can be ignored**
        
        ### Place Value Understanding:
        ```
        4.250 = 4 + 0.2 + 0.05 + 0.000 = 4.25
        0.80 = 0 + 0.8 + 0.00 = 0.8
        35.0 = 35 + 0.0 = 35
        ```
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple trailing zeros (0.5 ↔ 0.50)
        - **🟠 Level 3:** Multiple decimal places (12.340 ↔ 12.34)
        - **🔴 Level 4-5:** Complex numbers and mixed types
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master Level 5!
        """)

def generate_new_equivalent_question():
    """Generate a new equivalent decimals question"""
    difficulty = st.session_state.equivalent_decimals_difficulty
    
    # Randomly choose question type (60% multiple choice, 40% yes/no)
    question_type = random.choices(["find_equivalent", "are_equivalent"], weights=[0.6, 0.4])[0]
    
    if question_type == "find_equivalent":
        generate_find_equivalent_question(difficulty)
    else:
        generate_are_equivalent_question(difficulty)

def generate_find_equivalent_question(difficulty):
    """Generate 'find the equivalent' multiple choice question"""
    
    # Generate base number based on difficulty
    if difficulty == 1:
        # Level 1: Simple one decimal place with trailing zeros
        base_numbers = ["0.5", "0.8", "1.2", "2.6", "3.4", "4.7", "5.9"]
        
    elif difficulty == 2:
        # Level 2: Two decimal places
        base_numbers = ["0.25", "0.75", "1.50", "2.30", "3.60", "4.20", "5.80"]
        
    elif difficulty == 3:
        # Level 3: Three decimal places and larger numbers
        base_numbers = ["0.125", "0.250", "12.300", "25.400", "35.250", "48.600"]
        
    elif difficulty == 4:
        # Level 4: Mix of different lengths and whole numbers
        base_numbers = ["15.0", "25.00", "100.500", "200.750", "0.0625", "12.3750"]
        
    else:  # difficulty == 5
        # Level 5: Complex numbers with multiple trailing zeros
        base_numbers = ["125.0000", "75.2500", "300.1250", "0.06250", "999.0000"]
    
    given_number = random.choice(base_numbers)
    
    # Create the equivalent form (add or remove trailing zeros)
    correct_equivalent = create_equivalent_form(given_number)
    
    # Generate distractors
    distractors = generate_equivalent_distractors(given_number, correct_equivalent)
    
    # Create options
    options = [correct_equivalent] + distractors
    random.shuffle(options)
    
    st.session_state.equivalent_question_data = {
        "question_type": "find_equivalent",
        "given_number": given_number,
        "correct_answer": correct_equivalent,
        "options": options
    }
    st.session_state.equivalent_correct_answer = correct_equivalent
    st.session_state.current_equivalent_question = f"Which decimal is equivalent to {given_number}?"

def generate_are_equivalent_question(difficulty):
    """Generate 'are these equivalent' yes/no question"""
    
    # 70% of time make them equivalent, 30% not equivalent
    are_equivalent = random.choices([True, False], weights=[0.7, 0.3])[0]
    
    if are_equivalent:
        # Generate equivalent pair
        if difficulty == 1:
            base_numbers = ["0.5", "0.8", "1.2", "2.6", "3.4"]
        elif difficulty == 2:
            base_numbers = ["0.25", "0.75", "1.50", "2.30", "3.60"]
        elif difficulty == 3:
            base_numbers = ["0.125", "12.300", "25.400", "35.250"]
        elif difficulty == 4:
            base_numbers = ["15.0", "100.500", "0.0625", "12.3750"]
        else:
            base_numbers = ["125.0000", "75.2500", "0.06250"]
        
        number1 = random.choice(base_numbers)
        number2 = create_equivalent_form(number1)
        correct_answer = "yes"
        
    else:
        # Generate non-equivalent pair
        if difficulty <= 2:
            pairs = [
                ("0.5", "0.05"), ("0.8", "0.08"), ("1.2", "1.02"), 
                ("2.5", "2.05"), ("3.4", "3.04"), ("0.6", "0.60")  # One equivalent pair as distractor
            ]
        elif difficulty == 3:
            pairs = [
                ("0.25", "0.025"), ("12.3", "12.03"), ("35.25", "35.025"),
                ("0.125", "0.0125"), ("25.4", "25.04")
            ]
        else:
            pairs = [
                ("15.0", "1.50"), ("100.5", "10.05"), ("0.625", "0.0625"),
                ("12.375", "12.0375"), ("200.75", "20.075")
            ]
        
        number1, number2 = random.choice(pairs)
        correct_answer = "no"
    
    st.session_state.equivalent_question_data = {
        "question_type": "are_equivalent",
        "number1": number1,
        "number2": number2,
        "correct_answer": correct_answer,
        "options": ["yes", "no"]
    }
    st.session_state.equivalent_correct_answer = correct_answer
    st.session_state.current_equivalent_question = f"Are {number1} and {number2} equivalent decimals?"

def create_equivalent_form(number_str):
    """Create an equivalent form by adding/removing trailing zeros"""
    
    # Convert to float and back to remove unnecessary zeros, then add some
    num = float(number_str)
    
    # Randomly decide to add or remove zeros (if possible)
    operations = []
    
    # Can we remove trailing zeros?
    if number_str.endswith('0') and '.' in number_str:
        operations.append("remove_zeros")
    
    # Can we add trailing zeros?
    if '.' in number_str:
        operations.append("add_zeros")
    else:
        # If it's a whole number, we can add decimal point and zeros
        operations.append("add_decimal_zeros")
    
    operation = random.choice(operations)
    
    if operation == "remove_zeros":
        # Remove trailing zeros
        result = number_str.rstrip('0').rstrip('.')
        if result == "":
            result = "0"
        elif not '.' in result and '.' in number_str:
            # If we removed all decimal places, keep it as whole number
            pass
        return result
        
    elif operation == "add_zeros":
        # Add 1-3 trailing zeros
        zeros_to_add = random.randint(1, 3)
        return number_str + ('0' * zeros_to_add)
        
    else:  # add_decimal_zeros
        # Add decimal point and zeros to whole number
        zeros_to_add = random.randint(1, 3)
        return number_str + '.' + ('0' * zeros_to_add)

def generate_equivalent_distractors(given_number, correct_answer):
    """Generate wrong answers for equivalent decimal questions"""
    distractors = []
    
    given_float = float(given_number)
    
    # Distractor 1: Move decimal point
    if given_float >= 1:
        # Make it smaller by moving decimal right
        distractor1 = str(given_float / 10)
        if distractor1 != correct_answer and distractor1 != given_number:
            distractors.append(distractor1)
    else:
        # Make it bigger by moving decimal left
        distractor1 = str(given_float * 10)
        if distractor1 != correct_answer and distractor1 != given_number:
            distractors.append(distractor1)
    
    # Distractor 2: Add/remove zeros in wrong place
    if '.' in given_number:
        parts = given_number.split('.')
        if len(parts[1]) > 1:
            # Remove a zero from middle of decimal part
            decimal_part = parts[1]
            if '0' in decimal_part[:-1]:  # Not the last character
                new_decimal = decimal_part.replace('0', '', 1)
                distractor2 = parts[0] + '.' + new_decimal
                if distractor2 != correct_answer and distractor2 != given_number:
                    distractors.append(distractor2)
    
    # Distractor 3: Change a digit slightly
    digits = given_number.replace('.', '')
    if len(digits) > 1:
        digit_list = list(digits)
        # Change last non-zero digit
        for i in range(len(digit_list) - 1, -1, -1):
            if digit_list[i] != '0':
                old_digit = int(digit_list[i])
                new_digit = (old_digit + 1) % 10
                if new_digit == 0:
                    new_digit = (old_digit - 1) % 10
                digit_list[i] = str(new_digit)
                break
        
        new_digits = ''.join(digit_list)
        # Reconstruct number with decimal point
        if '.' in given_number:
            decimal_pos = given_number.index('.')
            distractor3 = new_digits[:decimal_pos] + '.' + new_digits[decimal_pos:]
        else:
            distractor3 = new_digits
            
        if distractor3 != correct_answer and distractor3 != given_number:
            distractors.append(distractor3)
    
    # Ensure we have exactly 3 distractors
    while len(distractors) < 3:
        # Generate additional distractors
        multipliers = [0.1, 10, 0.01, 100]
        random_multiplier = random.choice(multipliers)
        random_distractor = str(given_float * random_multiplier)
        
        if (random_distractor != correct_answer and 
            random_distractor != given_number and 
            random_distractor not in distractors):
            distractors.append(random_distractor)
    
    return distractors[:3]

def display_equivalent_question():
    """Display the current equivalent decimals question"""
    data = st.session_state.equivalent_question_data
    question_type = data["question_type"]
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_equivalent_question}**")
    
    if question_type == "find_equivalent":
        display_find_equivalent_tiles(data)
    else:  # are_equivalent
        display_yes_no_tiles(data)
    
    # Show feedback and next button
    handle_equivalent_feedback_and_next()

def display_find_equivalent_tiles(data):
    """Display clickable tiles for find equivalent question"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create clickable tiles in 2x2 grid
    options = data["options"]
    
    # Create columns for tiles (2 tiles per row)
    cols_per_row = 2
    rows = [options[i:i + cols_per_row] for i in range(0, len(options), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, option in enumerate(row):
            with cols[i]:
                # Check if this tile is selected
                is_selected = st.session_state.get("selected_equivalent_tile") == option
                
                # Create button style based on selection
                if is_selected:
                    button_type = "primary"
                else:
                    button_type = "secondary"
                
                if st.button(
                    option,
                    key=f"equiv_tile_{option}",
                    type=button_type,
                    use_container_width=True
                ):
                    st.session_state.selected_equivalent_tile = option
                    st.rerun()
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if st.session_state.get("selected_equivalent_tile"):
                st.session_state.equivalent_user_answer = st.session_state.selected_equivalent_tile
                st.session_state.equivalent_show_feedback = True
                st.session_state.equivalent_answer_submitted = True
                st.rerun()
            else:
                st.warning("⚠️ Please select an answer first!")

def display_yes_no_tiles(data):
    """Display yes/no clickable tiles"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create yes/no tiles
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        is_selected_yes = st.session_state.get("selected_equivalent_tile") == "yes"
        button_type_yes = "primary" if is_selected_yes else "secondary"
        
        if st.button(
            "yes",
            key="equiv_yes_tile",
            type=button_type_yes,
            use_container_width=True
        ):
            st.session_state.selected_equivalent_tile = "yes"
            st.rerun()
    
    with col2:
        is_selected_no = st.session_state.get("selected_equivalent_tile") == "no"
        button_type_no = "primary" if is_selected_no else "secondary"
        
        if st.button(
            "no",
            key="equiv_no_tile",
            type=button_type_no,
            use_container_width=True
        ):
            st.session_state.selected_equivalent_tile = "no"
            st.rerun()
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if st.session_state.get("selected_equivalent_tile"):
                st.session_state.equivalent_user_answer = st.session_state.selected_equivalent_tile
                st.session_state.equivalent_show_feedback = True
                st.session_state.equivalent_answer_submitted = True
                st.rerun()
            else:
                st.warning("⚠️ Please select an answer first!")

def handle_equivalent_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.equivalent_show_feedback:
        show_equivalent_feedback()
    
    # Next question button
    if st.session_state.equivalent_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_equivalent_state()
                st.rerun()

def show_equivalent_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.equivalent_user_answer
    correct_answer = st.session_state.equivalent_correct_answer
    
    is_correct = user_answer == correct_answer
    
    st.markdown("---")
    st.markdown("### 📋 Results:")
    
    if is_correct:
        st.success("🎉 **Perfect! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.equivalent_decimals_difficulty
        st.session_state.equivalent_decimals_difficulty = min(
            st.session_state.equivalent_decimals_difficulty + 1, 5
        )
        
        if st.session_state.equivalent_decimals_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered equivalent decimals!**")
        elif old_difficulty < st.session_state.equivalent_decimals_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.equivalent_decimals_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.equivalent_decimals_difficulty
        st.session_state.equivalent_decimals_difficulty = max(
            st.session_state.equivalent_decimals_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.equivalent_decimals_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.equivalent_decimals_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_equivalent_explanation(is_correct)

def show_equivalent_explanation(correct=True):
    """Show detailed explanation of equivalent decimals"""
    data = st.session_state.equivalent_question_data
    user_answer = st.session_state.equivalent_user_answer
    correct_answer = st.session_state.equivalent_correct_answer
    
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
            <h4 style="color: {title_color}; margin-top: 0;">💡 Understanding Equivalent Decimals:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        question_type = data["question_type"]
        
        if question_type == "find_equivalent":
            given_number = data["given_number"]
            
            st.markdown(f"""
            ### 🔢 **Question Analysis:**
            - **Given number:** {given_number}
            - **Correct equivalent:** {correct_answer}
            - **Your answer:** {user_answer}
            """)
            
            # Show why they're equivalent
            show_equivalence_explanation(given_number, correct_answer)
            
        else:  # are_equivalent
            number1 = data["number1"]
            number2 = data["number2"]
            
            st.markdown(f"""
            ### 🔢 **Question Analysis:**
            - **Comparing:** {number1} and {number2}
            - **Are they equivalent?** {correct_answer}
            - **Your answer:** {user_answer}
            """)
            
            # Show why they are or aren't equivalent
            show_comparison_explanation(number1, number2, correct_answer)

def show_equivalence_explanation(num1, num2):
    """Show why two numbers are equivalent"""
    st.markdown(f"### 🔍 **Why {num1} = {num2}:**")
    
    # Convert both to floats to verify they're equal
    val1 = float(num1)
    val2 = float(num2)
    
    if val1 == val2:
        st.markdown(f"✅ Both numbers represent the same value: **{val1}**")
        
        # Show the trailing zero explanation
        if len(num1) != len(num2):
            if len(num1) > len(num2):
                longer, shorter = num1, num2
            else:
                longer, shorter = num2, num1
                
            st.markdown(f"""
            ### 🎯 **Key Concept: Trailing Zeros**
            - **{shorter}** = **{longer}**
            - Adding zeros at the END doesn't change the value
            - These zeros are called "trailing zeros"
            """)
            
            # Show place value breakdown
            st.markdown("### 📊 **Place Value Breakdown:**")
            show_place_value_breakdown(longer)
        
    else:
        st.markdown(f"❌ These numbers have different values: {val1} ≠ {val2}")

def show_comparison_explanation(num1, num2, correct_answer):
    """Show comparison between two numbers"""
    val1 = float(num1)
    val2 = float(num2)
    
    if correct_answer == "yes":
        st.markdown(f"### ✅ **Why {num1} = {num2}:**")
        st.markdown(f"Both numbers represent the same value: **{val1}**")
        
        # Show step-by-step comparison
        st.markdown("### 🔍 **Step-by-Step Check:**")
        
        # Normalize to same decimal places
        max_decimal_places = max(
            len(num1.split('.')[1]) if '.' in num1 else 0,
            len(num2.split('.')[1]) if '.' in num2 else 0
        )
        
        normalized1 = f"{val1:.{max_decimal_places}f}"
        normalized2 = f"{val2:.{max_decimal_places}f}"
        
        st.markdown(f"1. **Normalize to same decimal places:**")
        st.markdown(f"   - {num1} → {normalized1}")
        st.markdown(f"   - {num2} → {normalized2}")
        st.markdown(f"2. **Compare:** {normalized1} = {normalized2} ✅")
        
    else:  # "no"
        st.markdown(f"### ❌ **Why {num1} ≠ {num2}:**")
        st.markdown(f"These numbers have different values: **{val1}** ≠ **{val2}**")
        
        # Show the difference
        difference = abs(val1 - val2)
        st.markdown(f"**Difference:** {difference}")
        
        # Common mistake explanation
        if "0" in num1 or "0" in num2:
            st.markdown("""
            ### ⚠️ **Common Mistake:**
            Be careful about WHERE the zeros are placed:
            - **Trailing zeros** (at the end) don't change value
            - **Zeros in the middle** DO change the value
            """)

def show_place_value_breakdown(number_str):
    """Show place value breakdown of a number"""
    if '.' not in number_str:
        number_str += '.0'
    
    whole_part, decimal_part = number_str.split('.')
    
    st.markdown("**Place values:**")
    
    # Show whole part
    for i, digit in enumerate(reversed(whole_part)):
        place_value = 10 ** i
        if place_value == 1:
            place_name = "ones"
        elif place_value == 10:
            place_name = "tens"
        elif place_value == 100:
            place_name = "hundreds"
        else:
            place_name = f"{place_value}s"
            
        value = int(digit) * place_value
        if value > 0:
            st.markdown(f"- {digit} in {place_name} place = {value}")
    
    # Show decimal part
    for i, digit in enumerate(decimal_part):
        place_value = 0.1 ** (i + 1)
        if i == 0:
            place_name = "tenths"
        elif i == 1:
            place_name = "hundredths"
        elif i == 2:
            place_name = "thousandths"
        else:
            place_name = f"ten-thousandths+"
            
        value = int(digit) * place_value
        if value > 0:
            st.markdown(f"- {digit} in {place_name} place = {value}")
        elif digit == '0':
            st.markdown(f"- {digit} in {place_name} place = 0 (this zero doesn't add value)")

def reset_equivalent_state():
    """Reset state for next question"""
    st.session_state.current_equivalent_question = None
    st.session_state.equivalent_correct_answer = None
    st.session_state.equivalent_show_feedback = False
    st.session_state.equivalent_answer_submitted = False
    st.session_state.equivalent_question_data = {}
    st.session_state.selected_equivalent_tile = None
    
    # Clear any stored answers
    if "equivalent_user_answer" in st.session_state:
        del st.session_state.equivalent_user_answer