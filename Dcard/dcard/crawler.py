import requests

Dcard_API = 'https://www.dcard.tw/service/api/v2/{ctype}'

class Type:
    posts = 'posts/'
    id = 'posts/{id}'

class Dcard:
    def __init__(self, ctype, id=None, comment=False):
        self.ctype = ctype
        self.id = id
        self.comment = comment
    
    def crawler(self):
        self._url()
        self._comment()
        self._requests()

        if self.ctype == Type.posts:
            return self._return__posts()
        elif self.ctype == Type.id:
            return self._return__id()
    
    def _url(self):
        ctype=self.ctype.format(id=self.id)
        self.rurl = Dcard_API.format(
            ctype=ctype
        )
    
    def _comment(self):
        if self.comment:
            self.curl = self.rurl+'/comments'
    
    def _requests(self):
        r = requests.get(self.rurl)
        self.rjson = r.json()
        
        if self.comment:
            rcomments = requests.get(self.curl)
            self.allcomments = list()
            self.comment_json = rcomments.json()

            for com in self.comment_json:
                self.allcomments.append(com['content'])
            
    def _return__id(self):
        rdict = {
            'id': self.rjson['id'],
            'title': self.rjson['title'],
            'content': self.rjson['content'],
            'createdAt': self.rjson['createdAt'],
            'tags': self.rjson['tags'],
            'topics': self.rjson['topics'],
            'forumName': self.rjson['forumName']
        }
        
        if self.comment:
            rdict['allcomments'] = self.allcomments

        return rdict
    
    def _return__posts(self):
        for post in self.rjson:
            yield {
                'id': post['id'],
                'title': post['title'],
                'excerpt': post['excerpt'],
                'createdAt': post['createdAt'],
                'tags': post['tags'],
                'topics': post['topics'],
                'forumName': post['forumName']
            }
