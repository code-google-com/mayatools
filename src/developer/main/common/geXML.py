# References
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import os.path
from multiprocessing.connection import _xml_dumps

# Public Constants
XML_PATH_DEFAULT = os.path.dirname(os.path.abspath(__file__)) + '\\testHung3.xml';

def get_first(iterable, default=None):
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
    def initXmlPath(self, xmlPath):
        global XML_PATH_DEFAULT
        
        if os.path.isfile(xmlPath):
            self._xmlPath = xmlPath
        else:
            self._xmlPath = XML_PATH_DEFAULT
    
    # Save XML file.
    def save(self):
        xmlFile = open(self._xmlPath, 'w')
        xmlFile.write(self._doc.toprettyxml())
        xmlFile.close()
    
    # Create history XML file.
    def createHistory(self, xmlPath):
        self._doc = Document()
        nodeHistory = self._doc.createElement('history')
        self._doc.appendChild(nodeHistory)
        
        self.save()
    
    # Write info to history.
    def writeHistory(self, element, value):
        elemmentsNodes = self._doc.getElementsByTagName(element + 's')
        elemmentsNode = get_first(elemmentsNodes)
        
        if not elemmentsNode:
            elemmentsNode = self._doc.createElement(element + 's')
            self._doc.firstChild.appendChild(elemmentsNode)
        
        elemmentNode = self._doc.createElement(element)
        elemmentNode.setAttribute('value', value)
        elemmentsNode.appendChild(elemmentNode)
        
        self.save()
    
    # Write info to history XML file.
    def writeHistoryFile(self, xmlPath, element, value):
        self.initXmlPath(xmlPath)
        
        if os.path.exists(self._xmlPath):
            self._doc = parse(self._xmlPath)
        else:
            self.createHistory(self._xmlPath)
        
        self.writeHistory(element, value)
    
    # Get info from history.
    def readHistory(self, element):
        elemmentsNodes = self._doc.getElementsByTagName(element + 's')
        
        if elemmentsNodes == None:
            return Node
        else:
            elementResults
            for elementNode in elemmentsNodes:
                elementResults.append(elementNode.getValue())
            return elementResults
    
    # Get info from history XML file.
    def readHistoryFile(self, xmlPath, element):
        self.initXmlPath(xmlPath)
        
        if os.path.exists(self._xmlPath):
            self._doc = parse(self._xmlPath)
            return self.readHistory(element)
        else:
            return None
    
    # Test: write IP server info to XML file.
    def writeIpServer(self, xmlPath, ipServer):
        if not xmlPath:
            xmlPath = _xmlPathDefault
        
        doc = Document()
        nodeRoot = doc.createElement('history')
        nodeHost = doc.createElement('host')
        
        nodeIpServer = doc.createElement('ipServer')
        nodeIpServer.setAttribute('value', ipServer)
        nodeHost.appendChild(nodeIpServer)
        nodeRoot.appendChild(nodeHost)
        doc.appendChild(nodeRoot)
        
        xmlFile = open(xmlPath, 'w')
        xmlFile.write(doc.toprettyxml())
        xmlFile.close()
        
        return
       
    # Test: read IP server info from XML file.
    def readIpServer(self, xmlPath):
        if (not xmlPath) or (os.path.isfile(xmlPath)) :
            dom = parse('test.xml')
        else:
            dom = parse(xmlPath)
        return