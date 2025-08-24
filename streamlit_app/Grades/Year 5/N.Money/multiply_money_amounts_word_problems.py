import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Multiply money amounts: word problems.
    Uses Decimal for exact money calculations.
    """
    # Initialize session state
    if "multiply_difficulty" not in st.session_state:
        st.session_state.multiply_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("✖️ Multiply Money Amounts: Word Problems")
    st.markdown("*Solve multiplication problems with money*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.multiply_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (single-digit × whole dollar)",
            2: "Medium (larger numbers, decimals)", 
            3: "Advanced (multi-step, complex)"
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
        ### How to Solve:
        
        **Step 1: Identify the information**
        - How many items?
        - Cost per item?
        - What are we finding?
        
        **Step 2: Set up the multiplication**
        - Quantity × Price per item = Total cost
        - Write it clearly
        
        **Step 3: Calculate carefully**
        - Multiply the numbers
        - Don't forget the decimal point
        - Check your answer makes sense
        
        ### Problem Types:
        - **🟢 Easy:** Small quantities × whole dollar amounts
        - **🟡 Medium:** Larger quantities × prices with cents
        - **🔴 Hard:** Multi-step problems, bulk pricing, discounts
        
        ### Tips:
        - Read the problem twice
        - Write down what you know
        - Estimate first to check your answer
        - Always include the dollar sign ($)
        """)

def generate_new_problem():
    """Generate a new multiplication word problem based on difficulty"""
    difficulty = st.session_state.multiply_difficulty
    
    if difficulty == 1:  # Easy - simple multiplication
        scenarios = [
            # Basic multiplication - whole dollars
            {
                "template": "How much does it cost to buy {quantity} {items} that cost ${price} apiece?",
                "items": [
                    ("magazines", 5),
                    ("books", 8),
                    ("notebooks", 3),
                    ("pens", 2),
                    ("folders", 4),
                    ("markers", 6),
                    ("calendars", 7),
                    ("posters", 9)
                ],
                "quantities": [2, 3, 4, 5, 6, 7, 8, 9],
                "type": "basic"
            },
            {
                "template": "How much does it cost to buy {quantity} {items} if each {item} costs ${price}?",
                "items": [
                    ("storage bins", "storage bin", 8),
                    ("picture frames", "picture frame", 12),
                    ("plant pots", "plant pot", 6),
                    ("towels", "towel", 10),
                    ("pillows", "pillow", 15),
                    ("lamps", "lamp", 20)
                ],
                "quantities": [2, 3, 4, 5],
                "type": "basic_each"
            },
            {
                "template": "A {item} costs ${price}. How much would it cost to buy {quantity} {items}?",
                "items": [
                    ("candle holder", "candle holders", 10),
                    ("picture frame", "picture frames", 12),
                    ("coffee mug", "coffee mugs", 8),
                    ("notebook", "notebooks", 5),
                    ("water bottle", "water bottles", 15),
                    ("lunch box", "lunch boxes", 20)
                ],
                "quantities": [2, 3, 4, 5, 6],
                "type": "item_first"
            },
            {
                "template": "A package of {item} costs ${price}. If {person} buys {quantity} packages of {item}, how much will it cost?",
                "items": [
                    ("chocolate biscuits", 4),
                    ("cookies", 3),
                    ("crackers", 5),
                    ("fruit snacks", 6),
                    ("granola bars", 8),
                    ("juice boxes", 10)
                ],
                "people": ["Katy", "James", "Sofia", "Miguel", "Emma", "Ryan"],
                "quantities": [2, 3, 4, 5],
                "type": "package"
            },
            {
                "template": "{person} buys {quantity} {items}. Each {item} costs ${price}. How much does {person} spend?",
                "items": [
                    ("houseplants", "houseplant", 10),
                    ("succulents", "succulent", 5),
                    ("flower pots", "flower pot", 8),
                    ("gardening tools", "gardening tool", 12),
                    ("seed packets", "seed packet", 3),
                    ("watering cans", "watering can", 15)
                ],
                "people": ["Dale", "Maya", "Alex", "Zoe", "Noah", "Lily"],
                "quantities": [3, 4, 5, 6, 7, 8],
                "type": "person_buy"
            }
        ]
        
    elif difficulty == 2:  # Medium - decimals and larger numbers
        scenarios = [
            {
                "template": "{person} needs to buy {quantity} {items} for a party. Each {item} costs ${price}. What is the total cost?",
                "items": [
                    ("paper plates", "paper plate", 2.50),
                    ("plastic cups", "plastic cup", 1.75),
                    ("napkins", "napkin", 3.25),
                    ("party hats", "party hat", 4.50),
                    ("balloons", "balloon", 0.75),
                    ("streamers", "streamer", 5.99)
                ],
                "people": ["Sarah", "David", "Maria", "Chris", "Anna", "Ben"],
                "quantities": [12, 15, 20, 24, 25, 30],
                "type": "party"
            },
            {
                "template": "A {place} sells {items} for ${price} each. How much would {quantity} {items} cost?",
                "places": ["bakery", "cafe", "restaurant", "food truck", "deli"],
                "items": [
                    ("muffins", "muffin", 3.50),
                    ("sandwiches", "sandwich", 6.75),
                    ("salads", "salad", 8.25),
                    ("smoothies", "smoothie", 4.99),
                    ("wraps", "wrap", 7.50),
                    ("pizzas", "pizza", 12.99)
                ],
                "quantities": [6, 8, 10, 12, 15],
                "type": "food"
            },
            {
                "template": "The school is ordering {quantity} {items} for the classroom. If each {item} costs ${price}, what is the total bill?",
                "items": [
                    ("calculators", "calculator", 15.99),
                    ("dictionaries", "dictionary", 12.50),
                    ("textbooks", "textbook", 24.75),
                    ("whiteboards", "whiteboard", 8.95),
                    ("desk organizers", "desk organizer", 6.49),
                    ("pencil cases", "pencil case", 4.25)
                ],
                "quantities": [20, 25, 30, 35, 40],
                "type": "school"
            },
            {
                "template": "{person} is buying supplies for their business. They need {quantity} {items} at ${price} per {item}. How much will they spend?",
                "items": [
                    ("printer cartridges", "cartridge", 32.50),
                    ("reams of paper", "ream", 8.99),
                    ("boxes of pens", "box", 12.75),
                    ("staplers", "stapler", 15.49),
                    ("file folders", "folder", 0.89),
                    ("notebooks", "notebook", 3.25)
                ],
                "people": ["Mr. Johnson", "Ms. Smith", "Dr. Brown", "Mrs. Davis"],
                "quantities": [15, 24, 36, 48, 50],
                "type": "business"
            }
        ]
        
    else:  # Hard - multi-step and complex scenarios
        scenarios = [
            {
                "template": "{person} is organizing a fundraiser. They're selling {items} for ${price} each. If they sell {quantity} {items}, how much money will they raise?",
                "items": [
                    ("raffle tickets", 2.50),
                    ("cupcakes", 3.00),
                    ("t-shirts", 15.00),
                    ("wristbands", 5.00),
                    ("calendars", 12.00),
                    ("cookie boxes", 8.50)
                ],
                "people": ["The student council", "The PTA", "The sports team", "The drama club"],
                "quantities": [125, 150, 200, 250, 300],
                "type": "fundraiser"
            },
            {
                "template": "A {place} offers a bulk discount: {items} cost ${price} each when you buy {min_qty} or more. {person} buys {quantity}. How much does {person} pay?",
                "items": [
                    ("notebooks", 3.25, 20),
                    ("water bottles", 8.50, 10),
                    ("lunch boxes", 12.00, 15),
                    ("backpacks", 24.99, 5),
                    ("pencil sets", 4.75, 25)
                ],
                "places": ["store", "warehouse", "supplier"],
                "people": ["The teacher", "The coach", "The principal"],
                "quantities": [25, 30, 40, 50],
                "type": "bulk"
            },
            {
                "template": "{person} runs a small business making {items}. Materials for each {item} cost ${material_cost}, and they sell each for ${sell_price}. If they make and sell {quantity} {items}, what is their total revenue?",
                "items": [
                    ("bracelets", "bracelet", 2.50, 8.00),
                    ("keychains", "keychain", 1.75, 5.50),
                    ("bookmarks", "bookmark", 0.50, 3.00),
                    ("candles", "candle", 3.25, 12.00),
                    ("soap bars", "soap bar", 1.50, 6.00)
                ],
                "people": ["Emma", "Jake", "Sophia", "Lucas"],
                "quantities": [75, 100, 120, 150],
                "type": "business_revenue"
            },
            {
                "template": "A catering company charges ${price} per person for events. They're catering a {event} for {quantity} people. What is the total catering cost?",
                "price_ranges": [(12.50, 15.99), (18.75, 22.50), (25.00, 35.00)],
                "events": ["wedding", "birthday party", "corporate lunch", "graduation party", "anniversary dinner"],
                "quantities": [85, 120, 150, 200, 250],
                "type": "catering"
            },
            {
                "template": "The {team} is ordering new uniforms. Each complete uniform (jersey and shorts) costs ${price}. If they need uniforms for {quantity} players, what's the total cost?",
                "teams": ["soccer team", "basketball team", "volleyball team", "baseball team"],
                "prices": [45.50, 52.75, 38.99, 64.25],
                "quantities": [18, 22, 25, 30, 35],
                "type": "uniforms"
            }
        ]
    
    # Select and generate specific problem
    scenario = random.choice(scenarios)
    generate_specific_problem(scenario, difficulty)

def generate_specific_problem(scenario, difficulty):
    """Generate a specific problem from the scenario template"""
    data = {}
    
    if difficulty == 1:  # Easy problems
        if scenario["type"] == "basic":
            item_data = random.choice(scenario["items"])
            items, price = item_data
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                quantity=quantity,
                items=items,
                price=price
            )
            answer = Decimal(str(quantity * price))
            
        elif scenario["type"] == "basic_each":
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                quantity=quantity,
                items=items,
                item=item,
                price=price
            )
            answer = Decimal(str(quantity * price))
            
        elif scenario["type"] == "item_first":
            item_data = random.choice(scenario["items"])
            item, items, price = item_data
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                item=item,
                items=items,
                price=price,
                quantity=quantity
            )
            answer = Decimal(str(quantity * price))
            
        elif scenario["type"] == "package":
            item_data = random.choice(scenario["items"])
            item, price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                item=item,
                price=price,
                person=person,
                quantity=quantity
            )
            answer = Decimal(str(quantity * price))
            
        elif scenario["type"] == "person_buy":
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                person=person,
                quantity=quantity,
                items=items,
                item=item,
                price=price
            )
            answer = Decimal(str(quantity * price))
    
    elif difficulty == 2:  # Medium problems
        if scenario["type"] == "party":
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                person=person,
                quantity=quantity,
                items=items,
                item=item,
                price=price
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
            
        elif scenario["type"] == "food":
            place = random.choice(scenario["places"])
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                place=place,
                items=items,
                item=item,
                price=price,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
            
        elif scenario["type"] == "school":
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                quantity=quantity,
                items=items,
                item=item,
                price=price
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
            
        elif scenario["type"] == "business":
            item_data = random.choice(scenario["items"])
            items, item, price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                person=person,
                quantity=quantity,
                items=items,
                item=item,
                price=price
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
    
    else:  # Hard problems
        if scenario["type"] == "fundraiser":
            item_data = random.choice(scenario["items"])
            items, price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                person=person,
                items=items,
                price=price,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
            
        elif scenario["type"] == "bulk":
            item_data = random.choice(scenario["items"])
            items, price, min_qty = item_data
            place = random.choice(scenario["places"])
            person = random.choice(scenario["people"])
            quantity = random.choice([q for q in scenario["quantities"] if q >= min_qty])
            
            problem = scenario["template"].format(
                place=place,
                items=items,
                price=price,
                min_qty=min_qty,
                person=person,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * Decimal(str(price))
            
        elif scenario["type"] == "business_revenue":
            item_data = random.choice(scenario["items"])
            items, item, material_cost, sell_price = item_data
            person = random.choice(scenario["people"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                person=person,
                items=items,
                item=item,
                material_cost=material_cost,
                sell_price=sell_price,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * Decimal(str(sell_price))
            
        elif scenario["type"] == "catering":
            price_range = random.choice(scenario["price_ranges"])
            price = Decimal(str(random.uniform(*price_range))).quantize(Decimal('0.01'))
            event = random.choice(scenario["events"])
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                price=price,
                event=event,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * price
            
        elif scenario["type"] == "uniforms":
            team = random.choice(scenario["teams"])
            price = Decimal(str(random.choice(scenario["prices"])))
            quantity = random.choice(scenario["quantities"])
            
            problem = scenario["template"].format(
                team=team,
                price=price,
                quantity=quantity
            )
            answer = Decimal(str(quantity)) * price
    
    # Round answer to 2 decimal places
    answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    st.session_state.problem_data = {
        'problem': problem,
        'answer': answer,
        'quantity': quantity,
        'price': price if 'price' in locals() else 0,
        'difficulty': difficulty
    }
    st.session_state.current_problem = problem

def display_problem():
    """Display the word problem with input field"""
    data = st.session_state.problem_data
    
    # Display the problem in a nice box
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 20px 0;
        font-size: 18px;
    ">
        {data['problem']}
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create input with dollar sign
        input_col1, input_col2 = st.columns([0.5, 5])
        
        with input_col1:
            st.markdown("### $")
        
        with input_col2:
            user_answer = st.text_input(
                "Your answer:",
                value=st.session_state.user_answer,
                key="answer_input",
                placeholder="0.00",
                label_visibility="collapsed"
            )
            st.session_state.user_answer = user_answer
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True):
            check_answer()
        
        # Show feedback
        if st.session_state.show_feedback:
            show_feedback()
        
        # Next question button
        if st.session_state.answer_submitted:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def check_answer():
    """Check the user's answer"""
    data = st.session_state.problem_data
    user_input = st.session_state.user_answer.strip()
    
    # Remove dollar sign if present
    if user_input.startswith('$'):
        user_input = user_input[1:]
    
    try:
        # Convert to Decimal and round
        user_answer = Decimal(user_input).quantize(Decimal('0.01'))
        correct_answer = data['answer']
        
        # Check if correct
        correct = (user_answer == correct_answer)
        
        st.session_state.answer_submitted = True
        st.session_state.show_feedback = True
        st.session_state.user_correct = correct
        
        # Update difficulty
        if correct:
            st.session_state.consecutive_correct += 1
            if st.session_state.consecutive_correct >= 3:
                st.session_state.multiply_difficulty = min(st.session_state.multiply_difficulty + 1, 3)
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            if st.session_state.multiply_difficulty > 1:
                st.session_state.multiply_difficulty -= 1
                
    except:
        st.error("⚠️ Please enter a valid amount (e.g., 45.00 or 45)")
        return

def show_feedback():
    """Display feedback with solution"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.multiply_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting more challenging.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is ${data['answer']}**")
        
        # Show solution
        with st.expander("📖 **See the solution**", expanded=True):
            st.markdown("### How to solve this problem:")
            
            # Show the problem again
            st.markdown(f"**Problem:** {data['problem']}")
            st.markdown("")
            
            # Show calculation based on difficulty
            if data['difficulty'] == 1:
                st.markdown("**Solution:**")
                st.markdown(f"• Quantity: {data['quantity']}")
                st.markdown(f"• Price per item: ${data['price']}")
                st.markdown(f"• Calculation: {data['quantity']} × ${data['price']} = ${data['answer']}")
                
            elif data['difficulty'] == 2:
                st.markdown("**Step-by-step solution:**")
                st.markdown(f"1. Identify the quantity: **{data['quantity']} items**")
                st.markdown(f"2. Identify the price per item: **${data['price']}**")
                st.markdown(f"3. Multiply: **{data['quantity']} × ${data['price']}**")
                
                # Show work for decimal multiplication
                if '.' in str(data['price']):
                    st.markdown(f"4. Work:")
                    st.markdown(f"   - {data['quantity']} × {data['price']} = {data['answer']}")
                    
                st.markdown(f"\n**Answer: ${data['answer']}**")
                
            else:  # Hard problems
                st.markdown("**Detailed solution:**")
                st.markdown(f"1. Read carefully to identify:")
                st.markdown(f"   - Quantity: **{data['quantity']}**")
                st.markdown(f"   - Price per unit: **${data['price']}**")
                st.markdown(f"2. Set up the multiplication:")
                st.markdown(f"   - {data['quantity']} × ${data['price']}")
                st.markdown(f"3. Calculate:")
                st.markdown(f"   - {data['quantity']} × {data['price']} = **{data['answer']}**")
                st.markdown(f"\n**Final answer: ${data['answer']}**")
            
            # Add tips
            st.markdown("---")
            st.info("💡 **Remember:** Always check if your answer makes sense. Estimate first!")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""