class Inventory(object):
    """
    Representation of a inventory
    """
    def __init__(self):
        """
        Initialize inventory
        """
        self.inventory = {}

    def add(self, item):
        """
        Adds an item to the inventory, and checks
        that we do not ecounter any KeyErrors
        """
        try:
            self.inventory.update(item)
        except KeyError:
            print("Invalid command")

    def remove(self, item_name):
        """
        Removes an item form the inventory, and checks
        that we do not ecounter any KeyErrors
        """
        try:
            self.inventory.pop(item_name)
        except KeyError:
            print("Invalid command")

    def __str__(self):
        for key, value in self.inventory.items():
            return(f"{key}:{value}")