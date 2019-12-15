# In CeciliaInterface.onClose() - not finished to add cleanup() method to all widgets.

# to track down remaining references to an object.
import sys, gc
print(sys.getrefcount(self))
referers = gc.get_referrers(self)
for referer in referers:
    print()
    print(referer)
