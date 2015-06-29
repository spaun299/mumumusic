class Build:

    def __init__(self,username=None,page=None,bandname=None):
        self._url="http://www.last.fm/"
        self.username=username
        self.page=page
        self.bandname=bandname

    def build(self):
        if self.username!=None and self.page!=None:
            return "%suser/%s/tracks?page=%s" % (self._url,self.username,self.page)
        elif self.username!=None:
            return "%suser/%s" % (self._url,self.username)
        elif self.bandname!=None:
            return "%smusic/%s" % (self._url,self.bandname)

"""class Build1:

    def __init__(self):
        self._url="http://www.last.fm/"

    def build_profile_page(self,username):
        return "%suser/%s" % (self._url,username)


    def build_band_url(self,bandname):
        return "%smusic/%s" % (self._url,bandname)
"""