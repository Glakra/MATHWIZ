import streamlit as st
import random

def run():
    """
    Main function to run the arithmetic sequences activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/arithmetic_sequences_whole_numbers.py
    """
    # Initialize session state
    if "arithmetic_difficulty" not in st.session_state:
        st.session_state.arithmetic_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Arithmetic Sequences with Whole Numbers")
    st.markdown("*Find the missing number in the arithmetic sequence*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.arithmetic_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic sequences (step 1-5)",
            2: "Medium sequences (step 6-10)",
            3: "Larger steps (step 11-20)",
            4: "Complex sequences (mixed steps)",
            5: "Challenge sequences (large numbers)"
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
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Look at the numbers** in the sequence
        2. **Find the common difference** between consecutive numbers
        3. **Apply the pattern** to find the missing number
        4. **Type your answer** in the box
        
        ### What is an Arithmetic Sequence?
        - Numbers that increase or decrease by the **same amount** each time
        - This amount is called the **common difference**
        
        ### Examples:
        - **2, 4, 6, 8, 10** → Adding 2 each time
        - **20, 15, 10, 5, 0** → Subtracting 5 each time
        - **11, 22, 33, 44, 55** → Adding 11 each time
        
        ### Tips:
        - **Check two consecutive numbers** to find the difference
        - **Verify the pattern** works for all given numbers
        - **Count carefully** when the missing number is in the middle
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Small steps (1-10)
        - **🟡 Level 3:** Larger steps (11-20)
        - **🔴 Level 4-5:** Complex patterns & large numbers
        """)

def generate_new_problem():
    """Generate a new arithmetic sequence problem"""
    difficulty = st.session_state.arithmetic_difficulty
    
    # Determine sequence parameters based on difficulty
    if difficulty == 1:
        # Basic sequences (step 1-5)
        step = random.randint(1, 5)
        start = random.randint(1, 20)
        length = random.randint(5, 6)
        increasing = True
    
    elif difficulty == 2:
        # Medium sequences (step 6-10)
        step = random.randint(6, 10)
        start = random.randint(10, 50)
        length = random.randint(5, 7)
        increasing = random.choice([True, False])
        if not increasing:
            start = random.randint(50, 100)
    
    elif difficulty == 3:
        # Larger steps (step 11-20)
        step = random.randint(11, 20)
        start = random.randint(20, 100)
        length = random.randint(5, 7)
        increasing = random.choice([True, False])
        if not increasing:
            start = random.randint(100, 200)
    
    elif difficulty == 4:
        # Complex sequences (mixed steps, both directions)
        step = random.randint(3, 25)
        length = random.randint(6, 8)
        increasing = random.choice([True, False])
        if increasing:
            start = random.randint(10, 50)
        else:
            start = random.randint(100, 300)
    
    else:  # difficulty == 5
        # Challenge sequences (large numbers, various steps)
        step = random.randint(7, 50)
        length = random.randint(6, 8)
        increasing = random.choice([True, False])
        if increasing:
            start = random.randint(50, 200)
        else:
            start = random.randint(500, 1000)
    
    # Generate the sequence
    sequence = []
    for i in range(length):
        if increasing:
            sequence.append(start + step * i)
        else:
            sequence.append(start - step * i)
    
    # Choose which position to hide
    # Vary the position based on difficulty
    if difficulty <= 2:
        # Hide near the end for easier levels
        missing_index = random.choice([length - 2, length - 1])
    else:
        # Hide anywhere for harder levels
        missing_index = random.randint(1, length - 1)
    
    st.session_state.problem_data = {
        'sequence': sequence,
        'missing_index': missing_index,
        'step': step,
        'increasing': increasing,
        'difficulty': difficulty
    }
    st.session_state.current_problem = True

def display_problem():
    """Display the arithmetic sequence problem"""
    data = st.session_state.problem_data
    
    # Display instruction
    st.markdown("### Type the missing number in this sequence:")
    
    # Create the sequence display
    sequence_container = st.container()
    with sequence_container:
        # Use columns for better layout
        cols = st.columns(len(data['sequence']) + 1)
        
        for i, num in enumerate(data['sequence']):
            with cols[i]:
                if i == data['missing_index']:
                    # Input field for missing number
                    user_answer = st.text_input(
                        "",
                        key=f"arithmetic_input_{i}",
                        placeholder="",
                        label_visibility="collapsed"
                    )
                    # Store reference to user answer
                    st.session_state.temp_user_answer = user_answer
                else:
                    # Display the number
                    if i < len(data['sequence']) - 1:
                        st.markdown(f"<div style='text-align:center; font-size:20px; padding:8px;'><b>{num},</b></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align:center; font-size:20px; padding:8px;'><b>{num}</b></div>", unsafe_allow_html=True)
    
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
        background-color: #f0f8ff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            if hasattr(st.session_state, 'temp_user_answer') and st.session_state.temp_user_answer:
                validate_answer(st.session_state.temp_user_answer)
            else:
                st.warning("Please enter a number!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def validate_answer(user_answer):
    """Validate the user's answer"""
    try:
        # Convert to integer
        user_value = int(user_answer)
        correct_value = st.session_state.problem_data['sequence'][st.session_state.problem_data['missing_index']]
        
        st.session_state.total_attempted += 1
        
        if user_value == correct_value:
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            st.session_state.user_correct = True
            
            # Increase difficulty after 3 consecutive correct
            if st.session_state.consecutive_correct >= 3:
                if st.session_state.arithmetic_difficulty < 5:
                    st.session_state.arithmetic_difficulty += 1
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            st.session_state.user_correct = False
            st.session_state.user_answer = user_value
            st.session_state.correct_answer = correct_value
            
            # Decrease difficulty after 2 wrong
            if st.session_state.total_attempted % 2 == 0 and st.session_state.total_correct < st.session_state.total_attempted / 2:
                if st.session_state.arithmetic_difficulty > 1:
                    st.session_state.arithmetic_difficulty -= 1
        
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True
        
    except:
        st.error("Please enter a valid whole number!")

def show_feedback():
    """Display feedback"""
    if st.session_state.user_correct:
        st.success("✅ **Correct! Excellent work!**")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.arithmetic_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.arithmetic_difficulty), unsafe_allow_html=True)
    else:
        correct = st.session_state.correct_answer
        user = st.session_state.user_answer
        st.error(f"❌ **Not quite. The correct answer is {correct}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the sequence
        sequence_str = []
        for i, num in enumerate(data['sequence']):
            if i == data['missing_index']:
                sequence_str.append("**?**")
            else:
                sequence_str.append(str(num))
        st.markdown(f"**Sequence:** {', '.join(sequence_str)}")
        
        # Find and show the common difference
        st.markdown("**Step 1: Find the common difference**")
        
        # Find two consecutive known numbers
        idx1, idx2 = None, None
        for i in range(len(data['sequence']) - 1):
            if i != data['missing_index'] and i + 1 != data['missing_index']:
                idx1, idx2 = i, i + 1
                break
        
        if idx1 is not None:
            num1, num2 = data['sequence'][idx1], data['sequence'][idx2]
            diff = num2 - num1
            st.code(f"{num2} - {num1} = {diff}")
            st.markdown(f"The common difference is **{diff}**")
        
        # Show how to find the missing number
        st.markdown("**Step 2: Find the missing number**")
        
        missing_idx = data['missing_index']
        if missing_idx > 0 and missing_idx - 1 != data['missing_index']:
            # Use previous number
            prev_num = data['sequence'][missing_idx - 1]
            if data['increasing']:
                st.code(f"? = {prev_num} + {data['step']}")
                st.code(f"? = {data['sequence'][missing_idx]}")
            else:
                st.code(f"? = {prev_num} - {data['step']}")
                st.code(f"? = {data['sequence'][missing_idx]}")
        elif missing_idx < len(data['sequence']) - 1:
            # Use next number
            next_num = data['sequence'][missing_idx + 1]
            if data['increasing']:
                st.code(f"? = {next_num} - {data['step']}")
                st.code(f"? = {data['sequence'][missing_idx]}")
            else:
                st.code(f"? = {next_num} + {data['step']}")
                st.code(f"? = {data['sequence'][missing_idx]}")
        
        # Pattern description
        if data['increasing']:
            st.info(f"💡 This is an **increasing** arithmetic sequence. Each number is **{data['step']} more** than the previous one.")
        else:
            st.info(f"💡 This is a **decreasing** arithmetic sequence. Each number is **{data['step']} less** than the previous one.")
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
    if "user_correct" in st.session_state:
        del st.session_state.user_correct
    if "correct_answer" in st.session_state:
        del st.session_state.correct_answer
    if "temp_user_answer" in st.session_state:
        del st.session_state.temp_user_answer