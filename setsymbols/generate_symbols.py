import edges, rarity, gradient
import sys


base_path = sys.argv[1]
thickness = int(sys.argv[2])

edge_path, big_path = edges.generate_edge_mask(base_path, thickness)

for color in gradient.colors:
    rarity.make_icon(edge_path, big_path, f'{color}_gradient.png', f"{base_path[:-4]}_{color}.png")