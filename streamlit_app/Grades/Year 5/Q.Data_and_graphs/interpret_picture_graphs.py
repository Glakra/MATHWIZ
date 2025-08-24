import streamlit as st
import random
import math

def run():
    """
    Main function to run the Interpret Picture Graphs activity.
    Students read and interpret data from pictographs with various symbols and scales.
    """
    # Initialize session state
    if "pictograph_difficulty" not in st.session_state:
        st.session_state.pictograph_difficulty = 1
        st.session_state.pictograph_consecutive_correct = 0
        st.session_state.pictograph_consecutive_wrong = 0
        st.session_state.pictograph_total_score = 0
        st.session_state.pictograph_total_attempts = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.show_feedback = False
    
    if "current_pictograph_problem" not in st.session_state:
        generate_pictograph_problem()
    
    # Page header
    st.markdown("**📚 Year 5 > K. Data and graphs**")
    st.title("📊 Interpret Picture Graphs")
    st.markdown("*Count the symbols to find the values in picture graphs*")
    st.markdown("---")
    
    # Display progress
    display_pictograph_progress()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            clear_pictograph_state()
            st.query_params.clear()
            st.rerun()
    
    # Display the problem
    display_pictograph_problem()
    
    # Instructions
    with st.expander("💡 **How to Read Picture Graphs**", expanded=False):
        st.markdown("""
        ### Understanding Picture Graphs:
        1. **Look at the legend** - It tells you what each symbol represents
        2. **Count the symbols** in the row for your answer
        3. **Multiply** the number of symbols by the value per symbol
        4. **Watch for partial symbols** - Half symbols mean half the value
        
        ### Example:
        If each 🍎 = 5 apples and you see 3 full apples and 1 half apple:
        - 3 × 5 = 15 (for full apples)
        - 0.5 × 5 = 2.5 (for half apple)
        - Total = 15 + 2.5 = 17.5 apples
        
        ### Tips:
        - Count carefully - don't miss any symbols
        - Pay attention to the legend value
        - Check if there are partial symbols
        - Double-check your multiplication
        """)

def get_pictograph_difficulty_settings():
    """Get settings based on current difficulty level"""
    difficulty = st.session_state.pictograph_difficulty
    
    settings = {
        1: {
            "max_symbols": 5,
            "value_per_symbol": 1,
            "use_partial": False,
            "num_categories": 3,
            "label": "Basic - Each symbol = 1",
            "color": "🟢"
        },
        2: {
            "max_symbols": 8,
            "value_per_symbol": random.choice([1, 2]),
            "use_partial": False,
            "num_categories": 4,
            "label": "Simple Multiplication",
            "color": "🟡"
        },
        3: {
            "max_symbols": 6,
            "value_per_symbol": random.choice([2, 5]),
            "use_partial": False,
            "num_categories": 4,
            "label": "Larger Values",
            "color": "🟠"
        },
        4: {
            "max_symbols": 8,
            "value_per_symbol": random.choice([5, 10]),
            "use_partial": True,
            "num_categories": 4,
            "label": "With Half Symbols",
            "color": "🔴"
        },
        5: {
            "max_symbols": 6,
            "value_per_symbol": random.choice([10, 20, 25]),
            "use_partial": True,
            "num_categories": 5,
            "label": "Large Scale Values",
            "color": "🟣"
        },
        6: {
            "max_symbols": 8,
            "value_per_symbol": random.choice([50, 100, 200]),
            "use_partial": True,
            "num_categories": 5,
            "label": "Complex Graphs",
            "color": "⚫"
        }
    }
    
    return settings.get(difficulty, settings[1])

def display_pictograph_progress():
    """Display current level and progress"""
    settings = get_pictograph_difficulty_settings()
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Level", f"{settings['color']} {st.session_state.pictograph_difficulty}/6")
    
    with col2:
        st.metric("Graph Type", settings['label'])
    
    with col3:
        if st.session_state.pictograph_total_attempts > 0:
            accuracy = (st.session_state.pictograph_total_score / st.session_state.pictograph_total_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
    
    with col4:
        st.metric("Streak", f"🔥 {st.session_state.pictograph_consecutive_correct}")

def generate_graph_data(settings):
    """Generate data for the pictograph based on difficulty"""
    themes = [
        {
            "title": "People per television",
            "categories": ["Ukraine", "Japan", "Spain", "South Korea", "China"],
            "symbol": "👤",
            "unit": "people",
            "question_template": "How many people per television are there in {category}?"
        },
        {
            "title": "Baskets made",
            "categories": ["Justine", "Chloe", "Alice", "Marcus", "Tyler"],
            "symbol": "🏀",
            "unit": "baskets",
            "question_template": "How many baskets did {category} make?"
        },
        {
            "title": "Favourite sports",
            "categories": ["Running", "Volleyball", "Tennis", "Soccer", "Basketball"],
            "symbol": "👟",
            "unit": "children",
            "question_template": "How many children chose {category} as their favourite sport?"
        },
        {
            "title": "Lifespans of animals",
            "categories": ["Flying squirrel", "Porcupine", "Blackbird", "Lion", "Cow", "Pigeon"],
            "symbol": "⏰",
            "unit": "years",
            "question_template": "What is the lifespan of a {category}?"
        },
        {
            "title": "Web pages visited",
            "categories": ["Avery", "Carmen", "Rosanne", "David", "Emma"],
            "symbol": "📁",
            "unit": "web pages",
            "question_template": "How many web pages did {category} visit?"
        },
        {
            "title": "Average millimetres of rainfall in Seattle",
            "categories": ["April", "May", "June", "July", "August", "September"],
            "symbol": "💧",
            "unit": "millimetres",
            "question_template": "What is the average rainfall in {category}?"
        },
        {
            "title": "Favourite Winter Olympics sports",
            "categories": ["Luge", "Figure skating", "Ski jumping", "Hockey", "Curling"],
            "symbol": "❄️",
            "unit": "children",
            "question_template": "How many children chose {category} as their favourite?"
        },
        {
            "title": "Reading competition results",
            "categories": ["Juan", "Gwen", "Erica", "Caleb", "Maya"],
            "symbol": "📚",
            "unit": "books",
            "question_template": "How many books did {category} read?"
        },
        {
            "title": "Kilometres biked",
            "categories": ["Celine", "Percy", "Xavier", "Julia", "Andre"],
            "symbol": "🚲",
            "unit": "kilometres",
            "question_template": "How many kilometres did {category} bike?"
        },
        {
            "title": "Cookies sold at bake sale",
            "categories": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "symbol": "🍪",
            "unit": "cookies",
            "question_template": "How many cookies were sold on {category}?"
        },
        {
            "title": "Trees planted",
            "categories": ["Oak", "Pine", "Maple", "Birch", "Willow"],
            "symbol": "🌳",
            "unit": "trees",
            "question_template": "How many {category} trees were planted?"
        },
        {
            "title": "Minutes of exercise",
            "categories": ["Sarah", "Tom", "Lisa", "Mike", "Anna"],
            "symbol": "⏱️",
            "unit": "minutes",
            "question_template": "How many minutes did {category} exercise?"
        }
    ]
    
    # Select theme
    theme = random.choice(themes)
    
    # Use specified number of categories
    categories = theme["categories"][:settings["num_categories"]]
    
    # Generate symbol counts for each category
    data = {}
    for category in categories:
        if settings["use_partial"]:
            # Can have 0.5 symbols
            full_symbols = random.randint(0, settings["max_symbols"] - 1)
            has_half = random.choice([True, False])
            symbol_count = full_symbols + (0.5 if has_half else 0)
        else:
            symbol_count = random.randint(1, settings["max_symbols"])
        
        data[category] = {
            "symbol_count": symbol_count,
            "value": symbol_count * settings["value_per_symbol"]
        }
    
    # Select which category to ask about
    target_category = random.choice(categories)
    question = theme["question_template"].format(category=target_category)
    correct_answer = data[target_category]["value"]
    
    return {
        "theme": theme,
        "categories": categories,
        "data": data,
        "target_category": target_category,
        "question": question,
        "correct_answer": correct_answer,
        "value_per_symbol": settings["value_per_symbol"]
    }

def generate_pictograph_problem():
    """Generate a new pictograph interpretation problem"""
    settings = get_pictograph_difficulty_settings()
    graph_data = generate_graph_data(settings)
    
    st.session_state.current_pictograph_problem = {
        "settings": settings,
        "graph_data": graph_data
    }
    
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    st.session_state.show_feedback = False

def display_pictograph(problem):
    """Display the pictograph using Streamlit components"""
    graph_data = problem["graph_data"]
    theme = graph_data["theme"]
    
    # Title with colored background
    st.markdown(
        f"""
        <div style='background-color: #ffe6e6; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <h3 style='text-align: center; margin: 0;'>{theme['title']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create the pictograph using columns
    for category in graph_data["categories"]:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"**{category}**")
        
        with col2:
            symbol_count = graph_data["data"][category]["symbol_count"]
            full_symbols = int(symbol_count)
            has_half = (symbol_count % 1) == 0.5
            
            # Display symbols
            symbol_string = ""
            for _ in range(full_symbols):
                symbol_string += f"{theme['symbol']} "
            
            if has_half:
                # Add a lighter/smaller half symbol
                symbol_string += f"◗"  # Using a half-circle as a generic half symbol
            
            st.markdown(f"<span style='font-size: 30px;'>{symbol_string}</span>", unsafe_allow_html=True)
    
    # Legend
    st.markdown("---")
    value_per = graph_data["value_per_symbol"]
    legend_text = f"**Each {theme['symbol']} = {value_per} {theme['unit']}**"
    
    if problem["settings"]["use_partial"]:
        half_value = value_per / 2
        if half_value == int(half_value):
            half_value = int(half_value)
        legend_text += f"\n\nEach ◗ = {half_value} {theme['unit']}"
    
    st.info(legend_text)

def display_pictograph_problem():
    """Display the current pictograph problem"""
    problem = st.session_state.current_pictograph_problem
    graph_data = problem["graph_data"]
    
    # Display the instruction
    st.markdown("### Look at this picture graph:")
    
    # Display the pictograph
    with st.container():
        display_pictograph(problem)
    
    # Display the question
    st.markdown(f"### {graph_data['question']}")
    
    # Answer input
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col2:
            # Determine if answer should be integer or allow decimals
            if problem["settings"]["use_partial"] and graph_data["value_per_symbol"] % 2 != 0:
                step = 0.5
            else:
                step = 1.0
            
            user_answer = st.number_input(
                f"{graph_data['theme']['unit']}",
                min_value=0.0,
                max_value=1000.0,
                step=step,
                format="%.1f" if step == 0.5 else "%.0f",
                key="pictograph_answer_input"
            )
            
            if st.button("Submit", type="primary", use_container_width=True):
                st.session_state.user_answer = user_answer
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
                check_pictograph_answer()
                st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        display_pictograph_feedback()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Question", type="primary", use_container_width=True):
                generate_pictograph_problem()
                st.rerun()

def check_pictograph_answer():
    """Check if the answer is correct"""
    problem = st.session_state.current_pictograph_problem
    correct_answer = problem["graph_data"]["correct_answer"]
    user_answer = st.session_state.user_answer
    
    st.session_state.pictograph_total_attempts += 1
    
    # Allow for floating point comparison
    is_correct = abs(user_answer - correct_answer) < 0.01
    
    if is_correct:
        st.session_state.pictograph_total_score += 1
        st.session_state.pictograph_consecutive_correct += 1
        st.session_state.pictograph_consecutive_wrong = 0
        
        # Check for level up
        if (st.session_state.pictograph_consecutive_correct >= 3 and 
            st.session_state.pictograph_difficulty < 6):
            st.session_state.pictograph_difficulty += 1
            st.session_state.pictograph_consecutive_correct = 0
    else:
        st.session_state.pictograph_consecutive_wrong += 1
        st.session_state.pictograph_consecutive_correct = 0
        
        # Check for level down
        if (st.session_state.pictograph_consecutive_wrong >= 3 and 
            st.session_state.pictograph_difficulty > 1):
            st.session_state.pictograph_difficulty -= 1
            st.session_state.pictograph_consecutive_wrong = 0

def display_pictograph_feedback():
    """Display feedback after answer submission"""
    problem = st.session_state.current_pictograph_problem
    graph_data = problem["graph_data"]
    correct_answer = graph_data["correct_answer"]
    user_answer = st.session_state.user_answer
    
    is_correct = abs(user_answer - correct_answer) < 0.01
    
    if is_correct:
        st.success("✅ Correct! Well done!")
        
        if st.session_state.pictograph_consecutive_correct >= 2:
            st.balloons()
            st.info(f"🎉 Fantastic! {st.session_state.pictograph_consecutive_correct} correct in a row!")
        
        # Level up message
        if st.session_state.pictograph_consecutive_correct == 0:
            settings = get_pictograph_difficulty_settings()
            st.success(f"🎉 Level Up! Now working on: {settings['label']}!")
    else:
        st.error(f"❌ Not quite. The correct answer is {correct_answer} {graph_data['theme']['unit']}.")
        
        # Show explanation
        with st.expander("📊 See how to solve this", expanded=True):
            target = graph_data["target_category"]
            symbol_count = graph_data["data"][target]["symbol_count"]
            value_per = graph_data["value_per_symbol"]
            
            st.markdown(f"**Step-by-step solution:**")
            st.markdown(f"1. Find **{target}** in the graph")
            
            if symbol_count == int(symbol_count):
                st.markdown(f"2. Count the symbols: **{int(symbol_count)}** {graph_data['theme']['symbol']}")
                st.markdown(f"3. Each {graph_data['theme']['symbol']} = **{value_per}** {graph_data['theme']['unit']}")
                st.markdown(f"4. Calculate: {int(symbol_count)} × {value_per} = **{correct_answer}**")
            else:
                full = int(symbol_count)
                st.markdown(f"2. Count the symbols: **{full}** full {graph_data['theme']['symbol']} and **1** half ◗")
                st.markdown(f"3. Each full {graph_data['theme']['symbol']} = **{value_per}** {graph_data['theme']['unit']}")
                st.markdown(f"4. Each half ◗ = **{value_per/2}** {graph_data['theme']['unit']}")
                st.markdown(f"5. Calculate: ({full} × {value_per}) + (0.5 × {value_per}) = {full * value_per} + {value_per/2} = **{correct_answer}**")
        
        # Level down message
        if st.session_state.pictograph_consecutive_wrong == 0:
            settings = get_pictograph_difficulty_settings()
            st.warning(f"📉 Moving to easier graphs: {settings['label']}")

def clear_pictograph_state():
    """Clear all pictograph related session state"""
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith('pictograph_') or 
                     k in ['current_pictograph_problem', 'answer_submitted', 'user_answer', 'show_feedback']]
    for key in keys_to_clear:
        del st.session_state[key]