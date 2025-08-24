import random
import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display, HTML
from fractions import Fraction

def load_add_three_fractions(container):
    """
    Render an addition problem with three or more fractions:
    - Display 3-4 fractions to add
    - User enters answer as a fraction
    - Provide feedback and explanation
    - Generate various difficulty levels
    """
    # Clear previous content
    container.clear_output()
    with container:
        # 1) Define fraction problem sets with varying difficulty
        problem_sets = [
            # Easy: Common denominators or easy to find LCD
            {
                "fractions": [Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)],
                "difficulty": "easy",
                "hint": "Find LCD of 10, 5, and 2"
            },
            {
                "fractions": [Fraction(1, 10), Fraction(1, 2), Fraction(1, 10)],
                "difficulty": "easy",
                "hint": "Find LCD of 10 and 2"
            },
            {
                "fractions": [Fraction(5, 12), Fraction(1, 4), Fraction(1, 6)],
                "difficulty": "medium",
                "hint": "Find LCD of 12, 4, and 6"
            },
            {
                "fractions": [Fraction(1, 3), Fraction(1, 6), Fraction(1, 9)],
                "difficulty": "medium",
                "hint": "Find LCD of 3, 6, and 9"
            },
            {
                "fractions": [Fraction(2, 5), Fraction(1, 10), Fraction(3, 20)],
                "difficulty": "medium",
                "hint": "Find LCD of 5, 10, and 20"
            },
            {
                "fractions": [Fraction(1, 4), Fraction(2, 3), Fraction(1, 6)],
                "difficulty": "medium",
                "hint": "Find LCD of 4, 3, and 6"
            },
            {
                "fractions": [Fraction(3, 8), Fraction(1, 4), Fraction(1, 2)],
                "difficulty": "easy",
                "hint": "Find LCD of 8, 4, and 2"
            },
            {
                "fractions": [Fraction(2, 7), Fraction(3, 14), Fraction(1, 2)],
                "difficulty": "hard",
                "hint": "Find LCD of 7, 14, and 2"
            },
            {
                "fractions": [Fraction(5, 6), Fraction(1, 3), Fraction(1, 4)],
                "difficulty": "hard",
                "hint": "Find LCD of 6, 3, and 4"
            },
            {
                "fractions": [Fraction(3, 10), Fraction(2, 5), Fraction(1, 15)],
                "difficulty": "hard",
                "hint": "Find LCD of 10, 5, and 15"
            },
            # Four fractions for extra challenge
            {
                "fractions": [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 6)],
                "difficulty": "hard",
                "hint": "Find LCD of 2, 3, 4, and 6"
            },
            {
                "fractions": [Fraction(1, 5), Fraction(2, 15), Fraction(1, 3), Fraction(1, 10)],
                "difficulty": "hard",
                "hint": "Find LCD of 5, 15, 3, and 10"
            }
        ]
        
        # 2) Select a random problem
        problem = random.choice(problem_sets)
        fractions = problem["fractions"]
        
        # 3) Calculate the correct answer
        correct_answer = sum(fractions)
        
        # 4) Display the problem
        display(HTML("<h3>Add.</h3>"))
        
        # Create the fraction display
        fraction_html = ""
        for i, frac in enumerate(fractions):
            if i > 0:
                fraction_html += " + "
            fraction_html += f'<span style="display: inline-block; text-align: center; vertical-align: middle; margin: 0 5px;">'
            fraction_html += f'<span style="display: block; border-bottom: 2px solid black; padding: 0 5px;">{frac.numerator}</span>'
            fraction_html += f'<span style="display: block; padding: 0 5px;">{frac.denominator}</span>'
            fraction_html += f'</span>'
        
        fraction_html += ' = '
        
        # 5) Create input elements
        numerator_input = widgets.Text(
            value='',
            placeholder='',
            layout=Layout(width='60px', height='30px'),
            style={'text-align': 'center'}
        )
        
        denominator_input = widgets.Text(
            value='',
            placeholder='',
            layout=Layout(width='60px', height='30px'),
            style={'text-align': 'center'}
        )
        
        # Create fraction input display
        input_fraction_html = widgets.HTML(
            value=f'''
            <div style="display: inline-block; text-align: center; vertical-align: middle; margin-left: 10px;">
                <div style="border-bottom: 2px solid black; padding: 2px; min-width: 60px;">
                    <div id="num-placeholder"></div>
                </div>
                <div style="padding: 2px; min-width: 60px;">
                    <div id="denom-placeholder"></div>
                </div>
            </div>
            '''
        )
        
        # 6) Display the problem with inputs
        problem_container = widgets.HBox([
            widgets.HTML(value=f'<div style="font-size: 18px; margin: 20px 0;">{fraction_html}</div>'),
            widgets.VBox([numerator_input, denominator_input], layout=Layout(margin='0 0 0 10px'))
        ])
        display(problem_container)
        
        # 7) Create submit button and feedback area
        submit_btn = widgets.Button(
            description='Submit',
            button_style='success',
            layout=Layout(width='120px', height='40px', margin='20px 0')
        )
        
        feedback = widgets.Output()
        next_btn = widgets.Button(
            description='Next Question',
            button_style='info',
            layout=Layout(display='none', margin='0 0 0 20px')
        )
        
        # 8) Define submit handler
        def on_submit(_):
            with feedback:
                feedback.clear_output()
                
                # Validate inputs
                try:
                    if not numerator_input.value or not denominator_input.value:
                        display(HTML("<div style='color:orange; font-weight:bold; font-size:16px;'>Please enter both numerator and denominator.</div>"))
                        return
                    
                    user_num = int(numerator_input.value)
                    user_denom = int(denominator_input.value)
                    
                    if user_denom == 0:
                        display(HTML("<div style='color:orange; font-weight:bold; font-size:16px;'>Denominator cannot be zero.</div>"))
                        return
                    
                    user_answer = Fraction(user_num, user_denom)
                    
                except ValueError:
                    display(HTML("<div style='color:orange; font-weight:bold; font-size:16px;'>Please enter valid numbers.</div>"))
                    return
                
                # Check answer
                if user_answer == correct_answer:
                    display(HTML("<div style='color:green; font-weight:bold; font-size:16px;'>✅ Correct!</div>"))
                    
                    # Show work if answer is in simplest form
                    if correct_answer.denominator != user_answer.denominator:
                        display(HTML(f"<div style='color:green; margin-top:10px;'>Good job! You simplified to {user_answer}.</div>"))
                else:
                    display(HTML(f"<div style='color:red; font-weight:bold; font-size:16px;'>❌ Incorrect.</div>"))
                    display(HTML(f"<div style='color:red; margin-top:10px;'>The correct answer is {correct_answer} or {correct_answer.numerator}/{correct_answer.denominator}.</div>"))
                    
                    # Show step-by-step solution
                    display(HTML("<div style='margin-top:15px; padding:10px; background:#f5f5f5; border-left:3px solid #2196F3;'>"))
                    display(HTML("<strong>Step-by-step solution:</strong><br/>"))
                    
                    # Find LCD
                    denominators = [f.denominator for f in fractions]
                    lcd = denominators[0]
                    for d in denominators[1:]:
                        lcd = lcd * d // gcd(lcd, d)
                    
                    display(HTML(f"1. Find the LCD of {', '.join(map(str, denominators))}: LCD = {lcd}<br/>"))
                    
                    # Convert fractions
                    display(HTML("2. Convert each fraction:<br/>"))
                    converted_fractions = []
                    for frac in fractions:
                        multiplier = lcd // frac.denominator
                        new_num = frac.numerator * multiplier
                        converted_fractions.append(f"{new_num}/{lcd}")
                        display(HTML(f"   • {frac} = {frac.numerator} × {multiplier}/{frac.denominator} × {multiplier} = {new_num}/{lcd}<br/>"))
                    
                    # Add numerators
                    sum_numerators = sum(f.numerator * (lcd // f.denominator) for f in fractions)
                    display(HTML(f"3. Add the numerators: {' + '.join(str(f.numerator * (lcd // f.denominator)) for f in fractions)} = {sum_numerators}<br/>"))
                    display(HTML(f"4. Result: {sum_numerators}/{lcd}<br/>"))
                    
                    # Simplify if needed
                    if correct_answer.denominator != lcd:
                        display(HTML(f"5. Simplify: {sum_numerators}/{lcd} = {correct_answer}<br/>"))
                    
                    display(HTML("</div>"))
                
                # Disable inputs and show next button
                submit_btn.disabled = True
                numerator_input.disabled = True
                denominator_input.disabled = True
                next_btn.layout.display = None
        
        # 9) Define next button handler
        def on_next(_):
            load_add_three_fractions(container)
        
        submit_btn.on_click(on_submit)
        next_btn.on_click(on_next)
        
        # 10) Display controls
        controls_box = widgets.HBox([submit_btn, next_btn])
        display(controls_box)
        display(feedback)
        
        # 11) Display hint
        display(HTML(f"<div style='margin-top:20px; color:#666; font-style:italic;'>Hint: {problem['hint']}</div>"))

# Helper function for GCD (if not imported)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a