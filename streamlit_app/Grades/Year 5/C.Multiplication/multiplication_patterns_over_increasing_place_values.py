import streamlit as st
import random

def run():
    """
    Main function to run the Multiplication Patterns Over Increasing Place Values practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiplication_patterns_over_increasing_place_values.py
    """
    # Initialize session state for difficulty and game state
    if "patterns_difficulty" not in st.session_state:
        st.session_state.patterns_difficulty = 1  # Start with basic patterns
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answers = {}
        st.session_state.pattern_type = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📈 Multiplication Patterns Over Increasing Place Values")
    st.markdown("*Discover patterns when multiplying by powers of 10*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.patterns_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        pattern_names = ["Basic Facts", "Larger Numbers", "Complex Patterns"]
        st.markdown(f"**Current Level:** {pattern_names[difficulty_level - 1]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
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
        ### Understanding Multiplication Patterns:
        
        **🔢 Pattern Type 1 - Products Increase:**
        ```
        9 × 8 = 72
        90 × 8 = 720      (72 × 10)
        900 × 8 = 7,200   (72 × 100)
        ```
        When the first number gets 10 times bigger, the product gets 10 times bigger!
        
        **🔢 Pattern Type 2 - Find Missing Multiplier:**
        ```
        9 × 5 = 45
        9 × 50 = 450      (5 × 10)
        9 × 500 = 4,500   (5 × 100)
        ```
        When the product gets 10 times bigger, the multiplier gets 10 times bigger!
        
        **🔢 Pattern Type 3 - Find Missing Multiplicand:**
        ```
        7 × 4 = 28
        70 × 4 = 280      (7 × 10)
        700 × 4 = 2,800   (7 × 100)
        ```
        
        ### Key Patterns to Remember:
        - **× 10** → Add one zero (or move decimal right 1 place)
        - **× 100** → Add two zeros (or move decimal right 2 places)  
        - **× 1,000** → Add three zeros (or move decimal right 3 places)
        
        ### Tips for Success:
        - **Start with the first equation** - it gives you the basic fact
        - **Look for the pattern** - how are numbers changing?
        - **Count the zeros** - they tell you the place value
        - **Use the previous answer** to help find the next one
        - **Check your work** - does the pattern make sense?
        
        ### Examples:
        
        **Pattern 1 Example:**
        If 6 × 7 = 42, then:
        - 60 × 7 = 420 (add one zero)
        - 600 × 7 = 4,200 (add two zeros)
        
        **Pattern 2 Example:**  
        If 8 × ? = 320, and we know 8 × 4 = 32, then ? = 40
        
        **Pattern 3 Example:**
        If ? × 30 = 2,400, and we know 8 × 3 = 24, then ? = 80
        
        ### Common Mistakes to Avoid:
        - ❌ **Forgetting to add zeros** when numbers get bigger
        - ❌ **Adding too many zeros** - count carefully!
        - ❌ **Not using the first equation** as your starting point
        - ❌ **Ignoring the pattern** - each step follows the same rule
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Basic facts with single digits (2-9)
        - **🟠 Level 2:** Larger starting numbers (10-99)  
        - **🔴 Level 3:** Complex patterns with larger numbers
        """)

def generate_new_question():
    """Generate a new multiplication pattern question"""
    difficulty = st.session_state.patterns_difficulty
    
    # Choose pattern type randomly
    pattern_type = random.randint(1, 3)
    st.session_state.pattern_type = pattern_type
    
    # Generate base numbers based on difficulty
    if difficulty == 1:
        # Basic single digits
        base_factor1 = random.randint(2, 9)
        base_factor2 = random.randint(2, 9)
    elif difficulty == 2:
        # Slightly larger numbers
        base_factor1 = random.randint(2, 12)
        base_factor2 = random.randint(2, 12)
    else:
        # More complex patterns
        base_factor1 = random.randint(2, 15)
        base_factor2 = random.randint(2, 15)
    
    # Calculate base product
    base_product = base_factor1 * base_factor2
    
    # Create pattern equations based on type
    if pattern_type == 1:
        # Type 1: First factor increases, find products
        equations = []
        powers = [1, 10, 100, 1000, 10000, 100000, 1000000]
        
        for i, power in enumerate(powers[:7]):
            factor1 = base_factor1 * power
            factor2 = base_factor2
            product = factor1 * factor2
            
            equations.append({
                'factor1': factor1,
                'factor2': factor2,
                'product': product,
                'missing': 'product'
            })
        
        st.session_state.current_question = "Complete the pattern:"
        pattern_description = f"Finding products when the first number increases by powers of 10"
        
    elif pattern_type == 2:
        # Type 2: Second factor increases, find missing second factors
        equations = []
        powers = [1, 10, 100, 1000, 10000, 100000, 1000000]
        
        for i, power in enumerate(powers[:7]):
            factor1 = base_factor1
            factor2 = base_factor2 * power
            product = factor1 * factor2
            
            equations.append({
                'factor1': factor1,
                'factor2': factor2,
                'product': product,
                'missing': 'factor2'
            })
        
        st.session_state.current_question = "Complete the pattern:"
        pattern_description = f"Finding missing multipliers when products increase by powers of 10"
        
    else:
        # Type 3: First factor increases, find missing first factors
        equations = []
        powers = [1, 10, 100, 1000, 10000, 100000, 1000000]
        
        for i, power in enumerate(powers[:7]):
            factor1 = base_factor1 * power
            factor2 = base_factor2 * (powers[1] if i > 0 else powers[0])  # Second factor also increases
            product = factor1 * factor2
            
            equations.append({
                'factor1': factor1,
                'factor2': factor2,
                'product': product,
                'missing': 'factor1'
            })
        
        st.session_state.current_question = "Complete the pattern:"
        pattern_description = f"Finding missing multiplicands when both factors increase"
    
    # Store question data
    st.session_state.question_data = {
        'equations': equations,
        'pattern_type': pattern_type,
        'description': pattern_description,
        'base_factor1': base_factor1,
        'base_factor2': base_factor2
    }
    
    # Set up correct answers
    st.session_state.correct_answers = {}
    for i, eq in enumerate(equations):
        if eq['missing'] == 'product':
            st.session_state.correct_answers[f'answer_{i}'] = eq['product']
        elif eq['missing'] == 'factor2':
            st.session_state.correct_answers[f'answer_{i}'] = eq['factor2']
        elif eq['missing'] == 'factor1':
            st.session_state.correct_answers[f'answer_{i}'] = eq['factor1']

def display_question():
    """Display the current pattern question"""
    data = st.session_state.question_data
    
    # Display question header
    st.markdown("### 📈 Pattern Recognition:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Show pattern type
    pattern_type = data['pattern_type']
    if pattern_type == 1:
        st.markdown("🔢 **Type 1:** Find the products as the first number increases")
    elif pattern_type == 2:
        st.markdown("🔍 **Type 2:** Find the missing multipliers")
    else:
        st.markdown("🎯 **Type 3:** Find the missing multiplicands")
    
    # Create form for answers
    with st.form("patterns_form"):
        # Style for the pattern container
        st.markdown("""
        <style>
        .pattern-container {
            background-color: #f8f9fa;
            border: 2px solid #e1e5e9;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
        }
        .pattern-equation {
            margin: 15px 0;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown('<div class="pattern-container">', unsafe_allow_html=True)
            
            user_answers = {}
            equations = data['equations']
            
            for i, equation in enumerate(equations):
                # Create columns for each part of the equation
                eq_cols = st.columns([2, 1, 2, 1, 3])
                
                with eq_cols[0]:
                    if equation['missing'] == 'factor1':
                        # Input field for missing first factor
                        answer = st.number_input(
                            f"Equation {i+1} - Factor 1",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed",
                            placeholder="?"
                        )
                        user_answers[f'answer_{i}'] = answer
                    else:
                        # Show the first factor
                        st.markdown(f"<div style='font-size: 20px; text-align: right; margin-top: 8px;'>{equation['factor1']:,}</div>", unsafe_allow_html=True)
                
                with eq_cols[1]:
                    st.markdown("<div style='font-size: 20px; text-align: center; margin-top: 8px;'>×</div>", unsafe_allow_html=True)
                
                with eq_cols[2]:
                    if equation['missing'] == 'factor2':
                        # Input field for missing second factor
                        answer = st.number_input(
                            f"Equation {i+1} - Factor 2",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed",
                            placeholder="?"
                        )
                        user_answers[f'answer_{i}'] = answer
                    else:
                        # Show the second factor
                        st.markdown(f"<div style='font-size: 20px; text-align: right; margin-top: 8px;'>{equation['factor2']:,}</div>", unsafe_allow_html=True)
                
                with eq_cols[3]:
                    st.markdown("<div style='font-size: 20px; text-align: center; margin-top: 8px;'>=</div>", unsafe_allow_html=True)
                
                with eq_cols[4]:
                    if equation['missing'] == 'product':
                        # Input field for missing product
                        answer = st.number_input(
                            f"Equation {i+1} - Product",
                            min_value=0,
                            step=1,
                            key=f"answer_{i}",
                            label_visibility="collapsed",
                            placeholder="?"
                        )
                        user_answers[f'answer_{i}'] = answer
                    else:
                        # Show the product
                        st.markdown(f"<div style='font-size: 20px; text-align: left; margin-top: 8px;'>{equation['product']:,}</div>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answers = user_answers
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
            if st.button("🔄 Next Pattern", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answers"""
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    
    all_correct = True
    feedback_messages = []
    
    # Check each answer
    for i, equation in enumerate(data['equations']):
        user_val = user_answers.get(f'answer_{i}', 0)
        correct_val = correct_answers[f'answer_{i}']
        
        if user_val == correct_val:
            feedback_messages.append(f"✅ Equation {i+1}: **{user_val:,}** is correct!")
        else:
            feedback_messages.append(f"❌ Equation {i+1}: You wrote **{user_val:,}**, but the correct answer is **{correct_val:,}**")
            all_correct = False
    
    # Display overall result
    if all_correct:
        st.success("🎉 **Excellent! You found the complete pattern!**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.patterns_difficulty
        st.session_state.patterns_difficulty = min(
            st.session_state.patterns_difficulty + 1, 3
        )
        
        if st.session_state.patterns_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered complex multiplication patterns!**")
        elif old_difficulty < st.session_state.patterns_difficulty:
            st.info(f"⬆️ **Great pattern recognition! Moving up to Level {st.session_state.patterns_difficulty}**")
    
    else:
        st.error("❌ **Some answers need work. Let's review the pattern:**")
        
        # Stay at current difficulty or decrease slightly
        if st.session_state.patterns_difficulty > 1:
            old_difficulty = st.session_state.patterns_difficulty
            st.session_state.patterns_difficulty = max(
                st.session_state.patterns_difficulty - 1, 1
            )
            if old_difficulty > st.session_state.patterns_difficulty:
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.patterns_difficulty}**")
    
    # Show detailed feedback
    st.markdown("### 📋 Detailed Feedback:")
    for message in feedback_messages:
        st.markdown(f"- {message}")
    
    # Show pattern explanation
    show_pattern_explanation()

def show_pattern_explanation():
    """Show explanation of the multiplication pattern"""
    data = st.session_state.question_data
    pattern_type = data['pattern_type']
    
    with st.expander("📖 **Click here for pattern explanation**", expanded=False):
        st.markdown(f"""
        ### Pattern Analysis:
        **Pattern Type:** {pattern_type}
        
        ### How this pattern works:
        """)
        
        if pattern_type == 1:
            st.markdown(f"""
            **Rule:** When the first number gets 10 times bigger, the product gets 10 times bigger!
            
            **Base fact:** {data['base_factor1']} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2']}
            
            **Pattern breakdown:**
            - {data['base_factor1']} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2']}
            - {data['base_factor1'] * 10:,} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2'] * 10:,} (add 1 zero)
            - {data['base_factor1'] * 100:,} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2'] * 100:,} (add 2 zeros)
            - And so on...
            
            💡 **Key insight:** Multiplying by powers of 10 just adds zeros to the product!
            """)
            
        elif pattern_type == 2:
            st.markdown(f"""
            **Rule:** When the product gets 10 times bigger, the missing factor gets 10 times bigger!
            
            **Base fact:** {data['base_factor1']} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2']}
            
            **Pattern breakdown:**
            - If {data['base_factor1']} × ? = {data['base_factor1'] * data['base_factor2']}, then ? = {data['base_factor2']}
            - If {data['base_factor1']} × ? = {data['base_factor1'] * data['base_factor2'] * 10:,}, then ? = {data['base_factor2'] * 10:,}
            - If {data['base_factor1']} × ? = {data['base_factor1'] * data['base_factor2'] * 100:,}, then ? = {data['base_factor2'] * 100:,}
            - And so on...
            
            💡 **Key insight:** When the product grows by a factor of 10, so does the missing multiplier!
            """)
            
        else:
            st.markdown(f"""
            **Rule:** When both factors grow by powers of 10, the product grows by their combined effect!
            
            **Base fact:** {data['base_factor1']} × {data['base_factor2']} = {data['base_factor1'] * data['base_factor2']}
            
            **Pattern breakdown:**
            Look at how both numbers change and how it affects the product.
            Each step follows the same multiplication pattern with larger place values.
            
            💡 **Key insight:** Place value patterns help us multiply large numbers quickly!
            """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answers = {}
    st.session_state.pattern_type = None