import streamlit as st
import random

def run():
    """
    Main function to run the Inequalities with Addition and Subtraction practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/inequalities_with_addition_and_subtraction.py
    """
    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.question_count = 0
        st.session_state.correct_count = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("⚖️ Inequalities with Addition and Subtraction")
    st.markdown("*Practice with =, <, and > symbols and missing numbers*")
    st.markdown("---")
    
    # Progress indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.session_state.question_count > 0:
            accuracy = (st.session_state.correct_count / st.session_state.question_count) * 100
            st.markdown(f"**Score:** {st.session_state.correct_count}/{st.session_state.question_count} ({accuracy:.0f}%)")
        else:
            st.markdown("**Score:** Starting...")
        progress_text = f"Question #{st.session_state.question_count + 1}"
        st.markdown(f"*{progress_text}*")
    
    with col2:
        st.markdown("**⚖️ Inequalities**")
    
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
    with st.expander("💡 **Learn About Inequalities and Equations**", expanded=False):
        st.markdown("""
        ### ⚖️ Understanding Mathematical Symbols:
        
        #### **Equality Symbol (=)**
        - **Meaning:** "is equal to" or "is the same as"
        - **Example:** 8 + 5 = 13 (both sides have the same value)
        - **Rule:** Both sides must have exactly the same value
        
        #### **Greater Than Symbol (>)**
        - **Meaning:** "is greater than" or "is bigger than"
        - **Example:** 15 > 12 (15 is bigger than 12)
        - **Memory tip:** The open side points to the larger number
        - **Think:** The symbol "eats" the bigger number (like Pac-Man!)
        
        #### **Less Than Symbol (<)**
        - **Meaning:** "is less than" or "is smaller than"
        - **Example:** 7 < 10 (7 is smaller than 10)
        - **Memory tip:** The open side points to the larger number
        - **Same rule:** The symbol still "eats" the bigger number
        
        ### 🎯 **Two Types of Problems:**
        
        #### **Type 1: Missing Number Problems**
        - **Format:** Something like "18 = 5 + ?"
        - **Strategy:** Work backwards to find the missing number
        - **Example:** 18 = 5 + ? → Think: 5 + ? = 18 → ? = 18 - 5 = 13
        
        #### **Type 2: Inequality Symbol Problems**
        - **Format:** Something like "25 ? 17"
        - **Strategy:** Compare the two numbers to choose the right symbol
        - **Example:** 25 ? 17 → Since 25 is bigger than 17 → 25 > 17
        
        ### 🧮 **Problem-Solving Steps:**
        
        **For Missing Numbers:**
        1. **Look at what you know:** What numbers are given?
        2. **Identify the operation:** Addition or subtraction?
        3. **Work backwards:** Use the opposite operation
        4. **Check your answer:** Does it make the equation true?
        
        **For Inequality Symbols:**
        1. **Compare the numbers:** Which is bigger?
        2. **Remember the rule:** Open side points to the larger number
        3. **Choose the symbol:** >, <, or =
        4. **Double-check:** Read it aloud to see if it makes sense
        
        ### 💭 **Memory Tricks:**
        
        - **Alligator mouth:** The symbol is like an alligator that wants to eat the bigger number
        - **Arrow pointer:** The symbol points toward the larger number
        - **L for Less:** < looks like the letter L, which starts "Less than"
        - **Equal balance:** = means both sides balance perfectly like a scale
        
        ### 📈 **Examples to Practice:**
        
        **Missing Numbers:**
        - 12 = 7 + ? → Answer: 5 (because 7 + 5 = 12)
        - 20 - ? = 8 → Answer: 12 (because 20 - 12 = 8)
        
        **Inequality Symbols:**
        - 15 ? 23 → Answer: < (because 15 is less than 23)
        - 8 + 7 ? 14 → Answer: > (because 8 + 7 = 15, and 15 > 14)
        """)

