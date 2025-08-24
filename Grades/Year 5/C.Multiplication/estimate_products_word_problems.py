import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Products: Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/estimate_products_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "word_estimate_difficulty" not in st.session_state:
        st.session_state.word_estimate_difficulty = 1  # Start with basic problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.word_estimate_score = 0
        st.session_state.total_questions = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Estimate Products: Word Problems")
    st.markdown("*Solve real-world estimation problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_estimate_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Simple Scenarios", 2: "Real-World Problems", 3: "Complex Situations"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Simple Scenarios')}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
        
        # Show score
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.word_estimate_score / st.session_state.total_questions) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
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
    with st.expander("💡 **Instructions & Estimation Strategies**", expanded=False):
        st.markdown("""
        ### How to Solve Word Problems with Estimation:
        
        #### 🔹 **Step 1: Read Carefully**
        - Find the two numbers you need to multiply
        - Understand what the problem is asking for
        - Look for keywords like "each," "per," "total," "altogether"
        
        #### 🔹 **Step 2: Round Smart**
        - Round to numbers that are easy to multiply mentally
        - Usually round to nearest 10, 100, or 1000
        - Choose rounding that makes sense for the context
        
        #### 🔹 **Step 3: Estimate**
        - Multiply the rounded numbers
        - Use mental math with the easier numbers
        - Get a reasonable ballpark answer
        
        #### 🔹 **Step 4: Choose Wisely**
        - Compare your estimate to the answer choices
        - Pick the answer closest to your estimate
        - Think about whether your answer makes sense
        
        ### 💰 **Example from Art Gallery:**
        - **Problem:** 71 vases × $936 each
        - **Round:** 70 × $900 = $63,000
        - **Or:** 70 × $1000 = $70,000 (too high)
        - **Best estimate:** $63,000
        
        ### 🎯 **Estimation Tips:**
        - **Round both numbers** if they're both complex
        - **Keep one exact** if it's simple (like 5, 10, 25)
        - **Think reasonably** - does your answer make sense?
        - **Check magnitude** - thousands? tens of thousands?
        
        ### 📚 **Scenario Types:**
        - 🛒 Shopping & retail
        - 🏗️ Construction & building  
        - 🍕 Food & cooking
        - 🚗 Transportation
        - 🏫 School situations
        - ⚽ Sports & entertainment
        - 🌱 Nature & science
        """)

def generate_new_question():
    """Generate a new word problem estimation question"""
    difficulty = st.session_state.word_estimate_difficulty
    
    # Define different scenario categories with various question types
    scenarios = {
        "money": [
            "A toy store bought {num1} teddy bears. Each teddy bear costs ${num2}. About how much did the store spend in total?",
            "An art dealer bought a set of {num1} beautiful vases. Each of the vases is worth ${num2}. About how much is the set of vases worth in all?",
            "A bookstore ordered {num1} books. Each book costs ${num2}. Estimate the total cost of the books.",
            "A school bought {num1} textbooks. Each textbook costs ${num2}. About how much did the school spend?"
        ],
        "distance": [
            "A cyclist rides {num1} miles each day. If she cycles for {num2} days, about how many miles will she travel in total?",
            "A delivery truck travels {num1} miles per trip. If it makes {num2} trips, about how many miles does it travel altogether?",
            "A train travels {num1} miles per hour. In {num2} hours, about how many miles will it travel?",
            "A runner jogs {num1} meters each lap. If she runs {num2} laps, about how many meters does she jog?"
        ],
        "weight": [
            "A box weighs {num1} pounds. If you have {num2} boxes, about how much do they weigh altogether?",
            "Each bag of rice weighs {num1} pounds. If a store orders {num2} bags, about how many pounds of rice is that?",
            "A truck can carry {num1} pounds per load. In {num2} loads, about how many pounds can it carry?",
            "Each student weighs about {num1} pounds. With {num2} students, what's the total weight?"
        ],
        "time": [
            "It takes {num1} minutes to bake one batch of cookies. To bake {num2} batches, about how many minutes will it take?",
            "A movie is {num1} minutes long. If you watch {num2} movies, about how many minutes is that?",
            "Each class period lasts {num1} minutes. In {num2} periods, about how many minutes of class time is that?",
            "A worker spends {num1} minutes on each task. With {num2} tasks, about how many minutes will they work?"
        ],
        "volume": [
            "Each bottle holds {num1} ounces. If you have {num2} bottles, about how many ounces is that total?",
            "A tank holds {num1} gallons of water. If you fill {num2} tanks, about how many gallons is that?",
            "Each cup contains {num1} milliliters. With {num2} cups, about how many milliliters altogether?",
            "A bucket holds {num1} liters. If you use {num2} buckets, about how many liters is that?"
        ],
        "area": [
            "Each room is {num1} square feet. In a building with {num2} rooms, about how many square feet is that?",
            "A garden plot is {num1} square meters. If the farm has {num2} plots, about how many square meters?",
            "Each tile covers {num1} square inches. To cover a floor with {num2} tiles, about how many square inches?",
            "A field is {num1} acres. If the ranch has {num2} fields, about how many acres total?"
        ],
        "count": [
            "Each box contains {num1} pencils. If you have {num2} boxes, about how many pencils is that?",
            "A pack has {num1} stickers. With {num2} packs, about how many stickers altogether?",
            "Each bag holds {num1} marbles. If you buy {num2} bags, about how many marbles will you have?",
            "A classroom has {num1} students. In {num2} classrooms, about how many students total?"
        ],
        "speed": [
            "A car travels {num1} miles per hour. In {num2} hours, about how many miles will it go?",
            "A plane flies {num1} kilometers per hour. After {num2} hours, about how many kilometers will it travel?",
            "A boat moves {num1} miles per hour. In {num2} hours, about how far will it travel?",
            "A bike goes {num1} feet per minute. In {num2} minutes, about how many feet will it travel?"
        ]
    }
    
    # Generate numbers based on difficulty
    if difficulty == 1:
        # Simple numbers, easier rounding
        quantities = [18, 19, 21, 22, 28, 29, 31, 32, 38, 39, 41, 42, 48, 49, 51, 52]
        values = [18, 19, 21, 22, 28, 29, 31, 32, 38, 39, 41, 42, 48, 49, 51, 52, 58, 59, 61, 62]
        
    elif difficulty == 2:
        # Medium complexity
        quantities = [67, 71, 73, 82, 89, 91, 97, 103, 108, 112, 118, 122, 127, 133, 138, 142]
        values = [187, 194, 208, 215, 223, 236, 241, 258, 267, 273, 284, 291, 306, 312, 327, 334]
        
    else:  # difficulty == 3
        # More complex numbers
        quantities = [156, 167, 173, 184, 192, 203, 218, 227, 234, 246, 251, 263, 278, 284, 297, 305]
        values = [567, 583, 596, 612, 627, 634, 648, 655, 671, 688, 694, 703, 719, 726, 732, 748]
    
    # Pick random scenario and numbers
    category = random.choice(list(scenarios.keys()))
    template = random.choice(scenarios[category])
    quantity = random.choice(quantities)
    value = random.choice(values)
    
    # Create the word problem
    problem_text = template.format(num1=quantity, num2=value)
    
    # Calculate actual product and rounded estimates
    actual_product = quantity * value
    
    # Round quantity and value for estimation
    rounded_quantity = round_to_best_place(quantity)
    rounded_value = round_to_best_place(value)
    estimated_product = rounded_quantity * rounded_value
    
    # Generate multiple choice options
    options = generate_answer_choices(estimated_product, actual_product)
    
    # Shuffle options and track correct answer
    correct_answer = min(options, key=lambda x: abs(x - estimated_product))
    random.shuffle(options)
    
    # Determine units based on category
    units = {
        "money": "$",
        "distance": " miles" if "miles" in template else " meters" if "meters" in template else " kilometers",
        "weight": " pounds",
        "time": " minutes",
        "volume": " ounces" if "ounces" in template else " gallons" if "gallons" in template else " milliliters" if "milliliters" in template else " liters",
        "area": " square feet" if "square feet" in template else " square meters" if "square meters" in template else " square inches" if "square inches" in template else " acres",
        "count": "",
        "speed": " miles" if "miles" in template else " kilometers" if "kilometers" in template else " feet"
    }
    
    unit = units.get(category, "")
    
    st.session_state.question_data = {
        "problem_text": problem_text,
        "quantity": quantity,
        "value": value,
        "actual_product": actual_product,
        "estimated_product": estimated_product,
        "rounded_quantity": rounded_quantity,
        "rounded_value": rounded_value,
        "options": options,
        "correct_answer": correct_answer,
        "category": category,
        "unit": unit
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = problem_text

def round_to_best_place(num):
    """Round number to the most appropriate place value for estimation"""
    if num < 50:
        # Round to nearest 10
        return round(num / 10) * 10
    elif num < 500:
        # Round to nearest 50 or 100
        if num % 50 < 25:
            return (num // 50) * 50
        else:
            return ((num // 50) + 1) * 50
    else:
        # Round to nearest 100
        return round(num / 100) * 100

def generate_answer_choices(estimated_product, actual_product):
    """Generate realistic multiple choice options"""
    # Create options around the estimated product
    base = estimated_product
    
    # Generate options at different scales
    options = [
        int(base * 0.7),   # Much lower
        int(base * 0.85),  # Somewhat lower  
        int(base),         # The estimate
        int(base * 1.15),  # Somewhat higher
        int(base * 1.3)    # Much higher
    ]
    
    # Round options to nice numbers
    rounded_options = []
    for opt in options:
        if opt < 1000:
            rounded_options.append(round(opt / 100) * 100)
        else:
            rounded_options.append(round(opt / 1000) * 1000)
    
    # Remove duplicates and sort
    unique_options = sorted(list(set(rounded_options)))
    
    # Take 2 best options (closest to our estimate)
    best_options = sorted(unique_options, key=lambda x: abs(x - estimated_product))[:2]
    
    return best_options

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the word problem
    st.markdown("### 📖 Word Problem:")
    
    # Display problem text in a story-like box
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
        {data['problem_text']} Choose the better estimate.
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Choose the better estimate:**")
        
        # Create answer choices with proper units
        unit = data['unit']
        if unit == "$":
            formatted_options = [f"${opt:,}" for opt in data['options']]
        elif unit == "":
            formatted_options = [f"{opt:,}" for opt in data['options']]
        else:
            formatted_options = [f"{opt:,}{unit}" for opt in data['options']]
        
        user_answer = st.radio(
            "Select your answer:",
            options=formatted_options,
            key="estimate_choice",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Convert back to integer for comparison
            if unit == "$":
                selected_amount = int(user_answer.replace("$", "").replace(",", ""))
            else:
                # Remove unit and commas, extract number
                clean_answer = user_answer.replace(",", "")
                for u in [" miles", " meters", " kilometers", " pounds", " minutes", " ounces", " gallons", " milliliters", " liters", " square feet", " square meters", " square inches", " acres", " feet"]:
                    clean_answer = clean_answer.replace(u, "")
                selected_amount = int(clean_answer)
            
            st.session_state.user_answer = selected_amount
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.session_state.total_questions += 1
    
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
        st.success("🎉 **Excellent! You chose the better estimate!**")
        st.session_state.word_estimate_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.word_estimate_score / st.session_state.total_questions
            if accuracy >= 0.75 and st.session_state.word_estimate_difficulty < 3:
                old_difficulty = st.session_state.word_estimate_difficulty
                st.session_state.word_estimate_difficulty += 1
                if old_difficulty < st.session_state.word_estimate_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.word_estimate_difficulty}**")
                    if st.session_state.word_estimate_difficulty == 3:
                        st.balloons()
    
    else:
        # Format correct answer with units
        unit = data['unit']
        if unit == "$":
            formatted_answer = f"${correct_answer:,}"
        elif unit == "":
            formatted_answer = f"{correct_answer:,}"
        else:
            formatted_answer = f"{correct_answer:,}{unit}"
            
        st.error(f"❌ **Not quite right.** The better estimate was **{formatted_answer}**.")
        
        # Decrease difficulty if struggling
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.word_estimate_score / st.session_state.total_questions
            if accuracy < 0.4 and st.session_state.word_estimate_difficulty > 1:
                old_difficulty = st.session_state.word_estimate_difficulty
                st.session_state.word_estimate_difficulty = max(st.session_state.word_estimate_difficulty - 1, 1)
                if old_difficulty > st.session_state.word_estimate_difficulty:
                    st.warning(f"⬇️ **Let's try simpler problems. Back to Level {st.session_state.word_estimate_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show step-by-step explanation of the estimation process"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        quantity = data['quantity']
        value = data['value']
        rounded_quantity = data['rounded_quantity']
        rounded_value = data['rounded_value']
        estimated_product = data['estimated_product']
        actual_product = data['actual_product']
        unit = data['unit']
        category = data['category']
        
        # Format numbers with units
        def format_with_unit(num):
            if unit == "$":
                return f"${num:,}"
            elif unit == "":
                return f"{num:,}"
            else:
                return f"{num:,}{unit}"
        
        st.markdown(f"""
        ### Step-by-Step Estimation:
        
        **Original numbers:** {quantity} × {value}
        """)
        
        st.markdown(f"""
        **Step 1: Round to easier numbers**
        - Round {quantity} to **{rounded_quantity}**
        - Round {value} to **{rounded_value}**
        """)
        
        st.markdown(f"""
        **Step 2: Multiply the rounded numbers**
        - {rounded_quantity} × {rounded_value} = **{estimated_product:,}**
        """)
        
        # Format options with units
        formatted_options = []
        for opt in data['options']:
            formatted_options.append(format_with_unit(opt))
        
        st.markdown(f"""
        **Step 3: Compare to answer choices**
        - Your estimate: **{format_with_unit(estimated_product)}**
        - Answer choices were: {', '.join(formatted_options)}
        - Best choice: **{format_with_unit(data['correct_answer'])}**
        """)
        
        # Show how close the estimate is to actual
        percentage_error = abs(estimated_product - actual_product) / actual_product * 100
        st.markdown(f"""
        ### 🎯 How Good Was Our Estimate?
        - **Actual exact answer:** {format_with_unit(actual_product)}
        - **Our estimate:** {format_with_unit(estimated_product)}
        - **Estimation error:** {percentage_error:.1f}%
        
        💡 **Remember:** In real life, we often need quick estimates rather than exact calculations!
        """)
        
        # Give tips based on the category
        category_tips = {
            "money": "💰 **Money Tip:** Round prices to make mental math easier - $936 becomes $900 or $1000",
            "distance": "🚗 **Distance Tip:** Round distances for quick travel calculations",
            "weight": "⚖️ **Weight Tip:** Estimate weights by rounding to easier numbers",
            "time": "⏰ **Time Tip:** Round time periods to make scheduling easier",
            "volume": "🥤 **Volume Tip:** Round capacities for quick quantity estimates",
            "area": "📐 **Area Tip:** Round measurements to estimate space quickly",
            "count": "🔢 **Counting Tip:** Round quantities to get quick totals",
            "speed": "🏃 **Speed Tip:** Round speeds and times for distance estimates"
        }
        
        tip = category_tips.get(category, "💡 **Estimation Tip:** Round numbers to make mental math easier")
        st.markdown(f"""
        ### {tip}
        """)
        
        # Give tips based on the numbers used
        if quantity < 50:
            st.markdown(f"- **{quantity}** is close to **{rounded_quantity}**, making mental math easier")
        elif quantity < 100:
            st.markdown(f"- **{quantity}** rounds nicely to **{rounded_quantity}** for quick multiplication")
        else:
            st.markdown(f"- **{quantity}** is a larger number, so rounding to **{rounded_quantity}** simplifies the calculation")
            
        if value < 100:
            st.markdown(f"- **{value}** rounds to **{rounded_value}**, which is easier to multiply")
        else:
            st.markdown(f"- **{value}** is rounded to **{rounded_value}** to make mental math manageable")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer