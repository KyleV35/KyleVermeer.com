import webapp2
from webapp2_extras import routes

routes= [
    #webapp2.Route(r'/', handler='main.MainHandler'),
    #For now
    webapp2.Route(r'/',handler='handlers.kyle.FrontPageHandler'),
    webapp2.Route(r'/examples',handler='handlers.kyle.KyleExamplesHandler'),
    webapp2.Route(r'/family',handler='handlers.family.FamilyMainPageHandler'),
    webapp2.Route(r'/family/member/<familyMemberName>', handler='handlers.family.FamilyHandler'),
    routes.PathPrefixRoute(r'/family/videos', [
        webapp2.Route(r'/display',handler='handlers.family.VideoHandler'),
        webapp2.Route(r'/like',handler='handlers.family.VideoLikeHandler'), #Ajax handler
    ]),
    webapp2.Route(r'/family/makedummydata', handler='handlers.family.DummyData')
    ]