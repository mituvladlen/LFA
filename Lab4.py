import random
import re

def parse_regex(pattern):
    """Parse the regex into a structured format."""
    i = 0
    parsed = []
    while i < len(pattern):
        char = pattern[i]
        if char.isspace():
            # Skip spaces
            i += 1
            continue
        if char == '(':
            # Handle alternation groups (a|b|c)
            end = pattern.find(')', i)
            options = pattern[i + 1:end].split('|')
            parsed.append(('group', options))
            i = end
        elif char == '^':
            # Handle repetitions (X^+), (X^*), (X^n)
            if pattern[i + 1] == '+':
                parsed[-1] = ('repeat', parsed[-1], 1, 3)  # At least 1, max 3
                i += 1
            elif pattern[i + 1] == '*':
                parsed[-1] = ('repeat', parsed[-1], 0, 3)  # 0 to 3
                i += 1
            elif pattern[i + 1].isdigit():
                end = i + 2
                while end < len(pattern) and pattern[end].isdigit():
                    end += 1
                count = int(pattern[i + 1:end])
                parsed[-1] = ('repeat', parsed[-1], count, count)
                i = end - 1
        elif char == '[':
            # Handle alternation groups [abc]
            end = pattern.find(']', i)
            options = list(pattern[i + 1:end])
            parsed.append(('group', options))
            i = end
        elif char == '{':
            # Handle explicit repetitions {min,max}
            end = pattern.find('}', i)
            min_max = pattern[i + 1:end].split(',')
            min_count = int(min_max[0])
            max_count = int(min_max[1]) if len(min_max) > 1 else min_count
            parsed[-1] = ('repeat', parsed[-1], min_count, max_count)
            i = end
        else:
            # Handle regular characters
            parsed.append(('char', char))
        i += 1
    return parsed

def generate_from_parsed(parsed):
    """Generate a string from the parsed regex structure."""
    result = []
    for token in parsed:
        if token[0] == 'char':
            result.append(token[1])
        elif token[0] == 'group':
            result.append(random.choice(token[1]))
        elif token[0] == 'repeat':
            _, sub_token, min_count, max_count = token
            count = random.randint(min_count, max_count)
            for _ in range(count):
                result.append(generate_from_parsed([sub_token]))
    return ''.join(result)

def generate_from_regex(pattern, num_samples=10):
    """Generate multiple strings from a regex."""
    parsed = parse_regex(pattern)
    return [generate_from_parsed(parsed) for _ in range(num_samples)]

def preprocess_regex(regex):
    """Convert 'the power of' syntax to your variant's syntax."""
    regex = regex.replace(" the power of \"*\"", "^*")
    regex = regex.replace(" the power of \"+\"", "^+")
    regex = re.sub(r'the power of \"(\d+)\"', r'^\1', regex)
    return regex

def main():
    examples = [
        "(S|T)(U|V) W the power of \"*\" Y the power of \"+\" 24",
        "L(M|N)O the power of \"3\" P the power of \"*\" Q(2|3)",
        "R the power of \"*\" S(T|U|V) W(X|Y|Z) the power of \"2\""
    ]
    for regex in examples:
        regex = preprocess_regex(regex)  # Convert to your variant's syntax
        print(f"\nRegex: {regex}")
        strings = generate_from_regex(regex, num_samples=30)  # Generate 30 strings
        print(f"Generated {len(strings)} strings:")
        print(strings)
        if regex == "(S|T)(U|V)W^*Y^+24":
            check_examples = ["SUWWY24", "SVWY24"]
        elif regex == "L(M|N)O^3P^*Q(2|3)":
            check_examples = ["LMOOOPPPQ2", "LNOOOPQ3"]
        elif regex == "R^*S(T|U|V)W(X|Y|Z)^2":
            check_examples = ["RSTWXX", "RRRSUWYY"]


if __name__ == "__main__":
    main()