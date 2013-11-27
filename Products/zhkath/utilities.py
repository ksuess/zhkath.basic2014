# from config import TAG_STARTSEITE

# siehe feed.py 
# 
# 
# 

# def feeditem_created_handler(feeditem, event):
#     """Add tag after creation of FeedItem
#     AND remove tag from all other FeedItems
#     weil wir nur das erste Post auf der Starseite sehen wollen. :-( """
#     sbj = feeditem.Subject()
#     # print "TAG_STARTSEITE in sbj", str(sbj), TAG_STARTSEITE in sbj
#     if TAG_STARTSEITE in sbj:        
#         # print "feeditem_created_handler obsolete"
#         return
#     piep = set(sbj)
#     piep.update((TAG_STARTSEITE,))
#     feeditem.setSubject(list(piep))
#     feeditem.reindexObject()
#     # TODO: remove tag from all other FeedItems
#     