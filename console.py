#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State


def parse(arg):
    curlybrackets = re.search(r"\{(.*?)\}", arg)
    squarebrackets = re.search(r"\[(.*?)\]", arg)
    if curlybrackets is None:
        if squarebrackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:squarebrackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(squarebrackets.group())
            return retl
    else:
        lexer = split(arg[:curlybrackets.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curlybrackets.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB CLI.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argmnt1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argmnt1[1])
            if match is not None:
                command = [argmnt1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argmnt1[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argmnt1 = parse(arg)
        if len(argmnt1) == 0:
            print("** class name missing **")
        elif argmnt1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argmnt1[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argmnt1 = parse(arg)
        objectdictionary = storage.all()
        if len(argmnt1) == 0:
            print("** class name missing **")
        elif argmnt1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argmnt1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argmnt1[0], argmnt1[1]) not in objectdictionary:
            print("** no instance found **")
        else:
            print(objectdictionary["{}.{}".format(argmnt1[0], argmnt1[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argmnt1 = parse(arg)
        objectdictionary = storage.all()
        if len(argmnt1) == 0:
            print("** class name missing **")
        elif argmnt1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argmnt1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argmnt1[0], argmnt1[1]) not in objectdictionary.keys():
            print("** no instance found **")
        else:
            del objectdictionary["{}.{}".format(argmnt1[0], argmnt1[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argmnt1 = parse(arg)
        if len(argmnt1) > 0 and argmnt1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argmnt1) > 0 and argmnt1[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argmnt1) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argmnt1 = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argmnt1[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argmnt1 = parse(arg)
        objectdictionary = storage.all()

        if len(argmnt1) == 0:
            print("** class name missing **")
            return False
        if argmnt1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argmnt1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argmnt1[0], argmnt1[1]) not in objectdictionary.keys():
            print("** no instance found **")
            return False
        if len(argmnt1) == 2:
            print("** attribute name missing **")
            return False
        if len(argmnt1) == 3:
            try:
                type(eval(argmnt1[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argmnt1) == 4:
            obj = objectdictionary["{}.{}".format(argmnt1[0], argmnt1[1])]
            if argmnt1[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argmnt1[2]])
                obj.__dict__[argmnt1[2]] = valtype(argmnt1[3])
            else:
                obj.__dict__[argmnt1[2]] = argmnt1[3]
        elif type(eval(argmnt1[2])) == dict:
            obj = objectdictionary["{}.{}".format(argmnt1[0], argmnt1[1])]
            for k, v in eval(argmnt1[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
