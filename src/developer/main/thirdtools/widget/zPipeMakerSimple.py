from developer.main.thirdtools.fn.python import zPipeMakerSimple
from developer.main.common import commonFunctions as cf

icon = cf.getPath(__file__, 1) + '/icons/zPipeMakerSimple.png'
tooltip = 'Tao he thong pipe:\n\t-Xoay theo cac huong.\n\t-Tu dong unwrap.'

def main():
    zPipeMakerSimple.gui()