import streamlit as st
import random

def run():
    """
    Main function to run the Guess-and-check problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/guess_and_check_problems.py
    """
    # Initialize session state
    if "guess_check_difficulty" not in st.session_state:
        st.session_state.guess_check_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answers = {}
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🔍 Guess-and-Check Problems")
    st.markdown("*Use logical thinking to find the answer*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.guess_check_difficulty
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
        generate_new_guess_check_problem()
    
    # Display current problem
    display_guess_check_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Solve Guess-and-Check Problems**", expanded=False):
        st.markdown("""
        ### The Guess-and-Check Method:
        
        **Step 1: Understand what you're looking for** 📝
        - Two different items/amounts
        - Two clues about them
        
        **Step 2: Make an organized guess** 🎯
        - Start with a reasonable number
        - Check if it works with BOTH clues
        
        **Step 3: Adjust your guess** 🔄
        - Too high? Try smaller numbers
        - Too low? Try bigger numbers
        - Getting closer? Keep going!
        
        **Step 4: Check your answer** ✅
        - Does it work for the total?
        - Does it work for the count?
        - Both must be correct!
        
        ### Example Strategy:
        
        **Problem:** "Sarah bought 5 items total. Apples cost $2 each and oranges cost $3 each. She spent $12 total."
        
        **Guess-and-Check Table:**
        | Apples | Oranges | Total Items | Total Cost | Result |
        |--------|---------|-------------|------------|--------|
        | 1      | 4       | ✓ 5         | $14        | Too high |
        | 2      | 3       | ✓ 5         | $13        | Too high |
        | 3      | 2       | ✓ 5         | ✓ $12      | Perfect! |
        
        ### Tips for Success:
        
        **1. Start in the middle** 🎯
        - If you have 10 items, try 5 and 5
        - Adjust from there
        
        **2. Look for patterns** 🔍
        - Each change affects the total
        - Notice how much each change adds/subtracts
        
        **3. Use logical limits** 🧠
        - Can't have more items than the total
        - Can't spend more than the budget
        
        **4. Make a table** 📊
        - Keep track of your guesses
        - See patterns more easily
        
        **5. Check both constraints** ✌️
        - Number of items must match
        - Total amount must match
        - BOTH must be correct!
        """)

def generate_problem_scenarios():
    """Generate diverse scenarios for guess-and-check problems"""
    return {
        "shopping_items": [
            {
                "template": "{name} bought {total_items} {container} of {item1} and {item2}. The {item1} came in {size1}-{unit} {container} and the {item2} came in {size2}-{unit} {container}. In all, {name} {action} {total_amount} {unit_plural} of {category}. How many {container} of {item1} and {container} of {item2} did {pronoun} {action2}?",
                "names": ["Florence", "Marcus", "Elena", "David"],
                "pronouns": ["she", "he", "she", "he"],
                "items": [
                    ("kiwis", "lemons", "fruit", "unpacked", "unpack"),
                    ("apples", "oranges", "fruit", "bought", "buy"),
                    ("strawberries", "blueberries", "berries", "picked", "pick"),
                    ("carrots", "potatoes", "vegetables", "harvested", "harvest")
                ],
                "containers": ["bags", "boxes", "crates", "baskets"],
                "units": ["kilogram", "pound", "litre"],
                "unit_plurals": ["kilograms", "pounds", "litres"]
            },
            {
                "template": "{name} found {total_items} rolls of {item1} ribbon and {item2} ribbon. Each roll of {item1} ribbon was {size1} {unit} long and each roll of {item2} ribbon was {size2} {unit} long. If {name} found {total_amount} {unit} of ribbon in total, how many rolls of each colour did {pronoun} find?",
                "names": ["Lauren", "Sophie", "Emma", "Olivia"],
                "pronouns": ["she", "she", "she", "she"],
                "items": [
                    ("white", "indigo"),
                    ("red", "blue"),
                    ("gold", "silver"),
                    ("pink", "purple")
                ],
                "units": ["metre", "foot", "yard"],
                "unit_plural": ["metres", "feet", "yards"]
            }
        ],
        
        "garden_store": [
            {
                "template": "The gardening store sells {item1} flower pots, which hold {size1} litres of dirt, and {item2} flower pots, which hold {size2} litre. {name} bought {total_items} flower pots, which will hold a total of {total_amount} litres of dirt. How many of each type of flower pot did {pronoun} buy?",
                "names": ["Grace", "Tom", "Maria", "Jack"],
                "pronouns": ["she", "he", "she", "he"],
                "items": [
                    ("clay", "ceramic"),
                    ("plastic", "terracotta"),
                    ("large", "small"),
                    ("round", "square")
                ]
            },
            {
                "template": "The nursery sells {item1} plants in {size1}-plant trays and {item2} plants in {size2}-plant trays. {name} bought {total_items} trays with a total of {total_amount} plants. How many trays of each type did {pronoun} buy?",
                "names": ["Carlos", "Anna", "Peter", "Lisa"],
                "pronouns": ["he", "she", "he", "she"],
                "items": [
                    ("tomato", "pepper"),
                    ("flower", "herb"),
                    ("succulent", "cactus"),
                    ("annual", "perennial")
                ]
            }
        ],
        
        "aquarium_shop": [
            {
                "template": "At the aquarium, posters of {item1} cost ${price1} and posters of {item2} cost ${price2}. {name} spent ${total_amount} to buy {total_items} posters. How many of each type of poster did {name} buy?",
                "names": ["Mr. Singleton", "Mrs. Chen", "Dr. Patel", "Ms. Rodriguez"],
                "items": [
                    ("sharks", "jellyfish"),
                    ("dolphins", "turtles"),
                    ("whales", "octopi"),
                    ("seahorses", "starfish")
                ]
            },
            {
                "template": "The aquarium gift shop sells {item1} keychains for ${price1} each and {item2} keychains for ${price2} each. {name} bought {total_items} keychains for ${total_amount}. How many of each type did {pronoun} buy?",
                "names": ["Alex", "Jordan", "Sam", "Casey"],
                "pronouns": ["they", "they", "they", "they"],
                "items": [
                    ("metal", "plastic"),
                    ("large", "small"),
                    ("3D", "flat"),
                    ("glow", "regular")
                ]
            }
        ],
        
        "stickers_stamps": [
            {
                "template": "{name} bought {total_items} {item1} and {item2} stickers for {pronoun_poss} little {relative}. The {item1} stickers cost {price1} cents apiece and the {item2} stickers cost {price2} cent apiece. If {name} spent exactly {total_amount} cents, how many of each type of sticker did {pronoun} buy?",
                "names": ["Greta", "Maya", "Nina", "Rosa"],
                "pronouns": ["she", "she", "she", "she"],
                "pronoun_poss": ["her", "her", "her", "her"],
                "relatives": ["sister", "brother", "cousin", "nephew"],
                "items": [
                    ("rainbow", "balloon"),
                    ("star", "heart"),
                    ("animal", "flower"),
                    ("sparkle", "plain")
                ]
            },
            {
                "template": "{name} collects stamps. {pronoun_cap} bought {total_items} stamps this week: some {item1} stamps at {price1} cents each and some {item2} stamps at {price2} cents each. {pronoun_cap} spent {total_amount} cents total. How many of each type did {pronoun} buy?",
                "names": ["Oliver", "Ethan", "Lucas", "Noah"],
                "pronouns": ["he", "he", "he", "he"],
                "pronoun_cap": ["He", "He", "He", "He"],
                "items": [
                    ("vintage", "modern"),
                    ("foreign", "domestic"),
                    ("commemorative", "regular"),
                    ("rare", "common")
                ]
            }
        ],
        
        "restaurant_supplies": [
            {
                "template": "A restaurant owner {action} {total_amount} kilograms of vegetables, some {item1} and some {item2}. The {item1} came in {size1}-kilogram bags and the {item2} came in {size2}-kilogram bags. The owner {action} {total_items} bags of vegetables in all. How many bags of each kind did {pronoun} {action2}?",
                "names": ["the chef", "the owner", "the manager", "the cook"],
                "pronouns": ["he", "she", "they", "he"],
                "actions": ["washed", "ordered", "received", "prepared"],
                "action2": ["wash", "order", "receive", "prepare"],
                "items": [
                    ("corn", "mushrooms"),
                    ("carrots", "onions"),
                    ("potatoes", "tomatoes"),
                    ("peppers", "zucchini")
                ]
            }
        ],
        
        "tickets_events": [
            {
                "template": "For the school play, adult tickets cost ${price1} and child tickets cost ${price2}. The {name} family bought {total_items} tickets for ${total_amount}. How many adult tickets and child tickets did they buy?",
                "names": ["Johnson", "Williams", "Brown", "Davis"],
                "price_ranges": {
                    "adult": [8, 10, 12, 15],
                    "child": [4, 5, 6, 8]
                }
            },
            {
                "template": "At the {event}, {item1} passes cost ${price1} and {item2} passes cost ${price2}. {name} spent ${total_amount} on {total_items} passes. How many of each type did {pronoun} buy?",
                "names": ["Sarah", "Mike", "Jenny", "Tom"],
                "pronouns": ["she", "he", "she", "he"],
                "events": ["carnival", "fair", "festival", "amusement park"],
                "items": [
                    ("all-day", "half-day"),
                    ("premium", "regular"),
                    ("VIP", "general"),
                    ("weekend", "weekday")
                ]
            }
        ],
        
        "craft_supplies": [
            {
                "template": "{name} is buying supplies for art class. {item1} come in packs of {size1} and {item2} come in packs of {size2}. {pronoun_cap} needs exactly {total_amount} items and can buy {total_items} packs. How many packs of each should {pronoun} buy?",
                "names": ["Emma", "Liam", "Ava", "Mason"],
                "pronouns": ["she", "he", "she", "he"],
                "pronoun_cap": ["She", "He", "She", "He"],
                "items": [
                    ("paintbrushes", "sponges"),
                    ("markers", "crayons"),
                    ("pencils", "erasers"),
                    ("scissors", "glue sticks")
                ]
            }
        ],
        
        "sports_equipment": [
            {
                "template": "The sports store sells {item1} in packs of {size1} and {item2} in packs of {size2}. Coach {name} bought {total_items} packs containing {total_amount} items total. How many packs of each type did the coach buy?",
                "names": ["Martinez", "Thompson", "Anderson", "Wilson"],
                "items": [
                    ("tennis balls", "shuttlecocks"),
                    ("baseballs", "softballs"),
                    ("ping pong balls", "golf balls"),
                    ("footballs", "soccer balls")
                ]
            }
        ],
        
        "bakery_items": [
            {
                "template": "At the bakery, {item1} cost ${price1} each and {item2} cost ${price2} each. {name} spent ${total_amount} on {total_items} items. How many of each did {pronoun} buy?",
                "names": ["Mrs. Lee", "Mr. Garcia", "Ms. Taylor", "Dr. White"],
                "pronouns": ["she", "he", "she", "he"],
                "items": [
                    ("muffins", "cookies"),
                    ("donuts", "bagels"),
                    ("croissants", "danish"),
                    ("cupcakes", "brownies")
                ]
            }
        ],
        
        "party_supplies": [
            {
                "template": "{name} is planning a party. {item1} decorations come in sets of {size1} and {item2} decorations come in sets of {size2}. {pronoun_cap} needs {total_amount} decorations and bought {total_items} sets. How many sets of each type did {pronoun} buy?",
                "names": ["Ashley", "Brandon", "Chloe", "Daniel"],
                "pronouns": ["she", "he", "she", "he"],
                "pronoun_cap": ["She", "He", "She", "He"],
                "items": [
                    ("balloon", "streamer"),
                    ("banner", "garland"),
                    ("centerpiece", "confetti"),
                    ("lantern", "ribbon")
                ]
            }
        ]
    }

def generate_new_guess_check_problem():
    """Generate a new guess-and-check problem"""
    difficulty = st.session_state.guess_check_difficulty
    scenarios = generate_problem_scenarios()
    
    # Choose scenario types based on difficulty
    if difficulty == 1:
        scenario_types = ["shopping_items", "stickers_stamps", "aquarium_shop"]
    elif difficulty == 2:
        scenario_types = ["garden_store", "restaurant_supplies", "tickets_events"]
    elif difficulty == 3:
        scenario_types = ["craft_supplies", "bakery_items", "party_supplies"]
    elif difficulty == 4:
        scenario_types = ["sports_equipment", "tickets_events", "restaurant_supplies"]
    else:  # difficulty == 5
        scenario_types = list(scenarios.keys())
    
    # Select random scenario
    scenario_type = random.choice(scenario_types)
    scenario_templates = scenarios[scenario_type]
    template = random.choice(scenario_templates)
    
    # Generate problem parameters
    problem_text = template["template"]
    
    # Generate valid problem numbers
    if scenario_type == "shopping_items":
        if "kilogram" in problem_text:
            # Bags of produce problem
            size1 = random.choice([2, 3, 4, 5])
            size2 = random.choice([3, 4, 5, 6, 7, 8, 9])
            while size2 == size1:
                size2 = random.choice([3, 4, 5, 6, 7, 8, 9])
            
            # Find valid combinations
            valid_combos = []
            for i in range(1, 10):
                for j in range(1, 10):
                    if 3 <= i + j <= 8:  # reasonable number of bags
                        total_weight = i * size1 + j * size2
                        if 20 <= total_weight <= 60:  # reasonable total weight
                            valid_combos.append((i, j, i + j, total_weight))
            
            if valid_combos:
                answer1, answer2, total_items, total_amount = random.choice(valid_combos)
            else:
                answer1, answer2 = 2, 3
                total_items = 5
                total_amount = answer1 * size1 + answer2 * size2
                
        else:
            # Ribbon problem
            size1 = random.choice([1, 2])
            size2 = random.choice([3, 4, 5, 6])
            
            valid_combos = []
            for i in range(1, 8):
                for j in range(1, 8):
                    if 2 <= i + j <= 6:
                        total_length = i * size1 + j * size2
                        if 10 <= total_length <= 30:
                            valid_combos.append((i, j, i + j, total_length))
            
            if valid_combos:
                answer1, answer2, total_items, total_amount = random.choice(valid_combos)
            else:
                answer1, answer2 = 2, 3
                total_items = 5
                total_amount = answer1 * size1 + answer2 * size2
    
    elif scenario_type == "garden_store":
        # Flower pots problem
        size1 = random.choice([5, 10, 15, 20])
        size2 = 1  # small pots hold 1 litre
        
        valid_combos = []
        for i in range(1, 10):
            for j in range(1, 20):
                if 4 <= i + j <= 12:
                    total_litres = i * size1 + j * size2
                    if 30 <= total_litres <= 80:
                        valid_combos.append((i, j, i + j, total_litres))
        
        if valid_combos:
            answer1, answer2, total_items, total_amount = random.choice(valid_combos)
        else:
            answer1, answer2 = 2, 5
            total_items = 7
            total_amount = answer1 * size1 + answer2 * size2
    
    elif scenario_type in ["aquarium_shop", "stickers_stamps", "tickets_events", "bakery_items"]:
        # Money problems
        if scenario_type == "stickers_stamps" and "cent" in template["template"]:
            price1 = random.choice([5, 6, 8, 10])
            price2 = random.choice([1, 2, 3])
            money_unit = "cents"
            max_total = 50
        else:
            price1 = random.choice([2, 3, 4, 5])
            price2 = random.choice([1, 2])
            money_unit = "dollars"
            max_total = 20
        
        size1, size2 = price1, price2
        
        valid_combos = []
        for i in range(1, 10):
            for j in range(1, 10):
                if 3 <= i + j <= 10:
                    total_cost = i * price1 + j * price2
                    if total_cost <= max_total:
                        valid_combos.append((i, j, i + j, total_cost))
        
        if valid_combos:
            answer1, answer2, total_items, total_amount = random.choice(valid_combos)
        else:
            answer1, answer2 = 2, 3
            total_items = 5
            total_amount = answer1 * price1 + answer2 * price2
    
    else:
        # Other scenarios with pack sizes
        size1 = random.choice([3, 4, 5, 6])
        size2 = random.choice([8, 10, 12])
        
        valid_combos = []
        for i in range(1, 8):
            for j in range(1, 8):
                if 3 <= i + j <= 10:
                    total_count = i * size1 + j * size2
                    if 30 <= total_count <= 100:
                        valid_combos.append((i, j, i + j, total_count))
        
        if valid_combos:
            answer1, answer2, total_items, total_amount = random.choice(valid_combos)
        else:
            answer1, answer2 = 3, 2
            total_items = 5
            total_amount = answer1 * size1 + answer2 * size2
    
    # Replace template variables
    if "names" in template:
        name = random.choice(template["names"])
        problem_text = problem_text.replace("{name}", name)
    
    if "pronouns" in template:
        pronoun = template["pronouns"][template["names"].index(name)]
        problem_text = problem_text.replace("{pronoun}", pronoun)
    
    if "pronoun_cap" in template:
        pronoun_cap = template["pronoun_cap"][template["names"].index(name)]
        problem_text = problem_text.replace("{pronoun_cap}", pronoun_cap)
    
    if "pronoun_poss" in template:
        pronoun_poss = template["pronoun_poss"][template["names"].index(name)]
        problem_text = problem_text.replace("{pronoun_poss}", pronoun_poss)
    
    # Replace item placeholders
    if "items" in template:
        if isinstance(template["items"][0], tuple):
            items = random.choice(template["items"])
            if len(items) >= 3:
                problem_text = problem_text.replace("{item1}", items[0])
                problem_text = problem_text.replace("{item2}", items[1])
                problem_text = problem_text.replace("{category}", items[2])
                if len(items) >= 4:
                    problem_text = problem_text.replace("{action}", items[3])
                if len(items) >= 5:
                    problem_text = problem_text.replace("{action2}", items[4])
            else:
                problem_text = problem_text.replace("{item1}", items[0])
                problem_text = problem_text.replace("{item2}", items[1])
    
    # Replace other placeholders
    for key in ["containers", "container", "units", "unit", "unit_plural", "unit_plurals", 
                "relatives", "relative", "events", "event"]:
        if key in template:
            if isinstance(template[key], list):
                value = random.choice(template[key])
            else:
                value = template[key]
            problem_text = problem_text.replace(f"{{{key}}}", value)
    
    # Replace numeric values
    problem_text = problem_text.replace("{size1}", str(size1))
    problem_text = problem_text.replace("{size2}", str(size2))
    problem_text = problem_text.replace("{price1}", str(size1))
    problem_text = problem_text.replace("{price2}", str(size2))
    problem_text = problem_text.replace("{total_items}", str(total_items))
    problem_text = problem_text.replace("{total_amount}", str(total_amount))
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "answer1": answer1,
        "answer2": answer2,
        "size1": size1,
        "size2": size2,
        "total_items": total_items,
        "total_amount": total_amount,
        "scenario_type": scenario_type,
        "item1_name": template.get("items", [("item 1", "item 2")])[0][0] if "items" in template else "item 1",
        "item2_name": template.get("items", [("item 1", "item 2")])[0][1] if "items" in template else "item 2"
    }
    st.session_state.current_problem = problem_text

