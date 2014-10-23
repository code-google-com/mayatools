# References
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import os.path
from multiprocessing.connection import _xml_dumps

# Public Constants
XML_PATH_DEFAULT = os.path.dirname(os.path.abspath(__file__)) + '\\testHung3.xml';

# Public Function
# Get first element of array.
# Reference: http://stackoverflow.com/questions/363944/python-idiom-to-return-first-item-or-none
def getFirst(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

class cGeXML:
    #######################################################################################
    
    # Private Properties
    # XML file path.
    _xmlPath = None
    # XML document.
    _doc = None
    
    #######################################################################################
    
    # Public Functions
    # Initialization class.
    def __init__(self):
        self._xmlPath = ''
        self._doc = None
    
    # Initialization XML path.
    # Check xmlPath is true, if not, use default.
    def initXmlPath(self, xmlPath):
        global XML_PATH_DEFAULT
        
        if xmlPath == None:
            self._xmlPath = XML_PATH_DEFAULT
            return
        
        if xmlPath == '':
            self._xmlPath = XML_PATH_DEFAULT
            return
            
        if os.path.isfile(xmlPath):
            self._xmlPath = xmlPath
            return
        
        self._xmlPath = XML_PATH_DEFAULT
    
    # Save XML file.
    # Save current _doc content to XML file.
    def save(self):
        xmlFile = open(self._xmlPath, 'w')
        xmlFile.write(self._doc.toprettyxml())
        xmlFile.close()
    
    # Create XML file.
    # Create XML, create type-tag nodeRoot.
    def create(self, xmlPath):
        self._doc = Document()
        nodeRoot = self._doc.createElement('root')
        self._doc.appendChild(nodeRoot)
        
        self.save()
    
    # Write info.
    # Write element & value to type-tag.
    def write(self, type, element, value):
        nodeSType = self._doc.getElementsByTagName(type)
        nodeType = getFirst(nodeSType)
        
        if not nodeType:
            nodeType = self._doc.createElement(type)
            self._doc.firstChild.appendChild(nodeType)
        
        nodeSElementS = nodeType.getElementsByTagName(element + 's')
        nodeElementS = getFirst(nodeSElementS)
        
        if not nodeElementS:
            nodeElementS = self._doc.createElement(element + 's')
            nodeType.appendChild(nodeElementS)
        
        nodeElement = self._doc.createElement(element)
        nodeElement.setAttribute('value', value)
        nodeElementS.appendChild(nodeElement)
        
        self.save()
    
    # Write info to XML file.
    def writeFile(self, xmlPath, type, element, value):
        if value == None:
            return
        
        if value == '':
            return
        
        self.initXmlPath(xmlPath)
        
        if os.path.exists(self._xmlPath):
            try:
                self._doc = parse(self._xmlPath)
            except:
                self.create(self._xmlPath)
        else:
            self.create(self._xmlPath)
        
        self.write(type, element, value)
    
    # Get info.
    # Get info from type-tag
    def read(self, type, element):
        nodeSType = self._doc.getElementsByTagName(type)
        nodeType = getFirst(nodeSType)
        if not nodeType:
            return None
        
        nodeSElementS = nodeType.getElementsByTagName(element + 's')
        nodeElementS = getFirst(nodeSElementS)
        if nodeElementS == None:
            return None
        
        nodeSResult = nodeElementS.getElementsByTagName(element)
        nodeResult = getFirst(nodeSResult)
        if nodeResult == None:
            return None
        
        resultS = []
        for nodeResult in nodeSResult:
            resultS.append(nodeResult.getAttribute('value'))
        return resultS
    
    # Get info from XML file.
    def readFile(self, xmlPath, type, element):
        self.initXmlPath(xmlPath)
        
        if os.path.exists(self._xmlPath):
            self._doc = parse(self._xmlPath)
            return self.read(type, element)
        else:
            return None