import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Quotients: Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/estimate_quotients_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "estimate_word_difficulty" not in st.session_state:
        st.session_state.estimate_word_difficulty = 1  # Start with simple problems
    
    if "current_estimate_word_problem" not in st.session_state:
        st.session_state.current_estimate_word_problem = None
        st.session_state.correct_estimate_word_answer = None
        st.session_state.show_estimate_word_feedback = False
        st.session_state.estimate_word_answer_submitted = False
        st.session_state.estimate_word_problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("📝 Estimate Quotients: Word Problems")
    st.markdown("*Use estimation to solve real-world division problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.estimate_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple scenarios (small numbers & everyday situations)",
            2: "Intermediate scenarios (medium numbers & school/work)", 
            3: "Advanced scenarios (large numbers & complex situations)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
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
    if st.session_state.current_estimate_word_problem is None:
        generate_new_estimate_word_problem()
    
    # Display current question
    display_estimate_word_problem()
    
    # Instructions section
    show_instructions()

def show_instructions():
    """Display the instructions in an expandable section"""
    with st.expander("💡 **Estimation Word Problem Strategies**", expanded=False):
        st.markdown("""
        ### Why Estimate in Word Problems?
        Real-life situations where estimation is perfect:
        - About how many...? - Exact answers are not needed
        - Quick decision making - Fast estimates help with planning
        - Checking reasonableness - Is my calculator answer realistic?
        - Mental math - Solve problems without paper or calculator
        
        ### Step-by-Step Strategy:
        
        **Step 1: Identify the Division**
        Look for keywords that signal division:
        - How many groups of...
        - How many items per...
        - About how many...
        - Each costs... total budget...
        
        **Step 2: Find the Numbers**
        - Total amount (dividend)
        - Size of each group or cost per item (divisor)
        
        **Step 3: Round for Easy Division**
        Make the numbers friendly for mental math:
        - Round to nearest 10, 50, or 100
        - Choose numbers that divide easily
        
        **Step 4: Estimate the Division**
        Use the rounded numbers to estimate quickly.
        
        **Step 5: Check Answer Choices**
        Pick the estimate closest to your calculation.
        
        ### Example Walkthrough:
        A tour group has $245 to buy train tickets. Each ticket costs $8. About how many tickets can they buy?
        
        Step 1: This is asking how many groups of $8 in $245
        Step 2: Total = $245, Cost per ticket = $8  
        Step 3: Round $245 to $240 (easy to divide by 8)
        Step 4: $240 ÷ $8 = 30 tickets
        Step 5: Choose 30 from the options
        
        ### Another Example:
        Jamie has 156 stickers. She puts 7 stickers on each page. About how many pages can she fill?
        
        Step 1: This is asking how many groups of 7 in 156
        Step 2: Total = 156 stickers, Per page = 7 stickers
        Step 3: Round 156 to 140 (easy to divide by 7)
        Step 4: 140 ÷ 7 = 20 pages
        Step 5: Choose 20 from the options
        
        ### Quick Estimation Tricks:
        
        **Money Problems:**
        - Divide by $5: Think how many $5 bills?
        - Divide by $10: Drop the last zero
        - Divide by $25: Think quarters in dollars
        
        **Time Problems:**
        - Divide by 60: Convert hours to minutes
        - Divide by 24: Days to hours
        - Divide by 7: Weeks to days
        
        **Quantity Problems:**
        - Divide by 10: Move decimal point left
        - Divide by 100: Move decimal point left twice
        - Divide by 5: Double then divide by 10
        
        ### Common Scenarios:
        
        **Shopping & Budget:**
        - How many items can I buy with $X?
        - About how much per person?
        
        **Transportation & Travel:**
        - How many trips needed?
        - About how many people per vehicle?
        
        **Time & Scheduling:**
        - How many sessions possible?
        - About how many minutes per activity?
        
        **School & Learning:**
        - How many problems to solve?
        - About how many books per shelf?
        
        ### Remember:
        - Estimation should be quick - do not spend time on exact calculation
        - Round strategically - make the math easier
        - Check reasonableness - does your estimate make sense?
        - Context matters - think about what is realistic in the situation
        """)

def generate_new_estimate_word_problem():
    """Generate a new estimation word problem based on difficulty"""
    difficulty = st.session_state.estimate_word_difficulty
    
    # Problem scenarios with different contexts
    scenarios = {
        1: [  # Beginner (simpler numbers and contexts)
            {
                "template": "A tour group has ${total} to buy train tickets. Each ticket costs ${divisor}. About how many train tickets can the group buy?",
                "context": "transportation",
                "total_range": (180, 350),
                "divisors": [6, 7, 8, 9, 12, 15]
            },
            {
                "template": "Tom has {total} minutes to complete homework problems. Each problem takes about {divisor} minutes. About how many problems can he complete?",
                "context": "time",
                "total_range": (95, 280),
                "divisors": [4, 5, 6, 7, 8]
            },
            {
                "template": "There are {total} students going on a field trip. Each bus holds {divisor} students. About how many buses are needed?",
                "context": "transportation",
                "total_range": (125, 350),
                "divisors": [15, 18, 20, 25, 30]
            },
            {
                "template": "A baker made {total} cookies. She puts {divisor} cookies in each box. About how many boxes can she fill?",
                "context": "packaging",
                "total_range": (150, 380),
                "divisors": [6, 8, 9, 12, 15]
            },
            {
                "template": "Jake collected {total} bottle caps. He organizes them in groups of {divisor}. About how many groups can he make?",
                "context": "organizing",
                "total_range": (85, 290),
                "divisors": [4, 5, 6, 7, 8]
            },
            {
                "template": "Maria is reading a {total}-page book. She reads about {divisor} pages each day. About how many days will it take her to finish?",
                "context": "reading",
                "total_range": (95, 280),
                "divisors": [4, 5, 6, 7, 8]
            }
        ],
        
        2: [  # Intermediate (larger numbers, more complex scenarios)
            {
                "template": "A school ordered {total} pencils for the year. Each classroom gets {divisor} pencils. About how many classrooms will receive pencils?",
                "context": "education",
                "total_range": (850, 1800),
                "divisors": [25, 30, 35, 40, 45]
            },
            {
                "template": "A factory produces {total} widgets per day. They pack {divisor} widgets in each shipping container. About how many containers do they need daily?",
                "context": "manufacturing",
                "total_range": (750, 1600),
                "divisors": [18, 20, 24, 25, 30]
            },
            {
                "template": "A video game has {total} points to collect. Each level gives you {divisor} points. About how many levels are in the game?",
                "context": "gaming",
                "total_range": (950, 1600),
                "divisors": [35, 40, 45, 50, 60]
            },
            {
                "template": "A farmer harvested {total} pounds of apples. Each crate holds {divisor} pounds. About how many crates will he need?",
                "context": "farming",
                "total_range": (1200, 2000),
                "divisors": [40, 50, 60, 75, 80]
            },
            {
                "template": "Jamie is saving aluminum cans. She has {total} cans and puts {divisor} cans in each bag. About how many bags will she fill?",
                "context": "recycling",
                "total_range": (875, 1650),
                "divisors": [25, 30, 35, 40, 50]
            }
        ],
        
        3: [  # Advanced (large numbers, complex scenarios)
            {
                "template": "A stadium can hold {total} people. Each section holds {divisor} people. About how many sections are in the stadium?",
                "context": "entertainment",
                "total_range": (15000, 45000),
                "divisors": [450, 500, 600, 750, 850]
            },
            {
                "template": "A university has {total} students enrolled. Each lecture hall holds {divisor} students. About how many lecture halls are needed for full capacity?",
                "context": "education",
                "total_range": (18000, 42000),
                "divisors": [120, 150, 180, 200, 250]
            },
            {
                "template": "A city recycles {total} pounds of materials each month. Each recycling truck can carry {divisor} pounds. About how many truck loads are needed monthly?",
                "context": "recycling",
                "total_range": (25000, 60000),
                "divisors": [800, 1000, 1200, 1500, 2000]
            },
            {
                "template": "A construction project requires {total} tons of concrete. Each concrete truck carries {divisor} tons. About how many truck deliveries are needed?",
                "context": "construction",
                "total_range": (1800, 4200),
                "divisors": [8, 10, 12, 15, 18]
            }
        ]
    }
    
    # Select random scenario from current difficulty
    scenario = random.choice(scenarios[difficulty])
    
    # Generate numbers
    total = random.randint(*scenario["total_range"])
    divisor = random.choice(scenario["divisors"])
    
    # Calculate exact quotient for creating options
    exact_quotient = total / divisor
    
    # Create the best estimate (rounded to nearest 5 or 10)
    if exact_quotient < 50:
        best_estimate = round(exact_quotient / 5) * 5
    elif exact_quotient < 100:
        best_estimate = round(exact_quotient / 10) * 10
    else:
        best_estimate = round(exact_quotient / 20) * 20
    
    # Create distractor options
    options = [best_estimate]
    
    # Add 3 other plausible but incorrect options
    multipliers = [0.5, 0.7, 1.4, 1.8, 2.0, 2.5]
    for multiplier in multipliers:
        distractor = int(best_estimate * multiplier)
        if distractor != best_estimate and distractor > 0 and distractor not in options:
            options.append(distractor)
        if len(options) >= 4:
            break
    
    # If we need more options, add some calculated differently
    while len(options) < 4:
        if difficulty == 1:
            distractor = best_estimate + random.choice([-15, -10, -5, 5, 10, 15, 20])
        elif difficulty == 2:
            distractor = best_estimate + random.choice([-30, -20, -10, 10, 20, 30, 40])
        else:
            distractor = best_estimate + random.choice([-50, -30, -20, 20, 30, 50, 80])
        
        if distractor > 0 and distractor not in options:
            options.append(distractor)
    
    # Limit to 4 options and sort
    options = sorted(options[:4])
    random.shuffle(options)  # Shuffle so correct answer is not always first
    
    # Create problem text
    problem_text = scenario["template"].format(total=total, divisor=divisor)
    
    st.session_state.estimate_word_problem_data = {
        "problem_text": problem_text,
        "total": total,
        "divisor": divisor,
        "exact_quotient": exact_quotient,
        "options": options,
        "context": scenario["context"]
    }
    st.session_state.correct_estimate_word_answer = best_estimate
    st.session_state.current_estimate_word_problem = problem_text

def display_estimate_word_problem():
    """Display the current estimation word problem interface"""
    data = st.session_state.estimate_word_problem_data
    
    # Display question header
    st.markdown("### 📝 Estimation Word Problem:")
    
    # Display the problem in a nice box
    problem_html = f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #4682b4;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        color: #333;
    ">
        {data['problem_text']} <strong>Choose the better estimate.</strong>
    </div>
    """
    st.markdown(problem_html, unsafe_allow_html=True)
    
    # Show the estimation hint
    if '$' in data['problem_text']:
        hint_msg = f"Think about ${data['total']:,} ÷ ${data['divisor']} = ?"
    else:
        hint_msg = f"Think about {data['total']:,} ÷ {data['divisor']} = ?"
    
    hint_html = f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 4px solid #6c757d;
        font-size: 16px;
        margin: 20px 0;
        text-align: center;
        color: #495057;
    ">
        💡 <strong>Estimation Hint:</strong> {hint_msg}
    </div>
    """
    st.markdown(hint_html, unsafe_allow_html=True)
    
    # Display answer options
    st.markdown("**Choose the best estimate:**")
    
    # Create option buttons in a 2x2 grid
    col1, col2 = st.columns(2)
    
    for i, option in enumerate(data['options']):
        col_index = i % 2
        with col1 if col_index == 0 else col2:
            if st.button(f"{option:,}", use_container_width=True, type="secondary", key=f"word_option_{i}"):
                st.session_state.user_estimate_word_answer = option
                st.session_state.show_estimate_word_feedback = True
                st.session_state.estimate_word_answer_submitted = True
                st.rerun()
    
    # Show feedback and next button
    handle_estimate_word_feedback_and_next()

def handle_estimate_word_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_estimate_word_feedback:
        show_estimate_word_feedback()
    
    # Next question button
    if st.session_state.estimate_word_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_estimate_word_question_state()
                st.rerun()

def show_estimate_word_feedback():
    """Display feedback for the submitted estimation word problem answer"""
    user_answer = st.session_state.user_estimate_word_answer
    correct_answer = st.session_state.correct_estimate_word_answer
    data = st.session_state.estimate_word_problem_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That is the better estimate!**")
        
        # Show the complete solution
        exact_quotient = data['exact_quotient']
        st.info(f"✅ **Your estimate: {user_answer:,}** | **Exact answer: {exact_quotient:.1f}**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.estimate_word_difficulty
        st.session_state.estimate_word_difficulty = min(st.session_state.estimate_word_difficulty + 1, 3)
        
        if st.session_state.estimate_word_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You have mastered estimation word problems!**")
        elif old_difficulty < st.session_state.estimate_word_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working on Level {st.session_state.estimate_word_difficulty} problems**")
    
    else:
        st.error(f"❌ **Not the best estimate.** The better estimate is **{correct_answer:,}**.")
        
        # Show how far off they were
        exact_quotient = data['exact_quotient']
        user_error = abs(user_answer - exact_quotient) / exact_quotient * 100
        correct_error = abs(correct_answer - exact_quotient) / exact_quotient * 100
        
        error_info = f"Your choice: {user_answer:,} (off by {user_error:.1f}%) | Better estimate: {correct_answer:,} (off by {correct_error:.1f}%)"
        st.info(error_info)
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.estimate_word_difficulty
        st.session_state.estimate_word_difficulty = max(st.session_state.estimate_word_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.estimate_word_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.estimate_word_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_estimate_word_explanation()

def show_estimate_word_explanation():
    """Show step-by-step explanation of the estimation word problem solution"""
    data = st.session_state.estimate_word_problem_data
    total = data["total"]
    divisor = data["divisor"]
    exact_quotient = data["exact_quotient"]
    correct_answer = st.session_state.correct_estimate_word_answer
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        # Pre-calculate values to avoid complex expressions in strings
        rounded_total_100 = round(total/100)*100
        rounded_total_50 = round(total/50)*50
        estimated_quotient = rounded_total_50 // divisor
        error_percent = abs(correct_answer - exact_quotient) / exact_quotient * 100
        
        explanation_text = f"""
        ### Problem Analysis:
        **What we need to find:** About how many groups of {divisor} are in {total:,}
        
        ### Estimation Strategy:
        **Step 1: Identify the division**
        - This problem asks: {total:,} ÷ {divisor} = ?
        
        **Step 2: Round to make estimation easier**
        - Round {total:,} to a number that divides easily by {divisor}
        - Good choice: {rounded_total_100:,} or {rounded_total_50:,}
        
        **Step 3: Estimate the division**
        Let us try {rounded_total_50:,} ÷ {divisor}:
        - {rounded_total_50:,} ÷ {divisor} = {estimated_quotient:,}
        
        **Step 4: Check against options**
        - Our estimate: about {estimated_quotient:,}
        - Closest option: {correct_answer:,}
        
        ### Verification:
        **Exact calculation:** {total:,} ÷ {divisor} = {exact_quotient:.1f}
        **Best estimate:** {correct_answer:,} (error: {error_percent:.1f}%)
        
        ### Key Points:
        - Estimation should be quick - round to friendly numbers
        - Choose the closest option to your estimate
        - Context matters - think about what makes sense in real life
        """
        
        st.markdown(explanation_text)

def reset_estimate_word_question_state():
    """Reset the question state for next question"""
    st.session_state.current_estimate_word_problem = None
    st.session_state.correct_estimate_word_answer = None
    st.session_state.show_estimate_word_feedback = False
    st.session_state.estimate_word_answer_submitted = False
    st.session_state.estimate_word_problem_data = {}
    if "user_estimate_word_answer" in st.session_state:
        del st.session_state.user_estimate_word_answer