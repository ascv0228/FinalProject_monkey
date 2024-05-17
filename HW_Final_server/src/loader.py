
import os

def importFile(importPath, dictObj = {}):
    for filename in os.listdir(importPath):
        if(os.path.isdir(importPath + "\\" +filename)):
            importFile(importPath + "\\" +filename, dictObj)
        elif(filename[-3:] == ".py"):
            f = filename[:-3]
            modulePath = importPath.replace("\\", ".").replace("/", ".")
            m = __import__(f"{modulePath}.{f}",globals(), locals(), ["__exports__"])
            try:
                dictObj.update({m.__exports__["name"]:m.__exports__})
            except AttributeError as e:
                pass
        
    else:
        return dictObj