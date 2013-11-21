## Script (Python) "cookFolderTeaser2colView"
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

batchlist = list(batch) #[b for b in batch]
lenbatch = len(batchlist)

# put FeedItem on position 01
# positions are 00,01,10,11,20,21
context.plone_log(str([b.portal_type for b in batch]))

ffis = [b for b in batchlist if b.portal_type=="FeedFeederItem"]
ffi = ffis and ffis[0] or None
if ffi:
    ind = batchlist.index(ffi)
    del batchlist[ind]
    batchlist.insert(1,ffi)

nbitemslastrow = lenbatch % 2
if nbitemslastrow:
    nbrows = (lenbatch / 2) + 1
    for n in range(nbrows-1):
        rowitems = [batchlist[n*2],batchlist[n*2+1]]
        results.append(rowitems)
    if nbitemslastrow==1:
        lastrowitems = [batchlist[nbrows*2-2]]
        results.append(lastrowitems)
else:
    nbrows = lenbatch / 2
    for n in range(nbrows):
        rowitems = [batchlist[n*2],batchlist[n*2+1]]
        results.append(rowitems)
return results