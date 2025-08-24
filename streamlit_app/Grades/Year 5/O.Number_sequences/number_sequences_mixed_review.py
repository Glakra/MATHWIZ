import streamlit as st
import random

def run():
    """
    Main function to run the mixed number sequences review activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/number_sequences_mixed_review.py
    """
    # Initialize session state
    if "mixed_seq_difficulty" not in st.session_state:
        st.session_state.mixed_seq_difficulty = 1
    
    if "current_mixed_problem" not in st.session_state:
        st.session_state.current_mixed_problem = None
        st.session_state.mixed_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.user_answers = {}
        st.session_state.selected_choice = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Number Sequences: Mixed Review")
    st.markdown("*Practice all types of number patterns*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mixed_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic patterns (1 blank)",
            2: "Mixed patterns (1-2 blanks)",
            3: "Multiple choice challenges",
            4: "Complex patterns (2 blanks)",
            5: "Expert mode (all types)"
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
    if st.session_state.current_mixed_problem is None:
        generate_new_mixed_problem()
    
    # Display current problem
    display_mixed_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Types of Sequences:
        
        **1. Arithmetic (Add/Subtract same amount):**
        - Example: 5, 8, 11, 14... (+3 each time)
        - Example: 50, 45, 40, 35... (-5 each time)
        
        **2. Geometric (Multiply/Divide by same amount):**
        - Example: 3, 6, 12, 24... (×2 each time)
        - Example: 81, 27, 9, 3... (÷3 each time)
        
        **3. Increasing Patterns (Differences increase):**
        - Example: 1, 2, 4, 7, 11... (+1, +2, +3, +4...)
        - Example: 5, 5, 6, 8, 11... (+0, +1, +2, +3...)
        
        **4. Special Patterns:**
        - Fibonacci: Each number is sum of previous two
        - Squares: 1, 4, 9, 16, 25...
        - Mixed operations
        
        ### How to Solve:
        1. **Check differences** - Are they the same? (arithmetic)
        2. **Check ratios** - Do you multiply by the same number? (geometric)
        3. **Check if differences change** - Do they increase? (increasing pattern)
        4. **Look for special patterns** - Squares, doubles, etc.
        
        ### Multiple Choice Tips:
        - **Test each option** in the sequence
        - **Check the pattern** continues correctly
        - **Eliminate** obviously wrong answers first
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Single pattern types
        - **🟡 Level 3:** Multiple choice questions
        - **🔴 Level 4-5:** Mixed patterns, multiple blanks
        """)

def generate_new_mixed_problem():
    """Generate a new mixed sequence problem"""
    difficulty = st.session_state.mixed_seq_difficulty
    
    # Choose sequence type based on difficulty
    if difficulty == 1:
        # Basic patterns
        sequence_types = ['arithmetic', 'geometric_simple']
        weights = [0.6, 0.4]
    elif difficulty == 2:
        # Mixed patterns
        sequence_types = ['arithmetic', 'geometric', 'increasing']
        weights = [0.4, 0.3, 0.3]
    elif difficulty == 3:
        # Multiple choice focus
        sequence_types = ['arithmetic', 'geometric', 'increasing', 'decreasing']
        weights = [0.3, 0.3, 0.2, 0.2]
    elif difficulty == 4:
        # Complex patterns
        sequence_types = ['arithmetic', 'geometric', 'increasing', 'fibonacci', 'mixed']
        weights = [0.2, 0.2, 0.3, 0.15, 0.15]
    else:  # difficulty == 5
        # All types
        sequence_types = ['arithmetic', 'geometric', 'increasing', 'fibonacci', 'squares', 'decreasing', 'mixed']
        weights = [0.15, 0.15, 0.2, 0.15, 0.1, 0.15, 0.1]
    
    sequence_type = random.choices(sequence_types, weights=weights)[0]
    
    # Decide if multiple choice (more common at level 3+)
    if difficulty >= 3:
        is_multiple_choice = random.random() < 0.5
    else:
        is_multiple_choice = random.random() < 0.2
    
    # Generate sequence based on type
    if sequence_type == 'arithmetic':
        generate_arithmetic_sequence(difficulty, is_multiple_choice)
    elif sequence_type == 'geometric' or sequence_type == 'geometric_simple':
        generate_geometric_sequence(difficulty, is_multiple_choice, simple=(sequence_type == 'geometric_simple'))
    elif sequence_type == 'increasing':
        generate_increasing_sequence(difficulty, is_multiple_choice)
    elif sequence_type == 'decreasing':
        generate_decreasing_sequence(difficulty, is_multiple_choice)
    elif sequence_type == 'fibonacci':
        generate_fibonacci_sequence(difficulty, is_multiple_choice)
    elif sequence_type == 'squares':
        generate_squares_sequence(difficulty, is_multiple_choice)
    else:  # mixed
        generate_mixed_pattern_sequence(difficulty, is_multiple_choice)

def generate_arithmetic_sequence(difficulty, is_multiple_choice):
    """Generate arithmetic sequence problem"""
    if difficulty <= 2:
        step = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        start = random.randint(10, 100) if step < 0 else random.randint(1, 50)
        length = 6
        num_blanks = 1
    else:
        step = random.choice([-10, -8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8, 10])
        start = random.randint(20, 150) if step < 0 else random.randint(1, 100)
        length = random.randint(6, 8)
        num_blanks = 2 if difficulty >= 4 else random.choice([1, 2])
    
    # Generate sequence
    sequence = [start + i * step for i in range(length)]
    
    # Choose blank positions
    positions = list(range(length))
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice and num_blanks <= 2:
        options = generate_multiple_choice_options(sequence, missing_positions, 'arithmetic', step)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'arithmetic',
        'step': step,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_geometric_sequence(difficulty, is_multiple_choice, simple=False):
    """Generate geometric sequence problem"""
    if simple or difficulty <= 2:
        ratio = random.choice([2, 3, 4])
        start = random.choice([1, 2, 3, 4, 5])
        length = 5
        num_blanks = 1
    else:
        ratio = random.choice([2, 3, 4, 5, 0.5])
        start = random.choice([1, 2, 3, 4, 5, 8]) if ratio > 1 else random.choice([256, 512, 1024])
        length = random.randint(5, 7)
        num_blanks = 2 if difficulty >= 4 else random.choice([1, 2])
    
    # Generate sequence
    sequence = []
    current = start
    for _ in range(length):
        sequence.append(int(current))
        current *= ratio
    
    # Choose blank positions
    positions = list(range(length))
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice and num_blanks <= 2:
        options = generate_multiple_choice_options(sequence, missing_positions, 'geometric', ratio)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'geometric',
        'ratio': ratio,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_increasing_sequence(difficulty, is_multiple_choice):
    """Generate increasing difference sequence"""
    pattern_increment = random.choice([1, 2]) if difficulty <= 2 else random.choice([1, 2, 3])
    start = random.choice([1, 2, 3, 4, 5, 10])
    first_diff = random.choice([0, 1, 2, 3])
    length = random.randint(6, 8)
    num_blanks = 1 if difficulty <= 2 else random.choice([1, 2])
    
    # Generate sequence
    sequence = [start]
    current_diff = first_diff
    for i in range(1, length):
        sequence.append(sequence[-1] + current_diff)
        current_diff += pattern_increment
    
    # Choose blank positions
    positions = list(range(length))
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice and num_blanks <= 2:
        options = generate_multiple_choice_options(sequence, missing_positions, 'increasing', pattern_increment)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'increasing',
        'pattern_increment': pattern_increment,
        'first_diff': first_diff,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_decreasing_sequence(difficulty, is_multiple_choice):
    """Generate decreasing sequence"""
    if difficulty <= 3:
        step = random.choice([-10, -8, -6, -5])
        start = random.randint(70, 100)
    else:
        step = random.choice([-12, -10, -8, -6, -4])
        start = random.randint(80, 150)
    
    length = random.randint(6, 8)
    num_blanks = 2
    
    # Generate sequence
    sequence = [start + i * step for i in range(length)]
    
    # Always put blanks at beginning and end for decreasing
    missing_positions = [0, length - 1]
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice:
        options = generate_multiple_choice_options(sequence, missing_positions, 'arithmetic', step)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'decreasing',
        'step': step,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_fibonacci_sequence(difficulty, is_multiple_choice):
    """Generate Fibonacci-like sequence"""
    start1 = random.choice([1, 2, 3])
    start2 = random.choice([1, 2, 3, 4])
    length = random.randint(6, 8)
    
    # Generate sequence
    sequence = [start1, start2]
    for i in range(2, length):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    # Choose blank positions
    num_blanks = 1 if difficulty <= 3 else 2
    positions = list(range(2, length))  # Don't blank the first two
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice and num_blanks <= 2:
        options = generate_multiple_choice_options(sequence, missing_positions, 'fibonacci', None)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'fibonacci',
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_squares_sequence(difficulty, is_multiple_choice):
    """Generate squares sequence"""
    start = random.choice([1, 2, 3])
    length = random.randint(5, 7)
    
    # Generate sequence
    sequence = [(start + i) ** 2 for i in range(length)]
    
    # Choose blank positions
    num_blanks = 1 if difficulty <= 4 else 2
    positions = list(range(length))
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice and num_blanks <= 2:
        options = generate_multiple_choice_options(sequence, missing_positions, 'squares', None)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'squares',
        'start': start,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_mixed_pattern_sequence(difficulty, is_multiple_choice):
    """Generate mixed pattern sequence"""
    # For now, generate a simple alternating pattern
    pattern = random.choice(['alternating_add', 'alternating_multiply'])
    
    if pattern == 'alternating_add':
        step1 = random.choice([1, 2, 3])
        step2 = random.choice([4, 5, 6])
        start = random.randint(5, 20)
        length = 8
        
        sequence = [start]
        for i in range(1, length):
            if i % 2 == 1:
                sequence.append(sequence[-1] + step1)
            else:
                sequence.append(sequence[-1] + step2)
    else:
        # Alternating multiply/add
        multiply = 2
        add = random.choice([1, 2, 3])
        start = random.randint(2, 5)
        length = 6
        
        sequence = [start]
        for i in range(1, length):
            if i % 2 == 1:
                sequence.append(sequence[-1] * multiply)
            else:
                sequence.append(sequence[-1] + add)
    
    # Choose blank positions
    num_blanks = 2
    positions = list(range(length))
    missing_positions = random.sample(positions, num_blanks)
    missing_positions.sort()
    
    # Generate options if multiple choice
    options = None
    if is_multiple_choice:
        options = generate_multiple_choice_options(sequence, missing_positions, 'mixed', None)
    
    st.session_state.mixed_problem_data = {
        'sequence': sequence,
        'missing_positions': missing_positions,
        'type': 'mixed',
        'pattern': pattern,
        'is_multiple_choice': is_multiple_choice,
        'options': options
    }
    st.session_state.current_mixed_problem = True

def generate_multiple_choice_options(sequence, missing_positions, seq_type, pattern_value):
    """Generate multiple choice options for missing numbers"""
    correct_values = [sequence[pos] for pos in missing_positions]
    
    options = []
    
    # Always include the correct answer
    if len(correct_values) == 1:
        options.append(str(correct_values[0]))
    else:
        options.append(f"{correct_values[0]}, {correct_values[1]}")
    
    # Generate wrong options
    while len(options) < 4:
        wrong_values = []
        
        for i, correct in enumerate(correct_values):
            # Generate variations
            if seq_type == 'arithmetic':
                # Common mistakes: wrong step or off by one
                variations = [
                    correct + pattern_value,  # One step too far
                    correct - pattern_value,  # One step back
                    correct + 1,  # Off by 1
                    correct - 1,
                    correct + 2 * pattern_value,  # Two steps
                ]
            elif seq_type == 'geometric':
                variations = [
                    int(correct * pattern_value),  # One more multiplication
                    int(correct / pattern_value) if pattern_value > 1 else correct * 2,  # Wrong direction
                    correct + int(pattern_value),  # Add instead of multiply
                    correct - 1,
                ]
            else:
                # General variations
                variations = [
                    correct + random.randint(-5, 5),
                    correct * 2,
                    correct // 2 if correct > 10 else correct + 10,
                ]
            
            wrong = random.choice([v for v in variations if v > 0 and v != correct])
            wrong_values.append(wrong)
        
        # Format option
        if len(wrong_values) == 1:
            option = str(wrong_values[0])
        else:
            option = f"{wrong_values[0]}, {wrong_values[1]}"
        
        if option not in options:
            options.append(option)
    
    # Shuffle options
    random.shuffle(options)
    
    return options

def display_mixed_problem():
    """Display the mixed sequence problem"""
    data = st.session_state.mixed_problem_data
    
    # Display instruction
    if data['is_multiple_choice']:
        if len(data['missing_positions']) == 1:
            st.markdown("### Which number is missing from this sequence?")
        else:
            st.markdown("### Which numbers are missing from this sequence?")
    else:
        if len(data['missing_positions']) == 1:
            st.markdown("### Type the missing number in this sequence:")
        else:
            st.markdown(f"### Type the {len(data['missing_positions'])} missing numbers in this sequence:")
    
    # Display sequence
    if data['is_multiple_choice']:
        display_multiple_choice_sequence(data)
    else:
        display_text_input_sequence(data)

def display_text_input_sequence(data):
    """Display sequence with text input fields"""
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
                    key=f"mixed_input_{i}",
                    placeholder="",
                    label_visibility="collapsed"
                )
                input_fields[i] = user_input
            else:
                # Display the number
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
                validate_text_answers()
            else:
                st.warning("Please fill in all missing numbers!")

def display_multiple_choice_sequence(data):
    """Display sequence with multiple choice options"""
    # Display the sequence with blanks
    sequence_parts = []
    for i, num in enumerate(data['sequence']):
        if i in data['missing_positions']:
            sequence_parts.append("___")
        else:
            if num >= 1000:
                sequence_parts.append(f"{num:,}")
            else:
                sequence_parts.append(str(num))
    
    # Display sequence
    sequence_str = ",  ".join(sequence_parts)
    st.markdown(f"""
    <div style='text-align: center; font-size: 24px; font-weight: bold; margin: 30px 0; 
                padding: 20px; background-color: #f0f0f0; border-radius: 10px;'>
        {sequence_str}
    </div>
    """, unsafe_allow_html=True)
    
    # Display options as clickable tiles
    st.markdown("**Choose the correct answer:**")
    
    cols = st.columns(2)
    for i, option in enumerate(data['options']):
        col_idx = i % 2
        with cols[col_idx]:
            # Create button for each option
            button_key = f"option_{i}"
            
            # Style based on selection
            if st.session_state.selected_choice == option:
                button_type = "primary"
            else:
                button_type = "secondary"
            
            if st.button(
                option,
                key=button_key,
                type=button_type,
                use_container_width=True,
                disabled=st.session_state.answer_submitted
            ):
                st.session_state.selected_choice = option
                st.rerun()
    
    # Submit button
    st.markdown("")  # Add space
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            if st.session_state.selected_choice:
                validate_multiple_choice_answer()
            else:
                st.warning("Please select an answer!")

def validate_text_answers():
    """Validate text input answers"""
    data = st.session_state.mixed_problem_data
    all_correct = True
    
    st.session_state.total_attempted += 1
    
    # Check each answer
    for pos in data['missing_positions']:
        try:
            user_value = int(st.session_state.user_answers[pos].replace(',', ''))
            correct_value = data['sequence'][pos]
            
            if user_value != correct_value:
                all_correct = False
        except:
            all_correct = False
    
    process_answer_result(all_correct)

def validate_multiple_choice_answer():
    """Validate multiple choice answer"""
    data = st.session_state.mixed_problem_data
    
    st.session_state.total_attempted += 1
    
    # Get correct answer
    correct_values = [data['sequence'][pos] for pos in data['missing_positions']]
    if len(correct_values) == 1:
        correct_answer = str(correct_values[0])
    else:
        correct_answer = f"{correct_values[0]}, {correct_values[1]}"
    
    # Check if selected answer is correct
    all_correct = (st.session_state.selected_choice == correct_answer)
    
    process_answer_result(all_correct)

def process_answer_result(all_correct):
    """Process the result of answer validation"""
    if all_correct:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        st.session_state.user_correct = True
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            if st.session_state.mixed_seq_difficulty < 5:
                st.session_state.mixed_seq_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        st.session_state.user_correct = False
        
        # Decrease difficulty after poor performance
        if st.session_state.total_attempted % 3 == 0:
            accuracy = st.session_state.total_correct / st.session_state.total_attempted
            if accuracy < 0.5 and st.session_state.mixed_seq_difficulty > 1:
                st.session_state.mixed_seq_difficulty -= 1
    
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_mixed_feedback():
    """Display feedback for mixed sequence problems"""
    data = st.session_state.mixed_problem_data
    
    if st.session_state.user_correct:
        st.success("✅ **Correct! Well done!**")
        
        # Show pattern type
        pattern_names = {
            'arithmetic': 'arithmetic sequence',
            'geometric': 'geometric sequence',
            'increasing': 'increasing difference pattern',
            'decreasing': 'decreasing sequence',
            'fibonacci': 'Fibonacci-like sequence',
            'squares': 'square numbers',
            'mixed': 'mixed pattern'
        }
        st.info(f"This was a **{pattern_names.get(data['type'], 'number pattern')}**!")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.mixed_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.mixed_seq_difficulty), unsafe_allow_html=True)
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answers
        if data['is_multiple_choice']:
            correct_values = [data['sequence'][pos] for pos in data['missing_positions']]
            if len(correct_values) == 1:
                correct_display = str(correct_values[0])
            else:
                correct_display = f"{correct_values[0]}, {correct_values[1]}"
            st.markdown(f"**Correct answer:** {correct_display}")
        else:
            st.markdown("**Correct answers:**")
            for pos in sorted(data['missing_positions']):
                correct_value = data['sequence'][pos]
                user_value = st.session_state.user_answers.get(pos, "")
                
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
        show_mixed_explanation()

def show_mixed_explanation():
    """Show explanation based on sequence type"""
    data = st.session_state.mixed_problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show complete sequence
        sequence_display = []
        for i, num in enumerate(data['sequence']):
            if num >= 1000:
                sequence_display.append(f"{num:,}")
            else:
                sequence_display.append(str(num))
        
        st.markdown(f"**Complete sequence:** {', '.join(sequence_display)}")
        
        # Type-specific explanations
        if data['type'] == 'arithmetic':
            st.markdown(f"**Pattern:** This is an arithmetic sequence with common difference **{data['step']}**")
            st.markdown("Each number = previous number + " + str(data['step']))
            
        elif data['type'] == 'geometric':
            st.markdown(f"**Pattern:** This is a geometric sequence with common ratio **{data['ratio']}**")
            if data['ratio'] < 1:
                st.markdown(f"Each number = previous number ÷ {int(1/data['ratio'])}")
            else:
                st.markdown(f"Each number = previous number × {int(data['ratio'])}")
                
        elif data['type'] == 'increasing':
            st.markdown(f"**Pattern:** The differences increase by **{data['pattern_increment']}** each time")
            st.markdown(f"Differences: +{data['first_diff']}, +{data['first_diff'] + data['pattern_increment']}, +{data['first_diff'] + 2*data['pattern_increment']}...")
            
        elif data['type'] == 'decreasing':
            st.markdown(f"**Pattern:** This is a decreasing arithmetic sequence with step **{data['step']}**")
            
        elif data['type'] == 'fibonacci':
            st.markdown("**Pattern:** Each number is the sum of the two previous numbers")
            st.markdown("(Fibonacci-like sequence)")
            
        elif data['type'] == 'squares':
            st.markdown(f"**Pattern:** These are square numbers starting from {data['start']}")
            for i in range(min(4, len(data['sequence']))):
                st.code(f"{data['start'] + i}² = {(data['start'] + i)**2}")
                
        elif data['type'] == 'mixed':
            st.markdown("**Pattern:** This sequence uses alternating operations")
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

# Update display_mixed_problem to show feedback
def display_mixed_problem():
    """Display the mixed sequence problem"""
    data = st.session_state.mixed_problem_data
    
    # Display instruction
    if data['is_multiple_choice']:
        if len(data['missing_positions']) == 1:
            st.markdown("### Which number is missing from this sequence?")
        else:
            st.markdown("### Which numbers are missing from this sequence?")
    else:
        if len(data['missing_positions']) == 1:
            st.markdown("### Type the missing number in this sequence:")
        else:
            st.markdown(f"### Type the {len(data['missing_positions'])} missing numbers in this sequence:")
    
    # Display sequence
    if data['is_multiple_choice']:
        display_multiple_choice_sequence(data)
    else:
        display_text_input_sequence(data)
    
    # Show feedback
    if st.session_state.show_feedback:
        show_mixed_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_mixed_problem_state()
                st.rerun()

def reset_mixed_problem_state():
    """Reset for next problem"""
    st.session_state.current_mixed_problem = None
    st.session_state.mixed_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}
    st.session_state.selected_choice = None
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "input_fields" in st.session_state:
        del st.session_state.input_fields