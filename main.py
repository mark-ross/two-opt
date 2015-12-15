from File import File
from TwoOpt import TwoOpt
import pylab

pylab.ion()  # make this interactive! Woo!


def main():

    f = "tsp-medium.tsp"
    j = File.read(f)  # to generate data, use the R_File.read access
    t = TwoOpt(j)  # returns an object ready to sort

    pylab.show()
    pylab.waitforbuttonpress()

    t.sort()  # one round of sorting

    # finally, once it's finished, just wait for button press
    pylab.waitforbuttonpress()
    pylab.close()


if __name__ == '__main__':
    main()