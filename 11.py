from tqdm import trange

nums = open('11_input.txt').readlines()[0].strip().split(' ')
nums = [int(num) for num in nums]

nums = {k:nums.count(k) for k in set(nums)}

# def do_rules(nums):
#     new_nums = []
#     for i in range(len(nums)):
#         num = nums[i]
#         if num == 0:
#             new_nums.append(1)
#         elif len(str(num)) % 2 == 0:
#             left = num // (10 ** (len(str(num)) //2))
#             right = num % (10 ** (len(str(num)) //2))
#             # print(left, right)
#             new_nums.append(left)
#             new_nums.append(right)
#         else:
#             new_nums.append(num * 2024)
#     return new_nums


def do_rules(nums):
    new_nums = {}
    for n in nums: # nums is a dict
        if n == 0:
            if 1 not in new_nums:
                new_nums[1] = 0
            new_nums[1] += nums[0]
        elif len(str(n)) % 2 == 0:
            n = str(n)
            left = int(n[:len(n) // 2])
            right = int(n[len(n) // 2:])
            n=int(n)
            if left not in new_nums:
                new_nums[left] = 0
            if right not in new_nums:
                new_nums[right] = 0
            new_nums[left] += nums[n]
            new_nums[right] += nums[n]
        else:
            if n * 2024 not in new_nums:
                new_nums[n * 2024] = 0
            new_nums[n * 2024] += nums[n]

    return new_nums

for i in trange(75):
    nums = do_rules(nums)

print(sum(nums.values()))