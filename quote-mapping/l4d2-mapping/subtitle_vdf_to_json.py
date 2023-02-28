import os, sys
import json
import vdf
import re

def insert_quote(dictionary, charname, filename, lang, quote):
    if charname not in dictionary:
        dictionary[charname] = {}
    if filename not in dictionary[charname]:
        dictionary[charname][filename] = {}
    if "quote" not in dictionary[charname][filename]:
        dictionary[charname][filename]["quote"] = {}
    dictionary[charname][filename]["quote"][lang] = quote

def simplify_commentary_key(key):
    # each character key is in the format charname_filename
    if key.find("_") != -1:
        pair = key.split("_")
        filename = "_".join(pair[1:len(pair)]).lower() # re-join because it had more than 1 underscore
    else:
        pair = key.split("\\")
        filename = pair[1]

    charname = pair[0].lower()

    return filename, charname

def simplify_commentary_quote(value):
    # remove all text marks (everything enclosed in < and >)
    quote = re.sub('<[^<>]*>', '', value)
    
    # remove the speakers name, which could be in the format "[name] quote"
    # otherwise, it doesn't need removing anything
    if quote.startswith("["):
        quote = quote.split("]")[1]

    return quote

def simplify_character_key(key):
    # each character key is in the format charname_filename
    pair = key.split("_")
    charname = pair[0].lower()
    if len(pair) > 2: # re-join keys that had more than 1 underscore
        filename = "_".join(pair[1:len(pair)]).lower() 
        #print(filename)
    else:
        filename = pair[1].lower()
    return charname, filename

def simplify_character_quote(value):
    # remove all text marks (everything enclosed in < and >)
    quote = re.sub('<[^<>]*>', '', value)

    # if the quote has any ":" symbol, most of probably it's for the chacater's name
    if quote.find(":") != -1:
        sq = quote.split(":")
        quote = ":".join(sq[1:len(sq)]) # but we should keep any further text with ":"
        quote = quote.strip() # remove any trailing or leading spaces

    # screams, laughs and others sometimes don't have quotes and are only empty text marks
    if not quote.isspace() and quote != "":
        return quote
    else:
        return None

def remove_prefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s

def identify_alt_lang(s, main_lang):
    if s.startswith("[english]"):
        key = remove_prefix(s, "[english]")
        lang = "english"
    else:
        key = s
        lang = main_lang

    return key, lang

def clean(subtitles):
    clean_quotes = {}
    main_lang = subtitles["lang"]["Language"]
    subtitles = subtitles["lang"]["Tokens"]
    for s in subtitles:        
        # if it's a commentary quote 
        if s.lower().find("commentary") != -1:
            # sometimes, non-english quotes have an english duplicate
            key, lang = identify_alt_lang(s, main_lang)

            # reformat and clean key
            filename, charname = simplify_commentary_key(key)

            # reformat and clean quote
            quote = simplify_commentary_quote(subtitles[s])

            # add to the clean quotes dictionary
            insert_quote(clean_quotes, charname, filename, lang, quote)
        
        # if it's a character quote
        elif s.find("_") != -1:
            # sometimes, all non-english quotes have an english duplicate
            key, lang = identify_alt_lang(s, main_lang)

            # reformat and clean key
            charname, filename = simplify_character_key(key)

            # reformat and clean quote
            quote = simplify_character_quote(subtitles[s])
            if quote is None:
                quote = "[" + filename + "]"

            # add to the clean quotes dictionary
            insert_quote(clean_quotes, charname, filename, lang, quote)
    
    return clean_quotes

# read vdf
path = sys.argv[1]
with open(path, "r", encoding="utf-16") as f:
    quotes = vdf.load(f)

# reformat and remove unnecesary data
quotes = clean(quotes)

# save file
name = os.path.basename(path)
name = os.path.splitext(name)[0]
with open(f"{name}.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(quotes, indent=4, ensure_ascii=False))

print("VDF file converted to JSON successfully!")
