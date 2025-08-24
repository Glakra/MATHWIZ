import streamlit as st
import random

def run():
    """
    Main function to run the Multiplication Facts Word Problems practice activity.
    This gets called when the subtopic is loaded from the main navigation.
    """
    # Initialize session state for difficulty and game state
    if "multiplication_word_difficulty" not in st.session_state:
        st.session_state.multiplication_word_difficulty = 1  # Start with difficulty level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📚 Multiplication Facts to 10: Word Problems")
    st.markdown("*Solve real-world multiplication problems using facts to 10*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiplication_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 10)
        progress = (difficulty_level - 1) / 9  # Convert 1-10 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/10")
    
    with col2:
        if difficulty_level <= 3:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 7:
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
        - **Identify what you need to multiply**
        - **Find the two numbers** in the problem
        - **Calculate the answer** using multiplication facts
        - **Include the unit** in your thinking (but just enter the number)
        
        ### Steps to Solve Word Problems:
        1. **Read twice:** Read the problem slowly and carefully
        2. **Find the numbers:** Look for the two amounts to multiply
        3. **Identify the operation:** Look for words like "each," "groups of," "total"
        4. **Set up the problem:** Write it as a multiplication
        5. **Solve and check:** Use your multiplication facts
        
        ### Key Words for Multiplication:
        - **"each"** → tells you one factor
        - **"groups of"** → shows multiplication
        - **"total"** → what you're finding
        - **"in all"** → the final answer
        - **"altogether"** → the complete amount
        
        ### Example Problem:
        *"There are 6 pencils in each box. How many pencils are in 4 boxes?"*
        - **Numbers:** 6 and 4
        - **Operation:** 6 × 4 (6 pencils × 4 boxes)
        - **Answer:** 24 pencils
        
        ### Problem Types You'll See:
        - 📦 **Boxes and items:** Cards in boxes, cookies in packages
        - 🏫 **School scenarios:** Students in classrooms, books on shelves
        - 🌸 **Groups in nature:** Flowers in pots, animals in groups
        - 🍽️ **Kitchen math:** Items on trays, ingredients in recipes
        
        ### Difficulty Levels:
        - **🟡 Levels 1-3:** Easier numbers (2-5 range)
        - **🟠 Levels 4-7:** Medium numbers (3-8 range)
        - **🔴 Levels 8-10:** Harder numbers (5-10 range)
        
        ### Scoring:
        - ✅ **Correct answer:** Level increases
        - ❌ **Wrong answer:** Level decreases
        - 🎯 **Goal:** Reach Level 10 mastery!
        """)

def generate_new_question():
    """Generate a new multiplication word problem based on difficulty level"""
    difficulty = st.session_state.multiplication_word_difficulty
    
    # Adjust number ranges based on difficulty
    if difficulty <= 3:
        min_factor, max_factor = 2, 5
    elif difficulty <= 7:
        min_factor, max_factor = 3, 8
    else:  # difficulty 8-10
        min_factor, max_factor = 5, 10
    
    # Generate two factors
    a = random.randint(min_factor, max_factor)
    b = random.randint(min_factor, max_factor)
    correct_answer = a * b
    
    # Scenario templates with more variety
    templates = [
        ("A card factory puts **{a}** greeting cards in each box. How many greeting cards will there be in **{b}** boxes?", "greeting cards", "🎴"),
        ("Each pencil case has **{a}** pencils. How many pencils are there in **{b}** pencil cases?", "pencils", "✏️"),
        ("A shelf has **{a}** books on each row. If there are **{b}** rows, how many books are on the shelf?", "books", "📚"),
        ("There are **{a}** students in each of **{b}** classrooms. How many students are there in total?", "students", "👨‍🎓"),
        ("Each flower pot contains **{a}** flowers. If you have **{b}** pots, how many flowers are there?", "flowers", "🌸"),
        ("A baker puts **{a}** cookies in each box. How many cookies are there in **{b}** boxes?", "cookies", "🍪"),
        ("A tray holds **{a}** cups. How many cups are there on **{b}** trays?", "cups", "☕"),
        ("Each packet has **{a}** stickers. How many stickers are in **{b}** packets?", "stickers", "⭐"),
        ("A parking lot has **{a}** cars in each row. There are **{b}** rows. How many cars in total?", "cars", "🚗"),
        ("Each tree has **{a}** apples. How many apples are on **{b}** trees?", "apples", "🍎"),
        ("A toy store puts **{a}** action figures in each package. How many figures are in **{b}** packages?", "action figures", "🎭"),
        ("Each pizza has **{a}** slices. How many slices are there in **{b}** pizzas?", "pizza slices", "🍕")
    ]
    
    # Select a random template
    template, unit, emoji = random.choice(templates)
    question_text = template.format(a=a, b=b)
    
    st.session_state.question_data = {
        "question_text": question_text,
        "factor_a": a,
        "factor_b": b,
        "unit": unit,
        "emoji": emoji
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = question_text

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Word Problem:")
    
    # Display the question in a highlighted box with emoji
    st.markdown(f"""
    <div style="
        background-color: #fff3cd; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #ffc107;
        font-size: 18px;
        margin: 20px 0;
        line-height: 1.8;
    ">
        <div style="font-size: 24px; margin-bottom: 15px;">{data['emoji']}</div>
        {data['question_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Show the multiplication setup
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="
            background-color: #e8f4fd; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
            margin: 15px 0;
            border: 2px dashed #1f77b4;
        ">
            <div style="font-size: 16px; color: #666; margin-bottom: 5px;">Think: What multiplication do I need?</div>
            <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">
                {data['factor_a']} × {data['factor_b']} = ?
            </div>
            <div style="font-size: 14px; color: #666; margin-top: 5px;">
                {data['factor_a']} groups of {data['factor_b']} {data['unit']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        st.markdown(f"**How many {data['unit']} are there in total?**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.number_input(
                f"Your answer:",
                min_value=0,
                max_value=200,
                value=None,
                step=1,
                key="word_problem_input",
                placeholder="Enter the total number"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer is not None:
            st.session_state.user_answer = int(user_answer)
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Correct! There are {correct_answer} {data['unit']}!**")
        
        # Increase difficulty (max level 10)
        old_difficulty = st.session_state.multiplication_word_difficulty
        st.session_state.multiplication_word_difficulty = min(
            st.session_state.multiplication_word_difficulty + 1, 10
        )
        
        # Show encouragement based on difficulty
        if st.session_state.multiplication_word_difficulty == 10 and old_difficulty < 10:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered multiplication word problems!**")
        elif old_difficulty < st.session_state.multiplication_word_difficulty:
            new_level = st.session_state.multiplication_word_difficulty
            st.info(f"⬆️ **Level up! Now on Level {new_level} - {get_level_description(new_level)}**")
        
        # Show the solution method
        st.info(f"✨ **Solution:** {data['factor_a']} × {data['factor_b']} = {correct_answer}")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer} {data['unit']}**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.multiplication_word_difficulty
        st.session_state.multiplication_word_difficulty = max(
            st.session_state.multiplication_word_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.multiplication_word_difficulty:
            new_level = st.session_state.multiplication_word_difficulty
            st.warning(f"⬇️ **Back to Level {new_level}. Let's practice with easier problems!**")
        
        # Show explanation
        show_explanation()

def get_level_description(level):
    """Get description for difficulty level"""
    if level <= 3:
        return "Easier numbers"
    elif level <= 7:
        return "Medium challenge"
    else:
        return "Expert level"

def show_explanation():
    """Show step-by-step explanation for solving the word problem"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here to see how to solve this step-by-step**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution:
        
        **The Problem:** {data['question_text'].replace('**', '')}
        
        ### Breaking it down:
        1. **Identify the numbers:** {data['factor_a']} and {data['factor_b']}
        2. **Understand what each means:**
           - {data['factor_a']} = items in each group
           - {data['factor_b']} = number of groups
        3. **Set up the multiplication:** {data['factor_a']} × {data['factor_b']}
        4. **Calculate:** {data['factor_a']} × {data['factor_b']} = **{correct_answer}**
        5. **Answer with units:** {correct_answer} {data['unit']}
        
        ### Why multiplication?
        When you have **equal groups**, you multiply:
        - **{data['factor_a']} {data['unit']}** in each group
        - **{data['factor_b']} groups** total
        - **Total = {data['factor_a']} × {data['factor_b']} = {correct_answer}**
        
        ### Think of it this way:
        """)
        
        # Show visual grouping for smaller numbers
        if data['factor_a'] <= 6 and data['factor_b'] <= 6:
            visual_groups = []
            for group in range(data['factor_b']):
                group_items = [data['emoji']] * data['factor_a']
                visual_groups.append(' '.join(group_items))
            
            st.markdown("**Visual representation:**")
            for i, group in enumerate(visual_groups):
                st.markdown(f"Group {i+1}: {group} = {data['factor_a']} {data['unit']}")
            
            st.markdown(f"**Total: {data['factor_b']} groups × {data['factor_a']} each = {correct_answer} {data['unit']}**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer