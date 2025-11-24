#!/run/current-system/sw/bin/python3

import random
import os
import argparse

# argparsing shennanigans

parser = argparse.ArgumentParser(description='French Vocabulary Quiz')
parser.add_argument('vocab_file', help='which vocab unit')
args = parser.parse_args()
vocab = args.vocab_file


os.chdir("/home/rhemus/french")
def quiz(vocab):
    os.chdir("/home/rhemus/french/vocab")

    with open(vocab, "r") as f:     # opens vocab file 
        vocab_list = f.readlines()   # file --> list
        vocab_list = [x[:-1] for x in vocab_list] # removes \n from list elements
        del vocab_list[0:2] # removes all but vocab from list
        f.close()
        
    num = input(">> ")
    if num != 'max' and num != "con" :
        int(num)
        max(num, vocab_list)
        pass
    elif num == 'con':
        con(vocab_list)
    else:
        max(num, vocab_list)


            
def ran(num, vocab_list):      # creates a random even number (corresponding to french word)
    r = 2#random.randint(0, len(vocab_list))
    while (r % 2) == 0: # changed from !=
        r = random.randint(0, len(vocab_list))
    return r



def max(num, vocab_list):

        print("Total questions:", round(len(vocab_list)/2))
        num = int(len(vocab_list)/2)

        for i in range(0, int(num)):
            r = ran(num, vocab_list) # even = english
            print("Translate", vocab_list[r-1]) # even-1 = french
            ans = input("Answer: ")
            if ans != (vocab_list[(r)]): # changed from r+1
                print("Correct answer:", vocab_list[(r)]) # changed from r+1
                continue
            else:
                print("Correct")
                continue
            del vocab_list[r] # removes q&a to avoid repeutition
            del vocab_list[(r+1)]
            



def con(vocab_list):

    print("Continuous Mode \n \n")
    num = int(len(vocab_list)/2)

    while True:
        r = ran(num, vocab_list)
        print("Translate", vocab_list[r-1]) # changed from r
        ans = input("Answer: ")
        if ans != (vocab_list[(r)]): # changed from r+1
            print("Correct answer:", vocab_list[(r)]) # changed from r+1
            continue
        else:
            print("Correct")
            continue
        del vocab_list[r] # removes q&a to avoid repeutition
        del vocab_list[(r+1)]




        
quiz(vocab)
