import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Compare percents to each other and to fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/M. Percent/compare_percents_to_each_other_and_to_fractions.py
    """
    # Initialize session state
    if "comparison_difficulty" not in st.session_state:
        st.session_state.comparison_difficulty = 1  # Start with easy comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_sign = None
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_incorrect = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > M. Percent**")
    st.title("⚖️ Compare Percents to Each Other and to Fractions")
    st.markdown("*Compare percents with percents, fractions, and decimals*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.comparison_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Comparisons",
            2: "Mixed Comparisons", 
            3: "Complex Comparisons"
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
        generate_new_comparison()
    
    # Display current question
    display_comparison_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Compare:
        
        **When comparing percents to percents:**
        - Simply compare the numbers
        - 45% > 38% because 45 > 38
        
        **When comparing percents to fractions:**
        - Convert one to match the other
        - Option 1: Convert fraction to percent
        - Option 2: Convert percent to fraction
        - Then compare
        
        **When comparing percents to decimals:**
        - Convert percent to decimal (divide by 100)
        - Or convert decimal to percent (multiply by 100)
        - Then compare
        
        ### Quick Reference:
        | Fraction | Decimal | Percent |
        |----------|---------|---------|
        | 1/2      | 0.5     | 50%     |
        | 1/4      | 0.25    | 25%     |
        | 3/4      | 0.75    | 75%     |
        | 1/5      | 0.2     | 20%     |
        | 2/5      | 0.4     | 40%     |
        | 3/5      | 0.6     | 60%     |
        | 4/5      | 0.8     | 80%     |
        | 1/10     | 0.1     | 10%     |
        
        ### Comparison Symbols:
        - **>** means "greater than"
        - **<** means "less than"
        - **=** means "equal to"
        
        ### Tips:
        - When values are close, convert to the same form
        - Remember: 50% = 0.5 = 1/2
        - Watch out for tricky ones like 33% vs 1/3
        """)

def generate_new_comparison():
    """Generate a new comparison question based on difficulty"""
    difficulty = st.session_state.comparison_difficulty
    
    # Choose comparison type
    comparison_types = ["percent_percent", "percent_fraction", "percent_decimal"]
    
    if difficulty == 1:
        # Easy: Focus on percent-to-percent and simple conversions
        weights = [0.5, 0.25, 0.25]
    elif difficulty == 2:
        # Medium: Balanced mix
        weights = [0.33, 0.34, 0.33]
    else:
        # Hard: Focus on trickier fraction and decimal comparisons
        weights = [0.2, 0.4, 0.4]
    
    comparison_type = random.choices(comparison_types, weights=weights)[0]
    
    if comparison_type == "percent_percent":
        generate_percent_percent_comparison(difficulty)
    elif comparison_type == "percent_fraction":
        generate_percent_fraction_comparison(difficulty)
    else:
        generate_percent_decimal_comparison(difficulty)

def generate_percent_percent_comparison(difficulty):
    """Generate percent to percent comparison"""
    if difficulty == 1:
        # Easy: Clear differences
        left = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        # Ensure different values
        options = [x for x in [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90] if x != left]
        right = random.choice(options)
    elif difficulty == 2:
        # Medium: Closer values
        left = random.choice([15, 25, 35, 45, 55, 65, 75, 85])
        offset = random.choice([-3, -2, -1, 1, 2, 3])
        right = left + offset
        # Ensure valid percent
        if right < 0 or right > 100:
            right = left - offset
    else:
        # Hard: Very close values or same values
        if random.random() < 0.3:  # 30% chance of equal values
            left = random.choice([37, 43, 67, 83])
            right = left
        else:
            left = random.randint(10, 90)
            right = left + random.choice([-1, 1])
    
    # Determine correct answer
    if left > right:
        correct_sign = ">"
    elif left < right:
        correct_sign = "<"
    else:
        correct_sign = "="
    
    st.session_state.question_data = {
        "left_value": f"{left}%",
        "right_value": f"{right}%",
        "left_percent": left,
        "right_percent": right,
        "comparison_type": "percent_percent"
    }
    st.session_state.correct_answer = correct_sign
    st.session_state.current_question = "comparison_question"  # Mark that we have a question

def generate_percent_fraction_comparison(difficulty):
    """Generate percent to fraction comparison"""
    if difficulty == 1:
        # Easy: Common fractions with clear differences
        fractions = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10)]
        numerator, denominator = random.choice(fractions)
        fraction_percent = (numerator / denominator) * 100
        
        # Choose a percent that's clearly different
        if fraction_percent > 50:
            percent = random.choice([10, 20, 30, 40])
        else:
            percent = random.choice([60, 70, 80, 90])
    
    elif difficulty == 2:
        # Medium: Closer values
        fractions = [(1, 3), (2, 3), (1, 6), (5, 6), (3, 8), (5, 8), (7, 8)]
        numerator, denominator = random.choice(fractions)
        fraction_percent = (numerator / denominator) * 100
        
        # Choose a percent within 10% of the fraction
        offset = random.randint(-10, 10)
        percent = int(fraction_percent + offset)
        percent = max(1, min(99, percent))  # Keep within valid range
    
    else:
        # Hard: Very close or equal values
        if random.random() < 0.3:  # 30% chance of equal values
            # Pick fractions that convert to nice percents
            equal_pairs = [
                ((1, 2), 50), ((1, 4), 25), ((3, 4), 75), 
                ((1, 5), 20), ((2, 5), 40), ((3, 5), 60), ((4, 5), 80)
            ]
            (numerator, denominator), percent = random.choice(equal_pairs)
        else:
            # Close but not equal
            fractions = [(1, 3), (2, 3), (1, 6), (5, 6), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
            numerator, denominator = random.choice(fractions)
            fraction_percent = (numerator / denominator) * 100
            percent = round(fraction_percent + random.choice([-1, 1]))
    
    # Randomly choose which side gets percent/fraction
    if random.random() < 0.5:
        left_is_percent = True
        left_value = f"{percent}%"
        right_value = f"{numerator}/{denominator}"
        left_percent = percent
        right_percent = (numerator / denominator) * 100
    else:
        left_is_percent = False
        left_value = f"{numerator}/{denominator}"
        right_value = f"{percent}%"
        left_percent = (numerator / denominator) * 100
        right_percent = percent
    
    # Determine correct answer
    if abs(left_percent - right_percent) < 0.0001:  # Account for floating point
        correct_sign = "="
    elif left_percent > right_percent:
        correct_sign = ">"
    else:
        correct_sign = "<"
    
    st.session_state.question_data = {
        "left_value": left_value,
        "right_value": right_value,
        "left_percent": left_percent,
        "right_percent": right_percent,
        "comparison_type": "percent_fraction",
        "fraction": (numerator, denominator)
    }
    st.session_state.correct_answer = correct_sign
    st.session_state.current_question = "comparison_question"  # Mark that we have a question

def generate_percent_decimal_comparison(difficulty):
    """Generate percent to decimal comparison"""
    if difficulty == 1:
        # Easy: Clear differences
        decimals = [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
        decimal = random.choice(decimals)
        decimal_as_percent = decimal * 100
        
        # Choose a percent that's clearly different
        if decimal_as_percent > 50:
            percent = random.choice([10, 20, 30, 40])
        else:
            percent = random.choice([60, 70, 80, 90])
    
    elif difficulty == 2:
        # Medium: Closer values
        decimal = round(random.uniform(0.1, 0.9), 2)
        decimal_as_percent = decimal * 100
        
        # Choose a percent within 5% of the decimal
        offset = random.randint(-5, 5)
        percent = int(decimal_as_percent + offset)
        percent = max(1, min(99, percent))
    
    else:
        # Hard: Very close or equal values, including > 1 and < 0.01
        if random.random() < 0.3:  # 30% chance of equal values
            percent = random.choice([25, 50, 75, 10, 20, 30, 40, 60, 70, 80, 90])
            decimal = percent / 100
        else:
            # Include challenging cases
            if random.random() < 0.3:
                # Decimal greater than 1
                decimal = round(random.uniform(1.01, 2.5), 2)
                decimal_as_percent = decimal * 100
                percent = int(decimal_as_percent + random.choice([-1, 0, 1]))
            elif random.random() < 0.5:
                # Very small decimal
                decimal = round(random.uniform(0.001, 0.099), 3)
                decimal_as_percent = decimal * 100
                percent = round(decimal_as_percent, 1)
            else:
                # Close regular values
                decimal = round(random.uniform(0.1, 0.9), 3)
                decimal_as_percent = decimal * 100
                percent = round(decimal_as_percent)
    
    # Randomly choose which side gets percent/decimal
    if random.random() < 0.5:
        left_is_percent = True
        left_value = f"{percent}%"
        right_value = str(decimal)
        left_percent = percent
        right_percent = decimal * 100
    else:
        left_is_percent = False
        left_value = str(decimal)
        right_value = f"{percent}%"
        left_percent = decimal * 100
        right_percent = percent
    
    # Determine correct answer
    if abs(left_percent - right_percent) < 0.0001:  # Account for floating point
        correct_sign = "="
    elif left_percent > right_percent:
        correct_sign = ">"
    else:
        correct_sign = "<"
    
    st.session_state.question_data = {
        "left_value": left_value,
        "right_value": right_value,
        "left_percent": left_percent,
        "right_percent": right_percent,
        "comparison_type": "percent_decimal",
        "decimal": decimal
    }
    st.session_state.correct_answer = correct_sign
    st.session_state.current_question = "comparison_question"  # Mark that we have a question

def display_comparison_question():
    """Display the current comparison question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Which sign makes the statement true?")
    
    # Display the comparison with placeholder
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"<div style='text-align: right; font-size: 24px; padding: 20px;'><b>{data['left_value']}</b></div>", unsafe_allow_html=True)
    
    with col2:
        if st.session_state.selected_sign:
            st.markdown(f"<div style='text-align: center; font-size: 24px; padding: 20px; color: #1f77b4;'><b>{st.session_state.selected_sign}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; font-size: 24px; padding: 20px;'>❓</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='text-align: left; font-size: 24px; padding: 20px;'><b>{data['right_value']}</b></div>", unsafe_allow_html=True)
    
    # Create clickable sign buttons
    st.markdown("### Choose the correct sign:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("**>**", key="greater", use_container_width=True, 
                    help="Greater than",
                    type="primary" if st.session_state.selected_sign == ">" else "secondary"):
            st.session_state.selected_sign = ">"
    
    with col2:
        if st.button("**<**", key="less", use_container_width=True,
                    help="Less than", 
                    type="primary" if st.session_state.selected_sign == "<" else "secondary"):
            st.session_state.selected_sign = "<"
    
    with col3:
        if st.button("**=**", key="equal", use_container_width=True,
                    help="Equal to",
                    type="primary" if st.session_state.selected_sign == "=" else "secondary"):
            st.session_state.selected_sign = "="
    
    # Submit button
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True, 
                    disabled=st.session_state.selected_sign is None):
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

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.selected_sign
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete statement
        st.markdown(f"### ✅ {data['left_value']} {correct_answer} {data['right_value']}")
        
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_incorrect = 0
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.comparison_difficulty
            st.session_state.comparison_difficulty = min(
                st.session_state.comparison_difficulty + 1, 3
            )
            
            if st.session_state.comparison_difficulty > old_difficulty:
                st.info(f"⬆️ **Difficulty increased! Now tackling more challenging comparisons.**")
                st.session_state.consecutive_correct = 0
            elif st.session_state.comparison_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've mastered all comparison types!**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct sign is **{correct_answer}**")
        
        # Show the correct statement
        st.markdown(f"### ✅ {data['left_value']} {correct_answer} {data['right_value']}")
        
        st.session_state.consecutive_incorrect += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive incorrect
        if st.session_state.consecutive_incorrect >= 3:
            old_difficulty = st.session_state.comparison_difficulty
            st.session_state.comparison_difficulty = max(
                st.session_state.comparison_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.comparison_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to help you practice. Keep going!**")
                st.session_state.consecutive_incorrect = 0
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the comparison"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"### Comparing {data['left_value']} and {data['right_value']}")
        
        if data["comparison_type"] == "percent_percent":
            st.markdown(f"""
            **Comparing two percents is straightforward:**
            - {data['left_value']} = {data['left_percent']}
            - {data['right_value']} = {data['right_percent']}
            - Since {data['left_percent']} {st.session_state.correct_answer} {data['right_percent']}
            - Therefore: {data['left_value']} {st.session_state.correct_answer} {data['right_value']}
            """)
        
        elif data["comparison_type"] == "percent_fraction":
            fraction = data["fraction"]
            fraction_as_percent = round((fraction[0] / fraction[1]) * 100, 2)
            
            st.markdown(f"""
            **To compare a percent and a fraction:**
            
            **Method 1: Convert fraction to percent**
            - {fraction[0]}/{fraction[1]} = {fraction[0]} ÷ {fraction[1]} = {fraction[0]/fraction[1]:.4f}
            - {fraction[0]/fraction[1]:.4f} × 100 = {fraction_as_percent}%
            
            **Method 2: Convert percent to fraction**
            - Convert the percent to a fraction over 100 and compare
            
            **Comparison:**
            - Left side = {data['left_percent']}%
            - Right side = {data['right_percent']}%
            - Since {data['left_percent']}% {st.session_state.correct_answer} {data['right_percent']}%
            - Therefore: {data['left_value']} {st.session_state.correct_answer} {data['right_value']}
            """)
        
        else:  # percent_decimal
            decimal = data["decimal"]
            decimal_as_percent = decimal * 100
            
            st.markdown(f"""
            **To compare a percent and a decimal:**
            
            **Method 1: Convert decimal to percent**
            - {decimal} × 100 = {decimal_as_percent}%
            
            **Method 2: Convert percent to decimal**
            - Divide the percent by 100
            
            **Comparison:**
            - Left side = {data['left_percent']}%
            - Right side = {data['right_percent']}%
            - Since {data['left_percent']}% {st.session_state.correct_answer} {data['right_percent']}%
            - Therefore: {data['left_value']} {st.session_state.correct_answer} {data['right_value']}
            """)
        
        # Add visual comparison
        st.markdown("---")
        st.markdown("### 📊 Visual Comparison:")
        
        # Create progress bars for visual comparison
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{data['left_value']}**")
            st.progress(min(data['left_percent'] / 100, 1.0))
            st.caption(f"= {data['left_percent']:.1f}%")
        
        with col2:
            st.markdown(f"**{data['right_value']}**")
            st.progress(min(data['right_percent'] / 100, 1.0))
            st.caption(f"= {data['right_percent']:.1f}%")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_sign = None