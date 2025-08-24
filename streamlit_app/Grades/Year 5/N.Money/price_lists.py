import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Price lists word problems.
    Uses Decimal for exact money calculations.
    """
    # Initialize session state
    if "price_list_difficulty" not in st.session_state:
        st.session_state.price_list_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
        st.session_state.problem_type = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("🛒 Price Lists")
    st.markdown("*Use price lists to solve money problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.price_list_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (2 items, basic operations)",
            2: "Medium (3 items, mixed operations)", 
            3: "Advanced (complex calculations)"
        }
        st.markdown(f"**Current Level:** {difficulty_text[difficulty_level]}")
        progress = (difficulty_level - 1) / 2
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
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
        generate_new_problem()
    
    # Display the problem
    display_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Types of Price List Problems:
        
        **1. Money Left Over**
        - Start with total money
        - Subtract cost of items
        - Find remaining amount
        
        **2. Total Cost**
        - Add up prices of selected items
        - Include all items mentioned
        
        **3. Do I Have Enough?**
        - Add up cost of items
        - Compare to money available
        - Answer yes or no
        
        **4. Price Difference**
        - Find price of each item
        - Subtract smaller from larger
        
        **5. Multi-step Problems**
        - May need to add AND subtract
        - Read carefully!
        
        ### Tips:
        - Always check the price list carefully
        - Add all items mentioned in the question
        - For "money left", subtract from starting amount
        - For "difference", always larger - smaller
        """)

def generate_new_problem():
    """Generate a new price list problem based on difficulty"""
    difficulty = st.session_state.price_list_difficulty
    
    # Define price list scenarios
    scenarios = {
        "clothing": {
            "items": [
                ("blue jumper", 33.35),
                ("pair of boots", 55.95),
                ("winter jacket", 33.60),
                ("red hat", 11.10),
                ("denim jacket", 19.30),
                ("pair of shorts", 23.40),
                ("t-shirt", 15.50),
                ("scarf", 12.75),
                ("gloves", 8.90),
                ("sweater", 42.25)
            ],
            "theme": "clothing store"
        },
        "home": {
            "items": [
                ("navy blue bath mat", 5.85),
                ("flannel sheet", 8.65),
                ("beach blanket", 5.95),
                ("pillow", 9.95),
                ("towel set", 12.50),
                ("curtains", 22.30),
                ("throw cushion", 7.45),
                ("table runner", 15.60),
                ("placemat set", 18.90),
                ("lamp shade", 25.75)
            ],
            "theme": "home goods"
        },
        "art": {
            "items": [
                ("rug", 97.00),
                ("silver coat rack", 91.00),
                ("oil painting", 77.00),
                ("ceramic vase", 82.00),
                ("wall mirror", 65.50),
                ("sculpture", 125.00),
                ("photo frame", 28.75),
                ("canvas print", 45.00),
                ("decorative bowl", 38.50),
                ("art supplies", 52.25)
            ],
            "theme": "art gallery"
        },
        "tools": {
            "items": [
                ("mop", 5.00),
                ("measuring tape", 4.00),
                ("spanner", 5.00),
                ("padlock", 7.00),
                ("bucket", 6.00),
                ("broom", 9.00),
                ("hammer", 12.50),
                ("screwdriver set", 15.75),
                ("pliers", 8.25),
                ("toolbox", 22.00)
            ],
            "theme": "hardware store"
        },
        "office": {
            "items": [
                ("large cardboard box", 1.05),
                ("small red box", 1.10),
                ("piece of bubble wrap", 1.10),
                ("sheet of mountain stamps", 1.05),
                ("roll of packaging tape", 1.00),
                ("sheet of animal stamps", 1.00),
                ("envelope pack", 2.50),
                ("marker set", 4.75),
                ("stapler", 6.90),
                ("file folders", 3.25)
            ],
            "theme": "office supplies"
        }
    }
    
    # Problem types based on difficulty
    if difficulty == 1:
        problem_types = [
            {
                "type": "money_left",
                "template": "{person} has ${total}. How much money will {person} have left if {he_she} buys {item1} and {item2}?",
                "needs": ["person", "total", "item1", "item2"]
            },
            {
                "type": "total_cost",
                "template": "How much money does {person} need to buy {item1} and {item2}?",
                "needs": ["person", "item1", "item2"]
            },
            {
                "type": "price_difference",
                "template": "How much more does a {item1} cost than a {item2}?",
                "needs": ["item1", "item2"]
            }
        ]
    elif difficulty == 2:
        problem_types = [
            {
                "type": "money_left",
                "template": "{person} has ${total}. How much will {he_she} have left after buying {item1}, {item2}, and {item3}?",
                "needs": ["person", "total", "item1", "item2", "item3"]
            },
            {
                "type": "total_cost",
                "template": "How much money does {person} need to buy {item1}, {item2}, and {item3}?",
                "needs": ["person", "item1", "item2", "item3"]
            },
            {
                "type": "enough_money",
                "template": "{person} has ${total}. Does {he_she} have enough to buy {item1} and {item2}?",
                "needs": ["person", "total", "item1", "item2"]
            }
        ]
    else:  # difficulty == 3
        problem_types = [
            {
                "type": "money_left",
                "template": "{person} has ${total}. {He_She} wants to buy {item1}, {item2}, {item3}, and {item4}. How much money will {he_she} have left?",
                "needs": ["person", "total", "item1", "item2", "item3", "item4"]
            },
            {
                "type": "enough_money",
                "template": "{person} has ${total}. Does {he_she} have enough to buy {item1}, {item2}, and {item3}?",
                "needs": ["person", "total", "item1", "item2", "item3"]
            },
            {
                "type": "complex_total",
                "template": "{person} needs to buy 2 {item1}s and 3 {item2}s. How much will this cost in total?",
                "needs": ["person", "item1", "item2"]
            }
        ]
    
    # Select scenario and problem type
    scenario_key = random.choice(list(scenarios.keys()))
    scenario = scenarios[scenario_key]
    problem_type = random.choice(problem_types)
    
    # Generate specific problem
    generate_specific_problem(scenario, problem_type, difficulty)

