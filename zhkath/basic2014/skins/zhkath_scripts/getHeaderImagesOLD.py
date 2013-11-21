## Script (Python) "getHeaderImages"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName

results = []
counter = 0
urltool = getToolByName(context, 'portal_url')
portal = urltool.getPortalObject()
headerimagescontainer = getattr(portal,'headerimages',None)

if headerimagescontainer:
    headerimages = headerimagescontainer.getFolderContents(contentFilter={'portal_type':['Image']})
    if headerimages:
        sorter = [(img.id, img) for img in headerimages]
        headerimages = [ tuple[1] for tuple in sorter ]
        sorter.sort()
        for image in headerimages:
            obj = image.getObject()
            results.append({'title':obj.title_or_id(),'url':obj.absolute_url(),'counter':counter})
            counter += 1
return results
