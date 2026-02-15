import os.path
import os
from itertools import cycle


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


df_list = [int(x) for x in data.splitlines()]

print("Part 1:", sum(df_list))

f = 0
seen = {0}
for df in cycle(df_list):
    f += df
    if f in seen:
        break
    seen.add(f)
    
    
print("Part 2:", f)

