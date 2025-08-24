import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Compare percents and fractions: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/M. Percent/compare_percents_and_fractions_word_problems.py
    """
    # Initialize session state
    if "word_comparison_difficulty" not in st.session_state:
        st.session_state.word_comparison_difficulty = 1  # Start with easy comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_option = None
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_incorrect = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > M. Percent**")
    st.title("📊 Compare Percents and Fractions: Word Problems")
    st.markdown("*Determine which option has the greater percentage*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_comparison_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Scenarios",
            2: "Intermediate Problems", 
            3: "Complex Situations"
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
        generate_new_word_problem()
    
    # Display current question
    display_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve These Problems:
        
        **Step 1: Read the problem carefully**
        - Identify the two values being compared
        - Note if they're percents, fractions, or decimals
        
        **Step 2: Convert to the same form**
        - Convert fractions to percents: multiply by 100
        - Convert decimals to percents: multiply by 100
        - Or convert all to decimals for comparison
        
        **Step 3: Compare and choose**
        - Click the option with the greater percentage
        
        ### Common Conversions:
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
        | 1/3      | 0.333...| 33.3%   |
        | 2/3      | 0.666...| 66.7%   |
        
        ### Remember:
        - Read carefully to understand what's being compared
        - Convert to the same form before comparing
        - Think about which value represents a larger portion
        """)

def generate_new_word_problem():
    """Generate a new comparison word problem based on difficulty"""
    difficulty = st.session_state.word_comparison_difficulty
    
    # Define problem templates based on difficulty
    if difficulty == 1:
        # Easy: Common fractions and simple percents
        problems = [
            {
                "context": "At Delia's Desserts, {fraction} of the items sold were cupcakes. At Harvest Bakery, cupcakes made up {percent}% of the items sold.",
                "question": "Which bakery had a greater percentage of cupcakes sold?",
                "option1": "Delia's Desserts",
                "option2": "Harvest Bakery",
                "type": "fraction_percent",
                "fractions": [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10)],
                "percents": [20, 30, 40, 50, 60, 70, 80, 25, 75, 10]
            },
            {
                "context": "Yesterday, {percent1}% of the flights at Richmond County Airport were delayed. At Greene County Airport, {fraction} of the flights were delayed.",
                "question": "Which airport had a higher percentage of delayed flights?",
                "option1": "Richmond County Airport",
                "option2": "Greene County Airport",
                "type": "percent_fraction",
                "percents": [30, 40, 50, 60, 20, 35, 45, 55, 65, 25],
                "fractions": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5)]
            },
            {
                "context": "Yesterday, Tina bought {percent}% of the items on her shopping list. Vivian purchased {fraction} of the items on her shopping list.",
                "question": "Who bought a greater percentage of the items on her shopping list?",
                "option1": "Tina",
                "option2": "Vivian",
                "type": "percent_fraction",
                "percents": [20, 30, 40, 50, 60, 70, 80, 25, 75, 15],
                "fractions": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5)]
            },
            {
                "context": "In Store A, {percent1}% of customers made a purchase. In Store B, {percent2}% of customers made a purchase.",
                "question": "Which store had a greater percentage of customers making purchases?",
                "option1": "Store A",
                "option2": "Store B",
                "type": "percent_percent",
                "percent_pairs": [(45, 55), (30, 70), (60, 40), (25, 75), (80, 20), (35, 65), (15, 85)]
            }
        ]
    
    elif difficulty == 2:
        # Medium: Less common fractions, closer values
        problems = [
            {
                "context": "Last year, {percent}% of Oliver's friends learnt how to ride bikes, while {fraction} of Nolan's friends learnt how to ride bikes.",
                "question": "Who had a greater percentage of friends who learnt how to ride bikes last year?",
                "option1": "Oliver",
                "option2": "Nolan",
                "type": "percent_fraction",
                "percents": [33, 37, 42, 48, 52, 58, 62, 67, 73, 38],
                "fractions": [(1, 3), (2, 3), (3, 8), (5, 8), (2, 7), (3, 7), (4, 7), (5, 9), (7, 9)]
            },
            {
                "context": "A supermarket found that {fraction} of customers bought produce and {percent}% of customers bought processed food.",
                "question": "Which purchase was made by a greater percentage of customers?",
                "option1": "produce",
                "option2": "processed food",
                "type": "fraction_percent",
                "fractions": [(2, 5), (3, 7), (5, 8), (4, 9), (5, 11), (7, 12), (3, 8), (5, 12), (7, 15)],
                "percents": [45, 52, 38, 61, 47, 56, 39, 53, 48]
            },
            {
                "context": "In a poll, {fraction} of the children said they read every night before bed, whereas {percent}% of the adults said they read every night before bed.",
                "question": "Which group had a greater percentage of people who read before bed?",
                "option1": "children",
                "option2": "adults",
                "type": "fraction_percent",
                "fractions": [(2, 3), (3, 4), (5, 6), (7, 8), (4, 5), (5, 7), (8, 9), (3, 5), (7, 10)],
                "percents": [71, 68, 76, 82, 79, 73, 84, 65, 69]
            },
            {
                "context": "Machine A operates at {decimal} efficiency, while Machine B operates at {percent}% efficiency.",
                "question": "Which machine has greater efficiency?",
                "option1": "Machine A",
                "option2": "Machine B",
                "type": "decimal_percent",
                "decimals": [0.72, 0.68, 0.83, 0.77, 0.91, 0.64, 0.86, 0.74, 0.69],
                "percents": [71, 69, 82, 78, 90, 65, 85, 75, 70]
            }
        ]
    
    else:
        # Hard: Complex fractions, very close values, mixed comparisons
        problems = [
            {
                "context": "Last year, Kenny read {fraction1} of the new books in the library. This year, Kenny plans to read {percent}% of the new books in the library.",
                "question": "During which year will Kenny read a greater percentage of the library's new books?",
                "option1": "last year",
                "option2": "this year",
                "type": "fraction_percent",
                "fractions": [(1, 30), (1, 25), (1, 40), (1, 50), (2, 35), (3, 40), (2, 45), (3, 50), (1, 60)],
                "percents": [3.3, 4.1, 2.4, 2.1, 5.8, 7.4, 4.3, 6.1, 1.6]
            },
            {
                "context": "Company X achieved {percent1}% of their sales target, while Company Y achieved {percent2}% of their sales target.",
                "question": "Which company achieved a greater percentage of their sales target?",
                "option1": "Company X",
                "option2": "Company Y",
                "type": "percent_percent",
                "percent_pairs": [(98, 97), (87, 88), (94, 94), (91, 92), (83, 82), (76, 77), (89, 89)]
            },
            {
                "context": "Test A has a success rate of {fraction}, while Test B has a success rate of {decimal}.",
                "question": "Which test has a greater success rate?",
                "option1": "Test A",
                "option2": "Test B",
                "type": "fraction_decimal",
                "fractions": [(11, 12), (13, 15), (17, 20), (19, 25), (21, 25), (23, 30), (27, 35), (31, 40)],
                "decimals": [0.917, 0.866, 0.851, 0.759, 0.841, 0.766, 0.772, 0.774]
            },
            {
                "context": "Sensor reading shows {decimal1} for Location A and {decimal2} for Location B.",
                "question": "Which location has a higher sensor reading?",
                "option1": "Location A",
                "option2": "Location B",
                "type": "decimal_decimal",
                "decimal_pairs": [(0.783, 0.784), (0.921, 0.919), (0.666, 0.667), (0.444, 0.443), (0.875, 0.875)]
            }
        ]
    
    # Select a random problem template
    problem = random.choice(problems)
    
    # Generate specific values based on problem type
    if problem["type"] == "fraction_percent":
        fraction = random.choice(problem["fractions"])
        percent = random.choice(problem["percents"])
        
        # Calculate which is greater
        fraction_as_percent = (fraction[0] / fraction[1]) * 100
        
        if "fraction" in problem["context"] and "percent" in problem["context"]:
            context = problem["context"].format(fraction=f"{fraction[0]}/{fraction[1]}", percent=percent)
            value1 = fraction_as_percent
            value2 = percent
        else:
            context = problem["context"].format(percent1=percent, fraction=f"{fraction[0]}/{fraction[1]}")
            value1 = percent
            value2 = fraction_as_percent
    
    elif problem["type"] == "percent_fraction":
        percent = random.choice(problem["percents"])
        fraction = random.choice(problem["fractions"])
        
        # Calculate which is greater
        fraction_as_percent = (fraction[0] / fraction[1]) * 100
        
        context = problem["context"].format(percent=percent, fraction=f"{fraction[0]}/{fraction[1]}")
        value1 = percent
        value2 = fraction_as_percent
    
    elif problem["type"] == "percent_percent":
        percent1, percent2 = random.choice(problem["percent_pairs"])
        context = problem["context"].format(percent1=percent1, percent2=percent2)
        value1 = percent1
        value2 = percent2
    
    elif problem["type"] == "decimal_percent":
        decimal = random.choice(problem["decimals"])
        percent = random.choice(problem["percents"])
        context = problem["context"].format(decimal=decimal, percent=percent)
        value1 = decimal * 100
        value2 = percent
    
    elif problem["type"] == "fraction_decimal":
        fraction = random.choice(problem["fractions"])
        decimal = random.choice(problem["decimals"])
        context = problem["context"].format(fraction=f"{fraction[0]}/{fraction[1]}", decimal=decimal)
        value1 = (fraction[0] / fraction[1]) * 100
        value2 = decimal * 100
    
    elif problem["type"] == "decimal_decimal":
        decimal1, decimal2 = random.choice(problem["decimal_pairs"])
        context = problem["context"].format(decimal1=decimal1, decimal2=decimal2)
        value1 = decimal1 * 100
        value2 = decimal2 * 100
    
    elif problem["type"] == "fraction_fraction":
        fraction1 = random.choice(problem["fractions"])
        fraction2 = random.choice([f for f in problem["fractions"] if f != fraction1])
        context = problem["context"].format(
            fraction1=f"{fraction1[0]}/{fraction1[1]}", 
            fraction2=f"{fraction2[0]}/{fraction2[1]}"
        )
        value1 = (fraction1[0] / fraction1[1]) * 100
        value2 = (fraction2[0] / fraction2[1]) * 100
    
    # Determine correct answer
    if abs(value1 - value2) < 0.0001:  # Equal
        correct_answer = "equal"
    elif value1 > value2:
        correct_answer = problem["option1"]
    else:
        correct_answer = problem["option2"]
    
    # Store question data
    st.session_state.question_data = {
        "context": context,
        "question": problem["question"],
        "option1": problem["option1"],
        "option2": problem["option2"],
        "value1": value1,
        "value2": value2,
        "type": problem["type"],
        "raw_values": {
            "fraction": fraction if "fraction" in locals() else None,
            "percent": percent if "percent" in locals() else None,
            "decimal": decimal if "decimal" in locals() else None,
            "percent1": percent1 if "percent1" in locals() else None,
            "percent2": percent2 if "percent2" in locals() else None,
            "decimal1": decimal1 if "decimal1" in locals() else None,
            "decimal2": decimal2 if "decimal2" in locals() else None,
            "fraction1": fraction1 if "fraction1" in locals() else None,
            "fraction2": fraction2 if "fraction2" in locals() else None
        }
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "word_comparison"

def display_word_problem():
    """Display the current word problem interface"""
    data = st.session_state.question_data
    
    # Display the problem
    st.markdown(f"{data['context']} **{data['question']}**")
    
    # Create clickable option buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            data['option1'], 
            key="option1_btn",
            use_container_width=True,
            type="primary" if st.session_state.selected_option == data['option1'] else "secondary"
        ):
            st.session_state.selected_option = data['option1']
    
    with col2:
        if st.button(
            data['option2'], 
            key="option2_btn",
            use_container_width=True,
            type="primary" if st.session_state.selected_option == data['option2'] else "secondary"
        ):
            st.session_state.selected_option = data['option2']
    
    # Submit button
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, 
                    disabled=st.session_state.selected_option is None):
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
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.selected_option
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    # Check if values are equal
    is_equal = abs(data['value1'] - data['value2']) < 0.0001
    
    if is_equal and user_answer in [data['option1'], data['option2']]:
        # Special case: values are equal, any answer is acceptable
        st.info("✓ **The values are equal!** Both options have the same percentage.")
        is_correct = True
    elif user_answer == correct_answer:
        st.success("🎉 **Correct! Well done!**")
        is_correct = True
    else:
        st.error(f"❌ **Not quite.** The correct answer is **{correct_answer}**.")
        is_correct = False
    
    if is_correct:
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_incorrect = 0
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.word_comparison_difficulty
            st.session_state.word_comparison_difficulty = min(
                st.session_state.word_comparison_difficulty + 1, 3
            )
            
            if st.session_state.word_comparison_difficulty > old_difficulty:
                st.info(f"⬆️ **Level up! Moving to more challenging problems.**")
                st.session_state.consecutive_correct = 0
            elif st.session_state.word_comparison_difficulty == 3:
                st.balloons()
                st.info("🏆 **Excellent! You've mastered all difficulty levels!**")
    else:
        st.session_state.consecutive_incorrect += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive incorrect
        if st.session_state.consecutive_incorrect >= 3:
            old_difficulty = st.session_state.word_comparison_difficulty
            st.session_state.word_comparison_difficulty = max(
                st.session_state.word_comparison_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.word_comparison_difficulty:
                st.warning(f"⬇️ **Let's practice with easier problems.**")
                st.session_state.consecutive_incorrect = 0
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the comparison"""
    data = st.session_state.question_data
    raw = data['raw_values']
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Step-by-step solution:")
        
        if data['type'] == "fraction_percent":
            fraction = raw['fraction']
            percent = raw['percent']
            fraction_as_percent = (fraction[0] / fraction[1]) * 100
            
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {fraction[0]}/{fraction[1]}
            - {data['option2']}: {percent}%
            
            **Convert fraction to percent:**
            - {fraction[0]}/{fraction[1]} = {fraction[0]} ÷ {fraction[1]} = {fraction[0]/fraction[1]:.4f}
            - {fraction[0]/fraction[1]:.4f} × 100 = **{fraction_as_percent:.1f}%**
            
            **Compare:**
            - {data['option1']}: {fraction_as_percent:.1f}%
            - {data['option2']}: {percent}%
            """)
            
            if abs(fraction_as_percent - percent) < 0.0001:
                st.markdown("**Result: Both are equal!**")
            elif fraction_as_percent > percent:
                st.markdown(f"**Result: {data['option1']} has the greater percentage**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater percentage**")
        
        elif data['type'] == "percent_fraction":
            percent = raw['percent']
            fraction = raw['fraction']
            fraction_as_percent = (fraction[0] / fraction[1]) * 100
            
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {percent}%
            - {data['option2']}: {fraction[0]}/{fraction[1]}
            
            **Convert fraction to percent:**
            - {fraction[0]}/{fraction[1]} = {fraction[0]} ÷ {fraction[1]} = {fraction[0]/fraction[1]:.4f}
            - {fraction[0]/fraction[1]:.4f} × 100 = **{fraction_as_percent:.1f}%**
            
            **Compare:**
            - {data['option1']}: {percent}%
            - {data['option2']}: {fraction_as_percent:.1f}%
            """)
            
            if abs(percent - fraction_as_percent) < 0.0001:
                st.markdown("**Result: Both are equal!**")
            elif percent > fraction_as_percent:
                st.markdown(f"**Result: {data['option1']} has the greater percentage**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater percentage**")
        
        elif data['type'] == "percent_percent":
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {raw['percent1']}%
            - {data['option2']}: {raw['percent2']}%
            
            **Direct comparison:**
            - {raw['percent1']}% {'=' if raw['percent1'] == raw['percent2'] else '>' if raw['percent1'] > raw['percent2'] else '<'} {raw['percent2']}%
            """)
            
            if raw['percent1'] == raw['percent2']:
                st.markdown("**Result: Both are equal!**")
            elif raw['percent1'] > raw['percent2']:
                st.markdown(f"**Result: {data['option1']} has the greater percentage**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater percentage**")
        
        elif data['type'] == "decimal_percent":
            decimal = raw['decimal']
            percent = raw['percent']
            decimal_as_percent = decimal * 100
            
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {decimal}
            - {data['option2']}: {percent}%
            
            **Convert decimal to percent:**
            - {decimal} × 100 = **{decimal_as_percent:.1f}%**
            
            **Compare:**
            - {data['option1']}: {decimal_as_percent:.1f}%
            - {data['option2']}: {percent}%
            """)
            
            if abs(decimal_as_percent - percent) < 0.0001:
                st.markdown("**Result: Both are equal!**")
            elif decimal_as_percent > percent:
                st.markdown(f"**Result: {data['option1']} has the greater value**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater value**")
        
        elif data['type'] == "fraction_decimal":
            fraction = raw['fraction']
            decimal = raw['decimal']
            fraction_value = fraction[0] / fraction[1]
            
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {fraction[0]}/{fraction[1]}
            - {data['option2']}: {decimal}
            
            **Convert to decimals:**
            - {fraction[0]}/{fraction[1]} = {fraction[0]} ÷ {fraction[1]} = **{fraction_value:.4f}**
            
            **Compare:**
            - {data['option1']}: {fraction_value:.4f}
            - {data['option2']}: {decimal:.4f}
            """)
            
            if abs(fraction_value - decimal) < 0.0001:
                st.markdown("**Result: Both are equal!**")
            elif fraction_value > decimal:
                st.markdown(f"**Result: {data['option1']} has the greater value**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater value**")
        
        elif data['type'] == "decimal_decimal":
            st.markdown(f"""
            **Given:**
            - {data['option1']}: {raw['decimal1']}
            - {data['option2']}: {raw['decimal2']}
            
            **Direct comparison:**
            - {raw['decimal1']} {'=' if abs(raw['decimal1'] - raw['decimal2']) < 0.0001 else '>' if raw['decimal1'] > raw['decimal2'] else '<'} {raw['decimal2']}
            """)
            
            if abs(raw['decimal1'] - raw['decimal2']) < 0.0001:
                st.markdown("**Result: Both are equal!**")
            elif raw['decimal1'] > raw['decimal2']:
                st.markdown(f"**Result: {data['option1']} has the greater value**")
            else:
                st.markdown(f"**Result: {data['option2']} has the greater value**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_option = None