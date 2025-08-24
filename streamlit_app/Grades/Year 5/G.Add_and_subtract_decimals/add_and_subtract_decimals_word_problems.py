import streamlit as st
import random
from decimal import Decimal

def run():
    """
    Main function to run the Add and Subtract Decimals Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/G. Add and subtract decimals/add_and_subtract_decimals_word_problems.py
    """
    # Initialize session state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > G. Add and subtract decimals**")
    st.title("📝 Add and Subtract Decimals: Word Problems")
    st.markdown("*Solve real-world problems involving decimal operations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Expert"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level - 1]}")
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level} of 4")
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
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
        ### How to Solve Word Problems:
        1. **Read carefully** - What is the problem asking?
        2. **Identify the operation** - Are you adding or subtracting?
        3. **Find the numbers** - Look for the decimal values
        4. **Calculate** - Line up decimal points!
        5. **Check your answer** - Does it make sense?
        
        ### Keywords to Look For:
        - **Addition words**: total, altogether, combined, sum, plus, more than, increased by
        - **Subtraction words**: difference, less than, fewer, minus, decreased by, how many more
        
        ### Tips:
        - **Estimate first** to check if your answer is reasonable
        - **Include units** in your answer (km, kg, points, etc.)
        - **Round appropriately** based on the context
        
        ### Difficulty Levels:
        - **🟢 Basic:** Simple one-step problems
        - **🟡 Intermediate:** More complex scenarios
        - **🟠 Advanced:** Multi-step problems
        - **🔴 Expert:** Challenging real-world applications
        """)

def generate_problem_scenario():
    """Generate different types of word problems"""
    scenarios = {
        'distance': {
            'units': ['kilometres', 'miles', 'metres'],
            'contexts': [
                "walked", "ran", "cycled", "drove", "jogged", "hiked", "travelled"
            ],
            'people': ["Alex", "Maria", "Sam", "Chen", "Priya", "Omar", "Emma", "Liam"]
        },
        'weight': {
            'units': ['kilograms', 'grams', 'pounds'],
            'items': [
                ('apples', 'oranges'), ('flour', 'sugar'), ('potatoes', 'onions'),
                ('cheese', 'butter'), ('almonds', 'pecans'), ('rice', 'pasta'),
                ('chicken', 'beef'), ('tomatoes', 'cucumbers')
            ],
            'contexts': ["bought", "sold", "used", "mixed", "packaged"]
        },
        'money': {
            'units': ['dollars', 'pounds', 'euros'],
            'contexts': [
                "spent", "saved", "earned", "received", "paid", "donated"
            ],
            'items': ["groceries", "books", "clothes", "games", "supplies", "tickets"]
        },
        'sports': {
            'units': ['points', 'seconds', 'metres'],
            'sports': [
                "basketball", "swimming", "running", "surfing", "gymnastics",
                "skating", "tennis", "golf"
            ],
            'contexts': ["scored", "completed", "achieved", "recorded"]
        },
        'measurement': {
            'units': ['litres', 'millilitres', 'gallons'],
            'contexts': [
                "filled", "poured", "mixed", "used", "added", "removed"
            ],
            'items': ["water", "juice", "milk", "paint", "fuel", "oil"]
        },
        'temperature': {
            'units': ['degrees Celsius', 'degrees Fahrenheit'],
            'contexts': ["rose", "fell", "changed", "increased", "decreased"],
            'times': ["morning", "afternoon", "evening", "night"]
        }
    }
    
    return scenarios

def generate_new_question():
    """Generate a new word problem based on difficulty"""
    level = st.session_state.word_problem_difficulty
    scenarios = generate_problem_scenario()
    
    # Choose scenario type
    scenario_type = random.choice(list(scenarios.keys()))
    scenario = scenarios[scenario_type]
    
    # Generate numbers based on difficulty
    if level == 1:  # Basic - one decimal place
        if random.choice(['add', 'subtract']) == 'add':
            num1 = round(random.uniform(1.0, 20.0), 1)
            num2 = round(random.uniform(1.0, 20.0), 1)
            operation = 'add'
        else:
            num1 = round(random.uniform(10.0, 30.0), 1)
            num2 = round(random.uniform(1.0, num1 - 0.1), 1)
            operation = 'subtract'
    
    elif level == 2:  # Intermediate - two decimal places
        if random.choice(['add', 'subtract']) == 'add':
            num1 = round(random.uniform(0.01, 50.00), 2)
            num2 = round(random.uniform(0.01, 50.00), 2)
            operation = 'add'
        else:
            num1 = round(random.uniform(20.00, 99.99), 2)
            num2 = round(random.uniform(0.01, num1 - 0.01), 2)
            operation = 'subtract'
    
    elif level == 3:  # Advanced - mixed operations
        if random.choice(['add', 'subtract']) == 'add':
            num1 = round(random.uniform(0.1, 100.0), random.choice([1, 2]))
            num2 = round(random.uniform(0.1, 100.0), random.choice([1, 2]))
            operation = 'add'
        else:
            num1 = round(random.uniform(50.0, 200.0), random.choice([1, 2]))
            num2 = round(random.uniform(0.1, num1 - 0.1), random.choice([1, 2]))
            operation = 'subtract'
    
    else:  # Expert - complex scenarios
        if random.choice(['add', 'subtract', 'multi']) == 'multi':
            # Multi-step problem
            num1 = round(random.uniform(10.0, 100.0), 2)
            num2 = round(random.uniform(10.0, 100.0), 2)
            num3 = round(random.uniform(10.0, 100.0), 2)
            operation = 'multi'
        else:
            num1 = round(random.uniform(100.0, 999.0), 2)
            num2 = round(random.uniform(10.0, num1 - 0.1), 2)
            operation = random.choice(['add', 'subtract'])
    
    # Generate problem text based on scenario
    problem_text = generate_problem_text(scenario_type, scenario, num1, num2, 
                                       operation, level)
    
    # Calculate answer
    if operation == 'add':
        answer = float(Decimal(str(num1)) + Decimal(str(num2)))
    elif operation == 'subtract':
        answer = float(Decimal(str(num1)) - Decimal(str(num2)))
    else:  # multi-step
        # For simplicity, let's do add then subtract
        temp = float(Decimal(str(num1)) + Decimal(str(num2)))
        answer = float(Decimal(str(temp)) - Decimal(str(num3)))
        problem_text = generate_multi_step_problem(scenario_type, scenario, 
                                                 num1, num2, num3)
    
    st.session_state.question_data = {
        'problem_text': problem_text,
        'answer': round(answer, 2),
        'unit': scenario['units'][0] if 'units' in scenario else '',
        'operation': operation
    }
    st.session_state.correct_answer = round(answer, 2)
    st.session_state.current_question = problem_text

def generate_problem_text(scenario_type, scenario, num1, num2, operation, level):
    """Generate the actual problem text"""
    
    if scenario_type == 'distance':
        person = random.choice(scenario['people'])
        unit = random.choice(scenario['units'])
        context = random.choice(scenario['contexts'])
        
        if operation == 'add':
            templates = [
                f"{person} {context} {num1} {unit} in the morning and {num2} {unit} in the afternoon. How far did {person} travel in total?",
                f"On Monday, {person} {context} {num1} {unit}. On Tuesday, {person} {context} {num2} {unit}. What was the total distance?",
                f"{person} {context} {num1} {unit} to school and {num2} {unit} back home. How many {unit} did {person} travel altogether?"
            ]
        else:
            templates = [
                f"On Monday, {person} {context} {num1} {unit}. On Tuesday, {'he' if person in ['Alex', 'Chen', 'Omar', 'Liam'] else 'she'} {context} {num2} {unit} less than on Monday. How far did {person} {context} on Tuesday?",
                f"{person} planned to {context[:-1]} {num1} {unit} but only managed {num2} {unit} less. How far did {person} actually {context[:-1]}?",
                f"Last week, {person} {context} {num1} {unit}. This week, {person} {context} {num2} {unit} fewer. How far did {person} {context[:-1]} this week?"
            ]
    
    elif scenario_type == 'weight':
        items = random.choice(scenario['items'])
        unit = random.choice(scenario['units'])
        context = random.choice(scenario['contexts'])
        
        if operation == 'add':
            templates = [
                f"A chef {context} {num1} {unit} of {items[0]} and {num2} {unit} of {items[1]}. How many {unit} of ingredients did the chef buy in all?",
                f"A store {context} {num1} {unit} of {items[0]} in the morning and {num2} {unit} more in the afternoon. What is the total weight {context}?",
                f"A recipe needs {num1} {unit} of {items[0]} and {num2} {unit} of {items[1]}. How many {unit} of ingredients are needed in total?"
            ]
        else:
            templates = [
                f"A bag contained {num1} {unit} of {items[0]}. After using {num2} {unit}, how many {unit} remained?",
                f"A shop had {num1} {unit} of {items[0]}. They sold {num2} {unit}. How many {unit} are left?",
                f"A container holds {num1} {unit} of {items[0]}. If {num2} {unit} were removed, how much remains?"
            ]
    
    elif scenario_type == 'money':
        person = random.choice(scenario['people'] if 'people' in scenario else ['Alex', 'Maria', 'Sam'])
        unit = random.choice(scenario['units'])
        context = random.choice(scenario['contexts'])
        item = random.choice(scenario['items'])
        
        if operation == 'add':
            templates = [
                f"{person} {context} {num1} {unit} on {item} and {num2} {unit} on lunch. How much did {person} spend in total?",
                f"{person} saved {num1} {unit} in January and {num2} {unit} in February. How much did {person} save altogether?",
                f"{person} earned {num1} {unit} on Monday and {num2} {unit} on Tuesday. What were the total earnings?"
            ]
        else:
            templates = [
                f"{person} had {num1} {unit} and {context} {num2} {unit} on {item}. How much money does {person} have left?",
                f"{person} earned {num1} {unit} but had to pay {num2} {unit} in expenses. How much does {person} have remaining?",
                f"After receiving {num1} {unit}, {person} {context} {num2} {unit}. How much money remains?"
            ]
    
    elif scenario_type == 'sports':
        sport = random.choice(scenario['sports'])
        unit = random.choice(scenario['units'])
        person = random.choice(['Alex', 'Maria', 'Sam', 'Chen', 'Priya', 'Omar'])
        
        if operation == 'add':
            templates = [
                f"{person} scored {num1} {unit} in the first round and {num2} {unit} in the second round of a {sport} competition. What was the total score?",
                f"In a {sport} match, {person} earned {num1} {unit} in the first half and {num2} {unit} in the second half. How many {unit} in total?",
                f"{person} entered a {sport} competition. In the first round, {'he' if person in ['Alex', 'Chen', 'Omar'] else 'she'} scored {num1} {unit}. Later in the day, {'he' if person in ['Alex', 'Chen', 'Omar'] else 'she'} scored {num2} {unit} in the second round. How many total {unit} did {person} score?"
            ]
        else:
            templates = [
                f"{person}'s best {sport} score was {num1} {unit}. Today's score was {num2} {unit} less. What was today's score?",
                f"In {sport}, {person} scored {num1} {unit} last week but {num2} {unit} fewer this week. What was this week's score?",
                f"{person} needs {num1} {unit} to win the {sport} competition but is {num2} {unit} short. How many {unit} does {person} have?"
            ]
    
    elif scenario_type == 'measurement':
        item = random.choice(scenario['items'])
        unit = random.choice(scenario['units'])
        context = random.choice(scenario['contexts'])
        
        if operation == 'add':
            templates = [
                f"A container had {num1} {unit} of {item}. Then {num2} {unit} more were {context}. How many {unit} are there now?",
                f"A recipe {context} {num1} {unit} of {item} and then {num2} {unit} more. What is the total amount?",
                f"Two bottles contain {num1} {unit} and {num2} {unit} of {item} respectively. What is the combined volume?"
            ]
        else:
            templates = [
                f"A tank contained {num1} {unit} of {item}. After {num2} {unit} were {context}, how much remained?",
                f"From {num1} {unit} of {item}, {num2} {unit} were used. How many {unit} are left?",
                f"A bottle had {num1} {unit} of {item}. If {num2} {unit} were poured out, how much remains?"
            ]
    
    elif scenario_type == 'temperature':
        unit = random.choice(scenario['units'])
        time1 = random.choice(scenario['times'])
        time2 = random.choice([t for t in scenario['times'] if t != time1])
        
        if operation == 'add':
            templates = [
                f"The temperature in the {time1} was {num1} {unit}. It rose by {num2} degrees. What is the new temperature?",
                f"The {time1} temperature was {num1} {unit} and increased by {num2} degrees by {time2}. What was the {time2} temperature?",
                f"Starting at {num1} {unit}, the temperature increased by {num2} degrees. What is the final temperature?"
            ]
        else:
            templates = [
                f"The temperature was {num1} {unit} in the {time1} but fell by {num2} degrees by {time2}. What was the {time2} temperature?",
                f"From a high of {num1} {unit}, the temperature dropped {num2} degrees. What is the current temperature?",
                f"The {time1} temperature was {num1} {unit}. By {time2}, it had decreased by {num2} degrees. What was the temperature in the {time2}?"
            ]
    
    return random.choice(templates)

def generate_multi_step_problem(scenario_type, scenario, num1, num2, num3):
    """Generate multi-step problems for expert level"""
    if scenario_type == 'distance':
        person = random.choice(scenario['people'])
        unit = random.choice(scenario['units'])
        templates = [
            f"{person} walked {num1} {unit} to the store, then {num2} {unit} to the park. On the way home, {person} took a shortcut that was {num3} {unit} less than the total distance traveled. How far was the trip home?"
        ]
    elif scenario_type == 'money':
        person = random.choice(['Alex', 'Maria', 'Sam'])
        unit = random.choice(scenario['units'])
        templates = [
            f"{person} had {num1} {unit} in savings. {person} earned {num2} {unit} from work, then spent {num3} {unit} on bills. How much money does {person} have now?"
        ]
    else:
        # Default multi-step
        templates = [
            f"A container started with {num1} litres. {num2} litres were added, then {num3} litres were removed. How many litres remain?"
        ]
    
    return random.choice(templates)

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the word problem
    st.markdown("### 📝 Problem:")
    st.markdown(f"**{data['problem_text']}**")
    
    # Answer input area
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input field with unit label
        user_input = st.text_input(
            "Your answer:",
            key="answer_input",
            placeholder="Enter your answer",
            label_visibility="collapsed"
        )
        
        # Display unit
        if data['unit']:
            st.markdown(f"**Unit:** {data['unit']}")
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            if user_input:
                try:
                    user_answer = float(user_input.strip())
                    st.session_state.user_answer = user_answer
                    st.session_state.show_feedback = True
                    st.session_state.answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("Please enter a valid number!")
            else:
                st.warning("Please enter your answer!")
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    # Check if answer is correct (with small tolerance)
    if abs(user_answer - correct_answer) < 0.01:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the complete answer with unit
        if data['unit']:
            st.info(f"**Answer:** {correct_answer} {data['unit']}")
        
        # Increase difficulty
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = min(
            st.session_state.word_problem_difficulty + 1, 4
        )
        
        if st.session_state.word_problem_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered decimal word problems!**")
        elif old_difficulty < st.session_state.word_problem_difficulty:
            st.info(f"⬆️ **Level up! Moving to {['', 'Basic', 'Intermediate', 'Advanced', 'Expert'][st.session_state.word_problem_difficulty]} problems**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        st.markdown(f"**Your answer:** {user_answer} {data['unit'] if data['unit'] else ''}")
        st.markdown(f"**Correct answer:** {correct_answer} {data['unit'] if data['unit'] else ''}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.word_problem_difficulty
        st.session_state.word_problem_difficulty = max(
            st.session_state.word_problem_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.word_problem_difficulty:
            st.warning(f"⬇️ **Level adjusted. Keep practicing!**")
        
        # Show solution
        show_solution()

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown("### How to solve this problem:")
        
        # Extract numbers from the problem
        st.markdown("**Step 1: Identify the important information**")
        st.markdown(f"- Look for the numbers and what operation to use")
        st.markdown(f"- Operation: {data['operation'].capitalize()}")
        
        st.markdown("**Step 2: Set up the calculation**")
        if data['operation'] == 'add':
            st.markdown("- We need to ADD the numbers")
            st.markdown("- Line up the decimal points")
        elif data['operation'] == 'subtract':
            st.markdown("- We need to SUBTRACT the numbers")
            st.markdown("- Line up the decimal points")
        else:
            st.markdown("- This is a multi-step problem")
            st.markdown("- Work through each step carefully")
        
        st.markdown("**Step 3: Calculate**")
        st.markdown(f"**Answer:** {data['answer']} {data['unit'] if data['unit'] else ''}")
        
        st.markdown("**Step 4: Check**")
        st.markdown("- Does the answer make sense?")
        st.markdown("- Did you include the correct unit?")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""