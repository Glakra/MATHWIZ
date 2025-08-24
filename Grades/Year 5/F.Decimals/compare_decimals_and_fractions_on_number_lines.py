import streamlit as st
import random
import math
from fractions import Fraction
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run():
    """
    Main function to run the Compare decimals and fractions on number lines activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimals_and_fractions_on_number_lines.py
    """
    # Initialize session state for difficulty and game state
    if "decimals_fractions_difficulty" not in st.session_state:
        st.session_state.decimals_fractions_difficulty = 1  # Start with basic level
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_plots = {}
        st.session_state.plots_complete = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Compare Decimals and Fractions on Number Lines")
    st.markdown("*Plot numbers on number lines and compare their values*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimals_fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Basic (tenths)", 2: "Intermediate (hundredths)", 3: "Advanced (mixed)"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=difficulty_names[difficulty_level])
    
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
        ### How to Play:
        - **Read the numbers** (fractions and decimals)
        - **Click on the number line** to plot each number
        - **Answer the comparison question**
        - **Watch the visual feedback** to understand the relationships
        
        ### Tips for Success:
        - **Convert to compare:** Change fractions to decimals or vice versa
        - **Use the number line:** Visual placement helps with comparison
        - **Think in parts:** 1/2 = 0.5, 1/4 = 0.25, 3/4 = 0.75
        
        ### Examples:
        - **9/10 = 0.9** (closer to 1.0 than 0.2)
        - **1/4 = 0.25** (between 0.2 and 0.3)
        - **3/5 = 0.6** (greater than 0.5)
        
        ### Common Fractions to Decimals:
        - **1/2 = 0.5** | **1/4 = 0.25** | **3/4 = 0.75**
        - **1/5 = 0.2** | **2/5 = 0.4** | **3/5 = 0.6** | **4/5 = 0.8**
        - **1/10 = 0.1** | **3/10 = 0.3** | **7/10 = 0.7** | **9/10 = 0.9**
        
        ### Difficulty Levels:
        - **🟡 Basic:** Simple fractions and tenths (0.1, 0.2, etc.)
        - **🟠 Intermediate:** Hundredths and more complex fractions
        - **🔴 Advanced:** Mixed fractions, decimals, and complex comparisons
        """)

def generate_new_question():
    """Generate a new comparison question with plotting"""
    difficulty = st.session_state.decimals_fractions_difficulty
    
    # Define number pools based on difficulty
    if difficulty == 1:
        # Basic: simple fractions and tenths
        fractions = [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), 
                    Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(1, 10), 
                    Fraction(3, 10), Fraction(7, 10), Fraction(9, 10)]
        decimals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        number_line_range = (0, 1)
        step = 0.1
        
    elif difficulty == 2:
        # Intermediate: hundredths and more fractions
        fractions = [Fraction(1, 3), Fraction(2, 3), Fraction(1, 6), Fraction(5, 6),
                    Fraction(3, 8), Fraction(5, 8), Fraction(7, 8), Fraction(2, 3),
                    Fraction(4, 9), Fraction(5, 9), Fraction(7, 9)]
        decimals = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 
                   0.12, 0.37, 0.62, 0.87]
        number_line_range = (0, 1)
        step = 0.1
        
    else:
        # Advanced: mixed ranges and complex numbers
        fractions = [Fraction(5, 4), Fraction(7, 4), Fraction(3, 2), Fraction(5, 3),
                    Fraction(4, 3), Fraction(7, 6), Fraction(11, 8), Fraction(13, 10)]
        decimals = [0.3, 0.7, 1.2, 1.6, 1.8, 0.8, 1.4, 1.9]
        number_line_range = (0, 2)
        step = 0.2
    
    # Select two numbers to compare
    all_numbers = []
    
    # Add fractions
    for frac in random.sample(fractions, min(3, len(fractions))):
        decimal_value = float(frac)
        if number_line_range[0] <= decimal_value <= number_line_range[1]:
            all_numbers.append({"value": frac, "type": "fraction", "decimal": decimal_value})
    
    # Add decimals
    for dec in random.sample(decimals, min(3, len(decimals))):
        if number_line_range[0] <= dec <= number_line_range[1]:
            all_numbers.append({"value": dec, "type": "decimal", "decimal": dec})
    
    # Pick two different numbers for comparison
    if len(all_numbers) < 2:
        # Fallback to ensure we have enough numbers
        all_numbers = [
            {"value": Fraction(1, 4), "type": "fraction", "decimal": 0.25},
            {"value": 0.7, "type": "decimal", "decimal": 0.7}
        ]
    
    numbers_to_plot = random.sample(all_numbers, 2)
    
    # Generate comparison questions
    questions = [
        "Which number is closer to 0?",
        "Which number is closer to 1?",
        "Which number is greater?",
        "Which number is smaller?"
    ]
    
    if number_line_range[1] > 1:
        questions.extend([
            "Which number is closer to 1.5?",
            "Which number is closer to 2?"
        ])
    
    question_text = random.choice(questions)
    
    # Determine correct answer based on question
    num1, num2 = numbers_to_plot[0], numbers_to_plot[1]
    dec1, dec2 = num1["decimal"], num2["decimal"]
    
    if "closer to 0" in question_text:
        correct_answer = num1 if dec1 < dec2 else num2
    elif "closer to 1" in question_text:
        correct_answer = num1 if abs(dec1 - 1) < abs(dec2 - 1) else num2
    elif "closer to 1.5" in question_text:
        correct_answer = num1 if abs(dec1 - 1.5) < abs(dec2 - 1.5) else num2
    elif "closer to 2" in question_text:
        correct_answer = num1 if abs(dec1 - 2) < abs(dec2 - 2) else num2
    elif "greater" in question_text:
        correct_answer = num1 if dec1 > dec2 else num2
    else:  # smaller
        correct_answer = num1 if dec1 < dec2 else num2
    
    st.session_state.question_data = {
        "numbers": numbers_to_plot,
        "question": question_text,
        "range": number_line_range,
        "step": step
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Graph the numbers on the number line and answer: {question_text}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    numbers_text = " and ".join([format_number(num["value"]) for num in data["numbers"]])
    st.markdown(f"**Graph {numbers_text} on the number line.**")
    
    # Display interactive number line
    display_interactive_number_line()
    
    # Display comparison question after plotting
    if st.session_state.plots_complete:
        st.markdown(f"### 🤔 {data['question']}")
        display_answer_choices()

def format_number(value):
    """Format number for display"""
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    else:
        return str(value)

def display_interactive_number_line():
    """Display an interactive number line for plotting"""
    data = st.session_state.question_data
    range_min, range_max = data["range"]
    step = data["step"]
    
    # Create number line points
    points = []
    current = range_min
    while current <= range_max + 0.001:  # Small epsilon for floating point comparison
        points.append(round(current, 2))
        current += step
    
    st.markdown("### 📏 Number Line")
    st.markdown("**Click directly on the number line to plot each number:**")
    
    # Show which numbers need to be plotted
    col1, col2 = st.columns(2)
    for i, num_data in enumerate(data["numbers"]):
        number_text = format_number(num_data["value"])
        with col1 if i == 0 else col2:
            if number_text in st.session_state.user_plots:
                st.success(f"✅ **{number_text}** - plotted at {st.session_state.user_plots[number_text]}")
            else:
                st.info(f"⭕ **{number_text}** - needs to be plotted")
    
    # Show current number to plot
    unplotted_numbers = [num_data for num_data in data["numbers"] 
                        if format_number(num_data["value"]) not in st.session_state.user_plots]
    
    if unplotted_numbers:
        current_num = unplotted_numbers[0]
        st.markdown(f"### 📍 Currently plotting: **{format_number(current_num['value'])}**")
        
        # Create interactive number line with clickable zones
        create_interactive_number_line_with_clicks(points, current_num)
    else:
        st.success("🎉 **All numbers have been plotted!**")
        # Still show the number line for visualization
        create_number_line_svg()
    
    # Reset button
    if st.session_state.user_plots:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Clear All Plots", use_container_width=True):
                st.session_state.user_plots = {}
                st.session_state.plots_complete = False
                st.rerun()

def create_interactive_number_line_with_clicks(points, current_num):
    """Create an interactive number line with clickable areas"""
    # First, display the beautiful number line
    create_number_line_svg()
    
    # Then add clickable zones aligned with the number line
    st.markdown("**👆 Click on any tick mark on the number line above to plot the number:**")
    
    # Create a grid of clickable buttons that align with the number line positions
    cols = st.columns(len(points))
    
    for i, point in enumerate(points):
        with cols[i]:
            # Create invisible buttons that align with number line positions
            button_label = f"📍"
            if st.button(button_label, key=f"plot_{point}", 
                        help=f"Click to plot at {point}",
                        use_container_width=True):
                # Record the plot
                number_text = format_number(current_num["value"])
                st.session_state.user_plots[number_text] = point
                
                # Check if all numbers are plotted
                data = st.session_state.question_data
                if len(st.session_state.user_plots) == len(data["numbers"]):
                    st.session_state.plots_complete = True
                
                st.rerun()

def create_number_line_svg():
    """Create beautiful matplotlib visualization of the number line with plots"""
    data = st.session_state.question_data
    range_min, range_max = data["range"]
    step = data["step"]
    
    # Calculate points on the number line
    points = []
    current = range_min
    while current <= range_max + 0.001:
        points.append(round(current, 2))
        current += step
    
    # Create figure with better styling
    plt.style.use('default')
    fig, ax = plt.subplots(1, 1, figsize=(14, 4))
    fig.patch.set_facecolor('#f8f9fa')
    
    # Draw the main number line with gradient effect
    line_y = 0
    ax.plot([range_min, range_max], [line_y, line_y], 
            color='#2c3e50', linewidth=4, solid_capstyle='round', zorder=2)
    
    # Add subtle shadow under the line
    ax.plot([range_min, range_max], [line_y - 0.02, line_y - 0.02], 
            color='#bdc3c7', linewidth=6, solid_capstyle='round', alpha=0.3, zorder=1)
    
    # Add tick marks with better styling
    for point in points:
        # Main tick marks
        ax.plot([point, point], [line_y - 0.08, line_y + 0.08], 
                color='#34495e', linewidth=3, solid_capstyle='round', zorder=3)
        
        # Tick labels with better typography
        ax.text(point, line_y - 0.18, str(point), 
                ha='center', va='top', fontsize=13, fontweight='600',
                color='#2c3e50', family='sans-serif')
    
    # Add plotted points with beautiful styling
    colors = ['#e74c3c', '#3498db', '#f39c12', '#27ae60']  # Modern flat colors
    color_names = ['Red', 'Blue', 'Orange', 'Green']
    
    for i, (number_text, plotted_value) in enumerate(st.session_state.user_plots.items()):
        color = colors[i % len(colors)]
        
        # Draw point with glow effect
        ax.plot(plotted_value, line_y, 'o', color=color, markersize=16, 
                markeredgecolor='white', markeredgewidth=3, zorder=5)
        ax.plot(plotted_value, line_y, 'o', color=color, markersize=20, 
                alpha=0.3, zorder=4)  # Glow effect
        
        # Add elegant label above the point
        label_y = line_y + 0.25
        ax.text(plotted_value, label_y, number_text, 
                ha='center', va='bottom', fontsize=14, fontweight='bold', 
                color='white', family='sans-serif',
                bbox=dict(boxstyle="round,pad=0.4", facecolor=color, 
                         edgecolor='white', linewidth=2, alpha=0.9),
                zorder=6)
        
        # Add connecting line from point to label
        ax.plot([plotted_value, plotted_value], [line_y + 0.08, label_y - 0.05], 
                color=color, linewidth=2, alpha=0.7, zorder=4)
    
    # Add arrow ends to the number line
    arrow_size = 0.06
    # Left arrow
    ax.annotate('', xy=(range_min - 0.05, line_y), 
                xytext=(range_min + 0.05, line_y),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=3))
    # Right arrow  
    ax.annotate('', xy=(range_max + 0.05, line_y), 
                xytext=(range_max - 0.05, line_y),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=3))
    
    # Set up the plot with better margins and styling
    margin = (range_max - range_min) * 0.15
    ax.set_xlim(range_min - margin, range_max + margin)
    ax.set_ylim(-0.4, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title with better styling
    ax.text((range_min + range_max) / 2, 0.4, 'Number Line', 
            ha='center', va='bottom', fontsize=18, fontweight='bold',
            color='#2c3e50', family='sans-serif')
    
    # Adjust layout for better appearance
    plt.tight_layout()
    
    # Display the plot
    st.pyplot(fig, use_container_width=True)
    plt.close()
    
    # Show plotted numbers summary with better styling
    if st.session_state.user_plots:
        st.markdown("### 📍 **Plotted Numbers**")
        cols = st.columns(len(st.session_state.user_plots))
        colors_hex = ['#e74c3c', '#3498db', '#f39c12', '#27ae60']
        
        for i, (number_text, plotted_value) in enumerate(st.session_state.user_plots.items()):
            with cols[i]:
                color = colors_hex[i % len(colors_hex)]
                st.markdown(f"""
                <div style="
                    background: {color}; 
                    color: white; 
                    padding: 10px; 
                    border-radius: 8px; 
                    text-align: center;
                    font-weight: bold;
                    margin: 5px 0;
                ">
                    {number_text} → {plotted_value}
                </div>
                """, unsafe_allow_html=True)

def display_answer_choices():
    """Display multiple choice answers for the comparison question"""
    data = st.session_state.question_data
    
    # Create answer options
    option1_text = format_number(data["numbers"][0]["value"])
    option2_text = format_number(data["numbers"][1]["value"])
    
    # Answer selection
    with st.form("comparison_form", clear_on_submit=False):
        user_answer = st.radio(
            "Choose your answer:",
            options=[option1_text, option2_text],
            key="comparison_choice"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            # Find which number was selected
            selected_number = None
            for num_data in data["numbers"]:
                if format_number(num_data["value"]) == user_answer:
                    selected_number = num_data
                    break
            
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
        
        # Increase difficulty (max level 3)
        old_difficulty = st.session_state.decimals_fractions_difficulty
        st.session_state.decimals_fractions_difficulty = min(
            st.session_state.decimals_fractions_difficulty + 1, 3
        )
        
        if st.session_state.decimals_fractions_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered advanced decimal and fraction comparison!**")
        elif old_difficulty < st.session_state.decimals_fractions_difficulty:
            difficulty_names = {1: "Basic", 2: "Intermediate", 3: "Advanced"}
            new_level = difficulty_names[st.session_state.decimals_fractions_difficulty]
            st.info(f"⬆️ **Difficulty increased to {new_level} level!**")
    
    else:
        correct_text = format_number(correct_answer["value"])
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_text}**.")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.decimals_fractions_difficulty
        st.session_state.decimals_fractions_difficulty = max(
            st.session_state.decimals_fractions_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.decimals_fractions_difficulty:
            difficulty_names = {1: "Basic", 2: "Intermediate", 3: "Advanced"}
            new_level = difficulty_names[st.session_state.decimals_fractions_difficulty]
            st.warning(f"⬇️ **Difficulty decreased to {new_level} level. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    question = data["question"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Step-by-step explanation:")
        
        # Show decimal values for both numbers
        st.markdown("**Converting to decimals for comparison:**")
        for num_data in data["numbers"]:
            number_text = format_number(num_data["value"])
            decimal_value = num_data["decimal"]
            if isinstance(num_data["value"], Fraction):
                st.markdown(f"- **{number_text}** = {decimal_value}")
            else:
                st.markdown(f"- **{number_text}** = {decimal_value}")
        
        st.markdown("---")
        
        # Explain the specific comparison
        correct_text = format_number(correct_answer["value"])
        correct_decimal = correct_answer["decimal"]
        
        if "closer to 0" in question:
            st.markdown(f"**{correct_text}** ({correct_decimal}) is closer to 0 because it has the smallest value.")
        elif "closer to 1" in question:
            distances = []
            for num_data in data["numbers"]:
                distance = abs(num_data["decimal"] - 1)
                distances.append((format_number(num_data["value"]), distance))
            
            st.markdown("**Distances from 1.0:**")
            for num_text, distance in distances:
                st.markdown(f"- {num_text}: {distance}")
            st.markdown(f"**{correct_text}** is closest to 1.0.")
        elif "greater" in question:
            st.markdown(f"**{correct_text}** ({correct_decimal}) is the greater number.")
        elif "smaller" in question:
            st.markdown(f"**{correct_text}** ({correct_decimal}) is the smaller number.")
        
        # Visual reminder
        st.info("💡 **Remember:** Use the number line to visualize the positions. Numbers to the right are greater!")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_plots = {}
    st.session_state.plots_complete = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer