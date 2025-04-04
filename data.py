import numpy as np
import matplotlib.pyplot as plt
import os

operation = input("Operation? ")
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutoring-files", operation)
times = {}
plt.rcParams.update({'font.size': 8})

for filename in os.listdir(directory):
    print(f"\n{filename}: ", end='')
    tables = []
    f = os.path.join(directory, filename)
    if not os.path.isfile(f):
        continue
    file = open(f, "r")
    lines = file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if operation in line:
            num1loc = line.index(operation) - 2
            if line[num1loc - 1] == " ":    
                num1 = int(line[num1loc])
            else: num1 = int(line[num1loc]) + 10

            num2loc = line.index(operation) + len(operation)+1
            if line[num2loc + 1] == "?":
                num2 = int(line[num2loc])
            else:
                num2 = int(line[num2loc + 1]) + 10
                        
            j = i + 1
            answerExists = True
            for newLine in lines[i+1:]:
                if "[" in newLine: 
                    answerExists = False
                    break
                if operation in newLine:
                    break
                j += 1
            
            if not answerExists:
                i += 1
                continue
            
            j -= 1 # j is now the index of the line just before the next question
            time = float(lines[j]) # i.e. the time of this question
            if time > 20:
               time = 20

            if num1 not in tables:
                tables.append(num1)
                print(num1, end=' ')
            if (num1, num2) not in times:
                times[(num1, num2)] = [time]
            else:
                times[(num1, num2)].append(time)
        i += 1

print()
for thing in times:
    times[thing] = round(np.mean(times[thing]), 2)

offset = 2 if operation == "times" else 1
heatmap = np.zeros((9 + offset, 9 + offset))

for thing in times:
    heatmap[thing[0] - offset][thing[1] - offset] = times[thing]
    if operation == "plus":
        heatmap[thing[1] - offset][thing[0] - offset] = times[thing]

# From: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
nums1 = [str(i+offset) for i in range(9 + offset)]
nums2 = [str(i+offset) for i in range(9 + offset)]

fig, ax = plt.subplots()
im = ax.imshow(heatmap, cmap="OrRd")

ax.set_xticks(range(len(nums1)), labels=nums1,
              rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticks(range(len(nums2)), labels=nums2)

for i in range(len(nums1)):
    for j in range(len(nums2)):
        text = ax.text(j, i, heatmap[i, j],
                       ha="center", va="center", color="w")

ax.set_title(operation + " tables")
fig.tight_layout()
plt.show()
