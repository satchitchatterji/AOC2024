from tqdm import trange

data = open('9_input.txt').read().strip()

# part 1

def decompress(data):
    file = True
    file_idx = 0
    uncompressed = []
    for digit in data:
        if file:
            uncompressed += [file_idx] * int(digit)
            file_idx+=1
            file = False
        else:
            uncompressed += ['.' for  x in range(int(digit))]
            file = True
    return uncompressed

def check_reorg_complete(data_list):
    first_empty = data_list.index('.')
    return all([x=='.' for x in data_list[first_empty:]])

def compute_checksum(data_list):
    total = 0
    for pos, digit in enumerate(data_list):
        if digit != ".":
            total += pos * digit
    return total

def reorganize(data):
    num_ref = ['n' if n!='.' else '.' for n in data]
    while not check_reorg_complete(data):
        last_number_idx = len(num_ref) - 1 - num_ref[::-1].index('n')
        first_empty = data.index('.')
        data[last_number_idx], data[first_empty] = data[first_empty], data[last_number_idx]
        num_ref[last_number_idx], num_ref[first_empty] = num_ref[first_empty], num_ref[last_number_idx]
    return data

data1 = decompress(data)
data1 = reorganize(data1)
print(compute_checksum(data1))

# part 2

class Block:
    def __init__(self, pos, len, data):
        self.pos = pos
        self.len = len
        self.data = data

    def __str__(self):
        # print(type(self.len))
        return "".join([str(self.data) for _ in range(self.len)])
    
    def checksum_contribution(self):
        if self.data == ".":
            return 0
        total = 0
        for i in range(self.len):
            total += self.data*(self.pos+i)
        return total

def data_to_blocks(data_compressed):
    file = True
    file_idx = 0
    cur_pos = 0
    blocks = []
    for digit in data_compressed:
        if file:
            blocks.append(Block(pos=cur_pos, data=file_idx, len=int(digit)))
            cur_pos += int(digit)
            file_idx+=1
            file = False
        else:
            blocks.append(Block(pos=cur_pos, len=int(digit), data='.',))
            cur_pos += int(digit)
            file = True
    return blocks

def consolidate_empty_blocks(blocks):
    blocks = sorted(blocks, key=lambda x: x.pos)
    del_blocks = []
    for block1, block2 in zip(blocks[:-1], blocks[1:]):
        if block1.data == "." and block2.data == ".":
            block1.len += block2.len
            del_blocks.append(block2)
    
    for block in del_blocks:
        blocks.remove(block)
    return blocks

def reorganize2(blocks):
    max_idx = max([block.data for block in blocks if block.data!='.'])
    # print(decompress_blocks(blocks))
    for num in trange(max_idx, -1, -1):
        blocks = sorted(blocks, key=lambda x: x.pos)
        block_num = [block for block in blocks if block.data == num][0]
        for block in blocks:
            if block.data == '.':
                if block.len >= block_num.len and block.pos < block_num.pos:
                    if block.len > block_num.len:
                        blocks.append(Block(pos=block.pos+block_num.len, len=block.len-block_num.len, data='.'))
                        block.len = block_num.len
                    block.pos, block_num.pos = block_num.pos, block.pos
                    break
        blocks = consolidate_empty_blocks(blocks)

    return blocks


def compute_checksum_blocks(blocks):
    total = 0
    for block in blocks:
        if block.data != ".":
            total += block.checksum_contribution()
    return total


def decompress_blocks(blocks):
    data = ""
    blocks = sorted(blocks, key=lambda x: x.pos)
    for block in blocks:
        data += str(block)
    return data


data = data_to_blocks(data)
data = reorganize2(data)
print(compute_checksum_blocks(data))