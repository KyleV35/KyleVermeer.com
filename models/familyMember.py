from google.appengine.ext import db
from google.appengine.api import memcache
from util.memcacheHelper import safeMemcacheSet
from datetime import date

import logging

 
class Comment(db.Model):
    """ Models a comment. """
    content= db.TextProperty()
    author= db.StringProperty()
    date_time= db.DateTimeProperty(auto_now_add=True)
    likes= db.IntegerProperty()
    
    
class Image(db.Model):
    """ Models an image. """
    url= db.StringProperty()
    comments= db.ListProperty(item_type=str,default=[])
    likes= db.IntegerProperty()

class FamilyMember(db.Model):
    """ Models an individual family member. """
    height= db.StringProperty()
    weight= db.StringProperty()
    first_name= db.StringProperty()
    GPA= db.StringProperty()
    normalized_name= db.StringProperty()
    last_name= db.StringProperty()
    profile_picture= db.StringProperty()
    #Profile video is unique Youtube identifier
    profile_video= db.StringProperty()
    birth_date= db.DateProperty()
    #List of Images
    images= db.ListProperty(item_type=str,default=[])
    high_school= db.StringProperty()
    high_school_link= db.StringProperty()
    email= db.EmailProperty()
    name_image_string= db.StringProperty()
    twitter_username= db.StringProperty()
    #Add twitter
    #Transcripts and grades
    
    def get_videos(self):
        videos= memcache.get(self.normalized_name+"_videos")
        if videos is not None:
            logging.error("Cache hit")
            return videos
        videos= []
        query= db.Query(Video).ancestor(self)
        for video in query.run():
            videos.append(video)
        safeMemcacheSet(key=self.normalized_name+"_videos",value=videos)
        return videos
        #for video_ID in self.video_list:
            #logging.info(video_ID)
        #    video= memcache.get(video_ID)
        #    if video is not None:
                #logging.info("Cache hit!")
        #        videos.append(video)
        #    else:
                #logging.info("Cache miss!")
        #        q= db.Query(Video)
        #        q.filter("youtube_id =",video_ID)
        #        videos.append(q.get())
        #return videos
        
    def add_videoID(self,videoID):
        self.video_list.append(videoID)
        self.delete(self.normalized_name+"_videos") #Remove cached video list
        self.put()
        safeMemcacheSet(key=self.normalized_name,value=self)
        
    def getAgeInYears(self):
        birth_date= self.birth_date
        year= birth_date.year
        month= birth_date.month
        day= birth_date.day
        today = date.today()
        age= today.year - year
        if today.month <= month:
            if today.month==month:
                if today.day < day:
                    return age-1
                return age
            return age-1
        return age
        
class Video(db.Model):
    """ Models a video on the website. """
    video_name= db.StringProperty()
    family_member= db.ReferenceProperty(FamilyMember)
    comments= db.ListProperty(item_type=str,default=[])
    likes= db.IntegerProperty()
    youtube_id = db.StringProperty()
    
    def addLike(self):
        self.likes= self.likes + 1
        self.put()
        safeMemcacheSet(key=self.youtube_id,value=self)
                
    