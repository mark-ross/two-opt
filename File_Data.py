class File_Data:
    """
    A class for holding the data that is read from the file
    """

    def __init__(self):
        """
        Create an initializer that doesn't have any specific
        arguments so that it can be changed later
        :return:
        """
        self.name = ""
        self.dime = 0
        self.dict = {}

    def add_name(self, name):
        """
        Adds a name to the name
        parameter of the class
        :param name: String
        :return:
        """
        self.name = name

    def add_dimension(self, dime):
        """
        Adds a dimension to the class's
        num_v parameter
        :param dime: integer
        :return:
        """
        self.dime = dime

    def add_point(self, num, x, y):
        """
        Adds an entry to the dictionary
        using the first number as the index
        and the other two in a Point Structure
        :param num: = int num
        :param x: int x
        :param y: int y
        :return:
        """
        self.dict[num] = (x, y)

    def __repr__(self):
        """
        Print out the information in the class
            The name of the file
            The number of vertices
            The contents of the dictionary
        :return:
        """
        string = ""
        string += "Name of file: "
        string += self.name
        string += "\n"
        string += "Number of vertices: "
        string += self.dime
        string += "\n"
        string += "Dictionary..."
        string += "\n"
        for l in self.dict:
            string += str(l)
            string += ": ("
            string += str(self.dict[l].x)
            string += ","
            string += str(self.dict[l].y)
            string += ")\n"

        return string

    __str__ = __repr__