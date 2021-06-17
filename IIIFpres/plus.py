# -*- coding: UTF-8 -*-.
class HeightWidthDuration(object):
    def set_width(self,width):
        self.width = width
    
    def set_height(self,height):
        self.height = height
    
    def set_hightwidth(self,height, width):
        self.set_width = width
        self.set_height = height





class ViewingDirection(object):
    def set_viewingDirection(self,viewingDirection):
        """
        left-to-right	The object is displayed from left to right. The default if not specified.
        right-to-left	The object is displayed from right to left.
        top-to-bottom	The object is displayed from the top to the bottom.
        bottom-to-top	The object is displayed from the bottom to the top.
        """
        viewingDirections = ["left-to-right",
        "right-to-left",
        "bottom-to-top",
        "top-to-bottom"]
        msg = "viewingDirection mu must be one of these values %s" %viewingDirections
        assert viewingDirection in viewingDirections, msg
        self.viewingDirection = viewingDirection

class navDate(object):
    def __init__(self):
        self.navDate = None

    def set_navDate(self,date):
        #TODO
        self.navDate = date

class format(object):
    pass