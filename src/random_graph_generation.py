import src.read_data
import src.vis
from src import graph
import random
import os


def true_random_layered_graph(k, n, d):
	"""
	:param k: number of layers
	:param n: number of nodes per layer
	:param d: average edge density of the resultant graph
	:return: LayeredGraph object g
	"""

	n_edges_per_layer = round(d * (n ** 2))
	assert n_edges_per_layer * (k - 1) >= n * k, "graph will not be connected"

	flip_edges = d > 0.5
	d = 1 - d if flip_edges else d

	while True:
		g = graph.LayeredGraph()
		n_edges_per_layer = round(d * (n ** 2))

		for i in range(k):  # add nodes
			for j in range(n):
				g.add_node(i + 1)

		for i in range(1, k):  # randomly, uniformly select edges
			n_added = 0
			while n_added < n_edges_per_layer:
				n1 = random.randint(0, n-1) + ((i - 1) * n)
				n2 = random.randint(0, n-1) + (i * n)
				if (n1, n2) not in g.edge_names:
					g.add_edge(n1, n2)
					n_added += 1
		if flip_edges:
			edges = set(g.edge_names.keys())
			g.edges = []
			g.edge_names = {}
			for i in range(1, k):
				for n1 in range((i - 1) * n, n + ((i - 1) * n)):
					for n2 in range(i * n, n + (i * n)):
						if (n1, n2) not in edges:
							g.add_edge(n1, n2)

		if g.is_connected():
			return g


def random_layered_graph_connect_help(k, n, d):
	"""
	:param k: number of layers
	:param n: number of nodes per layer
	:param d: average edge density of the resultant graph
	:return: LayeredGraph object g
	"""

	n_edges_per_layer = round(d * (n ** 2))
	assert n_edges_per_layer * (k - 1) >= n * k, "graph will not be connected"

	flip_edges = d > 0.5
	d = 1 - d if flip_edges else d

	while True:
		g = graph.LayeredGraph()
		n_edges_per_layer = round(d * (n ** 2))

		for i in range(k):  # add nodes
			for j in range(n):
				g.add_node(i + 1)

		not_seen = set(range(n * k))
		for i in range(1, k):  # randomly, uniformly select edges
			n_added = 0
			not_seen_l1 = set((x for x in not_seen if ((i - 1) * n) <= x < n + ((i - 1) * n)))
			if i == k - 1:
				not_seen_l2 = set((x for x in not_seen if (i * n) <= x < n + (i * n)))
			while n_added < n_edges_per_layer:
				n1 = random.randint(0, n-1) + ((i - 1) * n)
				while len(not_seen_l1) == n_edges_per_layer - n_added and n1 not in not_seen_l1:
					n1 = random.randint(0, n - 1) + ((i - 1) * n)
				n2 = random.randint(0, n-1) + (i * n)
				if i == k - 1:
					while len(not_seen_l2) == n_edges_per_layer - n_added and n2 not in not_seen_l2:
						n2 = random.randint(0, n-1) + (i * n)
				if (n1, n2) not in g.edge_names:
					g.add_edge(n1, n2)
					n_added += 1
					if n1 in not_seen:
						not_seen.remove(n1)
						not_seen_l1.remove(n1)
					if n2 in not_seen:
						not_seen.remove(n2)
						if i == k - 1:
							not_seen_l2.remove(n2)
		if flip_edges:
			edges = set(g.edge_names.keys())
			g.edges = []
			g.edge_names = {}
			for i in range(1, k):
				for n1 in range((i - 1) * n, n + ((i - 1) * n)):
					for n2 in range(i * n, n + (i * n)):
						if (n1, n2) not in edges:
							g.add_edge(n1, n2)

		if g.is_connected():
			return g


def generate_gange_dataset(seed=None):
	if seed is not None:
		random.seed(seed)

	if "random graphs" not in os.listdir(".."):
		os.mkdir("../random graphs")
	if "gange" not in os.listdir("../random graphs"):
		os.mkdir("../random graphs/gange")

	for k in range(3, 11):
		for n in range(7, 11 if k < 5 else (10 if k < 8 else 9)):
			if f"g{k}_{n}" not in os.listdir("../random graphs/gange"):
				os.mkdir(f"../random graphs/gange/g{k}_{n}")
			for i in range(10):
				ng = true_random_layered_graph(k, n, 0.2)
				ng.write_out(f"../random graphs/gange/g{k}_{n}/graph{i}.lgbin")


def generate_random_density_set(seed=None):
	if seed is not None:
		random.seed(seed)

	if "random graphs" not in os.listdir(".."):
		os.mkdir("../random graphs")
	if "density_exp" not in os.listdir("../random graphs"):
		os.mkdir("../random graphs/density_exp")

	for d in range(14, 51, 2):
		if f"d{d}" not in os.listdir("../random graphs/density_exp"):
			os.mkdir(f"../random graphs/density_exp/d{d}")
		for i in range(10):
			ng = true_random_layered_graph(5, 10, d / 100)
			print(f"d={d} graph {i}")
			ng.write_out(f"../random graphs/density_exp/d{d}/graph{i}.lgbin")


def generate_random_fixed_density_set(seed=None):
	if seed is not None:
		random.seed(seed)

	if "random graphs" not in os.listdir(".."):
		os.mkdir("../random graphs")
	if "fixed_density_exp" not in os.listdir("../random graphs"):
		os.mkdir("../random graphs/fixed_density_exp")

	for k in range(3, 21):
		if f"k{k}" not in os.listdir("../random graphs/fixed_density_exp"):
			os.mkdir(f"../random graphs/fixed_density_exp/k{k}")
		for i in range(10):
			ng = random_layered_graph_connect_help(k, 10, 0.15)
			print(f"k={k} graph {i}")
			ng.write_out(f"../random graphs/fixed_density_exp/k{k}/graph{i}.lgbin")


if __name__ == '__main__':
	# generate_gange_dataset(seed=22)
	# generate_random_density_set(seed=49)
	# generate_random_fixed_density_set(seed=71)

	gr = src.read_data.read("../random graphs/fixed_density_exp/k20/graph2.lgbin")
	src.vis.draw_graph(gr, "rand", gravity=True, nested=True)
