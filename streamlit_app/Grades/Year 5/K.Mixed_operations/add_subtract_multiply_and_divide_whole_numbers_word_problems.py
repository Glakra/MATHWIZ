import streamlit as st
import random

def run():
    """
    Main function to run the word problems activity for mixed operations.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/add_subtract_multiply_and_divide_whole_numbers_word_problems.py
    """
    # Initialize session state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("📖 Word Problems: Add, Subtract, Multiply & Divide")
    st.markdown("*Solve real-world problems using the four operations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Expert", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_word_problem()
    
    # Display current problem
    display_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Word Problems:
        
        **1. Read Carefully** 📖
        - Read the problem twice
        - Identify what you need to find
        - Look for key words
        
        **2. Identify the Operation** 🔍
        
        **Addition Keywords:**
        - total, sum, altogether, combined
        - more than, increased by
        - in all, both
        
        **Subtraction Keywords:**
        - difference, less than, fewer
        - left, remaining, still need
        - how many more/less
        
        **Multiplication Keywords:**
        - each, every, per
        - times, groups of
        - rows of, sets of
        
        **Division Keywords:**
        - share equally, split
        - each gets, per person
        - how many groups
        
        **3. Write the Equation** ✏️
        - Use the numbers from the problem
        - Choose the correct operation
        - Check if your answer makes sense
        
        **4. Solve & Check** ✓
        - Do the calculation carefully
        - Read the problem again
        - Does your answer make sense?
        
        ### Example:
        *"Sarah has 24 cookies. She wants to share them equally among 6 friends. How many cookies will each friend get?"*
        
        - **Key words:** "share equally" → Division
        - **Equation:** 24 ÷ 6 = ?
        - **Answer:** 4 cookies each
        - **Check:** 6 × 4 = 24 ✓
        """)

def generate_word_problem_scenarios():
    """Generate diverse word problem scenarios"""
    return {
        "addition": [
            # Nature/Environment
            {
                "template": "Rangers at {location} stocked the lake with {num1} fish yesterday. Today they added {num2} more fish. How many fish are in the lake now?",
                "locations": ["Scott Lake", "Pine River", "Crystal Lake", "Blue Mountain Lake", "Silver Creek"],
                "unit": "fish"
            },
            {
                "template": "Archaeologists uncovered an ancient city. They found {num1} pieces of clay and {num2} pieces of stone. In all, how many pieces did the archaeologists find?",
                "unit": "pieces"
            },
            {
                "template": "A wildlife sanctuary has {num1} birds. They rescued {num2} more birds this week. How many birds are in the sanctuary now?",
                "unit": "birds"
            },
            
            # School/Education
            {
                "template": "{name}'s school collected {num1} books for charity last month and {num2} books this month. What is the total number of books collected?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "books"
            },
            {
                "template": "The library had {num1} visitors on Monday and {num2} visitors on Tuesday. How many visitors came in total?",
                "unit": "visitors"
            },
            
            # Sports/Recreation
            {
                "template": "A stadium has {num1} seats in the lower section and {num2} seats in the upper section. What is the total seating capacity?",
                "unit": "seats"
            },
            {
                "template": "During a basketball game, Team A scored {num1} points and Team B scored {num2} points. What was the total score?",
                "unit": "points"
            },
            
            # Business/Shopping
            {
                "template": "A toy store sold {num1} toys in the morning and {num2} toys in the afternoon. How many toys were sold in total?",
                "unit": "toys"
            },
            {
                "template": "A bakery made {num1} loaves of bread on Saturday and {num2} loaves on Sunday. How many loaves did they make over the weekend?",
                "unit": "loaves"
            },
            
            # Travel/Transportation
            {
                "template": "An airport had {num1} arrivals in the morning and {num2} arrivals in the evening. How many planes arrived that day?",
                "unit": "planes"
            }
        ],
        
        "subtraction": [
            # Nature/Environment
            {
                "template": "Rangers at {location} stocked the lake with {num1} fish. {num2} of the fish were trout and the rest were catfish. How many catfish were there?",
                "locations": ["Scott Lake", "Pine River", "Crystal Lake", "Blue Mountain Lake", "Silver Creek"],
                "unit": "catfish"
            },
            {
                "template": "A forest had {num1} trees. A storm knocked down {num2} trees. How many trees are still standing?",
                "unit": "trees"
            },
            
            # School/Education
            {
                "template": "{name}'s school has {num1} students. If {num2} students are in primary grades, how many are in upper grades?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "students"
            },
            {
                "template": "A library has {num1} books. {num2} books were checked out. How many books remain in the library?",
                "unit": "books"
            },
            
            # Sports/Recreation
            {
                "template": "A marathon had {num1} registered runners. Only {num2} runners finished the race. How many didn't finish?",
                "unit": "runners"
            },
            {
                "template": "A swimming pool can hold {num1} gallons of water. It currently has {num2} gallons. How many more gallons are needed to fill it?",
                "unit": "gallons"
            },
            
            # Business/Shopping
            {
                "template": "A store had {num1} items in stock. They sold {num2} items. How many items are left?",
                "unit": "items"
            },
            {
                "template": "A parking lot has {num1} spaces. {num2} cars are parked. How many empty spaces are there?",
                "unit": "spaces"
            },
            
            # Money/Finance
            {
                "template": "{name} saved ${num1}. After buying a bicycle for ${num2}, how much money does {name} have left?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "dollars"
            }
        ],
        
        "multiplication": [
            # Packaging/Groups
            {
                "template": "A factory packs {num2} bottles in each box. How many bottles are in {num1} boxes?",
                "unit": "bottles"
            },
            {
                "template": "Each classroom has {num2} desks. How many desks are in {num1} classrooms?",
                "unit": "desks"
            },
            
            # Arrays/Arrangements
            {
                "template": "A parking lot has {num1} rows with {num2} spaces in each row. How many parking spaces are there in total?",
                "unit": "spaces"
            },
            {
                "template": "An auditorium has {num1} rows of seats with {num2} seats in each row. What is the total number of seats?",
                "unit": "seats"
            },
            
            # Time/Rates
            {
                "template": "A machine produces {num2} items per hour. How many items will it produce in {num1} hours?",
                "unit": "items"
            },
            {
                "template": "{name} reads {num2} pages per day. How many pages will {name} read in {num1} days?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "pages"
            },
            
            # Money/Cost
            {
                "template": "Movie tickets cost ${num2} each. How much will {num1} tickets cost?",
                "unit": "dollars"
            },
            {
                "template": "Each pizza costs ${num2}. How much do {num1} pizzas cost?",
                "unit": "dollars"
            },
            
            # Nature/Science
            {
                "template": "Each tree produces {num2} apples. How many apples will {num1} trees produce?",
                "unit": "apples"
            },
            {
                "template": "A spider has {num2} legs. How many legs do {num1} spiders have altogether?",
                "unit": "legs"
            }
        ],
        
        "division": [
            # Sharing/Distribution
            {
                "template": "{name} has {num1} cookies to share equally among {num2} friends. How many cookies will each friend get?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "cookies",
                "unit_per": "cookies per friend"
            },
            {
                "template": "A teacher has {num1} pencils to distribute equally to {num2} students. How many pencils will each student receive?",
                "unit": "pencils",
                "unit_per": "pencils per student"
            },
            
            # Grouping
            {
                "template": "A bakery has {num1} muffins. They pack them in boxes of {num2}. How many boxes can they fill?",
                "unit": "muffins",
                "unit_per": "boxes"
            },
            {
                "template": "There are {num1} students going on a field trip. Each bus holds {num2} students. How many buses are needed?",
                "unit": "students",
                "unit_per": "buses"
            },
            
            # Rate/Time
            {
                "template": "A factory produced {num1} toys in {num2} days. How many toys did they produce per day?",
                "unit": "toys",
                "unit_per": "toys per day"
            },
            {
                "template": "{name} traveled {num1} miles in {num2} hours. What was the average speed in miles per hour?",
                "names": ["Emma", "James", "Sophia", "Oliver", "Ava"],
                "unit": "miles",
                "unit_per": "miles per hour"
            },
            
            # Money
            {
                "template": "A prize of ${num1} is to be shared equally among {num2} winners. How much will each winner receive?",
                "unit": "dollars",
                "unit_per": "dollars per winner"
            },
            {
                "template": "{num1} identical items cost ${num2} in total. What is the cost of one item?",
                "unit": "items",
                "unit_per": "dollars per item"
            },
            
            # Measurement
            {
                "template": "A rope {num1} meters long is cut into {num2} equal pieces. How long is each piece?",
                "unit": "meters",
                "unit_per": "meters per piece"
            }
        ]
    }

def generate_new_word_problem():
    """Generate a new word problem based on difficulty"""
    difficulty = st.session_state.word_problem_difficulty
    scenarios = generate_word_problem_scenarios()
    
    # Choose operation based on difficulty
    if difficulty == 1:
        operations = ["addition", "subtraction"]
    else:
        operations = ["addition", "subtraction", "multiplication", "division"]
    
    operation = random.choice(operations)
    scenario = random.choice(scenarios[operation])
    
    # Generate numbers based on operation and difficulty
    if operation == "addition":
        if difficulty == 1:
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
        elif difficulty == 2:
            num1 = random.randint(1000, 4999)
            num2 = random.randint(1000, 4999)
        elif difficulty == 3:
            num1 = random.randint(5000, 9999)
            num2 = random.randint(1000, 9999)
        elif difficulty == 4:
            num1 = random.randint(10000, 49999)
            num2 = random.randint(5000, 49999)
        else:
            num1 = random.randint(50000, 99999)
            num2 = random.randint(10000, 99999)
        answer = num1 + num2
        
    elif operation == "subtraction":
        if difficulty == 1:
            num1 = random.randint(500, 999)
            num2 = random.randint(100, num1-50)
        elif difficulty == 2:
            num1 = random.randint(2000, 9999)
            num2 = random.randint(1000, num1-100)
        elif difficulty == 3:
            num1 = random.randint(5000, 9999)
            num2 = random.randint(1000, num1-500)
        elif difficulty == 4:
            num1 = random.randint(10000, 99999)
            num2 = random.randint(5000, num1-1000)
        else:
            num1 = random.randint(50000, 99999)
            num2 = random.randint(10000, num1-5000)
        answer = num1 - num2
        
    elif operation == "multiplication":
        if difficulty <= 2:
            num1 = random.randint(10, 99)
            num2 = random.randint(2, 9)
        elif difficulty == 3:
            num1 = random.randint(100, 999)
            num2 = random.randint(2, 12)
        elif difficulty == 4:
            num1 = random.randint(100, 999)
            num2 = random.randint(10, 99)
        else:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(10, 99)
        answer = num1 * num2
        
    else:  # division
        if difficulty <= 2:
            divisor = random.randint(2, 12)
            quotient = random.randint(10, 99)
        elif difficulty == 3:
            divisor = random.randint(2, 12)
            quotient = random.randint(100, 999)
        elif difficulty == 4:
            divisor = random.randint(10, 25)
            quotient = random.randint(100, 999)
        else:
            divisor = random.randint(10, 99)
            quotient = random.randint(100, 999)
        
        # For word problems, we'll use exact division (no remainders)
        num1 = divisor * quotient
        num2 = divisor
        answer = quotient
    
    # Build the problem text
    problem_text = scenario["template"]
    
    # Replace placeholders
    if "names" in scenario:
        name = random.choice(scenario["names"])
        problem_text = problem_text.replace("{name}", name)
    
    if "locations" in scenario:
        location = random.choice(scenario["locations"])
        problem_text = problem_text.replace("{location}", location)
    
    problem_text = problem_text.replace("{num1}", f"{num1:,}")
    problem_text = problem_text.replace("{num2}", f"{num2:,}")
    
    # Store problem data
    st.session_state.problem_data = {
        "operation": operation,
        "problem_text": problem_text,
        "num1": num1,
        "num2": num2,
        "unit": scenario.get("unit_per", scenario["unit"])
    }
    st.session_state.correct_answer = answer
    st.session_state.current_problem = problem_text

def display_word_problem():
    """Display the current word problem"""
    # Display the problem in a nice card
    st.markdown("""
    <div style="
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        font-size: 18px;
        line-height: 1.6;
    ">
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{st.session_state.current_problem}**")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show work area
    with st.expander("📝 **Work Space** (optional)", expanded=False):
        st.markdown("""
        Use this space to organize your thoughts:
        
        **What do I know?**
        - 
        - 
        
        **What do I need to find?**
        - 
        
        **What operation should I use?**
        - [ ] Addition (+)
        - [ ] Subtraction (-)
        - [ ] Multiplication (×)
        - [ ] Division (÷)
        
        **My equation:**
        _____ ○ _____ = _____
        """)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_answer = st.number_input(
                "Your answer:",
                min_value=0,
                step=1,
                key="answer_input"
            )
        
        with col2:
            unit = st.session_state.problem_data["unit"]
            st.markdown(f"<div style='padding-top: 30px;'>{unit}</div>", unsafe_allow_html=True)
        
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
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    unit = st.session_state.problem_data["unit"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! {correct_answer:,} {unit} is correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = min(
            st.session_state.word_problem_difficulty + 1, 5
        )
        
        if st.session_state.word_problem_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered complex word problems!**")
        elif old_difficulty < st.session_state.word_problem_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.word_problem_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer:,} {unit}.**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = max(
            st.session_state.word_problem_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.word_problem_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.word_problem_difficulty}. Keep practicing!**")
        
        # Show solution
        show_solution()

def show_solution():
    """Show detailed solution for the problem"""
    data = st.session_state.problem_data
    operation = data["operation"]
    num1 = data["num1"]
    num2 = data["num2"]
    answer = st.session_state.correct_answer
    
    with st.expander("📖 **Solution Explained**", expanded=True):
        st.markdown("### Step-by-step solution:")
        
        # Identify what we know
        st.markdown("**1. What we know:**")
        if operation == "addition":
            st.markdown(f"- First amount: {num1:,}")
            st.markdown(f"- Second amount: {num2:,}")
            st.markdown("- We need the total")
            
        elif operation == "subtraction":
            st.markdown(f"- Total amount: {num1:,}")
            st.markdown(f"- Amount to subtract: {num2:,}")
            st.markdown("- We need the remaining amount")
            
        elif operation == "multiplication":
            st.markdown(f"- Number of groups: {num1:,}")
            st.markdown(f"- Amount in each group: {num2:,}")
            st.markdown("- We need the total")
            
        else:  # division
            st.markdown(f"- Total amount: {num1:,}")
            st.markdown(f"- Number to divide by: {num2:,}")
            st.markdown("- We need the amount per group")
        
        # Show the operation
        st.markdown("\n**2. The operation:**")
        if operation == "addition":
            st.markdown(f"Addition: {num1:,} + {num2:,}")
        elif operation == "subtraction":
            st.markdown(f"Subtraction: {num1:,} - {num2:,}")
        elif operation == "multiplication":
            st.markdown(f"Multiplication: {num1:,} × {num2:,}")
        else:
            st.markdown(f"Division: {num1:,} ÷ {num2:,}")
        
        # Show the calculation
        st.markdown("\n**3. The calculation:**")
        st.markdown(f"```")
        if operation in ["addition", "subtraction"]:
            st.markdown(f"{num1:>10,}")
            st.markdown(f"{'+' if operation == 'addition' else '-'} {num2:>8,}")
            st.markdown(f"{'─' * 10}")
            st.markdown(f"{answer:>10,}")
        elif operation == "multiplication":
            st.markdown(f"{num1:>10,}")
            st.markdown(f"×{num2:>9,}")
            st.markdown(f"{'─' * 10}")
            st.markdown(f"{answer:>10,}")
        else:  # division
            st.markdown(f"{num1:,} ÷ {num2:,} = {answer:,}")
        st.markdown(f"```")
        
        # Answer statement
        st.markdown(f"\n**4. Answer:** {answer:,} {data['unit']}")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer