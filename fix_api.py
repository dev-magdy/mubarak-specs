
import sys
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import copy
def camelCase(words):
    for i,word in enumerate(words):
        word = list(word)
        word[0] = word[0].upper()
        words[i] = "".join(word)
    return "".join(words)

def generate(path):
    words=[]
    for word in path.split("/")[1:]:
        word =  word.lower()
        word =  word.replace("{","")
        word =  word.replace("}","")
        if word:
            if "-" in word:
                word =  camelCase(word.split("-"))
            if "_" in word:
                word =  camelCase(word.split("_"))
            words.append(word)
    return camelCase(words)



filename=sys.argv[1]
obj = load(open(filename,"r"),Loader=Loader)
verbs=["get","post","put","patch","head"]

for path in obj["paths"]:
    path_obj = obj["paths"][path]
    if not path_obj:
        continue
    for verb in verbs:
        if verb in path_obj:
            path_obj[verb]["operationId"] = verb+generate(path)
            
name,ext=filename.split(".")                                        
dump(obj,open(name+"_fixed."+ext,"w"),Dumper=Dumper)

