import streamlit as st
import random

def run():
    """
    Main function to run the Place Values in Decimal Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/place_values_in_decimal_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "place_values_difficulty" not in st.session_state:
        st.session_state.place_values_difficulty = 1  # Start with simple 3-4 digit numbers
    
    if "current_place_values_question" not in st.session_state:
        st.session_state.current_place_values_question = None
        st.session_state.place_values_correct_answer = None
        st.session_state.place_values_show_feedback = False
        st.session_state.place_values_answer_submitted = False
        st.session_state.place_values_question_data = {}
        st.session_state.selected_tile = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Place Values in Decimal Numbers")
    st.markdown("*Identify the place value of digits in decimal numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.place_values_difficulty
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
    if st.session_state.current_place_values_question is None:
        generate_new_place_values_question()
    
    # Display current question
    display_place_values_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Place Values in Decimals**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Two question types:** Identify place values in both directions
        - **Clickable tiles:** Choose the correct place value name
        - **Text input:** Type the digit in a specific place value
        - **Think systematically** about each digit's position
        
        ### Place Value Chart:
        ```
        Thousands | Hundreds | Tens | Ones | . | Tenths | Hundredths | Thousandths
            1000      100      10     1    .    0.1       0.01        0.001
        ```
        
        ### Examples:
        **Number: 2543.67**
        - **2** is in the **thousands** place (2000)
        - **5** is in the **hundreds** place (500)  
        - **4** is in the **tens** place (40)
        - **3** is in the **ones** place (3)
        - **6** is in the **tenths** place (0.6)
        - **7** is in the **hundredths** place (0.07)
        
        ### Tips for Success:
        
        #### **Finding Which Place a Digit is In:**
        - **Count from the decimal point** both ways
        - **Left of decimal:** ones, tens, hundreds, thousands...
        - **Right of decimal:** tenths, hundredths, thousandths...
        - **Remember:** The decimal point is your anchor!
        
        #### **Finding Which Digit is in a Place:**
        - **Locate the place value** first
        - **Count positions** from the decimal point
        - **Check your answer** by saying the number out loud
        
        ### Place Value Positions:
        - **To the left of decimal point:**
          - 1st position: **Ones** (1)
          - 2nd position: **Tens** (10)  
          - 3rd position: **Hundreds** (100)
          - 4th position: **Thousands** (1000)
          - 5th position: **Ten thousands** (10,000)
        
        - **To the right of decimal point:**
          - 1st position: **Tenths** (0.1)
          - 2nd position: **Hundredths** (0.01)
          - 3rd position: **Thousandths** (0.001)
        
        ### Common Mistakes to Avoid:
        - ❌ Don't confuse "tens" and "tenths"
        - ❌ Don't start counting from the wrong end
        - ✅ Always use the decimal point as your reference
        - ✅ Remember: tenths are BIGGER than hundredths
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** 3-4 digit numbers with 1-2 decimal places
        - **🟠 Level 3:** 4-5 digit numbers with 2-3 decimal places  
        - **🔴 Level 4-5:** Larger numbers with more decimal places
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master Level 5!
        """)

def generate_new_place_values_question():
    """Generate a new place values question"""
    difficulty = st.session_state.place_values_difficulty
    
    # Randomly choose question type (50/50 split)
    question_type = random.choice(["digit_to_place", "place_to_digit"])
    
    # Generate number based on difficulty level
    if difficulty == 1:
        # Level 1: 3-4 digit whole numbers with 1 decimal place (123.4, 1234.5)
        whole_digits = random.randint(3, 4)
        decimal_digits = 1
        
    elif difficulty == 2:
        # Level 2: 3-4 digit numbers with 1-2 decimal places (123.45, 1234.5)
        whole_digits = random.randint(3, 4)
        decimal_digits = random.randint(1, 2)
        
    elif difficulty == 3:
        # Level 3: 4-5 digit numbers with 2-3 decimal places (1234.567, 12345.67)
        whole_digits = random.randint(4, 5)
        decimal_digits = random.randint(2, 3)
        
    elif difficulty == 4:
        # Level 4: 4-6 digit numbers with 2-3 decimal places
        whole_digits = random.randint(4, 6)
        decimal_digits = random.randint(2, 3)
        
    else:  # difficulty == 5
        # Level 5: 5-7 digit numbers with 3 decimal places
        whole_digits = random.randint(5, 7)
        decimal_digits = 3
    
    # Generate the number
    whole_part = ""
    for i in range(whole_digits):
        if i == 0:
            # First digit can't be 0
            whole_part += str(random.randint(1, 9))
        else:
            whole_part += str(random.randint(0, 9))
    
    decimal_part = ""
    for i in range(decimal_digits):
        decimal_part += str(random.randint(0, 9))
    
    number_str = f"{whole_part}.{decimal_part}"
    
    # Create place value mapping
    place_values = []
    digits = []
    
    # Add whole number places (right to left)
    for i, digit in enumerate(reversed(whole_part)):
        digits.append(digit)
        if i == 0:
            place_values.append("ones")
        elif i == 1:
            place_values.append("tens")
        elif i == 2:
            place_values.append("hundreds")
        elif i == 3:
            place_values.append("thousands")
        elif i == 4:
            place_values.append("ten thousands")
        elif i == 5:
            place_values.append("hundred thousands")
        elif i == 6:
            place_values.append("millions")
    
    # Reverse to get correct order (left to right)
    digits.reverse()
    place_values.reverse()
    
    # Add decimal places (left to right)
    for i, digit in enumerate(decimal_part):
        digits.append(digit)
        if i == 0:
            place_values.append("tenths")
        elif i == 1:
            place_values.append("hundredths")
        elif i == 2:
            place_values.append("thousandths")
    
    if question_type == "digit_to_place":
        # Choose a digit and ask for its place value
        digit_index = random.randint(0, len(digits) - 1)
        target_digit = digits[digit_index]
        correct_place = place_values[digit_index]
        
        # Generate distractors
        all_possible_places = ["millions", "hundred thousands", "ten thousands", "thousands", 
                              "hundreds", "tens", "ones", "tenths", "hundredths", "thousandths"]
        
        # Filter to places that exist in this number range
        relevant_places = [p for p in all_possible_places if p in place_values]
        
        # Add some nearby places as distractors
        distractors = []
        current_index = all_possible_places.index(correct_place)
        
        # Add adjacent places
        for offset in [-2, -1, 1, 2]:
            new_index = current_index + offset
            if 0 <= new_index < len(all_possible_places):
                distractor = all_possible_places[new_index]
                if distractor != correct_place and distractor not in distractors:
                    distractors.append(distractor)
        
        # Ensure we have exactly 3 distractors
        while len(distractors) < 3:
            random_place = random.choice(all_possible_places)
            if random_place != correct_place and random_place not in distractors:
                distractors.append(random_place)
        
        distractors = distractors[:3]
        
        # Create options
        options = [correct_place] + distractors
        random.shuffle(options)
        
        st.session_state.place_values_question_data = {
            "question_type": "digit_to_place",
            "number": number_str,
            "target_digit": target_digit,
            "correct_place": correct_place,
            "options": options,
            "digits": digits,
            "place_values": place_values
        }
        st.session_state.place_values_correct_answer = correct_place
        st.session_state.current_place_values_question = f"In {number_str}, in which place is the {target_digit}?"
        
    else:  # place_to_digit
        # Choose a place and ask for the digit
        place_index = random.randint(0, len(place_values) - 1)
        target_place = place_values[place_index]
        correct_digit = digits[place_index]
        
        st.session_state.place_values_question_data = {
            "question_type": "place_to_digit",
            "number": number_str,
            "target_place": target_place,
            "correct_digit": correct_digit,
            "digits": digits,
            "place_values": place_values
        }
        st.session_state.place_values_correct_answer = correct_digit
        st.session_state.current_place_values_question = f"In {number_str}, which digit is in the {target_place} place?"

def display_place_values_question():
    """Display the current question interface"""
    data = st.session_state.place_values_question_data
    question_type = data["question_type"]
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_place_values_question}**")
    
    # Display the number in a highlighted box
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
        letter-spacing: 3px;
    ">
        {data['number']}
    </div>
    """, unsafe_allow_html=True)
    
    if question_type == "digit_to_place":
        # Digit → Place: Show clickable tiles for place values
        display_clickable_tiles(data)
        
    else:  # place_to_digit
        # Place → Digit: Show text input
        display_digit_input(data)
    
    # Show feedback and next button
    handle_place_values_feedback_and_next()

def display_clickable_tiles(data):
    """Display clickable tiles for place value selection"""
    st.markdown("**Click on the correct place value:**")
    
    # Create clickable tiles
    options = data["options"]
    
    # Create columns for tiles (2 tiles per row)
    cols_per_row = 2
    rows = [options[i:i + cols_per_row] for i in range(0, len(options), cols_per_row)]
    
    selected_option = None
    
    for row in rows:
        cols = st.columns(len(row))
        for i, option in enumerate(row):
            with cols[i]:
                # Check if this tile is selected
                is_selected = st.session_state.get("selected_tile") == option
                
                # Create button style based on selection
                if is_selected:
                    button_type = "primary"
                else:
                    button_type = "secondary"
                
                if st.button(
                    option,
                    key=f"tile_{option}",
                    type=button_type,
                    use_container_width=True
                ):
                    st.session_state.selected_tile = option
                    selected_option = option
                    st.rerun()
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True):
            if st.session_state.get("selected_tile"):
                st.session_state.place_values_user_answer = st.session_state.selected_tile
                st.session_state.place_values_show_feedback = True
                st.session_state.place_values_answer_submitted = True
                st.rerun()
            else:
                st.warning("⚠️ Please select a place value first!")

def display_digit_input(data):
    """Display text input for digit entry"""
    st.markdown("**Enter the digit in the specified place:**")
    
    # Show which place we're looking for
    target_place = data["target_place"]
    st.markdown(f"""
    <div style="
        background-color: #fff3e0; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #ff9800;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #e65100;
    ">
        Looking for the digit in the <strong>{target_place}</strong> place
    </div>
    """, unsafe_allow_html=True)
    
    # Input and submit in a form
    with st.form("digit_input_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_input = st.text_input(
                "Enter the digit:",
                placeholder="Enter a single digit (0-9)",
                key="digit_input",
                label_visibility="collapsed",
                max_chars=1
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_input.strip():
            st.session_state.place_values_user_answer = user_input.strip()
            st.session_state.place_values_show_feedback = True
            st.session_state.place_values_answer_submitted = True

def handle_place_values_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.place_values_show_feedback:
        show_place_values_feedback()
    
    # Next question button
    if st.session_state.place_values_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_place_values_state()
                st.rerun()

def show_place_values_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.place_values_user_answer
    correct_answer = st.session_state.place_values_correct_answer
    data = st.session_state.place_values_question_data
    
    is_correct = user_answer == correct_answer
    
    st.markdown("---")
    st.markdown("### 📋 Results:")
    
    if is_correct:
        st.success("🎉 **Perfect! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.place_values_difficulty
        st.session_state.place_values_difficulty = min(
            st.session_state.place_values_difficulty + 1, 5
        )
        
        if st.session_state.place_values_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered place values in decimals!**")
        elif old_difficulty < st.session_state.place_values_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.place_values_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.place_values_difficulty
        st.session_state.place_values_difficulty = max(
            st.session_state.place_values_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.place_values_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.place_values_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_place_values_explanation(is_correct)

def show_place_values_explanation(correct=True):
    """Show detailed explanation"""
    data = st.session_state.place_values_question_data
    user_answer = st.session_state.place_values_user_answer
    correct_answer = st.session_state.place_values_correct_answer
    
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
            <h4 style="color: {title_color}; margin-top: 0;">💡 Understanding Place Values:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        number = data["number"]
        digits = data["digits"]
        place_values = data["place_values"]
        question_type = data["question_type"]
        
        st.markdown(f"### 🔢 **Number Breakdown: {number}**")
        
        # Create a visual place value chart
        st.markdown("#### Place Value Chart:")
        
        # Split into whole and decimal parts for display
        whole_part, decimal_part = number.split('.')
        
        # Build the chart
        chart_header = []
        chart_digits = []
        
        # Whole number part (right to left, then reverse)
        whole_places = []
        whole_digits_list = []
        
        for i, digit in enumerate(reversed(whole_part)):
            whole_digits_list.append(digit)
            if i == 0:
                whole_places.append("Ones")
            elif i == 1:
                whole_places.append("Tens")
            elif i == 2:
                whole_places.append("Hundreds")
            elif i == 3:
                whole_places.append("Thousands")
            elif i == 4:
                whole_places.append("Ten Thousands")
            elif i == 5:
                whole_places.append("Hundred Thousands")
        
        # Reverse to get left-to-right order
        whole_places.reverse()
        whole_digits_list.reverse()
        
        # Decimal part
        decimal_places = []
        decimal_digits_list = list(decimal_part)
        
        for i in range(len(decimal_part)):
            if i == 0:
                decimal_places.append("Tenths")
            elif i == 1:
                decimal_places.append("Hundredths")
            elif i == 2:
                decimal_places.append("Thousandths")
        
        # Combine for display
        all_places = whole_places + ["."] + decimal_places
        all_digits = whole_digits_list + ["."] + decimal_digits_list
        
        # Display as table
        col_count = len(all_places)
        cols = st.columns(col_count)
        
        # Header row
        for i, place in enumerate(all_places):
            with cols[i]:
                if place == ".":
                    st.markdown("**.**")
                else:
                    st.markdown(f"**{place}**")
        
        # Digit row
        for i, digit in enumerate(all_digits):
            with cols[i]:
                if digit == ".":
                    st.markdown("**.**")
                else:
                    # Highlight the target digit/place
                    if question_type == "digit_to_place":
                        target_digit = data["target_digit"]
                        target_place = data["correct_place"]
                        if digit == target_digit and all_places[i].lower() == target_place:
                            st.markdown(f"🎯 **{digit}**")
                        else:
                            st.markdown(f"{digit}")
                    else:  # place_to_digit
                        target_place = data["target_place"]
                        if all_places[i].lower() == target_place:
                            st.markdown(f"🎯 **{digit}**")
                        else:
                            st.markdown(f"{digit}")
        
        # Explanation based on question type
        if question_type == "digit_to_place":
            target_digit = data["target_digit"]
            correct_place = data["correct_place"]
            st.markdown(f"""
            ### 🎯 **Question Analysis:**
            - **Looking for:** Where is the digit **{target_digit}**?
            - **Correct answer:** **{correct_place}**
            - **Your answer:** {user_answer}
            
            ### 📍 **How to find it:**
            1. **Locate the digit {target_digit}** in the number {number}
            2. **Count its position** from the decimal point
            3. **Identify the place value** name for that position
            """)
            
        else:  # place_to_digit
            target_place = data["target_place"]
            correct_digit = data["correct_digit"]
            st.markdown(f"""
            ### 🎯 **Question Analysis:**
            - **Looking for:** What digit is in the **{target_place}** place?
            - **Correct answer:** **{correct_digit}**
            - **Your answer:** {user_answer}
            
            ### 📍 **How to find it:**
            1. **Locate the {target_place} place** in the place value chart
            2. **Find the corresponding position** in the number {number}
            3. **Read the digit** in that position
            """)
        
        # General tips
        st.markdown("""
        ### 💡 **Remember:**
        - **Decimal point** is your reference point
        - **Left of decimal:** ones, tens, hundreds, thousands...
        - **Right of decimal:** tenths, hundredths, thousandths...
        - **Each position** has a specific name and value
        """)

def reset_place_values_state():
    """Reset state for next question"""
    st.session_state.current_place_values_question = None
    st.session_state.place_values_correct_answer = None
    st.session_state.place_values_show_feedback = False
    st.session_state.place_values_answer_submitted = False
    st.session_state.place_values_question_data = {}
    st.session_state.selected_tile = None
    
    # Clear any stored answers
    if "place_values_user_answer" in st.session_state:
        del st.session_state.place_values_user_answer