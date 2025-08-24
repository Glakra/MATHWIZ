import streamlit as st
import random

def run():
    """
    Main function to run the Rounding practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/rounding.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "rounding_numbers_difficulty" not in st.session_state:
        st.session_state.rounding_numbers_difficulty = 3  # Start with 3-digit numbers
    
    if "rounding_numbers_current_question" not in st.session_state:
        st.session_state.rounding_numbers_current_question = None
        st.session_state.rounding_numbers_correct_answer = None
        st.session_state.rounding_numbers_show_feedback = False
        st.session_state.rounding_numbers_answer_submitted = False
        st.session_state.rounding_numbers_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🎯 Rounding")
    st.markdown("*Round numbers to the nearest ten, hundred, or thousand*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.rounding_numbers_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (2 to 5 digits)
        progress = (difficulty_level - 2) / 3  # Convert 2-5 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level <= 3:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 4:
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
    if st.session_state.rounding_numbers_current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the number** shown
        - **Round it** to the specified place value
        - **Type your answer** in the text box
        
        ### Rounding Rules:
        - **Look at the digit to the right** of the rounding place
        - **If it's 5 or more:** Round UP
        - **If it's 4 or less:** Round DOWN
        - **Replace digits to the right** with zeros
        
        ### Examples:
        **Rounding to nearest ten:**
        - **347** → Look at 7 → Round UP → **350**
        - **342** → Look at 2 → Round DOWN → **340**
        
        **Rounding to nearest hundred:**
        - **1,678** → Look at 7 → Round UP → **1,700**
        - **1,634** → Look at 3 → Round DOWN → **1,600**
        
        **Rounding to nearest thousand:**
        - **15,789** → Look at 7 → Round UP → **16,000**
        - **15,234** → Look at 2 → Round DOWN → **15,000**
        
        ### Difficulty Levels:
        - **🟡 2-3 digit numbers:** (10s - 100s)
        - **🟠 4 digit numbers:** (1,000s)  
        - **🔴 5 digit numbers:** (10,000s)
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 5-digit number rounding!
        """)

def round_number(num, place):
    """Round number to specified place value"""
    if place == "ten":
        return round(num, -1)
    elif place == "hundred":
        return round(num, -2)
    elif place == "thousand":
        return round(num, -3)
    else:
        return num

def generate_new_question():
    """Generate a new rounding question"""
    digits = st.session_state.rounding_numbers_difficulty
    
    # Generate a random number with the specified number of digits
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    number = random.randint(min_val, max_val)
    
    # Choose rounding place based on number size
    if digits <= 2:
        place_options = ["ten"]
    elif digits == 3:
        place_options = ["ten", "hundred"]
    else:
        place_options = ["ten", "hundred", "thousand"]
    
    place = random.choice(place_options)
    
    place_labels = {
        "ten": "nearest ten",
        "hundred": "nearest hundred", 
        "thousand": "nearest thousand"
    }
    
    place_label = place_labels[place]
    correct_answer = int(round_number(number, place))
    
    st.session_state.rounding_numbers_question_data = {
        "number": number,
        "place": place,
        "place_label": place_label
    }
    st.session_state.rounding_numbers_correct_answer = str(correct_answer)
    st.session_state.rounding_numbers_current_question = f"What is **{number:,}** rounded to the **{place_label}**?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.rounding_numbers_question_data
    
    # Display question with nice formatting
    st.markdown("### 🎯 Question:")
    st.markdown(st.session_state.rounding_numbers_current_question)
    
    # Display the number and rounding instruction in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #1f77b4;
        font-size: 24px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #1f77b4;
    ">
        Round {data['number']:,} to the {data['place_label']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Type your answer:**")
        
        user_answer = st.text_input(
            "Your answer:",
            placeholder="Enter your answer",
            key="rounding_numbers_input",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer.strip():
            st.session_state.rounding_numbers_user_answer = user_answer.strip()
            st.session_state.rounding_numbers_show_feedback = True
            st.session_state.rounding_numbers_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.rounding_numbers_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.rounding_numbers_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.rounding_numbers_user_answer
    correct_answer = st.session_state.rounding_numbers_correct_answer
    
    # Clean user input (remove commas and spaces)
    cleaned_user_answer = user_answer.replace(",", "").replace(" ", "")
    
    if cleaned_user_answer == correct_answer:
        st.success("🎉 **Excellent! Nice rounding.**")
        
        # Increase difficulty (max 5 digits)
        old_difficulty = st.session_state.rounding_numbers_difficulty
        st.session_state.rounding_numbers_difficulty = min(
            st.session_state.rounding_numbers_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.rounding_numbers_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 5-digit number rounding!**")
        elif old_difficulty < st.session_state.rounding_numbers_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.rounding_numbers_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{int(correct_answer):,}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.rounding_numbers_difficulty
        st.session_state.rounding_numbers_difficulty = max(
            st.session_state.rounding_numbers_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.rounding_numbers_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.rounding_numbers_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.rounding_numbers_question_data
    number = data['number']
    place = data['place']
    place_label = data['place_label']
    correct_answer = int(st.session_state.rounding_numbers_correct_answer)
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step rounding: {number:,} → {correct_answer:,}
        
        **Rounding {number:,} to the {place_label}:**
        """)
        
        # Identify the key digit to look at
        if place == "ten":
            # Look at the ones digit
            key_digit = number % 10
            place_value = (number // 10) * 10
            st.markdown(f"1. **Look at the ones digit:** {key_digit}")
            
        elif place == "hundred":
            # Look at the tens digit
            key_digit = (number // 10) % 10
            place_value = (number // 100) * 100
            st.markdown(f"1. **Look at the tens digit:** {key_digit}")
            
        else:  # thousand
            # Look at the hundreds digit
            key_digit = (number // 100) % 10
            place_value = (number // 1000) * 1000
            st.markdown(f"1. **Look at the hundreds digit:** {key_digit}")
        
        # Explain the rounding rule
        if key_digit >= 5:
            st.markdown(f"2. **Since {key_digit} ≥ 5:** Round UP")
            if place == "ten":
                st.markdown(f"3. **Round {place_value:,} up to {place_value + 10:,}**")
            elif place == "hundred":
                st.markdown(f"3. **Round {place_value:,} up to {place_value + 100:,}**")
            else:
                st.markdown(f"3. **Round {place_value:,} up to {place_value + 1000:,}**")
        else:
            st.markdown(f"2. **Since {key_digit} < 5:** Round DOWN")
            st.markdown(f"3. **Keep {place_value:,}**")
        
        st.markdown(f"**Final answer:** {correct_answer:,}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.rounding_numbers_current_question = None
    st.session_state.rounding_numbers_correct_answer = None
    st.session_state.rounding_numbers_show_feedback = False
    st.session_state.rounding_numbers_answer_submitted = False
    st.session_state.rounding_numbers_question_data = {}
    if "rounding_numbers_user_answer" in st.session_state:
        del st.session_state.rounding_numbers_user_answer