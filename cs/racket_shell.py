#!/bin/python
from cmd import Cmd

class RacketShell(Cmd):
    intro = 'Welcome to a "Racket" Shell. Type help or ? for a list for documentation'
    prompt = '>'

    # 1. Addition (+)
    # 2. Subtraction (-)
    # 3. Division (/)
    # 4. Multiplication (*)
    # 5. Defining single character variables (define)
    # 6. End the REPL (exit)


    
    # library functions
    def default(self, line):
        # only run commands only if command is first or last in line 
       return self.process_command(line)

    # internal functions
    # recursive function to runa
    def process_command(self, s):
        #check command has parens on the outside
        line = self.check_parens(s)
        if line: 
            #check for if command exits else return not found error
            command = line.split()[0]
            #arg fixer
            args = self.arg_parser(line)

            #check if command is known if so run it with args
            print(args)


    def arg_parser(self,s):
    # find and return a list of arguments from a string
        split_list=s.split()

        inside_command=''

        arg_list=[]

        inside=False

        for i in range(1,len(split_list)):
            if  '(' not in split_list[i] and not inside:
                arg_list.append(split_list[i])
            else:
                inside=True
                inside_command += split_list[i] + ' '
                if ')' in split_list[i]:
                    arg_list.append(inside_command[:-1])
                    inside_command=''
                    inside=False

        return arg_list







    def check_parens(self, s):
    #check for parenthesis on outside if good return command inside with out whitespace on the outside
        if s[0]=='(' and s[-1]==')': 
            return s[1:-1].strip()
        else:
            self.error('please ensure all commands start with `(` and end with `)`')

    def error(self, reason):
        print(f'Error: {reason}')


    #user commands




if __name__ == '__main__':
    RacketShell().cmdloop()