import streamlit as st
import random

def run():
    """
    Main function to run the Add and Subtract Fractions with Number Lines practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/add_and_subtract_fractions_with_like_denominators_using_number_lines.py
    """
    # Initialize session state for difficulty and game state
    if "add_subtract_numberline_difficulty" not in st.session_state:
        st.session_state.add_subtract_numberline_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕➖ Add and Subtract Fractions Using Number Lines")
    st.markdown("*Complete the addition or subtraction number sentence for this model*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.add_subtract_numberline_difficulty
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
        ### How to Use Number Lines:
        
        **For Addition:**
        - Start at the first fraction
        - Jump RIGHT (forward) by the second fraction
        - Where you land is your answer
        
        **For Subtraction:**
        - Start at the first fraction
        - Jump LEFT (backward) by the second fraction
        - Where you land is your answer
        
        ### Visual Clues:
        - **Blue arc** = Addition (jumping forward) ➡️
        - **Pink arc** = Subtraction (jumping backward) ⬅️
        - Count the tick marks to find your answer
        
        ### Remember:
        - The denominator never changes
        - Addition = move right
        - Subtraction = move left
        """)

def generate_new_question():
    """Generate a new number line addition or subtraction question"""
    difficulty = st.session_state.add_subtract_numberline_difficulty
    
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
    
    # Randomly choose operation
    operation = random.choice(["add", "subtract"])
    
    if operation == "add":
        # Generate addition problem
        # Ensure sum doesn't exceed denominator
        numerator1 = random.randint(1, min(denominator - 1, denominator - 1))
        max_num2 = min(denominator - numerator1, denominator - 1)
        numerator2 = random.randint(1, max_num2)
        result = numerator1 + numerator2
    else:
        # Generate subtraction problem
        # Ensure positive result
        numerator1 = random.randint(2, denominator - 1)
        numerator2 = random.randint(1, numerator1 - 1)
        result = numerator1 - numerator2
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "result": result,
        "operation": operation
    }
    
    st.session_state.correct_answer = result
    st.session_state.current_question = "Complete the addition number sentence for this model." if operation == "add" else "Complete the subtraction number sentence for this model."

def create_number_line_svg(data):
    """Create an SVG number line showing fraction addition or subtraction"""
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
    
    # Add arrow marker definitions
    svg_parts.append('<defs>')
    # Blue arrow for addition (pointing right)
    svg_parts.append('<marker id="arrowhead-blue" markerWidth="10" markerHeight="7" ')
    svg_parts.append('refX="9" refY="3.5" orient="auto">')
    svg_parts.append('<polygon points="0 0, 10 3.5, 0 7" fill="#2196F3"/>')
    svg_parts.append('</marker>')
    # Pink arrow for subtraction (pointing left)
    svg_parts.append('<marker id="arrowhead-pink" markerWidth="10" markerHeight="7" ')
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
    x1 = start_x + data['numerator1'] * unit_width
    x2 = start_x + data['result'] * unit_width
    
    # First position with label
    svg_parts.append(f'<rect x="{x1 - 20}" y="{line_y - 5}" ')
    svg_parts.append('width="40" height="10" fill="#E3F2FD" stroke="#2196F3" stroke-width="2" rx="3"/>')
    
    fraction1_label = f"{data['numerator1']}/{data['denominator']}"
    svg_parts.append(f'<text x="{x1}" y="{line_y - 15}" ')
    svg_parts.append(f'text-anchor="middle" font-size="14" fill="#2196F3" font-weight="bold">{fraction1_label}</text>')
    
    # Result position
    if data['operation'] == 'add':
        fill_color = "#E3F2FD"
        stroke_color = "#2196F3"
    else:
        fill_color = "#FFEBEE"
        stroke_color = "#E91E63"
    
    svg_parts.append(f'<rect x="{x2 - 20}" y="{line_y - 5}" ')
    svg_parts.append(f'width="40" height="10" fill="{fill_color}" stroke="{stroke_color}" stroke-width="2" rx="3"/>')
    
    # Add question mark at result position
    svg_parts.append(f'<text x="{x2}" y="{line_y - 15}" ')
    svg_parts.append(f'text-anchor="middle" font-size="16" fill="{stroke_color}" font-weight="bold">?</text>')
    
    # Jump arc
    arc_height = 50
    
    if data['operation'] == 'add':
        # Forward arc for addition (left to right)
        jump_start = x1
        jump_end = x2
        jump_mid = (jump_start + jump_end) / 2
        arc_color = "#2196F3"
        marker = "url(#arrowhead-blue)"
        operation_symbol = "+"
        
        # Draw arc from left to right
        svg_parts.append(f'<path d="M {jump_start} {line_y - 10}')
        svg_parts.append(f' Q {jump_mid} {line_y - arc_height} ')
        svg_parts.append(f'{jump_end} {line_y - 10}" ')
        svg_parts.append(f'stroke="{arc_color}" stroke-width="3" fill="none" marker-end="{marker}"/>')
    else:
        # Backward arc for subtraction (right to left)
        jump_start = x1  # Starting position
        jump_end = x2    # Ending position (to the left)
        jump_mid = (jump_start + jump_end) / 2
        arc_color = "#E91E63"
        marker = "url(#arrowhead-pink)"
        operation_symbol = "−"
        
        # Draw arc from right to left (start at x1, end at x2)
        svg_parts.append(f'<path d="M {jump_start} {line_y - 10}')
        svg_parts.append(f' Q {jump_mid} {line_y - arc_height} ')
        svg_parts.append(f'{jump_end} {line_y - 10}" ')
        svg_parts.append(f'stroke="{arc_color}" stroke-width="3" fill="none" marker-end="{marker}"/>')
    
    # Label the jump
    jump_label = f"{operation_symbol}{data['numerator2']}/{data['denominator']}"
    svg_parts.append(f'<text x="{jump_mid}" y="{line_y - arc_height - 10}" ')
    svg_parts.append(f'text-anchor="middle" font-size="18" fill="{arc_color}" font-weight="bold">')
    svg_parts.append(f'{jump_label}</text>')
    
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
    
    # Display the equation to complete with a single form
    st.markdown("")
    
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
        
        with col1:
            # First fraction (display only)
            html = '<div style="text-align: center; padding: 15px; background-color: #f0f0f0; border-radius: 10px;">'
            html += '<div style="font-size: 24px; font-weight: bold;">'
            html += '<span style="border-bottom: 2px solid black; padding: 0 8px;">' + str(data['numerator1']) + '</span>'
            html += '<br>'
            html += '<span style="padding: 0 8px;">' + str(data['denominator']) + '</span>'
            html += '</div></div>'
            st.markdown(html, unsafe_allow_html=True)
        
        with col2:
            operation_symbol = "+" if data['operation'] == 'add' else "−"
            st.markdown(f"""
            <div style="text-align: center; font-size: 28px; padding-top: 25px;">
                {operation_symbol}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Second fraction with input
            numerator2_input = st.text_input(
                "",
                key="numerator2_input",
                placeholder="?",
                label_visibility="collapsed"
            )
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; font-weight: bold; margin-top: -10px;">
                <div style="border-top: 2px solid black; padding: 0 8px;">{data['denominator']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="text-align: center; font-size: 28px; padding-top: 25px;">
                =
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # Result input
            result_input = st.text_input(
                "",
                key="result_input",
                placeholder=f"?/{data['denominator']}",
                label_visibility="collapsed"
            )
        
        # Submit button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit:
                process_answer()
    
    # Show feedback
    handle_feedback_and_next()

def process_answer():
    """Process the submitted answer"""
    data = st.session_state.question_data
    
    # Get inputs
    numerator2_input = st.session_state.get('numerator2_input', '').strip()
    result_input = st.session_state.get('result_input', '').strip()
    
    if not numerator2_input or not result_input:
        st.error("Please fill in both blanks")
        return
    
    try:
        # Parse inputs
        user_num2 = int(numerator2_input)
        
        # Parse result
        if '/' in result_input:
            parts = result_input.split('/')
            user_result_num = int(parts[0])
            user_result_denom = int(parts[1])
            
            if user_result_denom != data['denominator']:
                st.error(f"The denominator should be {data['denominator']}")
                return
        else:
            user_result_num = int(result_input)
        
        # Check if second fraction is correct
        if user_num2 != data['numerator2']:
            st.error(f"The second fraction should be {data['numerator2']}/{data['denominator']}")
            return
        
        # Check if result is correct
        st.session_state.user_answer = user_result_num
        st.session_state.answer_submitted = True
        st.session_state.show_feedback = True
        
    except ValueError:
        st.error("Please enter valid numbers")

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
        operation_symbol = "+" if data['operation'] == 'add' else "−"
        
        st.success(f"✓ {fraction1} {operation_symbol} {fraction2} = {result}")
        
        # Show visual explanation
        with st.expander("🎯 **How the number line shows the answer**", expanded=True):
            if data['operation'] == 'add':
                st.markdown(f"""
                **Visual explanation:**
                - You started at {fraction1} on the number line
                - You jumped {fraction2} to the RIGHT (addition)
                - You landed at {result}
                
                The blue arc shows addition - jumping forward!
                """)
            else:
                st.markdown(f"""
                **Visual explanation:**
                - You started at {fraction1} on the number line
                - You jumped {fraction2} to the LEFT (subtraction)
                - You landed at {result}
                
                The pink arc shows subtraction - jumping backward!
                """)
        
        # Check special cases
        if correct_answer == data['denominator']:
            st.info("💡 **Special note:** Your answer equals 1 whole!")
        elif correct_answer == 0:
            st.info("💡 **Special note:** Your answer is 0!")
        
        # Increase difficulty
        old_difficulty = st.session_state.add_subtract_numberline_difficulty
        st.session_state.add_subtract_numberline_difficulty = min(
            st.session_state.add_subtract_numberline_difficulty + 1, 5
        )
        
        if st.session_state.add_subtract_numberline_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered adding and subtracting fractions with number lines!**")
        elif old_difficulty < st.session_state.add_subtract_numberline_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.add_subtract_numberline_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.add_subtract_numberline_difficulty
        st.session_state.add_subtract_numberline_difficulty = max(
            st.session_state.add_subtract_numberline_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.add_subtract_numberline_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.add_subtract_numberline_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the current problem"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Number Lines**", expanded=True):
        operation_name = "Addition" if data['operation'] == 'add' else "Subtraction"
        operation_symbol = "+" if data['operation'] == 'add' else "−"
        
        st.markdown(f"""
        ### {operation_name} on a Number Line
        
        **Your problem:**
        {data['numerator1']}/{data['denominator']} {operation_symbol} {data['numerator2']}/{data['denominator']} = ?
        
        **Step 1: Find your starting point**
        - Look for the first fraction: {data['numerator1']}/{data['denominator']}
        
        **Step 2: See the jump**
        - The arc shows {operation_symbol}{data['numerator2']}/{data['denominator']}
        """)
        
        if data['operation'] == 'add':
            st.markdown(f"""
        - This means jump {data['numerator2']} spaces to the RIGHT
        
        **Step 3: Find where you land**
        - {data['numerator1']} + {data['numerator2']} = {data['result']}
        - You land at {data['result']}/{data['denominator']}
        
        **Remember:** Addition = Jump RIGHT (forward) ➡️
        """)
        else:
            st.markdown(f"""
        - This means jump {data['numerator2']} spaces to the LEFT
        
        **Step 3: Find where you land**
        - {data['numerator1']} − {data['numerator2']} = {data['result']}
        - You land at {data['result']}/{data['denominator']}
        
        **Remember:** Subtraction = Jump LEFT (backward) ⬅️
        """)
        
        st.markdown(f"""
        **Answer: {data['result']}/{data['denominator']}**
        
        ### Visual Clues:
        - 🔵 Blue = Addition (forward)
        - 🔴 Pink = Subtraction (backward)
        - The denominator always stays {data['denominator']}
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