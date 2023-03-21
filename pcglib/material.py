from random import choice
from random import choices

class material():
    def __init__(self, ids, selector='rand',weights=None):
        selector_types = ['rand','weighted','perlin', 'perlin2d','perlin3d']

        if selector not in selector_types:
            raise ValueError("Invalid selector {s}, expected one of :{t}".format(s=selector, t=selector_types))
        
        self.f = selector
        self.ids = ids

        if selector == 'rand':
            pass

        elif selector == 'weighted':
            self.weigths = weights

        elif selector == 'perlin':
            self.weigths = weights


    def get(self,*args):
        if self.f == 'rand':
            return choice(self.ids)

        elif self.f == 'weighted':
            return choices(self.ids, weights=self.weigths, k=1)
        
        elif self.f == 'perlin':
            pass

