import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Mixed Numbers Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_mixed_numbers_with_unlike_denominators_word_problems.py
    """
    # Initialize session state
    if "mixed_word_level" not in st.session_state:
        st.session_state.mixed_word_level = 1
    
    if "mixed_word_streak" not in st.session_state:
        st.session_state.mixed_word_streak = 0
    
    if "mixed_word_mistakes" not in st.session_state:
        st.session_state.mixed_word_mistakes = 0
    
    if "current_mixed_word_problem" not in st.session_state:
        st.session_state.current_mixed_word_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Word problem styling */
    .word-problem {
        font-size: 18px;
        line-height: 1.6;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Input field */
    input[type="text"] {
        font-size: 16px !important;
        width: 150px !important;
    }
    
    /* Submit button */
    div.stButton > button[type="submit"] {
        background-color: #4CAF50;
        color: white;
    }
    
    /* Mixed number display in solution */
    .mixed-display {
        font-size: 20px;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("📖 Mixed Numbers: Word Problems")
    st.markdown("*Solve real-world problems with mixed numbers*")
    
    # Difficulty and progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        level_names = {1: "Basic", 2: "Simple", 3: "Standard", 4: "Advanced", 5: "Challenge"}
        level_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🟣"}
        level = st.session_state.mixed_word_level
        st.markdown(f"**Level:** {level_colors[level]} {level_names[level]}")
        st.progress(level / 5, text=f"Progress: {level}/5")
    
    with col2:
        if st.session_state.mixed_word_streak > 0:
            st.metric("Streak", f"🔥 {st.session_state.mixed_word_streak}")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    st.markdown("---")
    
    # Generate new problem if needed
    if st.session_state.current_mixed_word_problem is None:
        generate_mixed_word_problem()
    
    # Display problem
    display_mixed_word_problem()
    
    # Tips
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### Solving Mixed Number Word Problems:
        
        **Step 1: Read Carefully**
        - What quantities are given?
        - What are you asked to find?
        - Is it addition or subtraction?
        
        **Step 2: Identify Keywords**
        - **Addition**: total, combined, altogether, mixed together
        - **Subtraction**: left, remaining, used, difference, how much more
        
        **Step 3: Convert Mixed Numbers**
        - Convert to improper fractions
        - Find common denominator
        - Calculate
        - Convert back to mixed number
        
        **Step 4: Check Your Answer**
        - Does it make sense?
        - Is it in simplest form?
        - Does it answer what was asked?
        
        ### Level Progression:
        - **Level 1**: Simple contexts, friendly fractions
        - **Level 2**: Everyday scenarios
        - **Level 3**: Real-world applications
        - **Level 4**: Complex scenarios
        - **Level 5**: Multi-step problems
        """)

def generate_mixed_word_problem():
    """Generate an adaptive mixed number word problem"""
    level = st.session_state.mixed_word_level
    
    # Problem templates by level and type
    problem_templates = {
        1: [  # Basic - simple contexts
            # Addition problems
            {
                "template": "Tom walked {mixed1} miles in the morning and {mixed2} miles in the afternoon. How many miles did Tom walk in total?",
                "unit": "miles",
                "operation": "add",
                "context": "distance"
            },
            {
                "template": "Sarah used {mixed1} cups of flour for cookies and {mixed2} cups for bread. How many cups of flour did she use altogether?",
                "unit": "cups",
                "operation": "add",
                "context": "cooking"
            },
            # Subtraction problems
            {
                "template": "A water jug contained {mixed1} liters. After filling some bottles, {mixed2} liters remained. How many liters were used?",
                "unit": "liters",
                "operation": "subtract",
                "context": "liquid",
                "ask_for": "difference"
            },
            {
                "template": "Jake had {mixed1} pounds of candy. He gave away {mixed2} pounds. How many pounds does he have left?",
                "unit": "pounds",
                "operation": "subtract",
                "context": "food"
            }
        ],
        2: [  # Simple - everyday scenarios
            # Addition
            {
                "template": "Lisa studied {mixed1} hours on Monday and {mixed2} hours on Tuesday. How many hours did she study in total?",
                "unit": "hours",
                "operation": "add",
                "context": "time"
            },
            {
                "template": "A recipe needs {mixed1} cups of milk and {mixed2} cups of cream. How many cups of dairy products are needed?",
                "unit": "cups",
                "operation": "add",
                "context": "cooking"
            },
            # Subtraction
            {
                "template": "A carpenter had {mixed1} meters of wood. After building a shelf, {mixed2} meters were left. How much wood was used?",
                "unit": "meters",
                "operation": "subtract",
                "context": "construction",
                "ask_for": "difference"
            },
            {
                "template": "Emma bought {mixed1} yards of fabric. She used {mixed2} yards for a dress. How much fabric is left?",
                "unit": "yards",
                "operation": "subtract",
                "context": "crafts"
            }
        ],
        3: [  # Standard - real-world applications
            # Addition
            {
                "template": "To make some punch for a party, Dana mixed together {mixed1} bottles of pineapple juice and {mixed2} bottles of club soda. How many bottles of punch did Dana make?",
                "unit": "bottles",
                "operation": "add",
                "context": "party"
            },
            {
                "template": "A baker used {mixed1} pounds of chocolate chips and {mixed2} pounds of walnuts in a batch of cookies. How many pounds of mix-ins were used?",
                "unit": "pounds",
                "operation": "add",
                "context": "baking"
            },
            # Subtraction
            {
                "template": "Mary brought {mixed1} jugs of juice to a volleyball game, and the players drank {mixed2} jugs of it. How much juice is left?",
                "unit": "jugs",
                "operation": "subtract",
                "context": "sports"
            },
            {
                "template": "A farmer started the day with {mixed1} buckets of seeds. After spending the morning sowing seeds, she now has {mixed2} buckets left. How many buckets of seeds did the farmer sow?",
                "unit": "buckets",
                "operation": "subtract",
                "context": "farming",
                "ask_for": "difference"
            }
        ],
        4: [  # Advanced - complex scenarios
            # Addition
            {
                "template": "A construction crew poured {mixed1} cubic yards of concrete on Monday and {mixed2} cubic yards on Tuesday. What was the total amount of concrete poured?",
                "unit": "cubic yards",
                "operation": "add",
                "context": "construction"
            },
            {
                "template": "During a science experiment, {mixed1} liters of solution A were mixed with {mixed2} liters of solution B. How many liters of mixture were created?",
                "unit": "liters",
                "operation": "add",
                "context": "science"
            },
            # Subtraction
            {
                "template": "A fuel tank contained {mixed1} gallons. After a long trip, only {mixed2} gallons remained. How many gallons were used during the trip?",
                "unit": "gallons",
                "operation": "subtract",
                "context": "travel",
                "ask_for": "difference"
            },
            {
                "template": "A warehouse had {mixed1} tons of grain. After shipping orders, {mixed2} tons remained. How many tons were shipped?",
                "unit": "tons",
                "operation": "subtract",
                "context": "shipping",
                "ask_for": "difference"
            }
        ],
        5: [  # Challenge - complex problems
            # Addition
            {
                "template": "An artist mixed {mixed1} quarts of blue paint with {mixed2} quarts of yellow paint to create green. How many quarts of green paint were made?",
                "unit": "quarts",
                "operation": "add",
                "context": "art"
            },
            {
                "template": "A marathon runner completed {mixed1} kilometers in the first segment and {mixed2} kilometers in the second segment. What was the total distance covered?",
                "unit": "kilometers",
                "operation": "add",
                "context": "athletics"
            },
            # Subtraction
            {
                "template": "A swimming pool held {mixed1} thousand gallons of water. After a leak, it now holds {mixed2} thousand gallons. How many thousand gallons leaked out?",
                "unit": "thousand gallons",
                "operation": "subtract",
                "context": "maintenance",
                "ask_for": "difference"
            },
            {
                "template": "A factory produced {mixed1} tons of steel. After fulfilling orders, {mixed2} tons remain in inventory. How many tons were shipped to customers?",
                "unit": "tons",
                "operation": "subtract",
                "context": "manufacturing",
                "ask_for": "difference"
            }
        ]
    }
    
    # Select problem template
    templates = problem_templates[level]
    problem_data = random.choice(templates)
    
    # Generate appropriate mixed numbers
    mixed_nums = generate_mixed_numbers_for_level(level, problem_data["operation"])
    
    # Create problem text
    problem_text = problem_data["template"].format(
        mixed1=format_mixed_for_display(mixed_nums["mixed1"]),
        mixed2=format_mixed_for_display(mixed_nums["mixed2"])
    )
    
    # Calculate result
    if problem_data["operation"] == "add":
        result = mixed_nums["frac1"] + mixed_nums["frac2"]
    else:
        # For subtraction, ensure first > second
        if mixed_nums["frac1"] < mixed_nums["frac2"]:
            mixed_nums["frac1"], mixed_nums["frac2"] = mixed_nums["frac2"], mixed_nums["frac1"]
            mixed_nums["mixed1"], mixed_nums["mixed2"] = mixed_nums["mixed2"], mixed_nums["mixed1"]
        result = mixed_nums["frac1"] - mixed_nums["frac2"]
    
    # Determine what we're asking for
    if problem_data.get("ask_for") == "difference" and problem_data["operation"] == "subtract":
        # We're asking for the difference (what was used/taken)
        actual_result = result
        result = mixed_nums["frac1"] - mixed_nums["frac2"]
    
    st.session_state.current_mixed_word_problem = {
        "text": problem_text,
        "unit": problem_data["unit"],
        "operation": problem_data["operation"],
        "mixed1": mixed_nums["mixed1"],
        "mixed2": mixed_nums["mixed2"],
        "frac1": mixed_nums["frac1"],
        "frac2": mixed_nums["frac2"],
        "result": result,
        "context": problem_data["context"]
    }

def generate_mixed_numbers_for_level(level, operation):
    """Generate appropriate mixed numbers based on level"""
    # Parameters by level
    level_params = {
        1: {
            "whole_range": (1, 5),
            "denominators": [2, 4],
            "max_result": 15
        },
        2: {
            "whole_range": (2, 10),
            "denominators": [2, 3, 4, 6],
            "max_result": 20
        },
        3: {
            "whole_range": (5, 20),
            "denominators": [2, 3, 4, 5, 6, 8],
            "max_result": 30
        },
        4: {
            "whole_range": (10, 30),
            "denominators": [3, 4, 5, 6, 8, 10, 12],
            "max_result": 50
        },
        5: {
            "whole_range": (15, 50),
            "denominators": [4, 5, 6, 8, 9, 10, 12, 15],
            "max_result": 100
        }
    }
    
    params = level_params[level]
    
    attempts = 0
    while attempts < 50:
        # Generate whole parts
        whole1 = random.randint(*params["whole_range"])
        whole2 = random.randint(params["whole_range"][0], whole1)  # Ensure second isn't larger
        
        # Generate fractions
        denom1 = random.choice(params["denominators"])
        denom2 = random.choice([d for d in params["denominators"] if d != denom1])
        
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)
        
        # Create fractions
        frac1 = Fraction(whole1 * denom1 + num1, denom1)
        frac2 = Fraction(whole2 * denom2 + num2, denom2)
        
        # Check constraints
        if operation == "add":
            result = frac1 + frac2
            if result > params["max_result"]:
                continue
        else:  # subtract
            if frac1 < frac2:
                frac1, frac2 = frac2, frac1
                whole1, whole2 = whole2, whole1
                num1, num2, denom1, denom2 = num2, num1, denom2, denom1
            
            result = frac1 - frac2
            if result <= 0:
                continue
        
        break
        attempts += 1
    
    return {
        "mixed1": (whole1, num1, denom1),
        "mixed2": (whole2, num2, denom2),
        "frac1": frac1,
        "frac2": frac2
    }

def format_mixed_for_display(mixed_tuple):
    """Format mixed number tuple as string for display"""
    whole, num, denom = mixed_tuple
    return f"{whole} {num}/{denom}"

def display_mixed_word_problem():
    """Display the current word problem"""
    problem = st.session_state.current_mixed_word_problem
    
    # Display problem in a box
    st.markdown(f"""
    <div class="word-problem">
        {problem['text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Instruction
    st.markdown("*Write your answer as a fraction or as a whole or mixed number.*")
    
    # Answer input
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if not st.session_state.answer_submitted:
            answer = st.text_input("", key="answer_input", label_visibility="collapsed",
                                 placeholder="Answer")
        else:
            # Show result
            result_str = format_mixed_number(problem['result'])
            if st.session_state.user_correct:
                st.markdown(f"""
                <div style='color: green; font-size: 20px; font-weight: bold;'>
                    ✓ {result_str}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='color: red; font-size: 20px; font-weight: bold;'>
                    ✗ {result_str}
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

def format_mixed_number(fraction):
    """Format a fraction as a mixed number string"""
    if fraction.denominator == 1:
        return str(fraction.numerator)
    elif fraction.numerator < fraction.denominator:
        return f"{fraction.numerator}/{fraction.denominator}"
    else:
        whole = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        if remainder == 0:
            return str(whole)
        else:
            return f"{whole} {remainder}/{fraction.denominator}"

def parse_mixed_number(input_str):
    """Parse user input as a mixed number"""
    input_str = input_str.strip()
    
    # Try mixed number (e.g., "2 3/4")
    if ' ' in input_str:
        parts = input_str.split(' ', 1)
        if len(parts) == 2:
            try:
                whole = int(parts[0])
                if '/' in parts[1]:
                    frac_parts = parts[1].split('/')
                    if len(frac_parts) == 2:
                        num = int(frac_parts[0])
                        denom = int(frac_parts[1])
                        if denom == 0:
                            return None, "Denominator cannot be zero"
                        return Fraction(whole * denom + num, denom), None
            except ValueError:
                pass
    
    # Try fraction (e.g., "3/4")
    if '/' in input_str:
        parts = input_str.split('/')
        if len(parts) == 2:
            try:
                num = int(parts[0])
                denom = int(parts[1])
                if denom == 0:
                    return None, "Denominator cannot be zero"
                return Fraction(num, denom), None
            except ValueError:
                pass
    
    # Try whole number
    try:
        whole = int(input_str)
        return Fraction(whole, 1), None
    except ValueError:
        pass
    
    return None, "Invalid format. Use: whole number (5), fraction (3/4), or mixed (2 1/2)"

def check_answer():
    """Check answer and update difficulty"""
    user_input = st.session_state.answer_input
    
    if not user_input:
        st.warning("Please enter an answer.")
        return
    
    # Parse user answer
    user_answer, error = parse_mixed_number(user_input)
    
    if error:
        st.error(error)
        return
    
    # Check if correct
    correct_answer = st.session_state.current_mixed_word_problem['result']
    st.session_state.user_correct = (user_answer == correct_answer)
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    
    # Update difficulty
    if st.session_state.user_correct:
        st.session_state.mixed_word_streak += 1
        st.session_state.mixed_word_mistakes = 0
        
        if st.session_state.mixed_word_streak >= 3 and st.session_state.mixed_word_level < 5:
            st.session_state.mixed_word_level += 1
            st.session_state.mixed_word_streak = 0
    else:
        st.session_state.mixed_word_mistakes += 1
        st.session_state.mixed_word_streak = 0
        
        if st.session_state.mixed_word_mistakes >= 2 and st.session_state.mixed_word_level > 1:
            st.session_state.mixed_word_level -= 1
            st.session_state.mixed_word_mistakes = 0
    
    st.rerun()

def show_feedback():
    """Display feedback with solution"""
    problem = st.session_state.current_mixed_word_problem
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Excellent work!**")
        if st.session_state.mixed_word_streak == 2:
            st.info("🔥 **One more correct answer to level up!**")
        elif st.session_state.mixed_word_streak == 0 and st.session_state.mixed_word_level < 5:
            st.balloons()
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.mixed_word_level}**")
    else:
        result_str = format_mixed_number(problem['result'])
        st.error(f"❌ **Not quite. The correct answer is {result_str} {problem['unit']}**")
        
        # Show solution
        with st.expander("📖 **See step-by-step solution**", expanded=True):
            show_solution(problem)

def show_solution(problem):
    """Show step-by-step solution"""
    st.markdown("### Solution:")
    
    # Step 1: Understand the problem
    st.markdown("**Step 1: Understand the problem**")
    if problem['operation'] == 'add':
        st.markdown(f"We need to find the total by adding the two amounts.")
    else:
        st.markdown(f"We need to find the difference by subtracting.")
    
    # Step 2: Identify the mixed numbers
    mixed1_str = format_mixed_for_display(problem['mixed1'])
    mixed2_str = format_mixed_for_display(problem['mixed2'])
    
    st.markdown(f"""
    **Step 2: Identify the mixed numbers**
    - First amount: <span class="mixed-display">{mixed1_str}</span>
    - Second amount: <span class="mixed-display">{mixed2_str}</span>
    """, unsafe_allow_html=True)
    
    # Step 3: Convert to improper fractions
    whole1, num1, denom1 = problem['mixed1']
    whole2, num2, denom2 = problem['mixed2']
    
    improper1 = whole1 * denom1 + num1
    improper2 = whole2 * denom2 + num2
    
    st.markdown(f"""
    **Step 3: Convert to improper fractions**
    - {mixed1_str} = {improper1}/{denom1}
    - {mixed2_str} = {improper2}/{denom2}
    """)
    
    # Step 4: Find LCD and convert
    from math import gcd
    lcd = abs(denom1 * denom2) // gcd(denom1, denom2)
    
    equiv1 = improper1 * (lcd // denom1)
    equiv2 = improper2 * (lcd // denom2)
    
    st.markdown(f"""
    **Step 4: Find common denominator**
    - LCD of {denom1} and {denom2} = {lcd}
    - {improper1}/{denom1} = {equiv1}/{lcd}
    - {improper2}/{denom2} = {equiv2}/{lcd}
    """)
    
    # Step 5: Calculate
    op_symbol = "+" if problem['operation'] == 'add' else "−"
    if problem['operation'] == 'add':
        result_num = equiv1 + equiv2
    else:
        result_num = equiv1 - equiv2
    
    st.markdown(f"""
    **Step 5: {problem['operation'].capitalize()}**
    - {equiv1}/{lcd} {op_symbol} {equiv2}/{lcd} = {result_num}/{lcd}
    """)
    
    # Step 6: Convert back to mixed number
    result_str = format_mixed_number(problem['result'])
    
    st.markdown(f"""
    **Step 6: Simplify and convert to mixed number**
    - {result_num}/{lcd} = **{result_str}**
    
    **Answer: {result_str} {problem['unit']}**
    """)

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_mixed_word_problem = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_answer'):
        del st.session_state.user_answer
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct