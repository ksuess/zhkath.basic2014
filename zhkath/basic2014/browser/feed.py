import logging

from zope import interface
from zope import component

from Products.CMFCore.utils import getToolByName

from Products.feedfeeder.interfaces.consumer import IFeedConsumer
from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.browser.feed import UpdateFeedItems, IUpdateFeedItems

from zhkath.basic2014.config import TAG_STARTSEITE

from Products.statusmessages.interfaces import IStatusMessage

from Products.feedfeeder import _

logger = logging.getLogger("feedfeeder_kath")


class UpdateFeedItemsZhkath(UpdateFeedItems):
    """A view for updating the feed items in a feed folder.
    """

    interface.implements(IUpdateFeedItems)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        # Tag fuer Startseite an neusten Post vergeben; vorher Tag allen Posts nehmen
        # logger.info("Tags von Posts entfernen")
        catalog = getToolByName(self.context, 'portal_catalog')
        items = catalog(
            portal_type='FeedFeederItem', sort_on="effective", sort_order="reverse")
        for item in items:
            feeditem = item.getObject()
            sbj = feeditem.Subject()
            # print feeditem
            if TAG_STARTSEITE in sbj:  
                piep = set(sbj)
                piep.remove(TAG_STARTSEITE)
                feeditem.setSubject(list(piep))
                feeditem.reindexObject()
                # print str(feeditem), "cleaned"
        if items:
            firstitem = items[0]
            feeditem = firstitem.getObject()
            sbj = set(feeditem.Subject())
            sbj.update((TAG_STARTSEITE,))
            feeditem.setSubject(list(sbj))
            feeditem.reindexObject()
            # print "newest FeedItem:", str(feeditem), str(sbj)
        
        
        
        
        
        # Rest wie in feedfeeder
        message = _('Feed items updated')
        messages = IStatusMessage(self.request, alternate=None)
        if messages is not None:
            messages.addStatusMessage(message, 'info')
        self.request.response.redirect(self.context.absolute_url())