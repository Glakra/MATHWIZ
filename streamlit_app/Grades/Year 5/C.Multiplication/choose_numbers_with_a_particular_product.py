import streamlit as st
import random
import itertools

def run():
    """
    Main function to run the Choose numbers with a particular product activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C.Multiplication/choose_numbers_with_particular_product.py
    """
    # Initialize session state for difficulty and game state
    if "choose_product_difficulty" not in st.session_state:
        st.session_state.choose_product_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_numbers = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🎯 Choose Numbers with a Particular Product")
    st.markdown("*Find two numbers from the given set that multiply to make the target product*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.choose_product_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
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
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Find the Right Numbers:
        - **Look at the target product** (the answer you need)
        - **Think of factor pairs** - which two numbers multiply to give this product?
        - **Check the available numbers** - are both factors in the box?
        - **Select the correct pair** by clicking on them
        
        ### Strategy Tips:
        1. **Start with small factors**: If target is 12, try 2×6, 3×4, 1×12
        2. **Use division**: If target is 15, try 15÷3=5, 15÷5=3
        3. **Look for patterns**: Even products need at least one even factor
        4. **Check your work**: Multiply your chosen numbers to verify
        
        ### Example:
        **Numbers available:** 2, 3, 5, 8  
        **Target product:** 15  
        **Solution:** 3 and 5 (because 3 × 5 = 15)
        
        ### Common Factor Pairs to Remember:
        - **2 × 6 = 12**    - **3 × 4 = 12**    - **3 × 5 = 15**
        - **2 × 8 = 16**    - **4 × 5 = 20**    - **4 × 6 = 24**
        - **5 × 6 = 30**    - **6 × 7 = 42**    - **7 × 8 = 56**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Products up to 30, basic factor pairs
        - **🟠 Level 3:** Products up to 60, more numbers to choose from
        - **🔴 Level 4-5:** Products up to 100+, complex factor combinations
        
        ### Key Skills:
        - ✅ **Factor recognition** - knowing multiplication facts
        - ✅ **Mental math** - quick multiplication and division
        - ✅ **Pattern recognition** - spotting factor relationships
        - ✅ **Logical thinking** - eliminating wrong choices
        """)

def generate_factor_pairs(target_product, difficulty):
    """Generate appropriate factor pairs based on difficulty"""
    pairs = []
    for i in range(1, int(target_product**0.5) + 1):
        if target_product % i == 0:
            pairs.append((i, target_product // i))
    
    # Filter pairs based on difficulty
    if difficulty <= 2:
        # Prefer smaller factors, avoid 1 as a factor unless necessary
        pairs = [(a, b) for a, b in pairs if a > 1 and b <= 15]
    elif difficulty <= 3:
        # Allow medium-sized factors
        pairs = [(a, b) for a, b in pairs if a > 1 and b <= 25]
    else:
        # Allow larger factors
        pairs = [(a, b) for a, b in pairs if a > 1 and b <= 50]
    
    return pairs if pairs else [(1, target_product)]

def generate_new_question():
    """Generate a new choose numbers question"""
    level = st.session_state.choose_product_difficulty
    
    # Define target products based on difficulty
    if level == 1:
        possible_products = [6, 8, 10, 12, 14, 15, 16, 18, 20, 21]
    elif level == 2:
        possible_products = [12, 15, 18, 20, 21, 24, 25, 27, 28, 30, 32, 35]
    elif level == 3:
        possible_products = [24, 28, 30, 32, 35, 36, 40, 42, 45, 48, 54, 56, 60]
    elif level == 4:
        possible_products = [36, 40, 42, 48, 54, 56, 63, 64, 70, 72, 80, 84, 90]
    else:  # level 5
        possible_products = [56, 63, 64, 70, 72, 80, 84, 90, 96, 100, 108, 120, 132]
    
    target_product = random.choice(possible_products)
    
    # Get factor pairs for this product
    factor_pairs = generate_factor_pairs(target_product, level)
    
    if not factor_pairs:
        # Fallback if no suitable pairs found
        target_product = 12
        factor_pairs = [(3, 4)]
    
    # Choose one correct pair
    correct_pair = random.choice(factor_pairs)
    
    # Generate number choices
    num_choices = 6 if level >= 3 else 4
    
    # Start with the correct pair
    available_numbers = list(correct_pair)
    
    # Add distractor numbers
    while len(available_numbers) < num_choices:
        # Generate numbers that could be plausible but don't work
        if level <= 2:
            distractor = random.randint(2, 12)
        elif level <= 3:
            distractor = random.randint(2, 20)
        else:
            distractor = random.randint(2, 30)
        
        # Make sure this distractor doesn't create another valid pair
        if distractor not in available_numbers:
            # Check if this would create an unwanted solution
            creates_solution = False
            for existing in available_numbers:
                if existing * distractor == target_product:
                    creates_solution = True
                    break
            
            if not creates_solution:
                available_numbers.append(distractor)
    
    # Shuffle the numbers
    random.shuffle(available_numbers)
    
    # Choose question format
    question_formats = [
        "Choose two numbers from the box to complete the sentence.",
        "Choose two numbers from the box to complete the multiplication number sentence."
    ]
    
    sentence_formats = [
        f"___ and ___ have a product of {target_product}.",
        f"___ × ___ = {target_product}"
    ]
    
    format_type = random.choice([0, 1])
    question_text = question_formats[format_type]
    sentence_text = sentence_formats[format_type]
    
    st.session_state.question_data = {
        "target_product": target_product,
        "available_numbers": available_numbers,
        "correct_pair": correct_pair,
        "question_text": question_text,
        "sentence_text": sentence_text,
        "format_type": format_type
    }
    st.session_state.correct_answer = correct_pair
    st.session_state.current_question = question_text
    st.session_state.selected_numbers = []

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 🎯 Task:")
    st.markdown(f"**{data['question_text']}**")
    
    # Display available numbers in a box
    st.markdown("**Available Numbers:**")
    
    # Create number selection buttons
    cols = st.columns(len(data['available_numbers']))
    
    for i, number in enumerate(data['available_numbers']):
        with cols[i]:
            # Check if this number is selected
            is_selected = number in st.session_state.selected_numbers
            
            # Button styling based on selection
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(f"{number}", key=f"num_{number}_{i}", type=button_type, use_container_width=True):
                if number in st.session_state.selected_numbers:
                    # Deselect if already selected
                    st.session_state.selected_numbers.remove(number)
                else:
                    # Select if not selected (max 2 numbers)
                    if len(st.session_state.selected_numbers) < 2:
                        st.session_state.selected_numbers.append(number)
                    else:
                        # Replace first selected number
                        st.session_state.selected_numbers[0] = st.session_state.selected_numbers[1]
                        st.session_state.selected_numbers[1] = number
                st.rerun()
    
    # Display the sentence with selected numbers
    st.markdown("---")
    if len(st.session_state.selected_numbers) == 0:
        display_sentence = data['sentence_text']
    elif len(st.session_state.selected_numbers) == 1:
        if data['format_type'] == 0:  # "and" format
            display_sentence = data['sentence_text'].replace("___", f"**{st.session_state.selected_numbers[0]}**", 1)
        else:  # multiplication format
            display_sentence = data['sentence_text'].replace("___", f"**{st.session_state.selected_numbers[0]}**", 1)
    else:  # 2 numbers selected
        temp_sentence = data['sentence_text']
        temp_sentence = temp_sentence.replace("___", f"**{st.session_state.selected_numbers[0]}**", 1)
        display_sentence = temp_sentence.replace("___", f"**{st.session_state.selected_numbers[1]}**", 1)
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 5px solid #6c757d;
        font-size: 20px;
        text-align: center;
        margin: 20px 0;
        font-weight: 500;
        color: #2c3e50;
    ">
        {display_sentence}
    </div>
    """, unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if len(st.session_state.selected_numbers) == 2:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        else:
            st.info("👆 Select exactly 2 numbers from the box above")
    
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
    user_selection = sorted(st.session_state.selected_numbers)
    correct_pair = sorted(st.session_state.correct_answer)
    data = st.session_state.question_data
    
    if user_selection == correct_pair:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the solution
        st.markdown(f"**{user_selection[0]} × {user_selection[1]} = {data['target_product']}** ✓")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.choose_product_difficulty
        st.session_state.choose_product_difficulty = min(
            st.session_state.choose_product_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.choose_product_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 factor finding!**")
        elif old_level < st.session_state.choose_product_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.choose_product_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they selected
        if len(user_selection) == 2:
            product = user_selection[0] * user_selection[1]
            st.markdown(f"You selected: **{user_selection[0]} × {user_selection[1]} = {product}**")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.choose_product_difficulty
        st.session_state.choose_product_difficulty = max(
            st.session_state.choose_product_difficulty - 1, 1
        )
        
        if old_level > st.session_state.choose_product_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.choose_product_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_pair = sorted(st.session_state.correct_answer)
    data = st.session_state.question_data
    target = data['target_product']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Finding the Correct Factor Pair:
        
        **Target Product:** {target}
        **Correct Answer:** {correct_pair[0]} and {correct_pair[1]}
        
        **Why this works:**
        {correct_pair[0]} × {correct_pair[1]} = {target} ✓
        
        ### How to find factor pairs:
        """)
        
        # Show all factor pairs for this number
        all_pairs = []
        for i in range(1, target + 1):
            if target % i == 0:
                other = target // i
                if i <= other:  # Avoid duplicates like (3,4) and (4,3)
                    all_pairs.append((i, other))
        
        st.markdown("**All possible factor pairs for {}:**".format(target))
        for pair in all_pairs:
            if pair == tuple(correct_pair):
                st.markdown(f"- **{pair[0]} × {pair[1]} = {target}** ← This pair was available!")
            else:
                st.markdown(f"- {pair[0]} × {pair[1]} = {target}")
        
        # Show which numbers were available
        st.markdown(f"""
        **Available numbers were:** {', '.join(map(str, sorted(data['available_numbers'])))}
        
        **Strategy tip:** Look for two numbers from the available set that multiply to give {target}.
        """)
        
        # Show why other combinations don't work
        other_combinations = []
        available = data['available_numbers']
        for i in range(len(available)):
            for j in range(i + 1, len(available)):
                if sorted([available[i], available[j]]) != correct_pair:
                    product = available[i] * available[j]
                    other_combinations.append((available[i], available[j], product))
        
        if other_combinations and len(other_combinations) <= 5:
            st.markdown("**Why other combinations don't work:**")
            for combo in other_combinations[:3]:  # Show max 3 examples
                st.markdown(f"- {combo[0]} × {combo[1]} = {combo[2]} (not {target})")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_numbers = []