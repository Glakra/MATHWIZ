import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse
import numpy as np

def run():
    """
    Main function to run the Schedules and Timelines - 12-hour time activity.
    This gets called when the subtopic is loaded from the curriculum.
    """
    # Initialize session state
    if "timeline_difficulty" not in st.session_state:
        st.session_state.timeline_difficulty = 1
    
    if "current_timeline" not in st.session_state:
        st.session_state.current_timeline = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.timeline_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
    
    # Page header
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("📅 Schedules and Timelines - 12-Hour Time")
    st.markdown("*Read and interpret schedules and timelines with events*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.timeline_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (Daily schedules)",
            2: "Intermediate (Before/After)",
            3: "Advanced (Historical timelines)",
            4: "Expert (Complex questions)"
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
    
    # Generate new timeline if needed
    if st.session_state.current_timeline is None:
        generate_new_timeline()
    
    # Display current timeline
    display_timeline()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Read Timelines:
        
        **Daily Schedules (12-hour time):**
        - Events are shown in chronological order
        - Read times carefully (A.M. vs P.M.)
        - Earlier times are to the left
        - Later times are to the right
        
        **Historical Timelines:**
        - Events are arranged by year
        - Earlier years are to the left
        - Later years are to the right
        - Calculate differences between years
        
        **Question Types:**
        1. **Before/After:** Which event happens before or after another?
        2. **First/Last:** Which event happens first or last?
        3. **Time Between:** How much time between two events?
        4. **Ordering:** Put events in chronological order
        5. **Between Years:** What happened between two dates?
        
        **Tips:**
        - Look at the timeline carefully before answering
        - Pay attention to A.M. and P.M.
        - For years, remember that smaller numbers mean earlier dates
        - Check the scale of the timeline (hours, days, years)
        """)

def generate_new_timeline():
    """Generate a new timeline scenario"""
    difficulty = st.session_state.timeline_difficulty
    
    if difficulty == 1:
        # Basic: Daily schedules
        scenario = generate_daily_schedule()
    elif difficulty == 2:
        # Intermediate: Before/After questions
        scenario = generate_before_after_scenario()
    elif difficulty == 3:
        # Advanced: Historical timelines
        scenario = generate_historical_timeline()
    else:
        # Expert: Complex questions
        scenario = generate_complex_scenario()
    
    st.session_state.timeline_data = scenario
    st.session_state.current_timeline = scenario['question']
    st.session_state.correct_answer = scenario['correct_answer']

def generate_daily_schedule():
    """Generate a daily schedule scenario"""
    
    name_pool = ["James", "Sarah", "Michael", "Emily", "David", "Lisa", "Tom", "Anna", "Ben", "Kate"]
    name = random.choice(name_pool)
    
    scenarios = [
        {
            "name": name,
            "events": [
                ("feeds cat", "6 A.M."),
                ("volunteers at library", "10 A.M."),
                ("shops for groceries", "12 P.M."),
                ("goes to gym", "2 P.M."),
                ("watches movie", "8 P.M.")
            ],
            "question": f"Does {name} shop for groceries before or after 4 A.M.?",
            "options": ["before", "after"],
            "correct_answer": "after",
            "question_type": "before_after_time"
        },
        {
            "name": name,
            "events": [
                ("has snack", "11 A.M."),
                ("eats lunch", "12 P.M."),
                ("walks dog", "2 P.M."),
                ("practises trumpet", "4 P.M."),
                ("revises spelling words", "6 P.M.")
            ],
            "question": f"Has {name} practised the trumpet by 1 P.M.?",
            "options": ["yes", "no"],
            "correct_answer": "no",
            "question_type": "by_time"
        },
        {
            "name": name,
            "events": [
                ("eats lunch", "12 P.M."),
                ("leaves school", "2 P.M."),
                ("has snack", "3 P.M."),
                ("practises piano", "5 P.M."),
                ("revises for maths quiz", "6 P.M.")
            ],
            "question": "Which event happens later?",
            "options": [f"{name} eats lunch", f"{name} practises piano"],
            "correct_answer": f"{name} practises piano",
            "question_type": "which_later"
        },
        {
            "name": name,
            "events": [
                ("goes to gym", "6 A.M."),
                ("attends business meeting", "10 A.M."),
                ("eats lunch", "12 P.M."),
                ("cooks dinner", "6 P.M."),
                ("watches TV", "8 P.M.")
            ],
            "question": "Which event happens first?",
            "options": ["goes to gym", "attends business meeting", "eats lunch", "cooks dinner"],
            "correct_answer": "goes to gym",
            "question_type": "which_first"
        },
        {
            "name": name,
            "events": [
                ("morning jog", "7 A.M."),
                ("breakfast", "8 A.M."),
                ("work meeting", "10 A.M."),
                ("lunch break", "1 P.M."),
                ("gym session", "6 P.M.")
            ],
            "question": f"How many hours between {name}'s breakfast and lunch break?",
            "options": ["3 hours", "4 hours", "5 hours", "6 hours"],
            "correct_answer": "5 hours",
            "question_type": "time_between"
        }
    ]
    
    return random.choice(scenarios)

def generate_before_after_scenario():
    """Generate before/after scenarios with more complexity"""
    
    name_pool = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Drew"]
    name = random.choice(name_pool)
    
    scenarios = [
        {
            "name": name,
            "events": [
                ("wakes up", "6:30 A.M."),
                ("morning exercise", "7:00 A.M."),
                ("breakfast", "8:00 A.M."),
                ("starts work", "9:00 A.M."),
                ("coffee break", "10:30 A.M."),
                ("lunch meeting", "12:30 P.M."),
                ("project review", "3:00 P.M."),
                ("leaves office", "5:30 P.M.")
            ],
            "question": f"Does {name} have the coffee break before or after the lunch meeting?",
            "options": ["before", "after"],
            "correct_answer": "before",
            "question_type": "before_after_event"
        },
        {
            "name": name,
            "events": [
                ("morning swim", "6:00 A.M."),
                ("breakfast", "7:30 A.M."),
                ("team meeting", "9:00 A.M."),
                ("client call", "11:00 A.M."),
                ("lunch", "12:30 P.M."),
                ("presentation", "2:00 P.M."),
                ("gym", "6:00 P.M.")
            ],
            "question": f"What does {name} do between the team meeting and lunch?",
            "options": ["morning swim", "client call", "presentation", "gym"],
            "correct_answer": "client call",
            "question_type": "between_events"
        },
        {
            "name": name,
            "events": [
                ("yoga class", "7:00 A.M."),
                ("shower", "8:00 A.M."),
                ("work commute", "8:30 A.M."),
                ("morning meeting", "10:00 A.M."),
                ("lunch", "1:00 P.M."),
                ("afternoon workshop", "3:00 P.M."),
                ("dinner", "7:00 P.M.")
            ],
            "question": "Which happens last in the morning (before 12:00 P.M.)?",
            "options": ["yoga class", "work commute", "morning meeting", "afternoon workshop"],
            "correct_answer": "morning meeting",
            "question_type": "last_in_period"
        }
    ]
    
    return random.choice(scenarios)

def generate_historical_timeline():
    """Generate historical timeline scenarios"""
    
    scenarios = [
        {
            "name": "Olympic Games",
            "events": [
                ("Los Angeles Olympics", "1984"),
                ("Calgary Winter Olympics", "1988"),
                ("Barcelona Olympics", "1992"),
                ("Atlanta Olympics", "1996"),
                ("Beijing Olympics", "2008")
            ],
            "question": "Select the event that happened between 1986 and 1992.",
            "options": [
                "Los Angeles Olympics",
                "Calgary Winter Olympics",
                "Atlanta Olympics",
                "Beijing Olympics"
            ],
            "correct_answer": "Calgary Winter Olympics",
            "question_type": "between_years"
        },
        {
            "name": "Nobel Peace Prize Winners",
            "events": [
                ("Ralph Bunche wins", "1950"),
                ("Martin Luther King Jr. wins", "1964"),
                ("Mother Teresa wins", "1979"),
                ("Elie Wiesel wins", "1986"),
                ("Leymah Gbowee wins", "2011")
            ],
            "question": "Which event happened earlier?",
            "options": [
                "Elie Wiesel wins",
                "Ralph Bunche wins"
            ],
            "correct_answer": "Ralph Bunche wins",
            "question_type": "which_earlier"
        },
        {
            "name": "Space Exploration",
            "events": [
                ("First human in space", "1961"),
                ("Moon landing", "1969"),
                ("First Space Shuttle", "1981"),
                ("ISS begins", "1998"),
                ("Private spacecraft to ISS", "2012")
            ],
            "question": "Select the event that happened last.",
            "options": [
                "Moon landing",
                "First Space Shuttle",
                "ISS begins",
                "Private spacecraft to ISS"
            ],
            "correct_answer": "Private spacecraft to ISS",
            "question_type": "which_last"
        },
        {
            "name": "Technology Milestones",
            "events": [
                ("First PC", "1975"),
                ("World Wide Web", "1989"),
                ("Google founded", "1998"),
                ("Facebook launched", "2004"),
                ("iPhone released", "2007")
            ],
            "question": "How many years between the World Wide Web creation and Google founding?",
            "options": ["7 years", "8 years", "9 years", "10 years"],
            "correct_answer": "9 years",
            "question_type": "years_between"
        }
    ]
    
    return random.choice(scenarios)

def generate_complex_scenario():
    """Generate complex timeline scenarios"""
    
    scenarios = [
        {
            "name": "Multi-Day Conference Schedule",
            "events": [
                ("Registration", "Mon 8:00 A.M."),
                ("Keynote speech", "Mon 10:00 A.M."),
                ("Lunch break", "Mon 12:30 P.M."),
                ("Workshop A", "Mon 2:00 P.M."),
                ("Panel discussion", "Tue 9:00 A.M."),
                ("Workshop B", "Tue 11:00 A.M."),
                ("Closing ceremony", "Tue 4:00 P.M.")
            ],
            "question": "Which event happens on Monday afternoon?",
            "options": ["Keynote speech", "Workshop A", "Panel discussion", "Workshop B"],
            "correct_answer": "Workshop A",
            "question_type": "specific_period"
        },
        {
            "name": "Student's Week",
            "events": [
                ("Math test", "Mon 9:00 A.M."),
                ("Soccer practice", "Tue 3:30 P.M."),
                ("Piano lesson", "Wed 4:00 P.M."),
                ("Science project", "Thu 8:30 A.M."),
                ("Movie night", "Fri 7:00 P.M."),
                ("Basketball game", "Sat 10:00 A.M.")
            ],
            "question": "How many activities are scheduled after 3:00 P.M.?",
            "options": ["2", "3", "4", "5"],
            "correct_answer": "3",
            "question_type": "count_events"
        }
    ]
    
    return random.choice(scenarios)

def display_timeline():
    """Display the timeline visualization and question"""
    data = st.session_state.timeline_data
    
    # Display the question
    st.markdown(f"### 📊 Look at {data.get('name', 'this')}'s timeline:")
    
    # Create the timeline visualization
    create_timeline_visual(data)
    
    # Display the specific question
    st.markdown(f"### ❓ {data['question']}")
    
    # Handle different question types
    question_type = data.get('question_type', 'multiple_choice')
    
    if question_type in ['before_after_time', 'before_after_event', 'by_time']:
        # Simple choice buttons
        display_choice_buttons(data['options'])
    else:
        # Multiple choice buttons
        display_multiple_choice(data['options'])
    
    # Show feedback if answer submitted
    if st.session_state.answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_timeline_state()
                st.rerun()

def create_timeline_visual(data):
    """Create a timeline visualization using matplotlib"""
    events = data.get('events', [])
    
    if not events:
        return
    
    # Determine if it's a time-based or year-based timeline
    is_year_timeline = any(len(str(time)) == 4 and str(time).isdigit() for _, time in events)
    
    if is_year_timeline:
        create_year_timeline_plot(events)
    else:
        create_time_timeline_plot(events)

def create_time_timeline_plot(events):
    """Create a minimalist daily schedule timeline with large, readable text - all leaning right"""
    
    # Convert times to numerical values for plotting
    def time_to_hours(time_str):
        """Convert 12-hour time to hours since midnight"""
        time_str = time_str.strip()
        # Handle multi-day events (Mon, Tue, etc.)
        if any(day in time_str for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            # Extract the day and time
            parts = time_str.split()
            if len(parts) >= 2:
                # Map days to offset hours
                day_offset = {
                    'Mon': 0, 'Tue': 24, 'Wed': 48, 'Thu': 72, 
                    'Fri': 96, 'Sat': 120, 'Sun': 144
                }
                day = parts[0]
                time_part = ' '.join(parts[1:])
                base_hours = day_offset.get(day, 0)
                
                # Parse the time part
                if ":" in time_part:
                    time_str_clean, period = time_part.rsplit(" ", 1)
                    hour, minute = map(int, time_str_clean.split(":"))
                else:
                    time_parts = time_part.split()
                    hour = int(time_parts[0])
                    minute = 0
                    period = time_parts[1]
                
                if period.upper() in ["P.M.", "PM"] and hour != 12:
                    hour += 12
                elif period.upper() in ["A.M.", "AM"] and hour == 12:
                    hour = 0
                
                return base_hours + hour + minute / 60
        
        # Regular time parsing
        if ":" in time_str:
            time_part, period = time_str.rsplit(" ", 1)
            hour, minute = map(int, time_part.split(":"))
        else:
            parts = time_str.split()
            hour = int(parts[0])
            minute = 0
            period = parts[1]
        
        if period.upper() in ["P.M.", "PM"] and hour != 12:
            hour += 12
        elif period.upper() in ["A.M.", "AM"] and hour == 12:
            hour = 0
        
        return hour + minute / 60
    
    # Sort events by time
    sorted_events = sorted(events, key=lambda x: time_to_hours(x[1]))
    
    # Create figure - even bigger for better readability
    fig = plt.figure(figsize=(24, 12), facecolor='white')
    ax = fig.add_subplot(111)
    
    # Calculate time range
    times = [time_to_hours(e[1]) for e in sorted_events]
    min_time = min(times) - 2
    max_time = max(times) + 2
    
    # Ensure reasonable span
    if max_time - min_time < 10:
        center = (max_time + min_time) / 2
        min_time = center - 5
        max_time = center + 5
    
    ax.set_xlim(min_time, max_time)
    ax.set_ylim(-3, 6)
    
    # Draw main timeline - thicker line
    timeline_y = 0
    ax.plot([min_time, max_time], [timeline_y, timeline_y], 
            color='#000000', linewidth=6, solid_capstyle='round', zorder=1)
    
    # Add arrows
    ax.annotate('', xy=(max_time - 0.1, timeline_y), xytext=(max_time - 0.3, timeline_y),
                arrowprops=dict(arrowstyle='->', lw=5, color='#000000'), zorder=2)
    ax.annotate('', xy=(min_time + 0.1, timeline_y), xytext=(min_time + 0.3, timeline_y),
                arrowprops=dict(arrowstyle='<-', lw=5, color='#000000'), zorder=2)
    
    # Color scheme - darker, professional colors
    colors = ['#0052CC', '#006644', '#CC5500', '#CC0000', '#6600CC']
    
    # Plot events - all leaning to the right
    for i, (event, time) in enumerate(sorted_events):
        x = time_to_hours(time)
        color = colors[i % len(colors)]
        
        # Vertical tick mark - thicker
        ax.plot([x, x], [timeline_y - 0.3, timeline_y + 2.0], 
                color=color, linewidth=4, zorder=3)
        
        # Event text - VERY LARGE and all leaning right at 35 degrees
        # Stagger the vertical position slightly for better readability
        text_y = 2.2 + (i % 3) * 0.4  # Slight vertical staggering
        
        ax.text(x + 0.1, text_y, event,
                rotation=35,  # All text at 35 degrees
                ha='left',
                va='bottom',
                fontsize=24,  # Even larger font
                color=color,
                fontweight='bold',
                zorder=5,
                fontfamily='Arial')
        
        # Time label - VERY LARGE and clear
        ax.text(x, -1.2, time,
                ha='center',
                va='center',
                fontsize=22,  # Larger time font
                fontweight='bold',
                color=color,
                bbox=dict(boxstyle="round,pad=0.4", 
                         facecolor='white', 
                         edgecolor=color, 
                         linewidth=3),
                zorder=5)
        
        # Dot on timeline - bigger
        ax.scatter(x, timeline_y, s=300, c=color, 
                  edgecolors='white', linewidth=4, zorder=6)
    
    # Add subtle hour grid (only for non-multi-day timelines)
    if max_time - min_time < 24:  # Single day timeline
        for hour in range(int(min_time), int(max_time) + 1):
            if min_time <= hour <= max_time:
                # Check distance from events
                min_distance = min([abs(hour - time_to_hours(t)) for _, t in sorted_events])
                if min_distance > 0.5:  # Only show if not too close to an event
                    ax.axvline(x=hour, ymin=0.45, ymax=0.55, 
                              color='#dddddd', linewidth=1.5, alpha=0.5, zorder=0)
                    
                    # Hour label
                    hour_display = hour % 24
                    if hour_display == 0 or hour_display == 24:
                        label = "12 AM"
                    elif hour_display < 12:
                        label = f"{hour_display} AM"
                    elif hour_display == 12:
                        label = "12 PM"
                    else:
                        label = f"{hour_display-12} PM"
                    
                    ax.text(hour, -2.5, label, ha='center', va='top',
                           fontsize=12, alpha=0.4, color='#999999')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Clean white background
    ax.set_facecolor('white')
    
    # Tight layout with padding
    plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)
    
    # Display
    st.pyplot(fig)
    plt.close()

def create_year_timeline_plot(events):
    """Create a minimalist historical timeline with large, readable text - all leaning right"""
    
    # Sort events by year
    sorted_events = sorted(events, key=lambda x: int(x[1]))
    
    # Get year range
    years = [int(y) for _, y in sorted_events]
    min_year = min(years) - 5
    max_year = max(years) + 5
    
    # Create figure - bigger for better readability
    fig = plt.figure(figsize=(24, 12), facecolor='white')
    ax = fig.add_subplot(111)
    
    # Set up the plot
    ax.set_xlim(min_year, max_year)
    ax.set_ylim(-3, 6)
    
    # Draw main timeline - thicker
    timeline_y = 0
    ax.plot([min_year, max_year], [timeline_y, timeline_y], 
            color='#000000', linewidth=6, solid_capstyle='round', zorder=1)
    
    # Add arrow heads
    ax.annotate('', xy=(max_year - 0.5, timeline_y), xytext=(max_year - 1.5, timeline_y),
                arrowprops=dict(arrowstyle='->', lw=5, color='#000000'), zorder=2)
    ax.annotate('', xy=(min_year + 0.5, timeline_y), xytext=(min_year + 1.5, timeline_y),
                arrowprops=dict(arrowstyle='<-', lw=5, color='#000000'), zorder=2)
    
    # Color scheme
    colors = ['#0052CC', '#006644', '#CC5500', '#CC0000', '#6600CC']
    
    # Plot events - all leaning to the right
    for i, (event, year) in enumerate(sorted_events):
        x = int(year)
        color = colors[i % len(colors)]
        
        # Vertical line - thicker
        ax.plot([x, x], [timeline_y - 0.3, timeline_y + 2.0], 
                color=color, linewidth=4, zorder=3)
        
        # Event text - all leaning right at 35 degrees
        # Stagger the vertical position for better readability
        text_y = 2.2 + (i % 3) * 0.4  # Slight vertical staggering
        
        # Truncate long text if needed
        display_text = event if len(event) <= 35 else event[:32] + '...'
        
        ax.text(x + 0.3, text_y, display_text,
                rotation=35,  # All text at 35 degrees
                ha='left',
                va='bottom',
                fontsize=22,  # Very large font
                color=color,
                fontweight='bold',
                zorder=5,
                fontfamily='Arial')
        
        # Year label with background - bigger
        ax.text(x, -1.2, str(year),
                ha='center',
                va='center',
                fontsize=22,  # Larger year font
                fontweight='bold',
                color=color,
                bbox=dict(boxstyle="round,pad=0.4",
                         facecolor='white',
                         edgecolor=color,
                         linewidth=3),
                zorder=5)
        
        # Timeline dot - bigger
        ax.scatter(x, timeline_y, s=300, c=color,
                  edgecolors='white', linewidth=4, zorder=6)
    
    # Add subtle decade markers
    for decade in range((min_year//10) * 10, max_year + 10, 10):
        if min_year < decade < max_year:
            # Check if decade marker is too close to an event
            too_close = False
            for event, year_str in sorted_events:
                if abs(decade - int(year_str)) < 2:
                    too_close = True
                    break
            
            if not too_close:
                ax.axvline(x=decade, ymin=0.45, ymax=0.55,
                          color='#dddddd', linewidth=1.5, alpha=0.5, zorder=0)
                ax.text(decade, -2.5, str(decade), ha='center', va='top',
                       fontsize=12, alpha=0.4, color='#999999')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Clean white background
    ax.set_facecolor('white')
    
    # Tight layout with padding
    plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)
    
    # Display
    st.pyplot(fig)
    plt.close()

def display_choice_buttons(options):
    """Display simple choice buttons (before/after, yes/no)"""
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        with cols[i]:
            if st.button(option.capitalize(), key=f"choice_{i}", use_container_width=True):
                st.session_state.user_answer = option
                st.session_state.answer_submitted = True
                st.rerun()

def display_multiple_choice(options):
    """Display multiple choice options"""
    cols = st.columns(2)
    for i, option in enumerate(options):
        with cols[i % 2]:
            if st.button(option, key=f"mc_{i}", use_container_width=True):
                st.session_state.user_answer = option
                st.session_state.answer_submitted = True
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if not st.session_state.show_feedback:
        user_answer = st.session_state.user_answer
        correct_answer = st.session_state.correct_answer
        data = st.session_state.timeline_data
        
        if user_answer.lower() == correct_answer.lower():
            st.success("🎉 **Excellent! That's correct!**")
            
            # Show explanation based on question type
            show_explanation(data, correct=True)
            
            # Increase difficulty
            st.session_state.consecutive_correct += 1
            if st.session_state.consecutive_correct >= 2 and st.session_state.timeline_difficulty < 4:
                st.session_state.timeline_difficulty += 1
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.timeline_difficulty}**")
                st.session_state.consecutive_correct = 0
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
            
            # Show explanation
            show_explanation(data, correct=False)
            
            # Decrease difficulty
            st.session_state.consecutive_correct = 0
            if st.session_state.timeline_difficulty > 1:
                st.session_state.timeline_difficulty -= 1
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.timeline_difficulty}**")
        
        st.session_state.show_feedback = True
        st.session_state.total_attempted += 1

def show_explanation(data, correct):
    """Show detailed explanation for the answer"""
    question_type = data.get('question_type', '')
    
    with st.expander("📖 **Understanding the Timeline**", expanded=not correct):
        if question_type == 'before_after_time':
            st.markdown("""
            **How to solve:**
            1. Find the event on the timeline
            2. Check its time
            3. Compare with the given time
            4. Determine if it's before or after
            """)
            
        elif question_type == 'by_time':
            st.markdown("""
            **How to solve:**
            1. Find the event on the timeline
            2. Check when it happens
            3. Compare with the given time
            4. Answer yes if it happens before that time, no if after
            """)
            
        elif question_type == 'which_later' or question_type == 'which_first':
            st.markdown("""
            **How to solve:**
            1. Find all mentioned events on the timeline
            2. Compare their times
            3. Choose the earliest (for first) or latest (for later)
            """)
            
        elif question_type == 'time_between':
            st.markdown("""
            **How to calculate time between events:**
            1. Find both events on the timeline
            2. Note their times
            3. Calculate the difference
            4. Remember: From A.M. to P.M. crosses noon
            """)
            
        elif question_type == 'between_years':
            st.markdown("""
            **How to find events between years:**
            1. Identify the year range given
            2. Check each event's year
            3. Select events that fall within the range
            4. Remember: "Between" includes the boundary years
            """)
            
        elif question_type == 'years_between':
            st.markdown("""
            **How to calculate years between events:**
            1. Find both events on the timeline
            2. Note their years
            3. Subtract the earlier year from the later year
            """)
            
        elif question_type == 'between_events':
            st.markdown("""
            **How to find events between two other events:**
            1. Locate both boundary events on the timeline
            2. Identify all events that occur between them
            3. Select the correct event from the options
            """)
            
        elif question_type == 'last_in_period':
            st.markdown("""
            **How to find the last event in a time period:**
            1. Identify the time period boundaries
            2. Find all events within that period
            3. Choose the one that happens latest
            """)
            
        elif question_type == 'specific_period':
            st.markdown("""
            **How to identify events in a specific period:**
            1. Understand the period (e.g., Monday afternoon = 12 P.M. to 6 P.M.)
            2. Check which events fall within that time range
            3. Select the correct event from the options
            """)
            
        elif question_type == 'count_events':
            st.markdown("""
            **How to count events meeting a criteria:**
            1. Identify the criteria (e.g., after 3:00 P.M.)
            2. Check each event against the criteria
            3. Count how many events meet it
            """)
            
        elif question_type == 'which_last':
            st.markdown("""
            **How to find the last event:**
            1. Look at all events on the timeline
            2. Compare their times/years
            3. Choose the one that happens latest
            """)
            
        elif question_type == 'which_earlier':
            st.markdown("""
            **How to find the earlier event:**
            1. Look at the events mentioned in the options
            2. Find them on the timeline
            3. Choose the one that happens first
            """)

def reset_timeline_state():
    """Reset the timeline state for next question"""
    st.session_state.current_timeline = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.timeline_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer