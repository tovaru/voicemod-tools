import os, sys
import json
import posixpath
import ntpath
import random

def makelist(quotes):
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
        #print(f"{target_path}|{sid}|{quote}")
    return filelist

def partition(filelist, ratio):
    # calculate number the number of the validation partition
    val_count = len(filelist) * ratio / 100
    val_count = int(val_count)

    # get n different elements from the filelist and use that as the validation data
    val_data = []
    train_data = filelist.copy() # don't modify the original filelist
    for n in range(val_count):
        # get a index inside the remaining training list items
        index = random.randint(0, len(train_data) - 1)

        # get the chosen item and remove it from the training list
        item = train_data.pop(index)

        # add it to the validation list
        val_data.append(item)

    return train_data, val_data
        

# input: transcription file, character name, model id, language to read, file system type
trans_path = sys.argv[1]
charname = sys.argv[2]
sid = sys.argv[3]
lang = sys.argv[4]
ratio = int(sys.argv[5])
system_type = sys.argv[6]

# load transcriptions, it has to be in the quote JSON format
with open(trans_path, "r", encoding="utf-8") as f:
    quotes = json.load(f)

# make list 
filelist = makelist(quotes)

# parition it between training and validation data
train, val = partition(filelist, ratio)

print("Full list count: ", len(filelist))
print("Training list count: ", len(train))
print("Validation list count: ", len(val))

# save training list
with open(f"{charname}_train.txt", "w", encoding="utf-8") as f:
    for line in train:
        f.write(f"{line}\n")

# save validation list
with open(f"{charname}_val.txt", "w", encoding="utf-8") as f:
    for line in val:
        f.write(f"{line}\n")

print("List created successfully!")

