import unittest
import flowtext

class ReflowTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def testConstruction(self):
        """This tests the default constuctor"""
        flow = flowtext.FormatText()
        self.assertEqual(66, flow.getMaxWidth())
        
    def testUnwrap(self):
        flow = flowtext.FormatText()
        testText = ("This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it. ")
        expectedText = ("This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it. ")
        self.assertEqual(expectedText, flow.unwrap(testText))
        
    def testUnwrapTwoParagraphs(self):
        flow = flowtext.FormatText()
        testText = ("This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it.\n\n" + 
            "and sneakily has a second \n" + 
            "paragraph")
        expectedText = ("This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it.\n\n" +
            "and sneakily has a second " + 
            "paragraph")

        self.assertEqual(expectedText, flow.unwrap(testText))

    """
    def testUnwrapQuoted(self):
        pass;
    """
    
    """
    def testFlow(self):
        testText = ("This line spans a few \n" + 
            "lines and has a couple of soft \n" +
            "breaks in it. It also has a very, very long line which spans a little too long and therefore needs to be well wrapped.\n"
            )
        #We are going with the exected output from the unwrap
    """
            
    """             + 
            "\nAfter which there is a new paragraph. This new paragraph has only one long line\n" +
            " And now an indented (therefore quoted) section \n" +
            " which also spans a few lines, with soft line breaks (using the space then crlf convention)\n" +
            "\n>Another quoted test using the greater than sign \n" +
            ">but its otherwise nothing special.\n\n" +
            ">And here I am going to give a soft break \n" +
            ">>And change the quoting depth - this is an illegal operation"
   """
        
    
testSuite = unittest.TestSuite((unittest.makeSuite(ReflowTestCase)))

runner = unittest.TextTestRunner(verbosity = 2)
runner.run(testSuite)