import flowtext
import unittest

class ReflowTestCase( unittest.TestCase ):
    def setUp( self ):
        pass
    
    def testConstruction( self ):
        flow = flowtext.FormatText()
        self.assertEqual( 66, flow.getMaxWidth() )
        #Try constructing again
        flow = flowtext.FormatText( 23 )
        self.assertEqual( 23, flow.getMaxWidth() )
    
    def testSetMaxWidth( self ):
        flow = flowtext.FormatText()
        flow.setMaxWidth( 40 )
        self.assertEqual( 40, flow.getMaxWidth() )
        def setOverWide():
            flow.setMaxWidth( 99 )
        self.assertRaises( ValueError, setOverWide )
        
    def testUnwrap( self ):
        flow = flowtext.FormatText()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it. " )
        expectedText = ( "This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it. " )
        self.assertEqual( expectedText, flow.unwrap( testText ) )

    def testNegativeUnwrap( self ):
        flow = flowtext.FormatText()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it. " )
        self.assertNotEqual( testText, flow.unwrap( testText ) )    
    
    def testUnwrapTwoParagraphs( self ):
        flow = flowtext.FormatText()
        testText = ( "This line spans a few \n" +
            "lines and has a couple of soft \n" +
            "breaks in it.\n\n" + 
            "and sneakily has a second \n" + 
            "paragraph" )
        expectedText = ( "This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it.\n\n" +
            "and sneakily has a second " + 
            "paragraph" )

        self.assertEqual( expectedText, flow.unwrap( testText ) )
                
    
    def testUnwrapQuotedWithSpace( self ):
        flow = flowtext.FormatText()
        testText = ( " This line is \n" +
            " quoted and has a couple of soft \n" +
            " breaks in it." )
        expectedText = ( " This line is " +
            "quoted and has a couple of soft " +
            "breaks in it." )

        self.assertEqual( expectedText, flow.unwrapquoted( testText ) )

    def testBUnwrapQuotedWithGt( self ):
        flow = flowtext.FormatText()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it." )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it." )

        self.assertEqual( expectedText, flow.unwrapquoted( testText ) )

    def testASimpleUnwrapQuotedWithGt( self ):
        flow = flowtext.FormatText()
        testText = ( ">This line is \n>quoted" )
        expectedText = ( ">This line is quoted" )

        self.assertEqual( expectedText, flow.unwrapquoted( testText ) )    

    def testUnwrapMixedNormalAndQuoted( self ):
        flow = flowtext.FormatText()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n\n" +
            "This line is not \n" + 
            "quoted" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            "This line is not " + 
            "quoted" )
            
        self.assertEqual( expectedText, flow.unwrapquoted( testText ) )

    def testUnwrapTwoQuotedLines( self ):
        flow = flowtext.FormatText()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n\n" +
            ">This line is also \n" + 
            ">quoted" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            ">This line is also " + 
            "quoted" )
    
    
    def testUnwrapMixedQuoted( self ):
        flow = flowtext.FormatText()
        testText = ( ">This line is \n" +
            ">quoted and has a couple of soft \n" +
            ">breaks in it.\n\n" +
            " This line is also \n" + 
            " quoted" )
        expectedText = ( ">This line is " +
            "quoted and has a couple of soft " +
            "breaks in it.\n\n" +
            " This line is also " + 
            "quoted" )

        self.assertEqual( expectedText, flow.unwrapquoted( testText ) )
    
    def testUnwrapAll( self ):
        flow = flowtext.FormatText()
        testText = ( "This line spans a few \n" + 
            "lines and has a couple of soft \n" +
            "breaks in it. It also has a very, very long line which spans a little " +
            "too long and therefore needs to be well wrapped.\n" + 
            "\nAfter which there is a new paragraph. This new paragraph has only " + 
            "one long line\n" +
            " And now an indented (therefore quoted) section \n" +
            " which also spans a few lines, with soft line breaks (using the space " +
            "then crlf convention)\n" +
            "\n>Another quoted test using the greater than sign \n" +
            ">but its otherwise nothing special.\n\n" +
            ">And here I am going to give a soft break \n" +
            ">>And change the quoting depth - this is an illegal operation" )
        expectedText = ( "This line spans a few " + 
            "lines and has a couple of soft " +
            "breaks in it. It also has a very, very long line which spans a little " +
            "too long and therefore needs to be well wrapped.\n" + 
            "\nAfter which there is a new paragraph. This new paragraph has only " + 
            "one long line\n" +
            " And now an indented (therefore quoted) section" +
            " which also spans a few lines, with soft line breaks (using the space " +
            "then crlf convention)\n" +
            "\n>Another quoted test using the greater than sign " +
            "but its otherwise nothing special.\n\n" +
            ">And here I am going to give a soft break \n" +
            ">>And change the quoting depth - this is an illegal operation" )
        self.assertEqual( expectedText, flow.unwrap( testText ) )

testSuite = unittest.TestSuite( ( unittest.makeSuite( ReflowTestCase ) ) )

runner = unittest.TextTestRunner( verbosity = 2 )
runner.run( testSuite )