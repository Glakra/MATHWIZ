import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Multiply money amounts with decimals: word problems.
    Uses Decimal for exact money calculations with cents.
    """
    # Initialize session state
    if "decimal_multiply_difficulty" not in st.session_state:
        st.session_state.decimal_multiply_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("💰 Multiply Money Amounts with Decimals: Word Problems")
    st.markdown("*Multiply decimal amounts in real-world situations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_multiply_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (small quantities, round cents)",
            2: "Medium (larger quantities, any cents)", 
            3: "Advanced (complex decimals, larger numbers)"
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
        ### How to Multiply Money with Decimals:
        
        **Step 1: Set up the problem**
        - Identify the quantity (how many)
        - Identify the price (cost per item)
        - Write: Quantity × Price = Total
        
        **Step 2: Multiply carefully**
        - Multiply as if there's no decimal
        - Count decimal places in the price
        - Put decimal in the answer
        
        **Example:**
        - 5 × $0.43 = ?
        - 5 × 43 = 215
        - $0.43 has 2 decimal places
        - Answer: $2.15
        
        ### Difficulty Levels:
        - **🟢 Easy:** Small quantities (2-10), prices ending in 0 or 5
        - **🟡 Medium:** Larger quantities (10-25), any cent amounts
        - **🔴 Hard:** Large quantities (25-100), complex decimals
        
        ### Tips:
        - Line up decimals in your work
        - Check: Does the answer make sense?
        - Remember: 100 cents = $1.00
        """)

def generate_new_problem():
    """Generate a new decimal multiplication problem based on difficulty"""
    difficulty = st.session_state.decimal_multiply_difficulty
    
    if difficulty == 1:  # Easy - simple decimals, small quantities
        # Template variations matching the examples
        templates = [
            {
                "format": "If a {item} costs ${price}, how much would {quantity} {items} cost?",
                "type": "if_cost"
            },
            {
                "format": "A {item} costs ${price}. {person} bought {quantity} {items}. How much did {person} spend in all?",
                "type": "person_bought"
            },
            {
                "format": "{person} bought {quantity} {items}. Each {item_singular} cost ${price}. How much money did {person} spend?",
                "type": "bought_each"
            },
            {
                "format": "If a {item} costs ${price}, how much would it cost to buy {quantity} {items}?",
                "type": "if_buy"
            },
            {
                "format": "How much does it cost to buy {quantity} {items} if each {item_singular} costs ${price}?",
                "type": "how_much_each"
            }
        ]
        
        # Items with prices ending in 0 or 5 for easy level
        items = [
            ("shiny key chain", "shiny key chains", "shiny key chain", 0.90),
            ("plastic bracelet", "plastic bracelets", "plastic bracelet", 0.45),
            ("rubber stamp", "rubber stamps", "rubber stamp", 0.40),
            ("pencil", "pencils", "pencil", 0.35),
            ("eraser", "erasers", "eraser", 0.25),
            ("bookmark", "bookmarks", "bookmark", 0.50),
            ("sticker", "stickers", "sticker", 0.15),
            ("paper clip", "paper clips", "paper clip", 0.05),
            ("button", "buttons", "button", 0.20),
            ("marble", "marbles", "marble", 0.30),
            ("toy car", "toy cars", "toy car", 0.85),
            ("bouncy ball", "bouncy balls", "bouncy ball", 0.75)
        ]
        
        # Small quantities for easy level
        quantities = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        
    elif difficulty == 2:  # Medium - any cents, larger quantities
        templates = [
            {
                "format": "A {item} costs ${price}. {person} bought {quantity} {items}. How much did {person} spend?",
                "type": "person_bought"
            },
            {
                "format": "{person} needs {quantity} {items} for a project. Each {item_singular} costs ${price}. What is the total cost?",
                "type": "project"
            },
            {
                "format": "At the store, {items} cost ${price} each. How much would {quantity} {items} cost?",
                "type": "store"
            },
            {
                "format": "If one {item} costs ${price}, what is the cost of {quantity} {items}?",
                "type": "one_costs"
            },
            {
                "format": "{person} is buying {quantity} {items}. If each costs ${price}, how much will {person} pay?",
                "type": "buying_pay"
            }
        ]
        
        # Items with any cent amounts
        items = [
            ("box of breath mints", "boxes of breath mints", "box", 0.95),
            ("pack of gum", "packs of gum", "pack", 0.38),
            ("candy bar", "candy bars", "candy bar", 0.67),
            ("juice box", "juice boxes", "juice box", 0.89),
            ("fruit snack", "fruit snacks", "fruit snack", 0.42),
            ("granola bar", "granola bars", "granola bar", 0.73),
            ("small notebook", "small notebooks", "notebook", 0.58),
            ("pen refill", "pen refills", "refill", 0.29),
            ("glue stick", "glue sticks", "glue stick", 0.84),
            ("tape roll", "tape rolls", "roll", 0.96),
            ("index card pack", "index card packs", "pack", 0.51),
            ("paper folder", "paper folders", "folder", 0.76)
        ]
        
        # Larger quantities
        quantities = [8, 10, 12, 15, 18, 20, 24, 25]
        
    else:  # Hard - complex decimals, very large quantities
        templates = [
            {
                "format": "The school cafeteria sells {items} for ${price} each. If they sold {quantity} today, how much money did they collect?",
                "type": "cafeteria"
            },
            {
                "format": "A charity is selling {items} for ${price} each. They sold {quantity} {items}. What was their total revenue?",
                "type": "charity"
            },
            {
                "format": "{person} owns a store that sells {items} for ${price} per unit. Last week, {quantity} units were sold. Calculate the total sales.",
                "type": "store_owner"
            },
            {
                "format": "For a fundraiser, students are selling {items} at ${price} each. If {quantity} were sold, what is the total amount raised?",
                "type": "fundraiser"
            },
            {
                "format": "A vending machine charges ${price} for {items}. If {quantity} {items} were purchased yesterday, how much money was collected?",
                "type": "vending"
            }
        ]
        
        # Items with complex prices
        items = [
            ("chocolate chip cookie", "chocolate chip cookies", "cookie", 0.37),
            ("lollipop", "lollipops", "lollipop", 0.23),
            ("trading card", "trading cards", "card", 0.94),
            ("small toy", "small toys", "toy", 0.68),
            ("raffle ticket", "raffle tickets", "ticket", 0.17),
            ("carnival token", "carnival tokens", "token", 0.82),
            ("game ticket", "game tickets", "ticket", 0.49),
            ("prize coupon", "prize coupons", "coupon", 0.71),
            ("activity pass", "activity passes", "pass", 0.86),
            ("snack voucher", "snack vouchers", "voucher", 0.54),
            ("drink ticket", "drink tickets", "ticket", 0.91),
            ("ride token", "ride tokens", "token", 0.63)
        ]
        
        # Very large quantities
        quantities = [35, 40, 45, 50, 60, 75, 80, 100]
    
    # Select template and generate problem
    template = random.choice(templates)
    item_data = random.choice(items)
    quantity = random.choice(quantities)
    
    # Names for personalization
    people = ["Katie", "Stanley", "Maria", "James", "Sophie", "Michael", 
              "Emma", "David", "Lily", "Ryan", "Zoe", "Alex"]
    
    # Generate the specific problem
    generate_specific_problem(template, item_data, quantity, people, difficulty)

def generate_specific_problem(template, item_data, quantity, people, difficulty):
    """Generate a specific problem from template"""
    item_singular, item_plural, item_short, price = item_data
    person = random.choice(people)
    
    # Format the problem based on template type
    if template["type"] == "if_cost":
        problem = template["format"].format(
            item=item_singular,
            items=item_plural,
            price=price,
            quantity=quantity
        )
    elif template["type"] == "person_bought":
        problem = template["format"].format(
            item=item_singular,
            items=item_plural,
            price=price,
            quantity=quantity,
            person=person
        )
    elif template["type"] == "bought_each":
        # Special case for boxes/packs
        if "box" in item_singular or "pack" in item_singular:
            item_text = item_plural
            each_text = item_singular
        else:
            item_text = item_plural
            each_text = item_short
        
        problem = template["format"].format(
            person=person,
            quantity=quantity,
            items=item_text,
            item_singular=each_text,
            price=price
        )
    elif template["type"] in ["if_buy", "how_much_each", "one_costs"]:
        problem = template["format"].format(
            item=item_singular,
            items=item_plural,
            item_singular=item_short,
            price=price,
            quantity=quantity
        )
    elif template["type"] in ["project", "buying_pay"]:
        problem = template["format"].format(
            person=person,
            quantity=quantity,
            items=item_plural,
            item_singular=item_short,
            price=price
        )
    elif template["type"] == "store":
        problem = template["format"].format(
            items=item_plural,
            price=price,
            quantity=quantity
        )
    elif template["type"] in ["cafeteria", "charity", "fundraiser", "vending"]:
        problem = template["format"].format(
            items=item_plural,
            price=price,
            quantity=quantity
        )
    elif template["type"] == "store_owner":
        problem = template["format"].format(
            person=person,
            items=item_plural,
            price=price,
            quantity=quantity
        )
    
    # Calculate answer
    price_decimal = Decimal(str(price))
    answer = price_decimal * quantity
    answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    st.session_state.problem_data = {
        'problem': problem,
        'answer': answer,
        'quantity': quantity,
        'price': price_decimal,
        'item': item_singular,
        'difficulty': difficulty
    }
    st.session_state.current_problem = problem

def display_problem():
    """Display the word problem with input field"""
    data = st.session_state.problem_data
    
    # Display the problem in a box matching the style
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
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create input with dollar sign
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
        st.markdown("")  # Add spacing
        if st.button("Submit", type="primary", use_container_width=True):
            check_answer()
        
        # Show feedback
        if st.session_state.show_feedback:
            show_feedback()
        
        # Next question button
        if st.session_state.answer_submitted:
            st.markdown("")  # Add spacing
            if st.button("Next Problem →", type="secondary", use_container_width=True):
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
                st.session_state.decimal_multiply_difficulty = min(
                    st.session_state.decimal_multiply_difficulty + 1, 3
                )
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            if st.session_state.decimal_multiply_difficulty > 1:
                st.session_state.decimal_multiply_difficulty -= 1
                
    except:
        st.error("⚠️ Please enter a valid amount (numbers only)")
        return

def show_feedback():
    """Display feedback with solution"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Great job!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.decimal_multiply_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting harder.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is ${data['answer']}**")
        
        # Show solution
        with st.expander("📖 **See how to solve it**", expanded=True):
            st.markdown("### Step-by-step solution:")
            
            # Show the problem
            st.markdown(f"**Problem:** {data['problem']}")
            st.markdown("")
            
            # Show the multiplication
            st.markdown("**Solution:**")
            st.markdown(f"• Quantity: **{data['quantity']}**")
            st.markdown(f"• Price per item: **${data['price']}**")
            st.markdown("")
            
            # Show the calculation
            st.markdown("**Calculation:**")
            st.markdown(f"{data['quantity']} × ${data['price']} = ${data['answer']}")
            
            # Show work for larger numbers
            if data['difficulty'] >= 2:
                st.markdown("")
                st.markdown("**How to multiply:**")
                
                # Convert price to cents for easier calculation
                cents = int(data['price'] * 100)
                st.markdown(f"1. Convert to cents: ${data['price']} = {cents}¢")
                st.markdown(f"2. Multiply: {data['quantity']} × {cents}¢ = {data['quantity'] * cents}¢")
                st.markdown(f"3. Convert back: {data['quantity'] * cents}¢ = ${data['answer']}")
            
            st.markdown("")
            st.markdown(f"**Answer: ${data['answer']}**")
            
            # Add tip
            st.info("💡 **Tip:** When multiplying money, you can multiply by the cents and then convert back to dollars!")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""