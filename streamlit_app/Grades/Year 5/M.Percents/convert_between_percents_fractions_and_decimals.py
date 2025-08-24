import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Convert between percents, fractions and decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/M. Percent/convert_between_percents_fractions_and_decimals.py
    """
    # Initialize session state
    if "conversion_difficulty" not in st.session_state:
        st.session_state.conversion_difficulty = 1  # Start with easy conversions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.conversion_type = None
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_incorrect = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > M. Percent**")
    st.title("🔄 Convert Between Percents, Fractions and Decimals")
    st.markdown("*Master conversions between different number representations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.conversion_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Conversions",
            2: "Common Fractions", 
            3: "Complex Conversions"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
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
        ### Conversion Rules:
        
        **🔄 Percent ↔ Decimal:**
        - Percent to Decimal: Divide by 100 (move decimal 2 places left)
        - Decimal to Percent: Multiply by 100 (move decimal 2 places right)
        - Example: 25% = 0.25, 0.75 = 75%
        
        **🔄 Percent ↔ Fraction:**
        - Percent to Fraction: Write over 100, then simplify
        - Fraction to Percent: Divide numerator by denominator, multiply by 100
        - Example: 50% = 50/100 = 1/2, 3/4 = 0.75 = 75%
        
        **🔄 Decimal ↔ Fraction:**
        - Decimal to Fraction: Write decimal places as denominator power of 10
        - Fraction to Decimal: Divide numerator by denominator
        - Example: 0.25 = 25/100 = 1/4, 2/5 = 0.4
        
        ### Common Equivalents to Memorize:
        - **1/2 = 0.5 = 50%**
        - **1/4 = 0.25 = 25%**
        - **3/4 = 0.75 = 75%**
        - **1/5 = 0.2 = 20%**
        - **1/10 = 0.1 = 10%**
        
        ### Difficulty Levels:
        - **🟢 Easy:** Basic percents, simple decimals, common fractions
        - **🟡 Medium:** Two-digit percents, repeating decimals, various fractions
        - **🔴 Hard:** Complex conversions, mixed numbers, challenging fractions
        """)

def generate_new_question():
    """Generate a new conversion question based on difficulty"""
    difficulty = st.session_state.conversion_difficulty
    
    # Define conversion types
    conversion_types = [
        "percent_to_fraction",
        "percent_to_decimal",
        "fraction_to_percent",
        "fraction_to_decimal",
        "decimal_to_percent",
        "decimal_to_fraction"
    ]
    
    # Choose a random conversion type
    conversion_type = random.choice(conversion_types)
    st.session_state.conversion_type = conversion_type
    
    # Generate question based on type and difficulty
    if conversion_type == "percent_to_fraction":
        generate_percent_to_fraction(difficulty)
    elif conversion_type == "percent_to_decimal":
        generate_percent_to_decimal(difficulty)
    elif conversion_type == "fraction_to_percent":
        generate_fraction_to_percent(difficulty)
    elif conversion_type == "fraction_to_decimal":
        generate_fraction_to_decimal(difficulty)
    elif conversion_type == "decimal_to_percent":
        generate_decimal_to_percent(difficulty)
    else:  # decimal_to_fraction
        generate_decimal_to_fraction(difficulty)

def generate_percent_to_fraction(difficulty):
    """Generate percent to fraction conversion"""
    if difficulty == 1:
        # Easy: multiples of 10, 25, 50
        percents = [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100]
        percent = random.choice(percents)
    elif difficulty == 2:
        # Medium: any multiple of 5
        percent = random.choice([5, 15, 35, 45, 55, 65, 85, 95])
    else:
        # Hard: any percent
        percent = random.randint(1, 99)
    
    # Calculate fraction and simplify
    fraction = Fraction(percent, 100)
    
    st.session_state.question_data = {
        "value": f"{percent}%",
        "percent": percent,
        "answer_str": f"{fraction.numerator}/{fraction.denominator}" if fraction.denominator != 1 else str(fraction.numerator)
    }
    st.session_state.correct_answer = st.session_state.question_data["answer_str"]
    st.session_state.current_question = f"How do you write {percent}% as a fraction?"

def generate_percent_to_decimal(difficulty):
    """Generate percent to decimal conversion"""
    if difficulty == 1:
        # Easy: whole number percents
        percent = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100])
    elif difficulty == 2:
        # Medium: include single decimal percents
        percent = random.choice([12.5, 37.5, 62.5, 87.5, 15, 35, 45, 55, 65, 85, 95])
    else:
        # Hard: any percent including decimals
        percent = round(random.uniform(0.1, 99.9), 1)
    
    decimal = percent / 100
    
    st.session_state.question_data = {
        "value": f"{percent}%",
        "percent": percent,
        "answer": decimal,
        "answer_str": str(decimal).rstrip('0').rstrip('.')
    }
    st.session_state.correct_answer = st.session_state.question_data["answer_str"]
    st.session_state.current_question = f"How do you write {percent}% as a decimal?"

def generate_fraction_to_percent(difficulty):
    """Generate fraction to percent conversion"""
    if difficulty == 1:
        # Easy: common fractions
        fractions = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10)]
        numerator, denominator = random.choice(fractions)
    elif difficulty == 2:
        # Medium: more fractions
        fractions = [(1, 3), (2, 3), (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8), (1, 20), (3, 20), (7, 20), (9, 20)]
        numerator, denominator = random.choice(fractions)
    else:
        # Hard: any proper fraction
        denominator = random.choice([3, 6, 7, 8, 9, 12, 15, 16, 20, 25, 40, 50])
        numerator = random.randint(1, denominator - 1)
        # Ensure it's in simplest form
        f = Fraction(numerator, denominator)
        numerator, denominator = f.numerator, f.denominator
    
    percent = round((numerator / denominator) * 100, 2)
    # Format answer
    if percent == int(percent):
        answer_str = str(int(percent))
    else:
        answer_str = f"{percent:.10g}".rstrip('0').rstrip('.')
    
    st.session_state.question_data = {
        "value": f"{numerator}/{denominator}",
        "numerator": numerator,
        "denominator": denominator,
        "answer": percent,
        "answer_str": answer_str
    }
    st.session_state.correct_answer = answer_str
    st.session_state.current_question = f"How do you write {numerator}/{denominator} as a percentage?"

def generate_fraction_to_decimal(difficulty):
    """Generate fraction to decimal conversion"""
    if difficulty == 1:
        # Easy: fractions that convert to terminating decimals
        fractions = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10)]
        numerator, denominator = random.choice(fractions)
    elif difficulty == 2:
        # Medium: include eighths and twentieths
        fractions = [(1, 8), (3, 8), (5, 8), (7, 8), (1, 20), (3, 20), (7, 20), (9, 20), (11, 20)]
        numerator, denominator = random.choice(fractions)
    else:
        # Hard: include repeating decimals
        fractions = [(1, 3), (2, 3), (1, 6), (5, 6), (1, 9), (2, 9), (4, 9), (5, 9), (7, 9), (8, 9)]
        numerator, denominator = random.choice(fractions)
    
    decimal = numerator / denominator
    
    # Format answer appropriately
    if denominator in [3, 6, 9]:  # Repeating decimals
        if denominator == 3:
            if numerator == 1:
                answer_str = "0.333... or 0.3̄"
            else:
                answer_str = "0.666... or 0.6̄"
        elif denominator == 6:
            if numerator == 1:
                answer_str = "0.166... or 0.16̄"
            else:
                answer_str = "0.833... or 0.83̄"
        else:  # denominator == 9
            digit = str(numerator)
            answer_str = f"0.{digit}{digit}{digit}... or 0.{digit}̄"
    else:
        answer_str = f"{decimal:.10g}".rstrip('0').rstrip('.')
    
    st.session_state.question_data = {
        "value": f"{numerator}/{denominator}",
        "numerator": numerator,
        "denominator": denominator,
        "answer": decimal,
        "answer_str": answer_str,
        "is_repeating": denominator in [3, 6, 9]
    }
    st.session_state.correct_answer = answer_str
    st.session_state.current_question = f"How do you write {numerator}/{denominator} as a decimal?"

def generate_decimal_to_percent(difficulty):
    """Generate decimal to percent conversion"""
    if difficulty == 1:
        # Easy: one or two decimal places
        decimal = random.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9])
    elif difficulty == 2:
        # Medium: include hundredths
        decimal = round(random.uniform(0.01, 0.99), 2)
    else:
        # Hard: include numbers greater than 1 and smaller than 0.01
        if random.random() < 0.5:
            decimal = round(random.uniform(1.01, 2.5), 2)
        else:
            decimal = round(random.uniform(0.001, 0.099), 3)
    
    percent = decimal * 100
    # Format answer
    if percent == int(percent):
        answer_str = str(int(percent))
    else:
        answer_str = f"{percent:.10g}".rstrip('0').rstrip('.')
    
    st.session_state.question_data = {
        "value": str(decimal),
        "decimal": decimal,
        "answer": percent,
        "answer_str": answer_str
    }
    st.session_state.correct_answer = answer_str
    st.session_state.current_question = f"How do you write {decimal} as a percentage?"

def generate_decimal_to_fraction(difficulty):
    """Generate decimal to fraction conversion"""
    if difficulty == 1:
        # Easy: tenths and hundredths
        decimals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.25, 0.75]
        decimal = random.choice(decimals)
    elif difficulty == 2:
        # Medium: more complex decimals
        decimal = round(random.choice([0.125, 0.375, 0.625, 0.875, 0.05, 0.15, 0.35, 0.45]), 3)
    else:
        # Hard: thousandths
        decimal = round(random.uniform(0.001, 0.999), 3)
    
    # Convert to fraction
    fraction = Fraction(str(decimal)).limit_denominator()
    
    st.session_state.question_data = {
        "value": str(decimal),
        "decimal": decimal,
        "answer_str": f"{fraction.numerator}/{fraction.denominator}" if fraction.denominator != 1 else str(fraction.numerator)
    }
    st.session_state.correct_answer = st.session_state.question_data["answer_str"]
    st.session_state.current_question = f"How do you write {decimal} as a fraction?"

def display_question():
    """Display the current question interface"""
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Add specific instructions based on conversion type
    conversion_type = st.session_state.conversion_type
    if "percent" in conversion_type and conversion_type.endswith("percent"):
        st.markdown("*Write your answer using a percent sign (%).*")
    elif conversion_type.endswith("fraction"):
        st.markdown("*Write your answer as a simplified fraction (e.g., 1/2, 3/4).*")
    elif conversion_type.endswith("decimal"):
        st.markdown("*Write your answer as a decimal number.*")
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.text_input(
                "Your answer:",
                key="conversion_input",
                placeholder="Enter your answer",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.user_answer = user_answer.strip()
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def validate_answer(user_answer, correct_answer, conversion_type):
    """Validate user answer with flexibility for different formats"""
    # Clean up user answer
    user_answer = user_answer.strip().replace(" ", "")
    
    # Handle percent answers
    if "to_percent" in conversion_type:
        # Accept with or without % sign
        user_answer = user_answer.rstrip('%')
        correct_answer = correct_answer.rstrip('%')
        
        try:
            return float(user_answer) == float(correct_answer)
        except:
            return False
    
    # Handle fraction answers
    elif conversion_type.endswith("fraction"):
        # Accept various fraction formats
        try:
            # Try to parse as fraction
            if '/' in user_answer:
                parts = user_answer.split('/')
                if len(parts) == 2:
                    user_num = int(parts[0])
                    user_den = int(parts[1])
                    user_frac = Fraction(user_num, user_den)
                    
                    # Parse correct answer
                    if '/' in correct_answer:
                        parts = correct_answer.split('/')
                        correct_num = int(parts[0])
                        correct_den = int(parts[1])
                        correct_frac = Fraction(correct_num, correct_den)
                    else:
                        correct_frac = Fraction(int(correct_answer))
                    
                    return user_frac == correct_frac
            else:
                # Whole number
                return int(user_answer) == int(correct_answer)
        except:
            return False
    
    # Handle decimal answers
    else:
        # For repeating decimals, accept multiple formats
        if "repeating" in st.session_state.question_data and st.session_state.question_data.get("is_repeating"):
            # Check various representations
            acceptable_answers = correct_answer.split(" or ")
            user_lower = user_answer.lower()
            
            for acceptable in acceptable_answers:
                if user_lower == acceptable.lower():
                    return True
                # Also check without special characters
                clean_user = user_lower.replace("...", "").replace("̄", "")
                clean_acceptable = acceptable.lower().replace("...", "").replace("̄", "")
                if clean_user.startswith(clean_acceptable[:5]):  # Check first 5 chars
                    return True
            return False
        else:
            try:
                return float(user_answer) == float(correct_answer)
            except:
                return False

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    conversion_type = st.session_state.conversion_type
    
    # Validate answer
    is_correct = validate_answer(user_answer, correct_answer, conversion_type)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_incorrect = 0
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.conversion_difficulty
            st.session_state.conversion_difficulty = min(
                st.session_state.conversion_difficulty + 1, 3
            )
            
            if st.session_state.conversion_difficulty > old_difficulty:
                st.info(f"⬆️ **Difficulty increased! Now tackling more complex conversions.**")
                st.session_state.consecutive_correct = 0
            elif st.session_state.conversion_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've mastered all conversion types!**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**.")
        st.session_state.consecutive_incorrect += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive incorrect
        if st.session_state.consecutive_incorrect >= 3:
            old_difficulty = st.session_state.conversion_difficulty
            st.session_state.conversion_difficulty = max(
                st.session_state.conversion_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.conversion_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to help you practice. Keep going!**")
                st.session_state.consecutive_incorrect = 0
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    conversion_type = st.session_state.conversion_type
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"### Converting {data['value']}:")
        
        if conversion_type == "percent_to_fraction":
            st.markdown(f"""
            **Step 1:** Write the percent as a fraction over 100
            - {data['percent']}% = {data['percent']}/100
            
            **Step 2:** Simplify the fraction
            - Find the GCD of {data['percent']} and 100
            - {data['percent']}/100 = **{st.session_state.correct_answer}**
            
            **Remember:** Percent means "per hundred"!
            """)
            
        elif conversion_type == "percent_to_decimal":
            st.markdown(f"""
            **Method:** Divide by 100 (or move decimal point 2 places left)
            - {data['percent']}% ÷ 100 = **{st.session_state.correct_answer}**
            
            **Quick tip:** Just move the decimal point 2 places to the left!
            - {data['percent']}.% → {st.session_state.correct_answer}
            """)
            
        elif conversion_type == "fraction_to_percent":
            decimal_value = data['numerator'] / data['denominator']
            st.markdown(f"""
            **Method 1:** Convert to decimal first, then multiply by 100
            - {data['value']} = {decimal_value:.6g}
            - {decimal_value:.6g} × 100 = **{st.session_state.correct_answer}%**
            
            **Method 2:** Cross multiply with x/100
            - {data['value']} = x/100
            - {data['numerator']} × 100 = {data['denominator']} × x
            - x = {data['numerator'] * 100} ÷ {data['denominator']} = **{st.session_state.correct_answer}**
            """)
            
        elif conversion_type == "fraction_to_decimal":
            st.markdown(f"""
            **Method:** Divide numerator by denominator
            - {data['value']} = {data['numerator']} ÷ {data['denominator']}
            - = **{st.session_state.correct_answer}**
            
            **Calculator tip:** Simply divide top by bottom!
            """)
            if data.get("is_repeating"):
                st.markdown("""
                **Note:** This is a repeating decimal. You can write it with:
                - Three dots (...) to show it repeats
                - A bar over the repeating digit(s)
                """)
                
        elif conversion_type == "decimal_to_percent":
            st.markdown(f"""
            **Method:** Multiply by 100 (or move decimal point 2 places right)
            - {data['value']} × 100 = **{st.session_state.correct_answer}%**
            
            **Quick tip:** Just move the decimal point 2 places to the right!
            """)
            
        else:  # decimal_to_fraction
            # Show decimal place analysis
            decimal_str = str(data['decimal'])
            decimal_places = len(decimal_str.split('.')[-1]) if '.' in decimal_str else 0
            denominator_power = 10 ** decimal_places
            
            st.markdown(f"""
            **Step 1:** Count decimal places
            - {data['value']} has {decimal_places} decimal place(s)
            
            **Step 2:** Write as fraction with denominator {denominator_power}
            - {data['value']} = {int(data['decimal'] * denominator_power)}/{denominator_power}
            
            **Step 3:** Simplify
            - {int(data['decimal'] * denominator_power)}/{denominator_power} = **{st.session_state.correct_answer}**
            """)
        
        # Add conversion chart
        st.markdown("""
        ---
        ### 🔄 Quick Reference Chart:
        | Fraction | Decimal | Percent |
        |----------|---------|---------|
        | 1/2      | 0.5     | 50%     |
        | 1/4      | 0.25    | 25%     |
        | 3/4      | 0.75    | 75%     |
        | 1/5      | 0.2     | 20%     |
        | 1/10     | 0.1     | 10%     |
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.conversion_type = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer