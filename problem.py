import pandas as pd
import numpy as np

class DeploymentProblem:

    def __init__(self, regions, adjacent, locations, namb, demand, coverage, train_indices, test_indices):

        self.namb = namb

        #regions = parse through hourly_calls dataframe from column 5 to end and convert to int array
        self.nregions = regions

        #locations = first array from coverage dataframe
        self.nlocations = len(locations)

        #adjacent = an array from the adjacent_nbhd true or false instead of 1 or 0
        self.adjacency = adjacent

        #demand = convert hourly_calls dataframe to an array of just the number of calls and the first row is the neighborhood
        self.demand = demand

        self.coverage = coverage

        #indices = array of size numrows of hourly_calls
        #train_indices = array of all hourly_calls from 2012 january to march
        #test_indices = array of hourly_calls thats not from 2012 january to march
        self.train = train_indices
        self.test = test_indices
