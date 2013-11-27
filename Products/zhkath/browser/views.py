import re
from bs4 import BeautifulSoup
import urllib2
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

    # @memoize
    def getImageUrl(self, link):
        # print "getImageUrl", link
        text = ""
        try:
            f = urllib2.urlopen(link)
        except urllib2.HTTPError, e:
            log.error(str(e))
            return None
        text = f.read(20000)
        
        soup = BeautifulSoup(text)
        allimages = [img['src'] for img in soup.find_all('img', class_="wp-post-image", src=True, limit=2)] 
        # print allimages 
        return allimages and allimages[0] or None