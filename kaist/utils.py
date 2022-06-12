def input_yes_no_question(prompt, default=False):
    """Input yes or no question"""
    true_false_to_str = {
        True: 'y',
        False: 'n'
    }
    
    while True:
        print(f"{prompt} (Press ENTER for default: {true_false_to_str[default]}): ", end='')
        answer = input("Answer [y/n]: ").lower()
        if any(answer == f for f in ["yes", 'y', '1', 'ye', 'yep', 'yeah']):
            return True
        elif any(answer == f for f in ['no', 'n', '0', 'nope']):
            return False
        elif answer == '':
            return default
        else: 
            print("Answer with yes or no: ", end='')
            continue


def input_with_default(prompt, default, yes_no_question=False):
    """Input with default"""
    if yes_no_question:
        return input_yes_no_question(prompt, default)
    print(f"{prompt} (Press ENTER for default: {default}): ", end='')
    return input() or default