def generate_specific_problem(scenario, problem_type, difficulty):
    """Generate a specific problem from scenario and type"""
    
    # Names and pronouns
    people_data = [
        ("Steven", "he", "He"),
        ("Mabel", "she", "She"),
        ("Florence", "she", "She"),
        ("Nancy", "she", "She"),
        ("David", "he", "He"),
        ("Emma", "she", "She"),
        ("James", "he", "He"),
        ("Sophie", "she", "She")
    ]
    
    person_data = random.choice(people_data)
    person, he_she, He_She = person_data
    
    # Select items for the problem
    items = scenario["items"]
    selected_items = []
    
    if "item1" in problem_type["needs"]:
        selected_items.append(random.choice(items))
    if "item2" in problem_type["needs"]:
        remaining = [item for item in items if item not in selected_items]
        selected_items.append(random.choice(remaining))
    if "item3" in problem_type["needs"]:
        remaining = [item for item in items if item not in selected_items]
        selected_items.append(random.choice(remaining))
    if "item4" in problem_type["needs"]:
        remaining = [item for item in items if item not in selected_items]
        selected_items.append(random.choice(remaining))
    
    # Generate total money if needed
    if "total" in problem_type["needs"]:
        if problem_type["type"] == "money_left":
            # Ensure they have more than enough
            item_total = sum(item[1] for item in selected_items)
            extra = Decimal(str(random.uniform(20, 100))).quantize(Decimal('0.01'))
            total = (Decimal(str(item_total)) + extra).quantize(Decimal('0.01'))
        elif problem_type["type"] == "enough_money":
            # Sometimes yes, sometimes no
            item_total = sum(item[1] for item in selected_items)
            if random.choice([True, False]):
                # Yes - have enough
                extra = Decimal(str(random.uniform(5, 50))).quantize(Decimal('0.01'))
                total = (Decimal(str(item_total)) + extra).quantize(Decimal('0.01'))
            else:
                # No - don't have enough
                shortage = Decimal(str(random.uniform(5, 30))).quantize(Decimal('0.01'))
                total = (Decimal(str(item_total)) - shortage).quantize(Decimal('0.01'))
    
    # Format the problem
    problem_text = problem_type["template"]
    
    # Replace placeholders
    replacements = {
        "{person}": person,
        "{he_she}": he_she,
        "{He_She}": He_She,
        "{total}": str(total) if "total" in locals() else "",
        "{item1}": f"a {selected_items[0][0]}" if len(selected_items) > 0 else "",
        "{item2}": f"a {selected_items[1][0]}" if len(selected_items) > 1 else "",
        "{item3}": f"a {selected_items[2][0]}" if len(selected_items) > 2 else "",
        "{item4}": f"a {selected_items[3][0]}" if len(selected_items) > 3 else ""
    }
    
    for key, value in replacements.items():
        problem_text = problem_text.replace(key, value)
    
    # Calculate answer based on problem type
    if problem_type["type"] == "money_left":
        item_cost = sum(Decimal(str(item[1])) for item in selected_items)
        answer = total - item_cost
        answer = answer.quantize(Decimal('0.01'))
    elif problem_type["type"] == "total_cost":
        answer = sum(Decimal(str(item[1])) for item in selected_items)
        answer = answer.quantize(Decimal('0.01'))
    elif problem_type["type"] == "price_difference":
        price1 = Decimal(str(selected_items[0][1]))
        price2 = Decimal(str(selected_items[1][1]))
        answer = abs(price1 - price2)
        answer = answer.quantize(Decimal('0.01'))
    elif problem_type["type"] == "enough_money":
        item_cost = sum(Decimal(str(item[1])) for item in selected_items)
        answer = "yes" if total >= item_cost else "no"
    elif problem_type["type"] == "complex_total":
        # 2 of first item, 3 of second item
        price1 = Decimal(str(selected_items[0][1]))
        price2 = Decimal(str(selected_items[1][1]))
        answer = (2 * price1 + 3 * price2).quantize(Decimal('0.01'))
    
    # Store problem data
    st.session_state.problem_data = {
        'problem': problem_text,
        'answer': answer,
        'type': problem_type["type"],
        'items': selected_items,
        'all_items': items,
        'total': total if "total" in locals() else None,
        'difficulty': difficulty
    }
    st.session_state.current_problem = problem_text
    st.session_state.problem_type = problem_type["type"]

def display_problem():
    """Display the problem with price list"""
    data = st.session_state.problem_data
    
    # Display the problem
    st.markdown(f"""
    <div style="
        background-color: #f9f9f9;
        padding: 15px 20px;
        border-radius: 5px;
        margin: 20px 0;
        font-size: 16px;
        line-height: 1.5;
    ">
        {data['problem']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display the price list
    st.markdown("### Price List:")
    
    # Create price list table
    if data['type'] == 'enough_money':
        # Pink background for yes/no questions
        table_style = """
        <style>
        .price-table {
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
        }
        .price-table td {
            padding: 8px 15px;
            border-bottom: 1px solid #ddd;
            background-color: #ffe6f2;
        }
        .price-table td:first-child {
            text-align: left;
            width: 70%;
        }
        .price-table td:last-child {
            text-align: right;
            font-weight: bold;
        }
        </style>
        """
    else:
        # Blue background for other questions
        table_style = """
        <style>
        .price-table {
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
        }
        .price-table td {
            padding: 8px 15px;
            border-bottom: 1px solid #ddd;
            background-color: #e6f3ff;
        }
        .price-table td:first-child {
            text-align: left;
            width: 70%;
        }
        .price-table td:last-child {
            text-align: right;
            font-weight: bold;
        }
        </style>
        """
    
    st.markdown(table_style, unsafe_allow_html=True)
    
    # Show 6-8 items from the list including the ones needed
    all_items = data['all_items']
    needed_items = data['items']
    
    # Ensure needed items are in the display
    display_items = needed_items.copy()
    
    # Add random other items
    other_items = [item for item in all_items if item not in needed_items]
    random.shuffle(other_items)
    
    # Add items until we have 6-8
    target_count = random.randint(6, 8)
    while len(display_items) < target_count and len(other_items) > 0:
        display_items.append(other_items.pop(0))
    
    # Shuffle the display items
    random.shuffle(display_items)
    
    # Create table HTML
    table_html = '<table class="price-table">'
    for item_name, price in display_items:
        table_html += f'<tr><td>{item_name}</td><td>${price:.2f}</td></tr>'
    table_html += '</table>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if data['type'] == 'enough_money':
            # Yes/No buttons
            st.markdown("")
            cols = st.columns(2)
            with cols[0]:
                if st.button("yes", type="primary", use_container_width=True):
                    st.session_state.user_answer = "yes"
                    check_answer()
            with cols[1]:
                if st.button("no", type="primary", use_container_width=True):
                    st.session_state.user_answer = "no"
                    check_answer()
        else:
            # Dollar amount input
            input_cols = st.columns([0.5, 5])
            
            with input_cols[0]:
                st.markdown("### $")
            
            with input_cols[1]:
                user_answer = st.text_input(
                    "Your answer:",
                    value=st.session_state.user_answer,
                    key="answer_input",
                    placeholder="",
                    label_visibility="collapsed"
                )
                st.session_state.user_answer = user_answer
            
            # Submit button
            st.markdown("")
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
        
        # Show feedback
        if st.session_state.show_feedback:
            show_feedback()
        
        # Next question button
        if st.session_state.answer_submitted:
            st.markdown("")
            if st.button("Next Problem →", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def check_answer():
    """Check the user's answer"""
    data = st.session_state.problem_data
    
    if data['type'] == 'enough_money':
        # Yes/No answer
        user_answer = st.session_state.user_answer
        correct = (user_answer == data['answer'])
    else:
        # Numeric answer
        user_input = st.session_state.user_answer.strip()
        
        # Remove dollar sign if present
        if user_input.startswith('$'):
            user_input = user_input[1:]
        
        try:
            user_answer = Decimal(user_input).quantize(Decimal('0.01'))
            correct = (user_answer == data['answer'])
        except:
            st.error("⚠️ Please enter a valid amount")
            return
    
    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True
    st.session_state.user_correct = correct
    
    # Update difficulty
    if correct:
        st.session_state.consecutive_correct += 1
        if st.session_state.consecutive_correct >= 3:
            st.session_state.price_list_difficulty = min(
                st.session_state.price_list_difficulty + 1, 3
            )
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        if st.session_state.price_list_difficulty > 1:
            st.session_state.price_list_difficulty -= 1

def show_feedback():
    """Display feedback with solution"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Great job!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.price_list_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting harder.**")
    else:
        if data['type'] == 'enough_money':
            st.error(f"❌ **Not quite. The correct answer is {data['answer']}**")
        else:
            st.error(f"❌ **Not quite. The correct answer is ${data['answer']}**")
        
        # Show solution
        with st.expander("📖 **See the solution**", expanded=True):
            st.markdown("### Step-by-step solution:")
            
            # Show items and prices
            st.markdown("**Items to buy:**")
            total_cost = Decimal('0')
            for item_name, price in data['items']:
                st.markdown(f"• {item_name}: ${price}")
                total_cost += Decimal(str(price))
            
            st.markdown("")
            
            # Show calculation based on problem type
            if data['type'] == 'money_left':
                st.markdown("**Calculation:**")
                st.markdown(f"1. Total cost of items: ${total_cost}")
                st.markdown(f"2. Money Steven has: ${data['total']}")
                st.markdown(f"3. Money left: ${data['total']} - ${total_cost} = ${data['answer']}")
                
            elif data['type'] == 'total_cost':
                st.markdown("**Calculation:**")
                price_str = " + ".join([f"${item[1]}" for item in data['items']])
                st.markdown(f"Total needed: {price_str} = ${data['answer']}")
                
            elif data['type'] == 'price_difference':
                item1_name, price1 = data['items'][0]
                item2_name, price2 = data['items'][1]
                larger_price = max(price1, price2)
                smaller_price = min(price1, price2)
                st.markdown("**Calculation:**")
                st.markdown(f"1. {item1_name}: ${price1}")
                st.markdown(f"2. {item2_name}: ${price2}")
                st.markdown(f"3. Difference: ${larger_price} - ${smaller_price} = ${data['answer']}")
                
            elif data['type'] == 'enough_money':
                st.markdown("**Calculation:**")
                st.markdown(f"1. Total cost: ${total_cost}")
                st.markdown(f"2. Money available: ${data['total']}")
                if data['answer'] == 'yes':
                    st.markdown(f"3. ${data['total']} ≥ ${total_cost}, so **YES**")
                else:
                    st.markdown(f"3. ${data['total']} < ${total_cost}, so **NO**")
                    shortage = total_cost - data['total']
                    st.markdown(f"   (Short by ${shortage})")
                    
            elif data['type'] == 'complex_total':
                item1_name, price1 = data['items'][0]
                item2_name, price2 = data['items'][1]
                st.markdown("**Calculation:**")
                st.markdown(f"1. 2 × {item1_name} = 2 × ${price1} = ${2 * Decimal(str(price1))}")
                st.markdown(f"2. 3 × {item2_name} = 3 × ${price2} = ${3 * Decimal(str(price2))}")
                st.markdown(f"3. Total: ${2 * Decimal(str(price1))} + ${3 * Decimal(str(price2))} = ${data['answer']}")
            
            st.markdown("")
            if data['type'] == 'enough_money':
                st.markdown(f"**Answer: {data['answer']}**")
            else:
                st.markdown(f"**Answer: ${data['answer']}**")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""
    st.session_state.problem_type = None