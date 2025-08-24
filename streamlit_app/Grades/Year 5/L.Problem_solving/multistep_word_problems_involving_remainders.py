import streamlit as st
import random

def run():
    """
    Main function to run the Multi-step word problems involving remainders activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/multistep_word_problems_involving_remainders.py
    """
    # Initialize session state
    if "remainder_difficulty" not in st.session_state:
        st.session_state.remainder_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🔢 Multi-Step Word Problems: Remainders")
    st.markdown("*Solve problems involving division with remainders*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.remainder_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Simple Division", "Two-Step Division", "Complex Context", "Advanced", "Master"]
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
        generate_new_remainder_problem()
    
    # Display current problem
    display_remainder_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Remainders Guide**", expanded=False):
        st.markdown("""
        ### Division with Remainders:
        
        **What are remainders?**
        When we divide and the numbers don't divide evenly, we have a remainder - the amount left over.
        
        **Example:** 17 ÷ 5 = 3 remainder 2
        - 5 goes into 17 three times (3 × 5 = 15)
        - We have 2 left over (17 - 15 = 2)
        
        ### Steps to Solve Remainder Problems:
        
        **1. Find the Total** 📊
        - Add or multiply to find total items
        - Make sure you have the complete amount
        
        **2. Divide** ➗
        - Divide total by group size
        - Find quotient (whole number) and remainder
        
        **3. Interpret the Remainder** 🤔
        - **Full groups:** The quotient tells you complete groups
        - **Left over:** The remainder tells you extras
        - **Context matters:** Think about what makes sense
        
        ### Common Remainder Situations:
        
        **Sharing Equally:**
        - "Each person gets ___ with ___ left over"
        - Example: 23 cookies ÷ 4 people = 5 each, 3 left over
        
        **Making Groups:**
        - "We can make ___ groups with ___ left over"
        - Example: 38 students ÷ 6 per team = 6 teams, 2 left over
        
        **Buying/Using Items:**
        - "We can buy/use ___ with $___ left"
        - Example: $25 ÷ $3 per item = 8 items, $1 left
        
        **Filling Containers:**
        - "We can fill ___ containers with ___ left"
        - Example: 47 eggs ÷ 12 per carton = 3 full cartons, 11 eggs left
        
        ### Tips:
        - Always check: quotient × divisor + remainder = total
        - Think: "Does my answer make sense?"
        - Label what the quotient and remainder represent
        """)

def generate_remainder_scenarios():
    """Generate diverse remainder problem scenarios"""
    return {
        "sharing_items": [
            {
                "template": "The {group} made {qty1} {items} before {time1} and {qty2} after {time2}. They decide to {action} them evenly.\n\nComplete the sentence.\n\nEach {member} will get [___] {items}, and there will be [___] left over.",
                "groups": ["neighborhood kids", "scout troop", "art club", "science team"],
                "items": ["snowballs", "paper airplanes", "origami cranes", "friendship bracelets"],
                "times": [("lunch", "lunch"), ("recess", "recess"), ("class", "class")],
                "actions": ["share", "divide", "split"],
                "members": ["team", "person", "member", "child"],
                "answer_type": "items_leftover"
            },
            {
                "template": "{name} and {pronoun} friends are {activity} that uses {total} {items1} and {extra} {items2}. The {total_all} {items_combined} {action} evenly, with some {items_combined} left over.\n\nComplete the sentence.\n\nEach player gets [___] {items_combined}, and there are [___] left over.",
                "names": [("Cora", "her"), ("Max", "his"), ("Alex", "their")],
                "activities": ["playing a card game", "doing a craft project", "playing a board game"],
                "items": [
                    ("regular cards", "jokers", "cards"),
                    ("colored beads", "special beads", "beads"),
                    ("game pieces", "bonus pieces", "pieces")
                ],
                "actions": ["split", "are divided"],
                "answer_type": "items_leftover"
            }
        ],
        
        "purchasing": [
            {
                "template": "{name} has been saving ${amount} a week for {weeks} weeks. {pronoun_cap} wants to spend {pronoun_poss} savings on {items}. They cost ${price} each, and {name} wants to buy as many as {pronoun} can.\n\nComplete the sentence.\n\n{name} can buy [___] {items}, and {pronoun} will have $[___] left.",
                "names": [
                    ("Ethan", "He", "his", "he"),
                    ("Sofia", "She", "her", "she"),
                    ("Jordan", "They", "their", "they")
                ],
                "items": ["comic books", "video games", "movie tickets", "art supplies"],
                "answer_type": "purchase_money"
            },
            {
                "template": "The {group} raised ${total} at their {event}. They want to buy {items} that cost ${price} each for their {purpose}.\n\nComplete the sentence.\n\nThey can buy [___] {items}, and they will have $[___] remaining.",
                "groups": ["chess club", "drama club", "robotics team", "debate team"],
                "events": ["bake sale", "car wash", "talent show", "garage sale"],
                "items": ["chess sets", "costumes", "robot parts", "reference books"],
                "purposes": ["club room", "next play", "competition", "library"],
                "answer_type": "purchase_money"
            }
        ],
        
        "grouping": [
            {
                "template": "At a school assembly, there are {qty1} in Year {y1}, {qty2} in Year {y2} and {qty3} in Year {y3}. They sit in rows of {per_row}.\n\nComplete the sentence.\n\nThere will be [___] full rows and one last row with only [___] students.",
                "answer_type": "rows_students"
            },
            {
                "template": "The {venue} is arranging {total} {items} for a {event}. They want to put {per_group} {items} on each {container}.\n\nComplete the sentence.\n\nThey will need [___] {containers}, with the last {container} having only [___] {items}.",
                "venues": ["library", "museum", "community center", "school"],
                "items": ["chairs", "displays", "books", "artworks"],
                "events": ["presentation", "exhibition", "book fair", "art show"],
                "containers": ["table", "shelf", "stand", "wall"],
                "answer_type": "containers_items"
            }
        ],
        
        "production": [
            {
                "template": "A {maker} has {qty1} {color1} {items} and another {qty2} {color2} {items}. {pronoun_cap} decides to {action} them together and make {products} with {per_product} {items} each.\n\nComplete the sentence.\n\nThe {maker} can make [___] {products}, and {pronoun} will have [___] {items} left.",
                "makers": [("florist", "He", "he"), ("artist", "She", "she"), ("crafter", "They", "they")],
                "items": ["roses", "beads", "ribbons", "buttons"],
                "colors": [("pink", "red"), ("blue", "green"), ("gold", "silver")],
                "actions": ["mix", "combine", "blend"],
                "products": ["bouquets", "necklaces", "decorations", "accessories"],
                "answer_type": "products_leftover"
            },
            {
                "template": "A bakery made {batch1} {item1} in the morning and {batch2} {item2} in the afternoon. They pack them in boxes of {per_box} treats each.\n\nComplete the sentence.\n\nThey can fill [___] complete boxes, with [___] treats not fitting in a full box.",
                "items": [("cookies", "brownies"), ("cupcakes", "muffins"), ("donuts", "bagels")],
                "answer_type": "boxes_treats"
            }
        ],
        
        "distribution": [
            {
                "template": "{name} got new {items} for {pronoun_poss} {location}, and now {pronoun} needs to put {supplies} in them. {pronoun_cap} has {packs} packs of {supplies} with {per_pack} {supplies} each. Each {item} needs {per_item} {supplies}.\n\nComplete the sentence.\n\n{name} can fill [___] {items}, and {pronoun} will have [___] {supplies} left over.",
                "names": [
                    ("Ms Smith", "her", "she", "She"),
                    ("Mr Johnson", "his", "he", "He"),
                    ("Mx Taylor", "their", "they", "They")
                ],
                "items": ["calculators", "pencil cases", "storage boxes", "folders"],
                "locations": ["classroom", "office", "lab", "studio"],
                "supplies": ["batteries", "pencils", "markers", "clips"],
                "answer_type": "items_supplies"
            }
        ],
        
        "complex_division": [
            {
                "template": "A {business} has {employees} employees working in {shifts} equal shifts. However, {absent} employees called in sick today. The remaining employees need to be divided equally among the shifts.\n\nComplete the sentence.\n\nEach shift will have [___] employees, with [___] employee(s) assigned to early shifts to balance the schedule.",
                "businesses": ["restaurant", "store", "factory", "hotel"],
                "answer_type": "shifts_extra"
            },
            {
                "template": "The {organization} collected {total} {items} for charity. They first set aside {reserve} for emergency use, then divided the rest equally among {recipients} {groups}.\n\nComplete the sentence.\n\nEach {group} will receive [___] {items}, and [___] will remain in the general fund.",
                "organizations": ["food bank", "toy drive", "book club", "clothing drive"],
                "items": ["cans of food", "toys", "books", "jackets"],
                "groups": ["families", "shelters", "schools", "centers"],
                "answer_type": "recipients_leftover"
            }
        ]
    }

