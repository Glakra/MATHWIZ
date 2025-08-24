import streamlit as st
import random

def run():
    """
    Main function to run decimal word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/K. Mixed operations/add_subtract_and_multiply_decimals_word_problems.py
    """
    # Initialize session state
    if "decimal_word_difficulty" not in st.session_state:
        st.session_state.decimal_word_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > K. Mixed operations**")
    st.title("📖 Decimal Word Problems: Add, Subtract & Multiply")
    st.markdown("*Solve real-world problems with decimal numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic Decimals", "Mixed Decimals", "Complex Problems", "Multi-Step", "Master Level"]
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
        generate_new_decimal_word_problem()
    
    # Display current problem
    display_decimal_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Problem-Solving Guide**", expanded=False):
        st.markdown("""
        ### Steps to Solve Decimal Word Problems:
        
        **1. Understand the Problem** 📖
        - Read carefully - what are we finding?
        - Identify the decimal numbers
        - Look for keywords
        
        **2. Choose the Operation** 🔍
        
        **Addition Keywords:**
        - total, sum, altogether, combined
        - bought... and bought more
        - in all, both together
        
        **Subtraction Keywords:**
        - left, remaining, how much more
        - used, spent, cut off, sawed off
        - difference between
        
        **Multiplication Keywords:**
        - each, per, every
        - rate × time
        - groups of, sets of
        
        **3. Work with Decimals** 🔢
        - **Addition/Subtraction:** Line up decimal points!
        - **Multiplication:** Count total decimal places
        - Always estimate first
        
        **4. Check Your Answer** ✓
        - Does it make sense?
        - Is it reasonable?
        - Did you place the decimal correctly?
        
        ### Example Problems:
        
        **Addition:** "Maya ran 3.5 km on Monday and 2.75 km on Tuesday. How far did she run in total?"
        - 3.5 + 2.75 = 6.25 km
        
        **Subtraction:** "A rope is 5.2 meters long. If 1.85 meters is cut off, how much remains?"
        - 5.2 - 1.85 = 3.35 meters
        
        **Multiplication:** "Gas costs $1.45 per liter. How much for 8 liters?"
        - 1.45 × 8 = $11.60
        """)

