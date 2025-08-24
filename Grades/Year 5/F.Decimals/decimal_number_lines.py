import streamlit as st
import random

def run():
    """
    Main function to run the Decimal Number Lines practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/decimal_number_lines.py
    """
    # Initialize session state for difficulty and game state
    if "decimal_lines_difficulty" not in st.session_state:
        st.session_state.decimal_lines_difficulty = 1  # Start with 0-1 range
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📏 Decimal Number Lines")
    st.markdown("*Find decimal values on number lines*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_lines_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "0 to 1 (tenths)",
            2: "0 to 1 (hundredths)", 
            3: "0 to 10 (decimals)",
            4: "Mixed ranges",
            5: "Complex decimals"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the number line** and find where the point is marked
        - **Count the divisions** between the whole numbers
        - **Write the decimal value** of the marked point
        
        ### Reading Number Lines:
        - **Each line represents a decimal place**
        - **Count from the starting number** (usually 0)
        - **Each small division** is worth a specific amount
        
        ### Examples:
        - **0 to 1 with 10 divisions:** Each division = 0.1 (tenths)
        - **0 to 1 with 100 divisions:** Each division = 0.01 (hundredths)
        - **0 to 10 with 10 divisions:** Each division = 1.0
        
        ### Tips:
        - **Look at the endpoints** to know the range
        - **Count the total divisions** to find the value of each
        - **Count from the start** to the marked point
        - **Write as a decimal** (like 0.7 or 2.3)
        
        ### Difficulty Levels:
        - **🟡 Level 1:** 0 to 1, tenths (0.1, 0.2, 0.3...)
        - **🟡 Level 2:** 0 to 1, hundredths (0.01, 0.02, 0.03...)
        - **🟠 Level 3:** 0 to 10, various decimals
        - **🔴 Level 4:** Different ranges and scales
        - **🔴 Level 5:** Complex decimal positions
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all number line levels!
        """)

def generate_new_question():
    """Generate a new decimal number line question based on difficulty level"""
    difficulty = st.session_state.decimal_lines_difficulty
    
    # Define question parameters by difficulty
    if difficulty == 1:
        # 0 to 1 range, tenths
        start = 0
        end = 1
        divisions = 10
        step = 0.1
        possible_values = [round(i * step, 1) for i in range(1, divisions)]
        
    elif difficulty == 2:
        # 0 to 1 range, hundredths (but show fewer marks for clarity)
        start = 0
        end = 1
        divisions = 20  # Show every 0.05 for readability
        step = 0.05
        possible_values = [round(i * step, 2) for i in range(1, divisions)]
        
    elif difficulty == 3:
        # 0 to 10 range
        start = 0
        end = 10
        divisions = 20
        step = 0.5
        possible_values = [round(i * step, 1) for i in range(1, divisions)]
        
    elif difficulty == 4:
        # Mixed ranges
        ranges = [
            (0, 2, 0.2),
            (0, 5, 0.5), 
            (1, 3, 0.1),
            (2, 4, 0.2)
        ]
        start, end, step = random.choice(ranges)
        divisions = int((end - start) / step)
        possible_values = [round(start + i * step, 2) for i in range(1, divisions)]
        
    else:  # difficulty == 5
        # Complex decimals
        ranges = [
            (0, 1, 0.02),
            (0, 2, 0.15),
            (1, 4, 0.25),
            (0, 3, 0.3)
        ]
        start, end, step = random.choice(ranges)
        divisions = int((end - start) / step)
        possible_values = [round(start + i * step, 2) for i in range(1, divisions)]
    
    # Select a random value
    point_value = random.choice(possible_values)
    
    # Generate a letter for the point
    point_letter = random.choice(['f', 'g', 'h', 'p', 'q', 'r', 's', 't'])
    
    # Store question data
    st.session_state.question_data = {
        "start": start,
        "end": end,
        "step": step,
        "point_value": point_value,
        "point_letter": point_letter,
        "divisions": divisions
    }
    st.session_state.correct_answer = point_value
    st.session_state.current_question = f"Find the value of {point_letter}. Write your answer as a decimal number."

def create_number_line_svg(data):
    """Create an SVG number line with the marked point"""
    start = data["start"]
    end = data["end"]
    step = data["step"]
    point_value = data["point_value"]
    point_letter = data["point_letter"]
    
    # SVG dimensions
    width = 600
    height = 120
    margin = 50
    line_width = width - 2 * margin
    
    # Calculate positions
    total_range = end - start
    
    # Create tick marks
    ticks = []
    labels = []
    
    # Major ticks at start and end
    ticks.append(f'<line x1="{margin}" y1="50" x2="{margin}" y2="70" stroke="#333" stroke-width="2"/>')
    labels.append(f'<text x="{margin}" y="90" text-anchor="middle" font-size="14" fill="#333">{start}</text>')
    
    ticks.append(f'<line x1="{margin + line_width}" y1="50" x2="{margin + line_width}" y2="70" stroke="#333" stroke-width="2"/>')
    labels.append(f'<text x="{margin + line_width}" y="90" text-anchor="middle" font-size="14" fill="#333">{end}</text>')
    
    # Add intermediate ticks
    num_divisions = int(total_range / step)
    for i in range(1, num_divisions):
        x_pos = margin + (i * step / total_range) * line_width
        ticks.append(f'<line x1="{x_pos}" y1="55" x2="{x_pos}" y2="65" stroke="#666" stroke-width="1"/>')
    
    # Mark the point
    point_x = margin + ((point_value - start) / total_range) * line_width
    point_mark = f'<line x1="{point_x}" y1="40" x2="{point_x}" y2="80" stroke="#007acc" stroke-width="3"/>'
    point_label = f'<text x="{point_x}" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#007acc">{point_letter}</text>'
    
    # Create the complete SVG
    svg = f'''
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
        <!-- Main line -->
        <line x1="{margin}" y1="60" x2="{margin + line_width}" y2="60" stroke="#333" stroke-width="3"/>
        
        <!-- Arrow -->
        <polygon points="{margin + line_width},{60} {margin + line_width - 8},{55} {margin + line_width - 8},{65}" fill="#333"/>
        
        <!-- Ticks -->
        {chr(10).join(ticks)}
        
        <!-- Point marker -->
        {point_mark}
        {point_label}
        
        <!-- Labels -->
        {chr(10).join(labels)}
    </svg>
    '''
    
    return svg

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📏 Question:")
    
    # Display the question in a clean format
    question_text = st.session_state.current_question
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #007acc;
        font-size: 18px;
        margin: 20px 0;
        color: #333;
    ">
        {question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Display the number line using Streamlit's HTML component
    svg_content = create_number_line_svg(data)
    
    # Use HTML component for proper SVG rendering
    import streamlit.components.v1 as components
    
    html_content = f"""
    <div style="text-align: center; margin: 30px 0; background-color: white; padding: 20px;">
        {svg_content}
    </div>
    """
    
    components.html(html_content, height=200)
    
    # Answer input
    st.markdown("**Enter your answer:**")
    
    # Create the answer input with specific styling
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"**{data['point_letter']} =**")
    
    # Create a form for better UX
    with st.form("answer_form", clear_on_submit=False):
        # Text input styled to match the images
        user_input = st.text_input(
            "Answer:", 
            key="line_answer_input",
            placeholder="Enter decimal number...",
            label_visibility="collapsed"
        )
        
        # Submit button styled like the images
        submit_button = st.form_submit_button(
            "Submit", 
            type="primary"
        )
        
        if submit_button and user_input:
            try:
                # Convert user input to float for comparison
                user_answer = float(user_input.strip())
                st.session_state.submitted_answer = user_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            except ValueError:
                st.error("❌ Please enter a valid decimal number.")
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.submitted_answer
    correct_answer = st.session_state.correct_answer
    
    # Check if answers match (allowing for floating point precision issues)
    if abs(user_answer - correct_answer) < 0.001:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.decimal_lines_difficulty
        st.session_state.decimal_lines_difficulty = min(
            st.session_state.decimal_lines_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.decimal_lines_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal number lines!**")
        elif old_difficulty < st.session_state.decimal_lines_difficulty:
            difficulty_names = {
                2: "hundredths on 0-1 lines",
                3: "decimals on 0-10 lines", 
                4: "mixed range number lines",
                5: "complex decimal lines"
            }
            next_level = difficulty_names.get(st.session_state.decimal_lines_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    start = data["start"]
    end = data["end"]
    step = data["step"]
    point_letter = data["point_letter"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution:
        
        **Number line range:** {start} to {end}
        **Point {point_letter} is at:** {correct_answer}
        
        ### How to solve:
        """)
        
        # Calculate steps from start
        steps_from_start = (correct_answer - start) / step
        
        st.markdown(f"""
        1. **Identify the range:** This number line goes from {start} to {end}
        2. **Find the step size:** Each division represents {step}
        3. **Count from {start}:** Point {point_letter} is {steps_from_start:.0f} steps from {start}
        4. **Calculate:** {start} + ({steps_from_start:.0f} × {step}) = **{correct_answer}**
        """)
        
        # Visual explanation
        if step == 0.1:
            st.markdown("💡 **Remember:** On a 0-1 line with 10 divisions, each step = 0.1 (one tenth)")
        elif step == 0.05:
            st.markdown("💡 **Remember:** Each small division = 0.05 (five hundredths)")
        elif step == 0.5:
            st.markdown("💡 **Remember:** Each division = 0.5 (one half)")
        
        st.markdown("""
        ### 💡 General tips:
        - **Count the total divisions** between whole numbers
        - **Calculate the step size** by dividing the range by divisions
        - **Count steps from the starting point** to find the value
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "submitted_answer" in st.session_state:
        del st.session_state.submitted_answer