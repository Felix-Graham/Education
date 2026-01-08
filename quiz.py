import random
import time
import os
import argparse


##############
# autoupdate #
##############

def autoupdate():
    try:
        os.system("git pull")
        #os.system("python3 quiz.py select")
    except:
        pass



############
# autoconf #
############

def autoconf():
    import sys
    load(10, 0.1)
    homedir = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open("config.txt", "w") as f:
        f.write(homedir)
        f.close()

def getconf():
    try:
        with open("config.txt", "r") as f:
            l = f.readlines()
            print(l)
            f.close()
            script_location = ''.join(l)
            print(script_location)

            vocab_location = script_location+"/vocab"
            return script_location, vocab_location
    except:
        print("Config not loaded. Please re-run with 'load' as a keyword")


#################
# miscellaneous #
#################

def pront(string, t):
    string = list(string)
    for i in range(len(string)):
        print(f"{string[i]}", end='')
        time.sleep(t)
    print()

def load(lnum, speed):
    for i in range(0, 100+lnum, lnum):
        print(f"{i}% \r", end="")
        time.sleep(speed)
    print("\r    ", end="")
    print("")

def ran(num, vocab_list):
    r = random.randint(0, len(vocab_list)-1)
    while (r % 2) == 0:  # loop for odd
        r = random.randint(0, len(vocab_list)-1)
    return r

def ran_multi(vocab_list):
    # multi choice for french
    r = random.randint(0, len(vocab_list)-1)
    while (r % 2) != 0:  # continuous for french
        r = random.randint(0, len(vocab_list)-1)
    return r

###########
#  files  #
###########

def getfiles(choice):
    #autoupdate()
    os.chdir(vocab_location)
    files = os.listdir()
    files = purefiles(files)
    
    if choice == 'all':
        return files
    else:
        for i in range(len(files)):
            print(f"{i+1}: {files[i]}")
        q = False
        chosenfiles = []
        print("\nSelect files (enter number), type 'q' when done:")
        while q == False and (len(files) > 0):
            selection = input("> ")
            if selection == 'q':
                if len(chosenfiles) >= 1:
                    q = True
                    break
                else:
                    print("You must select at least 1 file")
            else:
                try:
                    selection = int(selection)
                    chosenfiles.append(files[selection-1])
                    files.remove(files[selection-1])
                    os.system("clear")
                    for i in range(len(files)):
                        print(f"{i+1}: {files[i]}")
                except:
                    print("Invalid selection")
        return chosenfiles

def purefiles(files):
    clean_files = []
    for f in files:
        if "~" not in f and f.endswith('.txt'):
            clean_files.append(f)
    return clean_files

def merge(files):
    os.chdir(vocab_location)
    total = []
    
    for file in files:
        with open(file, "r") as f:
            l = f.readlines()
            l = [s.rstrip() for s in l]
            if len(l) > 2:
                del l[0:2]
            for x in l:
                if x.strip():
                    total.append(x)
    
    return total

#################
# quizing/modes #
#################

def regular_quiz(num, vocab_list):
    vocab_copy = vocab_list.copy()
    questions_asked = 0
    
    if num == 'max':
        num = int(len(vocab_copy)/2)
    else:
        num = int(num)
    
    print(f"\nTotal questions: {num}\n")
    
    for i in range(num):
        if len(vocab_copy) < 2:
            print("\nNo more questions available!")
            break
            
        r = ran(len(vocab_copy), vocab_copy)
        if r >= len(vocab_copy):
            r = len(vocab_copy) - 1
            if r % 2 == 0:
                r -= 1
            
        # r is odd (English), r-1 is even (French)
        print(f"Question {i+1}: Translate '{vocab_copy[r-1]}'")
        ans = input("Answer: ")
        
        if ans.strip().lower() != vocab_copy[r].strip().lower():
            print(f"Incorrect. Correct answer: {vocab_copy[r]}\n")
        else:
            print("Correct!\n")
        
        time.sleep(0.5)

def continuous_quiz(vocab_list):
    print("Continuous Mode - Press Ctrl+C to exit\n")
    
    try:
        while True:
            vocab_copy = vocab_list.copy()
            if len(vocab_copy) < 2:
                break
                
            r = ran(len(vocab_copy), vocab_copy)
            if r >= len(vocab_copy):
                r = len(vocab_copy) - 1
                if r % 2 == 0:
                    r -= 1
                
            # r - English; r-1 - french
            # Ask french, expect English answer
            print(f"Translate '{vocab_copy[r-1]}'")
            ans = input("Answer: ")
            
            if ans.strip().lower() != vocab_copy[r].strip().lower():
                print(f"Incorrect. Correct answer: {vocab_copy[r]}\n")
            else:
                print("Correct!\n")
            
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\n\nQuiz ended!")

def multi_choice_quiz(vocab_list, num_questions):
    
    def get_qa_pair(questions):
        # find q & a for mchoice
        r = ran_multi(questions)
        if r >= len(questions) - 1:
            r = len(questions) - 2
        
        question = questions[r]      # French 
        answer = questions[r + 1]     # English
        
        return question, answer
    
    def get_wrong_answers(questions, correct_answer):
        wrong = []
        attempts = 0
        while len(wrong) < 3 and attempts < 50:
            _, potential = get_qa_pair(questions)
            if potential != correct_answer and potential not in wrong:
                wrong.append(potential)
            attempts += 1
        return wrong
    
    def display_question(question, options, answer):
        print(f"\nWhat is the translation of '{question}'?\n")
        for i in range(len(options)):
            print(f"{i+1}) {options[i]}")
        
        try:
            guess = int(input("\n> "))
            if 1 <= guess <= len(options):
                if options[guess-1] == answer:
                    print("Correct!\n")
                else:
                    print(f"Incorrect. The answer was: {answer}\n")
            else:
                print(f"Invalid selection. The answer was: {answer}\n")
        except:
            print(f"Invalid input. The answer was: {answer}\n")
        
        time.sleep(0.8)
    
    if num_questions == 'max':
        num_questions = int(len(vocab_list)/2)
    else:
        num_questions = int(num_questions)
    
    print(f"\nMultiple Choice Quiz - {num_questions} questions\n")
    
    for i in range(num_questions):
        question, answer = get_qa_pair(vocab_list)
        options = [answer]
        options.extend(get_wrong_answers(vocab_list, answer))
        random.shuffle(options)
        
        print(f"Question {i+1}/{num_questions}")
        display_question(question, options, answer)

def multi_choice_continuous(vocab_list):
    print("Multiple Choice Continuous Mode - Press Ctrl+C to exit\n")
    
    def get_qa_pair(questions):
        r = ran_multi(questions)
        if r >= len(questions) - 1:
            r = len(questions) - 2
        
        question = questions[r]      # French 
        answer = questions[r + 1]     # English        
        return question, answer
    
    def get_wrong_answers(questions, correct_answer):
        wrong = []
        attempts = 0
        while len(wrong) < 3 and attempts < 50:
            _, potential = get_qa_pair(questions)
            if potential != correct_answer and potential not in wrong:
                wrong.append(potential)
            attempts += 1
        return wrong
    
    def display_question(question, options, answer):
        print(f"\nWhat is the translation of '{question}'?\n")
        for i in range(len(options)):
            print(f"{i+1}) {options[i]}")
        
        try:
            guess = int(input("\n> "))
            if 1 <= guess <= len(options):
                if options[guess-1] == answer:
                    print("Correct!\n")
                else:
                    print(f"Incorrect. The answer was: {answer}\n")
            else:
                print(f"Invalid selection. The answer was: {answer}\n")
        except:
            print(f"Invalid input. The answer was: {answer}\n")
        
        time.sleep(0.5)
    
    try:
        while True:
            question, answer = get_qa_pair(vocab_list)
            options = [answer]
            options.extend(get_wrong_answers(vocab_list, answer))
            random.shuffle(options)
            
            display_question(question, options, answer)
    except KeyboardInterrupt:
        print("\n\nQuiz ended!")

########
# main #
########

def main(option):
    os.system("clear")
    pront("Welcome to French Vocabulary Quiz", 0.05)
    print()

    global script_location
    global vocab_location
    script_location, vocab_location = getconf()
    #exit()
    # Get files
    files = getfiles(option)
    vocab_list = merge(files)
    
    if len(vocab_list) < 2:
        print("Error: Not enough vocabulary words loaded!")
        return
    
    print(f"\nLoaded {int(len(vocab_list)/2)} vocabulary pairs\n")
    
    # Select quiz type
    print("Select quiz type:")
    print("1) Traditional (type answer)")
    print("2) Multiple choice")
    quiz_type = input("> ")
    
    # Select mode
    print("\nSelect mode:")
    print("1) Continuous")
    print("2) Set number of questions")
    print("3) Maximum (all questions)")
    mode = input("> ")
    
    os.system("clear")
    
    if quiz_type == "1":  # Traditional
        if mode == "1":  # Continuous
            continuous_quiz(vocab_list)
        elif mode == "3":  # Max
            regular_quiz('max', vocab_list)
        else:  # Set number
            num = input("How many questions? ")
            regular_quiz(num, vocab_list)
    
    elif quiz_type == "2":  # Multiple choice
        if mode == "1":  # Continuous
            multi_choice_continuous(vocab_list)
        elif mode == "3":  # Max
            multi_choice_quiz(vocab_list, 'max')
        else:  # Set number
            num = input("How many questions? ")
            multi_choice_quiz(vocab_list, num)
    
    print("\nThank you for practicing!")

###########
# parsing #
###########

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='French Vocabulary Quiz')
    parser.add_argument('option', help="'all' to use all files, or 'select' to choose files")
    args = parser.parse_args()
    inp = args.option
    
    if inp == 'all':
        print("Selected: ALL files")
        #time.sleep(1)
        autoupdate()
        main(inp)
    elif inp == "load":
        print("Generating...")
        autoconf()
        exit()
    else:
        print("Selected: SELECT files")
        #time.sleep(1)
        autoupdate()
        main(inp)
