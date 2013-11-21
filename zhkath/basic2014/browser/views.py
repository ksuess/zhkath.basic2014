import re
from bs4 import BeautifulSoup
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

import logging
log = logging.getLogger("feedfeeder views >> ")

class UtilityView(BrowserView):
    
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
    
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_state = getMultiAdapter((context, request),
                                               name=u'plone_portal_state')
        self.navigation_root_url = self.portal_state.navigation_root_url()

    def getImagesUrls(self, text):
        soup = BeautifulSoup(text)
        allimages = [img['src'] for img in soup.findAll('img', src=True)]  
        return allimages