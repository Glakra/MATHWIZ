import streamlit as st
import random

def run():
    """
    Main function to run the Lattice Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 4/D. Multiplication/lattice_multiplication.py
    """
    # Initialize session state for difficulty and game state
    if "lattice_difficulty" not in st.session_state:
        st.session_state.lattice_difficulty = 1  # Start with level 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.diagonal_inputs = [None, None, None, None]
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 4 > D. Multiplication**")
    st.title("🔢 Lattice Multiplication")
    st.markdown("*Use the lattice method with diagonal sums to multiply*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.lattice_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Easy Start (×10s and simple)",
            2: "Building Up (×20s-×30s)",
            3: "Standard Practice (×40s-×60s)",
            4: "Getting Harder (×70s-×90s)",
            5: "Expert Challenge (large numbers)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Advanced')}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
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
    with st.expander("💡 **Instructions & Lattice Method Guide**", expanded=False):
        st.markdown("""
        ### How the Lattice Method Works:
        
        The **lattice method** uses a grid with diagonal lines to multiply numbers:
        
        #### Example: 23 × 45
        
        **Step 1:** Create a grid
        - Put **23** across the top (2, 3)
        - Put **45** down the side (4, 5)
        - Draw diagonal lines in each cell
        
        **Step 2:** Fill each cell
        ```
          2   3
        4|08|12|
         |/ |/ |
        5|10|15|
        ```
        - **2 × 4 = 08** (0 top, 8 bottom)
        - **3 × 4 = 12** (1 top, 2 bottom)
        - **2 × 5 = 10** (1 top, 0 bottom)
        - **3 × 5 = 15** (1 top, 5 bottom)
        
        **Step 3:** Add diagonals (from right to left)
        - **Right diagonal:** 5
        - **Next diagonal:** 2 + 0 + 1 = 3
        - **Next diagonal:** 1 + 1 + 1 = 3
        - **Left diagonal:** 0
        
        **Step 4:** Read the answer
        - **0335** but carry over: **1035**
        - So **23 × 45 = 1035**
        
        ### Why This Method Works:
        - **Visual:** Shows place values clearly
        - **Organized:** Each multiplication has its own cell
        - **Systematic:** Diagonal addition handles carrying automatically
        - **Reliable:** Reduces mental math errors
        
        ### Tips:
        - **Fill cells carefully** - tens digit on top, ones on bottom
        - **Add diagonals from right to left** - this handles place values
        - **Carry over** when diagonal sums are ≥ 10
        - **Check your work** by estimating first
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Easy start (×10s and simple)
        - **🟡 Level 2:** Building up (×20s-×30s)
        - **🟠 Level 3:** Standard practice (×40s-×60s)
        - **🔴 Level 4:** Getting harder (×70s-×90s)
        - **🔴 Level 5:** Expert challenge (large numbers)
        """)

def generate_new_question():
    """Generate a new lattice multiplication question based on difficulty"""
    difficulty = st.session_state.lattice_difficulty
    
    if difficulty == 1:
        # Level 1: Easy start with simple numbers
        first_options = [10, 20, 30, 12, 13, 14, 15]
        second_options = [11, 12, 13, 14, 15, 21, 22, 23]
        
    elif difficulty == 2:
        # Level 2: Building up
        first_options = list(range(20, 40))
        second_options = list(range(15, 35))
        
    elif difficulty == 3:
        # Level 3: Standard practice (like the example 60 × 81)
        first_options = list(range(30, 70))
        second_options = list(range(25, 85))
        
    elif difficulty == 4:
        # Level 4: Getting harder
        first_options = list(range(50, 95))
        second_options = list(range(35, 90))
        
    else:  # Level 5
        # Level 5: Expert challenge
        first_options = list(range(60, 99))
        second_options = list(range(45, 99))
    
    # Generate the two numbers
    num1 = random.choice(first_options)
    num2 = random.choice(second_options)
    
    # Convert to digits
    num1_digits = [int(d) for d in str(num1)]
    num2_digits = [int(d) for d in str(num2)]
    
    # Pad with zeros if needed (ensure 2-digit numbers)
    while len(num1_digits) < 2:
        num1_digits.insert(0, 0)
    while len(num2_digits) < 2:
        num2_digits.insert(0, 0)
    
    # Calculate lattice cells
    lattice_cells = []
    for i, d1 in enumerate(num2_digits):  # rows (second number)
        row = []
        for j, d2 in enumerate(num1_digits):  # columns (first number)
            product = d1 * d2
            tens = product // 10
            ones = product % 10
            row.append((tens, ones))
        lattice_cells.append(row)
    
    # Calculate diagonal sums (this is the tricky part)
    diagonal_sums = calculate_diagonal_sums(lattice_cells)
    
    # Calculate correct answer
    correct_answer = num1 * num2
    
    # Store question data
    st.session_state.question_data = {
        "num1": num1,
        "num2": num2,
        "num1_digits": num1_digits,
        "num2_digits": num2_digits,
        "lattice_cells": lattice_cells,
        "diagonal_sums": diagonal_sums
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Use the lattice method to find {num1} × {num2}"

def calculate_diagonal_sums(lattice_cells):
    """Calculate the diagonal sums for lattice multiplication"""
    rows = len(lattice_cells)
    cols = len(lattice_cells[0])
    
    # For a 2x2 grid, we have 3 diagonals (right to left)
    diagonal_sums = []
    
    # Rightmost diagonal (bottom-right corner)
    diagonal_sums.append(lattice_cells[-1][-1][1])  # ones digit of bottom-right cell
    
    # Middle diagonal(s)
    if rows == 2 and cols == 2:
        # For 2x2: middle diagonal has two elements
        middle_sum = (lattice_cells[0][1][1] +  # ones of top-right
                     lattice_cells[1][0][1] +   # ones of bottom-left  
                     lattice_cells[1][1][0])    # tens of bottom-right
        diagonal_sums.append(middle_sum)
        
        # Next diagonal
        next_sum = (lattice_cells[0][0][1] +    # ones of top-left
                   lattice_cells[0][1][0] +     # tens of top-right
                   lattice_cells[1][0][0])      # tens of bottom-left
        diagonal_sums.append(next_sum)
        
        # Leftmost diagonal (top-left corner)
        diagonal_sums.append(lattice_cells[0][0][0])  # tens digit of top-left cell
    
    return diagonal_sums

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question title
    st.markdown(f"### {st.session_state.current_question}")
    st.markdown("*Calculate the sum of each diagonal and enter them in the blue input boxes.*")
    
    # Display the main equation
    st.markdown(f"""
    <div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; color: #333;">
        {data['num1']} × {data['num2']} = ????
    </div>
    """, unsafe_allow_html=True)
    
    # Create the lattice grid with embedded input boxes
    create_lattice_grid_simple(data)
    
    # Submit button and form handling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True, key="submit_lattice"):
            # Get the diagonal inputs from session state (handle None values)
            diagonal_inputs = st.session_state.get('diagonal_inputs', [None, None, None, None])
            
            # Check if all inputs are provided
            if any(x is None for x in diagonal_inputs):
                st.error("Please fill in all diagonal sum boxes before submitting!")
                return
            
            st.session_state.user_diagonal_sums = diagonal_inputs
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback and next button
    handle_feedback_and_next()

def create_lattice_grid_simple(data):
    """Create the visual lattice grid using Streamlit components"""
    st.markdown("### 🔢 Lattice Grid:")
    
    # Extract cell values for easier reference
    tens1, ones1 = data['lattice_cells'][0][0]  # top-left
    tens2, ones2 = data['lattice_cells'][0][1]  # top-right
    tens3, ones3 = data['lattice_cells'][1][0]  # bottom-left
    tens4, ones4 = data['lattice_cells'][1][1]  # bottom-right
    
    # Create the layout with the lattice grid and input boxes positioned correctly
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Left side input boxes
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        diagonal_3_input = st.number_input("", min_value=0, max_value=100, value=None, key="diagonal_3", 
                                         placeholder="D3", label_visibility="collapsed", 
                                         help="Diagonal 3 sum")
        
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing between boxes
        diagonal_2_input = st.number_input("", min_value=0, max_value=100, value=None, key="diagonal_2", 
                                         placeholder="D2", label_visibility="collapsed",
                                         help="Diagonal 2 sum")
    
    with col2:
        # Create matplotlib lattice grid (without the sum boxes)
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        fig, ax = plt.subplots(1, 1, figsize=(3, 3), dpi=100)
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Draw main grid
        outer_rect = patches.Rectangle((0.5, 0.5), 2.0, 2.0, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(outer_rect)
        
        # Internal grid lines
        ax.plot([1.5, 1.5], [0.5, 2.5], 'k-', linewidth=1.5)  # Vertical divider
        ax.plot([0.5, 2.5], [1.5, 1.5], 'k-', linewidth=1.5)  # Horizontal divider
        
        # Diagonal lines in each cell
        ax.plot([0.5, 1.5], [1.5, 2.5], 'k-', linewidth=1)  # Top-left
        ax.plot([1.5, 2.5], [1.5, 2.5], 'k-', linewidth=1)  # Top-right
        ax.plot([0.5, 1.5], [0.5, 1.5], 'k-', linewidth=1)  # Bottom-left
        ax.plot([1.5, 2.5], [0.5, 1.5], 'k-', linewidth=1)  # Bottom-right
        
        # Add numbers
        # Top headers
        ax.text(1.0, 2.7, str(data['num1_digits'][0]), ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(2.0, 2.7, str(data['num1_digits'][1]), ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Right headers
        ax.text(2.7, 2.0, str(data['num2_digits'][0]), ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(2.7, 1.0, str(data['num2_digits'][1]), ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Cell values
        # Top-left cell
        ax.text(0.8, 2.2, str(tens1), ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(1.2, 1.8, str(ones1), ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Top-right cell
        ax.text(1.8, 2.2, str(tens2), ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(2.2, 1.8, str(ones2), ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Bottom-left cell
        ax.text(0.8, 1.2, str(tens3), ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(1.2, 0.8, str(ones3), ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Bottom-right cell
        ax.text(1.8, 1.2, str(tens4), ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(2.2, 0.8, str(ones4), ha='center', va='center', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)
        plt.close()
        
        # Bottom input boxes
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            diagonal_4_input = st.number_input("", min_value=0, max_value=100, value=None, key="diagonal_4", 
                                             placeholder="D4", label_visibility="collapsed",
                                             help="Diagonal 4 sum (leftmost)")
        with col_b:
            diagonal_1_input = st.number_input("", min_value=0, max_value=100, value=None, key="diagonal_1", 
                                             placeholder="D1", label_visibility="collapsed",
                                             help="Diagonal 1 sum (rightmost)")
    
    with col3:
        # Right side - could add instructions or leave empty
        st.markdown("")
    
    # Store the inputs in session state for easy access
    st.session_state.diagonal_inputs = [diagonal_1_input, diagonal_2_input, diagonal_3_input, diagonal_4_input]
    
    # Show what to calculate for each diagonal
    st.markdown("**Quick Reference:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**D1 (rightmost):** {ones4}")
    with col2:
        st.markdown(f"**D2:** {ones2} + {ones3} + {tens4}")
    with col3:
        st.markdown(f"**D3:** {ones1} + {tens2} + {tens3}")
    with col4:
        st.markdown(f"**D4 (leftmost):** {tens1}")

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
    """Display feedback for the submitted answers"""
    user_sums = st.session_state.user_diagonal_sums
    expected_sums = st.session_state.question_data['diagonal_sums']
    
    # Check diagonal sums
    all_correct = True
    for i, (user_sum, expected_sum) in enumerate(zip(user_sums, expected_sums)):
        if user_sum != expected_sum:
            all_correct = False
            break
    
    # Show feedback for each diagonal
    cols = st.columns(len(expected_sums))
    for i, (user_sum, expected_sum) in enumerate(zip(user_sums, expected_sums)):
        with cols[i]:
            if user_sum == expected_sum:
                st.success(f"✅ Diagonal {i+1}: {expected_sum}")
            else:
                st.error(f"❌ Diagonal {i+1}: {expected_sum} (you put {user_sum})")
    
    # Overall feedback
    if all_correct:
        st.success("🎉 **Perfect! You mastered the lattice method!**")
        
        # Calculate and show final answer
        final_answer = form_final_answer(expected_sums)
        st.info(f"**Final Answer:** {final_answer}")
        
        # Track consecutive correct answers
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3 and st.session_state.lattice_difficulty < 5:
            old_difficulty = st.session_state.lattice_difficulty
            st.session_state.lattice_difficulty += 1
            st.session_state.consecutive_correct = 0
            
            if st.session_state.lattice_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Outstanding! You've reached Expert Level!**")
            else:
                st.info(f"⬆️ **Level Up! Now on Level {st.session_state.lattice_difficulty}**")
    
    else:
        # Reset consecutive correct counter
        st.session_state.consecutive_correct = 0
        
        # Show explanation
        show_explanation()
        
        # Decrease difficulty if multiple wrong
        wrong_count = sum([user != expected for user, expected in zip(user_sums, expected_sums)])
        if wrong_count >= 2 and st.session_state.lattice_difficulty > 1:
            st.session_state.lattice_difficulty -= 1
            st.warning(f"⬇️ **Moving to Level {st.session_state.lattice_difficulty} for more practice.**")

def form_final_answer(diagonal_sums):
    """Form the final answer from diagonal sums with carrying"""
    # Start from rightmost diagonal and handle carrying
    result_digits = []
    carry = 0
    
    for i in range(len(diagonal_sums)):
        total = diagonal_sums[-(i+1)] + carry  # Start from rightmost
        result_digits.insert(0, total % 10)
        carry = total // 10
    
    # Add any remaining carry
    if carry > 0:
        result_digits.insert(0, carry)
    
    return int(''.join(map(str, result_digits)))

def show_explanation():
    """Show step-by-step explanation"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Step-by-step solution**", expanded=True):
        st.markdown(f"### Lattice Method for {data['num1']} × {data['num2']}")
        
        st.markdown("#### Step 1: Fill the lattice cells")
        for i, row in enumerate(data['lattice_cells']):
            for j, (tens, ones) in enumerate(row):
                product = data['num2_digits'][i] * data['num1_digits'][j]
                st.markdown(f"- **{data['num2_digits'][i]} × {data['num1_digits'][j]} = {product:02d}** (tens: {tens}, ones: {ones})")
        
        st.markdown("#### Step 2: Add diagonal sums")
        for i, diagonal_sum in enumerate(data['diagonal_sums']):
            st.markdown(f"- **Diagonal {i+1}:** {diagonal_sum}")
        
        st.markdown("#### Step 3: Form final answer")
        final_answer = form_final_answer(data['diagonal_sums'])
        st.markdown(f"Reading the diagonal sums from left to right (with carrying): **{final_answer}**")
        st.markdown(f"**Check:** {data['num1']} × {data['num2']} = {st.session_state.correct_answer} ✓")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    
    # Clear the diagonal input values
    for i in range(1, 5):
        key = f"diagonal_{i}"
        if key in st.session_state:
            del st.session_state[key]
    
    if "user_diagonal_sums" in st.session_state:
        del st.session_state.user_diagonal_sums
    if "diagonal_inputs" in st.session_state:
        del st.session_state.diagonal_inputs