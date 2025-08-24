import streamlit as st
import random

def run():
    """
    Main function to run the Box Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/D. Multiplication/box_multiplication.py
    """
    # Initialize session state for difficulty and game state
    if "box_mult_difficulty" not in st.session_state:
        st.session_state.box_mult_difficulty = 1  # Start with level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > D. Multiplication**")
    st.title("📦 Box Multiplication")
    st.markdown("*Use the area model to break down multiplication problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.box_mult_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Easy Start (×10s and teens)",
            2: "Building Up (×20s with teens)",
            3: "Standard Practice (×20s-×30s)",
            4: "Getting Harder (×40s-×60s)",
            5: "Expert Challenge (×70s-×90s)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
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
    with st.expander("💡 **Instructions & Box Method Guide**", expanded=False):
        st.markdown("""
        ### How the Box Method Works:
        
        The **box method** (also called area model) breaks multiplication into easier parts:
        
        #### Example: 25 × 24
        
        **Step 1:** Break down each number
        - **25** = 20 + 5
        - **24** = 20 + 4
        
        **Step 2:** Create a box grid
        ```
             20  +  5
        20 | 400 | 100 |
        +  |-----|-----|
        4  |  80 |  20 |
        ```
        
        **Step 3:** Multiply each section
        - **20 × 20** = 400
        - **20 × 5** = 100  
        - **4 × 20** = 80
        - **4 × 5** = 20
        
        **Step 4:** Add all parts
        - **400 + 100 + 80 + 20 = 600**
        
        ### Why This Method Works:
        - **Visual:** You can see each part clearly
        - **Easier:** Breaks big problems into smaller ones
        - **Understanding:** Shows what multiplication really means
        - **Flexible:** Works for any size numbers
        
        ### Tips:
        - **Break into tens and ones** (like 25 = 20 + 5)
        - **Fill the grid carefully** - multiply row × column
        - **Add step by step** to avoid mistakes
        - **Check your work** by estimating first
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Easy start (×10s and teens)
        - **🟡 Level 2:** Building up (×20s with teens)
        - **🟠 Level 3:** Standard practice (×20s-×30s)
        - **🔴 Level 4:** Getting harder (×40s-×60s)
        - **🔴 Level 5:** Expert challenge (×70s-×90s)
        """)

def generate_new_question():
    """Generate a new box multiplication question based on difficulty"""
    difficulty = st.session_state.box_mult_difficulty
    
    if difficulty == 1:
        # Level 1: Easy start with tens and teens
        first_options = [10, 20, 30]
        second_options = list(range(11, 17))  # 11-16
        
    elif difficulty == 2:
        # Level 2: Building up
        first_options = list(range(20, 31))  # 20-30
        second_options = list(range(11, 20))  # 11-19
        
    elif difficulty == 3:
        # Level 3: Standard practice
        first_options = list(range(20, 40))   # 20-39
        second_options = list(range(12, 30))  # 12-29
        
    elif difficulty == 4:
        # Level 4: Getting harder
        first_options = list(range(30, 70))   # 30-69
        second_options = list(range(15, 40))  # 15-39
        
    else:  # Level 5
        # Level 5: Expert challenge
        first_options = list(range(40, 100))  # 40-99
        second_options = list(range(20, 60))  # 20-59
    
    # Generate the two numbers
    num1 = random.choice(first_options)
    num2 = random.choice(second_options)
    
    # Break down into tens and ones
    num1_tens = (num1 // 10) * 10
    num1_ones = num1 % 10
    num2_tens = (num2 // 10) * 10
    num2_ones = num2 % 10
    
    # Calculate each box
    box_tl = num1_tens * num2_tens  # top-left
    box_tr = num1_tens * num2_ones  # top-right  
    box_bl = num1_ones * num2_tens  # bottom-left
    box_br = num1_ones * num2_ones  # bottom-right
    
    # Calculate correct answer
    correct_answer = num1 * num2
    
    # Store question data
    st.session_state.question_data = {
        "num1": num1,
        "num2": num2,
        "num1_tens": num1_tens,
        "num1_ones": num1_ones,
        "num2_tens": num2_tens,
        "num2_ones": num2_ones,
        "box_tl": box_tl,
        "box_tr": box_tr,
        "box_bl": box_bl,
        "box_br": box_br
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Use the box method to find {num1} × {num2}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question title
    st.markdown(f"### {st.session_state.current_question}")
    st.markdown("*Calculate the sums in the grid. Add these sums to find the final answer.*")
    
    # Display the main equation
    st.markdown(f"""
    <div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; color: #333;">
        {data['num1']} × {data['num2']} = ???
    </div>
    """, unsafe_allow_html=True)
    
    # Create the box multiplication grid using Streamlit components
    st.markdown(f"**Break down: {data['num1']} = {data['num1_tens']} + {data['num1_ones']} and {data['num2']} = {data['num2_tens']} + {data['num2_ones']}**")
    
    # Create visual grid using columns and containers
    st.markdown("### 📦 Box Method Grid:")
    
    # Use form for the entire grid
    with st.form("box_grid_form", clear_on_submit=False):
        # Header row showing breakdown
        col_empty, col_header1, col_header2, col_sum = st.columns([1, 2, 2, 1])
        with col_header1:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;'>{data['num2_tens']}</div>", unsafe_allow_html=True)
        with col_header2:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;'>{data['num2_ones']}</div>", unsafe_allow_html=True)
        with col_sum:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;'>Sum</div>", unsafe_allow_html=True)
        
        # First row with input
        col_label1, col_box1, col_box2, col_sum1 = st.columns([1, 2, 2, 1])
        with col_label1:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f0f0f0; padding: 15px; border: 1px solid #ccc;'>{data['num1_tens']}</div>", unsafe_allow_html=True)
        with col_box1:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #e3f2fd; padding: 15px; border: 2px solid #333; font-size: 18px;'>{data['box_tl']}</div>", unsafe_allow_html=True)
        with col_box2:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f3e5f5; padding: 15px; border: 2px solid #333; font-size: 18px;'>{data['box_tr']}</div>", unsafe_allow_html=True)
        with col_sum1:
            sum1 = st.number_input("", min_value=0, max_value=10000, value=None, key="sum1_grid", label_visibility="collapsed", placeholder="sum")
        
        # Second row with input
        col_label2, col_box3, col_box4, col_sum2 = st.columns([1, 2, 2, 1])
        with col_label2:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #f0f0f0; padding: 15px; border: 1px solid #ccc;'>{data['num1_ones']}</div>", unsafe_allow_html=True)
        with col_box3:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #fff9c4; padding: 15px; border: 2px solid #333; font-size: 18px;'>{data['box_bl']}</div>", unsafe_allow_html=True)
        with col_box4:
            st.markdown(f"<div style='text-align: center; font-weight: bold; background-color: #fce4ec; padding: 15px; border: 2px solid #333; font-size: 18px;'>{data['box_br']}</div>", unsafe_allow_html=True)
        with col_sum2:
            sum2 = st.number_input("", min_value=0, max_value=10000, value=None, key="sum2_grid", label_visibility="collapsed", placeholder="sum")
        
        # Final answer row with input
        col_final_label, col_final_empty1, col_final_empty2, col_final_answer = st.columns([1, 2, 2, 1])
        with col_final_label:
            st.markdown("<div style='text-align: center; font-weight: bold; background-color: #f8f9fa; padding: 15px; border: 1px solid #ccc; font-size: 14px;'>Final<br>Answer</div>", unsafe_allow_html=True)
        with col_final_empty1:
            st.markdown("<div style='padding: 15px; border: 1px solid #ccc;'></div>", unsafe_allow_html=True)
        with col_final_empty2:
            st.markdown("<div style='padding: 15px; border: 1px solid #ccc;'></div>", unsafe_allow_html=True)
        with col_final_answer:
            final_answer = st.number_input("", min_value=0, max_value=50000, value=None, key="final_grid", label_visibility="collapsed", placeholder="total")
        
        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            # Check all answers
            expected_sum1 = data['box_tl'] + data['box_tr']
            expected_sum2 = data['box_bl'] + data['box_br']
            expected_final = st.session_state.correct_answer
            
            st.session_state.user_answers = {
                "sum1": sum1,
                "sum2": sum2, 
                "final": final_answer,
                "expected_sum1": expected_sum1,
                "expected_sum2": expected_sum2,
                "expected_final": expected_final
            }
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
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answers"""
    answers = st.session_state.user_answers
    
    # Check each part
    sum1_correct = answers["sum1"] == answers["expected_sum1"]
    sum2_correct = answers["sum2"] == answers["expected_sum2"] 
    final_correct = answers["final"] == answers["expected_final"]
    
    # Show feedback for each step
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if sum1_correct:
            st.success(f"✅ Top sum: {answers['sum1']} ✓")
        else:
            st.error(f"❌ Top sum: {answers['expected_sum1']} (you put {answers['sum1']})")
    
    with col2:
        if sum2_correct:
            st.success(f"✅ Bottom sum: {answers['sum2']} ✓")
        else:
            st.error(f"❌ Bottom sum: {answers['expected_sum2']} (you put {answers['sum2']})")
    
    with col3:
        if final_correct:
            st.success(f"✅ Final: {answers['final']} ✓")
        else:
            st.error(f"❌ Final: {answers['expected_final']} (you put {answers['final']})")
    
    # Overall feedback
    if sum1_correct and sum2_correct and final_correct:
        st.success("🎉 **Perfect! You mastered the box method!**")
        
        # Track consecutive correct answers
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive perfect answers
        if st.session_state.consecutive_correct >= 3 and st.session_state.box_mult_difficulty < 5:
            old_difficulty = st.session_state.box_mult_difficulty
            st.session_state.box_mult_difficulty += 1
            st.session_state.consecutive_correct = 0
            
            if st.session_state.box_mult_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Outstanding! You've reached Expert Level!**")
            else:
                st.info(f"⬆️ **Level Up! Now on Level {st.session_state.box_mult_difficulty}**")
    
    else:
        # Reset consecutive correct counter
        st.session_state.consecutive_correct = 0
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if they get multiple parts wrong
        wrong_count = sum([not sum1_correct, not sum2_correct, not final_correct])
        if wrong_count >= 2 and st.session_state.box_mult_difficulty > 1:
            st.session_state.box_mult_difficulty -= 1
            st.warning(f"⬇️ **Moving to Level {st.session_state.box_mult_difficulty} for more practice.**")

def show_explanation():
    """Show step-by-step explanation"""
    data = st.session_state.question_data
    answers = st.session_state.user_answers
    
    with st.expander("📖 **Step-by-step solution**", expanded=True):
        st.markdown(f"### Box Method for {data['num1']} × {data['num2']}")
        
        st.markdown("#### Step 1: Break down the numbers")
        st.markdown(f"- **{data['num1']}** = {data['num1_tens']} + {data['num1_ones']}")
        st.markdown(f"- **{data['num2']}** = {data['num2_tens']} + {data['num2_ones']}")
        
        st.markdown("#### Step 2: Fill the boxes")
        st.markdown(f"""
        - **Top-left:** {data['num1_tens']} × {data['num2_tens']} = {data['box_tl']}
        - **Top-right:** {data['num1_tens']} × {data['num2_ones']} = {data['box_tr']}
        - **Bottom-left:** {data['num1_ones']} × {data['num2_tens']} = {data['box_bl']}
        - **Bottom-right:** {data['num1_ones']} × {data['num2_ones']} = {data['box_br']}
        """)
        
        st.markdown("#### Step 3: Add the sums")
        st.markdown(f"- **Top row:** {data['box_tl']} + {data['box_tr']} = {answers['expected_sum1']}")
        st.markdown(f"- **Bottom row:** {data['box_bl']} + {data['box_br']} = {answers['expected_sum2']}")
        
        st.markdown("#### Step 4: Final answer")
        st.markdown(f"**{answers['expected_sum1']} + {answers['expected_sum2']} = {answers['expected_final']}**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answers" in st.session_state:
        del st.session_state.user_answers