def generate_decimal_scenarios():
    """Generate diverse decimal word problem scenarios"""
    return {
        "addition": [
            # Food/Cooking
            {
                "template": "A chef bought {num1} kilograms of {item1} and {num2} kilograms of {item2}. How many kilograms of {category} did the chef buy in all?",
                "items": [
                    ("almonds", "pecans", "nuts"),
                    ("flour", "sugar", "ingredients"),
                    ("chicken", "beef", "meat"),
                    ("apples", "oranges", "fruit"),
                    ("potatoes", "carrots", "vegetables")
                ],
                "unit": "kilograms"
            },
            {
                "template": "{name} bought {num1} liters of milk on Monday and {num2} liters on Wednesday. How many liters of milk did {name} buy in total?",
                "names": ["Sarah", "Tom", "Maria", "Ahmed", "Lisa"],
                "unit": "liters"
            },
            
            # Distance/Travel
            {
                "template": "{name} jogged {num1} km in the morning and {num2} km in the evening. What was the total distance {name} jogged?",
                "names": ["Emma", "Carlos", "Priya", "James", "Sofia"],
                "unit": "kilometers"
            },
            {
                "template": "A delivery truck traveled {num1} miles to the first stop and {num2} miles to the second stop. What was the total distance traveled?",
                "unit": "miles"
            },
            
            # Money/Shopping
            {
                "template": "{name} spent ${num1} on groceries and ${num2} on gas. How much did {name} spend in total?",
                "names": ["Michael", "Ana", "David", "Rachel", "Kevin"],
                "unit": "dollars"
            },
            {
                "template": "A store sold {num1} meters of fabric in the morning and {num2} meters in the afternoon. How many meters were sold altogether?",
                "unit": "meters"
            },
            
            # Science/Measurement
            {
                "template": "A scientist mixed {num1} milliliters of solution A with {num2} milliliters of solution B. What is the total volume?",
                "unit": "milliliters"
            },
            {
                "template": "During an experiment, the temperature rose {num1}°C in the first hour and {num2}°C in the second hour. What was the total temperature increase?",
                "unit": "degrees"
            },
            
            # Construction/Building
            {
                "template": "A builder used {num1} cubic meters of concrete for the foundation and {num2} cubic meters for the walls. How much concrete was used in total?",
                "unit": "cubic meters"
            },
            
            # Time/Duration
            {
                "template": "{name} studied for {num1} hours on Saturday and {num2} hours on Sunday. How many hours did {name} study over the weekend?",
                "names": ["Alex", "Maya", "Jordan", "Emily", "Nathan"],
                "unit": "hours"
            }
        ],
        
        "subtraction": [
            # Construction/Crafts
            {
                "template": "A carpenter bought a piece of wood that was {num1} meters long. Then she sawed {num2} meters off the end. How long is the piece of wood now?",
                "unit": "meters"
            },
            {
                "template": "A roll of ribbon was {num1} meters long. After using {num2} meters for decorations, how much ribbon remains?",
                "unit": "meters"
            },
            
            # Food/Cooking
            {
                "template": "{name} had {num1} kilograms of flour. After baking, {num2} kilograms were used. How much flour is left?",
                "names": ["The bakery", "Mrs. Chen", "The restaurant", "Chef Marco", "Grandma"],
                "unit": "kilograms"
            },
            {
                "template": "A container held {num1} liters of juice. If {num2} liters were poured out, how much juice remains?",
                "unit": "liters"
            },
            
            # Money/Finance
            {
                "template": "{name} had ${num1} in savings. After buying a {item} for ${num2}, how much money is left?",
                "names": ["Sam", "Kelly", "Marcus", "Nina", "Diego"],
                "items": ["bicycle", "video game", "skateboard", "watch", "backpack"],
                "unit": "dollars"
            },
            
            # Distance/Travel
            {
                "template": "The distance from home to school is {num1} km. If {name} has already walked {num2} km, how much farther to go?",
                "names": ["Jamie", "Ali", "Taylor", "Chris", "Pat"],
                "unit": "kilometers"
            },
            
            # Weight/Mass
            {
                "template": "A bag of rice weighed {num1} kg. After using {num2} kg for dinner, how much rice is left?",
                "unit": "kilograms"
            },
            
            # Volume/Capacity
            {
                "template": "A swimming pool contains {num1} kiloliters of water. If {num2} kiloliters leaked out, how much water remains?",
                "unit": "kiloliters"
            },
            
            # Time
            {
                "template": "A movie is {num1} hours long. If {name} has watched {num2} hours, how much time is left?",
                "names": ["Leo", "Zoe", "Max", "Eva", "Ben"],
                "unit": "hours"
            },
            
            # Temperature
            {
                "template": "The temperature was {num1}°C. It dropped by {num2}°C overnight. What is the new temperature?",
                "unit": "degrees Celsius"
            }
        ],
        
        "multiplication": [
            # Rate × Time
            {
                "template": "{name} is using a stair-climbing machine set to {num1} flights of stairs per minute. How many flights will {name} climb in {num2} minutes?",
                "names": ["Sam", "Alex", "Jordan", "Casey", "Morgan"],
                "unit": "flights"
            },
            {
                "template": "A printer prints {num1} pages per minute. How many pages will it print in {num2} minutes?",
                "unit": "pages"
            },
            
            # Price × Quantity
            {
                "template": "Apples cost ${num1} per kilogram. How much will {num2} kilograms cost?",
                "unit": "dollars"
            },
            {
                "template": "Movie tickets cost ${num1} each. How much will {num2} tickets cost in total?",
                "unit": "dollars"
            },
            
            # Speed × Time
            {
                "template": "A cyclist rides at {num1} km per hour. How far will they travel in {num2} hours?",
                "unit": "kilometers"
            },
            {
                "template": "{name} walks at a speed of {num1} meters per minute. How far will {name} walk in {num2} minutes?",
                "names": ["Hannah", "Oliver", "Sophia", "Ethan", "Ava"],
                "unit": "meters"
            },
            
            # Consumption Rates
            {
                "template": "A car uses {num1} liters of fuel per kilometer. How much fuel is needed for a {num2} kilometer trip?",
                "unit": "liters"
            },
            {
                "template": "A factory produces {num1} items per hour. How many items will be produced in {num2} hours?",
                "unit": "items"
            },
            
            # Recipes/Portions
            {
                "template": "A recipe calls for {num1} cups of flour per batch. How much flour is needed for {num2} batches?",
                "unit": "cups"
            },
            {
                "template": "Each pizza requires {num1} kilograms of cheese. How much cheese is needed for {num2} pizzas?",
                "unit": "kilograms"
            },
            
            # Work/Labor
            {
                "template": "{name} earns ${num1} per hour. How much will {name} earn working {num2} hours?",
                "names": ["Lisa", "Ryan", "Mia", "Jake", "Emma"],
                "unit": "dollars"
            },
            
            # Science/Experiments
            {
                "template": "A plant grows {num1} centimeters per week. How much will it grow in {num2} weeks?",
                "unit": "centimeters"
            }
        ]
    }

def generate_new_decimal_word_problem():
    """Generate a new decimal word problem based on difficulty"""
    difficulty = st.session_state.decimal_word_difficulty
    scenarios = generate_decimal_scenarios()
    
    # Choose operation based on difficulty
    if difficulty == 1:
        operations = ["addition", "subtraction"]
        weights = [0.5, 0.5]
    elif difficulty == 2:
        operations = ["addition", "subtraction", "multiplication"]
        weights = [0.3, 0.3, 0.4]
    else:
        operations = ["addition", "subtraction", "multiplication"]
        weights = [0.3, 0.3, 0.4]
    
    operation = random.choices(operations, weights=weights)[0]
    scenario = random.choice(scenarios[operation])
    
    # Generate numbers based on operation and difficulty
    if operation == "addition":
        if difficulty == 1:
            num1 = round(random.uniform(0.1, 9.9), 1)
            num2 = round(random.uniform(0.1, 9.9), 1)
        elif difficulty == 2:
            num1 = round(random.uniform(1.0, 99.99), 2)
            num2 = round(random.uniform(0.1, 99.99), 2)
        elif difficulty == 3:
            num1 = round(random.uniform(10.0, 999.99), 2)
            num2 = round(random.uniform(1.0, 999.99), 2)
        elif difficulty == 4:
            num1 = round(random.uniform(10.01, 999.999), 3)
            num2 = round(random.uniform(10.01, 999.999), 3)
        else:
            num1 = round(random.uniform(100.0, 9999.99), 2)
            num2 = round(random.uniform(10.0, 9999.99), 2)
        answer = round(num1 + num2, 6)
        
    elif operation == "subtraction":
        if difficulty == 1:
            num1 = round(random.uniform(5.0, 20.0), 1)
            num2 = round(random.uniform(0.1, num1 - 0.1), 1)
        elif difficulty == 2:
            num1 = round(random.uniform(10.0, 99.99), 2)
            num2 = round(random.uniform(0.01, num1 - 0.01), 2)
        elif difficulty == 3:
            num1 = round(random.uniform(50.0, 999.99), 2)
            num2 = round(random.uniform(0.01, num1 - 1.0), 2)
        elif difficulty == 4:
            num1 = round(random.uniform(100.0, 999.999), 3)
            num2 = round(random.uniform(0.001, num1 - 10.0), 3)
        else:
            num1 = round(random.uniform(100.0, 9999.99), 2)
            num2 = round(random.uniform(1.0, num1 - 10.0), 2)
        answer = round(num1 - num2, 6)
        
    else:  # multiplication
        if difficulty <= 2:
            num1 = round(random.uniform(0.1, 9.9), 1)
            num2 = random.randint(2, 9)
        elif difficulty == 3:
            num1 = round(random.uniform(0.01, 99.99), 2)
            num2 = random.randint(2, 99)
        elif difficulty == 4:
            num1 = round(random.uniform(0.1, 99.9), 1)
            num2 = round(random.uniform(0.1, 9.9), 1)
        else:
            num1 = round(random.uniform(0.01, 999.99), 2)
            num2 = round(random.uniform(0.1, 99.9), 1)
        answer = round(num1 * num2, 6)
    
    # Build the problem text
    problem_text = scenario["template"]
    
    # Replace placeholders
    if "names" in scenario:
        name = random.choice(scenario["names"])
        problem_text = problem_text.replace("{name}", name)
    
    if "items" in scenario:
        item_set = random.choice(scenario["items"])
        problem_text = problem_text.replace("{item1}", item_set[0])
        problem_text = problem_text.replace("{item2}", item_set[1])
        problem_text = problem_text.replace("{category}", item_set[2])
    
    if "items" in scenario and isinstance(scenario["items"], list) and isinstance(scenario["items"][0], str):
        item = random.choice(scenario["items"])
        problem_text = problem_text.replace("{item}", item)
    
    # Format numbers nicely (remove trailing zeros)
    num1_str = f"{num1:.6f}".rstrip('0').rstrip('.')
    num2_str = f"{num2:.6f}".rstrip('0').rstrip('.')
    
    problem_text = problem_text.replace("{num1}", num1_str)
    problem_text = problem_text.replace("{num2}", num2_str)
    
    # Clean up answer
    answer = float(f"{answer:.6f}".rstrip('0').rstrip('.'))
    
    # Store problem data
    st.session_state.problem_data = {
        "operation": operation,
        "problem_text": problem_text,
        "num1": num1,
        "num2": num2,
        "unit": scenario["unit"]
    }
    st.session_state.correct_answer = answer
    st.session_state.current_problem = problem_text

