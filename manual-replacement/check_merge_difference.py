
import os, sys

folder1 = sys.argv[1]
folder2 = sys.argv[2]

list1 = os.listdir(folder1)
list2 = os.listdir(folder2)

missing_list2 = []
for l in list1:
    if l not in list2:
        missing_list2.append(os.path.splitext(l)[0])

missing_list1 = []
for l in list2:
    if l not in list1:
        missing_list1.append(os.path.splitext(l)[0])

with open("merge_diff.txt", "w", encoding="utf-8") as f:
    f.write("Missing on list 1 (" + folder1 + "):\n")
    for m in missing_list1:
        f.write(m + "\n")
        
    f.write("\nMissing on list 2 (" + folder2 + "):\n")
    for m in missing_list2:
        f.write(m + "\n")

print("List created successfully!")
print(len(missing_list1), "missing on", folder1)
print(len(missing_list2), "missing on", folder2)