def generate_new_remainder_problem():
    """Generate a new remainder problem based on difficulty"""
    difficulty = st.session_state.remainder_difficulty
    scenarios = generate_remainder_scenarios()
    
    # Choose scenario type based on difficulty
    if difficulty == 1:
        scenario_types = ["sharing_items", "grouping"]
    elif difficulty == 2:
        scenario_types = ["sharing_items", "purchasing", "grouping"]
    elif difficulty == 3:
        scenario_types = ["purchasing", "production", "distribution"]
    elif difficulty == 4:
        scenario_types = ["production", "distribution", "complex_division"]
    else:  # difficulty == 5
        scenario_types = list(scenarios.keys())
    
    scenario_type = random.choice(scenario_types)
    scenario = random.choice(scenarios[scenario_type])
    
    # Generate appropriate numbers based on difficulty and scenario
    if scenario_type == "sharing_items":
        if difficulty <= 2:
            qty1 = random.randint(10, 30)
            qty2 = random.randint(10, 25)
            divisor = random.randint(2, 5)
        else:
            qty1 = random.randint(20, 50)
            qty2 = random.randint(15, 45)
            divisor = random.randint(4, 8)
        
        total = qty1 + qty2
        quotient = total // divisor
        remainder = total % divisor
        
    elif scenario_type == "purchasing":
        if difficulty <= 3:
            if "weeks" in scenario["template"]:
                amount = random.randint(2, 5)
                weeks = random.randint(10, 20)
                total = amount * weeks
                price = random.randint(3, 8)
            else:
                total = random.randint(50, 200)
                price = random.randint(5, 15)
        else:
            if "weeks" in scenario["template"]:
                amount = random.randint(5, 15)
                weeks = random.randint(12, 26)
                total = amount * weeks
                price = random.randint(8, 25)
            else:
                total = random.randint(200, 500)
                price = random.randint(15, 40)
        
        quotient = total // price
        remainder = total % price
        
    elif scenario_type == "grouping":
        if "Year" in scenario.get("template", ""):
            qty1 = random.randint(18, 25)
            qty2 = random.randint(20, 28)
            qty3 = random.randint(19, 26)
            total = qty1 + qty2 + qty3
            per_row = random.randint(5, 8)
        else:
            total = random.randint(50, 150)
            per_group = random.randint(6, 12)
            per_row = per_group
        
        quotient = total // per_row
        remainder = total % per_row
        
    elif scenario_type == "production":
        if "color" in scenario.get("template", ""):
            qty1 = random.randint(15, 35)
            qty2 = random.randint(15, 35)
            total = qty1 + qty2
            per_product = random.randint(6, 12)
        else:
            batch1 = random.randint(20, 50)
            batch2 = random.randint(20, 50)
            total = batch1 + batch2
            per_product = random.randint(8, 15)
            per_box = per_product
        
        quotient = total // per_product
        remainder = total % per_product
        
    elif scenario_type == "distribution":
        packs = random.randint(3, 6)
        per_pack = random.randint(8, 15)
        total = packs * per_pack
        per_item = random.randint(3, 6)
        quotient = total // per_item
        remainder = total % per_item
        
    elif scenario_type == "complex_division":
        if "shifts" in scenario.get("template", ""):
            employees = random.randint(40, 80)
            shifts = random.randint(3, 5)
            absent = random.randint(3, 8)
            total = employees - absent
            quotient = total // shifts
            remainder = total % shifts
        else:
            total_collected = random.randint(200, 500)
            reserve = random.randint(20, 50)
            total = total_collected - reserve
            recipients = random.randint(6, 12)
            quotient = total // recipients
            remainder = total % recipients
    
    # Build the problem text
    problem_text = scenario["template"]
    
    # Replace placeholders based on scenario type
    if scenario_type == "sharing_items":
        if "{name}" in scenario["template"]:  # FIXED: Check for {name} instead of "neighborhood"
            # This is the second scenario with names
            name_data = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name_data[0])
            problem_text = problem_text.replace("{pronoun}", name_data[1])
            problem_text = problem_text.replace("{activity}", random.choice(scenario["activities"]))
            
            item_set = random.choice(scenario["items"])
            problem_text = problem_text.replace("{items1}", item_set[0])
            problem_text = problem_text.replace("{items2}", item_set[1])
            problem_text = problem_text.replace("{items_combined}", item_set[2])
            
            # For card game scenario
            if "cards" in item_set[2]:
                problem_text = problem_text.replace("{total}", "52")
                problem_text = problem_text.replace("{extra}", "2")
                problem_text = problem_text.replace("{total_all}", "54")
                total = 54
                divisor = 5
                quotient = 10
                remainder = 4
            else:
                problem_text = problem_text.replace("{total}", str(qty1))
                problem_text = problem_text.replace("{extra}", str(qty2))
                problem_text = problem_text.replace("{total_all}", str(total))
            
            problem_text = problem_text.replace("{action}", random.choice(scenario["actions"]))
            numbers = {"players": divisor}
        else:
            # This is the first scenario with groups
            problem_text = problem_text.replace("{group}", random.choice(scenario["groups"]))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            time_pair = random.choice(scenario["times"])
            problem_text = problem_text.replace("{time1}", time_pair[0])
            problem_text = problem_text.replace("{time2}", time_pair[1])
            problem_text = problem_text.replace("{action}", random.choice(scenario["actions"]))
            problem_text = problem_text.replace("{member}", random.choice(scenario["members"]))
            problem_text = problem_text.replace("{qty1}", str(qty1))
            problem_text = problem_text.replace("{qty2}", str(qty2))
            numbers = {"divisor": divisor}
    
    elif scenario_type == "purchasing":
        if "saving" in scenario["template"]:
            name_data = random.choice(scenario["names"])
            problem_text = problem_text.replace("{name}", name_data[0])
            problem_text = problem_text.replace("{pronoun_cap}", name_data[1])
            problem_text = problem_text.replace("{pronoun_poss}", name_data[2])
            problem_text = problem_text.replace("{pronoun}", name_data[3])
            problem_text = problem_text.replace("{amount}", str(amount))
            problem_text = problem_text.replace("{weeks}", str(weeks))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            problem_text = problem_text.replace("{price}", str(price))
        else:
            problem_text = problem_text.replace("{group}", random.choice(scenario["groups"]))
            problem_text = problem_text.replace("{event}", random.choice(scenario["events"]))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            problem_text = problem_text.replace("{purpose}", random.choice(scenario["purposes"]))
            problem_text = problem_text.replace("{total}", str(total))
            problem_text = problem_text.replace("{price}", str(price))
    
    elif scenario_type == "grouping":
        if "Year" in scenario.get("template", ""):
            problem_text = problem_text.replace("{qty1}", str(qty1))
            problem_text = problem_text.replace("{qty2}", str(qty2))
            problem_text = problem_text.replace("{qty3}", str(qty3))
            problem_text = problem_text.replace("{y1}", str(random.randint(6, 7)))
            problem_text = problem_text.replace("{y2}", str(random.randint(7, 8)))
            problem_text = problem_text.replace("{y3}", str(random.randint(8, 9)))
            problem_text = problem_text.replace("{per_row}", str(per_row))
        else:
            problem_text = problem_text.replace("{venue}", random.choice(scenario["venues"]))
            problem_text = problem_text.replace("{total}", str(total))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            problem_text = problem_text.replace("{event}", random.choice(scenario["events"]))
            problem_text = problem_text.replace("{per_group}", str(per_group))
            container = random.choice(scenario["containers"])
            problem_text = problem_text.replace("{container}", container)
            problem_text = problem_text.replace("{containers}", container + "s")
    
    elif scenario_type == "production":
        if "maker" in scenario.get("template", ""):
            maker_data = random.choice(scenario["makers"])
            problem_text = problem_text.replace("{maker}", maker_data[0])
            problem_text = problem_text.replace("{pronoun_cap}", maker_data[1])
            problem_text = problem_text.replace("{pronoun}", maker_data[2])
            
            colors = random.choice(scenario["colors"])
            problem_text = problem_text.replace("{color1}", colors[0])
            problem_text = problem_text.replace("{color2}", colors[1])
            
            problem_text = problem_text.replace("{qty1}", str(qty1))
            problem_text = problem_text.replace("{qty2}", str(qty2))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            problem_text = problem_text.replace("{action}", random.choice(scenario["actions"]))
            problem_text = problem_text.replace("{products}", random.choice(scenario["products"]))
            problem_text = problem_text.replace("{per_product}", str(per_product))
        else:
            items = random.choice(scenario["items"])
            problem_text = problem_text.replace("{item1}", items[0])
            problem_text = problem_text.replace("{item2}", items[1])
            problem_text = problem_text.replace("{batch1}", str(batch1))
            problem_text = problem_text.replace("{batch2}", str(batch2))
            problem_text = problem_text.replace("{per_box}", str(per_box))
    
    elif scenario_type == "distribution":
        name_data = random.choice(scenario["names"])
        problem_text = problem_text.replace("{name}", name_data[0])
        problem_text = problem_text.replace("{pronoun_poss}", name_data[1])
        problem_text = problem_text.replace("{pronoun}", name_data[2])
        problem_text = problem_text.replace("{pronoun_cap}", name_data[3])
        
        item = random.choice(scenario["items"])
        problem_text = problem_text.replace("{items}", item)
        problem_text = problem_text.replace("{item}", item[:-1])  # Remove 's'
        
        problem_text = problem_text.replace("{location}", random.choice(scenario["locations"]))
        problem_text = problem_text.replace("{supplies}", random.choice(scenario["supplies"]))
        problem_text = problem_text.replace("{packs}", str(packs))
        problem_text = problem_text.replace("{per_pack}", str(per_pack))
        problem_text = problem_text.replace("{per_item}", str(per_item))
    
    elif scenario_type == "complex_division":
        if "shifts" in scenario.get("template", ""):
            problem_text = problem_text.replace("{business}", random.choice(scenario["businesses"]))
            problem_text = problem_text.replace("{employees}", str(employees))
            problem_text = problem_text.replace("{shifts}", str(shifts))
            problem_text = problem_text.replace("{absent}", str(absent))
        else:
            problem_text = problem_text.replace("{organization}", random.choice(scenario["organizations"]))
            problem_text = problem_text.replace("{total}", str(total_collected))
            problem_text = problem_text.replace("{reserve}", str(reserve))
            problem_text = problem_text.replace("{recipients}", str(recipients))
            problem_text = problem_text.replace("{items}", random.choice(scenario["items"]))
            group = random.choice(scenario["groups"])
            problem_text = problem_text.replace("{groups}", group)
            problem_text = problem_text.replace("{group}", group[:-1] if group.endswith('s') else group)
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "answer_type": scenario["answer_type"],
        "quotient": quotient,
        "remainder": remainder,
        "scenario_type": scenario_type
    }
    st.session_state.current_problem = problem_text

def display_remainder_problem():
    """Display the current remainder problem with fill-in-the-blank interface"""
    problem_data = st.session_state.problem_data
    
    # Extract the problem text and sentence to complete
    parts = st.session_state.current_problem.split("\n\nComplete the sentence.\n\n")
    problem_text = parts[0]
    sentence_template = parts[1] if len(parts) > 1 else ""
    
    # Display problem with image placeholder
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <p style="font-size: 16px; line-height: 1.6; margin: 0;">
                {problem_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Image placeholder (you could add actual images based on scenario)
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd;
            border: 2px solid #90caf9;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <span style="font-size: 48px;">
                {get_scenario_emoji(problem_data['scenario_type'])}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Display the sentence completion form
    st.markdown("**Complete the sentence.**")
    
    # Create the fill-in-the-blank interface
    with st.form("answer_form", clear_on_submit=False):
        # Parse the sentence template to create input fields
        if problem_data["answer_type"] == "items_leftover":
            col1, col2, col3 = st.columns([2, 3, 2])
            with col1:
                st.markdown("Each person will get")
            with col2:
                answer1 = st.number_input("", min_value=0, max_value=999, key="answer1", label_visibility="collapsed")
            with col3:
                st.markdown("items, and there will be")
            
            col4, col5 = st.columns([1, 3])
            with col4:
                answer2 = st.number_input("", min_value=0, max_value=99, key="answer2", label_visibility="collapsed")
            with col5:
                st.markdown("left over.")
                
        elif problem_data["answer_type"] == "purchase_money":
            parts = sentence_template.split("[___]")
            st.markdown(parts[0])
            col1, col2 = st.columns([1, 4])
            with col1:
                answer1 = st.number_input("", min_value=0, max_value=999, key="answer1", label_visibility="collapsed")
            with col2:
                st.markdown(parts[1].split(",")[0] + ", and there will be $")
            
            col3, col4 = st.columns([1, 4])
            with col3:
                answer2 = st.number_input("", min_value=0, max_value=999, key="answer2", label_visibility="collapsed")
            with col4:
                st.markdown("left.")
                
        elif problem_data["answer_type"] == "rows_students":
            st.markdown("There will be")
            col1, col2 = st.columns([1, 4])
            with col1:
                answer1 = st.number_input("", min_value=0, max_value=999, key="answer1", label_visibility="collapsed")
            with col2:
                st.markdown("full rows and one last row with only")
            
            col3, col4 = st.columns([1, 4])
            with col3:
                answer2 = st.number_input("", min_value=0, max_value=99, key="answer2", label_visibility="collapsed")
            with col4:
                st.markdown("students.")
                
        else:  # Generic format
            parts = sentence_template.split("[___]")
            if len(parts) >= 3:
                st.markdown(parts[0])
                col1, col2 = st.columns([1, 4])
                with col1:
                    answer1 = st.number_input("", min_value=0, max_value=999, key="answer1", label_visibility="collapsed")
                with col2:
                    st.markdown(parts[1])
                
                col3, col4 = st.columns([1, 4])
                with col3:
                    answer2 = st.number_input("", min_value=0, max_value=999, key="answer2", label_visibility="collapsed")
                with col4:
                    st.markdown(parts[2] if len(parts) > 2 else "")
        
        # Submit button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "Submit", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            st.session_state.user_answers = {
                "answer1": answer1,
                "answer2": answer2
            }
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def get_scenario_emoji(scenario_type):
    """Get an emoji representation for each scenario type"""
    emoji_map = {
        "sharing_items": "🎯",
        "purchasing": "💰",
        "grouping": "👥",
        "production": "🏭",
        "distribution": "📦",
        "complex_division": "🔢"
    }
    return emoji_map.get(scenario_type, "📐")

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answers = st.session_state.user_answers
    correct_quotient = st.session_state.problem_data["quotient"]
    correct_remainder = st.session_state.problem_data["remainder"]
    
    # Check if both answers are correct
    is_correct = (user_answers["answer1"] == correct_quotient and 
                  user_answers["answer2"] == correct_remainder)
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.remainder_difficulty
        st.session_state.remainder_difficulty = min(
            st.session_state.remainder_difficulty + 1, 5
        )
        
        if st.session_state.remainder_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered remainder problems!**")
        elif old_difficulty < st.session_state.remainder_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.remainder_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_quotient} with {correct_remainder} left over.**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.remainder_difficulty
        st.session_state.remainder_difficulty = max(
            st.session_state.remainder_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.remainder_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.remainder_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show detailed explanation of the division"""
    problem_data = st.session_state.problem_data
    quotient = problem_data["quotient"]
    remainder = problem_data["remainder"]
    
    # Calculate total and divisor based on scenario
    total = quotient * get_divisor() + remainder
    divisor = get_divisor()
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Here's how to solve it:")
        
        # Step 1: Find total
        st.markdown(f"**Step 1: Find the total**")
        st.markdown(f"Total items = {total}")
        
        # Step 2: Divide
        st.markdown(f"\n**Step 2: Divide**")
        st.markdown(f"{total} ÷ {divisor} = {quotient} remainder {remainder}")
        
        # Step 3: Check
        st.markdown(f"\n**Step 3: Check our work**")
        st.markdown(f"{quotient} × {divisor} + {remainder} = {quotient * divisor} + {remainder} = {total} ✓")
        
        # Visual representation
        st.markdown("\n**Visual:**")
        st.markdown(f"```")
        st.markdown(f"Total: {'●' * min(total, 50)}{'...' if total > 50 else ''} ({total})")
        st.markdown(f"Groups of {divisor}: " + " | ".join(['●' * divisor for _ in range(min(quotient, 5))]) + 
                   (f"... ({quotient} groups)" if quotient > 5 else ""))
        st.markdown(f"Remainder: {'●' * remainder} ({remainder})")
        st.markdown(f"```")
        
        # Context-specific explanation
        st.markdown("\n### What this means:")
        if problem_data["answer_type"] == "items_leftover":
            st.markdown(f"- Each person gets **{quotient}** items")
            st.markdown(f"- **{remainder}** items are left over")
        elif problem_data["answer_type"] == "purchase_money":
            st.markdown(f"- Can buy **{quotient}** items")
            st.markdown(f"- **${remainder}** left over")
        elif problem_data["answer_type"] == "rows_students":
            st.markdown(f"- **{quotient}** complete rows")
            st.markdown(f"- Last row has only **{remainder}** students")

def get_divisor():
    """Get the divisor from the current problem context"""
    # This is a simplified version - in practice, you'd extract from problem data
    problem_data = st.session_state.problem_data
    
    # You could store the divisor in problem_data during generation
    # For now, we'll use some defaults based on scenario type
    scenario_defaults = {
        "sharing_items": 5,
        "purchasing": 3,
        "grouping": 6,
        "production": 9,
        "distribution": 4,
        "complex_division": 3
    }
    
    return scenario_defaults.get(problem_data["scenario_type"], 4)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answers = {}