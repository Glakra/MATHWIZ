import streamlit as st
import random

def run():
    """
    Main function to run the Division facts to 10: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D.Division/division_facts_to_10_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "division_word_difficulty" not in st.session_state:
        st.session_state.division_word_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("📝 Division Facts to 10: Word Problems")
    st.markdown("*Solve real-world division problems with equal sharing and grouping*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.division_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Division Word Problems:
        - **Read carefully** to understand what's being shared or grouped
        - **Identify the total amount** (dividend)
        - **Identify how many groups** or people (divisor)
        - **Calculate how much each gets** (quotient)
        
        ### Types of Division Problems:
        1. **Equal Sharing:** "24 cookies shared equally among 6 children"
        2. **Equal Grouping:** "18 pencils put into groups of 3"
        3. **Rate Problems:** "40 miles in 5 hours"
        
        ### Problem-Solving Steps:
        1. **Find the total** (what's being divided)
        2. **Find the groups** (how many parts)
        3. **Set up division:** total ÷ groups = amount per group
        4. **Check your answer** - multiply back to verify
        
        ### Key Words to Look For:
        - **"each"** - usually indicates division
        - **"equally"** - sharing evenly
        - **"groups of"** - making equal groups
        - **"per"** - rate problems (each, every)
        - **"shared among"** - dividing between people
        
        ### Example Problem:
        *"A group of 9 students collected 72 cans. If they each collected the same amount, how many cans did each student collect?"*
        
        **Solution:** 72 ÷ 9 = 8 cans per student
        
        ### Check Your Work:
        **Multiplication Check:** 8 × 9 = 72 ✓
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Division by 1, 2, 5, 10 (easier divisors)
        - **🟠 Level 3:** Division by 3, 4, 6 (medium divisors)
        - **🔴 Level 4-5:** All division facts 1-10 (all divisors)
        
        ### Key Skills:
        - ✅ **Read and comprehend** word problems
        - ✅ **Identify division situations** in real contexts
        - ✅ **Set up division equations** from word problems
        - ✅ **Apply division facts** to solve problems
        """)

def generate_division_word_problems():
    """Generate division word problems based on difficulty level"""
    level = st.session_state.division_word_difficulty
    
    # Define which divisors to use based on difficulty
    if level == 1:
        divisors = [2, 5, 10]  # Easiest facts
    elif level == 2:
        divisors = [1, 2, 3, 5, 10]  # Add 1 and 3
    elif level == 3:
        divisors = [2, 3, 4, 5, 6, 10]  # Add 4 and 6
    elif level == 4:
        divisors = [2, 3, 4, 5, 6, 7, 8, 9, 10]  # Add 7, 8, 9
    else:  # level 5
        divisors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # All facts
    
    # Choose a random divisor
    divisor = random.choice(divisors)
    
    # Generate appropriate quotients based on context
    if divisor == 1:
        quotient = random.randint(1, 20)
    else:
        quotient = random.randint(1, 12)
    
    # Calculate dividend
    dividend = divisor * quotient
    
    # Problem scenarios with various contexts
    scenarios = [
        # School/Classroom contexts
        {
            "template": "A group of {} students collected a total of {} cans for recycling. If they each collected the same amount, how many cans did each student collect?",
            "unit": "cans",
            "context": "recycling"
        },
        {
            "template": "A teacher has {} stickers to give equally to {} students. How many stickers will each student receive?",
            "unit": "stickers",
            "context": "classroom"
        },
        {
            "template": "The school library has {} books to arrange equally on {} shelves. How many books will go on each shelf?",
            "unit": "books",
            "context": "library"
        },
        {
            "template": "A class of {} students needs to form {} equal teams. How many students will be on each team?",
            "unit": "students",
            "context": "teams"
        },
        {
            "template": "There are {} pencils in the supply box. If {} students share them equally, how many pencils does each student get?",
            "unit": "pencils",
            "context": "supplies"
        },
        
        # Food/Cooking contexts
        {
            "template": "A baker made {} cookies and wants to put them equally into {} boxes. How many cookies will be in each box?",
            "unit": "cookies",
            "context": "baking"
        },
        {
            "template": "Mom bought {} apples and divided them equally among {} children. How many apples did each child get?",
            "unit": "apples",
            "context": "sharing_food"
        },
        {
            "template": "A pizza shop cut {} slices of pizza and served them equally to {} customers. How many slices did each customer get?",
            "unit": "slices",
            "context": "pizza"
        },
        {
            "template": "There are {} candies to be shared equally among {} friends. How many candies will each friend receive?",
            "unit": "candies",
            "context": "candy_sharing"
        },
        {
            "template": "A restaurant has {} rolls of bread to distribute equally to {} tables. How many rolls will each table get?",
            "unit": "rolls",
            "context": "restaurant"
        },
        
        # Sports/Games contexts
        {
            "template": "A coach has {} basketballs and {} teams. If the basketballs are shared equally, how many will each team get?",
            "unit": "basketballs",
            "context": "sports"
        },
        {
            "template": "There are {} players who need to be divided into {} equal groups. How many players will be in each group?",
            "unit": "players",
            "context": "game_groups"
        },
        {
            "template": "A gym teacher has {} jump ropes for {} classes. How many jump ropes will each class receive?",
            "unit": "jump ropes",
            "context": "gym_equipment"
        },
        
        # Money contexts
        {
            "template": "Sarah has {} rupees and wants to buy {} identical toys. How much can she spend on each toy?",
            "unit": "rupees",
            "context": "money_spending"
        },
        {
            "template": "A group of {} friends earned {} rupees from a car wash. If they split the money equally, how much will each friend get?",
            "unit": "rupees",
            "context": "earning_money"
        },
        
        # Transportation contexts
        {
            "template": "A school bus travels {} kilometers in {} hours. How many kilometers does it travel per hour?",
            "unit": "kilometers",
            "context": "travel_rate"
        },
        {
            "template": "There are {} students who need to ride in {} cars. If each car carries the same number of students, how many students will ride in each car?",
            "unit": "students",
            "context": "car_sharing"
        },
        
        # Arts/Crafts contexts
        {
            "template": "An art teacher has {} crayons to distribute equally to {} students. How many crayons will each student receive?",
            "unit": "crayons",
            "context": "art_supplies"
        },
        {
            "template": "There are {} sheets of paper to be divided equally among {} groups. How many sheets will each group get?",
            "unit": "sheets",
            "context": "craft_materials"
        },
        
        # Garden/Nature contexts
        {
            "template": "A gardener planted {} flowers in {} equal rows. How many flowers are in each row?",
            "unit": "flowers",
            "context": "gardening"
        },
        {
            "template": "There are {} seeds to be planted equally in {} pots. How many seeds will go in each pot?",
            "unit": "seeds",
            "context": "planting"
        },
        
        # Home/Family contexts
        {
            "template": "Mom has {} chores to divide equally among {} children. How many chores will each child do?",
            "unit": "chores",
            "context": "household_tasks"
        },
        {
            "template": "There are {} toys to be put away in {} toy boxes. If each box gets the same number, how many toys go in each box?",
            "unit": "toys",
            "context": "organizing"
        },
        
        # Time-based contexts
        {
            "template": "A project takes {} hours to complete. If {} people work on it equally, how many hours will each person work?",
            "unit": "hours",
            "context": "work_time"
        },
        {
            "template": "There are {} minutes of free time to be divided equally among {} activities. How many minutes will be spent on each activity?",
            "unit": "minutes",
            "context": "time_management"
        },
        
        # Collection contexts
        {
            "template": "A collector has {} stamps to organize into {} albums. How many stamps will go in each album?",
            "unit": "stamps",
            "context": "collecting"
        },
        {
            "template": "There are {} marbles to be shared equally among {} children. How many marbles will each child get?",
            "unit": "marbles",
            "context": "marble_sharing"
        }
    ]
    
    # Choose random scenario
    scenario = random.choice(scenarios)
    
    # Create the problem text
    problem_text = scenario["template"].format(divisor, dividend)
    
    return {
        "problem": problem_text,
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "unit": scenario["unit"],
        "context": scenario["context"]
    }

def generate_new_question():
    """Generate a new division word problem"""
    question_data = generate_division_word_problems()
    
    st.session_state.question_data = question_data
    st.session_state.correct_answer = question_data["quotient"]
    st.session_state.current_question = "Solve this word problem:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the problem in a clean format
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 5px solid #dc3545;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        font-weight: 500;
        color: #2c3e50;
    ">
        {data['problem']}
    </div>
    """, unsafe_allow_html=True)
    
    # Input and submit
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Input field with unit label
            st.markdown(f"**Answer:**")
            
            # Create input layout similar to the image
            input_col1, input_col2 = st.columns([3, 2])
            
            with input_col1:
                user_input = st.number_input(
                    f"",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key="answer_input",
                    label_visibility="collapsed",
                    placeholder="Enter number..."
                )
            
            with input_col2:
                st.markdown(f"**{data['unit']}**", unsafe_allow_html=True)
            
            # Submit button
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            if user_input is not None and user_input >= 0:
                st.session_state.user_answer = int(user_input)
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
            else:
                st.warning("Please enter a valid answer.")
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show the solution
        st.markdown(f"**{data['dividend']} ÷ {data['divisor']} = {correct_answer} {data['unit']}** ✓")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.division_word_difficulty
        st.session_state.division_word_difficulty = min(
            st.session_state.division_word_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.division_word_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 division word problems!**")
        elif old_level < st.session_state.division_word_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.division_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer} {data['unit']}**.")
        
        # Decrease difficulty (min level 1)
        old_level = st.session_state.division_word_difficulty
        st.session_state.division_word_difficulty = max(
            st.session_state.division_word_difficulty - 1, 1
        )
        
        if old_level > st.session_state.division_word_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.division_word_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['problem']}
        
        **Step 1: Identify what we know**
        - Total amount: **{data['dividend']} {data['unit']}**
        - Number of groups/people: **{data['divisor']}**
        - We need to find: Amount per group/person
        
        **Step 2: Set up the division**
        {data['dividend']} ÷ {data['divisor']} = ?
        
        **Step 3: Calculate**
        {data['dividend']} ÷ {data['divisor']} = **{correct_answer}**
        
        **Final Answer:** {correct_answer} {data['unit']}
        
        ### Check Your Work:
        **Multiply back:** {correct_answer} × {data['divisor']} = {data['dividend']} ✓
        
        This means {data['divisor']} groups of {correct_answer} {data['unit']} each gives us {data['dividend']} {data['unit']} total.
        """)
        
        # Context-specific explanation
        context_explanations = {
            "recycling": f"Each of the {data['divisor']} students collected {correct_answer} cans.",
            "classroom": f"Each of the {data['divisor']} students gets {correct_answer} stickers.",
            "sharing_food": f"Each of the {data['divisor']} children gets {correct_answer} pieces.",
            "sports": f"Each of the {data['divisor']} teams gets {correct_answer} items.",
            "money_spending": f"Each toy costs {correct_answer} rupees.",
            "travel_rate": f"The speed is {correct_answer} kilometers per hour."
        }
        
        if data['context'] in context_explanations:
            st.markdown(f"**Real-world meaning:** {context_explanations[data['context']]}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer