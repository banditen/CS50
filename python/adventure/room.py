from inventory import Inventory

class Room(object):

    """
    Representation of a room in Adventure
    """
    def __init__(self, id, name, description):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.routes = {}
        self.inventory = Inventory()

    def add_route(self, direction, room):
        """
        Adds a given direction and the connected room to our room object.
        """
        if direction not in self.routes:
            self.routes[direction] = room
        else:
            self.routes[direction].append(room)
        pass

    def is_connected(self, direction):
        """
        Checks whether the given direction has a connection from a room.
        Returns a boolean.
        """
        if direction in self.routes:
            return True
        else:
            return False

        pass

    def __repr__(self):
        return self.name
        return self.description
        return self.inventory