import streamlit as st
import random

def run():
    """
    Main function to run the Partial Products Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_one_digit_numbers_by_multi_digit_numbers_using_partial_products.py
    """
    # Initialize session state for difficulty and game state
    if "partial_products_difficulty" not in st.session_state:
        st.session_state.partial_products_difficulty = 2  # Start with 2-digit numbers
    
    if "question_type" not in st.session_state:
        st.session_state.question_type = 1  # Type 1 or Type 2
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answers = {}
        st.session_state.all_correct = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🧮 Multiply Using Partial Products")
    st.markdown("*Break numbers apart to make multiplication easier*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.partial_products_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (2 to 4 digits)
        progress = (difficulty_level - 2) / 2  # Convert 2-4 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level == 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 3:
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
        ### Two Question Types:
        
        **🔢 Type 1 - Calculate All Partial Products:**
        - **Break apart** the multi-digit number by place value
        - **Multiply each part** by the one-digit number
        - **Fill in all** the partial products and final answer
        
        **🎯 Type 2 - Fill in Missing Numbers:**
        - **Some partial products** are already given
        - **Fill in only** the missing partial products
        - **Complete** the final answer
        
        ### Example: 338 × 5 (Type 1)
        ```
        Break apart 338:  300 + 30 + 8
        
            338
        ×     5
        -------
           1500  (300 × 5)
        +   150  (30 × 5)
        +    40  (8 × 5)
        -------
           1690
        ```
        
        ### Example: 338 × 5 (Type 2)
        ```
            338
        ×     5
        -------
            ?   (You fill this in)
        +  150  (Given)
        +   40  (Given)
        -------
            ?   (You fill this in)
        ```
        
        ### Tips for Success:
        - **Think place value:** hundreds, tens, ones
        - **Use given information:** In Type 2, use the shown partial products as hints
        - **Check your work:** Add the partial products to verify
        - **Line up numbers:** Keep place values aligned
        - **Practice patterns:** 300 × 5 = 1500, 30 × 5 = 150, 8 × 5 = 40
        
        ### Difficulty Levels:
        - **🟡 2-digit × 1-digit:** (23 × 4)
        - **🟠 3-digit × 1-digit:** (234 × 6)
        - **🔴 4-digit × 1-digit:** (2345 × 7)
        
        ### Scoring:
        - ✅ **All correct:** Move to harder problems
        - ❌ **Some wrong:** Practice more at this level
        - 🎯 **Goal:** Master both types with 4-digit numbers!
        """)


def generate_new_question():
    """Generate a new partial products multiplication question"""
    digits = st.session_state.partial_products_difficulty
    
    # Always choose question type randomly if not already set
    if "question_type" not in st.session_state:
        st.session_state.question_type = random.choice([1, 2])
    
    # Generate multi-digit number and single digit multiplier
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    # Ensure interesting numbers (not too many zeros)
    multi_digit = random.randint(min_val, max_val)
    while str(multi_digit).count('0') > 1:  # Avoid too many zeros
        multi_digit = random.randint(min_val, max_val)
    
    single_digit = random.randint(2, 9)  # Avoid 0 and 1 for more interesting problems
    
    # Calculate all the partial products
    partial_products = []
    place_values = []
    temp = multi_digit
    position = 0
    
    while temp > 0:
        digit = temp % 10
        place_value = digit * (10 ** position)
        if place_value > 0:  # Only include non-zero place values
            partial_product = place_value * single_digit
            partial_products.append(partial_product)
            place_values.append(place_value)
        temp //= 10
        position += 1
    
    # Reverse to show from left to right (hundreds, tens, ones)
    partial_products.reverse()
    place_values.reverse()
    
    final_answer = sum(partial_products)
    
    # Initialize given_products and missing_indices
    given_products = []
    missing_indices = []
    
    if st.session_state.question_type == 2:
        # Type 2: Randomly show some partial products and hide others
        num_products = len(partial_products)
        if num_products == 2:
            # For 2 partial products, hide 1
            num_to_hide = 1
        else:
            # For 3+ partial products, hide 1-2 but leave at least 1 shown
            num_to_hide = random.randint(1, min(2, max(1, num_products - 1)))
        
        missing_indices = random.sample(range(num_products), num_to_hide)
        
        for i, product in enumerate(partial_products):
            if i in missing_indices:
                given_products.append(None)  # This will be an input field
            else:
                given_products.append(product)  # This will be shown
    else:
        # Type 1: All products need to be calculated
        given_products = [None] * len(partial_products)
        missing_indices = list(range(len(partial_products)))
    
    # Create question data
    st.session_state.question_data = {
        "multi_digit": multi_digit,
        "single_digit": single_digit,
        "partial_products": partial_products,
        "place_values": place_values,
        "final_answer": final_answer,
        "given_products": given_products,
        "missing_indices": missing_indices
    }
    
    # Reset correct answers for new question
    st.session_state.correct_answers = {}
    
    if st.session_state.question_type == 1:
        # Type 1: All partial products need to be filled in
        for i, product in enumerate(partial_products):
            st.session_state.correct_answers[f"partial_{i}"] = product
        st.session_state.current_question = f"Fill in the missing partial products:"
    else:
        # Type 2: Only missing partial products need to be filled in
        for i in missing_indices:
            st.session_state.correct_answers[f"partial_{i}"] = partial_products[i]
        st.session_state.current_question = f"Fill in the missing numbers:"
    
    # Final answer is always required
    st.session_state.correct_answers["final"] = final_answer

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 🧮 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Create form for answers
    with st.form("partial_products_form"):
        # Create the multiplication layout with input boxes
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Display the main multiplication problem
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 30px; 
                border-radius: 15px; 
                border: 2px solid #dee2e6;
                font-family: 'Courier New', monospace;
                font-size: 24px;
                text-align: right;
                margin: 20px 0;
                line-height: 1.8;
            ">
                <div style="margin-bottom: 15px; padding-right: 20px;">
                    {data['multi_digit']}
                </div>
                <div style="margin-bottom: 15px; padding-right: 20px;">
                    ×&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data['single_digit']}
                </div>
                <div style="border-bottom: 3px solid #000; margin: 10px 0;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display breakdown explanation
            st.markdown("**Break it down by place value:**")
            breakdown_parts = []
            for i, (place_val, partial) in enumerate(zip(data['place_values'], data['partial_products'])):
                breakdown_parts.append(f"{place_val} × {data['single_digit']}")
            
            breakdown_text = " + ".join(breakdown_parts)
            st.markdown(f"*{data['multi_digit']} = {' + '.join(map(str, data['place_values']))}*")
            st.markdown(f"*So we need to calculate: {breakdown_text}*")
            
            st.markdown("**Now calculate each partial product:**")
            
            # Create input fields for partial products with better alignment
            user_answers = {}
            
            # Style the partial products section like a traditional math worksheet
            st.markdown("""
            <style>
            .partial-products-container {
                background-color: #ffffff;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                padding: 25px;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="partial-products-container">', unsafe_allow_html=True)
            
            for i, (place_val, partial) in enumerate(zip(data['place_values'], data['partial_products'])):
                # Create a row with proper alignment
                row_cols = st.columns([1, 4, 3])
                
                with row_cols[0]:
                    if i > 0:
                        st.markdown(f"<div style='font-size: 20px; text-align: center; margin-top: 12px; color: #666;'>+</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='height: 44px;'></div>", unsafe_allow_html=True)
                
                with row_cols[1]:
                    st.markdown(f"<div style='margin-top: 12px; font-size: 18px; color: #333;'>{place_val} × {data['single_digit']} =</div>", unsafe_allow_html=True)
                
                with row_cols[2]:
                    user_input = st.number_input(
                        f"Product {i+1}",
                        min_value=0,
                        step=1,
                        key=f"partial_{i}",
                        label_visibility="collapsed",
                        help=f"What is {place_val} × {data['single_digit']}?",
                        placeholder="Enter answer"
                    )
                    user_answers[f"partial_{i}"] = user_input
            
            # Add a visual divider line
            st.markdown("""
            <div style='border-bottom: 2px solid #333; margin: 20px 40px; width: 60%;'></div>
            """, unsafe_allow_html=True)
            
            # Final answer input with better styling
            final_cols = st.columns([1, 4, 3])
            with final_cols[0]:
                st.markdown("<div style='height: 44px;'></div>", unsafe_allow_html=True)
            
            with final_cols[1]:
                st.markdown("<div style='margin-top: 12px; font-size: 18px; font-weight: bold; color: #333;'>Final Answer =</div>", unsafe_allow_html=True)
            
            with final_cols[2]:
                final_input = st.number_input(
                    "Sum of all partial products",
                    min_value=0,
                    step=1,
                    key="final",
                    label_visibility="collapsed",
                    help="Add up all the partial products",
                    placeholder="Enter sum"
                )
                user_answers["final"] = final_input
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Check My Work", type="primary", use_container_width=True)
        
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
    """Display feedback for the submitted answers"""
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    question_type = st.session_state.question_type
    
    all_correct = True
    feedback_messages = []
    
    # Check each partial product (only those that needed input)
    for i, partial in enumerate(data['partial_products']):
        if question_type == 2 and data['given_products'][i] is not None:
            # Type 2: This was given, so skip checking
            feedback_messages.append(f"ℹ️ Partial product {i+1}: **{data['given_products'][i]}** (given)")
            continue
        
        # This needed to be inputted
        user_val = user_answers.get(f"partial_{i}", 0)
        correct_val = correct_answers[f"partial_{i}"]
        
        if user_val == correct_val:
            feedback_messages.append(f"✅ Partial product {i+1}: **{user_val}** is correct!")
        else:
            if question_type == 1:
                feedback_messages.append(f"❌ Partial product {i+1}: You wrote **{user_val}**, but {data['place_values'][i]} × {data['single_digit']} = **{correct_val}**")
            else:
                feedback_messages.append(f"❌ Partial product {i+1}: You wrote **{user_val}**, but the correct answer is **{correct_val}**")
            all_correct = False
    
    # Check final answer
    user_final = user_answers.get("final", 0)
    correct_final = correct_answers["final"]
    
    if user_final == correct_final:
        feedback_messages.append(f"✅ Final answer: **{user_final}** is correct!")
    else:
        feedback_messages.append(f"❌ Final answer: You wrote **{user_final}**, but the sum is **{correct_final}**")
        all_correct = False
    
    # Display overall result
    if all_correct:
        st.success(f"🎉 **Perfect! You solved the Type {question_type} problem correctly!**")
        
        # Increase difficulty (max 4 digits)
        old_difficulty = st.session_state.partial_products_difficulty
        st.session_state.partial_products_difficulty = min(
            st.session_state.partial_products_difficulty + 1, 4
        )
        
        if st.session_state.partial_products_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 4-digit partial products multiplication!**")
        elif old_difficulty < st.session_state.partial_products_difficulty:
            st.info(f"⬆️ **Great work! Moving up to {st.session_state.partial_products_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Some answers need work in this Type {question_type} problem. Let's review:**")
        
        # Stay at current difficulty or decrease slightly
        if st.session_state.partial_products_difficulty > 2:
            old_difficulty = st.session_state.partial_products_difficulty
            st.session_state.partial_products_difficulty = max(
                st.session_state.partial_products_difficulty - 1, 2
            )
            if old_difficulty > st.session_state.partial_products_difficulty:
                st.warning(f"⬇️ **Let's practice more with {st.session_state.partial_products_difficulty}-digit numbers**")
    
    # Show detailed feedback
    st.markdown("### 📋 Detailed Feedback:")
    for message in feedback_messages:
        st.markdown(f"- {message}")
    
    # Show the complete solution
    show_complete_solution()
    
    st.session_state.all_correct = all_correct

def show_complete_solution():
    """Show the complete solution breakdown"""
    data = st.session_state.question_data
    
    with st.expander("📖 **See Complete Solution**", expanded=False):
        st.markdown(f"""
        ### Step-by-step solution for {data['multi_digit']} × {data['single_digit']}:
        
        **1. Break apart {data['multi_digit']} by place value:**
        """)
        
        breakdown = []
        temp = data['multi_digit']
        position = 0
        
        while temp > 0:
            digit = temp % 10
            if digit > 0:
                place_value = digit * (10 ** position)
                breakdown.append(place_value)
            temp //= 10
            position += 1
        
        breakdown.reverse()
        st.markdown(f"   {data['multi_digit']} = {' + '.join(map(str, breakdown))}")
        
        st.markdown(f"""
        **2. Multiply each part by {data['single_digit']}:**
        """)
        
        for place_val, partial in zip(data['place_values'], data['partial_products']):
            st.markdown(f"   {place_val} × {data['single_digit']} = {partial}")
        
        st.markdown(f"""
        **3. Add all partial products:**
        """)
        
        addition_str = " + ".join(map(str, data['partial_products']))
        st.markdown(f"   {addition_str} = {data['final_answer']}")
        
        st.markdown(f"""
        **Final Answer: {data['multi_digit']} × {data['single_digit']} = {data['final_answer']}**
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answers = {}
    st.session_state.all_correct = False
    # Always reset question type so it gets randomly selected again
    if "question_type" in st.session_state:
        del st.session_state.question_type