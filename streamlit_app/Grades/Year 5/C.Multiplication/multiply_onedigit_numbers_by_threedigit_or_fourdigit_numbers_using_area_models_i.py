import streamlit as st
import random

def run():
    """
    Main function to run the Expanded Form Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_onedigit_numbers_by_threedigit_or_fourdigit_numbers_using_expanded_form.py
    """
    # Initialize session state for difficulty and game state
    if "expanded_form_difficulty" not in st.session_state:
        st.session_state.expanded_form_difficulty = 1  # Start with 3-digit numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply Using Expanded Form")
    st.markdown("*Break down numbers and multiply each part separately*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.expanded_form_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "3-Digit Numbers",
            2: "Larger 3-Digit Numbers", 
            3: "4-Digit Numbers",
            4: "Complex Problems"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        # Progress bar (1 to 4 levels)
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
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
    with st.expander("💡 **Instructions & Expanded Form Guide**", expanded=False):
        st.markdown("""
        ### 📝 What is Expanded Form?
        
        **Expanded form** breaks a number into its place values:
        - **3-digit example:** 456 = 400 + 50 + 6
        - **4-digit example:** 2,834 = 2,000 + 800 + 30 + 4
        
        ### 🎯 How to Multiply Using Expanded Form:
        
        **Step 1: Break down the large number**
        - Example: 6 × 453
        - Break down 453: 453 = 400 + 50 + 3
        
        **Step 2: Multiply each part separately**
        - 6 × 400 = 2,400
        - 6 × 50 = 300  
        - 6 × 3 = 18
        
        **Step 3: Add all the products together**
        - 2,400 + 300 + 18 = 2,718
        - So 6 × 453 = 2,718
        
        ### 🔢 Complete Example: 7 × 2,648
        
        **Step 1: Expand 2,648**
        - 2,648 = 2,000 + 600 + 40 + 8
        
        **Step 2: Multiply each part by 7**
        - 7 × 2,000 = 14,000
        - 7 × 600 = 4,200
        - 7 × 40 = 280
        - 7 × 8 = 56
        
        **Step 3: Add them up**
        - 14,000 + 4,200 + 280 + 56 = 18,536
        
        ### 💡 Tips for Success:
        - **Place values:** thousands, hundreds, tens, ones
        - **Fill in each blank** as you work through the steps
        - **Check your work** by adding up all the partial products
        - **Watch for zeros** - 7 × 300 = 2,100 (not 21!)
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple 3-digit numbers (200-500)
        - **🟡 Level 2:** Larger 3-digit numbers (500-999)  
        - **🟠 Level 3:** 4-digit numbers (1000-5000)
        - **🔴 Level 4:** Complex problems with larger numbers
        """)

def generate_new_question():
    """Generate a new expanded form multiplication question"""
    difficulty = st.session_state.expanded_form_difficulty
    
    # Single digit multiplier (2-9)
    single_digit = random.randint(2, 9)
    
    # Generate large number based on difficulty
    if difficulty == 1:
        # Level 1: Simple 3-digit numbers
        large_number = random.randint(200, 500)
    elif difficulty == 2:
        # Level 2: Larger 3-digit numbers
        large_number = random.randint(500, 999)
    elif difficulty == 3:
        # Level 3: 4-digit numbers
        large_number = random.randint(1000, 5000)
    else:  # Level 4
        # Level 4: Complex numbers
        large_number = random.randint(1000, 9999)
    
    # Break down the number into expanded form
    expanded_parts = break_down_to_expanded_form(large_number)
    
    # Calculate partial products
    partial_products = {}
    for place_name, value in expanded_parts.items():
        partial_products[place_name] = single_digit * value
    
    # Calculate final answer
    final_answer = single_digit * large_number
    
    st.session_state.question_data = {
        "single_digit": single_digit,
        "large_number": large_number,
        "expanded_parts": expanded_parts,
        "partial_products": partial_products,
        "final_answer": final_answer
    }
    
    st.session_state.current_question = f"Calculate {single_digit} × {large_number:,} using expanded form"
    
    # Set up correct answers for form validation
    st.session_state.correct_answers = {
        **partial_products,
        "final_answer": final_answer
    }

def break_down_to_expanded_form(number):
    """Break down a number into expanded form parts"""
    parts = {}
    
    # Handle up to 4-digit numbers
    if number >= 1000:
        thousands = (number // 1000) * 1000
        if thousands > 0:
            parts['thousands'] = thousands
        number -= thousands
    
    if number >= 100:
        hundreds = (number // 100) * 100
        if hundreds > 0:
            parts['hundreds'] = hundreds
        number -= hundreds
    
    if number >= 10:
        tens = (number // 10) * 10
        if tens > 0:
            parts['tens'] = tens
        number -= tens
    
    if number > 0:
        parts['ones'] = number
    
    return parts

def display_question():
    """Display the expanded form multiplication question"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("---")
    
    # Show the problem setup
    st.markdown(f"### Step 1: Break down {data['large_number']:,} into expanded form")
    
    # Show the expanded form breakdown
    expanded_text = " + ".join([f"{value:,}" for value in data['expanded_parts'].values()])
    st.markdown(f"**{data['large_number']:,} = {expanded_text}**")
    
    st.markdown("### Step 2: Multiply each part and add them up")
    
    # Create the interactive form
    with st.form("expanded_form", clear_on_submit=False):
        user_answers = {}
        
        # Create input fields for each partial product
        for place_name, place_value in data['expanded_parts'].items():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
            
            with col1:
                st.markdown(f"**{data['single_digit']} × {place_value:,}**")
            
            with col2:
                st.markdown("**=**")
            
            with col3:
                user_answers[place_name] = st.number_input(
                    f"Answer for {place_value:,}",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get(place_name, 0),
                    step=1,
                    key=f"input_{place_name}",
                    label_visibility="collapsed"
                )
            
            with col4:
                st.markdown("")
            
            with col5:
                st.markdown("")
        
        # Add spacing
        st.markdown("---")
        
        # Final answer section
        st.markdown("### Step 3: Add all partial products together")
        
        # Show the addition equation with input for final answer
        addition_parts = []
        for place_name in data['expanded_parts'].keys():
            if place_name in user_answers and user_answers[place_name] > 0:
                addition_parts.append(f"{user_answers[place_name]:,}")
            else:
                addition_parts.append("___")
        
        addition_text = " + ".join(addition_parts)
        
        col1, col2, col3 = st.columns([3, 1, 2])
        
        with col1:
            st.markdown(f"**{addition_text}**")
        
        with col2:
            st.markdown("**=**")
        
        with col3:
            user_answers['final_answer'] = st.number_input(
                "Final answer",
                min_value=0,
                value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get('final_answer', 0),
                step=1,
                key="final_answer_input",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Check All Answers", type="primary", use_container_width=True)
        
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
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for all submitted answers"""
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    
    # Check each partial product
    all_correct = True
    partial_correct = 0
    total_parts = len(data['expanded_parts']) + 1  # +1 for final answer
    
    st.markdown("### 📊 Results:")
    
    # Check partial products
    for place_name, correct_value in data['partial_products'].items():
        user_value = user_answers.get(place_name, 0)
        place_value = data['expanded_parts'][place_name]
        
        if user_value == correct_value:
            st.success(f"✅ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - Correct!")
            partial_correct += 1
        else:
            st.error(f"❌ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - You answered: {user_value:,}")
            all_correct = False
    
    # Check final answer
    user_final = user_answers.get('final_answer', 0)
    correct_final = correct_answers['final_answer']
    
    if user_final == correct_final:
        st.success(f"✅ **Final Answer: {correct_final:,}** - Correct!")
        partial_correct += 1
    else:
        st.error(f"❌ **Final Answer: {correct_final:,}** - You answered: {user_final:,}")
        all_correct = False
    
    # Overall feedback
    if all_correct:
        st.success(f"🎉 **Perfect! You got everything right! ({partial_correct}/{total_parts})**")
        # Increase difficulty
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = min(
            st.session_state.expanded_form_difficulty + 1, 4
        )
        
        if st.session_state.expanded_form_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered expanded form multiplication!**")
        elif old_difficulty < st.session_state.expanded_form_difficulty:
            st.info(f"⬆️ **Excellent work! Moving to Level {st.session_state.expanded_form_difficulty}**")
    
    elif partial_correct >= total_parts // 2:
        st.warning(f"📈 **Good effort! You got {partial_correct}/{total_parts} correct. Keep practicing!**")
    else:
        st.error(f"📚 **Let's review the steps. You got {partial_correct}/{total_parts} correct.**")
        # Decrease difficulty
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = max(
            st.session_state.expanded_form_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.expanded_form_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Back to Level {st.session_state.expanded_form_difficulty}**")
    
    # Show explanation if not all correct
    if not all_correct:
        show_detailed_explanation()

def show_detailed_explanation():
    """Show detailed step-by-step explanation"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### ✅ Complete Solution: {data['single_digit']} × {data['large_number']:,}
        
        **Step 1: Break down {data['large_number']:,} into expanded form**
        """)
        
        expanded_parts_text = " + ".join([f"{value:,}" for value in data['expanded_parts'].values()])
        st.markdown(f"- {data['large_number']:,} = {expanded_parts_text}")
        
        st.markdown(f"""
        **Step 2: Multiply each part by {data['single_digit']}**
        """)
        
        for place_name, place_value in data['expanded_parts'].items():
            product = data['partial_products'][place_name]
            st.markdown(f"- {data['single_digit']} × {place_value:,} = {product:,}")
        
        st.markdown(f"""
        **Step 3: Add all the partial products**
        """)
        
        addition_parts = [f"{product:,}" for product in data['partial_products'].values()]
        addition_equation = " + ".join(addition_parts) + f" = {data['final_answer']:,}"
        st.markdown(f"- {addition_equation}")
        
        st.markdown(f"""
        **Final Answer: {data['single_digit']} × {data['large_number']:,} = {data['final_answer']:,}** ✅
        
        ### 💡 Remember:
        - Break down the large number by place value
        - Multiply each part separately  
        - Add all the partial products together
        - Check that your final answer makes sense!
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