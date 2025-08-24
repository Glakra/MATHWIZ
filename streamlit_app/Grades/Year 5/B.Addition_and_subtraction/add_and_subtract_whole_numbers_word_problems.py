import streamlit as st
import random

def run():
    """
    Main function to run the Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/add_and_subtract_whole_numbers_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = {"min": 10, "max": 100}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_text = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("📝 Word Problems Practice")
    st.markdown("*Solve real-world addition and subtraction problems*")
    st.markdown("---")
    
    # Difficulty indicator
    current_max = st.session_state.word_problem_difficulty["max"]
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
        - **Read the word problem carefully**
        - **Identify what operation to use** (addition or subtraction)
        - **Type your answer** in the input box
        - **Check your work** before submitting
        
        ### Problem-Solving Strategy:
        1. **Understand:** What is the problem asking?
        2. **Plan:** What operation do I need?
        3. **Solve:** Do the math carefully
        4. **Check:** Does my answer make sense?
        
        ### Key Words to Look For:
        - **Addition:** total, altogether, combined, sum, plus, more, gained, won
        - **Subtraction:** difference, less, fewer, minus, lost, gave away, left, remained
        
        ### Tips for Success:
        - **Read twice:** Make sure you understand what's happening
        - **Visualize:** Picture the problem in your head
        - **Estimate:** Does your answer seem reasonable?
        - **Units matter:** Include $ for money problems when appropriate
        
        ### Difficulty Progression:
        - ✅ **Correct answers:** Numbers get bigger (more challenging)
        - ❌ **Wrong answers:** Numbers get smaller (easier practice)
        - 🎯 **Goal:** Master problems with numbers up to 1,000!
        """)

def generate_new_question():
    """Generate a new word problem"""
    difficulty = st.session_state.word_problem_difficulty
    
    # Simple templates
    simple_templates = [
        lambda x, y: (f"Ali had {x} marbles. He won {y} more in a game. How many marbles does he have now?", x + y),
        lambda x, y: (f"A zoo had {x} birds. {y} flew away. How many birds are left?", x - y),
        lambda x, y: (f"A bookstore sold {x} books in the morning and {y} books in the afternoon. How many books were sold in total?", x + y),
        lambda x, y: (f"There were {x} people at a concert. {y} people left early. How many people remained?", x - y),
        lambda x, y: (f"A warehouse received {x} boxes on Monday and {y} on Tuesday. How many boxes in total?", x + y),
        lambda x, y: (f"Sarah had {x} candies. She gave {y} to her friend. How many candies does she have now?", x - y),
        lambda x, y: (f"A farm had {x} sheep and {y} cows. How many animals are there in total?", x + y),
        lambda x, y: (f"Leo collected {x} stickers. He lost {y} of them. How many does he still have?", x - y)
    ]

    # Story-based templates
    story_templates = [
        lambda x, y: (
            f"The Oxford Secondary School canteen goes through a lot of peanut butter. "
            f"Currently, they have {x} grams of regular peanut butter in stock. "
            f"They also have {y} grams of crunchy peanut butter. "
            f"How many grams do they have in total?",
            x + y
        ),
        lambda x, y: (
            f"A local library had {x} fiction books on its shelves. "
            f"During a donation drive, they received {y} additional fiction books. "
            f"How many fiction books are now in the library?",
            x + y
        ),
        lambda x, y: (
            f"The school bus transported {x} students in the morning. "
            f"In the afternoon, it transported {y} fewer students than the morning. "
            f"How many students were transported in the afternoon?",
            x - y
        ),
        lambda x, y: (
            f"A science lab had {x} ml of distilled water stored in flasks. "
            f"After an experiment, {y} ml were used. "
            f"How much distilled water remains in the lab?",
            x - y
        ),
        lambda x, y: (
            f"Lena baked {x} cookies for the school fundraiser. Her brother baked {y} cookies as well. "
            f"How many cookies did they bake together?",
            x + y
        )
    ]

    # Finance/money templates
    finance_templates = [
        lambda total, part: (
            f"There was an oil spill in a coral reef. As a result, it cost the oil company a combined total of ${total} in cleanup and repairs. "
            f"The repairs alone cost ${part}. How much money did the cleanup cost?",
            total - part
        ),
        lambda total, part: (
            f"A school spent ${total} on supplies. If ${part} was spent on textbooks, how much was spent on other supplies?",
            total - part
        ),
        lambda total, part: (
            f"A charity raised ${total} for an event. If ${part} was spent on venue and food, how much money remains for decorations and activities?",
            total - part
        ),
        lambda total, part: (
            f"A family planned a vacation budget of ${total}. They booked flights for ${part}. "
            f"How much money is left for accommodation and activities?",
            total - part
        ),
        lambda total, part: (
            f"A builder charged a client ${total} in total. If materials cost ${part}, how much was charged for labor?",
            total - part
        )
    ]
    
    # Combine all templates
    all_templates = simple_templates + story_templates + finance_templates
    
    # Generate numbers based on difficulty
    x = random.randint(difficulty["min"], difficulty["max"])
    y = random.randint(difficulty["min"] // 2, difficulty["max"] // 2)
    
    # Pick a random template
    template_func = random.choice(all_templates)
    question, answer = template_func(x, y)
    
    st.session_state.question_text = question
    st.session_state.correct_answer = str(answer)
    st.session_state.current_question = "Solve this word problem:"

def display_question():
    """Display the current question interface"""
    # Display question with nice formatting
    st.markdown("### 📝 Word Problem:")
    
    # Display the problem in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        color: #2c3e50;
    ">
        {st.session_state.question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**💭 Your Answer:**")
        
        # Determine if this is a money problem
        is_money_problem = "$" in st.session_state.question_text
        
        if is_money_problem:
            user_answer = st.number_input(
                "Enter your answer (numbers only, no $ sign):",
                min_value=0,
                step=1,
                format="%d",
                key="money_answer"
            )
        else:
            user_answer = st.number_input(
                "Enter your answer:",
                min_value=0,
                step=1,
                format="%d",
                key="regular_answer"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = str(int(user_answer))
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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_max = st.session_state.word_problem_difficulty["max"]
        st.session_state.word_problem_difficulty["max"] = min(
            st.session_state.word_problem_difficulty["max"] + 50, 1000
        )
        
        # Show encouragement based on difficulty
        if st.session_state.word_problem_difficulty["max"] == 1000 and old_max < 1000:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered word problems with numbers up to 1,000!**")
        elif old_max < st.session_state.word_problem_difficulty["max"]:
            st.info(f"⬆️ **Great job! Difficulty increased - now working with numbers up to {st.session_state.word_problem_difficulty['max']}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty
        old_max = st.session_state.word_problem_difficulty["max"]
        st.session_state.word_problem_difficulty["max"] = max(
            st.session_state.word_problem_difficulty["max"] - 10, 20
        )
        
        if old_max > st.session_state.word_problem_difficulty["max"]:
            st.warning(f"⬇️ **Let's practice with smaller numbers. Now working with numbers up to {st.session_state.word_problem_difficulty['max']}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    question_text = st.session_state.question_text
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### 🤔 Let's work through this step by step:")
        st.markdown(f"**Problem:** {question_text}")
        
        # Try to identify the operation based on keywords
        question_lower = question_text.lower()
        
        if any(word in question_lower for word in ["total", "altogether", "combined", "more", "won", "received", "additional"]):
            operation = "Addition"
            explanation = "This is an **addition** problem because we're combining or adding amounts together."
        elif any(word in question_lower for word in ["left", "remained", "flew away", "gave", "used", "lost", "fewer"]):
            operation = "Subtraction" 
            explanation = "This is a **subtraction** problem because we're taking away or finding the difference."
        else:
            operation = "Unknown"
            explanation = "Look for key words to identify whether to add or subtract."
        
        st.markdown(f"**Operation needed:** {operation}")
        st.markdown(f"**Why:** {explanation}")
        st.markdown(f"**Correct answer:** {correct_answer}")
        
        # Additional tip
        st.markdown("### 💡 **Next time, remember:**")
        if operation == "Addition":
            st.markdown("- Look for words like: *total, altogether, combined, more, plus, gained*")
        elif operation == "Subtraction":
            st.markdown("- Look for words like: *left, remained, less, minus, lost, gave away*")
        else:
            st.markdown("- Read carefully and identify whether you're combining amounts or taking them away")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_text = ""
    if "user_answer" in st.session_state:
        del st.session_state.user_answer