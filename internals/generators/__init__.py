
from msvs2013 import Msvs2013

# ---------------------------------------------------------------------------------------------------------------------
def getGeneratorDict():
    return {
        "Msvs2013": Msvs2013,
    }

# ---------------------------------------------------------------------------------------------------------------------
def getGeneratorListString():
    genDict = getGeneratorDict()

    itemList = [("Name", "Description")]
    for k, v in genDict.iteritems():
        itemList.append((k, v.Description))

    stringList = ["    {0:<12}{1:<4}{2}".format(name, "", desc) for name, desc in itemList]
    return "\n".join(stringList)
