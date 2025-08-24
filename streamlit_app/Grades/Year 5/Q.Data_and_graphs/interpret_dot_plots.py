import streamlit as st
import random

def run():
    """
    Main function to run the Interpret Dot Plots activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/Q. Data and graphs/interpret_dot_plots.py
    """
    # Initialize session state
    if "dot_plot_difficulty" not in st.session_state:
        st.session_state.dot_plot_difficulty = 1  # Start with simple counting
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > Q. Data and graphs**")
    st.title("📊 Interpret Dot Plots")
    st.markdown("*Read and interpret data from dot plots*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.dot_plot_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Counting",
            2: "Comparisons",
            3: "Range Questions",
            4: "Complex Analysis"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Simple Counting')}")
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
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Read Dot Plots:
        - **Each X represents one data point**
        - **Count the X's above each number** to find frequency
        - **The horizontal axis shows** the categories or values
        - **Stack of X's shows** how many times that value appears
        
        ### Question Types:
        - **Level 1 - Simple Counting:** "How many...?"
        - **Level 2 - Comparisons:** "Which has more/fewer...?"
        - **Level 3 - Range Questions:** "How many more than...?"
        - **Level 4 - Complex Analysis:** Combined conditions
        
        ### Tips for Success:
        - **Count carefully** - point to each X as you count
        - **Check the axis labels** to understand what's being measured
        - **For range questions**, identify which values to include
        - **Double-check** your counting before submitting
        
        ### Examples:
        - If 3 X's are above "2", then the value 2 appears 3 times
        - "More than 2" means values 3, 4, 5, etc.
        - "At least 2" means values 2, 3, 4, 5, etc.
        """)

def generate_new_problem():
    """Generate a new dot plot problem"""
    difficulty = st.session_state.dot_plot_difficulty
    
    # Define scenarios based on the provided images
    scenarios = [
        {
            "title": "Planting seeds in the garden",
            "x_label": "Seeds planted",
            "unit": "members",
            "context": "For Earth Day, the environmental club tracked the number of seeds planted by its members.",
            "color": "#ff6b35"  # Orange
        },
        {
            "title": "Running laps",
            "x_label": "Laps run",
            "unit": "clients",
            "context": "A health coach recorded how many laps each of his clients ran last week.",
            "color": "#4CAF50"  # Green
        },
        {
            "title": "Drawing a number between 1 and 6",
            "x_label": "Number drawn",
            "unit": "times",
            "context": "For a maths project, students pick cards numbered between 1 and 6 and write down the results.",
            "color": "#2196F3"  # Blue
        },
        {
            "title": "Making finger puppets",
            "x_label": "Finger puppets made",
            "unit": "children",
            "context": "Mr. Mason's art class counted the number of finger puppets they had made.",
            "color": "#9C27B0"  # Purple
        },
        {
            "title": "Spinning a wheel numbered 0 through 5",
            "x_label": "Number spun",
            "unit": "times",
            "context": "Some students spun a wheel that had numbers from 0 to 5 on it.",
            "color": "#00BCD4"  # Cyan
        },
        {
            "title": "Scarves",
            "x_label": "Number of scarves",
            "unit": "people",
            "context": "A craft store asked some people how many scarves they owned.",
            "color": "#009688"  # Teal
        },
        {
            "title": "Trips to a funfair last year",
            "x_label": "Number of trips",
            "unit": "people",
            "context": "Some friends compared how many times they visited a funfair last year.",
            "color": "#673AB7"  # Deep Purple
        },
        {
            "title": "Finding seashells",
            "x_label": "Seashells found",
            "unit": "people",
            "context": "At the beach, some people looked for shells.",
            "color": "#E91E63"  # Pink
        }
    ]
    
    # Choose a random scenario
    scenario = random.choice(scenarios)
    
    # Generate data distribution based on difficulty
    if difficulty == 1:
        # Simple distribution, 3-5 categories
        num_categories = random.randint(3, 5)
        max_frequency = random.randint(3, 6)
    elif difficulty == 2:
        # More categories, higher frequencies
        num_categories = random.randint(4, 6)
        max_frequency = random.randint(4, 8)
    elif difficulty == 3:
        # Even more categories
        num_categories = random.randint(5, 7)
        max_frequency = random.randint(5, 10)
    else:
        # Complex distribution
        num_categories = random.randint(6, 8)
        max_frequency = random.randint(6, 12)
    
    # Generate the data
    data = {}
    start_value = random.randint(0, 2)
    
    for i in range(num_categories):
        value = start_value + i
        # Generate frequency with some randomness
        if random.random() < 0.2:  # 20% chance of zero frequency
            frequency = 0
        else:
            frequency = random.randint(1, max_frequency)
        data[value] = frequency
    
    # Generate question based on difficulty
    question, answer = generate_question(data, scenario, difficulty)
    
    st.session_state.problem_data = {
        "scenario": scenario,
        "data": data,
        "question": question,
        "start_value": start_value,
        "num_categories": num_categories
    }
    st.session_state.correct_answer = answer
    st.session_state.current_problem = question

def get_context_word(scenario):
    """Get contextual verb based on scenario"""
    context_map = {
        "Planting seeds in the garden": "planted",
        "Running laps": "ran",
        "Drawing a number between 1 and 6": "drew",
        "Making finger puppets": "made",
        "Spinning a wheel numbered 0 through 5": "spun",
        "Scarves": "have",
        "Trips to a funfair last year": "visited the funfair",
        "Finding seashells": "found"
    }
    return context_map.get(scenario["title"], "had")

def generate_question(data, scenario, difficulty):
    """Generate a question based on the data and difficulty level"""
    unit = scenario["unit"]
    context_word = get_context_word(scenario)
    
    if difficulty == 1:
        # Simple counting questions
        question_types = [
            lambda: simple_count_question(data, unit, context_word),
            lambda: total_count_question(data, unit),
            lambda: specific_value_question(data, unit, scenario)
        ]
    elif difficulty == 2:
        # Comparison questions
        question_types = [
            lambda: most_frequent_question(data, unit, scenario),
            lambda: least_frequent_question(data, unit, scenario),
            lambda: comparison_question(data, unit, context_word)
        ]
    elif difficulty == 3:
        # Range questions
        question_types = [
            lambda: more_than_question(data, unit, context_word),
            lambda: less_than_question(data, unit, context_word),
            lambda: at_least_question(data, unit, context_word)
        ]
    else:
        # Complex analysis
        question_types = [
            lambda: between_range_question(data, unit, context_word),
            lambda: exactly_n_question(data, unit, context_word),
            lambda: difference_question(data, unit, scenario)
        ]
    
    # Choose a random question type
    return random.choice(question_types)()

def simple_count_question(data, unit, context_word):
    """Generate a simple counting question with better wording"""
    # Pick a value that exists in the data with non-zero frequency
    valid_values = [k for k, v in data.items() if v > 0]
    if not valid_values:
        value = random.choice(list(data.keys()))
    else:
        value = random.choice(valid_values)
    
    frequency = data[value]
    
    # Better wording based on context
    if context_word == "have":
        question = f"How many {unit} have {value} scarves?"
    elif context_word == "visited the funfair":
        question = f"How many {unit} visited the funfair {value} times?"
    elif context_word == "found":
        question = f"How many {unit} found {value} seashells?"
    elif context_word == "made":
        question = f"How many {unit} made {value} finger puppets?"
    elif context_word == "ran":
        question = f"How many {unit} ran {value} laps?"
    elif context_word == "planted":
        question = f"How many {unit} planted {value} seeds?"
    else:
        question = f"How many {unit} {context_word} {value}?"
    
    return question, frequency

def total_count_question(data, unit):
    """Ask for the total count with natural wording"""
    total = sum(data.values())
    question = f"How many {unit} are there in all?"
    return question, total

def specific_value_question(data, unit, scenario):
    """Ask about a specific value's frequency"""
    value = random.choice(list(data.keys()))
    frequency = data[value]
    
    if "Drawing" in scenario["title"]:
        question = f"How many times was {value} drawn?"
    elif "Spinning" in scenario["title"]:
        question = f"How many times was {value} spun?"
    else:
        question = f"How many times does {value} appear?"
    
    return question, frequency

def most_frequent_question(data, unit, scenario):
    """Ask which value appears most"""
    max_freq = max(data.values())
    most_frequent = [k for k, v in data.items() if v == max_freq]
    answer = min(most_frequent)
    
    if "Drawing" in scenario["title"]:
        question = f"Which number was drawn the most times?"
    elif "Spinning" in scenario["title"]:
        question = f"Which number was spun the most times?"
    elif "Making" in scenario["title"]:
        question = f"What number of finger puppets was made most often?"
    else:
        question = f"Which value appears most often?"
    
    return question, answer

def least_frequent_question(data, unit, scenario):
    """Ask which value appears least"""
    non_zero_data = {k: v for k, v in data.items() if v > 0}
    if not non_zero_data:
        answer = min(data.keys())
    else:
        min_freq = min(non_zero_data.values())
        least_frequent = [k for k, v in non_zero_data.items() if v == min_freq]
        answer = min(least_frequent)
    
    if "Drawing" in scenario["title"]:
        question = f"Which number was drawn the fewest times?"
    elif "Spinning" in scenario["title"]:
        question = f"Which number was spun the fewest times?"
    else:
        question = f"Which value appears least often?"
    
    return question, answer

def comparison_question(data, unit, context_word):
    """Ask to compare two values with better wording"""
    values = list(data.keys())
    if len(values) >= 2:
        val1, val2 = random.sample(values, 2)
        diff = abs(data[val1] - data[val2])
        
        # Natural wording for comparisons
        if data[val1] > data[val2]:
            if context_word == "have":
                question = f"How many more {unit} have {val1} scarves than have {val2} scarves?"
            elif context_word == "made":
                question = f"How many more {unit} made {val1} finger puppets than made {val2}?"
            elif context_word == "ran":
                question = f"How many more {unit} ran {val1} laps than ran {val2} laps?"
            else:
                question = f"How many more {unit} chose {val1} than {val2}?"
        else:
            if context_word == "have":
                question = f"How many more {unit} have {val2} scarves than have {val1} scarves?"
            elif context_word == "made":
                question = f"How many more {unit} made {val2} finger puppets than made {val1}?"
            elif context_word == "ran":
                question = f"How many more {unit} ran {val2} laps than ran {val1} laps?"
            else:
                question = f"How many more {unit} chose {val2} than {val1}?"
        
        return question, diff
    else:
        return simple_count_question(data, unit, context_word)

def more_than_question(data, unit, context_word):
    """Ask how many are more than a threshold"""
    values = sorted(data.keys())
    if len(values) > 2:
        threshold = random.choice(values[:-1])
        count = sum(freq for val, freq in data.items() if val > threshold)
        
        if context_word == "ran":
            question = f"How many {unit} ran more than {threshold} laps?"
        elif context_word == "have":
            question = f"How many {unit} have more than {threshold} scarves?"
        elif context_word == "found":
            question = f"How many {unit} found more than {threshold} seashells?"
        elif context_word == "made":
            question = f"How many {unit} made more than {threshold} finger puppets?"
        elif context_word == "planted":
            question = f"How many {unit} planted more than {threshold} seeds?"
        else:
            question = f"How many {unit} had more than {threshold}?"
        
        return question, count
    else:
        return simple_count_question(data, unit, context_word)

def less_than_question(data, unit, context_word):
    """Ask how many are less than a threshold"""
    values = sorted(data.keys())
    if len(values) > 2:
        threshold = random.choice(values[1:])
        count = sum(freq for val, freq in data.items() if val < threshold)
        
        if context_word == "have":
            question = f"How many {unit} have fewer than {threshold} scarves?"
        elif context_word == "ran":
            question = f"How many {unit} ran fewer than {threshold} laps?"
        elif context_word == "found":
            question = f"How many {unit} found fewer than {threshold} seashells?"
        elif context_word == "made":
            question = f"How many {unit} made fewer than {threshold} finger puppets?"
        elif context_word == "planted":
            question = f"How many {unit} planted fewer than {threshold} seeds?"
        else:
            question = f"How many {unit} had fewer than {threshold}?"
        
        return question, count
    else:
        return simple_count_question(data, unit, context_word)

def at_least_question(data, unit, context_word):
    """Ask how many have at least a certain value"""
    values = sorted(data.keys())
    if len(values) > 1:
        threshold = random.choice(values[:-1])
        count = sum(freq for val, freq in data.items() if val >= threshold)
        
        if context_word == "found":
            question = f"How many {unit} found at least {threshold} seashells?"
        elif context_word == "ran":
            question = f"How many {unit} ran at least {threshold} laps?"
        elif context_word == "have":
            question = f"How many {unit} have at least {threshold} scarves?"
        elif context_word == "made":
            question = f"How many {unit} made at least {threshold} finger puppets?"
        elif context_word == "planted":
            question = f"How many {unit} planted at least {threshold} seeds?"
        else:
            question = f"How many {unit} had at least {threshold}?"
        
        return question, count
    else:
        return total_count_question(data, unit)

def between_range_question(data, unit, context_word):
    """Ask about values in a range"""
    values = sorted(data.keys())
    if len(values) > 3:
        low = random.choice(values[:-2])
        high = random.choice([v for v in values if v > low + 1])
        count = sum(freq for val, freq in data.items() if low < val < high)
        
        if context_word == "ran":
            question = f"How many {unit} ran between {low} and {high} laps (not including {low} and {high})?"
        elif context_word == "have":
            question = f"How many {unit} have between {low} and {high} scarves (not including {low} and {high})?"
        elif context_word == "found":
            question = f"How many {unit} found between {low} and {high} seashells (not including {low} and {high})?"
        else:
            question = f"How many {unit} had between {low} and {high} (not including {low} and {high})?"
        
        return question, count
    else:
        return more_than_question(data, unit, context_word)

def exactly_n_question(data, unit, context_word):
    """Ask how many had exactly n occurrences"""
    # Pick a frequency that exists in the data
    frequencies = [f for f in data.values() if f > 0]
    if not frequencies:
        return total_count_question(data, unit)
    
    target_value = random.choice(list(data.keys()))
    target_freq = data[target_value]
    
    # Count how many have this exact value
    count = target_freq
    
    if context_word == "made":
        question = f"How many {unit} made exactly {target_value} finger puppets?"
    elif context_word == "ran":
        question = f"How many {unit} ran exactly {target_value} laps?"
    elif context_word == "have":
        question = f"How many {unit} have exactly {target_value} scarves?"
    elif context_word == "found":
        question = f"How many {unit} found exactly {target_value} seashells?"
    else:
        question = f"How many {unit} had exactly {target_value}?"
    
    return question, count

def difference_question(data, unit, scenario):
    """Ask about the difference between highest and lowest"""
    non_zero_freqs = [f for f in data.values() if f > 0]
    if len(non_zero_freqs) >= 2:
        max_freq = max(non_zero_freqs)
        min_freq = min(non_zero_freqs)
        diff = max_freq - min_freq
        
        if "Drawing" in scenario["title"]:
            question = f"What's the difference between the most and least frequently drawn numbers?"
        elif "Spinning" in scenario["title"]:
            question = f"What's the difference between the most and least frequently spun numbers?"
        else:
            question = f"What's the difference between the highest and lowest frequencies?"
        
        return question, diff
    else:
        return simple_count_question(data, unit, get_context_word(scenario))

def display_problem():
    """Display the current dot plot problem"""
    data = st.session_state.problem_data
    scenario = data["scenario"]
    plot_data = data["data"]
    
    # Display context and title
    st.markdown(f"### {scenario['context']}")
    st.markdown(f"**{scenario['title']}**")
    
    # Create the dot plot using SVG
    create_html_dot_plot(plot_data, scenario)
    
    # Display the question
    st.markdown("---")
    st.markdown(f"### ❓ {st.session_state.current_problem}")
    
    # Input area
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            # Determine input type based on question
            if "Which" in st.session_state.current_problem or "What number" in st.session_state.current_problem:
                # For "which number" questions, show selection
                user_answer = st.selectbox(
                    "Select your answer:",
                    options=[""] + [str(k) for k in sorted(plot_data.keys())],
                    key="answer_select"
                )
            else:
                # For counting questions, show number input
                user_answer = st.text_input(
                    f"Enter the number of {data['scenario']['unit']}:",
                    key="answer_input",
                    placeholder="Type your answer here"
                )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            process_answer(user_answer)
    
    # Show feedback if answer was submitted
    handle_feedback_and_next()

def create_html_dot_plot(data, scenario):
    """Create a dot plot using SVG for better control"""
    # Get the range of x values
    x_values = sorted(data.keys())
    x_min = min(x_values)
    x_max = max(x_values)
    
    # Calculate max frequency for scaling
    max_freq = max(data.values()) if data.values() else 1
    
    # SVG dimensions
    svg_width = 600
    svg_height = 350
    padding = 60
    plot_width = svg_width - 2 * padding
    plot_height = svg_height - 2 * padding
    
    # Calculate spacing
    num_values = x_max - x_min + 1
    column_width = plot_width / num_values
    
    # Start building SVG
    svg_parts = [f'<svg width="{svg_width}" height="{svg_height}" style="background-color: white;">']
    
    # Add background
    svg_parts.append(f'<rect x="0" y="0" width="{svg_width}" height="{svg_height}" fill="#f8f9fa" rx="10"/>')
    
    # Draw x-axis line
    svg_parts.append(f'<line x1="{padding}" y1="{svg_height - padding}" x2="{svg_width - padding}" y2="{svg_height - padding}" stroke="black" stroke-width="2"/>')
    
    # Add arrows to x-axis
    svg_parts.append(f'<polygon points="{padding-5},{svg_height-padding} {padding},{svg_height-padding-3} {padding},{svg_height-padding+3}" fill="black"/>')
    svg_parts.append(f'<polygon points="{svg_width-padding+5},{svg_height-padding} {svg_width-padding},{svg_height-padding-3} {svg_width-padding},{svg_height-padding+3}" fill="black"/>')
    
    # Draw data points and labels
    for i, x_val in enumerate(range(x_min, x_max + 1)):
        x_pos = padding + (i + 0.5) * column_width
        
        # Draw x-axis label
        svg_parts.append(f'<text x="{x_pos}" y="{svg_height - padding + 25}" text-anchor="middle" font-weight="bold" font-size="16">{x_val}</text>')
        
        # Draw X marks for this value
        if x_val in data:
            frequency = data[x_val]
            for j in range(frequency):
                y_pos = svg_height - padding - 30 - (j * 30)  # 30 pixels between each X
                svg_parts.append(f'<text x="{x_pos}" y="{y_pos}" text-anchor="middle" font-size="24" font-weight="bold" fill="{scenario["color"]}" font-family="Arial, sans-serif">X</text>')
    
    # Add x-axis label
    svg_parts.append(f'<text x="{svg_width/2}" y="{svg_height - 15}" text-anchor="middle" font-weight="bold" font-size="18">{scenario["x_label"]}</text>')
    
    svg_parts.append('</svg>')
    
    # Display the SVG
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0;">
            {''.join(svg_parts)}
        </div>
        """,
        unsafe_allow_html=True
    )

def process_answer(user_answer):
    """Process the user's answer"""
    try:
        # Convert answer to integer
        if user_answer.strip() == "":
            st.session_state.user_answer = None
        else:
            st.session_state.user_answer = int(user_answer)
        
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True
    except:
        st.session_state.user_answer = None
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    if user_answer is None:
        st.error("❌ **Please enter a valid answer.**")
        return
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Update consecutive counters
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.dot_plot_difficulty
            st.session_state.dot_plot_difficulty = min(
                st.session_state.dot_plot_difficulty + 1, 4
            )
            
            if st.session_state.dot_plot_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.dot_plot_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**.")
        
        # Update consecutive counters
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive wrong answers
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.dot_plot_difficulty
            st.session_state.dot_plot_difficulty = max(
                st.session_state.dot_plot_difficulty - 1, 1
            )
            
            if st.session_state.dot_plot_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.dot_plot_difficulty}**")
                st.session_state.consecutive_wrong = 0
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation"""
    data = st.session_state.problem_data
    plot_data = data["data"]
    question = st.session_state.current_problem
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **See the complete solution**", expanded=True):
        st.markdown("### How to solve this problem:")
        
        # Show the data in a table format
        st.markdown("**Step 1: Count the X's for each value**")
        
        # Create a simple table
        table_data = []
        for value in sorted(plot_data.keys()):
            freq = plot_data[value]
            table_data.append(f"Value {value}: {'X' * freq if freq > 0 else 'none'} = {freq}")
        
        for row in table_data:
            st.markdown(f"- {row}")
        
        st.markdown(f"\n**Step 2: Answer the question**")
        st.markdown(f"*{question}*")
        
        # Provide specific explanation based on question type
        if "How many" in question and "are there in all" in question:
            total = sum(plot_data.values())
            st.markdown(f"\nAdd all frequencies: {' + '.join(str(f) for f in plot_data.values() if f > 0)} = **{total}**")
        
        elif "more than" in question:
            # Find the threshold in the question
            parts = question.split()
            for i, part in enumerate(parts):
                if part == "than" and i > 0:
                    try:
                        threshold = int(parts[i+1].rstrip('?'))
                        relevant_values = [(v, f) for v, f in plot_data.items() if v > threshold]
                        st.markdown(f"\nValues more than {threshold}: {', '.join(str(v) for v, _ in relevant_values)}")
                        if relevant_values:
                            st.markdown(f"Count: {' + '.join(str(f) for _, f in relevant_values if f > 0)} = **{correct_answer}**")
                        else:
                            st.markdown(f"No values more than {threshold}, so count = **0**")
                        break
                    except:
                        pass
        
        elif "fewer than" in question or "less than" in question:
            # Find the threshold in the question
            parts = question.split()
            for i, part in enumerate(parts):
                if part == "than" and i > 0:
                    try:
                        threshold = int(parts[i+1].rstrip('?'))
                        relevant_values = [(v, f) for v, f in plot_data.items() if v < threshold]
                        st.markdown(f"\nValues less than {threshold}: {', '.join(str(v) for v, _ in relevant_values)}")
                        if relevant_values:
                            st.markdown(f"Count: {' + '.join(str(f) for _, f in relevant_values if f > 0)} = **{correct_answer}**")
                        else:
                            st.markdown(f"No values less than {threshold}, so count = **0**")
                        break
                    except:
                        pass
        
        elif "at least" in question:
            # Find the threshold in the question
            parts = question.split()
            for i, part in enumerate(parts):
                if part == "least" and i > 0:
                    try:
                        threshold = int(parts[i+1].rstrip('?'))
                        relevant_values = [(v, f) for v, f in plot_data.items() if v >= threshold]
                        st.markdown(f"\nValues at least {threshold}: {', '.join(str(v) for v, _ in relevant_values)}")
                        if relevant_values:
                            st.markdown(f"Count: {' + '.join(str(f) for _, f in relevant_values if f > 0)} = **{correct_answer}**")
                        else:
                            st.markdown(f"No values at least {threshold}, so count = **0**")
                        break
                    except:
                        pass
        
        elif "Which" in question and "most" in question:
            max_freq = max(plot_data.values())
            st.markdown(f"\nThe highest frequency is {max_freq}")
            st.markdown(f"Value {correct_answer} appears {max_freq} times")
        
        elif "Which" in question and "fewest" in question:
            non_zero = {k: v for k, v in plot_data.items() if v > 0}
            if non_zero:
                min_freq = min(non_zero.values())
                st.markdown(f"\nThe lowest frequency (excluding zeros) is {min_freq}")
                st.markdown(f"Value {correct_answer} appears {min_freq} times")
        
        elif "What's the difference" in question:
            st.markdown(f"\nThe difference is **{correct_answer}**")
        
        else:
            # For specific value questions
            st.markdown(f"\nThe answer is **{correct_answer}**")
        
        st.markdown("\n**Remember:** Each X represents one data point!")

def reset_question_state():
    """Reset the question state for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer