                           How to Set Up The French Vocab Quiz Script


                                          Disclaimer:
                             Whilst its intended use is for learning
                             vocabulary, it is also possible to use
                              the script for flashcards, provided the
                             given document follows the right syntax.


                                          Contents:

                               - Downloading and Installation
                               - Setting up the Script
                               - Running and Using
                               - Vocab Files
                               - Flashcard Expansion





                     Downloading & Installation
 
Having asked for the script and its counterparts, I will most likely email you in the ensuing 48 hours. When
you receive this email, you must download the base, packaged as `vocab_quiz.txt` (.txt for ease of downloading).
It is also advisable to download the attatched vocab files for out of the box usage. Once you have downloaded all
of these files to you main file system, it is recommended to create files to sort the scripts and vocab. Below is
my ideal layout for the above:

                ________
            >--| script |
 ________   |
| french | ⤭
            |   ________ 
            >--| vocab  |



                     Setting up the Script

Since I set up the script to match my system's file layout, there are a few lines which will need to be modified to
match your own. Hopefully the python is well documented enough to have pointed out the following lines, but if not:

15] os.chdir("/home/rhemus/french")

Should be changed to the folder in which both the script and vocab folder are, regardless of whether or not they are
inside of a subfolder.

17]     os.chdir("/home/rhemus/french/vocab")

Should lead to your vocab folder, or if you have chosen not to have that in a folder then the location of the vocab
documents.
Furthermore, in the above cases, the "/home/rhemus/" section should be replaced with your home folder, or the one with
'french' as a subfolder. Finally, to convert the script into TRUE python, change the extension (.txt) to .py either in
your file navigator or terminal. 




                     Running and Using the Script

To run the script, use the following syntax:

python3 vocab_quiz.py vocab_3-2.txt

You will have to have python installed to run this, but it should be already available and if not, easy to install anyway.
Naturally the `vocab_3-2` can be changed to something like `vocab_1-3`, or even any other text file in the right format.
When you do run it, you should receive the prompt `>>` to which there are several options:
- max
> gives you as many questions as there are in the file (may repeat questions)
- con
> continuous questions from the given file
- <number>
> gives you the number of questions you have asked for
I do imagine that this will by quite buggy, especially the number part as it is the oldest and less useful out of all of them.
Additionally I will continue to update the script with new features as I please, and as can you.




                     Vocab Files

As I mentioned before, there is a specific format to the vocab files due to the way in which they are handled with the code.
The first two lines are irrelevant, and usually have the title and an empty line for clarity. After this, the first line of
vocab (line 3) is in french, with its english translation on the next line (4). This pattern continues for the rest of the file.
Because each week we will learn new vocab, you (or I if you would rather) will have to make a new file for the next section.
Again, save it to the relevant file. If I get enough of a demand, I may open a Github page for easier downloading of the vocab
file for each week. Up to you.



                     Flashcard Expansion

Due to the way that the code works, it is definitely possible to have flashcards. If you use the format described in the above
section, you can figure out how to acheive this. It boils down to:

[1] Title
[2]
[3] Question
[4] Answer
    .
    .
    .
However if you want this to feel right, you can change line 52(max&num); 73(con) to your desired question text. Have fun!
