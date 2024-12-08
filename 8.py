import numpy as np

full_map = []
with open("8_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        letters = [x for x in line.strip()]
        full_map.append(letters)

full_map = np.array(full_map)
full_map_shape = full_map.shape

signal_types = set(full_map.flatten().tolist())
signal_types.remove('.')

maps = {k:np.full(full_map_shape, '.') for k in signal_types}

full_map = full_map.flatten()
for antenna_type, map in maps.items():
    map = map.flatten()
    antennas = np.where(full_map==antenna_type)
    map[antennas] = antenna_type
    maps[antenna_type] = map.reshape(full_map_shape)

antinode_maps = {k:np.full(full_map_shape, '.') for k in signal_types}
for antenna_type, map in maps.items():
    antinode_map = antinode_maps[antenna_type]
    antennas = np.where(map==antenna_type)
    antennas = list(zip(antennas[0], antennas[1]))
    for a_idx, antenna1 in enumerate(antennas):
        for b_idx, antenna2 in enumerate(antennas):
            if a_idx < b_idx:
                x_dist, y_dist = antenna2[0]-antenna1[0], antenna2[1]-antenna1[1]
                # follow pattern for x_dist, y_dist to make two new antennas
                # new_antinode1 = (antenna1[0]-x_dist, antenna1[1]-y_dist)
                # new_antinode2 = (antenna2[0]+x_dist, antenna2[1]+y_dist)
                # if not(new_antinode1[0] < 0 or new_antinode1[1] < 0 or new_antinode1[0] >= full_map_shape[0] or new_antinode1[1] >= full_map_shape[1]):
                #     antinode_map[new_antinode1] = "#"
                # if not(new_antinode2[0] < 0 or new_antinode2[1] < 0 or new_antinode2[0] >= full_map_shape[0] or new_antinode2[1] >= full_map_shape[1]):
                #     antinode_map[new_antinode2] = "#"
                # now we can have many antinodes in a line for each pair of antennas
                for i in range(0, len(full_map)): # we can have up to len(full_map) antinodes, but TODO: we can stop early if we reach the edge of the map
                    new_antinode1 = (antenna1[0]-x_dist*i, antenna1[1]-y_dist*i)
                    new_antinode2 = (antenna2[0]+x_dist*i, antenna2[1]+y_dist*i)
                    if not(new_antinode1[0] < 0 or new_antinode1[1] < 0 or new_antinode1[0] >= full_map_shape[0] or new_antinode1[1] >= full_map_shape[1]):
                        antinode_map[new_antinode1] = "#"
                    if not(new_antinode2[0] < 0 or new_antinode2[1] < 0 or new_antinode2[0] >= full_map_shape[0] or new_antinode2[1] >= full_map_shape[1]):
                        antinode_map[new_antinode2] = "#"
    antinode_maps[antenna_type] = antinode_map


# combined antinode map
combined_antinode_map = np.full(full_map_shape, ".")
for antinode_map in antinode_maps.values():
    combined_antinode_map[antinode_map=="#"] = "#"

total_antinodes = np.sum(combined_antinode_map=="#")
print(total_antinodes)
