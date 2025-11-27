#!/usr/bin/python3

# INET4031
# Your Name
# Data Created
# Date Last Modified

#REPLACE THIS COMMENT - identify what each of these imports is for.
import os
import re
import sys

#YOUR CODE SHOULD HAVE NONE OF THE INSTRUCTORS COMMENTS REMAINING WHEN YOU ARE FINISHED
#PLEASE REPLACE INSTRUCTOR "PROMPTS" WITH COMMENTS OF YOUR OWN

def main():
    for line in sys.stdin:

        #REPLACE THIS COMMENT - this "regular expression" is searching for the presence of a character - what is it and why?
        #The important part is WHY it is looking for a particular characer - what is that character being used for?
        match = re.match("^#",line)

        #REPLACE THIS COMMENT - why is the code doing this?
        fields = line.strip().split(':')

        #REPLACE THESE COMMENTS with a single comment describing the logic of the IF 
        #what would an appropriate comment be for describing what this IF statement is checking for?
        #what happens if the IF statement evaluates to true?
        #how does this IF statement rely on what happened in the prior two lines of code? The match and fields lines.
        #the code clearly shows that the variables match and the length of fields is being checked for being != 5  so why is it doing that?
        if match or len(fields) != 5:
            continue

        #REPLACE THIS COMMENT - what is the purpose of the next three lines. How does it relate to what is stored in the passwd file?
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        #REPLACE THIS COMMENT - why is this split being done?
        groups = fields[4].split(',')

        #REPLACE THIS COMMENT - what is the point of this print statement?
        print("==> Creating account for %s..." % (username))
        #REPLACE THIS COMMENT - what is this line doing?  What will the variable "cmd" contain.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        #REMOVE THIS COMMENT AFTER YOU UNDERSTAND WHAT TO DO - these statements are currently "commented out" as talked about in class
        #The first time you run the code...what should you do here?  If uncommented - what will the os.system(cmd) statemetn attempt to do?
        #print(cmd)
        #os.system(cmd)

        #REPLACE THIS COMMENT - what is the point of this print statement?
        print("==> Setting the password for %s..." % (username))
        #REPLACE THIS COMMENT - what is this line doing?  What will the variable "cmd" contain. You'll need to lookup what these linux commands do.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        #REMOVE THIS COMMENT AFTER YOU UNDERSTAND WHAT TO DO - these statements are currently "commented out" as talked about in class
        #The first time you run the code...what should you do here?  If uncommented - what will the os.system(cmd) statemetn attempt to do?
        #print(cmd)
        #os.system(cmd)

        for group in groups:
            #REPLACE THIS COMMENT with one that answers "What is this IF statement looking for and why? If group !='-' what happens?"
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print(cmd)
                #os.system(cmd)

if __name__ == '__main__':
    main()
