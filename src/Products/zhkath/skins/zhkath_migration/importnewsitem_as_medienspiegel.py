## Script (Python) "importnewsitem_as_medienspiegel"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Import News Item as Medienspiegel
##
path = '/'.join(context.getPhysicalPath())
wtool = context.portal_workflow

newsitems = [] # these are the News Items we want to migrate
numbernewsitems = 0
migrated = []
numbermigrated = 0
failed = []
numberfailed = 0
objstomigrate = []

allnewsinpath_incl_depr = context.portal_catalog(portal_type='News Item',sort_on='sortable_title',path=path)
allnewsinpath = [item for item in allnewsinpath_incl_depr if item.getId[-5:]!='_DEPR']
numberallnewsinpath = str(len(allnewsinpath))

for news in allnewsinpath:
    newsobj = news.getObject()
    newsitems.append(newsobj)
    numbernewsitems += 1

for obj in newsitems:
    linkstring = obj.Rights()
    linkinfo = linkstring.split('++++++++++')
    if linkinfo:
        try:
            linkurl = linkinfo[0]
            linktitle = linkinfo[1]
        except:
            linkurl = ''
            lintitle = ''
    else:
        linkurl = ''
        lintitle = ''        
    dict = {'obj':obj,
            'id':obj.getId(),
            'path':'/'.join(obj.getPhysicalPath()),
            'title':obj.Title(),
            'description':obj.aq_inner.aq_explicit.Description(),
            'text':obj.getText(),
            'image':obj.getImage(),
            'subjects':list(obj.Subject()),
            'state':wtool.getInfoFor(obj, 'review_state', ''),
            'creationdate':obj.created() or '',
            'modificationdate':obj.modified() or '',
            'creator':obj.Creator() or '',
            'linkurl':linkurl,
            'linktitle':linktitle,
            }
    objstomigrate.append(dict)  
    

for oldobj in objstomigrate:
#    try:
        oldid = oldobj['id']
        newid = oldid
        deprid = oldid+'_DEPR'
        newtitle = oldobj['title']
        parent = oldobj['obj'].aq_inner.aq_parent
        if hasattr(parent,newid):
            newid = newid+'_n'  
        
        # rename old object
        oldobj['obj'].setId(deprid)
        deprobj = getattr(parent,deprid)
        deprobj.reindexObject()
        
        # create news item
        parent.invokeFactory(type_name='zhkathmedienspiegel',id=newid,title=newtitle)
        new = getattr(parent,newid)
        new.setDescription(oldobj['description'])
        new.setSubject(oldobj['subjects'])
        new.setImage(oldobj['image'])
        new.setText(oldobj['text'])
        new.setCreationDate(oldobj['creationdate'])
        new.setCreators((oldobj['creator'],))
        # change workflow sate for new
        if oldobj['state'] == 'private':
            wtool.doActionFor(new, 'hide')
        if oldobj['state'] == 'pending':
            wtool.doActionFor(new, 'submit')
        if oldobj['state'] == 'published':
            wtool.doActionFor(new, 'publish')
        # set link url if exists into copyright field (temp)
        if oldobj['linkurl']:
            new.setRemoteUrl(oldobj['linkurl'])
        if oldobj['linktitle']:
            new.setRemoteUrlTitle(oldobj['linktitle'])        
        # set modification date and catalog object
        #new.setModificationDate(oldobj['modificationdate'])
        #context.portal_catalog.catalog_object(object=new,uid=new.UID())
        new.reindexObject()
            
        # pour chaque ba migré, counter-migré += 1
        migrated.append(oldobj)
        numbermigrated += 1       
    
#    except:
        # pour chaque erreur, counter-error-not-migré += 1
#        failed.append(oldobj)
#        numberfailed += 1
#        pass
    
# retourner: counter-migré, counter-error-not-migré, len-ba-sans-sub-ba-avant-migration, len-ba-avec-sub-ba-avant-migration
return {'number to migrate':numbernewsitems,
        'number migrated':numbermigrated,
        'number failed to migrate':numberfailed,
        'failed to migrate':failed,
        'migrated':migrated,
        }
    

### ensuite, relancer ce script jusqu'à ce que les compteurs soient à 0

