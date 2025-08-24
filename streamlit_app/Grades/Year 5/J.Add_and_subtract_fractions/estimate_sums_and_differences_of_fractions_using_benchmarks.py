import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Estimate Sums and Differences of Fractions Using Benchmarks activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/estimate_sums_and_differences_of_fractions_using_benchmarks.py
    """
    # Initialize session state
    if "benchmark_score" not in st.session_state:
        st.session_state.benchmark_score = 0
        st.session_state.benchmark_attempts = 0
    
    if "current_benchmark_problem" not in st.session_state:
        st.session_state.current_benchmark_problem = None
        st.session_state.selected_benchmark = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Add custom CSS for button styling
    st.markdown("""
    <style>
    /* Style for benchmark tiles */
    div.stButton > button {
        background-color: #f0f8ff;
        color: #333;
        font-size: 24px;
        font-weight: bold;
        height: 80px;
        width: 100%;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    div.stButton > button:hover {
        background-color: #e6f3ff;
        border-color: #4CAF50;
    }
    
    /* Selected button style */
    div.stButton > button[data-selected="true"] {
        background-color: #4CAF50;
        color: white;
        border-color: #45a049;
    }
    
    /* Submit button specific style */
    .submit-button > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-size: 18px !important;
        height: 50px !important;
        margin-top: 20px !important;
    }
    
    .submit-button > button:hover {
        background-color: #45a049 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("🎯 Estimate Sums and Differences Using Benchmarks")
    st.markdown("*Use benchmark fractions (0, ½, 1, 1½) to estimate*")
    
    # Score display
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown("**Score**")
        st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>{st.session_state.benchmark_score}/{st.session_state.benchmark_attempts}</div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.benchmark_attempts > 0:
            percentage = (st.session_state.benchmark_score / st.session_state.benchmark_attempts) * 100
            st.markdown("**Accuracy**")
            st.markdown(f"<div style='font-size: 24px; font-weight: bold;'>{percentage:.0f}%</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: right; margin-top: 20px;'></div>", unsafe_allow_html=True)
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_benchmark_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    with st.expander("💡 **How to Estimate Using Benchmarks**", expanded=False):
        st.markdown("""
        ### Benchmark Fractions:
        - **0** = Empty
        - **½** = Half
        - **1** = Whole
        - **1½** = One and a half
        
        ### Tips for Estimating:
        
        **Fractions close to 0:**
        - 1/8, 1/10, 1/12, 2/10
        
        **Fractions close to ½:**
        - 3/6, 4/8, 5/10, 6/12, 4/9, 5/11
        
        **Fractions close to 1:**
        - 7/8, 9/10, 11/12, 8/9, 10/11
        
        ### Strategy:
        1. Look at each fraction
        2. Decide which benchmark it's closest to
        3. Add or subtract the benchmarks
        
        ### Example:
        - **7/8 + 1/10** ≈ 1 + 0 = 1
        - **5/6 - 1/8** ≈ 1 - 0 = 1
        - **4/9 + 5/8** ≈ ½ + ½ = 1
        """)

def generate_new_problem():
    """Generate a new benchmark estimation problem"""
    # Define fractions close to different benchmarks
    close_to_0 = [(1, 8), (1, 10), (1, 12), (2, 10), (1, 6), (2, 12)]
    close_to_half = [(3, 6), (4, 8), (5, 10), (6, 12), (4, 9), (5, 11), (3, 7), (5, 9)]
    close_to_1 = [(7, 8), (9, 10), (11, 12), (8, 9), (10, 11), (5, 6), (6, 7)]
    
    # Problem types
    problem_types = [
        # Sum problems
        ("sum", close_to_0, close_to_half, "1/2"),
        ("sum", close_to_half, close_to_half, "1"),
        ("sum", close_to_0, close_to_1, "1"),
        ("sum", close_to_half, close_to_1, "1 1/2"),
        ("sum", close_to_0, close_to_0, "0"),
        
        # Difference problems
        ("difference", close_to_1, close_to_half, "1/2"),
        ("difference", close_to_1, close_to_0, "1"),
        ("difference", close_to_half, close_to_0, "1/2"),
        ("difference", close_to_1, close_to_1, "0"),
        ("difference", [(5, 6), (7, 8), (9, 10)], [(1, 8), (1, 10), (1, 6)], "1"),
        ("difference", [(5, 8), (5, 9), (6, 10)], [(1, 6), (1, 8), (2, 10)], "1/2")
    ]
    
    # Select random problem type
    operation, set1, set2, correct_answer = random.choice(problem_types)
    
    # Select random fractions from sets
    num1, denom1 = random.choice(set1)
    num2, denom2 = random.choice(set2)
    
    # Create fractions
    frac1 = Fraction(num1, denom1)
    frac2 = Fraction(num2, denom2)
    
    # For difference, ensure first fraction is larger
    if operation == "difference" and frac1 < frac2:
        frac1, frac2 = frac2, frac1
        num1, denom1, num2, denom2 = num2, denom2, num1, denom1
    
    # Determine benchmark options based on the problem
    if operation == "sum":
        benchmark_options = ["1/2", "1", "1 1/2"]
    else:  # difference
        benchmark_options = ["0", "1/2", "1"]
    
    st.session_state.current_benchmark_problem = {
        "operation": operation,
        "num1": num1,
        "denom1": denom1,
        "num2": num2,
        "denom2": denom2,
        "frac1": frac1,
        "frac2": frac2,
        "correct_answer": correct_answer,
        "benchmark_options": benchmark_options
    }
    st.session_state.selected_benchmark = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_problem():
    """Display the current benchmark problem"""
    problem = st.session_state.current_benchmark_problem
    
    # Display problem type
    if problem["operation"] == "sum":
        st.markdown("### Estimate the sum using benchmarks.")
    else:
        st.markdown("### Estimate the difference using benchmarks.")
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Display the fraction problem
    col1, col2, col3 = st.columns([1.5, 0.5, 1.5])
    
    with col1:
        # First fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; line-height: 1;">
                <div style="border-bottom: 3px solid black; display: inline-block; padding: 0 20px; min-width: 60px;">
                    {problem['num1']}
                </div>
                <div style="padding: 0 20px; min-width: 60px;">
                    {problem['denom1']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        op_symbol = "+" if problem["operation"] == "sum" else "−"
        st.markdown(f"<div style='text-align: center; font-size: 36px; margin-top: 25px;'>{op_symbol}</div>", unsafe_allow_html=True)
    
    with col3:
        # Second fraction
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; line-height: 1;">
                <div style="border-bottom: 3px solid black; display: inline-block; padding: 0 20px; min-width: 60px;">
                    {problem['num2']}
                </div>
                <div style="padding: 0 20px; min-width: 60px;">
                    {problem['denom2']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Display benchmark options as clickable tiles
    if not st.session_state.answer_submitted:
        display_benchmark_tiles(problem["benchmark_options"])
        
        # Submit button
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('<div class="submit-button">', unsafe_allow_html=True)
            if st.button("Submit", type="primary", use_container_width=True):
                if st.session_state.selected_benchmark:
                    check_answer()
                else:
                    st.warning("Please select a benchmark estimate.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next Problem →", type="secondary", use_container_width=True):
                reset_problem()
                st.rerun()

def display_benchmark_tiles(options):
    """Display clickable benchmark tiles"""
    cols = st.columns(len(options))
    
    for i, option in enumerate(options):
        with cols[i]:
            # Create clickable button for each benchmark
            if st.button(option, key=f"benchmark_{i}", use_container_width=True):
                st.session_state.selected_benchmark = option
                st.rerun()
            
            # Show selected state
            if st.session_state.selected_benchmark == option:
                st.markdown("✓ Selected", unsafe_allow_html=True)

def check_answer():
    """Check the selected benchmark answer"""
    problem = st.session_state.current_benchmark_problem
    correct_answer = problem["correct_answer"]
    user_answer = st.session_state.selected_benchmark
    
    st.session_state.answer_submitted = True
    st.session_state.benchmark_attempts += 1
    
    if user_answer == correct_answer:
        st.session_state.benchmark_score += 1
        st.session_state.user_correct = True
    else:
        st.session_state.user_correct = False
    
    st.session_state.show_feedback = True
    st.rerun()

def show_feedback():
    """Display feedback for the answer"""
    problem = st.session_state.current_benchmark_problem
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.user_correct:
        st.success("🎉 **Correct! Well done!**")
    else:
        st.error(f"❌ **Not quite right.** The correct estimate is **{problem['correct_answer']}**")
    
    # Show explanation
    with st.expander("📖 **See explanation**", expanded=True):
        show_explanation(problem)

def show_explanation(problem):
    """Show explanation for the benchmark estimation"""
    frac1 = problem['frac1']
    frac2 = problem['frac2']
    
    # Determine benchmarks for each fraction
    benchmark1 = get_closest_benchmark(frac1)
    benchmark2 = get_closest_benchmark(frac2)
    
    st.markdown(f"""
    ### How to estimate:
    
    **Step 1: Find the benchmark for each fraction**
    - {frac1} ≈ {benchmark1} (because {explain_benchmark(frac1, benchmark1)})
    - {frac2} ≈ {benchmark2} (because {explain_benchmark(frac2, benchmark2)})
    
    **Step 2: {problem['operation'].capitalize()} the benchmarks**
    """)
    
    if problem['operation'] == 'sum':
        st.markdown(f"- {benchmark1} + {benchmark2} = **{problem['correct_answer']}**")
    else:
        st.markdown(f"- {benchmark1} − {benchmark2} = **{problem['correct_answer']}**")
    
    # Show actual calculation for reference
    actual_result = frac1 + frac2 if problem['operation'] == 'sum' else frac1 - frac2
    st.markdown(f"""
    **Actual answer:** {actual_result} ≈ {float(actual_result):.2f}
    
    Our estimate of **{problem['correct_answer']}** is close!
    """)

def get_closest_benchmark(fraction):
    """Determine the closest benchmark for a fraction"""
    value = float(fraction)
    if value <= 0.25:
        return "0"
    elif value <= 0.75:
        return "1/2"
    elif value <= 1.25:
        return "1"
    else:
        return "1 1/2"

def explain_benchmark(fraction, benchmark):
    """Explain why a fraction is close to a benchmark"""
    value = float(fraction)
    
    if benchmark == "0":
        return f"{fraction} is close to 0 (it equals {value:.2f})"
    elif benchmark == "1/2":
        return f"{fraction} is close to 1/2 (it equals {value:.2f})"
    elif benchmark == "1":
        return f"{fraction} is close to 1 (it equals {value:.2f})"
    else:
        return f"{fraction} is close to 1 1/2 (it equals {value:.2f})"

def reset_problem():
    """Reset for next problem"""
    st.session_state.current_benchmark_problem = None
    st.session_state.selected_benchmark = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if hasattr(st.session_state, 'user_correct'):
        del st.session_state.user_correct