import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Products practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/estimate_products.py
    """
    # Initialize session state for difficulty and game state
    if "estimate_difficulty" not in st.session_state:
        st.session_state.estimate_difficulty = 1  # Start with basic estimation
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.estimate_score = 0
        st.session_state.total_questions = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📊 Estimate Products")
    st.markdown("*Round and estimate multiplication products*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.estimate_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Round to Tens", 2: "Round to Hundreds", 3: "Mixed Rounding"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Round to Tens')}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
        
        # Show score
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.estimate_score / st.session_state.total_questions) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
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
    with st.expander("💡 **Instructions & Estimation Guide**", expanded=False):
        st.markdown("""
        ### How to Estimate Products:
        
        #### 🔹 **Step 1: Round**
        - **Round to nearest ten:** Look at the ones digit
          - 0-4: Round down (23 → 20)
          - 5-9: Round up (27 → 30)
        - **Round to nearest hundred:** Look at the tens digit
          - 0-4: Round down (234 → 200)
          - 5-9: Round up (267 → 300)
        
        #### 🔹 **Step 2: Multiply**
        - Multiply the rounded number by the other factor
        - Use mental math with the easier numbers
        
        #### 🔹 **Examples:**
        - **29 × 5:** Round 29 to 30, then 30 × 5 = 150
        - **7 × 324:** Round 324 to 300, then 7 × 300 = 2,100
        - **48 × 23:** Round 48 to 50, then 50 × 23 = 1,150
        
        ### Tips for Success:
        - **Read carefully:** Which factor should you round?
        - **Round to the correct place:** Tens, hundreds, etc.
        - **Use mental math:** Rounded numbers are easier to multiply
        - **Check reasonableness:** Is your estimate close to what you'd expect?
        
        ### Difficulty Levels:
        - **🟢 Round to Tens:** Round one factor to nearest 10
        - **🟡 Round to Hundreds:** Round one factor to nearest 100  
        - **🔴 Mixed Rounding:** Different rounding rules and larger numbers
        
        ### Scoring:
        - ✅ **Exact match:** Full points
        - ⚠️ **Close estimate:** Partial credit for reasonable estimates
        - ❌ **Far off:** Try again with the rounding steps
        """)

def generate_new_question():
    """Generate a new estimation question"""
    difficulty = st.session_state.estimate_difficulty
    
    if difficulty == 1:
        # Level 1: Round to nearest ten
        rounding_options = [
            {"place": "ten", "factor": "first"},
            {"place": "ten", "factor": "second"}
        ]
        
        # Generate numbers where one needs rounding to tens
        if random.choice([True, False]):
            # Round first factor to tens
            first = random.randint(21, 99)  # Number to round
            second = random.randint(2, 9)   # Single digit multiplier
            round_factor = "first"
            round_place = "ten"
        else:
            # Round second factor to tens  
            first = random.randint(2, 9)    # Single digit multiplier
            second = random.randint(21, 99) # Number to round
            round_factor = "second" 
            round_place = "ten"
            
    elif difficulty == 2:
        # Level 2: Round to nearest hundred
        if random.choice([True, False]):
            # Round first factor to hundreds
            first = random.randint(150, 999)  # Number to round
            second = random.randint(2, 9)     # Single digit multiplier
            round_factor = "first"
            round_place = "hundred"
        else:
            # Round second factor to hundreds
            first = random.randint(2, 12)     # Small multiplier
            second = random.randint(150, 999) # Number to round
            round_factor = "second"
            round_place = "hundred"
            
    else:  # difficulty == 3
        # Level 3: Mixed rounding (tens, hundreds, thousands)
        round_options = [
            {"place": "ten", "range": (21, 99)},
            {"place": "hundred", "range": (150, 999)},
            {"place": "thousand", "range": (1500, 9999)}
        ]
        
        chosen_round = random.choice(round_options)
        round_place = chosen_round["place"]
        
        if random.choice([True, False]):
            # Round first factor
            first = random.randint(*chosen_round["range"])
            second = random.randint(2, 15)
            round_factor = "first"
        else:
            # Round second factor
            first = random.randint(2, 15)
            second = random.randint(*chosen_round["range"])
            round_factor = "second"
    
    # Calculate the correct estimated answer
    if round_factor == "first":
        if round_place == "ten":
            rounded_first = round_to_nearest_ten(first)
            estimated_product = rounded_first * second
        elif round_place == "hundred":
            rounded_first = round_to_nearest_hundred(first)
            estimated_product = rounded_first * second
        else:  # thousand
            rounded_first = round_to_nearest_thousand(first)
            estimated_product = rounded_first * second
    else:  # round_factor == "second"
        if round_place == "ten":
            rounded_second = round_to_nearest_ten(second)
            estimated_product = first * rounded_second
        elif round_place == "hundred":
            rounded_second = round_to_nearest_hundred(second)
            estimated_product = first * rounded_second
        else:  # thousand
            rounded_second = round_to_nearest_thousand(second)
            estimated_product = first * rounded_second
    
    # Create instruction text
    place_text = {
        "ten": "nearest ten",
        "hundred": "nearest hundred", 
        "thousand": "nearest thousand"
    }
    
    if round_factor == "first":
        instruction = f"Estimate the product. Round the first factor to the {place_text[round_place]}, and then multiply."
    else:
        instruction = f"Estimate the product. Round the second factor to the {place_text[round_place]}, and then multiply."
    
    st.session_state.question_data = {
        "first": first,
        "second": second,
        "round_factor": round_factor,
        "round_place": round_place,
        "estimated_product": estimated_product,
        "instruction": instruction
    }
    st.session_state.correct_answer = estimated_product
    st.session_state.current_question = instruction

def round_to_nearest_ten(num):
    """Round number to nearest ten"""
    return round(num / 10) * 10

def round_to_nearest_hundred(num):
    """Round number to nearest hundred"""
    return round(num / 100) * 100

def round_to_nearest_thousand(num):
    """Round number to nearest thousand"""
    return round(num / 1000) * 1000

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display instruction
    st.markdown("### 📝 Question:")
    st.markdown(f"**{data['instruction']}**")
    
    # Display the multiplication problem in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #FF9800;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        font-weight: bold;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    ">
        {data['first']} × {data['second']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("**The product is approximately:**")
            user_answer = st.number_input(
                "Enter your estimate:",
                min_value=0,
                max_value=1000000,
                value=None,
                step=1,
                key="estimate_input",
                label_visibility="collapsed",
                placeholder="Enter your estimate"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = int(user_answer)
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.session_state.total_questions += 1
    
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
    data = st.session_state.question_data
    
    # Check if answer is exactly correct
    if user_answer == correct_answer:
        st.success("🎉 **Perfect! That's the exact estimated product!**")
        st.session_state.estimate_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.estimate_score / st.session_state.total_questions
            if accuracy >= 0.75 and st.session_state.estimate_difficulty < 3:
                old_difficulty = st.session_state.estimate_difficulty
                st.session_state.estimate_difficulty += 1
                if old_difficulty < st.session_state.estimate_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.estimate_difficulty}**")
                    if st.session_state.estimate_difficulty == 3:
                        st.balloons()
    
    # Check if answer is reasonably close (within 10% for partial credit)
    elif abs(user_answer - correct_answer) <= (correct_answer * 0.1):
        st.warning("⚠️ **Close! Your estimate is reasonable, but not exact.**")
        st.session_state.estimate_score += 0.5  # Partial credit
        st.info(f"💡 **The exact estimated product is {correct_answer:,}**")
    
    else:
        st.error(f"❌ **Not quite right.** The estimated product should be **{correct_answer:,}**.")
        
        # Decrease difficulty if struggling  
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.estimate_score / st.session_state.total_questions
            if accuracy < 0.4 and st.session_state.estimate_difficulty > 1:
                old_difficulty = st.session_state.estimate_difficulty
                st.session_state.estimate_difficulty = max(st.session_state.estimate_difficulty - 1, 1)
                if old_difficulty > st.session_state.estimate_difficulty:
                    st.warning(f"⬇️ **Let's practice easier rounding. Back to Level {st.session_state.estimate_difficulty}**")
    
    # Always show explanation for learning
    show_explanation()

def show_explanation():
    """Show step-by-step explanation"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        first = data['first']
        second = data['second']
        round_factor = data['round_factor']
        round_place = data['round_place']
        
        st.markdown(f"""
        ### Step-by-Step Solution:
        **Original problem:** {first} × {second}
        """)
        
        # Show which number to round and how
        if round_factor == "first":
            if round_place == "ten":
                rounded_num = round_to_nearest_ten(first)
                st.markdown(f"""
                **Step 1:** Round the first factor ({first}) to the nearest ten
                - Look at the ones digit: {first % 10}
                - {first} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {rounded_num} × {second} = **{rounded_num * second}**
                """)
            elif round_place == "hundred":
                rounded_num = round_to_nearest_hundred(first)
                st.markdown(f"""
                **Step 1:** Round the first factor ({first}) to the nearest hundred
                - Look at the tens digit: {(first // 10) % 10}
                - {first} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {rounded_num} × {second} = **{rounded_num * second}**
                """)
            else:  # thousand
                rounded_num = round_to_nearest_thousand(first)
                st.markdown(f"""
                **Step 1:** Round the first factor ({first}) to the nearest thousand
                - Look at the hundreds digit: {(first // 100) % 10}
                - {first} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {rounded_num} × {second} = **{rounded_num * second}**
                """)
        else:  # round second factor
            if round_place == "ten":
                rounded_num = round_to_nearest_ten(second)
                st.markdown(f"""
                **Step 1:** Round the second factor ({second}) to the nearest ten
                - Look at the ones digit: {second % 10}
                - {second} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {first} × {rounded_num} = **{first * rounded_num}**
                """)
            elif round_place == "hundred":
                rounded_num = round_to_nearest_hundred(second)
                st.markdown(f"""
                **Step 1:** Round the second factor ({second}) to the nearest hundred
                - Look at the tens digit: {(second // 10) % 10}
                - {second} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {first} × {rounded_num} = **{first * rounded_num}**
                """)
            else:  # thousand
                rounded_num = round_to_nearest_thousand(second)
                st.markdown(f"""
                **Step 1:** Round the second factor ({second}) to the nearest thousand
                - Look at the hundreds digit: {(second // 100) % 10}
                - {second} rounds to **{rounded_num}**
                
                **Step 2:** Multiply the rounded number
                - {first} × {rounded_num} = **{first * rounded_num}**
                """)
        
        # Show rounding rules reminder
        st.markdown(f"""
        ### 💡 Rounding Rules Reminder:
        """)
        
        if round_place == "ten":
            st.markdown("""
            **Rounding to nearest ten:**
            - Look at the **ones digit**
            - 0, 1, 2, 3, 4 → Round DOWN
            - 5, 6, 7, 8, 9 → Round UP
            """)
        elif round_place == "hundred":
            st.markdown("""
            **Rounding to nearest hundred:**
            - Look at the **tens digit**
            - 0, 1, 2, 3, 4 → Round DOWN  
            - 5, 6, 7, 8, 9 → Round UP
            """)
        else:
            st.markdown("""
            **Rounding to nearest thousand:**
            - Look at the **hundreds digit**
            - 0, 1, 2, 3, 4 → Round DOWN
            - 5, 6, 7, 8, 9 → Round UP
            """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer