import streamlit as st
import random

def run():
    """
    Main function to run the Word problems with extra or missing information activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/word_problems_with_extra_or_missing_information.py
    """
    # Initialize session state
    if "extra_missing_difficulty" not in st.session_state:
        st.session_state.extra_missing_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🔍 Word Problems with Extra or Missing Information")
    st.markdown("*Identify what information you need to solve problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.extra_missing_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Complex", "Master"]
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
        generate_new_extra_missing_problem()
    
    # Display current problem
    display_extra_missing_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Identify Extra or Missing Information**", expanded=False):
        st.markdown("""
        ### Types of Word Problems:
        
        **1. Problems with EXTRA Information** 🎯
        - Contains numbers or facts you don't need
        - Read carefully to find what's actually asked
        - Cross out information that doesn't help
        
        **2. Problems with MISSING Information** ❓
        - Doesn't have all the numbers needed
        - Can't be solved without more facts
        - Need to identify what's missing
        
        **3. Problems with JUST RIGHT Information** ✅
        - Has exactly what you need
        - No extra, no missing
        - Can be solved completely
        
        ### How to Analyze Problems:
        
        **Step 1: What is being asked?**
        - Underline the question
        - Identify what you need to find
        
        **Step 2: What information is given?**
        - List all numbers and facts
        - Circle the important ones
        
        **Step 3: What do you need?**
        - Think about the calculation
        - What numbers are required?
        
        **Step 4: Compare given vs. needed**
        - Extra: More than needed
        - Missing: Less than needed
        - Just right: Exactly what's needed
        
        ### Examples:
        
        **Extra Information:**
        "Tom has 5 red marbles and 3 blue marbles. His sister is 8 years old. How many marbles does Tom have?"
        - Sister's age is EXTRA (not needed)
        
        **Missing Information:**
        "Sarah bought some apples for $2 each. How much did she spend?"
        - Number of apples is MISSING
        
        **Just Right:**
        "Mike has 4 boxes with 6 cookies each. How many cookies total?"
        - Has everything needed: 4 × 6 = 24
        """)

def generate_problem_scenarios():
    """Generate diverse scenarios for extra/missing information problems"""
    return {
        "school_supplies": [
            {
                "type": "extra",
                "problem": "{teacher} is organizing supplies for the art class. She has {pencils} colored pencils, {markers} markers, and {erasers} erasers. Each student needs {need_per} colored pencils. Her classroom has {desks} desks. If there are {students} students, how many colored pencils will {teacher} have left?",
                "variables": {
                    "teacher": ["Ms. Johnson", "Mrs. Smith", "Mr. Davis"],
                    "pencils": [120, 150, 180, 200],
                    "markers": [50, 75, 100],  # EXTRA
                    "erasers": [30, 40, 50],   # EXTRA
                    "desks": [25, 30, 35],     # EXTRA
                    "need_per": [5, 6, 8],
                    "students": [20, 24, 25]
                },
                "solution": "pencils - (students × need_per)",
                "extra_info": ["markers", "erasers", "desks"]
            },
            {
                "type": "missing",
                "problem": "{student} is buying supplies for school. Notebooks cost ${notebook_price} each and pens cost ${pen_price} each. {student} bought {notebooks} notebooks. How much did {student} spend in total?",
                "variables": {
                    "student": ["Emma", "Liam", "Olivia", "Noah"],
                    "notebook_price": [3, 4, 5],
                    "pen_price": [1, 2],
                    "notebooks": [4, 5, 6]
                },
                "missing": "number of pens"
            },
            {
                "type": "solvable",
                "problem": "{name} needs folders for school. Folders come in packs of {per_pack}. If {name} buys {packs} packs, how many folders will {pronoun} have?",
                "variables": {
                    "name": ["Alex", "Jordan", "Sam"],
                    "pronoun": ["they", "they", "they"],
                    "per_pack": [4, 5, 6, 8],
                    "packs": [3, 4, 5, 6]
                },
                "solution": "packs × per_pack"
            }
        ],
        
        "food_service": [
            {
                "type": "extra",
                "problem": "{restaurant} sold {burgers} hamburgers and {hotdogs} hot dogs on Friday. On Saturday, they sold {saturday_burgers} hamburgers. Each hamburger costs ${burger_price}. The restaurant is open {hours} hours per day. How many hamburgers did they sell in total?",
                "variables": {
                    "restaurant": ["Joe's Diner", "City Grill", "Main Street Cafe"],
                    "burgers": [45, 58, 67, 72],
                    "hotdogs": [32, 41, 55],  # EXTRA
                    "saturday_burgers": [51, 63, 78, 84],
                    "burger_price": [8, 10, 12],  # EXTRA
                    "hours": [10, 12, 14]  # EXTRA
                },
                "solution": "burgers + saturday_burgers",
                "extra_info": ["hotdogs", "burger_price", "hours"]
            },
            {
                "type": "missing",
                "problem": "The school cafeteria serves pizza slices. Each student can have {slices_per} slices. Yesterday they served {students} students. How many pizzas did they use?",
                "variables": {
                    "slices_per": [2, 3],
                    "students": [120, 150, 180]
                },
                "missing": "slices per pizza"
            },
            {
                "type": "solvable",
                "problem": "{bakery} baked {trays} trays of cookies. Each tray has {per_tray} cookies. If they sell all the cookies in boxes of {per_box}, how many boxes will they need?",
                "variables": {
                    "bakery": ["Sweet Dreams Bakery", "Corner Bakehouse", "Main Street Bakery"],
                    "trays": [8, 10, 12],
                    "per_tray": [24, 30, 36],
                    "per_box": [6, 8, 12]
                },
                "solution": "(trays × per_tray) ÷ per_box"
            }
        ],
        
        "transportation": [
            {
                "type": "extra",
                "problem": "A train has {cars} cars. Each car has {seats} seats. The train left at {time} and travels at {speed} mph. On Tuesday, {passengers} passengers rode the train. How many empty seats were there?",
                "variables": {
                    "cars": [8, 10, 12],
                    "seats": [50, 60, 72],
                    "time": ["8:30 AM", "9:15 AM", "10:00 AM"],  # EXTRA
                    "speed": [45, 55, 65],  # EXTRA
                    "passengers": [285, 342, 456, 520]
                },
                "solution": "(cars × seats) - passengers",
                "extra_info": ["time", "speed"]
            },
            {
                "type": "missing",
                "problem": "{name} is planning a road trip. The destination is {distance} miles away. Gas costs ${gas_price} per gallon. How much will {name} spend on gas for the round trip?",
                "variables": {
                    "name": ["Carlos", "Maria", "James"],
                    "distance": [120, 180, 240],
                    "gas_price": [3.50, 4.00, 4.25]
                },
                "missing": "miles per gallon"
            },
            {
                "type": "solvable",
                "problem": "A parking garage has {floors} floors. Each floor has {spaces} parking spaces. If {taken} spaces are currently taken, how many spaces are available?",
                "variables": {
                    "floors": [4, 5, 6, 8],
                    "spaces": [75, 80, 100, 120],
                    "taken": [234, 287, 345, 412]
                },
                "solution": "(floors × spaces) - taken"
            }
        ],
        
        "shopping": [
            {
                "type": "extra",
                "problem": "{name} went shopping for a party. {pronoun_cap} bought {pizzas} pizzas at ${pizza_price} each and {sodas} bottles of soda at ${soda_price} each. The store is {distance} miles from home. {pronoun_cap} has ${money} in total. How much did {pronoun} spend?",
                "variables": {
                    "name": ["Sarah", "Mike", "Jennifer"],
                    "pronoun": ["she", "he", "she"],
                    "pronoun_cap": ["She", "He", "She"],
                    "pizzas": [4, 5, 6, 8],
                    "pizza_price": [12, 15, 18],
                    "sodas": [6, 8, 10, 12],
                    "soda_price": [2, 3, 4],
                    "distance": [3, 5, 8],  # EXTRA
                    "money": [100, 150, 200]  # EXTRA
                },
                "solution": "(pizzas × pizza_price) + (sodas × soda_price)",
                "extra_info": ["distance", "money"]
            },
            {
                "type": "missing",
                "problem": "{store} is having a sale. Shirts are ${shirt_price} each and {name} bought some shirts and {pants} pairs of pants. {name} spent ${total} in total. How many shirts did {pronoun} buy?",
                "variables": {
                    "store": ["Fashion Plus", "Trend Setters", "Style Shop"],
                    "name": ["David", "Lisa", "Kevin"],
                    "pronoun": ["he", "she", "he"],
                    "shirt_price": [15, 20, 25],
                    "pants": [2, 3, 4],
                    "total": [120, 150, 180]
                },
                "missing": "price per pants"
            },
            {
                "type": "solvable",
                "problem": "{name} is buying {type} for a gift. Each roll has {length} meters. If {name} buys {rolls_1} rolls of {color1} and {rolls_2} rolls of {color2}, how many meters of {type} will {pronoun} have in total?",
                "variables": {
                    "name": ["Emma", "Jack", "Sophia"],
                    "pronoun": ["she", "he", "she"],
                    "type": ["ribbon", "gift wrap", "fabric"],
                    "length": [10, 12, 15, 16, 20],
                    "rolls_1": [8, 10, 12, 13, 15],
                    "color1": ["red", "blue", "gold"],
                    "rolls_2": [12, 15, 18, 19, 20],
                    "color2": ["silver", "green", "purple"]
                },
                "solution": "(rolls_1 + rolls_2) × length"
            }
        ],
        
        "collections": [
            {
                "type": "extra",
                "problem": "{name} collects {items}. On Monday, {pronoun} had {monday} {items}. {pronoun_cap} bought {bought} more on Tuesday and {received} more on Wednesday. {pronoun_cap_2} sister is {age} years old. {pronoun_cap} friend gave {pronoun_obj} {friend_gave} {items} on Thursday. How many {items} does {name} have now?",
                "variables": {
                    "name": ["Tom", "Amy", "Ben"],
                    "pronoun": ["he", "she", "he"],
                    "pronoun_cap": ["He", "She", "He"],
                    "pronoun_cap_2": ["His", "Her", "His"],
                    "pronoun_obj": ["him", "her", "him"],
                    "items": ["stamps", "coins", "cards"],
                    "monday": [45, 67, 89],
                    "bought": [12, 18, 24],
                    "received": [8, 15, 20],
                    "age": [10, 12, 14],  # EXTRA
                    "friend_gave": [10, 15, 22]
                },
                "solution": "monday + bought + received + friend_gave",
                "extra_info": ["age"]
            },
            {
                "type": "missing",
                "problem": "{name} has {color1} pencils, {color2_more} more {color2} pencils than {color1} pencils, and {color3_more} more {color3} pencils than {color2} pencils. {pronoun_cap} has {brown} brown pencils. How many pencils does {name} have in all?",
                "variables": {
                    "name": ["Laura", "Mark", "Nina"],
                    "pronoun_cap": ["She", "He", "She"],
                    "color1": ["purple", "blue", "green"],
                    "color2": ["red", "yellow", "orange"],
                    "color3": ["black", "white", "pink"],
                    "color2_more": [4, 6, 8],
                    "color3_more": [12, 15, 17],
                    "brown": [19, 24, 28]
                },
                "missing": "number of color1 pencils"
            },
            {
                "type": "solvable",
                "problem": "{name}'s class is collecting {items} for charity. {name} brought {amount1} {items}, {friend1} brought {amount2} {items}, and {friend2} brought {amount3} {items}. How many {items} did they collect together?",
                "variables": {
                    "name": ["Oliver", "Emma", "Lucas"],
                    "friend1": ["Maya", "Ethan", "Ava"],
                    "friend2": ["Noah", "Mia", "Liam"],
                    "items": ["canned goods", "books", "toys"],
                    "amount1": [24, 32, 45],
                    "amount2": [18, 28, 36],
                    "amount3": [21, 25, 40]
                },
                "solution": "amount1 + amount2 + amount3"
            }
        ],
        
        "time_distance": [
            {
                "type": "extra",
                "problem": "{person} practices {activity} for {daily} minutes each day. There are {days} days in a week. {person}'s coach is {age} years old and has been coaching for {years} years. How many minutes does {person} practice in {weeks} weeks?",
                "variables": {
                    "person": ["Rachel", "Daniel", "Grace"],
                    "activity": ["piano", "violin", "drums"],
                    "daily": [30, 45, 60],
                    "days": [7],  # Included but obvious
                    "age": [35, 42, 48],  # EXTRA
                    "years": [10, 15, 20],  # EXTRA
                    "weeks": [4, 6, 8]
                },
                "solution": "daily × 7 × weeks",
                "extra_info": ["age", "years"]
            },
            {
                "type": "missing",
                "problem": "{name} took the train from {city1} to {city2} by way of {city3} and {city4}. The train traveled for {time} minutes at {city3}. It was {distance} kilometers from {city4} to {city2}. How many kilometers was {name}'s train ride?",
                "variables": {
                    "name": ["Albert", "Betty", "Charles"],
                    "city1": ["Walnut City", "Oak Town", "Pine Village"],
                    "city2": ["Almondburg", "Cashewville", "Pecantown"],
                    "city3": ["Peanut Village", "Hazelnut Harbor", "Pistachio Point"],
                    "city4": ["Pecan Harbour", "Macadamia Marina", "Brazil Bay"],
                    "time": [8, 12, 15],
                    "distance": [12, 15, 18]
                },
                "missing": "distances between other cities"
            }
        ],
        
        "production": [
            {
                "type": "extra",
                "problem": "A factory makes {product}. They produce {morning} units in the morning shift and {afternoon} units in the afternoon shift. The factory has {workers} workers and {machines} machines. Each unit sells for ${price}. How many units do they make per day?",
                "variables": {
                    "product": ["widgets", "gadgets", "devices"],
                    "morning": [234, 345, 456],
                    "afternoon": [312, 425, 538],
                    "workers": [25, 30, 40],  # EXTRA
                    "machines": [8, 10, 12],  # EXTRA
                    "price": [15, 20, 25]  # EXTRA
                },
                "solution": "morning + afternoon",
                "extra_info": ["workers", "machines", "price"]
            },
            {
                "type": "missing",
                "problem": "A bakery makes {product} in batches. Yesterday they made {batches} batches. Each batch makes enough to fill {boxes} boxes. How many individual {product} did they make?",
                "variables": {
                    "product": ["cupcakes", "cookies", "muffins"],
                    "batches": [12, 15, 18],
                    "boxes": [8, 10, 12]
                },
                "missing": "items per box"
            },
            {
                "type": "solvable",
                "problem": "{company} produces {items} daily. On Monday they made {monday}, Tuesday they made {tuesday}, and Wednesday they made {wednesday}. What was their total production for these three days?",
                "variables": {
                    "company": ["TechCo", "BuildIt Inc", "MakersHub"],
                    "items": ["phones", "tablets", "laptops"],
                    "monday": [845, 923, 1050],
                    "tuesday": [892, 967, 1123],
                    "wednesday": [901, 1001, 1089]
                },
                "solution": "monday + tuesday + wednesday"
            }
        ]
    }

def generate_new_extra_missing_problem():
    """Generate a new problem with extra or missing information"""
    difficulty = st.session_state.extra_missing_difficulty
    scenarios = generate_problem_scenarios()
    
    # Choose scenario types based on difficulty
    if difficulty == 1:
        scenario_types = ["school_supplies", "food_service", "collections"]
        problem_types = ["extra", "solvable"]  # Start with easier types
    elif difficulty == 2:
        scenario_types = ["shopping", "transportation", "collections"]
        problem_types = ["extra", "missing", "solvable"]
    elif difficulty == 3:
        scenario_types = ["shopping", "time_distance", "production"]
        problem_types = ["extra", "missing", "solvable"]
    elif difficulty == 4:
        scenario_types = ["time_distance", "production", "transportation"]
        problem_types = ["extra", "missing", "solvable"]
    else:  # difficulty == 5
        scenario_types = list(scenarios.keys())
        problem_types = ["extra", "missing", "solvable"]
    
    # Select random scenario and problem
    scenario_type = random.choice(scenario_types)
    available_problems = [p for p in scenarios[scenario_type] if p["type"] in problem_types]
    problem_template = random.choice(available_problems)
    
    # Generate the problem text
    problem_text = problem_template["problem"]
    problem_type = problem_template["type"]
    
    # Replace variables
    variable_values = {}
    for var_name, var_options in problem_template["variables"].items():
        value = random.choice(var_options)
        variable_values[var_name] = value
        problem_text = problem_text.replace(f"{{{var_name}}}", str(value))
    
    # Calculate answer options based on problem type
    if problem_type == "solvable":
        # Calculate the actual answer
        solution = problem_template["solution"]
        # Replace variable names with values for calculation
        calc_expr = solution
        for var, val in variable_values.items():
            calc_expr = calc_expr.replace(var, str(val))
        
        try:
            correct_answer = eval(calc_expr)
            # Generate plausible wrong answers
            wrong_answers = []
            
            # Common mistakes
            if "×" in solution or "*" in solution:
                # Addition instead of multiplication
                parts = [variable_values[v] for v in variable_values if isinstance(variable_values[v], (int, float))]
                if len(parts) >= 2:
                    wrong_answers.append(sum(parts[:2]))
            
            # Off by factor of 10
            wrong_answers.append(correct_answer // 10 if correct_answer >= 10 else correct_answer * 10)
            
            # Random close values
            wrong_answers.append(correct_answer + random.randint(5, 20))
            wrong_answers.append(abs(correct_answer - random.randint(5, 20)))
            
            # Remove duplicates and correct answer
            wrong_answers = list(set([int(w) for w in wrong_answers if w != correct_answer and w > 0]))[:3]
            
            # Ensure we have 3 wrong answers
            while len(wrong_answers) < 3:
                offset = random.randint(10, 50)
                new_wrong = correct_answer + (offset if random.choice([True, False]) else -offset)
                if new_wrong > 0 and new_wrong != correct_answer and new_wrong not in wrong_answers:
                    wrong_answers.append(int(new_wrong))
            
            answer_options = [int(correct_answer)] + wrong_answers[:3]
            random.shuffle(answer_options)
            
        except:
            # Fallback if calculation fails
            correct_answer = None
            answer_options = []
    
    else:
        correct_answer = None
        answer_options = []
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "problem_type": problem_type,
        "scenario_type": scenario_type,
        "correct_answer": correct_answer,
        "answer_options": answer_options,
        "extra_info": problem_template.get("extra_info", []),
        "missing_info": problem_template.get("missing", ""),
        "variable_values": variable_values
    }
    st.session_state.current_problem = problem_text

def display_extra_missing_problem():
    """Display the current problem with extra or missing information"""
    problem_data = st.session_state.problem_data
    
    # Display problem
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 25px;
        font-size: 18px;
        line-height: 1.8;
    ">
        {problem_data['problem_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display answer options based on problem type
    problem_type = problem_data['problem_type']
    
    if problem_type == "solvable" and problem_data['answer_options']:
        # Show multiple choice answers
        st.markdown("### Choose your answer:")
        
        cols = st.columns(2)
        for i, option in enumerate(problem_data['answer_options']):
            with cols[i % 2]:
                if st.button(
                    str(option), 
                    key=f"answer_{i}",
                    use_container_width=True,
                    disabled=st.session_state.answer_submitted
                ):
                    handle_answer(option)
        
        # Add the "not enough information" option
        st.markdown("")
        if st.button(
            "There is not enough information to solve this problem.",
            key="missing_info_btn",
            use_container_width=True,
            type="secondary",
            disabled=st.session_state.answer_submitted
        ):
            handle_answer("missing")
    
    else:
        # For extra or missing info problems, just show the special button
        st.markdown("### Can you solve this problem?")
        
        # Generate some plausible but incorrect answers
        if problem_type == "extra":
            # For extra info problems, show options plus the correct "solvable" option
            fake_answers = generate_fake_answers(problem_data)
            
            cols = st.columns(2)
            for i, option in enumerate(fake_answers):
                with cols[i % 2]:
                    if st.button(
                        str(option), 
                        key=f"answer_{i}",
                        use_container_width=True,
                        disabled=st.session_state.answer_submitted
                    ):
                        handle_answer(option)
        
        elif problem_type == "missing":
            # For missing info problems, show fake answers
            fake_answers = generate_fake_answers(problem_data)
            
            cols = st.columns(2)
            for i, option in enumerate(fake_answers[:3]):
                with cols[i % 2]:
                    if st.button(
                        str(option), 
                        key=f"answer_{i}",
                        use_container_width=True,
                        disabled=st.session_state.answer_submitted
                    ):
                        handle_answer(option)
        
        # Always show the "not enough information" button for missing info problems
        st.markdown("")
        if st.button(
            "There is not enough information to solve this problem.",
            key="missing_info_btn",
            use_container_width=True,
            type="secondary" if problem_type != "missing" else "primary",
            disabled=st.session_state.answer_submitted
        ):
            handle_answer("missing")
    
    # Show feedback if answer submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next problem button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def generate_fake_answers(problem_data):
    """Generate plausible but incorrect answers for extra/missing problems"""
    # Extract numbers from the problem
    import re
    numbers = re.findall(r'\b\d+\b', problem_data['problem_text'])
    numbers = [int(n) for n in numbers if int(n) > 0]
    
    fake_answers = []
    
    if numbers:
        # Sum of some numbers
        if len(numbers) >= 2:
            fake_answers.append(sum(numbers[:2]))
            fake_answers.append(sum(numbers))
        
        # Product of some numbers
        if len(numbers) >= 2:
            fake_answers.append(numbers[0] * numbers[1])
        
        # Difference
        if len(numbers) >= 2:
            fake_answers.append(abs(numbers[0] - numbers[1]))
        
        # Random combinations
        for _ in range(3):
            if len(numbers) >= 2:
                n1, n2 = random.sample(numbers, 2)
                operation = random.choice([
                    lambda a, b: a + b,
                    lambda a, b: a * b,
                    lambda a, b: abs(a - b),
                    lambda a, b: a * b + random.randint(10, 50)
                ])
                result = operation(n1, n2)
                if result > 0:
                    fake_answers.append(result)
    
    # Ensure we have at least 3 options
    while len(fake_answers) < 3:
        fake_answers.append(random.randint(20, 200))
    
    # Remove duplicates and limit to 3
    fake_answers = list(set(fake_answers))[:3]
    
    return sorted(fake_answers)

def handle_answer(answer):
    """Handle user's answer selection"""
    st.session_state.user_answer = answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_feedback():
    """Display feedback for the submitted answer"""
    problem_data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    problem_type = problem_data['problem_type']
    
    is_correct = False
    
    if problem_type == "missing" and user_answer == "missing":
        is_correct = True
        st.success("✅ **Correct! This problem is missing information.**")
    elif problem_type == "extra" and user_answer != "missing":
        # For extra info problems, any calculated answer could be correct
        # depending on the specific problem
        is_correct = True
        st.success("✅ **Correct! This problem has extra information but can be solved.**")
    elif problem_type == "solvable" and user_answer == problem_data['correct_answer']:
        is_correct = True
        st.success("✅ **Correct! Well done!**")
    else:
        st.error("❌ **Not quite right.**")
    
    if is_correct:
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.extra_missing_difficulty
            st.session_state.extra_missing_difficulty = min(
                st.session_state.extra_missing_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.extra_missing_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Amazing! You've mastered identifying problem types!**")
            elif old_difficulty < st.session_state.extra_missing_difficulty:
                st.info(f"⬆️ **Level up! Now at Level {st.session_state.extra_missing_difficulty}**")
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty
        old_difficulty = st.session_state.extra_missing_difficulty
        st.session_state.extra_missing_difficulty = max(
            st.session_state.extra_missing_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.extra_missing_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.extra_missing_difficulty}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the problem type"""
    problem_data = st.session_state.problem_data
    problem_type = problem_data['problem_type']
    
    with st.expander("📖 **See the explanation**", expanded=True):
        if problem_type == "missing":
            st.markdown("### This problem is MISSING information! ❓")
            st.markdown(f"**What's missing:** {problem_data['missing_info']}")
            st.markdown("""
            To solve this problem, you would need to know this missing information.
            Without it, there's no way to find the answer.
            """)
            
        elif problem_type == "extra":
            st.markdown("### This problem has EXTRA information! 🎯")
            st.markdown("**Information you DON'T need:**")
            for extra in problem_data['extra_info']:
                # Find the value of this extra info
                extra_value = problem_data['variable_values'].get(extra, "")
                st.markdown(f"- **{extra.replace('_', ' ').title()}**: {extra_value}")
            
            st.markdown("""
            
            The extra information might make the problem seem harder, but you can ignore it!
            Focus only on what the question asks for.
            """)
            
        else:  # solvable
            st.markdown("### This problem has JUST THE RIGHT information! ✅")
            st.markdown("""
            Everything you need is in the problem, and nothing extra.
            You can solve it step by step using the given information.
            """)
            
            if problem_data['correct_answer']:
                st.markdown(f"**The answer is: {problem_data['correct_answer']}**")
        
        # Tips section
        st.markdown("---")
        st.markdown("### 💡 Remember:")
        st.markdown("""
        1. **Read the question first** - What are you trying to find?
        2. **List the information** - What numbers and facts are given?
        3. **Check what you need** - What information is required to solve it?
        4. **Compare** - Do you have too much, too little, or just right?
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None