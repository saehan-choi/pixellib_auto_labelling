from collections import deque

deq = deque()
num_length = deque()
deq = deque([1, 2, 3, 4, 5])

num_length.append(int(len(deq)))

print(num_length[-1])