import os, sys
import json
import posixpath
import ntpath

# input: transcription file, character name, model id, language to read, file system type

# load transcriptions, it has to be in the quote JSON format
trans_path = sys.argv[1]
charname = sys.argv[2]
sid = sys.argv[3]
lang = sys.argv[4]
system_type = sys.argv[5]
with open(trans_path, "r", encoding="utf-8") as f:
    quotes = json.load(f)

filelist = []
for filename, entry in quotes.items():
    # each file has to be in wav format, the user
    # should handle the resampling later,
    # these always have to be .wav
    basename = os.path.splitext(filename)[0]
    if system_type == "posix":
        target_path = posixpath.join("wav", charname, basename + ".wav")
    elif system_type == "ntpath":
        target_path = ntpath.join("wav", charname, basename + ".wav")
    else:
        print("Invalid system type, choose posix or ntpath")
        sys.exit()
    
    # build filelist entry line
    quote = entry["quote"][lang]
    filelist.append(f"{target_path}|{sid}|{quote}")
    print(f"{target_path}|{sid}|{quote}")

# save filelist
with open(f"{charname}_train.txt", "w", encoding="utf-8") as f:
    for line in filelist:
        f.write(f"{line}\n")

print("List created successfully!")