def generate_new_question():
    """Generate a new inequality question"""
    
    # Choose question type randomly
    question_type = random.choice(["missing_number", "inequality_symbol"])
    
    if question_type == "missing_number":
        # Generate missing number question like "18 = 5 + ?"
        a = random.randint(5, 20)
        b = random.randint(1, 10)
        total = a + b
        correct = total - b  # This is the missing number
        
        # Choose format randomly
        formats = [
            f"{total} = {b} + ?",
            f"{total} = ? + {b}",
            f"? + {b} = {total}",
            f"{b} + ? = {total}"
        ]
        display_text = random.choice(formats)
        
        # Generate distractors (wrong answers)
        options = [correct]
        while len(options) < 3:
            distractor = correct + random.randint(-3, 3)
            if distractor > 0 and distractor not in options:
                options.append(distractor)
        
        random.shuffle(options)
        
        st.session_state.problem_data = {
            "type": "missing_number",
            "display_text": display_text,
            "correct_answer": str(correct),
            "options": [str(opt) for opt in options]
        }
        
    else:
        # Generate inequality symbol question like "25 ? 17"
        left = random.randint(10, 99)
        right = random.randint(10, 99)
        
        # Determine correct symbol
        if left > right:
            correct = ">"
        elif left < right:
            correct = "<"
        else:
            correct = "="
        
        display_text = f"{left} ? {right}"
        options = [">", "<", "="]
        
        st.session_state.problem_data = {
            "type": "inequality_symbol",
            "display_text": display_text,
            "correct_answer": correct,
            "options": options,
            "left_value": left,
            "right_value": right
        }
    
    st.session_state.current_question = "Which value or symbol makes this statement true?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### ⚖️ Mathematical Statement:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the mathematical statement in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #fff3e0; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #ff9800;
        font-family: 'Courier New', monospace;
        font-size: 32px;
        text-align: center;
        margin: 30px 0;
        color: #e65100;
        font-weight: bold;
    ">
        {data['display_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("inequality_form", clear_on_submit=False):
        if data["type"] == "missing_number":
            st.markdown("**🤔 What number goes in place of the ?**")
            display_format = lambda x: x
        else:
            st.markdown("**🤔 Which symbol makes the statement true?**")
            display_format = lambda x: f"**{x}**" if x != "=" else f"**{x}** (equals)"
        
        user_answer = st.radio(
            "Choose the correct answer:",
            options=data["options"],
            format_func=display_format,
            key="answer_choice"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
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
                st.session_state.question_count += 1
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    correct_answer = data["correct_answer"]
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct!**")
        st.session_state.correct_count += 1
        show_explanation(correct=True)
    else:
        st.error(f"❌ **Incorrect.** The correct answer is **{correct_answer}**.")
        show_explanation(correct=False)

def show_explanation(correct=True):
    """Show explanation for the answer"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **Click here for explanation**", expanded=not correct):
        if data["type"] == "missing_number":
            show_missing_number_explanation()
        else:
            show_inequality_explanation()

def show_missing_number_explanation():
    """Show explanation for missing number problems"""
    data = st.session_state.problem_data
    display_text = data["display_text"]
    correct_answer = data["correct_answer"]
    
    st.markdown(f"### 🧮 **Solving: {display_text}**")
    
    # Parse the equation to explain the solution
    if "=" in display_text and "+" in display_text:
        # This is an addition equation
        if display_text.startswith("?"):
            # Format like "? + 5 = 18"
            parts = display_text.replace("?", "X").split()
            if len(parts) >= 5:
                known_num = parts[2]
                total = parts[4]
                st.markdown(f"**Step 1:** We know that X + {known_num} = {total}")
                st.markdown(f"**Step 2:** To find X, we subtract: X = {total} - {known_num}")
                st.markdown(f"**Step 3:** Calculate: {total} - {known_num} = {correct_answer}")
                st.markdown(f"**Check:** {correct_answer} + {known_num} = {total} ✓")
        else:
            # Format like "18 = 5 + ?" or "18 = ? + 5"
            parts = display_text.split()
            if len(parts) >= 5:
                total = parts[0]
                if parts[2] == "?":
                    known_num = parts[4]
                else:
                    known_num = parts[2]
                st.markdown(f"**Step 1:** We know that {total} equals something plus {known_num}")
                st.markdown(f"**Step 2:** To find the missing number: {total} - {known_num}")
                st.markdown(f"**Step 3:** Calculate: {total} - {known_num} = {correct_answer}")
                st.markdown(f"**Check:** {known_num} + {correct_answer} = {total} ✓")
    
    st.markdown("### 💡 **Strategy:**")
    st.markdown("- **Addition problems:** Use subtraction to find the missing number")
    st.markdown("- **Check your work:** Plug the answer back into the original equation")

def show_inequality_explanation():
    """Show explanation for inequality symbol problems"""
    data = st.session_state.problem_data
    left_value = data["left_value"]
    right_value = data["right_value"]
    correct_answer = data["correct_answer"]
    
    st.markdown(f"### ⚖️ **Comparing: {left_value} and {right_value}**")
    
    if correct_answer == ">":
        st.markdown(f"**{left_value} > {right_value}** means \"{left_value} is greater than {right_value}\"")
        st.markdown(f"**Why:** {left_value} is bigger than {right_value}")
        st.markdown("**Remember:** The open side (>) points to the larger number")
    elif correct_answer == "<":
        st.markdown(f"**{left_value} < {right_value}** means \"{left_value} is less than {right_value}\"")
        st.markdown(f"**Why:** {left_value} is smaller than {right_value}")
        st.markdown("**Remember:** The open side (<) points to the larger number")
    else:  # equals
        st.markdown(f"**{left_value} = {right_value}** means \"{left_value} equals {right_value}\"")
        st.markdown(f"**Why:** {left_value} and {right_value} have the same value")
        st.markdown("**Remember:** = means both sides are exactly equal")
    
    st.markdown("### 💡 **Memory Tips:**")
    st.markdown("- **Alligator mouth:** The symbol 'eats' the bigger number")
    st.markdown("- **Arrow:** The point aims at the smaller number")
    st.markdown("- **Number line:** Larger numbers are further to the right")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer