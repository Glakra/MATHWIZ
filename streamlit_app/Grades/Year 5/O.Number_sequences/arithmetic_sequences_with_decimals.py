import streamlit as st
import random

def run():
    """
    Main function to run the arithmetic sequences with decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/arithmetic_sequences_decimals.py
    """
    # Initialize session state
    if "decimal_seq_difficulty" not in st.session_state:
        st.session_state.decimal_seq_difficulty = 1
    
    if "current_decimal_problem" not in st.session_state:
        st.session_state.current_decimal_problem = None
        st.session_state.decimal_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Arithmetic Sequences with Decimals")
    st.markdown("*Find the missing decimal numbers in the pattern*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic decimals (0.1, 0.2, 0.5)",
            2: "Smaller steps (0.05, 0.25)",
            3: "Mixed decimals (various steps)",
            4: "Complex patterns (harder positions)",
            5: "Challenge mode (tricky decimals)"
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
    if st.session_state.current_decimal_problem is None:
        generate_new_decimal_problem()
    
    # Display current problem
    display_decimal_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Look at the decimal numbers** in the sequence
        2. **Find the common difference** (it will be a decimal)
        3. **Fill in BOTH missing numbers**
        4. **Click Submit** when done
        
        ### Working with Decimals:
        - **Count carefully** - 6.3 → 6.4 → 6.5 (adding 0.1)
        - **Watch decimal places** - 0.05 is different from 0.5
        - **Check your pattern** works for all numbers shown
        
        ### Common Decimal Steps:
        - **0.1** → 2.3, 2.4, 2.5, 2.6...
        - **0.05** → 1.20, 1.25, 1.30, 1.35...
        - **0.25** → 3.00, 3.25, 3.50, 3.75...
        - **0.5** → 4.0, 4.5, 5.0, 5.5...
        
        ### Tips:
        - **Line up decimal points** when calculating
        - **Add zeros if needed** - 6.0 = 6.00
        - **Check both answers** before submitting
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Common decimal steps
        - **🟡 Level 3:** Various decimal patterns
        - **🔴 Level 4-5:** Complex positions & unusual steps
        """)

def generate_new_decimal_problem():
    """Generate a new arithmetic sequence with decimals problem"""
    difficulty = st.session_state.decimal_seq_difficulty
    
    # Define step sizes and patterns by difficulty
    if difficulty == 1:
        # Basic decimals (0.1, 0.2, 0.5)
        steps = [0.1, 0.2, 0.5]
        step = random.choice(steps)
        start = round(random.choice([0.5, 1.0, 2.0, 3.0, 4.0, 5.0]), 1)
        length = 6
        missing_pattern = random.choice([
            [2, 3],  # Middle consecutive
            [4, 5],  # End consecutive
            [1, 3],  # Alternating
        ])
    
    elif difficulty == 2:
        # Smaller steps (0.05, 0.25)
        steps = [0.05, 0.1, 0.25]
        step = random.choice(steps)
        start = round(random.choice([0.20, 0.50, 1.00, 2.00, 3.00, 3.50]), 2)
        length = 6
        missing_pattern = random.choice([
            [1, 2],  # Beginning consecutive
            [2, 3],  # Middle consecutive
            [1, 4],  # Spread out
        ])
    
    elif difficulty == 3:
        # Mixed decimals (various steps)
        steps = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
        step = random.choice(steps)
        start = round(random.uniform(0.5, 5.0), 2)
        length = 6
        missing_pattern = random.choice([
            [0, 1],  # First two
            [2, 4],  # Alternating middle
            [3, 5],  # Alternating end
            [1, 4],  # Spread out
        ])
    
    elif difficulty == 4:
        # Complex patterns (harder positions)
        steps = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.75]
        step = random.choice(steps)
        start = round(random.uniform(0.1, 10.0), 2)
        length = random.choice([6, 7])
        # More challenging missing positions
        missing_pattern = random.choice([
            [0, 2],  # Skip pattern
            [1, 5],  # Far apart
            [0, 4],  # First and near end
            [2, 5],  # Middle and end
        ])
    
    else:  # difficulty == 5
        # Challenge mode (tricky decimals)
        steps = [0.05, 0.08, 0.12, 0.15, 0.25, 0.35, 0.45, 0.6, 0.75, 1.25]
        step = random.choice(steps)
        start = round(random.uniform(0.1, 20.0), 2)
        length = random.choice([7, 8])
        # Most challenging patterns
        missing_pattern = random.choice([
            [0, 1],  # First two (need to work backwards)
            [length-2, length-1],  # Last two
            [1, length-2],  # Near start and end
            [0, length-1],  # First and last
        ])
    
    # Generate the sequence
    sequence = []
    for i in range(length):
        value = start + step * i
        # Round to avoid floating point issues
        if step in [0.05, 0.15, 0.25, 0.35, 0.45, 0.75]:
            value = round(value, 2)
        else:
            value = round(value, 1)
        sequence.append(value)
    
    # Ensure missing indices are valid
    missing_indices = [i for i in missing_pattern if i < length][:2]
    
    st.session_state.decimal_problem_data = {
        'sequence': sequence,
        'missing_indices': missing_indices,
        'step': step,
        'difficulty': difficulty
    }
    st.session_state.current_decimal_problem = True

def display_decimal_problem():
    """Display the decimal arithmetic sequence problem"""
    data = st.session_state.decimal_problem_data
    
    # Display instruction
    st.markdown("### Fill in the missing numbers to complete the pattern:")
    
    # Create the sequence display using columns
    cols = st.columns(len(data['sequence']) + len(data['sequence']) - 1)
    
    # Track which columns have inputs
    input_refs = {}
    
    for i, num in enumerate(data['sequence']):
        col_idx = i * 2  # Account for comma columns
        
        with cols[col_idx]:
            if i in data['missing_indices']:
                # Input field for missing number
                user_input = st.text_input(
                    "",
                    key=f"decimal_input_{i}",
                    placeholder="",
                    label_visibility="collapsed"
                )
                input_refs[i] = user_input
            else:
                # Display the number
                st.markdown(f"<div style='text-align:center; font-size:18px; font-weight:bold; padding-top:5px;'>{num:.2f}</div>", unsafe_allow_html=True)
        
        # Add comma between numbers (except after last)
        if i < len(data['sequence']) - 1 and col_idx + 1 < len(cols):
            with cols[col_idx + 1]:
                st.markdown("<div style='text-align:center; font-size:18px; font-weight:bold; padding-top:5px;'>,</div>", unsafe_allow_html=True)
    
    # Style the input boxes
    st.markdown("""
    <style>
    input[type="text"] {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        height: 38px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        background-color: #e8f4fd;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Store input references
    st.session_state.input_refs = input_refs
    
    # Submit button
    st.markdown("")  # Add some space
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            # Check if all answers are provided
            all_answered = True
            for idx in data['missing_indices']:
                if idx not in input_refs or not input_refs[idx].strip():
                    all_answered = False
                    break
            
            if all_answered:
                # Store answers and validate
                for idx in data['missing_indices']:
                    st.session_state.user_answers[idx] = input_refs[idx]
                validate_decimal_answers()
            else:
                st.warning("Please fill in all missing numbers!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_decimal_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_decimal_problem_state()
                st.rerun()

def validate_decimal_answers():
    """Validate the user's decimal answers"""
    data = st.session_state.decimal_problem_data
    all_correct = True
    
    st.session_state.total_attempted += 1
    
    # Check each answer
    for missing_idx in data['missing_indices']:
        try:
            user_value = float(st.session_state.user_answers[missing_idx])
            correct_value = data['sequence'][missing_idx]
            
            # Allow small tolerance for floating point comparison
            if abs(user_value - correct_value) > 0.001:
                all_correct = False
        except:
            all_correct = False
    
    if all_correct:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        st.session_state.user_correct = True
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            if st.session_state.decimal_seq_difficulty < 5:
                st.session_state.decimal_seq_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        st.session_state.user_correct = False
        
        # Decrease difficulty after poor performance
        if st.session_state.total_attempted % 3 == 0:
            accuracy = st.session_state.total_correct / st.session_state.total_attempted
            if accuracy < 0.5 and st.session_state.decimal_seq_difficulty > 1:
                st.session_state.decimal_seq_difficulty -= 1
    
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_decimal_feedback():
    """Display feedback for decimal problems"""
    data = st.session_state.decimal_problem_data
    
    if st.session_state.user_correct:
        st.success("✅ **Correct! Both answers are right!**")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.decimal_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.decimal_seq_difficulty), unsafe_allow_html=True)
    else:
        st.error("❌ **Not quite right. Check your answers.**")
        
        # Show correct answers
        st.markdown("**Correct answers:**")
        for missing_idx in data['missing_indices']:
            correct_value = data['sequence'][missing_idx]
            user_value = st.session_state.user_answers.get(missing_idx, "")
            
            if user_value:
                try:
                    user_float = float(user_value)
                    if abs(user_float - correct_value) > 0.001:
                        st.markdown(f"Position {missing_idx + 1}: **{correct_value:.2f}** (You entered: {user_value})")
                except:
                    st.markdown(f"Position {missing_idx + 1}: **{correct_value:.2f}** (Invalid input)")
        
        # Show explanation
        show_decimal_explanation()

def show_decimal_explanation():
    """Show step-by-step solution for decimal sequences"""
    data = st.session_state.decimal_problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the complete sequence with missing positions marked
        sequence_display = []
        for i, num in enumerate(data['sequence']):
            if i in data['missing_indices']:
                sequence_display.append("**?**")
            else:
                sequence_display.append(f"{num:.2f}")
        
        st.markdown(f"**Sequence:** {', '.join(sequence_display)}")
        
        # Find the common difference
        st.markdown("**Step 1: Find the common difference**")
        
        # Find two consecutive known numbers
        for i in range(len(data['sequence']) - 1):
            if i not in data['missing_indices'] and (i + 1) not in data['missing_indices']:
                num1 = data['sequence'][i]
                num2 = data['sequence'][i + 1]
                diff = round(num2 - num1, 2)
                st.code(f"{num2:.2f} - {num1:.2f} = {diff:.2f}")
                break
        
        st.markdown(f"The common difference is **{data['step']}**")
        
        # Show how to find each missing number
        st.markdown("**Step 2: Calculate the missing numbers**")
        
        for missing_idx in sorted(data['missing_indices']):
            st.markdown(f"**Finding position {missing_idx + 1}:**")
            
            if missing_idx > 0 and (missing_idx - 1) not in data['missing_indices']:
                # Use previous number
                prev_num = data['sequence'][missing_idx - 1]
                result = data['sequence'][missing_idx]
                st.code(f"{prev_num:.2f} + {data['step']:.2f} = {result:.2f}")
            elif missing_idx < len(data['sequence']) - 1 and (missing_idx + 1) not in data['missing_indices']:
                # Use next number
                next_num = data['sequence'][missing_idx + 1]
                result = data['sequence'][missing_idx]
                st.code(f"{next_num:.2f} - {data['step']:.2f} = {result:.2f}")
            else:
                # Calculate from nearest known number
                result = data['sequence'][missing_idx]
                st.markdown(f"Answer: **{result:.2f}**")
        
        # Show the complete sequence
        st.markdown("**Complete sequence:**")
        complete_seq = [f"{num:.2f}" for num in data['sequence']]
        st.info(", ".join(complete_seq))
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_decimal_problem_state():
    """Reset for next problem"""
    st.session_state.current_decimal_problem = None
    st.session_state.decimal_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "input_refs" in st.session_state:
        del st.session_state.input_refs