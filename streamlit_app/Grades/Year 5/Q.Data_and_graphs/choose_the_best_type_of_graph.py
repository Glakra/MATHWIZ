import streamlit as st
import random

def run():
    """
    Main function to run the Choose the Best Type of Graph activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/Q.Data_and_graphs/choose_the_best_type_of_graph.py
    """
    # Initialize session state
    if "graph_choice_difficulty" not in st.session_state:
        st.session_state.graph_choice_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Q. Data and graphs**")
    st.title("📊 Choose the Best Type of Graph")
    st.markdown("*Learn when to use picture graphs, bar graphs, and line graphs*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.graph_choice_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Graph Types",
            2: "Time & Categories",
            3: "Groups & Multiples",
            4: "Complex Scenarios"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
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
        if st.button("← Back", type="secondary"):
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
    with st.expander("📚 **When to Use Each Graph Type**", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 📊 Bar Graph
            **Best for:**
            - Comparing different categories
            - Showing amounts for different groups
            - Data that doesn't change over time
            
            **Examples:**
            - Number of students in each class
            - Favourite colours in a survey
            - Sales of different products
            - Heights of different buildings
            """)
        
        with col2:
            st.markdown("""
            ### 📈 Line Graph
            **Best for:**
            - Showing change over time
            - Displaying trends
            - Continuous data
            
            **Examples:**
            - Temperature throughout the day
            - Population growth over years
            - Weekly sales data
            - Height of a plant over months
            """)
        
        with col3:
            st.markdown("""
            ### 🖼️ Picture Graph
            **Best for:**
            - Data in groups or bundles
            - When items come in sets
            - Making data visual and fun
            - When each symbol = multiple items
            
            **Examples:**
            - Books in stacks of 10
            - Eggs in dozens
            - Staples in rows of 50
            - Cars in lots of 100
            """)
        
        st.markdown("---")
        st.info("""
        💡 **Quick Decision Guide:**
        - **Over time?** → Line graph
        - **Different categories?** → Bar graph  
        - **Groups/multiples?** → Picture graph
        """)

def generate_new_problem():
    """Generate a new graph choice problem"""
    difficulty = st.session_state.graph_choice_difficulty
    
    # Define scenarios by difficulty level
    if difficulty == 1:
        scenarios = get_basic_scenarios()
    elif difficulty == 2:
        scenarios = get_intermediate_scenarios()
    elif difficulty == 3:
        scenarios = get_advanced_scenarios()
    else:
        scenarios = get_expert_scenarios()
    
    # Choose a random scenario
    scenario = random.choice(scenarios)
    
    # Store problem data
    st.session_state.problem_data = scenario
    st.session_state.correct_answer = scenario["correct_answer"]
    st.session_state.current_problem = scenario["question"]

def get_basic_scenarios():
    """Basic scenarios - clear distinctions between graph types"""
    return [
        {
            "question": "Which type of graph would you use to show the number of pets owned by different students?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph is best for comparing different categories (different students).",
            "hint": "You're comparing amounts for different people."
        },
        {
            "question": "Which is the best type of graph to show the temperature each hour during the day?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows change over time, perfect for temperature throughout the day.",
            "hint": "Temperature changes continuously over time."
        },
        {
            "question": "Which type of graph would best show the number of students in each year level?",
            "options": ["bar graph", "line graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different categories (year levels).",
            "hint": "You're comparing different groups."
        },
        {
            "question": "Which is the best type of graph to show your height measured each month for a year?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows change over time, perfect for tracking growth.",
            "hint": "You want to see how something changes over time."
        },
        {
            "question": "Which type of graph would you use to show the favourite ice cream flavours in your class?",
            "options": ["bar graph", "line graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different categories (ice cream flavours).",
            "hint": "You're comparing different choices."
        }
    ]

def get_intermediate_scenarios():
    """Intermediate scenarios - time vs categories focus"""
    return [
        {
            "question": "Which is the best type of graph to show the number of students who earned extra credit each day this week?",
            "options": ["picture graph", "line graph", "bar graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows daily changes over the week (time period).",
            "hint": "You're tracking something each day over a week."
        },
        {
            "question": "Which type of graph would you use to show the number of teachers in each school in a city?",
            "options": ["line graph", "bar graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different schools (categories).",
            "hint": "You're comparing different schools."
        },
        {
            "question": "Which type of graph would you use to show the population of a city each year for ten years?",
            "options": ["picture graph", "line graph", "bar graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows change over years (time).",
            "hint": "Population changes over years."
        },
        {
            "question": "Which is the best type of graph to show the length of four different books?",
            "options": ["bar graph", "line graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different items (books).",
            "hint": "You're comparing different books."
        },
        {
            "question": "Which type of graph would you use to show the number of cars sold in four different colours?",
            "options": ["bar graph", "line graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different categories (car colours).",
            "hint": "You're comparing different colours."
        },
        {
            "question": "Which is the best type of graph to show the number of books borrowed from the school library each week this month?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows weekly changes over time.",
            "hint": "You're tracking something each week over a month."
        },
        {
            "question": "Which type of graph would you use to show the number of students in each grade?",
            "options": ["bar graph", "line graph"],
            "correct_answer": "bar graph",
            "explanation": "A bar graph compares different grades (categories).",
            "hint": "You're comparing different grades."
        }
    ]

def get_advanced_scenarios():
    """Advanced scenarios - including picture graphs for multiples"""
    return [
        {
            "question": "Which type of graph would best show the number of staples used by each teacher, if the staples come in rows of 50?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "picture graph",
            "explanation": "A picture graph works well when items come in groups (rows of 50).",
            "hint": "The staples come in groups of 50."
        },
        {
            "question": "Which is the best type of graph to show the number of books on each cart, if the books are in stacks of ten?",
            "options": ["line graph", "bar graph", "picture graph"],
            "correct_answer": "picture graph",
            "explanation": "A picture graph is perfect when items are grouped (stacks of 10).",
            "hint": "The books come in stacks of 10."
        },
        {
            "question": "Which is the best type of graph to show the number of tins three students collected for a tin drive, if each bag can hold 100 tins?",
            "options": ["line graph", "picture graph", "bar graph"],
            "correct_answer": "picture graph",
            "explanation": "A picture graph works well for items in large groups (bags of 100).",
            "hint": "The tins are collected in bags of 100."
        },
        {
            "question": "Which type of graph would you use to show the number of cartons of milk sold each day, if milk comes in crates of 24?",
            "options": ["picture graph", "line graph", "bar graph"],
            "correct_answer": "picture graph",
            "explanation": "A picture graph is ideal when items come in fixed groups (crates of 24).",
            "hint": "The milk comes in crates of 24."
        },
        {
            "question": "Which is the best type of graph to show rainfall amounts each month for a year?",
            "options": ["picture graph", "bar graph", "line graph"],
            "correct_answer": "line graph",
            "explanation": "A line graph shows monthly changes over the year.",
            "hint": "You're tracking changes each month."
        },
        {
            "question": "Which type of graph would show the number of pencils in each classroom, if pencils come in boxes of 12?",
            "options": ["line graph", "picture graph", "bar graph"],
            "correct_answer": "picture graph",
            "explanation": "A picture graph is great for items that come in sets (boxes of 12).",
            "hint": "Pencils come in boxes of 12."
        }
    ]

def get_expert_scenarios():
    """Expert scenarios - complex real-world situations"""
    return [
        {
            "question": "A scientist measures bacteria growth every hour. Which graph should she use?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "line graph",
            "explanation": "Line graphs show continuous change over time, perfect for growth data.",
            "hint": "Growth is continuous over time."
        },
        {
            "question": "A store wants to show sales of 5 different phone models last month. Which graph is best?",
            "options": ["line graph", "bar graph", "picture graph"],
            "correct_answer": "bar graph",
            "explanation": "Bar graphs compare different categories (phone models).",
            "hint": "Comparing different products."
        },
        {
            "question": "You want to show the number of boxes of cookies sold by each scout, if cookies come in cases of 12 boxes. Which graph?",
            "options": ["bar graph", "picture graph", "line graph"],
            "correct_answer": "picture graph",
            "explanation": "Picture graphs work well when items come in groups (cases of 12).",
            "hint": "Cookies come in cases of 12 boxes."
        },
        {
            "question": "A weather station records wind speed every 30 minutes during a storm. Which graph should they use?",
            "options": ["picture graph", "bar graph", "line graph"],
            "correct_answer": "line graph",
            "explanation": "Line graphs show continuous change over time periods.",
            "hint": "Wind speed changes continuously over time."
        },
        {
            "question": "A teacher wants to show test scores for 6 different subjects. Which graph is most appropriate?",
            "options": ["line graph", "picture graph", "bar graph"],
            "correct_answer": "bar graph",
            "explanation": "Bar graphs compare different categories (subjects).",
            "hint": "Comparing scores across different subjects."
        },
        {
            "question": "A company tracks website visitors each hour for 24 hours. Which graph should they use?",
            "options": ["bar graph", "line graph", "picture graph"],
            "correct_answer": "line graph",
            "explanation": "Line graphs show hourly changes over a time period.",
            "hint": "Tracking changes every hour."
        },
        {
            "question": "A school wants to display the number of computers in each classroom, if computers come in sets of 5. Which graph?",
            "options": ["line graph", "bar graph", "picture graph"],
            "correct_answer": "picture graph",
            "explanation": "Picture graphs are ideal when items come in sets (sets of 5).",
            "hint": "Computers come in sets of 5."
        },
        {
            "question": "A gym tracks member check-ins each day for a month. Which graph type is best?",
            "options": ["picture graph", "line graph", "bar graph"],
            "correct_answer": "line graph",
            "explanation": "Line graphs show daily patterns over time.",
            "hint": "Tracking daily changes over a month."
        }
    ]

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown(f"### 📝 {st.session_state.current_problem}")
    
    # Add hint button
    if st.button("💡 Need a hint?", key="hint_btn"):
        st.info(f"**Hint:** {data.get('hint', 'Think about what you are comparing!')}")
    
    st.markdown("---")
    
    # Display options as clickable tiles
    options = data["options"]
    
    # Determine layout
    if len(options) == 2:
        cols = st.columns(2)
    else:
        cols = st.columns(3)
    
    # Create buttons for each option
    for i, option in enumerate(options):
        with cols[i]:
            # Add emoji for each graph type
            emoji_map = {
                "bar graph": "📊",
                "line graph": "📈",
                "picture graph": "🖼️"
            }
            emoji = emoji_map.get(option, "📊")
            
            button_label = f"{emoji}\n{option}"
            
            if st.button(
                button_label,
                key=f"option_{i}",
                use_container_width=True,
                disabled=st.session_state.answer_submitted,
                help=f"Click to select {option}"
            ):
                st.session_state.user_answer = option
                check_answer()
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation buttons
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 See Explanation", type="secondary", use_container_width=True):
                show_detailed_explanation()
            
            if st.button("Next Question →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        # Show progress
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%", 
                         f"{st.session_state.total_correct}/{st.session_state.total_attempted}")

def check_answer():
    """Check if the user's answer is correct"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    st.session_state.answer_correct = (user_answer == correct_answer)
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if st.session_state.answer_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    
    if st.session_state.answer_correct:
        correct_title = st.session_state.correct_answer.title()
        st.success(f"✅ **Correct! {correct_title} is the best choice!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.graph_choice_difficulty
            st.session_state.graph_choice_difficulty = min(
                st.session_state.graph_choice_difficulty + 1, 4
            )
            
            if st.session_state.graph_choice_difficulty > old_difficulty:
                st.balloons()
                level = st.session_state.graph_choice_difficulty
                st.info(f"🎉 **Excellent! Moving to Level {level}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. The best choice is {st.session_state.correct_answer}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.graph_choice_difficulty
            st.session_state.graph_choice_difficulty = max(
                st.session_state.graph_choice_difficulty - 1, 1
            )
            
            if st.session_state.graph_choice_difficulty < old_difficulty:
                level = st.session_state.graph_choice_difficulty
                st.warning(f"⬇️ **Let's practice at Level {level}**")
                st.session_state.consecutive_wrong = 0

def show_detailed_explanation():
    """Show detailed explanation of why each graph type would or wouldn't work"""
    with st.expander("📚 **Detailed Explanation**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown(f"### Why {st.session_state.correct_answer} is best:")
        st.success(data['explanation'])
        
        st.markdown("### Let's think about each option:")
        
        # Explain each graph type for this scenario
        options = data['options']
        for option in options:
            if option == st.session_state.correct_answer:
                reason = get_graph_reason(option, data)
                st.markdown(f"**✅ {option.title()}:** Perfect choice! {reason}")
            else:
                reason = get_why_not_reason(option, data)
                st.markdown(f"**❌ {option.title()}:** Not ideal because {reason}")
        
        # Add visual guide
        st.markdown("---")
        st.markdown("### 🎯 Remember the key questions:")
        st.markdown("""
        1. **Is it changing over time?** → Line graph
        2. **Are you comparing different things?** → Bar graph
        3. **Do items come in groups/sets?** → Picture graph
        """)

def get_graph_reason(graph_type, data):
    """Get positive reason for using this graph type"""
    reasons = {
        "line graph": "Shows trends and changes over time clearly.",
        "bar graph": "Makes it easy to compare different categories.",
        "picture graph": "Great for visualizing grouped data with symbols."
    }
    return reasons.get(graph_type, "")

def get_why_not_reason(graph_type, data):
    """Get reason why this graph type isn't ideal"""
    question_lower = data['question'].lower()
    
    # Check for time-based questions
    time_keywords = ["over time", "each day", "each week", "each month", "each year", "each hour", "every"]
    is_time_based = any(keyword in question_lower for keyword in time_keywords)
    
    # Check for grouped data
    group_keywords = ["stacks", "rows", "groups", "sets", "boxes", "cases", "crates", "bags"]
    is_grouped = any(keyword in question_lower for keyword in group_keywords)
    
    if is_time_based:
        # Time-based question
        reasons = {
            "bar graph": "bar graphs don't show trends over time as clearly.",
            "picture graph": "picture graphs don't show continuous change well."
        }
    elif is_grouped:
        # Grouped data
        reasons = {
            "line graph": "line graphs don't show grouped data effectively.",
            "bar graph": "bar graphs don't emphasize the grouped nature of the data."
        }
    else:
        # Category comparison (default)
        reasons = {
            "line graph": "this doesn't involve change over time.",
            "bar graph": "this isn't about comparing different categories.",
            "picture graph": "the data doesn't come in natural groups or sets."
        }
    
    return reasons.get(graph_type, "it doesn't match the data type.")

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct