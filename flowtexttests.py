import flowtext
import unittest

class ReflowTestCase( unittest.TestCase ):
    def setUp( self ):
        pass
    
    def testConstruction( self ):
        flow = flowtext.parser()
        self.assertEqual( 66, flow.getMaxWidth() )
        #Try constructing again
        flow = flowtext.parser( 23 )
        self.assertEqual( 23, flow.getMaxWidth() )
    
    def testSetMaxWidth( self ):
        flow = flowtext.parser()
        flow.setMaxWidth( 40 )
        self.assertEqual( 40, flow.getMaxWidth() )
        def setOverWide():
            flow.setMaxWidth( 99 )
        self.assertRaises( ValueError, setOverWide )
        
    def testBasicNormalUnwrap( self ):
        flow = flowtext.parser()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it.\n" )
        expectedText = ( "This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it.\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )    

    def testNegativeUnwrap( self ):
        flow = flowtext.parser()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it. \n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText            
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertNotEqual( testText, outputText )    
    
    def testUnwrapTwoParagraphs( self ):
        flow = flowtext.parser()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it.\n\n" + 
            "and sneakily has a second \n" + 
            "paragraph\n" )
        expectedText = ( "This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it.\n\n" +
            "and sneakily has a second " + 
            "paragraph\n" )

        self.assertEqual( expectedText, flow.unwrap( testText ) )

    def testBUnwrapQuotedWithGt( self ):
        flow = flowtext.parser()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n" )

        self.assertEqual( expectedText, flow.unwrap( testText ) )

    def testASimpleUnwrapQuotedWithGt( self ):
        flow = flowtext.parser()
        testText = ( ">This line is \n>quoted\n" )
        expectedText = ( ">This line is quoted\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )

    def testUnwrapMixedNormalAndQuoted( self ):
        flow = flowtext.parser()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n\n" +
            "This line is not \n" + 
            "quoted\n" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            "This line is not " + 
            "quoted\n" )
            
        self.assertEqual( expectedText, flow.unwrap( testText ) )

    def testUnwrapTwoGTQuotedLines( self ):
        flow = flowtext.parser()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n\n" +
            ">This line is also \n" + 
            ">quoted\n" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            ">This line is also " + 
            "quoted\n" )

        self.assertEqual( expectedText, flow.unwrap( testText ) )
        
    def testUnwrapQuotedWithOnlySoftWrap(self):
        flow = flowtext.parser()
        testText = ( ">This line is \n" +
            "quoted and has a couple of soft \n" +
            "breaks in it.\n")
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n")
        self.assertEqual( expectedText, flow.unwrap( testText ) )
        
    def testUnwrapQuotedWithSoftWrapAndQuoted(self):
        flow = flowtext.parser()
        testText = ( ">This line is \n" +
            "quoted and has a couple of soft \n" +
            ">breaks in it.\n")
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n")
        self.assertEqual( expectedText, flow.unwrap( testText ) )
        
    def testStandardiseNewlines(self):
        flow = flowtext.parser()
        testText = ("This is a basic newline\n" + 
                    "And another type\r" + 
                    "And another\n\r" + 
                    "And yet another\r\n")
        expectedText = ("This is a basic newline\n" + 
                    "And another type\n" + 
                    "And another\n" + 
                    "And yet another\n")
        self.assertEqual( expectedText, flow.standardiseNewlines(testText))
        
    def testUnwrapUsenetSignature(self):
        flow = flowtext.parser()
        testText = ( "This line is \n"
            "quoted and has a couple of soft \n"
            "breaks in it.\n\n"
            ">This line is also \n" 
            ">quoted and has an \n"
            ">example of embaressing wrap\n"
            "-- \n" 
            "And this is a usenet signature\n")
        expectedText = ( "This line is "
            "quoted and has a couple of soft "
            "breaks in it.\n\n"
            ">This line is also "
            "quoted and has an "
            "example of embaressing wrap\n"
            "-- \n"
            "And this is a usenet signature\n")
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        self.assertEqual( expectedText, outputText )       
    
    def testUnwrapEndingWithCr(self):
        flow = flowtext.parser()
        testText = ( "This line ends with a CR which should be untouched\n")
        expectedText = ( "This line ends with a CR which should be untouched\n")
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        self.assertEqual( expectedText, outputText )
        
    def testUnwrapMixedQuoted( self ):
        flow = flowtext.parser()
        testText = ( "This line is \n" +
            "quoted and has a couple of soft \n" +
            "breaks in it.\n\n" +
            ">This line is also \n" + 
            ">quoted and has an \n" + 
            ">example of embaressing wrap\n")
        expectedText = ( "This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            ">This line is also " + 
            "quoted and has an " + 
            "example of embaressing wrap\n")
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        self.assertEqual( expectedText, outputText )
    
    def testUnwrapAll( self ):
        flow = flowtext.parser()
        testText = ( "This line spans a few \n"
            "lines and has a couple of soft \n"
            "breaks in it. It also has a very, very long line which spans a little "
            "too long and therefore needs to be well wrapped.\n"
            "\nAfter which there is a new paragraph. This new paragraph has only "
            "one long line\n"
            " And now an indented (therefore space stuffed) section \n"
            " which also spans a few lines, with soft line breaks (using the space "
            "then crlf convention)\n\n"
            ">Another quoted test using the greater than sign \n"
            ">but its otherwise nothing special.\n\n"
            ">And here I am going to give a soft break \n"
            ">>And change the quoting depth - this is an illegal operation\n" )
        expectedText = ( "This line spans a few "
            "lines and has a couple of soft "
            "breaks in it. It also has a very, very long line which spans a little "
            "too long and therefore needs to be well wrapped.\n"
            "\nAfter which there is a new paragraph. This new paragraph has only "
            "one long line\n"
            " And now an indented (therefore space stuffed) section "
            "which also spans a few lines, with soft line breaks (using the space "
            "then crlf convention)\n\n"
            ">Another quoted test using the greater than sign "
            "but its otherwise nothing special.\n\n"
            ">And here I am going to give a soft break \n"
            ">>And change the quoting depth - this is an illegal operation\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        self.assertEqual( expectedText, outputText )

    def testWrapBasic(self):
        flow = flowtext.parser()
        testText = ( "This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = ("This line is very, very long indeed and will go on and on and on \n"
            "and will be over 66 characters long hopefully forcing the \n"
            "wrapping mechanism into action. Of course we then need to \n"
            "investigate real word boundary wrapping, not merely character \n"
            "splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )    

    def testWrapQuotedNoTrailingCr(self):
        flow = flowtext.parser()
        testText = ( ">This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = (">This line is very, very long indeed and will go on and on and on \n"
            ">and will be over 66 characters long hopefully forcing the \n"
            ">wrapping mechanism into action. Of course we then need to \n"
            ">investigate real word boundary wrapping, not merely character \n"
            ">splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        
    def testWrapQuotedLongQuote(self):
        flow = flowtext.parser()
        testText = ( ">>>>>This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = (">>>>>This line is very, very long indeed and will go on and on \n"
            ">>>>>and on and will be over 66 characters long hopefully forcing \n"
            ">>>>>the wrapping mechanism into action. Of course we then need \n"
            ">>>>>to investigate real word boundary wrapping, not merely \n"
            ">>>>>character splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
            
    def testWrapLongestLine(self):
        flow = flowtext.parser()
        testText = ( "ThisIsAllOneWordAndWillNotBeWrappedThislineisvery,verylongindeedandwillgoonandonandon"
            "andwillbeover66characterslonghopefullyforcingthewrapping"
            "mechanismintoaction.Ofcoursewethenneedtoinvestigaterealword"
            "boundarywrapping,notmerelycharactersplitting\n" )
        expectedText = testText
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )        
    
    def testUnwrapSpaceStuffed(self):
        flow = flowtext.parser()
        testText = ( " >This is a special line, and although it is more than 66 characters, \n"
            " it is space stuffed, and therefore the > should be ignored\n" )
        expectedText = (" >This is a special line, and although it is more than 66 characters, "
            "it is space stuffed, and therefore the > should be ignored\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.unwrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )        
    
    def testWrapQuoted(self):
        flow = flowtext.parser()
        testText = ( ">This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = (">This line is very, very long indeed and will go on and on and on \n"
            ">and will be over 66 characters long hopefully forcing the \n"
            ">wrapping mechanism into action. Of course we then need to \n"
            ">investigate real word boundary wrapping, not merely character \n"
            ">splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        outputText = flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText

        self.assertEqual( expectedText, outputText )
        
class ReflowSpeedTests( unittest.TestCase ):
    def setUp( self ):
        self.flow = flowtext.parser()        
            
    def testWrapSpeedQuoted(self):
        testText = ( ">This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = (">This line is very, very long indeed and will go on and on and on \n"
            ">and will be over 66 characters long hopefully forcing the \n"
            ">wrapping mechanism into action. Of course we then need to \n"
            ">investigate real word boundary wrapping, not merely character \n"
            ">splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        for i in range(0, 10000):
            outputText = self.flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        
        self.assertEqual( expectedText, outputText )
        
    def testWrapSpeedNotQuoted(self):
        testText = ( "This line is very, very long indeed and will go on and on and on "
            "and will be over 66 characters long hopefully forcing the wrapping "
            "mechanism into action. Of course we then need to investigate real word "
            "boundary wrapping, not merely character splitting\n" )
        expectedText = ("This line is very, very long indeed and will go on and on and on \n"
            "and will be over 66 characters long hopefully forcing the \n"
            "wrapping mechanism into action. Of course we then need to \n"
            "investigate real word boundary wrapping, not merely character \n"
            "splitting\n" )
        debug = False
        if(debug):
            print "\n---------------------------\ninput text\n"
            print testText
        for i in range(0, 10000):
            outputText = self.flow.wrap( testText, debug ) 
        if(debug):
            print "\n---------------------------\nExpected text\n"
            print expectedText
            print "\n---------------------------\noutput text\n"
            print outputText
        
        self.assertEqual( expectedText, outputText )


testSuite = unittest.TestSuite( ( unittest.makeSuite( ReflowTestCase ) ) )

runner = unittest.TextTestRunner( verbosity = 2 )
runner.run( testSuite )