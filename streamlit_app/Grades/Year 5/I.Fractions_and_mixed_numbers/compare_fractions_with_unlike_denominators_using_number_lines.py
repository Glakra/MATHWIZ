import streamlit as st
import random

def run():
    """
    Main function to run the Compare Fractions with Unlike Denominators Using Number Lines activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/compare_fractions_with_unlike_denominators_using_number_lines.py
    """
    # Initialize session state
    if "number_line_score" not in st.session_state:
        st.session_state.number_line_score = 0
        st.session_state.number_line_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.selected_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📏 Compare Fractions with Unlike Denominators Using Number Lines")
    st.markdown("*Use number lines to compare fractions with different denominators*")
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.session_state.number_line_attempts > 0:
            accuracy = (st.session_state.number_line_score / st.session_state.number_line_attempts) * 100
            st.metric("Score", f"{st.session_state.number_line_score}/{st.session_state.number_line_attempts}", 
                     f"{accuracy:.0f}%")
        else:
            st.metric("Score", "0/0", "Start practicing!")
    
    with col3:
        # Back button
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
        ### How to Play:
        - **Look at the two number lines** showing different fractions
        - **Compare the positions** of the colored dots
        - **Click on the fraction** that answers the question
        - **Submit your answer** to check if you're correct
        
        ### Understanding Number Lines:
        - **0 to 1:** All proper fractions are between 0 and 1
        - **Tick marks:** Show equal divisions based on the denominator
        - **Colored dots:** Show where each fraction is located
        - **Further right = larger:** The dot further to the right is the larger fraction
        
        ### Tips for Success:
        - **Look at position:** Which dot is closer to 1?
        - **Compare to 1/2:** Is each fraction more or less than halfway?
        - **Equal fractions:** Sometimes different fractions are at the same spot!
        - **Visual comparison:** You don't need to calculate - just look!
        
        ### Examples:
        - **1/2 vs 3/8:** 1/2 is at the halfway point, 3/8 is to the left
        - **2/3 vs 3/4:** Both are past halfway, but 3/4 is further right
        - **2/4 vs 1/2:** These are at the same position (they're equal!)
        
        ### Remember:
        - **Right = larger:** The fraction further right is larger
        - **Left = smaller:** The fraction further left is smaller
        - **Same position = equal:** Fractions at the same spot are equivalent
        """)

def generate_new_problem():
    """Generate a new fraction comparison problem with number lines"""
    
    problems = [
        # Basic comparisons
        {
            "fraction1": (1, 2),
            "fraction2": (2, 4),
            "question": "Which fraction is greater?",
            "correct_answer": "equal",  # They are equal
            "explanation": "1/2 and 2/4 are at the same position - they are equal!"
        },
        {
            "fraction1": (1, 3),
            "fraction2": (1, 6),
            "question": "Which fraction is greater?",
            "correct_answer": (1, 3),
            "explanation": "1/3 is further right on the number line than 1/6"
        },
        {
            "fraction1": (2, 3),
            "fraction2": (3, 4),
            "question": "Which fraction is less?",
            "correct_answer": (2, 3),
            "explanation": "2/3 is further left on the number line than 3/4"
        },
        {
            "fraction1": (3, 5),
            "fraction2": (5, 8),
            "question": "Which fraction is less?",
            "correct_answer": (3, 5),
            "explanation": "3/5 (0.6) is less than 5/8 (0.625)"
        },
        {
            "fraction1": (5, 8),
            "fraction2": (1, 2),
            "question": "Which fraction is greater?",
            "correct_answer": (5, 8),
            "explanation": "5/8 is further right than 1/2 (which is 4/8)"
        },
        {
            "fraction1": (2, 5),
            "fraction2": (3, 10),
            "question": "Which fraction is greater?",
            "correct_answer": (2, 5),
            "explanation": "2/5 (4/10) is greater than 3/10"
        },
        {
            "fraction1": (3, 4),
            "fraction2": (2, 3),
            "question": "Which fraction is greater?",
            "correct_answer": (3, 4),
            "explanation": "3/4 is further right on the number line than 2/3"
        },
        {
            "fraction1": (1, 4),
            "fraction2": (2, 8),
            "question": "Which fraction is less?",
            "correct_answer": "equal",
            "explanation": "1/4 and 2/8 are at the same position - they are equal!"
        },
        {
            "fraction1": (4, 6),
            "fraction2": (2, 3),
            "question": "Which fraction is greater?",
            "correct_answer": "equal",
            "explanation": "4/6 and 2/3 are at the same position - they are equal!"
        },
        {
            "fraction1": (1, 4),
            "fraction2": (3, 8),
            "question": "Which fraction is less?",
            "correct_answer": (1, 4),
            "explanation": "1/4 (2/8) is less than 3/8"
        },
        {
            "fraction1": (2, 5),
            "fraction2": (1, 2),
            "question": "Which fraction is less?",
            "correct_answer": (2, 5),
            "explanation": "2/5 is less than 1/2 (which is 2.5/5)"
        },
        {
            "fraction1": (5, 6),
            "fraction2": (7, 8),
            "question": "Which fraction is less?",
            "correct_answer": (5, 6),
            "explanation": "5/6 is less than 7/8 (both are close to 1, but 7/8 is closer)"
        },
        {
            "fraction1": (3, 10),
            "fraction2": (1, 3),
            "question": "Which fraction is less?",
            "correct_answer": (3, 10),
            "explanation": "3/10 (0.3) is less than 1/3 (approximately 0.33)"
        },
        {
            "fraction1": (4, 5),
            "fraction2": (3, 4),
            "question": "Which fraction is greater?",
            "correct_answer": (4, 5),
            "explanation": "4/5 (0.8) is greater than 3/4 (0.75)"
        },
        {
            "fraction1": (1, 6),
            "fraction2": (1, 4),
            "question": "Which fraction is less?",
            "correct_answer": (1, 6),
            "explanation": "1/6 is further left on the number line than 1/4"
        }
    ]
    
    st.session_state.current_problem = random.choice(problems)
    st.session_state.selected_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def create_number_line_svg(numerator, denominator, color, position="top"):
    """Create SVG number line with fraction marked"""
    
    # SVG dimensions
    width = 600
    height = 80
    margin = 50
    line_y = 40 if position == "top" else 40
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    
    # Draw main line with arrows
    svg_parts.append(f'<line x1="{margin - 30}" y1="{line_y}" x2="{width - margin + 30}" y2="{line_y}" stroke="gray" stroke-width="2"/>')
    svg_parts.append(f'<path d="M {margin - 35} {line_y} L {margin - 30} {line_y - 5} L {margin - 30} {line_y + 5} Z" fill="gray"/>')
    svg_parts.append(f'<path d="M {width - margin + 35} {line_y} L {width - margin + 30} {line_y - 5} L {width - margin + 30} {line_y + 5} Z" fill="gray"/>')
    
    # Calculate line length
    line_length = width - 2 * margin
    
    # Draw tick marks and labels for the denominator
    for i in range(denominator + 1):
        x = margin + (i / denominator) * line_length
        
        # Main tick marks at 0 and 1
        if i == 0 or i == denominator:
            svg_parts.append(f'<line x1="{x}" y1="{line_y - 10}" x2="{x}" y2="{line_y + 10}" stroke="black" stroke-width="2"/>')
            label = "0" if i == 0 else "1"
            svg_parts.append(f'<text x="{x}" y="{line_y + 25}" text-anchor="middle" font-size="14" font-weight="bold">{label}</text>')
        else:
            # Smaller tick marks for fractions
            svg_parts.append(f'<line x1="{x}" y1="{line_y - 8}" x2="{x}" y2="{line_y + 8}" stroke="black" stroke-width="1"/>')
            # Add fraction labels
            svg_parts.append(f'<text x="{x}" y="{line_y + 25}" text-anchor="middle" font-size="12">{i}/{denominator}</text>')
    
    # Mark the fraction position with a colored dot
    frac_x = margin + (numerator / denominator) * line_length
    svg_parts.append(f'<circle cx="{frac_x}" cy="{line_y}" r="8" fill="{color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def display_problem():
    """Display the current number line comparison problem"""
    
    problem = st.session_state.current_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Get fractions
    frac1 = problem['fraction1']
    frac2 = problem['fraction2']
    
    # Choose colors for the dots
    color1 = "#FFC107"  # Yellow/Orange
    color2 = "#9C27B0"  # Purple
    
    # Create and display number lines
    svg1 = create_number_line_svg(frac1[0], frac1[1], color1, "top")
    svg2 = create_number_line_svg(frac2[0], frac2[1], color2, "bottom")
    
    # Display both number lines
    st.markdown(f'<div style="margin: 20px 0;">{svg1}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin: 20px 0;">{svg2}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create clickable options
    if problem['correct_answer'] == "equal":
        # Three options: fraction1, fraction2, "they are equal"
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"{frac1[0]}/{frac1[1]}", key="frac1_btn", 
                        type="primary" if st.session_state.selected_answer == frac1 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac1
                st.rerun()
        
        with col2:
            if st.button(f"{frac2[0]}/{frac2[1]}", key="frac2_btn",
                        type="primary" if st.session_state.selected_answer == frac2 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac2
                st.rerun()
        
        with col3:
            # Determine the button text based on the question
            if "greater" in problem['question']:
                equal_text = "neither; they are equal"
            else:  # "less" in question
                equal_text = "neither; they are equal"
            
            if st.button(equal_text, key="equal_btn",
                        type="primary" if st.session_state.selected_answer == "equal" else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = "equal"
                st.rerun()
    else:
        # Two options: just the fractions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"{frac1[0]}/{frac1[1]}", key="frac1_btn", 
                        type="primary" if st.session_state.selected_answer == frac1 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac1
                st.rerun()
        
        with col2:
            if st.button(f"{frac2[0]}/{frac2[1]}", key="frac2_btn",
                        type="primary" if st.session_state.selected_answer == frac2 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac2
                st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True, 
                    disabled=st.session_state.answer_submitted):
            if st.session_state.selected_answer:
                check_answer()
            else:
                st.warning("Please select an answer before submitting!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.current_problem = None
                st.rerun()

def check_answer():
    """Check if the selected answer is correct"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    st.session_state.answer_submitted = True
    st.session_state.number_line_attempts += 1
    
    if st.session_state.selected_answer == correct_answer:
        st.session_state.number_line_score += 1
    
    st.session_state.show_feedback = True

def show_feedback():
    """Display feedback for the submitted answer"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    if st.session_state.selected_answer == correct_answer:
        st.success(f"🎉 **Correct! {problem['explanation']}**")
        
        # Add visual celebration for streaks
        if st.session_state.number_line_score % 5 == 0:
            st.balloons()
    else:
        if correct_answer == "equal":
            st.error(f"❌ **Not quite. The fractions are equal!**")
        else:
            st.error(f"❌ **Not quite. The correct answer is {correct_answer[0]}/{correct_answer[1]}**")
        st.info(f"💡 **{problem['explanation']}**")
        
        # Additional tips
        with st.expander("📚 **Learn More**", expanded=True):
            st.markdown("""
            ### How to Use Number Lines:
            
            1. **Look at the positions** - Which dot is further to the right?
            2. **Compare to benchmarks** - Where is 1/2? Where is each fraction?
            3. **Check if they're equal** - Are the dots at the same position?
            4. **Remember: Right = Larger** - The fraction further right is bigger
            
            ### Quick Tips:
            - **Same position?** The fractions are equivalent (equal)
            - **Different positions?** The one on the right is larger
            - **Close together?** Look carefully at the exact positions
            - **Use the tick marks** - They show you the exact locations
            
            ### Common Equivalent Fractions:
            - 1/2 = 2/4 = 3/6 = 4/8 = 5/10
            - 1/3 = 2/6 = 3/9 = 4/12
            - 2/3 = 4/6 = 6/9 = 8/12
            - 1/4 = 2/8 = 3/12 = 4/16
            - 3/4 = 6/8 = 9/12 = 12/16
            """)