import numpy as np
import matplotlib.pyplot as plt
import os

directory = os.getcwd() + "\\tutoring-files\\multiplication\\"
times = {}
plt.rcParams.update({'font.size': 8})


for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    if not os.path.isfile(f):
        continue
    file = open(f, "r")
    lines = file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "times" in line:
            num1loc = line.index("times") - 2
            if line[num1loc - 1] == " ":    
                num1 = int(line[num1loc])
            else: num1 = int(line[num1loc]) + 10

            num2loc = line.index("times") + len("times ")
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
                if "times" in newLine:
                    break
                j += 1
            
            if not answerExists:
                i += 1
                continue
            
            j -= 1 # j is now the index of the line just before the next question
            time = float(lines[j]) # i.e. the time of this question
            if time > 30:
               time = 30

            if (num1, num2) not in times:
                times[(num1, num2)] = [time]
            else:
                times[(num1, num2)].append(time)
        i += 1

for thing in times:
    times[thing] = round(np.mean(times[thing]), 2)

heatmap = np.zeros((11, 11))

for thing in times:
    heatmap[thing[0] - 2][thing[1] - 2] = times[thing]

# From: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
nums1 = [str(i+2) for i in range(11)]
nums2 = [str(i+2) for i in range(11)]

fig, ax = plt.subplots()
im = ax.imshow(heatmap, cmap="OrRd")

ax.set_xticks(range(len(nums1)), labels=nums1,
              rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticks(range(len(nums2)), labels=nums2)

for i in range(len(nums1)):
    for j in range(len(nums2)):
        text = ax.text(j, i, heatmap[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Times tables")
fig.tight_layout()
plt.show()
