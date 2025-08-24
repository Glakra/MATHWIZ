import streamlit as st
import random
import math

def run():
    """
    Main function to run the Fractions of a whole: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/fractions_of_a_whole_word_problems.py
    """
    # Initialize session state
    if "fraction_word_problem" not in st.session_state:
        st.session_state.fraction_word_problem = None
        st.session_state.fraction_word_submitted = False
        st.session_state.selected_model = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📖 Fractions of a Whole: Word Problems")
    st.markdown("*Choose the model that represents the fraction in the story*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.fraction_word_problem is None:
        st.session_state.fraction_word_problem = generate_word_problem()
        st.session_state.fraction_word_submitted = False
        st.session_state.selected_model = None
    
    problem = st.session_state.fraction_word_problem
    
    # Display the word problem
    st.markdown(f"### 📝 Problem:")
    st.info(problem['story'])
    st.markdown(f"**Which model represents the fraction of {problem['question']}?**")
    
    # Display the visual options
    st.markdown("### 🎨 Choose the correct model:")
    
    # Create columns for the options
    cols = st.columns(3)
    
    for i, option in enumerate(problem['options']):
        with cols[i % 3]:
            # Display the SVG
            st.markdown(option['svg'], unsafe_allow_html=True)
            
            # Radio button for selection
            if st.button(f"Select Model {i+1}", 
                        key=f"select_{i}",
                        type="primary" if st.session_state.selected_model == i else "secondary",
                        use_container_width=True,
                        disabled=st.session_state.fraction_word_submitted):
                st.session_state.selected_model = i
                st.rerun()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", 
                    type="primary", 
                    use_container_width=True,
                    disabled=st.session_state.fraction_word_submitted or st.session_state.selected_model is None):
            st.session_state.fraction_word_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.fraction_word_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.fraction_word_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.fraction_word_problem = None
                st.session_state.fraction_word_submitted = False
                st.session_state.selected_model = None
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Read carefully:** Understand what the story is saying
        2. **Find the numbers:** 
           - How many total parts?
           - How many parts are used/colored?
        3. **Check the models:** Look for the one that matches
        
        ### Example:
        - Story: "Sam has a pizza cut into 8 slices. He eats 3 slices."
        - Total parts: 8
        - Used parts: 3
        - Fraction: 3/8
        - Look for a model showing 3 out of 8 parts colored
        
        ### Tips:
        - **Count carefully:** Make sure to count all parts
        - **Match the story:** The colored parts should match what happens in the story
        - **Check your work:** Does the model make sense with the story?
        """)

def generate_word_problem():
    """Generate a random word problem with visual options"""
    scenarios = [
        {
            'character': 'Emma',
            'object': 'chocolate bar',
            'total': 6,
            'used': 2,
            'action': 'eats',
            'setup': 'Emma has a chocolate bar that is divided into {total} equal pieces. She {action} {used} pieces.',
            'question': 'the chocolate bar that Emma eats'
        },
        {
            'character': 'Jack',
            'object': 'garden',
            'total': 8,
            'used': 3,
            'action': 'plants flowers in',
            'setup': 'Jack has divided his garden into {total} equal sections. He {action} {used} sections.',
            'question': 'the garden where Jack plants flowers'
        },
        {
            'character': 'Lily',
            'object': 'art canvas',
            'total': 4,
            'used': 1,
            'action': 'paints',
            'setup': 'Lily divides her art canvas into {total} equal parts to create different designs. She {action} {used} part.',
            'question': 'the canvas that Lily paints'
        },
        {
            'character': 'Noah',
            'object': 'pizza',
            'total': 8,
            'used': 3,
            'action': 'eats',
            'setup': 'Noah orders a pizza that is cut into {total} equal slices. He {action} {used} slices.',
            'question': 'the pizza that Noah eats'
        },
        {
            'character': 'Sophia',
            'object': 'cookie sheet',
            'total': 12,
            'used': 4,
            'action': 'fills with cookies',
            'setup': 'Sophia has a cookie sheet divided into {total} equal spaces. She {action} {used} spaces.',
            'question': 'the cookie sheet that Sophia fills'
        },
        {
            'character': 'Oliver',
            'object': 'bookshelf',
            'total': 5,
            'used': 2,
            'action': 'fills with books',
            'setup': 'Oliver has a bookshelf with {total} equal compartments. He {action} {used} compartments.',
            'question': 'the bookshelf that Oliver fills with books'
        },
        {
            'character': 'Ava',
            'object': 'bead bracelet',
            'total': 10,
            'used': 3,
            'action': 'adds blue beads to',
            'setup': 'Ava is making a bracelet with {total} equal sections. She {action} {used} sections.',
            'question': 'the bracelet sections with blue beads'
        },
        {
            'character': 'Ethan',
            'object': 'sandwich',
            'total': 4,
            'used': 1,
            'action': 'eats',
            'setup': 'Ethan cuts his sandwich into {total} equal pieces. He {action} {used} piece.',
            'question': 'the sandwich that Ethan eats'
        },
        {
            'character': 'Mia',
            'object': 'flower pot arrangement',
            'total': 6,
            'used': 4,
            'action': 'plants roses in',
            'setup': 'Mia has a flower pot arrangement divided into {total} equal sections. She {action} {used} sections.',
            'question': 'the flower pot with roses'
        },
        {
            'character': 'Lucas',
            'object': 'ice cube tray',
            'total': 8,
            'used': 5,
            'action': 'fills with juice',
            'setup': 'Lucas has an ice cube tray with {total} equal compartments. He {action} {used} compartments.',
            'question': 'the ice cube tray that Lucas fills with juice'
        }
    ]
    
    # Select a random scenario
    scenario = random.choice(scenarios)
    
    # Create the story
    story = scenario['setup'].format(
        total=scenario['total'],
        used=scenario['used'],
        action=scenario['action']
    )
    
    # Generate visual options (correct answer + 2 distractors)
    options = []
    
    # Correct answer
    correct_option = {
        'numerator': scenario['used'],
        'denominator': scenario['total'],
        'is_correct': True
    }
    
    # Generate distractors
    distractors = []
    
    # Distractor 1: Different numerator
    if scenario['used'] > 1:
        distractors.append({
            'numerator': scenario['used'] - 1,
            'denominator': scenario['total'],
            'is_correct': False
        })
    else:
        distractors.append({
            'numerator': scenario['used'] + 1,
            'denominator': scenario['total'],
            'is_correct': False
        })
    
    # Distractor 2: Different denominator or switched values
    if scenario['total'] <= 8:
        # Use a different common denominator
        alt_denominators = [3, 4, 5, 6, 8, 10, 12]
        alt_denominators = [d for d in alt_denominators if d != scenario['total']]
        alt_denom = random.choice(alt_denominators)
        # Adjust numerator proportionally if possible
        alt_num = min(int(scenario['used'] * alt_denom / scenario['total']), alt_denom - 1)
        if alt_num == 0:
            alt_num = 1
        distractors.append({
            'numerator': alt_num,
            'denominator': alt_denom,
            'is_correct': False
        })
    else:
        # Swap numerator and denominator if valid
        if scenario['used'] > scenario['total']:
            distractors.append({
                'numerator': scenario['total'],
                'denominator': scenario['used'],
                'is_correct': False
            })
        else:
            distractors.append({
                'numerator': scenario['used'] + 2,
                'denominator': scenario['total'],
                'is_correct': False
            })
    
    # Combine and shuffle options
    all_options = [correct_option] + distractors
    random.shuffle(all_options)
    
    # Generate SVG for each option
    for i, opt in enumerate(all_options):
        # Randomly choose between rectangle or circle representation
        if random.choice(['rect', 'circle']) == 'rect' and opt['denominator'] <= 12:
            svg = create_rectangle_fraction_svg(opt['denominator'], opt['numerator'])
        else:
            svg = create_circle_fraction_svg(opt['denominator'], opt['numerator'])
        opt['svg'] = svg
    
    # Store which index has the correct answer
    correct_index = next(i for i, opt in enumerate(all_options) if opt['is_correct'])
    
    return {
        'story': story,
        'question': scenario['question'],
        'options': all_options,
        'correct_index': correct_index,
        'fraction': f"{scenario['used']}/{scenario['total']}"
    }

def create_rectangle_fraction_svg(total_parts, colored_parts):
    """Create a rectangle divided into parts with some colored"""
    # Determine layout (rows x cols)
    if total_parts <= 4:
        cols = total_parts
        rows = 1
    elif total_parts == 6:
        cols = 3
        rows = 2
    elif total_parts == 8:
        cols = 4
        rows = 2
    elif total_parts == 10:
        cols = 5
        rows = 2
    elif total_parts == 12:
        cols = 4
        rows = 3
    else:
        cols = min(total_parts, 6)
        rows = (total_parts + cols - 1) // cols
    
    # Colors to use
    colors = ['#4CAF50', '#FF9800', '#2196F3', '#9C27B0', '#F44336']
    color = random.choice(colors)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 20px 0;">')
    svg_parts.append('<svg width="240" height="120" viewBox="0 0 240 120" style="border: 2px solid #333;">')
    
    part_width = 240 / cols
    part_height = 120 / rows
    
    colored_count = 0
    
    for row in range(rows):
        for col in range(cols):
            if row * cols + col < total_parts:
                x = col * part_width
                y = row * part_height
                
                # Color the first 'colored_parts' sections
                if colored_count < colored_parts:
                    fill_color = color
                    colored_count += 1
                else:
                    fill_color = 'white'
                
                svg_parts.append(f'''<rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" 
                                    fill="{fill_color}" stroke="black" stroke-width="2"/>''')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def create_circle_fraction_svg(total_parts, colored_parts):
    """Create a circle divided into sectors with some colored"""
    colors = ['#FFD700', '#90EE90', '#FFB6C1', '#E6E6FA', '#FFA07A']
    color = random.choice(colors)
    
    svg_parts = []
    svg_parts.append('<div style="text-align: center; margin: 20px 0;">')
    svg_parts.append('<svg width="160" height="160" viewBox="0 0 160 160">')
    
    angle_per_part = 360 / total_parts
    
    for i in range(total_parts):
        start_angle = i * angle_per_part - 90
        end_angle = (i + 1) * angle_per_part - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = 80 + 70 * math.cos(start_rad)
        y1 = 80 + 70 * math.sin(start_rad)
        x2 = 80 + 70 * math.cos(end_rad)
        y2 = 80 + 70 * math.sin(end_rad)
        
        # Color the first 'colored_parts' sectors
        if i < colored_parts:
            fill_color = color
        else:
            fill_color = 'white'
        
        # Create sector path
        large_arc = 0 if angle_per_part <= 180 else 1
        path = f'M 80 80 L {x1:.2f} {y1:.2f} A 70 70 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'
        svg_parts.append(f'<path d="{path}" fill="{fill_color}" stroke="black" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    
    return ''.join(svg_parts)

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.fraction_word_problem
    selected = st.session_state.selected_model
    
    if selected == problem['correct_index']:
        st.success(f"🎉 **Correct! The fraction is {problem['fraction']}**")
        st.balloons()
    else:
        st.error(f"❌ **Not quite right.**")
        correct_option = problem['options'][problem['correct_index']]
        st.info(f"The correct answer is Model {problem['correct_index'] + 1}, which shows {problem['fraction']}")
        
        # Show explanation
        with st.expander("📖 **See explanation**", expanded=True):
            st.markdown(f"""
            **Understanding the problem:**
            
            {problem['story']}
            
            **Breaking it down:**
            - Total parts: **{correct_option['denominator']}**
            - Parts used/colored: **{correct_option['numerator']}**
            - Fraction: **{correct_option['numerator']}/{correct_option['denominator']}**
            
            The correct model shows {correct_option['numerator']} out of {correct_option['denominator']} parts colored.
            """)