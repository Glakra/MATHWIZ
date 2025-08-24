import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Divide money amounts with decimals: word problems.
    Uses Decimal for exact money calculations with cents.
    """
    # Initialize session state
    if "decimal_divide_difficulty" not in st.session_state:
        st.session_state.decimal_divide_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("➗ Divide Money Amounts with Decimals: Word Problems")
    st.markdown("*Find the unit price when dividing decimal amounts*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_divide_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (divides evenly to cents)",
            2: "Medium (smaller divisors)", 
            3: "Advanced (complex decimals)"
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
        ### How to Divide Money with Decimals:
        
        **Step 1: Understand what you're finding**
        - Total cost ÷ Number of items = Cost per item
        - All items have the same price
        
        **Step 2: Set up the division**
        - Write the total amount
        - Divide by the number of items
        - Keep track of decimal places
        
        **Example:**
        - $3.60 ÷ 9 items = ?
        - 360 cents ÷ 9 = 40 cents
        - Answer: $0.40 per item
        
        ### Division Tips:
        - Convert to cents if it helps
        - Check your answer by multiplying back
        - Make sure decimal point is in the right place
        
        ### Difficulty Levels:
        - **🟢 Easy:** Divides evenly to whole cents
        - **🟡 Medium:** Smaller numbers, various amounts
        - **🔴 Hard:** Larger totals, complex division
        """)

def generate_new_problem():
    """Generate a new decimal division problem based on difficulty"""
    difficulty = st.session_state.decimal_divide_difficulty
    
    if difficulty == 1:  # Easy - divides evenly to cents
        # Template variations matching the examples
        templates = [
            {
                "format": "It costs ${total} to buy {quantity} {items}. If the {items_short} all have the same price, how much does it cost to buy 1 {item}?",
                "type": "it_costs"
            },
            {
                "format": "{person} spends ${total} on {quantity} {items}. The {items} all cost the same amount. What is the cost of each {item}?",
                "type": "person_spends"
            },
            {
                "format": "If {quantity} {items} cost ${total} and the price of each {item_singular} is the same, how much does each {item_singular} cost?",
                "type": "if_cost"
            },
            {
                "format": "{quantity} {items} cost ${total}. The cost of each {item} is the same. What is the cost of each {item}?",
                "type": "simple_cost"
            },
            {
                "format": "{person} buys {quantity} {items}. The {items_short} all have the same price. She spends a total of ${total}. What is the cost of each {item_singular}?",
                "type": "buys_total"
            }
        ]
        
        # Items with totals that divide evenly
        items = [
            # (item_plural, item_singular, items_short, quantity, total)
            ("cherry ice blocks", "ice block", "ice blocks", 7, 3.15),
            ("gumballs", "gumball", "gumballs", 8, 1.60),
            ("lollipops", "lollipop", "lollipops", 5, 1.25),
            ("candy bars", "candy bar", "candy bars", 6, 4.80),
            ("chocolate coins", "chocolate coin", "coins", 9, 2.70),
            ("fruit chews", "fruit chew", "chews", 4, 1.20),
            ("peppermints", "peppermint", "mints", 10, 2.50),
            ("bubble gums", "bubble gum", "gums", 6, 1.80),
            ("jelly beans", "jelly bean", "beans", 8, 2.40),
            ("candy canes", "candy cane", "canes", 5, 3.75)
        ]
        
        # Food items
        food_items = [
            ("boxes of pasta", "box", "box", 8, 4.80),
            ("tea bags", "tea bag", "tea bag", 4, 2.60),
            ("apples", "apple", "apple", 6, 3.60),
            ("bananas", "banana", "banana", 7, 2.10),
            ("oranges", "orange", "orange", 5, 4.25),
            ("muffins", "muffin", "muffin", 4, 7.20),
            ("cookies", "cookie", "cookie", 9, 4.50),
            ("bread rolls", "roll", "roll", 8, 3.20),
            ("yogurt cups", "cup", "cup", 6, 5.40),
            ("juice boxes", "juice box", "box", 5, 6.25)
        ]
        
        # Other items
        other_items = [
            ("pieces of cherry candy", "piece", "pieces", 5, 1.50),
            ("pencils", "pencil", "pencils", 8, 2.00),
            ("erasers", "eraser", "erasers", 6, 1.80),
            ("stickers", "sticker", "stickers", 10, 1.50),
            ("marbles", "marble", "marbles", 7, 2.80),
            ("toy cars", "toy car", "cars", 4, 9.60),
            ("bouncy balls", "bouncy ball", "balls", 5, 3.75),
            ("trading cards", "card", "cards", 8, 6.40),
            ("bookmarks", "bookmark", "bookmarks", 6, 4.20),
            ("stamps", "stamp", "stamps", 9, 5.40)
        ]
        
        # Combine all items
        all_items = items + food_items + other_items
        
    elif difficulty == 2:  # Medium - smaller divisors, various amounts
        templates = [
            {
                "format": "{person} paid ${total} for {quantity} {items}. Each {item} costs the same. How much does one {item} cost?",
                "type": "paid_for"
            },
            {
                "format": "A pack of {quantity} {items} costs ${total}. If they all cost the same amount, what's the price of each {item}?",
                "type": "pack_of"
            },
            {
                "format": "${total} buys you {quantity} {items}. They all have the same price. What does each {item} cost?",
                "type": "buys_you"
            },
            {
                "format": "The total for {quantity} {items} is ${total}. Each costs the same. Find the cost of one {item}.",
                "type": "total_for"
            }
        ]
        
        # Medium difficulty items - smaller quantities
        all_items = [
            ("notebooks", "notebook", "notebooks", 3, 5.85),
            ("pens", "pen", "pens", 4, 7.80),
            ("folders", "folder", "folders", 5, 8.75),
            ("glue sticks", "glue stick", "sticks", 3, 4.35),
            ("scissors", "pair of scissors", "scissors", 2, 9.50),
            ("rulers", "ruler", "rulers", 4, 6.20),
            ("paint brushes", "brush", "brushes", 3, 11.25),
            ("colored pencils", "pencil", "pencils", 6, 9.30),
            ("markers", "marker", "markers", 4, 13.60),
            ("tape rolls", "roll", "rolls", 5, 12.25),
            # Snacks with smaller quantities
            ("donuts", "donut", "donuts", 3, 8.85),
            ("cupcakes", "cupcake", "cupcakes", 4, 11.80),
            ("brownies", "brownie", "brownies", 2, 5.90),
            ("ice cream bars", "bar", "bars", 3, 7.65),
            ("soft pretzels", "pretzel", "pretzels", 4, 10.60),
            ("smoothies", "smoothie", "smoothies", 2, 9.30),
            ("milkshakes", "milkshake", "shakes", 3, 14.85),
            ("sandwiches", "sandwich", "sandwiches", 2, 13.70)
        ]
        
    else:  # Hard - complex division with larger numbers
        templates = [
            {
                "format": "A school ordered {quantity} {items} for ${total}. What's the unit price if they all cost the same?",
                "type": "school"
            },
            {
                "format": "The store sold {quantity} {items} for a total of ${total}. Each had the same price. Calculate the price per {item}.",
                "type": "store"
            },
            {
                "format": "A company purchased {quantity} {items} at a total cost of ${total}. Find the cost of each {item}.",
                "type": "company"
            },
            {
                "format": "An event used {quantity} {items} costing ${total} total. They were all the same price. What did each cost?",
                "type": "event"
            }
        ]
        
        # Hard difficulty - larger quantities and totals
        all_items = [
            ("calculators", "calculator", "calculators", 15, 148.50),
            ("textbooks", "textbook", "textbooks", 12, 287.40),
            ("laptops", "laptop", "laptops", 8, 3192.00),
            ("tablets", "tablet", "tablets", 9, 2241.00),
            ("office chairs", "chair", "chairs", 6, 894.00),
            ("desk lamps", "lamp", "lamps", 18, 522.60),
            ("keyboards", "keyboard", "keyboards", 24, 718.80),
            ("monitors", "monitor", "monitors", 5, 1247.50),
            ("printers", "printer", "printers", 4, 679.60),
            ("headphones", "pair", "headphones", 20, 598.00),
            # Event items
            ("table decorations", "decoration", "decorations", 36, 162.00),
            ("party favors", "favor", "favors", 48, 144.00),
            ("centerpieces", "centerpiece", "centerpieces", 15, 337.50),
            ("chair covers", "cover", "covers", 25, 187.50),
            ("place settings", "setting", "settings", 30, 447.00),
            ("gift bags", "bag", "bags", 40, 158.00),
            ("name cards", "card", "cards", 50, 37.50),
            ("menu cards", "card", "cards", 24, 86.40)
        ]
    
    # Select template and item
    template = random.choice(templates)
    item_data = random.choice(all_items)
    
    # Names for personalization
    people = ["Lila", "Beth", "Sarah", "Emma", "Kate", "Maya", "Zoe", "Anna",
              "Tom", "Jack", "David", "Ryan", "Alex", "Ben", "Luke", "Noah"]
    
    # Generate the specific problem
    generate_specific_problem(template, item_data, people, difficulty)

def generate_specific_problem(template, item_data, people, difficulty):
    """Generate a specific problem from template"""
    
    items, item, items_short, quantity, total = item_data
    person = random.choice(people)
    
    # Format the problem based on template type
    if template["type"] == "it_costs":
        problem = template["format"].format(
            total=total,
            quantity=quantity,
            items=items,
            items_short=items_short,
            item=item
        )
    elif template["type"] == "person_spends":
        problem = template["format"].format(
            person=person,
            total=total,
            quantity=quantity,
            items=items,
            item=item
        )
    elif template["type"] == "if_cost":
        # Use singular form for "each box" type references
        item_singular = item if item != items_short else items_short
        problem = template["format"].format(
            quantity=quantity,
            items=items,
            total=total,
            item_singular=item_singular
        )
    elif template["type"] == "simple_cost":
        problem = template["format"].format(
            quantity=quantity,
            items=items,
            total=total,
            item=item
        )
    elif template["type"] == "buys_total":
        # Always use female pronouns for this template
        problem = template["format"].format(
            person=person,
            quantity=quantity,
            items=items,
            items_short=items_short,
            total=total,
            item_singular=item
        )
    elif template["type"] in ["paid_for", "pack_of", "buys_you", "total_for"]:
        problem = template["format"].format(
            person=person,
            total=total,
            quantity=quantity,
            items=items,
            item=item
        )
    elif template["type"] in ["school", "store", "company", "event"]:
        problem = template["format"].format(
            quantity=quantity,
            items=items,
            total=total,
            item=item
        )
    
    # Calculate answer
    total_decimal = Decimal(str(total))
    answer = total_decimal / quantity
    answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    st.session_state.problem_data = {
        'problem': problem,
        'answer': answer,
        'total': total_decimal,
        'quantity': quantity,
        'item': item,
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
                st.session_state.decimal_divide_difficulty = min(
                    st.session_state.decimal_divide_difficulty + 1, 3
                )
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            if st.session_state.decimal_divide_difficulty > 1:
                st.session_state.decimal_divide_difficulty -= 1
                
    except:
        st.error("⚠️ Please enter a valid amount (numbers only)")
        return

def show_feedback():
    """Display feedback with solution"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Excellent work!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.decimal_divide_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting more challenging.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is ${data['answer']}**")
        
        # Show solution
        with st.expander("📖 **See how to solve it**", expanded=True):
            st.markdown("### Step-by-step solution:")
            
            # Show the problem
            st.markdown(f"**Problem:** {data['problem']}")
            st.markdown("")
            
            # Show what we know
            st.markdown("**What we know:**")
            st.markdown(f"• Total cost: **${data['total']}**")
            st.markdown(f"• Number of items: **{data['quantity']}**")
            st.markdown(f"• All items cost the same")
            st.markdown("")
            
            # Show the division
            st.markdown("**To find the cost of one item:**")
            st.markdown(f"${data['total']} ÷ {data['quantity']} = ${data['answer']}")
            st.markdown("")
            
            # Show the work based on difficulty
            if data['difficulty'] <= 2:
                # Convert to cents for easier understanding
                total_cents = int(data['total'] * 100)
                answer_cents = int(data['answer'] * 100)
                
                st.markdown("**Another way to think about it:**")
                st.markdown(f"• ${data['total']} = {total_cents} cents")
                st.markdown(f"• {total_cents} ÷ {data['quantity']} = {answer_cents} cents")
                st.markdown(f"• {answer_cents} cents = ${data['answer']}")
            
            # Verification
            st.markdown("")
            st.markdown("**Check the answer:**")
            st.markdown(f"{data['quantity']} × ${data['answer']} = ${data['total']} ✓")
            
            st.markdown("")
            st.markdown(f"**Answer: ${data['answer']}**")
            
            # Add tip based on difficulty
            if data['difficulty'] == 1:
                st.info("💡 **Tip:** These problems divide evenly to whole cents!")
            elif data['difficulty'] == 2:
                st.info("💡 **Tip:** Converting to cents can make division easier!")
            else:
                st.info("💡 **Tip:** For large numbers, be extra careful with decimal placement!")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""