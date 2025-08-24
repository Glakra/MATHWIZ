import streamlit as st
import random

def run():
    """
    Main function to run the Frequency Tables activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/Q. Data and graphs/frequency_tables.py
    """
    # Initialize session state
    if "freq_table_difficulty" not in st.session_state:
        st.session_state.freq_table_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > Q. Data and graphs**")
    st.title("📊 Frequency Tables")
    st.markdown("*Read and interpret data from frequency tables*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.freq_table_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Questions",
            2: "Comparison Questions",
            3: "Complex Ranges",
            4: "Advanced Analysis"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic Questions')}")
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level}/4")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level == 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        if st.button("← Back to Curriculum", type="secondary"):
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
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Read Frequency Tables:
        - **First column:** Shows the values or categories
        - **Second column (Frequency):** Shows how many times each value occurs
        - **Total:** Add all frequencies to get the total count
        
        ### Question Types:
        - **Exact value:** "How many people have exactly 3?"
        - **More than:** "How many have more than 2?" (Don't include 2)
        - **Less than:** "How many have less than 5?" (Don't include 5)
        - **At least:** "How many have at least 1?" (Include 1 and above)
        - **At most:** "How many have at most 4?" (Include 4 and below)
        - **Between:** "How many have between 2 and 5?" (Check if inclusive)
        
        ### Tips:
        - **Read carefully:** "more than" vs "at least" are different!
        - **Add frequencies:** Sum the frequencies for all qualifying rows
        - **Check your work:** Make sure you included/excluded the right values
        """)

def generate_new_problem():
    """Generate a new frequency table problem"""
    difficulty = st.session_state.freq_table_difficulty
    
    # Define scenarios with rich contexts
    scenarios = [
        {
            "title": "Painting pictures",
            "context": "An art instructor kept track of how many total pictures were painted by each of the people enrolled in her class.",
            "item": "Pictures painted",
            "unit": "people",
            "color": "#FFB6C1",  # Light pink
            "min_val": 0,
            "max_val": 6
        },
        {
            "title": "Scarves",
            "context": "Jamie's Crafts is interested in offering a scarf knitting class, so the store considers how many scarves people already own.",
            "item": "Number of scarves",
            "unit": "people",
            "color": "#87CEEB",  # Sky blue
            "min_val": 0,
            "max_val": 5
        },
        {
            "title": "Drawing a card between 4 and 9",
            "context": "A maths textbook explains probability by showing a set of cards numbered 4 through 9 and showing the number of people who might draw each card.",
            "item": "Number drawn",
            "unit": "people",
            "color": "#FFB6C1",  # Light pink
            "min_val": 4,
            "max_val": 9
        },
        {
            "title": "Drawing a card between 2 and 8",
            "context": "As part of a maths lab, Larry tracked the number of times his classmates drew a number between 2 and 8.",
            "item": "Number drawn",
            "unit": "times",
            "color": "#FFB6C1",  # Light pink
            "min_val": 2,
            "max_val": 8
        },
        {
            "title": "Whale watching",
            "context": "An adventure tour company found out how many whales people saw on its most popular whale tour.",
            "item": "Whales spotted",
            "unit": "people",
            "color": "#90EE90",  # Light green
            "min_val": 0,
            "max_val": 6
        },
        {
            "title": "Playing miniature golf last summer",
            "context": "The Winchester Tourism Office researched how often people played miniature golf last summer.",
            "item": "Times played",
            "unit": "people",
            "color": "#E6E6FA",  # Lavender
            "min_val": 0,
            "max_val": 5
        },
        {
            "title": "Ice skating last winter",
            "context": "The Wagner Skating Rink counted the number of times people went ice skating last winter to see what types of discount passes it should offer this season.",
            "item": "Number of times",
            "unit": "people",
            "color": "#90EE90",  # Light green
            "min_val": 1,
            "max_val": 6
        },
        {
            "title": "Making leaf rubbings",
            "context": "After a field trip to the park, students in Mrs. Weber's art class counted the number of leaf rubbings they had made.",
            "item": "Leaf rubbings made",
            "unit": "students",
            "color": "#FFB6C1",  # Light pink
            "min_val": 0,
            "max_val": 5
        },
        {
            "title": "Sweatshirts",
            "context": "The Weston Secondary School fundraising committee found out how many sweatshirts students already had, in order to decide whether to sell sweatshirts for a fundraiser.",
            "item": "Number of sweatshirts",
            "unit": "students",
            "color": "#FFDAB9",  # Peach
            "min_val": 0,
            "max_val": 6
        },
        {
            "title": "Scores on a TV game show",
            "context": "Convinced that she could do well as a competitor, Kylie tracked the scores on a TV game show over the course of a week.",
            "item": "Score",
            "unit": "people",
            "color": "#90EE90",  # Light green
            "min_val": 5,
            "max_val": 10
        },
        {
            "title": "Books read last month",
            "context": "The school library surveyed students about their reading habits to plan for the upcoming book fair.",
            "item": "Books read",
            "unit": "students",
            "color": "#FFE4B5",  # Moccasin
            "min_val": 0,
            "max_val": 8
        },
        {
            "title": "Soccer goals scored",
            "context": "Coach Martinez tracked how many goals each player scored during the season to prepare for the awards ceremony.",
            "item": "Goals scored",
            "unit": "players",
            "color": "#98FB98",  # Pale green
            "min_val": 0,
            "max_val": 7
        }
    ]
    
    # Choose scenario
    scenario = random.choice(scenarios)
    
    # Generate frequency data
    if difficulty == 1:
        # Simple data, smaller range
        num_values = random.randint(4, 5)
        max_frequency = random.randint(10, 20)
    elif difficulty == 2:
        # Medium complexity
        num_values = random.randint(5, 6)
        max_frequency = random.randint(15, 25)
    elif difficulty == 3:
        # More complex data
        num_values = random.randint(6, 7)
        max_frequency = random.randint(10, 30)
    else:
        # Most complex
        num_values = random.randint(6, 8)
        max_frequency = random.randint(5, 35)
    
    # Create frequency distribution
    frequency_data = {}
    values = list(range(scenario["min_val"], 
                       min(scenario["min_val"] + num_values, scenario["max_val"] + 1)))
    
    for value in values:
        # Create realistic distributions
        if difficulty <= 2:
            frequency = random.randint(1, max_frequency)
        else:
            # More varied distributions for higher difficulties
            if random.random() < 0.2:
                frequency = 0  # Some values might have 0 frequency
            else:
                frequency = random.randint(1, max_frequency)
        frequency_data[value] = frequency
    
    # Generate question based on difficulty
    question_types = generate_question_types(difficulty, scenario, frequency_data)
    question = random.choice(question_types)
    
    # Store problem data
    st.session_state.problem_data = {
        "scenario": scenario,
        "frequency_data": frequency_data,
        "question": question["text"],
        "question_type": question["type"]
    }
    
    # Calculate correct answer
    st.session_state.correct_answer = question["calculate"](frequency_data)
    st.session_state.current_problem = question["text"]

def generate_question_types(difficulty, scenario, frequency_data):
    """Generate appropriate question types based on difficulty"""
    unit = scenario["unit"]
    item = scenario["item"].lower()
    
    question_types = []
    
    if difficulty == 1:
        # Basic questions - exact values and simple totals
        # Pick a value that exists in the data
        existing_values = [v for v, f in frequency_data.items() if f > 0]
        if existing_values:
            value = random.choice(existing_values)
            question_types.extend([
                {
                    "text": f"How many {unit} have exactly {value} {item}?",
                    "type": "exact",
                    "calculate": lambda fd: fd.get(value, 0)
                },
                {
                    "text": f"How many {unit} are there in all?",
                    "type": "total",
                    "calculate": lambda fd: sum(fd.values())
                }
            ])
    
    elif difficulty == 2:
        # Comparison questions - more than, less than
        values = list(frequency_data.keys())
        if len(values) > 2:
            threshold = values[len(values)//2]
            question_types.extend([
                {
                    "text": f"How many {unit} have more than {threshold} {item}?",
                    "type": "more_than",
                    "calculate": lambda fd: sum(f for v, f in fd.items() if v > threshold)
                },
                {
                    "text": f"How many {unit} have less than {threshold} {item}?",
                    "type": "less_than",
                    "calculate": lambda fd: sum(f for v, f in fd.items() if v < threshold)
                },
                {
                    "text": f"How many {unit} have at least {threshold} {item}?",
                    "type": "at_least",
                    "calculate": lambda fd: sum(f for v, f in fd.items() if v >= threshold)
                }
            ])
    
    elif difficulty >= 3:
        # Complex questions - ranges, specific conditions
        values = sorted(frequency_data.keys())
        if len(values) > 3:
            low = values[1]
            high = values[-2]
            mid = values[len(values)//2]
            
            question_types.extend([
                {
                    "text": f"How many {unit} have between {low} and {high} {item} (inclusive)?",
                    "type": "between_inclusive",
                    "calculate": lambda fd: sum(f for v, f in fd.items() if low <= v <= high)
                },
                {
                    "text": f"How many {unit} have at most {mid} {item}?",
                    "type": "at_most",
                    "calculate": lambda fd: sum(f for v, f in fd.items() if v <= mid)
                },
                {
                    "text": f"How many {unit} have either {values[0]} or {values[-1]} {item}?",
                    "type": "either",
                    "calculate": lambda fd: fd.get(values[0], 0) + fd.get(values[-1], 0)
                }
            ])
    
    # Add special questions based on scenario
    if "card" in scenario["title"].lower() or "draw" in scenario["title"].lower():
        if frequency_data:
            max_freq_value = max(frequency_data.items(), key=lambda x: x[1])[0]
            min_freq_value = min(frequency_data.items(), key=lambda x: x[1])[0]
            question_types.extend([
                {
                    "text": f"Which number was drawn the most times?",
                    "type": "max_value",
                    "calculate": lambda fd: max_freq_value
                },
                {
                    "text": f"Which number was drawn the fewest times?",
                    "type": "min_value",
                    "calculate": lambda fd: min_freq_value
                }
            ])
    
    # Ensure we always have at least one question
    if not question_types:
        question_types.append({
            "text": f"How many {unit} are there in all?",
            "type": "total",
            "calculate": lambda fd: sum(fd.values())
        })
    
    return question_types

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    scenario = data["scenario"]
    
    # Display context
    st.markdown(f"### {scenario['context']}")
    
    # Create and display the frequency table
    display_frequency_table(scenario, data["frequency_data"])
    
    # Display the question
    st.markdown("---")
    st.markdown(f"### {st.session_state.current_problem}")
    
    # Answer input
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        user_answer = st.text_input(
            "Your answer:",
            value=st.session_state.user_answer,
            key="answer_input",
            placeholder="Enter a number"
        )
        st.session_state.user_answer = user_answer
    
    with col2:
        if not st.session_state.answer_submitted:
            if st.button("Submit", type="primary", use_container_width=True):
                if user_answer:
                    check_answer()
                else:
                    st.error("Please enter an answer")
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Work it out button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Work it out", type="secondary", use_container_width=True):
                show_solution()
            
            if st.button("Next Question →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def display_frequency_table(scenario, frequency_data):
    """Display the frequency table with appropriate styling"""
    import pandas as pd
    
    # Create table title
    st.markdown(f"#### {scenario['title']}")
    
    # Prepare data for dataframe
    table_data = []
    for value, frequency in sorted(frequency_data.items()):
        table_data.append({
            scenario["item"]: value,
            "Frequency": frequency
        })
    
    df = pd.DataFrame(table_data)
    
    # Style the dataframe with custom CSS
    st.markdown(f"""
    <style>
    .frequency-table {{
        margin: 20px auto;
        border-collapse: collapse;
        background-color: white;
    }}
    .frequency-table th {{
        background-color: {scenario['color']};
        color: black;
        padding: 10px;
        font-weight: bold;
        border: 1px solid #ddd;
    }}
    .frequency-table td {{
        padding: 8px;
        text-align: center;
        border: 1px solid #ddd;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Display the dataframe
    st.dataframe(df, use_container_width=False, hide_index=True)

def check_answer():
    """Check if the user's answer is correct"""
    try:
        user_answer = int(st.session_state.user_answer)
        correct = (user_answer == st.session_state.correct_answer)
    except ValueError:
        correct = False
        user_answer = None
    
    st.session_state.answer_correct = correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_feedback():
    """Display feedback for the submitted answer"""
    if st.session_state.answer_correct:
        st.success("✅ **Correct! Well done!**")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.freq_table_difficulty
            st.session_state.freq_table_difficulty = min(
                st.session_state.freq_table_difficulty + 1, 4
            )
            
            if st.session_state.freq_table_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.freq_table_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. The correct answer is {st.session_state.correct_answer}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.freq_table_difficulty
            st.session_state.freq_table_difficulty = max(
                st.session_state.freq_table_difficulty - 1, 1
            )
            
            if st.session_state.freq_table_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.freq_table_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show step-by-step solution"""
    with st.expander("📝 **Step-by-step solution**", expanded=True):
        data = st.session_state.problem_data
        frequency_data = data["frequency_data"]
        question_type = data["question_type"]
        
        st.markdown("### How to solve this:")
        
        if question_type == "exact":
            st.markdown("1. **Find the row** in the table with the specified value")
            st.markdown("2. **Read the frequency** for that row")
            st.markdown(f"3. **Answer:** {st.session_state.correct_answer}")
            
        elif question_type == "total":
            st.markdown("1. **Add all frequencies** in the Frequency column:")
            frequencies = [f"{v}: {f}" for v, f in sorted(frequency_data.items())]
            st.markdown(f"   - {' + '.join(str(f) for _, f in sorted(frequency_data.items()))}")
            st.markdown(f"2. **Total:** {st.session_state.correct_answer}")
            
        elif question_type == "more_than":
            st.markdown("1. **Identify values** that are MORE THAN the threshold (not including it)")
            st.markdown("2. **Add their frequencies:**")
            threshold = extract_threshold_from_question(st.session_state.current_problem)
            qualifying = [(v, f) for v, f in frequency_data.items() if v > threshold]
            for v, f in sorted(qualifying):
                st.markdown(f"   - Value {v}: {f} {data['scenario']['unit']}")
            if qualifying:
                st.markdown(f"3. **Total:** {' + '.join(str(f) for _, f in qualifying)} = {st.session_state.correct_answer}")
            else:
                st.markdown(f"3. **No values qualify**, so answer is 0")
                
        elif question_type == "less_than":
            st.markdown("1. **Identify values** that are LESS THAN the threshold (not including it)")
            st.markdown("2. **Add their frequencies:**")
            threshold = extract_threshold_from_question(st.session_state.current_problem)
            qualifying = [(v, f) for v, f in frequency_data.items() if v < threshold]
            for v, f in sorted(qualifying):
                st.markdown(f"   - Value {v}: {f} {data['scenario']['unit']}")
            if qualifying:
                st.markdown(f"3. **Total:** {' + '.join(str(f) for _, f in qualifying)} = {st.session_state.correct_answer}")
            else:
                st.markdown(f"3. **No values qualify**, so answer is 0")
                
        elif question_type == "at_least":
            st.markdown("1. **Identify values** that are AT LEAST the threshold (including it)")
            st.markdown("2. **Add their frequencies:**")
            threshold = extract_threshold_from_question(st.session_state.current_problem)
            qualifying = [(v, f) for v, f in frequency_data.items() if v >= threshold]
            for v, f in sorted(qualifying):
                st.markdown(f"   - Value {v}: {f} {data['scenario']['unit']}")
            if qualifying:
                st.markdown(f"3. **Total:** {' + '.join(str(f) for _, f in qualifying)} = {st.session_state.correct_answer}")
            else:
                st.markdown(f"3. **No values qualify**, so answer is 0")

def extract_threshold_from_question(question):
    """Extract the threshold value from the question text"""
    import re
    # Look for patterns like "more than 3", "less than 5", "at least 2"
    patterns = [
        r"more than (\d+)",
        r"less than (\d+)",
        r"at least (\d+)",
        r"at most (\d+)",
        r"exactly (\d+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question)
        if match:
            return int(match.group(1))
    
    return 0

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct