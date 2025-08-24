import streamlit as st
import random

def run():
    """
    Main function to run the Write numerical expressions for word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/write_numerical_expressions_for_word_problems.py
    """
    # Initialize session state
    if "word_expression_difficulty" not in st.session_state:
        st.session_state.word_expression_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_expression = None
        st.session_state.wrong_expression = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.selected_expression = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("📝 Write Numerical Expressions for Word Problems")
    st.markdown("*Choose the expression that matches the story*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_expression_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Standard", "Complex", "Multi-Step", "Advanced"]
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
        generate_new_word_expression_problem()
    
    # Display current problem
    display_word_expression_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Tips for Writing Expressions**", expanded=False):
        st.markdown("""
        ### How to Choose the Right Expression:
        
        **1. Read Carefully** 📖
        - What is happening in the story?
        - What numbers are given?
        - What are we trying to find?
        
        **2. Identify the Operation** 🔍
        
        **➕ Addition - Combining or Adding Together:**
        - "made in all", "altogether", "total"
        - Combining different groups
        - Finding the sum
        
        **➖ Subtraction - Taking Away or Finding Difference:**
        - "left", "remaining", "how many more"
        - One amount being removed from another
        - Finding what's left
        
        **✖️ Multiplication - Groups or Repeated Addition:**
        - "each", "per", "every"
        - Equal groups being combined
        - Same amount multiple times
        
        **➗ Division - Sharing or Grouping:**
        - "share equally", "how many each"
        - Finding how many groups
        - Splitting into equal parts
        
        ### Examples:
        
        **Addition:** "Sarah has 12 apples. Tom has 8 apples. How many apples in total?"
        → **12 + 8** (combining two amounts)
        
        **Subtraction:** "A store had 50 toys. They sold 18 toys. How many toys are left?"
        → **50 - 18** (taking away from total)
        
        **Multiplication:** "There are 6 boxes. Each box has 9 cookies. How many cookies total?"
        → **6 × 9** (equal groups)
        
        **Division:** "24 students need to form teams of 4. How many teams can they make?"
        → **24 ÷ 4** (grouping)
        
        ### Common Mistakes:
        - Don't multiply just because you see two numbers!
        - Look for keywords that tell you the operation
        - Think: Does the answer get bigger or smaller?
        """)

def generate_word_problem_scenarios():
    """Generate diverse word problem scenarios"""
    return {
        "addition": [
            {
                "template": "{name1} made {num1} {item}. {name2} made {num2} {item}. Which expression tells you how many {item} {name1} and {name2} made in all?",
                "names": [("Abby", "Darnel"), ("Emma", "Jake"), ("Sofia", "Ryan"), ("Maya", "Luis")],
                "items": ["lemon blueberry scones", "chocolate chip cookies", "cupcakes", "muffins", "brownies"],
                "correct": "{num1} + {num2}",
                "wrong": "{num1} × {num2}"
            },
            {
                "template": "{name} is building a model of a {object}. On Monday, {pronoun} put together {num1} pieces. On Tuesday, {pronoun} put together {num2} pieces. Which expression tells you how many pieces {name} put together in all?",
                "names": [("Jacob", "he"), ("Sarah", "she"), ("Alex", "they"), ("Maria", "she")],
                "objects": ["skyscraper", "spaceship", "castle", "bridge", "dinosaur"],
                "correct": "{num1} + {num2}",
                "wrong": "{num1} × {num2}"
            },
            {
                "template": "A library received {num1} new books on Monday and {num2} new books on Wednesday. Which expression shows the total number of new books?",
                "correct": "{num1} + {num2}",
                "wrong": "{num1} - {num2}"
            },
            {
                "template": "{name} collected {num1} stamps last month and {num2} stamps this month. Which expression shows how many stamps {name} collected altogether?",
                "names": ["Oliver", "Sophia", "Ethan", "Isabella"],
                "correct": "{num1} + {num2}",
                "wrong": "{num1} × {num2}"
            }
        ],
        
        "subtraction": [
            {
                "template": "A parking lot has {num1} spaces. Currently, {num2} cars are parked. Which expression tells you how many empty spaces there are?",
                "correct": "{num1} - {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "{name} had {num1} {currency} in savings. {pronoun} spent {num2} {currency} on a new {item}. Which expression shows how much money {name} has left?",
                "names": [("Tom", "He"), ("Lisa", "She"), ("Sam", "They"), ("Anna", "She")],
                "currency": ["dollars", "pounds", "euros"],
                "items": ["video game", "book", "backpack", "skateboard"],
                "correct": "{num1} - {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "The school cafeteria prepared {num1} lunches. They served {num2} lunches. Which expression shows how many lunches are left?",
                "correct": "{num1} - {num2}",
                "wrong": "{num1} × {num2}"
            },
            {
                "template": "A store received {num1} {items}. They sold {num2} {items} by noon. Which expression tells you how many {items} remain?",
                "items": ["tablets", "phones", "laptops", "watches"],
                "correct": "{num1} - {num2}",
                "wrong": "{num1} ÷ {num2}"
            }
        ],
        
        "multiplication": [
            {
                "template": "The art teacher has {num1} boxes of markers. Each box has {num2} markers. Which expression tells you the total number of markers the art teacher has?",
                "correct": "{num1} × {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "A bakery makes {num1} batches of cookies. Each batch contains {num2} cookies. Which expression shows the total number of cookies?",
                "correct": "{num1} × {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "{name} is organizing a party. There are {num1} tables, and each table seats {num2} people. Which expression tells you how many people can be seated?",
                "names": ["Rachel", "Michael", "Jessica", "Daniel"],
                "correct": "{num1} × {num2}",
                "wrong": "{num1} - {num2}"
            },
            {
                "template": "A gardener planted {num1} rows of flowers. Each row has {num2} flowers. Which expression shows the total number of flowers?",
                "correct": "{num1} × {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "Movie tickets cost ${num2} each. {name} is buying {num1} tickets. Which expression shows how much {name} will pay?",
                "names": ["Chris", "Amy", "David", "Emma"],
                "correct": "{num1} × {num2}",
                "wrong": "{num1} + {num2}"
            }
        ],
        
        "division": [
            {
                "template": "{name} made ${num1} from selling containers of homemade {product}. {pronoun} charged ${num2} for each container. Which expression tells you how many containers of {product} {name} sold?",
                "names": [("Nora", "She"), ("James", "He"), ("Alex", "They"), ("Maya", "She")],
                "products": ["slime", "soap", "candles", "cookies"],
                "correct": "{num1} ÷ {num2}",
                "wrong": "{num1} × {num2}"
            },
            {
                "template": "A teacher has {num1} pencils to distribute equally among {num2} students. Which expression shows how many pencils each student will get?",
                "correct": "{num1} ÷ {num2}",
                "wrong": "{num1} - {num2}"
            },
            {
                "template": "A pizza restaurant cut a large pizza into {num1} slices. If {num2} friends share it equally, which expression tells you how many slices each friend gets?",
                "correct": "{num1} ÷ {num2}",
                "wrong": "{num1} + {num2}"
            },
            {
                "template": "{name} has {num1} {items} to pack into boxes. Each box holds {num2} {items}. Which expression shows how many boxes {name} needs?",
                "names": ["Kevin", "Sarah", "Mike", "Julia"],
                "items": ["books", "toys", "ornaments", "trophies"],
                "correct": "{num1} ÷ {num2}",
                "wrong": "{num1} × {num2}"
            }
        ]
    }

