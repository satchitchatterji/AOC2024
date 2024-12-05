import numpy as np

all_nums = []
with open("4_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        letters = [x for x in line.strip()]
        all_nums.append(letters)

def arr_to_str_list(arr):
    str_list = []
    for row in arr:
        str_list.append("".join(row))

    return str_list

all_nums = np.array(all_nums)

def get_horizontal_matches(arr, string):
    arr = arr_to_str_list(arr)
    matches = 0
    for row in arr:
        matches += row.count(string)
    return matches

def get_diagonal_matches(arr,string):
    matches = 0
    for idx_diag in range(-len(arr)+1, len(arr)):
        row = "".join(np.diagonal(arr,idx_diag))
        matches += row.count(string)
    return matches

matches = 0
# puzzle 1
matches += get_horizontal_matches(all_nums, "XMAS") # horizontal
matches += get_horizontal_matches(all_nums.T, "XMAS") # vertical
matches += get_horizontal_matches(all_nums, "SAMX") # horizontal backwards
matches += get_horizontal_matches(all_nums.T, "SAMX") # vertical backwards

matches += get_diagonal_matches(all_nums, "XMAS") # main diagonals
matches += get_diagonal_matches(all_nums[::-1,:], "XMAS") # vertical, off-diagonals
matches += get_diagonal_matches(all_nums, "SAMX") # reverse, main diagonals
matches += get_diagonal_matches(all_nums[::-1,:], "SAMX") # reverse, off-diagonals

# print(matches)

def window_match(arr, pattern):
    # faster to do convolve/correlation
    matches = 0
    for idx_row in range(len(arr)-len(pattern)+1):
        for idx_col in range(len(arr[0])-len(pattern[0])+1):
            match = True
            for idx_row_pattern in range(len(pattern)):
                for idx_col_pattern in range(len(pattern[0])):
                    if not match:
                        break
                    if pattern[idx_row_pattern, idx_col_pattern] == "~":
                        continue
                    if pattern[idx_row_pattern, idx_col_pattern] != arr[idx_row+idx_row_pattern, idx_col+idx_col_pattern]:
                        match = False
            
            matches += match
    
    return matches

pattern = np.array([["M", "~", "S"],
                    ["~", "A", "~"],
                    ["M", "~", "S"]])


matches = 0
matches += window_match(all_nums, pattern)
matches += window_match(all_nums, np.rot90(pattern,k=1))
matches += window_match(all_nums, np.rot90(pattern,k=2))
matches += window_match(all_nums, np.rot90(pattern,k=3))

print(matches)