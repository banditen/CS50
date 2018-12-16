from room import Room
from item import Item
from inventory import Inventory


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.items = self.load_items(f"data/{game}Items.txt")
        self.current_room = self.rooms[1]
        self.player = Inventory()
        self.item = [item[0] for item in self.items]

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a dictionary of 'id' : Room objects.
        """
        # First we parse all the data we need to create the rooms with.
        # All parsed lines of data are saved to rooms_data.
        rooms_data = []
        with open(filename, "r") as f:
            room_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    room_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    rooms_data.append(room_data)
                    room_data = []
        # Append a final time, because the files do not end on a blank newline.
        rooms_data.append(room_data)

        # Create room objects for each set of data we just parsed.
        rooms = {}
        for room_data in rooms_data:
            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its
            # id as key.
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created with the data from each set
        # we have parsed earlier.
        for room_data in rooms_data:
            id = int(room_data[0])
            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]
            # Here we get the current room object that we'll add routes to.
            room = rooms[id]
            for connection, target_room_id in connections:
                # Add routes to a room, and check if a room has a conditional movement
                if "/" in str(target_room_id):
                    # We store the conditional movement to a list, and add the list
                    # to room routes
                    target_room_id, condition = target_room_id.split("/")
                    if connection not in room.routes.keys():
                        conditional = [int(target_room_id), condition]
                        room.add_route(connection, conditional)
                    else:
                        conditional.append(int(target_room_id))
                        conditional.append(condition)

                else:
                    # If no conditinal movement found, add routes normally
                    room.add_route(connection, int(target_room_id))
                    pass

        return rooms

    def load_items(self, filename):
        """
        Parse filename to store items
        """
        # First we parse all the data we need to create the items with.
        # All parsed lines of data are saved to items_data.
        items_data = []
        with open(filename, "r") as f:
            item_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    item_data.append(line.strip())
                # A blank newline signals all data of a single item data is parsed.
                else:
                    items_data.append(item_data)
                    item_data = []
        # Append a final time, because the files do not end on a blank newline.
        items_data.append(item_data)

        # Create item objects for each set of data we just parsed.
        for item_data in items_data:
            name = item_data[0]
            description = item_data[1]
            initial_room_id = int(item_data[2])

            # We store an item as key: value
            item = {}
            item_ = Item(name, description)
            item[name] = description
            # Here we need to get the room id to append items to that room
            room = self.rooms[initial_room_id]
            # Add item to inventory using inventory.py add method
            room.inventory.add(item)
            pass

        return items_data

    def forced(self, direction):
        """
        Create a forced method which let's the player know if he/she attempted
        a move which isn't allowed
        """
        print(self.current_room.description)
        forced = "FORCED"
        # First we check if "FORCED" is found in the room's routes
        if "FORCED" in self.current_room.routes:
            # As long as a room has a FORCED route, we let the player know that
            # he/she attempts a move that isn't allowed
            while forced in self.current_room.routes:
                new_room = self.current_room.routes[forced]
                if any(self.player.inventory) == False:
                    # Because conditional movements are stored as lists, we need
                    # to check if the current room has a conditional movement
                    if isinstance(new_room, list):
                        self.current_room = self.rooms[int(new_room[2])]
                        print(self.current_room.description)
                    else:
                        # If the room has a '0' as it's connected room, it's means
                        # that we are at a dead-end, thus "except KeyError:"
                        try:
                            self.current_room = self.rooms[int(new_room)]
                            print(self.current_room.description)
                        except KeyError:
                            return 0

                # We have to check if the player have the required items
                elif any(self.player.inventory) == True:
                    # Because conditional movements are stored as lists, we need
                    # to check if the current room has a conditional movement
                    if isinstance(new_room, list):
                        # If the player have the required item, then we move to the
                        # conditional room
                        for i, item in enumerate(new_room):
                            if item in self.player.inventory.keys():
                            # If the item is found in player's inventory, then we move to
                            # the conditional room
                                newroom = new_room[i-1]
                                break
                            else:
                                newroom = new_room[i]

                        self.current_room = self.rooms[newroom]
                        print(self.current_room.description)

                    else:
                        # If the room has a '0' as it's connected room, it's means
                        # that we are at a dead-end, thus "except KeyError:"
                        try:
                            self.current_room = self.rooms[int(new_room)]
                            print(self.current_room.description)
                        except KeyError:
                            return 0

        else:
            pass

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        victory = 0
        # If the current room has a route of '0',
        # the game terminates
        if victory in self.current_room.routes.values():
            return True
        else:
            return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        Conditional movement is based on player's inventory,
        which is also checked
        """

        # First we check if a given direction can be found in
        # routes
        if direction not in self.current_room.routes:
            print("Invalid command!")
            return
        else:
            new_room = self.current_room.routes[direction]
            # Then we have to check if player's inventory is empty or not
            if any(self.player.inventory) == False:

                # Because rooms with conditinal moves are stored as lists, we need
                # to check if the new room's directions are stored in a list
                if isinstance(new_room, list):
                    self.current_room = self.rooms[int(new_room[2])]
                    Adventure.forced(self, direction)

                else:
                    self.current_room = self.rooms[int(new_room)]
                    Adventure.forced(self, direction)

            # If the player have an item in his/hers inventory
            elif any(self.player.inventory) == True:

                # Again, first we have to check if the new rooms's directions are
                # stored in a list
                if isinstance(new_room, list):
                    # If the player have the required item, then we move to the
                    # conditional room
                    for i, item in enumerate(new_room):
                        if item in self.player.inventory.keys():
                        # If the item is found in player's inventory, then we move to
                        # the conditional room
                            newroom = new_room[i-1]
                            break
                        else:
                            newroom = new_room[i]

                    self.current_room = self.rooms[newroom]
                    Adventure.forced(self, direction)
                # If the player doesn't have the required item, we move to
                # the other room
                else:
                    self.current_room = self.rooms[new_room]
                    Adventure.forced(self, direction)
                # If we are not at a room with conditional movement, we move the
                # player normally
            else:
                self.current_room = self.rooms[int(new_room)]
                Adventure.forced(self, direction)

        # Second, we check if the room has an item
        if any(self.current_room.inventory.inventory) == False:
            pass
        else:
            # If an item is found, then we let the player know about it
            for key, value in self.current_room.inventory.inventory.items():
                print(f"{key}: {value}")

        pass

    def take(self, command, item, key):
        """
        Implements a TAKE function, which adds an item to
        players inventory
        """
        # Check if command is TAKE
        if command.upper() == "TAKE":
            # Add item to player inventory and remove it from room inventory
            self.player.add(item)
            self.current_room.inventory.remove(key)
            print(f"{key} taken.")

        # Check if command is DROP
        elif command.upper() == "DROP":
            # Remove item from player inventory and add it to room inventory
            self.current_room.inventory.add(item)
            self.player.remove(key)
            print(f"{key} dropped.")

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n"
              "\n"
              "Type HELP to get started\n")

        print(self.current_room.description)

        # Prompt the user for commands until they've won the game.

        while not self.game_over():
            command = input("> ")
            command = command.upper()

            # Check if the command is a movement or not.
            if self.current_room.is_connected(command):
                # Performs a move based on the direction
                Adventure.move(self, command)

            # If the command is "TAKE"
            elif "TAKE" in command:
                # Split user input into two strings, and avoid other inputs
                try:
                    command, name = command.split()
                except ValueError:
                    print("Invalid command.")
                else:
                    # Check if command is something else than "TAKE"
                    if command != "TAKE":
                        print("Invalid command.")
                    # If item is in player's inventory or current room doesn't have the item, we let the player know
                    elif name in self.player.inventory.keys() or name not in self.current_room.inventory.inventory.keys():
                        print("No such item.")
                    else:
                        # Otherwise, we get the value by using get(name)
                        value = self.current_room.inventory.inventory.get(name)
                        # If room has more than 1 item, we have to check that the player doesn't have it already
                        item = {name: value}
                        Adventure.take(self, command, item, name)

            # If player drops an item
            elif "DROP" in command:
                # Split user input into to strings, and avoid other inputs
                try:
                    command, name = command.split()
                except ValueError:
                    print("Invalid command.")
                else:
                    # Check if command is "DROP"
                    if command != "DROP":
                        print("Invalid command.")
                    # If item is in current room's inventory or player doesn't have the item, we let the player know
                    elif name in self.current_room.inventory.inventory.keys() or name not in self.player.inventory.keys():
                        print("No such item.")
                    else:
                        # Otherwise, we get the value by using get(name)
                        value = self.player.inventory.get(name)
                        # If room has more than 1 item, we have to check that the player doesn't have it already
                        item = {name: value}
                        Adventure.take(self, command, item, name)

            # Outputs player's inventory
            elif command == "INVENTORY":
                if not self.player.inventory:
                    print("Your inventory is empty.")
                else:
                    for key, value in self.player.inventory.items():
                        print(f"{key}: {value}")

            # Outputs game instructions
            elif command == "HELP":
                print("You can move by typing directions such as EAST/WEST/IN/OUT.")
                print("QUIT quits the game.")
                print("HELP prints instructions for the game.")
                print("INVENTORY lists the item in your inventory.")
                print("LOOK lists the complete description of the room and its contents.")
                print("TAKE <item> take item from the room.")
                print("DROP <item> drop item from your inventory.")

            # Prints the current room's description and its items if it have any
            elif command.upper() == "LOOK":
                print(self.current_room.description)
                if not any(self.current_room.inventory.inventory) == False:
                    for key, value in self.current_room.inventory.inventory.items():
                        print(f"{key}: {value}")
                else:
                    pass

            # Quit's game
            elif command.upper() == "QUIT":
                print("Thanks for playing!")
                return 0

            else:
                print("Invalid command")
                pass


if __name__ == '__main__':
    adventure = Adventure("Crowther")
    adventure.play()
