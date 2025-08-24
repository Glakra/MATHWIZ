import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Add and Subtract Fractions Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_fractions_with_unlike_denominators_word_problems.py
    """
    # Initialize session state for adaptive difficulty
    if "word_problem_level" not in st.session_state:
        st.session_state.word_problem_level = 1
    
    if "word_problem_streak" not in st.session_state:
        st.session_state.word_problem_streak = 0
    
    if "word_problem_mistakes" not in st.session_state:
        st.session_state.word_problem_mistakes = 0
    
    if "current_word_problem" not in st.session_state:
        st.session_state.current_word_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Style for word problems */
    .word-problem {
        font-size: 18px;
        line-height: 1.6;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Style input field */
    input[type="text"] {
        font-size: 16px !important;
        width: 150px !important;
    }
    
    /* Submit button */
    div.stButton > button[type="submit"] {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("📖 Add and Subtract Fractions: Word Problems")
    st.markdown("*Solve real-world problems with fractions*")
    
    # Difficulty and progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        level_names = {1: "Basic", 2: "Simple", 3: "Standard", 4: "Advanced", 5: "Challenge"}
        level_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🟣"}
        level = st.session_state.word_problem_level
        st.markdown(f"**Difficulty:** {level_colors[level]} {level_names[level]}")
        st.progress(level / 5, text=f"Level {level}/5")
    
    with col2:
        if st.session_state.word_problem_streak > 0:
            st.metric("Streak", f"🔥 {st.session_state.word_problem_streak}")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    st.markdown("---")
    
    # Generate new problem if needed
    if st.session_state.current_word_problem is None:
        generate_word_problem()
    
    # Display problem
    display_word_problem()
    
    # Tips section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Fraction Word Problems:
        
        **Step 1: Identify what you're looking for**
        - Read carefully - what is the question asking?
        - Look for keywords: "altogether", "in total", "combined" (addition)
        - Look for: "left", "more than", "difference" (subtraction)
        
        **Step 2: Identify the fractions**
        - Find the fraction amounts in the problem
        - Note what they represent (parts of what whole?)
        
        **Step 3: Decide the operation**
        - Are you combining amounts? → Add
        - Are you finding how much more/less? → Subtract
        - Are you finding what's left? → Subtract
        
        **Step 4: Solve**
        - Find the LCD
        - Convert to equivalent fractions
        - Add or subtract
        - Simplify your answer
        
        **Step 5: Check your answer**
        - Does it make sense in the context?
        - Is it in simplest form?
        
        ### Difficulty Levels:
        - **Level 1**: Simple contexts, small denominators
        - **Level 2**: Common scenarios, friendly fractions
        - **Level 3**: Real-world contexts, moderate fractions
        - **Level 4**: Complex scenarios, larger fractions
        - **Level 5**: Multi-step problems, challenging fractions
        """)

def generate_word_problem():
    """Generate an adaptive word problem"""
    level = st.session_state.word_problem_level
    
    # Problem templates by level
    problem_templates = {
        1: [  # Basic - simple contexts
            {
                "template": "Tom ate {frac1} of a pizza for lunch and {frac2} of a pizza for dinner. How much pizza did Tom eat in total?",
                "unit": "of the pizza",
                "operation": "add",
                "context": "food"
            },
            {
                "template": "Sarah walked {frac1} of a mile to school and {frac2} of a mile to the park. How far did Sarah walk altogether?",
                "unit": "miles",
                "operation": "add",
                "context": "distance"
            },
            {
                "template": "A water bottle was {frac1} full. Jake drank {frac2} of the bottle. How much water is left?",
                "unit": "of the bottle",
                "operation": "subtract",
                "context": "liquid"
            }
        ],
        2: [  # Simple - everyday scenarios
            {
                "template": "At the bakery, {frac1} of the cookies were chocolate chip and {frac2} were sugar cookies. What fraction of the cookies were either chocolate chip or sugar?",
                "unit": "of the cookies",
                "operation": "add",
                "context": "food"
            },
            {
                "template": "Maria spent {frac1} of her allowance on books and {frac2} on art supplies. What fraction of her allowance did she spend?",
                "unit": "of her allowance",
                "operation": "add",
                "context": "money"
            },
            {
                "template": "A garden has {frac1} planted with roses. If {frac2} of the garden is replanted with tulips, what fraction is still roses?",
                "unit": "of the garden",
                "operation": "subtract",
                "context": "garden"
            }
        ],
        3: [  # Standard - real-world contexts
            {
                "template": "Of the smoothies sold yesterday at Belle's Smoothies Shop, {frac1} were banana and another {frac2} were strawberry. What fraction of the smoothies sold were either banana or strawberry?",
                "unit": "of the smoothies",
                "operation": "add",
                "context": "business"
            },
            {
                "template": "Brendan made some chilli with {frac1} of a tin of black beans and {frac2} of a tin of pinto beans. How many tins of beans did Brendan use in all?",
                "unit": "tins",
                "operation": "add",
                "context": "cooking"
            },
            {
                "template": "Of the shirts in Brenna's closet, {frac1} are blue and another {frac2} are teal. What fraction of the shirts are either blue or teal?",
                "unit": "of the shirts",
                "operation": "add",
                "context": "clothing"
            },
            {
                "template": "A recipe calls for {frac1} cup of sugar. Maya has already added {frac2} cup. How much more sugar does she need?",
                "unit": "cups",
                "operation": "subtract",
                "context": "cooking"
            }
        ],
        4: [  # Advanced - complex scenarios
            {
                "template": "At the school fair, {frac1} of the games were skill-based and {frac2} were chance-based. If the rest were sports games, what fraction were either skill or chance games?",
                "unit": "of the games",
                "operation": "add",
                "context": "event"
            },
            {
                "template": "A scientist mixed {frac1} liter of solution A with {frac2} liter of solution B. How many liters of mixture were created?",
                "unit": "liters",
                "operation": "add",
                "context": "science"
            },
            {
                "template": "During a marathon, runners complete {frac1} of the race at checkpoint A and reach {frac2} of the total distance at checkpoint B. How much of the race is between the two checkpoints?",
                "unit": "of the race",
                "operation": "subtract",
                "context": "sports"
            }
        ],
        5: [  # Challenge - complex fractions and contexts
            {
                "template": "A charity collected donations where {frac1} came from individual donors and {frac2} from corporate sponsors. What fraction of donations came from these two sources combined?",
                "unit": "of donations",
                "operation": "add",
                "context": "charity"
            },
            {
                "template": "In a nature reserve, {frac1} of the area is forest. Recent conservation efforts converted {frac2} of the total area from grassland to forest. What fraction is now forest?",
                "unit": "of the reserve",
                "operation": "add",
                "context": "environment"
            },
            {
                "template": "An artist completed {frac1} of a mural. Due to weather damage, {frac2} of the entire mural needs to be redone. What fraction of the mural remains intact?",
                "unit": "of the mural",
                "operation": "subtract",
                "context": "art"
            }
        ]
    }
    
    # Select appropriate problem template
    templates = problem_templates[level]
    problem_data = random.choice(templates)
    
    # Generate appropriate fractions based on level
    fractions = generate_fractions_for_level(level, problem_data["operation"])
    
    # Create the problem text
    problem_text = problem_data["template"].format(
        frac1=fractions["frac1"],
        frac2=fractions["frac2"]
    )
    
    # Calculate the answer
    if problem_data["operation"] == "add":
        result = fractions["frac1_obj"] + fractions["frac2_obj"]
    else:
        result = fractions["frac1_obj"] - fractions["frac2_obj"]
    
    st.session_state.current_word_problem = {
        "text": problem_text,
        "unit": problem_data["unit"],
        "operation": problem_data["operation"],
        "frac1": fractions["frac1_obj"],
        "frac2": fractions["frac2_obj"],
        "result": result,
        "context": problem_data["context"]
    }

def generate_fractions_for_level(level, operation):
    """Generate appropriate fractions based on difficulty level"""
    # Denominator sets by level
    level_denominators = {
        1: [2, 3, 4],
        2: [2, 3, 4, 5, 6],
        3: [3, 4, 5, 6, 8, 10, 12],
        4: [4, 5, 6, 8, 9, 10, 12, 15],
        5: [6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
    }
    
    denominators = level_denominators[level]
    
    # Generate fractions
    attempts = 0
    while attempts < 50:
        denom1 = random.choice(denominators)
        denom2 = random.choice([d for d in denominators if d != denom1])
        
        if level <= 2:
            num1 = random.randint(1, min(denom1 - 1, 3))
            num2 = random.randint(1, min(denom2 - 1, 3))
        else:
            num1 = random.randint(1, denom1 - 1)
            num2 = random.randint(1, denom2 - 1)
        
        frac1 = Fraction(num1, denom1)
        frac2 = Fraction(num2, denom2)
        
        # For subtraction, ensure positive result
        if operation == "subtract" and frac1 < frac2:
            frac1, frac2 = frac2, frac1
            num1, denom1, num2, denom2 = num2, denom2, num1, denom1
        
        # Check if result is reasonable
        if operation == "add":
            result = frac1 + frac2
            if level <= 2 and result > 2:
                continue
        else:
            result = frac1 - frac2
            if result <= 0:
                continue
        
        break
        attempts += 1
    
    return {
        "frac1": f"{num1}/{denom1}",
        "frac2": f"{num2}/{denom2}",
        "frac1_obj": frac1,
        "frac2_obj": frac2
    }

def display_word_problem():
    """Display the current word problem"""
    problem = st.session_state.current_word_problem
    
    # Display problem in a nice box
    st.markdown(f"""
    <div class="word-problem">
        {problem['text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Instruction line
    st.markdown("*Write your answer as a fraction or as a whole or mixed number.*")
    
    # Answer input with unit
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if not st.session_state.answer_submitted:
            answer = st.text_input("", key="answer_input", label_visibility="collapsed",
                                 placeholder="Answer")
        else:
            # Show result
            if st.session_state.user_correct:
                st.markdown(f"""
                <div style='color: green; font-size: 20px; font-weight: bold;'>
                    ✓ {problem['result']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='color: red; font-size: 20px; font-weight: bold;'>
                    ✗ {problem['result']}
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='margin-top: 8px; font-size: 18px;'>{problem['unit']}</div>", 
                   unsafe_allow_html=True)
    
    # Submit button
    if not st.session_state.answer_submitted:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        with col2:
            if st.button("Next Problem →", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def check_answer():
    """Check answer and update difficulty"""
    user_input = st.session_state.answer_input.strip()
    
    if not user_input:
        st.warning("Please enter an answer.")
        return
    
    try:
        # Parse mixed numbers (e.g., "1 1/2")
        if ' ' in user_input:
            parts = user_input.split(' ')
            if len(parts) == 2 and '/' in parts[1]:
                whole = int(parts[0])
                frac_parts = parts[1].split('/')
                num = int(frac_parts[0])
                denom = int(frac_parts[1])
                user_answer = Fraction(whole * denom + num, denom)
            else:
                st.error("Invalid format. Use: whole number, fraction (3/4), or mixed (1 1/2)")
                return
        elif '/' in user_input:
            parts = user_input.split('/')
            if len(parts) == 2:
                num = int(parts[0])
                denom = int(parts[1])
                if denom == 0:
                    st.error("Denominator cannot be zero.")
                    return
                user_answer = Fraction(num, denom)
            else:
                st.error("Invalid fraction format.")
                return
        else:
            user_answer = Fraction(int(user_input), 1)
    
    except ValueError:
        st.error("Please enter a valid number, fraction (3/4), or mixed number (1 1/2).")
        return
    
    # Check if correct
    correct_answer = st.session_state.current_word_problem['result']
    st.session_state.user_correct = (user_answer == correct_answer)
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    
    # Update difficulty
    if st.session_state.user_correct:
        st.session_state.word_problem_streak += 1
        st.session_state.word_problem_mistakes = 0
        
        if st.session_state.word_problem_streak >= 3 and st.session_state.word_problem_level < 5:
            st.session_state.word_problem_level += 1
            st.session_state.word_problem_streak = 0
    else:
        st.session_state.word_problem_mistakes += 1
        st.session_state.word_problem_streak = 0
        
        if st.session_state.word_problem_mistakes >= 2 and st.session_state.word_problem_level > 1:
            st.session_state.word_problem_level -= 1
            st.session_state.word_problem_mistakes = 0
    
    st.rerun()

def show_feedback():
    """Display feedback with solution"""
    problem = st.session_state.current_word_problem
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Excellent work!**")
        if st.session_state.word_problem_streak == 2:
            st.info("🔥 **One more correct answer to level up!**")
        elif st.session_state.word_problem_streak == 0 and st.session_state.word_problem_level < 5:
            st.balloons()
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.word_problem_level}**")
    else:
        st.error(f"❌ **Not quite. The correct answer is {problem['result']} {problem['unit']}**")
        if st.session_state.word_problem_mistakes == 1:
            st.warning("💡 **Tip:** Read the problem carefully and identify what operation to use.")
        
        # Show solution
        with st.expander("📖 **See step-by-step solution**", expanded=True):
            show_solution(problem)

def show_solution(problem):
    """Show step-by-step solution"""
    st.markdown("### Solution:")
    
    # Step 1: Understand the problem
    st.markdown("**Step 1: Understand what we need to find**")
    if problem['operation'] == 'add':
        st.markdown(f"We need to find the total/combined amount.")
    else:
        st.markdown(f"We need to find the difference/what's left.")
    
    # Step 2: Identify the fractions
    st.markdown(f"""
    **Step 2: Identify the fractions**
    - First amount: {problem['frac1']}
    - Second amount: {problem['frac2']}
    """)
    
    # Step 3: Set up the problem
    op_word = "add" if problem['operation'] == 'add' else "subtract"
    op_symbol = "+" if problem['operation'] == 'add' else "−"
    st.markdown(f"""
    **Step 3: Set up the problem**
    - We need to {op_word}: {problem['frac1']} {op_symbol} {problem['frac2']}
    """)
    
    # Step 4: Solve
    from math import gcd
    lcd = abs(problem['frac1'].denominator * problem['frac2'].denominator) // gcd(problem['frac1'].denominator, problem['frac2'].denominator)
    
    equiv1_num = problem['frac1'].numerator * (lcd // problem['frac1'].denominator)
    equiv2_num = problem['frac2'].numerator * (lcd // problem['frac2'].denominator)
    
    st.markdown(f"""
    **Step 4: Find common denominator and solve**
    - LCD of {problem['frac1'].denominator} and {problem['frac2'].denominator} = {lcd}
    - {problem['frac1']} = {equiv1_num}/{lcd}
    - {problem['frac2']} = {equiv2_num}/{lcd}
    """)
    
    if problem['operation'] == 'add':
        st.markdown(f"- {equiv1_num}/{lcd} + {equiv2_num}/{lcd} = {equiv1_num + equiv2_num}/{lcd}")
    else:
        st.markdown(f"- {equiv1_num}/{lcd} − {equiv2_num}/{lcd} = {equiv1_num - equiv2_num}/{lcd}")
    
    st.markdown(f"""
    **Step 5: Simplify**
    - Final answer: **{problem['result']} {problem['unit']}**
    """)

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_word_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_answer'):
        del st.session_state.user_answer
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct