import streamlit as st
import random

def run():
    """
    Main function to run the Area Models: Two-Digit × Two-Digit II practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_two_digit_area_models_II.py
    """
    # Initialize session state for difficulty and game state
    if "area_models_ii_difficulty" not in st.session_state:
        st.session_state.area_models_ii_difficulty = 1  # Start with basic models
    
    if "current_question_ii" not in st.session_state:
        st.session_state.current_question_ii = None
        st.session_state.correct_answers_ii = {}
        st.session_state.show_feedback_ii = False
        st.session_state.answer_submitted_ii = False
        st.session_state.question_data_ii = {}
        st.session_state.area_models_ii_score = 0
        st.session_state.total_questions_ii = 0
        st.session_state.user_answers_ii = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📐 Area Models: Two-Digit × Two-Digit II")
    st.markdown("*Step-by-step area model calculations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.area_models_ii_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Models", 2: "Intermediate", 3: "Advanced"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Models')}")
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
        if st.session_state.total_questions_ii > 0:
            accuracy = (st.session_state.area_models_ii_score / st.session_state.total_questions_ii) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question_ii is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Step-by-Step Guide**", expanded=False):
        st.markdown("""
        ### How This Activity Works:
        
        #### 🔹 **Step 1: Understand the Model**
        - Look at the **dimensions** labeled on the outside of each rectangle
        - Each rectangle represents a **partial multiplication**
        
        #### 🔹 **Step 2: Calculate Each Area**
        - **Top-left rectangle:** tens × tens
        - **Top-right rectangle:** tens × ones  
        - **Bottom-left rectangle:** ones × tens
        - **Bottom-right rectangle:** ones × ones
        - Enter each calculation in the **input box** inside each rectangle
        
        #### 🔹 **Step 3: Find the Total**
        - Add up all four partial products
        - Enter the final answer in the **total box**
        
        ### 📊 **Example: 28 × 44**
        ```
        Break down: 28 = 20 + 8, 44 = 40 + 4
        
        Partial products:
        • Top-left: 20 × 40 = 800
        • Top-right: 20 × 4 = 80  
        • Bottom-left: 8 × 40 = 320
        • Bottom-right: 8 × 4 = 32
        
        Total: 800 + 80 + 320 + 32 = 1,232
        ```
        
        ### 💡 **Tips for Success:**
        - **Look carefully** at the dimension labels
        - **Double-check** your multiplication for each rectangle
        - **Add systematically** - don't skip any partial products
        - **Estimate first** - does your answer seem reasonable?
        
        ### 🏆 **Why This Helps:**
        - **Breaks down** complex multiplication into simpler steps
        - **Shows the connection** between place value and multiplication
        - **Builds confidence** with systematic problem solving
        - **Prepares you** for algebraic thinking
        """)

def generate_new_question():
    """Generate a new step-by-step area model question"""
    difficulty = st.session_state.area_models_ii_difficulty
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        # Basic: smaller numbers, easier calculations
        tens_options1 = [20, 30, 40, 50]
        ones_options1 = [2, 3, 4, 5, 6, 7, 8, 9]
        tens_options2 = [10, 20, 30, 40]
        ones_options2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    elif difficulty == 2:
        # Intermediate: medium numbers
        tens_options1 = [20, 30, 40, 50, 60, 70]
        ones_options1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        tens_options2 = [10, 20, 30, 40, 50]
        ones_options2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:  # difficulty == 3
        # Advanced: larger numbers
        tens_options1 = [30, 40, 50, 60, 70, 80, 90]
        ones_options1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        tens_options2 = [20, 30, 40, 50, 60, 70]
        ones_options2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Generate the two numbers to multiply
    first_tens = random.choice(tens_options1)
    first_ones = random.choice(ones_options1)
    first_number = first_tens + first_ones
    
    second_tens = random.choice(tens_options2)
    second_ones = random.choice(ones_options2)
    second_number = second_tens + second_ones
    
    # Calculate all the parts
    tl_product = first_tens * second_tens  # top-left
    tr_product = first_tens * second_ones  # top-right
    bl_product = first_ones * second_tens  # bottom-left
    br_product = first_ones * second_ones  # bottom-right
    
    total_product = tl_product + tr_product + bl_product + br_product
    
    st.session_state.question_data_ii = {
        "first_number": first_number,
        "second_number": second_number,
        "first_tens": first_tens,
        "first_ones": first_ones,
        "second_tens": second_tens,
        "second_ones": second_ones,
        "tl_product": tl_product,
        "tr_product": tr_product,
        "bl_product": bl_product,
        "br_product": br_product,
        "total_product": total_product,
        "multiplication": f"{first_number} × {second_number}"
    }
    
    st.session_state.correct_answers_ii = {
        "tl": tl_product,
        "tr": tr_product, 
        "bl": bl_product,
        "br": br_product,
        "total": total_product
    }
    
    st.session_state.current_question_ii = f"Use the model to find {first_number} × {second_number}."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data_ii
    
    # Display question
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question_ii}**")
    st.markdown("**First, find the area of each rectangle.**")
    
    # Create the interactive area model
    create_interactive_area_model(data)
    
    # Final total input
    st.markdown("**Then, find the total area.**")
    
    with st.form("area_model_form", clear_on_submit=False):
        # Total calculation input
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            total_input = st.number_input(
                f"{data['multiplication']} =",
                min_value=0,
                max_value=100000,
                value=st.session_state.user_answers_ii.get("total", None) if "user_answers_ii" in st.session_state else None,
                step=1,
                key="total_calculation",
                placeholder="Enter total"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            # Collect all answers
            st.session_state.user_answers_ii = {
                "tl": st.session_state.get("tl_input", 0),
                "tr": st.session_state.get("tr_input", 0),
                "bl": st.session_state.get("bl_input", 0),
                "br": st.session_state.get("br_input", 0),
                "total": total_input if total_input is not None else 0
            }
            st.session_state.show_feedback_ii = True
            st.session_state.answer_submitted_ii = True
            st.session_state.total_questions_ii += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_interactive_area_model(data):
    """Create interactive area model using pure Streamlit components"""
    
    first_tens = data["first_tens"]
    first_ones = data["first_ones"]
    second_tens = data["second_tens"] 
    second_ones = data["second_ones"]
    
    st.markdown("---")
    
    # Display the breakdown
    st.markdown(f"**Breaking down the numbers:**")
    st.markdown(f"- {data['first_number']} = {first_tens} + {first_ones}")
    st.markdown(f"- {data['second_number']} = {second_tens} + {second_ones}")
    
    st.markdown("")
    st.markdown("**Area Model:**")
    
    # Create dimension headers
    col_empty, col_left_dim, col_right_dim = st.columns([1, 3, 2])
    with col_empty:
        st.markdown("")
    with col_left_dim:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; padding: 10px; background-color: #f8f9fa; border: 2px solid #dee2e6;'>{second_tens}</div>", unsafe_allow_html=True)
    with col_right_dim:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; padding: 10px; background-color: #f8f9fa; border: 2px solid #dee2e6;'>{second_ones}</div>", unsafe_allow_html=True)
    
    # Top row of rectangles
    col_left_label, col_tl_rect, col_tr_rect = st.columns([1, 3, 2])
    with col_left_label:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; padding: 40px 10px; background-color: #f8f9fa; border: 2px solid #dee2e6;'>{first_tens}</div>", unsafe_allow_html=True)
    with col_tl_rect:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding: 40px 20px; background-color: #FFE082; border: 3px solid #333; color: #333;'>🟡 Rectangle A<br>{first_tens} × {second_tens}</div>", unsafe_allow_html=True)
    with col_tr_rect:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding: 40px 20px; background-color: #81C784; border: 3px solid #333; color: #333;'>🟢 Rectangle B<br>{first_tens} × {second_ones}</div>", unsafe_allow_html=True)
    
    # Bottom row of rectangles
    col_left_label, col_bl_rect, col_br_rect = st.columns([1, 3, 2])
    with col_left_label:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; padding: 30px 10px; background-color: #f8f9fa; border: 2px solid #dee2e6;'>{first_ones}</div>", unsafe_allow_html=True)
    with col_bl_rect:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding: 30px 20px; background-color: #FFAB91; border: 3px solid #333; color: #333;'>🟠 Rectangle C<br>{first_ones} × {second_tens}</div>", unsafe_allow_html=True)
    with col_br_rect:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding: 30px 20px; background-color: #F48FB1; border: 3px solid #333; color: #333;'>🟣 Rectangle D<br>{first_ones} × {second_ones}</div>", unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("**📝 Enter the area of each rectangle:**")
    
    # Input section organized in a 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🟡 Rectangle A (Top-Left):**")
        tl_input = st.number_input(
            f"{first_tens} × {second_tens} =",
            min_value=0,
            max_value=100000,
            value=st.session_state.user_answers_ii.get("tl", None) if "user_answers_ii" in st.session_state else None,
            step=1,
            key="tl_input",
            placeholder="Enter area"
        )
        
        st.markdown("**🟠 Rectangle C (Bottom-Left):**")
        bl_input = st.number_input(
            f"{first_ones} × {second_tens} =",
            min_value=0,
            max_value=100000,
            value=st.session_state.user_answers_ii.get("bl", None) if "user_answers_ii" in st.session_state else None,
            step=1,
            key="bl_input",
            placeholder="Enter area"
        )
    
    with col2:
        st.markdown("**🟢 Rectangle B (Top-Right):**")
        tr_input = st.number_input(
            f"{first_tens} × {second_ones} =",
            min_value=0,
            max_value=100000,
            value=st.session_state.user_answers_ii.get("tr", None) if "user_answers_ii" in st.session_state else None,
            step=1,
            key="tr_input",
            placeholder="Enter area"
        )
        
        st.markdown("**🟣 Rectangle D (Bottom-Right):**")
        br_input = st.number_input(
            f"{first_ones} × {second_ones} =",
            min_value=0,
            max_value=100000,
            value=st.session_state.user_answers_ii.get("br", None) if "user_answers_ii" in st.session_state else None,
            step=1,
            key="br_input",
            placeholder="Enter area"
        )

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback_ii:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted_ii:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answers = st.session_state.user_answers_ii
    correct_answers = st.session_state.correct_answers_ii
    data = st.session_state.question_data_ii
    
    # Check each partial product
    partial_correct = 0
    total_parts = 4
    
    feedback_messages = []
    
    # Check top-left
    if user_answers["tl"] == correct_answers["tl"]:
        feedback_messages.append("✅ **Top-left:** Correct!")
        partial_correct += 1
    else:
        feedback_messages.append(f"❌ **Top-left:** {user_answers['tl']} ≠ {correct_answers['tl']} (should be {data['first_tens']} × {data['second_tens']} = {correct_answers['tl']})")
    
    # Check top-right
    if user_answers["tr"] == correct_answers["tr"]:
        feedback_messages.append("✅ **Top-right:** Correct!")
        partial_correct += 1
    else:
        feedback_messages.append(f"❌ **Top-right:** {user_answers['tr']} ≠ {correct_answers['tr']} (should be {data['first_tens']} × {data['second_ones']} = {correct_answers['tr']})")
    
    # Check bottom-left
    if user_answers["bl"] == correct_answers["bl"]:
        feedback_messages.append("✅ **Bottom-left:** Correct!")
        partial_correct += 1
    else:
        feedback_messages.append(f"❌ **Bottom-left:** {user_answers['bl']} ≠ {correct_answers['bl']} (should be {data['first_ones']} × {data['second_tens']} = {correct_answers['bl']})")
    
    # Check bottom-right
    if user_answers["br"] == correct_answers["br"]:
        feedback_messages.append("✅ **Bottom-right:** Correct!")
        partial_correct += 1
    else:
        feedback_messages.append(f"❌ **Bottom-right:** {user_answers['br']} ≠ {correct_answers['br']} (should be {data['first_ones']} × {data['second_ones']} = {correct_answers['br']})")
    
    # Check total
    total_correct = user_answers["total"] == correct_answers["total"]
    
    # Display partial product feedback
    st.markdown("### 📊 **Partial Products Check:**")
    for message in feedback_messages:
        st.markdown(message)
    
    # Display total feedback
    st.markdown("### 🎯 **Total Calculation:**")
    if total_correct:
        st.success("✅ **Total:** Excellent! Your final answer is correct!")
        if partial_correct == total_parts:
            st.session_state.area_models_ii_score += 1
            st.balloons()
            st.success("🏆 **Perfect! All partial products AND total are correct!**")
        else:
            st.info("💡 **Good job on the total, but double-check your partial products for better understanding.**")
    else:
        st.error(f"❌ **Total:** {user_answers['total']} ≠ {correct_answers['total']}")
        st.markdown(f"**Correct calculation:** {correct_answers['tl']} + {correct_answers['tr']} + {correct_answers['bl']} + {correct_answers['br']} = **{correct_answers['total']}**")
    
    # Scoring (perfect score only if all parts are correct)
    if partial_correct == total_parts and total_correct:
        score_message = "🎉 **Perfect Score!** All calculations correct!"
    elif partial_correct >= 3 and total_correct:
        score_message = f"🌟 **Great work!** {partial_correct}/4 partial products correct, plus correct total!"
    elif partial_correct >= 2:
        score_message = f"👍 **Good effort!** {partial_correct}/4 partial products correct. Keep practicing!"
    else:
        score_message = f"💪 **Keep trying!** {partial_correct}/4 partial products correct. Review the steps!"
    
    st.info(score_message)
    
    # Adjust difficulty based on performance
    if st.session_state.total_questions_ii % 3 == 0:  # Every 3 questions
        accuracy = st.session_state.area_models_ii_score / st.session_state.total_questions_ii
        if accuracy >= 0.8 and st.session_state.area_models_ii_difficulty < 3:
            old_difficulty = st.session_state.area_models_ii_difficulty
            st.session_state.area_models_ii_difficulty += 1
            if old_difficulty < st.session_state.area_models_ii_difficulty:
                st.success(f"⬆️ **Level Up! Now at Level {st.session_state.area_models_ii_difficulty}**")
        elif accuracy < 0.3 and st.session_state.area_models_ii_difficulty > 1:
            old_difficulty = st.session_state.area_models_ii_difficulty
            st.session_state.area_models_ii_difficulty = max(st.session_state.area_models_ii_difficulty - 1, 1)
            if old_difficulty > st.session_state.area_models_ii_difficulty:
                st.warning(f"⬇️ **Let's practice easier problems. Back to Level {st.session_state.area_models_ii_difficulty}**")
    
    # Show detailed explanation
    show_explanation()

def show_explanation():
    """Show detailed step-by-step explanation"""
    data = st.session_state.question_data_ii
    
    with st.expander("📖 **Click here for complete solution**", expanded=True):
        st.markdown(f"""
        ### Complete Step-by-Step Solution:
        
        **Problem:** {data['multiplication']}
        
        **Step 1: Break down the numbers**
        - {data['first_number']} = {data['first_tens']} + {data['first_ones']}
        - {data['second_number']} = {data['second_tens']} + {data['second_ones']}
        
        **Step 2: Calculate each partial product**
        - **Top-left:** {data['first_tens']} × {data['second_tens']} = {data['tl_product']}
        - **Top-right:** {data['first_tens']} × {data['second_ones']} = {data['tr_product']}
        - **Bottom-left:** {data['first_ones']} × {data['second_tens']} = {data['bl_product']}
        - **Bottom-right:** {data['first_ones']} × {data['second_ones']} = {data['br_product']}
        
        **Step 3: Add all partial products**
        {data['tl_product']} + {data['tr_product']} + {data['bl_product']} + {data['br_product']} = **{data['total_product']}**
        
        ### 💡 **Why Each Step Matters:**
        - **Partial products** help break down complex multiplication into manageable pieces
        - **Visual organization** prevents missing any part of the calculation  
        - **Systematic approach** builds confidence and accuracy
        - **Understanding place value** prepares you for more advanced mathematics
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question_ii = None
    st.session_state.correct_answers_ii = {}
    st.session_state.show_feedback_ii = False
    st.session_state.answer_submitted_ii = False
    st.session_state.question_data_ii = {}
    st.session_state.user_answers_ii = {}
    
    # Clear input values
    for key in ["tl_input", "tr_input", "bl_input", "br_input", "total_calculation"]:
        if key in st.session_state:
            del st.session_state[key]