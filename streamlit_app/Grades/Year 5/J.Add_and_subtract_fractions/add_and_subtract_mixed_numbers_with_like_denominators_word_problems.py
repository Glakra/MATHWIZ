import streamlit as st
import random
from fractions import Fraction
import re

def run():
    """
    Main function to run the Add and subtract mixed numbers with like denominators word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_mixed_numbers_with_like_denominators_word_problems.py
    """
    # Initialize session state
    if "mixed_word_difficulty" not in st.session_state:
        st.session_state.mixed_word_difficulty = 1  # Start with simple problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.score = {"correct": 0, "attempted": 0}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("📖 Mixed Numbers: Word Problems")
    st.markdown("*Solve real-world problems with mixed numbers that have the same denominator*")
    st.markdown("---")
    
    # Display score and difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Difficulty indicator
        diff_names = ["Easy", "Medium", "Hard", "Expert"]
        diff_level = st.session_state.mixed_word_difficulty
        st.markdown(f"**Difficulty:** {diff_names[diff_level-1]}")
        
        # Progress bar
        progress = (diff_level - 1) / 3
        st.progress(progress, text=f"Level {diff_level}/4")
    
    with col2:
        # Score display
        score = st.session_state.score
        if score["attempted"] > 0:
            percentage = (score["correct"] / score["attempted"]) * 100
            st.metric("Score", f"{score['correct']}/{score['attempted']}", f"{percentage:.0f}%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Help & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Mixed Number Word Problems:
        
        **Step 1: Identify the numbers**
        - Find the mixed numbers in the problem
        - Note what operation to use (add or subtract)
        
        **Step 2: Set up the problem**
        - Write the equation with the mixed numbers
        - Make sure denominators are the same
        
        **Step 3: Solve**
        - Add/subtract whole numbers
        - Add/subtract fractions
        - Simplify if needed
        
        ### Example:
        "A baker used 2 3/4 cups of flour for bread and 1 1/4 cups for cookies. How much flour in total?"
        - 2 3/4 + 1 1/4
        - = (2 + 1) + (3/4 + 1/4)
        - = 3 + 4/4
        - = 3 + 1 = 4 cups
        
        ### How to Enter Your Answer:
        - **Whole number:** Just type the number (e.g., 5)
        - **Fraction:** Type as numerator/denominator (e.g., 3/4)
        - **Mixed number:** Type as whole fraction (e.g., 2 3/4)
        
        ### Tips:
        - Read carefully to identify if you add or subtract
        - Check your answer makes sense in context
        - Remember to include the unit in your thinking
        """)

def generate_new_problem():
    """Generate a new mixed number word problem based on difficulty"""
    difficulty = st.session_state.mixed_word_difficulty
    
    # Define denominators by difficulty
    if difficulty == 1:
        denominators = [2, 3, 4]         # Easy
        whole_range = (1, 5)
    elif difficulty == 2:
        denominators = [4, 5, 6, 8]      # Medium
        whole_range = (2, 10)
    elif difficulty == 3:
        denominators = [8, 10, 12]       # Hard
        whole_range = (3, 15)
    else:
        denominators = [12, 16, 20]      # Expert
        whole_range = (5, 20)
    
    # Define problem scenarios
    scenarios = [
        # Food & Cooking scenarios
        {
            "type": "cooking",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person} is making a cake that requires {num1} cups of flour for the batter and {num2} cups for the frosting. How much flour does {person} need in total?",
                    "unit": "cups",
                    "names": ["Maria", "James", "Sophie", "David", "Emma", "Lucas"]
                },
                {
                    "operation": "subtract",
                    "template": "A recipe calls for {num1} cups of sugar. {person} has already added {num2} cups. How much more sugar is needed?",
                    "unit": "cups",
                    "names": ["Sarah", "Michael", "Anna", "Robert", "Lisa", "Tom"]
                },
                {
                    "operation": "add",
                    "template": "For breakfast, {person} ate {num1} slices of pizza and for lunch ate {num2} more slices. How many slices did {person} eat altogether?",
                    "unit": "slices",
                    "names": ["Alex", "Jordan", "Sam", "Chris", "Pat", "Taylor"]
                },
                {
                    "operation": "subtract",
                    "template": "{person} bought {num1} pounds of chocolate. After making brownies, {num2} pounds were used. How much chocolate remains?",
                    "unit": "pounds",
                    "names": ["Rachel", "Kevin", "Diana", "Peter", "Grace", "Mark"]
                }
            ]
        },
        
        # Beverages scenarios
        {
            "type": "beverages",
            "templates": [
                {
                    "operation": "add",
                    "template": "Yesterday, Just Sip Awhile Cafe sold {num1} carafes of caffeinated coffee and {num2} carafes of decaffeinated coffee. How many carafes of coffee did they sell in all?",
                    "unit": "carafes"
                },
                {
                    "operation": "subtract",
                    "template": "A tea shop brewed {num1} jugs of chamomile tea, of which it sold {num2} jugs. How many jugs remained unsold?",
                    "unit": "jugs"
                },
                {
                    "operation": "add",
                    "template": "The juice bar made {num1} liters of orange juice in the morning and {num2} liters in the afternoon. What was the total production?",
                    "unit": "liters"
                },
                {
                    "operation": "subtract",
                    "template": "A coffee shop had {num1} gallons of cold brew. They sold {num2} gallons during lunch rush. How much cold brew is left?",
                    "unit": "gallons"
                }
            ]
        },
        
        # Construction & Materials scenarios
        {
            "type": "construction",
            "templates": [
                {
                    "operation": "add",
                    "template": "A carpenter used {num1} meters of wood for shelving and {num2} meters for a table. How much wood was used in total?",
                    "unit": "meters"
                },
                {
                    "operation": "subtract",
                    "template": "A construction site had {num1} tons of cement. Workers used {num2} tons for the foundation. How much cement remains?",
                    "unit": "tons"
                },
                {
                    "operation": "add",
                    "template": "{person} cut {num1} yards of fabric for curtains and {num2} yards for cushions. How much fabric was cut altogether?",
                    "unit": "yards",
                    "names": ["Helen", "George", "Martha", "Frank", "Betty", "Carl"]
                },
                {
                    "operation": "subtract",
                    "template": "A painter had {num1} gallons of paint. After painting two rooms, {num2} gallons were used. How much paint is left?",
                    "unit": "gallons"
                }
            ]
        },
        
        # Inventory & Storage scenarios
        {
            "type": "inventory",
            "templates": [
                {
                    "operation": "subtract",
                    "template": "While taking inventory at her pastry shop, Leslie realises that she had {num1} boxes of baking powder yesterday, but the supply is now down to {num2} boxes. How much more baking powder did Leslie have yesterday?",
                    "unit": "boxes"
                },
                {
                    "operation": "add",
                    "template": "A warehouse received {num1} crates of supplies on Monday and {num2} crates on Tuesday. How many crates were received in total?",
                    "unit": "crates"
                },
                {
                    "operation": "subtract",
                    "template": "A store had {num1} cases of soda in stock. After a busy weekend, only {num2} cases remained. How many cases were sold?",
                    "unit": "cases"
                },
                {
                    "operation": "add",
                    "template": "The library received {num1} boxes of new books in January and {num2} boxes in February. How many boxes in total?",
                    "unit": "boxes"
                }
            ]
        },
        
        # Distance & Travel scenarios
        {
            "type": "travel",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person} walked {num1} miles to the park and then {num2} miles to the store. What was the total distance walked?",
                    "unit": "miles",
                    "names": ["John", "Mary", "Steve", "Linda", "Mike", "Susan"]
                },
                {
                    "operation": "subtract",
                    "template": "A delivery truck needs to travel {num1} kilometers. It has already covered {num2} kilometers. How much farther must it go?",
                    "unit": "kilometers"
                },
                {
                    "operation": "add",
                    "template": "A cyclist rode {num1} miles on Saturday and {num2} miles on Sunday. What was the weekend total?",
                    "unit": "miles"
                },
                {
                    "operation": "subtract",
                    "template": "A marathon is {num1} miles long. {person} has completed {num2} miles. How many miles remain?",
                    "unit": "miles",
                    "names": ["Dan", "Amy", "Joe", "Kate", "Ben", "Eve"]
                }
            ]
        },
        
        # Time scenarios
        {
            "type": "time",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person} studied math for {num1} hours on Monday and {num2} hours on Tuesday. How many hours did {person} study in total?",
                    "unit": "hours",
                    "names": ["Oliver", "Sophia", "William", "Emily", "James", "Ava"]
                },
                {
                    "operation": "subtract",
                    "template": "A movie is {num1} hours long. {person} has watched {num2} hours. How much is left to watch?",
                    "unit": "hours",
                    "names": ["Noah", "Emma", "Liam", "Olivia", "Mason", "Isabella"]
                },
                {
                    "operation": "add",
                    "template": "A project took {num1} days to plan and {num2} days to execute. What was the total time?",
                    "unit": "days"
                },
                {
                    "operation": "subtract",
                    "template": "{person} has {num1} weeks of vacation time. After a trip, {num2} weeks remain. How long was the trip?",
                    "unit": "weeks",
                    "names": ["Lucas", "Mia", "Ethan", "Harper", "Jacob", "Ella"]
                }
            ]
        },
        
        # Garden & Nature scenarios
        {
            "type": "garden",
            "templates": [
                {
                    "operation": "add",
                    "template": "A gardener planted {num1} rows of tomatoes and {num2} rows of peppers. How many rows were planted in total?",
                    "unit": "rows"
                },
                {
                    "operation": "subtract",
                    "template": "{person} had {num1} bags of soil. After planting flowers, {num2} bags remain. How many bags were used?",
                    "unit": "bags",
                    "names": ["Rose", "Jack", "Lily", "Oscar", "Daisy", "Henry"]
                },
                {
                    "operation": "add",
                    "template": "A farm harvested {num1} bushels of apples from the north orchard and {num2} bushels from the south orchard. What was the total harvest?",
                    "unit": "bushels"
                },
                {
                    "operation": "subtract",
                    "template": "A nursery had {num1} flats of seedlings. They sold {num2} flats at the farmer's market. How many flats are left?",
                    "unit": "flats"
                }
            ]
        },
        
        # Money & Finance scenarios
        {
            "type": "money",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person} saved ${num1} thousand in January and ${num2} thousand in February. How much was saved in total?",
                    "unit": "thousand dollars",
                    "names": ["Richard", "Patricia", "Charles", "Jennifer", "Joseph", "Barbara"]
                },
                {
                    "operation": "subtract",
                    "template": "A charity goal was ${num1} thousand. They have raised ${num2} thousand so far. How much more is needed?",
                    "unit": "thousand dollars"
                },
                {
                    "operation": "add",
                    "template": "A business earned ${num1} million in Q1 and ${num2} million in Q2. What was the total for the first half?",
                    "unit": "million dollars"
                },
                {
                    "operation": "subtract",
                    "template": "{person} had ${num1} hundred in savings. After buying a bike, ${num2} hundred remained. How much did the bike cost?",
                    "unit": "hundred dollars",
                    "names": ["Paul", "Nancy", "Daniel", "Karen", "Matthew", "Betty"]
                }
            ]
        },
        
        # Sports & Exercise scenarios
        {
            "type": "sports",
            "templates": [
                {
                    "operation": "add",
                    "template": "A basketball player scored {num1} points in the first half and {num2} points in the second half. What was the total score?",
                    "unit": "points"
                },
                {
                    "operation": "subtract",
                    "template": "A swimmer's goal is {num1} laps. They have completed {num2} laps. How many more laps to go?",
                    "unit": "laps"
                },
                {
                    "operation": "add",
                    "template": "{person} ran {num1} miles on the track and {num2} miles on the trail. What was the total distance?",
                    "unit": "miles",
                    "names": ["Tyler", "Ashley", "Ryan", "Jessica", "Brian", "Nicole"]
                },
                {
                    "operation": "subtract",
                    "template": "A yoga class is {num1} hours long. After {num2} hours, how much time remains?",
                    "unit": "hours"
                }
            ]
        },
        
        # Art & Craft scenarios
        {
            "type": "art",
            "templates": [
                {
                    "operation": "add",
                    "template": "An artist used {num1} tubes of blue paint and {num2} tubes of red paint for a mural. How many tubes in total?",
                    "unit": "tubes"
                },
                {
                    "operation": "subtract",
                    "template": "{person} bought {num1} skeins of yarn. After knitting a sweater, {num2} skeins remain. How many were used?",
                    "unit": "skeins",
                    "names": ["Laura", "Jason", "Amanda", "Kevin", "Melissa", "Brandon"]
                },
                {
                    "operation": "add",
                    "template": "A sculptor used {num1} blocks of clay for one statue and {num2} blocks for another. How many blocks total?",
                    "unit": "blocks"
                },
                {
                    "operation": "subtract",
                    "template": "An art class had {num1} bottles of glue. After a project, {num2} bottles were left. How many were used?",
                    "unit": "bottles"
                }
            ]
        }
    ]
    
    # Choose random scenario
    scenario_type = random.choice(scenarios)
    template_data = random.choice(scenario_type["templates"])
    
    # Generate mixed numbers
    denominator = random.choice(denominators)
    
    if template_data["operation"] == "add":
        # For addition
        whole1 = random.randint(whole_range[0], whole_range[1])
        num1 = random.randint(1, denominator - 1)
        
        whole2 = random.randint(whole_range[0], whole_range[1])
        num2 = random.randint(1, denominator - 1)
        
        # Calculate answer
        total_whole = whole1 + whole2
        total_num = num1 + num2
        
        # Handle improper fraction
        if total_num >= denominator:
            extra_whole = total_num // denominator
            total_whole += extra_whole
            total_num = total_num % denominator
        
        # Create answer
        if total_num == 0:
            answer_str = str(total_whole)
            answer_value = total_whole
        else:
            answer_frac = Fraction(total_num, denominator)
            answer_str = f"{total_whole} {answer_frac}"
            answer_value = total_whole + answer_frac
            
    else:  # subtract
        # For subtraction, ensure first number is larger
        whole1 = random.randint(whole_range[0] + 2, whole_range[1])
        whole2 = random.randint(whole_range[0], min(whole1 - 1, whole_range[1] - 2))
        
        # Generate fractions
        num1 = random.randint(1, denominator - 1)
        num2 = random.randint(1, denominator - 1)
        
        # Store original values for display
        display_whole1 = whole1
        display_num1 = num1
        
        # Handle borrowing if needed
        if num1 < num2:
            # Need to borrow
            whole1 -= 1
            num1 += denominator
        
        # Calculate answer
        result_whole = whole1 - whole2
        result_num = num1 - num2
        
        # Create answer
        if result_num == 0:
            answer_str = str(result_whole)
            answer_value = result_whole
        else:
            answer_frac = Fraction(result_num, denominator)
            answer_str = f"{result_whole} {answer_frac}"
            answer_value = result_whole + answer_frac
    
    # Format the problem text
    problem_text = template_data["template"]
    
    # Replace placeholders
    if "{person}" in problem_text and "names" in template_data:
        name = random.choice(template_data["names"])
        problem_text = problem_text.replace("{person}", name)
    
    # Format mixed numbers for display
    if template_data["operation"] == "add":
        mixed1 = f"{whole1} {num1}/{denominator}"
        mixed2 = f"{whole2} {num2}/{denominator}"
    else:
        mixed1 = f"{display_whole1} {display_num1}/{denominator}"
        mixed2 = f"{whole2} {num2}/{denominator}"
    
    problem_text = problem_text.replace("{num1}", mixed1)
    problem_text = problem_text.replace("{num2}", mixed2)
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "operation": template_data["operation"],
        "mixed1": mixed1,
        "mixed2": mixed2,
        "answer_str": answer_str,
        "answer_value": answer_value,
        "unit": template_data["unit"]
    }
    
    st.session_state.current_problem = problem_text
    st.session_state.correct_answer = answer_str

def parse_mixed_answer(answer_str):
    """Parse various answer formats: whole number, fraction, or mixed number"""
    answer_str = answer_str.strip()
    
    # Check for whole number only
    if answer_str.isdigit():
        return int(answer_str)
    
    # Check for fraction only (e.g., "3/4")
    fraction_match = re.match(r'^(\d+)\s*/\s*(\d+)$', answer_str)
    if fraction_match:
        num = int(fraction_match.group(1))
        denom = int(fraction_match.group(2))
        if denom > 0:
            return Fraction(num, denom)
    
    # Check for mixed number (e.g., "2 3/4" or "2 3/4")
    mixed_match = re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)$', answer_str)
    if mixed_match:
        whole = int(mixed_match.group(1))
        num = int(mixed_match.group(2))
        denom = int(mixed_match.group(3))
        if denom > 0:
            return whole + Fraction(num, denom)
    
    return None

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display the problem in a nice box
    st.info(st.session_state.current_problem)
    
    # Add instruction line
    st.markdown("*Write your answer as a fraction or as a whole or mixed number.*")
    
    # Answer input section
    with st.form("answer_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            answer_input = st.text_input(
                "Your answer:",
                placeholder="e.g., 5 or 3/4 or 2 1/2",
                key="user_answer_input",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown(f"**{data['unit']}**")
        
        # Submit button
        submit_button = st.form_submit_button(
            "Submit", 
            type="primary", 
            use_container_width=True
        )
        
        if submit_button:
            # Parse the answer
            parsed_answer = parse_mixed_answer(answer_input)
            
            if parsed_answer is None:
                st.error("❌ Please enter a valid answer (whole number, fraction, or mixed number)")
            else:
                st.session_state.user_answer = parsed_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.score["attempted"] += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if "user_answer" not in st.session_state:
        return
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.problem_data["answer_value"]
    data = st.session_state.problem_data
    
    # Compare answers
    if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
        is_correct = abs(user_answer - correct_answer) < 0.0001
    else:
        is_correct = user_answer == correct_answer
    
    if is_correct:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.score["correct"] += 1
        
        # Show the complete solution
        st.markdown(f"### ✅ Answer: {st.session_state.correct_answer} {data['unit']}")
        
        # Increase difficulty if doing well
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate >= 0.8 and st.session_state.mixed_word_difficulty < 4:
                st.session_state.mixed_word_difficulty += 1
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.mixed_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{st.session_state.correct_answer} {data['unit']}**")
        
        # Show step-by-step solution
        show_solution()
        
        # Decrease difficulty if struggling
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate < 0.5 and st.session_state.mixed_word_difficulty > 1:
                st.session_state.mixed_word_difficulty -= 1
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.mixed_word_difficulty}**")

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        st.markdown(f"""
        **Problem:** {data['problem_text']}
        
        **Step 1: Identify the numbers**
        - First mixed number: {data['mixed1']}
        - Second mixed number: {data['mixed2']}
        - Operation: {data['operation']}
        """)
        
        if data['operation'] == "add":
            st.markdown(f"""
            **Step 2: Set up the addition**
            {data['mixed1']} + {data['mixed2']}
            
            **Step 3: Add the whole numbers and fractions separately**
            - Add whole numbers first
            - Add fractions with same denominator
            - Simplify if needed
            
            **Answer:** {st.session_state.correct_answer} {data['unit']}
            """)
        else:
            st.markdown(f"""
            **Step 2: Set up the subtraction**
            {data['mixed1']} − {data['mixed2']}
            
            **Step 3: Subtract (may need borrowing)**
            - Check if you can subtract the fractions
            - If not, borrow from the whole number
            - Subtract whole numbers and fractions
            
            **Answer:** {st.session_state.correct_answer} {data['unit']}
            """)
        
        # Add a tip about reasonableness
        st.markdown("""
        **💡 Check:** Does the answer make sense in the context of the problem?
        """)

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer