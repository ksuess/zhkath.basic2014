## Script (Python) "exportbernarticle_blocks_as_news"
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
    blocks = [{'blockid':o.getId(),'blocksubjects':list(o.Subject()),'blockimage':o.getImage1(),'blocktitle':o.Title(),'blocksubtitle':o.Subheading(),'blockdescription':o.getBlock_description(),'blocktext':o.getText(),'blockstate':wtool.getInfoFor(o, 'review_state', ''),'creationdate':o.created() or '','modificationdate':o.modified() or '','creator':o.Creator() or ''} for o in obj.listFolderContents(contentFilter={'portal_type':['BernArticleBlock',]})]
    files = [{'fileid':o.getId(),'filesubjects':list(o.Subject()),'filetitle':o.Title(),'filesubtitle':o.Subheading(),'filedescription':o.getBlock_description(),'filename':o.getName(),'filefile':o.getFile(),'filetext':o.getText(),'filestate':wtool.getInfoFor(o, 'review_state', ''),'creationdate':o.created() or '','modificationdate':o.modified() or '','creator':o.Creator() or ''} for o in obj.listFolderContents(contentFilter={'portal_type':['BernArticleBlockFile',]})]
    links = [{'linkid':o.getId(),'linksubjects':list(o.Subject()),'linktitle':o.Title(),'linksubtitle':o.Subheading(),'linkdescription':o.getBlock_description(),'linkurl':o.getUrl(),'linkstate':wtool.getInfoFor(o, 'review_state', ''),'creationdate':o.created() or '','modificationdate':o.modified() or '','creator':o.Creator() or ''} for o in obj.listFolderContents(contentFilter={'portal_type':['BernArticleBlockLink',]})]
    othercontentstocopy = [o for o in obj.listFolderContents() if o.Type() not in ['BernArticleBlock','BernArticleBlockFile','BernArticleBlockLink','BernArticle','BernArticleBlockAddress','BernArticleBaseBlock','BernArticleBlockEvent','BernArticleBlockHours','BernArticleBlockList','BernArticleBlockNews','BernArticleBlockTeaser','BernArticleCollector']]
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
            'blocks':blocks,
            'files':files,
            'links':links,
            'othercontentstocopy':othercontentstocopy,
            }
    objstomigrate.append(dict)  
    

for oldobj in objstomigrate:
#    try:
        oldid = oldobj['id']
        newid = oldid
        newfolderid = newid
        deprid = oldid+'_DEPR'
        newtitle = oldobj['title']
        parent = oldobj['obj'].aq_inner.aq_parent
        if hasattr(parent,newid):
            newid = newid+'_n'  
        
        # rename old object
        oldobj['obj'].setId(deprid)
        deprobj = getattr(parent,deprid)
        deprobj.reindexObject()
        
        # cook the main text for the new index page
        newcookedtext = oldobj['text']
                
        # cook the subjects for the new index page
        newcookedsubjects = oldobj['subjects']
                
        # if subcontents, create a folder:
        if oldobj['files'] or oldobj['links'] or oldobj['blocks'] or oldobj['othercontentstocopy']:
            
            # create the folder
            parent.invokeFactory(type_name='Folder',id=newfolderid,title=newtitle)
            newfolder = getattr(parent,newfolderid)
            newfolder.setCreationDate(oldobj['creationdate'])
            newfolder.setCreators((oldobj['creator'],))
            newfolder.setLayout('folder_summary_view')
            
            # change workflow sate for newfolder
            if oldobj['state'] == 'private':
                wtool.doActionFor(newfolder, 'hide')
            if oldobj['state'] == 'pending':
                wtool.doActionFor(newfolder, 'submit')
            if oldobj['state'] == 'published':
                wtool.doActionFor(newfolder, 'publish')
            
            # set modification date and catalog object
            #newfolder.setModificationDate(oldobj['modificationdate'])
            #context.portal_catalog.catalog_object(object=newfolder,uid=newfolder.UID())
            newfolder.reindexObject()
            
            # copy all non-bernarticle contents
            othercontentstocopy = [o for o in deprobj.listFolderContents() if o.Type() not in ['BernArticleBlock','BernArticleBlockFile','BernArticleBlockLink','BernArticle','BernArticleBlockAddress','BernArticleBaseBlock','BernArticleBlockEvent','BernArticleBlockHours','BernArticleBlockList','BernArticleBlockNews','BernArticleBlockTeaser','BernArticleCollector']]
            for tocopy in othercontentstocopy:
                newfolder.manage_pasteObjects(deprobj.manage_copyObjects(tocopy.getId()))
            
            # create the main news item as index page for the new folder
            newfolder.invokeFactory(type_name='News Item',id=oldid,title=newtitle)
            newindex = getattr(newfolder,oldid)
            newindex.setDescription(oldobj['description'])
            newindex.setSubject(newcookedsubjects)
            newindex.setImage(oldobj['img'])
            newindex.setText(newcookedtext)
            newindex.setCreationDate(oldobj['creationdate'])
            newindex.setCreators((oldobj['creator'],))
            
            # change workflow sate for newindex
            if oldobj['state'] == 'private':
                wtool.doActionFor(newindex, 'hide')
            if oldobj['state'] == 'pending':
                wtool.doActionFor(newindex, 'submit')
            if oldobj['state'] == 'published':
                wtool.doActionFor(newindex, 'publish')
            
            # set modification date and catalog object
            #newindex.setModificationDate(oldobj['modificationdate'])
            #context.portal_catalog.catalog_object(object=newindex,uid=newindex.UID())
            newindex.reindexObject()
            
            # create the contained blocks as news items:
            for oldblock in oldobj['blocks']:
                newblockid = oldblock['blockid']#+'_new'
                newblocktitle = oldblock['blocktitle']#+' (neu)'
                newcookedblockdescription = oldblock['blocksubtitle']
                if oldblock['blockdescription'] and newcookedblockdescription:
                    newcookedblockdescription += ' - '
                if oldblock['blockdescription']:
                    newcookedblockdescription += oldblock['blockdescription'] 
                newfolder.invokeFactory(type_name='News Item',id=newblockid,title=newblocktitle)
                newblock = getattr(newfolder,newblockid)
                newblock.setDescription(newcookedblockdescription)
                newblock.setText(oldblock['blocktext'])
                newblock.setCreationDate(oldblock['creationdate'])
                newblock.setCreators((oldblock['creator'],))
                newblock.setSubject(oldblock['blocksubjects'])
                newblock.setImage(oldblock['blockimage'])
                # change workflow sate for newfile
                if oldblock['blockstate'] == 'private':
                    wtool.doActionFor(newblock, 'hide')
                if oldblock['blockstate'] == 'pending':
                    wtool.doActionFor(newblock, 'submit')
                if oldblock['blockstate'] == 'published':
                    wtool.doActionFor(newblock, 'publish')
                # set modification date and catalog object
                #newblock.setModificationDate(oldblock['modificationdate'])
                #context.portal_catalog.catalog_object(object=newblock,uid=newblock.UID())
                newblock.reindexObject()
    
            # create the contained files:
            for oldfile in oldobj['files']:
                newfileid = oldfile['fileid']#+'_new'
                if hasattr(newfolder,newfileid):
                    newfileid = newfileid+'_n'
                if oldfile['filename']:
                    newfiletitle = oldfile['filename']#+' (neu)'
                elif oldfile['filesubtitle']:
                    newfiletitle = oldfile['filesubtitle']#+' (neu)'
                else:
                    newfiletitle = oldfile['filetitle']#+' (neu)'
                newcookedfiledescription = ''
                if oldfile['filedescription']:
                    newcookedfiledescription += oldfile['filedescription']
                if oldfile['filetext'] not in ['','<p>&nbsp;</p>'] and newcookedfiledescription:
                    newcookedfiledescription += ' - '
                if oldfile['filetext'] not in ['','<p>&nbsp;</p>']:
                    newcookedfiledescription += oldfile['filetext']
                newfolder.invokeFactory(type_name='File',id=newfileid,title=newfiletitle)
                newfile = getattr(newfolder,newfileid)
                newfile.setDescription(newcookedfiledescription)
                newfile.setFile(oldfile['filefile'])
                newfile.setCreationDate(oldfile['creationdate'])
                newfile.setCreators((oldfile['creator'],))
                newfile.setSubject(oldfile['filesubjects'])
                # change workflow sate for newfile
                if oldfile['filestate'] == 'private':
                    wtool.doActionFor(newfile, 'hide')
                if oldfile['filestate'] == 'pending':
                    wtool.doActionFor(newfile, 'submit')
                if oldfile['filestate'] == 'published':
                    wtool.doActionFor(newfile, 'publish')
                # set modification date and catalog object
                #newfile.setModificationDate(oldfile['modificationdate'])
                #context.portal_catalog.catalog_object(object=newfile,uid=newfile.UID())
                newfile.reindexObject()
                
            # create the contained links:
            for oldlink in oldobj['links']:
                newlinkid = oldlink['linkid']#+'_new'
                if hasattr(newfolder,newlinkid):
                    newlinkid = newlinkid+'_n'
                newlinktitle = oldlink['linktitle']#+' (neu)'
                newcookedlinkdescription = oldlink['linksubtitle']
                if oldlink['linkdescription'] and newcookedlinkdescription:
                    newcookedlinkdescription += ' - '
                if oldlink['linkdescription']:
                    newcookedlinkdescription += oldlink['linkdescription']
                newfolder.invokeFactory(type_name='Link',id=newlinkid,title=newlinktitle)
                newlink = getattr(newfolder,newlinkid)
                newlink.setDescription(newcookedlinkdescription)
                newlink.setRemoteUrl(oldlink['linkurl'])
                newlink.setCreationDate(oldlink['creationdate'])
                newlink.setCreators((oldlink['creator'],))
                newlink.setSubject(oldlink['linksubjects'])
                # change workflow sate for newlink
                if oldlink['linkstate'] == 'private':
                    wtool.doActionFor(newlink, 'hide')
                if oldlink['linkstate'] == 'pending':
                    wtool.doActionFor(newlink, 'submit')
                if oldlink['linkstate'] == 'published':
                    wtool.doActionFor(newlink, 'publish')
                # set modification date and catalog object
                #newlink.setModificationDate(oldlink['modificationdate'])
                #context.portal_catalog.catalog_object(object=newlink,uid=newlink.UID())       
                newlink.reindexObject()
            
        # if no subcontents, create only a news item:
        else:
            parent.invokeFactory(type_name='News Item',id=newid,title=newtitle)
            newindex = getattr(parent,newid)
            newindex.setDescription(oldobj['description'])
            newindex.setSubject(newcookedsubjects)
            newindex.setImage(oldobj['img'])
            newindex.setText(newcookedtext)
            newindex.setCreationDate(oldobj['creationdate'])
            newindex.setCreators((oldobj['creator'],))
            # change workflow sate for newindex
            if oldobj['state'] == 'private':
                wtool.doActionFor(newindex, 'hide')
            if oldobj['state'] == 'pending':
                wtool.doActionFor(newindex, 'submit')
            if oldobj['state'] == 'published':
                wtool.doActionFor(newindex, 'publish')
            
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

