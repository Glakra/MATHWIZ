import streamlit as st
import random

def run():
    """
    Main function to run the Choose Numbers with Sum/Difference practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/choose_numbers_with_a_particular_sum_or_difference.py
    """
    # Initialize session state for difficulty and game state
    if "sum_diff_difficulty" not in st.session_state:
        st.session_state.sum_diff_difficulty = {"max": 100}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("🎯 Choose Numbers with Sum or Difference")
    st.markdown("*Select the correct pair of numbers to complete the equation*")
    st.markdown("---")
    
    # Difficulty indicator
    current_max = st.session_state.sum_diff_difficulty["max"]
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** Numbers up to {current_max}")
        # Progress bar (20 to 1000)
        progress = min((current_max - 20) / 980, 1.0)  # Convert 20-1000 to 0-1
        st.progress(progress, text=f"Max number: {current_max}")
    
    with col2:
        if current_max <= 100:
            st.markdown("**🟡 Beginner**")
        elif current_max <= 500:
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
        - **Look at the equation** with a target sum or difference
        - **Choose TWO numbers** from the number box that make the equation correct
        - **Select the first number** and **second number** from the dropdown menus
        - **Submit your answer** to see if you're correct!
        
        ### Problem-Solving Strategy:
        1. **Read the equation:** Is it addition (+) or subtraction (−)?
        2. **Look at the target:** What result do you need to get?
        3. **Test combinations:** Try different pairs of numbers mentally
        4. **Check your work:** Does your chosen pair give the right answer?
        
        ### Mathematical Thinking:
        - **For addition:** Find two numbers that add up to the target
          - Example: ? + ? = 15 → Look for pairs like 7 + 8, 6 + 9, etc.
        - **For subtraction:** Find two numbers where first minus second equals target
          - Example: ? − ? = 5 → Look for pairs like 12 − 7, 15 − 10, etc.
        
        ### Tips for Success:
        - **Start with estimation:** About how big should each number be?
        - **Work systematically:** Try the largest number first, then work down
        - **Use number sense:** If the target is small, the numbers are probably close
        - **Check impossible pairs:** Some combinations won't work at all
        
        ### Addition Strategies:
        - **Doubles:** Look for numbers that are the same (8 + 8 = 16)
        - **Near doubles:** Numbers that are close (8 + 9 = 17)
        - **Make 10:** Find pairs that make 10, then add more (6 + 4 + 5 = 15)
        - **Compatible numbers:** Numbers that are easy to add (25 + 75 = 100)
        
        ### Subtraction Strategies:
        - **Count up:** From the smaller to the larger number
        - **Count back:** From the larger number
        - **Use addition:** What plus the result equals the first number?
        - **Look for patterns:** Numbers ending in the same digit often work well
        
        ### Difficulty Levels:
        - **🟡 Numbers up to 100:** Learn basic number relationships
        - **🟠 Numbers up to 500:** Build fluency with larger numbers
        - **🔴 Numbers up to 1000:** Master complex number combinations
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger and more challenging
        - ❌ **Wrong answer:** Numbers get smaller for more practice
        - 🎯 **Goal:** Master number relationships up to 1,000!
        """)

def generate_new_question():
    """Generate a new choose sum/difference problem"""
    max_val = st.session_state.sum_diff_difficulty["max"]
    
    # Choose operation randomly
    mode = random.choice(["+", "-"])
    
    if mode == "+":
        # For addition, create two numbers that add to target
        a = random.randint(1, max_val // 2)
        b = random.randint(1, max_val // 2)
        target = a + b
    else:
        # For subtraction, create two numbers where first - second = target
        a = random.randint(max_val // 2, max_val)
        b = random.randint(1, a - 1)
        target = a - b
    
    # Generate distractors (wrong numbers)
    distractors = []
    while len(distractors) < 2:
        d = random.randint(1, max_val)
        if d not in (a, b) and d not in distractors:
            distractors.append(d)
    
    # Combine correct answers with distractors and shuffle
    choices = [a, b] + distractors
    random.shuffle(choices)
    
    st.session_state.problem_data = {
        "mode": mode,
        "target": target,
        "correct_a": a,
        "correct_b": b,
        "choices": choices
    }
    
    operation_name = "addition" if mode == "+" else "subtraction"
    st.session_state.current_question = f"Choose two numbers to complete the {operation_name} sentence:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### 🎯 Number Selection Challenge:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display available numbers in a nice box
    numbers_display = " ".join([f"`{n}`" for n in data["choices"]])
    st.markdown(f"""
    <div style="
        background-color: #e3f2fd; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #2196f3;
        margin: 20px 0;
        text-align: center;
    ">
        <h4 style="margin-bottom: 15px; color: #1976d2;">Available Numbers:</h4>
        <div style="font-size: 18px; font-family: monospace; font-weight: bold; color: #0d47a1;">
            {numbers_display}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the equation template
    st.markdown("### 🧮 Complete this equation:")
    
    equation_html = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        color: #2c3e50;
    ">
        <div style="margin-bottom: 15px;">
            <span style="background-color: #fff3cd; padding: 8px 12px; border-radius: 5px; border: 2px dashed #856404;">?</span>
            <span style="margin: 0 15px;">{data['mode']}</span>
            <span style="background-color: #fff3cd; padding: 8px 12px; border-radius: 5px; border: 2px dashed #856404;">?</span>
            <span style="margin: 0 15px;">=</span>
            <span style="background-color: #d4edda; padding: 8px 12px; border-radius: 5px; font-weight: bold;">{data['target']}</span>
        </div>
    </div>
    """
    
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Answer selection section
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**🤔 Select your two numbers:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_number = st.selectbox(
                "First number:",
                options=data["choices"],
                key="first_num"
            )
        
        with col2:
            second_number = st.selectbox(
                "Second number:",
                options=data["choices"],
                key="second_num"
            )
        
        # Show preview of their equation
        if first_number != second_number:
            preview_result = first_number + second_number if data["mode"] == "+" else first_number - second_number
            st.markdown(f"**Preview:** {first_number} {data['mode']} {second_number} = {preview_result}")
        else:
            st.warning("⚠️ Please choose two different numbers!")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            if first_number == second_number:
                st.error("❌ Please choose two different numbers!")
            else:
                st.session_state.user_first = first_number
                st.session_state.user_second = second_number
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
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    user_first = st.session_state.user_first
    user_second = st.session_state.user_second
    
    # Check if the numbers are in the choices
    valid_choices = user_first in data["choices"] and user_second in data["choices"]
    
    # Calculate the result of their selection
    if data["mode"] == "+":
        user_result = user_first + user_second
    else:
        user_result = user_first - user_second
    
    # Check if they got the correct target
    correct_target = user_result == data["target"]
    
    # Check if they used the exact correct pair (in any order)
    correct_pair = ((user_first == data["correct_a"] and user_second == data["correct_b"]) or 
                   (user_first == data["correct_b"] and user_second == data["correct_a"]))
    
    if valid_choices and correct_target:
        st.success("🎉 **Excellent! Your numbers make the equation correct!**")
        
        # Increase difficulty
        old_max = st.session_state.sum_diff_difficulty["max"]
        st.session_state.sum_diff_difficulty["max"] = min(
            st.session_state.sum_diff_difficulty["max"] + 50, 1000
        )
        
        # Show encouragement based on difficulty
        if st.session_state.sum_diff_difficulty["max"] == 1000 and old_max < 1000:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered number relationships up to 1,000!**")
        elif old_max < st.session_state.sum_diff_difficulty["max"]:
            st.info(f"⬆️ **Great job! Difficulty increased - now working with numbers up to {st.session_state.sum_diff_difficulty['max']}**")
    
    else:
        st.error(f"❌ **Not quite right.** Your equation: {user_first} {data['mode']} {user_second} = {user_result}")
        
        # Decrease difficulty
        old_max = st.session_state.sum_diff_difficulty["max"]
        st.session_state.sum_diff_difficulty["max"] = max(
            20, st.session_state.sum_diff_difficulty["max"] - 20
        )
        
        if old_max > st.session_state.sum_diff_difficulty["max"]:
            st.warning(f"⬇️ **Let's practice with smaller numbers. Now working with numbers up to {st.session_state.sum_diff_difficulty['max']}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### 🧮 Correct solution:")
        
        correct_equation = f"{data['correct_a']} {data['mode']} {data['correct_b']} = {data['target']}"
        st.markdown(f"**One correct answer:** {correct_equation}")
        
        # Show alternative if subtraction and order matters
        if data["mode"] == "-":
            alt_equation = f"{data['correct_b']} {data['mode']} {data['correct_a']} = {data['correct_b'] - data['correct_a']}"
            st.markdown(f"**Note:** {alt_equation} would give a different result")
            st.markdown("**Remember:** In subtraction, order matters! a − b ≠ b − a")
        else:
            alt_equation = f"{data['correct_b']} {data['mode']} {data['correct_a']} = {data['target']}"
            st.markdown(f"**Alternative:** {alt_equation} (addition is commutative)")
            st.markdown("**Remember:** In addition, order doesn't matter! a + b = b + a")
        
        # Strategy explanation
        st.markdown("### 💡 **How to find the right numbers:**")
        
        if data["mode"] == "+":
            st.markdown(f"**For addition:** Look for two numbers that add up to {data['target']}")
            st.markdown("**Strategy:** Try the largest numbers first, or look for familiar number pairs")
            st.markdown(f"**Think:** What plus {data['correct_b']} equals {data['target']}? Answer: {data['correct_a']}")
        else:
            st.markdown(f"**For subtraction:** Look for two numbers where first minus second equals {data['target']}")
            st.markdown("**Strategy:** Start with larger numbers for the first position")
            st.markdown(f"**Think:** What minus {data['correct_b']} equals {data['target']}? Answer: {data['correct_a']}")
        
        # Available numbers reminder
        numbers_list = ", ".join(map(str, data["choices"]))
        st.markdown(f"**Available numbers were:** {numbers_list}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_first" in st.session_state:
        del st.session_state.user_first
    if "user_second" in st.session_state:
        del st.session_state.user_second