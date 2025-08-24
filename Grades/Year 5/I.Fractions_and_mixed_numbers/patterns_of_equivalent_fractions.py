import streamlit as st
import random
import math

def run():
    """
    Main function to run the Patterns of equivalent fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/patterns_of_equivalent_fractions.py
    """
    # Initialize session state
    if "pattern_problem" not in st.session_state:
        st.session_state.pattern_problem = None
        st.session_state.pattern_submitted = False
        st.session_state.user_answer = ""
    
    # Initialize adaptive difficulty
    if "pattern_difficulty" not in st.session_state:
        st.session_state.pattern_difficulty = 1  # Start at easy level (1-3)
        st.session_state.pattern_streak = 0  # Track consecutive correct answers
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🔢 Patterns of Equivalent Fractions")
    st.markdown("*Find the missing number in the pattern*")
    st.markdown("---")
    
    # Difficulty indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        diff_labels = {1: "Basic", 2: "Medium", 3: "Advanced"}
        st.markdown(f"**Difficulty:** {diff_labels[st.session_state.pattern_difficulty]}")
        st.progress(st.session_state.pattern_difficulty / 3)
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.pattern_problem is None:
        st.session_state.pattern_problem = generate_pattern_problem(st.session_state.pattern_difficulty)
        st.session_state.pattern_submitted = False
        st.session_state.user_answer = ""
    
    problem = st.session_state.pattern_problem
    
    # Display the problem
    display_pattern_problem(problem)
    
    # Show feedback if answer was submitted
    if st.session_state.pattern_submitted:
        show_pattern_feedback()
    
    # Next question button
    if st.session_state.pattern_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.pattern_problem = None
                st.session_state.pattern_submitted = False
                st.session_state.user_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Understanding Patterns:
        - Each fraction in the sequence is equivalent (equal value)
        - Look for patterns in how numerators and denominators change
        - Common patterns:
          - Multiply by 1, 2, 3, 4... (e.g., 1/3 = 2/6 = 3/9 = 4/12)
          - Multiply by the same number each time
        
        ### How to Solve:
        1. **Look at the first fraction** - this is usually in simplest form
        2. **Find the pattern** - how do numbers change from one fraction to the next?
        3. **Apply the pattern** - use it to find the missing number
        
        ### Example:
        - Pattern: 1/5 = 2/10 = 3/15 = ?/20
        - Notice: numerators go 1, 2, 3, ? (add 1 each time)
        - Notice: denominators go 5, 10, 15, 20 (add 5 each time)
        - Missing number: 4 (because 4/20 = 1/5)
        """)

def generate_pattern_problem(difficulty):
    """Generate a pattern of equivalent fractions problem based on difficulty"""
    # Choose base fraction based on difficulty
    if difficulty == 1:  # Easy
        base_num = 1  # Always unit fractions for easy
        base_den = random.choice([2, 3, 4, 5, 6])
        pattern_length = 4
    elif difficulty == 2:  # Medium
        base_num = random.randint(1, 3)
        base_den = random.randint(3, 10)
        pattern_length = 5
    else:  # Hard
        base_num = random.randint(1, 5)
        base_den = random.randint(4, 12)
        pattern_length = 6
    
    # Ensure fraction is in simplest form
    gcd = math.gcd(base_num, base_den)
    base_num //= gcd
    base_den //= gcd
    
    # Generate the pattern (multiply by 1, 2, 3, etc.)
    fractions = []
    for i in range(1, pattern_length + 1):
        fractions.append({
            'num': base_num * i,
            'den': base_den * i
        })
    
    # Choose which position to make blank
    # For easier levels, blank earlier positions; for harder, blank later ones
    if difficulty == 1:
        blank_position = random.choice([1, 2, 3])  # Not the first one
    elif difficulty == 2:
        blank_position = random.choice([1, 2, 3, 4])
    else:
        blank_position = random.choice([0, 1, 2, 3, 4, 5])
    
    # Randomly choose to blank numerator or denominator
    blank_type = random.choice(['numerator', 'denominator'])
    
    # Store the missing value
    if blank_type == 'numerator':
        missing_value = fractions[blank_position]['num']
    else:
        missing_value = fractions[blank_position]['den']
    
    return {
        'fractions': fractions,
        'blank_position': blank_position,
        'blank_type': blank_type,
        'missing_value': missing_value,
        'base_num': base_num,
        'base_den': base_den
    }

def display_pattern_problem(problem):
    """Display the pattern problem"""
    st.markdown("### 📝 Type the missing number to complete the equivalent fraction.")
    
    # Create HTML for the fraction pattern
    html_parts = ['<div style="font-size: 20px; margin: 20px 0; text-align: center;">']
    
    for i, frac in enumerate(problem['fractions']):
        if i > 0:
            html_parts.append(' = ')
        
        # Check if this fraction has the blank
        if i == problem['blank_position']:
            if problem['blank_type'] == 'numerator':
                # Blank numerator
                html_parts.append(f'''
                    <div style="display: inline-block; margin: 0 5px;">
                        <div style="border-bottom: 2px solid black; padding: 0 8px; min-width: 30px;">
                            <input type="text" style="width: 40px; border: 2px solid #1f77b4; text-align: center;" disabled>
                        </div>
                        <div style="padding: 0 8px;">{frac['den']}</div>
                    </div>
                ''')
            else:
                # Blank denominator
                html_parts.append(f'''
                    <div style="display: inline-block; margin: 0 5px;">
                        <div style="border-bottom: 2px solid black; padding: 0 8px; min-width: 30px;">
                            {frac['num']}
                        </div>
                        <div style="padding: 0 8px;">
                            <input type="text" style="width: 40px; border: 2px solid #1f77b4; text-align: center;" disabled>
                        </div>
                    </div>
                ''')
        else:
            # Normal fraction
            html_parts.append(f'''
                <div style="display: inline-block; margin: 0 5px;">
                    <div style="border-bottom: 2px solid black; padding: 0 8px; min-width: 30px;">
                        {frac['num']}
                    </div>
                    <div style="padding: 0 8px;">{frac['den']}</div>
                </div>
            ''')
    
    html_parts.append('</div>')
    
    # Display the pattern
    st.markdown(''.join(html_parts), unsafe_allow_html=True)
    
    # Input field
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_answer,
            key="pattern_input",
            disabled=st.session_state.pattern_submitted,
            placeholder="Type the missing number",
            label_visibility="collapsed"
        )
        st.session_state.user_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.pattern_submitted):
            
            if st.session_state.user_answer.strip() == "":
                st.warning("⚠️ Please enter a number.")
            else:
                st.session_state.pattern_submitted = True
                st.rerun()

def update_difficulty(is_correct):
    """Update difficulty based on performance"""
    if is_correct:
        st.session_state.pattern_streak += 1
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.pattern_streak >= 3 and st.session_state.pattern_difficulty < 3:
            st.session_state.pattern_difficulty += 1
            st.session_state.pattern_streak = 0
            st.info(f"🎯 Great job! Moving to {['Basic', 'Medium', 'Advanced'][st.session_state.pattern_difficulty - 1]} level!")
    else:
        st.session_state.pattern_streak = 0
        # Decrease difficulty after wrong answer
        if st.session_state.pattern_difficulty > 1:
            st.session_state.pattern_difficulty -= 1
            st.warning(f"📚 Let's practice more at {['Basic', 'Medium', 'Advanced'][st.session_state.pattern_difficulty - 1]} level!")

def show_pattern_feedback():
    """Show feedback for the pattern problem"""
    problem = st.session_state.pattern_problem
    user_answer = st.session_state.user_answer.strip()
    
    try:
        user_value = int(user_answer)
        correct_value = problem['missing_value']
        
        is_correct = user_value == correct_value
        
        if is_correct:
            st.success(f"🎉 **Excellent! {user_value} is correct!**")
            st.balloons()
            
            # Show the complete pattern
            complete_pattern = []
            for i, frac in enumerate(problem['fractions']):
                complete_pattern.append(f"{frac['num']}/{frac['den']}")
            st.info(f"✓ Complete pattern: {' = '.join(complete_pattern)}")
            
        else:
            st.error(f"❌ **Not quite right. The correct answer is {correct_value}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"""
                **Understanding the pattern:**
                
                The base fraction is: **{problem['base_num']}/{problem['base_den']}**
                
                **The pattern works like this:**
                """)
                
                # Show how each fraction is formed
                for i, frac in enumerate(problem['fractions']):
                    multiplier = i + 1
                    st.markdown(f"- Position {i+1}: {problem['base_num']} × {multiplier} = {frac['num']}, "
                              f"{problem['base_den']} × {multiplier} = {frac['den']} → **{frac['num']}/{frac['den']}**")
                
                st.markdown(f"""
                
                **For the missing number:**
                - Position: {problem['blank_position'] + 1}
                - Multiplier: {problem['blank_position'] + 1}
                """)
                
                if problem['blank_type'] == 'numerator':
                    st.markdown(f"- Missing numerator: {problem['base_num']} × {problem['blank_position'] + 1} = **{correct_value}**")
                else:
                    st.markdown(f"- Missing denominator: {problem['base_den']} × {problem['blank_position'] + 1} = **{correct_value}**")
                
                st.markdown(f"\nYour answer: {user_answer}")
        
        # Update difficulty
        update_difficulty(is_correct)
                
    except ValueError:
        st.error("❌ Please enter a whole number")