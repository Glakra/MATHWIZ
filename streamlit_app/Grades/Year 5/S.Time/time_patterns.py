import streamlit as st
import random
from datetime import datetime, timedelta
import math

def run():
    """
    Main function to run the Time Patterns practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S. Time/time_patterns.py
    """
    
    # Initialize session state
    if "time_patterns_difficulty" not in st.session_state:
        st.session_state.time_patterns_difficulty = 1  # Start with simple patterns
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
    
    if "question_type" not in st.session_state:
        st.session_state.question_type = None
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None  # Track selected answer
        st.session_state.answer_options = []  # Store options
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("⏰ Time Patterns")
    st.markdown("*Find patterns in time sequences and complete them*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_patterns_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple intervals (15, 30 min)",
            2: "Mixed intervals (15, 30, 45 min)",
            3: "Complex patterns (varied intervals)",
            4: "Backward patterns",
            5: "Advanced mixed patterns"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Level ' + str(difficulty_level))}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question based on type
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the time sequence** shown in clocks or numbers
        - **Find the pattern** (adding/subtracting minutes or hours)
        - **Click on a time option** to select it (it will be highlighted)
        - **Click Submit** to check your answer
        - **Click Next Question** to continue after seeing feedback
        
        ### Types of Patterns:
        - **Regular intervals:** Same time added each step (e.g., +15 min)
        - **Increasing intervals:** Pattern grows (e.g., +15, +30, +45...)
        - **Backward patterns:** Time goes backwards
        - **Hour transitions:** Patterns that cross hour boundaries
        
        ### Tips for Success:
        - **Find the difference** between consecutive times
        - **Check if the pattern is consistent** or changing
        - **Be careful with hour transitions** (e.g., 12:45 + 30 min = 1:15)
        
        ### Examples:
        - **Simple:** 1:00, 1:15, 1:30, ? → Pattern: +15 min → Answer: 1:45
        - **Hour transition:** 11:45, 12:00, 12:15, ? → Pattern: +15 min → Answer: 12:30
        - **Backward:** 3:00, 2:30, 2:00, ? → Pattern: -30 min → Answer: 1:30
        """)

def generate_new_question():
    """Generate a new time pattern question based on difficulty"""
    
    difficulty = st.session_state.time_patterns_difficulty
    
    # Choose question type based on difficulty
    if difficulty <= 2:
        question_types = ["digital_display", "text_sequence"]
    elif difficulty <= 3:
        question_types = ["digital_display", "text_sequence", "analog_display"]
    else:
        question_types = ["digital_display", "text_sequence", "analog_display"]
    
    question_type = random.choice(question_types)
    st.session_state.question_type = question_type
    
    # Generate pattern based on difficulty
    if difficulty == 1:
        intervals = [15, 30]
        interval = random.choice(intervals)
        pattern_type = "forward"
        sequence_length = 4
    elif difficulty == 2:
        intervals = [15, 30, 45]
        interval = random.choice(intervals)
        pattern_type = "forward"
        sequence_length = 4
    elif difficulty == 3:
        intervals = [15, 20, 25, 30, 45, 60, 75, 90]
        interval = random.choice(intervals)
        pattern_type = "forward"
        sequence_length = 5
    elif difficulty == 4:
        intervals = [15, 30, 45, 60]
        interval = random.choice(intervals)
        pattern_type = "backward"
        sequence_length = 4
    else:
        pattern_type = random.choice(["forward", "backward", "alternating"])
        if pattern_type == "alternating":
            interval = (15, 30)
        else:
            intervals = [15, 20, 25, 30, 45, 60, 75, 90]
            interval = random.choice(intervals)
        sequence_length = 5
    
    # Generate the time sequence
    sequence = generate_time_sequence(pattern_type, interval, sequence_length)
    
    # Choose which position to hide
    if difficulty <= 2:
        missing_index = len(sequence) - 1
    else:
        missing_index = random.randint(1, len(sequence) - 1)
    
    # Generate options
    correct_answer = sequence[missing_index]
    options = generate_time_options(correct_answer, interval, pattern_type)
    random.shuffle(options)
    st.session_state.answer_options = options[:6]
    
    # Store question data
    st.session_state.question_data = {
        "sequence": sequence,
        "missing_index": missing_index,
        "pattern_type": pattern_type,
        "interval": interval,
        "question_type": question_type
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Which is the missing time?" if question_type != "text_sequence" else "Fill in the missing time."

def generate_time_sequence(pattern_type, interval, length):
    """Generate a time sequence based on pattern type"""
    
    # Random starting time
    start_hour = random.randint(1, 11)
    start_minute = random.choice([0, 15, 30, 45])
    
    sequence = []
    current_time = datetime.strptime(f"{start_hour}:{start_minute:02d}", "%H:%M")
    
    for i in range(length):
        # Format time without leading zeros for single-digit hours
        hour = current_time.hour if current_time.hour <= 12 else current_time.hour - 12
        if hour == 0:
            hour = 12
        time_str = f"{hour}:{current_time.minute:02d}"
        sequence.append(time_str)
        
        if pattern_type == "forward":
            current_time += timedelta(minutes=interval)
        elif pattern_type == "backward":
            current_time -= timedelta(minutes=interval)
        elif pattern_type == "alternating":
            if i % 2 == 0:
                current_time += timedelta(minutes=interval[0])
            else:
                current_time += timedelta(minutes=interval[1])
    
    return sequence

def display_question():
    """Display the current question based on type"""
    
    data = st.session_state.question_data
    question_type = data["question_type"]
    
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    if question_type == "digital_display":
        display_digital_clocks_styled(data)
    elif question_type == "analog_display":
        display_analog_clocks_simple(data)
    else:  # text_sequence
        display_text_sequence(data)

def display_digital_clocks_styled(data):
    """Display digital clock style question using styled divs"""
    
    sequence = data["sequence"]
    missing_index = data["missing_index"]
    
    # Generate color for clocks
    colors = ["#FF69B4", "#4CAF50", "#FF8C00", "#00CED1", "#6495ED"]
    clock_color = random.choice(colors)
    
    # Create columns for clocks
    clock_cols = st.columns(len(sequence))
    
    for i, (col, time) in enumerate(zip(clock_cols, sequence)):
        with col:
            if i == missing_index:
                # Show question mark for missing time
                st.markdown(
                    f"""
                    <div style="
                        background: {clock_color};
                        border-radius: 10px;
                        padding: 15px;
                        text-align: center;
                        margin: 10px;
                    ">
                        <div style="
                            background: #E8F5E9;
                            border-radius: 5px;
                            padding: 10px;
                            font-size: 24px;
                            font-weight: bold;
                            color: #333;
                        ">?</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background: {clock_color};
                        border-radius: 10px;
                        padding: 15px;
                        text-align: center;
                        margin: 10px;
                    ">
                        <div style="
                            background: #E8F5E9;
                            border-radius: 5px;
                            padding: 10px;
                            font-size: 20px;
                            font-weight: bold;
                            color: #333;
                        ">{time}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Space before answer options
    st.markdown("---")
    
    # Create answer options with proper form handling
    display_answer_tiles_with_form(data)

def display_analog_clocks_simple(data):
    """Display analog clock style using simple visual representation"""
    
    sequence = data["sequence"]
    missing_index = data["missing_index"]
    
    # Create columns for clocks
    clock_cols = st.columns(len(sequence))
    
    for i, (col, time_str) in enumerate(zip(clock_cols, sequence)):
        with col:
            if i == missing_index:
                # Show question mark
                st.markdown(
                    """
                    <div style="
                        width: 100px;
                        height: 100px;
                        border: 3px solid #2196F3;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 10px auto;
                        background: white;
                    ">
                        <span style="font-size: 30px; font-weight: bold;">?</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Show time as text in circle (simplified analog representation)
                st.markdown(
                    f"""
                    <div style="
                        width: 100px;
                        height: 100px;
                        border: 3px solid #2196F3;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 10px auto;
                        background: white;
                    ">
                        <span style="font-size: 16px; font-weight: bold;">{time_str}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Space before answer options
    st.markdown("---")
    
    # Create answer options with proper form handling
    display_answer_tiles_with_form(data)

def display_text_sequence(data):
    """Display text sequence style question"""
    
    sequence = data["sequence"]
    missing_index = data["missing_index"]
    
    # Create the sequence display
    sequence_parts = []
    for i, time in enumerate(sequence):
        if i == missing_index:
            sequence_parts.append("___")
        else:
            sequence_parts.append(f"**{time}**")
    
    # Display sequence
    st.markdown(
        f"<div style='font-size: 24px; text-align: center; padding: 20px;'>{', '.join(sequence_parts)}</div>",
        unsafe_allow_html=True
    )
    
    # Input field for answer with form
    with st.form("text_answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_input = st.text_input(
                "Enter the missing time (e.g., 1:30):",
                key="time_text_input",
                placeholder="H:MM"
            )
            
            submitted = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submitted and user_input:
                st.session_state.selected_answer = user_input.strip()
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Show feedback and next button
    if st.session_state.answer_submitted:
        show_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def display_answer_tiles_with_form(data):
    """Display answer options as clickable tiles with proper form handling"""
    
    st.markdown("**Select your answer:**")
    
    # Get options from session state
    options = st.session_state.answer_options
    
    # If answer not submitted, show selection interface
    if not st.session_state.answer_submitted:
        with st.form("answer_selection_form", clear_on_submit=False):
            # Create tiles in a 3x2 grid
            tile_selection = None
            for row in range(2):
                cols = st.columns(3)
                for col in range(3):
                    idx = row * 3 + col
                    if idx < len(options):
                        with cols[col]:
                            option = options[idx]
                            # Use selectbox or radio in each position
                            if st.form_submit_button(
                                option,
                                use_container_width=True,
                                type="secondary"
                            ):
                                tile_selection = option
            
            # Store selection if made
            if tile_selection:
                st.session_state.selected_answer = tile_selection
                st.session_state.answer_submitted = True
                st.rerun()
    
    else:
        # After submission, show tiles with results
        correct_answer = st.session_state.correct_answer
        selected = st.session_state.selected_answer
        
        for row in range(2):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                if idx < len(options):
                    with cols[col]:
                        option = options[idx]
                        
                        # Style based on correctness
                        if option == correct_answer:
                            st.success(option)
                        elif option == selected:
                            st.error(option)
                        else:
                            st.button(option, disabled=True, use_container_width=True)
        
        # Show feedback
        show_feedback()
        
        # Next question button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def generate_time_options(correct_answer, interval, pattern_type):
    """Generate multiple choice options including the correct answer"""
    
    options = [correct_answer]
    
    # Parse correct answer
    time_parts = correct_answer.split(":")
    correct_hour = int(time_parts[0])
    correct_minute = int(time_parts[1])
    
    # Generate distractors based on common mistakes
    base_time = datetime.strptime(f"{correct_hour if correct_hour != 12 else 0}:{correct_minute:02d}", "%H:%M")
    if correct_hour == 12:
        base_time = base_time.replace(hour=12)
    
    if isinstance(interval, int):
        # Common mistakes
        offsets = [-interval*2, -interval, interval, interval*2, -15, 15, -30, 30, -45, 45]
        for offset in offsets:
            try:
                wrong_time = base_time + timedelta(minutes=offset)
                hour = wrong_time.hour if wrong_time.hour <= 12 else wrong_time.hour - 12
                if hour == 0:
                    hour = 12
                time_str = f"{hour}:{wrong_time.minute:02d}"
                if time_str != correct_answer and time_str not in options:
                    options.append(time_str)
            except:
                continue
    
    # Ensure we have at least 6 unique options
    while len(options) < 6:
        offset = random.choice([-90, -60, -45, -30, -15, 15, 30, 45, 60, 90])
        try:
            wrong_time = base_time + timedelta(minutes=offset)
            hour = wrong_time.hour if wrong_time.hour <= 12 else wrong_time.hour - 12
            if hour == 0:
                hour = 12
            time_str = f"{hour}:{wrong_time.minute:02d}"
            if time_str not in options:
                options.append(time_str)
        except:
            continue
    
    return options[:6]

def show_feedback():
    """Display feedback for the submitted answer"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    
    # Normalize answers for comparison
    def normalize_time(time_str):
        """Normalize time string for comparison"""
        time_str = time_str.strip()
        if ":" in time_str:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            return f"{hour}:{minute:02d}"
        return time_str
    
    normalized_user = normalize_time(user_answer)
    normalized_correct = normalize_time(correct_answer)
    
    if normalized_user == normalized_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.time_patterns_difficulty
            st.session_state.time_patterns_difficulty = min(
                st.session_state.time_patterns_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.time_patterns_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.time_patterns_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.time_patterns_difficulty
            st.session_state.time_patterns_difficulty = max(
                st.session_state.time_patterns_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.time_patterns_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.time_patterns_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_pattern_explanation()

def show_pattern_explanation():
    """Show explanation for the time pattern"""
    
    data = st.session_state.question_data
    sequence = data["sequence"]
    pattern_type = data["pattern_type"]
    interval = data["interval"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Understanding the Pattern:")
        
        # Show the complete sequence
        st.markdown(f"**Complete sequence:** {', '.join(sequence)}")
        
        # Explain the pattern
        if pattern_type == "forward":
            if isinstance(interval, int):
                st.markdown(f"**Pattern:** Add **{interval} minutes** each time")
                
                # Show step-by-step
                st.markdown("**Step-by-step:**")
                for i in range(len(sequence) - 1):
                    st.markdown(f"- {sequence[i]} + {interval} min = {sequence[i+1]}")
                    
        elif pattern_type == "backward":
            st.markdown(f"**Pattern:** Subtract **{interval} minutes** each time")
            
            # Show step-by-step
            st.markdown("**Step-by-step:**")
            for i in range(len(sequence) - 1):
                st.markdown(f"- {sequence[i]} - {interval} min = {sequence[i+1]}")
                
        elif pattern_type == "alternating":
            st.markdown(f"**Pattern:** Alternating between +{interval[0]} and +{interval[1]} minutes")
        
        # Tips
        st.markdown("""
        ### Tips for Finding Patterns:
        1. **Calculate the difference** between consecutive times
        2. **Check if the difference is constant**
        3. **Look for patterns** in the differences
        4. **Apply the pattern** to find the missing time
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.question_type = None
    st.session_state.selected_answer = None
    st.session_state.answer_options = []