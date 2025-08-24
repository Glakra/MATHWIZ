import streamlit as st
import random

def run():
    """
    Main function to run the number sequence completion activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Patterns/use_rule_complete_number_sequence.py
    """
    # Initialize session state
    if "sequence_difficulty" not in st.session_state:
        st.session_state.sequence_difficulty = 1
    
    if "current_sequence" not in st.session_state:
        st.session_state.current_sequence = None
        st.session_state.sequence_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Patterns**")
    st.title("🔢 Use a Rule to Complete a Number Sequence")
    st.markdown("*Find the pattern and fill in the missing number*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.sequence_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Addition/Subtraction (1-5)",
            2: "Larger Steps (6-10)",
            3: "Multiplication Patterns",
            4: "Mixed Operations",
            5: "Complex Patterns"
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
    
    # Generate new sequence if needed
    if st.session_state.current_sequence is None:
        generate_new_sequence()
    
    # Display current sequence
    display_sequence()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        1. **Look at the numbers** in the pattern
        2. **Find the rule** - what's happening from one number to the next?
        3. **Apply the rule** to find the missing number
        4. **Type your answer** and click Submit
        
        ### Pattern Types by Level:
        
        **🟢 Level 1-2: Addition & Subtraction**
        - Add or subtract the same number each time
        - Examples: +2, +5, -3, -4
        
        **🟡 Level 3: Multiplication**
        - Multiply by the same number each time
        - Examples: ×2, ×3, ÷2
        
        **🔴 Level 4-5: Complex Patterns**
        - Mixed operations: +3 then ×2
        - Square numbers: 1, 4, 9, 16...
        - Fibonacci-like: add the previous two numbers
        
        ### Tips:
        - **Find the difference** between consecutive numbers
        - **Check if it's the same** each time
        - **Look for multiplication** if differences aren't constant
        - **Test your rule** on all given numbers
        """)

def generate_new_sequence():
    """Generate a new number sequence"""
    difficulty = st.session_state.sequence_difficulty
    
    if difficulty == 1:
        # Simple addition/subtraction (1-5)
        operation = random.randint(0, 1)  # 0 = add, 1 = subtract
        step = random.randint(1, 5)
        start = random.randint(1, 20)
        
        if operation == 0:  # Addition
            rule_text = f"add {step}"
            sequence = [start + step * i for i in range(4)]
        else:  # Subtraction
            start = random.randint(15, 30)  # Ensure positive results
            rule_text = f"subtract {step}"
            sequence = [start - step * i for i in range(4)]
    
    elif difficulty == 2:
        # Larger steps (6-10)
        operation = random.randint(0, 1)
        step = random.randint(6, 10)
        
        if operation == 0:  # Addition
            start = random.randint(1, 20)
            rule_text = f"add {step}"
            sequence = [start + step * i for i in range(4)]
        else:  # Subtraction
            start = random.randint(40, 60)
            rule_text = f"subtract {step}"
            sequence = [start - step * i for i in range(4)]
    
    elif difficulty == 3:
        # Multiplication patterns
        operation = random.randint(0, 2)
        
        if operation == 0:  # Multiply
            factor = random.randint(2, 4)
            start = random.randint(1, 5)
            rule_text = f"multiply by {factor}"
            sequence = [start * (factor ** i) for i in range(4)]
        elif operation == 1:  # Divide
            factor = 2
            start = random.randint(32, 64)
            rule_text = f"divide by {factor}"
            sequence = [start // (factor ** i) for i in range(4)]
        else:  # Add increasing amounts
            start = random.randint(1, 10)
            rule_text = "add increasing numbers (1, 2, 3, ...)"
            sequence = [start + sum(range(1, i+1)) for i in range(4)]
    
    elif difficulty == 4:
        # Mixed operations
        pattern_type = random.randint(0, 2)
        
        if pattern_type == 0:  # Alternating add/subtract
            step1 = random.randint(2, 5)
            step2 = random.randint(1, 3)
            start = random.randint(10, 20)
            rule_text = f"alternately add {step1} and subtract {step2}"
            sequence = [start]
            for i in range(1, 4):
                if (i - 1) % 2 == 0:
                    sequence.append(sequence[-1] + step1)
                else:
                    sequence.append(sequence[-1] - step2)
        elif pattern_type == 1:  # Add then multiply
            add_val = random.randint(1, 3)
            mult_val = 2
            start = random.randint(1, 5)
            rule_text = f"add {add_val} then multiply by {mult_val}, alternating"
            sequence = [start]
            for i in range(1, 4):
                if (i - 1) % 2 == 0:
                    sequence.append(sequence[-1] + add_val)
                else:
                    sequence.append(sequence[-1] * mult_val)
        else:  # Double and add
            start = random.randint(1, 5)
            rule_text = "double and add 1"
            sequence = [start * (2 ** i) + i for i in range(4)]
    
    else:  # difficulty == 5
        # Complex patterns
        pattern_type = random.randint(0, 2)
        
        if pattern_type == 0:  # Square numbers
            start = 1
            rule_text = "square numbers"
            sequence = [(i + 1) ** 2 for i in range(4)]
        elif pattern_type == 1:  # Triangular numbers
            start = 1
            rule_text = "triangular numbers (1, 3, 6, 10, ...)"
            sequence = [(i + 1) * (i + 2) // 2 for i in range(4)]
        else:  # Fibonacci-like
            start = random.randint(1, 3)
            second = random.randint(1, 3)
            rule_text = "add the previous two numbers"
            sequence = [start, second]
            for i in range(2, 4):
                sequence.append(sequence[i-1] + sequence[i-2])
    
    # Choose which position to hide (preferably the last one)
    missing_index = 3
    
    st.session_state.sequence_data = {
        'sequence': sequence,
        'missing_index': missing_index,
        'rule_text': rule_text,
        'start': sequence[0],
        'difficulty': difficulty
    }
    st.session_state.current_sequence = True

def display_sequence():
    """Display the sequence problem interface"""
    data = st.session_state.sequence_data
    
    # Display the instruction
    st.markdown("### Fill in the missing number in the pattern.")
    
    # Display the rule
    st.markdown(f"The first number is **{data['start']}**. The rule is to **{data['rule_text']}**.")
    
    # Create the sequence display with input field
    cols = st.columns(len(data['sequence']))
    user_answer = None
    
    for i, (col, num) in enumerate(zip(cols, data['sequence'])):
        with col:
            if i == data['missing_index']:
                # Input field for missing number
                user_answer = st.text_input(
                    "",
                    key=f"sequence_input_{i}",
                    placeholder="?",
                    label_visibility="collapsed"
                )
                # Style the input to match the images
                st.markdown("""
                <style>
                input[type="text"] {
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    height: 50px;
                    border: 2px solid #1f77b4;
                    border-radius: 5px;
                }
                </style>
                """, unsafe_allow_html=True)
            else:
                # Display the number
                if i < data['missing_index']:
                    st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:bold; padding:10px;'>{num},</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:bold; padding:10px;'>{num}</div>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            if user_answer:
                validate_answer(user_answer)
            else:
                st.warning("Please enter a number!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def validate_answer(user_answer):
    """Validate the user's answer"""
    try:
        # Convert to integer
        user_value = int(user_answer)
        correct_value = st.session_state.sequence_data['sequence'][st.session_state.sequence_data['missing_index']]
        
        st.session_state.total_attempted += 1
        
        if user_value == correct_value:
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            st.session_state.user_correct = True
            
            # Increase difficulty after 3 consecutive correct
            if st.session_state.consecutive_correct >= 3:
                if st.session_state.sequence_difficulty < 5:
                    st.session_state.sequence_difficulty += 1
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            st.session_state.user_correct = False
            st.session_state.user_answer = user_value
            st.session_state.correct_answer = correct_value
            
            # Decrease difficulty after mistakes
            if st.session_state.sequence_difficulty > 1:
                st.session_state.sequence_difficulty -= 1
        
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True
        
    except:
        st.error("Please enter a valid whole number!")

def show_feedback():
    """Display feedback"""
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
        
        # Show celebration message
        if st.session_state.consecutive_correct == 0:  # Just leveled up
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center;'>
                <h2 style='color: #4CAF50; margin: 0;'>🌟 FANTASTIC! 🌟</h2>
                <p style='font-size: 18px; color: #2196F3; margin: 10px 0;'>You're ready for the next level!</p>
                <p style='font-size: 24px; margin: 0;'>🎯 🏆 🎉</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        correct = st.session_state.correct_answer
        user = st.session_state.user_answer
        st.error(f"❌ **Not quite right.** The correct answer is **{correct}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step solution"""
    data = st.session_state.sequence_data
    
    with st.expander("📖 **See the complete solution**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the sequence with the pattern
        sequence_str = ', '.join([str(n) if i != data['missing_index'] else '?' for i, n in enumerate(data['sequence'])])
        st.markdown(f"**Given sequence:** {sequence_str}")
        st.markdown(f"**Rule:** {data['rule_text']}")
        
        # Show how to apply the rule
        st.markdown("**Applying the rule:**")
        
        if data['difficulty'] <= 2:
            # Simple arithmetic progression
            st.markdown("Let's check the pattern:")
            for i in range(1, len(data['sequence'])):
                if i != data['missing_index'] and i-1 != data['missing_index']:
                    diff = data['sequence'][i] - data['sequence'][i-1]
                    st.code(f"{data['sequence'][i]} - {data['sequence'][i-1]} = {diff}")
        
        # Show the calculation for the missing number
        st.markdown("**Finding the missing number:**")
        correct_answer = data['sequence'][data['missing_index']]
        
        if data['difficulty'] <= 2:
            # For simple arithmetic
            step = data['sequence'][1] - data['sequence'][0]
            st.code(f"? = {data['sequence'][2]} + {step}")
            st.code(f"? = {correct_answer}")
        else:
            # For complex patterns
            st.markdown(f"Apply the rule '{data['rule_text']}' to get:")
            st.code(f"? = {correct_answer}")
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_question_state():
    """Reset for next question"""
    st.session_state.current_sequence = None
    st.session_state.sequence_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "correct_answer" in st.session_state:
        del st.session_state.correct_answer