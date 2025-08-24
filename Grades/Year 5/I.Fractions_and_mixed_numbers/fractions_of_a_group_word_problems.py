import streamlit as st
import random

def run():
    """
    Main function to run the Fractions of a group: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/fractions_of_a_group_word_problems.py
    """
    # Initialize session state
    if "fraction_group_problem" not in st.session_state:
        st.session_state.fraction_group_problem = None
        st.session_state.fraction_group_submitted = False
        st.session_state.user_fraction_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("👥 Fractions of a Group: Word Problems")
    st.markdown("*Read the word problem and write the fraction*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.fraction_group_problem is None:
        st.session_state.fraction_group_problem = generate_group_problem()
        st.session_state.fraction_group_submitted = False
        st.session_state.user_fraction_answer = ""
    
    problem = st.session_state.fraction_group_problem
    
    # Display the word problem
    st.markdown("### 📝 Problem:")
    st.info(problem['story'])
    
    # Input section
    st.markdown("**Use a forward slash ( / ) to separate the numerator and denominator.**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_input(
            "Your answer:",
            value=st.session_state.user_fraction_answer,
            key="fraction_group_input",
            disabled=st.session_state.fraction_group_submitted,
            placeholder="e.g., 3/4",
            label_visibility="collapsed"
        )
        st.session_state.user_fraction_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.fraction_group_submitted):
            
            if st.session_state.user_fraction_answer.strip() == "":
                st.warning("⚠️ Please enter your answer as a fraction (e.g., 3/4).")
            else:
                st.session_state.fraction_group_submitted = True
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.fraction_group_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.fraction_group_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.fraction_group_problem = None
                st.session_state.fraction_group_submitted = False
                st.session_state.user_fraction_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Read carefully:** Find the important numbers in the problem
        2. **Identify:**
           - The total number of items
           - The specific items mentioned
        3. **Write the fraction:**
           - Numerator (top) = specific items
           - Denominator (bottom) = total items
        
        ### Examples:
        - "5 apples total, 2 are red" → **2/5**
        - "8 marbles, 3 rolled away" → **3/8**
        - "12 cookies, ate 5" → **5/12**
        
        ### Remember:
        - Count ALL items for the denominator
        - Count only the SPECIFIC items for the numerator
        - Always use / to separate the numbers
        """)

def generate_group_problem():
    """Generate a random word problem about fractions of groups"""
    scenarios = [
        # Animals
        {
            'template': "{character} went to the {place}. They saw {total} {animals}. {specific_num} of the {animals} were {attribute}. What fraction of the {animals} were {attribute}?",
            'variables': {
                'character': ['Emma', 'Jack', 'Lily', 'Noah', 'Sophia', 'Oliver', 'Ava', 'Ethan'],
                'place': ['zoo', 'park', 'farm', 'pet store', 'animal shelter', 'aquarium'],
                'total': [6, 8, 10, 12, 9, 7],
                'animals': ['cats', 'dogs', 'birds', 'rabbits', 'fish', 'turtles', 'hamsters'],
                'specific_num': None,  # Will be calculated
                'attribute': ['sleeping', 'eating', 'playing', 'brown', 'small', 'young']
            }
        },
        # Food items
        {
            'template': "{character} {action} {total} {food}. {specific_num} of them {attribute}. What fraction of the {food} {attribute_past}?",
            'variables': {
                'character': ['Maya', 'Lucas', 'Isabella', 'Mason', 'Charlotte', 'Aiden'],
                'action': ['bought', 'made', 'found', 'received', 'prepared', 'picked'],
                'total': [8, 12, 10, 15, 6, 9],
                'food': ['cookies', 'apples', 'sandwiches', 'muffins', 'oranges', 'cupcakes'],
                'specific_num': None,
                'attribute': ['had chocolate chips', 'were red', 'had cheese', 'had sprinkles', 'were ripe', 'had frosting'],
                'attribute_past': ['had chocolate chips', 'were red', 'had cheese', 'had sprinkles', 'were ripe', 'had frosting']
            }
        },
        # School supplies
        {
            'template': "{character} has {total} {items} in their {container}. {specific_num} of them are {attribute}. What fraction of the {items} are {attribute}?",
            'variables': {
                'character': ['Alex', 'Riley', 'Jordan', 'Taylor', 'Casey', 'Morgan'],
                'total': [10, 12, 8, 15, 20, 6],
                'items': ['pencils', 'markers', 'crayons', 'erasers', 'stickers', 'books'],
                'container': ['pencil case', 'backpack', 'desk', 'drawer', 'box', 'bag'],
                'specific_num': None,
                'attribute': ['blue', 'new', 'broken', 'missing', 'colorful', 'small']
            }
        },
        # Sports/Games
        {
            'template': "In a {game}, {character} {action} {total} times. They {result} {specific_num} times. What fraction of the {attempts} were {successful}?",
            'variables': {
                'character': ['Sam', 'Kim', 'Pat', 'Chris', 'Jamie', 'Drew'],
                'game': ['basketball game', 'soccer match', 'tennis match', 'bowling game', 'dart game'],
                'action': ['shot', 'kicked', 'served', 'rolled', 'threw'],
                'total': [10, 12, 8, 6, 15],
                'specific_num': None,
                'result': ['scored', 'scored', 'aced', 'got strikes', 'hit the target'],
                'attempts': ['shots', 'kicks', 'serves', 'rolls', 'throws'],
                'successful': ['successful', 'goals', 'aces', 'strikes', 'hits']
            }
        },
        # Nature/Garden
        {
            'template': "{character} planted {total} {plants} in their garden. {specific_num} of them {result}. What fraction of the {plants} {result}?",
            'variables': {
                'character': ['Grace', 'Henry', 'Violet', 'Leo', 'Hazel', 'Felix'],
                'total': [12, 10, 8, 15, 9, 6],
                'plants': ['flowers', 'seeds', 'tomato plants', 'herbs', 'tulip bulbs', 'trees'],
                'specific_num': None,
                'result': ['bloomed', 'grew', 'produced fruit', 'survived', 'sprouted', 'grew tall']
            }
        },
        # Collections
        {
            'template': "{character} has a collection of {total} {items}. {specific_num} of them are {attribute}. What fraction of the {items} are {attribute}?",
            'variables': {
                'character': ['Ruby', 'Max', 'Luna', 'Oscar', 'Stella', 'Jasper'],
                'total': [20, 15, 12, 18, 10, 8],
                'items': ['stamps', 'coins', 'marbles', 'shells', 'cards', 'buttons'],
                'specific_num': None,
                'attribute': ['from other countries', 'silver', 'blue', 'spiral shaped', 'rare', 'plastic']
            }
        },
        # Classroom scenarios
        {
            'template': "In {character}'s class, there are {total} students. {specific_num} of them {action}. What fraction of the students {action}?",
            'variables': {
                'character': ['Mrs. Smith', 'Mr. Johnson', 'Ms. Davis', 'Mr. Wilson'],
                'total': [24, 20, 25, 18, 30],
                'specific_num': None,
                'action': ['wear glasses', 'have brown hair', 'brought lunch', 'ride the bus', 'play an instrument']
            }
        },
        # Simple quantity problems
        {
            'template': "{character} {action} {total} {items}. {specific_num} {result}. What fraction of the {items} {result_question}?",
            'variables': {
                'character': ['Ben', 'Amy', 'Tom', 'Sara', 'Mike', 'Kate'],
                'action': ['counted', 'found', 'collected', 'bought', 'made'],
                'total': [5, 6, 8, 10, 12, 4],
                'items': ['balloons', 'rocks', 'leaves', 'beads', 'paper airplanes', 'blocks'],
                'specific_num': None,
                'result': ['popped', 'were smooth', 'were yellow', 'were wooden', 'flew well', 'were red'],
                'result_question': ['popped', 'were smooth', 'were yellow', 'were wooden', 'flew well', 'were red']
            }
        }
    ]
    
    # Select a random scenario
    scenario_template = random.choice(scenarios)
    
    # Build the problem
    variables = {}
    for key, options in scenario_template['variables'].items():
        if key == 'specific_num':
            # Calculate specific_num based on total
            total = variables['total']
            # Make sure specific_num is less than total and greater than 0
            specific_num = random.randint(1, total - 1)
            variables[key] = specific_num
        elif isinstance(options, list):
            variables[key] = random.choice(options)
        else:
            variables[key] = options
    
    # Generate the story
    story = scenario_template['template'].format(**variables)
    
    # Calculate the answer
    numerator = variables['specific_num']
    denominator = variables['total']
    
    return {
        'story': story,
        'numerator': numerator,
        'denominator': denominator,
        'answer': f"{numerator}/{denominator}"
    }

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.fraction_group_problem
    user_answer = st.session_state.user_fraction_answer.strip()
    
    # Parse user answer
    try:
        if '/' not in user_answer:
            st.error("❌ Please enter your answer as a fraction using / (e.g., 3/4)")
            return
        
        parts = user_answer.split('/')
        if len(parts) != 2:
            st.error("❌ Please use exactly one / to separate numerator and denominator")
            return
        
        user_num = int(parts[0].strip())
        user_den = int(parts[1].strip())
        
        # Check if fraction is valid
        if user_den == 0:
            st.error("❌ The denominator cannot be zero")
            return
        
        # Check if answer is correct
        correct_num = problem['numerator']
        correct_den = problem['denominator']
        
        # Check for exact match or equivalent fraction
        is_exact_match = (user_num == correct_num and user_den == correct_den)
        is_equivalent = (user_num * correct_den == correct_num * user_den)
        
        if is_exact_match:
            st.success(f"🎉 **Excellent! {user_answer} is correct!**")
            st.balloons()
            
        elif is_equivalent:
            st.success(f"🎉 **Correct! {user_answer} is equivalent to {problem['answer']}**")
            st.info(f"Both fractions equal {user_num/user_den:.3f}")
            
        else:
            st.error(f"❌ **Not quite right. The correct answer is {problem['answer']}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(f"""
                **Let's break down the problem:**
                
                {problem['story']}
                
                **Finding the fraction:**
                - Total items (denominator): **{correct_den}**
                - Specific items (numerator): **{correct_num}**
                - Fraction: **{correct_num}/{correct_den}**
                
                **Remember:**
                - The numerator is the part we're counting
                - The denominator is the total number in the group
                
                Your answer: {user_answer}
                """)
                
    except ValueError:
        st.error("❌ Please enter whole numbers for the numerator and denominator (e.g., 3/4)")
    except Exception as e:
        st.error("❌ Invalid input. Please enter your answer as a fraction (e.g., 3/4)")