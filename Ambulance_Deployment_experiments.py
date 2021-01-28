import csv
from datetime import datetime

from stochastic import StochasticDeployment
from problem import DeploymentProblem
from numpy import genfromtxt


beg = datetime.now()
locations = genfromtxt('./Julia_CSV_Converter/pythonData/locations.csv', delimiter=',')
adjacency = genfromtxt('./Julia_CSV_Converter/pythonData/adjacent.csv', delimiter=',')
demand = genfromtxt('./Julia_CSV_Converter/pythonData/demand.csv', delimiter=',')
train_indices = genfromtxt('./Julia_CSV_Converter/pythonData/train_indices.csv', delimiter=',')
test_indices = genfromtxt('./Julia_CSV_Converter/pythonData/test_indices.csv', delimiter=',')
regions = genfromtxt('./Julia_CSV_Converter/pythonData/regions.csv', delimiter=',')

# coverage = genfromtxt('./Julia_CSV_Converter/pythonData/coverage.csv', delimiter=',')
textfile = open('./Julia_CSV_Converter/pythonData/coverage.csv')
coverage = list(csv.reader(textfile))
# for line in textfile:
#     row_data = line.strip("\n").split()
#     for i, item in enumerate(row_data):
#         try:
#             row_data[i] = float(item)
#         except ValueError:
#             pass
#     coverage.append(row_data)

problem = DeploymentProblem(regions.size, adjacency, locations, 30, demand, coverage, train_indices, test_indices)
amb_deployment = []
for namb in range(30,55,5):
    print(namb)
    problem.nambulances = namb
    next_model = StochasticDeployment(problem)
    next_model.model.update()
    next_model.model.optimize()
    next_model.model.update()
    print(next_model.variables.tolist())
    for var in next_model.variables.tolist():
        print(var.X)
    amb_deployment.append(next_model.model.getVars())
print()
end = datetime.now()

run_time = (end-beg).strftime("%H:%M:%S")
print("Run Time =", run_time)
