from zope.interface import implements
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.Archetypes import atapi
from Products.ATContentTypes.content import newsitem, link
from Products.ATContentTypes.content import schemata
from Products.zhkath.interfaces import Izhkathmedienspiegel
from Products.zhkath.config import PROJECTNAME

copied_fields = {}
copied_fields['remoteUrl'] = link.ATLinkSchema['remoteUrl'].copy()
copied_fields['remoteUrl'].primary=False
copied_fields['remoteUrl'].required=False
copied_fields['remoteUrl'].default=''

zhkathmedienspiegelSchema = newsitem.ATNewsItemSchema.copy() + atapi.Schema((
                                                                             
    atapi.StringField(
            name='fullPublishTime',
            widget=atapi.SelectionWidget(
                label='Full publish time',
                label_msgid='label_fullpublishtime',
                description='',
                description_msgid='description_fullpublishtime',
                i18n_domaine='Plone',
                ),
            vocabulary=['0_day','7_days','14_days','30_days','infinite'],
            default='O_day',
            required=True,
            searchable=False,                   
           ),
                                                                             
    copied_fields['remoteUrl'],
    
    atapi.StringField(
            name='remoteUrlTitle',
            widget=atapi.StringWidget(
                label='URL title',
                label_msgid='label_remoteurltitle',
                description='',
                description_msgid='description_remoteurltitle',
                i18n_domaine='Plone',
                ),
            searchable=True,                   
           ),
           
))

zhkathmedienspiegelSchema['title'].storage = atapi.AnnotationStorage()
zhkathmedienspiegelSchema['description'].storage = atapi.AnnotationStorage()
zhkathmedienspiegelSchema['image'].sizes= {
                'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
                'teaser' :  (225, 225),
                'portlethorizontal' :  (227, 227),
                'portletvertical' :  (328, 328),
                'fullwidth' :  (473, 473),
                'banner'    : (977, 977),
               }
schemata.finalizeATCTSchema(zhkathmedienspiegelSchema, moveDiscussion=False)
zhkathmedienspiegelSchema['subject'].schemata = 'default'
zhkathmedienspiegelSchema['relatedItems'].schemata = 'default'




class zhkathmedienspiegel(newsitem.ATNewsItem,link.ATLink):
    """A medienspiegel object"""
    implements(Izhkathmedienspiegel)

    meta_type = "zhkathmedienspiegel"
    schema = zhkathmedienspiegelSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def userHasPermissionSeeFulltext(self):
        portal_state = self.restrictedTraverse('@@plone_portal_state')
        user = portal_state.member()
        usergroups = [g.id for g in self.portal_groups.getGroupsByUserId(user.getUserName())]
        if 'group_Medienspiegel' in usergroups or self.portal_membership.checkPermission('Modify portal content',self):
            return 1
        else:
            return 0
    
    def displayFulltext(self):
        """ returns 1 if the full text has to be displayed
        """
        publishtime = self.getFullPublishTime()
        lenShortText = 700
        fulltextlength = len(self.getText())
        if fulltextlength <= lenShortText:
            return 1
        if publishtime == 'infinite':
            return 1
        elif self.userHasPermissionSeeFulltext():
            return 1
        elif publishtime == '0_day':
            return 0
        elif publishtime == '7_days':
            if DateTime(self.created()) + 7 < DateTime():
                return 0
            else:
                return 1
        elif publishtime == '14_days':
            if DateTime(self.created()) + 14 < DateTime():
                return 0
            else:
                return 1
        elif publishtime == '30_days':
            if DateTime(self.created()) + 30 < DateTime():
                return 0
            else:
                return 1
        else:
            return 0
        
    def getTextToDisplay(self):
        """ returns the main text to display
        """
        lenShortText = 700
        fulltext = self.getText()
        displayfulltext = self.displayFulltext()
        if displayfulltext:
            return fulltext
        else:
            return fulltext[:lenShortText]+' [...]'
        
        

atapi.registerType(zhkathmedienspiegel, PROJECTNAME)
