import streamlit as st
import random

def run():
    """
    Main function to run the Add Fractions with Strip Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/add_fractions_with_like_denominators_using_strip_models.py
    """
    # Initialize session state for difficulty and game state
    if "strip_model_difficulty" not in st.session_state:
        st.session_state.strip_model_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➕ Add Fractions Using Strip Models")
    st.markdown("*Use the fraction strips to help you add*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.strip_model_difficulty
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
        ### How to Use Strip Models:
        1. The **yellow strip** represents 1 whole
        2. The **pink strips** below show the fraction units (like 1/8 each)
        3. The **brackets** show which parts you're adding
        4. Count the total number of unit fractions
        5. Write your answer in the box
        
        ### Example:
        If you see:
        - First bracket covering 2 strips of 1/8 → that's 2/8
        - Second bracket covering 3 strips of 1/8 → that's 3/8
        - Together: 2/8 + 3/8 = 5/8 (5 strips total)
        
        ### Remember:
        - The denominator stays the same
        - Just add the numerators (count the strips)
        - The strip model shows you exactly what you're adding!
        """)

def generate_new_question():
    """Generate a new strip model addition question"""
    difficulty = st.session_state.strip_model_difficulty
    
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
    
    # Generate numerators that don't exceed the denominator when added
    max_sum = denominator  # Can equal the whole but not exceed
    
    # Generate first numerator
    numerator1 = random.randint(1, min(denominator - 1, max_sum - 1))
    
    # Generate second numerator
    max_num2 = min(denominator - 1, max_sum - numerator1)
    numerator2 = random.randint(1, max_num2)
    
    # Calculate the sum
    sum_numerator = numerator1 + numerator2
    
    st.session_state.question_data = {
        "numerator1": numerator1,
        "numerator2": numerator2,
        "denominator": denominator,
        "sum_numerator": sum_numerator
    }
    
    st.session_state.correct_answer = sum_numerator
    st.session_state.current_question = "Add. Use the fraction strips to help."

def create_strip_model_svg(data):
    """Create an SVG strip model for fraction addition"""
    width = 600
    height = 150
    strip_height = 40
    unit_strip_height = 35
    
    # Calculate unit width
    unit_width = (width - 20) / data['denominator']
    
    # Build SVG string without f-strings to avoid brace issues
    svg_parts = []
    svg_parts.append('<svg width="' + str(width) + '" height="' + str(height) + '" style="margin: 20px 0;">')
    
    # Whole strip (1)
    svg_parts.append('<rect x="10" y="10" width="' + str(width-20) + '" height="' + str(strip_height) + '" ')
    svg_parts.append('fill="#FFD700" stroke="#333" stroke-width="2"/>')
    svg_parts.append('<text x="' + str(width/2) + '" y="35" text-anchor="middle" font-size="20" font-weight="bold">1</text>')
    
    # Unit fraction strips
    y_position = 60
    for i in range(data['denominator']):
        x_position = 10 + i * unit_width
        svg_parts.append('<rect x="' + str(x_position) + '" y="' + str(y_position) + '" width="' + str(unit_width) + '" height="' + str(unit_strip_height) + '" ')
        svg_parts.append('fill="#FFB6C1" stroke="#333" stroke-width="1"/>')
        text_x = x_position + unit_width/2
        text_y = y_position + unit_strip_height/2 + 5
        svg_parts.append('<text x="' + str(text_x) + '" y="' + str(text_y) + '" ')
        svg_parts.append('text-anchor="middle" font-size="14">1/' + str(data['denominator']) + '</text>')
    
    # Draw brackets for the two fractions
    bracket_y = y_position + unit_strip_height + 10
    
    # First fraction bracket
    x1_start = 10
    x1_end = 10 + data['numerator1'] * unit_width
    svg_parts.append('<path d="M ' + str(x1_start) + ' ' + str(bracket_y) + ' L ' + str(x1_start) + ' ' + str(bracket_y + 15))
    svg_parts.append(' L ' + str(x1_end) + ' ' + str(bracket_y + 15) + ' L ' + str(x1_end) + ' ' + str(bracket_y) + '" ')
    svg_parts.append('stroke="#333" stroke-width="2" fill="none"/>')
    text_x = (x1_start + x1_end)/2
    text_y = bracket_y + 30
    svg_parts.append('<text x="' + str(text_x) + '" y="' + str(text_y) + '" text-anchor="middle" font-size="16" font-weight="bold">')
    svg_parts.append(str(data['numerator1']) + '/' + str(data['denominator']) + '</text>')
    
    # Second fraction bracket
    x2_start = x1_end
    x2_end = x2_start + data['numerator2'] * unit_width
    svg_parts.append('<path d="M ' + str(x2_start) + ' ' + str(bracket_y) + ' L ' + str(x2_start) + ' ' + str(bracket_y + 15))
    svg_parts.append(' L ' + str(x2_end) + ' ' + str(bracket_y + 15) + ' L ' + str(x2_end) + ' ' + str(bracket_y) + '" ')
    svg_parts.append('stroke="#333" stroke-width="2" fill="none"/>')
    text_x = (x2_start + x2_end)/2
    text_y = bracket_y + 30
    svg_parts.append('<text x="' + str(text_x) + '" y="' + str(text_y) + '" text-anchor="middle" font-size="16" font-weight="bold">')
    svg_parts.append(str(data['numerator2']) + '/' + str(data['denominator']) + '</text>')
    
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the strip model
    strip_svg = create_strip_model_svg(data)
    st.markdown(strip_svg, unsafe_allow_html=True)
    
    # Display the equation
    st.markdown("")
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 2])
    
    with col1:
        # Build fraction HTML without f-strings
        html = '<div style="text-align: center; padding: 20px; background-color: #f0f0f0; border-radius: 10px;">'
        html += '<div style="font-size: 28px; font-weight: bold;">'
        html += '<span style="border-bottom: 2px solid black; padding: 0 10px;">' + str(data['numerator1']) + '</span>'
        html += '<br>'
        html += '<span style="padding: 0 10px;">' + str(data['denominator']) + '</span>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 30px;">
            +
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Build fraction HTML without f-strings
        html = '<div style="text-align: center; padding: 20px; background-color: #f0f0f0; border-radius: 10px;">'
        html += '<div style="font-size: 28px; font-weight: bold;">'
        html += '<span style="border-bottom: 2px solid black; padding: 0 10px;">' + str(data['numerator2']) + '</span>'
        html += '<br>'
        html += '<span style="padding: 0 10px;">' + str(data['denominator']) + '</span>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding-top: 30px;">
            =
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Create form for answer input
        with st.form("answer_form"):
            answer_col1, answer_col2 = st.columns([1, 2])
            
            with answer_col1:
                user_input = st.text_input(
                    "",
                    key="fraction_input",
                    placeholder="?",
                    label_visibility="collapsed"
                )
            
            # Submit button
            st.markdown("")
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
                        st.error("Please enter a valid fraction (e.g., 3/8)")
                else:
                    try:
                        # If they just entered the numerator
                        user_num = int(user_input)
                        st.session_state.user_answer = user_num
                        st.session_state.answer_submitted = True
                        st.session_state.show_feedback = True
                    except:
                        st.error("Please enter a valid answer")
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
        
        st.success(f"✓ {fraction1} + {fraction2} = {result}")
        
        # Show visual explanation
        with st.expander("🎯 **See how the strips show the answer**", expanded=True):
            st.markdown(f"""
            **Visual explanation:**
            - The first bracket shows {data['numerator1']} strips of 1/{data['denominator']}
            - The second bracket shows {data['numerator2']} strips of 1/{data['denominator']}
            - Together, you have {data['numerator1']} + {data['numerator2']} = {correct_answer} strips
            - So the answer is {result}
            
            The strip model makes it easy to see that you're just counting the total number of unit fractions!
            """)
        
        # Check if sum equals 1
        if correct_answer == data['denominator']:
            st.info("💡 **Special note:** Your answer equals 1 whole!")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.strip_model_difficulty
        st.session_state.strip_model_difficulty = min(
            st.session_state.strip_model_difficulty + 1, 5
        )
        
        if st.session_state.strip_model_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered adding fractions with strip models!**")
        elif old_difficulty < st.session_state.strip_model_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.strip_model_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        user_fraction = f"{user_answer}/{data['denominator']}"
        st.error(f"You answered: {user_fraction}")
        
        # Show the correct answer
        correct_fraction = f"{correct_answer}/{data['denominator']}"
        st.success(f"The correct answer is: {correct_fraction}")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.strip_model_difficulty
        st.session_state.strip_model_difficulty = max(
            st.session_state.strip_model_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.strip_model_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.strip_model_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for adding fractions with strip models"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Understanding Strip Models for Adding Fractions**", expanded=True):
        st.markdown(f"""
        ### How to Use the Strip Model
        
        **Your problem:**
        {data['numerator1']}/{data['denominator']} + {data['numerator2']}/{data['denominator']} = ?
        
        **Step 1: Look at the strips**
        - The yellow strip shows 1 whole
        - The pink strips show the unit fractions (1/{data['denominator']} each)
        - There are {data['denominator']} unit strips in total (making 1 whole)
        
        **Step 2: Count the first fraction**
        - The first bracket covers {data['numerator1']} strips
        - This represents {data['numerator1']}/{data['denominator']}
        
        **Step 3: Count the second fraction**
        - The second bracket covers {data['numerator2']} strips
        - This represents {data['numerator2']}/{data['denominator']}
        
        **Step 4: Add them together**
        - Total strips: {data['numerator1']} + {data['numerator2']} = {data['sum_numerator']}
        - The denominator stays {data['denominator']}
        
        **Answer: {data['sum_numerator']}/{data['denominator']}**
        
        ### Key Points:
        - Strip models help you visualize fractions as parts of a whole
        - Each small strip is one unit fraction
        - Adding fractions = counting the total number of strips
        - The denominator never changes when adding like fractions
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