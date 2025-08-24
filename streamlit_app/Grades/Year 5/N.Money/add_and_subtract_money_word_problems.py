import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Add and subtract money: word problems.
    Uses Decimal for exact money calculations.
    """
    # Initialize session state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("💵 Add and Subtract Money: Word Problems")
    st.markdown("*Solve real-world problems with money*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (one-step problems)",
            2: "Medium (two-step problems)", 
            3: "Advanced (multi-step problems)"
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
        ### How to Solve Money Word Problems:
        
        **Step 1: Read carefully**
        - Identify what you need to find
        - Note all the amounts mentioned
        - Determine if you need to add or subtract
        
        **Step 2: Plan your solution**
        - Write down the amounts
        - Decide the operation(s) needed
        - Think about the order of operations
        
        **Step 3: Calculate**
        - Line up decimal points
        - Add or subtract carefully
        - Check your answer makes sense
        
        ### Problem Types:
        - **🟢 Easy:** Single addition or subtraction
        - **🟡 Medium:** Two operations needed
        - **🔴 Hard:** Multiple steps with various operations
        
        ### Tips:
        - Always include the dollar sign ($)
        - Write amounts with two decimal places (e.g., $5.00)
        - Estimate first to check if your answer is reasonable
        """)

def generate_new_problem():
    """Generate a new word problem based on difficulty"""
    difficulty = st.session_state.word_problem_difficulty
    
    if difficulty == 1:  # Easy - single operation
        problem_types = [
            # Simple addition
            {
                "template": "{person} bought a {item1} for ${price1} and a {item2} for ${price2}. How much did {person} spend altogether?",
                "operation": "add",
                "items": [
                    ("notebook", 3.50, 8.00),
                    ("pen", 1.25, 3.50),
                    ("pencil case", 4.75, 9.50),
                    ("ruler", 2.00, 4.50),
                    ("eraser", 0.75, 2.00),
                    ("book", 12.99, 18.99),
                    ("magazine", 4.50, 7.50),
                    ("toy", 8.75, 15.50)
                ],
                "people": ["Sarah", "Tom", "Emma", "Jack", "Lily", "Max", "Zoe", "Ben"]
            },
            # Simple subtraction - change
            {
                "template": "{person} had ${total}. After buying a {item} for ${price}, how much money does {person} have left?",
                "operation": "subtract_change",
                "items": [
                    ("sandwich", 6.50, 20.00),
                    ("drink", 3.25, 10.00),
                    ("snack", 2.75, 5.00),
                    ("ticket", 15.00, 25.00),
                    ("game", 24.99, 50.00),
                    ("shirt", 18.50, 30.00)
                ],
                "people": ["Alex", "Maya", "Oliver", "Sophie", "Ryan", "Chloe"]
            },
            # Simple subtraction - comparison
            {
                "template": "A {item1} costs ${price1} and a {item2} costs ${price2}. How much more does the {item1} cost than the {item2}?",
                "operation": "subtract_compare",
                "items": [
                    ("bicycle", 125.00, "skateboard", 45.00),
                    ("laptop", 599.00, "tablet", 299.00),
                    ("watch", 85.50, "bracelet", 25.50),
                    ("jacket", 75.00, "t-shirt", 15.00),
                    ("camera", 450.00, "phone", 350.00)
                ]
            },
            # Discount problems
            {
                "template": "The regular price of a {item} is ${regular}, but today it is on sale for ${discount} off the regular price. What is the sale price of the {item}?",
                "operation": "discount",
                "items": [
                    ("board game", 41.00, 18.00),
                    ("backpack", 35.00, 12.00),
                    ("calculator", 25.00, 8.00),
                    ("headphones", 60.00, 15.00),
                    ("video game", 50.00, 20.00)
                ]
            },
            # Coupon problems
            {
                "template": "The regular price of a {item} is ${price}. {person} has a coupon for ${coupon} off. How much will {he_she} pay for the {item} if {he_she} uses the coupon?",
                "operation": "coupon",
                "items": [
                    ("bottle of salad dressing", 6.00, 3.00),
                    ("pizza", 15.00, 5.00),
                    ("shampoo", 8.50, 2.50),
                    ("book", 12.00, 4.00),
                    ("toy", 20.00, 7.00)
                ],
                "people": [
                    ("My mum", "she", "she"),
                    ("Dad", "he", "he"),
                    ("Jamie", "he", "he"),
                    ("Kelly", "she", "she")
                ]
            }
        ]
        
        problem_type = random.choice(problem_types)
        
    elif difficulty == 2:  # Medium - two operations
        problem_types = [
            # Buy multiple, get change
            {
                "template": "{person} went to the store with ${total}. {He_She} bought a {item1} for ${price1} and a {item2} for ${price2}. How much change did {person} receive?",
                "operation": "add_subtract",
                "items": [
                    ("book", 12.50, "pen", 3.75, 25.00),
                    ("lunch", 8.50, "drink", 2.50, 15.00),
                    ("toy", 15.99, "candy", 2.99, 20.00),
                    ("shirt", 22.00, "socks", 5.50, 40.00),
                    ("game", 35.00, "controller", 25.00, 100.00)
                ],
                "people": [
                    ("Emma", "She"),
                    ("Jack", "He"),
                    ("Sophia", "She"),
                    ("Noah", "He")
                ]
            },
            # Compare two totals
            {
                "template": "{person1} spent ${amount1} on a {item1} and ${amount2} on a {item2}. How much more did {person1} spend on the {item1} than the {item2}?",
                "operation": "double_compare",
                "items": [
                    ("sparkly headband", 4.00, "shiny bracelet", 3.00),
                    ("notebook", 5.50, "folder", 2.25),
                    ("soccer ball", 18.00, "basketball", 15.50),
                    ("video game", 45.00, "board game", 28.00)
                ],
                "people": ["Maggie", "David", "Alice", "Carlos"]
            },
            # Earn and spend
            {
                "template": "{person} earned ${earned1} {job1} and ${earned2} {job2}. If {he_she} spent ${spent} on {item}, how much money does {person} have left?",
                "operation": "earn_spend",
                "items": [
                    ("mowing lawns", 25.00, "washing cars", 15.00, 12.50, "a new book"),
                    ("babysitting", 30.00, "dog walking", 20.00, 18.75, "a video game"),
                    ("doing chores", 10.00, "helping neighbors", 15.00, 8.50, "candy"),
                    ("selling lemonade", 12.50, "bake sale", 18.50, 15.00, "art supplies")
                ],
                "people": [
                    ("Tom", "he"),
                    ("Lisa", "she"),
                    ("Mike", "he"),
                    ("Kate", "she")
                ]
            }
        ]
        
        problem_type = random.choice(problem_types)
        
    else:  # Hard - multi-step problems
        problem_types = [
            # Shopping with multiple items and change
            {
                "template": "{person} went shopping with ${total}. {He_She} bought {count1} {item1} at ${price1} each and {count2} {item2} at ${price2} each. How much money does {person} have left?",
                "operation": "multi_buy",
                "items": [
                    (3, "notebooks", 4.50, 2, "pens", 2.25, 50.00),
                    (4, "books", 8.75, 2, "bookmarks", 1.50, 60.00),
                    (5, "apples", 0.75, 3, "oranges", 1.25, 10.00),
                    (2, "pizzas", 12.50, 4, "drinks", 2.50, 40.00)
                ],
                "people": [
                    ("Sarah", "She"),
                    ("James", "He"),
                    ("Emily", "She"),
                    ("Daniel", "He")
                ]
            },
            # Group purchases with individual contributions
            {
                "template": "{person1} and {person2} decided to buy a {item} together. The {item} costs ${total}. If {person1} paid ${amount1}, how much did {person2} pay?",
                "operation": "group_buy",
                "items": [
                    ("birthday present", 45.00, 28.50),
                    ("video game", 60.00, 35.75),
                    ("pizza order", 32.50, 18.25),
                    ("concert tickets", 85.00, 47.50)
                ],
                "people": [
                    ("Amy", "Ben"),
                    ("Chris", "Dana"),
                    ("Eva", "Frank"),
                    ("Grace", "Henry")
                ]
            },
            # Business earnings
            {
                "template": "{person1} and {person2} decided to start their own {business} business. {person1} earned ${earned1} {job1}, and {person2} earned ${earned2} {job2}. Altogether, how much money did they earn?",
                "operation": "business",
                "items": [
                    ("babysitting", 29.00, "babysitting for his cousins", 12.00, "babysitting for family friends"),
                    ("lawn mowing", 45.50, "mowing 3 lawns", 28.00, "mowing 2 lawns"),
                    ("car washing", 35.00, "washing 5 cars", 21.00, "washing 3 cars"),
                    ("dog walking", 18.50, "walking dogs", 15.75, "pet sitting")
                ],
                "people": [
                    ("Leo", "Dominic"),
                    ("Mia", "Zara"),
                    ("Jake", "Tyler"),
                    ("Ruby", "Pearl")
                ]
            },
            # Complex shopping scenarios
            {
                "template": "At a {place}, {person} paid ${amount1} to {action1} and ${amount2} to {action2}. How much did {person} pay altogether?",
                "operation": "service_total",
                "items": [
                    ("printing shop", "Reid", 0.25, "make a copy of an important document", 0.20, "print a copy of a photograph"),
                    ("craft store", "Maya", 3.75, "buy ribbon", 5.50, "buy stickers"),
                    ("bakery", "Luis", 2.50, "buy a muffin", 3.25, "buy a smoothie"),
                    ("arcade", "Jenna", 5.00, "play games", 3.50, "buy tokens")
                ],
                "people": ["Reid", "Maya", "Luis", "Jenna"]
            },
            # Garage sale scenarios
            {
                "template": "{person}'s neighbours are having a garage sale. {person} sees {item1} for ${price1} and {item2} for ${price2}. How much money would it cost to buy those items?",
                "operation": "garage_sale",
                "items": [
                    ("an umbrella", 17.00, "a set of dishes", 20.00),
                    ("a bicycle helmet", 8.50, "a skateboard", 15.00),
                    ("a board game", 5.00, "a puzzle", 3.50),
                    ("a lamp", 12.00, "a mirror", 18.50)
                ],
                "people": ["Dwayne", "Chelsea", "Marcus", "Tiffany"]
            }
        ]
        
        problem_type = random.choice(problem_types)
    
    # Generate the specific problem
    generate_specific_problem(problem_type, difficulty)

def generate_specific_problem(problem_type, difficulty):
    """Generate a specific problem based on type"""
    data = {}
    
    if difficulty == 1:
        if problem_type["operation"] == "add":
            person = random.choice(problem_type["people"])
            item_pair = random.choice(problem_type["items"])
            item1, price1_min, price1_max = item_pair[0], item_pair[1], item_pair[2]
            item2, price2_min, price2_max = random.choice(problem_type["items"])[:3]
            
            price1 = Decimal(str(random.uniform(price1_min, price1_max))).quantize(Decimal('0.01'))
            price2 = Decimal(str(random.uniform(price2_min, price2_max))).quantize(Decimal('0.01'))
            
            problem = problem_type["template"].format(
                person=person, item1=item1, price1=price1,
                item2=item2, price2=price2
            )
            answer = price1 + price2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${price1} + ${price2} = ${answer}",
                'operation': 'add'
            }
            
        elif problem_type["operation"] == "subtract_change":
            person = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            item, price_min, total_min = item_data
            
            price = Decimal(str(random.uniform(price_min, price_min * 1.5))).quantize(Decimal('0.01'))
            total = Decimal(str(random.uniform(total_min, total_min * 1.5))).quantize(Decimal('0.01'))
            
            problem = problem_type["template"].format(
                person=person, total=total, item=item, price=price
            )
            answer = total - price
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${total} - ${price} = ${answer}",
                'operation': 'subtract'
            }
            
        elif problem_type["operation"] == "subtract_compare":
            item_data = random.choice(problem_type["items"])
            item1, price1, item2, price2 = item_data
            
            price1 = Decimal(str(price1))
            price2 = Decimal(str(price2))
            
            problem = problem_type["template"].format(
                item1=item1, price1=price1, item2=item2, price2=price2
            )
            answer = price1 - price2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${price1} - ${price2} = ${answer}",
                'operation': 'subtract'
            }
            
        elif problem_type["operation"] == "discount":
            item_data = random.choice(problem_type["items"])
            item, regular, discount = item_data
            
            regular = Decimal(str(regular))
            discount = Decimal(str(discount))
            
            problem = problem_type["template"].format(
                item=item, regular=regular, discount=discount
            )
            answer = regular - discount
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${regular} - ${discount} = ${answer}",
                'operation': 'subtract'
            }
            
        elif problem_type["operation"] == "coupon":
            item_data = random.choice(problem_type["items"])
            person_data = random.choice(problem_type["people"])
            
            item, price, coupon = item_data[:3]
            person, he_she, he_she2 = person_data
            
            price = Decimal(str(price))
            coupon = Decimal(str(coupon))
            
            problem = problem_type["template"].format(
                item=item, price=price, person=person,
                he_she=he_she, coupon=coupon
            )
            answer = price - coupon
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${price} - ${coupon} = ${answer}",
                'operation': 'subtract'
            }
    
    elif difficulty == 2:
        if problem_type["operation"] == "add_subtract":
            person_data = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            person, he_she = person_data
            item1, price1, item2, price2, total = item_data
            
            price1 = Decimal(str(price1))
            price2 = Decimal(str(price2))
            total = Decimal(str(total))
            
            problem = problem_type["template"].format(
                person=person, He_She=he_she, total=total,
                item1=item1, price1=price1, item2=item2, price2=price2
            )
            
            spent = price1 + price2
            answer = total - spent
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"Step 1: ${price1} + ${price2} = ${spent}\nStep 2: ${total} - ${spent} = ${answer}",
                'operation': 'multi'
            }
            
        elif problem_type["operation"] == "double_compare":
            person = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            item1, amount1, item2, amount2 = item_data
            amount1 = Decimal(str(amount1))
            amount2 = Decimal(str(amount2))
            
            problem = problem_type["template"].format(
                person1=person, item1=item1, amount1=amount1,
                item2=item2, amount2=amount2
            )
            answer = amount1 - amount2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${amount1} - ${amount2} = ${answer}",
                'operation': 'subtract'
            }
            
        elif problem_type["operation"] == "earn_spend":
            person_data = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            person, he_she = person_data
            job1, earned1, job2, earned2, spent, item = item_data
            
            earned1 = Decimal(str(earned1))
            earned2 = Decimal(str(earned2))
            spent = Decimal(str(spent))
            
            problem = problem_type["template"].format(
                person=person, he_she=he_she, job1=job1, earned1=earned1,
                job2=job2, earned2=earned2, spent=spent, item=item
            )
            
            total_earned = earned1 + earned2
            answer = total_earned - spent
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"Step 1: ${earned1} + ${earned2} = ${total_earned}\nStep 2: ${total_earned} - ${spent} = ${answer}",
                'operation': 'multi'
            }
    
    else:  # difficulty == 3
        if problem_type["operation"] == "multi_buy":
            person_data = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            person, he_she = person_data
            count1, item1, price1, count2, item2, price2, total = item_data
            
            price1 = Decimal(str(price1))
            price2 = Decimal(str(price2))
            total = Decimal(str(total))
            
            problem = problem_type["template"].format(
                person=person, He_She=he_she, total=total,
                count1=count1, item1=item1, price1=price1,
                count2=count2, item2=item2, price2=price2
            )
            
            cost1 = price1 * count1
            cost2 = price2 * count2
            total_cost = cost1 + cost2
            answer = total - total_cost
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"Step 1: {count1} × ${price1} = ${cost1}\nStep 2: {count2} × ${price2} = ${cost2}\nStep 3: ${cost1} + ${cost2} = ${total_cost}\nStep 4: ${total} - ${total_cost} = ${answer}",
                'operation': 'complex'
            }
            
        elif problem_type["operation"] == "group_buy":
            people = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            person1, person2 = people
            item, total, amount1 = item_data
            
            total = Decimal(str(total))
            amount1 = Decimal(str(amount1))
            
            problem = problem_type["template"].format(
                person1=person1, person2=person2, item=item,
                total=total, amount1=amount1
            )
            answer = total - amount1
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${total} - ${amount1} = ${answer}",
                'operation': 'subtract'
            }
            
        elif problem_type["operation"] == "business":
            people = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            person1, person2 = people
            business, earned1, job1, earned2, job2 = item_data
            
            earned1 = Decimal(str(earned1))
            earned2 = Decimal(str(earned2))
            
            problem = problem_type["template"].format(
                person1=person1, person2=person2, business=business,
                earned1=earned1, job1=job1, earned2=earned2, job2=job2
            )
            answer = earned1 + earned2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${earned1} + ${earned2} = ${answer}",
                'operation': 'add'
            }
            
        elif problem_type["operation"] == "service_total":
            item_data = random.choice(problem_type["items"])
            
            place, person, amount1, action1, amount2, action2 = item_data
            
            amount1 = Decimal(str(amount1))
            amount2 = Decimal(str(amount2))
            
            problem = problem_type["template"].format(
                place=place, person=person, amount1=amount1,
                action1=action1, amount2=amount2, action2=action2
            )
            answer = amount1 + amount2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${amount1} + ${amount2} = ${answer}",
                'operation': 'add'
            }
            
        elif problem_type["operation"] == "garage_sale":
            person = random.choice(problem_type["people"])
            item_data = random.choice(problem_type["items"])
            
            item1, price1, item2, price2 = item_data
            
            price1 = Decimal(str(price1))
            price2 = Decimal(str(price2))
            
            problem = problem_type["template"].format(
                person=person, item1=item1, price1=price1,
                item2=item2, price2=price2
            )
            answer = price1 + price2
            
            data = {
                'problem': problem,
                'answer': answer,
                'solution': f"${price1} + ${price2} = ${answer}",
                'operation': 'add'
            }
    
    st.session_state.problem_data = data
    st.session_state.current_problem = data['problem']

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
    ">
        <p style="font-size: 18px; margin: 0; color: #333;">
            {data['problem']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create input field like in the examples
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input field with dollar sign
        user_answer = st.text_input(
            "Your answer:",
            value=st.session_state.user_answer,
            key="answer_input",
            placeholder="0.00",
            label_visibility="collapsed"
        )
        
        # Update session state
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
    user_input = st.session_state.user_answer
    
    # Clean the input
    user_input = user_input.strip()
    if user_input.startswith('$'):
        user_input = user_input[1:]
    
    try:
        # Convert to Decimal
        user_answer = Decimal(user_input).quantize(Decimal('0.01'))
        correct_answer = Decimal(str(data['answer'])).quantize(Decimal('0.01'))
        
        # Check if correct
        correct = (user_answer == correct_answer)
        
        st.session_state.answer_submitted = True
        st.session_state.show_feedback = True
        st.session_state.user_correct = correct
        
        # Update difficulty
        if correct:
            st.session_state.consecutive_correct += 1
            if st.session_state.consecutive_correct >= 3:
                st.session_state.word_problem_difficulty = min(st.session_state.word_problem_difficulty + 1, 3)
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            if st.session_state.word_problem_difficulty > 1:
                st.session_state.word_problem_difficulty -= 1
                
    except:
        st.error("Please enter a valid money amount (e.g., 12.50)")
        return

def show_feedback():
    """Display feedback"""
    data = st.session_state.problem_data
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Excellent work!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.word_problem_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting more challenging.**")
    else:
        correct_answer = Decimal(str(data['answer'])).quantize(Decimal('0.01'))
        st.error(f"❌ **Not quite. The correct answer is ${correct_answer}**")
        
        # Show solution
        with st.expander("📖 **See the solution**", expanded=True):
            st.markdown("### How to solve:")
            
            # Show the problem again
            st.markdown(f"**Problem:** {data['problem']}")
            st.markdown("")
            
            # Show step-by-step solution
            if '\n' in data['solution']:
                # Multi-step solution
                steps = data['solution'].split('\n')
                for step in steps:
                    st.markdown(f"**{step}**")
            else:
                # Single-step solution
                st.markdown(f"**Solution:** {data['solution']}")
            
            st.markdown(f"\n**Answer: ${correct_answer}**")
            
            # Add tips based on operation
            if data['operation'] == 'add':
                st.info("💡 **Tip:** When adding money, line up the decimal points and add from right to left.")
            elif data['operation'] == 'subtract':
                st.info("💡 **Tip:** When subtracting money, make sure the larger amount is on top.")
            elif data['operation'] in ['multi', 'complex']:
                st.info("💡 **Tip:** For multi-step problems, solve one step at a time and write down your work.")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""