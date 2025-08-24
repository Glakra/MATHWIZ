import streamlit as st
import random

def run():
    """
    Main function to run the Complete Missing Steps multiplication activity.
    """
    # Initialize session state
    if "missing_steps_difficulty" not in st.session_state:
        st.session_state.missing_steps_difficulty = "easy"
        st.session_state.correct_streak = 0
        st.session_state.total_attempts = 0
        st.session_state.performance_history = []
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.show_step_solution = False
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Complete the Missing Steps")
    st.markdown("*Fill in the missing numbers in two-digit multiplication*")
    st.markdown("---")
    
    # Performance Dashboard
    display_performance_dashboard()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        display_instructions()

def display_performance_dashboard():
    """Display performance tracking"""
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_map = {"easy": "🟡 Easy", "medium": "🟠 Medium", "hard": "🔴 Hard"}
        st.markdown(f"**Current Level:** {difficulty_map[st.session_state.missing_steps_difficulty]}")
        
        if st.session_state.total_attempts > 0:
            success_rate = (st.session_state.correct_streak / max(st.session_state.total_attempts, 1)) * 100
            st.progress(success_rate / 100, text=f"Success Rate: {success_rate:.0f}%")
    
    with col2:
        st.metric("🔥 Streak", st.session_state.correct_streak)
    
    with col3:
        st.metric("📊 Total", st.session_state.total_attempts)
    
    with col4:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

def display_instructions():
    """Display adaptive instructions"""
    difficulty = st.session_state.missing_steps_difficulty
    
    if difficulty == "easy":
        st.markdown("""
        ### 🌟 Traditional Multiplication Method:
        
        **Step-by-Step Process:**
        1. **Multiply by ones digit:** Start with the ones digit of the bottom number
        2. **Multiply by tens digit:** Then the tens digit (remember to add a zero!)
        3. **Add them together:** Line up the columns and add
        
        **Example: 49 × 47**
        ```
            4 9
        ×   4 7
        -------
          3 4 3  ← 49 × 7
        + 1 9 6 0  ← 49 × 40 (shifted left)
        -------
          2 3 0 3
        ```
        
        **Key Points:**
        - First line: 49 × 7 = 343
        - Second line: 49 × 4 = 196, but we're multiplying by 40, so it becomes 1960
        - Final answer: 343 + 1960 = 2303
        """)
    
    elif difficulty == "medium":
        st.markdown("""
        ### 🚀 Building Mastery:
        
        **You're getting good at this!** Now we'll have more missing numbers and bigger challenges.
        
        **Pro Tips:**
        - **Place value matters:** When multiplying by tens, remember to shift left
        - **Carrying:** Don't forget to carry when products are > 9
        - **Alignment:** Keep your columns lined up perfectly
        
        **Common Mistakes to Avoid:**
        - Forgetting to add the zero when multiplying by tens
        - Misaligning the partial products
        - Forgetting to carry in multiplication or addition
        """)
    
    else:  # hard
        st.markdown("""
        ### 🏆 Expert Level:
        
        **You're mastering the traditional algorithm!** These problems have multiple missing steps.
        
        **Advanced Strategies:**
        - **Mental estimation:** 47 × 49 should be close to 50 × 50 = 2500
        - **Digit analysis:** Look for patterns in the given numbers
        - **Work backwards:** Sometimes you can figure out missing numbers from the final answer
        
        **Challenge:** Can you spot which step contains the error if one exists?
        """)

def generate_new_question():
    """Generate questions with missing steps"""
    
    # Adaptive difficulty adjustment
    if len(st.session_state.performance_history) >= 3:
        recent_performance = st.session_state.performance_history[-3:]
        if all(recent_performance) and st.session_state.missing_steps_difficulty != "hard":
            if st.session_state.missing_steps_difficulty == "easy":
                st.session_state.missing_steps_difficulty = "medium"
            else:
                st.session_state.missing_steps_difficulty = "hard"
        elif not any(recent_performance) and st.session_state.missing_steps_difficulty != "easy":
            if st.session_state.missing_steps_difficulty == "hard":
                st.session_state.missing_steps_difficulty = "medium"
            else:
                st.session_state.missing_steps_difficulty = "easy"
    
    scenarios = {
        "easy": [
            {"multiplicand": 23, "multiplier": 34, "missing": ["step1"]},
            {"multiplicand": 41, "multiplier": 27, "missing": ["step2"]},
            {"multiplicand": 35, "multiplier": 42, "missing": ["final"]},
            {"multiplicand": 52, "multiplier": 36, "missing": ["step1"]},
            {"multiplicand": 46, "multiplier": 25, "missing": ["step2"]},
        ],
        "medium": [
            {"multiplicand": 67, "multiplier": 48, "missing": ["step1", "final"]},
            {"multiplicand": 54, "multiplier": 73, "missing": ["step2", "final"]},
            {"multiplicand": 89, "multiplier": 56, "missing": ["step1", "step2"]},
            {"multiplicand": 72, "multiplier": 64, "missing": ["step1", "final"]},
        ],
        "hard": [
            {"multiplicand": 78, "multiplier": 94, "missing": ["step1", "step2", "final"]},
            {"multiplicand": 86, "multiplier": 57, "missing": ["step1", "step2", "final"]},
            {"multiplicand": 93, "multiplier": 76, "missing": ["step1", "step2", "final"]},
            {"multiplicand": 84, "multiplier": 69, "missing": ["step1", "step2", "final"]},
        ]
    }
    
    scenario = random.choice(scenarios[st.session_state.missing_steps_difficulty])
    
    multiplicand = scenario["multiplicand"]
    multiplier = scenario["multiplier"]
    
    # Calculate the steps
    ones_digit = multiplier % 10
    tens_digit = multiplier // 10
    
    # Step 1: multiplicand × ones digit
    step1_result = multiplicand * ones_digit
    
    # Step 2: multiplicand × tens digit (shifted)
    step2_partial = multiplicand * tens_digit
    step2_result = step2_partial * 10  # This represents the shift
    
    # Final result
    final_result = step1_result + step2_result
    
    st.session_state.question_data = {
        "multiplicand": multiplicand,
        "multiplier": multiplier,
        "ones_digit": ones_digit,
        "tens_digit": tens_digit,
        "step1_result": step1_result,
        "step2_partial": step2_partial,
        "step2_result": step2_result,
        "final_result": final_result,
        "missing_positions": scenario["missing"]
    }
    
    st.session_state.correct_answers = {
        "step1": step1_result,
        "step2": step2_result,
        "final": final_result
    }
    
    st.session_state.current_question = f"Fill in the missing numbers to complete the multiplication!"

def display_question():
    """Display the multiplication problem with missing steps"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Create the visual multiplication layout with embedded inputs
    user_answers = create_multiplication_layout(data)
    
    # Input form
    with st.form("missing_steps_form", clear_on_submit=False):
        # The inputs are now embedded in the layout above
        # We just need to store the current values in session state for the form
        if user_answers:
            for key, value in user_answers.items():
                if value is not None:
                    st.session_state[f"form_{key}"] = value
        
        # Buttons
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        with col3:
            help_button = st.form_submit_button("🔍 Show Steps", type="secondary", use_container_width=True)
        
        if submit_button:
            # Get the current values from the embedded inputs
            current_answers = {}
            missing_positions = data['missing_positions']
            
            # Collect answers from the embedded inputs
            for position in missing_positions:
                if position == "step1" and "step1" in user_answers:
                    current_answers['step1'] = user_answers['step1']
                elif position == "step2" and "step2" in user_answers:
                    current_answers['step2'] = user_answers['step2']
                elif position == "final" and "final" in user_answers:
                    current_answers['final'] = user_answers['final']
            
            # Add non-missing values
            for position in ["step1", "step2", "final"]:
                if position not in missing_positions:
                    current_answers[position] = user_answers[position]
            
            # Validate inputs
            valid_submission = True
            for position in missing_positions:
                if position in current_answers and (current_answers[position] is None or current_answers[position] == ""):
                    valid_submission = False
                    break
            
            if valid_submission:
                st.session_state.user_answers = current_answers
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.total_attempts += 1
            else:
                st.warning("⚠️ Please fill in all the missing numbers before submitting.")
        
        if help_button:
            st.session_state.show_step_solution = True
    
    # Show step-by-step solution if requested
    if st.session_state.show_step_solution:
        show_step_by_step_solution()
    
    # Handle feedback and next button
    handle_feedback_and_next()

def create_multiplication_layout(data):
    """Create the visual multiplication problem layout with embedded inputs"""
    
    st.markdown("### 🔢 Complete the multiplication:")
    
    # Create the multiplication layout with better organization and positioning
    with st.container():
        # Create a more focused, better-centered layout
        col1, col2, col3 = st.columns([0.8, 2, 0.8])
        
        with col2:
            # Top part of multiplication - better formatted
            st.markdown(f"""
            <div style="text-align: center; font-family: 'Courier New', monospace; 
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 30px; border-radius: 15px; margin-bottom: 25px;
                        border: 2px solid #dee2e6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; color: #1976d2; font-weight: bold; margin-bottom: 15px;">
                    {data['multiplicand']}
                </div>
                <div style="font-size: 28px; margin-bottom: 25px;">
                    <span style="color: #333; font-weight: bold;">×</span>
                    <span style="color: #7b1fa2; font-weight: bold; margin-left: 20px;">{data['multiplier']}</span>
                </div>
                <div style="border-bottom: 3px solid #333; margin: 0 auto; width: 80%;"></div>
            </div>
            """, unsafe_allow_html=True)
        
        # First partial product line - better spacing and formatting
        col_a, col_b, col_c = st.columns([0.5, 1, 0.5])
        with col_b:
            if "step1" in data['missing_positions']:
                step1_input = st.number_input(
                    "step1",
                    value=None, step=1, key="input_step1",
                    label_visibility="collapsed",
                    placeholder="Enter answer"
                )
            else:
                st.markdown(f"""
                <div style="text-align: center; font-family: 'Courier New', monospace; 
                            font-size: 26px; color: #4caf50; font-weight: bold; 
                            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%); 
                            padding: 15px; border-radius: 8px; margin: 10px 0;
                            border: 2px solid #4caf50;">
                    {data['step1_result']}
                </div>
                """, unsafe_allow_html=True)
                step1_input = data['step1_result']
        
        # Second partial product line - better alignment and formatting
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        col_plus, col_input, col_space = st.columns([0.3, 1, 0.7])
        
        with col_plus:
            st.markdown("""
            <div style='text-align: center; font-size: 28px; font-weight: bold; 
                        color: #333; padding-top: 15px;'>+</div>
            """, unsafe_allow_html=True)
        
        with col_input:
            if "step2" in data['missing_positions']:
                step2_input = st.number_input(
                    "step2",
                    value=None, step=1, key="input_step2",
                    label_visibility="collapsed",
                    placeholder="Enter answer"
                )
            else:
                st.markdown(f"""
                <div style="text-align: center; font-family: 'Courier New', monospace; 
                            font-size: 26px; color: #ff9800; font-weight: bold;
                            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                            padding: 15px; border-radius: 8px; margin: 10px 0;
                            border: 2px solid #ff9800;">
                    {data['step2_result']}
                </div>
                """, unsafe_allow_html=True)
                step2_input = data['step2_result']
        
        # Horizontal line - better positioned and styled
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        col_line1, col_line2, col_line3 = st.columns([0.8, 2, 0.8])
        with col_line2:
            st.markdown("""
            <div style="border-bottom: 3px solid #333; margin: 20px auto; width: 80%;"></div>
            """, unsafe_allow_html=True)
        
        # Final answer line - better centered and formatted
        col_d, col_e, col_f = st.columns([0.5, 1, 0.5])
        with col_e:
            if "final" in data['missing_positions']:
                final_input = st.number_input(
                    "final",
                    value=None, step=1, key="input_final",
                    label_visibility="collapsed",
                    placeholder="Final answer"
                )
            else:
                st.markdown(f"""
                <div style="text-align: center; font-family: 'Courier New', monospace; 
                            font-size: 30px; color: #e91e63; font-weight: bold;
                            background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
                            padding: 18px; border-radius: 8px; margin: 15px 0;
                            border: 2px solid #e91e63;">
                    {data['final_result']}
                </div>
                """, unsafe_allow_html=True)
                final_input = data['final_result']
    
    # Store the inputs
    user_answers = {}
    if "step1" in data['missing_positions']:
        user_answers['step1'] = step1_input
    else:
        user_answers['step1'] = data['step1_result']
        
    if "step2" in data['missing_positions']:
        user_answers['step2'] = step2_input
    else:
        user_answers['step2'] = data['step2_result']
        
    if "final" in data['missing_positions']:
        user_answers['final'] = final_input
    else:
        user_answers['final'] = data['final_result']
    
    # Add just a helpful reminder if needed - simplified
    if any(pos in data['missing_positions'] for pos in ["step1", "step2", "final"]):
        st.markdown("---")
        with st.expander("💡 **Need Help? Click here for hints**"):
            st.markdown(f"""
            **For this problem ({data['multiplicand']} × {data['multiplier']}):**
            
            • **Step 1:** {data['multiplicand']} × {data['ones_digit']} = {data['step1_result']}
            • **Step 2:** {data['multiplicand']} × {data['tens_digit']}0 = {data['step2_result']}
            • **Final:** {data['step1_result']} + {data['step2_result']} = {data['final_result']}
            
            **Remember:** The second step is multiplying by {data['tens_digit']}0, not just {data['tens_digit']}!
            """)
    
    return user_answers



def show_step_by_step_solution():
    """Show detailed step-by-step solution"""
    data = st.session_state.question_data
    
    st.markdown("---")
    st.markdown("## 🎓 **Step-by-Step Solution**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Setup", "1️⃣ First Step", "2️⃣ Second Step", "➕ Final Answer"])
    
    with tab1:
        st.markdown(f"""
        ### Understanding the Problem: {data['multiplicand']} × {data['multiplier']}
        
        **We use the traditional multiplication algorithm:**
        1. Multiply by the **ones digit** ({data['ones_digit']})
        2. Multiply by the **tens digit** ({data['tens_digit']}) - but remember it's really {data['tens_digit']}0!
        3. Add the two partial products together
        
        **Why this works:**
        {data['multiplier']} = {data['tens_digit']}0 + {data['ones_digit']}
        
        So {data['multiplicand']} × {data['multiplier']} = {data['multiplicand']} × ({data['tens_digit']}0 + {data['ones_digit']})
        = {data['multiplicand']} × {data['tens_digit']}0 + {data['multiplicand']} × {data['ones_digit']}
        """)
    
    with tab2:
        st.markdown(f"""
        ### First Step: Multiply by the Ones Digit
        
        **Calculate: {data['multiplicand']} × {data['ones_digit']}**
        
        Let's break this down if needed:
        """)
        
        # Show the multiplication breakdown for step 1
        if data['step1_result'] >= 100:
            st.markdown(f"""
            {data['multiplicand']} × {data['ones_digit']} = {data['step1_result']}
            
            This goes in the first line of our answer.
            """)
        else:
            st.markdown(f"""
            {data['multiplicand']} × {data['ones_digit']} = {data['step1_result']}
            
            This is straightforward - just regular multiplication!
            """)
        
        st.success(f"✅ **First partial product: {data['step1_result']}**")
    
    with tab3:
        st.markdown(f"""
        ### Second Step: Multiply by the Tens Digit
        
        **Calculate: {data['multiplicand']} × {data['tens_digit']}0**
        
        **Important:** We're multiplying by {data['tens_digit']}0, not just {data['tens_digit']}!
        
        Step by step:
        1. First calculate: {data['multiplicand']} × {data['tens_digit']} = {data['step2_partial']}
        2. Then shift left (multiply by 10): {data['step2_partial']} × 10 = {data['step2_result']}
        
        **Why shift left?** Because we're really multiplying by the tens place!
        """)
        
        st.success(f"✅ **Second partial product: {data['step2_result']}**")
    
    with tab4:
        st.markdown(f"""
        ### Final Step: Add the Partial Products
        
        **Add them together:**
        
        ```
          {data['step1_result']:>4}  ← First partial product
        + {data['step2_result']:>4}  ← Second partial product  
        -------
          {data['final_result']:>4}  ← Final answer
        ```
        
        **Verification:**
        Let's check if this makes sense by estimating:
        - {data['multiplicand']} is about {round(data['multiplicand']/10)*10}
        - {data['multiplier']} is about {round(data['multiplier']/10)*10}  
        - So the answer should be around {round(data['multiplicand']/10)*10 * round(data['multiplier']/10)*10}
        - Our answer {data['final_result']} ✅ looks reasonable!
        """)
        
        st.success(f"🎉 **Final Answer: {data['multiplicand']} × {data['multiplier']} = {data['final_result']}**")
    
    if st.button("❌ Close Step-by-Step Help"):
        st.session_state.show_step_solution = False
        st.rerun()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted and st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.question_data
    user_answers = st.session_state.get('user_answers', {})
    
    all_correct = True
    
    # Check each missing position
    for position in data['missing_positions']:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            
            if user_value != correct_value:
                all_correct = False
                break
    
    if all_correct:
        st.success("🎉 **Excellent! You completed all the steps correctly!**")
        st.balloons()
        
        # Update performance tracking
        st.session_state.correct_streak += 1
        st.session_state.performance_history.append(True)
        
        if st.session_state.correct_streak >= 5:
            st.info("🔥 **Outstanding! You're really mastering the traditional algorithm!**")
        elif st.session_state.correct_streak >= 3:
            st.info("💪 **Great work! You're getting the hang of this!**")
        
        show_complete_solution()
    else:
        st.error("❌ **Some steps need correction. Let's fix them!**")
        
        # Reset streak but track performance
        st.session_state.correct_streak = 0
        st.session_state.performance_history.append(False)
        
        # Show which answers were wrong
        show_wrong_answers(data, user_answers)
        provide_hints(data, user_answers)
        show_complete_solution()

def show_wrong_answers(data, user_answers):
    """Show which specific answers were incorrect"""
    wrong_answers = []
    
    for position in data['missing_positions']:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            if user_value != correct_value:
                step_names = {
                    "step1": f"🟢 First step ({data['multiplicand']} × {data['ones_digit']})",
                    "step2": f"🟠 Second step ({data['multiplicand']} × {data['tens_digit']}0)",
                    "final": "🔴 Final answer"
                }
                wrong_answers.append(f"**{step_names[position]}:** You wrote {user_value}, but it should be {correct_value}")
    
    if wrong_answers:
        st.markdown("**❌ These steps need correction:**")
        for wrong in wrong_answers:
            st.markdown(f"- {wrong}")

def provide_hints(data, user_answers):
    """Provide specific hints based on wrong answers"""
    for position in data['missing_positions']:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            if user_value != correct_value:
                if position == "step1":
                    st.info(f"💡 **Hint for Step 1:** Remember, {data['multiplicand']} × {data['ones_digit']} = {correct_value}")
                elif position == "step2":
                    st.info(f"💡 **Hint for Step 2:** You're multiplying by {data['tens_digit']}0, not {data['tens_digit']}. So {data['multiplicand']} × {data['tens_digit']} = {data['step2_partial']}, then shift left to get {correct_value}")
                elif position == "final":
                    st.info(f"💡 **Hint for Final Answer:** Add {data['step1_result']} + {data['step2_result']} = {correct_value}")

def show_complete_solution():
    """Show the complete worked solution"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Complete Solution**", expanded=True):
        st.markdown(f"""
        ### 🔢 Complete solution for {data['multiplicand']} × {data['multiplier']}:
        
        **Step 1:** {data['multiplicand']} × {data['ones_digit']} = {data['step1_result']}
        
        **Step 2:** {data['multiplicand']} × {data['tens_digit']}0 = {data['step2_result']}
        (First calculate {data['multiplicand']} × {data['tens_digit']} = {data['step2_partial']}, then shift: {data['step2_partial']} × 10 = {data['step2_result']})
        
        **Step 3:** Add the partial products: {data['step1_result']} + {data['step2_result']} = {data['final_result']}
        
        **Final Answer: {data['multiplicand']} × {data['multiplier']} = {data['final_result']}** ✅
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.show_step_solution = False
    st.session_state.user_answers = {}