import random
import networkx as nx
import numpy as np
import pylab
from shapely.geometry import MultiPoint, Point


def dist(p1, p2):
    """
    Accepts 2 Vertices from the Vertex class
    and returns the distance between them
    :param p1: --> Tuple of coordinates
    :param p2: --> Tuple of coordinates
    """
    # set shortcuts for the variables
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]

    # or... sqrt( (x1-x2)^2 + (y1-y2)^2 ) <- basic Euclidean distance
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5


def slope(x1, x2):
    """
    Return the slope of the 2 points given
    :param x1: Tuple of coordinates
    :param x2: Tuple of coordinates
    :return:
    """

    a = x1[1]
    b = x1[0]
    c = x2[1]
    d = x2[0]

    e = a - c
    f = b - d

    try:
        g = e/f
    except ZeroDivisionError:
        return f

    return g


def calc_converge(x, x1, y, y1):
    """
    return true if there is an intersection between the
    two lines.
    :param x: tuple
    :param x1: tuple - edge with x
    :param y: tuple
    :param y1: tuple - edge with y
    :return: bool - True if intersect point, False if no solution
    """

    m1 = slope(x, x1)               # calculate the slope of line 1
    a1 = -1 * m1                    # attached to x coordinate which = -slope
    b1 = 1                          # assume constant
    c1 = -1 * ((m1 * x[0]) - x[1])  # y-intercept constant

    m2 = slope(y, y1)                # store the slope
    a2 = -1 * m2                     # attached to x coordinate which = -slope
    b2 = 1                           # assume constant
    c2 = -1 * ((m2 * y[0]) - y[1])   # y-intercept constant

    # create the two matrices
    mata = np.array([[a1, b1], [a2, b2]])  # one with the lines
    matb = np.array([c1, c2])              # one with the solutions

    try:
        s = np.linalg.solve(mata, matb)  # by the power of numpy!
    except np.linalg.LinAlgError:
        return False

    shape = MultiPoint([x, x1, y, y1]).convex_hull
    intersect = Point(s)

    result = intersect.within(shape)

    return result


class TwoOpt:
    """
    Receive the input of the File_Data type,
    perform the heuristic on it, and output
    the data as another File_Data
    """
    def __init__(self, i):
        """
        This initializes the Greedy class.  input is a
        File_Data class that stores all the information
        it needs to compute the solution

        :param i: File_Data used for all process
        :return:
        """
        self.data = i.dict
        self.graph = nx.Graph()
        self.randomize()
        # counters for the while loops
        self.counter = 0
        self.fig = pylab.figure()

    def randomize(self):
        """
        This function randomizes the graph that is
        instantiated in the class.  This function
        returns nothing; it serves only to
        randomize the current graph.
        :return:
        """

        # shortcuts for quick references
        l = self.data.keys()  # make a list of the vertices

        f = random.choice(l)  # pick a random first place
        visited = list()  # initialize an empty visited list
        visited.append(f)  # add the first city to the list

        # while the number of visited nodes is less
        # than the number of entries in the list
        while len(visited) < len(l):
            n = random.choice(l)  # select a random choice

            # If the node hasn't been visited
            if n not in visited:
                visited.append(n)  # Append the visited list

        # Add the final connection between the
        # last node visited and the first node
        visited.append(f)
        self.graph.add_path(visited)

    def _switch(self, a, b, c, d):
        g = self.graph
        # Add in the new edges
        g.add_edge(a, c)
        g.add_edge(b, d)
        # Remove the edges
        g.remove_edge(a, b)
        g.remove_edge(c, d)

    def _check_solution(self, a, b, c, d):
        g = self.graph
        results = list()

        self._switch(a, b, c, d)  # reorients to a-c b-d

        for i in g.nodes():
            if len(g[i]) == 2:
                # print "Sufficient connections"
                results.append(True)
            else:
                # print "Error in connections. . ."
                results.append(False)

        # print results

        f = True
        for e in results:
            f = f and e

        self._switch(a, c, b, d)  # undo the swap
        return f

    def _get_fig(self):
        nx.draw(self.graph, self.data, node_color="green", node_size=400, with_labels=True)

    def _update_screen(self):
        pylab.clf()             # clear the buffer
        self._get_fig()         # get the figure with the new data
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # pylab.pause(1)

    def sort(self):
        """
        This function performs the '2-opt' sorting
        function.  Number of rounds is the number of times
        the number of turns are performed.  A turn is the
        number of comparisons checked and changed.
        :return: Graph()
        """

        # shortcuts for reference
        g = self.graph
        nm = self.data

        pylab.show()
        self._update_screen()
        no_change = 0

        while no_change <= 10000:
            count1 = 0
            while count1 < len(g.edges()):
                count2 = 0
                while count2 < len(g.edges()):

                    e1 = g.edges()[count1]
                    e2 = random.choice(g.edges())

                    if e1 != e2:

                        a = e1[0]
                        b = e1[1]
                        c = e2[0]
                        d = e2[1]

                        # If there was a collision between the 2 edges,
                        if calc_converge(nm[a], nm[b], nm[c], nm[d]):
                            if (dist(nm[a], nm[b]) + dist(nm[c], nm[d])) > \
                               (dist(nm[a], nm[c]) + dist(nm[b], nm[d]))\
                                    and self._check_solution(a, b, c, d):
                                print "Switch Out!"
                                self._switch(a, b, c, d)
                                no_change = 0
                                self._update_screen()
                                break
                            elif(dist(nm[a], nm[b]) + dist(nm[c], nm[d])) > \
                                (dist(nm[a], nm[c]) + dist(nm[b], nm[d]))\
                                    and self._check_solution(b, a, c, d):
                                print "Switch Out!"
                                # self._switch(b, a, c, d)
                                no_change = 0
                                self._update_screen()
                                break

                    count2 += 1
                    no_change += 1

                count1 += 1
