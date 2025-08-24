import streamlit as st
import random
import math

def run():
    """
    Main function to run the Create Picture Graphs activity.
    Students create pictographs by clicking to add/remove icons based on given data.
    """
    # Initialize session state
    if "create_pictograph_difficulty" not in st.session_state:
        st.session_state.create_pictograph_difficulty = 1
        st.session_state.create_pictograph_consecutive_correct = 0
        st.session_state.create_pictograph_consecutive_wrong = 0
        st.session_state.create_pictograph_total_score = 0
        st.session_state.create_pictograph_total_attempts = 0
        st.session_state.answer_submitted = False
        st.session_state.current_icons = {}
        st.session_state.show_feedback = False
    
    if "current_create_pictograph_problem" not in st.session_state:
        generate_create_pictograph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("🎨 Create Picture Graphs")
    st.markdown("*Click the icons to create a pictograph from the given data*")
    st.markdown("---")
    
    # Display progress
    display_create_pictograph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_create_pictograph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_create_pictograph_problem()
    
    # Instructions
    with st.expander("💡 **How to Create Picture Graphs**", expanded=False):
        st.markdown("""
        ### Creating Picture Graphs:
        1. **Read the data** carefully - either from a table or description
        2. **Check the legend** - see how many items each icon represents
        3. **Calculate** how many icons you need
        4. **Click the icons** to add them to each row
        5. **Gray icons** are placeholders - click to activate them
        
        ### Example:
        If you need to show 15 items and each icon = 5 items:
        - 15 ÷ 5 = 3 icons needed
        - Click 3 gray icons to turn them into colored icons
        
        ### Tips:
        - Count your data carefully
        - Remember what each icon represents
        - Click active icons again to deactivate them
        - Make sure your total matches the data exactly
        """)

def get_create_pictograph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.create_pictograph_difficulty
    
    settings = {
        1: {
            "max_value": 25,
            "value_per_icon": 5,
            "num_categories": 3,
            "missing_rows": 1,
            "data_format": "table",
            "label": "Basic - Single Row",
            "color": "🟢"
        },
        2: {
            "max_value": 40,
            "value_per_icon": random.choice([5, 10]),
            "num_categories": 4,
            "missing_rows": 2,
            "data_format": "table",
            "label": "Two Rows",
            "color": "🟡"
        },
        3: {
            "max_value": 50,
            "value_per_icon": 10,
            "num_categories": 5,
            "missing_rows": 3,
            "data_format": "mixed",
            "label": "Multiple Rows",
            "color": "🟠"
        },
        4: {
            "max_value": 100,
            "value_per_icon": random.choice([10, 20]),
            "num_categories": 5,
            "missing_rows": 4,
            "data_format": "description",
            "label": "From Description",
            "color": "🔴"
        },
        5: {
            "max_value": 200,
            "value_per_icon": random.choice([20, 25, 50]),
            "num_categories": 6,
            "missing_rows": 5,
            "data_format": "mixed",
            "label": "Large Values",
            "color": "🟣"
        },
        6: {
            "max_value": 500,
            "value_per_icon": random.choice([50, 100]),
            "num_categories": 6,
            "missing_rows": 6,
            "data_format": "mixed",
            "label": "Complex Graphs",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_create_pictograph_progress():
    """Display current level and progress"""
    settings = get_create_pictograph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.create_pictograph_difficulty}/6")
    
    with col2:
        st.metric("Task Type", settings['label'])
    
    with col3:
        if st.session_state.create_pictograph_total_attempts > 0:
            accuracy = (st.session_state.create_pictograph_total_score / st.session_state.create_pictograph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.create_pictograph_consecutive_correct}")

def generate_graph_scenario(settings):
    """Generate a scenario for the pictograph"""
    scenarios = [
        {
            "title": "Car sales last week",
            "categories": ["Smith Family Cars", "Eastside Cars", "Checkers Cars", "Downtown Cars", "City Cars", "Metro Cars"],
            "icon": "🚗",
            "unit": "cars",
            "context": "car dealership sales"
        },
        {
            "title": "Can recycling drive",
            "categories": ["Charlotte", "Dave", "Neil", "Bryan", "Clara", "Emma"],
            "icon": "🥤",
            "unit": "cans",
            "context": "recycling competition"
        },
        {
            "title": "Pumpkin carving competition",
            "categories": ["Oliver", "Colette", "Nate", "Isabella", "Sofia", "Max"],
            "icon": "🎃",
            "unit": "votes",
            "context": "competition votes"
        },
        {
            "title": "Favourite Summer Olympics sports",
            "categories": ["soccer", "gymnastics", "basketball", "volleyball", "swimming", "track"],
            "icon": "👟",
            "unit": "children",
            "context": "sports preference"
        },
        {
            "title": "Favourite Winter Olympics sports",
            "categories": ["snowboarding", "luge", "cross-country skiing", "figure skating", "downhill skiing", "ski jumping"],
            "icon": "❄️",
            "unit": "children",
            "context": "winter sports preference"
        },
        {
            "title": "House sales last year",
            "categories": ["New Hamburg", "Brampton", "Melville", "Centre City", "Parkville", "Oakwood"],
            "icon": "🏠",
            "unit": "houses",
            "context": "real estate sales"
        },
        {
            "title": "Times on an aeroplane",
            "categories": ["Carla", "Grayson", "Jill", "Eduardo", "Marcy", "Erik"],
            "icon": "✈️",
            "unit": "times",
            "context": "travel frequency"
        },
        {
            "title": "U.S. Representatives",
            "categories": ["Alabama", "Mississippi", "Utah", "Delaware", "Minnesota", "Tennessee"],
            "icon": "👤",
            "unit": "representatives",
            "context": "government representation"
        },
        {
            "title": "Daily flights out of the city airport",
            "categories": ["Boston", "New York City", "Nashville", "Los Angeles", "Dallas", "Philadelphia"],
            "icon": "✈️",
            "unit": "flights",
            "context": "airport traffic"
        },
        {
            "title": "Books read this summer",
            "categories": ["Emma", "Jake", "Sophie", "Liam", "Olivia", "Noah"],
            "icon": "📚",
            "unit": "books",
            "context": "reading challenge"
        },
        {
            "title": "Pizzas sold last week",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "icon": "🍕",
            "unit": "pizzas",
            "context": "restaurant sales"
        },
        {
            "title": "Trees planted",
            "categories": ["Oak Grove", "Pine Valley", "Maple Park", "Birch Lane", "Willow Creek", "Cedar Hills"],
            "icon": "🌳",
            "unit": "trees",
            "context": "environmental project"
        }
    ]
    
    return random.choice(scenarios)

def generate_data_values(scenario, settings):
    """Generate data values for the scenario"""
    categories = scenario["categories"][:settings["num_categories"]]
    data = {}
    
    for category in categories:
        # Generate value that's a multiple of value_per_icon
        multiplier = random.randint(1, settings["max_value"] // settings["value_per_icon"])
        value = multiplier * settings["value_per_icon"]
        data[category] = value
    
    # Select which rows will be missing (need to be completed)
    all_indices = list(range(len(categories)))
    missing_indices = random.sample(all_indices, min(settings["missing_rows"], len(categories)))
    
    return {
        "categories": categories,
        "values": data,
        "missing_indices": missing_indices
    }

def create_data_description(scenario, data, settings):
    """Create a text description of the data"""
    descriptions = []
    categories = data["categories"]
    values = data["values"]
    
    if scenario["context"] == "car dealership sales":
        for cat in categories:
            descriptions.append(f"{cat} sold {values[cat]} {scenario['unit']}")
    
    elif scenario["context"] == "recycling competition":
        parts = []
        for i, cat in enumerate(categories[:-1]):
            parts.append(f"{cat} recycled {values[cat]} {scenario['unit']}")
        final_part = f"{categories[-1]} recycled {values[categories[-1]]} {scenario['unit']}"
        descriptions.append(f"At a can recycling drive, {', '.join(parts)}, and {final_part}.")
    
    elif scenario["context"] == "competition votes":
        for cat in categories:
            descriptions.append(f"{cat}: {values[cat]} {scenario['unit']}")
    
    elif "sports" in scenario["context"]:
        for cat in categories:
            descriptions.append(f"{values[cat]} {scenario['unit']} chose {cat}")
    
    elif scenario["context"] == "real estate sales":
        parts = []
        for cat in categories[:-1]:
            parts.append(f"{values[cat]} houses were sold in {cat}")
        final_part = f"{values[categories[-1]]} in {categories[-1]}"
        descriptions.append(f"Last year, {', '.join(parts)}, and {final_part}.")
    
    elif scenario["context"] == "travel frequency":
        for cat in categories:
            descriptions.append(f"{cat} has been on an aeroplane {values[cat]} {scenario['unit']}")
    
    elif scenario["context"] == "government representation":
        states_data = []
        for cat in categories:
            rep_count = values[cat] // settings["value_per_icon"]
            states_data.append(f"{cat} has {rep_count} representatives")
        all_but_last = ", ".join(states_data[:-1])
        descriptions.append(f"{all_but_last}, and {states_data[-1]}.")
    
    elif scenario["context"] == "airport traffic":
        for cat in categories:
            descriptions.append(f"{cat}: {values[cat]} {scenario['unit']}")
    
    else:
        for cat in categories:
            descriptions.append(f"{cat}: {values[cat]} {scenario['unit']}")
    
    return " ".join(descriptions) if len(descriptions) > 1 else descriptions[0]

def generate_create_pictograph_problem():
    """Generate a new create pictograph problem"""
    settings = get_create_pictograph_difficulty_settings()
    scenario = generate_graph_scenario(settings)
    data = generate_data_values(scenario, settings)
    
    # Initialize current icons state
    st.session_state.current_icons = {}
    for i, cat in enumerate(data["categories"]):
        if i in data["missing_indices"]:
            st.session_state.current_icons[cat] = 0
        else:
            st.session_state.current_icons[cat] = data["values"][cat] // settings["value_per_icon"]
    
    problem = {
        "settings": settings,
        "scenario": scenario,
        "data": data,
        "description": create_data_description(scenario, data, settings)
    }
    
    st.session_state.current_create_pictograph_problem = problem
    st.session_state.answer_submitted = False
    st.session_state.show_feedback = False

def display_data_table(problem):
    """Display the data in table format"""
    data = problem["data"]
    scenario = problem["scenario"]
    settings = problem["settings"]
    
    if settings["data_format"] == "table":
        # Create a simple table
        st.markdown(f"### {scenario['title']}")
        
        # Table header
        cols = st.columns([1, 1])
        with cols[0]:
            st.markdown("**Name**")
        with cols[1]:
            st.markdown(f"**{scenario['unit'].capitalize()}**")
        
        # Table rows
        for cat in data["categories"]:
            cols = st.columns([1, 1])
            with cols[0]:
                st.markdown(cat)
            with cols[1]:
                st.markdown(str(data["values"][cat]))
    
    elif settings["data_format"] == "description":
        # Show as text description
        st.markdown(f"### {problem['description']}")
    
    else:  # mixed format
        # Randomly choose between table and description
        if random.choice([True, False]):
            # Show table format
            st.markdown(f"### {scenario['title']}")
            
            cols = st.columns([1, 1])
            with cols[0]:
                st.markdown("**Name**")
            with cols[1]:
                st.markdown(f"**{scenario['unit'].capitalize()}**")
            
            for cat in data["categories"]:
                cols = st.columns([1, 1])
                with cols[0]:
                    st.markdown(cat)
                with cols[1]:
                    st.markdown(str(data["values"][cat]))
        else:
            # Show description format
            st.markdown(f"### {problem['description']}")

def create_clickable_pictograph(problem):
    """Create the interactive pictograph interface"""
    scenario = problem["scenario"]
    data = problem["data"]
    settings = problem["settings"]
    
    # Title
    st.markdown(
        f"""
        <div style='background-color: #e6f0ff; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <h3 style='text-align: center; margin: 0;'>{scenario['title']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create the pictograph rows
    max_icons = 10  # Maximum icons to show per row
    
    for i, category in enumerate(data["categories"]):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if i in data["missing_indices"]:
                st.markdown(f"**{category}** ⚡")
            else:
                st.markdown(f"**{category}**")
        
        with col2:
            # Create clickable icons
            icon_cols = st.columns(max_icons)
            current_count = st.session_state.current_icons.get(category, 0)
            
            for j in range(max_icons):
                with icon_cols[j]:
                    if i in data["missing_indices"]:
                        # This is a row that needs to be completed
                        if j < current_count:
                            # Active icon
                            if st.button(scenario["icon"], key=f"icon_{category}_{j}", 
                                       help="Click to remove"):
                                st.session_state.current_icons[category] = current_count - 1
                                st.rerun()
                        else:
                            # Inactive placeholder
                            if st.button("⚪", key=f"icon_{category}_{j}", 
                                       help="Click to add"):
                                st.session_state.current_icons[category] = j + 1
                                st.rerun()
                    else:
                        # This is a completed row (reference)
                        if j < current_count:
                            st.markdown(f"<span style='font-size: 30px;'>{scenario['icon']}</span>", 
                                      unsafe_allow_html=True)
                        else:
                            st.markdown("")
    
    # Legend
    st.markdown("---")
    st.info(f"**Each {scenario['icon']} = {settings['value_per_icon']} {scenario['unit']}**")

def display_create_pictograph_problem():
    """Display the current create pictograph problem"""
    problem = st.session_state.current_create_pictograph_problem
    
    # Instructions
    st.markdown("### Use the data to complete the missing row in the pictograph below.")
    
    # Display the data
    display_data_table(problem)
    
    st.markdown("---")
    st.markdown("### Click to select the icons:")
    st.info("⚡ Rows with lightning bolts need to be completed. Click the circles to add icons!")
    
    # Create the interactive pictograph
    create_clickable_pictograph(problem)
    
    # Submit button
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                check_create_pictograph_answer()
                st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        display_create_pictograph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="primary", use_container_width=True):
                generate_create_pictograph_problem()
                st.rerun()

def check_create_pictograph_answer():
    """Check if the created pictograph is correct"""
    problem = st.session_state.current_create_pictograph_problem
    data = problem["data"]
    settings = problem["settings"]
    
    st.session_state.create_pictograph_total_attempts += 1
    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True
    
    # Check each missing row
    all_correct = True
    errors = []
    
    for i, category in enumerate(data["categories"]):
        if i in data["missing_indices"]:
            expected_icons = data["values"][category] // settings["value_per_icon"]
            actual_icons = st.session_state.current_icons.get(category, 0)
            
            if actual_icons != expected_icons:
                all_correct = False
                errors.append({
                    "category": category,
                    "expected": expected_icons,
                    "actual": actual_icons,
                    "expected_value": data["values"][category],
                    "actual_value": actual_icons * settings["value_per_icon"]
                })
    
    st.session_state.current_create_pictograph_problem["errors"] = errors
    
    if all_correct:
        st.session_state.create_pictograph_total_score += 1
        st.session_state.create_pictograph_consecutive_correct += 1
        st.session_state.create_pictograph_consecutive_wrong = 0
        
        # Check for level up
        if (st.session_state.create_pictograph_consecutive_correct >= 3 and 
            st.session_state.create_pictograph_difficulty < 6):
            st.session_state.create_pictograph_difficulty += 1
            st.session_state.create_pictograph_consecutive_correct = 0
    else:
        st.session_state.create_pictograph_consecutive_wrong += 1
        st.session_state.create_pictograph_consecutive_correct = 0
        
        # Check for level down
        if (st.session_state.create_pictograph_consecutive_wrong >= 3 and 
            st.session_state.create_pictograph_difficulty > 1):
            st.session_state.create_pictograph_difficulty -= 1
            st.session_state.create_pictograph_consecutive_wrong = 0

def display_create_pictograph_feedback():
    """Display feedback after answer submission"""
    problem = st.session_state.current_create_pictograph_problem
    errors = problem.get("errors", [])
    scenario = problem["scenario"]
    settings = problem["settings"]
    
    if not errors:
        st.success("✅ Perfect! You created the pictograph correctly!")
        
        if st.session_state.create_pictograph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Excellent work! {st.session_state.create_pictograph_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.create_pictograph_consecutive_correct == 0:
            new_settings = get_create_pictograph_difficulty_settings()
            st.success(f"🎉 Level Up! Now working on: {new_settings['label']}!")
    else:
        st.error("❌ Not quite right. Let's check the rows that need adjustment.")
        
        # Show specific errors
        with st.expander("📊 See what needs to be fixed", expanded=True):
            for error in errors:
                st.markdown(f"**{error['category']}:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.error(f"You showed: {error['actual']} {scenario['icon']} = {error['actual_value']} {scenario['unit']}")
                
                with col2:
                    st.success(f"Should be: {error['expected']} {scenario['icon']} = {error['expected_value']} {scenario['unit']}")
                
                # Show calculation
                st.markdown(f"**Calculation:** {error['expected_value']} ÷ {settings['value_per_icon']} = {error['expected']} icons")
                st.markdown("---")
            
            st.markdown("**Remember:**")
            st.markdown(f"- Each {scenario['icon']} represents {settings['value_per_icon']} {scenario['unit']}")
            st.markdown("- Divide the total by the icon value to find how many icons you need")
            st.markdown("- Click gray circles to add icons, click colored icons to remove them")
        
        # Level down message
        if st.session_state.create_pictograph_consecutive_wrong == 0:
            new_settings = get_create_pictograph_difficulty_settings()
            st.warning(f"📉 Moving to easier problems: {new_settings['label']}")

def clear_create_pictograph_state():
    """Clear all create pictograph related session state"""
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith('create_pictograph_') or 
                     k in ['current_create_pictograph_problem', 'current_icons', 'answer_submitted', 'show_feedback']]
    for key in keys_to_clear:
        del st.session_state[key]