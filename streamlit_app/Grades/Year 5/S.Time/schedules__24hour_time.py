import streamlit as st
import random
import pandas as pd

def run():
    """
    Main function to run the Schedules - 24-hour time activity.
    This gets called when the subtopic is loaded from the curriculum.
    """
    # Initialize session state
    if "schedule_24hr_difficulty" not in st.session_state:
        st.session_state.schedule_24hr_difficulty = 1
    
    if "current_schedule" not in st.session_state:
        st.session_state.current_schedule = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.schedule_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
    
    # Page header
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("🕐 Schedules - 24-Hour Time")
    st.markdown("*Read and interpret schedules using 24-hour time format*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.schedule_24hr_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (Simple schedules)",
            2: "Intermediate (Complex schedules)",
            3: "Advanced (Multi-column schedules)",
            4: "Expert (Transportation & events)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
        progress = (difficulty_level - 1) / 3
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
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new schedule if needed
    if st.session_state.current_schedule is None:
        generate_new_schedule()
    
    # Display current schedule
    display_schedule()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Understanding 24-Hour Time:
        
        **24-Hour Time Format:**
        - 00:00 = Midnight
        - 01:00 to 11:59 = Morning (1 AM to 11:59 AM)
        - 12:00 = Noon
        - 13:00 to 23:59 = Afternoon/Evening (1 PM to 11:59 PM)
        
        **Converting to 12-Hour Time:**
        - 00:00-12:59 = Same, just add AM (00:00 = 12:00 AM)
        - 13:00-23:59 = Subtract 12, add PM (13:00 = 1:00 PM)
        
        **Examples:**
        - 07:40 = 7:40 AM
        - 13:00 = 1:00 PM
        - 15:30 = 3:30 PM
        - 21:45 = 9:45 PM
        
        **Schedule Types:**
        - **Class schedules**: Begin and end times
        - **Transport schedules**: Arrival and departure times
        - **Event schedules**: Start and finish times
        - **Single-time schedules**: One time per location/event
        
        **Tips for Success:**
        1. Look at the column headers carefully
        2. Find the row mentioned in the question
        3. Read the correct column (begin/end, arrive/depart)
        4. Match the time exactly
        """)

def generate_new_schedule():
    """Generate a new schedule scenario"""
    difficulty = st.session_state.schedule_24hr_difficulty
    
    if difficulty == 1:
        # Basic: Simple class or activity schedules
        scenario = generate_basic_schedule()
    elif difficulty == 2:
        # Intermediate: More complex schedules
        scenario = generate_intermediate_schedule()
    elif difficulty == 3:
        # Advanced: Transportation schedules
        scenario = generate_advanced_schedule()
    else:
        # Expert: Complex multi-column schedules
        scenario = generate_expert_schedule()
    
    st.session_state.schedule_data = scenario
    st.session_state.current_schedule = scenario['question']
    st.session_state.correct_answer = scenario['correct_answer']

def generate_basic_schedule():
    """Generate basic schedule scenarios"""
    
    scenarios = [
        {
            "title": "Class Schedule",
            "table_data": {
                "Subject": ["Art", "Handwriting", "Spanish", "Social Studies", "Geography", "Recess", "Gym", "Science", "Spelling"],
                "Begin": ["07:40", "08:45", "09:50", "10:50", "12:05", "13:00", "13:40", "14:50", "15:55"],
                "End": ["08:40", "09:40", "10:40", "12:00", "12:55", "13:30", "14:40", "15:50", "16:40"]
            },
            "question": "Which class begins at 13:00?",
            "options": ["Science class", "Gym class", "Geography class", "Recess"],
            "correct_answer": "Recess",
            "question_type": "begins_at"
        },
        {
            "title": "Dance Studio Schedule",
            "table_data": {
                "Class": ["western dance", "advanced ballet", "tap dance", "modern dance", "intermediate ballet", "beginning ballet", "hip hop dance", "swing dance", "jazz dance"],
                "Begin": ["08:15", "10:05", "11:00", "11:35", "12:40", "14:15", "15:35", "17:05", "18:00"],
                "End": ["09:55", "10:50", "11:30", "12:35", "14:10", "15:30", "17:00", "17:55", "19:20"]
            },
            "question": "Which class begins at 12:40?",
            "options": ["the western dance class", "the beginning ballet class", "the intermediate ballet class", "the jazz dance class"],
            "correct_answer": "the intermediate ballet class",
            "question_type": "begins_at"
        },
        {
            "title": "Summer Olympics Schedule",
            "table_data": {
                "Event": ["track and field", "diving", "badminton", "gymnastics", "tennis"],
                "Begin": ["10:05", "13:10", "16:30", "18:35", "19:00"],
                "End": ["14:50", "16:55", "19:30", "20:40", "21:45"]
            },
            "question": "When does the track and field event end?",
            "options": ["14:50", "10:05", "18:35", "21:45"],
            "correct_answer": "14:50",
            "question_type": "when_end"
        },
        {
            "title": "Gymnastics Meet Schedule",
            "table_data": {
                "Event": ["men's parallel bars", "men's vault", "men's rings", "women's vault", "women's balance beam", "women's uneven bars"],
                "Begin": ["10:10", "10:40", "11:20", "12:05", "12:55", "13:10"],
                "End": ["10:35", "11:35", "11:50", "12:45", "13:30", "13:50"]
            },
            "question": "When does the women's balance beam event begin?",
            "options": ["12:55", "12:05", "10:40", "13:30"],
            "correct_answer": "12:55",
            "question_type": "when_begin"
        },
        {
            "title": "Music School Schedule",
            "table_data": {
                "Class": ["Piano basics", "Guitar intro", "Violin practice", "Music theory", "Choir", "Band practice"],
                "Begin": ["09:00", "10:15", "11:30", "14:00", "15:30", "17:00"],
                "End": ["10:00", "11:15", "12:30", "15:00", "16:45", "18:30"]
            },
            "question": "Which class ends at 15:00?",
            "options": ["Piano basics", "Music theory", "Choir", "Band practice"],
            "correct_answer": "Music theory",
            "question_type": "ends_at"
        }
    ]
    
    return random.choice(scenarios)

def generate_intermediate_schedule():
    """Generate intermediate schedule scenarios"""
    
    scenarios = [
        {
            "title": "Art Teacher's Schedule",
            "table_data": {
                "Class": ["Computer Graphics", "Art History", "Photography", "Architecture", "Pottery", "Sketching"],
                "Begin": ["09:15", "10:35", "11:25", "13:05", "14:20", "15:35"],
                "End": ["10:20", "11:10", "12:50", "14:05", "15:25", "16:50"]
            },
            "question": "When does Sketching class begin?",
            "options": ["15:35", "11:25", "13:05", "09:15"],
            "correct_answer": "15:35",
            "question_type": "when_begin"
        },
        {
            "title": "Library Workshop Schedule",
            "table_data": {
                "Workshop": ["Research Skills", "Digital Literacy", "Creative Writing", "Book Club", "Study Skills", "Reading Hour"],
                "Start": ["08:30", "09:45", "11:00", "13:15", "14:30", "16:00"],
                "Finish": ["09:30", "10:45", "12:00", "14:15", "15:30", "17:00"]
            },
            "question": "Which workshop starts at 13:15?",
            "options": ["Research Skills", "Book Club", "Study Skills", "Creative Writing"],
            "correct_answer": "Book Club",
            "question_type": "starts_at"
        },
        {
            "title": "Sports Complex Schedule",
            "table_data": {
                "Activity": ["Swimming", "Basketball", "Yoga", "Tennis", "Martial Arts", "Aerobics"],
                "Begin": ["06:00", "08:00", "09:30", "11:00", "14:00", "17:30"],
                "End": ["07:30", "09:15", "10:45", "12:30", "15:30", "18:45"]
            },
            "question": "When does Martial Arts end?",
            "options": ["14:00", "15:30", "17:30", "18:45"],
            "correct_answer": "15:30",
            "question_type": "when_end"
        },
        {
            "title": "Conference Room Schedule",
            "table_data": {
                "Meeting": ["Team briefing", "Client presentation", "Budget review", "Project planning", "Staff training", "Board meeting"],
                "Start": ["08:00", "09:30", "11:00", "13:30", "15:00", "16:30"],
                "End": ["08:45", "10:45", "12:00", "14:30", "16:00", "18:00"]
            },
            "question": "Which meeting starts at 15:00?",
            "options": ["Team briefing", "Staff training", "Board meeting", "Budget review"],
            "correct_answer": "Staff training",
            "question_type": "starts_at"
        }
    ]
    
    return random.choice(scenarios)

def generate_advanced_schedule():
    """Generate advanced transportation schedule scenarios"""
    
    scenarios = [
        {
            "title": "Train Schedule",
            "table_data": {
                "Location": ["Westford", "Springdale", "Kensington", "Stanford", "Milford", "Newberg", "Rockport"],
                "Arrive": ["02:40", "04:15", "05:20", "06:55", "07:50", "09:25", "10:10"],
                "Depart": ["03:00", "04:35", "05:45", "07:05", "08:05", "09:35", "10:25"]
            },
            "question": "Which stop does the train depart from at 03:00?",
            "options": ["Stanford", "Rockport", "Kensington", "Westford"],
            "correct_answer": "Westford",
            "question_type": "depart_from"
        },
        {
            "title": "Tour Bus Schedule",
            "table_data": {
                "Location": ["shopping district", "the aquarium", "famous bridge", "landmark sculpture", "historic house", "art museum", "old building", "governor's mansion", "downtown", "city hall"],
                "Arrive": ["08:40", "09:40", "10:50", "12:15", "13:10", "13:55", "14:55", "15:40", "16:30", "17:00"],
                "Depart": ["09:35", "10:05", "11:35", "12:40", "13:35", "14:30", "15:05", "15:50", "16:55", "17:20"]
            },
            "question": "When does the bus depart from downtown?",
            "options": ["13:35", "16:30", "13:10", "16:55"],
            "correct_answer": "16:55",
            "question_type": "when_depart"
        },
        {
            "title": "Hotel Shuttle Bus Schedule",
            "table_data": {
                "Location": ["downtown", "university campus", "baseball stadium", "pizza place", "park", "American football stadium", "art museum"],
                "Arrive": ["08:40", "09:25", "10:15", "11:00", "11:40", "12:15", "13:05"],
                "Depart": ["08:45", "09:35", "10:25", "11:05", "11:50", "12:25", "13:20"]
            },
            "question": "At which stop does the bus arrive at 08:40?",
            "options": ["the art museum", "downtown", "the university campus", "the baseball stadium"],
            "correct_answer": "downtown",
            "question_type": "arrive_at"
        },
        {
            "title": "Airport Shuttle Schedule",
            "table_data": {
                "Terminal": ["Terminal A", "Terminal B", "Terminal C", "Parking Lot 1", "Parking Lot 2", "Car Rental", "Hotel Zone"],
                "Arrive": ["06:00", "06:15", "06:30", "06:45", "07:00", "07:15", "07:30"],
                "Depart": ["06:05", "06:20", "06:35", "06:50", "07:05", "07:20", "07:35"]
            },
            "question": "Which location does the shuttle depart from at 06:50?",
            "options": ["Terminal A", "Terminal C", "Parking Lot 1", "Car Rental"],
            "correct_answer": "Parking Lot 1",
            "question_type": "depart_from"
        }
    ]
    
    return random.choice(scenarios)

def generate_expert_schedule():
    """Generate expert schedule scenarios with single time columns"""
    
    scenarios = [
        {
            "title": "Subway Train Schedule",
            "table_data": {
                "Location": ["American football stadium", "history museum", "city park", "university", "shopping district", "civic centre"],
                "Time": ["10:50", "11:35", "11:50", "12:35", "13:25", "13:35"]
            },
            "question": "Which stop does the train depart from at 11:35?",
            "options": ["the history museum", "the shopping district", "the civic centre", "the university"],
            "correct_answer": "the history museum",
            "question_type": "single_time"
        },
        {
            "title": "Bus Schedule",
            "table_data": {
                "Location": ["the mall", "the post office", "the grocery store", "the playground", "the cinema", "the doctor's office", "the school", "the zoo", "the library"],
                "Time": ["10:40", "10:45", "11:30", "12:00", "12:10", "12:40", "12:45", "13:15", "13:45"]
            },
            "question": "Which stop does the bus depart from at 12:10?",
            "options": ["the cinema", "the doctor's office", "the playground", "the mall"],
            "correct_answer": "the cinema",
            "question_type": "single_time"
        },
        {
            "title": "Ferry Schedule",
            "table_data": {
                "Port": ["Harbor Bay", "Sunset Marina", "Fisherman's Wharf", "Ocean View", "Lighthouse Point", "Beach Resort"],
                "Departure": ["07:30", "08:15", "09:00", "10:30", "11:45", "13:00"]
            },
            "question": "What time does the ferry depart from Ocean View?",
            "options": ["09:00", "10:30", "11:45", "13:00"],
            "correct_answer": "10:30",
            "question_type": "single_time_when"
        },
        {
            "title": "Museum Tour Schedule",
            "table_data": {
                "Exhibition": ["Ancient Egypt", "Medieval Times", "Renaissance Art", "Modern Science", "Space Exploration", "Ocean Life"],
                "Tour Start": ["09:00", "10:15", "11:30", "13:00", "14:30", "16:00"]
            },
            "question": "Which exhibition tour starts at 14:30?",
            "options": ["Ancient Egypt", "Space Exploration", "Ocean Life", "Modern Science"],
            "correct_answer": "Space Exploration",
            "question_type": "single_time"
        },
        {
            "title": "Theater Show Schedule",
            "table_data": {
                "Performance": ["Morning Matinee", "Lunch Special", "Afternoon Delight", "Early Evening", "Prime Time", "Late Night"],
                "Showtime": ["10:00", "12:30", "14:45", "17:00", "19:30", "22:00"]
            },
            "question": "What time does the Prime Time show start?",
            "options": ["17:00", "19:30", "22:00", "14:45"],
            "correct_answer": "19:30",
            "question_type": "single_time_when"
        }
    ]
    
    return random.choice(scenarios)

def display_schedule():
    """Display the schedule table and question"""
    data = st.session_state.schedule_data
    
    # Display the question context
    st.markdown("### Look at the following schedule:")
    
    # Create and display the schedule table
    df = pd.DataFrame(data['table_data'])
    
    # Style the table
    styled_df = df.style.set_properties(**{
        'background-color': '#f0f8ff',
        'color': 'black',
        'border': '2px solid #4CAF50',
        'text-align': 'center',
        'font-size': '16px',
        'font-weight': 'bold'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#4CAF50'),
            ('color', 'white'),
            ('font-size', '18px'),
            ('font-weight', 'bold'),
            ('text-align', 'center'),
            ('border', '2px solid #4CAF50')
        ]},
        {'selector': 'td', 'props': [
            ('border', '1px solid #ddd'),
            ('padding', '10px')
        ]},
        {'selector': 'table', 'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%'),
            ('margin', '20px 0')
        ]},
        {'selector': 'caption', 'props': [
            ('caption-side', 'top'),
            ('font-size', '20px'),
            ('font-weight', 'bold'),
            ('color', '#4CAF50'),
            ('padding', '10px'),
            ('background-color', '#e8f5e9')
        ]}
    ])
    
    # Add title as caption
    styled_df = styled_df.set_caption(data['title'])
    
    # Display the styled table
    st.write(styled_df.to_html(), unsafe_allow_html=True)
    
    # Display the question
    st.markdown(f"### ❓ {data['question']}")
    
    # Display answer options
    display_answer_options(data['options'])
    
    # Show feedback if answer submitted
    if st.session_state.answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_schedule_state()
                st.rerun()

def display_answer_options(options):
    """Display answer option buttons"""
    # Create columns based on number of options
    if len(options) == 2:
        cols = st.columns(2)
    elif len(options) == 3:
        cols = st.columns(3)
    else:
        cols = st.columns(2)
    
    for i, option in enumerate(options):
        with cols[i % len(cols)]:
            if st.button(option, key=f"option_{i}", use_container_width=True):
                st.session_state.user_answer = option
                st.session_state.answer_submitted = True
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if not st.session_state.show_feedback:
        user_answer = st.session_state.user_answer
        correct_answer = st.session_state.correct_answer
        data = st.session_state.schedule_data
        
        if user_answer == correct_answer:
            st.success("🎉 **Excellent! That's correct!**")
            
            # Show explanation
            show_explanation(data, correct=True)
            
            # Increase difficulty
            st.session_state.consecutive_correct += 1
            if st.session_state.consecutive_correct >= 2 and st.session_state.schedule_24hr_difficulty < 4:
                st.session_state.schedule_24hr_difficulty += 1
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.schedule_24hr_difficulty}**")
                st.session_state.consecutive_correct = 0
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
            
            # Show explanation
            show_explanation(data, correct=False)
            
            # Decrease difficulty
            st.session_state.consecutive_correct = 0
            if st.session_state.schedule_24hr_difficulty > 1:
                st.session_state.schedule_24hr_difficulty -= 1
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.schedule_24hr_difficulty}**")
        
        st.session_state.show_feedback = True
        st.session_state.total_attempted += 1

def show_explanation(data, correct):
    """Show detailed explanation for the answer"""
    question_type = data.get('question_type', '')
    
    with st.expander("📖 **Understanding the Schedule**", expanded=not correct):
        if question_type in ['begins_at', 'starts_at']:
            st.markdown("""
            **How to solve:**
            1. Look at the **Begin** or **Start** column
            2. Find the time mentioned in the question
            3. Look at the same row to find which class/event it is
            4. That's your answer!
            
            **Tip:** Make sure you're looking at the correct column - Begin, not End!
            """)
            
        elif question_type in ['ends_at', 'finishes_at']:
            st.markdown("""
            **How to solve:**
            1. Look at the **End** or **Finish** column
            2. Find the time mentioned in the question
            3. Look at the same row to find which class/event it is
            4. That's your answer!
            
            **Tip:** Make sure you're looking at the End column, not Begin!
            """)
            
        elif question_type in ['when_begin', 'when_start']:
            st.markdown("""
            **How to solve:**
            1. Find the event/class mentioned in the question
            2. Look at the same row
            3. Read the time in the **Begin** or **Start** column
            4. That's your answer!
            """)
            
        elif question_type in ['when_end', 'when_finish']:
            st.markdown("""
            **How to solve:**
            1. Find the event/class mentioned in the question
            2. Look at the same row
            3. Read the time in the **End** or **Finish** column
            4. That's your answer!
            """)
            
        elif question_type == 'depart_from':
            st.markdown("""
            **How to solve:**
            1. Look at the **Depart** column
            2. Find the time mentioned in the question
            3. Look at the same row in the **Location** column
            4. That location is where the transport departs from at that time!
            
            **Remember:** Depart means leaving FROM that location.
            """)
            
        elif question_type == 'arrive_at':
            st.markdown("""
            **How to solve:**
            1. Look at the **Arrive** column
            2. Find the time mentioned in the question
            3. Look at the same row in the **Location** column
            4. That location is where the transport arrives at that time!
            
            **Remember:** Arrive means coming TO that location.
            """)
            
        elif question_type == 'when_depart':
            st.markdown("""
            **How to solve:**
            1. Find the location mentioned in the question
            2. Look at the same row
            3. Read the time in the **Depart** column
            4. That's when the transport leaves from that location!
            """)
            
        elif question_type == 'when_arrive':
            st.markdown("""
            **How to solve:**
            1. Find the location mentioned in the question
            2. Look at the same row
            3. Read the time in the **Arrive** column
            4. That's when the transport arrives at that location!
            """)
            
        elif question_type == 'single_time':
            st.markdown("""
            **How to solve:**
            1. Look at the **Time** column
            2. Find the time mentioned in the question
            3. Look at the same row in the **Location** column
            4. That's the location for that time!
            
            **Note:** Single time columns usually show departure times.
            """)
            
        elif question_type == 'single_time_when':
            st.markdown("""
            **How to solve:**
            1. Find the location/event mentioned in the question
            2. Look at the same row
            3. Read the time in the **Time** column
            4. That's your answer!
            """)
        
        # Add 24-hour time conversion help
        st.markdown("""
        ---
        ### 24-Hour Time Quick Reference:
        - **13:00** = 1:00 PM
        - **14:00** = 2:00 PM
        - **15:00** = 3:00 PM
        - **16:00** = 4:00 PM
        - **17:00** = 5:00 PM
        - **18:00** = 6:00 PM
        - **19:00** = 7:00 PM
        - **20:00** = 8:00 PM
        - **21:00** = 9:00 PM
        - **22:00** = 10:00 PM
        - **23:00** = 11:00 PM
        """)

def reset_schedule_state():
    """Reset the schedule state for next question"""
    st.session_state.current_schedule = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.schedule_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer