# Python French Quiz

### Contents

> Installation [installation]
> Setup [setup]
> Usage [usage]
> Modification and Enhancement [modification-and-enhancement]


## Installation

To install the program is very simple. Simply navigate to you command line/cmd/terminal and type in the following:

      git clone https://github.com/Felix-Graham/French-Vocab-Quiz.git

This should install everything you can see above to your home in your file system. Once again in the terminal, type 'ls' to show all files and folders at your current location. You should see something like `French-Vocab-Quiz` as well as any other files which you may have there. Finally, type `cd French-Vocab-Quiz`, or whichever name you beleive it is. A last `ls` will confirm that your are in you own copy of the vocab quiz.


## Setup

I have very recently added an auto-config feature, meaning that you have to do almost nothing. If you are following this step individually (without reading the above recently) I recommend you do so that you can navigate into the folder in your terminal. Once you are in, you can initialise the setting up of the code with

      python3 quiz.py load

which will create a text file called `config.txt` in the folder. This simply stores the address of the code, meaning that you don't have to manualy edit it. 


## Usage

After all of the above steps have been completed, you may run the script with 

      python3 quiz.py select/all

where `select` and `all` are interchangeable and self explanatory. From there on you will be prompted to either choose file, if you typed select, a mode and the amount of questions to receive. Have fun!
