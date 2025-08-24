import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Add up to 4 fractions with denominators of 10 and 100 activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/add_up_to_4_fractions_with_denominators_of_10_and_100.py
    """
    # Initialize session state for difficulty
    if "fractions_10_100_difficulty" not in st.session_state:
        st.session_state.fractions_10_100_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "fractions_10_100_score" not in st.session_state:
        st.session_state.fractions_10_100_score = 0
        st.session_state.fractions_10_100_attempts = 0
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_incorrect = 0
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_options = []
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.selected_options = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕ Add Fractions with Denominators of 10 and 100")
    st.markdown("*Find expressions that equal the target fraction*")
    st.markdown("---")
    
    # Difficulty and score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        difficulty_colors = {1: "🟢", 2: "🟡", 3: "🔴"}
        st.markdown(f"**Difficulty:** {difficulty_colors[st.session_state.fractions_10_100_difficulty]} {difficulty_names[st.session_state.fractions_10_100_difficulty]}")
        st.markdown(f"**Score:** {st.session_state.fractions_10_100_score}/{st.session_state.fractions_10_100_attempts}")
        
        # Progress bar for difficulty
        progress = (st.session_state.fractions_10_100_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.fractions_10_100_difficulty}/3")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Tips for Adding with 10 and 100**", expanded=False):
        st.markdown("""
        ### Key Concepts:
        - **10 and 100 are related**: 100 = 10 × 10
        - **Convert to same denominator**: 1/10 = 10/100
        - **Add numerators**: Once denominators match, add the numerators
        
        ### Examples:
        - **3/10 + 25/100**
          - Convert: 3/10 = 30/100
          - Add: 30/100 + 25/100 = 55/100
        
        - **1/10 + 2/10 + 30/100**
          - Convert: 1/10 = 10/100, 2/10 = 20/100
          - Add: 10/100 + 20/100 + 30/100 = 60/100
        
        ### Quick Conversion:
        - To convert from 10 to 100: multiply numerator by 10
        - Examples: 1/10 = 10/100, 4/10 = 40/100, 7/10 = 70/100
        """)

def generate_new_question():
    """Generate a new multiple choice question based on difficulty"""
    difficulty = st.session_state.fractions_10_100_difficulty
    
    if difficulty == 1:  # Easy - smaller numbers, 2 fractions, 1 correct answer
        # Generate target fraction (20-50)
        target_numerator = random.randint(20, 50)
        target_fraction = Fraction(target_numerator, 100)
        
        # Generate 1 correct expression (simple)
        correct_expressions = []
        
        # Simple split with round numbers
        if target_numerator % 10 == 0:
            expr = [(target_numerator // 10, 10)]
        else:
            tens = target_numerator // 10
            ones = target_numerator % 10
            expr = [(tens, 10), (ones * 10, 100)]
        correct_expressions.append(expr)
        
        # Generate 1 incorrect expression
        incorrect_expressions = []
        wrong_target = target_numerator + random.choice([-10, 10])
        if 10 <= wrong_target <= 100:
            if wrong_target % 10 == 0:
                expr = [(wrong_target // 10, 10)]
            else:
                tens = wrong_target // 10
                ones = wrong_target % 10
                expr = [(tens, 10), (ones * 10, 100)]
            incorrect_expressions.append(expr)
        
        num_options = 2
        
    elif difficulty == 2:  # Medium - larger numbers, 3 fractions, 1-2 correct answers
        # Generate target fraction (40-80)
        target_numerator = random.randint(40, 80)
        target_fraction = Fraction(target_numerator, 100)
        
        # Generate 1-2 correct expressions
        correct_expressions = []
        
        # Type 1: Two fractions
        tens_part = random.randint(1, target_numerator // 10)
        hundreds_part = target_numerator - (tens_part * 10)
        if hundreds_part >= 0:
            expr = [(tens_part, 10), (hundreds_part, 100)]
            correct_expressions.append(expr)
        
        # Type 2: Three fractions (sometimes)
        if target_numerator >= 30 and random.choice([True, False]):
            part1 = random.randint(1, 3)
            part2 = random.randint(1, 3)
            part3 = target_numerator - (part1 * 10) - (part2 * 10)
            if 0 <= part3 < 100:
                expr = [(part1, 10), (part2, 10), (part3, 100)]
                correct_expressions.append(expr)
        
        # Generate 1-2 incorrect expressions
        incorrect_expressions = []
        for offset in [-20, -10, 10, 20]:
            wrong_target = target_numerator + offset
            if 10 <= wrong_target <= 100 and len(incorrect_expressions) < 2:
                tens = wrong_target // 10
                ones = wrong_target % 10
                if ones == 0:
                    expr = [(tens, 10)]
                else:
                    expr = [(tens, 10), (ones * 10, 100)]
                incorrect_expressions.append(expr)
        
        num_options = 3
        
    else:  # Hard - any numbers, 4 fractions, 2-3 correct answers
        # Generate target fraction (50-95)
        target_numerator = random.randint(50, 95)
        target_fraction = Fraction(target_numerator, 100)
        
        # Generate 2-3 correct expressions
        correct_expressions = []
        
        # Type 1: Mixed denominators
        tens_part = random.randint(2, min(8, target_numerator // 10))
        hundreds_part = target_numerator - (tens_part * 10)
        expr = [(tens_part, 10), (hundreds_part, 100)]
        correct_expressions.append(expr)
        
        # Type 2: Three fractions
        part1 = random.randint(1, 3)
        part2 = random.randint(1, 3)
        part3 = target_numerator - (part1 * 10) - (part2 * 10)
        if 0 <= part3 < 100:
            expr = [(part1, 10), (part2, 10), (part3, 100)]
            random.shuffle(expr)
            correct_expressions.append(expr)
        
        # Type 3: Four fractions (if possible)
        if target_numerator >= 40:
            p1 = random.randint(1, 2)
            p2 = random.randint(1, 2)
            p3 = random.randint(1, 2)
            p4 = target_numerator - (p1 * 10) - (p2 * 10) - (p3 * 10)
            if 0 <= p4 < 100:
                expr = [(p1, 10), (p2, 10), (p3, 10), (p4, 100)]
                random.shuffle(expr)
                correct_expressions.append(expr)
        
        # Generate incorrect expressions
        incorrect_expressions = []
        
        # Common mistake: not converting properly
        part1 = random.randint(1, 9)
        part2 = target_numerator - part1
        if 0 < part2 < 100:
            expr = [(part1, 10), (part2, 100)]
            incorrect_expressions.append(expr)
        
        # Off by 10 or 20
        for offset in [-30, -20, 20, 30]:
            wrong_target = target_numerator + offset
            if 10 <= wrong_target <= 100:
                tens = random.randint(1, min(9, wrong_target // 10))
                ones = wrong_target - (tens * 10)
                if ones >= 0:
                    expr = [(tens, 10), (ones, 100)]
                    incorrect_expressions.append(expr)
        
        num_options = 4
    
    # Select options based on difficulty
    if difficulty == 1:
        # 1 correct, 1 incorrect
        selected_correct = correct_expressions[:1]
        selected_incorrect = incorrect_expressions[:1]
    elif difficulty == 2:
        # 1-2 correct, rest incorrect
        num_correct = random.randint(1, min(2, len(correct_expressions)))
        selected_correct = random.sample(correct_expressions, num_correct)
        selected_incorrect = random.sample(incorrect_expressions, min(num_options - num_correct, len(incorrect_expressions)))
    else:
        # 2-3 correct, rest incorrect
        num_correct = random.randint(2, min(3, len(correct_expressions)))
        selected_correct = random.sample(correct_expressions, num_correct)
        selected_incorrect = random.sample(incorrect_expressions, min(num_options - num_correct, len(incorrect_expressions)))
    
    # Create options list
    options = selected_correct + selected_incorrect
    
    # Shuffle options
    random.shuffle(options)
    
    # Store question data
    st.session_state.current_question = {
        "target": target_fraction,
        "target_display": f"{target_numerator}/100",
        "options": options,
        "correct_indices": [i for i, opt in enumerate(options) if opt in selected_correct]
    }
    st.session_state.correct_options = st.session_state.current_question["correct_indices"]
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.selected_options = []

def format_expression(expr):
    """Format an expression for display"""
    parts = []
    for i, (num, denom) in enumerate(expr):
        if i > 0:
            parts.append(" + ")
        parts.append(f"{num}/{denom}")
    return "".join(parts)

def display_question():
    """Display the current question"""
    question = st.session_state.current_question
    
    # Display question
    st.markdown(f"### Which of the following expressions equal {question['target_display']}?")
    if len(question['correct_indices']) > 1:
        st.markdown("*Select all correct answers*")
    else:
        st.markdown("*Select the correct answer*")
    
    # Create checkboxes for each option
    st.markdown("")
    
    # Track selected options
    selected = []
    
    for i, option in enumerate(question['options']):
        # Format the expression
        expr_text = format_expression(option)
        
        # Create checkbox with custom styling
        col1, col2 = st.columns([0.1, 3])
        with col1:
            # Use a checkbox
            is_selected = st.checkbox(
                "",
                key=f"option_{i}",
                value=i in st.session_state.selected_options,
                disabled=st.session_state.answer_submitted
            )
            if is_selected and i not in selected:
                selected.append(i)
        
        with col2:
            # Display the expression in a box
            if st.session_state.show_feedback:
                # Show feedback colors
                if i in question['correct_indices']:
                    if i in st.session_state.selected_options:
                        st.success(f"✅ {expr_text}")
                    else:
                        st.warning(f"⚠️ {expr_text} (This was correct!)")
                else:
                    if i in st.session_state.selected_options:
                        st.error(f"❌ {expr_text}")
                    else:
                        st.info(f"{expr_text}")
            else:
                # Normal display
                st.markdown(
                    f"""<div style="
                        padding: 10px;
                        background-color: {'#e3f2fd' if i in selected else '#f5f5f5'};
                        border-radius: 5px;
                        margin: 5px 0;
                        font-size: 18px;
                    ">{expr_text}</div>""",
                    unsafe_allow_html=True
                )
    
    # Update selected options
    if not st.session_state.answer_submitted:
        st.session_state.selected_options = [i for i in range(len(question['options'])) 
                                            if st.session_state.get(f"option_{i}", False)]
    
    st.markdown("")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.answer_submitted:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                if st.session_state.selected_options:
                    st.session_state.answer_submitted = True
                    st.session_state.show_feedback = True
                    st.session_state.fractions_10_100_attempts += 1
                    st.rerun()
                else:
                    st.warning("Please select at least one answer.")
    
    # Show feedback and next button
    if st.session_state.show_feedback:
        show_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    question = st.session_state.current_question
    selected = set(st.session_state.selected_options)
    correct = set(question['correct_indices'])
    
    # Check if answer is correct
    is_correct = selected == correct
    
    if is_correct:
        st.success("🎉 **Perfect! You found all the correct expressions!**")
        st.session_state.fractions_10_100_score += 1
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_incorrect = 0
        
        # Check for difficulty increase
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.fractions_10_100_difficulty
            st.session_state.fractions_10_100_difficulty = min(3, old_difficulty + 1)
            if st.session_state.fractions_10_100_difficulty > old_difficulty:
                st.info(f"⬆️ **Level up! Moving to {['', 'Easy', 'Medium', 'Hard'][st.session_state.fractions_10_100_difficulty]} level.**")
                st.balloons()
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_incorrect += 1
        st.session_state.consecutive_correct = 0
        
        if selected.issubset(correct) and len(selected) > 0:
            st.warning("⚠️ **Partially correct!** You selected correct answers but missed some.")
        elif correct.issubset(selected) and len(correct) > 0:
            st.error("❌ **Almost there!** You selected all correct answers but also some incorrect ones.")
        else:
            st.error("❌ **Not quite right.** Review which expressions equal the target.")
        
        # Check for difficulty decrease
        if st.session_state.consecutive_incorrect >= 3:
            old_difficulty = st.session_state.fractions_10_100_difficulty
            st.session_state.fractions_10_100_difficulty = max(1, old_difficulty - 1)
            if st.session_state.fractions_10_100_difficulty < old_difficulty:
                st.info(f"⬇️ **Let's practice more at {['', 'Easy', 'Medium', 'Hard'][st.session_state.fractions_10_100_difficulty]} level.**")
            st.session_state.consecutive_incorrect = 0
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answers"""
    question = st.session_state.current_question
    
    with st.expander("📖 **See Explanation**", expanded=True):
        st.markdown("### Let's calculate each expression:")
        
        for i, option in enumerate(question['options']):
            st.markdown(f"**Expression {i+1}: {format_expression(option)}**")
            
            # Calculate the sum
            total = Fraction(0)
            steps = []
            
            # Convert all to denominator 100
            for num, denom in option:
                if denom == 10:
                    converted = num * 10
                    steps.append(f"{num}/10 = {converted}/100")
                    total += Fraction(converted, 100)
                else:
                    steps.append(f"{num}/100 = {num}/100")
                    total += Fraction(num, 100)
            
            # Show conversion steps
            if any(denom == 10 for _, denom in option):
                st.markdown("Convert to common denominator:")
                for step in steps:
                    st.markdown(f"- {step}")
            
            # Show sum
            nums = []
            for num, denom in option:
                if denom == 10:
                    nums.append(f"{num * 10}/100")
                else:
                    nums.append(f"{num}/100")
            
            st.markdown(f"Sum: {' + '.join(nums)} = {total.numerator}/100")
            
            # Show if it equals target
            if total == question['target']:
                st.markdown(f"✅ **Equals {question['target_display']}**")
            else:
                st.markdown(f"❌ Does not equal {question['target_display']}")
            
            st.markdown("")

def reset_question():
    """Reset for next question"""
    st.session_state.current_question = None
    st.session_state.correct_options = []
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.selected_options = []
    
    # Clear checkbox states
    i = 0
    while f"option_{i}" in st.session_state:
        del st.session_state[f"option_{i}"]
        i += 1