import streamlit as st
import random

def run():
    """
    Main function to run the Expanded Form Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_onedigit_numbers_by_threedigit_or_fourdigit_numbers_using_expanded_form.py
    """
    # Initialize session state for difficulty and game state
    if "expanded_form_difficulty" not in st.session_state:
        st.session_state.expanded_form_difficulty = 1  # Start with 3-digit numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📝 Multiply Using Expanded Form")
    st.markdown("*Break down numbers and multiply each part separately*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.expanded_form_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "3-Digit Numbers",
            2: "Larger 3-Digit Numbers", 
            3: "4-Digit Numbers",
            4: "Complex Problems"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        # Progress bar (1 to 4 levels)
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
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
    with st.expander("💡 **Instructions & Expanded Form Guide**", expanded=False):
        st.markdown("""
        ### 📝 What is Expanded Form?
        
        **Expanded form** breaks a number into its place values:
        - **3-digit example:** 456 = 400 + 50 + 6
        - **4-digit example:** 2,834 = 2,000 + 800 + 30 + 4
        
        ### 🎯 Two Types of Questions:
        
        **Type 1: Step-by-Step Calculation** 
        - **Step 1:** We show you the expanded form breakdown
        - **Step 2:** You calculate each multiplication separately
        - **Step 3:** You enter your Step 2 answers again and add them up
        - **Purpose:** Practice both multiplication AND addition skills
        
        **Type 2: Fill in the Blanks**
        - Complete the missing parts of the equation
        - Fill in expanded form values
        - Calculate missing partial products
        - Find the final answer
        
        ### 🔢 How Expanded Form Multiplication Works:
        
        **Step 1: Break down the large number**
        - Example: 6 × 453
        - Break down 453: 453 = 400 + 50 + 3
        
        **Step 2: Multiply each part separately**
        - 6 × 400 = 2,400
        - 6 × 50 = 300  
        - 6 × 3 = 18
        
        **Step 3: Add all the products together**
        - 2,400 + 300 + 18 = 2,718
        - So 6 × 453 = 2,718
        
        ### 🔢 Example: Type 1 - 4 × 1,900
        
        **Step 1: Break down 1,900**
        - 1,900 = 1,000 + 900
        
        **Step 2: Multiply each part**
        - 4 × 1,000 = [you calculate: 4,000]
        - 4 × 900 = [you calculate: 3,600]
        
        **Step 3: Add them up**
        - [enter 4,000] + [enter 3,600] = [you calculate: 7,600]
        - This reinforces both multiplication AND addition skills!
        
        ### 🔢 Example: Type 2 - 4 × 615 (Fill in the Blanks)
        
        ### 🔢 Example: Type 2 - 4 × 615 (Fill in the Blanks)
        
        **Step 1: Complete the expanded form**
        - 4 × 615 = 4 × (600 + 10 + 5)
        
        **Step 2: Apply distributive property**
        - = (4 × 600) + (4 × 10) + (4 × 5)
        
        **Step 3: Calculate each part**
        - = 2400 + 40 + 20
        
        **Step 4: Add them up**
        - = 2460
        
        ### 💡 Tips for Success:
        - **Place values:** thousands, hundreds, tens, ones
        - **Fill in each blank** carefully
        - **Check your arithmetic** for each multiplication
        - **Watch for zeros** - 4 × 600 = 2,400 (not 24!)
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple 3-digit numbers (200-500)
        - **🟡 Level 2:** Larger 3-digit numbers (500-999)  
        - **🟠 Level 3:** 4-digit numbers (1000-5000)
        - **🔴 Level 4:** Complex problems with larger numbers
        """)

def generate_new_question():
    """Generate a new expanded form multiplication question - either Type 1 or Type 2"""
    difficulty = st.session_state.expanded_form_difficulty
    
    # Randomly choose question type
    question_type = random.choice([1, 2])  # 1 = step-by-step, 2 = fill-in-the-blanks
    
    # Single digit multiplier (2-9)
    single_digit = random.randint(2, 9)
    
    # Generate large number based on difficulty
    if difficulty == 1:
        # Level 1: Simple 3-digit numbers
        large_number = random.randint(200, 500)
    elif difficulty == 2:
        # Level 2: Larger 3-digit numbers
        large_number = random.randint(500, 999)
    elif difficulty == 3:
        # Level 3: 4-digit numbers
        large_number = random.randint(1000, 5000)
    else:  # Level 4
        # Level 4: Complex numbers
        large_number = random.randint(1000, 9999)
    
    # Break down the number into expanded form
    expanded_parts = break_down_to_expanded_form(large_number)
    
    # Calculate partial products
    partial_products = {}
    for place_name, value in expanded_parts.items():
        partial_products[place_name] = single_digit * value
    
    # Calculate final answer
    final_answer = single_digit * large_number
    
    if question_type == 1:
        # Type 1: Step-by-step calculation (current format)
        st.session_state.question_data = {
            "type": 1,
            "single_digit": single_digit,
            "large_number": large_number,
            "expanded_parts": expanded_parts,
            "partial_products": partial_products,
            "final_answer": final_answer
        }
        st.session_state.current_question = f"Calculate {single_digit} × {large_number:,} using expanded form"
        st.session_state.correct_answers = {
            **partial_products,
            "final_answer": final_answer
        }
    else:
        # Type 2: Fill-in-the-blanks format
        # Create blanks for some expanded form values and products
        blanks_needed = create_fill_in_blanks_structure(expanded_parts, partial_products, single_digit)
        
        st.session_state.question_data = {
            "type": 2,
            "single_digit": single_digit,
            "large_number": large_number,
            "expanded_parts": expanded_parts,
            "partial_products": partial_products,
            "final_answer": final_answer,
            "blanks": blanks_needed
        }
        st.session_state.current_question = "Complete the steps to find the product."
        st.session_state.correct_answers = blanks_needed

def create_fill_in_blanks_structure(expanded_parts, partial_products, single_digit):
    """Create the structure for fill-in-the-blanks questions"""
    blanks = {}
    
    # Choose 1-2 place values to be blanks in the expanded form
    place_names = list(expanded_parts.keys())
    num_blanks = min(2, len(place_names))
    blank_places = random.sample(place_names, num_blanks)
    
    # Add blanks for expanded form values
    for place in blank_places:
        blanks[f"expanded_{place}"] = expanded_parts[place]
    
    # Add blanks for corresponding partial products
    for place in blank_places:
        blanks[f"product_{place}"] = partial_products[place]
    
    # Always include final answer as a blank
    blanks["final_answer"] = single_digit * sum(expanded_parts.values())
    
    return blanks

def break_down_to_expanded_form(number):
    """Break down a number into expanded form parts"""
    parts = {}
    
    # Handle up to 4-digit numbers
    if number >= 1000:
        thousands = (number // 1000) * 1000
        if thousands > 0:
            parts['thousands'] = thousands
        number -= thousands
    
    if number >= 100:
        hundreds = (number // 100) * 100
        if hundreds > 0:
            parts['hundreds'] = hundreds
        number -= hundreds
    
    if number >= 10:
        tens = (number // 10) * 10
        if tens > 0:
            parts['tens'] = tens
        number -= tens
    
    if number > 0:
        parts['ones'] = number
    
    return parts

def display_question():
    """Display the expanded form multiplication question - handles both types"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("---")
    
    if data["type"] == 1:
        display_type1_question(data)
    else:
        display_type2_question(data)

def display_type1_question(data):
    """Display Type 1 (step-by-step) question with input boxes in Step 3"""
    # Show the problem setup
    st.markdown(f"### Step 1: Break down {data['large_number']:,} into expanded form")
    
    # Show the expanded form breakdown
    expanded_text = " + ".join([f"{value:,}" for value in data['expanded_parts'].values()])
    st.markdown(f"**{data['large_number']:,} = {expanded_text}**")
    
    st.markdown("### Step 2: Multiply each part and add them up")
    
    # Create the interactive form
    with st.form("expanded_form_type1", clear_on_submit=False):
        user_answers = {}
        
        # Create input fields for each partial product
        for place_name, place_value in data['expanded_parts'].items():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])
            
            with col1:
                st.markdown(f"**{data['single_digit']} × {place_value:,}**")
            
            with col2:
                st.markdown("**=**")
            
            with col3:
                user_answers[place_name] = st.number_input(
                    f"Answer for {place_value:,}",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get(place_name, 0),
                    step=1,
                    key=f"input_{place_name}",
                    label_visibility="collapsed"
                )
            
            with col4:
                st.markdown("")
            
            with col5:
                st.markdown("")
        
        # Add spacing
        st.markdown("---")
        
        # Step 3: Add partial products with input boxes
        st.markdown("### Step 3: Add all partial products together")
        
        # Create input boxes for each partial product that students calculated in Step 2
        place_names = list(data['expanded_parts'].keys())
        
        if len(place_names) == 2:
            # 2 parts: [input] + [input] = [final_input]
            cols = st.columns([2, 1, 2, 1, 2])
            
            with cols[0]:
                user_answers[f"sum_{place_names[0]}"] = st.number_input(
                    f"Enter your answer from {data['single_digit']} × {data['expanded_parts'][place_names[0]]:,}",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else user_answers.get(place_names[0], 0),
                    step=1,
                    key=f"sum_input_{place_names[0]}",
                    label_visibility="collapsed"
                )
            with cols[1]:
                st.markdown("**+**")
            with cols[2]:
                user_answers[f"sum_{place_names[1]}"] = st.number_input(
                    f"Enter your answer from {data['single_digit']} × {data['expanded_parts'][place_names[1]]:,}",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else user_answers.get(place_names[1], 0),
                    step=1,
                    key=f"sum_input_{place_names[1]}",
                    label_visibility="collapsed"
                )
            with cols[3]:
                st.markdown("**=**")
            with cols[4]:
                user_answers['final_answer'] = st.number_input(
                    "Final sum",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get('final_answer', 0),
                    step=1,
                    key="final_answer_input",
                    label_visibility="collapsed"
                )
                
        elif len(place_names) == 3:
            # 3 parts: [input] + [input] + [input] = [final_input]
            cols = st.columns([2, 1, 2, 1, 2, 1, 2])
            
            for i, place_name in enumerate(place_names):
                with cols[i * 2]:
                    user_answers[f"sum_{place_name}"] = st.number_input(
                        f"Enter your answer from {data['single_digit']} × {data['expanded_parts'][place_name]:,}",
                        min_value=0,
                        value=0 if not st.session_state.answer_submitted else user_answers.get(place_name, 0),
                        step=1,
                        key=f"sum_input_{place_name}",
                        label_visibility="collapsed"
                    )
                
                if i < len(place_names) - 1:
                    with cols[i * 2 + 1]:
                        st.markdown("**+**")
            
            with cols[5]:
                st.markdown("**=**")
            with cols[6]:
                user_answers['final_answer'] = st.number_input(
                    "Final sum",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get('final_answer', 0),
                    step=1,
                    key="final_answer_input",
                    label_visibility="collapsed"
                )
                
        else:
            # 4 parts: [input] + [input] + [input] + [input] = [final_input]
            cols = st.columns([1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5])
            
            for i, place_name in enumerate(place_names):
                with cols[i * 2]:
                    user_answers[f"sum_{place_name}"] = st.number_input(
                        f"Enter your answer from {data['single_digit']} × {data['expanded_parts'][place_name]:,}",
                        min_value=0,
                        value=0 if not st.session_state.answer_submitted else user_answers.get(place_name, 0),
                        step=1,
                        key=f"sum_input_{place_name}",
                        label_visibility="collapsed"
                    )
                
                if i < len(place_names) - 1:
                    with cols[i * 2 + 1]:
                        st.markdown("**+**")
            
            with cols[7]:
                st.markdown("**=**")
            with cols[8]:
                user_answers['final_answer'] = st.number_input(
                    "Final sum",
                    min_value=0,
                    value=0 if not st.session_state.answer_submitted else st.session_state.correct_answers.get('final_answer', 0),
                    step=1,
                    key="final_answer_input",
                    label_visibility="collapsed"
                )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Check All Answers", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answers = user_answers
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_type2_question(data):
    """Display Type 2 (fill-in-the-blanks) question with clean, simple layout"""
    
    st.markdown("### Complete the steps to find the product.")
    st.markdown("---")
    
    with st.form("expanded_form_type2", clear_on_submit=False):
        user_answers = {}
        
        # Get the expanded parts in order (thousands, hundreds, tens, ones)
        ordered_parts = []
        place_order = ['thousands', 'hundreds', 'tens', 'ones']
        for place in place_order:
            if place in data['expanded_parts']:
                ordered_parts.append((place, data['expanded_parts'][place]))
        
        # Add custom CSS for clean input boxes
        st.markdown("""
        <style>
        .clean-input {
            border: 2px solid #007bff;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            width: 80px;
            height: 40px;
            background-color: white;
        }
        .equation-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 15px 0;
            font-size: 18px;
            font-weight: bold;
        }
        .section-header {
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            margin: 20px 0 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Section 1: Expanded form
        st.markdown('<div class="section-header">Complete the expanded form:</div>', unsafe_allow_html=True)
        
        # Create the equation line by line using simple columns
        cols1 = st.columns([1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1])
        
        with cols1[0]:
            st.markdown(f'<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">{data["single_digit"]}</div>', unsafe_allow_html=True)
        with cols1[1]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">×</div>', unsafe_allow_html=True)
        with cols1[2]:
            st.markdown(f'<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">{data["large_number"]:,}</div>', unsafe_allow_html=True)
        with cols1[3]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">=</div>', unsafe_allow_html=True)
        with cols1[4]:
            st.markdown(f'<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">{data["single_digit"]}</div>', unsafe_allow_html=True)
        with cols1[5]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">×</div>', unsafe_allow_html=True)
        with cols1[6]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">(</div>', unsafe_allow_html=True)
        
        # Add the expanded parts with input boxes
        input_col_idx = 7
        for i, (place_name, value) in enumerate(ordered_parts):
            if f"expanded_{place_name}" in data['blanks']:
                with cols1[input_col_idx]:
                    user_answers[f"expanded_{place_name}"] = st.number_input(
                        f"Input {place_name}",
                        min_value=0,
                        value=0 if not st.session_state.answer_submitted else data['blanks'][f"expanded_{place_name}"],
                        step=1,
                        key=f"exp_{place_name}",
                        label_visibility="collapsed"
                    )
            else:
                with cols1[input_col_idx]:
                    st.markdown(f'<div style="font-size: 18px; font-weight: bold; padding: 10px 0; text-align: center;">{value}</div>', unsafe_allow_html=True)
            
            input_col_idx += 1
            
            # Add + or closing parenthesis
            if i < len(ordered_parts) - 1:
                with cols1[input_col_idx]:
                    st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0; text-align: center;">+</div>', unsafe_allow_html=True)
                input_col_idx += 1
            else:
                with cols1[input_col_idx]:
                    st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0; text-align: center;">)</div>', unsafe_allow_html=True)
                break
        
        # Section 2: Distributive property (display only)
        st.markdown('<div class="section-header">Apply distributive property:</div>', unsafe_allow_html=True)
        
        # Build the distributive equation
        distributive_parts = []
        for place_name, value in ordered_parts:
            if f"expanded_{place_name}" in data['blanks']:
                if f"expanded_{place_name}" in user_answers and user_answers[f"expanded_{place_name}"] > 0:
                    distributive_parts.append(f"({data['single_digit']} × {user_answers[f'expanded_{place_name}']:,})")
                else:
                    distributive_parts.append(f"({data['single_digit']} × ___)")
            else:
                distributive_parts.append(f"({data['single_digit']} × {value})")
        
        distributive_text = "= " + " + ".join(distributive_parts)
        st.markdown(f'''
        <div style="
            font-size: 18px; 
            font-weight: bold; 
            padding: 15px; 
            background-color: #e9ecef; 
            border-radius: 6px; 
            text-align: center; 
            margin: 10px 0;
        ">
            {distributive_text}
        </div>
        ''', unsafe_allow_html=True)
        
        # Section 3: Calculate products
        st.markdown('<div class="section-header">Calculate each product:</div>', unsafe_allow_html=True)
        
        # Create columns for products
        num_parts = len(ordered_parts)
        if num_parts == 2:
            cols3 = st.columns([1, 2, 1, 2, 6])
        elif num_parts == 3:
            cols3 = st.columns([1, 2, 1, 2, 1, 2, 4])
        else:  # 4 parts
            cols3 = st.columns([1, 1.5, 1, 1.5, 1, 1.5, 1, 1.5, 2])
        
        with cols3[0]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">=</div>', unsafe_allow_html=True)
        
        col_idx = 1
        for i, (place_name, value) in enumerate(ordered_parts):
            if f"product_{place_name}" in data['blanks']:
                with cols3[col_idx]:
                    user_answers[f"product_{place_name}"] = st.number_input(
                        f"Product {place_name}",
                        min_value=0,
                        value=0 if not st.session_state.answer_submitted else data['blanks'][f"product_{place_name}"],
                        step=1,
                        key=f"prod_{place_name}",
                        label_visibility="collapsed"
                    )
            else:
                product = data['partial_products'][place_name]
                with cols3[col_idx]:
                    st.markdown(f'<div style="font-size: 18px; font-weight: bold; padding: 10px 0; text-align: center;">{product}</div>', unsafe_allow_html=True)
            
            col_idx += 1
            
            # Add + between products
            if i < len(ordered_parts) - 1:
                with cols3[col_idx]:
                    st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0; text-align: center;">+</div>', unsafe_allow_html=True)
                col_idx += 1
        
        # Section 4: Final answer
        st.markdown('<div class="section-header">Final answer:</div>', unsafe_allow_html=True)
        
        cols4 = st.columns([1, 3, 8])
        with cols4[0]:
            st.markdown('<div style="font-size: 18px; font-weight: bold; padding: 10px 0;">=</div>', unsafe_allow_html=True)
        with cols4[1]:
            user_answers['final_answer'] = st.number_input(
                "Final answer",
                min_value=0,
                value=0 if not st.session_state.answer_submitted else data['blanks']['final_answer'],
                step=1,
                key="final_ans",
                label_visibility="collapsed"
            )
        
        # Submit button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answers = user_answers
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
    """Display feedback for submitted answers - handles both question types"""
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    
    st.markdown("### 📊 Results:")
    
    all_correct = True
    partial_correct = 0
    total_parts = len(correct_answers)
    
    # Check each answer
    for key, correct_value in correct_answers.items():
        user_value = user_answers.get(key, 0)
        
        if user_value == correct_value:
            if key == "final_answer":
                st.success(f"✅ **Final Answer: {correct_value:,}** - Correct!")
            elif key.startswith("expanded_"):
                place_name = key.replace("expanded_", "")
                st.success(f"✅ **Expanded form ({place_name}): {correct_value:,}** - Correct!")
            elif key.startswith("product_"):
                place_name = key.replace("product_", "")
                place_value = data['expanded_parts'][place_name]
                st.success(f"✅ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - Correct!")
            else:
                # Type 1 format
                place_value = data['expanded_parts'].get(key, 0)
                st.success(f"✅ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - Correct!")
            partial_correct += 1
        else:
            if key == "final_answer":
                st.error(f"❌ **Final Answer: {correct_value:,}** - You answered: {user_value:,}")
            elif key.startswith("expanded_"):
                place_name = key.replace("expanded_", "")
                st.error(f"❌ **Expanded form ({place_name}): {correct_value:,}** - You answered: {user_value:,}")
            elif key.startswith("product_"):
                place_name = key.replace("product_", "")
                place_value = data['expanded_parts'][place_name]
                st.error(f"❌ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - You answered: {user_value:,}")
            else:
                # Type 1 format
                place_value = data['expanded_parts'].get(key, 0)
                st.error(f"❌ **{data['single_digit']} × {place_value:,} = {correct_value:,}** - You answered: {user_value:,}")
            all_correct = False
    
    # Overall feedback
    if all_correct:
        st.success(f"🎉 **Perfect! You got everything right! ({partial_correct}/{total_parts})**")
        # Increase difficulty
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = min(
            st.session_state.expanded_form_difficulty + 1, 4
        )
        
        if st.session_state.expanded_form_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered expanded form multiplication!**")
        elif old_difficulty < st.session_state.expanded_form_difficulty:
            st.info(f"⬆️ **Excellent work! Moving to Level {st.session_state.expanded_form_difficulty}**")
    
    elif partial_correct >= total_parts // 2:
        st.warning(f"📈 **Good effort! You got {partial_correct}/{total_parts} correct. Keep practicing!**")
    else:
        st.error(f"📚 **Let's review the steps. You got {partial_correct}/{total_parts} correct.**")
        # Decrease difficulty
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = max(
            st.session_state.expanded_form_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.expanded_form_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Back to Level {st.session_state.expanded_form_difficulty}**")
    
    # Show explanation if not all correct
    if not all_correct:
        show_detailed_explanation()

def show_detailed_explanation():
    """Show detailed step-by-step explanation"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### ✅ Complete Solution: {data['single_digit']} × {data['large_number']:,}
        
        **Step 1: Break down {data['large_number']:,} into expanded form**
        """)
        
        expanded_parts_text = " + ".join([f"{value:,}" for value in data['expanded_parts'].values()])
        st.markdown(f"- {data['large_number']:,} = {expanded_parts_text}")
        
        st.markdown(f"""
        **Step 2: Apply distributive property**
        """)
        
        distributive_parts = [f"({data['single_digit']} × {value:,})" for value in data['expanded_parts'].values()]
        distributive_text = " + ".join(distributive_parts)
        st.markdown(f"- {data['single_digit']} × {data['large_number']:,} = {distributive_text}")
        
        st.markdown(f"""
        **Step 3: Calculate each product**
        """)
        
        for place_name, place_value in data['expanded_parts'].items():
            product = data['partial_products'][place_name]
            st.markdown(f"- {data['single_digit']} × {place_value:,} = {product:,}")
        
        st.markdown(f"""
        **Step 4: Add all the partial products**
        """)
        
        addition_parts = [f"{product:,}" for product in data['partial_products'].values()]
        addition_equation = " + ".join(addition_parts) + f" = {data['final_answer']:,}"
        st.markdown(f"- {addition_equation}")
        
        st.markdown(f"""
        **Final Answer: {data['single_digit']} × {data['large_number']:,} = {data['final_answer']:,}** ✅
        
        ### 💡 Remember:
        - Break down the large number by place value
        - Apply the distributive property: a × (b + c) = (a × b) + (a × c)
        - Calculate each partial product carefully
        - Add all the partial products together
        - Double-check your arithmetic at each step!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answers" in st.session_state:
        del st.session_state.user_answers