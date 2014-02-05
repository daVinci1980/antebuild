
__all__ = ["c", "cpp"]

import cpp
import c

from sln import Solution

# ---------------------------------------------------------------------------------------------------------------------
def getProjectGroupDict():
    return {
        "c": c,
        "cpp": cpp,
        "Solution": Solution
    }
