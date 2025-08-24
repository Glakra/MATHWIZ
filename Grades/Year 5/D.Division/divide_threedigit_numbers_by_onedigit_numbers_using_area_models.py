import streamlit as st
import random

def run():
    """
    Main function to run the Divide using Area Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 3/L. Division/divide_three_digit_numbers_by_one_digit_numbers_using_area_models.py
    """
    # Initialize session state for difficulty and game state
    if "divide_area_models_difficulty" not in st.session_state:
        st.session_state.divide_area_models_difficulty = 1  # Start with basic problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 3 > L. Division**")
    st.title("📐 Divide Using Area Models")
    st.markdown("*Use visual area models to understand three-digit division*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_area_models_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "3-digit ÷ 2-5", 2: "3-digit ÷ 3-7", 3: "3-digit ÷ 4-9"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/3")
    
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
        ### How to Play:
        - **Look at the area model** showing rectangles representing the division
        - **Find the missing side lengths** for each rectangle
        - **Calculate the total quotient** by adding the partial quotients
        
        ### Understanding Area Models:
        - **Total area = dividend** (the number being divided)
        - **One side = divisor** (the number we're dividing by)
        - **Other side = quotient** (the answer we're finding)
        - **Area = length × width**
        
        ### How it works:
        **525 ÷ 5 using area model:**
        - **Break 525 into:** 500 + 25
        - **Rectangle 1:** 500 ÷ 5 = 100 (width)
        - **Rectangle 2:** 25 ÷ 5 = 5 (width)
        - **Total quotient:** 100 + 5 = 105
        
        ### Strategy Tips:
        - **Split into friendly numbers:** Use hundreds, tens that divide easily
        - **Think about multiplication:** If area = 500 and height = 5, then width = ?
        - **Check your work:** Multiply quotient × divisor = dividend
        
        ### Common Splits:
        - **For ÷2:** Use 200, 400, 600, 800
        - **For ÷3:** Use 300, 600, 900
        - **For ÷4:** Use 400, 800
        - **For ÷5:** Use 500
        
        ### Difficulty Levels:
        - **🟡 Level 1:** 3-digit ÷ 2-5 (easier divisors)
        - **🟠 Level 2:** 3-digit ÷ 3-7 (medium divisors)
        - **🔴 Level 3:** 3-digit ÷ 4-9 (harder divisors)
        
        ### Scoring:
        - ✅ **All correct:** Move to harder problems
        - ❌ **Any wrong:** Practice easier problems
        - 🎯 **Goal:** Master area model division!
        """)

def generate_new_question():
    """Generate a new area model division question"""
    difficulty = st.session_state.divide_area_models_difficulty
    
    # Set number ranges based on difficulty
    if difficulty == 1:
        divisors = [2, 3, 4, 5]
        min_dividend = 200
        max_dividend = 600
    elif difficulty == 2:
        divisors = [3, 4, 5, 6, 7]
        min_dividend = 300
        max_dividend = 800
    else:
        divisors = [4, 5, 6, 7, 8, 9]
        min_dividend = 400
        max_dividend = 999
    
    divisor = random.choice(divisors)
    
    # Generate a dividend that works well with area models
    # We want to split into a large "hundreds" part and a smaller remainder
    
    # Choose a hundreds part that divides evenly
    hundreds_choices = []
    for h in range(2, 10):  # 200, 300, 400, etc.
        hundreds_val = h * 100
        if min_dividend <= hundreds_val <= max_dividend - 50 and hundreds_val % divisor == 0:
            hundreds_choices.append(hundreds_val)
    
    if not hundreds_choices:
        # Fallback: use a number that works
        hundreds_part = 500 if divisor <= 5 else 600
    else:
        hundreds_part = random.choice(hundreds_choices)
    
    # Add a remainder part that also divides evenly
    remainder_options = []
    for r in range(divisor, 100, divisor):  # Multiples of divisor
        if hundreds_part + r <= max_dividend:
            remainder_options.append(r)
    
    if remainder_options:
        remainder_part = random.choice(remainder_options[:5])  # Pick from first few options
    else:
        remainder_part = divisor * 2  # Simple fallback
    
    dividend = hundreds_part + remainder_part
    
    # Calculate quotients
    total_quotient = dividend // divisor
    hundreds_quotient = hundreds_part // divisor
    remainder_quotient = remainder_part // divisor
    
    # Choose colors for the rectangles
    colors = [
        ("#FFA07A", "#FF6B35"),  # Orange tones
        ("#FFB6C1", "#FF69B4"),  # Pink tones  
        ("#98FB98", "#32CD32"),  # Green tones
        ("#87CEEB", "#4169E1"),  # Blue tones
        ("#DDA0DD", "#9370DB"),  # Purple tones
    ]
    
    rect_colors = random.choice(colors)
    
    # Store question data
    st.session_state.question_data = {
        "dividend": dividend,
        "divisor": divisor,
        "hundreds_part": hundreds_part,
        "remainder_part": remainder_part,
        "total_quotient": total_quotient,
        "hundreds_quotient": hundreds_quotient,
        "remainder_quotient": remainder_quotient,
        "rect_colors": rect_colors
    }
    
    # Set up correct answers
    st.session_state.correct_answers = {
        "hundreds_quotient": hundreds_quotient,
        "remainder_quotient": remainder_quotient,
        "total_quotient": total_quotient
    }
    
    st.session_state.current_question = f"Use the model to find {dividend} ÷ {divisor}."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with prominent formatting
    st.markdown(f"""
    <div style="
        font-size: 24px; 
        font-weight: bold; 
        color: #1f77b4; 
        background-color: #f0f8ff; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #1f77b4;
        margin: 20px 0;
        text-align: center;
    ">
        {st.session_state.current_question}
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("area_model_form", clear_on_submit=False):
        
        # Instruction text
        st.markdown("**First, find the missing side lengths.**")
        st.markdown("---")
        
        # Create the area model visual with input boxes
        create_area_model_visual(data)
        
        st.markdown("---")
        
        # Final quotient question
        st.markdown("**Then, find the quotient.**")
        
        col1, col2, col3 = st.columns([1.5, 1.5, 1])
        
        with col1:
            st.markdown(f"""
            <div style="font-size: 20px; font-weight: bold; margin-top: 15px;">
                {data['dividend']} ÷ {data['divisor']} =
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_quotient_input = st.number_input(
                "Enter final quotient",
                min_value=0,
                max_value=500,
                value=None,
                step=1,
                key="total_quotient",
                help="Add the two widths together"
            )
        
        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            # Get the input values from session state
            hundreds_quotient_input = st.session_state.get("hundreds_quotient_input")
            remainder_quotient_input = st.session_state.get("remainder_quotient_input")
            
            # Validate all answers
            user_answers = {
                "hundreds_quotient": hundreds_quotient_input,
                "remainder_quotient": remainder_quotient_input,
                "total_quotient": total_quotient_input
            }
            
            # Check if all fields are filled
            if any(answer is None for answer in user_answers.values()):
                st.error("❌ Please fill in all the blanks before submitting.")
                return
            
            st.session_state.user_answers = user_answers
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_area_model_visual(data):
    """Create the visual area model with rectangles and input boxes"""
    
    # Create simpler visual using Streamlit components
    st.markdown("### 📐 Area Model:")
    
    # Layout: divisor on left, then two rectangles with input boxes above
    col1, col2, col3 = st.columns([0.5, 2, 2])
    
    with col1:
        # Divisor on the left side
        st.markdown("### ")  # Add space to align with rectangles
        st.markdown(f"""
        <div style="
            font-size: 48px; 
            font-weight: bold; 
            color: #1f77b4; 
            text-align: center;
            margin-top: 60px;
        ">
            {data['divisor']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Input box above Rectangle 1
        hundreds_quotient_input = st.number_input(
            f"Width 1",
            min_value=0,
            max_value=200,
            value=None,
            step=1,
            key="hundreds_quotient_input",
            help=f"What is {data['hundreds_part']} ÷ {data['divisor']}?"
        )
        
        # Rectangle 1 (hundreds part)
        st.markdown(f"""
        <div style="
            background-color: #FFA07A; 
            border: 3px solid #333; 
            border-radius: 8px; 
            padding: 40px; 
            text-align: center; 
            margin: 10px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 28px; font-weight: bold; color: #333;">
                {data['hundreds_part']}
            </div>
        </div>
        <div style="text-align: center; margin: 10px; font-size: 16px; font-weight: bold; color: #666;">
            Height: {data['divisor']}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Input box above Rectangle 2
        remainder_quotient_input = st.number_input(
            f"Width 2",
            min_value=0,
            max_value=50,
            value=None,
            step=1,
            key="remainder_quotient_input",
            help=f"What is {data['remainder_part']} ÷ {data['divisor']}?"
        )
        
        # Rectangle 2 (remainder part)
        st.markdown(f"""
        <div style="
            background-color: #FFB6C1; 
            border: 3px solid #333; 
            border-radius: 8px; 
            padding: 40px; 
            text-align: center; 
            margin: 10px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 28px; font-weight: bold; color: #333;">
                {data['remainder_part']}
            </div>
        </div>
        <div style="text-align: center; margin: 10px; font-size: 16px; font-weight: bold; color: #666;">
            Height: {data['divisor']}
        </div>
        """, unsafe_allow_html=True)
    
    # Add explanation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"""
        **📊 Area Model Explanation:**
        
        🔶 **Rectangle 1:** Area = {data['hundreds_part']}, Height = {data['divisor']}
        ➗ Width = {data['hundreds_part']} ÷ {data['divisor']} = ?
        
        🔷 **Rectangle 2:** Area = {data['remainder_part']}, Height = {data['divisor']}  
        ➗ Width = {data['remainder_part']} ÷ {data['divisor']} = ?
        
        🟰 **Total Width = Width 1 + Width 2**
        """)
    st.markdown("---")

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
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    
    # Check each answer
    all_correct = True
    feedback_messages = []
    
    # Check hundreds quotient
    if user_answers["hundreds_quotient"] == correct_answers["hundreds_quotient"]:
        feedback_messages.append("✅ First rectangle width is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ First rectangle width: Expected {correct_answers['hundreds_quotient']}, got {user_answers['hundreds_quotient']}")
    
    # Check remainder quotient
    if user_answers["remainder_quotient"] == correct_answers["remainder_quotient"]:
        feedback_messages.append("✅ Second rectangle width is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ Second rectangle width: Expected {correct_answers['remainder_quotient']}, got {user_answers['remainder_quotient']}")
    
    # Check total quotient
    if user_answers["total_quotient"] == correct_answers["total_quotient"]:
        feedback_messages.append("✅ Final quotient is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ Final quotient: Expected {correct_answers['total_quotient']}, got {user_answers['total_quotient']}")
    
    # Display overall result
    if all_correct:
        st.success("🎉 **Perfect! All answers are correct!**")
        
        # Increase difficulty (max level 3)
        old_difficulty = st.session_state.divide_area_models_difficulty
        st.session_state.divide_area_models_difficulty = min(
            st.session_state.divide_area_models_difficulty + 1, 3
        )
        
        # Show encouragement based on difficulty
        if st.session_state.divide_area_models_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered area model division!**")
        elif old_difficulty < st.session_state.divide_area_models_difficulty:
            st.info(f"⬆️ **Level up! Now working with harder division problems**")
    
    else:
        st.error("❌ **Some answers need correction. Let's review:**")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.divide_area_models_difficulty
        st.session_state.divide_area_models_difficulty = max(
            st.session_state.divide_area_models_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.divide_area_models_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Keep going!**")
    
    # Show detailed feedback
    for message in feedback_messages:
        if "✅" in message:
            st.success(message)
        else:
            st.error(message)
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct solution"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        st.markdown(f"""
        ### Complete Solution:
        
        **Problem:** {data['dividend']} ÷ {data['divisor']}
        
        ### Step-by-step using area model:
        
        **Step 1: Break down the dividend**
        - We split {data['dividend']} into {data['hundreds_part']} + {data['remainder_part']}
        - This creates two rectangles with easier-to-divide areas
        
        **Step 2: Find each rectangle's width**
        - **Rectangle 1:** Area = {data['hundreds_part']}, Height = {data['divisor']}
        - **Width = {data['hundreds_part']} ÷ {data['divisor']} = {data['hundreds_quotient']}**
        
        - **Rectangle 2:** Area = {data['remainder_part']}, Height = {data['divisor']}  
        - **Width = {data['remainder_part']} ÷ {data['divisor']} = {data['remainder_quotient']}**
        
        **Step 3: Add the widths for total quotient**
        - **Total width = {data['hundreds_quotient']} + {data['remainder_quotient']} = {data['total_quotient']}**
        
        ### Why area models work:
        - **Area = Length × Width** (or Area = Height × Width)
        - **If we know Area and Height, we can find Width**
        - **Width = Area ÷ Height**
        - **Total quotient = sum of all partial quotients**
        
        ### Check our work:
        - **{data['total_quotient']} × {data['divisor']} = {data['total_quotient'] * data['divisor']}**
        - **Does {data['total_quotient'] * data['divisor']} = {data['dividend']}?** {"✅ Yes!" if data['total_quotient'] * data['divisor'] == data['dividend'] else "❌ No"}
        
        ### Visual representation:
        - **Rectangle 1:** {data['hundreds_quotient']} × {data['divisor']} = {data['hundreds_part']}
        - **Rectangle 2:** {data['remainder_quotient']} × {data['divisor']} = {data['remainder_part']}
        - **Total:** ({data['hundreds_quotient']} + {data['remainder_quotient']}) × {data['divisor']} = {data['dividend']}
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answers" in st.session_state:
        del st.session_state.user_answers
    # Clear the input values
    if "hundreds_quotient_input" in st.session_state:
        del st.session_state.hundreds_quotient_input
    if "remainder_quotient_input" in st.session_state:
        del st.session_state.remainder_quotient_input