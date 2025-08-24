import streamlit as st
import random

def run():
    """
    Main function to run the number sequences word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/number_sequences_word_problems.py
    """
    # Initialize session state
    if "word_seq_difficulty" not in st.session_state:
        st.session_state.word_seq_difficulty = 1
    
    if "current_word_problem" not in st.session_state:
        st.session_state.current_word_problem = None
        st.session_state.word_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("📝 Number Sequences: Word Problems")
    st.markdown("*Find patterns in real-world situations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple arithmetic patterns",
            2: "Geometric & larger steps",
            3: "Mixed patterns",
            4: "Complex scenarios",
            5: "Challenge problems"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
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
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Tips for Word Problems**", expanded=False):
        st.markdown("""
        ### How to Solve Sequence Word Problems:
        
        1. **Read carefully** - Identify what's happening in each step
        2. **Find the pattern** - Look for:
           - Same amount added/subtracted (arithmetic)
           - Same amount multiplied/divided (geometric)
           - Increasing differences
           - Special patterns
        
        3. **Write the sequence** - List the numbers given
        4. **Continue the pattern** - Apply it to find the answer
        
        ### Common Patterns in Word Problems:
        
        **Arithmetic (Add/Subtract):**
        - "puts 5 more each time" → +5
        - "receives 10 fewer each day" → -10
        - "increases by 7 every month" → +7
        
        **Geometric (Multiply/Divide):**
        - "doubles each time" → ×2
        - "triples every day" → ×3
        - "half as many" → ÷2
        
        **Increasing Patterns:**
        - "adds 2 more than the previous increase"
        - "the difference grows by 3 each time"
        
        ### Key Words to Watch For:
        - **"continues"** = keep the same pattern
        - **"pattern"** = look for the rule
        - **"next"** = find what comes after
        - **"how many"** = calculate the answer
        
        ### Strategy:
        1. Underline the numbers in order
        2. Calculate differences or ratios
        3. Check if pattern is consistent
        4. Apply pattern to find answer
        """)

def generate_new_word_problem():
    """Generate a new word problem"""
    difficulty = st.session_state.word_seq_difficulty
    
    # Problem scenarios by difficulty
    if difficulty == 1:
        # Simple arithmetic patterns
        scenarios = [
            {
                "context": "A baker is putting cupcakes on trays to cool. She put {n1} cupcakes on the first tray, {n2} cupcakes on the second tray, {n3} cupcakes on the third tray, and {n4} cupcakes on the fourth tray.",
                "question": "If this pattern continues, how many cupcakes will the baker put on the fifth tray?",
                "unit": "cupcakes",
                "pattern_type": "arithmetic",
                "step": 7,
                "start": 49,
                "position": 5
            },
            {
                "context": "The teacher's helper was putting biscuits onto plates. He put {n1} biscuits on the first plate, {n2} biscuits on the second plate, {n3} biscuits on the third plate, {n4} biscuits on the fourth plate, and {n5} biscuits on the fifth plate.",
                "question": "If this pattern continues, how many biscuits will the helper put on the sixth plate?",
                "unit": "biscuits",
                "pattern_type": "arithmetic",
                "step": 5,
                "start": 30,
                "position": 6
            },
            {
                "context": "A gardener plants flowers in rows. She plants {n1} flowers in the first row, {n2} flowers in the second row, {n3} flowers in the third row, and {n4} flowers in the fourth row.",
                "question": "If this pattern continues, how many flowers will she plant in the fifth row?",
                "unit": "flowers",
                "pattern_type": "arithmetic",
                "step": random.choice([3, 4, 6, 8]),
                "start": random.randint(10, 30),
                "position": 5
            },
            {
                "context": "Tom is saving money each week. He saved ${n1} in the first week, ${n2} in the second week, ${n3} in the third week, and ${n4} in the fourth week.",
                "question": "If this pattern continues, how much will Tom save in the fifth week?",
                "unit": "dollars",
                "pattern_type": "arithmetic",
                "step": random.choice([5, 10, 15, 20]),
                "start": random.randint(10, 50),
                "position": 5
            }
        ]
    
    elif difficulty == 2:
        # Geometric & larger arithmetic steps
        scenarios = [
            {
                "context": "At a birthday party, the first child receives {n1} smiley stickers, the second child receives {n2} smiley stickers, the third child receives {n3} smiley stickers, and the fourth child receives {n4} smiley stickers.",
                "question": "If this pattern continues, how many smiley stickers will the fifth child receive?",
                "unit": "smiley stickers",
                "pattern_type": "arithmetic",
                "step": 5,
                "start": 17,
                "position": 5
            },
            {
                "context": "While organizing her DVD collection, Elizabeth put {n1} DVDs on the first rack, {n2} DVDs on the second rack, {n3} DVDs on the third rack, and {n4} DVDs on the fourth rack.",
                "question": "If this pattern continues, how many DVDs will Elizabeth put on the fifth rack?",
                "unit": "DVDs",
                "pattern_type": "geometric",
                "ratio": 2,
                "start": 5,
                "position": 5
            },
            {
                "context": "A library displays books on special shelves. They put {n1} books on the first shelf, {n2} books on the second shelf, {n3} books on the third shelf, and {n4} books on the fourth shelf.",
                "question": "If this pattern continues, how many books will be on the fifth shelf?",
                "unit": "books",
                "pattern_type": "geometric",
                "ratio": random.choice([2, 3]),
                "start": random.randint(3, 8),
                "position": 5
            },
            {
                "context": "Hanson's Bakery is getting more and more orders for blackberry pies. The bakers made {n1} blackberry pies in November, {n2} blackberry pies in December, {n3} blackberry pies in January, {n4} blackberry pies in February, and {n5} blackberry pies in March.",
                "question": "If this pattern continues, how many blackberry pies will the bakery make in April?",
                "unit": "blackberry pies",
                "pattern_type": "arithmetic",
                "step": 10,
                "start": 55,
                "position": 6
            }
        ]
    
    elif difficulty == 3:
        # Mixed patterns including geometric with ×3
        scenarios = [
            {
                "context": "While sorting some change into piggy banks, Maura put {n1} coins in the first piggy bank, {n2} coins in the second piggy bank, {n3} coins in the third piggy bank, {n4} coins in the fourth piggy bank, and {n5} coins in the fifth piggy bank.",
                "question": "If this pattern continues, how many coins will Maura put in the sixth piggy bank?",
                "unit": "coins",
                "pattern_type": "geometric",
                "ratio": 3,
                "start": 3,
                "position": 6
            },
            {
                "context": "Ivan sent {n1} e-mails on Thursday, {n2} e-mails on Friday, {n3} e-mails on Saturday, and {n4} e-mails on Sunday.",
                "question": "If this pattern continues, how many e-mails will Ivan send on Monday?",
                "unit": "e-mails",
                "pattern_type": "geometric",
                "ratio": 3,
                "start": 3,
                "position": 5
            },
            {
                "context": "While sorting some buttons, Dakota put {n1} buttons in the first box, {n2} buttons in the second box, {n3} buttons in the third box, and {n4} buttons in the fourth box.",
                "question": "If this pattern continues, how many buttons will Dakota put in the fifth box?",
                "unit": "buttons",
                "pattern_type": "geometric",
                "ratio": 2,
                "start": 5,
                "position": 5
            },
            {
                "context": "A scientist observes bacteria growth. On day 1 there were {n1} bacteria, on day 2 there were {n2} bacteria, on day 3 there were {n3} bacteria, and on day 4 there were {n4} bacteria.",
                "question": "If this pattern continues, how many bacteria will there be on day 5?",
                "unit": "bacteria",
                "pattern_type": "geometric",
                "ratio": random.choice([2, 3, 4]),
                "start": random.randint(2, 10),
                "position": 5
            }
        ]
    
    elif difficulty == 4:
        # Complex scenarios including increasing patterns
        scenarios = [
            {
                "context": "The flower shop displays a different number of roses in the front window every month. It displayed {n1} roses in September, {n2} roses in October, {n3} roses in November, and {n4} roses in December.",
                "question": "If this pattern continues, how many roses will the flower shop window display in January?",
                "unit": "roses",
                "pattern_type": "increasing",
                "start": 4,
                "first_diff": 2,
                "increment": 2,
                "position": 5
            },
            {
                "context": "Samantha sent {n1} e-mails on Tuesday, {n2} e-mails on Wednesday, {n3} e-mails on Thursday, {n4} e-mails on Friday, and {n5} e-mails on Saturday.",
                "question": "If this pattern continues, how many e-mails will Samantha send on Sunday?",
                "unit": "e-mails",
                "pattern_type": "fibonacci",
                "sequence": [4, 5, 8, 13, 20],
                "position": 6
            },
            {
                "context": "A charity fundraiser collects more donations each day. They collected ${n1} on Monday, ${n2} on Tuesday, ${n3} on Wednesday, and ${n4} on Thursday.",
                "question": "If this pattern continues, how much will they collect on Friday?",
                "unit": "dollars",
                "pattern_type": "increasing",
                "start": random.randint(10, 50),
                "first_diff": random.randint(5, 10),
                "increment": random.randint(5, 10),
                "position": 5
            },
            {
                "context": "A social media post is going viral. It had {n1} shares after 1 hour, {n2} shares after 2 hours, {n3} shares after 3 hours, and {n4} shares after 4 hours.",
                "question": "If this pattern continues, how many shares will it have after 5 hours?",
                "unit": "shares",
                "pattern_type": "geometric",
                "ratio": random.choice([3, 4, 5]),
                "start": random.randint(2, 10),
                "position": 5
            }
        ]
    
    else:  # difficulty == 5
        # Challenge problems with various complex patterns
        scenarios = [
            {
                "context": "A tree grows in an unusual pattern. In year 1 it was {n1} feet tall, in year 2 it was {n2} feet tall, in year 3 it was {n3} feet tall, in year 4 it was {n4} feet tall, and in year 5 it was {n5} feet tall.",
                "question": "If this pattern continues, how tall will the tree be in year 6?",
                "unit": "feet",
                "pattern_type": "fibonacci",
                "sequence": [3, 5, 8, 13, 21],
                "position": 6
            },
            {
                "context": "A game show increases prize money in a special way. Round 1 had ${n1}, round 2 had ${n2}, round 3 had ${n3}, and round 4 had ${n4}.",
                "question": "If this pattern continues, what will be the prize money for round 5?",
                "unit": "dollars",
                "pattern_type": "squares",
                "multiplier": random.choice([100, 200, 500]),
                "start": 1,
                "position": 5
            },
            {
                "context": "A company's user base is growing rapidly. They had {n1} users in January, {n2} users in February, {n3} users in March, and {n4} users in April.",
                "question": "If this pattern continues, how many users will they have in May?",
                "unit": "users",
                "pattern_type": "geometric",
                "ratio": random.choice([5, 6, 10]),
                "start": random.randint(10, 100),
                "position": 5
            },
            {
                "context": "An artist creates a pattern with tiles. Row 1 has {n1} tiles, row 2 has {n2} tiles, row 3 has {n3} tiles, row 4 has {n4} tiles, and row 5 has {n5} tiles.",
                "question": "If this pattern continues, how many tiles will be in row 6?",
                "unit": "tiles",
                "pattern_type": "increasing",
                "start": random.randint(1, 10),
                "first_diff": random.randint(1, 5),
                "increment": random.randint(2, 5),
                "position": 6
            }
        ]
    
    # Select a scenario
    scenario = random.choice(scenarios)
    
    # Generate the sequence based on pattern type
    sequence = []
    
    if scenario["pattern_type"] == "arithmetic":
        for i in range(scenario["position"]):
            sequence.append(scenario["start"] + i * scenario["step"])
    
    elif scenario["pattern_type"] == "geometric":
        current = scenario["start"]
        for i in range(scenario["position"]):
            sequence.append(current)
            current *= scenario["ratio"]
    
    elif scenario["pattern_type"] == "increasing":
        sequence = [scenario["start"]]
        current_diff = scenario["first_diff"]
        for i in range(1, scenario["position"]):
            sequence.append(sequence[-1] + current_diff)
            current_diff += scenario["increment"]
    
    elif scenario["pattern_type"] == "fibonacci":
        # Use provided sequence and calculate next
        sequence = scenario["sequence"].copy()
        while len(sequence) < scenario["position"]:
            sequence.append(sequence[-1] + sequence[-2])
    
    elif scenario["pattern_type"] == "squares":
        mult = scenario["multiplier"]
        for i in range(1, scenario["position"] + 1):
            sequence.append(i * i * mult)
    
    # Format the context with the sequence values
    context_values = {}
    for i in range(min(len(sequence) - 1, 5)):
        context_values[f"n{i+1}"] = sequence[i]
    
    formatted_context = scenario["context"].format(**context_values)
    
    # Store problem data
    st.session_state.word_problem_data = {
        'context': formatted_context,
        'question': scenario["question"],
        'unit': scenario["unit"],
        'sequence': sequence,
        'answer': sequence[scenario["position"] - 1],
        'pattern_type': scenario["pattern_type"],
        'given_count': len(context_values)
    }
    st.session_state.current_word_problem = True

def display_word_problem():
    """Display the word problem"""
    data = st.session_state.word_problem_data
    
    # Display the problem text
    st.markdown("### 📖 Problem:")
    st.markdown(f"**{data['context']}**")
    st.markdown(f"**{data['question']}**")
    
    # Input field for answer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create input with unit label
        user_input = st.text_input(
            "",
            key="word_answer",
            placeholder=f"Enter number of {data['unit']}",
            label_visibility="collapsed"
        )
        
        # Show unit next to input
        st.markdown(f"<p style='text-align: center; margin-top: -10px; color: #666;'>{data['unit']}</p>", 
                   unsafe_allow_html=True)
    
    # Style the input
    st.markdown("""
    <style>
    input[type="text"] {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        height: 45px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            if user_input:
                st.session_state.user_answer = user_input
                validate_word_answer()
            else:
                st.warning(f"Please enter the number of {data['unit']}!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_word_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_word_problem_state()
                st.rerun()

def validate_word_answer():
    """Validate the user's answer"""
    data = st.session_state.word_problem_data
    
    st.session_state.total_attempted += 1
    
    try:
        # Remove commas and convert to integer
        user_value = int(st.session_state.user_answer.replace(',', '').replace('$', ''))
        correct_value = data['answer']
        
        if user_value == correct_value:
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            st.session_state.user_correct = True
            
            # Increase difficulty after 3 consecutive correct
            if st.session_state.consecutive_correct >= 3:
                if st.session_state.word_seq_difficulty < 5:
                    st.session_state.word_seq_difficulty += 1
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            st.session_state.user_correct = False
            
            # Decrease difficulty after poor performance
            if st.session_state.total_attempted % 3 == 0:
                accuracy = st.session_state.total_correct / st.session_state.total_attempted
                if accuracy < 0.5 and st.session_state.word_seq_difficulty > 1:
                    st.session_state.word_seq_difficulty -= 1
    except:
        st.session_state.user_correct = False
        st.session_state.consecutive_correct = 0
    
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_word_feedback():
    """Display feedback for word problems"""
    data = st.session_state.word_problem_data
    
    if st.session_state.user_correct:
        st.success("✅ **Correct! Excellent work!**")
        
        # Show pattern recognition
        pattern_descriptions = {
            'arithmetic': f"You recognized the arithmetic pattern (adding {data['sequence'][1] - data['sequence'][0]} each time)!",
            'geometric': f"You found the geometric pattern (multiplying by {data['sequence'][1] // data['sequence'][0]} each time)!",
            'increasing': "You identified the increasing difference pattern!",
            'fibonacci': "You recognized the Fibonacci-like pattern!",
            'squares': "You found the square numbers pattern!"
        }
        
        if data['pattern_type'] in pattern_descriptions:
            st.info(f"💡 {pattern_descriptions[data['pattern_type']]}")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.word_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.word_seq_difficulty), unsafe_allow_html=True)
    else:
        correct_answer = data['answer']
        st.error(f"❌ **Not quite. The correct answer is {correct_answer} {data['unit']}.**")
        
        # Show explanation
        show_word_explanation()

def show_word_explanation():
    """Show step-by-step solution for word problems"""
    data = st.session_state.word_problem_data
    
    with st.expander("📖 **See the solution step-by-step**", expanded=True):
        st.markdown("### How to solve this problem:")
        
        # Extract the given numbers
        st.markdown("**Step 1: Write down the numbers in order**")
        given_sequence = data['sequence'][:data['given_count']]
        sequence_str = ", ".join([str(n) for n in given_sequence])
        st.code(f"Sequence: {sequence_str}")
        
        # Show pattern identification
        st.markdown("**Step 2: Find the pattern**")
        
        if data['pattern_type'] == 'arithmetic':
            # Calculate differences
            differences = []
            for i in range(1, len(given_sequence)):
                diff = given_sequence[i] - given_sequence[i-1]
                differences.append(diff)
                st.code(f"{given_sequence[i]} - {given_sequence[i-1]} = {diff}")
            
            if all(d == differences[0] for d in differences):
                st.markdown(f"**Pattern found:** Add {differences[0]} each time")
        
        elif data['pattern_type'] == 'geometric':
            # Calculate ratios
            ratios = []
            for i in range(1, len(given_sequence)):
                if given_sequence[i-1] != 0:
                    ratio = given_sequence[i] // given_sequence[i-1]
                    ratios.append(ratio)
                    st.code(f"{given_sequence[i]} ÷ {given_sequence[i-1]} = {ratio}")
            
            if ratios and all(r == ratios[0] for r in ratios):
                st.markdown(f"**Pattern found:** Multiply by {ratios[0]} each time")
        
        elif data['pattern_type'] == 'increasing':
            # Show increasing differences
            differences = []
            for i in range(1, len(given_sequence)):
                diff = given_sequence[i] - given_sequence[i-1]
                differences.append(diff)
                st.code(f"{given_sequence[i]} - {given_sequence[i-1]} = {diff}")
            
            st.markdown("**Pattern found:** The differences increase each time")
            diff_of_diffs = []
            for i in range(1, len(differences)):
                dd = differences[i] - differences[i-1]
                diff_of_diffs.append(dd)
                st.code(f"Difference increases by: {dd}")
        
        elif data['pattern_type'] == 'fibonacci':
            st.markdown("**Pattern found:** Each number is the sum of the two before it")
            for i in range(2, len(given_sequence)):
                st.code(f"{given_sequence[i-2]} + {given_sequence[i-1]} = {given_sequence[i]}")
        
        elif data['pattern_type'] == 'squares':
            st.markdown("**Pattern found:** These are square numbers")
            mult = given_sequence[0]
            for i in range(len(given_sequence)):
                base = i + 1
                st.code(f"{base}² × {mult // (base * base)} = {given_sequence[i]}")
        
        # Show the calculation for the answer
        st.markdown("**Step 3: Continue the pattern**")
        
        # Show how to get to the answer
        if len(data['sequence']) > data['given_count']:
            missing_steps = data['sequence'][data['given_count']:]
            position_names = ["fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
            
            for i, value in enumerate(missing_steps):
                pos_name = position_names[data['given_count'] + i - 5] if data['given_count'] + i - 5 < len(position_names) else f"position {data['given_count'] + i + 1}"
                
                if data['pattern_type'] == 'arithmetic':
                    prev = data['sequence'][data['given_count'] + i - 1]
                    step = data['sequence'][1] - data['sequence'][0]
                    st.code(f"The {pos_name}: {prev} + {step} = {value}")
                    
                elif data['pattern_type'] == 'geometric':
                    prev = data['sequence'][data['given_count'] + i - 1]
                    ratio = data['sequence'][1] // data['sequence'][0]
                    st.code(f"The {pos_name}: {prev} × {ratio} = {value}")
                    
                elif data['pattern_type'] == 'fibonacci':
                    prev1 = data['sequence'][data['given_count'] + i - 2]
                    prev2 = data['sequence'][data['given_count'] + i - 1]
                    st.code(f"The {pos_name}: {prev1} + {prev2} = {value}")
                    
                else:
                    st.markdown(f"The {pos_name}: **{value}**")
        
        # Show final answer
        st.markdown("**Answer:**")
        st.success(f"{data['answer']} {data['unit']}")
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_word_problem_state():
    """Reset for next problem"""
    st.session_state.current_word_problem = None
    st.session_state.word_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""
    if "user_correct" in st.session_state:
        del st.session_state.user_correct