def generate_new_word_expression_problem():
    """Generate a new word expression problem based on difficulty"""
    difficulty = st.session_state.word_expression_difficulty
    scenarios = generate_word_problem_scenarios()
    
    # Choose operation based on difficulty
    if difficulty == 1:
        operations = ["addition", "subtraction"]
    else:
        operations = ["addition", "subtraction", "multiplication", "division"]
    
    operation = random.choice(operations)
    scenario = random.choice(scenarios[operation])
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        if operation == "addition":
            num1 = random.randint(5, 50)
            num2 = random.randint(5, 50)
        elif operation == "subtraction":
            num1 = random.randint(20, 100)
            num2 = random.randint(5, num1 - 5)
    elif difficulty == 2:
        if operation == "addition":
            num1 = random.randint(10, 200)
            num2 = random.randint(10, 200)
        elif operation == "subtraction":
            num1 = random.randint(50, 500)
            num2 = random.randint(10, num1 - 10)
        elif operation == "multiplication":
            num1 = random.randint(2, 20)
            num2 = random.randint(2, 12)
        else:  # division
            num2 = random.randint(2, 10)
            num1 = num2 * random.randint(3, 20)
    elif difficulty == 3:
        if operation == "addition":
            num1 = random.randint(50, 500)
            num2 = random.randint(50, 500)
        elif operation == "subtraction":
            num1 = random.randint(100, 1000)
            num2 = random.randint(50, num1 - 50)
        elif operation == "multiplication":
            num1 = random.randint(10, 50)
            num2 = random.randint(2, 25)
        else:  # division
            num2 = random.randint(3, 15)
            num1 = num2 * random.randint(5, 50)
    elif difficulty == 4:
        if operation == "addition":
            num1 = random.randint(100, 1000)
            num2 = random.randint(100, 1000)
        elif operation == "subtraction":
            num1 = random.randint(500, 5000)
            num2 = random.randint(100, num1 - 100)
        elif operation == "multiplication":
            num1 = random.randint(20, 100)
            num2 = random.randint(5, 50)
        else:  # division
            num2 = random.randint(5, 25)
            num1 = num2 * random.randint(10, 100)
    else:  # difficulty == 5
        if operation == "addition":
            num1 = random.randint(500, 5000)
            num2 = random.randint(500, 5000)
        elif operation == "subtraction":
            num1 = random.randint(1000, 10000)
            num2 = random.randint(500, num1 - 500)
        elif operation == "multiplication":
            num1 = random.randint(50, 500)
            num2 = random.randint(10, 100)
        else:  # division
            num2 = random.randint(10, 50)
            num1 = num2 * random.randint(20, 200)
    
    # Build the problem text
    problem_text = scenario["template"]
    
    # Replace placeholders
    if "names" in scenario:
        if isinstance(scenario["names"][0], tuple):
            name_data = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name_data[0])
            problem_text = problem_text.replace("{pronoun}", name_data[1])
        else:
            name = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name)
    
    if "names" in scenario and isinstance(scenario["names"][0], tuple):
        names = random.choice(scenario["names"])
        problem_text = problem_text.replace("{name1}", names[0])
        problem_text = problem_text.replace("{name2}", names[1])
    
    # Replace other placeholders
    for placeholder in ["items", "objects", "currency", "products"]:
        if placeholder in scenario:
            item = random.choice(scenario[placeholder])
            problem_text = problem_text.replace(f"{{{placeholder[:-1]}}}", item)
            problem_text = problem_text.replace(f"{{{placeholder}}}", item)
    
    problem_text = problem_text.replace("{num1}", str(num1))
    problem_text = problem_text.replace("{num2}", str(num2))
    
    # Generate expressions
    correct_expression = scenario["correct"].replace("{num1}", str(num1)).replace("{num2}", str(num2))
    wrong_expression = scenario["wrong"].replace("{num1}", str(num1)).replace("{num2}", str(num2))
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "operation": operation,
        "num1": num1,
        "num2": num2
    }
    st.session_state.correct_expression = correct_expression
    st.session_state.wrong_expression = wrong_expression
    st.session_state.current_problem = problem_text

def display_word_expression_problem():
    """Display the current word expression problem"""
    # Display the story
    st.markdown("### Read the story.")
    
    # Story in a card
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        font-size: 18px;
        line-height: 1.6;
    ">
        {st.session_state.current_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Expression options
    st.markdown("### Which expression tells you the answer?")
    
    # Randomly order the expressions
    if random.random() < 0.5:
        left_expr = st.session_state.correct_expression
        right_expr = st.session_state.wrong_expression
        left_is_correct = True
    else:
        left_expr = st.session_state.wrong_expression
        right_expr = st.session_state.correct_expression
        left_is_correct = False
    
    # Create clickable tiles
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            left_expr,
            key="left_tile",
            use_container_width=True,
            disabled=st.session_state.answer_submitted,
            type="secondary" if st.session_state.selected_expression != "left" else "primary"
        ):
            st.session_state.selected_expression = "left"
            st.rerun()
    
    with col2:
        if st.button(
            right_expr,
            key="right_tile",
            use_container_width=True,
            disabled=st.session_state.answer_submitted,
            type="secondary" if st.session_state.selected_expression != "right" else "primary"
        ):
            st.session_state.selected_expression = "right"
            st.rerun()
    
    # Submit button
    if st.session_state.selected_expression and not st.session_state.answer_submitted:
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                # Check answer
                if st.session_state.selected_expression == "left":
                    st.session_state.user_answer = left_expr
                    st.session_state.is_correct = left_is_correct
                else:
                    st.session_state.user_answer = right_expr
                    st.session_state.is_correct = not left_is_correct
                
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
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
    is_correct = st.session_state.is_correct
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_expression
    
    if is_correct:
        st.success(f"🎉 **Correct! {correct_answer} is the right expression!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.word_expression_difficulty
        st.session_state.word_expression_difficulty = min(
            st.session_state.word_expression_difficulty + 1, 5
        )
        
        if st.session_state.word_expression_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Fantastic! You've mastered expression writing!**")
        elif old_difficulty < st.session_state.word_expression_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.word_expression_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct expression is {correct_answer}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.word_expression_difficulty
        st.session_state.word_expression_difficulty = max(
            st.session_state.word_expression_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.word_expression_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.word_expression_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_problem_explanation()

def show_problem_explanation():
    """Show explanation for the correct expression"""
    operation = st.session_state.problem_data["operation"]
    num1 = st.session_state.problem_data["num1"]
    num2 = st.session_state.problem_data["num2"]
    
    with st.expander("📖 **Understanding the Problem**", expanded=True):
        st.markdown("### Let's break down the story:")
        
        # Operation-specific explanations
        if operation == "addition":
            st.markdown(f"""
            **What's happening:** Two amounts are being combined
            - First amount: {num1}
            - Second amount: {num2}
            - We need to find: the total
            
            **Key words:** "in all", "altogether", "made together"
            
            **Operation:** Addition (+)
            
            **Expression:** {num1} + {num2}
            
            💡 **Why not multiplication?**
            We're combining two separate amounts, not finding groups of equal size.
            """)
            
        elif operation == "subtraction":
            st.markdown(f"""
            **What's happening:** One amount is being taken from another
            - Starting amount: {num1}
            - Amount removed: {num2}
            - We need to find: what's left
            
            **Key words:** "left", "remaining", "spent"
            
            **Operation:** Subtraction (-)
            
            **Expression:** {num1} - {num2}
            
            💡 **Why not addition?**
            We're finding what remains after taking away, not combining.
            """)
            
        elif operation == "multiplication":
            st.markdown(f"""
            **What's happening:** Equal groups are being combined
            - Number of groups: {num1}
            - Amount in each group: {num2}
            - We need to find: the total
            
            **Key words:** "each", "per", "every"
            
            **Operation:** Multiplication (×)
            
            **Expression:** {num1} × {num2}
            
            💡 **Why not addition?**
            We have equal groups, not just two amounts to add.
            Example: 5 groups of 3 = 5 × 3 = 15 (not 5 + 3 = 8)
            """)
            
        else:  # division
            st.markdown(f"""
            **What's happening:** A total is being split into equal parts
            - Total amount: {num1}
            - Size/cost of each part: {num2}
            - We need to find: how many parts
            
            **Key words:** "how many", "charged each", "per"
            
            **Operation:** Division (÷)
            
            **Expression:** {num1} ÷ {num2}
            
            💡 **Why not multiplication?**
            We're finding how many groups, not the total of groups.
            Example: $30 total ÷ $3 each = 10 items (not 30 × 3 = 90)
            """)
        
        # Visual tip
        st.markdown("""
        ### Remember:
        - **Addition (+)**: Combining different amounts
        - **Subtraction (-)**: Taking away or finding what's left
        - **Multiplication (×)**: Equal groups or "each"
        - **Division (÷)**: Sharing equally or finding "how many"
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_expression = None
    st.session_state.wrong_expression = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    st.session_state.selected_expression = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
    if "is_correct" in st.session_state:
        del st.session_state.is_correct