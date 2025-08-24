import streamlit as st
import random

def run():
    """
    Main function to run the Multiply three or more numbers: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C.Multiplication/multiply_three_or_more_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "mult_three_word_difficulty" not in st.session_state:
        st.session_state.mult_three_word_difficulty = 1  # Start with easier problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply Three or More Numbers: Word Problems")
    st.markdown("*Solve real-world problems involving multiple factors*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mult_three_word_difficulty
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
        ### How to Solve Multi-Step Multiplication:
        - **Read carefully** and identify all the numbers you need to multiply
        - **Find the pattern** - look for groups, layers, or repeated structures
        - **Set up the multiplication** with 3 or more factors
        - **Calculate step by step** - multiply from left to right or group smart pairs
        - **Check your answer** makes sense in the real-world context
        
        ### Common Problem Types:
        1. **Arrays/Grids:** rows × columns × items per space
        2. **Time Patterns:** rate × time periods × number of cycles
        3. **Packaging:** items per package × packages per box × number of boxes
        4. **Money Problems:** price × quantity × number of groups
        5. **Building/Construction:** length × width × height or layers
        
        ### Solution Strategies:
        - **Left to Right:** 4 × 3 × 5 = (4 × 3) × 5 = 12 × 5 = 60
        - **Smart Grouping:** 8 × 5 × 2 × 3 = (8 × 2) × (5 × 3) = 16 × 15 = 240
        - **Look for 10s:** 2 × 7 × 5 = (2 × 5) × 7 = 10 × 7 = 70
        
        ### Example Problem:
        *"A bakery makes 4 trays of muffins. Each tray has 6 rows with 3 muffins per row. How many muffins in total?"*
        
        **Solution:** 4 trays × 6 rows × 3 muffins = 72 muffins
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** 3 factors, smaller numbers
        - **🟠 Level 3:** 3-4 factors, medium numbers
        - **🔴 Level 4-5:** 4-5 factors, larger numbers
        
        ### Key Skills:
        - ✅ **Identify** all factors in the problem
        - ✅ **Organize** the multiplication setup
        - ✅ **Calculate** accurately step by step
        - ✅ **Verify** the answer makes sense
        """)

def generate_word_problems():
    """Generate different word problem scenarios based on difficulty"""
    
    level = st.session_state.mult_three_word_difficulty
    
    # Define number ranges and factor counts based on difficulty
    if level == 1:
        num_factors = 3
        ranges = [(2, 5), (2, 4), (2, 6)]
    elif level == 2:
        num_factors = 3
        ranges = [(3, 6), (3, 5), (2, 8)]
    elif level == 3:
        num_factors = random.choice([3, 4])
        if num_factors == 3:
            ranges = [(4, 8), (3, 7), (2, 10)]
        else:
            ranges = [(2, 6), (3, 5), (2, 4), (2, 5)]
    elif level == 4:
        num_factors = random.choice([3, 4, 4])
        if num_factors == 3:
            ranges = [(5, 12), (4, 8), (3, 10)]
        else:
            ranges = [(3, 8), (3, 6), (2, 7), (2, 6)]
    else:  # level 5
        num_factors = random.choice([4, 4, 5])
        if num_factors == 4:
            ranges = [(4, 15), (3, 10), (2, 8), (3, 7)]
        else:
            ranges = [(3, 8), (2, 6), (2, 5), (2, 4), (2, 6)]
    
    # Generate factors
    factors = []
    for i in range(num_factors):
        min_val, max_val = ranges[i] if i < len(ranges) else (2, 8)
        factor = random.randint(min_val, max_val)
        factors.append(factor)
    
    # Problem scenarios based on number of factors
    if num_factors == 3:
        scenarios = [
            # Money scenarios
            {
                "template": "A bake sale is charging ${} per brownie. Each pan of brownies is cut into {} rows, with {} brownies in each row. How much money will the bake sale make if they sell {} pans of brownies?",
                "factors_desc": ["price per brownie", "rows per pan", "brownies per row", "number of pans"],
                "unit": "dollars",
                "context": "bake_sale_money",
                "calculation": "price × rows × brownies per row × pans"
            },
            {
                "template": "Movie tickets cost ${} each. A school is buying tickets for {} classes, with {} students in each class. How much will the school spend on movie tickets?",
                "factors_desc": ["price per ticket", "number of classes", "students per class"],
                "unit": "dollars",
                "context": "movie_tickets_money"
            },
            {
                "template": "A pizza costs ${} per slice. Each pizza is cut into {} slices. If a party orders {} pizzas, how much will they spend?",
                "factors_desc": ["price per slice", "slices per pizza", "number of pizzas"],
                "unit": "dollars",
                "context": "pizza_money"
            },
            {
                "template": "Stickers cost ${} per pack. Each pack has {} sheets with {} stickers per sheet. How much would {} packs cost?",
                "factors_desc": ["price per pack", "sheets per pack", "stickers per sheet", "number of packs"],
                "unit": "dollars",
                "context": "stickers_money",
                "calculation": "price × sheets × stickers per sheet × packs"
            },
            
            # Non-money scenarios
            {
                "template": "A library has {} floors. Each floor has {} shelves, and each shelf holds {} books. How many books can the library hold?",
                "factors_desc": ["number of floors", "shelves per floor", "books per shelf"],
                "unit": "books",
                "context": "library"
            },
            {
                "template": "A garden has {} rows of plants. Each row has {} sections, and each section has {} plants. How many plants are in the garden?",
                "factors_desc": ["number of rows", "sections per row", "plants per section"],
                "unit": "plants",
                "context": "garden"
            },
            {
                "template": "A parking garage has {} levels. Each level has {} rows with {} parking spaces per row. How many parking spaces are there in total?",
                "factors_desc": ["number of levels", "rows per level", "spaces per row"],
                "unit": "parking spaces",
                "context": "parking"
            },
            {
                "template": "A bakery makes {} batches of cookies. Each batch fills {} trays, and each tray holds {} cookies. How many cookies does the bakery make?",
                "factors_desc": ["number of batches", "trays per batch", "cookies per tray"],
                "unit": "cookies",
                "context": "bakery"
            },
            {
                "template": "A school has {} grades. Each grade has {} classes, and each class has {} desks. How many desks are there in the school?",
                "factors_desc": ["number of grades", "classes per grade", "desks per class"],
                "unit": "desks",
                "context": "school_desks"
            },
            {
                "template": "A factory has {} machines. Each machine works {} hours per day and produces {} items per hour. How many items does the factory produce in one day?",
                "factors_desc": ["number of machines", "hours per day", "items per hour"],
                "unit": "items",
                "context": "factory"
            },
            {
                "template": "An apartment building has {} floors. Each floor has {} apartments, and each apartment has {} rooms. How many rooms are there in total?",
                "factors_desc": ["number of floors", "apartments per floor", "rooms per apartment"],
                "unit": "rooms",
                "context": "apartments"
            },
            {
                "template": "A zoo has {} sections. Each section has {} enclosures, and each enclosure houses {} animals. How many animals are in the zoo?",
                "factors_desc": ["number of sections", "enclosures per section", "animals per enclosure"],
                "unit": "animals",
                "context": "zoo"
            },
            {
                "template": "A stadium has {} sections. Each section has {} rows with {} seats per row. How many seats are there in the stadium?",
                "factors_desc": ["number of sections", "rows per section", "seats per row"],
                "unit": "seats",
                "context": "stadium"
            }
        ]
    
    elif num_factors == 4:
        scenarios = [
            # Money scenarios
            {
                "template": "Notebooks cost ${} each. A school orders {} sets, with {} notebooks per set, for {} classrooms. How much does the school spend?",
                "factors_desc": ["price per notebook", "sets per classroom", "notebooks per set", "number of classrooms"],
                "unit": "dollars",
                "context": "notebooks_money"
            },
            {
                "template": "Concert tickets cost ${} each. There are {} sections, {} rows per section, and {} seats per row. If all seats are sold, how much money is collected?",
                "factors_desc": ["price per ticket", "number of sections", "rows per section", "seats per row"],
                "unit": "dollars",
                "context": "concert_money"
            },
            {
                "template": "Art supplies cost ${} per item. A teacher buys {} types of supplies, {} packages of each type, for {} students. How much does she spend?",
                "factors_desc": ["price per item", "types of supplies", "packages per type", "number of students"],
                "unit": "dollars",
                "context": "art_supplies_money"
            },
            
            # Non-money scenarios
            {
                "template": "A warehouse has {} floors. Each floor has {} aisles, {} shelves per aisle, and {} boxes per shelf. How many boxes are stored in the warehouse?",
                "factors_desc": ["number of floors", "aisles per floor", "shelves per aisle", "boxes per shelf"],
                "unit": "boxes",
                "context": "warehouse"
            },
            {
                "template": "A school district has {} schools. Each school has {} grades, {} classes per grade, and {} students per class. How many students are in the district?",
                "factors_desc": ["number of schools", "grades per school", "classes per grade", "students per class"],
                "unit": "students",
                "context": "school_district"
            },
            {
                "template": "A hotel has {} floors. Each floor has {} wings, {} rooms per wing, and {} beds per room. How many beds are there in the hotel?",
                "factors_desc": ["number of floors", "wings per floor", "rooms per wing", "beds per room"],
                "unit": "beds",
                "context": "hotel"
            },
            {
                "template": "A farm has {} barns. Each barn has {} pens, {} animals per pen, and each animal produces {} units of product per day. How many units are produced daily?",
                "factors_desc": ["number of barns", "pens per barn", "animals per pen", "units per animal"],
                "unit": "units",
                "context": "farm_production"
            },
            {
                "template": "A library system has {} branches. Each branch has {} floors, {} sections per floor, and {} books per section. How many books are in the system?",
                "factors_desc": ["number of branches", "floors per branch", "sections per floor", "books per section"],
                "unit": "books",
                "context": "library_system"
            },
            {
                "template": "A theater complex has {} theaters. Each theater has {} sections, {} rows per section, and {} seats per row. How many seats are there in total?",
                "factors_desc": ["number of theaters", "sections per theater", "rows per section", "seats per row"],
                "unit": "seats",
                "context": "theater_complex"
            }
        ]
    
    else:  # 5 factors
        scenarios = [
            # Money scenarios
            {
                "template": "Pencils cost ${} each. A district orders for {} schools, {} grades per school, {} classes per grade, and {} students per class. How much do they spend?",
                "factors_desc": ["price per pencil", "number of schools", "grades per school", "classes per grade", "students per class"],
                "unit": "dollars",
                "context": "pencils_money"
            },
            
            # Non-money scenarios
            {
                "template": "A company has {} buildings. Each building has {} floors, {} departments per floor, {} teams per department, and {} employees per team. How many employees work for the company?",
                "factors_desc": ["number of buildings", "floors per building", "departments per floor", "teams per department", "employees per team"],
                "unit": "employees",
                "context": "company"
            },
            {
                "template": "A storage facility has {} warehouses. Each warehouse has {} zones, {} aisles per zone, {} shelves per aisle, and {} items per shelf. How many items can be stored?",
                "factors_desc": ["number of warehouses", "zones per warehouse", "aisles per zone", "shelves per aisle", "items per shelf"],
                "unit": "items",
                "context": "storage_facility"
            },
            {
                "template": "A university has {} campuses. Each campus has {} colleges, {} departments per college, {} courses per department, and {} students per course. How many course enrollments are there?",
                "factors_desc": ["number of campuses", "colleges per campus", "departments per college", "courses per department", "students per course"],
                "unit": "enrollments",
                "context": "university"
            }
        ]
    
    # Choose random scenario
    scenario = random.choice(scenarios)
    
    # Handle special 4-factor money scenarios (bake sale style)
    if scenario.get("calculation") and num_factors == 3:
        # For scenarios like bake sale that need 4 factors but show as 3-factor template
        factors.append(random.randint(2, 6))  # Add the fourth factor
        num_factors = 4
    
    # Create the problem text
    if num_factors == len(factors):
        problem_text = scenario["template"].format(*factors)
    else:
        # Fallback for mismatched factors
        problem_text = scenario["template"].format(*factors[:num_factors])
    
    # Calculate answer
    answer = 1
    for factor in factors:
        answer *= factor
    
    return {
        "problem": problem_text,
        "factors": factors,
        "answer": answer,
        "unit": scenario["unit"],
        "context": scenario["context"],
        "factors_desc": scenario["factors_desc"][:len(factors)]
    }

def generate_new_question():
    """Generate a new word problem question"""
    question_data = generate_word_problems()
    
    # Generate smart distractors (wrong answers)
    correct = question_data["answer"]
    factors = question_data["factors"]
    
    options = [correct]
    
    # Common mistake patterns for multi-factor problems
    possible_mistakes = [
        # Multiply only some factors
        factors[0] * factors[1] if len(factors) >= 2 else correct + 10,
        factors[0] * factors[1] * factors[2] if len(factors) >= 3 else correct + 20,
        # Add instead of multiply
        sum(factors),
        # Off by one factor
        correct + factors[0] if len(factors) >= 1 else correct + 5,
        correct - factors[-1] if len(factors) >= 1 else correct - 5,
        # Calculation errors
        correct + 10,
        correct - 10,
        correct * 2 // 3,  # Common fraction error
        correct + factors[0] * factors[1] if len(factors) >= 2 else correct + 15,
    ]
    
    # Add unique mistakes to options
    for mistake in possible_mistakes:
        if mistake > 0 and mistake != correct and mistake not in options and len(options) < 4:
            options.append(mistake)
    
    # Fill remaining options with random nearby values
    while len(options) < 4:
        wrong = correct + random.randint(-50, 50)
        if wrong > 0 and wrong != correct and wrong not in options:
            options.append(wrong)
    
    # Shuffle options
    random.shuffle(options)
    
    st.session_state.question_data = {
        "problem": question_data["problem"],
        "options": options,
        "factors": factors,
        "unit": question_data["unit"],
        "context": question_data["context"],
        "factors_desc": question_data["factors_desc"]
    }
    st.session_state.correct_answer = correct
    st.session_state.current_question = "Solve this word problem:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Word Problem:")
    
    # Display the problem in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 5px solid #17a2b8;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        font-weight: 500;
        color: #2c3e50;
    ">
        {data['problem']}
    </div>
    """, unsafe_allow_html=True)
    
    # Show the multiplication setup
    st.markdown("**This problem asks you to multiply:**")
    multiplication_setup = " × ".join([f"**{factor}**" for factor in data['factors']])
    st.markdown(f"**{multiplication_setup}**")
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        # For money problems, show $ symbol
        if data['unit'] == 'dollars':
            st.markdown("**Choose the correct answer:**")
            formatted_options = [f"${opt:,}" for opt in data['options']]
        else:
            st.markdown("**Choose the correct answer:**")
            formatted_options = [f"{opt:,} {data['unit']}" for opt in data['options']]
        
        # Create radio button options
        user_answer = st.radio(
            "Select your answer:",
            options=formatted_options,
            key="answer_choice",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Extract number from answer
            if data['unit'] == 'dollars':
                selected_number = int(user_answer.replace('$', '').replace(',', ''))
            else:
                selected_number = int(user_answer.split()[0].replace(',', ''))
            st.session_state.user_answer = selected_number
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
        factors_text = " × ".join(map(str, data['factors']))
        if data['unit'] == 'dollars':
            st.markdown(f"**Solution:** {factors_text} = ${correct_answer:,}")
        else:
            st.markdown(f"**Solution:** {factors_text} = {correct_answer:,} {data['unit']}")
        
        # Increase difficulty (max level 5)
        old_level = st.session_state.mult_three_word_difficulty
        st.session_state.mult_three_word_difficulty = min(
            st.session_state.mult_three_word_difficulty + 1, 5
        )
        
        # Show encouragement based on level
        if st.session_state.mult_three_word_difficulty == 5 and old_level < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered Level 5 multi-factor word problems!**")
        elif old_level < st.session_state.mult_three_word_difficulty:
            st.info(f"⬆️ **Level Up! Now on Level {st.session_state.mult_three_word_difficulty}**")
    
    else:
        if data['unit'] == 'dollars':
            st.error(f"❌ **Not quite right.** The correct answer was **${correct_answer:,}**.")
        else:
            st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer:,} {data['unit']}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    factors = data['factors']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Step-by-Step Solution:
        
        **Problem:** {data['problem']}
        
        **Step 1: Identify what we need to multiply**
        """)
        
        for i, (factor, desc) in enumerate(zip(factors, data['factors_desc'])):
            st.markdown(f"- {desc.title()}: **{factor}**")
        
        st.markdown(f"""
        **Step 2: Set up the multiplication**
        {' × '.join(map(str, factors))}
        
        **Step 3: Calculate step by step**
        """)
        
        # Show step-by-step calculation
        result = factors[0]
        calculation_steps = [f"Start with: **{factors[0]}**"]
        
        for i in range(1, len(factors)):
            old_result = result
            result *= factors[i]
            calculation_steps.append(f"{old_result} × {factors[i]} = **{result}**")
        
        for step in calculation_steps:
            st.markdown(f"- {step}")
        
        if data['unit'] == 'dollars':
            st.markdown(f"**Final Answer: ${correct_answer:,}**")
        else:
            st.markdown(f"**Final Answer: {correct_answer:,} {data['unit']}**")
        
        # Show why this makes sense
        st.markdown("### Why this makes sense:")
        if len(factors) == 3:
            st.markdown(f"We have {factors[0]} groups, each containing {factors[1]} subgroups, with {factors[2]} items in each subgroup.")
        elif len(factors) == 4:
            st.markdown(f"We have a 4-level structure: {factors[0]} × {factors[1]} × {factors[2]} × {factors[3]} = {correct_answer:,} total items.")
        else:
            st.markdown(f"This problem involves {len(factors)} different factors that all multiply together to give us the total.")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer