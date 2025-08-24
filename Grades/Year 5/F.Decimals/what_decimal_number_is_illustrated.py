import streamlit as st
import random
import math

def run():
    """
    Main function to run the What Decimal Number is Illustrated activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/F. Decimals/what_decimal_number_is_illustrated.py
    """
    # Initialize session state
    if "decimal_illus_difficulty" not in st.session_state:
        st.session_state.decimal_illus_difficulty = 1
    
    if "current_decimal_illus_problem" not in st.session_state:
        st.session_state.current_decimal_illus_problem = None
        st.session_state.decimal_illus_answer = None
        st.session_state.decimal_illus_feedback = False
        st.session_state.decimal_illus_submitted = False
        st.session_state.decimal_illus_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > F. Decimals**")
    st.title("🔍 What Decimal Number is Illustrated?")
    st.markdown("*Look at the visual representation and write the decimal number*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimal_illus_difficulty
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
        
        # Add debug toggle (hidden by default)
        if st.button("🔧", help="Debug Mode"):
            st.session_state.debug_mode = not st.session_state.get("debug_mode", False)
    
    # Generate new question if needed
    if st.session_state.current_decimal_illus_problem is None:
        generate_decimal_illus_problem()
    
    # Display current question
    display_decimal_illus_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Understanding Decimal Representations**", expanded=False):
        st.markdown("""
        ### How to Read Visual Decimal Representations:
        
        #### **Tenths (0.1) - Vertical Strips:**
        - **One whole** is divided into **10 equal strips**
        - **Each strip = 0.1** (one tenth)
        - **Count the shaded strips** to find the decimal
        
        **Example:** 7 shaded strips = **0.7**
        
        #### **Hundredths (0.01) - Grid Squares:**
        - **One whole** is divided into **100 small squares** (10×10 grid)
        - **Each square = 0.01** (one hundredth)
        - **Count the shaded squares** to find the decimal
        
        **Example:** 23 shaded squares = **0.23**
        
        #### **Mixed Numbers:**
        - **Whole parts** + **decimal parts**
        - **Count whole units first**, then decimal parts
        
        **Example:** 1 whole + 4 tenths = **1.4**
        
        ### Visual Patterns to Look For:
        
        #### **Tenths Representations:**
        - **Vertical bars/strips** (Green = shaded, White = unshaded)
        - **10 equal sections** in a rectangle
        - **Each section = 0.1**
        
        #### **Hundredths Representations:**
        - **10×10 grids** (Blue = shaded, White = unshaded)
        - **100 small squares total**
        - **Each square = 0.01**
        - **10 squares in a row = 0.1**
        
        ### Quick Counting Tips:
        
        #### **For Tenths:**
        - Count shaded strips: 1, 2, 3, 4, 5...
        - Convert to decimal: 5 strips = 0.5
        
        #### **For Hundredths:**
        - **Count by rows first** (easier): 1 row = 0.1
        - **Then count individual squares**: each = 0.01
        - **Example:** 2 full rows + 3 squares = 0.2 + 0.03 = 0.23
        
        ### Common Decimal Values:
        - **0.1** = 1 tenth (1 strip, 10 squares)
        - **0.5** = 5 tenths (5 strips, 50 squares) = half
        - **0.25** = 25 hundredths (25 squares) = quarter
        - **0.75** = 75 hundredths (75 squares) = three quarters
        
        ### Writing Decimal Answers:
        - **Use decimal point**: 0.7 (not 7/10)
        - **Include zero before decimal**: 0.5 (not .5)
        - **Don't add unnecessary zeros**: 0.3 (not 0.30) unless specified
        - **For whole numbers**: 1.2, 2.7, etc.
        """)

def generate_decimal_illus_problem():
    """Generate unlimited decimal illustration problems using algorithmic generation"""
    difficulty = st.session_state.decimal_illus_difficulty
    
    if difficulty == 1:
        # Level 1: Simple tenths only (0.1 to 0.9)
        representation_type = "tenths"
        decimal_value = random.randint(1, 9) / 10
        
    elif difficulty == 2:
        # Level 2: More tenths + simple hundredths (multiples of 0.05)
        representation_type = random.choice(["tenths", "hundredths_simple"])
        
        if representation_type == "tenths":
            decimal_value = random.randint(1, 9) / 10
        else:  # hundredths_simple
            # Use multiples of 5 hundredths for easier counting
            hundredths = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95])
            decimal_value = hundredths / 100
    
    elif difficulty == 3:
        # Level 3: All hundredths + simple mixed numbers (tenths only)
        representation_type = random.choice(["hundredths", "mixed_tenths"])
        
        if representation_type == "hundredths":
            hundredths = random.randint(1, 99)
            decimal_value = hundredths / 100
        else:  # mixed_tenths
            # Simple mixed numbers with tenths only
            whole_part = random.randint(1, 3)
            tenths = random.randint(1, 9)
            decimal_value = whole_part + (tenths / 10)
    
    elif difficulty == 4:
        # Level 4: Complex hundredths + mixed numbers with hundredths/tenths
        representation_type = random.choice(["hundredths", "mixed_hundredths", "mixed_tenths"])
        
        if representation_type == "hundredths":
            hundredths = random.randint(1, 99)
            decimal_value = hundredths / 100
        elif representation_type == "mixed_hundredths":
            # Mixed with hundredths - will show hundredths grid
            whole_part = random.randint(1, 2)
            hundredths = random.randint(1, 99)
            decimal_value = whole_part + (hundredths / 100)
        else:  # mixed_tenths
            # Mixed with tenths - will show tenths strips, so use tenths only
            whole_part = random.randint(1, 4)
            tenths = random.randint(1, 9)
            decimal_value = whole_part + (tenths / 10)
    
    else:  # difficulty == 5
        # Level 5: All types including complex mixed numbers
        representation_type = random.choice(["hundredths", "mixed_hundredths", "mixed_tenths", "mixed_complex"])
        
        if representation_type == "hundredths":
            hundredths = random.randint(1, 99)
            decimal_value = hundredths / 100
        elif representation_type == "mixed_hundredths":
            # Mixed with hundredths - will show hundredths grid
            whole_part = random.randint(1, 3)
            hundredths = random.randint(1, 99)
            decimal_value = whole_part + (hundredths / 100)
        elif representation_type == "mixed_tenths":
            # Mixed with tenths - will show tenths strips
            whole_part = random.randint(2, 5)
            tenths = random.randint(1, 9)
            decimal_value = whole_part + (tenths / 10)
        else:  # mixed_complex - large mixed numbers with hundredths
            whole_part = random.randint(3, 6)
            hundredths = random.randint(1, 99)
            decimal_value = whole_part + (hundredths / 100)
    
    # Round to avoid floating point precision issues
    decimal_value = round(decimal_value, 2)
    
    # Validation: ensure the problem makes sense
    whole_part = int(decimal_value)
    decimal_part = decimal_value - whole_part
    
    # For pure decimal problems, there should be no whole part
    if representation_type in ["tenths", "hundredths", "hundredths_simple"]:
        if whole_part > 0:
            # This shouldn't happen - regenerate with just decimal part
            decimal_value = decimal_part
    
    # For mixed problems, there should be a whole part
    elif representation_type.startswith("mixed"):
        if whole_part == 0:
            # Add at least 1 whole part for mixed number problems
            if representation_type in ["mixed_hundredths", "mixed_complex"]:
                # Keep hundredths precision
                decimal_value = 1 + decimal_part
            else:
                # Round to tenths for tenths-based mixed problems
                tenths = round(decimal_part * 10)
                decimal_value = 1 + (tenths / 10)
    
    st.session_state.decimal_illus_data = {
        "decimal_value": decimal_value,
        "representation_type": representation_type
    }
    st.session_state.decimal_illus_answer = decimal_value
    st.session_state.current_decimal_illus_problem = "What decimal number is illustrated?"

def display_decimal_illus_problem():
    """Display the current decimal illustration problem with visual representation"""
    data = st.session_state.decimal_illus_data
    decimal_value = data["decimal_value"]
    representation_type = data["representation_type"]
    
    # Validation check: ensure visual matches expected answer
    whole_part = int(decimal_value)
    decimal_part = decimal_value - whole_part
    
    # For pure decimal representations, whole_part should be 0
    if representation_type in ["tenths", "hundredths", "hundredths_simple"] and whole_part > 0:
        st.error(f"⚠️ **Problem Generation Error**: Pure decimal problem has whole part {whole_part}. Regenerating...")
        st.session_state.current_decimal_illus_problem = None
        st.rerun()
        return
    
    # For mixed number representations, validate decimal precision matches visual type
    if representation_type.startswith("mixed"):
        if representation_type in ["mixed_hundredths", "mixed_complex"]:
            # Should have hundredths precision - this is OK
            pass
        else:  # mixed_tenths and other tenths-based mixed
            # Should only have tenths precision
            expected_decimal = round(decimal_part * 10) / 10
            if abs(decimal_part - expected_decimal) > 0.001:
                st.error(f"⚠️ **Problem Generation Error**: Tenths mixed problem has hundredths precision. Regenerating...")
                if st.session_state.get("debug_mode", False):
                    st.warning(f"**Debug**: Expected {expected_decimal} for tenths but got {decimal_part}")
                st.session_state.current_decimal_illus_problem = None
                st.rerun()
                return
    
    # Display the question
    st.markdown("### 🎯 Question:")
    st.markdown("""
    <div style="
        background-color: #f0f8ff; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #2c3e50;
    ">
        What decimal number is illustrated?
    </div>
    """, unsafe_allow_html=True)
    
    # Generate and display the visual representation
    generate_and_display_visual(decimal_value, representation_type)
    
    # Create input field with form
    with st.form("decimal_illus_form", clear_on_submit=False):
        # Center the input field
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Text input for answer
            user_input = st.text_input(
                "Enter the decimal number:",
                key="decimal_illus_input",
                placeholder="e.g., 0.7 or 1.25",
                label_visibility="collapsed",
                help="Enter the decimal number shown in the illustration"
            )
            
            # Add some spacing
            st.markdown("")
            
            # Submit button
            submit_button = st.form_submit_button(
                "✅ Submit", 
                type="primary", 
                use_container_width=True
            )
        
        # Handle form submission
        if submit_button:
            if user_input.strip():
                try:
                    user_answer = float(user_input.strip())
                    st.session_state.decimal_illus_user_answer = user_answer
                    st.session_state.decimal_illus_feedback = True
                    st.session_state.decimal_illus_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("Please enter a valid decimal number!")
            else:
                st.error("Please enter an answer!")
    
    # Show feedback and next button
    handle_decimal_illus_feedback()

