import os, sys
import json
import re

def insert(char_quotes, source, target, lang):
    # check all quotes for this character
    for filename, data in char_quotes.items():
        org_text = char_quotes[filename]["quote"][lang]
        if org_text is not None:
            # replaced desired text (if possible)
            new_text = org_text.replace(source, target)
            char_quotes[filename]["quote"][lang] = new_text
            
def insert_regex(char_quotes, source, target, lang):
    # check all quotes for this character
    for filename, data in char_quotes.items():
        org_text = char_quotes[filename]["quote"][lang]
        if org_text is not None:
            # replaced desired text (if possible)
            new_text = re.sub(source, target, org_text)
            char_quotes[filename]["quote"][lang] = new_text

def replace(quotes, dictionary, lang):
    # first traverse character entries
    for charname, entries in dictionary.items():
        if charname not in ["global", "regex"] and charname in quotes:
            # apply every target text to a source text
            for source, target in entries.items():
                insert(quotes[charname], source, target, lang)
    
    # then apply global entries
    for source, target in dictionary["global"].items():
        for charname in quotes:
            insert(quotes[charname], source, target, lang)

    # finally, apply regex entries globally
    for source, target in dictionary["regex"].items():
        for charname in quotes:
            insert_regex(quotes[charname], source, target, lang)
    
    #for charname, entries in dictionary.items():
    #    if charname == "global":
    #        # replace text for the whole quotes file (only one lang tho)
    #        for global_name in quotes:
    #            for source, target in entries.items():
    #                insert(quotes[global_name], source, target, lang)

def replace_all_lang(quotes, dictionary):
    localization = quotes.copy()

    # all entries are applied once for each language in the dictionary
    for lang in dictionary:
        replace(localization, dictionary[lang], lang)

    return localization

# load quotes
quotes_path = sys.argv[1]
with open(quotes_path, "r", encoding="utf-8") as f:
    quotes = json.load(f)

# load dictionary
dict_path = sys.argv[2]
with open(dict_path, "r", encoding="utf-8") as f:
    dictionary = json.load(f)

localization = replace_all_lang(quotes, dictionary)

filename = os.path.basename(quotes_path)
filename = os.path.splitext(filename)[0]
with open(f"{filename}_localized.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(localization, indent=4, ensure_ascii=False))

print("All dictionary entries were applied successfully!")
