## Script (Python) "listbawithsubba"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=nlines=0
##title=List paths BernArticle having subarticles
##
from Products.CMFCore.utils import getToolByName
url_tool = getToolByName(context, 'portal_url')
portal = url_tool.getPortalObject()

counter = 0
baswithsubs = []
allbas = portal.portal_catalog(meta_type='BernArticle',sort_on='sortable_title')
nbbas = len(allbas)
for ba in allbas:
    nbsub = len(ba.getObject().listFolderContents(contentFilter={'portal_type':['BernArticle',]}))
    if nbsub:
        counter += 1
        baswithsubs.append('/'.join(ba.getObject().getPhysicalPath()))
baswithsubs.sort()
return baswithsubs
