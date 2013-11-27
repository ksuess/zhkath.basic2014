from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner
from AccessControl import getSecurityManager
from zope.component import getMultiAdapter, queryMultiAdapter
from Products.CMFPlone.utils import base_hasattr
from Products.CMFCore.utils import _checkPermission
from plone.app.layout.globals.interfaces import IViewView
from datetime import date
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
import random

class zhkathFooter(ViewletBase):
    render = ViewPageTemplateFile('footer.pt')

    def update(self):
        self.year = date.today().year
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.footer_actions = context_state.actions('footer_actions')
        self.user_actions = context_state.actions('user')
        

class zhkathSocial(ViewletBase):
    index = ViewPageTemplateFile('social.pt')

    @memoize
    def show(self):
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        showSocialViewlet = site_properties.getProperty(
            'showSocialViewlet', False)
        return showSocialViewlet
            
class zhkathHeaderimage(ViewletBase):
    index = ViewPageTemplateFile('headerimage.pt')

    def update(self):
        self.headerimage = self.getHeaderImage()
        
    @memoize
    def show(self):
        context = aq_inner(self.context)
        contextid = context.getId()
        if contextid == 'startseite':
            return 1
        else:
            return 0

    @memoize
    def getHeaderImage(self):        
        result = None
        urltool = getToolByName(self, 'portal_url')
        portal = urltool.getPortalObject()
        headerimagescontainer = getattr(portal,'headerimages',None)
        if headerimagescontainer:
            headerimages = headerimagescontainer.getFolderContents(contentFilter={'portal_type':['Image']})
            if headerimages:
                result = random.choice(headerimages)
        return result

class zhkathHeaderactions(ViewletBase):
    index = ViewPageTemplateFile('headeractions.pt')

    def update(self):
        self.year = date.today().year
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.header_actions = context_state.actions('site_actions')

class zhkathDocumentBylineViewlet(ViewletBase):

    index = ViewPageTemplateFile("document_byline.pt")

    def update(self):
        super(zhkathDocumentBylineViewlet, self).update()
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.anonymous = self.portal_state.anonymous()

    def show(self):
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        allowAnonymousViewAbout = site_properties.getProperty(
            'allowAnonymousViewAbout', True)
        return (not self.anonymous or allowAnonymousViewAbout) and not self.hasTeasersLayout() and not self.context.Type() in ['Topic','Folder']
    
    def hasTeasersLayout(self):
        layout = self.context.getLayout()
        if layout in ['folder_teasers_3col_view','folder_teasers_2col_view']:
            return True
        else:
            return False
        
    def show_history(self):
        if not _checkPermission('CMFEditions: Access previous versions', self.context):
            return False
        if IViewView.providedBy(self.__parent__):
            return True
        return False

    def locked_icon(self):
        if not getSecurityManager().checkPermission('Modify portal content',
                                                    self.context):
            return ""

        locked = False
        lock_info = queryMultiAdapter((self.context, self.request),
                                      name='plone_lock_info')
        if lock_info is not None:
            locked = lock_info.is_locked()
        else:
            context = aq_inner(self.context)
            lockable = getattr(context.aq_explicit, 'wl_isLocked', None) is not None
            locked = lockable and context.wl_isLocked()

        if not locked:
            return ""

        portal = self.portal_state.portal()
        icon = portal.restrictedTraverse('lock_icon.gif')
        return icon.tag(title='Locked')

    def creator(self):
        return self.context.Creator()

    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

    def isExpired(self):
        if base_hasattr(self.context, 'expires'):
            return self.context.expires().isPast()
        return False

    def toLocalizedTime(self, time, long_format=None, time_only = None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        return util.ulocalized_time(time, long_format, time_only, self.context,
                                    domain='plonelocales')
    def allowedToModify(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.checkPermission('Modify portal content', self.context)

