import streamlit as st
import random

def run():
    """
    Main function to run the Multiply Two-Digit Numbers Using Partial Products activity.
    """
    # Initialize session state
    if "partial_products_difficulty" not in st.session_state:
        st.session_state.partial_products_difficulty = "easy"
        st.session_state.correct_streak = 0
        st.session_state.total_attempts = 0
        st.session_state.performance_history = []
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.show_step_solution = False
        st.session_state.user_answers = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔢 Multiply Two-Digit Numbers Using Partial Products")
    st.markdown("*Break down multiplication into easier parts*")
    st.markdown("---")
    
    # Adaptive Performance Dashboard
    display_performance_dashboard()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        display_adaptive_instructions()

def display_performance_dashboard():
    """Display adaptive performance tracking"""
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_map = {"easy": "🟡 Easy", "medium": "🟠 Medium", "hard": "🔴 Hard"}
        st.markdown(f"**Current Level:** {difficulty_map[st.session_state.partial_products_difficulty]}")
        
        # Adaptive progress bar
        if st.session_state.total_attempts > 0:
            success_rate = (st.session_state.correct_streak / max(st.session_state.total_attempts, 1)) * 100
            st.progress(success_rate / 100, text=f"Success Rate: {success_rate:.0f}%")
    
    with col2:
        st.metric("🔥 Streak", st.session_state.correct_streak)
    
    with col3:
        st.metric("📊 Total", st.session_state.total_attempts)
    
    with col4:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

def display_adaptive_instructions():
    """Display instructions that adapt based on current difficulty and performance"""
    difficulty = st.session_state.partial_products_difficulty
    
    if difficulty == "easy":
        st.markdown("""
        ### 🌟 Getting Started with Partial Products:
        
        **The Big Idea:** Instead of multiplying big numbers all at once, we break them into smaller, easier pieces!
        
        **Step-by-Step Process:**
        1. **Split the numbers:** 23 = 20 + 3, and 34 = 30 + 4
        2. **Make a grid:** Like a tic-tac-toe board for multiplication
        3. **Fill each square:** Multiply the parts (20×30, 20×4, 3×30, 3×4)
        4. **Add them up:** All the pieces together give you the answer!
        
        **Visual Helper:**
        ```
             |  20  |   3  
        -----+------+------
          30 | 600  |  90  
        -----+------+------
           4 |  80  |  12  
        ```
        **Answer:** 600 + 90 + 80 + 12 = 782
        """)
    
    elif difficulty == "medium":
        st.markdown("""
        ### 🚀 Building Your Skills:
        
        **You're doing great!** Now we're working with slightly bigger numbers and more missing pieces.
        
        **Pro Tips:**
        - **Double-check your place values:** Is it tens × tens or tens × ones?
        - **Use patterns:** Notice how 40 × 30 = 4 × 3 × 100 = 1,200
        - **Estimate first:** 47 × 38 should be close to 50 × 40 = 2,000
        
        **Memory Trick:** Think of it like organizing a classroom:
        - Tens sit with tens (biggest numbers)
        - Ones sit with ones (smallest numbers)
        - Cross-combinations in the middle
        """)
    
    else:  # hard
        st.markdown("""
        ### 🏆 Master Level Challenge:
        
        **You're a partial products expert!** These problems have multiple missing pieces and require careful attention.
        
        **Advanced Strategies:**
        - **Work systematically:** Fill in what you know first, then solve for unknowns
        - **Use relationships:** If you know 3 partial products, you can find the 4th by subtracting from the total
        - **Mental math shortcuts:** 60 × 80 = 6 × 8 × 100 = 4,800
        
        **Challenge yourself:** Can you solve it in your head before filling in the blanks?
        """)

def generate_new_question():
    """Generate adaptive questions based on performance"""
    
    # Adaptive difficulty adjustment
    if len(st.session_state.performance_history) >= 3:
        recent_performance = st.session_state.performance_history[-3:]
        if all(recent_performance) and st.session_state.partial_products_difficulty != "hard":
            # Move up if last 3 were correct
            if st.session_state.partial_products_difficulty == "easy":
                st.session_state.partial_products_difficulty = "medium"
            else:
                st.session_state.partial_products_difficulty = "hard"
        elif not any(recent_performance) and st.session_state.partial_products_difficulty != "easy":
            # Move down if last 3 were wrong
            if st.session_state.partial_products_difficulty == "hard":
                st.session_state.partial_products_difficulty = "medium"
            else:
                st.session_state.partial_products_difficulty = "easy"
    
    scenarios = {
        "easy": [
            {"multiplicand": 21, "multiplier": 34, "missing": ["partial2"]},
            {"multiplicand": 23, "multiplier": 42, "missing": ["partial3"]},
            {"multiplicand": 31, "multiplier": 25, "missing": ["partial1"]},
            {"multiplicand": 32, "multiplier": 23, "missing": ["partial4"]},
            {"multiplicand": 24, "multiplier": 31, "missing": ["partial2"]},
        ],
        "medium": [
            {"multiplicand": 47, "multiplier": 38, "missing": ["partial2", "partial4"]},
            {"multiplicand": 56, "multiplier": 29, "missing": ["partial1", "partial3"]},
            {"multiplicand": 43, "multiplier": 67, "missing": ["partial2", "sum"]},
            {"multiplicand": 34, "multiplier": 56, "missing": ["partial1", "partial4"]},
        ],
        "hard": [
            {"multiplicand": 78, "multiplier": 45, "missing": ["partial1", "partial2", "sum"]},
            {"multiplicand": 69, "multiplier": 87, "missing": ["partial3", "partial4", "sum"]},
            {"multiplicand": 84, "multiplier": 56, "missing": ["partial1", "partial4", "sum"]},
            {"multiplicand": 67, "multiplier": 89, "missing": ["partial2", "partial3", "sum"]},
        ]
    }
    
    scenario = random.choice(scenarios[st.session_state.partial_products_difficulty])
    
    # Calculate all partial products
    multiplicand = scenario["multiplicand"]
    multiplier = scenario["multiplier"]
    
    # Break down into tens and ones
    m1_tens = (multiplicand // 10) * 10
    m1_ones = multiplicand % 10
    m2_tens = (multiplier // 10) * 10
    m2_ones = multiplier % 10
    
    # Calculate partial products
    partial1 = m1_tens * m2_tens    # tens × tens
    partial2 = m1_tens * m2_ones    # tens × ones
    partial3 = m1_ones * m2_tens    # ones × tens
    partial4 = m1_ones * m2_ones    # ones × ones
    
    total_sum = partial1 + partial2 + partial3 + partial4
    
    st.session_state.question_data = {
        "multiplicand": multiplicand,
        "multiplier": multiplier,
        "m1_tens": m1_tens,
        "m1_ones": m1_ones,
        "m2_tens": m2_tens,
        "m2_ones": m2_ones,
        "partial1": partial1,
        "partial2": partial2,
        "partial3": partial3,
        "partial4": partial4,
        "total_sum": total_sum,
        "missing_positions": scenario["missing"]
    }
    
    st.session_state.correct_answers = {
        "partial1": partial1,
        "partial2": partial2,
        "partial3": partial3,
        "partial4": partial4,
        "sum": total_sum
    }
    
    st.session_state.current_question = f"Fill in the missing numbers to complete the partial products multiplication!"

def display_question():
    """Display the current question interface with enhanced visuals"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 🧮 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Show the original problem in a nice box
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 24px; font-weight: bold;">
        {data['multiplicand']} × {data['multiplier']} = ?
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Show the breakdown
    st.markdown("### 🔹 Step 1: Break down the numbers")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 4px solid #2196f3;">
            <strong>{data['multiplicand']}</strong> = <span style="color: #1976d2;">{data['m1_tens']}</span> + <span style="color: #0d47a1;">{data['m1_ones']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #f3e5f5; padding: 15px; border-radius: 10px; border-left: 4px solid #9c27b0;">
            <strong>{data['multiplier']}</strong> = <span style="color: #7b1fa2;">{data['m2_tens']}</span> + <span style="color: #4a148c;">{data['m2_ones']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Step 2: Visual Grid
    st.markdown("### 🔹 Step 2: Multiplication Grid")
    create_visual_grid(data)
    
    # Step 3: Traditional Format
    st.markdown("### 🔹 Step 3: Add up the partial products")
    
    # Create input form - FIXED VERSION
    with st.form("partial_products_form", clear_on_submit=False):
        user_answers = create_traditional_format(data)
        
        # Buttons row
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        with col3:
            step_solution_button = st.form_submit_button("🔍 Step-by-Step Help", type="secondary", use_container_width=True)
        
        # FIXED: Check if user has filled required fields before processing
        if submit_button:
            # Validate that all required fields have been filled
            positions_to_check = list(data['missing_positions'])
            if data['missing_positions']:
                positions_to_check.append("sum")
            
            valid_submission = True
            for position in positions_to_check:
                if position in user_answers and (user_answers[position] is None or user_answers[position] == ""):
                    valid_submission = False
                    break
            
            if valid_submission:
                # Capture user answers and store in session state
                st.session_state.user_answers = user_answers
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.total_attempts += 1
            else:
                st.warning("⚠️ Please fill in all the missing numbers before submitting.")
            
        if step_solution_button:
            st.session_state.show_step_solution = True

    # Show step-by-step solution if requested
    if st.session_state.show_step_solution:
        show_interactive_step_solution()
    
    # Show feedback and next button - FIXED: Only call this outside the form
    handle_feedback_and_next()

def create_visual_grid(data):
    """Create an interactive visual grid showing the multiplication"""
    
    # Helper function to get input or show value
    def get_cell_content(position, value, color, text_color="white"):
        if position in data['missing_positions']:
            return f"""
            <div style="background: {color}; border: 3px dashed #ffeb3b; color: black; text-align: center; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 8px;">
                ?
            </div>
            """
        else:
            return f"""
            <div style="background: {color}; color: {text_color}; text-align: center; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 8px; border: 2px solid rgba(255,255,255,0.3);">
                {value}
            </div>
            """
    
    # Create the grid HTML
    grid_html = f"""
    <div style="margin: 20px 0;">
        <table style="margin: 0 auto; border-collapse: separate; border-spacing: 10px;">
            <tr>
                <td style="background: #37474f; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">×</td>
                <td style="background: #1976d2; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_tens']}</td>
                <td style="background: #0d47a1; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_ones']}</td>
            </tr>
            <tr>
                <td style="background: #7b1fa2; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m2_tens']}</td>
                <td>{get_cell_content("partial1", data['partial1'], "#4caf50")}</td>
                <td>{get_cell_content("partial3", data['partial3'], "#2e7d32")}</td>
            </tr>
            <tr>
                <td style="background: #4a148c; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m2_ones']}</td>
                <td>{get_cell_content("partial2", data['partial2'], "#ff9800")}</td>
                <td>{get_cell_content("partial4", data['partial4'], "#f57c00")}</td>
            </tr>
        </table>
    </div>
    """
    
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Legend
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 20px; height: 20px; background: #4caf50; border-radius: 4px;"></div>
            <span>Tens × Tens</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 20px; height: 20px; background: #ff9800; border-radius: 4px;"></div>
            <span>Tens × Ones</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 20px; height: 20px; background: #2e7d32; border-radius: 4px;"></div>
            <span>Ones × Tens</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 20px; height: 20px; background: #f57c00; border-radius: 4px;"></div>
            <span>Ones × Ones</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_traditional_format(data):
    """Create the traditional multiplication format with inputs - RETURNS USER ANSWERS"""
    
    st.markdown(f"""
    <div style="font-family: 'Courier New', monospace; font-size: 18px; background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <div style="text-align: center;">
            <div style="margin-bottom: 10px; font-size: 20px; font-weight: bold;">{data['multiplicand']} × {data['multiplier']}</div>
            <div style="border-bottom: 2px solid #333; margin: 10px auto; width: 150px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create input fields for missing values
    st.markdown("**Fill in the missing partial products:**")
    
    cols = st.columns(4)
    user_answers = {}
    
    with cols[0]:
        if "partial1" in data['missing_positions']:
            user_answers['partial1'] = st.number_input(
                f"🟢 {data['m1_tens']//10} × {data['m2_tens']//10} × 100",
                value=None, step=1, key="input_partial1"
            )
        else:
            st.markdown(f"🟢 **{data['partial1']}**")
            st.caption(f"{data['m1_tens']//10} × {data['m2_tens']//10} × 100")
            user_answers['partial1'] = data['partial1']
    
    with cols[1]:
        if "partial2" in data['missing_positions']:
            user_answers['partial2'] = st.number_input(
                f"🟠 {data['m1_tens']//10} × {data['m2_ones']} × 10",
                value=None, step=1, key="input_partial2"
            )
        else:
            st.markdown(f"🟠 **{data['partial2']}**")
            st.caption(f"{data['m1_tens']//10} × {data['m2_ones']} × 10")
            user_answers['partial2'] = data['partial2']
    
    with cols[2]:
        if "partial3" in data['missing_positions']:
            user_answers['partial3'] = st.number_input(
                f"🟤 {data['m1_ones']} × {data['m2_tens']//10} × 10",
                value=None, step=1, key="input_partial3"
            )
        else:
            st.markdown(f"🟤 **{data['partial3']}**")
            st.caption(f"{data['m1_ones']} × {data['m2_tens']//10} × 10")
            user_answers['partial3'] = data['partial3']
    
    with cols[3]:
        if "partial4" in data['missing_positions']:
            user_answers['partial4'] = st.number_input(
                f"🟫 {data['m1_ones']} × {data['m2_ones']}",
                value=None, step=1, key="input_partial4"
            )
        else:
            st.markdown(f"🟫 **{data['partial4']}**")
            st.caption(f"{data['m1_ones']} × {data['m2_ones']}")
            user_answers['partial4'] = data['partial4']
    
    # Final sum
    st.markdown("---")
    st.markdown("**🎯 Final Answer:**")
    
    # Create the addition string without revealing missing values
    addition_parts = []
    for position in ["partial1", "partial2", "partial3", "partial4"]:
        if position in data['missing_positions']:
            addition_parts.append("___")
        else:
            addition_parts.append(str(data[position]))
    
    addition_string = " + ".join(addition_parts)
    
    if data['missing_positions']:
        user_answers['sum'] = st.number_input(
            f"Add them all up: {addition_string} =",
            value=None, step=1, key="input_sum"
        )
    else:
        st.markdown(f"**Final Answer:** {data['total_sum']}")
        user_answers['sum'] = data['total_sum']
    
    return user_answers

def show_interactive_step_solution():
    """Interactive step-by-step solution walkthrough"""
    data = st.session_state.question_data
    
    st.markdown("---")
    st.markdown("## 🎓 **Interactive Step-by-Step Solution**")
    
    # Create tabs for each step
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Setup", "🔢 Breakdown", "🎯 Grid Method", "➕ Calculate", "✅ Verify"])
    
    with tab1:
        st.markdown("### Step 1: Understanding the Problem")
        st.markdown(f"""
        We need to multiply **{data['multiplicand']} × {data['multiplier']}**
        
        **Why use partial products?**
        - It breaks big problems into smaller, manageable pieces
        - Each piece is easier to calculate
        - We can check our work step by step
        
        **The goal:** Find four partial products and add them together!
        """)
        
        st.markdown(f"""
        <div style="background: #e8f5e8; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <strong>🎯 Target:</strong> {data['multiplicand']} × {data['multiplier']} = {data['total_sum']}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Step 2: Breaking Down the Numbers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Breaking down {data['multiplicand']}:**
            
            {data['multiplicand']} = {data['m1_tens']} + {data['m1_ones']}
            
            - **{data['m1_tens']}** is the "tens" part
            - **{data['m1_ones']}** is the "ones" part
            """)
        
        with col2:
            st.markdown(f"""
            **Breaking down {data['multiplier']}:**
            
            {data['multiplier']} = {data['m2_tens']} + {data['m2_ones']}
            
            - **{data['m2_tens']}** is the "tens" part  
            - **{data['m2_ones']}** is the "ones" part
            """)
        
        st.info("💡 **Tip:** Think of place value! The tens digit tells us how many groups of 10 we have.")
    
    with tab3:
        st.markdown("### Step 3: Setting Up the Grid")
        
        st.markdown("Now we create a multiplication grid where each cell represents one partial product:")
        
        # Interactive grid with explanations
        st.markdown(f"""
        <div style="margin: 20px 0;">
            <table style="margin: 0 auto; border-collapse: separate; border-spacing: 10px;">
                <tr>
                    <td style="background: #37474f; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">×</td>
                    <td style="background: #1976d2; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_tens']}</td>
                    <td style="background: #0d47a1; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_ones']}</td>
                </tr>
                <tr>
                    <td style="background: #7b1fa2; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m2_tens']}</td>
                    <td style="background: #4caf50; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_tens']} × {data['m2_tens']}</td>
                    <td style="background: #2e7d32; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_ones']} × {data['m2_tens']}</td>
                </tr>
                <tr>
                    <td style="background: #4a148c; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m2_ones']}</td>
                    <td style="background: #ff9800; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_tens']} × {data['m2_ones']}</td>
                    <td style="background: #f57c00; color: white; text-align: center; padding: 15px; font-weight: bold; border-radius: 8px;">{data['m1_ones']} × {data['m2_ones']}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Each colored cell represents:**
        - 🟢 **Green:** Tens × Tens (biggest partial product)
        - 🟠 **Orange:** Tens × Ones  
        - 🟤 **Brown:** Ones × Tens
        - 🟫 **Dark Orange:** Ones × Ones (smallest partial product)
        """)
    
    with tab4:
        st.markdown("### Step 4: Calculate Each Partial Product")
        
        # Show each calculation with explanations
        calculations = [
            ("🟢 Tens × Tens", f"{data['m1_tens']} × {data['m2_tens']}", data['partial1'], "This is usually the largest piece!"),
            ("🟠 Tens × Ones", f"{data['m1_tens']} × {data['m2_ones']}", data['partial2'], "Multiply the first tens by the second ones"),
            ("🟤 Ones × Tens", f"{data['m1_ones']} × {data['m2_tens']}", data['partial3'], "Multiply the first ones by the second tens"),
            ("🟫 Ones × Ones", f"{data['m1_ones']} × {data['m2_ones']}", data['partial4'], "This is usually the smallest piece!")
        ]
        
        for color, calculation, result, tip in calculations:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #007bff;">
                <strong>{color}</strong><br>
                {calculation} = <strong>{result}</strong><br>
                <em style="color: #666;">{tip}</em>
            </div>
            """, unsafe_allow_html=True)
        
        st.success(f"🎯 **All partial products:** {data['partial1']}, {data['partial2']}, {data['partial3']}, {data['partial4']}")
    
    with tab5:
        st.markdown("### Step 5: Add and Verify")
        
        st.markdown(f"""
        **Final Addition:**
        
        {data['partial1']} + {data['partial2']} + {data['partial3']} + {data['partial4']} = **{data['total_sum']}**
        
        **Let's verify this makes sense:**
        """)
        
        # Verification using estimation
        estimated = round(data['multiplicand'] / 10) * 10 * round(data['multiplier'] / 10) * 10
        st.markdown(f"""
        - **Estimation check:** {data['multiplicand']} is about {round(data['multiplicand'] / 10) * 10}, and {data['multiplier']} is about {round(data['multiplier'] / 10) * 10}
        - **Rough estimate:** {round(data['multiplicand'] / 10) * 10} × {round(data['multiplier'] / 10) * 10} = {estimated}
        - **Our answer {data['total_sum']}** is {"✅ reasonable!" if abs(data['total_sum'] - estimated) < estimated * 0.3 else "⚠️ let's double-check"}
        """)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h3 style="margin: 0; color: white;">🎉 Final Answer: {data['multiplicand']} × {data['multiplier']} = {data['total_sum']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Close step-by-step when done
    if st.button("❌ Close Step-by-Step Help"):
        st.session_state.show_step_solution = False
        st.rerun()

def handle_feedback_and_next():
    """Handle feedback display and next question button - FIXED VERSION"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Show next question button only AFTER feedback is shown AND answer was submitted
    if st.session_state.answer_submitted and st.session_state.show_feedback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display adaptive feedback for the submitted answer"""
    data = st.session_state.question_data
    user_answers = st.session_state.get('user_answers', {})
    
    all_correct = True
    
    # Check each missing position (including the implicit sum)
    positions_to_check = list(data['missing_positions'])
    if data['missing_positions']:
        positions_to_check.append("sum")
    
    for position in positions_to_check:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            
            if user_value != correct_value:
                all_correct = False
                break
    
    if all_correct:
        st.success("🎉 **Fantastic! You got it right!**")
        st.balloons()
        
        # Update performance tracking
        st.session_state.correct_streak += 1
        st.session_state.performance_history.append(True)
        
        # Adaptive encouragement based on streak
        if st.session_state.correct_streak >= 5:
            st.info("🔥 **Amazing streak! You're really mastering this!**")
        elif st.session_state.correct_streak >= 3:
            st.info("💪 **Great job! You're on a roll!**")
        
        show_solution()
    else:
        st.error("❌ **Not quite right. Let's learn from this!**")
        
        # Reset streak but track performance
        st.session_state.correct_streak = 0
        st.session_state.performance_history.append(False)
        
        # Show which answers were wrong
        show_wrong_answers(data, user_answers)
        
        # Adaptive hints based on what was wrong
        provide_targeted_hints(data, user_answers)
        show_solution()

def show_wrong_answers(data, user_answers):
    """Show which specific answers were incorrect"""
    positions_to_check = list(data['missing_positions'])
    if data['missing_positions']:
        positions_to_check.append("sum")
    
    wrong_answers = []
    for position in positions_to_check:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            if user_value != correct_value:
                position_names = {
                    "partial1": "🟢 Tens × Tens",
                    "partial2": "🟠 Tens × Ones", 
                    "partial3": "🟤 Ones × Tens",
                    "partial4": "🟫 Ones × Ones",
                    "sum": "🎯 Final Sum"
                }
                wrong_answers.append(f"**{position_names[position]}:** You wrote {user_value}, but it should be {correct_value}")
    
    if wrong_answers:
        st.markdown("**❌ These answers need correction:**")
        for wrong in wrong_answers:
            st.markdown(f"- {wrong}")

def provide_targeted_hints(data, user_answers):
    """Provide specific hints based on what the student got wrong"""
    positions_to_check = list(data['missing_positions'])
    if data['missing_positions']:
        positions_to_check.append("sum")
    
    wrong_positions = []
    for position in positions_to_check:
        if position in user_answers:
            user_value = user_answers[position]
            correct_value = st.session_state.correct_answers[position]
            if user_value != correct_value:
                wrong_positions.append(position)
    
    if "partial1" in wrong_positions:
        st.info("💡 **Hint for Tens × Tens:** Remember to multiply the tens digits and then add the zeros!")
    
    if "partial2" in wrong_positions or "partial3" in wrong_positions:
        st.info("💡 **Hint for Mixed Products:** Check which number is tens and which is ones carefully.")
    
    if "partial4" in wrong_positions:
        st.info("💡 **Hint for Ones × Ones:** This should be the simplest multiplication - just the ones digits!")
    
    if "sum" in wrong_positions:
        st.info("💡 **Hint for Final Sum:** Double-check your addition. Try adding the numbers in a different order!")

def show_solution():
    """Show the complete solution with visual aids"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Complete Solution**", expanded=True):
        st.markdown(f"""
        ### 🧮 Step-by-step solution for {data['multiplicand']} × {data['multiplier']}:
        """)
        
        # Visual breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **🔹 Breaking down {data['multiplicand']}:**
            - {data['multiplicand']} = {data['m1_tens']} + {data['m1_ones']}
            
            **🔹 Breaking down {data['multiplier']}:**
            - {data['multiplier']} = {data['m2_tens']} + {data['m2_ones']}
            """)
        
        with col2:
            st.markdown(f"""
            **🔹 Partial Products:**
            - 🟢 {data['m1_tens']} × {data['m2_tens']} = {data['partial1']}
            - 🟠 {data['m1_tens']} × {data['m2_ones']} = {data['partial2']}
            - 🟤 {data['m1_ones']} × {data['m2_tens']} = {data['partial3']}
            - 🟫 {data['m1_ones']} × {data['m2_ones']} = {data['partial4']}
            """)
        
        st.markdown(f"""
        **🎯 Final Answer:**
        {data['partial1']} + {data['partial2']} + {data['partial3']} + {data['partial4']} = **{data['total_sum']}**
        
        So {data['multiplicand']} × {data['multiplier']} = **{data['total_sum']}** ✅
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.show_step_solution = False
    st.session_state.user_answers = {}