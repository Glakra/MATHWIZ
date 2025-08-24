import streamlit as st
import random

def run():
    """
    Main function to run the Multi-step word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/multistep_word_problems.py
    """
    # Initialize session state
    if "multistep_difficulty" not in st.session_state:
        st.session_state.multistep_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.solution_steps = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🧩 Multi-Step Word Problems")
    st.markdown("*Solve complex problems using multiple operations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multistep_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Two Steps", "Three Steps", "Complex", "Advanced", "Master"]
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
        generate_new_multistep_problem()
    
    # Display current problem
    display_multistep_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Multi-Step Problem Solving Guide**", expanded=False):
        st.markdown("""
        ### How to Solve Multi-Step Problems:
        
        **1. Read Carefully** 📖
        - Read the entire problem twice
        - Identify what you're asked to find
        - Circle or underline important numbers
        
        **2. Break It Down** 🔍
        - Identify each step needed
        - Figure out the order of operations
        - Write down what each step will find
        
        **3. Work Step by Step** ✏️
        - Do one calculation at a time
        - Label what each answer represents
        - Use your answers in the next steps
        
        **4. Check Your Work** ✓
        - Re-read the question
        - Make sure you answered what was asked
        - Check if your answer makes sense
        
        ### Example Problem:
        
        **"Tom has $50. He buys 3 books for $8 each and 2 pens for $3 each. How much money does he have left?"**
        
        **Step 1:** Cost of books = 3 × $8 = $24
        **Step 2:** Cost of pens = 2 × $3 = $6
        **Step 3:** Total spent = $24 + $6 = $30
        **Step 4:** Money left = $50 - $30 = $20
        
        **Answer:** Tom has $20 left
        
        ### Common Multi-Step Patterns:
        
        **Pattern 1: Buy Multiple Items**
        - Find cost of each type
        - Add total costs
        - Subtract from money given
        
        **Pattern 2: Compare Groups**
        - Calculate each group size
        - Find the difference
        
        **Pattern 3: Distribute Items**
        - Find total items
        - Divide or multiply for distribution
        
        **Pattern 4: Complex Relationships**
        - "more than", "less than", "times as many"
        - Build from known to unknown
        
        ### Tips:
        - Draw pictures or diagrams
        - Make a table to organize information
        - Write equations for each step
        - Always label your answers
        """)

def generate_multistep_scenarios():
    """Generate diverse multi-step problem scenarios"""
    return {
        "shopping": [
            {
                "template": "{name}'s {relative} gave {pronoun} ${money} to go to the store. {name} bought {qty1} {item1} and {qty2} {item2}. Each {single1} cost ${price1} and each {single2} cost ${price2}. How much money does {name} have left?",
                "names": [("Jerry", "him"), ("Sarah", "her"), ("Alex", "them"), ("Maria", "her")],
                "relatives": ["mother", "father", "grandmother", "aunt", "uncle"],
                "items": [
                    ("loaves of bread", "loaf of bread", "cartons of orange juice", "carton of orange juice"),
                    ("bags of chips", "bag of chips", "bottles of soda", "bottle of soda"),
                    ("notebooks", "notebook", "packs of pens", "pack of pens"),
                    ("apples", "apple", "oranges", "orange"),
                    ("candy bars", "candy bar", "packs of gum", "pack of gum")
                ],
                "steps": [
                    "Calculate cost of {item1}: {qty1} × ${price1}",
                    "Calculate cost of {item2}: {qty2} × ${price2}",
                    "Find total spent: add both costs",
                    "Find money left: ${money} - total spent"
                ]
            },
            {
                "template": "{name} went to the bookstore with ${money}. {pronoun_cap} bought {qty1} {item1} for ${price1} each and spent ${spent2} on {item2}. {pronoun_cap} then bought a {item3} with half of the remaining money. How much money did {name} have left?",
                "names": [("Tom", "He", "he"), ("Lisa", "She", "she"), ("Sam", "They", "they")],
                "items": [
                    ("comic books", "magazines", "bookmark"),
                    ("novels", "newspapers", "poster"),
                    ("textbooks", "workbooks", "pencil case")
                ],
                "steps": [
                    "Calculate cost of {item1}: {qty1} × ${price1}",
                    "Find money after first two purchases: ${money} - cost1 - ${spent2}",
                    "Calculate cost of {item3}: remaining ÷ 2",
                    "Find final amount: remaining - cost of {item3}"
                ]
            }
        ],
        
        "comparison": [
            {
                "template": "{name} bought {qty1} packs of {color1} {item} and {qty2} packs of {color2} {item}. Each package contained {per_pack} {item}. How many more {color1} {item} than {color2} {item} did {name} buy?",
                "names": ["Mary", "John", "Emma", "David"],
                "colors": [("red", "yellow"), ("blue", "green"), ("purple", "orange"), ("black", "white")],
                "items": ["bouncy balls", "marbles", "stickers", "trading cards", "beads"],
                "unit": "{color1} {item}",
                "steps": [
                    "Calculate total {color1} {item}: {qty1} × {per_pack}",
                    "Calculate total {color2} {item}: {qty2} × {per_pack}",
                    "Find difference: {color1} total - {color2} total"
                ]
            },
            {
                "template": "Class A has {students1} students and collected {qty1} {items} in total. Class B has {students2} students and each student brought {per_student} {items}. How many more {items} did Class B collect than Class A?",
                "items": ["cans for recycling", "books for charity", "toys for donation", "bottles for fundraising"],
                "unit": "{items}",
                "steps": [
                    "Class A total: {qty1} {items}",
                    "Class B total: {students2} × {per_student}",
                    "Find difference: Class B total - Class A total"
                ]
            }
        ],
        
        "transportation": [
            {
                "template": "The {group} went on a {activity} to see a {destination}. To get to the {activity}, the {group} took {qty1} cars and {qty2} vans. There were {per_car} people in each car and {per_van} people in each van. How many people went on the {activity}?",
                "groups": ["adventure club", "science class", "scout troop", "youth group", "sports team"],
                "activities": ["hike", "field trip", "camping trip", "excursion"],
                "destinations": ["waterfall", "museum", "nature reserve", "historical site", "observatory"],
                "unit": "people",
                "steps": [
                    "Calculate people in cars: {qty1} × {per_car}",
                    "Calculate people in vans: {qty2} × {per_van}",
                    "Find total: add people in cars and vans"
                ]
            },
            {
                "template": "A school is planning a trip. They have {buses} buses that can hold {per_bus} students each and {vans} vans that can hold {per_van} students each. If {absent} students are absent that day, how many empty seats will there be?",
                "unit": "empty seats",
                "steps": [
                    "Calculate bus capacity: {buses} × {per_bus}",
                    "Calculate van capacity: {vans} × {per_van}",
                    "Find total capacity: bus capacity + van capacity",
                    "Find empty seats: total capacity - students going"
                ]
            }
        ],
        
        "complex_relationships": [
            {
                "template": "There are {base} {item1} in the {location}. There are {diff} more {item2} than {item1}, and there are {multiplier} times as many {item3} as {item2}. How many pieces of {category} are there in all?",
                "items": [
                    ("forks", "knives", "spoons", "cutlery", "cutlery drawer"),
                    ("pencils", "pens", "markers", "writing tools", "desk"),
                    ("roses", "tulips", "daisies", "flowers", "garden"),
                    ("cars", "trucks", "motorcycles", "vehicles", "parking lot")
                ],
                "unit": "pieces of {category}",
                "steps": [
                    "Count {item1}: {base}",
                    "Calculate {item2}: {base} + {diff}",
                    "Calculate {item3}: {item2} × {multiplier}",
                    "Find total: {item1} + {item2} + {item3}"
                ]
            },
            {
                "template": "{name} is collecting {items}. On Monday, {pronoun} collected {day1}. On Tuesday, {pronoun} collected {multiplier} times as many as Monday. On Wednesday, {pronoun} collected {diff} fewer than Tuesday. How many {items} did {name} collect in total?",
                "names": [("Jack", "he"), ("Lily", "she"), ("Jordan", "they")],
                "items": ["stamps", "coins", "seashells", "leaves", "rocks"],
                "unit": "{items}",
                "steps": [
                    "Monday: {day1} {items}",
                    "Tuesday: {day1} × {multiplier}",
                    "Wednesday: Tuesday amount - {diff}",
                    "Total: Monday + Tuesday + Wednesday"
                ]
            }
        ],
        
        "production": [
            {
                "template": "A bakery makes {item1} and {item2}. They make {batches1} batches of {item1} with {per_batch1} in each batch. They make {batches2} batches of {item2} with {per_batch2} in each batch. If they sell {sold} items, how many items are left?",
                "items": [
                    ("cookies", "brownies"),
                    ("muffins", "cupcakes"),
                    ("donuts", "bagels"),
                    ("pies", "cakes")
                ],
                "unit": "items",
                "steps": [
                    "Calculate total {item1}: {batches1} × {per_batch1}",
                    "Calculate total {item2}: {batches2} × {per_batch2}",
                    "Find total made: {item1} total + {item2} total",
                    "Find items left: total made - {sold}"
                ]
            }
        ],
        
        "distribution": [
            {
                "template": "{name} has {total} {items} to share equally among {groups} friends. After sharing, {name} buys {more} more {items} for each friend. How many {items} does each friend have now?",
                "names": ["Emma", "Noah", "Olivia", "Liam"],
                "items": ["candies", "stickers", "marbles", "cards"],
                "unit": "{items}",
                "steps": [
                    "Calculate initial share: {total} ÷ {groups}",
                    "Add additional {items}: initial + {more}",
                    "Each friend has: initial + additional"
                ]
            }
        ]
    }

def generate_new_multistep_problem():
    """Generate a new multi-step problem based on difficulty"""
    difficulty = st.session_state.multistep_difficulty
    scenarios = generate_multistep_scenarios()
    
    # Choose scenario type based on difficulty
    if difficulty == 1:
        scenario_types = ["shopping", "comparison", "transportation"]
    elif difficulty == 2:
        scenario_types = ["shopping", "comparison", "transportation", "production"]
    elif difficulty == 3:
        scenario_types = ["shopping", "complex_relationships", "production", "distribution"]
    elif difficulty == 4:
        scenario_types = ["complex_relationships", "production", "distribution"]
    else:  # difficulty == 5
        scenario_types = list(scenarios.keys())
    
    scenario_type = random.choice(scenario_types)
    scenario = random.choice(scenarios[scenario_type])
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        numbers = {
            "money": random.randint(50, 150),
            "qty1": random.randint(2, 5),
            "qty2": random.randint(2, 5),
            "price1": random.randint(3, 10),
            "price2": random.randint(2, 8),
            "per_pack": random.randint(10, 20),
            "per_car": random.randint(2, 4),
            "per_van": random.randint(5, 8),
            "base": random.randint(5, 15),
            "diff": random.randint(5, 15),
            "multiplier": 2
        }
    elif difficulty == 2:
        numbers = {
            "money": random.randint(100, 300),
            "qty1": random.randint(3, 8),
            "qty2": random.randint(3, 8),
            "price1": random.randint(5, 20),
            "price2": random.randint(4, 15),
            "spent2": random.randint(20, 50),
            "per_pack": random.randint(15, 30),
            "per_car": random.randint(3, 5),
            "per_van": random.randint(6, 12),
            "students1": random.randint(20, 35),
            "students2": random.randint(25, 40),
            "per_student": random.randint(3, 8),
            "base": random.randint(8, 20),
            "diff": random.randint(8, 20),
            "multiplier": random.randint(2, 3)
        }
    elif difficulty == 3:
        numbers = {
            "money": random.randint(200, 500),
            "qty1": random.randint(4, 12),
            "qty2": random.randint(4, 12),
            "price1": random.randint(8, 30),
            "price2": random.randint(6, 25),
            "spent2": random.randint(30, 80),
            "per_pack": random.randint(20, 50),
            "base": random.randint(10, 30),
            "diff": random.randint(10, 30),
            "multiplier": random.randint(2, 5),
            "batches1": random.randint(5, 15),
            "batches2": random.randint(5, 15),
            "per_batch1": random.randint(12, 24),
            "per_batch2": random.randint(10, 20),
            "sold": random.randint(50, 150)
        }
    elif difficulty == 4:
        numbers = {
            "money": random.randint(300, 800),
            "base": random.randint(15, 40),
            "diff": random.randint(15, 40),
            "multiplier": random.randint(3, 6),
            "day1": random.randint(20, 50),
            "total": random.randint(100, 300),
            "groups": random.randint(4, 8),
            "more": random.randint(5, 15),
            "buses": random.randint(3, 6),
            "per_bus": random.randint(40, 60),
            "vans": random.randint(2, 5),
            "per_van": random.randint(8, 15),
            "absent": random.randint(20, 50)
        }
    else:  # difficulty == 5
        numbers = {
            "money": random.randint(500, 1000),
            "base": random.randint(20, 50),
            "diff": random.randint(20, 50),
            "multiplier": random.randint(3, 8),
            "day1": random.randint(30, 80),
            "total": random.randint(200, 500),
            "groups": random.randint(5, 12),
            "more": random.randint(10, 25)
        }
    
    # Build the problem
    problem_text = scenario["template"]
    
    # Replace placeholders
    if "names" in scenario:
        if isinstance(scenario["names"][0], tuple):
            name_data = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name_data[0])
            if len(name_data) > 2:
                problem_text = problem_text.replace("{pronoun_cap}", name_data[1])
                problem_text = problem_text.replace("{pronoun}", name_data[2])
            else:
                problem_text = problem_text.replace("{pronoun}", name_data[1])
        else:
            name = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name)
    
    # Replace other lists
    for key in ["relatives", "items", "colors", "groups", "activities", "destinations"]:
        if key in scenario:
            if key == "items" and isinstance(scenario["items"][0], tuple):
                item_set = random.choice(scenario["items"])
                if len(item_set) == 5:  # Complex relationships
                    problem_text = problem_text.replace("{item1}", item_set[0])
                    problem_text = problem_text.replace("{item2}", item_set[1])
                    problem_text = problem_text.replace("{item3}", item_set[2])
                    problem_text = problem_text.replace("{category}", item_set[3])
                    problem_text = problem_text.replace("{location}", item_set[4])
                elif len(item_set) == 4:  # Shopping with singles
                    problem_text = problem_text.replace("{item1}", item_set[0])
                    problem_text = problem_text.replace("{single1}", item_set[1])
                    problem_text = problem_text.replace("{item2}", item_set[2])
                    problem_text = problem_text.replace("{single2}", item_set[3])
                else:
                    problem_text = problem_text.replace("{item1}", item_set[0])
                    problem_text = problem_text.replace("{item2}", item_set[1])
                    if len(item_set) > 2:
                        problem_text = problem_text.replace("{item3}", item_set[2])
            elif key == "colors" and isinstance(scenario["colors"][0], tuple):
                colors = random.choice(scenario["colors"])
                problem_text = problem_text.replace("{color1}", colors[0])
                problem_text = problem_text.replace("{color2}", colors[1])
            else:
                item = random.choice(scenario[key])
                problem_text = problem_text.replace(f"{{{key[:-1]}}}", item)
                problem_text = problem_text.replace(f"{{{key}}}", item)
    
    # Replace numbers
    for key, value in numbers.items():
        problem_text = problem_text.replace(f"{{{key}}}", str(value))
    
    # Calculate the answer and build solution steps
    solution_steps = []
    
    if scenario_type == "shopping" and "gave" in problem_text and "have left" in problem_text:
        # Standard shopping problem
        cost1 = numbers.get("qty1", 1) * numbers.get("price1", 1)
        cost2 = numbers.get("qty2", 1) * numbers.get("price2", 1)
        total_spent = cost1 + cost2
        answer = numbers.get("money", 100) - total_spent
        
        solution_steps = [
            f"Cost of first item: {numbers.get('qty1', 1)} × ${numbers.get('price1', 1)} = ${cost1}",
            f"Cost of second item: {numbers.get('qty2', 1)} × ${numbers.get('price2', 1)} = ${cost2}",
            f"Total spent: ${cost1} + ${cost2} = ${total_spent}",
            f"Money left: ${numbers.get('money', 100)} - ${total_spent} = ${answer}"
        ]
        
    elif scenario_type == "comparison":
        if "packs" in problem_text:
            total1 = numbers.get("qty1", 1) * numbers.get("per_pack", 1)
            total2 = numbers.get("qty2", 1) * numbers.get("per_pack", 1)
            answer = total1 - total2
            
            solution_steps = [
                f"First group total: {numbers.get('qty1', 1)} × {numbers.get('per_pack', 1)} = {total1}",
                f"Second group total: {numbers.get('qty2', 1)} × {numbers.get('per_pack', 1)} = {total2}",
                f"Difference: {total1} - {total2} = {answer}"
            ]
        else:
            # Class collection problem
            class_a = numbers.get("qty1", 100)
            class_b = numbers.get("students2", 30) * numbers.get("per_student", 5)
            answer = class_b - class_a
            
            solution_steps = [
                f"Class A total: {class_a} items",
                f"Class B total: {numbers.get('students2', 30)} × {numbers.get('per_student', 5)} = {class_b}",
                f"Difference: {class_b} - {class_a} = {answer}"
            ]
            
    elif scenario_type == "transportation":
        if "went on" in problem_text and "How many people" in problem_text:
            people_cars = numbers.get("qty1", 4) * numbers.get("per_car", 3)
            people_vans = numbers.get("qty2", 3) * numbers.get("per_van", 6)
            answer = people_cars + people_vans
            
            solution_steps = [
                f"People in cars: {numbers.get('qty1', 4)} × {numbers.get('per_car', 3)} = {people_cars}",
                f"People in vans: {numbers.get('qty2', 3)} × {numbers.get('per_van', 6)} = {people_vans}",
                f"Total people: {people_cars} + {people_vans} = {answer}"
            ]
        else:
            # Empty seats problem
            bus_capacity = numbers.get("buses", 4) * numbers.get("per_bus", 50)
            van_capacity = numbers.get("vans", 3) * numbers.get("per_van", 12)
            total_capacity = bus_capacity + van_capacity
            students_going = total_capacity - numbers.get("absent", 30)
            answer = numbers.get("absent", 30)
            
            solution_steps = [
                f"Bus capacity: {numbers.get('buses', 4)} × {numbers.get('per_bus', 50)} = {bus_capacity}",
                f"Van capacity: {numbers.get('vans', 3)} × {numbers.get('per_van', 12)} = {van_capacity}",
                f"Total capacity: {bus_capacity} + {van_capacity} = {total_capacity}",
                f"Empty seats: {answer}"
            ]
            
    elif scenario_type == "complex_relationships":
        if "cutlery" in problem_text or "drawer" in problem_text or "garden" in problem_text:
            item1_count = numbers.get("base", 10)
            item2_count = item1_count + numbers.get("diff", 10)
            item3_count = item2_count * numbers.get("multiplier", 2)
            answer = item1_count + item2_count + item3_count
            
            solution_steps = [
                f"First item count: {item1_count}",
                f"Second item count: {item1_count} + {numbers.get('diff', 10)} = {item2_count}",
                f"Third item count: {item2_count} × {numbers.get('multiplier', 2)} = {item3_count}",
                f"Total: {item1_count} + {item2_count} + {item3_count} = {answer}"
            ]
        else:
            # Collection over days
            monday = numbers.get("day1", 30)
            tuesday = monday * numbers.get("multiplier", 3)
            wednesday = tuesday - numbers.get("diff", 10)
            answer = monday + tuesday + wednesday
            
            solution_steps = [
                f"Monday: {monday} items",
                f"Tuesday: {monday} × {numbers.get('multiplier', 3)} = {tuesday}",
                f"Wednesday: {tuesday} - {numbers.get('diff', 10)} = {wednesday}",
                f"Total: {monday} + {tuesday} + {wednesday} = {answer}"
            ]
            
    elif scenario_type == "production":
        total1 = numbers.get("batches1", 10) * numbers.get("per_batch1", 20)
        total2 = numbers.get("batches2", 8) * numbers.get("per_batch2", 15)
        total_made = total1 + total2
        answer = total_made - numbers.get("sold", 100)
        
        solution_steps = [
            f"First item total: {numbers.get('batches1', 10)} × {numbers.get('per_batch1', 20)} = {total1}",
            f"Second item total: {numbers.get('batches2', 8)} × {numbers.get('per_batch2', 15)} = {total2}",
            f"Total made: {total1} + {total2} = {total_made}",
            f"Items left: {total_made} - {numbers.get('sold', 100)} = {answer}"
        ]
        
    elif scenario_type == "distribution":
        initial_share = numbers.get("total", 200) // numbers.get("groups", 5)
        final_amount = initial_share + numbers.get("more", 10)
        answer = final_amount
        
        solution_steps = [
            f"Initial share per friend: {numbers.get('total', 200)} ÷ {numbers.get('groups', 5)} = {initial_share}",
            f"Additional items per friend: {numbers.get('more', 10)}",
            f"Total per friend: {initial_share} + {numbers.get('more', 10)} = {answer}"
        ]
    
    # Determine unit
    unit = scenario.get("unit", "")
    for key, value in numbers.items():
        unit = unit.replace(f"{{{key}}}", str(value))
    
    # Replace any remaining placeholders in unit
    if "{item}" in unit or "{items}" in unit:
        if "items" in scenario:
            if isinstance(scenario["items"], list) and isinstance(scenario["items"][0], str):
                item = scenario["items"][0] if scenario["items"] else "items"
                unit = unit.replace("{item}", item).replace("{items}", item)
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "scenario_type": scenario_type,
        "numbers": numbers,
        "unit": unit
    }
    st.session_state.correct_answer = answer
    st.session_state.solution_steps = solution_steps
    st.session_state.current_problem = problem_text

