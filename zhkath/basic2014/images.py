""" Add alternative image sizes to default ATImage scales.
    NOTE: This does not effect available user interface options in the visual editor etc.
"""

import transaction
try:
    from zope.app.component.hooks import setHooks, setSite, getSite
except:
    from zope.component.hooks import setHooks, setSite, getSite

from Products.Five.browser import BrowserView

from Products.ATContentTypes.content.image import ATImage
from Products.ATContentTypes.interface.image import IATImage

from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.interface.news import IATNewsItem

# Monkeypatch our new image sizes to be available in ATImage default scales.
# This will also affect the "image sizes" option in the WYSIWYG text editor.

ATImage.schema["image"].sizes.update({
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
})
ATNewsItem.schema["image"].sizes.update({
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
})

class RescaleImages(BrowserView):
    """ Migration view to recreate all image scale versions on all Image content types on the site.

    To trigger this migration code, enter the view URL manually in the browser address bar::

        http://yourhost/site/@@rescale_images

    We assume that you are running Zope in the foreground, monitoring the console for messages.

    This code is designed to work with sites with plenty of images.
    Tested with > 5000 images.

    Note that you need to run this rescale code only once to migrate the existing image content.
    New images will have custom scale versions available when the images are created.
    """

    def __call__(self):
        """ View processing entry point.
        """

        portal = getSite()

        # Iterate through all Image content items on the site
        all_images = portal.portal_catalog(portal_type=['Image','News Item','zhkathmedienspiegel'])

        done = 0

        for brain in all_images:
            try:
                content = brain.getObject()
    
                # Access schema in Plone 4 / archetypes.schemaextender compatible way
                schema = content.Schema()
    
                # This will trigger ImageField scale rebuild
                if "image" in schema:
                    schema["image"].createScales(content)
                else:
                    print "Has bad ATImage schema:" + content.absolute_url()
    
                # Since this is a HUGE operation (think of resizing 2 GB images)
                # it is not a good idea to buffer the transaction in memory
                # (Zope default behavior).
                # Using subtransactions we hint Zope when it would be a good
                # time to buffer the changes on disk.
                # http://www.zodb.org/documentation/guide/transactions.html
                #if done % 10 == 0:
                    # Commit subtransaction for every 10th processed item
                #    transaction.commit(True)
    
                done += 1
                print "(%d / %d) created scales for image: %s" % (done, len(all_images), "/".join(content.getPhysicalPath()))
            except:
                print "(%d / %d) NOT CREATED scales for image: %s" % (done, len(all_images), "/".join(content.getPhysicalPath()))
                pass

        # Final commit
        transaction.commit()

        # Note that when entire transaction is commited, there will be a
        # huuuge delay before the message below is returned to the browser.
        # This is because Zope is busy updating the ZODB storage.

        # Make simple HTTP 200 answer
        return "Recreated image scales for %d images, news and medienspiegel" % len(all_images)