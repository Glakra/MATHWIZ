import streamlit as st
import streamlit.components.v1 as components
import random
import json

def run():
    """
    Create Bar Graphs with draggable bars using HTML/JS
    """
    # Initialize session state
    if "create_bar_difficulty" not in st.session_state:
        st.session_state.create_bar_difficulty = 1
        st.session_state.create_bar_consecutive_correct = 0
        st.session_state.create_bar_consecutive_wrong = 0
        st.session_state.create_bar_total_score = 0
        st.session_state.create_bar_total_attempts = 0
        st.session_state.graph_submitted = False
        st.session_state.current_values = {}
    
    if "current_create_bar_problem" not in st.session_state:
        generate_create_bar_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📊 Create Bar Graphs")
    st.markdown("*Drag the red bars up or down to match the correct heights*")
    st.markdown("---")
    
    # Display progress
    display_create_bar_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_create_bar_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_create_bar_problem()
    
    # Instructions
    with st.expander("💡 **How to Use Draggable Bar Graphs**", expanded=False):
        st.markdown("""
        ### Direct Manipulation:
        1. **Red bars** can be dragged - click and hold to adjust
        2. **Blue bars** are fixed reference values
        3. **Drag up** to increase height
        4. **Drag down** to decrease height
        5. **Green dotted lines** show target values
        
        ### Visual Feedback:
        - 🔴 **Red**: Incorrect height (drag these!)
        - 🟢 **Green**: Correct height!
        - 📏 **Grid lines**: Help align to exact values
        - 🎯 **Target lines**: Show where bars should be
        
        ### Tips:
        - Look for the "↕ Drag me!" hints above red bars
        - Watch the value display as you drag
        - Bars snap to the nearest grid line
        - Release mouse button to set the height
        """)

def get_create_bar_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.create_bar_difficulty
    
    settings = {
        1: {
            "value_range": (0, 20),
            "num_bars": 4,
            "missing_bars": 1,
            "label": "Single Bar - Small Values",
            "color": "🟢",
            "max_value": 25,
            "step_size": 5
        },
        2: {
            "value_range": (0, 50),
            "num_bars": 5,
            "missing_bars": 2,
            "label": "Two Bars - Medium Values",
            "color": "🟡",
            "max_value": 60,
            "step_size": 10
        },
        3: {
            "value_range": (0, 100),
            "num_bars": 5,
            "missing_bars": 2,
            "label": "Larger Values",
            "color": "🟠",
            "max_value": 120,
            "step_size": 10
        },
        4: {
            "value_range": (0, 100),
            "num_bars": 6,
            "missing_bars": 3,
            "label": "Multiple Missing Bars",
            "color": "🔴",
            "max_value": 120,
            "step_size": 10
        },
        5: {
            "value_range": (0, 200),
            "num_bars": 6,
            "missing_bars": 3,
            "label": "Large Values & Patterns",
            "color": "🟣",
            "max_value": 250,
            "step_size": 25
        },
        6: {
            "value_range": (0, 500),
            "num_bars": 7,
            "missing_bars": 4,
            "label": "Complex Graphs",
            "color": "⚫",
            "max_value": 600,
            "step_size": 50
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_create_bar_progress():
    """Display current level and progress"""
    settings = get_create_bar_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.create_bar_difficulty}/6")
    
    with col2:
        st.metric("Task Type", settings['label'])
    
    with col3:
        if st.session_state.create_bar_total_attempts > 0:
            accuracy = (st.session_state.create_bar_total_score / st.session_state.create_bar_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.create_bar_consecutive_correct}")

def generate_bar_data(settings):
    """Generate data for the bar graph"""
    contexts = [
        {
            "title": "Trivia game scores",
            "categories": ["Isabelle", "Jake", "Mackenzie", "Austin", "Bella"],
            "unit": "points",
            "x_label": "Name",
            "y_label": "Score"
        },
        {
            "title": "Temperature at noon",
            "categories": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
            "unit": "°C",
            "x_label": "Day",
            "y_label": "Temperature"
        },
        {
            "title": "Miles biked",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "unit": "miles",
            "x_label": "Day",
            "y_label": "Number of miles"
        },
        {
            "title": "Bottles collected",
            "categories": ["Keenan", "Leon", "Tyler", "Eve", "Max"],
            "unit": "bottles",
            "x_label": "Name",
            "y_label": "Number of bottles"
        },
        {
            "title": "Books read",
            "categories": ["Dylan", "Emilia", "Bridget", "Kaylee", "Nate"],
            "unit": "books",
            "x_label": "Name",
            "y_label": "Number of books"
        },
        {
            "title": "Running miles",
            "categories": ["Gary", "Erica", "Reba", "Pedro", "Vincent"],
            "unit": "miles",
            "x_label": "Name",
            "y_label": "Miles"
        },
        {
            "title": "Daily wind speed",
            "categories": ["Sunday", "Monday", "Tuesday"],
            "unit": "miles per hour",
            "x_label": "Day",
            "y_label": "Wind speed"
        },
        {
            "title": "Hours worked",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday"],
            "unit": "hours",
            "x_label": "Day",
            "y_label": "Hours"
        },
        {
            "title": "Biscuits baked",
            "categories": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "unit": "biscuits",
            "x_label": "Day",
            "y_label": "Number of biscuits"
        }
    ]
    
    context = random.choice(contexts)
    categories = context["categories"][:settings["num_bars"]]
    
    # Generate values
    values = []
    min_val, max_val = settings["value_range"]
    
    for i in range(settings["num_bars"]):
        val = random.randint(min_val + 10, max_val - 10)
        val = round(val / settings["step_size"]) * settings["step_size"]
        values.append(val)
    
    # Select which bars to hide
    missing_indices = random.sample(range(settings["num_bars"]), settings["missing_bars"])
    
    # Create description
    description_parts = []
    for i, (cat, val) in enumerate(zip(categories, values)):
        if "scores" in context["title"]:
            description_parts.append(f"{cat} scored {val} {context['unit']}")
        elif "Temperature" in context["title"]:
            description_parts.append(f"{cat}: {val}{context['unit']}")
        elif "books" in context["title"]:
            description_parts.append(f"{cat} read {val} {context['unit']}")
        elif "Bottles" in context["title"]:
            description_parts.append(f"{cat} collected {val} {context['unit']}")
        elif "Running" in context["title"]:
            description_parts.append(f"{cat} ran {val} {context['unit']}")
        elif "wind" in context["title"]:
            description_parts.append(f"{cat}: {val} {context['unit']}")
        elif "worked" in context["title"]:
            description_parts.append(f"{cat}: {val} {context['unit']}")
        elif "Biscuits" in context["title"]:
            description_parts.append(f"{cat}: {val} {context['unit']}")
        else:
            description_parts.append(f"{val} {context['unit']} on {cat}")
    
    if len(description_parts) > 1:
        description = "Data: " + ", ".join(description_parts[:-1]) + " and " + description_parts[-1] + "."
    else:
        description = "Data: " + description_parts[0] + "."
    
    return {
        "context": context,
        "categories": categories,
        "values": values,
        "missing_indices": missing_indices,
        "description": description
    }

def generate_create_bar_problem():
    """Generate a new bar graph creation problem"""
    settings = get_create_bar_difficulty_settings()
    data = generate_bar_data(settings)
    
    st.session_state.current_create_bar_problem = {
        "settings": settings,
        "data": data,
        "instruction": "Use this data to complete the bar graph below.",
        "hint": "Click and drag the red bars to adjust their heights. Red bars can be dragged up or down!"
    }
    
    # Initialize current values with step_size instead of 0 so bars are visible
    st.session_state.current_values = {}
    for idx in data["missing_indices"]:
        st.session_state.current_values[idx] = settings['step_size']
    
    st.session_state.graph_submitted = False

def create_draggable_bar_chart(problem):
    """Create HTML/JS for draggable bar chart"""
    data = problem["data"]
    settings = problem["settings"]
    context = data["context"]
    
    # Prepare data for JavaScript
    chart_data = []
    for i, (cat, val) in enumerate(zip(data["categories"], data["values"])):
        is_missing = i in data["missing_indices"]
        # Start missing bars with a small visible height instead of 0
        current_val = st.session_state.current_values.get(i, settings['step_size']) if is_missing else val
        
        chart_data.append({
            "category": cat,
            "value": current_val,
            "targetValue": val,
            "isDraggable": is_missing,
            "index": i
        })
    
    # Create the HTML/JS
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: white;
            }}
            .bar {{
                cursor: pointer;
                transition: opacity 0.2s;
            }}
            .bar.draggable {{
                cursor: ns-resize;
                stroke: #333;
                stroke-width: 2;
            }}
            .bar.draggable:hover {{
                opacity: 0.7;
            }}
            .axis {{
                font-size: 12px;
            }}
            .grid line {{
                stroke: #e0e0e0;
                stroke-dasharray: 3,3;
            }}
            .grid path {{
                stroke-width: 0;
            }}
            .target-line {{
                stroke: #52c41a;
                stroke-width: 3;
                stroke-dasharray: 5,5;
                opacity: 0.8;
            }}
            .value-label {{
                font-size: 14px;
                font-weight: bold;
                text-anchor: middle;
            }}
            .title {{
                font-size: 18px;
                font-weight: bold;
                text-anchor: middle;
            }}
            .drag-hint {{
                font-size: 12px;
                fill: #ff4d4f;
                text-anchor: middle;
                font-weight: bold;
            }}
            #submit-btn {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                padding: 10px 20px;
                background: #1890ff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }}
            #submit-btn:hover {{
                background: #40a9ff;
            }}
            .feedback {{
                position: absolute;
                top: 20px;
                right: 20px;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }}
            .feedback.correct {{
                background: #f6ffed;
                color: #52c41a;
                border: 1px solid #b7eb8f;
            }}
            .feedback.incorrect {{
                background: #fff2e8;
                color: #fa8c16;
                border: 1px solid #ffbb96;
            }}
            .arrow {{
                fill: #ff4d4f;
            }}
        </style>
    </head>
    <body>
        <div id="chart"></div>
        <div id="feedback" class="feedback" style="display: none;"></div>
        <button id="submit-btn" onclick="submitAnswer()">Check Answer</button>
        
        <script>
            // Data
            const data = {chart_data_json};
            const maxValue = {max_value};
            const stepSize = {step_size};
            
            // Dimensions
            const margin = {{top: 60, right: 40, bottom: 60, left: 60}};
            const width = 700 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;
            
            // Create SVG
            const svg = d3.select("#chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
            
            // Title
            svg.append("text")
                .attr("class", "title")
                .attr("x", width / 2)
                .attr("y", -30)
                .text("{title}");
            
            // Scales
            const x = d3.scaleBand()
                .range([0, width])
                .domain(data.map(d => d.category))
                .padding(0.2);
            
            const y = d3.scaleLinear()
                .range([height, 0])
                .domain([0, maxValue]);
            
            // Grid
            svg.append("g")
                .attr("class", "grid")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x)
                    .tickSize(-height)
                    .tickFormat("")
                );
            
            svg.append("g")
                .attr("class", "grid")
                .call(d3.axisLeft(y)
                    .tickSize(-width)
                    .tickFormat("")
                    .ticks(maxValue / stepSize)
                );
            
            // X axis
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x))
                .append("text")
                .attr("x", width / 2)
                .attr("y", 40)
                .style("text-anchor", "middle")
                .style("fill", "black")
                .text("{x_label}");
            
            // Y axis
            svg.append("g")
                .call(d3.axisLeft(y).ticks(maxValue / stepSize))
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", -40)
                .attr("x", -height / 2)
                .style("text-anchor", "middle")
                .style("fill", "black")
                .text("{y_label} ({unit})");
            
            // Target lines for draggable bars
            const targetLines = svg.selectAll(".target-line")
                .data(data.filter(d => d.isDraggable))
                .enter().append("line")
                .attr("class", "target-line")
                .attr("x1", d => x(d.category))
                .attr("x2", d => x(d.category) + x.bandwidth())
                .attr("y1", d => y(d.targetValue))
                .attr("y2", d => y(d.targetValue));
            
            // Add labels for target values
            svg.selectAll(".target-label")
                .data(data.filter(d => d.isDraggable))
                .enter().append("text")
                .attr("x", d => x(d.category) + x.bandwidth() + 5)
                .attr("y", d => y(d.targetValue))
                .attr("dy", "0.3em")
                .style("font-size", "12px")
                .style("fill", "#52c41a")
                .text(d => "Target: " + d.targetValue);
            
            // Bars
            const bars = svg.selectAll(".bar")
                .data(data)
                .enter().append("rect")
                .attr("class", d => d.isDraggable ? "bar draggable" : "bar")
                .attr("x", d => x(d.category))
                .attr("width", x.bandwidth())
                .attr("y", d => y(d.value))
                .attr("height", d => height - y(d.value))
                .attr("fill", d => {{
                    if (!d.isDraggable) return "#1890ff";
                    return d.value === d.targetValue ? "#52c41a" : "#ff4d4f";
                }});
            
            // Add drag hints for draggable bars
            const dragHints = svg.selectAll(".drag-hint")
                .data(data.filter(d => d.isDraggable))
                .enter().append("text")
                .attr("class", "drag-hint")
                .attr("x", d => x(d.category) + x.bandwidth() / 2)
                .attr("y", d => y(d.value) - 25)
                .text("↕ Drag me!");
            
            // Value labels
            const labels = svg.selectAll(".value-label")
                .data(data)
                .enter().append("text")
                .attr("class", "value-label")
                .attr("x", d => x(d.category) + x.bandwidth() / 2)
                .attr("y", d => y(d.value) - 5)
                .text(d => d.value);
            
            // Drag behavior
            const drag = d3.drag()
                .on("start", function(event, d) {{
                    if (!d.isDraggable) return;
                    d3.select(this).style("opacity", 0.6);
                    // Hide drag hint when dragging starts
                    dragHints.filter(h => h.index === d.index)
                        .style("display", "none");
                }})
                .on("drag", function(event, d) {{
                    if (!d.isDraggable) return;
                    
                    // Calculate new value
                    let newY = Math.max(0, Math.min(height, event.y));
                    let newValue = Math.round(y.invert(newY) / stepSize) * stepSize;
                    newValue = Math.max(0, Math.min(maxValue, newValue));
                    
                    // Update data
                    d.value = newValue;
                    
                    // Update bar
                    d3.select(this)
                        .attr("y", y(newValue))
                        .attr("height", height - y(newValue))
                        .attr("fill", newValue === d.targetValue ? "#52c41a" : "#ff4d4f");
                    
                    // Update label
                    labels.filter(l => l.index === d.index)
                        .attr("y", y(newValue) - 5)
                        .text(newValue);
                    
                    // Update drag hint position
                    dragHints.filter(h => h.index === d.index)
                        .attr("y", y(newValue) - 25);
                }})
                .on("end", function(event, d) {{
                    if (!d.isDraggable) return;
                    d3.select(this).style("opacity", 1);
                    
                    // Show drag hint again if not correct
                    if (d.value !== d.targetValue) {{
                        dragHints.filter(h => h.index === d.index)
                            .style("display", "block");
                    }}
                    
                    // Store the value
                    window.currentValues = window.currentValues || {{}};
                    window.currentValues[d.index] = d.value;
                }});
            
            bars.call(drag);
            
            // Submit function
            window.submitAnswer = function() {{
                const results = {{}};
                let allCorrect = true;
                
                data.forEach(d => {{
                    if (d.isDraggable) {{
                        results[d.index] = {{
                            value: d.value,
                            target: d.targetValue,
                            correct: d.value === d.targetValue
                        }};
                        if (d.value !== d.targetValue) {{
                            allCorrect = false;
                        }}
                    }}
                }});
                
                // Show feedback
                const feedback = document.getElementById('feedback');
                if (allCorrect) {{
                    feedback.className = 'feedback correct';
                    feedback.textContent = '✅ Perfect! All bars are correct!';
                }} else {{
                    feedback.className = 'feedback incorrect';
                    feedback.textContent = '❌ Some bars need adjustment. Check the green dotted lines!';
                }}
                feedback.style.display = 'block';
                
                // Send results to Streamlit
                window.parent.postMessage({{
                    type: 'submit',
                    results: results,
                    allCorrect: allCorrect
                }}, '*');
            }};
            
            // Initialize current values
            window.currentValues = {{}};
            data.forEach(d => {{
                if (d.isDraggable) {{
                    window.currentValues[d.index] = d.value;
                }}
            }});
        </script>
    </body>
    </html>
    """.format(
        chart_data_json=json.dumps(chart_data),
        max_value=settings['max_value'],
        step_size=settings['step_size'],
        title=context['title'],
        x_label=context.get('x_label', 'Category'),
        y_label=context.get('y_label', 'Value'),
        unit=context['unit']
    )
    
    return html_code

def display_create_bar_problem():
    """Display the bar graph creation interface"""
    problem = st.session_state.current_create_bar_problem
    data = problem["data"]
    
    # Display description
    st.markdown(f"### {data['description']}")
    st.markdown(problem['instruction'])
    st.info(f"💡 {problem['hint']}")
    
    # Create and display the draggable chart
    html_code = create_draggable_bar_chart(problem)
    
    # Display the interactive component
    components.html(html_code, height=500, scrolling=False)
    
    # Show current status
    if not st.session_state.graph_submitted:
        st.markdown("---")
        st.markdown("### Current Progress:")
        
        cols = st.columns(len(data["missing_indices"]))
        for i, idx in enumerate(sorted(data["missing_indices"])):
            with cols[i]:
                current = st.session_state.current_values.get(idx, 0)
                target = data["values"][idx]
                
                if current == target:
                    st.success(f"✅ {data['categories'][idx]}")
                else:
                    st.warning(f"🔄 {data['categories'][idx]}")
                
                st.caption(f"Target: {target} {data['context']['unit']}")
    
    # Manual submit button (since we can't easily get data back from iframe)
    if not st.session_state.graph_submitted:
        st.markdown("---")
        st.markdown("### Check Your Answer:")
        st.markdown("After adjusting all bars in the graph above, enter the values you set:")
        
        cols = st.columns(len(data["missing_indices"]))
        for i, idx in enumerate(sorted(data["missing_indices"])):
            with cols[i]:
                value = st.number_input(
                    f"{data['categories'][idx]}:",
                    min_value=0,
                    max_value=problem["settings"]["max_value"],
                    value=st.session_state.current_values.get(idx, problem["settings"]["step_size"]),
                    step=problem["settings"]["step_size"],
                    key=f"input_{idx}"
                )
                st.session_state.current_values[idx] = value
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Answer", type="primary", use_container_width=True):
                check_create_bar_answer()
                st.rerun()
    
    # Show feedback
    if st.session_state.graph_submitted:
        display_create_bar_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Graph", type="primary", use_container_width=True):
                generate_create_bar_problem()
                st.rerun()

def check_create_bar_answer():
    """Check if the created bar graph is correct"""
    problem = st.session_state.current_create_bar_problem
    data = problem["data"]
    
    st.session_state.create_bar_total_attempts += 1
    
    # Check each missing bar
    all_correct = True
    errors = []
    
    for missing_idx in data["missing_indices"]:
        correct_val = data["values"][missing_idx]
        user_val = st.session_state.current_values.get(missing_idx, 0)
        
        if user_val != correct_val:
            all_correct = False
            errors.append({
                "category": data["categories"][missing_idx],
                "user_value": user_val,
                "correct_value": correct_val
            })
    
    st.session_state.current_create_bar_problem["errors"] = errors
    
    if all_correct:
        st.session_state.create_bar_total_score += 1
        st.session_state.create_bar_consecutive_correct += 1
        st.session_state.create_bar_consecutive_wrong = 0
        
        if (st.session_state.create_bar_consecutive_correct >= 3 and 
            st.session_state.create_bar_difficulty < 6):
            st.session_state.create_bar_difficulty += 1
            st.session_state.create_bar_consecutive_correct = 0
    else:
        st.session_state.create_bar_consecutive_wrong += 1
        st.session_state.create_bar_consecutive_correct = 0
        
        if (st.session_state.create_bar_consecutive_wrong >= 3 and 
            st.session_state.create_bar_difficulty > 1):
            st.session_state.create_bar_difficulty -= 1
            st.session_state.create_bar_consecutive_wrong = 0
    
    st.session_state.graph_submitted = True

def display_create_bar_feedback():
    """Display feedback after submission"""
    problem = st.session_state.current_create_bar_problem
    errors = problem.get("errors", [])
    data = problem["data"]
    context = data["context"]
    
    if not errors:
        st.success("✅ Perfect! You completed the bar graph correctly!")
        
        if st.session_state.create_bar_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Excellent work! {st.session_state.create_bar_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.create_bar_consecutive_correct == 0:
            settings = get_create_bar_difficulty_settings()
            st.success(f"🎉 Level Up! Now working on: {settings['label']}!")
    else:
        st.error("❌ Not quite right. Let's check the bars that need adjustment.")
        
        # Show specific errors
        with st.expander("📊 See what needs to be fixed", expanded=True):
            for error in errors:
                st.markdown(f"**{error['category']}:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.error(f"Your value: {error['user_value']} {context['unit']}")
                with col2:
                    st.success(f"Correct: {error['correct_value']} {context['unit']}")
                with col3:
                    difference = error['correct_value'] - error['user_value']
                    if difference > 0:
                        st.info(f"↑ Add {difference}")
                    else:
                        st.info(f"↓ Subtract {abs(difference)}")
            
            st.markdown("---")
            st.markdown("**Remember:**")
            st.markdown("- Check the problem description carefully")
            st.markdown("- Make sure values match exactly")
            st.markdown("- Use the grid lines to align bars properly")
            st.markdown(f"- Values should be in steps of {problem['settings']['step_size']}")
        
        # Level down message
        if st.session_state.create_bar_consecutive_wrong == 0:
            settings = get_create_bar_difficulty_settings()
            st.warning(f"📉 Moving to easier graphs: {settings['label']}")

def clear_create_bar_state():
    """Clear all create bar graph related session state"""
    for key in list(st.session_state.keys()):
        if key.startswith('create_bar_') or key in ['current_create_bar_problem', 'current_values', 'graph_submitted']:
            del st.session_state[key]