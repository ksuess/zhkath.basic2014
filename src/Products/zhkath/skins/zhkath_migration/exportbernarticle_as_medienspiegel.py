## Script (Python) "exportbernarticle_blocks_as_medienspiegel"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Export BernArticle to Plone
##
path = '/'.join(context.getPhysicalPath())
wtool = context.portal_workflow
baswithsubs = []
numberbaswithsubs = 0
baswithoutsubs = [] # these are the BernArticle we want to migrate
numberbaswithoutsubs = 0
basmigrated = []
numberbasmigrated = 0
basfailed = []
numberbasfailed = 0
objstomigrate = []

# chercher tous les ba's dans le path actuel
allbasinpath_incl_depr = context.portal_catalog(meta_type='BernArticle',sort_on='sortable_title',path=path)
allbasinpath = [item for item in allbasinpath_incl_depr if item.getId[-5:]!='_DEPR']
numberallbasinpath = str(len(allbasinpath))

# creer liste ba's avec sub-ba's -> len(ba's avec sub-ba's avant migration)
# creer liste ba's sans sub-ba's -> len(ba's sans sub-ba's avant migration)
for ba in allbasinpath:
    baobj = ba.getObject()
    basubs = baobj.listFolderContents(contentFilter={'portal_type':['BernArticle',]})
    if basubs:
        baswithsubs.append(baobj)
        numberbaswithsubs += 1
    else:
        baswithoutsubs.append(baobj)
        numberbaswithoutsubs += 1

# pour chaque ba dans liste ba's sans sub-ba's faire la migration
for obj in baswithoutsubs:
    links = obj.listFolderContents(contentFilter={'portal_type':['BernArticleBlockLink',]})
    if links:
        link = links[0].getUrl()+'++++++++++'+links[0].Title()
    else:
        link = ''
    dict = {'obj':obj,
            'id':obj.getId(),
            'path':'/'.join(obj.getPhysicalPath()),
            'title':obj.Title(),
            'description':obj.aq_inner.aq_explicit.Description(),
            'text':obj.getText(),
            'img':obj.getImage1(),
            'subjects':list(obj.Subject()),
            'state':wtool.getInfoFor(obj, 'review_state', ''),
            'creationdate':obj.created() or '',
            'modificationdate':obj.modified() or '',
            'creator':obj.Creator() or '',
            'link':link,
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
        parent.invokeFactory(type_name='News Item',id=newid,title=newtitle)
        newindex = getattr(parent,newid)
        newindex.setDescription(oldobj['description'])
        newindex.setSubject(oldobj['subjects'])
        newindex.setImage(oldobj['img'])
        newindex.setText(oldobj['text'])
        newindex.setCreationDate(oldobj['creationdate'])
        newindex.setCreators((oldobj['creator'],))
        # change workflow sate for newindex
        if oldobj['state'] == 'private':
            wtool.doActionFor(newindex, 'hide')
        if oldobj['state'] == 'pending':
            wtool.doActionFor(newindex, 'submit')
        if oldobj['state'] == 'published':
            wtool.doActionFor(newindex, 'publish')
        # set link url if exists into copyright field (temp)
        if oldobj['link']:
            newindex.setRights(oldobj['link'])
        
        # set modification date and catalog object
        #newindex.setModificationDate(oldobj['modificationdate'])
        #context.portal_catalog.catalog_object(object=newindex,uid=newindex.UID())
        newindex.reindexObject()
            
        # pour chaque ba migré, counter-migré += 1
        basmigrated.append(oldobj)
        numberbasmigrated += 1       
    
#    except:
        # pour chaque erreur, counter-error-not-migré += 1
#        basfailed.append(oldobj)
#        numberbasfailed += 1
#        pass
    
# retourner: counter-migré, counter-error-not-migré, len-ba-sans-sub-ba-avant-migration, len-ba-avec-sub-ba-avant-migration
return {'number to migrate':numberbaswithoutsubs,
        'number migrated':numberbasmigrated,
        'number failed to migrate':numberbasfailed,
        'failed to migrate':basfailed,
        'migrated':basmigrated,
        }
    

### ensuite, relancer ce script jusqu'à ce que les compteurs soient à 0

