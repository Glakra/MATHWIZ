import streamlit as st
import random

def run():
    """
    Main function to run the Create Dot Plots activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/Q. Data and graphs/create_dot_plots.py
    """
    # Initialize session state
    if "create_plot_difficulty" not in st.session_state:
        st.session_state.create_plot_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_plot = {}
        st.session_state.user_plot = {}
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.plot_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > Q. Data and graphs**")
    st.title("📈 Create Dot Plots")
    st.markdown("*Use the data to complete the dot plot below*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.create_plot_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Tables",
            2: "Mixed Format",
            3: "Raw Data Lists",
            4: "Complex Data"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Simple Tables')}")
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
        ### How to Create Dot Plots:
        - **Click the gray boxes (⬜)** to add X marks
        - **Click on X marks (❌)** to remove them
        - **Click the numbers below** to clear entire columns
        - **Each X represents one data point**
        
        ### Reading the Data:
        - **Tables:** Look at the frequency column for how many X's to place
        - **Raw lists:** Count how many times each number appears
        
        ### Tips for Success:
        - **Count carefully** - especially with raw data lists
        - **Check your totals** match the original data
        - **Use the counter button** to verify your total
        
        ### Example:
        If the table shows "3 students have 2 pets", place 3 X's above the number 2.
        """)

def generate_new_problem():
    """Generate a new dot plot creation problem"""
    difficulty = st.session_state.create_plot_difficulty
    
    # Enhanced scenarios with richer contexts
    scenarios = [
        {
            "title": "American Football touchdowns scored last season",
            "context": "Coach Johnson tracked his team's performance last season. He recorded how many touchdowns each player scored throughout the year.",
            "instruction": "Use the data in the table to complete the dot plot below.",
            "x_label": "Touchdowns scored",
            "unit": "players",
            "button_label": "Number of players",
            "color": "green",
            "data_type": "touchdowns"
        },
        {
            "title": "Pets",
            "context": "Mrs. Garcia's class is learning about data collection. Each student counted their pets at home, including dogs, cats, fish, birds, and other animals.",
            "instruction": "Use the data to complete the dot plot below.",
            "x_label": "Number of pets",
            "unit": "students",
            "button_label": "Number of students",
            "color": "blue",
            "data_type": "pets"
        },
        {
            "title": "Making picture frames",
            "context": "In Mr. Thompson's woodworking class, students made decorative picture frames for Mother's Day. He recorded how many frames each student completed.",
            "instruction": "Use the data to complete the dot plot below.",
            "x_label": "Picture frames made",
            "unit": "students",
            "button_label": "Number of students",
            "color": "green",
            "data_type": "frames"
        },
        {
            "title": "Writing poems",
            "context": "The school held a poetry contest for National Poetry Month. Students could submit as many original poems as they wanted.",
            "instruction": "Use the data to complete the dot plot below.",
            "x_label": "Poems written",
            "unit": "students",
            "button_label": "Number of students",
            "color": "blue",
            "data_type": "poems"
        },
        {
            "title": "Playing soccer last week",
            "context": "Coach Martinez surveyed her youth soccer team about their practice habits. She asked each player how many times they played soccer outside of team practice last week.",
            "instruction": "Use the data in the table to complete the dot plot below.",
            "x_label": "Times played",
            "unit": "people",
            "button_label": "Number of people",
            "color": "green",
            "data_type": "soccer"
        },
        {
            "title": "Going down the slide at recess",
            "context": "During recess observation, Ms. Lee noticed the slide was very popular. She counted how many times each student went down the slide during one recess period.",
            "instruction": "Use the data to complete the dot plot below.",
            "x_label": "Number of times",
            "unit": "students",
            "button_label": "Number of students",
            "color": "orange",
            "data_type": "slide"
        },
        {
            "title": "Eating macaroni and cheese last month",
            "context": "A pasta company surveyed families about their eating habits. They asked people to recall how many times they ate macaroni and cheese in the past month.",
            "instruction": "Use the data in the table to complete the dot plot below.",
            "x_label": "Times eaten",
            "unit": "people",
            "button_label": "Number of people",
            "color": "orange",
            "data_type": "macaroni"
        },
        {
            "title": "Scores on a board game",
            "context": "Timothy hosted a game night with his friends. They played multiple rounds of their favorite board game and recorded everyone's final scores.",
            "instruction": "Use the data in the table to complete the dot plot below.",
            "x_label": "Score",
            "unit": "people",
            "button_label": "Number of people",
            "color": "purple",
            "data_type": "scores"
        },
        {
            "title": "Books read during summer vacation",
            "context": "The library's summer reading challenge just ended. Librarian Ms. Chen recorded how many books each participant completed over the summer break.",
            "instruction": "Use the data to complete the dot plot below.",
            "x_label": "Books read",
            "unit": "participants",
            "button_label": "Number of participants",
            "color": "red",
            "data_type": "books"
        },
        {
            "title": "Goals scored this season",
            "context": "The hockey team finished their season yesterday. Coach Davis tallied up the total goals scored by each player throughout all their games.",
            "instruction": "Use the data in the table to complete the dot plot below.",
            "x_label": "Goals scored",
            "unit": "players",
            "button_label": "Number of players",
            "color": "blue",
            "data_type": "goals"
        }
    ]
    
    # Choose a random scenario
    scenario = random.choice(scenarios)
    
    # Generate data based on difficulty
    if difficulty == 1:
        # Simple table format, small range
        data_format = "table"
        num_values = random.randint(4, 5)
        max_frequency = random.randint(3, 6)
        start_value = random.randint(0, 2)
    elif difficulty == 2:
        # Mixed format, medium range
        data_format = random.choice(["table", "list"])
        num_values = random.randint(5, 6)
        max_frequency = random.randint(4, 8)
        start_value = random.randint(0, 1)
    elif difficulty == 3:
        # Mostly raw lists, larger range
        data_format = "list"
        num_values = random.randint(5, 7)
        max_frequency = random.randint(5, 10)
        start_value = 0
    else:
        # Complex data, largest range
        data_format = random.choice(["table", "list"])
        num_values = random.randint(6, 8)
        max_frequency = random.randint(6, 12)
        start_value = random.randint(0, 5)
    
    # Generate the frequency data
    frequency_data = {}
    for i in range(num_values):
        value = start_value + i
        if random.random() < 0.15:  # 15% chance of zero frequency
            frequency = 0
        else:
            frequency = random.randint(1, max_frequency)
        frequency_data[value] = frequency
    
    # Create the data representation
    if data_format == "table":
        table_data = []
        for value, freq in sorted(frequency_data.items()):
            table_data.append({"value": value, "frequency": freq})
        data_representation = {"format": "table", "data": table_data}
    else:
        # Create raw list
        raw_list = []
        for value, freq in frequency_data.items():
            raw_list.extend([value] * freq)
        random.shuffle(raw_list)
        data_representation = {"format": "list", "data": raw_list}
    
    # Store problem data
    st.session_state.problem_data = {
        "scenario": scenario,
        "data_representation": data_representation,
        "frequency_data": frequency_data,
        "min_value": min(frequency_data.keys()),
        "max_value": max(frequency_data.keys())
    }
    st.session_state.correct_plot = frequency_data
    st.session_state.user_plot = {k: 0 for k in range(
        st.session_state.problem_data["min_value"],
        st.session_state.problem_data["max_value"] + 1
    )}
    st.session_state.current_problem = scenario["instruction"]

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    scenario = data["scenario"]
    
    # Display enhanced context
    st.markdown(f"### 📊 {scenario['context']}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Display the data
    display_data(data["data_representation"], scenario)
    
    # Interactive instruction
    st.markdown("---")
    st.info("**Click to select the X's. To clear a column, click on the number line below it.**")
    
    # Create the interactive plot
    create_interactive_plot(scenario)
    
    # Submit and counter buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.plot_submitted:
            if st.button("Submit", type="primary", use_container_width=True):
                check_answer()
    
    with col2:
        # Dynamic button label based on scenario
        button_label = scenario.get("button_label", "Number of items")
        if st.button(button_label, type="secondary", use_container_width=True):
            total = sum(st.session_state.user_plot.values())
            st.info(f"Total {scenario['unit']} in your plot: **{total}**")
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.plot_submitted:
        if st.button("🔄 Next Question", type="secondary", use_container_width=True):
            reset_problem_state()
            st.rerun()

def display_data(data_representation, scenario):
    """Display the data in table or list format"""
    if data_representation["format"] == "table":
        # Display as table
        st.markdown(f"#### {scenario['title']}")
        
        # Create a simple table using columns
        import pandas as pd
        df = pd.DataFrame(data_representation["data"])
        df.columns = [scenario['x_label'], f"Number of {scenario['unit']}"]
        
        # Style the dataframe with color based on scenario
        def style_header(df):
            return df.style.set_table_styles([
                {'selector': 'thead tr th',
                 'props': f'background-color: {scenario["color"]}; color: white;'}
            ])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        # Display as raw list
        st.markdown(f"#### {scenario['title']}")
        raw_data = data_representation["data"]
        
        # Display in a colored container with better formatting
        data_str = "  ".join(str(x) for x in raw_data)
        
        # Create a more visually appealing display
        st.markdown(f"**{scenario['unit'].capitalize()} data:**")
        st.info(data_str)
        st.caption(f"Count how many times each number appears in the list above.")

def create_interactive_plot(scenario):
    """Create an interactive dot plot grid where users can click to add X's"""
    data = st.session_state.problem_data
    min_val = data["min_value"]
    max_val = data["max_value"]
    
    # Create title for the plot
    st.markdown(f"#### {scenario['title']}")
    
    # Create a container for the plot with background
    with st.container():
        # Calculate grid dimensions
        num_columns = max_val - min_val + 1
        max_height = 10  # Maximum rows for X's
        
        # Create the plot grid
        for row in range(max_height, 0, -1):
            cols = st.columns(num_columns)
            for i, x_val in enumerate(range(min_val, max_val + 1)):
                with cols[i]:
                    current_count = st.session_state.user_plot.get(x_val, 0)
                    
                    if row <= current_count:
                        # Show X mark - clicking removes it
                        if st.button(
                            "❌",
                            key=f"x_{x_val}_{row}",
                            help=f"Click to remove",
                            use_container_width=True
                        ):
                            st.session_state.user_plot[x_val] = current_count - 1
                            st.rerun()
                    elif row == current_count + 1:
                        # Next available spot - show as clickable gray box
                        if st.button(
                            "⬜",
                            key=f"empty_{x_val}_{row}",
                            help=f"Click to add X",
                            use_container_width=True
                        ):
                            st.session_state.user_plot[x_val] = current_count + 1
                            st.rerun()
                    else:
                        # Empty space - use markdown for consistent height
                        st.markdown("&nbsp;", unsafe_allow_html=True)
        
        # Axis line
        st.markdown("---")
        
        # Axis labels (click to clear column)
        cols = st.columns(num_columns)
        for i, x_val in enumerate(range(min_val, max_val + 1)):
            with cols[i]:
                if st.button(
                    str(x_val),
                    key=f"axis_{x_val}",
                    help=f"Click to clear column",
                    use_container_width=True
                ):
                    st.session_state.user_plot[x_val] = 0
                    st.rerun()
        
        # X-axis label
        st.markdown(f"**{scenario['x_label']}**")

def check_answer():
    """Check if the user's plot matches the correct plot"""
    correct = st.session_state.correct_plot
    user = st.session_state.user_plot
    
    # Check if all values match
    all_correct = True
    for value in range(st.session_state.problem_data["min_value"], 
                      st.session_state.problem_data["max_value"] + 1):
        if correct.get(value, 0) != user.get(value, 0):
            all_correct = False
            break
    
    st.session_state.answer_correct = all_correct
    st.session_state.show_feedback = True
    st.session_state.plot_submitted = True

def show_feedback():
    """Display feedback for the submitted plot"""
    if st.session_state.answer_correct:
        st.success("🎉 **Correct! Well done!**")
        
        # Update consecutive counters
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.create_plot_difficulty
            st.session_state.create_plot_difficulty = min(
                st.session_state.create_plot_difficulty + 1, 4
            )
            
            if st.session_state.create_plot_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Great job! Moving to Level {st.session_state.create_plot_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error("❌ **Not quite right. Check your dot plot against the data.**")
        
        # Update consecutive counters
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive wrong
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.create_plot_difficulty
            st.session_state.create_plot_difficulty = max(
                st.session_state.create_plot_difficulty - 1, 1
            )
            
            if st.session_state.create_plot_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.create_plot_difficulty}**")
                st.session_state.consecutive_wrong = 0
        
        # Show the correct answer
        show_correct_plot()

def show_correct_plot():
    """Show the correct dot plot"""
    with st.expander("📊 **See the solution**", expanded=True):
        data = st.session_state.problem_data
        scenario = data["scenario"]
        correct_plot = st.session_state.correct_plot
        user_plot = st.session_state.user_plot
        
        # Show what went wrong
        st.markdown("### What needs fixing:")
        
        errors = []
        for value in range(data["min_value"], data["max_value"] + 1):
            user_count = user_plot.get(value, 0)
            correct_count = correct_plot.get(value, 0)
            if user_count != correct_count:
                if user_count < correct_count:
                    errors.append(f"**{scenario['x_label']} = {value}**: You have {user_count} {scenario['unit']}, but need {correct_count} (add {correct_count - user_count} more X's)")
                else:
                    errors.append(f"**{scenario['x_label']} = {value}**: You have {user_count} {scenario['unit']}, but need {correct_count} (remove {user_count - correct_count} X's)")
        
        for error in errors:
            st.markdown(f"• {error}")
        
        # Show the correct distribution
        st.markdown("---")
        st.markdown("### Correct distribution:")
        
        # Create a summary table
        import pandas as pd
        summary_data = []
        for value in range(data["min_value"], data["max_value"] + 1):
            summary_data.append({
                scenario['x_label']: value,
                f"Number of {scenario['unit']}": correct_plot.get(value, 0),
                "Your answer": user_plot.get(value, 0),
                "Status": "✅" if user_plot.get(value, 0) == correct_plot.get(value, 0) else "❌"
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        # Total count
        st.markdown(f"**Total {scenario['unit']}: {sum(correct_plot.values())}**")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_plot = {}
    st.session_state.user_plot = {}
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.plot_submitted = False
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct