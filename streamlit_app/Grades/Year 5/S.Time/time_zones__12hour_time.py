import streamlit as st
import random

def run():
    """
    Main function to run the Time Zones - 12-hour time activity.
    This gets called when the subtopic is loaded from the curriculum.
    """
    # Initialize session state for difficulty and game state
    if "time_zone_difficulty" not in st.session_state:
        st.session_state.time_zone_difficulty = 1  # Start with basic scenarios
    
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.scenario_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.show_hint = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("🌍 Time Zones - 12-Hour Time")
    st.markdown("*Convert times between different time zones using A.M./P.M. format*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_zone_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (Same country)",
            2: "Intermediate (Multiple countries)",
            3: "Advanced (Half-hour zones)",
            4: "Expert (Crossing midnight)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
        st.progress(progress, text=difficulty_names.get(difficulty_level, "Basic"))
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new scenario if needed
    if st.session_state.current_scenario is None:
        generate_new_scenario()
    
    # Display current scenario
    display_scenario()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Convert Time Zones:
        
        **1. Understand the Direction:**
        - **Moving East** → Add hours (time is later)
        - **Moving West** → Subtract hours (time is earlier)
        
        **2. Time Differences by Country:**
        
        **🇦🇺 Australia:**
        - AWST → ACST: +1 hour 30 minutes
        - ACST → AEST: +30 minutes
        - AWST → AEST: +2 hours
        
        **🇺🇸 USA:**
        - PST → MST: +1 hour
        - MST → CST: +1 hour
        - CST → EST: +1 hour
        - PST → EST: +3 hours
        
        **🇨🇦 Canada:**
        - PT → MT: +1 hour
        - MT → CT: +1 hour
        - CT → ET: +1 hour
        - ET → AT: +1 hour
        
        **🇪🇺 Europe:**
        - WET → CET: +1 hour
        - CET → EET: +1 hour
        - EET → MSK: +1 hour
        
        **🇧🇷 Brazil:**
        - ACT → AMT: +1 hour
        - AMT → BRT: +1 hour
        - BRT → FNT: +1 hour
        
        **🇮🇳 India & Neighbors:**
        - Pakistan (PKT) → India (IST): +30 minutes
        - India (IST) → Nepal (NPT): +15 minutes
        - India (IST) → Bhutan (BTT): +30 minutes
        
        **3. Crossing Midnight:**
        - If subtracting takes you before 12:00 A.M., it becomes the previous day
        - If adding takes you past 11:59 P.M., it becomes the next day
        
        **4. Remember:**
        - 12:00 P.M. = Noon (midday)
        - 12:00 A.M. = Midnight
        """)

def generate_new_scenario():
    """Generate a new time zone conversion scenario"""
    
    # Define all scenarios with progressive difficulty
    all_scenarios = get_all_scenarios()
    
    # Filter by difficulty
    difficulty = st.session_state.time_zone_difficulty
    available_scenarios = [s for s in all_scenarios if s['difficulty'] <= difficulty]
    
    if not available_scenarios:
        available_scenarios = all_scenarios[:3]  # Fallback to basic
    
    # Select random scenario
    scenario = random.choice(available_scenarios)
    
    # Store in session state
    st.session_state.scenario_data = scenario
    st.session_state.correct_answer = scenario['correct_answer']
    st.session_state.current_scenario = scenario['question']
    st.session_state.show_hint = False

def get_all_scenarios():
    """Return all time zone scenarios with multiple countries"""
    return [
        # AUSTRALIA - Level 1 (Basic)
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 5:00 P.M. in the Australian Eastern Standard Time Zone, what time is it in the Australian Central Standard Time Zone?",
            "from_zone": "AEST",
            "to_zone": "ACST",
            "from_time": "5:00 P.M.",
            "correct_answer": "4:30 P.M.",
            "time_difference": -0.5,
            "difficulty": 1,
            "explanation": "ACST is 30 minutes behind AEST. 5:00 P.M. - 30 minutes = 4:30 P.M.",
            "hint": "ACST is 30 minutes behind AEST. Subtract 30 minutes from the given time."
        },
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 6:00 P.M. in the Australian Central Standard Time Zone, what time is it in the Australian Western Standard Time Zone?",
            "from_zone": "ACST",
            "to_zone": "AWST",
            "from_time": "6:00 P.M.",
            "correct_answer": "4:30 P.M.",
            "time_difference": -1.5,
            "difficulty": 1,
            "explanation": "AWST is 1.5 hours behind ACST. 6:00 P.M. - 1 hour 30 minutes = 4:30 P.M.",
            "hint": "AWST is 1 hour and 30 minutes behind ACST. Subtract 1:30 from the given time."
        },
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 10:00 A.M. in the Australian Western Standard Time Zone, what time is it in the Australian Eastern Standard Time Zone?",
            "from_zone": "AWST",
            "to_zone": "AEST",
            "from_time": "10:00 A.M.",
            "correct_answer": "12:00 P.M.",
            "time_difference": 2,
            "difficulty": 1,
            "explanation": "AEST is 2 hours ahead of AWST. 10:00 A.M. + 2 hours = 12:00 P.M. (noon)",
            "hint": "AEST is 2 hours ahead of AWST. Add 2 hours to the given time."
        },
        
        # USA - Level 2
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 3:00 P.M. in New York (Eastern Time), what time is it in Los Angeles (Pacific Time)?",
            "from_zone": "EST",
            "to_zone": "PST",
            "from_time": "3:00 P.M.",
            "correct_answer": "12:00 P.M.",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "PST is 3 hours behind EST. 3:00 P.M. - 3 hours = 12:00 P.M. (noon)",
            "hint": "Pacific Time is 3 hours behind Eastern Time. Subtract 3 hours."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 9:00 A.M. in Denver (Mountain Time), what time is it in Chicago (Central Time)?",
            "from_zone": "MST",
            "to_zone": "CST",
            "from_time": "9:00 A.M.",
            "correct_answer": "10:00 A.M.",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "CST is 1 hour ahead of MST. 9:00 A.M. + 1 hour = 10:00 A.M.",
            "hint": "Central Time is 1 hour ahead of Mountain Time. Add 1 hour."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 5:30 P.M. in Chicago (Central Time), what time is it in Los Angeles (Pacific Time)?",
            "from_zone": "CST",
            "to_zone": "PST",
            "from_time": "5:30 P.M.",
            "correct_answer": "3:30 P.M.",
            "time_difference": -2,
            "difficulty": 2,
            "explanation": "PST is 2 hours behind CST. 5:30 P.M. - 2 hours = 3:30 P.M.",
            "hint": "Pacific Time is 2 hours behind Central Time. Subtract 2 hours."
        },
        
        # CANADA - Level 2
        {
            "country": "Canada",
            "country_flag": "🇨🇦",
            "map_type": "canada",
            "question": "If it is 4:00 P.M. in Toronto (Eastern Time), what time is it in Vancouver (Pacific Time)?",
            "from_zone": "ET",
            "to_zone": "PT",
            "from_time": "4:00 P.M.",
            "correct_answer": "1:00 P.M.",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "PT is 3 hours behind ET. 4:00 P.M. - 3 hours = 1:00 P.M.",
            "hint": "Pacific Time is 3 hours behind Eastern Time. Subtract 3 hours."
        },
        {
            "country": "Canada",
            "country_flag": "🇨🇦",
            "map_type": "canada",
            "question": "If it is 7:30 P.M. in Halifax (Atlantic Time), what time is it in Winnipeg (Central Time)?",
            "from_zone": "AT",
            "to_zone": "CT",
            "from_time": "7:30 P.M.",
            "correct_answer": "5:30 P.M.",
            "time_difference": -2,
            "difficulty": 2,
            "explanation": "CT is 2 hours behind AT. 7:30 P.M. - 2 hours = 5:30 P.M.",
            "hint": "Central Time is 2 hours behind Atlantic Time. Subtract 2 hours."
        },
        
        # EUROPE - Level 2
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 2:00 P.M. in London (WET), what time is it in Berlin (CET)?",
            "from_zone": "WET",
            "to_zone": "CET",
            "from_time": "2:00 P.M.",
            "correct_answer": "3:00 P.M.",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "CET is 1 hour ahead of WET. 2:00 P.M. + 1 hour = 3:00 P.M.",
            "hint": "Central European Time is 1 hour ahead of Western European Time. Add 1 hour."
        },
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 11:00 A.M. in Paris (CET), what time is it in Athens (EET)?",
            "from_zone": "CET",
            "to_zone": "EET",
            "from_time": "11:00 A.M.",
            "correct_answer": "12:00 P.M.",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "EET is 1 hour ahead of CET. 11:00 A.M. + 1 hour = 12:00 P.M.",
            "hint": "Eastern European Time is 1 hour ahead of Central European Time. Add 1 hour."
        },
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 8:00 P.M. in Moscow (MSK), what time is it in London (WET)?",
            "from_zone": "MSK",
            "to_zone": "WET",
            "from_time": "8:00 P.M.",
            "correct_answer": "5:00 P.M.",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "WET is 3 hours behind MSK. 8:00 P.M. - 3 hours = 5:00 P.M.",
            "hint": "Western European Time is 3 hours behind Moscow Time. Subtract 3 hours."
        },
        
        # BRAZIL - Level 3
        {
            "country": "Brazil",
            "country_flag": "🇧🇷",
            "map_type": "brazil",
            "question": "If it is 3:00 P.M. in São Paulo (BRT), what time is it in Manaus (AMT)?",
            "from_zone": "BRT",
            "to_zone": "AMT",
            "from_time": "3:00 P.M.",
            "correct_answer": "2:00 P.M.",
            "time_difference": -1,
            "difficulty": 3,
            "explanation": "AMT is 1 hour behind BRT. 3:00 P.M. - 1 hour = 2:00 P.M.",
            "hint": "Amazon Time is 1 hour behind Brasília Time. Subtract 1 hour."
        },
        {
            "country": "Brazil",
            "country_flag": "🇧🇷",
            "map_type": "brazil",
            "question": "If it is 10:00 A.M. in Acre (ACT), what time is it in São Paulo (BRT)?",
            "from_zone": "ACT",
            "to_zone": "BRT",
            "from_time": "10:00 A.M.",
            "correct_answer": "12:00 P.M.",
            "time_difference": 2,
            "difficulty": 3,
            "explanation": "BRT is 2 hours ahead of ACT. 10:00 A.M. + 2 hours = 12:00 P.M.",
            "hint": "Brasília Time is 2 hours ahead of Acre Time. Add 2 hours."
        },
        
        # INDIA & Neighbors - Level 3
        {
            "country": "India & Neighbors",
            "country_flag": "🇮🇳",
            "map_type": "india",
            "question": "If it is 2:30 P.M. in India (IST), what time is it in Nepal (NPT)?",
            "from_zone": "IST",
            "to_zone": "NPT",
            "from_time": "2:30 P.M.",
            "correct_answer": "2:45 P.M.",
            "time_difference": 0.25,
            "difficulty": 3,
            "explanation": "NPT is 15 minutes ahead of IST. 2:30 P.M. + 15 minutes = 2:45 P.M.",
            "hint": "Nepal Time is 15 minutes ahead of Indian Standard Time. Add 15 minutes."
        },
        {
            "country": "India & Neighbors",
            "country_flag": "🇮🇳",
            "map_type": "india",
            "question": "If it is 4:00 P.M. in Pakistan (PKT), what time is it in India (IST)?",
            "from_zone": "PKT",
            "to_zone": "IST",
            "from_time": "4:00 P.M.",
            "correct_answer": "4:30 P.M.",
            "time_difference": 0.5,
            "difficulty": 3,
            "explanation": "IST is 30 minutes ahead of PKT. 4:00 P.M. + 30 minutes = 4:30 P.M.",
            "hint": "Indian Standard Time is 30 minutes ahead of Pakistan Standard Time. Add 30 minutes."
        },
        
        # Level 4 - Crossing midnight
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 1:00 A.M. in Sydney (AEST), what time is it in Perth (AWST)?",
            "from_zone": "AEST",
            "to_zone": "AWST",
            "from_time": "1:00 A.M.",
            "correct_answer": "11:00 P.M.",
            "time_difference": -2,
            "difficulty": 4,
            "explanation": "AWST is 2 hours behind AEST. 1:00 A.M. - 2 hours = 11:00 P.M. (previous day)",
            "note": "(previous day)",
            "hint": "AWST is 2 hours behind AEST. When subtracting crosses midnight, it becomes the previous day."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 11:30 P.M. in Los Angeles (PST), what time is it in New York (EST)?",
            "from_zone": "PST",
            "to_zone": "EST",
            "from_time": "11:30 P.M.",
            "correct_answer": "2:30 A.M.",
            "time_difference": 3,
            "difficulty": 4,
            "explanation": "EST is 3 hours ahead of PST. 11:30 P.M. + 3 hours = 2:30 A.M. (next day)",
            "note": "(next day)",
            "hint": "EST is 3 hours ahead of PST. When adding crosses midnight, it becomes the next day."
        }
    ]

def display_scenario():
    """Display the current time zone scenario"""
    scenario = st.session_state.scenario_data
    
    # Display the question with country flag
    st.markdown(f"### {scenario['country_flag']} {scenario['question']}")
    
    # Add note about standard time
    st.info("💡 Assume it is Standard Time (no daylight saving)")
    
    # Display the map based on country
    if scenario['map_type'] == 'australia':
        display_australia_map(scenario)
    elif scenario['map_type'] == 'usa':
        display_usa_map(scenario)
    elif scenario['map_type'] == 'canada':
        display_canada_map(scenario)
    elif scenario['map_type'] == 'europe':
        display_europe_map(scenario)
    elif scenario['map_type'] == 'brazil':
        display_brazil_map(scenario)
    elif scenario['map_type'] == 'india':
        display_india_map(scenario)
    else:
        display_generic_map(scenario)
    
    # Hint button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💡 Need a Hint?", use_container_width=True, disabled=st.session_state.show_hint):
            st.session_state.show_hint = True
            st.rerun()
    
    if st.session_state.show_hint:
        st.info(f"💡 **Hint:** {scenario['hint']}")
    
    # Generate answer options
    options = generate_answer_options(scenario['correct_answer'], scenario.get('time_difference', 0))
    
    # Create answer selection
    st.markdown("### Select your answer:")
    
    # Create columns for options (2x3 grid)
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3, col1, col2, col3]
    
    selected_answer = None
    for i, option in enumerate(options):
        with columns[i % 3]:
            if st.button(option, key=f"option_{i}", use_container_width=True):
                st.session_state.user_answer = option
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Alternative text input
    st.markdown("**Or type your answer:**")
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_input(
            "Enter time (e.g., 4:30 P.M.)",
            key="time_input",
            placeholder="4:30 P.M."
        )
    with col2:
        if st.button("Submit Answer", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                st.session_state.user_answer = user_input
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Show feedback if answer submitted
    if st.session_state.answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_scenario_state()
                st.rerun()

def display_australia_map(scenario):
    """Display Australia time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    # Use columns to create the map layout
    st.markdown("### 🗺️ Australia Time Zones")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        awst_style = "border: 3px solid red;" if from_zone == "AWST" or to_zone == "AWST" else ""
        st.markdown(f"""
        <div style="background-color: #00ACC1; color: white; padding: 30px; border-radius: 10px; text-align: center; {awst_style}">
            <h4>AWST</h4>
            <p>Australian Western<br>Standard Time</p>
            <small>Perth, WA</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        acst_style = "border: 3px solid red;" if from_zone == "ACST" or to_zone == "ACST" else ""
        st.markdown(f"""
        <div style="background-color: #8BC34A; color: white; padding: 30px; border-radius: 10px; text-align: center; {acst_style}">
            <h4>ACST</h4>
            <p>Australian Central<br>Standard Time</p>
            <small>Adelaide, Darwin</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        aest_style = "border: 3px solid red;" if from_zone == "AEST" or to_zone == "AEST" else ""
        st.markdown(f"""
        <div style="background-color: #FFA726; color: white; padding: 30px; border-radius: 10px; text-align: center; {aest_style}">
            <h4>AEST</h4>
            <p>Australian Eastern<br>Standard Time</p>
            <small>Sydney, Melbourne, Brisbane</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in Australia"):
        st.markdown("""
        | From → To | AWST | ACST | AEST |
        |-----------|------|------|------|
        | **AWST** | - | +1:30 | +2:00 |
        | **ACST** | -1:30 | - | +0:30 |
        | **AEST** | -2:00 | -0:30 | - |
        """)

def display_usa_map(scenario):
    """Display USA time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    st.markdown("### 🗺️ USA Time Zones")
    
    col1, col2, col3, col4 = st.columns(4)
    
    zones = [
        ("PST", "Pacific", "Los Angeles", "#4CAF50", col1),
        ("MST", "Mountain", "Denver", "#2196F3", col2),
        ("CST", "Central", "Chicago", "#FF9800", col3),
        ("EST", "Eastern", "New York", "#F44336", col4)
    ]
    
    for zone_code, zone_name, city, color, column in zones:
        with column:
            zone_style = "border: 3px solid red;" if from_zone == zone_code or to_zone == zone_code else ""
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center; {zone_style}">
                <h5>{zone_code}</h5>
                <p>{zone_name}</p>
                <small>{city}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in USA"):
        st.markdown("""
        | From → To | PST | MST | CST | EST |
        |-----------|-----|-----|-----|-----|
        | **PST** | - | +1:00 | +2:00 | +3:00 |
        | **MST** | -1:00 | - | +1:00 | +2:00 |
        | **CST** | -2:00 | -1:00 | - | +1:00 |
        | **EST** | -3:00 | -2:00 | -1:00 | - |
        """)

def display_canada_map(scenario):
    """Display Canada time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    st.markdown("### 🗺️ Canada Time Zones")
    
    zones_data = [
        ("PT", "Pacific Time", "Vancouver", "#009688"),
        ("MT", "Mountain Time", "Calgary", "#3F51B5"),
        ("CT", "Central Time", "Winnipeg", "#E91E63"),
        ("ET", "Eastern Time", "Toronto", "#FF5722"),
        ("AT", "Atlantic Time", "Halifax", "#795548")
    ]
    
    cols = st.columns(5)
    for i, (zone_code, zone_name, city, color) in enumerate(zones_data):
        with cols[i]:
            zone_style = "border: 3px solid red;" if from_zone == zone_code or to_zone == zone_code else ""
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 15px; border-radius: 10px; text-align: center; {zone_style}">
                <h6>{zone_code}</h6>
                <small>{city}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in Canada"):
        st.markdown("""
        | From → To | PT | MT | CT | ET | AT |
        |-----------|----|----|----|----|-----|
        | **PT** | - | +1:00 | +2:00 | +3:00 | +4:00 |
        | **MT** | -1:00 | - | +1:00 | +2:00 | +3:00 |
        | **CT** | -2:00 | -1:00 | - | +1:00 | +2:00 |
        | **ET** | -3:00 | -2:00 | -1:00 | - | +1:00 |
        | **AT** | -4:00 | -3:00 | -2:00 | -1:00 | - |
        """)

def display_europe_map(scenario):
    """Display Europe time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    st.markdown("### 🗺️ Europe Time Zones")
    
    zones_data = [
        ("WET", "Western European", "London/Lisbon", "#00BCD4"),
        ("CET", "Central European", "Paris/Berlin", "#CDDC39"),
        ("EET", "Eastern European", "Athens/Helsinki", "#FF6B6B"),
        ("MSK", "Moscow Time", "Moscow", "#4ECDC4")
    ]
    
    cols = st.columns(4)
    for i, (zone_code, zone_name, cities, color) in enumerate(zones_data):
        with cols[i]:
            zone_style = "border: 3px solid red;" if from_zone == zone_code or to_zone == zone_code else ""
            text_color = "black" if zone_code == "CET" else "white"
            st.markdown(f"""
            <div style="background-color: {color}; color: {text_color}; padding: 20px; border-radius: 10px; text-align: center; {zone_style}">
                <h5>{zone_code}</h5>
                <small>{cities}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in Europe"):
        st.markdown("""
        | From → To | WET | CET | EET | MSK |
        |-----------|-----|-----|-----|-----|
        | **WET** | - | +1:00 | +2:00 | +3:00 |
        | **CET** | -1:00 | - | +1:00 | +2:00 |
        | **EET** | -2:00 | -1:00 | - | +1:00 |
        | **MSK** | -3:00 | -2:00 | -1:00 | - |
        """)

def display_brazil_map(scenario):
    """Display Brazil time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    st.markdown("### 🗺️ Brazil Time Zones")
    
    zones_data = [
        ("ACT", "Acre Time", "Rio Branco", "#8BC34A"),
        ("AMT", "Amazon Time", "Manaus", "#FFC107"),
        ("BRT", "Brasília Time", "São Paulo/Rio", "#03A9F4"),
        ("FNT", "Fernando de Noronha", "Island", "#E91E63")
    ]
    
    cols = st.columns(4)
    for i, (zone_code, zone_name, cities, color) in enumerate(zones_data):
        with cols[i]:
            zone_style = "border: 3px solid red;" if from_zone == zone_code or to_zone == zone_code else ""
            text_color = "black" if zone_code == "AMT" else "white"
            st.markdown(f"""
            <div style="background-color: {color}; color: {text_color}; padding: 20px; border-radius: 10px; text-align: center; {zone_style}">
                <h5>{zone_code}</h5>
                <small>{cities}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in Brazil"):
        st.markdown("""
        | From → To | ACT | AMT | BRT | FNT |
        |-----------|-----|-----|-----|-----|
        | **ACT** | - | +1:00 | +2:00 | +3:00 |
        | **AMT** | -1:00 | - | +1:00 | +2:00 |
        | **BRT** | -2:00 | -1:00 | - | +1:00 |
        | **FNT** | -3:00 | -2:00 | -1:00 | - |
        """)

def display_india_map(scenario):
    """Display India & Neighbors time zone map with time difference chart"""
    from_zone = scenario.get('from_zone', '')
    to_zone = scenario.get('to_zone', '')
    
    st.markdown("### 🗺️ India & Neighbors Time Zones")
    
    zones_data = [
        ("PKT", "Pakistan", "UTC+5:00", "#4CAF50"),
        ("IST", "India", "UTC+5:30", "#FF9800"),
        ("NPT", "Nepal", "UTC+5:45", "#2196F3"),
        ("BTT", "Bhutan", "UTC+6:00", "#9C27B0")
    ]
    
    cols = st.columns(4)
    for i, (zone_code, country, utc_offset, color) in enumerate(zones_data):
        with cols[i]:
            zone_style = "border: 3px solid red;" if from_zone == zone_code or to_zone == zone_code else ""
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center; {zone_style}">
                <h5>{zone_code}</h5>
                <p>{country}</p>
                <small>{utc_offset}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Time difference chart
    with st.expander("📊 Time Differences in India & Neighbors"):
        st.markdown("""
        | From → To | PKT | IST | NPT | BTT |
        |-----------|-----|-----|-----|-----|
        | **PKT** | - | +0:30 | +0:45 | +1:00 |
        | **IST** | -0:30 | - | +0:15 | +0:30 |
        | **NPT** | -0:45 | -0:15 | - | +0:15 |
        | **BTT** | -1:00 | -0:30 | -0:15 | - |
        """)

def display_generic_map(scenario):
    """Display generic time zone visualization"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center;">
        <h3>{scenario['country']} Time Zones</h3>
        <p style="font-size: 20px; margin-top: 15px;">
            Converting from <strong>{scenario.get('from_zone', 'Zone A')}</strong> to <strong>{scenario.get('to_zone', 'Zone B')}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

def generate_answer_options(correct_answer, time_difference):
    """Generate answer options using regular Python"""
    options = [correct_answer]
    
    # Parse the correct time
    time_parts = correct_answer.replace('.', '').split()
    hour_min = time_parts[0].split(':')
    hour = int(hour_min[0])
    minute = int(hour_min[1]) if len(hour_min) > 1 else 0
    period = time_parts[1]  # A.M. or P.M.
    
    # Convert to 24-hour for calculations
    if period == 'P.M.' and hour != 12:
        hour = hour + 12
    elif period == 'A.M.' and hour == 12:
        hour = 0
    
    # Generate variations
    variations = [30, -30, 60, -60, 90, -90, 15, -15, 45, -45]
    
    for var_minutes in variations:
        if len(options) >= 6:
            break
        
        # Calculate new time
        total_minutes = hour * 60 + minute + var_minutes
        
        # Handle day boundaries
        while total_minutes < 0:
            total_minutes = total_minutes + (24 * 60)
        while total_minutes >= (24 * 60):
            total_minutes = total_minutes - (24 * 60)
        
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        
        # Convert back to 12-hour format
        new_period = 'A.M.'
        display_hour = new_hour
        
        if new_hour >= 12:
            new_period = 'P.M.'
            if new_hour > 12:
                display_hour = new_hour - 12
        elif new_hour == 0:
            display_hour = 12
        
        # Format the time
        if new_minute == 0:
            new_time = f"{display_hour}:00 {new_period}"
        else:
            new_time = f"{display_hour}:{str(new_minute).zfill(2)} {new_period}"
        
        if new_time not in options:
            options.append(new_time)
    
    random.shuffle(options)
    return options[:6]

def show_feedback():
    """Display feedback for the submitted answer"""
    if not st.session_state.show_feedback:
        user_answer = st.session_state.user_answer
        correct_answer = st.session_state.correct_answer
        scenario = st.session_state.scenario_data
        
        # Normalize answers for comparison
        normalized_user = normalize_time(user_answer)
        normalized_correct = normalize_time(correct_answer)
        
        if normalized_user == normalized_correct:
            st.success("🎉 **Excellent! That's correct!**")
            st.markdown(f"**Explanation:** {scenario['explanation']}")
            
            # Show quick facts about the country
            show_country_facts(scenario['country'])
            
            # Increase difficulty
            st.session_state.consecutive_correct += 1
            if st.session_state.consecutive_correct >= 2 and st.session_state.time_zone_difficulty < 4:
                st.session_state.time_zone_difficulty += 1
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.time_zone_difficulty}**")
                st.session_state.consecutive_correct = 0
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}** {scenario.get('note', '')}")
            st.markdown(f"**Explanation:** {scenario['explanation']}")
            
            # Show step-by-step
            with st.expander("📖 **See step-by-step solution**", expanded=True):
                show_conversion_steps(scenario)
            
            # Decrease difficulty
            st.session_state.consecutive_correct = 0
            if st.session_state.time_zone_difficulty > 1:
                st.session_state.time_zone_difficulty -= 1
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.time_zone_difficulty}**")
        
        st.session_state.show_feedback = True
        st.session_state.total_attempted += 1

def show_country_facts(country):
    """Show interesting facts about the country's time zones"""
    facts = {
        "Australia": "🦘 **Fun Fact:** Australia has 3 main time zones, but during daylight saving time, it can have 5 different local times!",
        "United States": "🗽 **Fun Fact:** The Continental US spans 4 time zones, but including Alaska and Hawaii, it has 6!",
        "Canada": "🍁 **Fun Fact:** Canada spans 6 time zones from coast to coast!",
        "Europe": "🏰 **Fun Fact:** Russia spans 11 time zones - the most of any country!",
        "Brazil": "⚽ **Fun Fact:** Brazil has 4 time zones, making it challenging to schedule nationwide TV broadcasts!",
        "India & Neighbors": "🏔️ **Fun Fact:** Nepal's time zone is UTC+5:45, one of the few countries with a 45-minute offset!"
    }
    
    if country in facts:
        st.info(facts[country])

def normalize_time(time_str):
    """Normalize time string for comparison"""
    time_str = ' '.join(time_str.split())
    time_str = time_str.replace('AM', 'A.M.').replace('PM', 'P.M.')
    time_str = time_str.replace('a.m.', 'A.M.').replace('p.m.', 'P.M.')
    return time_str.upper()

def show_conversion_steps(scenario):
    """Show step-by-step conversion"""
    from_time = scenario['from_time']
    time_diff = scenario['time_difference']
    
    # Calculate hours and minutes
    hours = int(abs(time_diff))
    minutes = int((abs(time_diff) - hours) * 60)
    
    direction = "ahead" if time_diff > 0 else "behind"
    operation = "Add" if time_diff > 0 else "Subtract"
    
    diff_str = f"{hours} hour{'s' if hours != 1 else ''}"
    if minutes > 0:
        diff_str += f" and {minutes} minutes"
    
    st.markdown(f"""
    ### Step-by-step conversion:
    
    1. **Identify the time difference:** {scenario['to_zone']} is {diff_str} {direction} {scenario['from_zone']}
    
    2. **Starting time:** {from_time}
    
    3. **{operation} {diff_str}:** 
       - {from_time} {'+' if time_diff > 0 else '-'} {diff_str} = {scenario['correct_answer']}
    
    4. **Final answer:** {scenario['correct_answer']} {scenario.get('note', '')}
    
    💡 **Remember:** When moving east, add time. When moving west, subtract time.
    """)

def reset_scenario_state():
    """Reset the scenario state for next question"""
    st.session_state.current_scenario = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.scenario_data = {}
    st.session_state.show_hint = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer