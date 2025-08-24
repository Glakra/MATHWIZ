import streamlit as st
import random
from fractions import Fraction
import re

def run():
    """
    Main function to run the Add and subtract fractions with like denominators word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/add_and_subtract_fractions_with_like_denominators_word_problems.py
    """
    # Initialize session state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with simple denominators
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.score = {"correct": 0, "attempted": 0}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🍕 Add & Subtract Fractions: Word Problems")
    st.markdown("*Solve real-world problems with fractions that have the same denominator*")
    st.markdown("---")
    
    # Display score and difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Difficulty indicator
        diff_names = ["Easy", "Medium", "Hard", "Expert"]
        diff_level = st.session_state.fractions_difficulty
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
        try:
            generate_new_problem()
        except Exception as e:
            st.error(f"Error generating problem: {str(e)}")
            if st.button("Try Again"):
                st.rerun()
            return
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Help & Tips**", expanded=False):
        st.markdown("""
        ### How to Add/Subtract Fractions with Like Denominators:
        
        **When denominators are the same:**
        1. **Add or subtract** only the numerators (top numbers)
        2. **Keep** the same denominator (bottom number)
        3. **Simplify** the answer if possible
        
        ### Examples:
        - **Addition:** 2/5 + 1/5 = 3/5 (add 2+1=3, keep denominator 5)
        - **Subtraction:** 7/8 - 3/8 = 4/8 = 1/2 (subtract 7-3=4, simplify)
        
        ### How to Enter Your Answer:
        - Type your answer as a fraction: **numerator/denominator**
        - Examples: **3/4**, **5/8**, **1/2**
        
        ### Word Problem Tips:
        - 🔍 **Look for keywords:**
          - Add: "altogether", "in total", "combined"
          - Subtract: "left", "remains", "how much more"
        - 📝 **Write the equation** before solving
        - ✅ **Check** if your answer makes sense
        """)

def generate_new_problem():
    """Generate a new fraction word problem based on difficulty"""
    difficulty = st.session_state.fractions_difficulty
    
    # Define denominators by difficulty
    if difficulty == 1:
        denominators = [2, 3, 4, 5, 6]  # Easy
    elif difficulty == 2:
        denominators = [6, 8, 10, 12]   # Medium
    elif difficulty == 3:
        denominators = [12, 15, 16, 20] # Hard
    else:
        denominators = [20, 24, 25, 30] # Expert
    
    # Define problem scenarios
    scenarios = [
        # Food scenarios
        {
            "type": "pizza",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person1} ate {frac1} of a pizza. {person2} ate {frac2} of the same pizza. How much of the pizza did they eat altogether?",
                    "unit": "of the pizza",
                    "names": ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason"]
                },
                {
                    "operation": "subtract",
                    "template": "A pizza was cut into {denom} equal slices. {frac1} of the pizza remained after lunch. If {frac2} was eaten later, how much pizza is left?",
                    "unit": "of the pizza",
                    "names": ["Sarah", "James", "Isabella", "William", "Mia", "Alexander"]
                }
            ]
        },
        {
            "type": "cake",
            "templates": [
                {
                    "operation": "add",
                    "template": "Grandma baked a cake. She gave {frac1} to the neighbors and {frac2} to her grandchildren. What fraction of the cake did she give away?",
                    "unit": "of the cake"
                },
                {
                    "operation": "subtract",
                    "template": "A birthday cake was divided into {denom} pieces. After the party, {frac1} of the cake remained. If {frac2} was eaten the next day, how much cake is left?",
                    "unit": "of the cake"
                }
            ]
        },
        
        # Water/Liquid scenarios
        {
            "type": "water",
            "templates": [
                {
                    "operation": "add",
                    "template": "A water tank was {frac1} full in the morning. After rain, it filled up another {frac2}. What fraction of the tank is full now?",
                    "unit": "of the tank"
                },
                {
                    "operation": "subtract",
                    "template": "A juice bottle was {frac1} full. {person} drank {frac2} of the bottle. How much juice is left?",
                    "unit": "of the bottle",
                    "names": ["Sam", "Charlie", "Dakota", "Avery", "Quinn", "Sage"]
                }
            ]
        },
        
        # Garden/Nature scenarios
        {
            "type": "garden",
            "templates": [
                {
                    "operation": "add",
                    "template": "In a flower garden, {frac1} of the flowers are roses and {frac2} are tulips. What fraction of the garden has roses or tulips?",
                    "unit": "of the garden"
                },
                {
                    "operation": "subtract",
                    "template": "A farmer planted vegetables on {frac1} of his field. If {frac2} was destroyed by pests, how much of the planted area survived?",
                    "unit": "of the field"
                }
            ]
        },
        
        # Time scenarios
        {
            "type": "time",
            "templates": [
                {
                    "operation": "add",
                    "template": "{person} spent {frac1} of the day studying and {frac2} playing sports. What fraction of the day was spent on these activities?",
                    "unit": "of the day",
                    "names": ["Jamie", "Blake", "Reese", "Drew", "Skyler", "River"]
                },
                {
                    "operation": "subtract",
                    "template": "During a {denom}-hour shift, a worker spent {frac1} of the time on meetings. If {frac2} was for lunch, how much time was left for actual work?",
                    "unit": "of the shift"
                }
            ]
        }
    ]
    
    # Choose random scenario
    scenario_type = random.choice(scenarios)
    template_data = random.choice(scenario_type["templates"])
    
    # Generate fractions
    denominator = random.choice(denominators)
    
    if template_data["operation"] == "add":
        # For addition, ensure sum doesn't exceed 1
        max_num = denominator - 1
        num1 = random.randint(1, max(1, min(max_num - 1, denominator - 2)))
        num2 = random.randint(1, max(1, min(max_num - num1, denominator - 1)))
    else:
        # For subtraction, ensure we have valid ranges
        # Make sure we have at least 2 possible values for num1
        if denominator <= 3:
            num1 = denominator - 1
            num2 = random.randint(1, max(1, num1 - 1))
        else:
            num1 = random.randint(2, denominator - 1)
            num2 = random.randint(1, num1 - 1)
    
    frac1 = Fraction(num1, denominator)
    frac2 = Fraction(num2, denominator)
    
    # Calculate answer
    if template_data["operation"] == "add":
        answer = frac1 + frac2
    else:
        answer = frac1 - frac2
    
    # Format the problem text
    problem_text = template_data["template"]
    
    # Replace placeholders
    if "{person}" in problem_text or "{person1}" in problem_text:
        if "names" in template_data:
            name1 = random.choice(template_data["names"])
            name2 = random.choice([n for n in template_data["names"] if n != name1])
            problem_text = problem_text.replace("{person1}", name1)
            problem_text = problem_text.replace("{person2}", name2)
            problem_text = problem_text.replace("{person}", name1)
    
    problem_text = problem_text.replace("{frac1}", f"{num1}/{denominator}")
    problem_text = problem_text.replace("{frac2}", f"{num2}/{denominator}")
    problem_text = problem_text.replace("{num1}", str(num1))
    problem_text = problem_text.replace("{denom}", str(denominator))
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "operation": template_data["operation"],
        "frac1": frac1,
        "frac2": frac2,
        "num1": num1,
        "num2": num2,
        "denominator": denominator,
        "answer": answer,
        "unit": template_data["unit"],
        "scenario_type": scenario_type["type"]
    }
    st.session_state.current_problem = problem_text
    st.session_state.correct_answer = answer

def parse_fraction(fraction_str):
    """Parse a fraction string like '3/4' into a Fraction object"""
    # Remove extra spaces
    fraction_str = fraction_str.strip()
    
    # Check if it matches the pattern number/number
    match = re.match(r'^(\d+)\s*/\s*(\d+)$', fraction_str)
    if match:
        numerator = int(match.group(1))
        denominator = int(match.group(2))
        if denominator > 0:
            return Fraction(numerator, denominator)
    
    return None

def display_problem():
    """Display the current problem with visual aids"""
    data = st.session_state.problem_data
    
    # Display the problem
    st.markdown("### 📝 Problem:")
    st.info(st.session_state.current_problem)
    
    # Visual representation - use simple bar model
    display_bar_visual(data)
    
    # Answer input section
    st.markdown("### ✏️ Your Answer:")
    
    # Create the form for answer input
    with st.form("answer_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("Enter your answer as a fraction:")
            fraction_input = st.text_input(
                "Type your fraction (e.g., 3/4)",
                placeholder="numerator/denominator",
                key="user_fraction_input",
                label_visibility="collapsed"
            )
            st.markdown(f"**{data['unit']}**")
        
        with col2:
            st.markdown("")  # Spacer
            st.markdown("")  # Spacer
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            # Parse the fraction input
            parsed_fraction = parse_fraction(fraction_input)
            
            if parsed_fraction is None:
                st.error("❌ Please enter a valid fraction in the form: numerator/denominator (e.g., 3/4)")
            else:
                st.session_state.user_answer = parsed_fraction
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.score["attempted"] += 1
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_bar_visual(data):
    """Display bar visual for all scenarios"""
    denominator = data["denominator"]
    num1 = data["num1"]
    num2 = data["num2"]
    operation = data["operation"]
    
    # Create columns for visual representation
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"**First fraction: {num1}/{denominator}**")
        # Create visual bars using emojis
        filled1 = "🟦" * num1
        empty1 = "⬜" * (denominator - num1)
        st.markdown(f"{filled1}{empty1}")
    
    with col2:
        st.markdown(f"**{'+' if operation == 'add' else '−'}**", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"**Second fraction: {num2}/{denominator}**")
        # Create visual bars using emojis
        filled2 = "🟨" * num2
        empty2 = "⬜" * (denominator - num2)
        st.markdown(f"{filled2}{empty2}")
    
    st.markdown("---")

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
    correct_answer = st.session_state.correct_answer
    data = st.session_state.problem_data
    
    # Simplify answers for comparison
    user_simplified = user_answer
    correct_simplified = correct_answer
    
    if user_simplified == correct_simplified:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.score["correct"] += 1
        
        # Show the complete equation using text instead of LaTeX
        if data["operation"] == "add":
            st.markdown(f"### ✅ {data['num1']}/{data['denominator']} + {data['num2']}/{data['denominator']} = {correct_answer.numerator}/{correct_answer.denominator}")
        else:
            st.markdown(f"### ✅ {data['num1']}/{data['denominator']} − {data['num2']}/{data['denominator']} = {correct_answer.numerator}/{correct_answer.denominator}")
        
        # Increase difficulty if doing well
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate >= 0.8 and st.session_state.fractions_difficulty < 4:
                st.session_state.fractions_difficulty += 1
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.fractions_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
        
        # Show step-by-step solution
        show_solution()
        
        # Decrease difficulty if struggling
        if st.session_state.score["attempted"] >= 3:
            success_rate = st.session_state.score["correct"] / st.session_state.score["attempted"]
            if success_rate < 0.5 and st.session_state.fractions_difficulty > 1:
                st.session_state.fractions_difficulty -= 1
                st.warning(f"⬇️ **Let's practice more at Level {st.session_state.fractions_difficulty}**")

def show_solution():
    """Show step-by-step solution"""
    data = st.session_state.problem_data
    
    with st.expander("📖 **See Step-by-Step Solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **1. Identify the fractions:**
        - First fraction: {data['num1']}/{data['denominator']}
        - Second fraction: {data['num2']}/{data['denominator']}
        
        **2. Check the denominators:**
        - Both fractions have the same denominator: {data['denominator']}
        - ✅ We can add/subtract directly!
        
        **3. {("Add" if data["operation"] == "add" else "Subtract")} the numerators:**
        - {data['num1']} {("+" if data["operation"] == "add" else "−")} {data['num2']} = {data['answer'].numerator}
        
        **4. Keep the same denominator:**
        - Answer: {data['answer'].numerator}/{data['answer'].denominator}
        
        **5. Simplify if possible:**
        - {f"Already in simplest form!" if data['answer'] == data['answer'] else f"Simplified: {data['answer']}"}
        """)
        
        # Show visual representation using emojis
        st.markdown("### Visual representation:")
        if data["operation"] == "add":
            st.markdown(f"""
            First: {"🟦" * data['num1']}{"⬜" * (data['denominator'] - data['num1'])} = {data['num1']}/{data['denominator']}
            
            Second: {"🟨" * data['num2']}{"⬜" * (data['denominator'] - data['num2'])} = {data['num2']}/{data['denominator']}
            
            Total: {"🟩" * data['answer'].numerator}{"⬜" * (data['denominator'] - data['answer'].numerator)} = {data['answer'].numerator}/{data['denominator']}
            """)
        else:
            st.markdown(f"""
            Start with: {"🟦" * data['num1']}{"⬜" * (data['denominator'] - data['num1'])} = {data['num1']}/{data['denominator']}
            
            Take away: {"🟨" * data['num2']}{"⬜" * (data['denominator'] - data['num2'])} = {data['num2']}/{data['denominator']}
            
            Left with: {"🟩" * data['answer'].numerator}{"⬜" * (data['denominator'] - data['answer'].numerator)} = {data['answer'].numerator}/{data['denominator']}
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