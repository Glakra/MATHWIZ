import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

def run():
    """
    Main function for Divide money amounts: word problems.
    Uses Decimal for exact money calculations.
    """
    # Initialize session state
    if "divide_difficulty" not in st.session_state:
        st.session_state.divide_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Money**")
    st.title("➗ Divide Money Amounts: Word Problems")
    st.markdown("*Solve division problems with money*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Simple (whole dollar results)",
            2: "Medium (results with cents)", 
            3: "Advanced (complex division)"
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
        ### Types of Division Problems:
        
        **Type 1: Find the unit price**
        - Total cost ÷ Number of items = Price per item
        - Example: $20 ÷ 4 items = $5 per item
        
        **Type 2: Find how many items**
        - Total money ÷ Price per item = Number of items
        - Example: $20 ÷ $5 each = 4 items
        
        **Type 3: Find the rate**
        - Total earned ÷ Time worked = Rate per hour
        - Example: $100 ÷ 10 hours = $10 per hour
        
        ### Division Tips:
        - Read carefully to identify what you're finding
        - Set up the division correctly
        - Check: multiplication should give you back the original
        
        ### Difficulty Levels:
        - **🟢 Easy:** Results are whole dollars
        - **🟡 Medium:** Results include cents
        - **🔴 Hard:** Larger numbers, complex scenarios
        """)

def generate_new_problem():
    """Generate a new division word problem based on difficulty"""
    difficulty = st.session_state.divide_difficulty
    
    if difficulty == 1:  # Easy - whole dollar results
        problem_types = [
            # Type 1: Total spent, find unit price
            {
                "template": "{person} spent ${total} to buy {quantity} {items}. The {items} all had the same price. How much did each {item} cost?",
                "type": "unit_price",
                "items": [
                    ("kickballs", "kickball", 4, 40),
                    ("basketballs", "basketball", 5, 60),
                    ("soccer balls", "soccer ball", 3, 45),
                    ("tennis balls", "tennis ball", 6, 12),
                    ("jump ropes", "jump rope", 8, 32),
                    ("frisbees", "frisbee", 7, 21)
                ],
                "people": ["Jill", "Tom", "Maria", "Alex", "Sophie", "Ryan"]
            },
            {
                "template": "{person} bought {quantity} {items} that each cost the same amount. She spent ${total} in all. How much did each {item} cost?",
                "type": "unit_price_alt",
                "items": [
                    ("ironing boards", "ironing board", 5, 50),
                    ("storage bins", "storage bin", 4, 32),
                    ("picture frames", "picture frame", 6, 48),
                    ("flower pots", "flower pot", 3, 27),
                    ("notebooks", "notebook", 10, 30),
                    ("folders", "folder", 8, 24)
                ],
                "people": ["Emma", "Lisa", "Kate", "Anna", "Maya", "Zoe"]
            },
            {
                "template": "{quantity} {items} cost ${total}. The cost of each {item} is the same. What is the cost of each {item}?",
                "type": "cost_each",
                "items": [
                    ("beach towels", "towel", 6, 60),
                    ("bath mats", "mat", 4, 36),
                    ("pillowcases", "pillowcase", 8, 40),
                    ("placemats", "placemat", 5, 25),
                    ("dish towels", "dish towel", 9, 27),
                    ("wash cloths", "wash cloth", 12, 24)
                ]
            },
            {
                "template": "{quantity} {items} cost ${total}. If the {items} all cost the same amount, how much does each {item} cost?",
                "type": "all_same",
                "items": [
                    ("Halloween masks", "mask", 5, 35),
                    ("party hats", "hat", 8, 16),
                    ("costume accessories", "accessory", 4, 20),
                    ("decorations", "decoration", 6, 30),
                    ("treat bags", "bag", 10, 40),
                    ("glow sticks", "glow stick", 20, 20)
                ]
            },
            {
                "template": "If {quantity} {items} cost ${total} and the price of each {item} is the same, how much does each {item} cost?",
                "type": "if_same",
                "items": [
                    ("lip balms", "lip balm", 8, 8),
                    ("nail polishes", "nail polish", 4, 12),
                    ("hair ties", "hair tie", 10, 5),
                    ("hair clips", "hair clip", 6, 18),
                    ("compact mirrors", "mirror", 3, 15),
                    ("makeup brushes", "brush", 5, 25)
                ]
            },
            # Type 2: Hourly rate problems
            {
                "template": "{person} earned ${total} working as {job}. She worked for {hours} hours. How much did {person} earn per hour?",
                "type": "hourly_rate",
                "jobs": [
                    ("an office clerk", 100, 10),
                    ("a cashier", 80, 8),
                    ("a tutor", 120, 6),
                    ("a babysitter", 60, 4),
                    ("a dog walker", 45, 3),
                    ("a library assistant", 70, 7)
                ],
                "people": ["Barbara", "Sarah", "Jessica", "Michelle", "Amanda", "Jennifer"]
            }
        ]
        
    elif difficulty == 2:  # Medium - results with cents
        problem_types = [
            {
                "template": "{person} paid ${total} for {quantity} {items}. Each {item} was the same price. How much did one {item} cost?",
                "type": "one_cost",
                "items": [
                    ("magazines", "magazine", 6, 23.70),
                    ("paperback books", "book", 4, 31.80),
                    ("comic books", "comic book", 5, 18.75),
                    ("newspapers", "newspaper", 7, 10.50),
                    ("greeting cards", "card", 8, 22.40),
                    ("postcards", "postcard", 12, 15.60)
                ],
                "people": ["David", "Michael", "Robert", "James", "William", "Daniel"]
            },
            {
                "template": "The total cost of {quantity} {items} was ${total}. If they all cost the same, what was the price of each {item}?",
                "type": "total_was",
                "items": [
                    ("water bottles", "water bottle", 8, 34.40),
                    ("lunch boxes", "lunch box", 5, 42.50),
                    ("thermoses", "thermos", 4, 27.80),
                    ("ice packs", "ice pack", 6, 20.70),
                    ("sandwich containers", "container", 9, 40.50),
                    ("snack bags", "bag", 15, 33.75)
                ]
            },
            {
                "template": "{person} bought {quantity} identical {items} for a total of ${total}. What was the cost per {item}?",
                "type": "identical",
                "items": [
                    ("plant pots", "pot", 6, 35.70),
                    ("garden tools", "tool", 4, 47.60),
                    ("seed packets", "packet", 8, 30.40),
                    ("watering cans", "can", 3, 26.85),
                    ("garden gloves", "pair", 5, 37.45),
                    ("plant markers", "marker", 10, 12.50)
                ],
                "people": ["Carlos", "Luis", "Juan", "Miguel", "Pedro", "Diego"]
            },
            # Mixed division problems
            {
                "template": "A box of {quantity} {items} costs ${total}. How much would just one {item} cost?",
                "type": "box_one",
                "items": [
                    ("cookies", "cookie", 24, 8.40),
                    ("chocolates", "chocolate", 16, 12.80),
                    ("candies", "candy", 30, 6.90),
                    ("mints", "mint", 20, 5.60),
                    ("lollipops", "lollipop", 12, 7.20),
                    ("gummy bears", "gummy bear", 50, 4.50)
                ]
            }
        ]
        
    else:  # Hard - complex division scenarios
        problem_types = [
            {
                "template": "A restaurant ordered {quantity} {items} for ${total}. Each {item} costs the same. What is the unit price?",
                "type": "restaurant",
                "items": [
                    ("tablecloths", "tablecloth", 15, 187.50),
                    ("napkin sets", "set", 24, 143.76),
                    ("menu holders", "holder", 18, 251.82),
                    ("salt shakers", "shaker", 36, 97.20),
                    ("serving trays", "tray", 12, 215.88),
                    ("water pitchers", "pitcher", 8, 159.92)
                ]
            },
            {
                "template": "The school purchased {quantity} {items} for the science lab at a total cost of ${total}. What was the price per {item}?",
                "type": "school",
                "items": [
                    ("microscopes", "microscope", 6, 749.94),
                    ("beakers", "beaker", 48, 191.52),
                    ("test tubes", "test tube", 144, 86.40),
                    ("safety goggles", "pair", 30, 224.70),
                    ("lab coats", "coat", 25, 374.75),
                    ("thermometers", "thermometer", 20, 139.80)
                ]
            },
            {
                "template": "{person} runs a business and spent ${total} on {quantity} {items} for resale. Each costs the same. What's the cost per unit?",
                "type": "business",
                "items": [
                    ("phone cases", "case", 150, 562.50),
                    ("USB cables", "cable", 200, 478.00),
                    ("earbuds", "pair", 75, 446.25),
                    ("screen protectors", "protector", 300, 447.00),
                    ("phone grips", "grip", 250, 312.50),
                    ("charging blocks", "block", 100, 649.00)
                ],
                "people": ["Mr. Chen", "Ms. Rodriguez", "Mr. Patel", "Ms. Kim", "Mr. Johnson", "Ms. Lee"]
            },
            # Rate problems with decimals
            {
                "template": "{person} earned ${total} in {time} hours of {work}. What was the hourly rate?",
                "type": "hourly_decimal",
                "work": [
                    ("freelance writing", 187.50, 12.5),
                    ("graphic design", 315.60, 18),
                    ("web development", 562.40, 22),
                    ("consulting", 437.50, 17.5),
                    ("tutoring", 168.75, 7.5),
                    ("data entry", 134.40, 14)
                ],
                "people": ["Ashley", "Brandon", "Christina", "Derek", "Emily", "Frank"]
            }
        ]
    
    # Select problem type and generate
    problem_type = random.choice(problem_types)
    generate_specific_problem(problem_type, difficulty)

def generate_specific_problem(problem_type, difficulty):
    """Generate a specific problem from template"""
    
    if problem_type["type"] in ["unit_price", "unit_price_alt", "cost_each", "all_same", "if_same", 
                                "one_cost", "total_was", "identical", "box_one", "restaurant", 
                                "school", "business"]:
        # Item-based division problems
        if "people" in problem_type:
            person = random.choice(problem_type["people"])
        else:
            person = None
            
        item_data = random.choice(problem_type["items"])
        
        if problem_type["type"] == "business":
            items, item, quantity, total = item_data
            person = random.choice(problem_type["people"])
        else:
            items, item, quantity, total = item_data
        
        # Create problem text
        if person:
            problem = problem_type["template"].format(
                person=person,
                quantity=quantity,
                items=items,
                item=item,
                total=total
            )
        else:
            problem = problem_type["template"].format(
                quantity=quantity,
                items=items,
                item=item,
                total=total
            )
        
        # Calculate answer
        total_decimal = Decimal(str(total))
        answer = total_decimal / quantity
        answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        problem_data = {
            'type': 'find_unit_price',
            'total': total_decimal,
            'quantity': quantity,
            'item': item
        }
        
    elif problem_type["type"] == "hourly_rate":
        # Simple hourly rate problems
        person = random.choice(problem_type["people"])
        job_data = random.choice(problem_type["jobs"])
        job, total, hours = job_data
        
        problem = problem_type["template"].format(
            person=person,
            job=job,
            total=total,
            hours=hours
        )
        
        # Calculate answer
        total_decimal = Decimal(str(total))
        answer = total_decimal / hours
        answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        problem_data = {
            'type': 'hourly_rate',
            'total': total_decimal,
            'hours': hours,
            'job': job
        }
        
    elif problem_type["type"] == "hourly_decimal":
        # Complex hourly rate with decimal hours
        person = random.choice(problem_type["people"])
        work_data = random.choice(problem_type["work"])
        work, total, time = work_data
        
        problem = problem_type["template"].format(
            person=person,
            work=work,
            total=total,
            time=time
        )
        
        # Calculate answer
        total_decimal = Decimal(str(total))
        time_decimal = Decimal(str(time))
        answer = total_decimal / time_decimal
        answer = answer.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        problem_data = {
            'type': 'hourly_decimal',
            'total': total_decimal,
            'time': time_decimal,
            'work': work
        }
    
    # Store problem data
    st.session_state.problem_data = {
        'problem': problem,
        'answer': answer,
        'details': problem_data,
        'difficulty': difficulty
    }
    st.session_state.current_problem = problem

def display_problem():
    """Display the word problem with input field"""
    data = st.session_state.problem_data
    
    # Display the problem in a box
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
                st.session_state.divide_difficulty = min(
                    st.session_state.divide_difficulty + 1, 3
                )
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            if st.session_state.divide_difficulty > 1:
                st.session_state.divide_difficulty -= 1
                
    except:
        st.error("⚠️ Please enter a valid amount (numbers only)")
        return

def show_feedback():
    """Display feedback with solution"""
    data = st.session_state.problem_data
    details = data['details']
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Excellent work!**")
        
        if st.session_state.consecutive_correct == 0 and st.session_state.divide_difficulty < 3:
            st.info("⬆️ **Level up! The problems are getting more challenging.**")
    else:
        st.error(f"❌ **Not quite. The correct answer is ${data['answer']}**")
        
        # Show solution
        with st.expander("📖 **See how to solve it**", expanded=True):
            st.markdown("### Step-by-step solution:")
            
            # Show the problem
            st.markdown(f"**Problem:** {data['problem']}")
            st.markdown("")
            
            # Show solution based on problem type
            if details['type'] == 'find_unit_price':
                st.markdown("**What we know:**")
                st.markdown(f"• Total cost: **${details['total']}**")
                st.markdown(f"• Number of items: **{details['quantity']}**")
                st.markdown(f"• All items cost the same")
                st.markdown("")
                
                st.markdown("**To find the cost of one item:**")
                st.markdown(f"Total cost ÷ Number of items = Cost per item")
                st.markdown(f"${details['total']} ÷ {details['quantity']} = ${data['answer']}")
                
                # Verification
                st.markdown("")
                st.markdown("**Check:**")
                st.markdown(f"{details['quantity']} × ${data['answer']} = ${details['total']} ✓")
                
            elif details['type'] == 'hourly_rate':
                st.markdown("**What we know:**")
                st.markdown(f"• Total earned: **${details['total']}**")
                st.markdown(f"• Hours worked: **{details['hours']} hours**")
                st.markdown("")
                
                st.markdown("**To find hourly rate:**")
                st.markdown(f"Total earned ÷ Hours worked = Rate per hour")
                st.markdown(f"${details['total']} ÷ {details['hours']} = ${data['answer']} per hour")
                
            elif details['type'] == 'hourly_decimal':
                st.markdown("**What we know:**")
                st.markdown(f"• Total earned: **${details['total']}**")
                st.markdown(f"• Time worked: **{details['time']} hours**")
                st.markdown("")
                
                st.markdown("**To find hourly rate:**")
                st.markdown(f"Total earned ÷ Hours worked = Rate per hour")
                st.markdown(f"${details['total']} ÷ {details['time']} = ${data['answer']} per hour")
            
            st.markdown("")
            st.markdown(f"**Answer: ${data['answer']}**")
            
            # Add tip
            if data['difficulty'] == 1:
                st.info("💡 **Tip:** For easy division, think: What number times the quantity equals the total?")
            elif data['difficulty'] == 2:
                st.info("💡 **Tip:** When dividing money, place the decimal point carefully in your answer!")
            else:
                st.info("💡 **Tip:** For complex division, you can convert to cents first, divide, then convert back to dollars!")

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""