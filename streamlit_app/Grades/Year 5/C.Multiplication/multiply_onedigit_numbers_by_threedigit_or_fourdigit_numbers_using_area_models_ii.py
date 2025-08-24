import streamlit as st
import random

def run():
    """
    Main function to run the Area Models II practice activity.
    Students first calculate each partial product, then find the total.
    """
    # Initialize session state for difficulty and game state
    if "area_models_ii_difficulty" not in st.session_state:
        st.session_state.area_models_ii_difficulty = 1  # Start with 3-digit numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.partial_answers = {}
        st.session_state.step = 1  # 1 = calculate partial products, 2 = final answer
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📊 Multiply Using Area Models II")
    st.markdown("*Step-by-step: Calculate each area, then find the total*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.area_models_ii_difficulty
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
    with st.expander("💡 **Instructions & Step-by-Step Guide**", expanded=False):
        st.markdown("""
        ### 📊 How Area Models II Works:
        
        **This is a TWO-STEP process:**
        
        ### Step 1: Calculate Each Area (Partial Product)
        - Look at each colored rectangle
        - Calculate: multiplier × place value
        - Enter the result in the white box inside each rectangle
        
        ### Step 2: Find the Total Area
        - Add up all the partial products
        - Enter the final answer
        
        ### 🔢 Example: 2 × 335
        
        **Step 1: Break down 335**
        - 335 = 300 + 30 + 5
        
        **Step 2: Calculate each area**
        - Green rectangle: 2 × 300 = 600 ✏️
        - Orange rectangle: 2 × 30 = 60 ✏️
        - Pink rectangle: 2 × 5 = 10 ✏️
        
        **Step 3: Add all areas**
        - Total: 600 + 60 + 10 = 670
        
        ### 💡 Tips for Success:
        
        **For Partial Products:**
        - **× 100s:** 2 × 300 = 600 (multiply, then add zeros)
        - **× 10s:** 2 × 30 = 60 (multiply, then add one zero)
        - **× 1s:** 2 × 5 = 10 (simple multiplication)
        
        **For Final Answer:**
        - Add carefully: hundreds + tens + ones
        - Double-check by verifying the original multiplication
        
        ### 🎯 What Makes This Different:
        - **Interactive:** You calculate each step yourself
        - **Understanding:** Shows how place values work
        - **Step-by-step:** Builds confidence gradually
        - **Visual:** See exactly what you're multiplying
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple 3-digit numbers (200-500)
        - **🟡 Level 2:** Larger 3-digit numbers (500-999)
        - **🟠 Level 3:** 4-digit numbers (1000-5000)
        - **🔴 Level 4:** Complex problems with larger numbers
        """)

def generate_new_question():
    """Generate a new interactive area model question"""
    try:
        difficulty = st.session_state.area_models_ii_difficulty
        
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
        
        # Break down the number correctly
        breakdown = break_down_number(large_number)
        
        # Validate breakdown
        if not breakdown or len(breakdown) == 0:
            breakdown = [large_number]
        
        # Calculate partial products and total
        partial_products = [single_digit * value for value in breakdown]
        total = single_digit * large_number
        
        st.session_state.question_data = {
            "single_digit": single_digit,
            "large_number": large_number,
            "breakdown": breakdown,
            "partial_products": partial_products,
            "total": total
        }
        st.session_state.correct_answer = total
        st.session_state.current_question = f"Use the model to find {single_digit} × {large_number:,}."
        st.session_state.step = 1
        st.session_state.partial_answers = {}
        
    except Exception as e:
        # Emergency fallback
        st.session_state.question_data = {
            "single_digit": 2,
            "large_number": 335,
            "breakdown": [300, 30, 5],
            "partial_products": [600, 60, 10],
            "total": 670
        }
        st.session_state.correct_answer = 670
        st.session_state.current_question = "Use the model to find 2 × 335."
        st.session_state.step = 1
        st.session_state.partial_answers = {}

def break_down_number(number):
    """Break down a number into place values"""
    breakdown = []
    temp = number
    
    # Handle thousands
    if temp >= 1000:
        thousands = (temp // 1000) * 1000
        breakdown.append(thousands)
        temp -= thousands
    
    # Handle hundreds
    if temp >= 100:
        hundreds = (temp // 100) * 100
        breakdown.append(hundreds)
        temp -= hundreds
    
    # Handle tens
    if temp >= 10:
        tens = (temp // 10) * 10
        breakdown.append(tens)
        temp -= tens
    
    # Handle ones
    if temp > 0:
        breakdown.append(temp)
    
    return breakdown

def display_question():
    """Display the interactive area model question"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📊 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    if st.session_state.step == 1:
        display_step1_partial_products(data)
    else:
        display_step2_final_answer(data)

def display_step1_partial_products(data):
    """Display step 1: Calculate each partial product"""
    st.markdown("### First, find the area of each rectangle.")
    
    # Create the interactive area model (place values will be shown above each section)
    create_interactive_area_model(data)
    
    # Form for partial product inputs
    with st.form("partial_products_form", clear_on_submit=False):
        st.markdown("**Enter the area of each rectangle:**")
        
        # Create input fields for each partial product
        cols = st.columns(len(data['breakdown']))
        partial_inputs = {}
        
        for i, (place_val, correct_product) in enumerate(zip(data['breakdown'], data['partial_products'])):
            with cols[i]:
                st.markdown(f"**{data['single_digit']} × {place_val:,} =**")
                partial_inputs[i] = st.number_input(
                    f"Area {i+1}:",
                    min_value=0,
                    value=st.session_state.partial_answers.get(i, 0),
                    step=1,
                    key=f"partial_{i}",
                    label_visibility="collapsed"
                )
        
        # Submit button for partial products
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_partials = st.form_submit_button("✅ Check Areas", type="primary", use_container_width=True)
        
        if submit_partials:
            # Check all partial products
            all_correct = True
            st.session_state.partial_answers = partial_inputs.copy()
            
            for i, correct_product in enumerate(data['partial_products']):
                if partial_inputs[i] != correct_product:
                    all_correct = False
                    break
            
            if all_correct:
                st.success("🎉 **Great! All areas are correct!**")
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("❌ **Some areas are incorrect. Check your calculations.**")
                show_partial_feedback(data, partial_inputs)

def display_step2_final_answer(data):
    """Display step 2: Calculate the final answer with individual input verification"""
    st.markdown("### Then, find the total area.")
    
    # Show the completed area model with correct partial products
    create_completed_area_model(data)
    
    # Form for both partial product verification AND final answer
    with st.form("final_calculation_form", clear_on_submit=False):
        st.markdown("**Enter the area of each rectangle:**")
        
        # Create input fields for each partial product verification
        cols = st.columns(len(data['breakdown']))
        partial_inputs = {}
        
        for i, (place_val, correct_product) in enumerate(zip(data['breakdown'], data['partial_products'])):
            with cols[i]:
                st.markdown(f"**{data['single_digit']} × {place_val:,} =**")
                partial_inputs[i] = st.number_input(
                    f"Product {i+1}:",
                    min_value=0,
                    value=st.session_state.partial_answers.get(i, 0),
                    step=1,
                    key=f"final_partial_{i}",
                    label_visibility="collapsed"
                )
        
        # Show the addition equation
        addition_parts = [f"{product:,}" for product in data['partial_products']]
        addition_text = " + ".join(addition_parts) + " = ?"
        
        st.markdown(f"""
        <div style="
            text-align: center;
            margin: 20px 0;
            font-size: 18px;
            color: #333;
            font-weight: bold;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        ">
            {addition_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Final answer input
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"**{data['single_digit']} × {data['large_number']:,} =**")
        
        with col2:
            final_answer = st.number_input(
                "Final Answer:",
                min_value=0,
                value=0 if not st.session_state.get('answer_submitted', False) else st.session_state.get('user_answer', 0),
                step=1,
                key="final_answer_input",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("")  # Empty space
        
        # Submit button for everything
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_final = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_final:
            # Check both partial products and final answer
            partial_correct = True
            for i, correct_product in enumerate(data['partial_products']):
                if partial_inputs[i] != correct_product:
                    partial_correct = False
                    break
            
            final_correct = (final_answer == data['total'])
            
            # Store answers for feedback
            st.session_state.partial_answers = partial_inputs.copy()
            st.session_state.user_answer = final_answer
            st.session_state.partial_correct = partial_correct
            st.session_state.final_correct = final_correct
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_interactive_area_model(data):
    """Create area model with empty boxes for partial products"""
    # Colors for different place values
    colors = ['#4CAF50', '#FF9800', '#E91E63', '#2196F3', '#9C27B0']
    
    try:
        # First row: Place values above each section
        cols_top = st.columns([1] + [3] * len(data['breakdown']))
        
        # Empty space above multiplier
        with cols_top[0]:
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        # Place values above each section
        for i, value in enumerate(data['breakdown']):
            with cols_top[i + 1]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                    padding: 10px;
                    margin: 5px;
                ">
                    {value:,}
                </div>
                """, unsafe_allow_html=True)
        
        # Second row: Multiplier and colored sections with empty white boxes
        cols_main = st.columns([1] + [3] * len(data['breakdown']))
        
        # Multiplier column
        with cols_main[0]:
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 30px 5px;
                font-weight: bold;
                font-size: 32px;
                color: #333;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 120px;
            ">
                {data['single_digit']}
            </div>
            """, unsafe_allow_html=True)
        
        # Place value sections with empty white boxes
        for i, value in enumerate(data['breakdown']):
            with cols_main[i + 1]:
                color = colors[i % len(colors)]
                # Show user's answer if they've entered one
                user_answer = st.session_state.partial_answers.get(i, "")
                display_answer = f"{user_answer}" if user_answer else "?"
                
                st.markdown(f"""
                <div style="
                    background-color: {color};
                    color: white;
                    padding: 15px;
                    text-align: center;
                    border: 2px solid #333;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 5px;
                    height: 120px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                ">
                    <div style="
                        background-color: white;
                        color: #333;
                        border: 2px solid #333;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 20px;
                        font-weight: bold;
                        min-width: 80px;
                        min-height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        {display_answer}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error creating interactive model: {str(e)}")

def create_completed_area_model(data):
    """Create area model showing the correct partial products"""
    # Colors for different place values
    colors = ['#4CAF50', '#FF9800', '#E91E63', '#2196F3', '#9C27B0']
    
    try:
        # First row: Place values above each section
        cols_top = st.columns([1] + [3] * len(data['breakdown']))
        
        # Empty space above multiplier
        with cols_top[0]:
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        # Place values above each section
        for i, value in enumerate(data['breakdown']):
            with cols_top[i + 1]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                    padding: 10px;
                    margin: 5px;
                ">
                    {value:,}
                </div>
                """, unsafe_allow_html=True)
        
        # Second row: Multiplier and colored sections with correct partial products
        cols_main = st.columns([1] + [3] * len(data['breakdown']))
        
        # Multiplier column
        with cols_main[0]:
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 30px 5px;
                font-weight: bold;
                font-size: 32px;
                color: #333;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 120px;
            ">
                {data['single_digit']}
            </div>
            """, unsafe_allow_html=True)
        
        # Place value sections with correct partial products
        for i, (value, product) in enumerate(zip(data['breakdown'], data['partial_products'])):
            with cols_main[i + 1]:
                color = colors[i % len(colors)]
                st.markdown(f"""
                <div style="
                    background-color: {color};
                    color: white;
                    padding: 15px;
                    text-align: center;
                    border: 2px solid #333;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 5px;
                    height: 120px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="
                        background-color: white;
                        color: #333;
                        border: 2px solid #333;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 20px;
                        font-weight: bold;
                        min-width: 80px;
                        min-height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        {product:,}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error creating completed model: {str(e)}")

def show_partial_feedback(data, user_inputs):
    """Show feedback for partial products"""
    with st.expander("📖 **Check your calculations**", expanded=True):
        for i, (place_val, correct_product) in enumerate(zip(data['breakdown'], data['partial_products'])):
            user_answer = user_inputs[i]
            if user_answer == correct_product:
                st.success(f"✅ **Area {i+1}:** {data['single_digit']} × {place_val:,} = {correct_product:,} ✓")
            else:
                st.error(f"❌ **Area {i+1}:** {data['single_digit']} × {place_val:,} = {correct_product:,} (you entered {user_answer:,})")

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
    """Display feedback for the final answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! The answer is {correct_answer:,}!**")
        
        # Increase difficulty (max 4 levels)
        old_difficulty = st.session_state.area_models_ii_difficulty
        st.session_state.area_models_ii_difficulty = min(
            st.session_state.area_models_ii_difficulty + 1, 4
        )
        
        # Show encouragement based on difficulty
        if st.session_state.area_models_ii_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered interactive area models!**")
        elif old_difficulty < st.session_state.area_models_ii_difficulty:
            st.info(f"⬆️ **Great job! Moving to Level {st.session_state.area_models_ii_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,}**.")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.area_models_ii_difficulty
        st.session_state.area_models_ii_difficulty = max(
            st.session_state.area_models_ii_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.area_models_ii_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Back to Level {st.session_state.area_models_ii_difficulty}**")
        
        # Show explanation
        show_detailed_explanation()

def show_detailed_explanation():
    """Show detailed step-by-step explanation"""
    data = st.session_state.question_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for step-by-step explanation**", expanded=True):
        st.markdown(f"""
        ### ✅ Correct Answer: **{correct_answer:,}**
        
        **Complete solution for {data['single_digit']} × {data['large_number']:,}:**
        
        **Step 1: Break down {data['large_number']:,} by place value**
        """)
        
        breakdown_text = ' + '.join([f'{v:,}' for v in data['breakdown']])
        st.markdown(f"- {data['large_number']:,} = {breakdown_text}")
        
        st.markdown(f"""
        **Step 2: Calculate each partial product (area)**
        """)
        
        for place_val, product in zip(data['breakdown'], data['partial_products']):
            st.markdown(f"- {data['single_digit']} × {place_val:,} = {product:,}")
        
        st.markdown(f"""
        **Step 3: Add all partial products**
        """)
        
        addition_parts = [f"{product:,}" for product in data['partial_products']]
        addition_equation = " + ".join(addition_parts) + f" = {correct_answer:,}"
        st.markdown(f"- {addition_equation}")
        
        st.markdown(f"""
        **Step 4: Verify**
        - {data['single_digit']} × {data['large_number']:,} = {correct_answer:,} ✅
        
        **Remember:** Area models help you see exactly what you're multiplying!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.partial_answers = {}
    st.session_state.step = 1
    if "user_answer" in st.session_state:
        del st.session_state.user_answer