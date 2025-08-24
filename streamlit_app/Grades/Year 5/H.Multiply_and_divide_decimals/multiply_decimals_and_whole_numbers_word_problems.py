import streamlit as st
import random

def run():
    """
    Main function to run the Multiply decimals and whole numbers: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/H. Multiply and divide decimals/multiply_decimals_and_whole_numbers_word_problems.py
    """
    # Initialize session state
    if "word_problem" not in st.session_state:
        st.session_state.word_problem = None
        st.session_state.word_problem_answer_submitted = False
        st.session_state.user_word_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > H. Multiply and divide decimals**")
    st.title("📖 Multiply Decimals and Whole Numbers: Word Problems")
    st.markdown("*Solve real-world problems by multiplying decimals and whole numbers*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.word_problem is None:
        st.session_state.word_problem = generate_word_problem()
        st.session_state.word_problem_answer_submitted = False
        st.session_state.user_word_answer = ""
    
    problem = st.session_state.word_problem
    
    # Display the word problem
    st.markdown("### 📝 Problem:")
    st.markdown(f"""
    <div style="
        background-color: #f0f7ff;
        border-left: 4px solid #2196F3;
        padding: 20px;
        margin: 20px 0;
        font-size: 18px;
        line-height: 1.6;
    ">
        {problem['question']}
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            f"Answer ({problem['unit']}):",
            value=st.session_state.user_word_answer,
            key="word_answer_input",
            disabled=st.session_state.word_problem_answer_submitted,
            placeholder=f"Enter {problem['unit']}"
        )
        st.session_state.user_word_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.word_problem_answer_submitted):
            
            if st.session_state.user_word_answer.strip() == "":
                st.warning("⚠️ Please enter your answer.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_word_answer)
                    st.session_state.word_problem_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid number.")
    
    # Show feedback if answer was submitted
    if st.session_state.word_problem_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.word_problem_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.word_problem = None
                st.session_state.word_problem_answer_submitted = False
                st.session_state.user_word_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Problem-Solving Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Word Problems:
        
        **Step 1: Identify what you know**
        - Find the rate (decimal number per unit)
        - Find how many units
        
        **Step 2: Identify what you need to find**
        - Read the question carefully
        - Note the units for your answer
        
        **Step 3: Set up the multiplication**
        - Rate × Number of units = Total
        
        **Step 4: Calculate**
        - Multiply the decimal by the whole number
        - Remember decimal placement rules
        
        ### Example Problems:
        
        **Example 1:** A machine fills 2.5 litres per minute. How much in 6 minutes?
        - Rate: 2.5 litres per minute
        - Time: 6 minutes
        - Calculation: 2.5 × 6 = 15 litres
        
        **Example 2:** Each book weighs 0.8 kg. What's the weight of 9 books?
        - Rate: 0.8 kg per book
        - Count: 9 books
        - Calculation: 0.8 × 9 = 7.2 kg
        
        ### Tips:
        - **Look for keywords:** "each," "per," "every" indicate a rate
        - **Check units:** Make sure your answer has the right unit
        - **Estimate first:** Round to check if your answer is reasonable
        - **Draw a picture:** Visual representations can help
        """)

def generate_word_problem():
    """Generate a random word problem involving decimal × whole number multiplication"""
    
    scenarios = [
        # Food and drinks
        {
            'template': "{person} serves {decimal} litres of {drink} at the {place} each hour. How many litres of {drink} will {person} serve in {whole} hours?",
            'variables': {
                'person': ['Hassan', 'Maria', 'James', 'Sophie', 'Ahmed', 'Emma'],
                'decimal': [2.5, 3.1, 4.2, 1.8, 2.7, 3.5],
                'drink': ['soda', 'juice', 'lemonade', 'iced tea', 'water', 'smoothie'],
                'place': ['drive-thru', 'restaurant', 'café', 'food truck', 'canteen'],
                'whole': [5, 6, 7, 8, 9]
            },
            'unit': 'litres',
            'operation': 'multiply'
        },
        {
            'template': "A bakery uses {decimal} kg of flour for each batch of {item}. How much flour is needed for {whole} batches?",
            'variables': {
                'decimal': [1.5, 2.3, 3.2, 0.8, 1.7],
                'item': ['bread', 'cookies', 'muffins', 'cakes', 'pastries'],
                'whole': [4, 5, 6, 7, 8]
            },
            'unit': 'kg',
            'operation': 'multiply'
        },
        
        # Manufacturing and production
        {
            'template': "A factory makes {decimal} metres of {material} every minute. How many metres of {material} can the factory make in {whole} minutes?",
            'variables': {
                'decimal': [2.9, 4.5, 3.7, 5.2, 1.8],
                'material': ['masking tape', 'fabric', 'wire', 'ribbon', 'rope'],
                'whole': [6, 7, 8, 9, 12]
            },
            'unit': 'metres',
            'operation': 'multiply'
        },
        {
            'template': "A machine produces {decimal} {items} per second. How many {items} will it produce in {whole} seconds?",
            'variables': {
                'decimal': [1.5, 2.2, 3.4, 0.8, 1.2],
                'items': ['bottles', 'cans', 'boxes', 'packets', 'containers'],
                'whole': [5, 8, 10, 12, 15]
            },
            'unit': 'items',
            'operation': 'multiply'
        },
        
        # Distance and travel
        {
            'template': "{person} walks {decimal} km every morning. How far will {pronoun} walk in {whole} days?",
            'variables': {
                'person': ['Sarah', 'Tom', 'Lisa', 'David', 'Amy', 'Chris'],
                'pronoun': ['she', 'he', 'she', 'he', 'she', 'he'],
                'decimal': [2.5, 3.2, 4.1, 1.8, 2.7],
                'whole': [5, 6, 7, 10, 14]
            },
            'unit': 'km',
            'operation': 'multiply'
        },
        {
            'template': "A {vehicle} travels {decimal} km per litre of fuel. How far can it travel with {whole} litres?",
            'variables': {
                'vehicle': ['car', 'bus', 'truck', 'motorcycle', 'van'],
                'decimal': [12.5, 8.7, 15.3, 22.4, 10.8],
                'whole': [4, 5, 6, 8, 10]
            },
            'unit': 'km',
            'operation': 'multiply'
        },
        
        # Money and shopping
        {
            'template': "Each {item} costs £{decimal}. How much will {whole} {item}s cost?",
            'variables': {
                'item': ['pen', 'notebook', 'eraser', 'pencil', 'ruler'],
                'decimal': [1.25, 2.50, 0.75, 0.60, 1.80],
                'whole': [4, 5, 6, 8, 12]
            },
            'unit': '£',
            'operation': 'multiply'
        },
        {
            'template': "{person} earns £{decimal} per hour. How much will {pronoun} earn in {whole} hours?",
            'variables': {
                'person': ['Alice', 'Bob', 'Clara', 'Daniel', 'Eva'],
                'pronoun': ['she', 'he', 'she', 'he', 'she'],
                'decimal': [8.50, 9.25, 10.75, 12.50, 15.80],
                'whole': [6, 7, 8, 10, 12]
            },
            'unit': '£',
            'operation': 'multiply'
        },
        
        # Science and measurements
        {
            'template': "A plant grows {decimal} cm each week. How tall will it grow in {whole} weeks?",
            'variables': {
                'decimal': [1.5, 2.3, 3.2, 0.8, 1.7],
                'whole': [4, 6, 8, 10, 12]
            },
            'unit': 'cm',
            'operation': 'multiply'
        },
        {
            'template': "Each {container} holds {decimal} litres of {liquid}. How much {liquid} is in {whole} {container}s?",
            'variables': {
                'container': ['beaker', 'flask', 'bottle', 'jug', 'tank'],
                'decimal': [0.5, 0.75, 1.25, 2.5, 3.5],
                'liquid': ['water', 'oil', 'solution', 'chemical', 'mixture'],
                'whole': [4, 5, 6, 8, 10]
            },
            'unit': 'litres',
            'operation': 'multiply'
        },
        
        # Sports and activities
        {
            'template': "{person} swims {decimal} laps in one session. How many laps will {pronoun} swim in {whole} sessions?",
            'variables': {
                'person': ['Michael', 'Jessica', 'Ryan', 'Emily', 'Jake'],
                'pronoun': ['he', 'she', 'he', 'she', 'he'],
                'decimal': [2.5, 3.5, 4.5, 5.5, 6.5],
                'whole': [4, 5, 6, 7, 8]
            },
            'unit': 'laps',
            'operation': 'multiply'
        },
        {
            'template': "A {sport} player scores an average of {decimal} points per game. How many points in {whole} games?",
            'variables': {
                'sport': ['basketball', 'volleyball', 'cricket', 'hockey', 'football'],
                'decimal': [12.5, 15.8, 8.4, 10.2, 18.6],
                'whole': [4, 5, 6, 8, 10]
            },
            'unit': 'points',
            'operation': 'multiply'
        },
        
        # Time-based problems
        {
            'template': "A {device} uses {decimal} units of electricity per hour. How many units will it use in {whole} hours?",
            'variables': {
                'device': ['heater', 'air conditioner', 'computer', 'television', 'refrigerator'],
                'decimal': [1.2, 2.5, 0.8, 0.5, 1.5],
                'whole': [5, 8, 10, 12, 24]
            },
            'unit': 'units',
            'operation': 'multiply'
        },
        {
            'template': "A {worker} can {action} {decimal} {items} per hour. How many {items} can they {action} in {whole} hours?",
            'variables': {
                'worker': ['painter', 'carpenter', 'cleaner', 'mechanic', 'gardener'],
                'action': ['paint', 'build', 'clean', 'repair', 'plant'],
                'decimal': [2.5, 1.5, 3.2, 0.8, 4.5],
                'items': ['rooms', 'chairs', 'windows', 'engines', 'trees'],
                'whole': [4, 6, 8, 10, 12]
            },
            'unit': 'items',
            'operation': 'multiply'
        }
    ]
    
    # Choose a random scenario
    scenario = random.choice(scenarios)
    
    # Build the problem
    question_vars = {}
    for var, options in scenario['variables'].items():
        if var == 'pronoun':
            # Match pronoun to person
            person_index = scenario['variables']['person'].index(question_vars['person'])
            question_vars[var] = options[person_index]
        else:
            question_vars[var] = random.choice(options)
    
    # Generate question
    question = scenario['template'].format(**question_vars)
    
    # Calculate answer
    decimal_value = question_vars['decimal']
    whole_value = question_vars['whole']
    answer = round(decimal_value * whole_value, 2)
    
    # Remove trailing zeros
    if answer == int(answer):
        answer = int(answer)
    
    return {
        'question': question,
        'decimal': decimal_value,
        'whole': whole_value,
        'answer': answer,
        'unit': scenario['unit'],
        'operation': scenario['operation']
    }

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.word_problem
    
    try:
        user_answer = float(st.session_state.user_word_answer)
        
        # Check if answer is correct
        if abs(user_answer - problem['answer']) < 0.01:
            st.success("🎉 **Correct! Excellent problem-solving!**")
            
            # Show the solution
            with st.expander("✅ **See the solution**", expanded=True):
                st.markdown("### Solution Steps:")
                
                st.markdown(f"**Given information:**")
                st.markdown(f"- Rate: {problem['decimal']} {problem['unit']} per unit")
                st.markdown(f"- Count/Time: {problem['whole']} units")
                
                st.markdown(f"\n**Calculation:**")
                st.markdown(f"{problem['decimal']} × {problem['whole']} = **{problem['answer']} {problem['unit']}**")
                
                # Show work
                st.markdown(f"\n**Work shown:**")
                st.markdown(f"""
                ```
                    {problem['decimal']}
                  ×  {problem['whole']}
                  ------
                    {problem['answer']}
                ```
                """)
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{problem['answer']} {problem['unit']}**")
            
            # Show detailed explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown("### Let's solve this step by step:")
                
                st.markdown(f"**What we know:**")
                st.markdown(f"- Rate: {problem['decimal']} {problem['unit']} per unit")
                st.markdown(f"- Total units: {problem['whole']}")
                
                st.markdown(f"\n**What we need to find:** Total {problem['unit']}")
                
                st.markdown(f"\n**Set up the multiplication:**")
                st.markdown(f"{problem['decimal']} × {problem['whole']} = ?")
                
                st.markdown(f"\n**Calculate:**")
                # Show decimal multiplication process
                decimal_str = str(problem['decimal'])
                if '.' in decimal_str:
                    decimal_places = len(decimal_str.split('.')[-1])
                    no_decimal = int(decimal_str.replace('.', ''))
                    
                    st.markdown(f"1. Multiply without decimal: {no_decimal} × {problem['whole']} = {no_decimal * problem['whole']}")
                    st.markdown(f"2. Count decimal places: {problem['decimal']} has {decimal_places} decimal place{'s' if decimal_places > 1 else ''}")
                    st.markdown(f"3. Place decimal: {no_decimal * problem['whole']} → {problem['answer']}")
                
                st.markdown(f"\n**Answer:** {problem['answer']} {problem['unit']}")
                st.markdown(f"**Your answer:** {user_answer} {problem['unit']}")
                
                # Common mistakes
                if abs(user_answer - (problem['decimal'] + problem['whole'])) < 0.01:
                    st.warning("💡 You added instead of multiplying. Remember: rate × quantity = total")
                
    except ValueError:
        st.error("❌ Invalid number format. Please enter a valid number.")