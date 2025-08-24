import streamlit as st
import random

def run():
    """
    Main function to run the Unit fractions on number lines activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/unit_fractions_on_number_lines.py
    """
    # Initialize session state
    if "number_line_problem" not in st.session_state:
        st.session_state.number_line_problem = None
        st.session_state.number_line_submitted = False
        st.session_state.user_fraction_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📏 Unit Fractions on Number Lines")
    st.markdown("*Identify fractions shown on number lines*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.number_line_problem is None:
        st.session_state.number_line_problem = generate_number_line_problem()
        st.session_state.number_line_submitted = False
        st.session_state.user_fraction_answer = ""
    
    problem = st.session_state.number_line_problem
    
    # Display the question
    st.markdown("### 📝 What fraction does the number line show?")
    
    # Display the number line
    st.markdown(problem['svg'], unsafe_allow_html=True)
    
    # Input section
    st.markdown("**Use a forward slash ( / ) to separate the numerator and denominator.**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_fraction_answer,
            key="number_line_input",
            disabled=st.session_state.number_line_submitted,
            placeholder="e.g., 1/4",
            label_visibility="collapsed"
        )
        st.session_state.user_fraction_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.number_line_submitted):
            
            if st.session_state.user_fraction_answer.strip() == "":
                st.warning("⚠️ Please enter your answer as a fraction (e.g., 1/4).")
            else:
                st.session_state.number_line_submitted = True
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.number_line_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.number_line_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.number_line_problem = None
                st.session_state.number_line_submitted = False
                st.session_state.user_fraction_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Read Number Lines:
        1. **Start and End:** The line goes from 0 to 1
        2. **Divisions:** Count how many equal parts the line is divided into
        3. **Position:** Count which part the dot is on
        4. **Write the fraction:** position/total divisions
        
        ### Examples:
        - Line divided into 2 parts, dot at first mark → **1/2**
        - Line divided into 4 parts, dot at third mark → **3/4**
        - Line divided into 3 parts, dot at first mark → **1/3**
        
        ### Unit Fractions:
        - Unit fractions have 1 as the numerator (1/2, 1/3, 1/4, etc.)
        - They represent one equal part of a whole
        
        ### Tips:
        - **Count the divisions** between 0 and 1 carefully
        - **Count from 0** to find where the dot is
        - The denominator is the total number of equal parts
        """)

def generate_number_line_problem():
    """Generate a random number line problem"""
    # Choose denominator (number of divisions)
    # Include both unit fractions and non-unit fractions
    denominators = [2, 3, 4, 5, 6, 8, 10]
    denominator = random.choice(denominators)
    
    # For unit fractions focus, bias towards numerator = 1
    if random.random() < 0.6:  # 60% chance of unit fraction
        numerator = 1
    else:
        # Choose a random numerator less than denominator
        numerator = random.randint(1, denominator - 1)
    
    # Create the SVG
    svg = create_number_line_svg(denominator, numerator)
    
    return {
        'numerator': numerator,
        'denominator': denominator,
        'answer': f"{numerator}/{denominator}",
        'svg': svg,
        'is_unit_fraction': numerator == 1
    }

def create_number_line_svg(denominator, numerator):
    """Create an SVG of a number line from 0 to 1 with a marked fraction"""
    # Colors for the dot
    colors = ['#4CAF50', '#FF9800', '#2196F3', '#9C27B0', '#F44336', '#009688']
    dot_color = random.choice(colors)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 30px 0;">')
    svg_parts.append('<svg width="400" height="100" viewBox="0 0 400 100">')
    
    # Main line
    line_start_x = 40
    line_end_x = 360
    line_y = 50
    line_length = line_end_x - line_start_x
    
    # Draw main horizontal line
    svg_parts.append(f'<line x1="{line_start_x}" y1="{line_y}" x2="{line_end_x}" y2="{line_y}" '
                    f'stroke="black" stroke-width="2"/>')
    
    # Draw end markers (0 and 1)
    svg_parts.append(f'<line x1="{line_start_x}" y1="{line_y-10}" x2="{line_start_x}" y2="{line_y+10}" '
                    f'stroke="black" stroke-width="2"/>')
    svg_parts.append(f'<line x1="{line_end_x}" y1="{line_y-10}" x2="{line_end_x}" y2="{line_y+10}" '
                    f'stroke="black" stroke-width="2"/>')
    
    # Labels for 0 and 1
    svg_parts.append(f'<text x="{line_start_x}" y="{line_y+30}" text-anchor="middle" '
                    f'font-size="16" font-weight="bold">0</text>')
    svg_parts.append(f'<text x="{line_end_x}" y="{line_y+30}" text-anchor="middle" '
                    f'font-size="16" font-weight="bold">1</text>')
    
    # Draw division marks
    for i in range(1, denominator):
        x_pos = line_start_x + (i * line_length / denominator)
        # Make division marks smaller than end marks
        svg_parts.append(f'<line x1="{x_pos}" y1="{line_y-6}" x2="{x_pos}" y2="{line_y+6}" '
                        f'stroke="gray" stroke-width="1.5"/>')
    
    # Draw the dot at the fraction position
    dot_x = line_start_x + (numerator * line_length / denominator)
    svg_parts.append(f'<circle cx="{dot_x}" cy="{line_y}" r="8" fill="{dot_color}" '
                    f'stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.number_line_problem
    user_answer = st.session_state.user_fraction_answer.strip()
    
    # Parse user answer
    try:
        if '/' not in user_answer:
            st.error("❌ Please enter your answer as a fraction using / (e.g., 1/4)")
            return
        
        parts = user_answer.split('/')
        if len(parts) != 2:
            st.error("❌ Please use exactly one / to separate numerator and denominator")
            return
        
        user_num = int(parts[0].strip())
        user_den = int(parts[1].strip())
        
        # Check if fraction is valid
        if user_den == 0:
            st.error("❌ The denominator cannot be zero")
            return
        
        # Check if answer is correct
        correct_num = problem['numerator']
        correct_den = problem['denominator']
        
        # Check for exact match or equivalent fraction
        is_exact_match = (user_num == correct_num and user_den == correct_den)
        is_equivalent = (user_num * correct_den == correct_num * user_den)
        
        if is_exact_match:
            st.success(f"🎉 **Excellent! {user_answer} is correct!**")
            if problem['is_unit_fraction']:
                st.info("🌟 Great job identifying this unit fraction!")
            st.balloons()
            
        elif is_equivalent:
            st.success(f"🎉 **Correct! {user_answer} is equivalent to {problem['answer']}**")
            st.info(f"Both fractions equal {user_num/user_den:.3f}")
            
        else:
            st.error(f"❌ **Not quite right. The correct answer is {problem['answer']}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"""
                **Understanding the number line:**
                
                1. **Count the divisions:**
                   - The line from 0 to 1 is divided into **{correct_den} equal parts**
                   - This means each part represents **1/{correct_den}**
                
                2. **Find the position:**
                   - The dot is at the **{correct_num}** mark from 0
                   - This represents **{correct_num} parts out of {correct_den}**
                
                3. **Write the fraction:**
                   - Position: **{correct_num}**
                   - Total divisions: **{correct_den}**
                   - Fraction: **{correct_num}/{correct_den}**
                
                {"This is a **unit fraction** because the numerator is 1!" if problem['is_unit_fraction'] else ""}
                
                Your answer: {user_answer}
                """)
                
    except ValueError:
        st.error("❌ Please enter whole numbers for the numerator and denominator (e.g., 1/4)")
    except Exception as e:
        st.error("❌ Invalid input. Please enter your answer as a fraction (e.g., 1/4)")