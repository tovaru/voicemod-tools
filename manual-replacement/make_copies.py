import os, sys
import shutil

source_file_path = sys.argv[1]
target_list_path = sys.argv[2]
output_dir = sys.argv[3]

with open(target_list_path, "r", encoding="utf-8") as f:
    filelist = f.read().splitlines()

sourceformat = os.path.basename(source_file_path)
sourceformat = os.path.splitext(sourceformat)[1]
for file in filelist:
    newpath = os.path.join(output_dir, file + sourceformat)
    shutil.copy(source_file_path, newpath)
    print("Generated: " + file)

print("Finished making copies on " + output_dir)
