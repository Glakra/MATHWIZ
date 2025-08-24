import streamlit as st
import random
import streamlit.components.v1 as components

def run():
    """
    Main function to run the Compare Decimals on Number Lines practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimals_number_lines.py
    """
    # Initialize session state for difficulty and game state
    if "number_lines_difficulty" not in st.session_state:
        st.session_state.number_lines_difficulty = 1  # Start with 0-1 range
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_option = None
        st.session_state.plotting_complete = False
        st.session_state.plotted_points = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📏 Compare Decimals on Number Lines")
    st.markdown("*Plot decimals on number lines and compare their positions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.number_lines_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "0 to 1 (tenths)",
            2: "0 to 1 (hundredths)", 
            3: "0 to 10 range",
            4: "Mixed ranges",
            5: "Advanced plotting"
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
        - **Read the instruction** to see which decimals to plot
        - **Use the interactive number line** below to place points
        - **Click on the number line** where each decimal should go
        - **Answer the comparison question** after plotting
        
        ### Plotting on Number Lines:
        - **Each tick mark** represents a specific decimal value
        - **Count carefully** from 0.0 to find the right position
        - **Click exactly** where the decimal should be placed
        - **Watch for the colored dots** showing your plotted points
        
        ### Reading Number Lines:
        - **0 to 1 with tenths:** Each tick = 0.1 (0.1, 0.2, 0.3...)
        - **0 to 1 with hundredths:** Smaller divisions for precision
        - **0 to 10:** Each tick = 1.0 or smaller divisions
        
        ### Comparison Questions:
        - **"Which is closer to 0?"** - Find the smaller number
        - **"Which is greater?"** - Find the larger number
        - **"Which is in between?"** - Find the middle value
        - **Use the number line** to see the distances visually
        
        ### Examples:
        - **Plot 0.2 and 0.8:** 0.2 is closer to 0, 0.8 is closer to 1
        - **Plot 0.3 and 0.7:** Both are same distance from 0.5
        - **Plot 2.5 and 7.5:** 7.5 is greater than 2.5
        
        ### Tips for Success:
        - **Count tick marks carefully** from the starting point
        - **Use the visual spacing** to estimate positions
        - **Think about place value** - 0.25 is between 0.2 and 0.3
        - **Check your plots** before answering the question
        
        ### Difficulty Levels:
        - **🟡 Level 1:** 0-1 range, tenths only
        - **🟡 Level 2:** 0-1 range, hundredths
        - **🟠 Level 3:** 0-10 range with decimals
        - **🔴 Level 4:** Mixed ranges and scales
        - **🔴 Level 5:** Advanced decimal plotting
        
        ### Scoring:
        - ✅ **Correct plotting + answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all number line levels!
        """)

def generate_new_question():
    """Generate a new number line comparison question based on difficulty level"""
    difficulty = st.session_state.number_lines_difficulty
    
    if difficulty == 1:
        # 0 to 1 range, tenths
        decimals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        decimal1, decimal2 = random.sample(decimals, 2)
        number_line_range = (0, 1, 0.1)
        comparison_questions = [
            f"Which number is closer to 0?",
            f"Which number is closer to 1?", 
            f"Which number is greater?",
            f"Which number is smaller?"
        ]
        
    elif difficulty == 2:
        # 0 to 1 range, hundredths
        decimals = [round(i * 0.05, 2) for i in range(1, 20)]  # 0.05, 0.10, 0.15... 0.95
        decimal1, decimal2 = random.sample(decimals, 2)
        number_line_range = (0, 1, 0.05)
        comparison_questions = [
            f"Which number is closer to 0?",
            f"Which number is closer to 1?",
            f"Which number is greater?",
            f"Which number is smaller?"
        ]
        
    elif difficulty == 3:
        # 0 to 10 range
        decimals = [round(i * 0.5, 1) for i in range(1, 20)]  # 0.5, 1.0, 1.5... 9.5
        decimal1, decimal2 = random.sample(decimals, 2)
        number_line_range = (0, 10, 0.5)
        comparison_questions = [
            f"Which number is closer to 0?",
            f"Which number is closer to 10?",
            f"Which number is greater?",
            f"Which number is smaller?"
        ]
        
    elif difficulty == 4:
        # Mixed ranges
        ranges = [
            (0, 2, 0.1, [0.2, 0.4, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8]),
            (0, 5, 0.25, [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]),
            (1, 3, 0.1, [1.2, 1.4, 1.6, 1.8, 2.2, 2.4, 2.6, 2.8])
        ]
        start, end, step, decimals = random.choice(ranges)
        decimal1, decimal2 = random.sample(decimals, 2)
        number_line_range = (start, end, step)
        comparison_questions = [
            f"Which number is closer to {start}?",
            f"Which number is closer to {end}?",
            f"Which number is greater?",
            f"Which number is smaller?"
        ]
        
    else:  # difficulty == 5
        # Advanced plotting
        ranges = [
            (0, 1, 0.02, [round(i * 0.02, 2) for i in range(1, 50)]),
            (0, 3, 0.15, [round(i * 0.15, 2) for i in range(1, 20)]),
            (2, 5, 0.25, [round(2 + i * 0.25, 2) for i in range(1, 12)])
        ]
        start, end, step, decimals = random.choice(ranges)
        decimal1, decimal2 = random.sample(decimals, 2)
        number_line_range = (start, end, step)
        comparison_questions = [
            f"Which number is closer to {start}?",
            f"Which number is closer to {end}?",
            f"Which number is greater?",
            f"Which number is smaller?",
            f"Which number is closer to the middle?"
        ]
    
    # Choose a comparison question
    comparison_question = random.choice(comparison_questions)
    
    # Determine correct answer based on question type
    if "closer to 0" in comparison_question or "closer to" in comparison_question and str(number_line_range[0]) in comparison_question:
        correct_answer = min(decimal1, decimal2)
    elif "closer to 1" in comparison_question or "closer to 10" in comparison_question or "closer to" in comparison_question:
        if "closer to 1" in comparison_question:
            correct_answer = decimal1 if abs(decimal1 - 1) < abs(decimal2 - 1) else decimal2
        elif "closer to 10" in comparison_question:
            correct_answer = decimal1 if abs(decimal1 - 10) < abs(decimal2 - 10) else decimal2
        else:
            # Extract the target number from the question
            target = number_line_range[1]
            correct_answer = decimal1 if abs(decimal1 - target) < abs(decimal2 - target) else decimal2
    elif "greater" in comparison_question:
        correct_answer = max(decimal1, decimal2)
    elif "smaller" in comparison_question:
        correct_answer = min(decimal1, decimal2)
    elif "middle" in comparison_question:
        middle = (number_line_range[0] + number_line_range[1]) / 2
        correct_answer = decimal1 if abs(decimal1 - middle) < abs(decimal2 - middle) else decimal2
    
    # Store question data
    st.session_state.question_data = {
        "decimal1": decimal1,
        "decimal2": decimal2,
        "number_line_range": number_line_range,
        "comparison_question": comparison_question
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Graph {decimal1} and {decimal2} on the number line."

def create_interactive_number_line(start, end, step):
    """Create an interactive number line using SVG for better rendering"""
    
    # Calculate number of divisions
    num_divisions = int((end - start) / step)
    
    # SVG dimensions
    width = 700
    height = 150
    margin = 50
    line_width = width - 2 * margin
    
    # Create SVG content
    svg_content = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="background-color: white;">
        <!-- Main line -->
        <line x1="{margin}" y1="75" x2="{margin + line_width}" y2="75" stroke="#333" stroke-width="3"/>
        
        <!-- Arrow -->
        <polygon points="{margin + line_width},{75} {margin + line_width - 10},{70} {margin + line_width - 10},{80}" fill="#333"/>
    """
    
    # Add tick marks and labels
    for i in range(num_divisions + 1):
        x_pos = margin + (i * line_width / num_divisions)
        value = round(start + (i * step), 3)
        
        # Major tick marks
        svg_content += f'<line x1="{x_pos}" y1="65" x2="{x_pos}" y2="85" stroke="#333" stroke-width="2"/>'
        
        # Labels
        svg_content += f'<text x="{x_pos}" y="105" text-anchor="middle" font-size="14" fill="#333">{value}</text>'
        
        # Clickable areas
        svg_content += f'<rect x="{x_pos-10}" y="55" width="20" height="40" fill="transparent" stroke="none" style="cursor: pointer;" onclick="plotPoint({value}, {x_pos})"/>'
    
    svg_content += "</svg>"
    
    # Create the complete HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .container {{
                text-align: center;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            #instructions {{
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }}
            #feedback {{
                font-size: 14px;
                margin-top: 15px;
                padding: 10px;
                border-radius: 5px;
            }}
            .plotted-point {{
                fill: #ff4444;
                stroke: white;
                stroke-width: 2;
            }}
            .plotted-point.point2 {{
                fill: #4444ff;
            }}
            svg {{
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div id="instructions">Click on the number line to plot {st.session_state.question_data['decimal1']} and {st.session_state.question_data['decimal2']}</div>
            <div id="number-line-svg">
                {svg_content}
            </div>
            <div id="feedback"></div>
        </div>
        
        <script>
            let targetPoints = [{st.session_state.question_data['decimal1']}, {st.session_state.question_data['decimal2']}];
            let currentPointIndex = 0;
            let plotted = [];
            
            function plotPoint(value, xPos) {{
                if (currentPointIndex >= 2) {{
                    document.getElementById('feedback').innerHTML = '<div style="color: orange; background-color: #fff3cd; padding: 5px;">Both points already plotted! Click "Continue" below.</div>';
                    return;
                }}
                
                let targetValue = targetPoints[currentPointIndex];
                let tolerance = {step / 2};
                
                if (Math.abs(value - targetValue) <= tolerance) {{
                    // Remove any existing point for this index
                    let existingPoint = document.getElementById('point-' + currentPointIndex);
                    if (existingPoint) existingPoint.remove();
                    
                    // Add the point to SVG
                    let svg = document.querySelector('svg');
                    let point = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    point.setAttribute('cx', xPos);
                    point.setAttribute('cy', '75');
                    point.setAttribute('r', '6');
                    point.setAttribute('class', currentPointIndex === 0 ? 'plotted-point' : 'plotted-point point2');
                    point.setAttribute('id', 'point-' + currentPointIndex);
                    svg.appendChild(point);
                    
                    plotted.push(targetValue);
                    currentPointIndex++;
                    
                    if (currentPointIndex === 1) {{
                        document.getElementById('feedback').innerHTML = '<div style="color: green; background-color: #d4edda; padding: 5px;">✓ Good! Now plot ' + targetPoints[1] + '</div>';
                    }} else {{
                        document.getElementById('feedback').innerHTML = '<div style="color: green; background-color: #d4edda; padding: 5px;">✓ Excellent! Both points plotted correctly. Click "Continue" below.</div>';
                    }}
                }} else {{
                    document.getElementById('feedback').innerHTML = '<div style="color: red; background-color: #f8d7da; padding: 5px;">Try again! Click closer to ' + targetValue + '</div>';
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the plotting instruction
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
    
    # Create and display the interactive number line
    if not st.session_state.plotting_complete:
        start, end, step = data["number_line_range"]
        number_line_html = create_interactive_number_line(start, end, step)
        components.html(number_line_html, height=200)
        
        # Continue button (appears after plotting)
        if st.button("✅ Continue to Question", type="primary"):
            st.session_state.plotting_complete = True
            st.rerun()
    
    else:
        # Show the comparison question and answer options
        st.markdown("### " + data["comparison_question"])
        
        # Display answer options
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button(f"{data['decimal1']}", key="option_1", use_container_width=True,
                        disabled=st.session_state.answer_submitted):
                st.session_state.selected_option = data['decimal1']
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        
        with col2:
            if st.button(f"{data['decimal2']}", key="option_2", use_container_width=True,
                        disabled=st.session_state.answer_submitted):
                st.session_state.selected_option = data['decimal2']
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        
        # Show selected answer
        if st.session_state.selected_option:
            st.markdown(f"**Your answer:** {st.session_state.selected_option}")
        
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
    user_answer = st.session_state.selected_option
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.number_lines_difficulty
        st.session_state.number_lines_difficulty = min(
            st.session_state.number_lines_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.number_lines_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered number line comparisons!**")
        elif old_difficulty < st.session_state.number_lines_difficulty:
            difficulty_names = {
                2: "hundredths on number lines",
                3: "0-10 range plotting", 
                4: "mixed range number lines",
                5: "advanced decimal plotting"
            }
            next_level = difficulty_names.get(st.session_state.number_lines_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    decimal1 = data["decimal1"]
    decimal2 = data["decimal2"]
    comparison_question = data["comparison_question"]
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution:
        
        **Plotted numbers:** {decimal1} and {decimal2}
        **Question:** {comparison_question}
        **Correct answer:** {correct_answer}
        
        ### Using the number line:
        """)
        
        # Explain based on question type
        if "closer to 0" in comparison_question:
            st.markdown(f"""
            - **{decimal1}** is {decimal1} units from 0
            - **{decimal2}** is {decimal2} units from 0
            - **{correct_answer}** is closer to 0 because it's the smaller number
            """)
        elif "closer to 1" in comparison_question:
            dist1 = abs(decimal1 - 1)
            dist2 = abs(decimal2 - 1)
            st.markdown(f"""
            - **{decimal1}** is {dist1} units from 1
            - **{decimal2}** is {dist2} units from 1
            - **{correct_answer}** is closer to 1
            """)
        elif "greater" in comparison_question:
            st.markdown(f"""
            - **{decimal1}** vs **{decimal2}**
            - **{correct_answer}** is further right on the number line
            - **Further right = greater value**
            """)
        elif "smaller" in comparison_question:
            st.markdown(f"""
            - **{decimal1}** vs **{decimal2}**
            - **{correct_answer}** is further left on the number line
            - **Further left = smaller value**
            """)
        
        st.markdown("""
        ### 💡 Number line tips:
        - **Left to right** = smaller to larger
        - **Distance from points** shows how close numbers are
        - **Visual spacing** helps compare decimal values
        - **Practice plotting** helps build number sense!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_option = None
    st.session_state.plotting_complete = False
    st.session_state.plotted_points = {}