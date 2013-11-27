## Script (Python) "cookFolderTeaser3colView"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=batch=None
##title=
##
results=[]
if not batch:
    return results

batchlist = [b for b in batch]
lenbatch = len(batchlist)
nbitemslastrow = lenbatch % 3
if nbitemslastrow:
    nbrows = (lenbatch / 3) + 1
    for n in range(nbrows-1):
        rowitems = [batchlist[n*3],batchlist[n*3+1],batchlist[n*3+2]]
        results.append(rowitems)
    if nbitemslastrow==1:
        lastrowitems = [batchlist[nbrows*3-3]]
        results.append(lastrowitems)
    if nbitemslastrow==2:
        lastrowitems = [batchlist[nbrows*3-3],batchlist[nbrows*3-2]]
        results.append(lastrowitems)
else:
    nbrows = lenbatch / 3
    for n in range(nbrows):
        rowitems = [batchlist[n*3],batchlist[n*3+1],batchlist[n*3+2]]
        results.append(rowitems)
return results