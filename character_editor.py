
import json
import shlex

DATABASE_FILE = "completecharlist.json"


def loadDatabase():
    with open(DATABASE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def saveDatabase():
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(characters, file, indent=4, ensure_ascii=False)


def getCharacter(name):
    for character in characters:
        if character["name"].casefold() == name.casefold():
            return character

    return None


def getAttribute(name, attribute):
    character = getCharacter(name)

    if character is None:
        print("Character not found:", name)
        return

    if attribute not in character:
        print("Attribute not found:", attribute)
        return

    print(attribute + ":", character[attribute])


def setAttribute(name, attribute, value):
    character = getCharacter(name)

    if character is None:
        print("Character not found:", name)
        return

    if attribute not in character:
        print("Attribute not found:", attribute)
        return

    # Convert numeric values when appropriate
    if isinstance(character[attribute], int):
        try:
            value = int(value)
        except ValueError:
            pass

    character[attribute] = value
    saveDatabase()

    print("Updated", name + "'s", attribute + ".")


def getAllAttributes(name):
    character = getCharacter(name)

    if character is None:
        print("Character not found:", name)
        return

    for attribute, value in character.items():
        print(attribute + ":", value)


def fillAttributes(value):
    if isinstance(value, dict):
        return {key: fillAttributes(item) for key, item in value.items()}

    elif isinstance(value, list):
        return [fillAttributes(item) for item in value]

    return "[FILL IN]"


def addChar(name):
    if getCharacter(name) is not None:
        print("Character already exists:", name)
        return

    character = fillAttributes(characters[0])
    character["name"] = name

    characters.append(character)
    saveDatabase()

    print("Added", name + ".")


def removeChar(name):
    character = getCharacter(name)

    if character is None:
        print("Character not found:", name)
        return

    characters.remove(character)
    saveDatabase()

    print("Removed", name + ".")


def countValues(value, target):
    count = 0

    if isinstance(value, dict):
        for item in value.values():
            count += countValues(item, target)

    elif isinstance(value, list):
        for item in value:
            count += countValues(item, target)

    elif isinstance(value, str) and value.casefold() == target.casefold():
        count += 1

    return count


def getCharsToFill(num):
    count = 0

    for character in characters:
        if countValues(character, "[FILL IN]") >= 2:
            print(character["name"])
            count += 1

            if count == num:
                break


def getUnknChars(num):
    count = 0

    for character in characters:
        if countValues(character, "unknown") >= 4:
            print(character["name"])
            count += 1

            if count == num:
                break


def addAttribute(attribute):
    if not characters:
        print("Character database is empty.")
        return

    if attribute in characters[0]:
        print("Attribute already exists:", attribute)
        return

    for character in characters:
        newCharacter = {}

        for key, value in character.items():
            newCharacter[key] = value

            if key == "affiliation":
                newCharacter[attribute] = "[FILL IN]"

        character.clear()
        character.update(newCharacter)

    saveDatabase()
    print("Added attribute:", attribute)


def removeAttribute(attribute):
    if not characters:
        print("Character database is empty.")
        return

    if attribute not in characters[0]:
        print("Attribute not found:", attribute)
        return

    if attribute == "name":
        print("Cannot remove the name attribute.")
        return

    for character in characters:
        del character[attribute]

    saveDatabase()
    print("Removed attribute:", attribute)


def showHelp():
    print("""
Commands:
  get <character name> <attribute>
  set <character name> <attribute> <value>
  getAllAttributes <character name>
  addChar <character name>
  removeChar <character name>
  getCharsToFill <num>
  getUnknChars <num>
  addAttribute <attribute>
  removeAttribute <attribute>
  help
  exit

Put character names in quotes if they contain spaces.

Examples:
  get "Gol D. Roger" bounty
  set "Gol D. Roger" bounty 5500000000
  set "Gol D. Roger" affiliation "Roger Pirates"
  getAllAttributes "Gol D. Roger"
  addChar "Gol D. Roger"
  removeChar "Gol D. Roger"
  getCharsToFill 5
  getUnknChars 5
  addAttribute age
  removeAttribute age
""")


characters = loadDatabase()

print("Character Editor")
print("Type 'help' for commands.")

while True:
    try:
        command = shlex.split(input("\n> "))
    except ValueError:
        print("Invalid command formatting.")
        continue

    if not command:
        continue

    action = command[0].casefold()

    if action in ("quit", "exit", "q"):
        break

    elif action == "help":
        showHelp()

    elif action == "get":
        if len(command) < 3:
            print("Usage: get \"Character Name\" attribute")
            continue

        name = " ".join(command[1:-1])
        attribute = command[-1]

        getAttribute(name, attribute)

    elif action == "set":
        if len(command) < 4:
            print("Usage: set \"Character Name\" attribute value")
            continue

        name = " ".join(command[1:-2])
        attribute = command[-2]
        value = command[-1]

        setAttribute(name, attribute, value)

    elif action == "getallattributes":
        if len(command) < 2:
            print("Usage: getAllAttributes \"Character Name\"")
            continue

        name = " ".join(command[1:])
        getAllAttributes(name)

    elif action == "addchar":
        if len(command) < 2:
            print("Usage: addChar \"Character Name\"")
            continue

        name = " ".join(command[1:])
        addChar(name)

    elif action == "removechar":
        if len(command) < 2:
            print("Usage: removeChar \"Character Name\"")
            continue

        name = " ".join(command[1:])
        removeChar(name)

    elif action == "getcharstofill":
        if len(command) != 2:
            print("Usage: getCharsToFill num")
            continue

        try:
            num = int(command[1])
            if num < 1:
                raise ValueError
        except ValueError:
            print("Please enter a positive number.")
            continue

        getCharsToFill(num)

    elif action == "getunknchars":
        if len(command) != 2:
            print("Usage: getUnknChars num")
            continue

        try:
            num = int(command[1])
            if num < 1:
                raise ValueError
        except ValueError:
            print("Please enter a positive number.")
            continue

        getUnknChars(num)

    elif action == "addattribute":
        if len(command) != 2:
            print("Usage: addAttribute attribute")
            continue

        addAttribute(command[1])

    elif action == "removeattribute":
        if len(command) != 2:
            print("Usage: removeAttribute attribute")
            continue

        removeAttribute(command[1])

    else:
        print("Unknown command. Type 'help' for commands.")

print("Goodbye!")

