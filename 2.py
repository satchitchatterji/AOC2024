def safe_line(nums):
    # first condition
    if nums == sorted(nums) or nums[::-1] == sorted(nums):
        pass
    else:
        return False
    
    # second condition
    for i, num2 in enumerate(nums[1:]):
        num1 = nums[i]
        # print(num1, num2, abs(num1-num2))
        if abs(num1-num2) not in [1,2,3]:
            return False
    
    return True

def safe_damper(nums):
    for i, num in enumerate(nums):
        nums_copy = nums[:i]+nums[i+1:]
        if safe_line(nums_copy):
            return True
    return False

safe_lines = 0

with open("2_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        nums = [int(x.strip()) for x in line.split()]
        if safe_line(nums):
            safe_lines += 1
        elif safe_damper(nums):
            safe_lines += 1

print(safe_lines)
