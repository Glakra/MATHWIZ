import streamlit as st
import random
from itertools import combinations_with_replacement

def run():
    """
    Main function to run the Decompose Fractions Multiple Ways practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/decompose_fractions_multiple_ways.py
    """
    # Initialize session state for difficulty and game state
    if "decompose_multi_difficulty" not in st.session_state:
        st.session_state.decompose_multi_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_values_row1 = []
        st.session_state.selected_values_row2 = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🔀 Decompose Fractions Multiple Ways")
    st.markdown("*Find two different ways to write fractions as sums*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decompose_multi_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "2 terms, small fractions (3-5)",
            2: "2-3 terms, medium fractions (6-8)",
            3: "2-4 terms, larger fractions (9-12)",
            4: "3-5 terms, complex fractions (10-16)",
            5: "2-6 terms, challenge mode (all)"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
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
        ### How to Play:
        1. Look at the target fraction
        2. Find TWO DIFFERENT ways to write it as a sum of fractions
        3. Click buttons to fill in the blanks
        4. Each way must use different combinations (not just different order)
        
        ### Important Notes:
        - **The number of blanks varies by difficulty level**
        - **Same fractions in different order are NOT different answers**
        - **You can use the same fraction multiple times (e.g., 1/8 + 1/8 + 5/8)**
        
        ### Examples:
        **6/8 with 2 terms:**
        - Way 1: 2/8 + 4/8
        - Way 2: 1/8 + 5/8
        
        **7/8 with 3 terms:**
        - Way 1: 1/8 + 2/8 + 4/8
        - Way 2: 1/8 + 1/8 + 5/8
        
        **8/10 with 4 terms:**
        - Way 1: 2/10 + 2/10 + 2/10 + 2/10
        - Way 2: 1/10 + 1/10 + 3/10 + 3/10
        
        ### Strategy:
        1. Start with unit fractions (1/denominator)
        2. Build up to the target numerator
        3. Try different combinations
        4. Remember: order doesn't matter!
        """)

def generate_all_partitions(n, max_parts, min_val=1):
    """Generate all ways to partition n into at most max_parts positive integers >= min_val"""
    if n < min_val * max_parts:
        return []
    
    partitions = []
    
    def partition_helper(target, num_parts, current, min_value):
        if num_parts == 1:
            if target >= min_value:
                partitions.append(current + [target])
            return
        
        for i in range(min_value, target - num_parts + 2):
            partition_helper(target - i, num_parts - 1, current + [i], i)
    
    for num_parts in range(1, min(max_parts + 1, n + 1)):
        partition_helper(n, num_parts, [], min_val)
    
    return partitions

def generate_new_question():
    """Generate a new decompose fractions multiple ways question"""
    difficulty = st.session_state.decompose_multi_difficulty
    
    # Set parameters based on difficulty
    if difficulty == 1:
        denominator = random.randint(4, 6)
        num_terms_way1 = 2
        num_terms_way2 = 2
    elif difficulty == 2:
        denominator = random.randint(6, 8)
        num_terms_way1 = random.choice([2, 3])
        num_terms_way2 = random.choice([2, 3])
    elif difficulty == 3:
        denominator = random.randint(8, 12)
        num_terms_way1 = random.choice([2, 3, 4])
        num_terms_way2 = random.choice([2, 3, 4])
    elif difficulty == 4:
        denominator = random.randint(10, 16)
        num_terms_way1 = random.choice([3, 4, 5])
        num_terms_way2 = random.choice([3, 4, 5])
    else:  # difficulty == 5
        denominator = random.randint(8, 20)
        num_terms_way1 = random.choice([2, 3, 4, 5, 6])
        num_terms_way2 = random.choice([2, 3, 4, 5, 6])
    
    # Generate numerator that can be decomposed in multiple ways
    # Need enough to decompose into the required number of terms
    min_numerator = max(num_terms_way1, num_terms_way2, 3)
    max_numerator = min(denominator - 1, 15)  # Cap for usability
    
    # Ensure valid range
    if max_numerator < min_numerator:
        denominator = max(8, min_numerator + 2)
        max_numerator = min(denominator - 1, 15)
    
    numerator = random.randint(min_numerator, max_numerator)
    
    # Generate all valid partitions for both ways
    partitions_way1 = generate_all_partitions(numerator, num_terms_way1)
    partitions_way2 = generate_all_partitions(numerator, num_terms_way2)
    
    # If we don't have enough different partitions, adjust
    if len(partitions_way1) < 1 or len(partitions_way2) < 1:
        # Fallback to a known good configuration
        numerator = 8
        denominator = 10
        num_terms_way1 = 3
        num_terms_way2 = 2
        partitions_way1 = generate_all_partitions(numerator, num_terms_way1)
        partitions_way2 = generate_all_partitions(numerator, num_terms_way2)
    
    # Create button options - all fractions from 1/d to (numerator)/d
    options = []
    for i in range(1, min(numerator + 1, denominator)):
        fraction_str = f"{i}/{denominator}"
        options.append(fraction_str)
    
    # Limit to 10 options for cleaner interface
    if len(options) > 10:
        # Keep the most useful fractions
        useful_values = set()
        # Add unit fraction
        useful_values.add(1)
        # Add half if even
        if denominator % 2 == 0:
            useful_values.add(denominator // 2)
        # Add some common values
        useful_values.update([2, 3, 4, 5])
        # Add values from some partitions
        for p in partitions_way1[:3] + partitions_way2[:3]:
            useful_values.update(p)
        
        # Convert to list and sort
        useful_values = sorted(list(useful_values))[:10]
        options = []
        for i in useful_values:
            if i < denominator:
                fraction_str = f"{i}/{denominator}"
                options.append(fraction_str)
    
    # Initialize selected values with the correct number of blanks
    st.session_state.selected_values_row1 = [""] * num_terms_way1
    st.session_state.selected_values_row2 = [""] * num_terms_way2
    
    fraction_str = f"{numerator}/{denominator}"
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "fraction": fraction_str,
        "options": options,
        "num_terms_way1": num_terms_way1,
        "num_terms_way2": num_terms_way2,
        "partitions_way1": partitions_way1,
        "partitions_way2": partitions_way2
    }
    
    st.session_state.current_question = f"Decompose {fraction_str} into a sum of fractions two different ways."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("*Note: Answers using the same fractions in a different order are not different answers.*")
    
    # Display the equations with blanks
    st.markdown("")  # Add space
    
    # First decomposition
    st.markdown(f"#### First way ({data['num_terms_way1']} terms):")
    display_equation_row(data, 1)
    
    # Second decomposition
    st.markdown(f"#### Second way ({data['num_terms_way2']} terms):")
    display_equation_row(data, 2)
    
    # Number buttons
    st.markdown("")  # Add space
    st.markdown("### Click to select:")
    
    # Create button grid
    num_options = len(data["options"])
    cols_per_row = min(5, num_options)
    num_rows = (num_options + cols_per_row - 1) // cols_per_row
    
    button_index = 0
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            if button_index < num_options:
                with cols[col]:
                    option = data["options"][button_index]
                    if st.button(
                        option,
                        key=f"option_{button_index}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        # Find which row and position to fill
                        if "" in st.session_state.selected_values_row1:
                            # Fill in row 1
                            for i in range(len(st.session_state.selected_values_row1)):
                                if st.session_state.selected_values_row1[i] == "":
                                    st.session_state.selected_values_row1[i] = option
                                    st.rerun()
                                    break
                        elif "" in st.session_state.selected_values_row2:
                            # Fill in row 2
                            for i in range(len(st.session_state.selected_values_row2)):
                                if st.session_state.selected_values_row2[i] == "":
                                    st.session_state.selected_values_row2[i] = option
                                    st.rerun()
                                    break
                button_index += 1
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear All", type="secondary", use_container_width=True):
            st.session_state.selected_values_row1 = [""] * data['num_terms_way1']
            st.session_state.selected_values_row2 = [""] * data['num_terms_way2']
            st.rerun()
    
    with col2:
        if st.button("⬅️ Remove Last", type="secondary", use_container_width=True):
            # Find the last filled slot and clear it
            for i in range(len(st.session_state.selected_values_row2) - 1, -1, -1):
                if st.session_state.selected_values_row2[i] != "":
                    st.session_state.selected_values_row2[i] = ""
                    st.rerun()
                    break
            else:
                for i in range(len(st.session_state.selected_values_row1) - 1, -1, -1):
                    if st.session_state.selected_values_row1[i] != "":
                        st.session_state.selected_values_row1[i] = ""
                        st.rerun()
                        break
    
    with col3:
        # Check if all blanks are filled
        all_filled = (all(val != "" for val in st.session_state.selected_values_row1) and 
                     all(val != "" for val in st.session_state.selected_values_row2))
        
        if all_filled:
            submit_button = st.button(
                "✅ Submit",
                type="primary",
                use_container_width=True
            )
            
            if submit_button:
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
        else:
            st.button(
                "✅ Submit",
                type="secondary",
                use_container_width=True,
                disabled=True
            )
    
    # Show feedback
    handle_feedback_and_next()

def display_equation_row(data, row_num):
    """Display one equation row with variable number of blanks"""
    if row_num == 1:
        selected_values = st.session_state.selected_values_row1
        num_terms = data['num_terms_way1']
    else:
        selected_values = st.session_state.selected_values_row2
        num_terms = data['num_terms_way2']
    
    # Create columns: fraction = blank + blank + ... + blank
    # Need: 1 for fraction, 1 for =, and (2*num_terms - 1) for blanks and plus signs
    total_cols = 2 + (2 * num_terms - 1)
    cols = st.columns(total_cols)
    
    # Original fraction
    with cols[0]:
        st.markdown(f"""
        <div style="
            background-color: #f5f5f5;
            border: 3px solid #333;
            padding: 15px 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            border-radius: 6px;
            color: #333;
        ">{data['fraction']}</div>
        """, unsafe_allow_html=True)
    
    # Equal sign
    with cols[1]:
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            padding: 15px;
            color: #333;
        ">=</div>
        """, unsafe_allow_html=True)
    
    # Blanks and plus signs
    for i in range(num_terms):
        # Blank
        col_idx = 2 + (i * 2)
        with cols[col_idx]:
            value = selected_values[i]
            if value:
                st.markdown(f"""
                <div style="
                    background-color: #2196F3;
                    border: 3px solid #1976D2;
                    padding: 12px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 6px;
                    min-height: 45px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                ">{value}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background-color: #e6f3ff;
                    border: 3px solid #2196F3;
                    padding: 12px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 6px;
                    min-height: 45px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">&nbsp;</div>
                """, unsafe_allow_html=True)
        
        # Plus sign (if not last term)
        if i < num_terms - 1:
            with cols[col_idx + 1]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 12px;
                    color: #333;
                ">+</div>
                """, unsafe_allow_html=True)

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.question_data
    row1 = st.session_state.selected_values_row1
    row2 = st.session_state.selected_values_row2
    
    # Check if each row sums correctly
    row1_sum = sum(int(frac.split('/')[0]) for frac in row1 if frac)
    row2_sum = sum(int(frac.split('/')[0]) for frac in row2 if frac)
    
    row1_correct = (row1_sum == data["numerator"])
    row2_correct = (row2_sum == data["numerator"])
    
    # Check if the two ways are different (not just reordered)
    # Sort the numerators to compare
    row1_nums = sorted([int(frac.split('/')[0]) for frac in row1 if frac])
    row2_nums = sorted([int(frac.split('/')[0]) for frac in row2 if frac])
    
    different_ways = (row1_nums != row2_nums)
    
    # Overall correct if both rows sum correctly AND are different
    is_correct = row1_correct and row2_correct and different_ways
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show both decompositions
        eq1 = f"{data['fraction']} = " + " + ".join(row1)
        eq2 = f"{data['fraction']} = " + " + ".join(row2)
        st.success(f"✓ First way ({data['num_terms_way1']} terms): {eq1}")
        st.success(f"✓ Second way ({data['num_terms_way2']} terms): {eq2}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.decompose_multi_difficulty
        st.session_state.decompose_multi_difficulty = min(
            st.session_state.decompose_multi_difficulty + 1, 5
        )
        
        if st.session_state.decompose_multi_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decomposing fractions multiple ways with multiple terms!**")
        elif old_difficulty < st.session_state.decompose_multi_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decompose_multi_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show specific errors
        if not row1_correct:
            denom = data['denominator']
            frac_sum = f"{row1_sum}/{denom}"
            st.error(f"First way: {' + '.join(row1)} = {frac_sum} (should equal {data['fraction']})")
        else:
            st.success(f"✓ First way is correct: {' + '.join(row1)} = {data['fraction']}")
            
        if not row2_correct:
            denom = data['denominator']
            frac_sum = f"{row2_sum}/{denom}"
            st.error(f"Second way: {' + '.join(row2)} = {frac_sum} (should equal {data['fraction']})")
        else:
            st.success(f"✓ Second way is correct: {' + '.join(row2)} = {data['fraction']}")
            
        if row1_correct and row2_correct and not different_ways:
            st.error("❌ Both ways use the same combination of fractions! Remember: changing the order doesn't make it different.")
            # Create fraction strings for display
            denom = data["denominator"]
            fraction_list = []
            for n in sorted(row1_nums):
                frac_str = f"{n}/{denom}"
                fraction_list.append(frac_str)
            st.error(f"Both ways use: {', '.join(fraction_list)}")
        
        # Show some valid examples
        show_valid_examples(data)
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.decompose_multi_difficulty
        st.session_state.decompose_multi_difficulty = max(
            st.session_state.decompose_multi_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decompose_multi_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.decompose_multi_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_valid_examples(data):
    """Show examples of valid decompositions"""
    st.success("**Examples of different decompositions:**")
    
    # Show examples for way 1
    count = 0
    for partition in data["partitions_way1"][:2]:
        terms = []
        denom = data['denominator']
        for n in partition:
            frac_str = f"{n}/{denom}"
            terms.append(frac_str)
        example_str = ' + '.join(terms)
        st.success(f"• {data['num_terms_way1']} terms: {data['fraction']} = {example_str}")
        count += 1
    
    # Show examples for way 2
    for partition in data["partitions_way2"][:2]:
        terms = []
        denom = data['denominator']
        for n in partition:
            frac_str = f"{n}/{denom}"
            terms.append(frac_str)
        example_str = ' + '.join(terms)
        st.success(f"• {data['num_terms_way2']} terms: {data['fraction']} = {example_str}")
        count += 1

def show_explanation():
    """Show explanation for decomposing multiple ways"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Multiple Decompositions with Different Numbers of Terms**", expanded=True):
        st.markdown(f"""
        ### Decomposing {data['fraction']} in Two Different Ways
        
        **What makes decompositions different?**
        - They must use different combinations of numbers
        - Order doesn't matter: 2/8 + 1/8 + 5/8 is the same as 5/8 + 1/8 + 2/8
        - You can use the same fraction multiple times: 1/8 + 1/8 + 1/8 + 5/8
        - Both must add up to the original fraction
        
        **Example decompositions for {data['fraction']}:**
        
        **With {data['num_terms_way1']} terms:**
        """)
        
        # Show some partitions for way 1
        denom = data['denominator']
        for i, partition in enumerate(data["partitions_way1"][:3], 1):
            terms = []
            for n in partition:
                frac_str = f"{n}/{denom}"
                terms.append(frac_str)
            example_str = ' + '.join(terms)
            st.markdown(f"{i}. {example_str} = {data['fraction']}")
        
        st.markdown(f"""
        **With {data['num_terms_way2']} terms:**
        """)
        
        # Show some partitions for way 2
        for i, partition in enumerate(data["partitions_way2"][:3], 1):
            terms = []
            for n in partition:
                frac_str = f"{n}/{denom}"
                terms.append(frac_str)
            example_str = ' + '.join(terms)
            st.markdown(f"{i}. {example_str} = {data['fraction']}")
        
        # Fixed the problematic f-string here
        denominator = data['denominator']
        numerator = data['numerator']
        unit_fraction = f"1/{denominator}"  # Create the fraction string separately
        st.markdown(f"""
        **Remember:**
        - The denominator ({denominator}) stays the same
        - The numerators must add up to {numerator}
        - You can repeat fractions (like {unit_fraction} multiple times)
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_values_row1 = []
    st.session_state.selected_values_row2 = []
    if "user_answer" in st.session_state:
        del st.session_state.user_answer