def display_multistep_problem():
    """Display the current multi-step problem"""
    # Display the problem
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd;
        border: 3px solid #1976d2;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        font-size: 18px;
        line-height: 1.8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    ">
        <strong>{st.session_state.current_problem}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_answer = st.number_input(
                "Your answer:",
                min_value=0,
                max_value=99999,
                step=1,
                key="multistep_answer"
            )
        
        with col2:
            unit = st.session_state.problem_data.get("unit", "")
            # Clean up unit display
            if unit and not unit.startswith("{"):
                st.markdown(f"<div style='padding-top: 30px; font-size: 16px;'>{unit}</div>", 
                           unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", 
                                                 type="primary", 
                                                 use_container_width=True)
        
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
    unit = st.session_state.problem_data.get("unit", "")
    
    # Clean unit display
    if unit.startswith("{"):
        unit = ""
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! {correct_answer} {unit} is correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.multistep_difficulty
        st.session_state.multistep_difficulty = min(
            st.session_state.multistep_difficulty + 1, 5
        )
        
        if st.session_state.multistep_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered multi-step problems!**")
        elif old_difficulty < st.session_state.multistep_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.multistep_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer} {unit}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.multistep_difficulty
        st.session_state.multistep_difficulty = max(
            st.session_state.multistep_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.multistep_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.multistep_difficulty}. Keep practicing!**")
        
        # Show solution
        show_step_by_step_solution()

def show_step_by_step_solution():
    """Show detailed step-by-step solution"""
    with st.expander("📖 **Step-by-Step Solution**", expanded=True):
        st.markdown("### Let's solve this step by step:")
        
        # Display each step
        for i, step in enumerate(st.session_state.solution_steps, 1):
            st.markdown(f"**Step {i}:** {step}")
        
        # Final answer
        answer = st.session_state.correct_answer
        unit = st.session_state.problem_data.get("unit", "")
        if unit and not unit.startswith("{"):
            st.markdown(f"\n### Final Answer: **{answer} {unit}**")
        else:
            st.markdown(f"\n### Final Answer: **{answer}**")
        
        # Problem-solving tip
        st.markdown("""
        ### Remember:
        - Break complex problems into smaller steps
        - Do one calculation at a time
        - Label what each number represents
        - Check if your answer makes sense
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    st.session_state.solution_steps = []
    if "user_answer" in st.session_state:
        del st.session_state.user_answer