def generate_and_display_visual(decimal_value, representation_type):
    """Generate and display visual representation using Streamlit containers"""
    
    # Determine number of wholes and decimal part
    whole_part = int(decimal_value)
    decimal_part = decimal_value - whole_part
    
    # Debug info (can be enabled for troubleshooting)
    if st.session_state.get("debug_mode", False):
        st.info(f"🔧 **Debug**: decimal_value={decimal_value}, type={representation_type}, whole={whole_part}, decimal={decimal_part}")
        
        # Additional debug for mixed numbers
        if representation_type.startswith("mixed"):
            if representation_type in ["mixed_hundredths", "mixed_complex"]:
                expected_display = f"{whole_part} + {round(decimal_part * 100)} hundredths = {decimal_value}"
            else:
                expected_display = f"{whole_part} + {round(decimal_part * 10)} tenths = {decimal_value}"
            st.info(f"🔧 **Expected Display**: {expected_display}")
    
    # Create a centered container for the visual
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Pure decimal representations (no whole numbers)
            if representation_type == "tenths":
                display_tenths_visual(decimal_part)
            elif representation_type in ["hundredths", "hundredths_simple"]:
                display_hundredths_visual(decimal_part)
            # Mixed number representations (whole numbers + decimals)
            elif representation_type.startswith("mixed"):
                display_mixed_visual(whole_part, decimal_part, representation_type)
            else:
                # Fallback - if unsure, check if there are whole parts
                if whole_part > 0:
                    display_mixed_visual(whole_part, decimal_part, representation_type)
                else:
                    display_hundredths_visual(decimal_part)

def display_tenths_visual(decimal_part):
    """Display tenths representation using emoji-based visualization"""
    shaded_tenths = round(decimal_part * 10)
    
    st.markdown("**Tenths Grid (Each strip = 0.1):**")
    
    # Create visual representation using colored squares and text
    visual_row = ""
    for i in range(10):
        if i < shaded_tenths:
            visual_row += "🟩"  # Green square for shaded
        else:
            visual_row += "⬜"  # White square for unshaded
        visual_row += " "
    
    st.markdown(f"""
    <div style="
        text-align: center; 
        font-size: 24px; 
        padding: 20px; 
        background-color: #f9f9f9; 
        border: 2px solid #333; 
        border-radius: 10px;
        margin: 10px 0;
    ">
        {visual_row}
    </div>
    """, unsafe_allow_html=True)
    
    # Add numbers below
    number_row = ""
    for i in range(10):
        number_row += f"{i+1:2d} "
    
    st.markdown(f"""
    <div style="
        text-align: center; 
        font-family: monospace; 
        font-size: 12px; 
        color: #666;
        margin-top: 5px;
    ">
        {number_row}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**🟩 Shaded strips: {shaded_tenths} out of 10**")
    calculated_value = round(shaded_tenths / 10, 1)
    st.markdown(f"**Each strip = 0.1, so {shaded_tenths} strips = {shaded_tenths}/10 = {calculated_value}**")

def display_hundredths_visual(decimal_part):
    """Display hundredths representation using emoji-based 10x10 grid"""
    shaded_hundredths = round(decimal_part * 100)
    
    st.markdown("**Hundredths Grid (Each square = 0.01):**")
    
    # Create 10x10 grid representation
    grid_html = """
    <div style="
        text-align: center; 
        font-size: 16px; 
        padding: 20px; 
        background-color: #f9f9f9; 
        border: 2px solid #333; 
        border-radius: 10px;
        margin: 10px 0;
        line-height: 1.2;
    ">
    """
    
    square_count = 0
    for row in range(10):
        row_content = ""
        for col in range(10):
            square_count += 1
            if square_count <= shaded_hundredths:
                row_content += "🟦"  # Blue square for shaded
            else:
                row_content += "⬜"  # White square for unshaded
            row_content += " "
        
        grid_html += f"<div>{row_content}</div>"
    
    grid_html += "</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)
    
    st.markdown(f"**🟦 Shaded squares: {shaded_hundredths} out of 100**")
    calculated_value = round(shaded_hundredths / 100, 2)
    st.markdown(f"**Each square = 0.01, so {shaded_hundredths} squares = {shaded_hundredths}/100 = {calculated_value}**")

def display_mixed_visual(whole_part, decimal_part, representation_type):
    """Display mixed number representation"""
    st.markdown("**Mixed Number Representation:**")
    
    # Display whole parts
    if whole_part > 0:
        st.markdown(f"**Whole units: {whole_part}**")
        
        whole_visual = ""
        for i in range(whole_part):
            whole_visual += "🟫 "  # Brown squares for whole units
        
        st.markdown(f"""
        <div style="
            text-align: center; 
            font-size: 48px; 
            padding: 15px; 
            background-color: #f0f8f0; 
            border: 2px solid #4CAF50; 
            border-radius: 10px;
            margin: 10px 0;
        ">
            {whole_visual}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**🟫 Each brown square = 1 whole unit**")
    
    # Display decimal part based on the specific representation type
    if decimal_part > 0:
        st.markdown("**Plus decimal part:**")
        
        # Determine whether to show tenths or hundredths based on representation type
        if representation_type in ["mixed_hundredths", "mixed_complex"]:
            # Show hundredths grid for these types
            display_hundredths_visual(decimal_part)
        else:
            # Show tenths strips for mixed_tenths and other mixed types
            display_tenths_visual(decimal_part)

def handle_decimal_illus_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("decimal_illus_feedback", False):
        show_decimal_illus_feedback()
        
        # Show Next Question button immediately after feedback
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_decimal_illus_state()
                st.rerun()

def show_decimal_illus_feedback():
    """Display feedback for the decimal illustration problem"""
    user_answer = st.session_state.get("decimal_illus_user_answer")
    correct_answer = st.session_state.get("decimal_illus_answer")
    data = st.session_state.get("decimal_illus_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    decimal_value = data["decimal_value"]
    representation_type = data["representation_type"]
    
    # Calculate whole and decimal parts for validation
    whole_part = int(correct_answer)
    decimal_part = correct_answer - whole_part
    
    # Additional validation: For mixed numbers, ensure precision matches visual type
    if representation_type.startswith("mixed"):
        if representation_type in ["mixed_hundredths", "mixed_complex"]:
            # Hundredths-based mixed numbers - keep full precision
            pass  
        else:  # mixed_tenths and other tenths-based mixed
            # Tenths-based mixed numbers - should only have tenths precision
            expected_answer = whole_part + (round(decimal_part * 10) / 10)
            if abs(correct_answer - expected_answer) > 0.001:
                st.error("🐛 **Bug detected!** Tenths visual doesn't match hundredths answer. Correcting...")
                correct_answer = expected_answer
                st.session_state.decimal_illus_answer = correct_answer  # Fix the stored answer
                
                if st.session_state.get("debug_mode", False):
                    st.warning(f"**Debug**: Fixed answer from {decimal_value} to {correct_answer}")
    
    # For pure decimal problems, if correct_answer > 1 but representation shows only decimal part
    elif representation_type in ["tenths", "hundredths", "hundredths_simple"] and whole_part > 0:
        # This is the bug! The visual shows only decimal part but answer includes whole part
        st.error("🐛 **Bug detected!** Visual shows decimal only but answer includes whole number. Using visual value instead.")
        correct_answer = decimal_part
        st.session_state.decimal_illus_answer = correct_answer  # Fix the stored answer
        
        if st.session_state.get("debug_mode", False):
            st.warning(f"**Debug**: Fixed answer from {decimal_value} to {correct_answer}")
    
    # Check if answers match (allowing for small floating point differences)
    is_correct = abs(user_answer - correct_answer) < 0.001
    
    if is_correct:
        st.success(f"🎉 **Excellent!** The decimal number is {correct_answer}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.decimal_illus_difficulty
        st.session_state.decimal_illus_difficulty = min(
            st.session_state.decimal_illus_difficulty + 1, 5
        )
        
        if st.session_state.decimal_illus_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered reading decimal illustrations!**")
        elif old_difficulty < st.session_state.decimal_illus_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.decimal_illus_difficulty}**")
        
        show_decimal_illus_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** The correct decimal number is **{correct_answer}**.")
        
        # Provide specific hints
        if user_answer > correct_answer:
            st.warning("💡 **Hint:** Your answer is too high. Count the shaded parts more carefully.")
        elif user_answer < correct_answer:
            st.warning("💡 **Hint:** Your answer is too low. Make sure you counted all the shaded parts.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.decimal_illus_difficulty
        st.session_state.decimal_illus_difficulty = max(
            st.session_state.decimal_illus_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimal_illus_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.decimal_illus_difficulty}. Keep practicing!**")
        
        show_decimal_illus_explanation(correct=False)

def show_decimal_illus_explanation(correct=True):
    """Show explanation for the decimal illustration problem"""
    data = st.session_state.get("decimal_illus_data", {})
    correct_answer = st.session_state.get("decimal_illus_answer")
    user_answer = st.session_state.get("decimal_illus_user_answer")
    
    if not data or correct_answer is None:
        return
        
    decimal_value = data["decimal_value"]
    representation_type = data["representation_type"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 How to Read This Illustration:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        whole_part = int(decimal_value)
        decimal_part = decimal_value - whole_part
        
        st.markdown(f"### Correct Answer: **{correct_answer}**")
        
        if representation_type == "tenths":
            shaded_tenths = round(decimal_part * 10)
            st.markdown(f"""
            ### This is a **Tenths** representation:
            - **Total strips:** 10
            - **Each strip represents:** 0.1 (one tenth)
            - **Shaded strips (🟩):** {shaded_tenths}
            - **Calculation:** {shaded_tenths} × 0.1 = **{decimal_part}**
            """)
            
        elif representation_type.startswith("hundredths"):
            shaded_hundredths = round(decimal_part * 100)
            st.markdown(f"""
            ### This is a **Hundredths** representation:
            - **Total squares:** 100 (10×10 grid)
            - **Each square represents:** 0.01 (one hundredth)
            - **Shaded squares (🟦):** {shaded_hundredths}
            - **Calculation:** {shaded_hundredths} × 0.01 = **{decimal_part}**
            
            #### Quick counting tip:
            - **Each full row** = 10 squares = 0.1
            - **Full rows shaded:** {shaded_hundredths // 10}
            - **Extra squares:** {shaded_hundredths % 10}
            - **Total:** {shaded_hundredths // 10} × 0.1 + {shaded_hundredths % 10} × 0.01 = {decimal_part}
            """)
            
        elif representation_type.startswith("mixed"):
            if representation_type in ["mixed_hundredths", "mixed_complex"]:
                shaded_hundredths = round(decimal_part * 100)
                st.markdown(f"""
                ### This is a **Mixed Number** with hundredths:
                - **Whole parts (🟫):** {whole_part} (completely shaded units)
                - **Decimal part:** {decimal_part} (from the hundredths grid)
                - **Grid squares shaded (🟦):** {shaded_hundredths} out of 100
                - **Calculation:** {whole_part} + {decimal_part} = **{decimal_value}**
                """)
            else:  # mixed_tenths and other tenths-based mixed
                shaded_tenths = round(decimal_part * 10)
                st.markdown(f"""
                ### This is a **Mixed Number** with tenths:
                - **Whole parts (🟫):** {whole_part} (completely shaded units)
                - **Decimal part:** {decimal_part} (from the tenths strips)
                - **Strips shaded (🟩):** {shaded_tenths} out of 10
                - **Calculation:** {whole_part} + {decimal_part} = **{decimal_value}**
                """)
        
        # Show place value breakdown
        st.markdown("### 📊 Place Value Breakdown:")
        if whole_part > 0:
            st.markdown(f"- **Ones place:** {whole_part}")
        
        if decimal_part >= 0.1:
            tenths = int(decimal_part * 10) % 10
            st.markdown(f"- **Tenths place:** {tenths}")
        
        if decimal_part != round(decimal_part, 1):  # Has hundredths
            hundredths = int(decimal_part * 100) % 10
            st.markdown(f"- **Hundredths place:** {hundredths}")
        
        # Common mistake analysis
        if not correct and user_answer is not None:
            st.markdown(f"### ❌ Why {user_answer} is incorrect:")
            
            user_whole = int(user_answer)
            user_decimal = user_answer - user_whole
            
            if user_whole != whole_part:
                st.markdown(f"- **Whole parts:** You counted {user_whole}, but there are {whole_part}")
            
            if abs(user_decimal - decimal_part) > 0.001:
                if representation_type in ["tenths", "mixed_tenths"]:
                    user_tenths = round(user_decimal * 10)
                    correct_tenths = round(decimal_part * 10)
                    st.markdown(f"- **Decimal part:** You counted {user_tenths} tenths, but there are {correct_tenths} tenths")
                else:
                    user_hundredths = round(user_decimal * 100)
                    correct_hundredths = round(decimal_part * 100)
                    st.markdown(f"- **Decimal part:** You counted {user_hundredths} hundredths, but there are {correct_hundredths} hundredths")

def reset_decimal_illus_state():
    """Reset the state for next problem"""
    st.session_state.current_decimal_illus_problem = None
    st.session_state.decimal_illus_answer = None
    st.session_state.decimal_illus_feedback = False
    st.session_state.decimal_illus_submitted = False
    st.session_state.decimal_illus_data = {}
    
    if "decimal_illus_user_answer" in st.session_state:
        del st.session_state.decimal_illus_user_answer