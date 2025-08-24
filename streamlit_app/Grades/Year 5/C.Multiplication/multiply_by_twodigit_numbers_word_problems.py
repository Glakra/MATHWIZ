import streamlit as st
import random

def run():
    """
    Main function to run the Multiply by two-digit numbers: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C.Multiplication/multiply_by_two_digit_numbers_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "mult_word_difficulty" not in st.session_state:
        st.session_state.mult_word_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply by Two-Digit Numbers: Word Problems")
    st.markdown("*Solve real-world multiplication problems with two-digit numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mult_word_difficulty
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
        ### How to Solve:
        - **Read the problem carefully** and identify what you need to find
        - **Look for the two numbers** you need to multiply
        - **Set up the multiplication** (larger number × smaller number)
        - **Show your work** step by step
        - **Check your answer** makes sense in context
        
        ### Multiplication Strategies:
        - **Standard Algorithm:** Stack the numbers and multiply
        - **Area Model:** Break numbers into parts
        - **Distributive Property:** (20 + 3) × 45 = (20 × 45) + (3 × 45)
        
        ### Example Problem:
        *"A school has 24 classrooms. Each classroom has 35 desks. How many desks are there in total?"*
        
        **Step 1:** Identify the numbers: 24 classrooms, 35 desks each
        **Step 2:** Set up: 24 × 35
        **Step 3:** Calculate: 24 × 35 = 840
        **Step 4:** Answer: 840 desks
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Smaller two-digit numbers (11-25)
        - **🟠 Level 3:** Medium numbers (26-50) 
        - **🔴 Level 4-5:** Larger numbers (51-99)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Stay at current level and try again
        - 🎯 **Goal:** Master Level 5 problems!
        """)

def generate_word_problems():
    """Generate different word problem scenarios based on difficulty"""
    
    level = st.session_state.mult_word_difficulty
    
    # Define number ranges based on difficulty
    if level == 1:
        range1, range2 = (11, 19), (11, 19)
    elif level == 2:
        range1, range2 = (12, 25), (12, 25)
    elif level == 3:
        range1, range2 = (26, 40), (15, 35)
    elif level == 4:
        range1, range2 = (41, 60), (20, 45)
    else:  # level 5
        range1, range2 = (61, 99), (25, 99)
    
    # Generate two random numbers
    num1 = random.randint(*range1)
    num2 = random.randint(*range2)
    
    # Problem scenarios with various contexts
    scenarios = [
        # School/Education contexts
        {
            "context": "school_supplies",
            "template": "A school orders {num1} boxes of pencils. Each box contains {num2} pencils. How many pencils did the school order in total?",
            "unit": "pencils"
        },
        {
            "context": "classroom",
            "template": "There are {num1} classrooms in a school. Each classroom has {num2} desks. How many desks are there in the school?",
            "unit": "desks"
        },
        {
            "context": "books",
            "template": "A library has {num1} shelves. Each shelf holds {num2} books. How many books can the library hold in total?",
            "unit": "books"
        },
        {
            "context": "students",
            "template": "A school has {num1} classes. Each class has {num2} students. How many students are there in the school?",
            "unit": "students"
        },
        
        # Shopping/Business contexts
        {
            "context": "bakery",
            "template": "A bakery makes {num1} trays of cookies. Each tray has {num2} cookies. How many cookies did the bakery make?",
            "unit": "cookies"
        },
        {
            "context": "store",
            "template": "A store has {num1} cases of water bottles. Each case contains {num2} bottles. How many water bottles does the store have?",
            "unit": "bottles"
        },
        {
            "context": "restaurant",
            "template": "A restaurant has {num1} tables. Each table can seat {num2} people. What is the maximum number of people the restaurant can serve?",
            "unit": "people"
        },
        {
            "context": "grocery",
            "template": "A grocery store receives {num1} crates of apples. Each crate contains {num2} apples. How many apples did the store receive?",
            "unit": "apples"
        },
        
        # Sports/Recreation contexts
        {
            "context": "stadium",
            "template": "A stadium has {num1} sections. Each section has {num2} seats. How many seats are there in the stadium?",
            "unit": "seats"
        },
        {
            "context": "team",
            "template": "There are {num1} soccer teams in a league. Each team has {num2} players. How many players are there in total?",
            "unit": "players"
        },
        {
            "context": "games",
            "template": "A tournament has {num1} games. Each game lasts {num2} minutes. How many minutes of games are there in total?",
            "unit": "minutes"
        },
        
        # Time/Calendar contexts
        {
            "context": "days",
            "template": "Sarah exercises for {num2} minutes each day for {num1} days. How many minutes did she exercise in total?",
            "unit": "minutes"
        },
        {
            "context": "weeks",
            "template": "A factory operates for {num1} weeks. Each week they produce {num2} items. How many items do they produce in total?",
            "unit": "items"
        },
        
        # Transportation contexts
        {
            "context": "buses",
            "template": "A school district has {num1} buses. Each bus can carry {num2} students. How many students can all the buses carry together?",
            "unit": "students"
        },
        {
            "context": "parking",
            "template": "A parking garage has {num1} levels. Each level has {num2} parking spaces. How many parking spaces are there in total?",
            "unit": "parking spaces"
        },
        
        # Garden/Nature contexts
        {
            "context": "garden",
            "template": "A garden has {num1} rows of plants. Each row has {num2} plants. How many plants are there in the garden?",
            "unit": "plants"
        },
        {
            "context": "farm",
            "template": "A farmer plants {num1} rows of corn. Each row has {num2} corn plants. How many corn plants did the farmer plant?",
            "unit": "corn plants"
        },
        
        # Technology contexts
        {
            "context": "computer",
            "template": "A computer lab has {num1} computers. Each computer has {num2} keys on its keyboard. How many keys are there in total?",
            "unit": "keys"
        },
        {
            "context": "photos",
            "template": "Emma takes {num2} photos each day for {num1} days. How many photos did she take in total?",
            "unit": "photos"
        },
        
        # Manufacturing contexts
        {
            "context": "factory",
            "template": "A factory has {num1} machines. Each machine produces {num2} items per hour. How many items do all machines produce in one hour?",
            "unit": "items"
        },
        {
            "context": "boxes",
            "template": "A warehouse has {num1} boxes. Each box contains {num2} items. How many items are stored in the warehouse?",
            "unit": "items"
        },
        
        # Entertainment contexts
        {
            "context": "theater",
            "template": "A movie theater has {num1} rows. Each row has {num2} seats. How many seats are there in the theater?",
            "unit": "seats"
        },
        {
            "context": "concert",
            "template": "A concert venue sells tickets for {num1} shows. Each show sells {num2} tickets. How many tickets were sold in total?",
            "unit": "tickets"
        },
        
        # Collection contexts
        {
            "context": "stamps",
            "template": "Alex collects stamps in {num1} albums. Each album holds {num2} stamps. How many stamps does Alex have?",
            "unit": "stamps"
        },
        {
            "context": "coins",
            "template": "A coin collector has {num1} pages in a book. Each page holds {num2} coins. How many coins can the book hold?",
            "unit": "coins"
        }
    ]
    
    # Choose random scenario
    scenario = random.choice(scenarios)
    
    # Create the problem text
    problem_text = scenario["template"].format(num1=num1, num2=num2)
    answer = num1 * num2
    
    return {
        "problem": problem_text,
        "num1": num1,
        "num2": num2,
        "answer": answer,
        "unit": scenario["unit"],
        "context": scenario["context"]
    }

def generate_new_question():
    """Generate a new word problem question"""
    question_data = generate_word_problems()
    
    # Generate smart distractors (wrong answers)
    correct = question_data["answer"]
    num1, num2 = question_data["num1"], question_data["num2"]
    
    options = [correct]
    
    # Common mistake patterns
    possible_mistakes = [
        num1 + num2,  # Addition instead of multiplication
        correct + num1,  # Off by one factor
        correct - num2,  # Off by other factor
        correct + 10,  # Simple arithmetic error
        correct - 10,  # Simple arithmetic error
        num1 * (num2 + 1),  # Off by one
        num1 * (num2 - 1),  # Off by one
        (num1 + 1) * num2,  # Off by one
        (num1 - 1) * num2,  # Off by one
        correct // 10 * 10 + (correct % 10),  # Place value error
        int(str(num1) + str(num2)),  # Concatenation instead of multiplication
    ]
    
    # Add unique mistakes to options
    for mistake in possible_mistakes:
        if mistake > 0 and mistake != correct and mistake not in options and len(options) < 4:
            options.append(mistake)
    
    # Fill remaining options with random nearby values
    while len(options) < 4:
        wrong = correct + random.randint(-100, 100)
        if wrong > 0 and wrong != correct and wrong not in options:
            options.append(wrong)
    
    # Shuffle options
    random.shuffle(options)
    
    st.session_state.question_data = {
        "problem": question_data["problem"],
        "options": options,
        "num1": num1,
        "num2": num2,
        "unit": question_data["unit"],
        "context": question_data["context"]
    }
    st.session_state.correct_answer = correct
    st.session_state.current_question = "Solve this word problem:"

