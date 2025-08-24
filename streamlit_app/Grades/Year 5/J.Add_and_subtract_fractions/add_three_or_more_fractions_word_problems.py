import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Add three or more fractions word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J.Add_and_subtract_fractions/add_three_or_more_fractions_word_problems.py
    """
    # Initialize session state
    if "word_problems_score" not in st.session_state:
        st.session_state.word_problems_score = 0
        st.session_state.word_problems_attempts = 0
    
    if "current_word_problem" not in st.session_state:
        st.session_state.current_word_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("📝 Add Three or More Fractions: Word Problems")
    st.markdown("*Solve real-world problems by adding fractions*")
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Score:** {st.session_state.word_problems_score}/{st.session_state.word_problems_attempts}")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_word_problem is None:
        generate_new_word_problem()
    
    # Display current problem
    display_word_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### Steps to Solve:
        1. **Read carefully** - Identify what fractions to add
        2. **Write the equation** - List all fractions with + signs
        3. **Find the LCD** - Find common denominator
        4. **Convert fractions** - Make all denominators the same
        5. **Add numerators** - Keep the denominator
        6. **Simplify** - Reduce to lowest terms
        7. **Check** - Does your answer make sense?
        
        ### Example:
        "Tom ate 1/2 of a pizza, 1/4 of another, and 1/8 of a third."
        - Equation: 1/2 + 1/4 + 1/8
        - LCD = 8
        - 4/8 + 2/8 + 1/8 = 7/8
        - Tom ate 7/8 of a pizza in total
        """)

def generate_new_word_problem():
    """Generate a new word problem involving adding fractions"""
    
    word_problems = [
        # Weather/Nature problems
        {
            "context": "Eva recorded the snowfall every day during a snowstorm. She recorded {f1} of a centimetre on Wednesday, {f2} of a centimetre on Thursday, and {f3} of a centimetre on Friday. How many total centimetres of snow did Eva record?",
            "fractions": [Fraction(1, 2), Fraction(1, 5), Fraction(1, 10)],
            "unit": "centimetres",
            "subject": "Eva"
        },
        {
            "context": "During a rainy week, Maria measured {f1} of an inch on Monday, {f2} of an inch on Tuesday, and {f3} of an inch on Wednesday. What was the total rainfall?",
            "fractions": [Fraction(3, 4), Fraction(1, 2), Fraction(1, 8)],
            "unit": "inches",
            "subject": "the week"
        },
        {
            "context": "A plant grew {f1} of a foot in March, {f2} of a foot in April, and {f3} of a foot in May. How much did the plant grow in total?",
            "fractions": [Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)],
            "unit": "feet",
            "subject": "the plant"
        },
        
        # Food/Restaurant problems
        {
            "context": "The staff at Naomi's Restaurant tracked how much ketchup was used from day to day. Customers consumed {f1} of a bottle on Sunday, {f2} of a bottle on Monday, and {f3} of a bottle on Tuesday. In total, how many bottles of ketchup did the customers consume?",
            "fractions": [Fraction(1, 8), Fraction(1, 8), Fraction(1, 2)],
            "unit": "bottles",
            "subject": "the customers"
        },
        {
            "context": "At a bakery, {f1} of the flour was used for bread, {f2} was used for cakes, and {f3} was used for cookies. What fraction of the flour was used in total?",
            "fractions": [Fraction(2, 5), Fraction(1, 4), Fraction(1, 10)],
            "unit": "of the flour",
            "subject": "the bakery"
        },
        {
            "context": "During lunch, students drank {f1} of the orange juice, {f2} of the apple juice, and {f3} of the grape juice from the cafeteria's supply. How much juice was consumed in total?",
            "fractions": [Fraction(1, 3), Fraction(1, 4), Fraction(1, 6)],
            "unit": "of the juice supply",
            "subject": "the students"
        },
        
        # Shopping/Items problems
        {
            "context": "Desmond visited a toy shop with his younger brother. Near the register, there were jars filled with tiny items. They saw {f1} of a jar of toy soldiers, {f2} of a jar of rings, and {f3} of a jar of key chains. Altogether, how many jars would these items fill?",
            "fractions": [Fraction(1, 4), Fraction(1, 8), Fraction(1, 2)],
            "unit": "jars",
            "subject": "these items"
        },
        {
            "context": "At a craft store, Emma bought {f1} of a yard of blue ribbon, {f2} of a yard of red ribbon, and {f3} of a yard of yellow ribbon. How many yards of ribbon did she buy in total?",
            "fractions": [Fraction(3, 8), Fraction(1, 4), Fraction(1, 2)],
            "unit": "yards",
            "subject": "Emma"
        },
        {
            "context": "A carpenter used {f1} of his wood for a table, {f2} for a chair, and {f3} for shelves. What fraction of his wood did he use?",
            "fractions": [Fraction(1, 3), Fraction(1, 6), Fraction(1, 4)],
            "unit": "of his wood",
            "subject": "the carpenter"
        },
        
        # Time/Activity problems
        {
            "context": "Sarah spent {f1} of an hour on math homework, {f2} of an hour on science, and {f3} of an hour on reading. How many hours did she spend on homework?",
            "fractions": [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)],
            "unit": "hours",
            "subject": "Sarah"
        },
        {
            "context": "During practice, the team spent {f1} of the time on drills, {f2} on scrimmage, and {f3} on fitness. What fraction of practice time was used?",
            "fractions": [Fraction(2, 5), Fraction(1, 3), Fraction(1, 15)],
            "unit": "of the time",
            "subject": "the team"
        },
        {
            "context": "A video game player completed {f1} of a level on the first try, {f2} on the second try, and {f3} on the third try. How much of the level was completed?",
            "fractions": [Fraction(1, 4), Fraction(3, 8), Fraction(1, 8)],
            "unit": "of the level",
            "subject": "the player"
        },
        
        # Distance/Travel problems
        {
            "context": "A hiker walked {f1} of a mile before breakfast, {f2} of a mile after breakfast, and {f3} of a mile in the evening. What was the total distance walked?",
            "fractions": [Fraction(3, 4), Fraction(1, 2), Fraction(1, 4)],
            "unit": "miles",
            "subject": "the hiker"
        },
        {
            "context": "A delivery truck traveled {f1} of its route in the morning, {f2} at noon, and {f3} in the afternoon. What fraction of the route was completed?",
            "fractions": [Fraction(1, 3), Fraction(1, 4), Fraction(1, 6)],
            "unit": "of the route",
            "subject": "the truck"
        },
        
        # Container/Volume problems
        {
            "context": "A fish tank was filled {f1} full on Monday, then {f2} more on Tuesday, and {f3} more on Wednesday. What fraction of the tank is now filled?",
            "fractions": [Fraction(1, 4), Fraction(1, 3), Fraction(1, 12)],
            "unit": "of the tank",
            "subject": "the tank"
        },
        {
            "context": "Three friends shared a water cooler. Jake drank {f1} of the water, Maria drank {f2}, and Tom drank {f3}. How much water was consumed?",
            "fractions": [Fraction(1, 5), Fraction(2, 15), Fraction(1, 3)],
            "unit": "of the water",
            "subject": "the friends"
        },
        
        # Four fraction problems (harder)
        {
            "context": "During a week-long art project, students used {f1} of the paint on Monday, {f2} on Tuesday, {f3} on Wednesday, and {f4} on Thursday. How much paint was used?",
            "fractions": [Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(1, 12)],
            "unit": "of the paint",
            "subject": "the students"
        },
        {
            "context": "A garden has four sections. Roses take up {f1} of the space, tulips {f2}, daisies {f3}, and sunflowers {f4}. What fraction of the garden is planted?",
            "fractions": [Fraction(1, 4), Fraction(1, 6), Fraction(1, 8), Fraction(1, 3)],
            "unit": "of the garden",
            "subject": "the garden"
        }
    ]
    
    # Select random problem
    problem = random.choice(word_problems)
    
    # Format the context with fractions
    fractions = problem["fractions"]
    context = problem["context"]
    
    # Replace placeholders with fraction strings
    for i, frac in enumerate(fractions):
        placeholder = f"{{f{i+1}}}"
        if placeholder in context:
            context = context.replace(placeholder, str(frac))
    
    # Handle optional fourth fraction
    if "{f4}" in context and len(fractions) < 4:
        context = context.replace("{f4}", "")
    
    # Calculate answer
    answer = sum(fractions)
    
    st.session_state.current_word_problem = {
        "context": context,
        "fractions": fractions,
        "unit": problem["unit"],
        "answer": answer
    }
    st.session_state.correct_answer = answer
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_word_problem():
    """Display the current word problem"""
    problem = st.session_state.current_word_problem
    
    # Display problem in a nice box
    st.markdown(f"""
    <div style="
        background-color: #f5f5f5; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #2196F3;
        font-size: 16px;
        line-height: 1.6;
        margin: 20px 0;
    ">
        {problem['context']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input
    with st.form("word_problem_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            # Check if unit is a fraction (starts with "of")
            if problem['unit'].startswith("of"):
                answer_input = st.text_input(
                    f"Enter your answer as a fraction:",
                    placeholder="Example: 3/4",
                    key="fraction_input"
                )
            else:
                answer_input = st.text_input(
                    f"Enter your answer in {problem['unit']}:",
                    placeholder="Example: 3/4",
                    key="answer_input"
                )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit and answer_input:
            try:
                # Parse fraction input (handle mixed numbers too)
                if ' ' in answer_input:  # Mixed number
                    parts = answer_input.split()
                    whole = int(parts[0])
                    frac_parts = parts[1].split('/')
                    num = int(frac_parts[0])
                    denom = int(frac_parts[1])
                    user_answer = Fraction(whole * denom + num, denom)
                else:  # Regular fraction
                    frac_parts = answer_input.split('/')
                    if len(frac_parts) == 2:
                        user_answer = Fraction(int(frac_parts[0]), int(frac_parts[1]))
                    else:
                        user_answer = Fraction(int(answer_input))
                
                st.session_state.user_answer = user_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.word_problems_attempts += 1
                
            except:
                st.error("Please enter a valid fraction (e.g., 3/4 or 1 1/2)")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    problem = st.session_state.current_word_problem
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Excellent work!**")
        st.session_state.word_problems_score += 1
        
        # Show the complete answer with unit
        if problem['unit'].startswith("of"):
            st.info(f"✅ The answer is **{correct_answer} {problem['unit']}**")
        else:
            st.info(f"✅ The answer is **{correct_answer} {problem['unit']}**")
    else:
        st.error(f"❌ **Not quite right.**")
        
        # Show correct answer with unit
        if problem['unit'].startswith("of"):
            st.error(f"The correct answer is **{correct_answer} {problem['unit']}**")
        else:
            st.error(f"The correct answer is **{correct_answer} {problem['unit']}**")
        
        # Show solution
        show_word_problem_solution()

def show_word_problem_solution():
    """Show step-by-step solution for word problem"""
    problem = st.session_state.current_word_problem
    fractions = problem['fractions']
    
    with st.expander("📖 **See Complete Solution**", expanded=True):
        # Step 1: Identify what to add
        st.markdown("### Step 1: Identify the fractions to add")
        fraction_str = " + ".join([str(f) for f in fractions])
        st.markdown(f"We need to add: **{fraction_str}**")
        
        # Step 2: Find LCD
        denominators = [f.denominator for f in fractions]
        lcd = find_lcd(denominators)
        st.markdown("### Step 2: Find the LCD")
        st.markdown(f"Denominators: {', '.join(map(str, denominators))}")
        st.markdown(f"**LCD = {lcd}**")
        
        # Step 3: Convert fractions
        st.markdown("### Step 3: Convert to common denominator")
        converted_nums = []
        for frac in fractions:
            multiplier = lcd // frac.denominator
            new_num = frac.numerator * multiplier
            converted_nums.append(new_num)
            if multiplier > 1:
                st.markdown(f"- {frac} = {frac.numerator} × {multiplier}/{frac.denominator} × {multiplier} = **{new_num}/{lcd}**")
            else:
                st.markdown(f"- {frac} = **{new_num}/{lcd}** (already has LCD)")
        
        # Step 4: Add
        st.markdown("### Step 4: Add the numerators")
        sum_str = " + ".join([f"{n}/{lcd}" for n in converted_nums])
        total = sum(converted_nums)
        st.markdown(f"{sum_str} = **{total}/{lcd}**")
        
        # Step 5: Simplify
        result = Fraction(total, lcd)
        if result.denominator != lcd:
            st.markdown("### Step 5: Simplify")
            st.markdown(f"{total}/{lcd} = **{result}**")
        
        # Final answer
        st.markdown("### Final Answer:")
        if problem['unit'].startswith("of"):
            st.markdown(f"**{result} {problem['unit']}**")
        else:
            st.markdown(f"**{result} {problem['unit']}**")

def find_lcd(denominators):
    """Find the LCD of a list of denominators"""
    from math import gcd
    lcd = denominators[0]
    for d in denominators[1:]:
        lcd = lcd * d // gcd(lcd, d)
    return lcd

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_word_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer