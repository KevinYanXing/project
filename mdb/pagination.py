# --*-- coding:utf-8 --*--
from math import ceil

class Paged(object):
    def __init__(self,datas,page,per_page,total):
        '当前页数'
        self.page = int(page)
        '每页数据数'
        self.per_page = int(per_page)
        '总数据数'
        self.total = total
        '当前页数据'
        self.items = datas
        
    @property
    def pages(self):
        """The total number of pages"""
        return int(ceil(self.total / float(self.per_page)))
    
    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1
 
    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages
    
    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1
    
    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
    
 