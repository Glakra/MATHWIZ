import streamlit as st
import random

def run():
    """
    Main function to run the Subtract Fractions with Number Lines practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/subtract_fractions_with_like_denominators_using_number_lines.py
    """
    # Initialize session state for difficulty and game state
    if "subtract_numberline_difficulty" not in st.session_state:
        st.session_state.subtract_numberline_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions Using Number Lines")
    st.markdown("*Complete the subtraction number sentence for this model*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.subtract_numberline_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (denominators 2-4)",
            2: "Simple (denominators 4-6)",
            3: "Medium (denominators 6-8)",
            4: "Advanced (denominators 8-10)",
            5: "Expert (denominators 10-12)"
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
        ### How to Subtract on Number Lines:
        1. The number line goes from 0 to 1
        2. It's divided into equal parts based on the denominator
        3. **Start at the first fraction** (marked position)
        4. **Jump backwards** by the amount you're subtracting
        5. Where you land is your answer!
        
        ### Example:
        If you start at 7/8 and subtract 3/8:
        - Starting position: 7/8
        - Jump backwards: -3/8 (3 spaces left)
        - Final position: 4/8
        - So: 7/8 - 3/8 = 4/8
        
        ### Tips:
        - Subtraction means jumping LEFT (backwards)
        - Count the spaces you jump
        - The denominator stays the same
        - Check: your answer should be smaller than what you started with!
        """)

def generate_new_question():
    """Generate a new number line subtraction question"""
    difficulty = st.session_state.subtract_numberline_difficulty
    
    # Set denominator range based on difficulty
    if difficulty == 1:
        denominator = random.choice([2, 3, 4])
    elif difficulty == 2:
        denominator = random.choice([4, 5, 6])
    elif difficulty == 3:
        denominator = random.choice([6, 7, 8])
    elif difficulty == 4:
        denominator = random.choice([8, 9, 10])
    else:  # difficulty == 5
        denominator = random.choice([10, 11, 12])
    
    # Generate numerators (ensure first > second for positive result)
    # Start position should not be at the very beginning
    numerator1 = random.randint(2, denominator - 1)
    # Subtract amount should leave a positive result
    numerator2 = random.randint(1, numerator1 - 1)
    
    # Calculate the difference
    diff_numerator = numerator1 - numerator2
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "diff_numerator": diff_numerator
    }
    
    st.session_state.correct_answer = diff_numerator
    st.session_state.current_question = "Complete the subtraction number sentence for this model."

def create_number_line_svg(data):
    """Create an SVG number line showing fraction subtraction"""
    width = 600
    height = 200
    line_y = 120
    tick_height = 10
    
    # Calculate positions
    unit_width = (width - 100) / data['denominator']
    start_x = 50
    end_x = width - 50
    
    # Build SVG
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" style="margin: 20px 0;">')
    
    # Add arrow marker definition at the beginning
    svg_parts.append('<defs>')
    svg_parts.append('<marker id="arrowhead" markerWidth="10" markerHeight="7" ')
    svg_parts.append('refX="1" refY="3.5" orient="auto">')
    svg_parts.append('<polygon points="10 0, 0 3.5, 10 7" fill="#E91E63"/>')
    svg_parts.append('</marker>')
    svg_parts.append('</defs>')
    
    # Main number line
    svg_parts.append(f'<line x1="{start_x}" y1="{line_y}" x2="{end_x}" y2="{line_y}" ')
    svg_parts.append('stroke="#333" stroke-width="2"/>')
    
    # Arrows at ends
    svg_parts.append(f'<path d="M {start_x - 10} {line_y - 5} L {start_x} {line_y}')
    svg_parts.append(f' L {start_x - 10} {line_y + 5}" stroke="#333" stroke-width="2" fill="none"/>')
    svg_parts.append(f'<path d="M {end_x + 10} {line_y - 5} L {end_x} {line_y}')
    svg_parts.append(f' L {end_x + 10} {line_y + 5}" stroke="#333" stroke-width="2" fill="none"/>')
    
    # Tick marks and labels
    for i in range(data['denominator'] + 1):
        x = start_x + i * unit_width
        
        # Tick mark
        svg_parts.append(f'<line x1="{x}" y1="{line_y - tick_height}" ')
        svg_parts.append(f'x2="{x}" y2="{line_y + tick_height}" stroke="#333" stroke-width="1"/>')
        
        # Label
        if i == 0:
            label = "0"
        elif i == data['denominator']:
            label = "1"
        else:
            label = f"{i}/{data['denominator']}"
        
        svg_parts.append(f'<text x="{x}" y="{line_y + 25}" ')
        svg_parts.append(f'text-anchor="middle" font-size="12" fill="#666">{label}</text>')
    
    # Calculate positions for fractions
    x1 = start_x + data['numerator1'] * unit_width  # Starting position
    x2 = start_x + data['diff_numerator'] * unit_width  # Final position (after subtraction)
    
    # Starting position with enhanced label
    svg_parts.append(f'<rect x="{x1 - 20}" y="{line_y - 5}" ')
    svg_parts.append('width="40" height="10" fill="#E3F2FD" stroke="#2196F3" stroke-width="2" rx="3"/>')
    
    # Add label above the starting position
    fraction1_label = f"{data['numerator1']}/{data['denominator']}"
    svg_parts.append(f'<text x="{x1}" y="{line_y - 15}" ')
    svg_parts.append(f'text-anchor="middle" font-size="14" fill="#2196F3" font-weight="bold">{fraction1_label}</text>')
    
    # Final position - DON'T LABEL IT WITH THE ANSWER
    svg_parts.append(f'<rect x="{x2 - 20}" y="{line_y - 5}" ')
    svg_parts.append('width="40" height="10" fill="#FFEBEE" stroke="#E91E63" stroke-width="2" rx="3"/>')
    
    # Add a question mark at the final position
    svg_parts.append(f'<text x="{x2}" y="{line_y - 15}" ')
    svg_parts.append(f'text-anchor="middle" font-size="16" fill="#E91E63" font-weight="bold">?</text>')
    
    # Jump arc showing the subtraction (going backwards/left)
    jump_start = x1
    jump_end = x2
    jump_mid = (jump_start + jump_end) / 2
    arc_height = 50
    
    # Create backward jump arc path
    svg_parts.append(f'<path d="M {jump_start} {line_y - 10}')
    svg_parts.append(f' Q {jump_mid} {line_y - arc_height} ')
    svg_parts.append(f'{jump_end} {line_y - 10}" ')
    svg_parts.append('stroke="#E91E63" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>')
    
    # Label the jump with the subtraction amount
    jump_label = f"-{data['numerator2']}/{data['denominator']}"
    svg_parts.append(f'<text x="{jump_mid}" y="{line_y - arc_height - 10}" ')
    svg_parts.append('text-anchor="middle" font-size="18" fill="#E91E63" font-weight="bold">')
    svg_parts.append(f'{jump_label}</text>')
    
    # Add the equation at the top WITHOUT THE ANSWER
    equation_y = 50
    svg_parts.append(f'<rect x="{width/2 - 120}" y="{equation_y - 20}" ')
    svg_parts.append('width="240" height="40" fill="#F5F5F5" stroke="#DDD" stroke-width="1" rx="5"/>')
    
    # Display the equation at the top WITHOUT THE ANSWER
    equation = f"{data['numerator1']}/{data['denominator']} - {data['numerator2']}/{data['denominator']} = ?"
    svg_parts.append(f'<text x="{width/2}" y="{equation_y}" ')
    svg_parts.append('text-anchor="middle" font-size="18" font-weight="bold" fill="#333">')
    svg_parts.append(f'{equation}</text>')
    
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the number line
    numberline_svg = create_number_line_svg(data)
    st.markdown(numberline_svg, unsafe_allow_html=True)
    
    # Display the equation to complete
    st.markdown("")
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
    
    with col1:
        # First fraction
        html = '<div style="text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;">'
        html += '<div style="font-size: 24px; font-weight: bold;">'
        html += '<span style="border-bottom: 2px solid black; padding: 0 8px;">' + str(data['numerator1']) + '</span>'
        html += '<br>'
        html += '<span style="padding: 0 8px;">' + str(data['denominator']) + '</span>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 28px; padding-top: 25px;">
            −
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        html = '<div style="text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;">'
        html += '<div style="font-size: 24px; font-weight: bold;">'
        html += '<span style="border-bottom: 2px solid black; padding: 0 8px;">' + str(data['numerator2']) + '</span>'
        html += '<br>'
        html += '<span style="padding: 0 8px;">' + str(data['denominator']) + '</span>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 28px; padding-top: 25px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Input area
        with st.form("answer_form"):
            input_col, submit_col = st.columns([1, 1])
            
            with input_col:
                user_input = st.text_input(
                    "",
                    key="fraction_input",
                    placeholder="?/"+str(data['denominator']),
                    label_visibility="collapsed"
                )
            
            with submit_col:
                submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit and user_input.strip():
                # Parse the answer
                if '/' in user_input:
                    try:
                        parts = user_input.split('/')
                        user_num = int(parts[0])
                        user_denom = int(parts[1])
                        
                        # Check if denominator is correct
                        if user_denom != data['denominator']:
                            st.error(f"The denominator should be {data['denominator']}")
                        else:
                            st.session_state.user_answer = user_num
                            st.session_state.answer_submitted = True
                            st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid fraction")
                else:
                    try:
                        # If they just entered the numerator
                        user_num = int(user_input)
                        st.session_state.user_answer = user_num
                        st.session_state.answer_submitted = True
                        st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid number")
            elif submit:
                st.error("Please enter your answer")
    
    # Show feedback
    handle_feedback_and_next()

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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete equation
        fraction1 = f"{data['numerator1']}/{data['denominator']}"
        fraction2 = f"{data['numerator2']}/{data['denominator']}"
        result = f"{correct_answer}/{data['denominator']}"
        
        st.success(f"✓ {fraction1} - {fraction2} = {result}")
        
        # Show visual explanation
        with st.expander("🎯 **How the number line shows the answer**", expanded=True):
            st.markdown(f"""
            **Visual explanation:**
            - You started at {fraction1} on the number line
            - You jumped {fraction2} to the LEFT (subtraction)
            - You landed at {result}
            
            The number line helps you see that subtracting fractions is like jumping backwards!
            """)
        
        # Check if result is 0
        if correct_answer == 0:
            st.info("💡 **Special note:** Your answer is 0! You jumped all the way back to the start.")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.subtract_numberline_difficulty
        st.session_state.subtract_numberline_difficulty = min(
            st.session_state.subtract_numberline_difficulty + 1, 5
        )
        
        if st.session_state.subtract_numberline_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered subtracting fractions with number lines!**")
        elif old_difficulty < st.session_state.subtract_numberline_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.subtract_numberline_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        user_fraction = f"{user_answer}/{data['denominator']}"
        st.error(f"You answered: {user_fraction}")
        
        # Show the correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.subtract_numberline_difficulty
        st.session_state.subtract_numberline_difficulty = max(
            st.session_state.subtract_numberline_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.subtract_numberline_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.subtract_numberline_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for subtracting fractions with number lines"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Number Lines for Subtracting Fractions**", expanded=True):
        st.markdown(f"""
        ### How to Subtract Fractions on a Number Line
        
        **Your problem:**
        {data['numerator1']}/{data['denominator']} - {data['numerator2']}/{data['denominator']} = ?
        
        **Step 1: Find your starting point**
        - Look for the first highlighted box: {data['numerator1']}/{data['denominator']}
        - This is where you begin
        
        **Step 2: See the backward jump**
        - The curved arrow shows you're subtracting {data['numerator2']}/{data['denominator']}
        - This means you jump {data['numerator2']} spaces to the LEFT
        
        **Step 3: Find where you land**
        - Start at {data['numerator1']} and go back {data['numerator2']}
        - {data['numerator1']} - {data['numerator2']} = {data['diff_numerator']}
        - You land at {data['diff_numerator']}/{data['denominator']}
        
        **Answer: {data['diff_numerator']}/{data['denominator']}**
        
        ### Remember:
        - The number line is divided into {data['denominator']} equal parts
        - Each tick mark represents 1/{data['denominator']}
        - Subtracting means jumping to the LEFT
        - The denominator never changes!
        
        ### Visual Clues:
        - 🔵 Blue box = Starting position
        - 🔴 Pink box = Where you land
        - ⬅️ Pink arrow = Direction of subtraction
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer