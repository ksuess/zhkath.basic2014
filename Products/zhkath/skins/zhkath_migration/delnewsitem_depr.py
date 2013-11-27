## Script (Python) "delnewsitem_depr"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Delete _DEPR News Items objects
##
path = '/'.join(context.getPhysicalPath())
counter_deleted = 0

allbasinpath_incl_depr = context.portal_catalog(portal_type='News Item',sort_on='sortable_title',path=path)
allbasinpath_depr = [item.getObject() for item in allbasinpath_incl_depr if item.getId[-5:]=='_DEPR']

for todel in allbasinpath_depr:
    todel.aq_inner.aq_parent.manage_delObjects(todel.getId())
    counter_deleted +=1
    
if counter_deleted:
    return counter_deleted
else:
    return 'empty'