def display_guess_check_problem():
    """Display the current guess-and-check problem"""
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
    
    # Answer input fields
    st.markdown("### Enter your answers:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Extract item names from problem text
        item1_label = f"{problem_data['item1_name']} items"
        if "bags" in problem_data['problem_text']:
            item1_label = f"bags of {problem_data['item1_name']}"
        elif "rolls" in problem_data['problem_text']:
            item1_label = f"rolls of {problem_data['item1_name']} ribbon"
        elif "pots" in problem_data['problem_text']:
            item1_label = f"{problem_data['item1_name']} flower pots"
        elif "posters" in problem_data['problem_text']:
            item1_label = f"posters of {problem_data['item1_name']}"
        elif "stickers" in problem_data['problem_text']:
            item1_label = f"{problem_data['item1_name']} stickers"
        
        answer1 = st.number_input(
            item1_label,
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key="answer1_input",
            disabled=st.session_state.answer_submitted
        )
    
    with col2:
        item2_label = f"{problem_data['item2_name']} items"
        if "bags" in problem_data['problem_text']:
            item2_label = f"bags of {problem_data['item2_name']}"
        elif "rolls" in problem_data['problem_text']:
            item2_label = f"rolls of {problem_data['item2_name']} ribbon"
        elif "pots" in problem_data['problem_text']:
            item2_label = f"{problem_data['item2_name']} flower pots"
        elif "posters" in problem_data['problem_text']:
            item2_label = f"posters of {problem_data['item2_name']}"
        elif "stickers" in problem_data['problem_text']:
            item2_label = f"{problem_data['item2_name']} stickers"
        
        answer2 = st.number_input(
            item2_label,
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key="answer2_input",
            disabled=st.session_state.answer_submitted
        )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Submit", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.answer_submitted
        ):
            if answer1 == 0 and answer2 == 0:
                st.warning("Please enter your answers before submitting.")
            else:
                handle_answer(answer1, answer2)
    
    # Show feedback if answer submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next problem button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def handle_answer(answer1, answer2):
    """Handle user's answer submission"""
    st.session_state.user_answers = {
        "answer1": answer1,
        "answer2": answer2
    }
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_feedback():
    """Display feedback for the submitted answer"""
    problem_data = st.session_state.problem_data
    user_answers = st.session_state.user_answers
    
    correct_answer1 = problem_data['answer1']
    correct_answer2 = problem_data['answer2']
    user_answer1 = user_answers['answer1']
    user_answer2 = user_answers['answer2']
    
    # Check if answer is correct (order doesn't matter for some problems)
    is_correct = (
        (user_answer1 == correct_answer1 and user_answer2 == correct_answer2) or
        (user_answer1 == correct_answer2 and user_answer2 == correct_answer1)
    )
    
    if is_correct:
        st.success("✅ **Correct! Excellent work!**")
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.guess_check_difficulty
            st.session_state.guess_check_difficulty = min(
                st.session_state.guess_check_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.guess_check_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Fantastic! You've mastered guess-and-check problems!**")
            elif old_difficulty < st.session_state.guess_check_difficulty:
                st.info(f"⬆️ **Level up! Now at Level {st.session_state.guess_check_difficulty}**")
    
    else:
        st.error("❌ **Not quite right. Let's check your work.**")
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty
        old_difficulty = st.session_state.guess_check_difficulty
        st.session_state.guess_check_difficulty = max(
            st.session_state.guess_check_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.guess_check_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.guess_check_difficulty}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation with guess-and-check table"""
    problem_data = st.session_state.problem_data
    user_answers = st.session_state.user_answers
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Let's solve this step by step:")
        
        # Show what we know
        st.markdown("**What we know:**")
        st.markdown(f"- Each {problem_data['item1_name']} has/costs {problem_data['size1']} units")
        st.markdown(f"- Each {problem_data['item2_name']} has/costs {problem_data['size2']} units")
        st.markdown(f"- Total items: {problem_data['total_items']}")
        st.markdown(f"- Total amount: {problem_data['total_amount']} units")
        
        # Show guess-and-check table
        st.markdown("\n**Guess-and-Check Table:**")
        
        # Create a sample table showing the process
        table_data = []
        
        # Add some wrong guesses to show the process
        mid_point = problem_data['total_items'] // 2
        
        # First guess - split evenly
        guess1_1 = mid_point
        guess1_2 = problem_data['total_items'] - guess1_1
        total1 = guess1_1 * problem_data['size1'] + guess1_2 * problem_data['size2']
        table_data.append([
            guess1_1, guess1_2, 
            f"✓ {problem_data['total_items']}", 
            total1,
            "Too high" if total1 > problem_data['total_amount'] else "Too low"
        ])
        
        # Adjust and try again
        if total1 > problem_data['total_amount']:
            # Need fewer of the larger size
            guess2_1 = guess1_1 + 1
            guess2_2 = guess1_2 - 1
        else:
            guess2_1 = guess1_1 - 1
            guess2_2 = guess1_2 + 1
        
        if guess2_1 >= 0 and guess2_2 >= 0:
            total2 = guess2_1 * problem_data['size1'] + guess2_2 * problem_data['size2']
            table_data.append([
                guess2_1, guess2_2,
                f"✓ {problem_data['total_items']}",
                total2,
                "Too high" if total2 > problem_data['total_amount'] else "Too low" if total2 < problem_data['total_amount'] else "Just right!"
            ])
        
        # Add the correct answer
        table_data.append([
            problem_data['answer1'], 
            problem_data['answer2'],
            f"✓ {problem_data['total_items']}",
            f"✓ {problem_data['total_amount']}",
            "Perfect! ✅"
        ])
        
        # Display table
        headers = [
            problem_data['item1_name'].title(),
            problem_data['item2_name'].title(),
            "Total Items",
            "Total Amount",
            "Result"
        ]
        
        # Create HTML table
        table_html = "<table style='width:100%; margin-top:10px;'>"
        table_html += "<tr style='background-color:#f0f0f0;'>"
        for header in headers:
            table_html += f"<th style='padding:8px; border:1px solid #ddd;'>{header}</th>"
        table_html += "</tr>"
        
        for row in table_data:
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td style='padding:8px; border:1px solid #ddd; text-align:center;'>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Show the calculation
        st.markdown("\n**Checking the answer:**")
        st.markdown(f"- {problem_data['answer1']} × {problem_data['size1']} = {problem_data['answer1'] * problem_data['size1']}")
        st.markdown(f"- {problem_data['answer2']} × {problem_data['size2']} = {problem_data['answer2'] * problem_data['size2']}")
        st.markdown(f"- Total: {problem_data['answer1'] * problem_data['size1']} + {problem_data['answer2'] * problem_data['size2']} = **{problem_data['total_amount']}** ✓")
        st.markdown(f"- Items: {problem_data['answer1']} + {problem_data['answer2']} = **{problem_data['total_items']}** ✓")
        
        # Show user's attempt if wrong
        if user_answers['answer1'] != problem_data['answer1'] or user_answers['answer2'] != problem_data['answer2']:
            st.markdown("\n**Your answer:**")
            user_total = user_answers['answer1'] * problem_data['size1'] + user_answers['answer2'] * problem_data['size2']
            user_items = user_answers['answer1'] + user_answers['answer2']
            
            st.markdown(f"- {user_answers['answer1']} × {problem_data['size1']} + {user_answers['answer2']} × {problem_data['size2']} = {user_total}")
            st.markdown(f"- Total items: {user_items}")
            
            if user_items != problem_data['total_items']:
                st.markdown(f"❌ Item count doesn't match (need {problem_data['total_items']})")
            if user_total != problem_data['total_amount']:
                st.markdown(f"❌ Total amount doesn't match (need {problem_data['total_amount']})")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}