'''
Created on Jun 18, 2014

@author: trungtran
'''

try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf

dirUI = ''

form_class, base_class = cf.loadUIPyQt(uiFile)

class assetContentForm(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        