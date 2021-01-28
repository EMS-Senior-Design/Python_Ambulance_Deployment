import gurobipy as gp
from gurobipy import GRB
import numpy as np

class Params:

    def __init__(self, alpha, conv, tol, nperiods, maxiter):
        self.alpha = alpha
        self.epsilon = conv
        self.tol = tol
        self.nperiods = nperiods
        self.maxiter = maxiter

class StochasticDeployment:

    def __init__(self, dep_problem):

        params = Params(0.01, 0.5, 1e-6, 500, 50)

        nperiods = min(len(dep_problem.train), params.nperiods)
        demand = dep_problem.demand[len(dep_problem.train):]
        I = range(dep_problem.nlocations)
        J = range(dep_problem.nregions)
        T = range(params.nperiods)

        m = gp.Model('StochasticDeployment')

        x = m.addMVar(dep_problem.nlocations, name="x_vars")
        y = m.addMVar((dep_problem.nlocations, dep_problem.nregions, params.nperiods), name="y_vars")
        z = m.addMVar((dep_problem.nregions,params.nperiods), name="z_vars")
        m.update()

        m.setObjective(z.sum(), GRB.MINIMIZE)
        const1 = m.addConstr((x.sum() <= dep_problem.nambulances))
        i_coverage = []
        j_coverage = []
        for j in J:
            for i in I:
                if dep_problem.coverage[j][i] == "true":
                    if i not in i_coverage:
                        i_coverage.append(i)
                    if j not in j_coverage:
                        j_coverage.append(j)
        i_coverage.sort()
        j_coverage.sort()

        for i in I:
            for t in T:
                A = np.ones((dep_problem.nregions))
                const = m.addConstr(x[i] >= sum(y[i][j][t]*A[j] for j in j_coverage))

        for j in J:
            for t in T:
                A = np.ones((dep_problem.nlocations))
                const = m.addConstr(z[j][t] >= demand[t][j] - sum(y[i][j][t]*A[i] for i in i_coverage))

        m.write("myfile.lp")


        self.model = m
        self.variables = x

