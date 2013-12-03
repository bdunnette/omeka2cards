#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib
import json
import datetime

from google.appengine.api import users, urlfetch
from google.appengine.ext import ndb, blobstore

class Collection(ndb.Model):
    id = ndb.KeyProperty()
    title = ndb.StringProperty(indexed=False)
    url = ndb.StringProperty(indexed=True)
    modified = ndb.DateTimeProperty()
    item_count = ndb.IntegerProperty()
    item_url = ndb.StringProperty(indexed=False)
    json = ndb.JsonProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        
        url = "http://archive.pathology.umn.edu/api/collections"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            collections = json.loads(result.content)
            for collection in collections:
                new_collection = Collection()
                collection_url = collection['url']
                new_collection.key_name = collection_url
                new_collection.id = ndb.Key(Collection, collection_url)
                new_collection.url = collection_url
                new_collection.put()
                self.response.write(collection['element_texts'][0]['text'])

        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
