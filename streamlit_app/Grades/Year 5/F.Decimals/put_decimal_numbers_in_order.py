import streamlit as st
import random

def run():
    """
    Main function to run the Put Decimal Numbers in Order practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/put_decimal_numbers_order.py
    """
    # Initialize session state for difficulty and game state
    if "order_decimals_difficulty" not in st.session_state:
        st.session_state.order_decimals_difficulty = 1  # Start with simple decimals
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_order = []
        st.session_state.available_numbers = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Put Decimal Numbers in Order")
    st.markdown("*Arrange decimal numbers from smallest to largest or largest to smallest*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.order_decimals_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple tenths",
            2: "Hundredths ordering", 
            3: "Mixed decimal places",
            4: "Close value ordering",
            5: "Advanced decimal ordering"
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
        - **Read the instruction** - smallest to largest OR largest to smallest
        - **Click the numbers in the correct order** 
        - **Watch your selected order** appear below the tiles
        - **Click Submit** when you have all 4 numbers in order
        
        ### Ordering Strategies:
        1. **Compare whole numbers first** - 2.5 > 1.9 because 2 > 1
        2. **If whole numbers equal, compare tenths** - 1.6 > 1.3 because 6 > 3
        3. **If tenths equal, compare hundredths** - 0.85 > 0.82 because 5 > 2
        
        ### Examples:
        **Smallest to largest:** 0.2, 0.3, 0.5, 0.8
        - Start with 0.2 (smallest), end with 0.8 (largest)
        
        **Largest to smallest:** 2.5, 1.9, 1.6, 1.3  
        - Start with 2.5 (largest), end with 1.3 (smallest)
        
        ### Tips for Success:
        - **Read carefully** - smallest to largest vs largest to smallest
        - **Compare systematically** - don't just guess
        - **Think about number lines** - which numbers come first?
        - **Use place value** - understand tenths vs hundredths
        - **Double-check** your order before submitting
        
        ### Place Value Reminders:
        - **0.8 = 8 tenths** vs **0.3 = 3 tenths** → 0.8 > 0.3
        - **1.9 = 1 and 9 tenths** vs **1.6 = 1 and 6 tenths** → 1.9 > 1.6
        - **0.25 = 25 hundredths** vs **0.3 = 30 hundredths** → 0.3 > 0.25
        
        ### Common Mistakes:
        - **Reading the instruction wrong** - check if it's smallest→largest or largest→smallest
        - **Comparing incorrectly** - 0.5 is bigger than 0.45, not smaller
        - **Forgetting place value** - 2.1 > 1.9 even though 1 < 9
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple tenths (0.2, 0.3, 0.5, 0.8)
        - **🟡 Level 2:** Hundredths (1.23, 1.45, 1.67, 1.89)
        - **🟠 Level 3:** Mixed places (0.8 vs 0.75 vs 1.2)
        - **🔴 Level 4:** Close values (2.85 vs 2.9 vs 2.78)
        - **🔴 Level 5:** Advanced challenges
        
        ### Scoring:
        - ✅ **Correct order:** Move to next level
        - ❌ **Wrong order:** Practice more at current level
        - 🎯 **Goal:** Master all ordering levels!
        """)

def generate_new_question():
    """Generate a new decimal ordering question based on difficulty level"""
    difficulty = st.session_state.order_decimals_difficulty
    
    if difficulty == 1:
        # Simple tenths like in the images
        numbers = [0.2, 0.3, 0.5, 0.8]  # Like image 1
        random.shuffle(numbers)
        
    elif difficulty == 2:
        # Hundredths ordering
        base_numbers = [1.23, 1.45, 1.67, 1.89]
        numbers = base_numbers[:]
        random.shuffle(numbers)
        
    elif difficulty == 3:
        # Mixed decimal places with different whole numbers
        base_numbers = [1.3, 2.5, 1.6, 1.9]  # Like image 2
        numbers = base_numbers[:]
        random.shuffle(numbers)
        
    elif difficulty == 4:
        # Close value comparisons
        base = random.randint(2, 8)
        numbers = [
            round(base + 0.15, 2),
            round(base + 0.23, 2), 
            round(base + 0.07, 2),
            round(base + 0.31, 2)
        ]
        random.shuffle(numbers)
        
    else:  # difficulty == 5
        # Advanced ordering with very close values
        base = random.uniform(5, 15)
        numbers = [
            round(base + 0.025, 3),
            round(base + 0.078, 3),
            round(base + 0.003, 3),
            round(base + 0.156, 3)
        ]
        random.shuffle(numbers)
    
    # Randomly choose ascending or descending order
    order_type = random.choice(["smallest to largest", "largest to smallest"])
    
    # Calculate correct answer
    if order_type == "smallest to largest":
        correct_answer = sorted(numbers)
    else:
        correct_answer = sorted(numbers, reverse=True)
    
    # Store question data
    st.session_state.question_data = {
        "numbers": numbers,
        "order_type": order_type
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Put these numbers in order from {order_type}."
    st.session_state.available_numbers = numbers[:]
    st.session_state.selected_order = []

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question text (like the images)
    question_text = st.session_state.current_question
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #007acc;
        font-size: 18px;
        margin: 20px 0;
        color: #333;
    ">
        {question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Display clickable number tiles (blue tiles like the images)
    st.markdown("**Click the numbers in the correct order:**")
    
    # Create 4 columns for the number tiles
    cols = st.columns(4)
    
    for i, number in enumerate(data["numbers"]):
        with cols[i]:
            # Check if this number is still available
            if number in st.session_state.available_numbers:
                if st.button(f"{number}", key=f"num_{i}", use_container_width=True,
                           help=f"Click to select {number}"):
                    # Add to selected order and remove from available
                    st.session_state.selected_order.append(number)
                    st.session_state.available_numbers.remove(number)
                    st.rerun()
            else:
                # Show as selected/disabled
                st.button(f"{number}", key=f"num_disabled_{i}", use_container_width=True, 
                         disabled=True, help="Already selected")
    
    # Show current selection order
    if st.session_state.selected_order:
        st.markdown("### Your Order:")
        order_text = " → ".join([str(num) for num in st.session_state.selected_order])
        st.markdown(f"""
        <div style="
            text-align: center; 
            font-size: 24px; 
            font-weight: bold; 
            margin: 20px 0;
            padding: 15px;
            background-color: #e3f2fd;
            border-radius: 10px;
            color: #1976d2;
        ">
            {order_text}
        </div>
        """, unsafe_allow_html=True)
    
    # Reset button if user wants to start over
    if st.session_state.selected_order:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄 Reset", help="Start over"):
                st.session_state.selected_order = []
                st.session_state.available_numbers = data["numbers"][:]
                st.rerun()
    
    # Submit button (only show when all 4 numbers selected)
    if len(st.session_state.selected_order) == 4 and not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
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
    user_answer = st.session_state.selected_order
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! Perfect order!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.order_decimals_difficulty
        st.session_state.order_decimals_difficulty = min(
            st.session_state.order_decimals_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.order_decimals_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal number ordering!**")
        elif old_difficulty < st.session_state.order_decimals_difficulty:
            difficulty_names = {
                2: "hundredths ordering",
                3: "mixed decimal places", 
                4: "close value ordering",
                5: "advanced decimal challenges"
            }
            next_level = difficulty_names.get(st.session_state.order_decimals_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        st.error("❌ **Not quite right. Let's see the correct order:**")
        
        # Show correct answer
        correct_order_text = " → ".join([str(num) for num in correct_answer])
        st.markdown(f"""
        <div style="
            text-align: center; 
            font-size: 20px; 
            font-weight: bold; 
            margin: 15px 0;
            padding: 15px;
            background-color: #ffebee;
            border-radius: 10px;
            color: #c62828;
        ">
            Correct order: {correct_order_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    numbers = data["numbers"]
    order_type = data["order_type"]
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step ordering:
        
        **Task:** Order from {order_type}
        **Given numbers:** {', '.join([str(n) for n in numbers])}
        **Correct order:** {' → '.join([str(n) for n in correct_answer])}
        
        ### How to solve:
        """)
        
        # Show comparison process
        if order_type == "smallest to largest":
            st.markdown("**Finding smallest to largest:**")
            for i, num in enumerate(correct_answer):
                position = ["1st (smallest)", "2nd", "3rd", "4th (largest)"][i]
                st.markdown(f"- **{position}:** {num}")
        else:
            st.markdown("**Finding largest to smallest:**")
            for i, num in enumerate(correct_answer):
                position = ["1st (largest)", "2nd", "3rd", "4th (smallest)"][i]
                st.markdown(f"- **{position}:** {num}")
        
        # Show comparison strategy
        st.markdown("### 💡 Comparison strategy:")
        
        # Group by whole number parts for explanation
        whole_parts = {}
        for num in numbers:
            whole = int(num)
            if whole not in whole_parts:
                whole_parts[whole] = []
            whole_parts[whole].append(num)
        
        if len(whole_parts) > 1:
            st.markdown("**Step 1:** Compare whole number parts first")
            for whole in sorted(whole_parts.keys()):
                st.markdown(f"- Numbers starting with **{whole}**: {whole_parts[whole]}")
        
        st.markdown("**Step 2:** For numbers with same whole part, compare decimal places")
        for whole, group in whole_parts.items():
            if len(group) > 1:
                sorted_group = sorted(group)
                st.markdown(f"- Within **{whole}.x** numbers: {' < '.join([str(n) for n in sorted_group])}")
        
        st.markdown("""
        ### 🎯 Remember:
        - **Read the instruction carefully** - smallest→largest or largest→smallest?
        - **Compare systematically** - whole numbers first, then decimals
        - **Use place value** - 0.8 = 8 tenths, 0.75 = 75 hundredths
        - **Think about number lines** - which number comes first?
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_order = []
    st.session_state.available_numbers = []