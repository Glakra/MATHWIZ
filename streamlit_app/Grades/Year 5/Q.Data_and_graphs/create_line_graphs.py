import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random

def run():
    """
    Main function to run the Create Line Graphs activity.
    Interactive graph creation with direct click plotting on the graph.
    """
    # Initialize session state
    if "create_graph_difficulty" not in st.session_state:
        st.session_state.create_graph_difficulty = 1
        st.session_state.create_graph_consecutive_correct = 0
        st.session_state.create_graph_consecutive_wrong = 0
        st.session_state.create_graph_total_score = 0
        st.session_state.create_graph_total_attempts = 0
        st.session_state.show_result = False
        st.session_state.plotted_points = {}
        st.session_state.graph_submitted = False
        st.session_state.last_click = None
    
    if "current_create_graph_problem" not in st.session_state:
        generate_create_graph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📊 Create Line Graphs")
    st.markdown("*Click directly on the graph to plot points*")
    st.markdown("---")
    
    # Display progress
    display_create_graph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_create_graph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_create_graph_problem()
    
    # Instructions
    with st.expander("💡 **How to Create Line Graphs**", expanded=True):
        st.markdown("""
        ### Steps to Create a Line Graph:
        1. **Read the table** - Look at the x and y values
        2. **Click on the graph** - Click directly where each point should go
        3. **Use the grid lines** - They help you find exact positions
        4. **Points snap to grid** - Your clicks will snap to the nearest grid intersection
        5. **Submit when done** - Click submit after plotting all points
        
        ### Tips for Accurate Plotting:
        - **Find the x-value** first on the horizontal axis
        - **Move up** to the correct y-value
        - **Click** at the intersection
        - Red dots show your plotted points
        - Points connect automatically with lines
        """)

def get_create_graph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.create_graph_difficulty
    
    settings = {
        1: {
            "data_points": 3,
            "value_range": (0, 20),
            "allow_zero": False,
            "label": "Simple Graphs",
            "color": "🟢",
            "y_max": 20,
            "y_step": 5
        },
        2: {
            "data_points": 4,
            "value_range": (0, 40),
            "allow_zero": False,
            "label": "Basic Graphs",
            "color": "🟡",
            "y_max": 40,
            "y_step": 10
        },
        3: {
            "data_points": 5,
            "value_range": (0, 50),
            "allow_zero": False,
            "label": "Standard Graphs",
            "color": "🟠",
            "y_max": 50,
            "y_step": 10
        },
        4: {
            "data_points": 5,
            "value_range": (0, 50),
            "allow_zero": True,
            "label": "Graphs with Zeros",
            "color": "🔴",
            "y_max": 50,
            "y_step": 10
        },
        5: {
            "data_points": 6,
            "value_range": (0, 100),
            "allow_zero": True,
            "label": "Large Range Graphs",
            "color": "🟣",
            "y_max": 100,
            "y_step": 20
        },
        6: {
            "data_points": 7,
            "value_range": (0, 100),
            "allow_zero": True,
            "label": "Complex Graphs",
            "color": "⚫",
            "y_max": 100,
            "y_step": 10
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_create_graph_progress():
    """Display current level and progress"""
    settings = get_create_graph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.create_graph_difficulty}/6")
    
    with col2:
        st.metric("Graph Type", settings['label'])
    
    with col3:
        if st.session_state.create_graph_total_attempts > 0:
            accuracy = (st.session_state.create_graph_total_score / st.session_state.create_graph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.create_graph_consecutive_correct}")

def generate_graph_data(settings):
    """Generate data for the graph based on difficulty"""
    themes = [
        {
            "title": "Games won by the {team} baseball team",
            "context": "Fans of the {team} baseball team compared the number of games won by their team each year.",
            "x_label": "Year",
            "y_label": "Games won",
            "x_type": "year",
            "unit": "games",
            "teams": ["Maitland", "Bradford", "Riverside", "Northside", "Westfield"]
        },
        {
            "title": "Spelling errors made in The {newspaper} Chronicle",
            "context": "During a meeting, the editor of The {newspaper} Chronicle showed her staff that too many spelling errors were making it into the newspaper.",
            "x_label": "Month",
            "y_label": "Errors",
            "x_type": "month",
            "unit": "errors",
            "newspapers": ["Jamberoo", "Riverside", "Morning", "Evening", "Daily"]
        },
        {
            "title": "Art contest entries",
            "context": "Mrs Hill hosts an annual art contest for kids, and she keeps a record of the number of entries each year.",
            "x_label": "Year",
            "y_label": "Number of entries",
            "x_type": "year",
            "unit": "entries"
        },
        {
            "title": "Shoes purchased by {name}",
            "context": "{name}'s favourite shoe store used customer management software to track the shoes she purchased each year.",
            "x_label": "Year", 
            "y_label": "Pairs of shoes",
            "x_type": "year_skip",
            "unit": "pairs",
            "names": ["Christina", "Emma", "Sarah", "Jessica", "Ashley"]
        },
        {
            "title": "Text messages received by {name}",
            "context": "Before deciding to switch to an unlimited texting plan, {name} kept track of the number of text messages she received.",
            "x_label": "Day",
            "y_label": "Text messages",
            "x_type": "day",
            "unit": "messages",
            "names": ["Ava", "Olivia", "Emma", "Sophia", "Isabella"]
        }
    ]
    
    theme = random.choice(themes)
    
    # Customize theme
    if "teams" in theme:
        team = random.choice(theme["teams"])
        theme["title"] = theme["title"].format(team=team)
        theme["context"] = theme["context"].format(team=team)
    elif "newspapers" in theme:
        newspaper = random.choice(theme["newspapers"])
        theme["title"] = theme["title"].format(newspaper=newspaper)
        theme["context"] = theme["context"].format(newspaper=newspaper)
    elif "names" in theme:
        name = random.choice(theme["names"])
        theme["title"] = theme["title"].format(name=name)
        theme["context"] = theme["context"].format(name=name)
    
    # Generate x-axis values
    if theme["x_type"] == "year":
        start_year = 2018
        x_values = [start_year + i for i in range(settings["data_points"])]
    elif theme["x_type"] == "year_skip":
        start_year = 2011
        x_values = [start_year + i * 2 for i in range(settings["data_points"])]
    elif theme["x_type"] == "month":
        all_months = ["April", "May", "June", "July", "August"]
        x_values = all_months[:settings["data_points"]]
    elif theme["x_type"] == "day":
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        x_values = days[:settings["data_points"]]
    
    # Generate y-values aligned to grid
    y_values = []
    for i in range(len(x_values)):
        if i == 0:
            y = random.randint(1, 3) * settings["y_step"]
        else:
            prev = y_values[-1]
            if random.random() < 0.5:
                # Go up
                y = min(prev + settings["y_step"] * random.randint(1, 2), settings["y_max"])
            else:
                # Go down
                y = max(prev - settings["y_step"] * random.randint(1, 2), 0)
        y_values.append(y)
    
    # Add a zero if allowed
    if settings["allow_zero"] and random.random() < 0.3:
        zero_idx = random.randint(1, len(y_values) - 1)
        y_values[zero_idx] = 0
    
    return {
        "theme": theme,
        "x_values": x_values,
        "y_values": y_values
    }

def generate_create_graph_problem():
    """Generate a new graph creation problem"""
    settings = get_create_graph_difficulty_settings()
    
    # Generate data
    data = generate_graph_data(settings)
    
    problem_data = {
        "settings": settings,
        "data": data,
        "context": data["theme"]["context"],
        "instruction": "Use the data in the table to complete the line graph below."
    }
    
    st.session_state.current_create_graph_problem = problem_data
    st.session_state.plotted_points = {}
    st.session_state.graph_submitted = False
    st.session_state.show_result = False
    st.session_state.last_click = None

def display_create_graph_problem():
    """Display the graph creation interface"""
    problem = st.session_state.current_create_graph_problem
    data = problem["data"]
    
    # Display context
    st.markdown(f"### {problem['context']}")
    st.markdown(problem['instruction'])
    
    # Create two columns
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Display the data table
        display_data_table(data)
        
        # Display current points
        if st.session_state.plotted_points:
            st.markdown("### Points Plotted:")
            for x in data['x_values']:
                if x in st.session_state.plotted_points:
                    y = st.session_state.plotted_points[x]
                    st.success(f"✅ ({x}, {y})")
                else:
                    st.info(f"⭕ ({x}, ?)")
        
        # Last click info
        if st.session_state.last_click and not st.session_state.graph_submitted:
            st.info(f"Last click: {st.session_state.last_click}")
    
    with col2:
        # Display the interactive graph
        st.markdown("📍 **Click to select points on the graph.**")
        
        # Create the interactive Plotly graph
        fig = create_interactive_plotly_graph(problem)
        
        # Display with click events enabled
        selected_points = st.plotly_chart(
            fig, 
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="graph_plot"
        )
        
        # Process click events
        if selected_points and selected_points["selection"]["points"]:
            process_graph_click(selected_points["selection"]["points"][0], problem)
    
    # Control buttons
    if not st.session_state.graph_submitted:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Clear Last Point", type="secondary", use_container_width=True):
                if st.session_state.plotted_points:
                    # Remove the last plotted point
                    for x in reversed(data['x_values']):
                        if x in st.session_state.plotted_points:
                            del st.session_state.plotted_points[x]
                            break
                    st.rerun()
        
        with col2:
            if st.button("Reset Graph", type="secondary", use_container_width=True):
                st.session_state.plotted_points = {}
                st.session_state.last_click = None
                st.rerun()
        
        with col3:
            points_needed = len(data['x_values'])
            points_plotted = len(st.session_state.plotted_points)
            
            if st.button(
                f"Submit ({points_plotted}/{points_needed})", 
                type="primary", 
                use_container_width=True,
                disabled=points_plotted < points_needed
            ):
                check_create_graph_answer()
                st.rerun()
    
    # Show feedback
    if st.session_state.show_result:
        display_create_graph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Graph", type="primary", use_container_width=True):
                generate_create_graph_problem()
                st.rerun()

def create_interactive_plotly_graph(problem):
    """Create an interactive Plotly graph that responds to clicks"""
    data = problem["data"]
    settings = problem["settings"]
    theme = data["theme"]
    
    fig = go.Figure()
    
    # Create an invisible scatter plot covering the entire grid for click detection
    # This allows clicking anywhere on the graph
    grid_x = []
    grid_y = []
    hover_text = []
    
    # Create grid points for all possible click locations
    for i, x_val in enumerate(data['x_values']):
        for y in range(0, settings['y_max'] + 1, settings['y_step']):
            grid_x.append(i)
            grid_y.append(y)
            hover_text.append(f"Click to plot ({x_val}, {y})")
    
    # Add invisible clickable points
    fig.add_trace(go.Scatter(
        x=grid_x,
        y=grid_y,
        mode='markers',
        marker=dict(
            size=20,
            color='rgba(0,0,0,0.01)',  # Almost invisible
            line=dict(width=0)
        ),
        hovertext=hover_text,
        hoverinfo='text',
        showlegend=False,
        name='grid'
    ))
    
    # Plot user's points
    if st.session_state.plotted_points:
        user_x = []
        user_y = []
        user_labels = []
        
        for i, x_val in enumerate(data['x_values']):
            if x_val in st.session_state.plotted_points:
                user_x.append(i)
                user_y.append(st.session_state.plotted_points[x_val])
                user_labels.append(f"({x_val}, {st.session_state.plotted_points[x_val]})")
        
        # Add user points
        fig.add_trace(go.Scatter(
            x=user_x,
            y=user_y,
            mode='markers+lines',
            marker=dict(
                size=12,
                color='red',
                line=dict(width=2, color='darkred')
            ),
            line=dict(color='red', width=2),
            text=user_labels,
            hoverinfo='text',
            name='Your points'
        ))
    
    # Show correct answer if submitted
    if st.session_state.show_result and st.session_state.graph_submitted:
        correct_x = list(range(len(data['x_values'])))
        fig.add_trace(go.Scatter(
            x=correct_x,
            y=data['y_values'],
            mode='markers+lines',
            marker=dict(
                size=10,
                color='green',
                symbol='circle-open',
                line=dict(width=2)
            ),
            line=dict(color='green', width=2, dash='dash'),
            name='Correct answer'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=theme['title'],
            font=dict(size=16)
        ),
        xaxis=dict(
            title=theme['x_label'],
            tickmode='array',
            tickvals=list(range(len(data['x_values']))),
            ticktext=data['x_values'],
            showgrid=True,
            gridcolor='lightgray',
            range=[-0.5, len(data['x_values']) - 0.5]
        ),
        yaxis=dict(
            title=theme['y_label'],
            tickmode='linear',
            tick0=0,
            dtick=settings['y_step'],
            showgrid=True,
            gridcolor='lightgray',
            range=[-settings['y_max'] * 0.05, settings['y_max'] * 1.05]
        ),
        height=500,
        hovermode='closest',
        showlegend=True,
        plot_bgcolor='white'
    )
    
    # Add instruction text
    fig.add_annotation(
        text="Click on grid intersections to plot points",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=12, color="gray")
    )
    
    return fig

def process_graph_click(point_data, problem):
    """Process a click on the graph"""
    if st.session_state.graph_submitted:
        return
    
    data = problem["data"]
    settings = problem["settings"]
    
    # Get click coordinates
    x_index = int(round(point_data['x']))
    y_value = int(round(point_data['y'] / settings['y_step']) * settings['y_step'])
    
    # Ensure values are in valid range
    if 0 <= x_index < len(data['x_values']) and 0 <= y_value <= settings['y_max']:
        x_val = data['x_values'][x_index]
        st.session_state.plotted_points[x_val] = y_value
        st.session_state.last_click = f"Plotted ({x_val}, {y_value})"
        st.rerun()

def display_data_table(data):
    """Display the data table"""
    theme = data["theme"]
    
    st.markdown(f"#### {theme['title']}")
    
    # Create DataFrame
    df = pd.DataFrame({
        theme['x_label']: data['x_values'],
        theme['y_label']: data['y_values']
    })
    
    # Display with styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=min(400, 50 + len(data['x_values']) * 35)
    )

def check_create_graph_answer():
    """Check if the plotted graph is correct"""
    problem = st.session_state.current_create_graph_problem
    data = problem["data"]
    
    # Update statistics
    st.session_state.create_graph_total_attempts += 1
    
    # Check each point
    is_correct = True
    comparison = []
    
    for x_val, correct_y in zip(data['x_values'], data['y_values']):
        if x_val in st.session_state.plotted_points:
            user_y = st.session_state.plotted_points[x_val]
            point_correct = user_y == correct_y
            if not point_correct:
                is_correct = False
            comparison.append({
                "x": x_val,
                "correct_y": correct_y,
                "user_y": user_y,
                "is_correct": point_correct
            })
        else:
            is_correct = False
            comparison.append({
                "x": x_val,
                "correct_y": correct_y,
                "user_y": "Not plotted",
                "is_correct": False
            })
    
    if is_correct:
        st.session_state.create_graph_total_score += 1
        st.session_state.create_graph_consecutive_correct += 1
        st.session_state.create_graph_consecutive_wrong = 0
        st.session_state.current_create_graph_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.create_graph_consecutive_correct >= 3 and 
            st.session_state.create_graph_difficulty < 6):
            st.session_state.create_graph_difficulty += 1
            st.session_state.create_graph_consecutive_correct = 0
    else:
        st.session_state.create_graph_consecutive_wrong += 1
        st.session_state.create_graph_consecutive_correct = 0
        st.session_state.current_create_graph_problem["result"] = "incorrect"
        st.session_state.current_create_graph_problem["comparison"] = comparison
        
        # Check for level down
        if (st.session_state.create_graph_consecutive_wrong >= 3 and 
            st.session_state.create_graph_difficulty > 1):
            st.session_state.create_graph_difficulty -= 1
            st.session_state.create_graph_consecutive_wrong = 0
    
    st.session_state.graph_submitted = True
    st.session_state.show_result = True

def display_create_graph_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_create_graph_problem
    data = problem["data"]
    theme = data["theme"]
    
    if problem.get("result") == "correct":
        st.success("✅ Perfect! You plotted all points correctly by clicking on the graph!")
        
        if st.session_state.create_graph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Excellent graph plotting skills! {st.session_state.create_graph_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.create_graph_consecutive_correct == 0:
            st.success(f"🎉 Level Up! Now creating: {get_create_graph_difficulty_settings()['label']}!")
    else:
        st.error("❌ Not quite right. Review where each point should be plotted.")
        
        # Show detailed feedback
        with st.expander("📊 See the correct plotting positions", expanded=True):
            st.markdown("### Where to click for each point:")
            
            comparison = problem.get("comparison", [])
            
            for i, item in enumerate(comparison):
                x = item["x"]
                correct = item["correct_y"]
                user = item["user_y"]
                
                if item.get("is_correct"):
                    st.success(f"**Point {i+1}: ({x}, {correct})** ✅ Correctly plotted!")
                else:
                    st.error(f"**Point {i+1}: ({x}, {correct})** ❌")
                    
                    st.markdown(f"**To plot this point correctly:**")
                    st.markdown(f"1. Find **{x}** on the {theme['x_label'].lower()} axis")
                    st.markdown(f"2. Move straight up to **{correct}** on the {theme['y_label'].lower()} axis")
                    st.markdown(f"3. Click at that intersection")
                    
                    if user == "Not plotted":
                        st.warning("⚠️ You didn't plot this point")
                    else:
                        st.warning(f"⚠️ You clicked at ({x}, {user}) instead of ({x}, {correct})")
            
            st.info("""
            💡 **Remember:**
            - Click directly on the graph where lines intersect
            - Use grid lines to find exact positions
            - Your clicks will snap to the nearest grid point
            - Check each point against the table values
            """)
        
        # Level down message
        if st.session_state.create_graph_consecutive_wrong == 0:
            st.warning(f"📉 Moving to easier graphs: {get_create_graph_difficulty_settings()['label']}")

def clear_create_graph_state():
    """Clear all graph creation related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('create_graph_') or key in ['current_create_graph_problem', 'plotted_points', 
                                                       'graph_submitted', 'show_result', 'last_click']:
            del st.session_state[key]