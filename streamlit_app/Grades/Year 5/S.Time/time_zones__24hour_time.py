import streamlit as st
import random

def run():
    """
    Main function to run the Time Zones - 24-hour time activity.
    This gets called when the subtopic is loaded from the curriculum.
    """
    # Initialize session state for difficulty and game state
    if "time_zone_24h_difficulty" not in st.session_state:
        st.session_state.time_zone_24h_difficulty = 1  # Start with basic scenarios
    
    if "current_scenario_24h" not in st.session_state:
        st.session_state.current_scenario_24h = None
        st.session_state.correct_answer_24h = None
        st.session_state.show_feedback_24h = False
        st.session_state.answer_submitted_24h = False
        st.session_state.scenario_data_24h = {}
        st.session_state.consecutive_correct_24h = 0
        st.session_state.total_attempted_24h = 0
        st.session_state.show_hint_24h = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("🌍 Time Zones - 24-Hour Time")
    st.markdown("*Convert times between different time zones using 24-hour format (00:00 - 23:59)*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_zone_24h_difficulty
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
    if st.session_state.current_scenario_24h is None:
        generate_new_scenario()
    
    # Display current scenario
    display_scenario()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### 24-Hour Time Format:
        
        **Understanding 24-hour time:**
        - **00:00** = Midnight (start of day)
        - **01:00 - 11:59** = Morning hours (same as A.M.)
        - **12:00** = Noon (midday)
        - **13:00 - 23:59** = Afternoon/Evening (subtract 12 for P.M. time)
        - **23:59** = One minute before midnight
        
        **Quick Conversion Guide:**
        - 1:00 A.M. = 01:00
        - 12:00 P.M. (noon) = 12:00
        - 1:00 P.M. = 13:00
        - 6:00 P.M. = 18:00
        - 11:00 P.M. = 23:00
        - 12:00 A.M. (midnight) = 00:00
        
        **Time Zone Conversion Rules:**
        - **Moving East** → Add hours (time is later)
        - **Moving West** → Subtract hours (time is earlier)
        
        **Time Differences by Country:**
        
        **🇦🇺 Australia:**
        - AWST → ACST: +1:30
        - ACST → AEST: +0:30
        - AWST → AEST: +2:00
        
        **🇺🇸 USA:**
        - PST → MST: +1:00
        - MST → CST: +1:00
        - CST → EST: +1:00
        - PST → EST: +3:00
        
        **🇨🇦 Canada:**
        - PT → MT: +1:00
        - MT → CT: +1:00
        - CT → ET: +1:00
        - ET → AT: +1:00
        
        **🇪🇺 Europe:**
        - WET → CET: +1:00
        - CET → EET: +1:00
        - EET → MSK: +1:00
        
        **🇧🇷 Brazil:**
        - ACT → AMT: +1:00
        - AMT → BRT: +1:00
        - BRT → FNT: +1:00
        
        **🇮🇳 India & Neighbors:**
        - Pakistan (PKT) → India (IST): +0:30
        - India (IST) → Nepal (NPT): +0:15
        - India (IST) → Bhutan (BTT): +0:30
        
        **Crossing Midnight:**
        - If result < 00:00, add 24:00 (previous day)
        - If result ≥ 24:00, subtract 24:00 (next day)
        """)

def generate_new_scenario():
    """Generate a new time zone conversion scenario with 24-hour format"""
    
    # Define all scenarios with progressive difficulty
    all_scenarios = get_all_scenarios_24h()
    
    # Filter by difficulty
    difficulty = st.session_state.time_zone_24h_difficulty
    available_scenarios = [s for s in all_scenarios if s['difficulty'] <= difficulty]
    
    if not available_scenarios:
        available_scenarios = all_scenarios[:3]  # Fallback to basic
    
    # Select random scenario
    scenario = random.choice(available_scenarios)
    
    # Store in session state
    st.session_state.scenario_data_24h = scenario
    st.session_state.correct_answer_24h = scenario['correct_answer']
    st.session_state.current_scenario_24h = scenario['question']
    st.session_state.show_hint_24h = False

def get_all_scenarios_24h():
    """Return all time zone scenarios with 24-hour format"""
    return [
        # AUSTRALIA - Level 1 (Basic)
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 17:00 in the Australian Eastern Standard Time Zone, what time is it in the Australian Central Standard Time Zone?",
            "from_zone": "AEST",
            "to_zone": "ACST",
            "from_time": "17:00",
            "correct_answer": "16:30",
            "time_difference": -0.5,
            "difficulty": 1,
            "explanation": "ACST is 30 minutes behind AEST. 17:00 - 30 minutes = 16:30",
            "hint": "ACST is 30 minutes behind AEST. Subtract 30 minutes from the given time."
        },
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 18:00 in the Australian Central Standard Time Zone, what time is it in the Australian Western Standard Time Zone?",
            "from_zone": "ACST",
            "to_zone": "AWST",
            "from_time": "18:00",
            "correct_answer": "16:30",
            "time_difference": -1.5,
            "difficulty": 1,
            "explanation": "AWST is 1.5 hours behind ACST. 18:00 - 1 hour 30 minutes = 16:30",
            "hint": "AWST is 1 hour and 30 minutes behind ACST. Subtract 1:30 from the given time."
        },
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 10:00 in the Australian Western Standard Time Zone, what time is it in the Australian Eastern Standard Time Zone?",
            "from_zone": "AWST",
            "to_zone": "AEST",
            "from_time": "10:00",
            "correct_answer": "12:00",
            "time_difference": 2,
            "difficulty": 1,
            "explanation": "AEST is 2 hours ahead of AWST. 10:00 + 2 hours = 12:00",
            "hint": "AEST is 2 hours ahead of AWST. Add 2 hours to the given time."
        },
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 22:00 in the Australian Eastern Standard Time Zone, what time is it in the Australian Central Standard Time Zone?",
            "from_zone": "AEST",
            "to_zone": "ACST",
            "from_time": "22:00",
            "correct_answer": "21:30",
            "time_difference": -0.5,
            "difficulty": 1,
            "explanation": "ACST is 30 minutes behind AEST. 22:00 - 30 minutes = 21:30",
            "hint": "ACST is 30 minutes behind AEST. Subtract 30 minutes from the given time."
        },
        
        # USA - Level 2
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 15:00 in New York (Eastern Time), what time is it in Los Angeles (Pacific Time)?",
            "from_zone": "EST",
            "to_zone": "PST",
            "from_time": "15:00",
            "correct_answer": "12:00",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "PST is 3 hours behind EST. 15:00 - 3 hours = 12:00",
            "hint": "Pacific Time is 3 hours behind Eastern Time. Subtract 3 hours."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 09:00 in Denver (Mountain Time), what time is it in Chicago (Central Time)?",
            "from_zone": "MST",
            "to_zone": "CST",
            "from_time": "09:00",
            "correct_answer": "10:00",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "CST is 1 hour ahead of MST. 09:00 + 1 hour = 10:00",
            "hint": "Central Time is 1 hour ahead of Mountain Time. Add 1 hour."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 17:30 in Chicago (Central Time), what time is it in Los Angeles (Pacific Time)?",
            "from_zone": "CST",
            "to_zone": "PST",
            "from_time": "17:30",
            "correct_answer": "15:30",
            "time_difference": -2,
            "difficulty": 2,
            "explanation": "PST is 2 hours behind CST. 17:30 - 2 hours = 15:30",
            "hint": "Pacific Time is 2 hours behind Central Time. Subtract 2 hours."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 20:45 in Los Angeles (Pacific Time), what time is it in New York (Eastern Time)?",
            "from_zone": "PST",
            "to_zone": "EST",
            "from_time": "20:45",
            "correct_answer": "23:45",
            "time_difference": 3,
            "difficulty": 2,
            "explanation": "EST is 3 hours ahead of PST. 20:45 + 3 hours = 23:45",
            "hint": "Eastern Time is 3 hours ahead of Pacific Time. Add 3 hours."
        },
        
        # CANADA - Level 2
        {
            "country": "Canada",
            "country_flag": "🇨🇦",
            "map_type": "canada",
            "question": "If it is 16:00 in Toronto (Eastern Time), what time is it in Vancouver (Pacific Time)?",
            "from_zone": "ET",
            "to_zone": "PT",
            "from_time": "16:00",
            "correct_answer": "13:00",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "PT is 3 hours behind ET. 16:00 - 3 hours = 13:00",
            "hint": "Pacific Time is 3 hours behind Eastern Time. Subtract 3 hours."
        },
        {
            "country": "Canada",
            "country_flag": "🇨🇦",
            "map_type": "canada",
            "question": "If it is 19:30 in Halifax (Atlantic Time), what time is it in Winnipeg (Central Time)?",
            "from_zone": "AT",
            "to_zone": "CT",
            "from_time": "19:30",
            "correct_answer": "17:30",
            "time_difference": -2,
            "difficulty": 2,
            "explanation": "CT is 2 hours behind AT. 19:30 - 2 hours = 17:30",
            "hint": "Central Time is 2 hours behind Atlantic Time. Subtract 2 hours."
        },
        
        # EUROPE - Level 2
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 14:00 in London (WET), what time is it in Berlin (CET)?",
            "from_zone": "WET",
            "to_zone": "CET",
            "from_time": "14:00",
            "correct_answer": "15:00",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "CET is 1 hour ahead of WET. 14:00 + 1 hour = 15:00",
            "hint": "Central European Time is 1 hour ahead of Western European Time. Add 1 hour."
        },
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 11:00 in Paris (CET), what time is it in Athens (EET)?",
            "from_zone": "CET",
            "to_zone": "EET",
            "from_time": "11:00",
            "correct_answer": "12:00",
            "time_difference": 1,
            "difficulty": 2,
            "explanation": "EET is 1 hour ahead of CET. 11:00 + 1 hour = 12:00",
            "hint": "Eastern European Time is 1 hour ahead of Central European Time. Add 1 hour."
        },
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 20:00 in Moscow (MSK), what time is it in London (WET)?",
            "from_zone": "MSK",
            "to_zone": "WET",
            "from_time": "20:00",
            "correct_answer": "17:00",
            "time_difference": -3,
            "difficulty": 2,
            "explanation": "WET is 3 hours behind MSK. 20:00 - 3 hours = 17:00",
            "hint": "Western European Time is 3 hours behind Moscow Time. Subtract 3 hours."
        },
        
        # BRAZIL - Level 3
        {
            "country": "Brazil",
            "country_flag": "🇧🇷",
            "map_type": "brazil",
            "question": "If it is 15:00 in São Paulo (BRT), what time is it in Manaus (AMT)?",
            "from_zone": "BRT",
            "to_zone": "AMT",
            "from_time": "15:00",
            "correct_answer": "14:00",
            "time_difference": -1,
            "difficulty": 3,
            "explanation": "AMT is 1 hour behind BRT. 15:00 - 1 hour = 14:00",
            "hint": "Amazon Time is 1 hour behind Brasília Time. Subtract 1 hour."
        },
        {
            "country": "Brazil",
            "country_flag": "🇧🇷",
            "map_type": "brazil",
            "question": "If it is 10:00 in Acre (ACT), what time is it in São Paulo (BRT)?",
            "from_zone": "ACT",
            "to_zone": "BRT",
            "from_time": "10:00",
            "correct_answer": "12:00",
            "time_difference": 2,
            "difficulty": 3,
            "explanation": "BRT is 2 hours ahead of ACT. 10:00 + 2 hours = 12:00",
            "hint": "Brasília Time is 2 hours ahead of Acre Time. Add 2 hours."
        },
        
        # INDIA & Neighbors - Level 3
        {
            "country": "India & Neighbors",
            "country_flag": "🇮🇳",
            "map_type": "india",
            "question": "If it is 14:30 in India (IST), what time is it in Nepal (NPT)?",
            "from_zone": "IST",
            "to_zone": "NPT",
            "from_time": "14:30",
            "correct_answer": "14:45",
            "time_difference": 0.25,
            "difficulty": 3,
            "explanation": "NPT is 15 minutes ahead of IST. 14:30 + 15 minutes = 14:45",
            "hint": "Nepal Time is 15 minutes ahead of Indian Standard Time. Add 15 minutes."
        },
        {
            "country": "India & Neighbors",
            "country_flag": "🇮🇳",
            "map_type": "india",
            "question": "If it is 16:00 in Pakistan (PKT), what time is it in India (IST)?",
            "from_zone": "PKT",
            "to_zone": "IST",
            "from_time": "16:00",
            "correct_answer": "16:30",
            "time_difference": 0.5,
            "difficulty": 3,
            "explanation": "IST is 30 minutes ahead of PKT. 16:00 + 30 minutes = 16:30",
            "hint": "Indian Standard Time is 30 minutes ahead of Pakistan Standard Time. Add 30 minutes."
        },
        {
            "country": "India & Neighbors",
            "country_flag": "🇮🇳",
            "map_type": "india",
            "question": "If it is 21:15 in India (IST), what time is it in Bhutan (BTT)?",
            "from_zone": "IST",
            "to_zone": "BTT",
            "from_time": "21:15",
            "correct_answer": "21:45",
            "time_difference": 0.5,
            "difficulty": 3,
            "explanation": "BTT is 30 minutes ahead of IST. 21:15 + 30 minutes = 21:45",
            "hint": "Bhutan Time is 30 minutes ahead of Indian Standard Time. Add 30 minutes."
        },
        
        # Level 4 - Crossing midnight
        {
            "country": "Australia",
            "country_flag": "🇦🇺",
            "map_type": "australia",
            "question": "If it is 01:00 in Sydney (AEST), what time is it in Perth (AWST)?",
            "from_zone": "AEST",
            "to_zone": "AWST",
            "from_time": "01:00",
            "correct_answer": "23:00",
            "time_difference": -2,
            "difficulty": 4,
            "explanation": "AWST is 2 hours behind AEST. 01:00 - 2 hours = 23:00 (previous day)",
            "note": "(previous day)",
            "hint": "AWST is 2 hours behind AEST. When subtracting crosses 00:00, it becomes the previous day."
        },
        {
            "country": "United States",
            "country_flag": "🇺🇸",
            "map_type": "usa",
            "question": "If it is 23:30 in Los Angeles (PST), what time is it in New York (EST)?",
            "from_zone": "PST",
            "to_zone": "EST",
            "from_time": "23:30",
            "correct_answer": "02:30",
            "time_difference": 3,
            "difficulty": 4,
            "explanation": "EST is 3 hours ahead of PST. 23:30 + 3 hours = 02:30 (next day)",
            "note": "(next day)",
            "hint": "EST is 3 hours ahead of PST. When adding crosses 24:00, it becomes the next day."
        },
        {
            "country": "Canada",
            "country_flag": "🇨🇦",
            "map_type": "canada",
            "question": "If it is 00:45 in Halifax (Atlantic Time), what time is it in Vancouver (Pacific Time)?",
            "from_zone": "AT",
            "to_zone": "PT",
            "from_time": "00:45",
            "correct_answer": "20:45",
            "time_difference": -4,
            "difficulty": 4,
            "explanation": "PT is 4 hours behind AT. 00:45 - 4 hours = 20:45 (previous day)",
            "note": "(previous day)",
            "hint": "Pacific Time is 4 hours behind Atlantic Time. When subtracting crosses 00:00, it becomes the previous day."
        },
        {
            "country": "Europe",
            "country_flag": "🇪🇺",
            "map_type": "europe",
            "question": "If it is 22:15 in London (WET), what time is it in Moscow (MSK)?",
            "from_zone": "WET",
            "to_zone": "MSK",
            "from_time": "22:15",
            "correct_answer": "01:15",
            "time_difference": 3,
            "difficulty": 4,
            "explanation": "MSK is 3 hours ahead of WET. 22:15 + 3 hours = 01:15 (next day)",
            "note": "(next day)",
            "hint": "Moscow Time is 3 hours ahead of Western European Time. When adding crosses 24:00, it becomes the next day."
        }
    ]

def display_scenario():
    """Display the current time zone scenario with 24-hour format"""
    scenario = st.session_state.scenario_data_24h
    
    # Display the question with country flag
    st.markdown(f"### {scenario['country_flag']} {scenario['question']}")
    
    # Add note about standard time and 24-hour format
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 Assume it is Standard Time (no daylight saving)")
    with col2:
        st.info("🕐 Using 24-hour format (00:00 - 23:59)")
    
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
        if st.button("💡 Need a Hint?", use_container_width=True, disabled=st.session_state.show_hint_24h):
            st.session_state.show_hint_24h = True
            st.rerun()
    
    if st.session_state.show_hint_24h:
        st.info(f"💡 **Hint:** {scenario['hint']}")
    
    # Generate answer options
    options = generate_answer_options_24h(scenario['correct_answer'], scenario.get('time_difference', 0))
    
    # Create answer selection
    st.markdown("### Select your answer:")
    
    # Create columns for options (2x3 grid)
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3, col1, col2, col3]
    
    selected_answer = None
    for i, option in enumerate(options):
        with columns[i % 3]:
            if st.button(option, key=f"option_{i}", use_container_width=True):
                st.session_state.user_answer_24h = option
                st.session_state.answer_submitted_24h = True
                st.rerun()
    
    # Alternative text input
    st.markdown("**Or type your answer:**")
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_input(
            "Enter time in 24-hour format (e.g., 14:30)",
            key="time_input_24h",
            placeholder="14:30"
        )
    with col2:
        if st.button("Submit Answer", type="primary", disabled=st.session_state.answer_submitted_24h):
            if user_input:
                st.session_state.user_answer_24h = user_input
                st.session_state.answer_submitted_24h = True
                st.rerun()
    
    # Show feedback if answer submitted
    if st.session_state.answer_submitted_24h:
        show_feedback()
    
    # Next question button
    if st.session_state.show_feedback_24h:
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

def generate_answer_options_24h(correct_answer, time_difference):
    """Generate answer options using 24-hour format"""
    options = [correct_answer]
    
    # Parse the correct time (24-hour format)
    time_parts = correct_answer.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
    
    # Generate variations
    variations = [30, -30, 60, -60, 90, -90, 15, -15, 45, -45, 120, -120]
    
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
        
        # Format the time in 24-hour format
        new_time = f"{str(new_hour).zfill(2)}:{str(new_minute).zfill(2)}"
        
        if new_time not in options:
            options.append(new_time)
    
    random.shuffle(options)
    return options[:6]

def show_feedback():
    """Display feedback for the submitted answer"""
    if not st.session_state.show_feedback_24h:
        user_answer = st.session_state.user_answer_24h
        correct_answer = st.session_state.correct_answer_24h
        scenario = st.session_state.scenario_data_24h
        
        # Normalize answers for comparison
        normalized_user = normalize_time_24h(user_answer)
        normalized_correct = normalize_time_24h(correct_answer)
        
        if normalized_user == normalized_correct:
            st.success("🎉 **Excellent! That's correct!**")
            st.markdown(f"**Explanation:** {scenario['explanation']}")
            
            # Show quick facts about the country
            show_country_facts(scenario['country'])
            
            # Show 24-hour to 12-hour conversion
            show_time_conversion(correct_answer)
            
            # Increase difficulty
            st.session_state.consecutive_correct_24h += 1
            if st.session_state.consecutive_correct_24h >= 2 and st.session_state.time_zone_24h_difficulty < 4:
                st.session_state.time_zone_24h_difficulty += 1
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.time_zone_24h_difficulty}**")
                st.session_state.consecutive_correct_24h = 0
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}** {scenario.get('note', '')}")
            st.markdown(f"**Explanation:** {scenario['explanation']}")
            
            # Show step-by-step
            with st.expander("📖 **See step-by-step solution**", expanded=True):
                show_conversion_steps(scenario)
            
            # Decrease difficulty
            st.session_state.consecutive_correct_24h = 0
            if st.session_state.time_zone_24h_difficulty > 1:
                st.session_state.time_zone_24h_difficulty -= 1
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.time_zone_24h_difficulty}**")
        
        st.session_state.show_feedback_24h = True
        st.session_state.total_attempted_24h += 1

def show_time_conversion(time_24h):
    """Show conversion between 24-hour and 12-hour format"""
    hour = int(time_24h.split(':')[0])
    minute = time_24h.split(':')[1]
    
    if hour == 0:
        time_12h = f"12:{minute} A.M."
    elif hour < 12:
        time_12h = f"{hour}:{minute} A.M."
    elif hour == 12:
        time_12h = f"12:{minute} P.M."
    else:
        time_12h = f"{hour - 12}:{minute} P.M."
    
    st.info(f"💡 **Time Format Conversion:** {time_24h} (24-hour) = {time_12h} (12-hour)")

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

def normalize_time_24h(time_str):
    """Normalize 24-hour time string for comparison"""
    # Remove any spaces and handle different formats
    time_str = time_str.strip().replace(' ', '')
    
    # Add leading zeros if needed
    if ':' in time_str:
        parts = time_str.split(':')
        hour = parts[0].zfill(2)
        minute = parts[1].zfill(2) if len(parts) > 1 else '00'
        return f"{hour}:{minute}"
    else:
        # Handle case where user might enter just hours
        return f"{time_str.zfill(2)}:00"

def show_conversion_steps(scenario):
    """Show step-by-step conversion for 24-hour format"""
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
    ### Step-by-step conversion (24-hour format):
    
    1. **Identify the time difference:** {scenario['to_zone']} is {diff_str} {direction} {scenario['from_zone']}
    
    2. **Starting time:** {from_time}
    
    3. **{operation} {diff_str}:** 
       - {from_time} {'+' if time_diff > 0 else '-'} {diff_str} = {scenario['correct_answer']}
    
    4. **Final answer:** {scenario['correct_answer']} {scenario.get('note', '')}
    
    💡 **Remember in 24-hour format:**
    - When result < 00:00, add 24:00 (previous day)
    - When result ≥ 24:00, subtract 24:00 (next day)
    - Moving east → Add time
    - Moving west → Subtract time
    """)

def reset_scenario_state():
    """Reset the scenario state for next question"""
    st.session_state.current_scenario_24h = None
    st.session_state.correct_answer_24h = None
    st.session_state.show_feedback_24h = False
    st.session_state.answer_submitted_24h = False
    st.session_state.scenario_data_24h = {}
    st.session_state.show_hint_24h = False
    if "user_answer_24h" in st.session_state:
        del st.session_state.user_answer_24h