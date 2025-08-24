import streamlit as st
import random

def run():
    """
    Main function to run the Two-Digit Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/D. Multiplication/multiply_a_two_digit_number_by_a_two_digit_number.py
    """
    # Initialize session state for difficulty and game state
    if "multiplication_difficulty" not in st.session_state:
        st.session_state.multiplication_difficulty = 1  # Start with level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > D. Multiplication**")
    st.title("🧮 Multiply Two-Digit Numbers")
    st.markdown("*Practice multiplying two-digit numbers together*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiplication_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Easy Start (×10s with teens)",
            2: "Building Up (20-50 × 11-19)",
            3: "Standard Practice (20-60 × 11-30)",
            4: "Getting Harder (30-80 × 15-40)",
            5: "Expert Level (40-99 × 11-50)"
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
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Multiply the two numbers** shown
        - **Enter your answer** in the input box
        - **Click Submit** to check your work
        - **Practice both formats** - vertical and horizontal
        
        ### Problem Formats:
        You'll see problems in **two different styles**:
        
        #### Vertical Format:
        ```
           75
        ×  11
        -----
        [answer]
        ```
        
        #### Horizontal Format:
        ```
        20 × 34 = ?
        ```
        
        ### Multiplication Strategies:
        
        #### Method 1: Break it down
        For **23 × 15**:
        - **23 × 10** = 230
        - **23 × 5** = 115  
        - **Add them:** 230 + 115 = **345**
        
        #### Method 2: Standard Algorithm
        ```
           23
        ×  15
        -----
          115  (23 × 5)
         230   (23 × 10)
        -----
         345
        ```
        
        #### Method 3: Area Model
        Break into tens and ones:
        - **20 × 10** = 200
        - **20 × 5** = 100
        - **3 × 10** = 30
        - **3 × 5** = 15
        - **Total:** 200 + 100 + 30 + 15 = **345**
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Easy start (10, 20, 30... × 11-19)
        - **🟡 Level 2:** Building up (20-50 × 11-19)
        - **🟠 Level 3:** Standard practice (20-60 × 11-30)
        - **🔴 Level 4:** Getting harder (30-80 × 15-40)
        - **🔴 Level 5:** Expert level (40-99 × 11-50)
        
        ### Tips:
        - **Look for patterns** (multiples of 10 are easier)
        - **Break numbers down** into tens and ones
        - **Double-check** by estimating first
        - **Practice** makes perfect!
        """)

def generate_new_question():
    """Generate a new two-digit multiplication question based on difficulty"""
    difficulty = st.session_state.multiplication_difficulty
    
    if difficulty == 1:
        # Level 1: Easy combinations with round numbers
        first_options = [10, 20, 30, 40, 50, 60]
        second_options = [11, 12, 13, 14, 15, 16, 17, 18, 19]
        
    elif difficulty == 2:
        # Level 2: One number 11-19, other 20-50
        first_options = list(range(20, 51))
        second_options = list(range(11, 20))
        
    elif difficulty == 3:
        # Level 3: Standard textbook problems
        first_options = list(range(20, 60))
        second_options = list(range(11, 30))
        
    elif difficulty == 4:
        # Level 4: More challenging 
        first_options = list(range(30, 80))
        second_options = list(range(15, 40))
        
    else:  # Level 5
        # Level 5: Expert level (like 75 × 11, 84 × 23, etc.)
        first_options = list(range(40, 99))
        second_options = list(range(11, 50))
    
    # Generate the two numbers
    num1 = random.choice(first_options)
    num2 = random.choice(second_options)
    
    # Randomly choose display format (vertical or horizontal)
    display_format = random.choice(["vertical", "horizontal"])
    
    # Calculate correct answer
    correct_answer = num1 * num2
    
    # Store question data
    st.session_state.question_data = {
        "num1": num1,
        "num2": num2,
        "format": display_format
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"What is {num1} × {num2}?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🧮 Multiply:")
    
    # Create the multiplication display based on format
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if data["format"] == "vertical":
            # Vertical format like traditional worksheets
            st.markdown(f"""
            <div style="
                background-color: #ffffff; 
                padding: 30px; 
                border-radius: 10px; 
                border: 2px solid #dee2e6;
                text-align: center;
                margin: 30px 0;
                font-family: 'Courier New', monospace;
                max-width: 200px;
                margin-left: auto;
                margin-right: auto;
            ">
                <div style="font-size: 32px; font-weight: bold; color: #333; line-height: 1.2;">
                    <div style="text-align: right; padding-right: 20px;">{data['num1']:>3}</div>
                    <div style="text-align: right; padding-right: 20px;">× {data['num2']:>2}</div>
                    <div style="border-top: 2px solid #333; margin: 10px 0; padding-right: 20px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:  # horizontal format
            # Horizontal format like "20 × 34 = ___"
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 30px; 
                border-radius: 10px; 
                border: 2px solid #dee2e6;
                text-align: center;
                margin: 30px 0;
                font-family: 'Arial', sans-serif;
                max-width: 300px;
                margin-left: auto;
                margin-right: auto;
            ">
                <div style="font-size: 32px; font-weight: bold; color: #333;">
                    {data['num1']} × {data['num2']} = ?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("**Enter your answer:**")
            user_answer = st.number_input(
                "Answer:",
                min_value=0,
                max_value=10000,
                value=None,
                step=1,
                placeholder="Type your answer here...",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = user_answer
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
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Track consecutive correct answers
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3 and st.session_state.multiplication_difficulty < 5:
            old_difficulty = st.session_state.multiplication_difficulty
            st.session_state.multiplication_difficulty += 1
            st.session_state.consecutive_correct = 0  # Reset counter
            
            if st.session_state.multiplication_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Amazing! You've reached Expert Level!**")
            else:
                st.info(f"⬆️ **Level Up! Now on Level {st.session_state.multiplication_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,}**.")
        
        # Reset consecutive correct counter
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty if they get it wrong and not at level 1
        if st.session_state.multiplication_difficulty > 1:
            st.session_state.multiplication_difficulty -= 1
            st.warning(f"⬇️ **Don't worry! Moving to Level {st.session_state.multiplication_difficulty} for more practice.**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    num1 = st.session_state.question_data['num1']
    num2 = st.session_state.question_data['num2']
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"### Solving {num1} × {num2}")
        
        # Method 1: Break down approach
        st.markdown("#### Method 1: Break it down")
        
        # Split the second number into tens and ones
        tens_part = (num2 // 10) * 10
        ones_part = num2 % 10
        
        if tens_part > 0 and ones_part > 0:
            step1 = num1 * tens_part
            step2 = num1 * ones_part
            st.markdown(f"""
            - **{num1} × {tens_part}** = {step1:,}
            - **{num1} × {ones_part}** = {step2:,}
            - **Add them:** {step1:,} + {step2:,} = **{correct_answer:,}**
            """)
        else:
            st.markdown(f"**{num1} × {num2} = {correct_answer:,}**")
        
        # Method 2: Standard Algorithm
        st.markdown("#### Method 2: Standard Algorithm")
        
        # Show the vertical multiplication format
        if ones_part > 0 and tens_part > 0:
            line1 = num1 * ones_part
            line2 = num1 * tens_part
            st.markdown(f"""
            ```
               {num1:>2}
            ×  {num2:>2}
            -----
            {line1:>5}  ({num1} × {ones_part})
           {line2:>4}   ({num1} × {tens_part})
            -----
           {correct_answer:>4}
            ```
            """)
        
        # Method 3: Area Model (for more complex cases)
        if num1 >= 20 and num2 >= 20:
            st.markdown("#### Method 3: Area Model")
            
            # Break both numbers into tens and ones
            num1_tens = (num1 // 10) * 10
            num1_ones = num1 % 10
            num2_tens = (num2 // 10) * 10
            num2_ones = num2 % 10
            
            # Calculate each part
            part1 = num1_tens * num2_tens
            part2 = num1_tens * num2_ones
            part3 = num1_ones * num2_tens
            part4 = num1_ones * num2_ones
            
            st.markdown(f"""
            Break into parts:
            - **{num1_tens} × {num2_tens}** = {part1:,}
            - **{num1_tens} × {num2_ones}** = {part2:,}
            - **{num1_ones} × {num2_tens}** = {part3:,}
            - **{num1_ones} × {num2_ones}** = {part4:,}
            - **Total:** {part1:,} + {part2:,} + {part3:,} + {part4:,} = **{correct_answer:,}**
            """)
        
        # Quick estimation check
        st.markdown("#### Quick Check:")
        estimate_num1 = round(num1, -1)  # Round to nearest 10
        estimate_num2 = round(num2, -1)  # Round to nearest 10
        estimate = estimate_num1 * estimate_num2
        st.markdown(f"**Estimate:** {estimate_num1} × {estimate_num2} ≈ {estimate:,}")
        st.markdown(f"**Actual:** {correct_answer:,} ✓")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer