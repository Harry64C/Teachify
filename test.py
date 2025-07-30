import re
import random

def randomize_numbers_in_expression(expr):
    # Replace every integer or decimal in expr with a random integer 0-10
    def repl(match):
        # You can adjust this range as needed
        return str(random.randint(0, 10))
    # \d+(\.\d+)? matches integers and decimals
    return re.sub(r'\d+(\.\d+)?', repl, expr)

# 1. Read LaTeX file content
with open('static/HomeworkSample.tex', 'r', encoding='utf-8') as f:
    tex_content = f.read()

# 2. Regex for $...$ and $$...$$ math expressions
pattern = r'(\${1,2})(.*?)(\1)'  # Group 1: $ or $$, Group 2: the math expr

def replacer(match):
    delimiter = match.group(1)
    expr = match.group(2)
    randomized_expr = randomize_numbers_in_expression(expr)
    return f"{delimiter}{randomized_expr}{delimiter}"

# 3. Replace each math expression with randomized version
randomized_tex_content = re.sub(pattern, replacer, tex_content, flags=re.DOTALL)

# 4. Write out to a new file
with open('randomized_output.tex', 'w', encoding='utf-8') as f:
    f.write(randomized_tex_content)

