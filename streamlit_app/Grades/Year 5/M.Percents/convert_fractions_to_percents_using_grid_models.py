import streamlit as st
import random
import json

def run():
    """
    Main function to run the Convert Fractions to Percents practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/convert_fractions_to_percents_using_grid_models.py
    """
    # Initialize session state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.cells_needed = 0
        st.session_state.cells_shaded = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Convert Fractions to Percents Using Grid Models")
    st.markdown("*Click and drag to shade the grid, then convert to percent*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Tenths", 2: "Fifths & Twentieths", 3: "Complex Fractions"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
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
        ### How to Play:
        1. **Read the fraction** you need to shade
        2. **Click and drag** across cells to shade multiple cells at once
        3. **Click individual cells** to toggle them
        4. **Convert to percent** and enter your answer
        
        ### Tips for Success:
        - **Grid = 100 squares:** Perfect for percent conversion!
        - **Fraction to percent:** Multiply by 100
        - **Example:** 3/10 = 30/100 = 30%
        
        ### Difficulty Levels:
        - **🟢 Easy:** Fractions with denominator 10 (tenths)
        - **🟡 Medium:** Fractions with denominators 5, 20 (fifths, twentieths)
        - **🔴 Hard:** Fractions with denominators 25, 50, 4 (complex conversions)
        
        ### Quick Conversions:
        - **/10:** Multiply by 10 to get percent
        - **/5:** Multiply by 20 to get percent
        - **/20:** Multiply by 5 to get percent
        - **/4:** Multiply by 25 to get percent
        """)

def generate_new_question():
    """Generate a new fraction to percent question based on difficulty"""
    difficulty = st.session_state.fractions_difficulty
    
    # Define fractions by difficulty
    if difficulty == 1:  # Easy - tenths
        fractions = [
            (1, 10, 10), (2, 10, 20), (3, 10, 30), (4, 10, 40), 
            (5, 10, 50), (6, 10, 60), (7, 10, 70), (8, 10, 80), 
            (9, 10, 90)
        ]
    elif difficulty == 2:  # Medium - fifths and twentieths
        fractions = [
            (1, 5, 20), (2, 5, 40), (3, 5, 60), (4, 5, 80),
            (1, 20, 5), (3, 20, 15), (5, 20, 25), (7, 20, 35),
            (9, 20, 45), (11, 20, 55), (13, 20, 65), (15, 20, 75),
            (17, 20, 85), (19, 20, 95)
        ]
    else:  # Hard - quarters, twenty-fifths, fiftieths
        fractions = [
            (1, 4, 25), (3, 4, 75),
            (1, 25, 4), (2, 25, 8), (3, 25, 12), (4, 25, 16),
            (5, 25, 20), (6, 25, 24), (7, 25, 28), (8, 25, 32),
            (1, 50, 2), (3, 50, 6), (7, 50, 14), (9, 50, 18),
            (11, 50, 22), (13, 50, 26), (17, 50, 34), (19, 50, 38)
        ]
    
    # Select a random fraction
    numerator, denominator, percent = random.choice(fractions)
    cells_to_shade = (numerator * 100) // denominator
    
    st.session_state.question_data = {
        "numerator": numerator,
        "denominator": denominator,
        "fraction_str": f"{numerator}/{denominator}",
        "cells_needed": cells_to_shade
    }
    st.session_state.cells_needed = cells_to_shade
    st.session_state.correct_answer = percent
    st.session_state.current_question = f"Shade {numerator}/{denominator} of the grid."
    st.session_state.cells_shaded = 0

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    st.markdown("*Click and drag to shade.*")
    
    # Create placeholder for cell count
    cell_count_placeholder = st.empty()
    
    # Display initial progress
    update_progress(cell_count_placeholder)
    
    # Create interactive grid
    create_draggable_grid(cell_count_placeholder)
    
    # Clear button
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("🔄 Clear Grid", type="secondary"):
            st.session_state.cells_shaded = 0
            st.rerun()
    
    # Answer input section
    st.markdown("---")
    st.markdown(f"**What percent is equivalent to {data['fraction_str']}?**")
    
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.text_input(
                "Your answer:",
                key="percent_input",
                placeholder="Enter number only",
                label_visibility="collapsed"
            )
            st.markdown("**%**", unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def update_progress(placeholder):
    """Update the progress display"""
    cells_shaded = st.session_state.cells_shaded
    cells_needed = st.session_state.cells_needed
    
    with placeholder.container():
        if cells_shaded == cells_needed:
            st.success(f"✅ Perfect! You've shaded {cells_shaded}/{cells_needed} cells")
        elif cells_shaded < cells_needed:
            st.info(f"Cells shaded: {cells_shaded}/{cells_needed} (shade {cells_needed - cells_shaded} more)")
        else:
            st.warning(f"Too many! Cells shaded: {cells_shaded}/{cells_needed} (unshade {cells_shaded - cells_needed})")

def create_draggable_grid(cell_count_placeholder):
    """Create an interactive grid with drag functionality"""
    
    grid_html = f"""
    <div id="grid-container-wrapper">
        <style>
            #grid-container-wrapper {{
                text-align: center;
                margin: 20px 0;
            }}
            #fraction-grid {{
                display: inline-grid;
                grid-template-columns: repeat(10, 35px);
                grid-template-rows: repeat(10, 35px);
                gap: 0;
                border: 3px solid #333;
                background: white;
                cursor: crosshair;
                user-select: none;
                -webkit-user-select: none;
                -moz-user-select: none;
                -ms-user-select: none;
            }}
            .grid-cell {{
                width: 35px;
                height: 35px;
                border: 1px solid #ccc;
                background: white;
                transition: background-color 0.1s ease;
            }}
            .grid-cell.shaded {{
                background: #2196F3;
            }}
            .grid-cell.preview {{
                background: #90CAF9 !important;
            }}
            #grid-info {{
                text-align: center;
                margin: 10px 0;
                font-size: 14px;
                color: #666;
            }}
        </style>
        
        <div id="fraction-grid"></div>
        <div id="grid-info">Drag to shade • Click shaded cells to unshade</div>
        
        <script>
            (function() {{
                const GRID_SIZE = 10;
                let isMouseDown = false;
                let isShading = true;
                let startCell = null;
                let currentShadedCount = {st.session_state.cells_shaded};
                const grid = document.getElementById('fraction-grid');
                
                // Create grid
                for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++) {{
                    const cell = document.createElement('div');
                    cell.className = 'grid-cell';
                    cell.dataset.index = i;
                    cell.dataset.row = Math.floor(i / GRID_SIZE);
                    cell.dataset.col = i % GRID_SIZE;
                    grid.appendChild(cell);
                }}
                
                // Restore previous state if any
                if (currentShadedCount > 0) {{
                    const cells = grid.querySelectorAll('.grid-cell');
                    for (let i = 0; i < currentShadedCount && i < cells.length; i++) {{
                        cells[i].classList.add('shaded');
                    }}
                }}
                
                // Get all cells in rectangle between two cells
                function getCellsInRectangle(cell1, cell2) {{
                    if (!cell1 || !cell2) return [];
                    
                    const r1 = parseInt(cell1.dataset.row);
                    const c1 = parseInt(cell1.dataset.col);
                    const r2 = parseInt(cell2.dataset.row);
                    const c2 = parseInt(cell2.dataset.col);
                    
                    const minR = Math.min(r1, r2);
                    const maxR = Math.max(r1, r2);
                    const minC = Math.min(c1, c2);
                    const maxC = Math.max(c1, c2);
                    
                    const cells = [];
                    for (let r = minR; r <= maxR; r++) {{
                        for (let c = minC; c <= maxC; c++) {{
                            const index = r * GRID_SIZE + c;
                            const cell = grid.querySelector(`[data-index="${{index}}"]`);
                            if (cell) cells.push(cell);
                        }}
                    }}
                    return cells;
                }}
                
                // Clear preview
                function clearPreview() {{
                    grid.querySelectorAll('.preview').forEach(cell => {{
                        cell.classList.remove('preview');
                    }});
                }}
                
                // Update cells
                function updateCells(cells, shade) {{
                    cells.forEach(cell => {{
                        if (shade && !cell.classList.contains('shaded')) {{
                            cell.classList.add('shaded');
                            currentShadedCount++;
                        }} else if (!shade && cell.classList.contains('shaded')) {{
                            cell.classList.remove('shaded');
                            currentShadedCount--;
                        }}
                    }});
                    
                    // Update Streamlit
                    updateStreamlit();
                }}
                
                // Update Streamlit state
                function updateStreamlit() {{
                    // Create a custom event to communicate with Streamlit
                    window.parent.postMessage({{
                        type: 'UPDATE_CELLS',
                        count: currentShadedCount
                    }}, '*');
                }}
                
                // Mouse events
                grid.addEventListener('mousedown', (e) => {{
                    if (e.target.classList.contains('grid-cell')) {{
                        e.preventDefault();
                        isMouseDown = true;
                        startCell = e.target;
                        isShading = !e.target.classList.contains('shaded');
                        updateCells([e.target], isShading);
                    }}
                }});
                
                grid.addEventListener('mousemove', (e) => {{
                    if (isMouseDown && e.target.classList.contains('grid-cell')) {{
                        clearPreview();
                        const cells = getCellsInRectangle(startCell, e.target);
                        cells.forEach(cell => {{
                            if (isShading && !cell.classList.contains('shaded')) {{
                                cell.classList.add('preview');
                            }} else if (!isShading && cell.classList.contains('shaded')) {{
                                cell.classList.add('preview');
                            }}
                        }});
                    }}
                }});
                
                grid.addEventListener('mouseup', (e) => {{
                    if (isMouseDown) {{
                        clearPreview();
                        const endCell = e.target.classList.contains('grid-cell') ? e.target : startCell;
                        const cells = getCellsInRectangle(startCell, endCell);
                        updateCells(cells, isShading);
                        isMouseDown = false;
                        startCell = null;
                    }}
                }});
                
                // Global mouseup
                document.addEventListener('mouseup', () => {{
                    if (isMouseDown) {{
                        clearPreview();
                        isMouseDown = false;
                        startCell = null;
                    }}
                }});
                
                // Touch support
                let touchStartCell = null;
                
                grid.addEventListener('touchstart', (e) => {{
                    const touch = e.touches[0];
                    const element = document.elementFromPoint(touch.clientX, touch.clientY);
                    if (element && element.classList.contains('grid-cell')) {{
                        e.preventDefault();
                        touchStartCell = element;
                        isShading = !element.classList.contains('shaded');
                    }}
                }});
                
                grid.addEventListener('touchmove', (e) => {{
                    e.preventDefault();
                    const touch = e.touches[0];
                    const element = document.elementFromPoint(touch.clientX, touch.clientY);
                    if (element && element.classList.contains('grid-cell') && touchStartCell) {{
                        clearPreview();
                        const cells = getCellsInRectangle(touchStartCell, element);
                        cells.forEach(cell => {{
                            if (isShading && !cell.classList.contains('shaded')) {{
                                cell.classList.add('preview');
                            }} else if (!isShading && cell.classList.contains('shaded')) {{
                                cell.classList.add('preview');
                            }}
                        }});
                    }}
                }});
                
                grid.addEventListener('touchend', (e) => {{
                    if (touchStartCell) {{
                        clearPreview();
                        const touch = e.changedTouches[0];
                        const element = document.elementFromPoint(touch.clientX, touch.clientY);
                        const endCell = element && element.classList.contains('grid-cell') ? element : touchStartCell;
                        const cells = getCellsInRectangle(touchStartCell, endCell);
                        updateCells(cells, isShading);
                        touchStartCell = null;
                    }}
                }});
                
                // Listen for messages to update count
                window.addEventListener('message', (e) => {{
                    if (e.data && e.data.type === 'UPDATE_CELLS') {{
                        currentShadedCount = e.data.count;
                    }}
                }});
                
                // Initial update
                updateStreamlit();
            }})();
        </script>
    </div>
    """
    
    # Display the grid
    st.components.v1.html(grid_html, height=450)
    
    # JavaScript to handle updates from the grid
    st.markdown("""
    <script>
        window.addEventListener('message', (e) => {
            if (e.data && e.data.type === 'UPDATE_CELLS') {
                // Store the count for retrieval
                window.cellCount = e.data.count;
            }
        });
    </script>
    """, unsafe_allow_html=True)

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer.strip()
    correct_answer = st.session_state.correct_answer
    
    # Parse user answer
    try:
        user_percent = int(user_answer)
        valid_format = True
    except:
        valid_format = False
        st.error("❌ Please enter a valid number (without the % sign).")
    
    if valid_format:
        if user_percent == correct_answer:
            st.success("🎉 **Excellent! That's correct!**")
            
            # Increase difficulty
            old_difficulty = st.session_state.fractions_difficulty
            st.session_state.fractions_difficulty = min(
                st.session_state.fractions_difficulty + 1, 3
            )
            
            if st.session_state.fractions_difficulty > old_difficulty:
                st.info(f"⬆️ **Difficulty increased! Now working with more complex fractions.**")
            elif st.session_state.fractions_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've mastered fraction to percent conversion!**")
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}%**.")
            
            # Decrease difficulty
            old_difficulty = st.session_state.fractions_difficulty
            st.session_state.fractions_difficulty = max(
                st.session_state.fractions_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.fractions_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to simpler fractions. Keep practicing!**")
            
            # Show explanation
            show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Converting {data['fraction_str']} to a percentage:
        
        **Method 1: Using the grid**
        - The grid has 10×10 = 100 squares
        - {data['fraction_str']} of 100 = {data['cells_needed']} squares
        - {data['cells_needed']} out of 100 = **{correct_answer}%**
        
        **Method 2: Mathematical conversion**
        - To convert a fraction to percent, multiply by 100
        - {data['fraction_str']} × 100 = {data['numerator']} × 100 ÷ {data['denominator']}
        - = {data['numerator'] * 100} ÷ {data['denominator']}
        - = **{correct_answer}%**
        
        **Quick tip for denominator {data['denominator']}:**
        """)
        
        if data['denominator'] == 10:
            st.markdown("- For tenths (/10): Just multiply numerator by 10")
        elif data['denominator'] == 5:
            st.markdown("- For fifths (/5): Multiply numerator by 20")
        elif data['denominator'] == 20:
            st.markdown("- For twentieths (/20): Multiply numerator by 5")
        elif data['denominator'] == 4:
            st.markdown("- For quarters (/4): Multiply numerator by 25")
        elif data['denominator'] == 25:
            st.markdown("- For twenty-fifths (/25): Multiply numerator by 4")
        elif data['denominator'] == 50:
            st.markdown("- For fiftieths (/50): Multiply numerator by 2")
        
        st.markdown(f"""
        
        **Remember:** Percent means "out of 100", so the 10×10 grid 
        makes it easy to visualize percentages!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.cells_needed = 0
    st.session_state.cells_shaded = 0
    if "user_answer" in st.session_state:
        del st.session_state.user_answer