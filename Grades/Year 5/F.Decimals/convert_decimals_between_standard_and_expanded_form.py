import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Convert Decimals Between Standard and Expanded Form practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/convert_decimals_between_standard_and_expanded_form.py
    """
    # Initialize session state for difficulty and game state
    if "convert_decimals_difficulty" not in st.session_state:
        st.session_state.convert_decimals_difficulty = 1  # Start with simple conversions
    
    if "current_convert_question" not in st.session_state:
        st.session_state.current_convert_question = None
        st.session_state.convert_correct_answer = None
        st.session_state.convert_show_feedback = False
        st.session_state.convert_answer_submitted = False
        st.session_state.convert_question_data = {}
        st.session_state.selected_convert_tile = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Convert Decimals Between Standard and Expanded Form")
    st.markdown("*Convert between expanded form expressions and standard decimal notation*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.convert_decimals_difficulty
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
    if st.session_state.current_convert_question is None:
        generate_new_convert_question()
    
    # Display current question
    display_convert_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Converting Between Standard and Expanded Form**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the expanded form** expression carefully
        - **Calculate each term** (multiply the digit by its place value)
        - **Add all terms together** to get the standard form
        - **Click the correct tile** with your answer
        
        ### Understanding Expanded Form:
        
        #### **What is Expanded Form?**
        - Shows **each digit multiplied by its place value**
        - Makes the **value of each position** explicit
        - Helps understand **how decimal numbers are built**
        
        #### **Place Value Multipliers:**
        ```
        Hundreds: × 100    Tens: × 10      Ones: × 1
        Tenths: × 0.1      Hundredths: × 0.01    Thousandths: × 0.001
        ```
        
        ### Step-by-Step Examples:
        
        #### **Example 1: Simple Conversion**
        **Expanded:** `2 × 1 + 8 × 0.1 + 4 × 0.01`
        **Step 1:** 2 × 1 = 2
        **Step 2:** 8 × 0.1 = 0.8
        **Step 3:** 4 × 0.01 = 0.04
        **Step 4:** 2 + 0.8 + 0.04 = **2.84**
        
        #### **Example 2: With Thousandths**
        **Expanded:** `7 × 1 + 9 × 0.1 + 7 × 0.01 + 6 × 0.001`
        **Step 1:** 7 × 1 = 7
        **Step 2:** 9 × 0.1 = 0.9
        **Step 3:** 7 × 0.01 = 0.07
        **Step 4:** 6 × 0.001 = 0.006
        **Step 5:** 7 + 0.9 + 0.07 + 0.006 = **7.976**
        
        #### **Example 3: With Larger Numbers**
        **Expanded:** `3 × 10 + 5 × 1 + 2 × 0.1 + 6 × 0.01`
        **Step 1:** 3 × 10 = 30
        **Step 2:** 5 × 1 = 5
        **Step 3:** 2 × 0.1 = 0.2
        **Step 4:** 6 × 0.01 = 0.06
        **Step 5:** 30 + 5 + 0.2 + 0.06 = **35.26**
        
        ### Tips for Success:
        
        #### **Calculation Strategy:**
        - **Work left to right** (largest to smallest place values)
        - **Calculate each term separately** before adding
        - **Line up decimal points** when adding
        - **Double-check your arithmetic**
        
        #### **Common Mistakes to Avoid:**
        - ❌ Don't forget the decimal point
        - ❌ Don't mix up 0.1 and 0.01
        - ❌ Don't add the digits without multiplying first
        - ✅ Always multiply each digit by its place value
        
        #### **Quick Mental Math:**
        - **× 1 = same number** (3 × 1 = 3)
        - **× 0.1 = move decimal right 1** (8 × 0.1 = 0.8)
        - **× 0.01 = move decimal right 2** (4 × 0.01 = 0.04)
        - **× 0.001 = move decimal right 3** (6 × 0.001 = 0.006)
        
        ### Understanding Place Values:
        - **Ones place (× 1):** The whole number part
        - **Tenths place (× 0.1):** First digit after decimal
        - **Hundredths place (× 0.01):** Second digit after decimal
        - **Thousandths place (× 0.001):** Third digit after decimal
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Simple 2-3 terms (ones, tenths, hundredths)
        - **🟠 Level 3:** Include thousandths
        - **🔴 Level 4-5:** Include tens, hundreds, complex expressions
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Master Level 5!
        """)

def generate_new_convert_question():
    """Generate a new conversion question from expanded to standard form"""
    difficulty = st.session_state.convert_decimals_difficulty
    
    # Generate terms based on difficulty level
    terms = []
    
    if difficulty == 1:
        # Level 1: Simple 2-3 terms (ones, tenths, maybe hundredths)
        # Example: 3 × 1 + 4 × 0.1
        ones_digit = random.randint(1, 9)
        tenths_digit = random.randint(1, 9)
        
        terms.append((ones_digit, 1))
        terms.append((tenths_digit, 0.1))
        
        # Sometimes add hundredths
        if random.choice([True, False]):
            hundredths_digit = random.randint(1, 9)
            terms.append((hundredths_digit, 0.01))
            
    elif difficulty == 2:
        # Level 2: 3-4 terms (ones, tenths, hundredths)
        ones_digit = random.randint(1, 9)
        tenths_digit = random.randint(1, 9)
        hundredths_digit = random.randint(1, 9)
        
        terms.append((ones_digit, 1))
        terms.append((tenths_digit, 0.1))
        terms.append((hundredths_digit, 0.01))
        
        # Sometimes add another term
        if random.choice([True, False]):
            if random.choice([True, False]):
                # Add tens
                tens_digit = random.randint(1, 9)
                terms.append((tens_digit, 10))
            else:
                # Add thousandths
                thousandths_digit = random.randint(1, 9)
                terms.append((thousandths_digit, 0.001))
                
    elif difficulty == 3:
        # Level 3: Include thousandths regularly
        place_values = [1, 0.1, 0.01, 0.001]
        num_terms = random.randint(3, 4)
        
        selected_places = random.sample(place_values, num_terms)
        for place_value in selected_places:
            digit = random.randint(1, 9)
            terms.append((digit, place_value))
            
    elif difficulty == 4:
        # Level 4: Include tens and hundreds
        place_values = [100, 10, 1, 0.1, 0.01, 0.001]
        num_terms = random.randint(3, 5)
        
        selected_places = random.sample(place_values, num_terms)
        for place_value in selected_places:
            digit = random.randint(1, 9)
            terms.append((digit, place_value))
            
    else:  # difficulty == 5
        # Level 5: Complex expressions with many terms
        place_values = [1000, 100, 10, 1, 0.1, 0.01, 0.001]
        num_terms = random.randint(4, 6)
        
        selected_places = random.sample(place_values, num_terms)
        for place_value in selected_places:
            digit = random.randint(1, 9)
            terms.append((digit, place_value))
    
    # Sort terms by place value (descending)
    terms.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate the correct answer
    correct_answer = sum(digit * place_value for digit, place_value in terms)
    
    # Format the expanded form expression
    expanded_parts = []
    for digit, place_value in terms:
        if place_value >= 1:
            if place_value == 1:
                expanded_parts.append(f"{digit} × 1")
            else:
                expanded_parts.append(f"{digit} × {int(place_value)}")
        else:
            expanded_parts.append(f"{digit} × {place_value}")
    
    expanded_form = " + ".join(expanded_parts)
    
    # Generate distractors
    distractors = generate_conversion_distractors(terms, correct_answer)
    
    # Format the correct answer
    correct_answer_str = format_decimal(correct_answer)
    
    # Create options
    options = [correct_answer_str] + distractors
    random.shuffle(options)
    
    st.session_state.convert_question_data = {
        "expanded_form": expanded_form,
        "terms": terms,
        "correct_answer": correct_answer_str,
        "options": options
    }
    st.session_state.convert_correct_answer = correct_answer_str
    st.session_state.current_convert_question = f"Find the standard decimal form of:"

def format_decimal(num):
    """Format decimal number to remove unnecessary trailing zeros"""
    if num == int(num):
        return str(int(num))
    else:
        # Format with enough precision, then remove trailing zeros
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        return formatted

def generate_conversion_distractors(terms, correct_answer):
    """Generate plausible wrong answers for conversion problems"""
    distractors = []
    
    # Distractor 1: Forget decimal point (treat as whole number)
    whole_number_distractor = ""
    for digit, place_value in terms:
        whole_number_distractor += str(digit)
    if whole_number_distractor != str(int(correct_answer)) and len(whole_number_distractor) <= 6:
        distractors.append(whole_number_distractor)
    
    # Distractor 2: Wrong decimal placement
    if correct_answer < 1:
        # Make it bigger by removing leading zero or moving decimal
        decimal_str = format_decimal(correct_answer)
        if decimal_str.startswith("0."):
            wrong_placement = decimal_str[2:]  # Remove "0."
            if wrong_placement and wrong_placement != decimal_str:
                distractors.append(wrong_placement)
    elif correct_answer >= 1:
        # Make it smaller by adding leading zero or moving decimal
        decimal_str = format_decimal(correct_answer)
        wrong_placement = "0." + decimal_str.replace(".", "")
        if wrong_placement != decimal_str:
            distractors.append(wrong_placement)
    
    # Distractor 3: Calculation errors (add/subtract small amounts)
    for multiplier in [0.1, 0.01, 0.001, 0.1, 1, 10]:
        wrong_answer = correct_answer + multiplier
        wrong_str = format_decimal(wrong_answer)
        if wrong_str not in distractors and wrong_str != format_decimal(correct_answer):
            distractors.append(wrong_str)
            break
    
    # Distractor 4: Missing or extra terms
    # Calculate with one term missing
    if len(terms) > 1:
        missing_term = random.choice(terms)
        partial_sum = correct_answer - (missing_term[0] * missing_term[1])
        if partial_sum > 0:
            partial_str = format_decimal(partial_sum)
            if partial_str not in distractors and partial_str != format_decimal(correct_answer):
                distractors.append(partial_str)
    
    # Distractor 5: Add wrong multiplier
    extra_term_value = random.choice([0.1, 0.01, 0.001, 1, 10]) * random.randint(1, 9)
    wrong_sum = correct_answer + extra_term_value
    wrong_sum_str = format_decimal(wrong_sum)
    if wrong_sum_str not in distractors and wrong_sum_str != format_decimal(correct_answer):
        distractors.append(wrong_sum_str)
    
    # Ensure we have exactly 3 distractors
    while len(distractors) < 3:
        # Generate random but plausible distractors
        random_variation = correct_answer * random.choice([0.1, 0.01, 10, 100])
        random_str = format_decimal(random_variation)
        if random_str not in distractors and random_str != format_decimal(correct_answer):
            distractors.append(random_str)
    
    return distractors[:3]

def display_convert_question():
    """Display the current conversion question with clickable tiles"""
    data = st.session_state.convert_question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_convert_question}**")
    
    # Display the expanded form in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f3e5f5; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #9c27b0;
        font-size: 24px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #4a148c;
        font-family: 'Courier New', monospace;
    ">
        {data['expanded_form']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display clickable tiles
    display_conversion_tiles(data)
    
    # Show feedback and next button
    handle_conversion_feedback_and_next()

def display_conversion_tiles(data):
    """Display clickable tiles for answer selection"""
    st.markdown("**Click on the correct standard decimal form:**")
    
    # Create clickable tiles
    options = data["options"]
    
    # Create columns for tiles (2 tiles per row)
    cols_per_row = 2
    rows = [options[i:i + cols_per_row] for i in range(0, len(options), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, option in enumerate(row):
            with cols[i]:
                # Check if this tile is selected
                is_selected = st.session_state.get("selected_convert_tile") == option
                
                # Create button style based on selection
                if is_selected:
                    button_type = "primary"
                else:
                    button_type = "secondary"
                
                if st.button(
                    option,
                    key=f"convert_tile_{option}",
                    type=button_type,
                    use_container_width=True
                ):
                    st.session_state.selected_convert_tile = option
                    st.rerun()
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True):
            if st.session_state.get("selected_convert_tile"):
                st.session_state.convert_user_answer = st.session_state.selected_convert_tile
                st.session_state.convert_show_feedback = True
                st.session_state.convert_answer_submitted = True
                st.rerun()
            else:
                st.warning("⚠️ Please select an answer first!")

def handle_conversion_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.convert_show_feedback:
        show_conversion_feedback()
    
    # Next question button
    if st.session_state.convert_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_conversion_state()
                st.rerun()

def show_conversion_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.convert_user_answer
    correct_answer = st.session_state.convert_correct_answer
    
    is_correct = user_answer == correct_answer
    
    st.markdown("---")
    st.markdown("### 📋 Results:")
    
    if is_correct:
        st.success("🎉 **Perfect! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.convert_decimals_difficulty
        st.session_state.convert_decimals_difficulty = min(
            st.session_state.convert_decimals_difficulty + 1, 5
        )
        
        if st.session_state.convert_decimals_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decimal form conversion!**")
        elif old_difficulty < st.session_state.convert_decimals_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.convert_decimals_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.convert_decimals_difficulty
        st.session_state.convert_decimals_difficulty = max(
            st.session_state.convert_decimals_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.convert_decimals_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.convert_decimals_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_conversion_explanation(is_correct)

def show_conversion_explanation(correct=True):
    """Show detailed explanation of the conversion process"""
    data = st.session_state.convert_question_data
    user_answer = st.session_state.convert_user_answer
    correct_answer = st.session_state.convert_correct_answer
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click for step-by-step solution**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">🔍 Step-by-Step Solution:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        expanded_form = data["expanded_form"]
        terms = data["terms"]
        
        st.markdown(f"""
        ### 📝 **Problem:**
        **Expanded Form:** {expanded_form}
        **Your Answer:** {user_answer}
        **Correct Answer:** {correct_answer}
        """)
        
        st.markdown("### 🔢 **Step-by-Step Calculation:**")
        
        running_total = 0
        for i, (digit, place_value) in enumerate(terms):
            term_value = digit * place_value
            running_total += term_value
            
            if place_value >= 1:
                if place_value == 1:
                    place_str = "1"
                else:
                    place_str = str(int(place_value))
            else:
                place_str = str(place_value)
            
            st.markdown(f"**Step {i+1}:** {digit} × {place_str} = {format_decimal(term_value)}")
        
        st.markdown("### ➕ **Adding All Terms:**")
        
        # Show the addition
        term_values = [format_decimal(digit * place_value) for digit, place_value in terms]
        addition_string = " + ".join(term_values)
        st.markdown(f"{addition_string} = **{correct_answer}**")
        
        # Show place value breakdown
        st.markdown("### 📊 **Place Value Breakdown:**")
        
        # Create a visual breakdown
        breakdown_parts = []
        for digit, place_value in terms:
            if place_value >= 1:
                if place_value == 1:
                    breakdown_parts.append(f"{digit} (ones)")
                elif place_value == 10:
                    breakdown_parts.append(f"{digit}0 (tens)")
                elif place_value == 100:
                    breakdown_parts.append(f"{digit}00 (hundreds)")
                elif place_value == 1000:
                    breakdown_parts.append(f"{digit}000 (thousands)")
            else:
                if place_value == 0.1:
                    breakdown_parts.append(f"0.{digit} (tenths)")
                elif place_value == 0.01:
                    breakdown_parts.append(f"0.0{digit} (hundredths)")
                elif place_value == 0.001:
                    breakdown_parts.append(f"0.00{digit} (thousandths)")
        
        for part in breakdown_parts:
            st.markdown(f"- {part}")
        
        st.markdown(f"**Final result:** {correct_answer}")
        
        if not correct:
            st.markdown("### 💡 **Common Mistakes to Check:**")
            st.markdown("- Did you multiply each digit by its place value?")
            st.markdown("- Did you add all the terms correctly?")
            st.markdown("- Did you place the decimal point in the right position?")
            st.markdown("- Did you account for all terms in the expression?")



def reset_conversion_state():
    """Reset state for next question"""
    st.session_state.current_convert_question = None
    st.session_state.convert_correct_answer = None
    st.session_state.convert_show_feedback = False
    st.session_state.convert_answer_submitted = False
    st.session_state.convert_question_data = {}
    st.session_state.selected_convert_tile = None
    
    # Clear any stored answers
    if "convert_user_answer" in st.session_state:
        del st.session_state.convert_user_answer