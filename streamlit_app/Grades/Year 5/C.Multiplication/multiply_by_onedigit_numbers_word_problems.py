import streamlit as st
import random

def run():
    """
    Main function to run the Multiply by One-Digit Numbers: Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_by_onedigit_numbers_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "word_mult_difficulty" not in st.session_state:
        st.session_state.word_mult_difficulty = 2  # Start with 2-digit numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply by One-Digit Numbers: Word Problems")
    st.markdown("*Solve real-world multiplication problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_mult_difficulty
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
        ### How to Solve Multiplication Word Problems:
        
        **1. Read Carefully** 📖
        - Read the problem **twice**
        - **Identify** what you need to find
        - Look for **key words** that suggest multiplication
        
        **2. Find the Numbers** 🔢
        - **What is being repeated?** (groups, sets, arrays)
        - **How many in each group?** 
        - **How many groups are there?**
        
        **3. Set Up the Problem** ✖️
        - Write the multiplication: **groups × items per group**
        - Double-check your setup
        
        **4. Solve and Check** ✅
        - Calculate the answer
        - **Check:** Does your answer make sense?
        - Include the **correct units** in your thinking
        
        ### Key Words for Multiplication:
        - **"Each"** → groups of equal size
        - **"Per"** → rate (per day, per box, per row)  
        - **"In all"** → total amount
        - **"Total"** → final answer
        - **"Array"** → rows and columns
        
        ### Example Strategy:
        **Problem:** "Each box has 24 pencils. The teacher bought 6 boxes. How many pencils in total?"
        
        **Step 1:** What repeats? → pencils in boxes  
        **Step 2:** How many per group? → 24 pencils  
        **Step 3:** How many groups? → 6 boxes  
        **Step 4:** Calculate → 24 × 6 = 144 pencils  
        
        ### Types of Problems:
        - 🏗️ **Building & Construction** (fence posts, bricks)
        - 🍪 **Food & Shopping** (cookies, packages)  
        - 🚌 **Transportation** (buses, passengers)
        - 📚 **School & Supplies** (books, students)
        - 💰 **Money & Work** (earnings, savings)
        - 🌱 **Nature & Animals** (flowers, pets)
        
        ### Difficulty Levels:
        - **🟡 2-digit × 1-digit:** Easier numbers, clear contexts
        - **🟠 3-digit × 1-digit:** Larger numbers, varied scenarios  
        - **🔴 4-digit × 1-digit:** Complex problems, real-world data
        """)

def generate_new_question():
    """Generate a new word problem for one-digit multiplication"""
    digits = st.session_state.word_mult_difficulty
    
    # Generate numbers based on difficulty
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    # Generate the larger number (avoid too many zeros)
    large_number = random.randint(min_val, max_val)
    while str(large_number).count('0') > 1:
        large_number = random.randint(min_val, max_val)
    
    # Generate single digit multiplier
    single_digit = random.randint(2, 9)
    
    # Calculate answer
    correct_answer = large_number * single_digit
    
    # Create varied word problem scenarios
    scenarios = [
        # Building & Construction
        {
            "context": "🏗️ Building Project",
            "story": f"Roger's town built a new fence. Each section of the fence has {large_number} fence posts. The fence has {single_digit} sections. How many fence posts does the fence have in all?",
            "unit": "fence posts",
            "visual_context": "fence sections with posts"
        },
        {
            "context": "🧱 Construction Site", 
            "story": f"A construction worker is laying bricks. Each row has {large_number} bricks. She needs to build {single_digit} rows. How many bricks does she need in total?",
            "unit": "bricks",
            "visual_context": "rows of bricks"
        },
        {
            "context": "🏠 Home Building",
            "story": f"A carpenter is installing floor tiles. Each room needs {large_number} tiles. He is working on {single_digit} rooms. How many tiles will he use altogether?",
            "unit": "tiles", 
            "visual_context": "rooms with tiles"
        },
        
        # Food & Shopping
        {
            "context": "🍪 Bakery Business",
            "story": f"A bakery makes cookies in batches. Each batch contains {large_number} cookies. Today they made {single_digit} batches. How many cookies did they make in total?",
            "unit": "cookies",
            "visual_context": "batches of cookies"
        },
        {
            "context": "📦 Grocery Store",
            "story": f"The grocery store received a shipment of cereal boxes. Each case contains {large_number} boxes. They received {single_digit} cases. How many cereal boxes did they receive altogether?",
            "unit": "cereal boxes",
            "visual_context": "cases of cereal"
        },
        {
            "context": "🍎 Fruit Market",
            "story": f"An apple orchard harvests apples in baskets. Each basket holds {large_number} apples. The workers filled {single_digit} baskets today. How many apples were harvested?",
            "unit": "apples",
            "visual_context": "baskets of apples"
        },
        
        # Transportation
        {
            "context": "🚌 School Transportation",
            "story": f"The school district runs buses for field trips. Each bus can carry {large_number} students. For today's trip, they are using {single_digit} buses. How many students can go on the trip?",
            "unit": "students", 
            "visual_context": "buses with students"
        },
        {
            "context": "✈️ Airport Operations",
            "story": f"An airplane has {large_number} seats. The airline is operating {single_digit} flights with this type of plane today. What is the total seating capacity for all flights?",
            "unit": "seats",
            "visual_context": "flights with passengers"
        },
        {
            "context": "🚗 Parking Garage",
            "story": f"A parking garage has multiple levels. Each level can park {large_number} cars. The garage has {single_digit} levels. How many cars can the garage hold in total?",
            "unit": "cars",
            "visual_context": "parking levels"
        },
        
        # School & Supplies  
        {
            "context": "📚 School Library",
            "story": f"The school library is organizing books. Each shelf holds {large_number} books. The librarian is filling {single_digit} shelves. How many books will be on these shelves?",
            "unit": "books",
            "visual_context": "library shelves"
        },
        {
            "context": "✏️ Classroom Supplies",
            "story": f"A teacher ordered pencils for her class. Each pack contains {large_number} pencils. She bought {single_digit} packs. How many pencils did she buy altogether?",
            "unit": "pencils",
            "visual_context": "packs of pencils"
        },
        {
            "context": "🎨 Art Class",
            "story": f"The art teacher is preparing supplies. Each table gets {large_number} crayons. There are {single_digit} tables in the classroom. How many crayons are needed in total?",
            "unit": "crayons",
            "visual_context": "tables with art supplies"
        },
        
        # Money & Work
        {
            "context": "💰 Part-time Job",
            "story": f"Maria earns £{large_number} each day at her part-time job. She worked {single_digit} days this week. How much money did she earn this week?",
            "unit": "pounds",
            "visual_context": "daily earnings"
        },
        {
            "context": "🏪 Shop Sales",
            "story": f"A shop sells {large_number} items every day. The shop is open {single_digit} days this week. How many items will they sell this week?",
            "unit": "items",
            "visual_context": "daily sales"
        },
        {
            "context": "💵 Savings Plan",
            "story": f"Jake saves £{large_number} every month. He has been saving for {single_digit} months. How much money has he saved in total?",
            "unit": "pounds",
            "visual_context": "monthly savings"
        },
        
        # Nature & Animals
        {
            "context": "🌻 Garden Project",
            "story": f"A gardener plants flowers in rows. Each row has {large_number} flowers. She planted {single_digit} rows. How many flowers did she plant altogether?",
            "unit": "flowers",
            "visual_context": "rows of flowers"
        },
        {
            "context": "🐕 Animal Shelter",
            "story": f"An animal shelter feeds dogs every day. Each dog eats {large_number} grams of food daily. The shelter has {single_digit} dogs. How many grams of food do they need each day?",
            "unit": "grams of food",
            "visual_context": "dogs being fed"
        },
        {
            "context": "🌳 Tree Planting",
            "story": f"A conservation group plants trees in parks. Each park gets {large_number} trees. They are working on {single_digit} parks this year. How many trees will they plant in total?",
            "unit": "trees",
            "visual_context": "parks with trees"
        },
        
        # Entertainment & Sports
        {
            "context": "🎪 Theatre Show",
            "story": f"A theatre has {large_number} seats. They are putting on {single_digit} shows this weekend. What is the total seating capacity for all shows?",
            "unit": "seats",
            "visual_context": "theatre performances"
        },
        {
            "context": "⚽ Sports League",
            "story": f"In a football league, each team has {large_number} players. There are {single_digit} teams in the league. How many players are there in total?",
            "unit": "players",
            "visual_context": "sports teams"
        },
        {
            "context": "🎮 Gaming Tournament",
            "story": f"A gaming tournament awards {large_number} points for each win. Sarah won {single_digit} games. How many points did she earn in total?",
            "unit": "points",
            "visual_context": "gaming wins"
        }
    ]
    
    # Select a random scenario
    scenario = random.choice(scenarios)
    
    # Store question data
    st.session_state.question_data = {
        "large_number": large_number,
        "single_digit": single_digit,
        "correct_answer": correct_answer,
        "scenario": scenario,
        "story": scenario["story"],
        "unit": scenario["unit"],
        "context": scenario["context"]
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = scenario["story"]

def display_question():
    """Display the current word problem"""
    data = st.session_state.question_data
    
    # Display the word problem
    st.markdown("### 📝 Word Problem:")
    
    # Show context with icon
    st.markdown(f"**{data['context']}**")
    
    # Display the story in a highlighted box
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
        {data['story']}
    </div>
    """, unsafe_allow_html=True)
    
    # Create form for the answer
    with st.form("word_problem_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Input field matching the image style
            answer_cols = st.columns([3, 2])
            
            with answer_cols[0]:
                user_answer = st.number_input(
                    "Answer:",
                    min_value=0,
                    step=1,
                    key="word_answer",
                    label_visibility="collapsed",
                    help=f"Enter the total number of {data['unit']}",
                    placeholder="Enter your answer"
                )
            
            with answer_cols[1]:
                st.markdown(f"<div style='margin-top: 12px; font-size: 16px; color: #666;'>{data['unit']}</div>", unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
        
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! {correct_answer:,} {data['unit']} is correct!**")
        
        # Increase difficulty (max 4 digits)
        old_difficulty = st.session_state.word_mult_difficulty
        st.session_state.word_mult_difficulty = min(
            st.session_state.word_mult_difficulty + 1, 4
        )
        
        if st.session_state.word_mult_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 4-digit word problems!**")
        elif old_difficulty < st.session_state.word_mult_difficulty:
            st.info(f"⬆️ **Great problem solving! Moving up to {st.session_state.word_mult_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,} {data['unit']}**.")
        
        # Decrease difficulty (min 2 digits)
        old_difficulty = st.session_state.word_mult_difficulty
        st.session_state.word_mult_difficulty = max(
            st.session_state.word_mult_difficulty - 1, 2
        )
        
        if old_difficulty > st.session_state.word_mult_difficulty:
            st.warning(f"⬇️ **Let's practice with {st.session_state.word_mult_difficulty}-digit problems first**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the word problem"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Problem Analysis:
        **Context:** {data['context']}
        
        ### Step-by-step solution:
        
        **Step 1: Identify what we know** 📋
        - Each group has: **{data['large_number']:,} {data['unit']}**
        - Number of groups: **{data['single_digit']}**
        - We need to find: **Total {data['unit']}**
        
        **Step 2: Set up the multiplication** ✖️
        - This is a multiplication problem because we have **equal groups**
        - Calculation: **{data['large_number']:,} × {data['single_digit']}**
        
        **Step 3: Calculate the answer** 🧮
        - {data['large_number']:,} × {data['single_digit']} = **{data['correct_answer']:,}**
        
        **Step 4: Check our answer** ✅
        - Does {data['correct_answer']:,} {data['unit']} make sense? 
        - We can estimate: {round_for_estimation(data['large_number']):,} × {data['single_digit']} ≈ {round_for_estimation(data['large_number']) * data['single_digit']:,}
        - Our answer of {data['correct_answer']:,} is close to this estimate! ✓
        
        **Final Answer: {data['correct_answer']:,} {data['unit']}**
        """)

def round_for_estimation(n):
    """Round number for estimation purposes"""
    if n < 100:
        return round(n, -1)  # Round to nearest 10
    elif n < 1000:
        return round(n, -2)  # Round to nearest 100
    else:
        return round(n, -3)  # Round to nearest 1000

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""