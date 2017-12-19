import math
from six.moves import xrange
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import operator


def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(x1 - x2) + abs(y1 - y2)

    return dist


class TruckRoutefinder(object):

    def __init__(self, locations, demands, num_vehicles, vehicle_capacity):
        self.locations = locations
        self.demands = demands
        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity

    def find_route(self):
        # Create the data.
        data = create_data_array()
        num_locations = len(self.locations)
        depot = 0  # The depot is the start and end point of each route.

        # Create routing model.
        if num_locations > 0:
          routing = pywrapcp.RoutingModel(num_locations, self.num_vehicles, depot)
          search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

          # Callback to the distance function.
          dist_between_locations = CreateDistanceCallback(self.locations)
          dist_callback = dist_between_locations.Distance
          routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

          # Put a callback to the demands.
          demands_at_locations = CreateDemandCallback(self.demands)
          demands_callback = demands_at_locations.Demand

          # Add a dimension for demand.
          slack_max = 0
          fix_start_cumul_to_zero = True
          demand = "Demand"
          routing.AddDimension(demands_callback, slack_max, self.vehicle_capacity,
                               fix_start_cumul_to_zero, demand)

          # Solve, displays a solution if any.
          print("eh: " +str(self.num_vehicles))
          assignment = routing.SolveWithParameters(search_parameters)
          if assignment:
            # Display solution.
            # Solution cost.
            print("Total distance of all routes: " + str(assignment.ObjectiveValue()) + "\n")
            vehicle_routes = [None] * self.num_vehicles
            route_demands  = {}
            for vehicle_nbr in range(self.num_vehicles):
              index = routing.Start(vehicle_nbr)
              index_next = assignment.Value(routing.NextVar(index))
              route = ''
              route_dist = 0
              route_demand = 0
              vehicle_routes[vehicle_nbr] = []

              while not routing.IsEnd(index_next):
                node_index = routing.IndexToNode(index)
                node_index_next = routing.IndexToNode(index_next)
                route += str(node_index) + " -> "
                vehicle_routes[vehicle_nbr].append(self.locations[node_index])
                # Add the distance to the next node.
                route_dist += dist_callback(node_index, node_index_next)
                # Add demand.
                route_demand += self.demands[node_index_next]
                index = index_next
                index_next = assignment.Value(routing.NextVar(index))


              node_index = routing.IndexToNode(index)
              node_index_next = routing.IndexToNode(index_next)
              route += str(node_index) + " -> " + str(node_index_next)
              vehicle_routes[vehicle_nbr].append(self.locations[node_index])
              vehicle_routes[vehicle_nbr].append(self.locations[node_index_next])

              route_dist += dist_callback(node_index, node_index_next)
              route_demands[vehicle_nbr] = route_demand
              # print("Route for vehicle " + str(vehicle_nbr) + ":\n\n" + route + "\n")
              # print("Distance of route " + str(vehicle_nbr) + ": " + str(route_dist))
              # print("Demand met by vehicle " + str(vehicle_nbr) + ": " + str(route_demand) + "\n")

            sorted_d = sorted(route_demands.items(), key=operator.itemgetter(0))
            sorted_routes = [None] * self.num_vehicles
            print("dems: " + str(route_demands))
            print("veh: " + str(vehicle_routes))

            for idx, val in enumerate(vehicle_routes):
                sorted_routes[idx] = vehicle_routes[sorted_d[idx][0]]

            accepted_routes = []
            for veh in sorted_routes:
                print(len(veh))
                if len(veh) > 2:
                    accepted_routes.append(veh)

            return accepted_routes
          else:
            print('No solution found.')
        else:
          print('Specify an instance greater than 0.')



class CreateDistanceCallback(object):
  """Create callback to calculate distances between points."""

  def __init__(self, locations):
    """Initialize distance array."""
    size = len(locations)
    self.matrix = {}

    for from_node in xrange(size):
      self.matrix[from_node] = {}
      for to_node in xrange(size):
        x1 = locations[from_node][0]
        y1 = locations[from_node][1]
        x2 = locations[to_node][0]
        y2 = locations[to_node][1]
        self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

  def Distance(self, from_node, to_node):
    return int(self.matrix[from_node][to_node])

# Demand callback
class CreateDemandCallback(object):
  """Create callback to get demands at each location."""

  def __init__(self, demands):
    self.matrix = demands

  def Demand(self, from_node, to_node):
    return self.matrix[from_node]


def create_data_array():

  locations = [[82.235, 76], [96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39],
               [14, 24], [12, 39], [3, 82], [5, 10], [98, 52], [84, 25], [61, 59], [1, 65],
               [88, 51], [91, 2], [19, 32], [93, 3], [50, 93], [98, 14], [5, 42], [42, 9],
               [61, 62], [9, 97], [80, 55], [57, 69], [23, 15], [20, 70], [85, 60], [98, 5],]

  demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18,
             19, 1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9]
  data = [locations, demands]
  return data

def main():
    d = create_data_array()

    tr = TruckRoutefinder(d[0], d[1], 5, 100)
    tr.find_route()

if __name__ == '__main__':
  main()