def display_decimal_word_problem():
    """Display the current decimal word problem"""
    # Display the problem in a nice card
    st.markdown("""
    <div style="
        background-color: #e3f2fd;
        border: 2px solid #1976d2;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        font-size: 18px;
        line-height: 1.8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{st.session_state.current_problem}**")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show work area
    with st.expander("📝 **Scratch Pad** (Show your work)", expanded=False):
        data = st.session_state.problem_data
        operation = data["operation"]
        
        st.markdown("""
        **My work:**
        
        Numbers from the problem:
        - First number: _______
        - Second number: _______
        
        Operation to use: _______
        
        Calculation:
        """)
        
        if operation in ["addition", "subtraction"]:
            st.markdown("""
            ```
              _______
            ± _______
            ─────────
              _______
            ```
            """)
        else:
            st.markdown("""
            ```
            _______ × _______ = _______
            ```
            """)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_answer = st.number_input(
                "Your answer:",
                min_value=0.0,
                max_value=99999.999,
                step=0.001,
                format="%.3f",
                key="decimal_word_answer"
            )
        
        with col2:
            unit = st.session_state.problem_data["unit"]
            st.markdown(f"<div style='padding-top: 30px; font-size: 16px;'>{unit}</div>", 
                       unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", 
                                                 type="primary", 
                                                 use_container_width=True)
        
        if submit_button:
            # Clean up user answer
            cleaned_answer = float(f"{user_answer:.6f}".rstrip('0').rstrip('.'))
            st.session_state.user_answer = cleaned_answer
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
    
    # Check with small tolerance
    is_correct = abs(user_answer - correct_answer) < 0.001
    
    # Format for display
    correct_display = f"{correct_answer:.6f}".rstrip('0').rstrip('.')
    user_display = f"{user_answer:.6f}".rstrip('0').rstrip('.')
    
    if is_correct:
        st.success(f"🎉 **Excellent! {correct_display} {unit} is correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.decimal_word_difficulty
        st.session_state.decimal_word_difficulty = min(
            st.session_state.decimal_word_difficulty + 1, 5
        )
        
        if st.session_state.decimal_word_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decimal word problems!**")
        elif old_difficulty < st.session_state.decimal_word_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decimal_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_display} {unit}**")
        if abs(user_answer - correct_answer) > 0.001:
            st.error(f"You answered: {user_display} {unit}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.decimal_word_difficulty
        st.session_state.decimal_word_difficulty = max(
            st.session_state.decimal_word_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimal_word_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.decimal_word_difficulty}. Keep practicing!**")
        
        # Show solution
        show_word_problem_solution()

def show_word_problem_solution():
    """Show detailed solution for the word problem"""
    data = st.session_state.problem_data
    operation = data["operation"]
    num1 = data["num1"]
    num2 = data["num2"]
    answer = st.session_state.correct_answer
    unit = data["unit"]
    
    with st.expander("📖 **Solution Explained**", expanded=True):
        st.markdown("### Step-by-step solution:")
        
        # Step 1: Identify what we know
        st.markdown("**Step 1: What do we know?**")
        num1_display = f"{num1:.6f}".rstrip('0').rstrip('.')
        num2_display = f"{num2:.6f}".rstrip('0').rstrip('.')
        
        if operation == "addition":
            st.markdown(f"- First amount: {num1_display} {unit}")
            st.markdown(f"- Second amount: {num2_display} {unit}")
            st.markdown("- We need to find: the total")
            keyword = "altogether/in all"
            
        elif operation == "subtraction":
            st.markdown(f"- Starting amount: {num1_display} {unit}")
            st.markdown(f"- Amount removed: {num2_display} {unit}")
            st.markdown("- We need to find: what remains")
            keyword = "left/remaining"
            
        else:  # multiplication
            st.markdown(f"- Rate/Amount per unit: {num1_display}")
            st.markdown(f"- Number of units: {num2_display}")
            st.markdown("- We need to find: the total")
            keyword = "per/each"
        
        # Step 2: Choose operation
        st.markdown(f"\n**Step 2: Choose the operation**")
        st.markdown(f"Key word: **{keyword}** → {operation.capitalize()}")
        
        # Step 3: Set up the problem
        st.markdown(f"\n**Step 3: Set up the calculation**")
        if operation == "addition":
            st.markdown(f"{num1_display} + {num2_display} = ?")
        elif operation == "subtraction":
            st.markdown(f"{num1_display} - {num2_display} = ?")
        else:
            st.markdown(f"{num1_display} × {num2_display} = ?")
        
        # Step 4: Calculate
        st.markdown(f"\n**Step 4: Calculate**")
        
        if operation in ["addition", "subtraction"]:
            # Show vertical calculation
            st.markdown("```")
            st.markdown(f"  {num1_display}")
            st.markdown(f"{'+'if operation == 'addition' else '-'} {num2_display}")
            st.markdown(f"─────────")
            st.markdown(f"  {f'{answer:.6f}'.rstrip('0').rstrip('.')}")
            st.markdown("```")
            
        else:  # multiplication
            st.markdown(f"```")
            st.markdown(f"{num1_display} × {num2_display} = {f'{answer:.6f}'.rstrip('0').rstrip('.')}")
            st.markdown(f"```")
            
            # Show decimal place counting
            dec1 = len(str(num1).split('.')[-1]) if '.' in str(num1) else 0
            dec2 = len(str(num2).split('.')[-1]) if '.' in str(num2) else 0
            if dec1 > 0 or dec2 > 0:
                st.markdown(f"\n*Decimal places: {dec1} + {dec2} = {dec1 + dec2} total*")
        
        # Step 5: Answer
        answer_display = f"{answer:.6f}".rstrip('0').rstrip('.')
        st.markdown(f"\n**Step 5: Write the answer**")
        st.markdown(f"### Answer: {answer_display} {unit}")
        
        # Step 6: Check
        st.markdown(f"\n**Step 6: Does it make sense?**")
        if operation == "addition":
            st.markdown(f"✓ The sum is larger than both numbers")
        elif operation == "subtraction":
            st.markdown(f"✓ The difference is smaller than the starting amount")
        else:
            if num2 > 1:
                st.markdown(f"✓ The product is larger than the first number")
            else:
                st.markdown(f"✓ The product is smaller than the first number (multiplied by less than 1)")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer