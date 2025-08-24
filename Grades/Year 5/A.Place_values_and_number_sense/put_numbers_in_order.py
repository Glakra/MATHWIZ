import streamlit as st
import random

def run():
    """
    Main function to run the Put Numbers in Order practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/put_numbers_in_order.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "put_numbers_order_difficulty" not in st.session_state:
        st.session_state.put_numbers_order_difficulty = 3  # Start with 3-digit numbers
    
    if "put_numbers_order_current_question" not in st.session_state:
        st.session_state.put_numbers_order_current_question = None
        st.session_state.put_numbers_order_question_type = None
        st.session_state.put_numbers_order_correct_answer = None
        st.session_state.put_numbers_order_show_feedback = False
        st.session_state.put_numbers_order_answer_submitted = False
        st.session_state.put_numbers_order_question_data = {}
        st.session_state.put_numbers_order_selected_order = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Put Numbers in Order")
    st.markdown("*Arrange numbers from smallest to largest or largest to smallest*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.put_numbers_order_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (2 to 6 digits)
        progress = (difficulty_level - 2) / 4  # Convert 2-6 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level <= 3:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 4:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.put_numbers_order_current_question is None:
        generate_new_question()
    
    # Display current question based on type
    if st.session_state.put_numbers_order_question_type == "position_finder":
        display_position_finder_question()
    else:
        display_click_to_order_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Types of Questions:
        
        **🎯 Position Finder:**
        - Look at a list of numbers
        - Figure out which number comes 1st, 2nd, 3rd, etc. when sorted
        - Think about the order before answering
        
        **🔄 Click to Order:**
        - Click numbers in the correct order
        - Arrange from smallest to largest OR largest to smallest
        - Read the instruction carefully!
        
        ### Tips:
        - **Compare digit by digit** from left to right
        - **Smaller numbers** have fewer digits (usually)
        - **Same digit count?** Compare the leftmost digit first
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** (10s - 100s)
        - **🟠 4-5 digit numbers:** (1,000s - 10,000s)  
        - **🔴 6 digit numbers:** (100,000s)
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 6-digit numbers!
        """)

def generate_new_question():
    """Generate a new ordering question"""
    digits = st.session_state.put_numbers_order_difficulty
    
    # Randomly choose question type
    question_type = random.choice(["position_finder", "click_to_order"])
    
    st.session_state.put_numbers_order_question_type = question_type
    st.session_state.put_numbers_order_selected_order = []  # Reset selection
    
    if question_type == "position_finder":
        generate_position_finder_question(digits)
    else:
        generate_click_to_order_question(digits)

def generate_position_finder_question(digits):
    """Generate a position finder question"""
    # Generate 5 unique random numbers
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    numbers = random.sample(range(min_val, max_val), 5)
    
    order = random.choice(["ascending", "descending"])
    position_index = random.randint(1, 5)  # 1-based index
    
    correct_list = sorted(numbers) if order == "ascending" else sorted(numbers, reverse=True)
    correct_answer = str(correct_list[position_index - 1])
    
    order_text = "smallest to largest" if order == "ascending" else "largest to smallest"
    ordinal = ["first", "second", "third", "fourth", "fifth"][position_index - 1]
    
    st.session_state.put_numbers_order_question_data = {
        "numbers": numbers,
        "order": order,
        "position": position_index,
        "order_text": order_text,
        "ordinal": ordinal,
        "correct_list": correct_list
    }
    st.session_state.put_numbers_order_correct_answer = correct_answer
    st.session_state.put_numbers_order_current_question = f"If you arrange these numbers from **{order_text}**, which number will come **{ordinal}**?"

def generate_click_to_order_question(digits):
    """Generate a click to order question"""
    # Generate 4 unique random numbers
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    numbers = random.sample(range(min_val, max_val), 4)
    
    direction = random.choice(["ascending", "descending"])
    correct_order = sorted(numbers) if direction == "ascending" else sorted(numbers, reverse=True)
    direction_text = "smallest to largest" if direction == "ascending" else "largest to smallest"
    
    st.session_state.put_numbers_order_question_data = {
        "numbers": numbers,
        "direction": direction,
        "direction_text": direction_text,
        "correct_order": correct_order
    }
    st.session_state.put_numbers_order_correct_answer = correct_order
    st.session_state.put_numbers_order_current_question = f"Put these numbers in order from **{direction_text}**"

def display_position_finder_question():
    """Display position finder question interface"""
    data = st.session_state.put_numbers_order_question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.put_numbers_order_current_question}**")
    
    # Display numbers in a nice format
    st.markdown("**Numbers to consider:**")
    
    # Create columns for the numbers
    cols = st.columns(5)
    for i, number in enumerate(data['numbers']):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; font-size: 20px; padding: 10px; 
                        background-color: #f0f2f6; border-radius: 8px; margin: 5px;">
                <strong>{number:,}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.text_input(
                f"Which number comes {data['ordinal']}?",
                placeholder="Type the number",
                key="put_numbers_order_position_answer"
            )
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.put_numbers_order_user_answer = user_answer.strip()
            st.session_state.put_numbers_order_show_feedback = True
            st.session_state.put_numbers_order_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_click_to_order_question():
    """Display click to order question interface"""
    data = st.session_state.put_numbers_order_question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.put_numbers_order_current_question}**")
    
    # Display numbers as clickable elements
    st.markdown("**Click the numbers in the correct order:**")
    
    # Create buttons in columns
    cols = st.columns(4)
    
    # Track which numbers have been selected
    if "put_numbers_order_button_states" not in st.session_state:
        st.session_state.put_numbers_order_button_states = {num: False for num in data['numbers']}
    
    for i, number in enumerate(data['numbers']):
        with cols[i]:
            # Check if this number is already selected
            is_selected = number in st.session_state.put_numbers_order_selected_order
            button_style = "secondary" if is_selected else "primary"
            disabled = is_selected
            
            if st.button(
                f"{number:,}",
                key=f"put_numbers_order_btn_{number}",
                type=button_style,
                disabled=disabled,
                use_container_width=True
            ):
                if number not in st.session_state.put_numbers_order_selected_order:
                    st.session_state.put_numbers_order_selected_order.append(number)
                    st.rerun()
    
    # Show current selection
    if st.session_state.put_numbers_order_selected_order:
        st.markdown("**Your order so far:**")
        order_display = " → ".join([f"{num:,}" for num in st.session_state.put_numbers_order_selected_order])
        st.markdown(f"**{order_display}**")
    
    # Reset button
    if st.session_state.put_numbers_order_selected_order:
        if st.button("🔄 Reset Selection", type="secondary"):
            st.session_state.put_numbers_order_selected_order = []
            st.session_state.put_numbers_order_button_states = {num: False for num in data['numbers']}
            st.rerun()
    
    # Submit button (only show when all numbers are selected)
    if len(st.session_state.put_numbers_order_selected_order) == len(data['numbers']):
        if st.button("✅ Submit Order", type="primary", use_container_width=True):
            st.session_state.put_numbers_order_user_answer = st.session_state.put_numbers_order_selected_order.copy()
            st.session_state.put_numbers_order_show_feedback = True
            st.session_state.put_numbers_order_answer_submitted = True
            st.rerun()
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.put_numbers_order_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.put_numbers_order_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.put_numbers_order_user_answer
    correct_answer = st.session_state.put_numbers_order_correct_answer
    question_type = st.session_state.put_numbers_order_question_type
    
    # Compare answers based on question type
    if question_type == "position_finder":
        is_correct = str(user_answer) == str(correct_answer)
    else:
        is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 6 digits)
        old_difficulty = st.session_state.put_numbers_order_difficulty
        st.session_state.put_numbers_order_difficulty = min(
            st.session_state.put_numbers_order_difficulty + 1, 6
        )
        
        # Show encouragement based on difficulty
        if st.session_state.put_numbers_order_difficulty == 6 and old_difficulty < 6:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 6-digit number ordering!**")
        elif old_difficulty < st.session_state.put_numbers_order_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.put_numbers_order_difficulty}-digit numbers**")
    
    else:
        if question_type == "position_finder":
            st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        else:
            correct_text = " → ".join([f"{num:,}" for num in correct_answer])
            st.error(f"❌ **Not quite right.** The correct order was **{correct_text}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.put_numbers_order_difficulty
        st.session_state.put_numbers_order_difficulty = max(
            st.session_state.put_numbers_order_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.put_numbers_order_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.put_numbers_order_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    question_type = st.session_state.put_numbers_order_question_type
    data = st.session_state.put_numbers_order_question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "position_finder":
            numbers = data['numbers']
            correct_list = data['correct_list']
            ordinal = data['ordinal']
            order_text = data['order_text']
            
            st.markdown(f"""
            ### Step-by-step solution:
            
            **Original numbers:** {', '.join([f'{n:,}' for n in numbers])}
            
            **Arranged from {order_text}:**
            """)
            
            for i, num in enumerate(correct_list):
                position = ["1st", "2nd", "3rd", "4th", "5th"][i]
                marker = "👈 **YOUR ANSWER**" if i == (data['position'] - 1) else ""
                st.markdown(f"**{position}:** {num:,} {marker}")
        
        else:  # click_to_order
            numbers = data['numbers']
            correct_order = data['correct_order']
            direction_text = data['direction_text']
            
            st.markdown(f"""
            ### Step-by-step solution:
            
            **Original numbers:** {', '.join([f'{n:,}' for n in numbers])}
            
            **How to arrange from {direction_text}:**
            1. **Compare all numbers** digit by digit from left to right
            2. **Arrange accordingly** - smaller to larger or larger to smaller
            
            **Correct order:** {' → '.join([f'{n:,}' for n in correct_order])}
            """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.put_numbers_order_current_question = None
    st.session_state.put_numbers_order_question_type = None
    st.session_state.put_numbers_order_correct_answer = None
    st.session_state.put_numbers_order_show_feedback = False
    st.session_state.put_numbers_order_answer_submitted = False
    st.session_state.put_numbers_order_question_data = {}
    st.session_state.put_numbers_order_selected_order = []
    if "put_numbers_order_user_answer" in st.session_state:
        del st.session_state.put_numbers_order_user_answer
    if "put_numbers_order_button_states" in st.session_state:
        del st.session_state.put_numbers_order_button_states