from File_Data import File_Data
import re


class File:
    """
    A class for reading and writing to the files.

    Two static methods,
    read(f)
    write(name,dime,list)

    read reads from the file passed in the parameters
    and returns a File_Data structure.

    write takes a name, number of dimensions, and an ordered
    list and writes it to a file with <name>.tour as the name
    """
    @staticmethod
    def read(f):
        """
        Open the file, and store its contents
        :return:
        """
        f = open(f, "r")
        data = File_Data()

        # Set up the search queries for the RE
        name = "NAME:\s(.*).tsp"
        dime = "DIMENSION:\s(\d+)"
        nums = "(\d*) (\d*) (\d*)"

        # Since we know there are 6 lines at the top
        # Run through them to get to the meaty portion
        # of the file, while tagging the name and dimension
        for _ in range(6):
            l = f.readline()
            n = re.search(name, l)
            d = re.search(dime, l)
            if n:
                data.name = n.group(1)
            elif d:
                data.num_v = d.group(1)

        # Until EOF, input and add the
        # numbers to the dictionary
        for line in f:
            n = re.search(nums, line)
            if n:
                data.add_point(int(n.group(1)),
                               int(n.group(2)),
                               int(n.group(3)))

        f.close()  # close the file
        return data

    @staticmethod
    def write_graph(name, dime, g):

        dime = str(dime)
        out_file = name
        out_file += ".tour"
        f = open(out_file,"w")
        f.write("NAME: ")
        f.write(out_file)
        f.write("\n")
        f.write("TYPE: TOUR\n")
        f.write("DIMENSION: ")
        f.write(dime)
        f.write("\n")
        f.write("TOUR_SECTION\n")

        l = g.vertices()  # generate a list of vertices
        a = l[0]          # set a to the first in the list
        count = 0  # set counter to 0
        s = a  # starting position = a
        first = s  # first position is also initial start
        p = s  # set the previous to the initial start too

        # while start/current node != first node
        # or while the count is 0
        while first != s or count == 0:
            l = g.out_vertices(s)  # generate the list of possible jumps
            n = l[0]  # generate the next leap
            if n != p:   # if the next isn't the previous

                f.write(s.label)  # write the label to the file
                f.write("\n")  # add a newline...

                count += 1   # add one to the counter
                p = s    # set the previous to the current
                s = n    # set the current to the next, and repeat
            else:        # otherwise, make a new next node
                n = l[1]     # Repeat...
                if n != p:   # if the next isn't the previous node
                    f.write(s.label)  # write the label to the file
                    f.write("\n")  # add a newline...
                    count += 1   # add one to the counter
                    p = s    # set the previous to the current
                    s = n    # set the current to the next, and repeat
        f.write("-1")  # write the final line
        f.close()      # close the file

    @staticmethod
    def write(name, dime, l):
        """
        This function writes the solution of the heuristic
        to a file with the extension '.tour'. Then it
        writes out the numbers in order.

        :param name: --> String name of file
        :param dime: --> Integer Number of Vertices
        :param l: --> Ordered list of solution
        :return:
        """
        dime = str(dime)

        out_file = name
        out_file += ".tour"

        f = open(out_file,"w")
        f.write("NAME: ")
        f.write(out_file)
        f.write("\n")

        f.write("TYPE: TOUR\n")

        f.write("DIMENSION: ")
        f.write(dime)
        f.write("\n")

        f.write("TOUR_SECTION\n")

        for i in l:
            f.write(str(i))
            f.write("\n")

        f.write("-1")
        f.close()
