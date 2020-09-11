#!/bin/python
from cmd import Cmd


class RacketShell(Cmd):
    intro = 'Welcome to a "Dr. Racket" Shell. Type (?) for a some documentation'
    prompt = ">"

    # class variables

    variables = {}

    command_list = {}

    # sets command_list to below
    def set_cmds(self):

        ##command definitions
        # 1. Addition (+)
        # 2. Subtraction (-)
        # 2. Subtraction (-)
        # 3. Division (/)
        # 4. Multiplication (*)
        # 5. Defining single character variables (define)
        # 6. End the REPL (exit)
        # 7. Help (?)
        self.command_list = {
            "+": {"num_arg": 2, "command": self.add},
            "-": {"num_arg": 2, "command": self.subtract},
            "/": {"num_arg": 2, "command": self.divide},
            "*": {"num_arg": 2, "command": self.multiply},
            "define": {"num_arg": 2, "command": self.define},
            "exit": {"num_arg": 0, "command": self.exit},
            "?": {"num_arg": 0, "command": self.help},
            }

    # user commands
    def add(self, arg1, arg2):
        arg1 = self.process_var(arg1)
        arg2 = self.process_var(arg2)

        try:
            if arg1 and arg2:
                return arg1 + arg2
            else:
                raise TypeError

        except TypeError:
            return self.error("arg1 and arg2 must be numbers")

    def subtract(self, arg1, arg2):
        arg1 = self.process_var(arg1)
        arg2 = self.process_var(arg2)

        try:
            if arg1 and arg2:
                return arg1 - arg2
            else:
                raise TypeError

        except TypeError:
            return self.error("arg1 and arg2 must be numbers")

    def divide(self, arg1, arg2):
        arg1 = self.process_var(arg1)
        arg2 = self.process_var(arg2)

        try:
            if arg1 and arg2:
                return arg1 / arg2
            else:
                raise TypeError

        except TypeError:
            return self.error("arg1 and arg2 must be numbers")

    def multiply(self, arg1, arg2):
        arg1 = self.process_var(arg1)
        arg2 = self.process_var(arg2)

        try:
            if arg1 and arg2:
                return arg1 * arg2
            else:
                raise TypeError

        except TypeError:
            return self.error("arg1 and arg2 must be numbers")

    def define(self, arg1, arg2):
        arg1 = self.process_var(arg1, False)
        if type(arg1) == str and len(arg1) == 1:
            arg2 = self.process_var(arg2)
            if arg2:
                self.variables[arg1] = arg2
                return f"set {arg1} to {arg2}"
            else:
                return self.error("argument 2 must be a number")
        else:
            return self.error("argument 1 must be of a a-z character of length 1")

    def exit(self):
        print("byeeeee")
        return True

    def help(self):
        print("Welcome to Arjun's version of Dr.Racket but worse")
        print("Commands")
        print("=======================================")
        print(
            "You can use the following commands \n\t\
            1. Addition (+ arg1 arg2) \n\t\
            2. Subtraction (- arg1 arg2)\n\t\
            3. Division (/ arg1 arg2)\n\t\
            4. Multiplication (* arg1 arg2)\n\t\
            5. Defining single character variables (define var value)\n\t\
            6. End the REPL (exit)\n\t\7. Help (?)"
        )
        print("Other Fun Features!")
        print("=======================================")
        print("You can next functions like so: (+ 1 (* 2 3))")
        print("Yes. You can do this infinitely.")
        print(
            "The code base is designed to be easily expandable to handle more commands. \n\
            Define a command in the command list and the create a function for it to run, the rest will be taken care of automatically."
        )
        print(
            "The code should yell at you and tell you why you did a dumb thing I needed this for my own sanity.\n\
            80% of the bulk in this code comes from checking all the various ways you could try to hurt me. "
        )
        return False

    # library functions
    def default(self, line):
        # only run commands only if command is first or last in line
        result = self.process_command(line)
        if result == True:
            return result
        elif result != False:
            print(result)

    # internal functions
    # recursive function to runa
    def process_command(self, s):

        # check command has parens on the outside
        line = self.check_parens(s)

        if line:
            # check for if command exits else return not found error
            command = line.split()[0].strip()
            # arg finder
            args = self.arg_parser(line)
            # check if command is known if so run it with args
            if command in self.command_list.keys():
                command = self.command_list[command]
                if len(args) == command["num_arg"]:
                    # check and execute any internal commands
                    checked_args = [self.arg_check(a) for a in args]
                    return command["command"](*checked_args)
                else:
                    return self.error(
                        f'{command["command"].__name__} takes {command["num_arg"]} positional arguments you gave {len(args)}'
                    )
            else:
                return self.error(f"command: {command} is not a known command")
        else:
            return line

    def arg_check(self, a):
        if "(" in a:
            return self.process_command(a)
        else:
            return a

    def arg_parser(self, s):
        # find and return a list of arguments from a string
        split_list = s.split()

        inside_command = ""

        arg_list = []

        inside = False

        for i in range(1, len(split_list)):
            if "(" not in split_list[i] and not inside:
                arg_list.append(split_list[i])
            else:
                inside = True
                inside_command += split_list[i] + " "
                if ")" in split_list[i]:
                    # make sure ( and ) are same ammount before close
                    num_open = len([c for c in inside_command if c == "("])
                    num_close = len([c for c in inside_command if c == ")"])
                    if num_open == num_close:
                        arg_list.append(inside_command[:-1])
                        inside_command = ""
                        inside = False

        return arg_list

    def process_var(self, arg, check_var=True):
        try:
            val = int(arg)
            return val
        except ValueError:
            try:
                val = float(arg)
                return val
            except ValueError:
                try:
                    if check_var:
                        return self.variables[arg]
                    else:
                        return arg
                except:
                    return self.error(f"no variable {arg} found")

    def check_parens(self, s):
        # check for parenthesis on outside if good return command inside with out whitespace on the outside
        if s[0] == "(" and s[-1] == ")":
            return s[1:-1].strip()
        else:
            return self.error(
                "please ensure all commands start with `(` and end with `)`"
            )

    def error(self, reason):
        print(f"Error: {reason}")
        return False


if __name__ == "__main__":
    shell=RacketShell()
    shell.set_cmds()
    shell.cmdloop()
