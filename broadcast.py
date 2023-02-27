from ns import ns
import sys

cmd = ns.core.CommandLine()
cmd.Parse(sys.argv)

# Create 10 nodes
nodes = ns.network.NodeContainer()
nodes.Create(10)


# Read node connections from a text file
connections_file = open("./integration_tests/test/gen_data", "r")
connections = []