import streamlit as st
import random

def run():
    """
    Main function to run the Decompose Fractions practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add and subtract fractions/decompose_fractions.py
    """
    # Initialize session state for difficulty and game state
    if "decompose_flex_difficulty" not in st.session_state:
        st.session_state.decompose_flex_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_values = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🧩 Decompose Fractions")
    st.markdown("*Write fractions as sums of other fractions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decompose_flex_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Two parts (denominators 2-4)",
            2: "Two parts (denominators 5-8)",
            3: "Three parts (denominators 3-6)",
            4: "Three parts (denominators 7-10)",
            5: "Mixed parts (all combinations)"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
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
        1. Look at the fraction on the left
        2. Fill in the blanks to make a sum that equals the fraction
        3. Click the fraction buttons to fill each blank
        4. You can use the same fraction multiple times!
        
        ### Examples:
        - **5/6** = 2/6 + 3/6
        - **5/6** = 1/6 + 1/6 + 3/6
        - **2/3** = 1/3 + 1/3
        - **4/5** = 2/5 + 2/5
        - **7/8** = 3/8 + 4/8
        
        ### Rules:
        - All fractions must have the same denominator
        - The sum must equal the target fraction
        - You can use any combination that works!
        
        ### Tips:
        - Think about different ways to make the number
        - Try using bigger fractions first, then fill in with smaller ones
        - Remember: 3/6 = 1/6 + 2/6 = 1/6 + 1/6 + 1/6
        """)

def generate_new_question():
    """Generate a new decompose fractions question"""
    difficulty = st.session_state.decompose_flex_difficulty
    
    # Determine number of parts and denominator range
    if difficulty == 1:
        num_parts = 2
        denominator = random.randint(2, 4)
    elif difficulty == 2:
        num_parts = 2
        denominator = random.randint(5, 8)
    elif difficulty == 3:
        num_parts = 3
        denominator = random.randint(3, 6)
    elif difficulty == 4:
        num_parts = 3
        denominator = random.randint(7, 10)
    else:  # difficulty == 5
        num_parts = random.choice([2, 3, 4])
        denominator = random.randint(3, 10)
    
    # Generate target numerator (must be decomposable into num_parts)
    # Ensure it's at least num_parts (so we can decompose it)
    min_numerator = num_parts
    max_numerator = min(denominator - 1, num_parts * (denominator - 1))
    
    # For lower difficulties, keep numerators reasonable
    if difficulty <= 2:
        max_numerator = min(max_numerator, denominator - 1)
    
    numerator = random.randint(min_numerator, max_numerator)
    
    # Create all possible fraction options (1/d through numerator/d)
    options = []
    for i in range(1, denominator + 1):
        options.append(f"{i}/{denominator}")
    
    # Limit options to make interface cleaner
    # Always include useful fractions
    if len(options) > 6:
        # Keep 1/d, 2/d, ..., and some others
        useful_nums = [1, 2]
        if numerator > 2:
            useful_nums.append(numerator - 1)
        if numerator > 3:
            useful_nums.append(numerator // 2)
        useful_nums.append(numerator)
        useful_nums.append(denominator)
        
        # Remove duplicates and sort
        useful_nums = sorted(list(set([n for n in useful_nums if n <= denominator])))
        
        options = [f"{n}/{denominator}" for n in useful_nums[:6]]
    
    # Initialize selected values
    st.session_state.selected_values = [""] * num_parts
    
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "fraction": f"{numerator}/{denominator}",
        "num_parts": num_parts,
        "options": options
    }
    
    # Generate the question text
    parts_text = {2: "two", 3: "three", 4: "four"}
    st.session_state.current_question = f"Write {numerator}/{denominator} as a sum of {parts_text.get(num_parts, str(num_parts))} fractions."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the equation with blanks
    st.markdown("")  # Add space
    
    # Create container for equation
    equation_container = st.container()
    
    with equation_container:
        # Calculate columns needed
        total_cols = 2 + (data["num_parts"] * 2 - 1)  # fraction + = + blanks + plus signs
        cols = st.columns(total_cols)
        
        # Original fraction
        with cols[0]:
            st.markdown(f"""
            <div style="
                background-color: #f5f5f5;
                border: 3px solid #333;
                padding: 15px 25px;
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 10px;
                color: #333;
            ">{data['fraction']}</div>
            """, unsafe_allow_html=True)
        
        # Equal sign
        with cols[1]:
            st.markdown(f"""
            <div style="
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                padding: 15px;
                margin-top: 10px;
                color: #333;
            ">=</div>
            """, unsafe_allow_html=True)
        
        # Blanks and plus signs
        for i in range(data["num_parts"]):
            blank_col_idx = 2 + (i * 2)
            
            # Display blank or filled value
            with cols[blank_col_idx]:
                value = st.session_state.selected_values[i] if i < len(st.session_state.selected_values) else ""
                
                if value:
                    # Filled box with better contrast
                    st.markdown(f"""
                    <div style="
                        background-color: #2196F3;
                        border: 3px solid #1976D2;
                        padding: 15px;
                        text-align: center;
                        font-size: 22px;
                        font-weight: bold;
                        border-radius: 6px;
                        margin-top: 10px;
                        min-height: 60px;
                        min-width: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                    ">{value}</div>
                    """, unsafe_allow_html=True)
                else:
                    # Empty box - more visible with light blue background
                    st.markdown(f"""
                    <div style="
                        background-color: #e6f3ff;
                        border: 3px solid #2196F3;
                        padding: 15px;
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                        border-radius: 6px;
                        margin-top: 10px;
                        min-height: 60px;
                        min-width: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                    ">&nbsp;</div>
                    """, unsafe_allow_html=True)
            
            # Plus sign (if not last blank)
            if i < data["num_parts"] - 1:
                plus_col_idx = blank_col_idx + 1
                with cols[plus_col_idx]:
                    st.markdown(f"""
                    <div style="
                        text-align: center;
                        font-size: 32px;
                        font-weight: bold;
                        padding: 15px;
                        margin-top: 10px;
                        color: #333;
                    ">+</div>
                    """, unsafe_allow_html=True)
    
    # Number buttons
    st.markdown("")  # Add space
    st.markdown("### Click to select:")
    
    button_cols = st.columns(len(data["options"]))
    
    for idx, option in enumerate(data["options"]):
        with button_cols[idx]:
            if st.button(
                option,
                key=f"option_{idx}",
                use_container_width=True,
                type="secondary"
            ):
                # Find the first empty slot
                for i in range(len(st.session_state.selected_values)):
                    if st.session_state.selected_values[i] == "":
                        st.session_state.selected_values[i] = option
                        st.rerun()
                        break
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear All", type="secondary", use_container_width=True):
            st.session_state.selected_values = [""] * data["num_parts"]
            st.rerun()
    
    with col2:
        if st.button("⬅️ Remove Last", type="secondary", use_container_width=True):
            # Find the last filled slot and clear it
            for i in range(len(st.session_state.selected_values) - 1, -1, -1):
                if st.session_state.selected_values[i] != "":
                    st.session_state.selected_values[i] = ""
                    st.rerun()
                    break
    
    with col3:
        # Check if all blanks are filled
        all_filled = all(val != "" for val in st.session_state.selected_values)
        if all_filled:
            submit_button = st.button(
                "✅ Submit",
                type="primary",
                use_container_width=True
            )
            
            if submit_button:
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
        else:
            st.button(
                "✅ Submit",
                type="secondary",
                use_container_width=True,
                disabled=True
            )
    
    # Show feedback
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.question_data
    user_answer = st.session_state.selected_values
    
    # Calculate the sum of user's fractions
    user_sum = 0
    for frac in user_answer:
        if frac:
            parts = frac.split('/')
            user_sum += int(parts[0])
    
    # Check if answer is correct
    is_correct = (user_sum == data["numerator"])
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete equation
        equation = f"{data['fraction']} = " + " + ".join(user_answer)
        st.success(f"✓ {equation}")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.decompose_flex_difficulty
        st.session_state.decompose_flex_difficulty = min(
            st.session_state.decompose_flex_difficulty + 1, 5
        )
        
        if st.session_state.decompose_flex_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've mastered decomposing fractions!**")
        elif old_difficulty < st.session_state.decompose_flex_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decompose_flex_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they entered
        user_equation = f"{data['fraction']} = " + " + ".join(user_answer)
        st.error(f"You entered: {user_equation}")
        
        # Calculate what they got
        st.error(f"Your sum equals: {user_sum}/{data['denominator']}")
        
        # Show a correct example
        show_example_solution(data)
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.decompose_flex_difficulty
        st.session_state.decompose_flex_difficulty = max(
            st.session_state.decompose_flex_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decompose_flex_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.decompose_flex_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_example_solution(data):
    """Show an example of a correct solution"""
    numerator = data["numerator"]
    denominator = data["denominator"]
    num_parts = data["num_parts"]
    
    # Generate a valid decomposition
    if num_parts == 2:
        # Simple split
        part1 = numerator // 2
        part2 = numerator - part1
        example = f"{part1}/{denominator} + {part2}/{denominator}"
    elif num_parts == 3:
        # Try to split somewhat evenly
        part1 = numerator // 3
        part2 = numerator // 3
        part3 = numerator - part1 - part2
        example = f"{part1}/{denominator} + {part2}/{denominator} + {part3}/{denominator}"
    else:
        # Generic split
        parts = []
        remaining = numerator
        for i in range(num_parts - 1):
            part = max(1, remaining // (num_parts - i))
            parts.append(f"{part}/{denominator}")
            remaining -= part
        parts.append(f"{remaining}/{denominator}")
        example = " + ".join(parts)
    
    st.success(f"Example correct answer: {numerator}/{denominator} = {example}")

def show_explanation():
    """Show step-by-step explanation for decomposition"""
    data = st.session_state.question_data
    numerator = data["numerator"]
    denominator = data["denominator"]
    num_parts = data["num_parts"]
    
    with st.expander("📖 **Understanding Fraction Decomposition**", expanded=True):
        st.markdown(f"""
        ### Decomposing {numerator}/{denominator} into {num_parts} fractions
        
        **What does decomposition mean?**
        - Breaking a fraction into a sum of smaller fractions
        - All fractions must have the same denominator ({denominator})
        - The numerators must add up to {numerator}
        
        **How to think about it:**
        - You need to find {num_parts} numbers that add up to {numerator}
        - Each number becomes the numerator of a fraction with denominator {denominator}
        
        **Examples of valid decompositions:**
        """)
        
        # Show different valid decompositions
        if num_parts == 2:
            for i in range(1, numerator):
                j = numerator - i
                st.markdown(f"- {i}/{denominator} + {j}/{denominator} = {numerator}/{denominator}")
                if i >= 3:  # Limit examples
                    break
        else:
            # Show one example for 3+ parts
            if numerator >= num_parts:
                parts = ["1"] * (num_parts - 1)
                last = numerator - (num_parts - 1)
                parts.append(str(last))
                example = " + ".join([f"{p}/{denominator}" for p in parts])
                st.markdown(f"- {example} = {numerator}/{denominator}")
        
        st.markdown(f"""
        **Remember:**
        - The denominators stay the same ({denominator})
        - The numerators must add up to {numerator}
        - You can use the same fraction multiple times!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_values = []
    if "user_answer" in st.session_state:
        del st.session_state.user_answer