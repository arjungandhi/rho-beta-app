#!/bin/python
from cmd import Cmd

class RacketShell(Cmd):
    intro = 'Welcome to a "Racket" Shell. Type help or ? for a list for documentation'
    prompt = '>'

    #user functions

    variables = {}

    def add(self, arg1, arg2):
        return self.process_var(arg1) + self.process_var(arg2)

    
    def subtract(self, arg1, arg2):
         return self.process_var(arg1) - self.process_var(arg2)
    
    def divide(self, arg1, arg2):
         return self.process_var(arg1) / self.process_var(arg2)

    def multiply(self, arg1, arg2):
         return self.process_var(arg1) * self.process_var(arg2)

    def define(self, arg1, arg2):
        if arg1.isalpha() and len(arg1) == 1:
            if arg2.isnumeric():
                variables[arg1] = int(arg2)
                return(f'set {arg1} to {arg2}')
            else:
                self.error('argument 2 must be a number')
        else:
            self.error('argument 1 must be of a a-z character of length 1')


    def exit(self):
        print('byeeeee')
        return True
    

     
    
    # library functions
    def default(self, line):
        # only run commands only if command is first or last in line 
       print(self.process_command(line))

    # internal functions
    # recursive function to runa
    def process_command(self, s):
        ##command definitions
        # 1. Addition (+)
        # 2. Subtraction (-)
        # 3. Division (/)
        # 4. Multiplication (*)
        # 5. Defining single character variables (define)
        # 6. End the REPL (exit)
        command_list= {
            '+' : {
                'num_arg' : 2,
                'command': self.add

            },
            '-' : {
                'num_arg' : 2,
                'command': self.subtract

            },
            '/' : {
                'num_arg' : 2,
                'command': self.divide

            },
            '*' : {
                'num_arg' : 2,
                'command': self.multiply
            },
            'define' : {
                'num_arg' : 2,
                'command': self.define

            },
            'exit' : {
                'num_arg' : 0,
                'command': self.exit

            }
        }

        #check command has parens on the outside
        line = self.check_parens(s)
        if line: 
            #check for if command exits else return not found error
            command = line.split()[0].strip()
            #arg finder
            args = self.arg_parser(line)
            #check if command is known if so run it with args
            if command in command_list.keys():
                command = command_list[command]
                if len(args) == command['num_arg']:
                    #check and execute any internal commands
                    checked_args=[self.arg_check(a) for a in args]
                    return(command['command'](*checked_args))
                else:
                    self.error(f'{command} takes {command["num_arg"]} positional arguments you gave {len(args)}')
            else:
                self.error(f'command: {command} is not a known command')

    def arg_check(self, a):
        if '(' in a:
            return self.process_command(a)
        else:
            return a 

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
                    # make sure ( and ) are same ammount before close
                    num_open=len([c for c in inside_command if c =='('])
                    num_close=len([c for c in inside_command if c ==')'])
                    if num_open == num_close:
                        arg_list.append(inside_command[:-1])
                        inside_command=''
                        inside=False

        return arg_list


    def process_var(self, arg):
        if type(arg) is int or type(arg) is float:
            return arg
        elif type(arg) is str:
            try: 
                return self.variables(arg)
            except:
                self.error(f'no variable {arg} found')
        else:
            return False



    def check_parens(self, s):
    #check for parenthesis on outside if good return command inside with out whitespace on the outside
        if s[0]=='(' and s[-1]==')': 
            return s[1:-1].strip()
        else:
            self.error('please ensure all commands start with `(` and end with `)`')

    def error(self, reason):
        print(f'Error: {reason}')






if __name__ == '__main__':
    RacketShell().cmdloop()
