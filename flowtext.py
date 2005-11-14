import re

class FormatText:
    """Use this object to perform flow operations on text
    based upon RFC2646. The unwrap routines will take text
    formatted in RFC2646 and give back unformatted lines, perfect
    for a text control in a GUI which does its own wrapping,
    but as it can wrap, and insert quote '>' and ' ' characters
    where necessary, it is very good for formatting text for viewing."""
    
    def __init__( self, maxwidth = 66 ):
        """The parameter maxwidth specifies the maximum width 
        for a line. Its default is 66 as this is recommmended in
        RFC 2646 that 66 character lines are most readable"""
        self.setMaxWidth( maxwidth )
        #Set a useful item
        self.softnewlines = " (?:[\r\n]{1,2})(?![\r\n]{1,2})"
    
    def getMaxWidth( self ):
        return self.maxwidth
    
    def setMaxWidth( self, maxwidth ):
        """The maximum width you may specify here is 79. This
        will ensure it displays correctly even on a non-flowed program.
        Typically, column 80 is reserved for the line-wrap indicator"""
        if not isinstance( maxwidth, int ):
            raise TypeError( "Parameter to setMaxWidth must be an integer" )
        if maxwidth > 79:
            raise ValueError( "RFC2646 Specifies a maximum of 79 characters" )
        self.maxwidth = maxwidth
    
    def flow( self, text ):
        """This is the real workhorse function,
        The parameter text contains the text to 
        be flowed"""
        if not isinstance( text, str ):
            raise TypeError( "Parameter to flow must be of type string" )
        #Deal with unflowing everything, removing all soft breaks
        #unflow quoted strings (but place back in quote level)
        
        #Reflow each line
        
    def unwrapquoted( self, text ):
        """This will unwrap the text, dealing specifically with quoted stuff
        and try to keep paragraphs together"""
        #quotematch = "(?:(?:[> ]+)|(?:From ))"
        quotematch = "(?:[> ]+)"
        expression = "^(?P<quote>" + quotematch + ")(?P<text>.*?)" + self.softnewlines
        #Add the second line - repeated quote then text that is NOT 
        #the quote - note we use (?!...) for negative lookahead
        expression += "(?:(?P=quote))"
        #?" + "(?!" + quotematch + ")"
        replace = "\g<quote>\g<text> "
        return re.sub( string = text, pattern=expression, repl= replace)

        
    def unwrap( self, text ):
        """This will unwrap the text and try to keep paragraphs together"""
        expression = self.softnewlines
        replace = " "
        return re.sub( string = text, pattern=expression, repl= replace)

    
#    def unwrap(self, text):
#        """This will unwrap the text and try to keep paragraphs together"""
#        whitespace = False
#        newtext = ''
#        knownquotes = ['From ','>',' ']
#        quotechars = ''
#        oldquotechars = ''
#        newpara = True
#        newline = True
#        for char in text:
#            if char == '\n':
#                newline = True
#                oldquotechars = quotechars;
#                quotechars = ''
#                
#            if(newline and not whitespace):
#                newpara = True
#                oldquotechars = ''                
#            if not (whitespace and newline):
#                newtext += char
#                
#            #Handle quoting
#            if
#            #Handle whitespace
#            if char == ' ' or char == '\t':
#                whitespace = True
#            else:
#                whitespace = False
#                
#        return newtext
                
                
                
        
        
            