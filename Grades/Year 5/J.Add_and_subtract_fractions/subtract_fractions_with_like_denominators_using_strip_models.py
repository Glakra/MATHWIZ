import streamlit as st
import random

def run():
    """
    Main function to run the Subtract Fractions with Strip Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/subtract_fractions_with_like_denominators_using_strip_models.py
    """
    # Initialize session state for difficulty and game state
    if "subtract_strips_difficulty" not in st.session_state:
        st.session_state.subtract_strips_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions Using Strip Models")
    st.markdown("*Use the fraction strips to help*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.subtract_strips_difficulty
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
        ### How to Use Fraction Strips:
        
        1. **Top strip** - Shows 1 whole for reference
        2. **Bottom strips** - Show your fraction divided into equal parts
        3. **Crossed out parts** - These are being subtracted (taken away)
        4. **Count remaining** - The parts NOT crossed out are your answer!
        
        ### Example:
        If you have 5/7 and subtract 2/7:
        - Start with 5 blue parts out of 7
        - Cross out 2 parts (subtract them)
        - Count what's left: 3 parts
        - Answer: 3/7
        
        ### Visual Tips:
        - 🟦 Blue parts = Parts you have
        - ❌ Crossed out = Parts taken away
        - ✓ Remaining = Your answer
        
        ### Remember:
        - Only the numerator changes
        - The denominator stays the same
        - Count the parts that are NOT crossed out
        """)

def generate_new_question():
    """Generate a new strip model subtraction question"""
    difficulty = st.session_state.subtract_strips_difficulty
    
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
    numerator1 = random.randint(2, denominator - 1)
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
    st.session_state.current_question = "Subtract. Use the fraction strips to help."

def create_fraction_strips_svg(data):
    """Create an SVG showing fraction strips with crossed out parts"""
    width = 600
    height = 180
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    # Draw the "1 whole" reference strip
    whole_y = 20
    whole_height = 40
    svg_parts.append(f'<rect x="50" y="{whole_y}" width="500" height="{whole_height}" ')
    svg_parts.append('fill="#FFE082" stroke="#333" stroke-width="2" rx="5"/>')
    
    # Label for "1"
    svg_parts.append(f'<text x="300" y="{whole_y + 25}" text-anchor="middle" ')
    svg_parts.append('font-size="20" font-weight="bold" fill="#333">1</text>')
    
    # Draw the fraction strips
    strip_y = 90
    strip_height = 60
    strip_width = 500 / data['denominator']
    
    # Draw each fraction part
    for i in range(data['denominator']):
        x = 50 + i * strip_width
        
        # Determine if this part should be filled or crossed out
        if i < data['numerator1']:
            # This is part of the original fraction
            fill_color = "#90CAF9"  # Light blue
            
            # Draw the rectangle
            svg_parts.append(f'<rect x="{x}" y="{strip_y}" width="{strip_width}" height="{strip_height}" ')
            svg_parts.append(f'fill="{fill_color}" stroke="#333" stroke-width="2"/>')
            
            # Add fraction label
            label_y = strip_y + strip_height/2 + 5
            svg_parts.append(f'<text x="{x + strip_width/2}" y="{label_y}" text-anchor="middle" ')
            svg_parts.append(f'font-size="16" fill="#333">1/{data["denominator"]}</text>')
            
            # Add crossing out for parts being subtracted
            if i >= data['numerator1'] - data['numerator2']:
                # Draw diagonal lines to cross out
                svg_parts.append(f'<line x1="{x + 5}" y1="{strip_y + 5}" ')
                svg_parts.append(f'x2="{x + strip_width - 5}" y2="{strip_y + strip_height - 5}" ')
                svg_parts.append('stroke="#FF0000" stroke-width="3"/>')
                
                svg_parts.append(f'<line x1="{x + strip_width - 5}" y1="{strip_y + 5}" ')
                svg_parts.append(f'x2="{x + 5}" y2="{strip_y + strip_height - 5}" ')
                svg_parts.append('stroke="#FF0000" stroke-width="3"/>')
        else:
            # Empty part (not part of the original fraction)
            svg_parts.append(f'<rect x="{x}" y="{strip_y}" width="{strip_width}" height="{strip_height}" ')
            svg_parts.append('fill="white" stroke="#333" stroke-width="2"/>')
            
            # Add fraction label
            label_y = strip_y + strip_height/2 + 5
            svg_parts.append(f'<text x="{x + strip_width/2}" y="{label_y}" text-anchor="middle" ')
            svg_parts.append(f'font-size="16" fill="#999">1/{data["denominator"]}</text>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display instruction
    st.markdown("### Subtract. Use the fraction strips to help.")
    
    # Display the fraction strips
    strips_svg = create_fraction_strips_svg(data)
    st.markdown(strips_svg, unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("")
    
    # Display the equation
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
    
    with col1:
        # First fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 36px; line-height: 1;">
            <div style="border-bottom: 2px solid black; padding: 3px;">{data['numerator1']}</div>
            <div style="padding: 3px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 15px;">
            −
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        fraction_html = f"""
        <div style="text-align: center; font-size: 36px; line-height: 1;">
            <div style="border-bottom: 2px solid black; padding: 3px;">{data['numerator2']}</div>
            <div style="padding: 3px;">{data['denominator']}</div>
        </div>
        """
        st.markdown(fraction_html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 15px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Answer input
        with st.form("answer_form", clear_on_submit=False):
            user_input = st.text_input(
                "",
                key="fraction_answer",
                placeholder=f"?/{data['denominator']}",
                label_visibility="collapsed"
            )
            
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
            
            if submit and user_input.strip():
                # Parse the answer
                if '/' in user_input:
                    try:
                        parts = user_input.split('/')
                        user_num = int(parts[0])
                        user_denom = int(parts[1])
                        
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
        st.success("🎉 **Correct! Excellent work!**")
        
        # Show the complete equation
        st.success(f"✓ {data['numerator1']}/{data['denominator']} − {data['numerator2']}/{data['denominator']} = {correct_answer}/{data['denominator']}")
        
        # Visual explanation
        with st.expander("🎯 **How the strips show the answer**", expanded=True):
            st.markdown(f"""
            **Understanding the visual:**
            - You started with {data['numerator1']} blue parts
            - {data['numerator2']} parts were crossed out (subtracted)
            - {correct_answer} parts remain not crossed out
            
            The fraction strips make it easy to see subtraction as "crossing out" parts!
            """)
        
        # Check for simplified form
        if correct_answer == 0:
            st.info("💡 **Note:** When you subtract all the parts, you get 0!")
        
        # Increase difficulty
        old_difficulty = st.session_state.subtract_strips_difficulty
        st.session_state.subtract_strips_difficulty = min(
            st.session_state.subtract_strips_difficulty + 1, 5
        )
        
        if st.session_state.subtract_strips_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered subtracting with fraction strips!**")
        elif old_difficulty < st.session_state.subtract_strips_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.subtract_strips_difficulty}**")
    
    else:
        st.error("❌ **Not quite right. Let's try again!**")
        
        # Show what they entered
        st.error(f"You answered: {user_answer}/{data['denominator']}")
        
        # Show correct answer
        st.success(f"The correct answer is: {correct_answer}/{data['denominator']}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.subtract_strips_difficulty
        st.session_state.subtract_strips_difficulty = max(
            st.session_state.subtract_strips_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.subtract_strips_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.subtract_strips_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for subtracting with strip models"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Subtraction with Strips**", expanded=True):
        st.markdown(f"""
        ### Your Problem:
        **{data['numerator1']}/{data['denominator']} − {data['numerator2']}/{data['denominator']} = ?**
        
        ### How to Read the Strips:
        
        **Step 1: Count the original amount**
        - Look at the blue parts: {data['numerator1']} parts
        - This represents {data['numerator1']}/{data['denominator']}
        
        **Step 2: See what's being subtracted**
        - The crossed out parts (❌) show what to take away
        - {data['numerator2']} parts are crossed out
        
        **Step 3: Count what remains**
        - Count the blue parts that are NOT crossed out
        - {data['numerator1']} total − {data['numerator2']} crossed out = {data['diff_numerator']} remaining
        
        **Answer: {data['diff_numerator']}/{data['denominator']}**
        
        ### Visual Guide:
        - 🟨 Yellow strip = 1 whole (reference)
        - 🟦 Blue parts = Your starting fraction
        - ❌ Red crosses = Parts being subtracted
        - ✓ Remaining blue = Your answer
        
        ### Remember:
        - The strips are divided into {data['denominator']} equal parts
        - Only count the parts that aren't crossed out
        - The denominator never changes!
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