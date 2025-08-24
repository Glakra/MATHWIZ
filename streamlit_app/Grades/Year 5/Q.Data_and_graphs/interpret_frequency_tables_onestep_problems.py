import streamlit as st
import random

def run():
    """
    Main function to run the Interpret Frequency Tables: One-Step Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/Q. Data and graphs/interpret_frequency_tables_onestep_problems.py
    """
    # Initialize session state
    if "interpret_freq_difficulty" not in st.session_state:
        st.session_state.interpret_freq_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.question_type = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Q. Data and graphs**")
    st.title("📊 Interpret Frequency Tables: One-Step Problems")
    st.markdown("*Answer questions using data from frequency tables*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.interpret_freq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Totals",
            2: "Calculations & Comparisons",
            3: "Money Problems",
            4: "Complex Analysis"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Simple Totals')}")
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
        ### Types of One-Step Problems:
        
        **1. Finding Totals:**
        - Add all frequencies together
        - Example: "How many in all?" → Add every number in the frequency column
        
        **2. Finding Specific Values:**
        - Look for one row in the table
        - Example: "How many chose red?" → Find 'red' and read its frequency
        
        **3. Finding Most/Least Popular:**
        - Compare all frequencies
        - The highest number = most popular
        - The lowest number = least popular
        
        **4. Simple Comparisons:**
        - "How many more A than B?" → Subtract B from A
        - Only requires one calculation step
        
        **5. Money Calculations:**
        - Multiply frequency × price
        - Example: "27 smoothies at $6 each" → 27 × 6 = $162
        
        ### Tips:
        - **Read carefully** - what exactly is being asked?
        - **One step only** - these problems need just one calculation
        - **Check units** - especially for money problems ($)
        """)

def generate_new_problem():
    """Generate a new frequency table interpretation problem"""
    difficulty = st.session_state.interpret_freq_difficulty
    
    # Define comprehensive scenarios
    scenarios = [
        # Food/Drink scenarios
        {
            "title": "Smoothie sales",
            "context": "Sandra owns the Smooth Sips smoothie shop. She recorded her Friday morning sales in a frequency table.",
            "item_label": "Flavours",
            "frequency_label": "Frequency",
            "unit": "smoothies",
            "color": "#FF8C00",  # Dark orange
            "items": ["banana", "mango", "orange", "pineapple", "strawberry"],
            "has_price": True,
            "price_text": "Strawberry smoothies sell for $6 each.",
            "price_item": "strawberry",
            "price": 6
        },
        {
            "title": "Favourite flavours of ice cream",
            "context": "Mr Turner promised to bring his students ice cream on Friday. The students voted on their favourite flavour, and the votes were recorded in a frequency table.",
            "item_label": "Flavour",
            "frequency_label": "Frequency",
            "unit": "votes",
            "color": "#9370DB",  # Medium purple
            "items": ["chocolate", "cookie dough", "strawberry", "vanilla"],
            "has_price": False
        },
        {
            "title": "Lunch orders",
            "context": "Chef Lee works at Beachside Restaurant and wants to offer a lunch special based on the most popular dish. He records Saturday's lunch orders in a frequency table.",
            "item_label": "Dish",
            "frequency_label": "Frequency",
            "unit": "orders",
            "color": "#6A5ACD",  # Slate blue
            "items": ["clam chowder", "grilled salmon", "lobster roll", "prawn scampi"],
            "has_price": False
        },
        
        # Career/Activities scenarios
        {
            "title": "When I grow up",
            "context": "Ms Green asked her foundation students what they want to be when they grow up. She recorded their answers in a frequency table.",
            "item_label": "Job",
            "frequency_label": "Frequency",
            "unit": "students",
            "color": "#228B22",  # Forest green
            "items": ["astronaut", "doctor", "police officer", "singer", "teacher"],
            "has_price": False
        },
        {
            "title": "Art projects",
            "context": "Mr Green let each of his art students choose a material for his or her art project. He recorded their choices in a frequency table.",
            "item_label": "Material",
            "frequency_label": "Frequency",
            "unit": "projects",
            "color": "#7B68EE",  # Medium slate blue
            "items": ["pottery", "painting", "papier-mâché"],
            "has_price": False
        },
        {
            "title": "Guitar lessons",
            "context": "Carly teaches guitar lessons on the weekends. Her students play several different styles of guitar. She recorded how many lessons of each style she taught last month in the frequency table below.",
            "item_label": "Style",
            "frequency_label": "Frequency",
            "unit": "guitar lessons",
            "color": "#228B22",  # Forest green
            "items": ["acoustic", "classical", "electric"],
            "has_price": False
        },
        
        # Shopping scenarios
        {
            "title": "Jersey sizes",
            "context": "Reagan's netball team ordered new jerseys. She recorded the sizes they needed in a frequency table.",
            "item_label": "Size",
            "frequency_label": "Frequency",
            "unit": "jerseys",
            "color": "#00BFFF",  # Deep sky blue
            "items": ["small", "medium", "large"],
            "has_price": False
        },
        {
            "title": "Shirt sales",
            "context": "Button-Down Boutique sells shirts with a variety of prints. The manager wants to know which print is the most popular, so she keeps track of shirt sales over the weekend.",
            "item_label": "Print",
            "frequency_label": "Frequency",
            "unit": "shirts",
            "color": "#9370DB",  # Medium purple
            "items": ["floral", "paisley", "plaid", "polka dot", "striped"],
            "has_price": False
        },
        
        # School scenarios
        {
            "title": "Favourite colours",
            "context": "It's the first day of school, and Mr Wiley wants to get to know his students. He asks each student for their favourite colour and records their answers in a frequency table.",
            "item_label": "Colour",
            "frequency_label": "Frequency",
            "unit": "students",
            "color": "#FF8C00",  # Dark orange
            "items": ["red", "orange", "yellow", "green", "blue", "purple"],
            "has_price": False
        },
        {
            "title": "Favourite party activities",
            "context": "The Year 5 students at Seaside Elementary voted for their favourite end-of-the-year party activity. The results were recorded in a frequency table.",
            "item_label": "Activity",
            "frequency_label": "Frequency",
            "unit": "votes",
            "color": "#228B22",  # Forest green
            "items": ["water-balloon toss", "sack races", "dance contest", "sandcastle building"],
            "has_price": False
        }
    ]
    
    # Choose scenario
    scenario = random.choice(scenarios)
    
    # Generate frequency data
    if difficulty == 1:
        # Simple data for totals and finding specific values
        frequencies = generate_simple_frequencies(scenario["items"], 5, 30)
        question_types = ["total", "most_popular_mc", "specific_value"]
    elif difficulty == 2:
        # Comparisons and more complex questions
        frequencies = generate_varied_frequencies(scenario["items"], 3, 35)
        question_types = ["comparison", "most_popular_mc", "least_popular_mc", "total"]
    elif difficulty == 3:
        # Money calculations
        if scenario["has_price"]:
            frequencies = generate_varied_frequencies(scenario["items"], 10, 30)
            question_types = ["money_calculation", "total", "most_popular_mc"]
        else:
            frequencies = generate_varied_frequencies(scenario["items"], 5, 40)
            question_types = ["comparison", "total", "most_popular_mc"]
    else:
        # Complex analysis
        frequencies = generate_complex_frequencies(scenario["items"], 0, 50)
        question_types = ["comparison", "money_calculation" if scenario["has_price"] else "total", 
                        "most_popular_mc", "least_popular_mc"]
    
    # Generate question
    question_type = random.choice(question_types)
    question_data = generate_question(scenario, frequencies, question_type)
    
    # Store problem data
    st.session_state.problem_data = {
        "scenario": scenario,
        "frequencies": frequencies,
        "question": question_data["question"],
        "answer": question_data["answer"],
        "options": question_data.get("options", []),
        "answer_type": question_data["answer_type"],
        "unit": question_data.get("unit", "")
    }
    st.session_state.correct_answer = question_data["answer"]
    st.session_state.current_problem = question_data["question"]
    st.session_state.question_type = question_type

def generate_simple_frequencies(items, min_val, max_val):
    """Generate simple frequency data"""
    frequencies = {}
    for item in items:
        frequencies[item] = random.randint(min_val, max_val)
    return frequencies

def generate_varied_frequencies(items, min_val, max_val):
    """Generate varied frequency data with some patterns"""
    frequencies = {}
    # Ensure variety in values
    used_values = set()
    for item in items:
        val = random.randint(min_val, max_val)
        # Try to avoid too many duplicates
        attempts = 0
        while val in used_values and attempts < 5:
            val = random.randint(min_val, max_val)
            attempts += 1
        frequencies[item] = val
        used_values.add(val)
    return frequencies

def generate_complex_frequencies(items, min_val, max_val):
    """Generate complex frequency data with possible zeros"""
    frequencies = {}
    for item in items:
        if random.random() < 0.1:  # 10% chance of zero
            frequencies[item] = 0
        else:
            frequencies[item] = random.randint(min_val + 1, max_val)
    return frequencies

def generate_question(scenario, frequencies, question_type):
    """Generate a specific question based on type"""
    if question_type == "total":
        total = sum(frequencies.values())
        return {
            "question": f"How many {scenario['unit']} are there in all?",
            "answer": total,
            "answer_type": "number",
            "unit": scenario['unit']
        }
    
    elif question_type == "specific_value":
        item = random.choice(list(frequencies.keys()))
        return {
            "question": f"How many {scenario['unit']} chose {item}?",
            "answer": frequencies[item],
            "answer_type": "number",
            "unit": scenario['unit']
        }
    
    elif question_type == "comparison":
        # Pick two items for comparison
        items = list(frequencies.keys())
        if len(items) >= 2:
            item1, item2 = random.sample(items, 2)
            diff = frequencies[item1] - frequencies[item2]
            if diff > 0:
                return {
                    "question": f"How many more {scenario['unit']} want to be {item1}s than {item2}s?"
                               if "Job" in scenario["item_label"] 
                               else f"How many more {scenario['unit']} chose {item1} than {item2}?",
                    "answer": diff,
                    "answer_type": "number",
                    "unit": f"more {scenario['unit']}"
                }
            else:
                return generate_question(scenario, frequencies, "total")  # Fallback
        else:
            return generate_question(scenario, frequencies, "total")  # Fallback
    
    elif question_type == "most_popular_mc":
        max_item = max(frequencies.items(), key=lambda x: x[1])[0]
        options = list(frequencies.keys())
        
        question_text = {
            "ice cream": "Which flavour of ice cream received the greatest number of votes?",
            "colours": "Which colour is the most popular?",
            "lunch": "Which dish is ordered the most?",
            "shirt": "Which print is the most popular?",
            "party": "Which party activity got the most votes?"
        }
        
        default_q = f"Which {scenario['item_label'].lower()} is the most popular?"
        q_text = question_text.get(scenario['title'].split()[0].lower(), default_q)
        
        return {
            "question": q_text,
            "answer": max_item,
            "answer_type": "multiple_choice",
            "options": options
        }
    
    elif question_type == "least_popular_mc":
        min_item = min(frequencies.items(), key=lambda x: x[1])[0]
        options = list(frequencies.keys())
        
        return {
            "question": f"Which {scenario['item_label'].lower()} is the least popular?",
            "answer": min_item,
            "answer_type": "multiple_choice",
            "options": options
        }
    
    elif question_type == "money_calculation":
        if scenario["has_price"]:
            price_item = scenario["price_item"]
            price = scenario["price"]
            quantity = frequencies[price_item]
            total = quantity * price
            
            return {
                "question": f"{scenario['price_text']} How much money did Sandra's shop make from {price_item} {scenario['unit']}?",
                "answer": total,
                "answer_type": "money",
                "unit": ""
            }
        else:
            return generate_question(scenario, frequencies, "total")  # Fallback

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    scenario = data["scenario"]
    
    # Display context
    st.markdown(f"### {scenario['context']}")
    
    # Display frequency table
    display_frequency_table(scenario, data["frequencies"])
    
    # Display question
    st.markdown("---")
    st.markdown(f"### {st.session_state.current_problem}")
    
    # Display answer interface based on type
    if data["answer_type"] == "number":
        display_number_input()
    elif data["answer_type"] == "money":
        display_money_input()
    elif data["answer_type"] == "multiple_choice":
        display_multiple_choice(data["options"])
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Work it out", type="secondary", use_container_width=True):
                show_solution()
            
            if st.button("Next Question →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def display_frequency_table(scenario, frequencies):
    """Display the frequency table with appropriate styling"""
    import pandas as pd
    
    # Create table title
    st.markdown(f"#### {scenario['title']}")
    
    # Prepare data for dataframe
    table_data = []
    for item, frequency in frequencies.items():
        table_data.append({
            scenario["item_label"]: item,
            scenario["frequency_label"]: frequency
        })
    
    df = pd.DataFrame(table_data)
    
    # Apply custom styling using pandas styler
    def style_table(styler):
        styler.set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border': '1px solid #ddd'
        })
        styler.set_table_styles([
            {'selector': 'thead tr th',
             'props': f'background-color: {scenario["color"]}; color: white; font-weight: bold;'}
        ])
        return styler
    
    # Display the styled dataframe
    st.dataframe(
        df.style.pipe(style_table),
        use_container_width=False,
        hide_index=True
    )

def display_number_input():
    """Display number input field"""
    data = st.session_state.problem_data
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        user_answer = st.number_input(
            "Your answer:",
            min_value=0,
            step=1,
            key="number_answer",
            disabled=st.session_state.answer_submitted
        )
        
        # Add unit label if needed
        if data.get("unit"):
            st.caption(data["unit"])
    
    with col2:
        if not st.session_state.answer_submitted:
            if st.button("Submit", type="primary", use_container_width=True):
                st.session_state.user_answer = user_answer
                check_answer()

def display_money_input():
    """Display money input field with $ symbol"""
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Create a container for $ symbol and input
        subcol1, subcol2 = st.columns([1, 10])
        with subcol1:
            st.markdown("### $")
        with subcol2:
            user_answer = st.number_input(
                "Amount:",
                min_value=0,
                step=1,
                label_visibility="collapsed",
                key="money_answer",
                disabled=st.session_state.answer_submitted
            )
    
    with col2:
        if not st.session_state.answer_submitted:
            if st.button("Submit", type="primary", use_container_width=True):
                st.session_state.user_answer = user_answer
                check_answer()

def display_multiple_choice(options):
    """Display multiple choice options as clickable tiles"""
    # Determine layout based on number of options
    if len(options) <= 4:
        cols = st.columns(len(options))
        show_in_row = True
    else:
        # For more options, use 2 rows
        cols_per_row = (len(options) + 1) // 2
        show_in_row = False
    
    # If party activities scenario, use 2x2 grid
    if "party" in st.session_state.current_problem.lower() or len(options) == 4:
        col1, col2 = st.columns(2)
        with col1:
            for i in range(0, min(2, len(options))):
                if st.button(
                    options[i],
                    key=f"option_{i}",
                    use_container_width=True,
                    disabled=st.session_state.answer_submitted
                ):
                    st.session_state.user_answer = options[i]
                    check_answer()
        
        with col2:
            for i in range(2, min(4, len(options))):
                if st.button(
                    options[i],
                    key=f"option_{i}",
                    use_container_width=True,
                    disabled=st.session_state.answer_submitted
                ):
                    st.session_state.user_answer = options[i]
                    check_answer()
    else:
        # Regular layout
        if show_in_row:
            for i, col in enumerate(cols):
                with col:
                    if st.button(
                        options[i],
                        key=f"option_{i}",
                        use_container_width=True,
                        disabled=st.session_state.answer_submitted
                    ):
                        st.session_state.user_answer = options[i]
                        check_answer()
        else:
            # Two rows
            cols1 = st.columns(cols_per_row)
            for i in range(min(cols_per_row, len(options))):
                with cols1[i]:
                    if st.button(
                        options[i],
                        key=f"option_{i}",
                        use_container_width=True,
                        disabled=st.session_state.answer_submitted
                    ):
                        st.session_state.user_answer = options[i]
                        check_answer()
            
            if len(options) > cols_per_row:
                cols2 = st.columns(len(options) - cols_per_row)
                for i in range(cols_per_row, len(options)):
                    with cols2[i - cols_per_row]:
                        if st.button(
                            options[i],
                            key=f"option_{i}",
                            use_container_width=True,
                            disabled=st.session_state.answer_submitted
                        ):
                            st.session_state.user_answer = options[i]
                            check_answer()

def check_answer():
    """Check if the user's answer is correct"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    st.session_state.answer_correct = (user_answer == correct_answer)
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
            old_difficulty = st.session_state.interpret_freq_difficulty
            st.session_state.interpret_freq_difficulty = min(
                st.session_state.interpret_freq_difficulty + 1, 4
            )
            
            if st.session_state.interpret_freq_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.interpret_freq_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        correct = st.session_state.correct_answer
        answer_type = st.session_state.problem_data["answer_type"]
        
        if answer_type == "money":
            st.error(f"❌ **Not quite. The correct answer is ${correct}**")
        elif answer_type == "multiple_choice":
            st.error(f"❌ **Not quite. The correct answer is {correct}**")
        else:
            unit = st.session_state.problem_data.get("unit", "")
            st.error(f"❌ **Not quite. The correct answer is {correct} {unit}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.interpret_freq_difficulty
            st.session_state.interpret_freq_difficulty = max(
                st.session_state.interpret_freq_difficulty - 1, 1
            )
            
            if st.session_state.interpret_freq_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.interpret_freq_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show step-by-step solution"""
    with st.expander("📝 **Step-by-step solution**", expanded=True):
        data = st.session_state.problem_data
        question_type = st.session_state.question_type
        frequencies = data["frequencies"]
        
        st.markdown("### How to solve this one-step problem:")
        
        if question_type == "total":
            st.markdown("**Step 1: Add all the frequencies**")
            freq_list = [f"{item}: {freq}" for item, freq in frequencies.items()]
            st.markdown("- " + "\n- ".join(freq_list))
            
            calculation = " + ".join(str(freq) for freq in frequencies.values())
            total = sum(frequencies.values())
            st.markdown(f"\n**Calculation:** {calculation} = {total}")
            st.success(f"**Answer: {total} {data['unit']}**")
            
        elif question_type == "specific_value":
            st.markdown("**Step 1: Find the row in the table**")
            st.markdown("**Step 2: Read the frequency for that item**")
            st.success(f"**Answer: {st.session_state.correct_answer} {data['unit']}**")
            
        elif question_type == "comparison":
            st.markdown("**Step 1: Find the frequencies for both items**")
            st.markdown("**Step 2: Subtract the smaller from the larger**")
            st.success(f"**Answer: {st.session_state.correct_answer} {data['unit']}**")
            
        elif question_type in ["most_popular_mc", "least_popular_mc"]:
            st.markdown("**Step 1: Look at all the frequencies**")
            freq_display = [f"- {item}: {freq}" for item, freq in frequencies.items()]
            st.markdown("\n".join(freq_display))
            
            if question_type == "most_popular_mc":
                st.markdown("**Step 2: Find the highest number**")
                max_freq = max(frequencies.values())
                st.markdown(f"The highest frequency is {max_freq}")
            else:
                st.markdown("**Step 2: Find the lowest number**")
                min_freq = min(frequencies.values())
                st.markdown(f"The lowest frequency is {min_freq}")
            
            st.success(f"**Answer: {st.session_state.correct_answer}**")
            
        elif question_type == "money_calculation":
            scenario = data["scenario"]
            price = scenario["price"]
            quantity = frequencies[scenario["price_item"]]
            
            st.markdown(f"**Step 1: Find the quantity**")
            st.markdown(f"{scenario['price_item']}: {quantity}")
            
            st.markdown(f"**Step 2: Multiply by the price**")
            st.markdown(f"{quantity} × ${price} = ${quantity * price}")
            
            st.success(f"**Answer: ${st.session_state.correct_answer}**")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    st.session_state.question_type = None
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct