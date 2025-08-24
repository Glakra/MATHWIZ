import streamlit as st
import random

def run():
    """
    Main function to run the Round Decimals practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/round_decimals.py
    """
    # Initialize session state for difficulty and game state
    if "round_decimals_difficulty" not in st.session_state:
        st.session_state.round_decimals_difficulty = 1  # Start with whole numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Round Decimals")
    st.markdown("*Round decimal numbers to different place values*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.round_decimals_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Nearest whole number",
            2: "Nearest tenth", 
            3: "Nearest hundredth",
            4: "Mixed rounding",
            5: "Advanced rounding"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
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
        - **Read the decimal number** and the rounding instruction
        - **Type your answer** in the input box
        - **Remember the rounding rules** - look at the digit to the right
        
        ### Rounding Rules:
        - **Look at the digit to the right** of the place you're rounding to
        - **If it's 5 or greater:** Round UP
        - **If it's less than 5:** Round DOWN
        
        ### Examples:
        - **7.8148 to nearest tenth:** Look at 1 (hundredths) → 7.8
        - **6.8 to nearest whole:** Look at 8 (tenths) → 7
        - **2.074 to nearest hundredth:** Look at 4 (thousandths) → 2.07
        
        ### Place Values:
        - **Whole number:** 6.8 → 7
        - **Tenth (1 decimal place):** 7.81 → 7.8
        - **Hundredth (2 decimal places):** 2.074 → 2.07
        - **Thousandth (3 decimal places):** 5.1234 → 5.123
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Round to nearest whole number
        - **🟡 Level 2:** Round to nearest tenth
        - **🟠 Level 3:** Round to nearest hundredth  
        - **🔴 Level 4:** Mixed rounding practice
        - **🔴 Level 5:** Advanced decimals
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all rounding levels!
        """)

def generate_new_question():
    """Generate a new rounding question based on difficulty level"""
    difficulty = st.session_state.round_decimals_difficulty
    
    # Define question types by difficulty
    if difficulty == 1:
        # Round to nearest whole number
        number = round(random.uniform(1, 20) + random.random(), 1)
        rounding_place = "whole number"
        correct_answer = round(number)
        
    elif difficulty == 2:
        # Round to nearest tenth
        number = round(random.uniform(1, 20) + random.random() * 0.9999, 4)
        rounding_place = "tenth"
        correct_answer = round(number, 1)
        
    elif difficulty == 3:
        # Round to nearest hundredth
        number = round(random.uniform(1, 20) + random.random() * 0.9999, 4)
        rounding_place = "hundredth"
        correct_answer = round(number, 2)
        
    elif difficulty == 4:
        # Mixed rounding
        places = ["whole number", "tenth", "hundredth"]
        rounding_place = random.choice(places)
        number = round(random.uniform(1, 50) + random.random() * 0.9999, 4)
        
        if rounding_place == "whole number":
            correct_answer = round(number)
        elif rounding_place == "tenth":
            correct_answer = round(number, 1)
        else:  # hundredth
            correct_answer = round(number, 2)
            
    else:  # difficulty == 5
        # Advanced rounding with larger numbers
        places = ["whole number", "tenth", "hundredth", "thousandth"]
        rounding_place = random.choice(places)
        number = round(random.uniform(10, 1000) + random.random() * 0.9999, 5)
        
        if rounding_place == "whole number":
            correct_answer = round(number)
        elif rounding_place == "tenth":
            correct_answer = round(number, 1)
        elif rounding_place == "hundredth":
            correct_answer = round(number, 2)
        else:  # thousandth
            correct_answer = round(number, 3)
    
    # Store question data
    st.session_state.question_data = {
        "number": number,
        "rounding_place": rounding_place
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"What is {number} rounded to the nearest {rounding_place}?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🔢 Question:")
    
    # Display the question in a highlighted box like the images (no stars/bold formatting)
    question_text = f"What is {data['number']} rounded to the nearest {data['rounding_place']}?"
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        border-left: 4px solid #007acc;
        font-size: 20px;
        margin: 20px 0;
        color: #333;
    ">
        {question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input - styled like the images
    st.markdown("**Enter your answer:**")
    
    # Create a form for better UX
    with st.form("answer_form", clear_on_submit=False):
        # Text input styled to match the images
        user_input = st.text_input(
            "Answer:", 
            key="answer_input",  # Changed key to avoid conflict
            placeholder="Type your answer here...",
            label_visibility="collapsed"
        )
        
        # Submit button styled like the images
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit_button = st.form_submit_button(
                "Submit", 
                type="primary",
                use_container_width=True
            )
        
        if submit_button and user_input:
            try:
                # Convert user input to float for comparison
                user_answer = float(user_input.strip())
                st.session_state.submitted_answer = user_answer  # Use different session state key
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            except ValueError:
                st.error("❌ Please enter a valid number.")
    
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
    user_answer = st.session_state.submitted_answer  # Updated to use new session state key
    correct_answer = st.session_state.correct_answer
    
    # Check if answers match (allowing for floating point precision issues)
    if abs(user_answer - correct_answer) < 0.0001:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.round_decimals_difficulty
        st.session_state.round_decimals_difficulty = min(
            st.session_state.round_decimals_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.round_decimals_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal rounding!**")
        elif old_difficulty < st.session_state.round_decimals_difficulty:
            difficulty_names = {
                2: "nearest tenth",
                3: "nearest hundredth", 
                4: "mixed rounding",
                5: "advanced rounding"
            }
            next_level = difficulty_names.get(st.session_state.round_decimals_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{format_answer(correct_answer)}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    number = data['number']
    rounding_place = data['rounding_place']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step rounding:
        
        **Original number:** {number}
        **Round to nearest:** {rounding_place}
        **Answer:** {format_answer(correct_answer)}
        
        ### How to solve:
        """)
        
        # Show the rounding process
        if rounding_place == "whole number":
            decimal_part = number - int(number)
            digit_to_check = int(str(f"{decimal_part:.1f}").split('.')[1][0])
            
            st.markdown(f"""
            1. **Look at the tenths place:** {digit_to_check}
            2. **Since {digit_to_check} is {"≥ 5" if digit_to_check >= 5 else "< 5"}:** {"Round UP" if digit_to_check >= 5 else "Round DOWN"}
            3. **Answer:** {format_answer(correct_answer)}
            """)
            
        elif rounding_place == "tenth":
            # Find the hundredths digit
            number_str = f"{number:.4f}"
            hundredths_digit = int(number_str.split('.')[1][1]) if len(number_str.split('.')[1]) > 1 else 0
            
            st.markdown(f"""
            1. **Look at the hundredths place:** {hundredths_digit}
            2. **Since {hundredths_digit} is {"≥ 5" if hundredths_digit >= 5 else "< 5"}:** {"Round UP" if hundredths_digit >= 5 else "Round DOWN"}
            3. **Answer:** {format_answer(correct_answer)}
            """)
            
        elif rounding_place == "hundredth":
            # Find the thousandths digit
            number_str = f"{number:.4f}"
            thousandths_digit = int(number_str.split('.')[1][2]) if len(number_str.split('.')[1]) > 2 else 0
            
            st.markdown(f"""
            1. **Look at the thousandths place:** {thousandths_digit}
            2. **Since {thousandths_digit} is {"≥ 5" if thousandths_digit >= 5 else "< 5"}:** {"Round UP" if thousandths_digit >= 5 else "Round DOWN"}
            3. **Answer:** {format_answer(correct_answer)}
            """)
        
        # General rounding reminder
        st.markdown("""
        ### 💡 Remember:
        - **Look at the digit to the RIGHT** of where you're rounding
        - **If it's 5 or more:** Round UP
        - **If it's less than 5:** Round DOWN
        """)

def format_answer(answer):
    """Format the answer to remove unnecessary trailing zeros"""
    if answer == int(answer):
        return str(int(answer))
    else:
        return str(answer).rstrip('0').rstrip('.')

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "submitted_answer" in st.session_state:  # Updated to use new session state key
        del st.session_state.submitted_answer