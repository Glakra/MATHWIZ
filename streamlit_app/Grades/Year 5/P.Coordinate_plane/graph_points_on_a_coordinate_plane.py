import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
import random
import math

def run():
    """
    Main function to run the Graph Points on Coordinate Plane activity.
    Interactive plotting with direct click-on-graph functionality.
    """
    # Initialize session state
    if "graph_difficulty" not in st.session_state:
        st.session_state.graph_difficulty = 1
        st.session_state.graph_consecutive_correct = 0
        st.session_state.graph_consecutive_wrong = 0
        st.session_state.graph_total_score = 0
        st.session_state.graph_total_attempts = 0
        st.session_state.plotted_points = []
        st.session_state.show_result = False
        st.session_state.plot_key = 0
    
    if "current_graph_problem" not in st.session_state:
        generate_graph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > P. Coordinate plane**")
    st.title("📍 Graph Points on a Coordinate Plane")
    st.markdown("*Click directly on the grid to plot points*")
    st.markdown("---")
    
    # Display progress
    display_graph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_graph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_graph_problem()
    
    # Instructions
    with st.expander("💡 **How to Plot Points**", expanded=False):
        st.markdown("""
        ### How to Plot:
        1. **Read the coordinates** carefully (x, y)
        2. **Click directly on any grid intersection**
        3. Your point will appear at that location
        4. **Submit** when you've plotted all required points
        
        ### Coordinate System:
        - **x-coordinate (first number)**: Distance right (+) or left (-) from origin
        - **y-coordinate (second number)**: Distance up (+) or down (-) from origin
        - **Origin (0, 0)**: Where the axes cross
        
        ### Tips:
        - Click on the grid intersections (where lines cross)
        - Blue dots show your plotted points
        - If clicking doesn't work, use the manual input option
        """)

def get_graph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.graph_difficulty
    
    settings = {
        1: {
            "min_coord": 0,
            "max_coord": 5,
            "grid_size": 5,
            "num_points": 1,
            "point_type": "single",
            "tolerance": 0.5,
            "label": "Beginner (0-5)",
            "color": "🟢"
        },
        2: {
            "min_coord": 0,
            "max_coord": 10,
            "grid_size": 10,
            "num_points": 1,
            "point_type": "single",
            "tolerance": 0.5,
            "label": "Basic (0-10)",
            "color": "🟡"
        },
        3: {
            "min_coord": 0,
            "max_coord": 10,
            "grid_size": 10,
            "num_points": random.randint(2, 3),
            "point_type": "multiple",
            "tolerance": 0.5,
            "label": "Multiple Points",
            "color": "🟠"
        },
        4: {
            "min_coord": -5,
            "max_coord": 5,
            "grid_size": 10,
            "num_points": random.randint(1, 3),
            "point_type": "multiple",
            "tolerance": 0.5,
            "label": "With Negatives",
            "color": "🔴"
        },
        5: {
            "min_coord": -5,
            "max_coord": 5,
            "grid_size": 10,
            "num_points": random.randint(3, 4),
            "point_type": "shape",
            "tolerance": 0.5,
            "label": "Shape Plotting",
            "color": "🟣"
        },
        6: {
            "min_coord": -10,
            "max_coord": 10,
            "grid_size": 20,
            "num_points": random.randint(4, 6),
            "point_type": "pattern",
            "tolerance": 0.5,
            "label": "Advanced Patterns",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_graph_progress():
    """Display current level and progress"""
    settings = get_graph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.graph_difficulty}/6")
    
    with col2:
        st.metric("Difficulty", settings['label'])
    
    with col3:
        if st.session_state.graph_total_attempts > 0:
            accuracy = (st.session_state.graph_total_score / st.session_state.graph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.graph_consecutive_correct}")
    
    # Progress bar
    progress = (st.session_state.graph_difficulty - 1) / 5
    st.progress(progress, text=f"Progress to Master Level")

def generate_graph_problem():
    """Generate a new graph plotting problem"""
    settings = get_graph_difficulty_settings()
    
    problem_data = {
        "settings": settings,
        "points_to_plot": [],
        "description": "",
        "hint": ""
    }
    
    if settings["point_type"] == "single":
        # Single point
        x = random.randint(settings["min_coord"], settings["max_coord"])
        y = random.randint(settings["min_coord"], settings["max_coord"])
        problem_data["points_to_plot"] = [(x, y)]
        problem_data["description"] = f"Plot the point ({x}, {y})"
        
    elif settings["point_type"] == "multiple":
        # Multiple independent points
        points = []
        for i in range(settings["num_points"]):
            x = random.randint(settings["min_coord"], settings["max_coord"])
            y = random.randint(settings["min_coord"], settings["max_coord"])
            # Ensure points don't overlap
            while (x, y) in points:
                x = random.randint(settings["min_coord"], settings["max_coord"])
                y = random.randint(settings["min_coord"], settings["max_coord"])
            points.append((x, y))
        
        problem_data["points_to_plot"] = points
        point_list = ", ".join([f"({x}, {y})" for x, y in points])
        problem_data["description"] = f"Plot the points: {point_list}"
        
    elif settings["point_type"] == "shape":
        # Points that form a shape
        shape_type = random.choice(["triangle", "square", "rectangle"])
        
        if shape_type == "triangle":
            cx, cy = random.randint(-2, 2), random.randint(-2, 2)
            points = [
                (cx, cy + 3),
                (cx - 2, cy - 1),
                (cx + 2, cy - 1)
            ]
            problem_data["description"] = "Plot these points to form a triangle"
            problem_data["hint"] = "Connect these points to see the triangle!"
            
        elif shape_type == "square":
            cx, cy = random.randint(-2, 2), random.randint(-2, 2)
            size = random.randint(2, 3)
            points = [
                (cx - size, cy - size),
                (cx + size, cy - size),
                (cx + size, cy + size),
                (cx - size, cy + size)
            ]
            problem_data["description"] = "Plot these points to form a square"
            problem_data["hint"] = "These points are the corners of a square!"
            
        else:  # rectangle
            x1 = random.randint(settings["min_coord"] + 1, settings["max_coord"] - 3)
            y1 = random.randint(settings["min_coord"] + 1, settings["max_coord"] - 2)
            width = random.randint(2, 4)
            height = random.randint(1, 3)
            points = [
                (x1, y1),
                (x1 + width, y1),
                (x1 + width, y1 + height),
                (x1, y1 + height)
            ]
            problem_data["description"] = "Plot these points to form a rectangle"
        
        problem_data["points_to_plot"] = points
        
    else:  # pattern
        # Simple patterns
        pattern_type = random.choice(["line", "vertical", "horizontal"])
        
        if pattern_type == "line":
            points = []
            start = max(settings["min_coord"], -5)
            end = min(settings["max_coord"], 5)
            values = list(range(start, end + 1))
            random.shuffle(values)
            for val in values[:settings["num_points"]]:
                points.append((val, val))
            problem_data["description"] = "Plot points on the line y = x"
            problem_data["hint"] = "These points form a diagonal line!"
            
        elif pattern_type == "vertical":
            x = random.randint(settings["min_coord"] + 1, settings["max_coord"] - 1)
            points = []
            y_values = list(range(settings["min_coord"], settings["max_coord"] + 1))
            random.shuffle(y_values)
            for y in y_values[:settings["num_points"]]:
                points.append((x, y))
            problem_data["description"] = f"Plot points on the vertical line x = {x}"
            
        else:  # horizontal
            y = random.randint(settings["min_coord"] + 1, settings["max_coord"] - 1)
            points = []
            x_values = list(range(settings["min_coord"], settings["max_coord"] + 1))
            random.shuffle(x_values)
            for x in x_values[:settings["num_points"]]:
                points.append((x, y))
            problem_data["description"] = f"Plot points on the horizontal line y = {y}"
        
        problem_data["points_to_plot"] = points
    
    # Add point labels
    if len(problem_data["points_to_plot"]) > 1:
        labeled_points = []
        for i, point in enumerate(problem_data["points_to_plot"]):
            labeled_points.append(f"{chr(65 + i)}: ({point[0]}, {point[1]})")
        problem_data["point_labels"] = labeled_points
    
    st.session_state.current_graph_problem = problem_data
    st.session_state.plotted_points = []
    st.session_state.show_result = False
    st.session_state.plot_key += 1

def display_graph_problem():
    """Display the interactive coordinate plane"""
    problem = st.session_state.current_graph_problem
    settings = problem["settings"]
    
    # Display instructions
    st.markdown(f"### {problem['description']}")
    
    # Show individual points if multiple
    if "point_labels" in problem:
        cols = st.columns(min(4, len(problem["point_labels"])))
        for i, label in enumerate(problem["point_labels"]):
            with cols[i % len(cols)]:
                st.info(label)
    
    # Show hint if available
    if problem["hint"] and st.session_state.graph_difficulty >= 3:
        st.caption(f"💡 Hint: {problem['hint']}")
    
    # Create layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Create the interactive plot
        fig = create_interactive_plot(problem)
        
        # Display the plot and capture click events
        if not st.session_state.show_result:
            # Important: Add config to enable click events
            config = {'displayModeBar': False}
            
            clicked_points = plotly_events(
                fig,
                click_event=True,
                hover_event=False,
                select_event=False,
                override_height=600,
                override_width="100%",
                key=f"plotly_chart_{st.session_state.plot_key}"
            )
            
            # Handle click events
            if clicked_points and len(clicked_points) > 0:
                handle_click(clicked_points[0], problem)
        else:
            # Just display the plot without click events
            st.plotly_chart(fig, use_container_width=False, config={'displayModeBar': False})
    
    with col2:
        st.markdown("### Controls")
        
        # Show points needed/plotted
        points_needed = len(problem["points_to_plot"])
        points_plotted = len(st.session_state.plotted_points)
        
        if not st.session_state.show_result:
            st.info(f"Points: {points_plotted}/{points_needed}")
            
            # Clear button
            if st.session_state.plotted_points:
                if st.button("Clear All", type="secondary", use_container_width=True):
                    st.session_state.plotted_points = []
                    st.session_state.plot_key += 1
                    st.rerun()
            
            # Submit button
            if points_plotted == points_needed:
                if st.button("Submit", type="primary", use_container_width=True):
                    check_graph_answer()
                    st.rerun()
            else:
                st.caption(f"Plot {points_needed - points_plotted} more")
            
            # Manual input as backup
            st.markdown("---")
            st.markdown("### Manual Input")
            st.caption("If clicking doesn't work:")
            
            x_input = st.number_input(
                "X coordinate:",
                min_value=settings["min_coord"],
                max_value=settings["max_coord"],
                value=0,
                step=1,
                key=f"x_input_{st.session_state.plot_key}"
            )
            
            y_input = st.number_input(
                "Y coordinate:",
                min_value=settings["min_coord"],
                max_value=settings["max_coord"],
                value=0,
                step=1,
                key=f"y_input_{st.session_state.plot_key}"
            )
            
            if st.button("Add Point", use_container_width=True):
                if (x_input, y_input) not in st.session_state.plotted_points:
                    st.session_state.plotted_points.append((x_input, y_input))
                    st.session_state.plot_key += 1
                    st.rerun()
                else:
                    st.warning("Point already plotted!")
        
        # Show plotted points
        if st.session_state.plotted_points:
            st.markdown("### Plotted:")
            for i, (x, y) in enumerate(st.session_state.plotted_points):
                st.caption(f"{chr(65 + i)}: ({x}, {y})")
    
    # Show feedback
    if st.session_state.show_result:
        display_graph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="primary", use_container_width=True):
                generate_graph_problem()
                st.rerun()

def create_interactive_plot(problem):
    """Create an interactive Plotly plot with clickable grid"""
    settings = problem["settings"]
    
    # Create figure
    fig = go.Figure()
    
    # IMPORTANT: Add invisible scatter points for click detection
    # This creates a clickable grid
    grid_x = []
    grid_y = []
    for x in range(settings["min_coord"], settings["max_coord"] + 1):
        for y in range(settings["min_coord"], settings["max_coord"] + 1):
            grid_x.append(x)
            grid_y.append(y)
    
    # Add invisible clickable points first
    fig.add_trace(go.Scatter(
        x=grid_x,
        y=grid_y,
        mode='markers',
        marker=dict(
            size=30,  # Large enough to click easily
            color='rgba(0,0,0,0.01)',  # Nearly invisible
            symbol='square'  # Square markers for better coverage
        ),
        hoverinfo='text',
        hovertext=[f'({x},{y})' for x, y in zip(grid_x, grid_y)],
        showlegend=False,
        name='grid'
    ))
    
    # Add grid lines
    for i in range(settings["min_coord"], settings["max_coord"] + 1):
        # Vertical lines
        fig.add_shape(
            type="line",
            x0=i, y0=settings["min_coord"], 
            x1=i, y1=settings["max_coord"],
            line=dict(color="lightgray", width=1)
        )
        # Horizontal lines
        fig.add_shape(
            type="line",
            x0=settings["min_coord"], y0=i, 
            x1=settings["max_coord"], y1=i,
            line=dict(color="lightgray", width=1)
        )
    
    # Add axes (thicker lines at x=0 and y=0)
    fig.add_shape(
        type="line",
        x0=0, y0=settings["min_coord"], 
        x1=0, y1=settings["max_coord"],
        line=dict(color="black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=settings["min_coord"], y0=0, 
        x1=settings["max_coord"], y1=0,
        line=dict(color="black", width=2)
    )
    
    # Plot user's points
    if st.session_state.plotted_points:
        x_vals = [p[0] for p in st.session_state.plotted_points]
        y_vals = [p[1] for p in st.session_state.plotted_points]
        labels = [chr(65 + i) for i in range(len(st.session_state.plotted_points))]
        
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers+text',
            marker=dict(size=15, color='blue'),
            text=labels,
            textposition="top right",
            textfont=dict(size=14, color='blue', family='Arial Black'),
            name='Your Points',
            hovertemplate='%{text}: (%{x}, %{y})<extra></extra>',
            showlegend=False
        ))
    
    # Show correct points if in feedback mode
    if st.session_state.show_result:
        for x, y in problem["points_to_plot"]:
            is_correct = any(
                abs(px - x) < settings["tolerance"] and 
                abs(py - y) < settings["tolerance"] 
                for px, py in st.session_state.plotted_points
            )
            
            if is_correct:
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers',
                    marker=dict(
                        size=20, 
                        color='rgba(0,255,0,0.2)',
                        line=dict(color='green', width=3)
                    ),
                    showlegend=False
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(size=20, color='red', symbol='x'),
                    text=[f'({x},{y})'],
                    textposition="bottom center",
                    textfont=dict(size=10, color='red'),
                    showlegend=False
                ))
    
    # Update layout
    fig.update_layout(
        xaxis=dict(
            range=[settings["min_coord"] - 0.5, settings["max_coord"] + 0.5],
            dtick=1,
            title="x",
            showgrid=False,
            zeroline=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[settings["min_coord"] - 0.5, settings["max_coord"] + 0.5],
            dtick=1,
            title="y",
            showgrid=False,
            zeroline=False,
            scaleanchor="x",
            scaleratio=1,
            fixedrange=True
        ),
        width=600,
        height=600,
        showlegend=False,
        hovermode='closest',
        hoverdistance=50,  # Increase hover distance for easier clicking
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=50, b=50),
        dragmode=False
    )
    
    return fig

def handle_click(clicked_point, problem):
    """Handle click events on the plot"""
    settings = problem["settings"]
    
    if clicked_point and len(st.session_state.plotted_points) < len(problem["points_to_plot"]):
        # Get the clicked coordinates
        x = round(clicked_point['x'])
        y = round(clicked_point['y'])
        
        # Check if point is within bounds
        if (settings["min_coord"] <= x <= settings["max_coord"] and 
            settings["min_coord"] <= y <= settings["max_coord"]):
            
            # Check if point already plotted
            if (x, y) not in st.session_state.plotted_points:
                st.session_state.plotted_points.append((x, y))
                st.session_state.plot_key += 1
                st.rerun()

def check_graph_answer():
    """Check if the plotted points are correct"""
    problem = st.session_state.current_graph_problem
    settings = problem["settings"]
    tolerance = settings["tolerance"]
    
    correct_points = problem["points_to_plot"]
    plotted_points = st.session_state.plotted_points
    
    # Check each correct point
    all_correct = True
    correctly_plotted = 0
    
    for correct_x, correct_y in correct_points:
        # Find if this point was plotted within tolerance
        point_found = False
        for plotted_x, plotted_y in plotted_points:
            if (abs(plotted_x - correct_x) < tolerance and 
                abs(plotted_y - correct_y) < tolerance):
                point_found = True
                correctly_plotted += 1
                break
        
        if not point_found:
            all_correct = False
    
    # Update statistics
    st.session_state.graph_total_attempts += 1
    
    if all_correct and len(plotted_points) == len(correct_points):
        st.session_state.graph_total_score += 1
        st.session_state.graph_consecutive_correct += 1
        st.session_state.graph_consecutive_wrong = 0
        st.session_state.current_graph_problem["result"] = "correct"
        
        # Check for level up
        if (st.session_state.graph_consecutive_correct >= 3 and 
            st.session_state.graph_difficulty < 6):
            st.session_state.graph_difficulty += 1
            st.session_state.graph_consecutive_correct = 0
    else:
        st.session_state.graph_consecutive_wrong += 1
        st.session_state.graph_consecutive_correct = 0
        st.session_state.current_graph_problem["result"] = "incorrect"
        st.session_state.current_graph_problem["correctly_plotted"] = correctly_plotted
        
        # Check for level down
        if (st.session_state.graph_consecutive_wrong >= 3 and 
            st.session_state.graph_difficulty > 1):
            st.session_state.graph_difficulty -= 1
            st.session_state.graph_consecutive_wrong = 0
    
    st.session_state.show_result = True

def display_graph_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_graph_problem
    
    if problem.get("result") == "correct":
        st.success("✅ Excellent! All points plotted correctly!")
        
        if st.session_state.graph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Great streak of {st.session_state.graph_consecutive_correct} correct answers!")
        
        # Level up message
        if st.session_state.graph_consecutive_correct == 0:  # Just leveled up
            st.success(f"🎉 Level Up! You've reached Level {st.session_state.graph_difficulty}!")
    else:
        correctly_plotted = problem.get("correctly_plotted", 0)
        total_points = len(problem["points_to_plot"])
        
        st.error(f"❌ Not quite right. You plotted {correctly_plotted} out of {total_points} points correctly.")
        
        # Show what was wrong
        with st.expander("📊 See the solution"):
            st.markdown("**Correct points:**")
            for i, (x, y) in enumerate(problem["points_to_plot"]):
                st.write(f"Point {chr(65 + i)}: ({x}, {y})")
            
            if problem.get("hint"):
                st.info(f"Remember: {problem['hint']}")

def clear_graph_state():
    """Clear all graph-related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('graph_') or key in ['current_graph_problem', 'plotted_points', 'show_result', 'plot_key']:
            del st.session_state[key]