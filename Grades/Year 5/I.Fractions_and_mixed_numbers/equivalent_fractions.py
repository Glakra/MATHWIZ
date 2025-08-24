import streamlit as st
import random
import math

def run():
    """
    Main function to run the Equivalent fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/equivalent_fractions.py
    """
    # Initialize session state
    if "equiv_problem" not in st.session_state:
        st.session_state.equiv_problem = None
        st.session_state.equiv_submitted = False
        st.session_state.user_answer = ""
        st.session_state.selected_fractions = []
        st.session_state.problem_type = None
    
    # Initialize adaptive difficulty
    if "equiv_difficulty" not in st.session_state:
        st.session_state.equiv_difficulty = 1  # Start at easy level (1-3)
        st.session_state.equiv_streak = 0  # Track consecutive correct answers
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("🔄 Equivalent Fractions")
    st.markdown("*Find equivalent fractions and complete fraction equations*")
    st.markdown("---")
    
    # Difficulty indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        diff_labels = {1: "Basic", 2: "Medium", 3: "Advanced"}
        st.markdown(f"**Difficulty:** {diff_labels[st.session_state.equiv_difficulty]}")
        st.progress(st.session_state.equiv_difficulty / 3)
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.equiv_problem is None:
        problem_type = random.choice(['fill_blank', 'multiple_choice'])
        st.session_state.problem_type = problem_type
        
        if problem_type == 'fill_blank':
            st.session_state.equiv_problem = generate_fill_blank_problem(st.session_state.equiv_difficulty)
        else:
            st.session_state.equiv_problem = generate_multiple_choice_problem(st.session_state.equiv_difficulty)
        
        st.session_state.equiv_submitted = False
        st.session_state.user_answer = ""
        st.session_state.selected_fractions = []
    
    problem = st.session_state.equiv_problem
    
    # Display the appropriate problem type
    if st.session_state.problem_type == 'fill_blank':
        display_fill_blank_problem(problem)
    else:
        display_multiple_choice_problem(problem)
    
    # Show feedback if answer was submitted
    if st.session_state.equiv_submitted:
        if st.session_state.problem_type == 'fill_blank':
            show_fill_blank_feedback()
        else:
            show_multiple_choice_feedback()
    
    # Next question button
    if st.session_state.equiv_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.equiv_problem = None
                st.session_state.equiv_submitted = False
                st.session_state.user_answer = ""
                st.session_state.selected_fractions = []
                st.session_state.problem_type = None
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Equivalent Fractions:
        - Fractions that represent the same amount
        - Created by multiplying or dividing both numerator and denominator by the same number
        
        ### Examples:
        - 1/2 = 2/4 = 3/6 = 4/8 (multiply by 2, 3, 4)
        - 6/9 = 2/3 (divide both by 3)
        - 4/12 = 1/3 (divide both by 4)
        
        ### How to Find Equivalent Fractions:
        1. **Multiply method:** Multiply top and bottom by the same number
        2. **Divide method:** Divide top and bottom by their common factor
        3. **Cross multiply:** For a/b = c/d, check if a×d = b×c
        
        ### Tips:
        - Look for patterns in the numbers
        - Check if one fraction can be simplified
        - Remember: what you do to the top, you must do to the bottom!
        """)

def generate_fill_blank_problem(difficulty):
    """Generate a fill-in-the-blank equivalent fraction problem based on difficulty"""
    problem_types = ['missing_numerator', 'missing_denominator']
    problem_type = random.choice(problem_types)
    
    # Adjust ranges based on difficulty
    if difficulty == 1:  # Easy
        base_num = random.randint(1, 5)
        base_den = random.randint(2, 8)
        multiplier = random.randint(2, 3)
    elif difficulty == 2:  # Medium
        base_num = random.randint(2, 8)
        base_den = random.randint(3, 12)
        multiplier = random.randint(2, 5)
    else:  # Hard
        base_num = random.randint(3, 12)
        base_den = random.randint(4, 20)
        multiplier = random.randint(3, 8)
    
    # Ensure fraction is in simplest form for clarity
    gcd = math.gcd(base_num, base_den)
    base_num //= gcd
    base_den //= gcd
    
    if problem_type == 'missing_numerator':
        # Show: ?/new_den = base_num/base_den
        new_den = base_den * multiplier
        missing_value = base_num * multiplier
        
        return {
            'type': 'missing_numerator',
            'given_num': base_num,
            'given_den': base_den,
            'shown_den': new_den,
            'missing_value': missing_value,
            'multiplier': multiplier
        }
    else:
        # Show: new_num/? = base_num/base_den
        new_num = base_num * multiplier
        missing_value = base_den * multiplier
        
        return {
            'type': 'missing_denominator',
            'given_num': base_num,
            'given_den': base_den,
            'shown_num': new_num,
            'missing_value': missing_value,
            'multiplier': multiplier
        }

def generate_multiple_choice_problem(difficulty):
    """Generate a multiple choice equivalent fraction problem based on difficulty"""
    # Adjust ranges based on difficulty
    if difficulty == 1:  # Easy
        base_num = random.randint(1, 4)
        base_den = random.randint(2, 8)
        multipliers = [2, 3]
    elif difficulty == 2:  # Medium
        base_num = random.randint(2, 6)
        base_den = random.randint(3, 12)
        multipliers = [2, 3, 4, 5]
    else:  # Hard
        base_num = random.randint(3, 9)
        base_den = random.randint(4, 15)
        multipliers = [2, 3, 4, 5, 6, 7]
    
    # Simplify to lowest terms
    gcd = math.gcd(base_num, base_den)
    base_num //= gcd
    base_den //= gcd
    
    # Generate correct equivalent fractions
    correct_fractions = []
    num_correct = random.randint(1, min(3, len(multipliers)))
    selected_multipliers = random.sample(multipliers, num_correct)
    
    for mult in selected_multipliers:
        correct_fractions.append({
            'num': base_num * mult,
            'den': base_den * mult,
            'is_correct': True
        })
    
    # Generate incorrect fractions
    incorrect_fractions = []
    
    # Type 1: Only multiply numerator or denominator
    incorrect_fractions.append({
        'num': base_num * 2,
        'den': base_den,
        'is_correct': False
    })
    
    # Type 2: Add instead of multiply
    if base_num + 2 < base_den + 2:
        incorrect_fractions.append({
            'num': base_num + 2,
            'den': base_den + 2,
            'is_correct': False
        })
    
    # Type 3: Different fraction that's close in value
    close_num = base_num + random.choice([-1, 1])
    close_den = base_den + random.choice([-1, 0, 1])
    if close_num > 0 and close_den > 1 and close_num < close_den:
        if not (close_num == base_num and close_den == base_den):
            incorrect_fractions.append({
                'num': close_num,
                'den': close_den,
                'is_correct': False
            })
    
    # Combine and select 4 options total
    all_options = correct_fractions + incorrect_fractions
    
    # Ensure we have exactly 4 options
    while len(all_options) < 4:
        # Generate a random incorrect fraction
        rand_num = random.randint(1, 12)
        rand_den = random.randint(2, 15)
        if rand_den > rand_num and not any(opt['num'] == rand_num and opt['den'] == rand_den for opt in all_options):
            all_options.append({
                'num': rand_num,
                'den': rand_den,
                'is_correct': False
            })
    
    # Shuffle and take 4
    random.shuffle(all_options)
    options = all_options[:4]
    
    # Ensure at least one correct answer
    if not any(opt['is_correct'] for opt in options):
        options[0] = correct_fractions[0]
    
    return {
        'base_num': base_num,
        'base_den': base_den,
        'options': options,
        'correct_count': sum(1 for opt in options if opt['is_correct'])
    }

def display_fill_blank_problem(problem):
    """Display a fill-in-the-blank problem"""
    st.markdown("### 📝 Type the missing number that makes these fractions equal:")
    
    # Create the equation display
    if problem['type'] == 'missing_numerator':
        col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 1])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; padding: 20px;">
                <div style="border-bottom: 2px solid black; padding-bottom: 5px;">
                    <input type="text" style="width: 60px; font-size: 24px; text-align: center; border: 2px solid #1f77b4;" disabled>
                </div>
                <div style="padding-top: 5px;">
                    {problem['shown_den']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; font-size: 24px; padding-top: 35px;">
                =
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; padding: 20px;">
                <div style="border-bottom: 2px solid black; padding-bottom: 5px;">
                    {problem['given_num']}
                </div>
                <div style="padding-top: 5px;">
                    {problem['given_den']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:  # missing_denominator
        col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 1])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; padding: 20px;">
                <div style="border-bottom: 2px solid black; padding-bottom: 5px;">
                    {problem['shown_num']}
                </div>
                <div style="padding-top: 5px;">
                    <input type="text" style="width: 60px; font-size: 24px; text-align: center; border: 2px solid #1f77b4;" disabled>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; font-size: 24px; padding-top: 35px;">
                =
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; padding: 20px;">
                <div style="border-bottom: 2px solid black; padding-bottom: 5px;">
                    {problem['given_num']}
                </div>
                <div style="padding-top: 5px;">
                    {problem['given_den']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Input field
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_answer,
            key="equiv_input",
            disabled=st.session_state.equiv_submitted,
            placeholder="Type the missing number",
            label_visibility="collapsed"
        )
        st.session_state.user_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.equiv_submitted):
            
            if st.session_state.user_answer.strip() == "":
                st.warning("⚠️ Please enter a number.")
            else:
                st.session_state.equiv_submitted = True
                st.rerun()

def display_multiple_choice_problem(problem):
    """Display a multiple choice problem"""
    st.markdown(f"### 📝 Which fractions are equivalent to {problem['base_num']}/{problem['base_den']}?")
    
    if problem['correct_count'] > 1:
        st.info("**Hint:** There may be more than one.")
    
    # Display options as clickable tiles with proper fraction display
    cols = st.columns(4)
    
    for i, option in enumerate(problem['options']):
        with cols[i]:
            # Create fraction display with HTML
            is_selected = i in st.session_state.selected_fractions
            
            # Create a container for the fraction
            if is_selected and not st.session_state.equiv_submitted:
                check_display = "✓"
                border_color = "#1f77b4"
                bg_color = "#e6f2ff"
            else:
                check_display = ""
                border_color = "#ccc"
                bg_color = "white"
            
            # Display fraction as HTML card
            st.markdown(f"""
            <div style="
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                background-color: {bg_color};
                cursor: pointer;
                margin-bottom: 10px;
            ">
                <div style="font-size: 24px; font-weight: bold;">
                    <div style="border-bottom: 2px solid black; display: inline-block; padding: 0 10px;">
                        {option['num']}
                    </div>
                    <div style="padding: 0 10px;">
                        {option['den']}
                    </div>
                </div>
                <div style="color: #1f77b4; font-size: 20px; margin-top: 5px;">
                    {check_display}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add invisible button for clicking
            if st.button(
                f"Select",
                key=f"frac_{i}",
                use_container_width=True,
                disabled=st.session_state.equiv_submitted,
                type="secondary"
            ):
                if i in st.session_state.selected_fractions:
                    st.session_state.selected_fractions.remove(i)
                else:
                    st.session_state.selected_fractions.append(i)
                st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.equiv_submitted or len(st.session_state.selected_fractions) == 0):
            st.session_state.equiv_submitted = True
            st.rerun()

def update_difficulty(is_correct):
    """Update difficulty based on performance"""
    if is_correct:
        st.session_state.equiv_streak += 1
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.equiv_streak >= 3 and st.session_state.equiv_difficulty < 3:
            st.session_state.equiv_difficulty += 1
            st.session_state.equiv_streak = 0
            st.info(f"🎯 Great job! Moving to {['Basic', 'Medium', 'Advanced'][st.session_state.equiv_difficulty - 1]} level!")
    else:
        st.session_state.equiv_streak = 0
        # Decrease difficulty after 2 wrong answers in current session
        if st.session_state.equiv_difficulty > 1:
            st.session_state.equiv_difficulty -= 1
            st.warning(f"📚 Let's practice more at {['Basic', 'Medium', 'Advanced'][st.session_state.equiv_difficulty - 1]} level!")

def show_fill_blank_feedback():
    """Show feedback for fill-in-the-blank problems"""
    problem = st.session_state.equiv_problem
    user_answer = st.session_state.user_answer.strip()
    
    try:
        user_value = int(user_answer)
        correct_value = problem['missing_value']
        
        is_correct = user_value == correct_value
        
        if is_correct:
            st.success(f"🎉 **Correct! {user_value} is the right answer!**")
            st.balloons()
            
            # Show the complete equation
            if problem['type'] == 'missing_numerator':
                st.info(f"✓ {user_value}/{problem['shown_den']} = {problem['given_num']}/{problem['given_den']}")
            else:
                st.info(f"✓ {problem['shown_num']}/{user_value} = {problem['given_num']}/{problem['given_den']}")
            
        else:
            st.error(f"❌ **Not quite right. The correct answer is {correct_value}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"""
                **Finding equivalent fractions:**
                
                Starting fraction: **{problem['given_num']}/{problem['given_den']}**
                
                To find the missing number, notice that:
                """)
                
                if problem['type'] == 'missing_numerator':
                    st.markdown(f"""
                    - The denominator changed from {problem['given_den']} to {problem['shown_den']}
                    - That's multiplying by {problem['multiplier']} (because {problem['given_den']} × {problem['multiplier']} = {problem['shown_den']})
                    - So the numerator must also be multiplied by {problem['multiplier']}
                    - {problem['given_num']} × {problem['multiplier']} = **{correct_value}**
                    
                    Complete equation: **{correct_value}/{problem['shown_den']} = {problem['given_num']}/{problem['given_den']}**
                    """)
                else:
                    st.markdown(f"""
                    - The numerator changed from {problem['given_num']} to {problem['shown_num']}
                    - That's multiplying by {problem['multiplier']} (because {problem['given_num']} × {problem['multiplier']} = {problem['shown_num']})
                    - So the denominator must also be multiplied by {problem['multiplier']}
                    - {problem['given_den']} × {problem['multiplier']} = **{correct_value}**
                    
                    Complete equation: **{problem['shown_num']}/{correct_value} = {problem['given_num']}/{problem['given_den']}**
                    """)
        
        # Update difficulty
        update_difficulty(is_correct)
                
    except ValueError:
        st.error("❌ Please enter a whole number")

def show_multiple_choice_feedback():
    """Show feedback for multiple choice problems"""
    problem = st.session_state.equiv_problem
    selected = st.session_state.selected_fractions
    
    # Check which ones are correct
    correct_indices = [i for i, opt in enumerate(problem['options']) if opt['is_correct']]
    
    # Check if selection matches correct answers
    is_correct = set(selected) == set(correct_indices)
    
    if is_correct:
        st.success("🎉 **Perfect! You found all the equivalent fractions!**")
        st.balloons()
        
        # Show the correct fractions
        correct_fracs = [f"{problem['options'][i]['num']}/{problem['options'][i]['den']}" 
                        for i in correct_indices]
        st.info(f"✓ {problem['base_num']}/{problem['base_den']} = {' = '.join(correct_fracs)}")
        
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what was correct and what was missed
        with st.expander("📖 **See the correct answers**", expanded=True):
            st.markdown(f"**Finding fractions equivalent to {problem['base_num']}/{problem['base_den']}:**")
            
            for i, option in enumerate(problem['options']):
                frac = f"{option['num']}/{option['den']}"
                
                if option['is_correct']:
                    if i in selected:
                        st.markdown(f"✅ **{frac}** - Correct! You selected this.")
                    else:
                        st.markdown(f"❌ **{frac}** - This is equivalent but you didn't select it.")
                else:
                    if i in selected:
                        st.markdown(f"❌ **{frac}** - This is NOT equivalent but you selected it.")
                    else:
                        st.markdown(f"✓ **{frac}** - Correctly not selected (not equivalent).")
            
            # Explain why the correct ones are equivalent
            st.markdown("\n**Why they're equivalent:**")
            for i in correct_indices:
                opt = problem['options'][i]
                multiplier = opt['num'] // problem['base_num']
                st.markdown(f"- {opt['num']}/{opt['den']} = {problem['base_num']}×{multiplier}/{problem['base_den']}×{multiplier}")
    
    # Update difficulty
    update_difficulty(is_correct)