import streamlit as st
import random
import pandas as pd

def run():
    """
    Main function to run the Read a Table activity.
    Interactive table reading with progressive difficulty.
    """
    # Initialize session state
    if "table_difficulty" not in st.session_state:
        st.session_state.table_difficulty = 1
        st.session_state.table_consecutive_correct = 0
        st.session_state.table_consecutive_wrong = 0
        st.session_state.table_total_score = 0
        st.session_state.table_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.selected_answer = None
        st.session_state.user_input = ""
    
    if "current_table_problem" not in st.session_state:
        generate_table_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📊 Read a Table")
    st.markdown("*Extract and analyze information from data tables*")
    st.markdown("---")
    
    # Display progress
    display_table_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_table_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_table_problem()
    
    # Instructions
    with st.expander("💡 **How to Read Tables**", expanded=False):
        st.markdown("""
        ### Table Reading Tips:
        1. **Read the title** - Understand what the table shows
        2. **Check headers** - Row and column labels tell you what data means
        3. **Find intersections** - Look where rows and columns meet
        4. **Compare values** - Use subtraction for "how many more" questions
        
        ### Question Types:
        - **Direct reading**: Find a specific value
        - **Comparison**: Which is more/less/most/least
        - **Difference**: How many more/fewer
        - **Total/Sum**: Add values together
        - **Time changes**: Compare across years
        
        ### Difficulty Levels:
        - **Level 1**: Simple 2-3 row tables, direct reading
        - **Level 2**: 3-4 row tables, basic comparisons
        - **Level 3**: Larger tables, find differences
        - **Level 4**: Multi-column tables, time comparisons
        - **Level 5**: Complex tables, multiple calculations
        - **Level 6**: Advanced analysis, patterns
        """)

def get_table_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.table_difficulty
    
    settings = {
        1: {
            "rows": random.randint(2, 3),
            "columns": 2,
            "question_types": ["direct", "simple_compare"],
            "number_range": (1, 20),
            "label": "Simple Tables",
            "color": "🟢"
        },
        2: {
            "rows": random.randint(3, 4),
            "columns": 2,
            "question_types": ["direct", "compare", "which_most"],
            "number_range": (5, 30),
            "label": "Basic Comparison",
            "color": "🟡"
        },
        3: {
            "rows": random.randint(3, 5),
            "columns": random.choice([2, 3]),
            "question_types": ["difference", "compare", "which_least"],
            "number_range": (10, 50),
            "label": "Find Differences",
            "color": "🟠"
        },
        4: {
            "rows": random.randint(3, 4),
            "columns": 3,  # Time-based columns
            "question_types": ["time_compare", "difference", "which_most_year"],
            "number_range": (5, 100),
            "label": "Time Analysis",
            "color": "🔴"
        },
        5: {
            "rows": random.randint(4, 6),
            "columns": random.choice([2, 3]),
            "question_types": ["sum", "difference", "complex_compare"],
            "number_range": (10, 200),
            "label": "Complex Analysis",
            "color": "🟣"
        },
        6: {
            "rows": random.randint(5, 7),
            "columns": random.choice([3, 4]),
            "question_types": ["pattern", "multi_step", "complex_compare"],
            "number_range": (20, 500),
            "label": "Advanced Tables",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_table_progress():
    """Display current level and progress"""
    settings = get_table_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.table_difficulty}/6")
    
    with col2:
        st.metric("Table Type", settings['label'])
    
    with col3:
        if st.session_state.table_total_attempts > 0:
            accuracy = (st.session_state.table_total_score / st.session_state.table_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.table_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.table_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Data Master")

def generate_table_data(settings):
    """Generate table data based on difficulty settings"""
    table_themes = [
        {
            "title": "Birds in local lakes",
            "row_header": "Lake",
            "row_names": ["Mirror Lake", "Blue Lake", "Canyon Lake", "Long Lake", "Spring Lake", "Crystal Lake", "Green Lake"],
            "column_names": ["Geese", "Swans", "Ducks", "Herons"],
            "context": "A biologist recorded the number of birds at lakes"
        },
        {
            "title": "School play committees",
            "row_header": "Committee",
            "row_names": ["Casting", "Lighting", "Sound", "Costumes", "Props", "Marketing", "Stage"],
            "column_names": ["Girls", "Boys", "Total", "Adults"],
            "context": "Students signed up to help with the school play"
        },
        {
            "title": "Farm building repairs",
            "row_header": "Building",
            "row_names": ["Barn", "Greenhouse", "Hen house", "Stable", "Shed", "Silo", "Workshop"],
            "column_names": ["Working lights", "Broken lights", "Total lights", "Windows"],
            "context": "A farmer examined each building on his farm"
        },
        {
            "title": "Sports day results",
            "row_header": "Team",
            "row_names": ["Red Team", "Blue Team", "Green Team", "Yellow Team", "Purple Team", "Orange Team"],
            "column_names": ["Gold medals", "Silver medals", "Bronze medals", "Total medals"],
            "context": "Results from the annual sports day competition"
        },
        {
            "title": "Library book loans",
            "row_header": "Genre",
            "row_names": ["Fiction", "Science", "History", "Sports", "Art", "Comics", "Mystery"],
            "column_names": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "context": "The librarian tracked book loans by genre"
        },
        {
            "title": "Carnival game results",
            "row_header": "Person",
            "row_names": ["Uncle Ryan", "Aunt Betty", "Aunt Lisa", "Uncle William", "Cousin Sam", "Grandpa Joe"],
            "column_names": ["Hits", "Misses", "Prizes won", "Tickets used"],
            "context": "At the summer carnival, each family member played games"
        }
    ]
    
    # For time-based tables (difficulty 4+)
    time_themes = [
        {
            "title": "Cheese consumption per capita (kg)",
            "row_header": "Country",
            "row_names": ["Germany", "Australia", "Canada", "Argentina", "France", "Italy", "Greece"],
            "column_names": ["1996", "2006", "2016"],
            "context": "An agricultural agency researched cheese consumption"
        },
        {
            "title": "Nobel Prize winners",
            "row_header": "Country",
            "row_names": ["Russia", "Germany", "Japan", "USA", "UK", "France", "Sweden"],
            "column_names": ["1970s", "1980s", "1990s", "2000s"],
            "context": "Chase looked at Nobel Prizes by decade"
        },
        {
            "title": "Chocolate consumption per capita (kg)",
            "row_header": "Country",
            "row_names": ["Denmark", "Belgium", "Switzerland", "Netherlands", "Austria", "Finland"],
            "column_names": ["2002", "2005", "2008"],
            "context": "Warren's Candies studied chocolate consumption"
        }
    ]
    
    # Choose theme based on difficulty
    if settings["columns"] >= 3 and st.session_state.table_difficulty >= 4:
        theme = random.choice(time_themes)
    else:
        theme = random.choice(table_themes)
    
    # Select rows and columns
    selected_rows = random.sample(theme["row_names"], settings["rows"])
    selected_columns = theme["column_names"][:settings["columns"]]
    
    # Generate data
    data = {}
    for col in selected_columns:
        data[col] = []
        for row in selected_rows:
            # Generate numbers based on difficulty
            min_val, max_val = settings["number_range"]
            value = random.randint(min_val, max_val)
            data[col].append(value)
    
    # Create DataFrame
    df = pd.DataFrame(data, index=selected_rows)
    
    return df, theme

def generate_question(df, theme, settings):
    """Generate a question based on the table data"""
    question_type = random.choice(settings["question_types"])
    
    if question_type == "direct":
        # Direct reading question
        row = random.choice(df.index.tolist())
        col = random.choice(df.columns.tolist())
        value = df.loc[row, col]
        
        question = f"How many {col.lower()} are there in {row}?"
        correct_answer = str(value)
        answer_type = "number"
        options = None
        
    elif question_type == "simple_compare":
        # Simple comparison
        col = random.choice(df.columns.tolist())
        values = df[col].tolist()
        max_idx = values.index(max(values))
        
        question = f"Which has the most {col.lower()}?"
        correct_answer = df.index[max_idx]
        answer_type = "choice"
        options = df.index.tolist()
        
    elif question_type == "compare" or question_type == "which_most":
        # Which has most/least
        col = random.choice(df.columns.tolist())
        if question_type == "which_most" or random.random() < 0.5:
            idx = df[col].idxmax()
            question = f"Which {theme['row_header'].lower()} has the most {col.lower()}?"
        else:
            idx = df[col].idxmin()
            question = f"Which {theme['row_header'].lower()} has the least {col.lower()}?"
        
        correct_answer = idx
        answer_type = "choice"
        options = df.index.tolist()
        
    elif question_type == "which_least":
        # Which has least
        col = random.choice(df.columns.tolist())
        idx = df[col].idxmin()
        question = f"Which {theme['row_header'].lower()} has the fewest {col.lower()}?"
        correct_answer = idx
        answer_type = "choice"
        options = df.index.tolist()
        
    elif question_type == "difference":
        # How many more/fewer
        col = random.choice(df.columns.tolist())
        rows = random.sample(df.index.tolist(), 2)
        val1 = df.loc[rows[0], col]
        val2 = df.loc[rows[1], col]
        
        if val1 > val2:
            diff = val1 - val2
            question = f"How many more {col.lower()} does {rows[0]} have than {rows[1]}?"
        else:
            diff = val2 - val1
            question = f"How many more {col.lower()} does {rows[1]} have than {rows[0]}?"
        
        correct_answer = str(diff)
        answer_type = "number"
        options = None
        
    elif question_type == "time_compare":
        # Compare across time
        if len(df.columns) >= 2:
            row = random.choice(df.index.tolist())
            cols = df.columns.tolist()
            
            if df.loc[row, cols[-1]] > df.loc[row, cols[0]]:
                question = f"Did {row} consume more {theme['title'].split()[0].lower()} in {cols[-1]} or {cols[0]}?"
                correct_answer = cols[-1]
            else:
                question = f"Did {row} consume more {theme['title'].split()[0].lower()} in {cols[0]} or {cols[-1]}?"
                correct_answer = cols[0]
            
            answer_type = "choice"
            options = [cols[0], cols[-1]]
        else:
            # Fallback to simple compare
            return generate_question(df, theme, {"question_types": ["simple_compare"]})
    
    elif question_type == "which_most_year":
        # Which country had most in specific year
        col = random.choice(df.columns.tolist())
        idx = df[col].idxmax()
        
        question = f"Which country consumed the most {theme['title'].split()[0].lower()} per capita in {col}?"
        correct_answer = idx
        answer_type = "choice"
        options = df.index.tolist()
        
    elif question_type == "sum":
        # Calculate sum
        row = random.choice(df.index.tolist())
        if len(df.columns) >= 2:
            cols = random.sample(df.columns.tolist(), 2)
            total = sum(df.loc[row, col] for col in cols)
            question = f"What is the total {cols[0].lower()} and {cols[1].lower()} for {row}?"
        else:
            # Sum all for one row
            total = df.loc[row].sum()
            question = f"What is the total for {row}?"
        
        correct_answer = str(total)
        answer_type = "number"
        options = None
        
    else:  # complex_compare, pattern, multi_step
        # Complex comparison
        if len(df.columns) >= 2:
            col1, col2 = random.sample(df.columns.tolist(), 2)
            row = random.choice(df.index.tolist())
            total = df.loc[row, col1] + df.loc[row, col2]
            
            question = f"How many total {col1.lower()} and {col2.lower()} are there in {row}?"
            correct_answer = str(total)
            answer_type = "number"
            options = None
        else:
            # Fallback to difference
            return generate_question(df, theme, {"question_types": ["difference"]})
    
    # Add context to question
    full_question = f"{theme['context']}.\n\n{question}"
    
    return {
        "question": full_question,
        "correct_answer": correct_answer,
        "answer_type": answer_type,
        "options": options,
        "unit": col.lower() if answer_type == "number" else None
    }

def generate_table_problem():
    """Generate a new table reading problem"""
    settings = get_table_difficulty_settings()
    
    # Generate table data
    df, theme = generate_table_data(settings)
    
    # Generate question
    question_data = generate_question(df, theme, settings)
    
    problem_data = {
        "settings": settings,
        "table": df,
        "theme": theme,
        "question": question_data["question"],
        "correct_answer": question_data["correct_answer"],
        "answer_type": question_data["answer_type"],
        "options": question_data["options"],
        "unit": question_data["unit"]
    }
    
    st.session_state.current_table_problem = problem_data
    st.session_state.show_result = False
    st.session_state.selected_answer = None
    st.session_state.user_input = ""

def display_table_problem():
    """Display the table and question interface"""
    problem = st.session_state.current_table_problem
    
    # Display context and question
    st.markdown(f"### {problem['question']}")
    
    # Display the table
    display_data_table(problem)
    
    # Answer interface
    st.markdown("---")
    
    if problem["answer_type"] == "choice":
        # Multiple choice buttons
        st.markdown("### Select your answer:")
        
        # Create button grid
        cols = st.columns(min(len(problem["options"]), 4))
        
        if not st.session_state.show_result:
            for i, option in enumerate(problem["options"]):
                with cols[i % len(cols)]:
                    if st.button(
                        option,
                        key=f"option_{i}",
                        use_container_width=True,
                        type="primary" if st.session_state.selected_answer == option else "secondary"
                    ):
                        st.session_state.selected_answer = option
                        st.rerun()
            
            # Submit button
            if st.button("Submit", type="primary", disabled=st.session_state.selected_answer is None):
                check_table_answer()
                st.rerun()
        else:
            # Show results
            for i, option in enumerate(problem["options"]):
                with cols[i % len(cols)]:
                    if option == st.session_state.selected_answer:
                        if option == problem["correct_answer"]:
                            st.success(f"✅ {option}")
                        else:
                            st.error(f"❌ {option}")
                    elif option == problem["correct_answer"]:
                        st.info(f"✓ {option}")
                    else:
                        st.caption(option)
    
    else:  # number input
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if not st.session_state.show_result:
                user_input = st.text_input(
                    f"Enter your answer ({problem['unit'] if problem['unit'] else 'number'}):",
                    value=st.session_state.user_input,
                    key="number_input"
                )
                st.session_state.user_input = user_input
                
                if st.button("Submit", type="primary", use_container_width=True):
                    if user_input:
                        try:
                            int(user_input)
                            st.session_state.selected_answer = user_input
                            check_table_answer()
                            st.rerun()
                        except ValueError:
                            st.error("Please enter a valid number")
                    else:
                        st.error("Please enter an answer")
            else:
                # Show result
                st.markdown("Your answer:")
                if st.session_state.selected_answer == problem["correct_answer"]:
                    st.success(f"✅ {st.session_state.selected_answer} {problem['unit'] if problem['unit'] else ''}")
                else:
                    st.error(f"❌ {st.session_state.selected_answer} {problem['unit'] if problem['unit'] else ''}")
                    st.info(f"✓ Correct: {problem['correct_answer']} {problem['unit'] if problem['unit'] else ''}")
    
    # Show feedback
    if st.session_state.show_result:
        display_table_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                generate_table_problem()
                st.rerun()

def display_data_table(problem):
    """Display the data table with styling"""
    df = problem['table']
    theme = problem['theme']
    
    # Create a styled version of the dataframe
    styled_df = df.style.set_properties(**{
        'text-align': 'center',
        'font-size': '16px',
        'border': '1px solid black'
    })
    
    # Add header styling
    styled_df = styled_df.set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#e8f4fd' if st.session_state.table_difficulty <= 3 else '#e8e8ff'),
            ('color', 'black'),
            ('font-weight', 'bold'),
            ('text-align', 'center'),
            ('font-size', '16px')
        ]},
        {'selector': 'td', 'props': [
            ('text-align', 'center'),
            ('padding', '10px')
        ]}
    ])
    
    # Highlight relevant cells if showing result
    if st.session_state.show_result and problem["answer_type"] == "number":
        # Highlight cells used in calculation
        # This would require more complex logic to track which cells were used
        pass
    
    # Display table title
    st.markdown(f"#### {theme['title']}")
    
    # Display the table
    st.dataframe(df, use_container_width=False)

def check_table_answer():
    """Check if the submitted answer is correct"""
    problem = st.session_state.current_table_problem
    selected = st.session_state.selected_answer
    correct = problem['correct_answer']
    
    # Update statistics
    st.session_state.table_total_attempts += 1
    
    if str(selected) == str(correct):
        st.session_state.table_total_score += 1
        st.session_state.table_consecutive_correct += 1
        st.session_state.table_consecutive_wrong = 0
        st.session_state.current_table_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.table_consecutive_correct >= 3 and 
            st.session_state.table_difficulty < 6):
            st.session_state.table_difficulty += 1
            st.session_state.table_consecutive_correct = 0
    else:
        st.session_state.table_consecutive_wrong += 1
        st.session_state.table_consecutive_correct = 0
        st.session_state.current_table_problem["result"] = "incorrect"
        
        # Check for level down
        if (st.session_state.table_consecutive_wrong >= 3 and 
            st.session_state.table_difficulty > 1):
            st.session_state.table_difficulty -= 1
            st.session_state.table_consecutive_wrong = 0
    
    st.session_state.show_result = True

def display_table_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_table_problem
    
    if problem.get("result") == "correct":
        st.success("✅ Excellent! You read the table correctly!")
        
        if st.session_state.table_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Great data reading! {st.session_state.table_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.table_consecutive_correct == 0:  # Just leveled up
            st.success(f"🎉 Level Up! Now working with: {get_table_difficulty_settings()['label']}!")
    else:
        st.error("❌ Not quite right. Check the table again.")
        
        # Provide explanation
        with st.expander("📊 See how to find the answer"):
            problem = st.session_state.current_table_problem
            
            if problem["answer_type"] == "number":
                st.markdown("**How to find this answer:**")
                
                # Provide specific guidance based on question type
                if "more" in problem["question"].lower():
                    st.markdown("1. Find the first value in the table")
                    st.markdown("2. Find the second value in the table")
                    st.markdown("3. Subtract the smaller from the larger")
                    st.markdown(f"4. The answer is: **{problem['correct_answer']}**")
                elif "total" in problem["question"].lower():
                    st.markdown("1. Find all relevant values in the table")
                    st.markdown("2. Add them together")
                    st.markdown(f"3. The answer is: **{problem['correct_answer']}**")
                else:
                    st.markdown("1. Find the row in the table")
                    st.markdown("2. Find the column in the table")
                    st.markdown("3. Look where they meet")
                    st.markdown(f"4. The answer is: **{problem['correct_answer']}**")
            else:
                st.markdown("**How to find this answer:**")
                st.markdown("1. Look at the relevant column")
                st.markdown("2. Compare all values")
                st.markdown("3. Find the highest/lowest as asked")
                st.markdown(f"4. The answer is: **{problem['correct_answer']}**")
            
            st.info("""
            Remember:
            - Read row and column headers carefully
            - Make sure you're looking at the right data
            - Double-check your calculations
            """)
        
        # Level down message
        if st.session_state.table_consecutive_wrong == 0:  # Just leveled down
            st.warning(f"📉 Moving to easier tables: {get_table_difficulty_settings()['label']}")

def clear_table_state():
    """Clear all table-related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('table_') or key in ['current_table_problem', 'show_result', 'selected_answer', 'user_input']:
            del st.session_state[key]