import streamlit as st
import random

def run():
    """
    Main function to run the Multiply Numbers Ending in Zeroes: Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_numbers_ending_in_zeroes_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "zeroes_word_difficulty" not in st.session_state:
        st.session_state.zeroes_word_difficulty = 1  # Start with basic problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply Numbers Ending in Zeroes: Word Problems")
    st.markdown("*Solve real-world problems using the zero shortcut*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.zeroes_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Tens & Hundreds", "Thousands", "Large Numbers"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level - 1]}")
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Solving Word Problems with Numbers Ending in Zeros:
        
        **1. Read and Understand** 📖
        - **Identify** what you need to find
        - **Look for** multiplication keywords
        - **Find** the numbers in the problem
        
        **2. Set Up the Problem** ✖️
        - **Write** the multiplication equation
        - **Check** which numbers end in zeros
        - **Identify** the units for your answer
        
        **3. Use the Zero Shortcut** ⚡
        - **Multiply** the non-zero parts first
        - **Count** all the zeros from both numbers
        - **Add** the zeros to your answer
        
        **4. Check Your Answer** ✅
        - **Does it make sense** for the problem?
        - **Are the units correct?**
        - **Is it reasonable** in size?
        
        ### Example Problem:
        **"A thread factory puts 90 metres of thread on each spool. How many metres of thread will the factory need to make to fill 300 spools?"**
        
        **Step 1:** What do we need? Total metres of thread  
        **Step 2:** 90 metres × 300 spools  
        **Step 3:** Use zero shortcut:
        - Non-zero parts: 9 × 3 = 27
        - Count zeros: 90 has 1 zero, 300 has 2 zeros = 3 total
        - Answer: 27,000 metres
        
        ### Key Words for Multiplication:
        - **"Each"** → equal groups
        - **"Per"** → rate or amount for each
        - **"Total"** → multiplication often needed
        - **"In all"** → find the complete amount
        - **"Fill"** → complete a certain number
        
        ### Types of Scenarios:
        - 🏭 **Manufacturing** (thread, products, packaging)
        - 🏪 **Shopping & Business** (bulk buying, pricing)
        - 🚚 **Transportation** (cargo, capacity, distances)
        - 🏗️ **Construction** (materials, measurements)
        - 📦 **Packaging** (boxes, containers, shipping)
        - 🌾 **Agriculture** (crops, fields, harvests)
        - ⚡ **Utilities** (electricity, water, energy)
        - 🏫 **Education** (supplies, equipment, students)
        
        ### Zero Shortcut Reminder:
        **90 × 300**
        1. **9 × 3 = 27** (ignore zeros)
        2. **Count zeros:** 1 + 2 = 3 zeros total
        3. **Add zeros:** 27,000 ✅
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Tens and hundreds (20×40, 60×300)
        - **🟠 Level 2:** Thousands (200×4000, 50×8000)
        - **🔴 Level 3:** Large numbers (5000×60000)
        """)

def generate_new_question():
    """Generate a new word problem involving numbers ending in zeros"""
    difficulty = st.session_state.zeroes_word_difficulty
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        # Level 1: Tens and hundreds
        choices = [
            (random.randint(2, 9) * 10, random.randint(2, 9) * 10),        # 20 × 30
            (random.randint(2, 9) * 10, random.randint(2, 9) * 100),       # 20 × 300
            (random.randint(2, 9) * 100, random.randint(2, 9)),            # 200 × 3
            (random.randint(2, 9), random.randint(2, 9) * 100),            # 3 × 200
        ]
        factor1, factor2 = random.choice(choices)
        
    elif difficulty == 2:
        # Level 2: Thousands
        choices = [
            (random.randint(2, 9) * 100, random.randint(2, 9) * 100),      # 200 × 300
            (random.randint(2, 9) * 1000, random.randint(2, 9)),           # 2000 × 3
            (random.randint(2, 9), random.randint(2, 9) * 1000),           # 3 × 2000
            (random.randint(2, 9) * 10, random.randint(2, 9) * 1000),      # 20 × 3000
        ]
        factor1, factor2 = random.choice(choices)
        
    else:
        # Level 3: Large numbers
        choices = [
            (random.randint(2, 9) * 1000, random.randint(2, 9) * 100),     # 2000 × 300
            (random.randint(2, 9) * 10000, random.randint(2, 9)),          # 20000 × 3
            (random.randint(2, 9) * 100, random.randint(2, 9) * 10000),    # 200 × 30000
            (random.randint(2, 9) * 1000, random.randint(2, 9) * 1000),    # 2000 × 3000
        ]
        factor1, factor2 = random.choice(choices)
    
    # Calculate answer
    correct_answer = factor1 * factor2
    
    # Create varied word problem scenarios
    scenarios = [
        # Manufacturing & Production
        {
            "context": "🏭 Thread Factory",
            "story": f"A thread factory puts {factor1} metres of thread on each spool. How many metres of thread will the factory need to make to fill {factor2} spools?",
            "unit": "metres of thread",
            "calculation": f"{factor1} metres × {factor2} spools"
        },
        {
            "context": "🏭 Bottle Factory", 
            "story": f"A bottle factory produces {factor1} bottles every hour. How many bottles will they produce in {factor2} hours?",
            "unit": "bottles",
            "calculation": f"{factor1} bottles × {factor2} hours"
        },
        {
            "context": "📦 Box Manufacturing",
            "story": f"A packaging company puts {factor1} items in each box. How many items do they need to fill {factor2} boxes?",
            "unit": "items",
            "calculation": f"{factor1} items × {factor2} boxes"
        },
        
        # Shopping & Business
        {
            "context": "🏪 Bulk Shopping",
            "story": f"A shop sells pencils in bulk packs. Each pack contains {factor1} pencils and costs £{factor2}. If they sell one pack, how much money do they collect per pencil? No wait... If they have {factor2} packs, how many pencils do they have in total?",
            "unit": "pencils",
            "calculation": f"{factor1} pencils × {factor2} packs"
        },
        {
            "context": "💰 Business Sales",
            "story": f"A company sells products for £{factor1} each. If they sell {factor2} products, how much money will they earn?",
            "unit": "pounds",
            "calculation": f"£{factor1} × {factor2} products"
        },
        {
            "context": "🛒 Grocery Store",
            "story": f"A grocery store receives shipments of {factor1} cans per case. They ordered {factor2} cases. How many cans did they receive in total?",
            "unit": "cans",
            "calculation": f"{factor1} cans × {factor2} cases"
        },
        
        # Transportation & Logistics
        {
            "context": "🚚 Delivery Truck",
            "story": f"A delivery truck can carry {factor1} packages on each trip. How many packages can it deliver in {factor2} trips?",
            "unit": "packages",
            "calculation": f"{factor1} packages × {factor2} trips"
        },
        {
            "context": "✈️ Airport Cargo",
            "story": f"Each cargo plane can transport {factor1} kilograms of freight. How many kilograms can {factor2} planes transport together?",
            "unit": "kilograms",
            "calculation": f"{factor1} kg × {factor2} planes"
        },
        {
            "context": "🚢 Shipping Container",
            "story": f"A shipping container holds {factor1} boxes. How many boxes can be stored in {factor2} containers?",
            "unit": "boxes",
            "calculation": f"{factor1} boxes × {factor2} containers"
        },
        
        # Construction & Building
        {
            "context": "🏗️ Construction Site",
            "story": f"A construction project needs {factor1} bricks for each wall. How many bricks are needed to build {factor2} walls?",
            "unit": "bricks",
            "calculation": f"{factor1} bricks × {factor2} walls"
        },
        {
            "context": "🏠 Tile Installation",
            "story": f"Each room needs {factor1} floor tiles. How many tiles are needed for {factor2} rooms?",
            "unit": "tiles",
            "calculation": f"{factor1} tiles × {factor2} rooms"
        },
        {
            "context": "🔨 Hardware Store",
            "story": f"A hardware store sells nails in boxes. Each box contains {factor1} nails. How many nails are in {factor2} boxes?",
            "unit": "nails",
            "calculation": f"{factor1} nails × {factor2} boxes"
        },
        
        # Agriculture & Farming
        {
            "context": "🌾 Wheat Farm",
            "story": f"A farmer harvests {factor1} kilograms of wheat from each field. How many kilograms will he harvest from {factor2} fields?",
            "unit": "kilograms of wheat",
            "calculation": f"{factor1} kg × {factor2} fields"
        },
        {
            "context": "🐄 Dairy Farm",
            "story": f"Each cow produces {factor1} litres of milk per day. How many litres of milk will {factor2} cows produce in one day?",
            "unit": "litres of milk",
            "calculation": f"{factor1} litres × {factor2} cows"
        },
        {
            "context": "🍎 Apple Orchard",
            "story": f"Each apple tree produces {factor1} apples per season. How many apples will {factor2} trees produce?",
            "unit": "apples",
            "calculation": f"{factor1} apples × {factor2} trees"
        },
        
        # Education & Schools
        {
            "context": "📚 School Library",
            "story": f"The school library orders books in sets. Each set contains {factor1} books. How many books are in {factor2} sets?",
            "unit": "books",
            "calculation": f"{factor1} books × {factor2} sets"
        },
        {
            "context": "✏️ Classroom Supplies",
            "story": f"Each classroom gets {factor1} pencils for the term. How many pencils are needed for {factor2} classrooms?",
            "unit": "pencils",
            "calculation": f"{factor1} pencils × {factor2} classrooms"
        },
        {
            "context": "🎨 Art Supplies",
            "story": f"Each art kit contains {factor1} crayons. How many crayons are in {factor2} art kits?",
            "unit": "crayons",
            "calculation": f"{factor1} crayons × {factor2} kits"
        },
        
        # Utilities & Energy
        {
            "context": "⚡ Power Plant",
            "story": f"A power plant generates {factor1} kilowatts of electricity per hour. How many kilowatts will it generate in {factor2} hours?",
            "unit": "kilowatts",
            "calculation": f"{factor1} kW × {factor2} hours"
        },
        {
            "context": "💧 Water Treatment",
            "story": f"A water treatment plant processes {factor1} litres of water per minute. How many litres will it process in {factor2} minutes?",
            "unit": "litres of water",
            "calculation": f"{factor1} litres × {factor2} minutes"
        },
        
        # Entertainment & Sports
        {
            "context": "🎪 Concert Hall",
            "story": f"A concert hall has {factor1} seats in each section. How many seats are there in {factor2} sections?",
            "unit": "seats",
            "calculation": f"{factor1} seats × {factor2} sections"
        },
        {
            "context": "⚽ Sports Stadium",
            "story": f"Each section of the stadium holds {factor1} spectators. How many spectators can {factor2} sections hold?",
            "unit": "spectators",
            "calculation": f"{factor1} spectators × {factor2} sections"
        }
    ]
    
    # Select a random scenario
    scenario = random.choice(scenarios)
    
    # Store question data
    st.session_state.question_data = {
        'factor1': factor1,
        'factor2': factor2,
        'correct_answer': correct_answer,
        'scenario': scenario,
        'story': scenario['story'],
        'unit': scenario['unit'],
        'context': scenario['context'],
        'calculation': scenario['calculation']
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = scenario['story']

def display_question():
    """Display the current word problem"""
    data = st.session_state.question_data
    
    # Create form for the answer
    with st.form("zeroes_word_form"):
        # Display the word problem
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Show context with icon
            st.markdown(f"**{data['context']}**")
            
            # Display the story in a highlighted box
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa; 
                padding: 25px; 
                border-radius: 15px; 
                border-left: 5px solid #28a745;
                font-size: 18px;
                line-height: 1.6;
                margin: 20px 0;
                color: #2c3e50;
            ">
                {data['story']}
            </div>
            """, unsafe_allow_html=True)
            
            # Input field with unit label (matching the image format)
            answer_cols = st.columns([3, 4])
            
            with answer_cols[0]:
                user_answer = st.number_input(
                    "Answer",
                    min_value=0,
                    step=1,
                    key="word_zeroes_answer",
                    label_visibility="collapsed",
                    help=f"Calculate: {data['calculation']}",
                    placeholder="Enter your answer"
                )
            
            with answer_cols[1]:
                st.markdown(f"<div style='margin-top: 12px; font-size: 16px; color: #666;'>{data['unit']}</div>", unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
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
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! {correct_answer:,} {data['unit']} is correct!**")
        
        # Increase difficulty (max 3 levels)
        old_difficulty = st.session_state.zeroes_word_difficulty
        st.session_state.zeroes_word_difficulty = min(
            st.session_state.zeroes_word_difficulty + 1, 3
        )
        
        if st.session_state.zeroes_word_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered word problems with zeros!**")
        elif old_difficulty < st.session_state.zeroes_word_difficulty:
            st.info(f"⬆️ **Great problem solving! Moving up to Level {st.session_state.zeroes_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,} {data['unit']}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.zeroes_word_difficulty
        st.session_state.zeroes_word_difficulty = max(
            st.session_state.zeroes_word_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.zeroes_word_difficulty:
            st.warning(f"⬇️ **Let's practice more at Level {st.session_state.zeroes_word_difficulty}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the word problem using zero shortcut"""
    data = st.session_state.question_data
    factor1 = data['factor1']
    factor2 = data['factor2']
    correct_answer = data['correct_answer']
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Problem Analysis:
        **Context:** {data['context']}
        **Calculation needed:** {data['calculation']}
        
        ### Step-by-step solution using Zero Shortcut:
        
        **Step 1: Set up the multiplication** ✖️
        - {factor1:,} × {factor2:,}
        
        **Step 2: Use the Zero Shortcut** ⚡
        """)
        
        # Count zeros and show the shortcut method
        zeros_factor1 = count_trailing_zeros(factor1)
        zeros_factor2 = count_trailing_zeros(factor2)
        total_zeros = zeros_factor1 + zeros_factor2
        
        # Get non-zero parts
        non_zero1 = factor1 // (10 ** zeros_factor1) if zeros_factor1 > 0 else factor1
        non_zero2 = factor2 // (10 ** zeros_factor2) if zeros_factor2 > 0 else factor2
        
        basic_product = non_zero1 * non_zero2
        
        st.markdown(f"""
        - **Identify non-zero parts:** {factor1:,} = {non_zero1}, {factor2:,} = {non_zero2}
        - **Multiply non-zero parts:** {non_zero1} × {non_zero2} = {basic_product}
        - **Count total zeros:** {zeros_factor1} + {zeros_factor2} = {total_zeros} zeros
        - **Add zeros back:** {basic_product} + {total_zeros} zeros = {correct_answer:,}
        
        **Step 3: Include units** 📏
        - **Final answer:** {correct_answer:,} {data['unit']}
        
        **Step 4: Check reasonableness** ✅
        - Does {correct_answer:,} {data['unit']} make sense for this problem? ✓
        
        ### Quick Mental Math:
        Instead of calculating {factor1:,} × {factor2:,} the long way...  
        **Think:** {non_zero1} × {non_zero2} = {basic_product}, then add {total_zeros} zeros = **{correct_answer:,}** ⚡
        """)

def count_trailing_zeros(n):
    """Count the number of trailing zeros in a number"""
    if n == 0:
        return 1
    count = 0
    while n % 10 == 0:
        count += 1
        n //= 10
    return count

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""