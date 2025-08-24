import streamlit as st
import random

def run():
    """
    Main function to run the increasing number sequences activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/increasing_number_sequences.py
    """
    # Initialize session state
    if "increasing_seq_difficulty" not in st.session_state:
        st.session_state.increasing_seq_difficulty = 1
    
    if "current_increasing_problem" not in st.session_state:
        st.session_state.current_increasing_problem = None
        st.session_state.increasing_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Increasing Number Sequences")
    st.markdown("*Find the pattern where differences increase*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.increasing_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic patterns (1 blank, various positions)",
            2: "Skip patterns (1-2 blanks)",
            3: "Mixed patterns (2 blanks)",
            4: "Complex patterns (2-3 blanks)",
            5: "Challenge mode (3-4 blanks)"
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
    if st.session_state.current_increasing_problem is None:
        generate_new_increasing_problem()
    
    # Display current problem
    display_increasing_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Find the differences** between consecutive numbers
        2. **Look for the pattern** in the differences
        3. **Apply the pattern** to find missing numbers
        
        ### Common Patterns:
        
        **Adding 1 more each time:**
        - 1, 2, 4, 7, 11, 16...
        - Differences: +1, +2, +3, +4, +5...
        
        **Adding 2 more each time:**
        - 1, 3, 7, 13, 21...
        - Differences: +2, +4, +6, +8...
        
        **Triangular numbers:**
        - 1, 3, 6, 10, 15, 21...
        - Adding: +2, +3, +4, +5, +6...
        
        **Square pattern:**
        - 1, 4, 9, 16, 25...
        - These are 1², 2², 3², 4², 5²...
        
        ### Strategy for Multiple Blanks:
        1. **Use known numbers** to find the pattern
        2. **Work from both directions** if needed
        3. **Fill easier blanks first** to help with harder ones
        4. **Check your work** by verifying the pattern
        
        ### Tips:
        - **Start with differences** - subtract each number from the next
        - **Look for patterns** in how differences increase
        - **Work backwards** if the blank is at the beginning
        - **Use middle numbers** to verify your pattern
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Simple patterns, 1-2 blanks
        - **🟡 Level 3:** 2 blanks anywhere
        - **🔴 Level 4-5:** Multiple blanks, complex patterns
        """)

def generate_new_increasing_problem():
    """Generate a new increasing number sequence problem"""
    difficulty = st.session_state.increasing_seq_difficulty
    
    if difficulty == 1:
        # Basic patterns (+1 each time), 1 blank at various positions
        pattern_increment = 1  # Differences increase by 1
        start = random.choice([1, 2, 3, 4, 5, 10, 15, 20])
        first_diff = random.choice([0, 1, 2, 3, 4, 5])
        length = random.randint(6, 8)
        
        # 1 blank at any position
        missing_positions = [random.randint(0, length - 1)]
        
        # Sometimes use triangular numbers for variety
        if random.random() < 0.3:
            # Triangular numbers: 1, 3, 6, 10, 15...
            start = random.choice([1, 3, 6])
            first_diff = random.choice([2, 3, 4]) if start == 1 else random.choice([3, 4, 5])
        
    elif difficulty == 2:
        # Skip patterns (+2, +3), 1-2 blanks
        pattern_increment = random.choice([1, 2, 3])
        start = random.choice([1, 2, 3, 5, 8, 10])
        first_diff = random.choice([1, 2, 3, 4])
        length = random.randint(6, 8)
        
        # 1 or 2 blanks
        num_blanks = random.choice([1, 2])
        positions = list(range(length))
        missing_positions = random.sample(positions, num_blanks)
        missing_positions.sort()
        
    elif difficulty == 3:
        # Mixed patterns, always 2 blanks
        pattern_increment = random.choice([1, 2, 3, 4])
        start = random.choice([1, 2, 3, 5, 7, 10, 12])
        first_diff = random.choice([0, 1, 2, 3, 4, 5])
        length = random.randint(7, 9)
        
        # Always 2 blanks, can be consecutive or spread out
        positions = list(range(length))
        if random.random() < 0.3:
            # Sometimes make them consecutive
            start_pos = random.randint(0, length - 2)
            missing_positions = [start_pos, start_pos + 1]
        else:
            missing_positions = random.sample(positions, 2)
            missing_positions.sort()
        
    elif difficulty == 4:
        # Complex patterns, 2-3 blanks
        pattern_increment = random.choice([1, 2, 3, 4, 5])
        start = random.choice([1, 2, 3, 4, 5, 6, 8, 10])
        first_diff = random.choice([0, 1, 2, 3, 4, 5])
        length = random.randint(7, 9)
        
        # 2 or 3 blanks
        num_blanks = random.choice([2, 3])
        positions = list(range(length))
        missing_positions = random.sample(positions, num_blanks)
        missing_positions.sort()
        
    else:  # difficulty == 5
        # Complex patterns & 3-4 blanks
        pattern_type = random.choice(['arithmetic', 'square', 'fibonacci-like', 'odd', 'custom'])
        
        if pattern_type == 'arithmetic':
            pattern_increment = random.choice([1, 2, 3, 4, 5, 6])
            start = random.choice([1, 2, 3, 4, 5, 7, 10, 12, 15])
            first_diff = random.choice([0, 1, 2, 3, 4, 5, 6])
            length = random.randint(8, 10)
        elif pattern_type == 'square':
            # Square numbers: 1, 4, 9, 16, 25...
            start = 1
            pattern_increment = 'square'
            first_diff = 0
            length = random.randint(6, 8)
        elif pattern_type == 'fibonacci-like':
            # Each difference is sum of previous two
            start = random.choice([1, 2])
            pattern_increment = 'fibonacci'
            first_diff = 1
            length = random.randint(7, 9)
        elif pattern_type == 'odd':
            # Differences are odd numbers: 1, 3, 5, 7...
            start = random.choice([1, 2, 3, 5])
            pattern_increment = 'odd'
            first_diff = 1
            length = random.randint(7, 9)
        else:  # custom
            pattern_increment = random.choice([6, 7, 8])
            start = random.choice([1, 2, 3, 4, 5])
            first_diff = random.choice([1, 2, 3, 4])
            length = random.randint(7, 9)
        
        # 3 or 4 blanks
        num_blanks = random.choice([3, 4])
        positions = list(range(length))
        missing_positions = random.sample(positions, num_blanks)
        missing_positions.sort()
        
        # Ensure we don't have too many consecutive blanks
        if len(missing_positions) >= 3:
            # Check for 3+ consecutive blanks and resample if needed
            consecutive_count = 1
            for i in range(1, len(missing_positions)):
                if missing_positions[i] == missing_positions[i-1] + 1:
                    consecutive_count += 1
                    if consecutive_count >= 3:
                        # Resample with fewer blanks
                        num_blanks = 3
                        missing_positions = random.sample(positions, num_blanks)
                        missing_positions.sort()
                        break
                else:
                    consecutive_count = 1
    
    # Generate the sequence
    sequence = []
    
    if pattern_increment == 'square':
        for i in range(length):
            sequence.append((i + 1) ** 2)
    elif pattern_increment == 'fibonacci':
        sequence = [start]
        diffs = [first_diff, first_diff + 1]
        for i in range(1, length):
            sequence.append(sequence[-1] + diffs[i-1])
            if i < length - 1:
                diffs.append(diffs[-1] + diffs[-2])
    elif pattern_increment == 'odd':
        sequence = [start]
        for i in range(1, length):
            sequence.append(sequence[-1] + (2 * i - 1))
    else:
        # Regular arithmetic increasing
        sequence = [start]
        current_diff = first_diff
        for i in range(1, length):
            sequence.append(sequence[-1] + current_diff)
            current_diff += pattern_increment
    
    st.session_state.increasing_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'pattern_increment': pattern_increment,
        'first_diff': first_diff,
        'difficulty': difficulty
    }
    st.session_state.current_increasing_problem = True

def display_increasing_problem():
    """Display the increasing sequence problem"""
    data = st.session_state.increasing_problem_data
    
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
                    key=f"increasing_input_{i}",
                    placeholder="",
                    label_visibility="collapsed"
                )
                input_fields[i] = user_input
            else:
                # Display the number
                st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold; padding-top:8px;'>{num}</div>", 
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
        width: 80px;
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
                validate_increasing_answers()
            else:
                st.warning("Please fill in all missing numbers!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_increasing_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_increasing_problem_state()
                st.rerun()

def validate_increasing_answers():
    """Validate the user's answers"""
    data = st.session_state.increasing_problem_data
    all_correct = True
    
    st.session_state.total_attempted += 1
    
    # Check each answer
    for pos in data['missing_positions']:
        try:
            user_value = int(st.session_state.user_answers[pos])
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
            if st.session_state.increasing_seq_difficulty < 5:
                st.session_state.increasing_seq_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        st.session_state.user_correct = False
        
        # Decrease difficulty after poor performance
        if st.session_state.total_attempted % 3 == 0:
            accuracy = st.session_state.total_correct / st.session_state.total_attempted
            if accuracy < 0.5 and st.session_state.increasing_seq_difficulty > 1:
                st.session_state.increasing_seq_difficulty -= 1
    
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_increasing_feedback():
    """Display feedback for increasing sequence problems"""
    data = st.session_state.increasing_problem_data
    
    if st.session_state.user_correct:
        if len(data['missing_positions']) == 1:
            st.success("✅ **Correct! Well done!**")
        else:
            st.success("✅ **Excellent! All answers are correct!**")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.increasing_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.increasing_seq_difficulty), unsafe_allow_html=True)
    else:
        st.error("❌ **Not quite right. Check your answers.**")
        
        # Show correct answers
        st.markdown("**Correct answers:**")
        for pos in sorted(data['missing_positions']):
            correct_value = data['sequence'][pos]
            user_value = st.session_state.user_answers.get(pos, "")
            
            if user_value:
                try:
                    user_int = int(user_value)
                    if user_int != correct_value:
                        st.markdown(f"Position {pos + 1}: **{correct_value}** (You entered: {user_value})")
                except:
                    st.markdown(f"Position {pos + 1}: **{correct_value}** (Invalid input)")
            else:
                st.markdown(f"Position {pos + 1}: **{correct_value}**")
        
        # Show explanation
        show_increasing_explanation()

def show_increasing_explanation():
    """Show step-by-step solution for increasing sequences"""
    data = st.session_state.increasing_problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the complete sequence with missing positions marked
        sequence_display = []
        for i, num in enumerate(data['sequence']):
            if i in data['missing_positions']:
                sequence_display.append("**?**")
            else:
                sequence_display.append(str(num))
        
        st.markdown(f"**Sequence:** {', '.join(sequence_display)}")
        
        # Calculate and show differences
        st.markdown("**Step 1: Find the differences between consecutive known numbers**")
        
        differences = []
        diff_display = []
        
        # Calculate all differences between consecutive known numbers
        for i in range(1, len(data['sequence'])):
            if i - 1 not in data['missing_positions'] and i not in data['missing_positions']:
                diff = data['sequence'][i] - data['sequence'][i-1]
                differences.append((i, diff))
                diff_display.append(f"{data['sequence'][i]} - {data['sequence'][i-1]} = +{diff}")
        
        for display in diff_display:
            st.code(display)
        
        # Identify the pattern
        st.markdown("**Step 2: Find the pattern in the differences**")
        
        if data['pattern_increment'] == 'square':
            st.markdown("This is a **square number sequence**: 1², 2², 3², 4²...")
            for i, num in enumerate(data['sequence']):
                if i not in data['missing_positions']:
                    st.code(f"{i+1}² = {num}")
        
        elif data['pattern_increment'] == 'fibonacci':
            st.markdown("This is a **Fibonacci-like pattern** where each difference is the sum of the previous two")
        
        elif data['pattern_increment'] == 'odd':
            st.markdown("The differences are **odd numbers**: 1, 3, 5, 7, 9...")
            
        else:
            # Regular arithmetic pattern
            if len(differences) >= 2:
                diff_of_diffs = []
                for i in range(1, len(differences)):
                    d = differences[i][1] - differences[i-1][1]
                    diff_of_diffs.append(d)
                
                if diff_of_diffs and all(d == diff_of_diffs[0] for d in diff_of_diffs):
                    st.markdown(f"The differences increase by **{diff_of_diffs[0]}** each time")
                    st.markdown(f"Pattern: +{data['first_diff']}, +{data['first_diff'] + data['pattern_increment']}, +{data['first_diff'] + 2*data['pattern_increment']}, ...")
        
        # Show how to find missing numbers
        st.markdown("**Step 3: Calculate the missing numbers**")
        
        # Build the full difference sequence
        if isinstance(data['pattern_increment'], int):
            full_diffs = []
            current_diff = data['first_diff']
            for i in range(len(data['sequence']) - 1):
                full_diffs.append(current_diff)
                current_diff += data['pattern_increment']
            
            st.markdown("**Complete difference pattern:**")
            st.code("Differences: " + ", ".join([f"+{d}" for d in full_diffs]))
        
        # Show calculation for each missing position
        for pos in sorted(data['missing_positions']):
            st.markdown(f"**Finding position {pos + 1}:**")
            
            if data['pattern_increment'] == 'square':
                st.code(f"{pos + 1}² = {data['sequence'][pos]}")
            else:
                # Find the best way to calculate this position
                if pos > 0 and pos - 1 not in data['missing_positions']:
                    # Can use previous number
                    if isinstance(data['pattern_increment'], int):
                        expected_diff = data['first_diff'] + (pos - 1) * data['pattern_increment']
                        st.code(f"{data['sequence'][pos-1]} + {expected_diff} = {data['sequence'][pos]}")
                elif pos < len(data['sequence']) - 1 and pos + 1 not in data['missing_positions']:
                    # Can use next number
                    if isinstance(data['pattern_increment'], int):
                        expected_diff = data['first_diff'] + pos * data['pattern_increment']
                        st.code(f"{data['sequence'][pos+1]} - {expected_diff} = {data['sequence'][pos]}")
                else:
                    st.markdown(f"Answer: **{data['sequence'][pos]}**")
        
        # Show the complete sequence
        st.markdown("**Complete sequence:**")
        complete_seq = [str(num) for num in data['sequence']]
        st.info(", ".join(complete_seq))
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_increasing_problem_state():
    """Reset for next problem"""
    st.session_state.current_increasing_problem = None
    st.session_state.increasing_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "input_fields" in st.session_state:
        del st.session_state.input_fields