def generate_new_question():
    """Generate a new word problem question"""
    question_data = generate_word_problems()
    
    # Generate smart distractors (wrong answers)
    correct = question_data["answer"]
    num1, num2 = question_data["num1"], question_data["num2"]
    
    options = [correct]
    
    # Common mistake patterns
    possible_mistakes = [
        num1 + num2,  # Addition instead of multiplication
        correct + num1,  # Off by one factor
        correct - num2,  # Off by other factor
        correct + 10,  # Simple arithmetic error
        correct - 10,  # Simple arithmetic error
        num1 * (num2 + 1),  # Off by one
        num1 * (num2 - 1),  # Off by one
        (num1 + 1) * num2,  # Off by one
        (num1 - 1) * num2,  # Off by one
        int(str(num1) + str(num2)) if len(str(num1) + str(num2)) <= 4 else correct + 50,  # Concatenation
    ]
    
    # Add unique mistakes to options
    for mistake in possible_mistakes:
        if mistake > 0 and mistake != correct and mistake not in options and len(options) < 4:
            options.append(mistake)
    
    # Fill remaining options with random nearby values
    while len(options) < 4:
        wrong = correct + random.randint(-50, 50)
        if wrong > 0 and wrong != correct and wrong not in options:
            options.append(wrong)
    
    # Shuffle options
    random.shuffle(options)
    
    st.session_state.question_data = {
        "problem": question_data["problem"],
        "options": options,
        "num1": num1,
        "num2": num2,
        "unit": question_data["unit"],
        "context": question_data["context"]
    }
    st.session_state.correct_answer = correct
    st.session_state.current_question = "Solve this word problem:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Word Problem:")
    
    # Display the problem in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        font-weight: 500;
        color: #2c3e50;
    ">
        {data['problem']}
    </div>
    """, unsafe_allow_html=True)
    
    # Show the multiplication setup
    st.markdown("**This problem asks you to multiply:**")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown(f"**{data['num1']}**")
    with col2:
        st.markdown("**×**")
    with col3:
        st.markdown(f"**{data['num2']}**")
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Choose the correct answer:**")
        
        # Create radio button options
        user_answer = st.radio(
            "Select your answer:",
            options=[f"{opt:,} {data['unit']}" for opt in data['options']],
            key="answer_choice",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Extract number from answer
            selected_number = int(user_answer.split()[0].replace(",", ""))
            st.session_state.user_answer = selected_number
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
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the work
        st.markdown(f"**Solution:** {data['num1']} × {data['num2']} = {correct_answer:,}")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.mult_word_difficulty
        st.session_state.mult_word_difficulty = min(
            st.session_state.mult_word_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.mult_word_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 multiplication word problems!**")
        elif old_level < st.session_state.mult_word_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.mult_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer:,} {data['unit']}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    num1, num2 = data['num1'], data['num2']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['problem']}
        
        **Step 1: Identify the numbers**
        - First number: {num1}
        - Second number: {num2}
        - Operation: Multiplication (×)
        
        **Step 2: Set up the multiplication**
        {num1} × {num2}
        
        **Step 3: Calculate using standard algorithm**
        """)
        
        # Show the standard multiplication algorithm
        st.markdown(f"""
        ```
              {num2:>4}
        ×     {num1:>4}
        ─────────
        """)
        
        # Break down the calculation
        ones_digit = num1 % 10
        tens_digit = num1 // 10
        
        if tens_digit > 0:
            step1 = ones_digit * num2
            step2 = tens_digit * num2 * 10
            
            st.markdown(f"""
        **Step 4: Break it down**
        - {num2} × {ones_digit} = {step1}
        - {num2} × {tens_digit}0 = {step2}
        - Total: {step1} + {step2} = {correct_answer}
        """)
        else:
            st.markdown(f"""
        **Step 4: Simple multiplication**
        - {num2} × {num1} = {correct_answer}
        """)
        
        st.markdown(f"""
        **Final Answer:** {correct_answer:,} {data['unit']}
        
        ### Why this makes sense:
        """)
        
        # Context-specific explanation
        if "each" in data['problem'].lower():
            st.markdown(f"We have {num1} groups, with {num2} items in each group, so {num1} × {num2} = {correct_answer} total items.")
        elif "per" in data['problem'].lower():
            st.markdown(f"At a rate of {num2} per unit for {num1} units, we get {num1} × {num2} = {correct_answer} total.")
        else:
            st.markdown(f"When we multiply {num1} by {num2}, we get {correct_answer} as our answer.")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer