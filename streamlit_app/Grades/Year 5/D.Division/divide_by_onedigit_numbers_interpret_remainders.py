import streamlit as st
import random

def run():
    """
    Main function to run the Interpret Remainders practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_by_one_digit_numbers_interpret_remainders.py
    """
    # Initialize session state for difficulty and game state
    if "remainder_difficulty" not in st.session_state:
        st.session_state.remainder_difficulty = 1  # Start with simple problems
    
    if "current_remainder_problem" not in st.session_state:
        st.session_state.current_remainder_problem = None
        st.session_state.correct_remainder_answer = None
        st.session_state.show_remainder_feedback = False
        st.session_state.remainder_answer_submitted = False
        st.session_state.remainder_problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("🔍 Interpret Remainders")
    st.markdown("*Understand what remainders mean in real-world problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.remainder_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple remainder problems (2-digit numbers)",
            2: "Intermediate remainder problems (3-digit numbers)", 
            3: "Complex remainder problems (4+ digit numbers)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
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
    if st.session_state.current_remainder_problem is None:
        generate_new_remainder_problem()
    
    # Display current question
    display_remainder_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Remainders**", expanded=False):
        st.markdown("""
        ### What is a Remainder?
        A **remainder** is what's **left over** after division when the numbers don't divide evenly.
        
        **Example:** 17 ÷ 5 = 3 R 2
        - **3** is how many complete groups of 5 we can make
        - **2** is the remainder (what's left over)
        
        ### How to Find Remainders:
        1. **Divide** to find how many complete groups
        2. **Multiply** the quotient by the divisor  
        3. **Subtract** from the original number
        4. **The difference is the remainder**
        
        **Example:** 23 ÷ 4 = ?
        - 23 ÷ 4 = 5 R 3
        - Check: 5 × 4 = 20, and 23 - 20 = 3 ✓
        
        ### Real-World Remainder Meanings:
        
        **🎢 Tickets & Rides:**
        - "How many tickets left?" → The remainder
        - "287 tickets, 2 per ride" → 287 ÷ 2 = 143 R **1 ticket left**
        
        **🍕 Food & Sharing:**
        - "How many pieces left over?" → The remainder  
        - "23 pieces, 4 per person" → 23 ÷ 4 = 5 R **3 pieces left**
        
        **📦 Packing & Items:**
        - "How many items don't fit?" → The remainder
        - "47 toys, 6 per box" → 47 ÷ 6 = 7 R **5 toys don't fit**
        
        **🎈 Party Planning:**
        - "How many balloons left?" → The remainder
        - "85 balloons, 8 per table" → 85 ÷ 8 = 10 R **5 balloons left**
        
        **⏰ Time & Scheduling:**
        - "How many minutes extra?" → The remainder
        - "67 minutes, 15 per session" → 67 ÷ 15 = 4 R **7 minutes extra**
        
        ### Key Question Types:
        - **"How many ... left?"** → Find the remainder
        - **"How many ... left over?"** → Find the remainder  
        - **"How many extra ...?"** → Find the remainder
        - **"How many ... remaining?"** → Find the remainder
        - **"How many ... will not fit?"** → Find the remainder
        
        ### Remember:
        - The remainder is **always smaller** than the divisor
        - If remainder = 0, then it divides evenly (no leftovers)
        - Focus on **what the remainder represents** in the story
        
        ### Example Walkthrough:
        **"Sarah has 58 stickers. She puts 7 stickers on each page. How many stickers will be left over?"**
        
        **Step 1:** 58 ÷ 7 = ?
        **Step 2:** 58 ÷ 7 = 8 R 2
        **Step 3:** The remainder is 2
        **Answer:** 2 stickers will be left over
        """)

def generate_new_remainder_problem():
    """Generate a new remainder interpretation problem based on difficulty"""
    difficulty = st.session_state.remainder_difficulty
    
    # Problem templates focused on finding remainders
    scenarios = {
        1: [  # Beginner (2-digit numbers)
            {
                "template": "At the fair, Rose has {total} ride tickets. Each ride on the Ferris wheel costs {divisor} tickets. After riding the Ferris wheel as many times as possible, how many tickets will Rose have left?",
                "context": "tickets",
                "unit": "tickets",
                "range": (25, 99),
                "divisors": [2, 3, 4, 5, 6, 7, 8, 9]
            },
            {
                "template": "Jake has {total} stickers. He puts {divisor} stickers on each page of his album. How many stickers will be left over?",
                "context": "stickers",
                "unit": "stickers", 
                "range": (20, 85),
                "divisors": [3, 4, 5, 6, 7, 8]
            },
            {
                "template": "A teacher has {total} pencils to share equally among {divisor} students. How many pencils will be left over?",
                "context": "sharing",
                "unit": "pencils",
                "range": (30, 95),
                "divisors": [4, 5, 6, 7, 8, 9]
            },
            {
                "template": "There are {total} cookies. Each box holds {divisor} cookies. How many cookies will not fit in the boxes?",
                "context": "packing",
                "unit": "cookies",
                "range": (25, 89),
                "divisors": [3, 4, 5, 6, 7, 8]
            },
            {
                "template": "Maya has {total} marbles. She groups them into sets of {divisor}. How many marbles will be left over?",
                "context": "grouping",
                "unit": "marbles",
                "range": (35, 95),
                "divisors": [4, 5, 6, 7, 8, 9]
            },
            {
                "template": "A game takes {divisor} minutes. If Sam has {total} minutes to play, how many minutes will he have left after playing complete games?",
                "context": "time",
                "unit": "minutes",
                "range": (40, 85),
                "divisors": [6, 7, 8, 9]
            }
        ],
        
        2: [  # Intermediate (3-digit numbers)
            {
                "template": "The school cafeteria has {total} lunch trays. Each table seats {divisor} students. How many trays will be left over after filling complete tables?",
                "context": "seating",
                "unit": "trays",
                "range": (150, 399),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A factory produces {total} widgets per day. They pack {divisor} widgets in each shipping container. How many widgets will be left over at the end of the day?",
                "context": "production",
                "unit": "widgets",
                "range": (200, 450),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "The library has {total} books to arrange on shelves. Each shelf holds {divisor} books. How many books will be left over?",
                "context": "organizing",
                "unit": "books",
                "range": (180, 350),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A party planner has {total} balloons. She makes bouquets with {divisor} balloons each. How many balloons will be left over?",
                "context": "party",
                "unit": "balloons",
                "range": (165, 385),
                "divisors": [7, 8, 9]
            },
            {
                "template": "There are {total} students in the school. They form teams of {divisor} students each for field day. How many students will not be on a complete team?",
                "context": "teams",
                "unit": "students",
                "range": (240, 480),
                "divisors": [6, 7, 8]
            },
            {
                "template": "A bakery makes {total} muffins. They pack {divisor} muffins in each box. How many muffins will be left over?",
                "context": "baking",
                "unit": "muffins",
                "range": (220, 420),
                "divisors": [6, 8, 9]
            },
            {
                "template": "A movie theater has {total} seats. Each row has {divisor} seats. How many seats will be in the incomplete row?",
                "context": "seating",
                "unit": "seats",
                "range": (175, 365),
                "divisors": [6, 7, 8, 9]
            }
        ],
        
        3: [  # Advanced (4+ digit numbers)
            {
                "template": "A shipping company receives {total} packages. Each truck carries {divisor} packages. How many packages will be left for the next day?",
                "context": "shipping",
                "unit": "packages",
                "range": (2000, 5500),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A concert venue has {total} attendees. Each section holds {divisor} people. How many people will be in the partially filled section?",
                "context": "venue",
                "unit": "people",
                "range": (3000, 7500),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A warehouse has {total} items in inventory. They ship items in crates of {divisor}. How many items will remain in the warehouse?",
                "context": "inventory",
                "unit": "items",
                "range": (1800, 6200),
                "divisors": [7, 8, 9]
            },
            {
                "template": "An online store processes {total} orders per week. Each batch contains {divisor} orders. How many orders will be left for the next batch?",
                "context": "orders",
                "unit": "orders",
                "range": (2400, 5800),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A printing company has {total} sheets of paper. Each book requires {divisor} sheets. How many sheets will be left over after making complete books?",
                "context": "printing",
                "unit": "sheets",
                "range": (1500, 4999),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A school district has {total} textbooks. Each classroom gets {divisor} textbooks. How many textbooks will be left in storage?",
                "context": "distribution",
                "unit": "textbooks",
                "range": (3200, 6800),
                "divisors": [7, 8, 9]
            }
        ]
    }
    
    # Select random scenario from current difficulty
    scenario = random.choice(scenarios[difficulty])
    
    # Generate numbers that will have a remainder
    attempts = 0
    while attempts < 20:  # Prevent infinite loop
        total = random.randint(*scenario["range"])
        divisor = random.choice(scenario["divisors"])
        remainder = total % divisor
        
        # Ensure we have a remainder (not zero)
        if remainder > 0:
            break
        attempts += 1
    
    # If we couldn't find one with remainder, force a remainder
    if remainder == 0:
        total += random.randint(1, divisor - 1)
        remainder = total % divisor
    
    # Calculate division
    quotient = total // divisor
    
    # Create problem text
    problem_text = scenario["template"].format(total=total, divisor=divisor)
    
    st.session_state.remainder_problem_data = {
        "problem_text": problem_text,
        "total": total,
        "divisor": divisor,
        "quotient": quotient,
        "remainder": remainder,
        "context": scenario["context"],
        "unit": scenario["unit"]
    }
    st.session_state.correct_remainder_answer = remainder
    st.session_state.current_remainder_problem = problem_text

def display_remainder_problem():
    """Display the current remainder problem interface"""
    data = st.session_state.remainder_problem_data
    
    # Display question header
    st.markdown("### 🔍 Remainder Problem:")
    
    # Display the problem in a nice box
    st.markdown(f"""
    <div style="
        background-color: #fff3e0; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #ff9800;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        color: #333;
    ">
        {data['problem_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Show the division calculation for reference
    st.markdown(f"""
    <div style="
        background-color: #f3e5f5; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #9c27b0;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        margin: 20px 0;
        text-align: center;
    ">
        <strong>Division to solve:</strong> {data['total']:,} ÷ {data['divisor']} = ? R ?<br>
        <em>Remember: You need to find the remainder!</em>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("remainder_form", clear_on_submit=False):
        st.markdown(f"**How many {data['unit']} will be left over?**")
        
        user_answer = st.number_input(
            f"Number of {data['unit']} left over:",
            min_value=0,
            max_value=data['divisor']-1,
            step=1,
            key="remainder_answer_input",
            help=f"The remainder must be less than {data['divisor']}"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_remainder_answer = int(user_answer) if user_answer is not None else 0
            st.session_state.show_remainder_feedback = True
            st.session_state.remainder_answer_submitted = True
    
    # Show feedback and next button
    handle_remainder_feedback_and_next()

def handle_remainder_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_remainder_feedback:
        show_remainder_feedback()
    
    # Next question button
    if st.session_state.remainder_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_remainder_question_state()
                st.rerun()

def show_remainder_feedback():
    """Display feedback for the submitted remainder answer"""
    user_answer = st.session_state.user_remainder_answer
    correct_answer = st.session_state.correct_remainder_answer
    data = st.session_state.remainder_problem_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Perfect! You found the correct remainder!**")
        
        # Show the complete solution
        st.info(f"✅ **{correct_answer} {data['unit']} will be left over**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.remainder_difficulty
        st.session_state.remainder_difficulty = min(st.session_state.remainder_difficulty + 1, 3)
        
        if st.session_state.remainder_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered remainder interpretation!**")
        elif old_difficulty < st.session_state.remainder_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working on Level {st.session_state.remainder_difficulty} problems**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct remainder is **{correct_answer}**.")
        
        # Show what this means
        st.info(f"This means **{correct_answer} {data['unit']} will be left over**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.remainder_difficulty
        st.session_state.remainder_difficulty = max(st.session_state.remainder_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.remainder_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.remainder_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_remainder_explanation()

def show_remainder_explanation():
    """Show step-by-step explanation of the remainder problem solution"""
    data = st.session_state.remainder_problem_data
    total = data["total"]
    divisor = data["divisor"]
    quotient = data["quotient"]
    remainder = data["remainder"]
    unit = data["unit"]
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Problem Breakdown:
        **What we know:**
        - Total {unit}: {total:,}
        - Group size: {divisor}
        - Question: "How many {unit} will be left over?"
        
        ### Step 1: Set up the division
        {total:,} ÷ {divisor} = ?
        
        ### Step 2: Calculate the division
        {total:,} ÷ {divisor} = {quotient} R {remainder}
        
        ### Step 3: Interpret the remainder
        - **Quotient ({quotient}):** Number of complete groups
        - **Remainder ({remainder}):** Number of {unit} left over
        - **The question asks for the remainder**
        
        ### Step 4: Answer the question
        **{remainder} {unit} will be left over**
        
        ### Visual Breakdown:
        """)
        
        # Show visual representation for smaller numbers
        if total <= 50:
            st.markdown(f"""
            **Think of it this way:**
            - If you have {total} {unit}
            - And you make groups of {divisor}
            - You can make {quotient} complete groups ({quotient} × {divisor} = {quotient * divisor})
            - That uses {quotient * divisor} {unit}
            - So {total} - {quotient * divisor} = **{remainder} {unit} left over**
            """)
        else:
            st.markdown(f"""
            **Calculation check:**
            - {quotient} complete groups × {divisor} per group = {quotient * divisor} {unit} used
            - {total:,} total - {quotient * divisor:,} used = **{remainder} {unit} left over**
            """)
        
        # Show verification
        st.markdown(f"""
        ### Verification:
        **Check:** {quotient} × {divisor} + {remainder} = {quotient * divisor + remainder:,} = {total:,} ✅
        
        ### Remember:
        - The **remainder** is always what's "left over"
        - It's always **smaller than the divisor** ({remainder} < {divisor})
        - It answers questions like "How many will be left?" or "How many extra?"
        """)

def reset_remainder_question_state():
    """Reset the question state for next question"""
    st.session_state.current_remainder_problem = None
    st.session_state.correct_remainder_answer = None
    st.session_state.show_remainder_feedback = False
    st.session_state.remainder_answer_submitted = False
    st.session_state.remainder_problem_data = {}
    if "user_remainder_answer" in st.session_state:
        del st.session_state.user_remainder_answer