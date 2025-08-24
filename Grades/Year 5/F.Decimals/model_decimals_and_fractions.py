import streamlit as st
import streamlit.components.v1 as components
import random
import json

def run():
    """
    Main function to run the Model Decimals and Fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/F. Decimals/model_decimals_and_fractions.py
    """
    # Initialize session state
    if "model_df_difficulty" not in st.session_state:
        st.session_state.model_df_difficulty = 1
    
    if "current_model_df_problem" not in st.session_state:
        st.session_state.current_model_df_problem = None
        st.session_state.model_df_answer = None
        st.session_state.model_df_feedback = False
        st.session_state.model_df_submitted = False
        st.session_state.model_df_data = {}
        st.session_state.user_shaded_count = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > F. Decimals**")
    st.title("🎨 Model Decimals and Fractions")
    st.markdown("*Click and drag to shade squares and model the given fraction*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.model_df_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_model_df_problem is None:
        generate_model_df_problem()
    
    # Display current question
    display_model_df_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Model Decimals and Fractions**", expanded=False):
        st.markdown("""
        ### How to Use the Interactive Grid:
        
        #### **Drag and Shade:**
        - **Click and drag** across squares/strips to shade multiple at once
        - **Single click** to shade/unshade individual squares
        - **Right-click** to unshade (or click shaded squares)
        - **Visual feedback** shows what you're shading in real-time
        
        #### **For Tenths (x/10):**
        - **Grid Type:** 10 vertical strips
        - **Each strip represents:** 1/10 or 0.1
        - **Example:** To show 7/10, shade 7 strips
        
        #### **For Hundredths (x/100):**
        - **Grid Type:** 10×10 grid (100 squares)
        - **Each square represents:** 1/100 or 0.01
        - **Example:** To show 74/100, shade 74 squares
        
        ### Tips for Success:
        
        #### **Efficient Shading:**
        - **Drag across rows** for hundredths (easier counting)
        - **Drag across strips** for tenths
        - **Count as you go** to avoid over/under-shading
        - **Use the counter** to track your progress
        
        #### **Understanding Equivalents:**
        - **1/10 = 10/100** (1 strip = 10 squares)
        - **5/10 = 50/100 = 0.5** (half)
        - **25/100 = 0.25** (quarter)
        - **75/100 = 0.75** (three quarters)
        
        ### Visual Feedback:
        - **Blue squares/strips** = shaded
        - **White squares/strips** = unshaded
        - **Green highlight** = currently dragging over
        - **Counter updates** in real-time as you shade
        """)

def generate_model_df_problem():
    """Generate modeling problems based on difficulty level"""
    difficulty = st.session_state.model_df_difficulty
    
    if difficulty == 1:
        # Level 1: Simple tenths only (1/10 to 9/10)
        grid_type = "tenths"
        numerator = random.randint(2, 8)  # Avoid 1 and 9 to make it not too easy/hard
        denominator = 10
        
    elif difficulty == 2:
        # Level 2: Mix of tenths and easy hundredths (multiples of 10)
        grid_type = random.choice(["tenths", "hundredths"])
        
        if grid_type == "tenths":
            numerator = random.randint(1, 9)
            denominator = 10
        else:  # hundredths - use easy multiples of 10
            numerator = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90])
            denominator = 100
            
    elif difficulty == 3:
        # Level 3: More hundredths + some decimal notation
        grid_type = random.choice(["tenths", "hundredths", "hundredths"])  # 2/3 chance hundredths
        
        if grid_type == "tenths":
            numerator = random.randint(2, 8)
            denominator = 10
        else:  # hundredths - wider range
            numerator = random.randint(15, 85)  # Avoid very easy ones
            denominator = 100
    
    elif difficulty == 4:
        # Level 4: Mostly hundredths with some tenths
        grid_type = random.choice(["hundredths", "hundredths", "hundredths", "tenths"])  # 3/4 chance hundredths
        
        if grid_type == "tenths":
            numerator = random.randint(1, 9)
            denominator = 10
        else:
            numerator = random.randint(5, 95)
            denominator = 100
    
    else:  # difficulty == 5
        # Level 5: All types with emphasis on hundredths
        grid_type = random.choice(["hundredths", "hundredths", "tenths"])  # 2/3 chance hundredths
        
        if grid_type == "tenths":
            numerator = random.randint(1, 9)
            denominator = 10
        else:
            numerator = random.randint(1, 99)
            denominator = 100
    
    # Determine display format (fraction or decimal)
    display_formats = ["fraction"]
    if difficulty >= 3:
        display_formats.append("decimal")
    
    display_format = random.choice(display_formats)
    
    # Create problem text
    if display_format == "fraction":
        problem_text = f"Show {numerator}/{denominator} by shading the model."
        target_decimal = numerator / denominator
    else:  # decimal
        target_decimal = numerator / denominator
        problem_text = f"Show {target_decimal} by shading the model."
    
    st.session_state.model_df_data = {
        "grid_type": grid_type,
        "target_numerator": numerator,
        "target_denominator": denominator,
        "target_decimal": target_decimal,
        "problem_text": problem_text,
        "display_format": display_format
    }
    
    st.session_state.model_df_answer = numerator
    st.session_state.current_model_df_problem = problem_text
    st.session_state.user_shaded_count = 0
    st.session_state.model_df_feedback = False
    st.session_state.model_df_submitted = False

def display_model_df_problem():
    """Display the modeling problem with interactive drag-and-shade grid"""
    data = st.session_state.model_df_data
    
    # Display the problem
    st.markdown("### 🎯 Problem:")
    st.markdown(f"""
    <div style="
        background-color: #e8f4fd; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #2196F3;
        font-size: 20px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #1565C0;
    ">
        {data['problem_text']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Click and drag to shade. Click shaded squares to unshade.**")
    
    # Display the interactive grid
    display_interactive_grid(data)

def display_interactive_grid(data):
    """Display the interactive drag-and-shade grid"""
    grid_type = data["grid_type"]
    target_numerator = data["target_numerator"]
    target_denominator = data["target_denominator"]
    
    # Create the HTML/JavaScript grid
    if grid_type == "tenths":
        grid_html = create_tenths_grid_html(target_numerator, target_denominator)
        height = 450
    else:
        grid_html = create_hundredths_grid_html(target_numerator, target_denominator)
        height = 550
    
    # Display the interactive grid
    components.html(grid_html, height=height, scrolling=False)
    
    # Create manual submit section below the grid
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Manual input for shaded count (as backup and for validation)
        st.markdown("### 📊 Submit Your Answer:")
        
        shaded_count = st.number_input(
            "How many squares/strips did you shade?",
            min_value=0,
            max_value=target_denominator,
            value=st.session_state.get("user_shaded_count", 0),
            help="Count the blue squares/strips you shaded and enter the number"
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                st.session_state.user_shaded_count = shaded_count
                st.session_state.model_df_user_answer = shaded_count
                st.session_state.model_df_feedback = True
                st.session_state.model_df_submitted = True
                st.rerun()
        
        with col_b:
            if st.button("🔄 New Grid", use_container_width=True):
                st.rerun()  # This will regenerate the grid with same problem
    
    # Show feedback if submitted
    if st.session_state.get("model_df_feedback", False):
        show_model_df_feedback()

def create_tenths_grid_html(target_numerator, target_denominator):
    """Create HTML/JavaScript for interactive tenths grid"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .grid-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 10px;
                margin: 10px;
            }}
            .tenths-grid {{
                display: flex;
                border: 3px solid #333;
                border-radius: 5px;
                overflow: hidden;
            }}
            .strip {{
                width: 60px;
                height: 200px;
                border: 1px solid #333;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
                user-select: none;
                transition: background-color 0.1s;
            }}
            .strip.shaded {{
                background-color: #2196F3;
                color: white;
            }}
            .strip.unshaded {{
                background-color: white;
                color: #333;
            }}
            .strip.hover {{
                background-color: #4CAF50 !important;
                color: white;
            }}
            .counter {{
                text-align: center;
                margin: 20px;
                font-size: 18px;
                font-weight: bold;
                color: #1565C0;
            }}
            .controls {{
                text-align: center;
                margin: 20px;
            }}
            .btn {{
                padding: 10px 20px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }}
            .btn-clear {{ background-color: #f44336; color: white; }}
            .btn-clear:hover {{ background-color: #da190b; }}
        </style>
    </head>
    <body>
        <div class="grid-container">
            <div>
                <div class="tenths-grid" id="tenthsGrid">
                    <!-- Strips will be generated by JavaScript -->
                </div>
                <div class="counter" id="counter">Shaded: 0 out of 10</div>
                <div class="controls">
                    <button class="btn btn-clear" onclick="clearAll()">🧹 Clear All</button>
                </div>
                <div style="text-align: center; margin-top: 15px; color: #666; font-size: 14px;">
                    Click and drag to shade strips. Count your shaded strips and enter the number below.
                </div>
            </div>
        </div>

        <script>
            let shadedSquares = new Set();
            let isDragging = false;
            let isShading = true; // true for shading, false for unshading

            function initGrid() {{
                const grid = document.getElementById('tenthsGrid');
                
                for (let i = 0; i < 10; i++) {{
                    const strip = document.createElement('div');
                    strip.className = 'strip unshaded';
                    strip.textContent = i + 1;
                    strip.dataset.index = i;
                    
                    strip.addEventListener('mousedown', startDrag);
                    strip.addEventListener('mouseenter', dragOver);
                    strip.addEventListener('mouseup', endDrag);
                    strip.addEventListener('click', singleClick);
                    
                    grid.appendChild(strip);
                }}
                
                document.addEventListener('mouseup', endDrag);
            }}

            function singleClick(e) {{
                if (!isDragging) {{
                    const index = parseInt(e.target.dataset.index);
                    toggleSquare(index);
                }}
            }}

            function startDrag(e) {{
                e.preventDefault();
                isDragging = true;
                const index = parseInt(e.target.dataset.index);
                
                // Determine if we're shading or unshading based on current state
                isShading = !shadedSquares.has(index);
                
                toggleSquare(index);
            }}

            function dragOver(e) {{
                if (isDragging) {{
                    const index = parseInt(e.target.dataset.index);
                    
                    if (isShading && !shadedSquares.has(index)) {{
                        toggleSquare(index);
                    }} else if (!isShading && shadedSquares.has(index)) {{
                        toggleSquare(index);
                    }}
                    
                    // Add hover effect
                    e.target.classList.add('hover');
                    setTimeout(() => e.target.classList.remove('hover'), 100);
                }}
            }}

            function endDrag() {{
                isDragging = false;
            }}

            function toggleSquare(index) {{
                const strip = document.querySelector(`[data-index="${{index}}"]`);
                
                if (shadedSquares.has(index)) {{
                    shadedSquares.delete(index);
                    strip.classList.remove('shaded');
                    strip.classList.add('unshaded');
                }} else {{
                    shadedSquares.add(index);
                    strip.classList.remove('unshaded');
                    strip.classList.add('shaded');
                }}
                
                updateCounter();
            }}

            function updateCounter() {{
                const counter = document.getElementById('counter');
                counter.textContent = `Shaded: ${{shadedSquares.size}} out of 10`;
            }}

            function clearAll() {{
                shadedSquares.clear();
                const strips = document.querySelectorAll('.strip');
                strips.forEach(strip => {{
                    strip.classList.remove('shaded');
                    strip.classList.add('unshaded');
                }});
                updateCounter();
            }}

            // Initialize the grid when page loads
            initGrid();
        </script>
    </body>
    </html>
    """

def create_hundredths_grid_html(target_numerator, target_denominator):
    """Create HTML/JavaScript for interactive hundredths grid"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .grid-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 10px;
                margin: 10px;
            }}
            .hundredths-grid {{
                display: grid;
                grid-template-columns: repeat(10, 35px);
                grid-template-rows: repeat(10, 35px);
                gap: 2px;
                border: 3px solid #333;
                border-radius: 8px;
                padding: 5px;
                background-color: #e0e0e0;
            }}
            .square {{
                width: 35px;
                height: 35px;
                cursor: pointer;
                user-select: none;
                transition: background-color 0.1s;
                border: 1px solid #666;
                border-radius: 2px;
                box-sizing: border-box;
            }}
            .square.shaded {{
                background-color: #2196F3;
                border-color: #1976D2;
            }}
            .square.unshaded {{
                background-color: white;
                border-color: #666;
            }}
            .square.hover {{
                background-color: #4CAF50 !important;
                border-color: #388E3C !important;
                transform: scale(1.05);
            }}
            .counter {{
                text-align: center;
                margin: 20px;
                font-size: 18px;
                font-weight: bold;
                color: #1565C0;
            }}
            .controls {{
                text-align: center;
                margin: 20px;
            }}
            .btn {{
                padding: 10px 20px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }}
            .btn-clear {{ 
                background-color: #f44336; 
                color: white; 
            }}
            .btn-clear:hover {{ 
                background-color: #da190b; 
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="grid-container">
            <div>
                <div class="hundredths-grid" id="hundredthsGrid">
                    <!-- Squares will be generated by JavaScript -->
                </div>
                <div class="counter" id="counter">Shaded: 0 out of 100</div>
                <div class="controls">
                    <button class="btn btn-clear" onclick="clearAll()">🧹 Clear All</button>
                </div>
                <div style="text-align: center; margin-top: 15px; color: #666; font-size: 14px;">
                    Click and drag to shade squares. Count your shaded squares and enter the number below.
                </div>
            </div>
        </div>

        <script>
            let shadedSquares = new Set();
            let isDragging = false;
            let isShading = true; // true for shading, false for unshading

            function initGrid() {{
                const grid = document.getElementById('hundredthsGrid');
                
                for (let i = 0; i < 100; i++) {{
                    const square = document.createElement('div');
                    square.className = 'square unshaded';
                    square.dataset.index = i;
                    
                    square.addEventListener('mousedown', startDrag);
                    square.addEventListener('mouseenter', dragOver);
                    square.addEventListener('mouseup', endDrag);
                    square.addEventListener('click', singleClick);
                    
                    grid.appendChild(square);
                }}
                
                document.addEventListener('mouseup', endDrag);
                document.addEventListener('selectstart', e => e.preventDefault());
            }}

            function singleClick(e) {{
                if (!isDragging) {{
                    const index = parseInt(e.target.dataset.index);
                    toggleSquare(index);
                }}
            }}

            function startDrag(e) {{
                e.preventDefault();
                isDragging = true;
                const index = parseInt(e.target.dataset.index);
                
                // Determine if we're shading or unshading based on current state
                isShading = !shadedSquares.has(index);
                
                toggleSquare(index);
            }}

            function dragOver(e) {{
                if (isDragging) {{
                    const index = parseInt(e.target.dataset.index);
                    
                    if (isShading && !shadedSquares.has(index)) {{
                        toggleSquare(index);
                    }} else if (!isShading && shadedSquares.has(index)) {{
                        toggleSquare(index);
                    }}
                    
                    // Add hover effect
                    e.target.classList.add('hover');
                    setTimeout(() => e.target.classList.remove('hover'), 150);
                }}
            }}

            function endDrag() {{
                isDragging = false;
            }}

            function toggleSquare(index) {{
                const square = document.querySelector(`[data-index="${{index}}"]`);
                
                if (shadedSquares.has(index)) {{
                    shadedSquares.delete(index);
                    square.classList.remove('shaded');
                    square.classList.add('unshaded');
                }} else {{
                    shadedSquares.add(index);
                    square.classList.remove('unshaded');
                    square.classList.add('shaded');
                }}
                
                updateCounter();
            }}

            function updateCounter() {{
                const counter = document.getElementById('counter');
                counter.textContent = `Shaded: ${{shadedSquares.size}} out of 100`;
            }}

            function clearAll() {{
                shadedSquares.clear();
                const squares = document.querySelectorAll('.square');
                squares.forEach(square => {{
                    square.classList.remove('shaded');
                    square.classList.add('unshaded');
                }});
                updateCounter();
            }}

            // Initialize the grid when page loads
            initGrid();
        </script>
    </body>
    </html>
    """

def show_model_df_feedback():
    """Display feedback for the modeling problem"""
    user_answer = st.session_state.get("model_df_user_answer", 0)
    correct_answer = st.session_state.get("model_df_answer")
    data = st.session_state.get("model_df_data", {})
    
    if correct_answer is None:
        return
    
    target_numerator = data.get("target_numerator", 0)
    target_denominator = data.get("target_denominator", 1)
    target_decimal = data.get("target_decimal", 0)
    
    is_correct = user_answer == correct_answer
    
    st.markdown("---")
    st.markdown("### 📋 Results:")
    
    if is_correct:
        st.success(f"🎉 **Perfect!** You shaded exactly {target_numerator} out of {target_denominator}!")
        
        # Show equivalent representations
        st.info(f"**Equivalent representations:** {target_numerator}/{target_denominator} = {target_decimal}")
        
        # Increase difficulty
        old_difficulty = st.session_state.model_df_difficulty
        st.session_state.model_df_difficulty = min(
            st.session_state.model_df_difficulty + 1, 5
        )
        
        if st.session_state.model_df_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered modeling decimals and fractions!**")
        elif old_difficulty < st.session_state.model_df_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.model_df_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite.** You shaded {user_answer} but needed to shade {target_numerator}.")
        
        # Provide specific guidance
        difference = abs(user_answer - target_numerator)
        if user_answer > target_numerator:
            st.warning(f"💡 **Hint:** You shaded {difference} too many. Try the Clear All button and shade exactly {target_numerator}.")
        elif user_answer < target_numerator:
            st.warning(f"💡 **Hint:** You need {difference} more shaded squares/strips to reach {target_numerator}.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.model_df_difficulty
        st.session_state.model_df_difficulty = max(
            st.session_state.model_df_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.model_df_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.model_df_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_model_df_explanation(is_correct)
    
    # Next question button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Next Question", type="secondary", use_container_width=True):
            reset_model_df_state()
            st.rerun()

def show_model_df_explanation(correct=True):
    """Show detailed explanation"""
    data = st.session_state.get("model_df_data", {})
    user_answer = st.session_state.get("model_df_user_answer", 0)
    
    target_numerator = data.get("target_numerator", 0)
    target_denominator = data.get("target_denominator", 1)
    target_decimal = data.get("target_decimal", 0)
    grid_type = data.get("grid_type", "tenths")
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Understanding the Model:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if grid_type == "tenths":
            st.markdown(f"""
            ### **Tenths Model Explanation:**
            - **Total strips:** 10
            - **Each strip represents:** 1/10 = 0.1
            - **Target fraction:** {target_numerator}/10
            - **Target decimal:** {target_decimal}
            - **Strips to shade:** {target_numerator}
            
            ### **Your Work:**
            - **You shaded:** {user_answer} strips
            - **Fraction you modeled:** {user_answer}/10 = {user_answer/10}
            """)
        else:
            st.markdown(f"""
            ### **Hundredths Model Explanation:**
            - **Total squares:** 100 (10×10 grid)
            - **Each square represents:** 1/100 = 0.01
            - **Target fraction:** {target_numerator}/100
            - **Target decimal:** {target_decimal}
            - **Squares to shade:** {target_numerator}
            
            ### **Your Work:**
            - **You shaded:** {user_answer} squares
            - **Fraction you modeled:** {user_answer}/100 = {user_answer/100}
            """)
        
        # Show conversion tips
        st.markdown("### 🔄 **Fraction ↔ Decimal Conversion:**")
        if grid_type == "tenths":
            st.markdown(f"- **{target_numerator}/10** = {target_numerator} ÷ 10 = **{target_decimal}**")
        else:
            st.markdown(f"- **{target_numerator}/100** = {target_numerator} ÷ 100 = **{target_decimal}**")
        
        # Show equivalent fractions if applicable
        if grid_type == "hundredths" and target_numerator % 10 == 0:
            tenths_equivalent = target_numerator // 10
            st.markdown(f"### 🔗 **Equivalent Fraction:**")
            st.markdown(f"- **{target_numerator}/100** = **{tenths_equivalent}/10** (both equal {target_decimal})")

def reset_model_df_state():
    """Reset state for next problem"""
    st.session_state.current_model_df_problem = None
    st.session_state.model_df_answer = None
    st.session_state.model_df_feedback = False
    st.session_state.model_df_submitted = False
    st.session_state.model_df_data = {}
    st.session_state.user_shaded_count = 0
    
    # Clear any stored answers
    if "model_df_user_answer" in st.session_state:
        del st.session_state.model_df_user_answer