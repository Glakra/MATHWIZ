import streamlit as st
import random

def run():
    """
    Main function to run the geometric number sequences activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/geometric_number_sequences.py
    """
    # Initialize session state
    if "geometric_seq_difficulty" not in st.session_state:
        st.session_state.geometric_seq_difficulty = 1
    
    if "current_geometric_problem" not in st.session_state:
        st.session_state.current_geometric_problem = None
        st.session_state.geometric_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Geometric Number Sequences")
    st.markdown("*Find the pattern where numbers multiply*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.geometric_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (×2, ×3, 1 blank)",
            2: "Common ratios (×4, ×5, 1 blank)",
            3: "Mixed positions (1-2 blanks)",
            4: "Larger numbers (2 blanks)",
            5: "Challenge mode (fractions & multiple blanks)"
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
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_geometric_problem is None:
        generate_new_geometric_problem()
    
    # Display current problem
    display_geometric_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What are Geometric Sequences?
        In a geometric sequence, each number is found by **multiplying** the previous number by the same value (called the common ratio).
        
        ### Common Patterns:
        
        **Multiply by 2 (doubling):**
        - 1, 2, 4, 8, 16, 32...
        - Each number is 2 × the previous
        
        **Multiply by 3:**
        - 1, 3, 9, 27, 81...
        - Each number is 3 × the previous
        
        **Multiply by 4:**
        - 1, 4, 16, 64, 256...
        - Each number is 4 × the previous
        
        **Powers pattern:**
        - 2¹, 2², 2³, 2⁴... = 2, 4, 8, 16...
        - 3¹, 3², 3³, 3⁴... = 3, 9, 27, 81...
        
        ### How to Find the Pattern:
        1. **Divide** any number by the previous number
        2. **Check** if you get the same result each time
        3. **Apply** this ratio to find missing numbers
        
        ### Strategy:
        - **Going forward:** Multiply by the ratio
        - **Going backward:** Divide by the ratio
        - **Skip terms:** Multiply by ratio multiple times
        
        ### Examples:
        - If ratio is 2: 3 → 6 → 12 → 24
        - If ratio is 5: 2 → 10 → 50 → 250
        - Missing middle: 4, ?, 64 → ? = 4 × 4 = 16
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Simple ratios (2, 3, 4, 5)
        - **🟡 Level 3:** Blanks anywhere
        - **🔴 Level 4-5:** Large numbers, fractions, multiple blanks
        """)

def generate_new_geometric_problem():
    """Generate a new geometric sequence problem"""
    difficulty = st.session_state.geometric_seq_difficulty
    
    if difficulty == 1:
        # Basic patterns (×2, ×3), 1 blank
        ratio = random.choice([2, 3])
        start = random.choice([1, 2, 3, 4, 5])
        length = random.randint(5, 6)
        
        # Mostly blanks at end, sometimes in middle
        if random.random() < 0.7:
            missing_positions = [length - 1]  # Last position
        else:
            missing_positions = [random.randint(1, length - 2)]  # Middle position
        
    elif difficulty == 2:
        # Common ratios (×4, ×5), 1 blank
        ratio = random.choice([3, 4, 5])
        start = random.choice([1, 2, 3, 4])
        length = random.randint(5, 6)
        
        # Mix of positions
        missing_positions = [random.randint(0, length - 1)]
        
    elif difficulty == 3:
        # Mixed positions, 1-2 blanks
        ratio = random.choice([2, 3, 4, 5, 10])
        start = random.choice([1, 2, 3, 4, 5, 10])
        length = random.randint(5, 7)
        
        # 1 or 2 blanks
        num_blanks = random.choice([1, 2])
        positions = list(range(length))
        missing_positions = random.sample(positions, num_blanks)
        missing_positions.sort()
        
    elif difficulty == 4:
        # Larger numbers, 2 blanks
        ratio = random.choice([2, 3, 4, 5, 6, 10])
        start = random.choice([1, 2, 3, 4, 5, 6, 8, 10])
        length = random.randint(6, 8)
        
        # Always 2 blanks
        positions = list(range(length))
        missing_positions = random.sample(positions, 2)
        missing_positions.sort()
        
    else:  # difficulty == 5
        # Challenge mode - various patterns
        pattern_type = random.choice(['large_ratio', 'fractional', 'mixed', 'powers'])
        
        if pattern_type == 'large_ratio':
            ratio = random.choice([6, 7, 8, 9, 10, 12])
            start = random.choice([1, 2, 3])
            length = random.randint(5, 6)
        elif pattern_type == 'fractional':
            # Dividing sequences (ratio < 1)
            ratio = random.choice([0.5, 0.25, 1/3])
            start = random.choice([256, 512, 1024, 2048, 3125])
            length = random.randint(5, 7)
        elif pattern_type == 'powers':
            # Powers of small numbers
            base = random.choice([2, 3, 4, 5])
            ratio = base
            start = base
            length = random.randint(5, 7)
        else:  # mixed
            ratio = random.choice([2, 3, 4, 5, 10])
            start = random.choice([1, 2, 3, 5, 7, 11])
            length = random.randint(6, 8)
        
        # 2-3 blanks
        num_blanks = random.choice([2, 3])
        positions = list(range(length))
        missing_positions = random.sample(positions, num_blanks)
        missing_positions.sort()
    
    # Generate the sequence
    sequence = []
    current = start
    
    for i in range(length):
        if ratio < 1:
            # For fractional ratios, ensure we get integers
            sequence.append(int(current))
        else:
            sequence.append(current)
        current = current * ratio
    
    # Store problem data
    st.session_state.geometric_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'ratio': ratio,
        'start': start,
        'difficulty': difficulty
    }
    st.session_state.current_geometric_problem = True

def display_geometric_problem():
    """Display the geometric sequence problem"""
    data = st.session_state.geometric_problem_data
    
    # Display instruction
    num_blanks = len(data['missing_positions'])
    if num_blanks == 1:
        st.markdown("### Type the missing number in this sequence:")
    else:
        st.markdown(f"### Type the {num_blanks} missing numbers in this sequence:")
    
    # Create columns for the sequence
    cols = st.columns(len(data['sequence']) * 2 - 1)
    
    # Track input fields
    input_fields = {}
    
    for i, num in enumerate(data['sequence']):
        col_idx = i * 2
        
        with cols[col_idx]:
            if i in data['missing_positions']:
                # Input field for missing number
                user_input = st.text_input(
                    "",
                    key=f"geometric_input_{i}",
                    placeholder="",
                    label_visibility="collapsed"
                )
                input_fields[i] = user_input
            else:
                # Display the number
                # Format large numbers with commas
                if num >= 1000:
                    display_num = f"{num:,}"
                else:
                    display_num = str(num)
                st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold; padding-top:8px;'>{display_num}</div>", 
                          unsafe_allow_html=True)
        
        # Add comma between numbers (except last)
        if i < len(data['sequence']) - 1 and col_idx + 1 < len(cols):
            with cols[col_idx + 1]:
                st.markdown("<div style='text-align:center; font-size:20px; padding-top:8px;'>,</div>", 
                          unsafe_allow_html=True)
    
    # Style the input boxes
    st.markdown("""
    <style>
    input[type="text"] {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        height: 40px;
        width: 100px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        background-color: #e8f4fd;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Store input references
    st.session_state.input_fields = input_fields
    
    # Submit button
    st.markdown("")  # Add space
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            # Validate all inputs are filled
            all_filled = True
            for pos in data['missing_positions']:
                if pos not in input_fields or not input_fields[pos].strip():
                    all_filled = False
                    break
            
            if all_filled:
                # Store answers and validate
                for pos in data['missing_positions']:
                    st.session_state.user_answers[pos] = input_fields[pos]
                validate_geometric_answers()
            else:
                st.warning("Please fill in all missing numbers!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_geometric_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_geometric_problem_state()
                st.rerun()

def validate_geometric_answers():
    """Validate the user's answers"""
    data = st.session_state.geometric_problem_data
    all_correct = True
    
    st.session_state.total_attempted += 1
    
    # Check each answer
    for pos in data['missing_positions']:
        try:
            # Remove commas if user added them
            user_value = int(st.session_state.user_answers[pos].replace(',', ''))
            correct_value = data['sequence'][pos]
            
            if user_value != correct_value:
                all_correct = False
        except:
            all_correct = False
    
    if all_correct:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        st.session_state.user_correct = True
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            if st.session_state.geometric_seq_difficulty < 5:
                st.session_state.geometric_seq_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        st.session_state.user_correct = False
        
        # Decrease difficulty after poor performance
        if st.session_state.total_attempted % 3 == 0:
            accuracy = st.session_state.total_correct / st.session_state.total_attempted
            if accuracy < 0.5 and st.session_state.geometric_seq_difficulty > 1:
                st.session_state.geometric_seq_difficulty -= 1
    
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_geometric_feedback():
    """Display feedback for geometric sequence problems"""
    data = st.session_state.geometric_problem_data
    
    if st.session_state.user_correct:
        if len(data['missing_positions']) == 1:
            st.success("✅ **Correct! Well done!**")
        else:
            st.success("✅ **Excellent! All answers are correct!**")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.geometric_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.geometric_seq_difficulty), unsafe_allow_html=True)
    else:
        st.error("❌ **Not quite right. Check your answers.**")
        
        # Show correct answers
        st.markdown("**Correct answers:**")
        for pos in sorted(data['missing_positions']):
            correct_value = data['sequence'][pos]
            user_value = st.session_state.user_answers.get(pos, "")
            
            # Format large numbers with commas
            if correct_value >= 1000:
                correct_display = f"{correct_value:,}"
            else:
                correct_display = str(correct_value)
            
            if user_value:
                try:
                    user_int = int(user_value.replace(',', ''))
                    if user_int != correct_value:
                        st.markdown(f"Position {pos + 1}: **{correct_display}** (You entered: {user_value})")
                except:
                    st.markdown(f"Position {pos + 1}: **{correct_display}** (Invalid input)")
            else:
                st.markdown(f"Position {pos + 1}: **{correct_display}**")
        
        # Show explanation
        show_geometric_explanation()

def show_geometric_explanation():
    """Show step-by-step solution for geometric sequences"""
    data = st.session_state.geometric_problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the complete sequence with missing positions marked
        sequence_display = []
        for i, num in enumerate(data['sequence']):
            if i in data['missing_positions']:
                sequence_display.append("**?**")
            else:
                if num >= 1000:
                    sequence_display.append(f"{num:,}")
                else:
                    sequence_display.append(str(num))
        
        st.markdown(f"**Sequence:** {', '.join(sequence_display)}")
        
        # Find and show the ratio
        st.markdown("**Step 1: Find the common ratio (what we multiply by)**")
        
        # Find consecutive known numbers to calculate ratio
        ratios_found = []
        for i in range(1, len(data['sequence'])):
            if i - 1 not in data['missing_positions'] and i not in data['missing_positions']:
                ratio_calc = data['sequence'][i] / data['sequence'][i-1]
                ratios_found.append((i, ratio_calc))
                
                # Show calculation
                if data['sequence'][i] >= 1000:
                    num_display = f"{data['sequence'][i]:,}"
                else:
                    num_display = str(data['sequence'][i])
                    
                if data['sequence'][i-1] >= 1000:
                    prev_display = f"{data['sequence'][i-1]:,}"
                else:
                    prev_display = str(data['sequence'][i-1])
                
                st.code(f"{num_display} ÷ {prev_display} = {ratio_calc:.0f}")
        
        # Display the ratio
        if data['ratio'] < 1:
            st.markdown(f"**Common ratio = {data['ratio']}** (dividing by {int(1/data['ratio'])})")
        else:
            st.markdown(f"**Common ratio = {int(data['ratio'])}** (multiply by {int(data['ratio'])})")
        
        # Show pattern recognition
        st.markdown("**Step 2: Understand the pattern**")
        
        if data['ratio'] == 2:
            st.markdown("This is a **doubling sequence** - each number is 2 × the previous")
        elif data['ratio'] == 3:
            st.markdown("This is a **tripling sequence** - each number is 3 × the previous")
        elif data['ratio'] == 10:
            st.markdown("Each number is **10 times** the previous")
        elif data['ratio'] < 1:
            st.markdown(f"This is a **dividing sequence** - each number is divided by {int(1/data['ratio'])}")
        
        # Show as powers if appropriate
        if data['start'] == data['ratio'] and data['ratio'] in [2, 3, 4, 5]:
            st.markdown(f"**Powers pattern:** {int(data['ratio'])}¹, {int(data['ratio'])}², {int(data['ratio'])}³...")
            powers_display = []
            for i in range(len(data['sequence'])):
                if i not in data['missing_positions']:
                    powers_display.append(f"{int(data['ratio'])}^{i+1} = {data['sequence'][i]}")
            for p in powers_display[:3]:
                st.code(p)
        
        # Calculate missing numbers
        st.markdown("**Step 3: Calculate the missing numbers**")
        
        for pos in sorted(data['missing_positions']):
            st.markdown(f"**Finding position {pos + 1}:**")
            
            # Find the best way to calculate
            if pos > 0 and pos - 1 not in data['missing_positions']:
                # Use previous number
                prev_num = data['sequence'][pos-1]
                if prev_num >= 1000:
                    prev_display = f"{prev_num:,}"
                else:
                    prev_display = str(prev_num)
                
                result = data['sequence'][pos]
                if result >= 1000:
                    result_display = f"{result:,}"
                else:
                    result_display = str(result)
                
                if data['ratio'] < 1:
                    st.code(f"{prev_display} ÷ {int(1/data['ratio'])} = {result_display}")
                else:
                    st.code(f"{prev_display} × {int(data['ratio'])} = {result_display}")
                    
            elif pos < len(data['sequence']) - 1 and pos + 1 not in data['missing_positions']:
                # Use next number
                next_num = data['sequence'][pos+1]
                if next_num >= 1000:
                    next_display = f"{next_num:,}"
                else:
                    next_display = str(next_num)
                
                result = data['sequence'][pos]
                if result >= 1000:
                    result_display = f"{result:,}"
                else:
                    result_display = str(result)
                
                if data['ratio'] < 1:
                    st.code(f"{next_display} × {int(1/data['ratio'])} = {result_display}")
                else:
                    st.code(f"{next_display} ÷ {int(data['ratio'])} = {result_display}")
            else:
                # Calculate from start
                steps = pos
                result = data['sequence'][pos]
                if result >= 1000:
                    result_display = f"{result:,}"
                else:
                    result_display = str(result)
                
                if data['ratio'] < 1:
                    st.markdown(f"Start with {data['start']} and divide by {int(1/data['ratio'])} a total of {steps} times")
                else:
                    st.markdown(f"Start with {data['start']} and multiply by {int(data['ratio'])} a total of {steps} times")
                st.markdown(f"Answer: **{result_display}**")
        
        # Show complete sequence
        st.markdown("**Complete sequence:**")
        complete_seq = []
        for num in data['sequence']:
            if num >= 1000:
                complete_seq.append(f"{num:,}")
            else:
                complete_seq.append(str(num))
        st.info(", ".join(complete_seq))
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_geometric_problem_state():
    """Reset for next problem"""
    st.session_state.current_geometric_problem = None
    st.session_state.geometric_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "input_fields" in st.session_state:
        del st.session_state.input_fields