inputFile = open("uvsensor.txt", "r")
num_list = [float(num) for num in inputFile.read().split()]
# OR, num_list = map(float, inputFile.read().split())

counter = len(num_list)
total = sum(num_list)

# Your desired values
max_val = max(num_list)
min_val = min(num_list)

print(max_val)
