import streamlit as st
import random

def run():
    """
    Main function to run the Divide by One-Digit Numbers: Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_by_one_digit_numbers_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = 1  # Start with simple problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("📝 Division Word Problems")
    st.markdown("*Solve real-world problems using division*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple scenarios (2-digit numbers)",
            2: "Intermediate scenarios (3-digit numbers)", 
            3: "Complex scenarios (4+ digit numbers)"
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
    if st.session_state.current_problem is None:
        generate_new_word_problem()
    
    # Display current question
    display_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Division Word Problems:
        
        #### **Step 1: Read Carefully**
        - **Read the problem twice** to understand what's happening
        - **Identify the key information** (numbers and what they represent)
        - **Find the question** being asked
        
        #### **Step 2: Identify the Operation**
        - Look for **division keywords**: "packages of", "groups of", "per", "each", "split equally"
        - Ask: **"Am I sharing or grouping?"**
        
        #### **Step 3: Set Up the Division**
        - **Total amount ÷ Size of each group = Number of groups**
        - **Total amount ÷ Number of groups = Size of each group**
        
        #### **Step 4: Handle Remainders**
        - **Round UP** when you need whole packages/trips/groups
        - **Round DOWN** when the remainder can't be used
        - **Use the exact remainder** when it represents leftover items
        
        ### Common Scenarios:
        
        **🛒 Shopping Problems:**
        - "Items come in packages of X" → Usually round UP
        - "How many complete packages?" → Use quotient only
        
        **🚌 Transportation Problems:**
        - "How many buses needed?" → Usually round UP
        - "How many people per bus?" → Use quotient, remainder = extra people
        
        **🎯 Equal Groups:**
        - "Split equally among X people" → Quotient = amount per person
        - "How many complete teams?" → Use quotient only
        
        **📦 Packaging Problems:**
        - "How many boxes needed?" → Round UP
        - "How many items left over?" → Use remainder
        
        ### Example Walkthrough:
        **"72 students, 8 students per bus. How many buses needed?"**
        - 72 ÷ 8 = 9 R 0
        - Answer: 9 buses (no remainder, so exactly 9 buses)
        
        **"73 students, 8 students per bus. How many buses needed?"**  
        - 73 ÷ 8 = 9 R 1
        - Answer: 10 buses (need to round UP for the 1 extra student)
        
        ### Key Words to Look For:
        - **"packages of"** → Division needed, often round UP
        - **"groups of"** → Division needed
        - **"equally"** → Division for fair sharing
        - **"per"** → Division (rate problems)
        - **"how many complete"** → Use quotient only
        - **"how many more needed"** → Look at remainder
        """)

def generate_new_word_problem():
    """Generate a new division word problem based on difficulty"""
    difficulty = st.session_state.word_problem_difficulty
    
    # Problem templates with different scenarios
    scenarios = {
        1: [  # Beginner (2-digit numbers)
            {
                "template": "An electrician needs to buy {total} light bulbs. The light bulbs come in packages of {divisor}. How many packages should the electrician buy?",
                "context": "shopping",
                "round_up": True,
                "range": (20, 99),
                "divisors": [4, 5, 6, 8]
            },
            {
                "template": "A teacher has {total} stickers to share equally among {divisor} students. How many stickers will each student get?",
                "context": "sharing",
                "round_up": False,
                "range": (24, 96),
                "divisors": [3, 4, 6, 8]
            },
            {
                "template": "{total} students are going on a field trip. Each bus can hold {divisor} students. How many buses are needed?",
                "context": "transportation",
                "round_up": True,
                "range": (30, 89),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A baker made {total} cookies. She puts {divisor} cookies in each box. How many complete boxes can she fill?",
                "context": "complete_groups",
                "round_up": False,
                "range": (35, 95),
                "divisors": [4, 5, 6, 7, 8]
            },
            {
                "template": "There are {total} books to be placed on shelves. Each shelf holds {divisor} books. How many shelves will be completely filled?",
                "context": "complete_groups", 
                "round_up": False,
                "range": (28, 84),
                "divisors": [4, 6, 7, 9]
            }
        ],
        
        2: [  # Intermediate (3-digit numbers)
            {
                "template": "A factory produces {total} toys per day. The toys are packed in boxes of {divisor}. How many boxes are needed each day?",
                "context": "packaging",
                "round_up": True,
                "range": (150, 399),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A school has {total} students. They want to form equal teams of {divisor} students each for sports day. How many complete teams can they form?",
                "context": "complete_groups",
                "round_up": False,
                "range": (180, 350),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A charity collected {total} canned goods. They pack {divisor} cans in each bag for distribution. How many bags do they need?",
                "context": "packaging",
                "round_up": True,
                "range": (200, 450),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "An office building has {total} employees. Each elevator can carry {divisor} people. How many elevator trips are needed to transport everyone?",
                "context": "transportation",
                "round_up": True,
                "range": (165, 385),
                "divisors": [7, 8, 9]
            },
            {
                "template": "A restaurant needs to seat {total} customers. Each table seats {divisor} people. How many tables do they need?",
                "context": "seating",
                "round_up": True,
                "range": (175, 420),
                "divisors": [6, 8]
            },
            {
                "template": "A librarian has {total} books to distribute equally among {divisor} classrooms. How many books will each classroom receive?",
                "context": "sharing",
                "round_up": False,
                "range": (240, 480),
                "divisors": [6, 8]
            }
        ],
        
        3: [  # Advanced (4+ digit numbers)
            {
                "template": "A concert venue has {total} seats. The seats are arranged in sections of {divisor} seats each. How many complete sections are there?",
                "context": "complete_groups",
                "round_up": False,
                "range": (1500, 4999),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A shipping company needs to transport {total} packages. Each truck can carry {divisor} packages. How many trucks are needed?",
                "context": "transportation",
                "round_up": True,
                "range": (2000, 5500),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A factory has {total} items to pack. Each crate holds {divisor} items. How many crates are needed?",
                "context": "packaging",
                "round_up": True,
                "range": (1800, 6200),
                "divisors": [7, 8, 9]
            },
            {
                "template": "A stadium has {total} spectators. Each section holds {divisor} people. How many sections will be completely filled?",
                "context": "complete_groups",
                "round_up": False,
                "range": (3000, 7500),
                "divisors": [6, 7, 8, 9]
            },
            {
                "template": "A bookstore receives {total} books. They display {divisor} books per shelf. How many shelves do they need?",
                "context": "display",
                "round_up": True,
                "range": (2400, 5800),
                "divisors": [6, 7, 8, 9]
            }
        ]
    }
    
    # Select random scenario from current difficulty
    scenario = random.choice(scenarios[difficulty])
    
    # Generate numbers
    total = random.randint(*scenario["range"])
    divisor = random.choice(scenario["divisors"])
    
    # Calculate division
    quotient = total // divisor
    remainder = total % divisor
    
    # Determine correct answer based on context
    if scenario["round_up"] and remainder > 0:
        correct_answer = quotient + 1
        explanation_type = "round_up"
    else:
        correct_answer = quotient
        explanation_type = "quotient_only"
    
    # Create problem text
    problem_text = scenario["template"].format(total=total, divisor=divisor)
    
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "total": total,
        "divisor": divisor,
        "quotient": quotient,
        "remainder": remainder,
        "context": scenario["context"],
        "round_up": scenario["round_up"],
        "explanation_type": explanation_type
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_problem = problem_text

def display_word_problem():
    """Display the current word problem interface"""
    data = st.session_state.problem_data
    
    # Display question header
    st.markdown("### 📖 Word Problem:")
    
    # Display the problem in a nice box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
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
        background-color: #e3f2fd; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #1976d2;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        margin: 20px 0;
        text-align: center;
    ">
        <strong>Division needed:</strong> {data['total']} ÷ {data['divisor']} = ?
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("word_problem_form", clear_on_submit=False):
        st.markdown("**What is your answer?**")
        
        user_answer = st.number_input(
            "Enter your answer:",
            min_value=0,
            step=1,
            key="answer_input",
            help="Think about whether you need to round up or use just the quotient"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = int(user_answer) if user_answer is not None else 0
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
    data = st.session_state.problem_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete solution
        st.info(f"✅ **Answer: {correct_answer}**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = min(st.session_state.word_problem_difficulty + 1, 3)
        
        if st.session_state.word_problem_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered complex division word problems!**")
        elif old_difficulty < st.session_state.word_problem_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working on Level {st.session_state.word_problem_difficulty} problems**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = max(st.session_state.word_problem_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.word_problem_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.word_problem_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation of the word problem solution"""
    data = st.session_state.problem_data
    total = data["total"]
    divisor = data["divisor"]
    quotient = data["quotient"]
    remainder = data["remainder"]
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Problem Analysis:
        **Given information:**
        - Total amount: {total:,}
        - Group size: {divisor}
        - Question asks: {get_question_type(data['context'])}
        
        ### Step 1: Set up the division
        {total:,} ÷ {divisor} = ?
        
        ### Step 2: Calculate
        {total:,} ÷ {divisor} = {quotient} R {remainder}
        
        ### Step 3: Interpret the result
        """)
        
        if data["round_up"] and remainder > 0:
            st.markdown(f"""
            - **Quotient:** {quotient} (complete groups)
            - **Remainder:** {remainder} (leftover items)
            - **Since we need {get_round_up_reason(data['context'])}, we round UP**
            - **Answer:** {quotient} + 1 = **{correct_answer}**
            """)
        elif remainder > 0:
            st.markdown(f"""
            - **Quotient:** {quotient} (complete groups)
            - **Remainder:** {remainder} (leftover items that don't form a complete group)
            - **Since the question asks for complete groups only, we use the quotient**
            - **Answer:** **{quotient}**
            """)
        else:
            st.markdown(f"""
            - **Quotient:** {quotient} (complete groups)
            - **Remainder:** 0 (no leftover items)
            - **Perfect division - no remainder to consider**
            - **Answer:** **{quotient}**
            """)
        
        # Show verification
        st.markdown(f"""
        ### Verification:
        **Check:** {quotient} × {divisor} + {remainder} = {quotient * divisor + remainder} = {total:,} ✅
        """)

def get_question_type(context):
    """Return description of what the question is asking based on context"""
    descriptions = {
        "shopping": "How many packages to buy",
        "sharing": "How many items per person", 
        "transportation": "How many vehicles needed",
        "complete_groups": "How many complete groups can be formed",
        "packaging": "How many containers needed",
        "seating": "How many tables/sections needed",
        "display": "How many shelves needed"
    }
    return descriptions.get(context, "The answer to the question")

def get_round_up_reason(context):
    """Return explanation for why we round up in this context"""
    reasons = {
        "shopping": "enough packages to get all items",
        "transportation": "enough vehicles for all people",
        "packaging": "enough containers for all items", 
        "seating": "enough tables for all customers",
        "display": "enough shelves for all items"
    }
    return reasons.get(context, "to accommodate all items")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer