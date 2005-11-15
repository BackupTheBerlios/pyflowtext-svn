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
        self.newline = r"\n"
        self.softnewlines = " " + self.newline + r"(?![\n])"
        #self.softnewlines = " (?:[\r\n]{1,2})(?![\r\n]{1,2})"
        
    def standardiseNewlines(self, text):
        """This function turns ALL newlines into a simple \n sequence.
        Thus simplifiying our job a little"""
        anynewline = r"((?:\r\n)|(?:\n\r)|(?:\n)|(?:\r))"
        replace = r"\n"
        return re.sub(string = text, pattern=anynewline, repl=replace )
    
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
        
    def unwrapquoted( self, text, debug = False ):
        """This will unwrap the text, dealing specifically with quoted stuff
        and try to keep paragraphs together"""
        text = self.standardiseNewlines(text)

        #This class offers a callable to be used in the callback for
        #the regular expression replace
        class quotedpatternmatcher:
            def __init__( self, debug ):
                self.quotelevel = None
                self.debug = debug
                
            def __call__( self, matchobj ):
                #if we have a quote, and not after a soft new line(wrap)
                if matchobj.group( "quotenotsoft" ):
                    if(self.debug):
                        print "\nNotsoft Replacing the quotelevel object '" , self.quotelevel, \
                                "' with '" +  matchobj.group( "quotenotsoft" ) + "'"
                    #then set quotelevel to the new quote
                    self.quotelevel = matchobj.group( "quotenotsoft" )                
                    #and return (with out changing anything)
                    return matchobj.group( 0 )
                
                #if we have a quote pattern (after a soft break)
                if matchobj.group( "quote" ):
                    # If we have a previously stored quote level
                    #  and this one doesnt match
                    if ( self.quotelevel != matchobj.group( "quote" ) ):
                        #   reset the quote level to the new one
                        if(self.debug):
                            print "\nReplacing the quotelevel object '" + self.quotelevel + \
                                "' with '" +  matchobj.group( "quote" ) + "'"
                        self.quotelevel = matchobj.group( "quote" )
                        #   dont continue the line (less soft break)
                        return "\n" + matchobj.group( "quote" )
                    elif (self.debug):
                        print "Keeping quote level, and unwrapping"
                else:                    
                    if(self.debug):
                        print "\nSimple unwrap - removing soft break"
                    pass;
                    #if(self.debug):
                    #    print "\nSoft Discarding quotelevel object"
                    #self.quotelevel = None
                    # join the line by returning a single space (removing the softbreak and quote)
                return " "

        #quotematch = "(?:(?:[> ]+)|(?:From ))"
        quotematch = "(?:[> ]+)"
        #A newline followed by a quotematch(or not)
        expression = "(?:(?:"+ self.softnewlines + ")(?P<quote>" + quotematch + ")?"
        #or a quotematch at the start of a line
        expression += "|^(?P<quotenotsoft>" + quotematch + "))"        
        #either followed by something that is NOT a quotematch
        expression += "(?!" + quotematch + ")"
        #Decision has been to go with complex pattern matcher
        replace = quotedpatternmatcher(debug)
        return re.sub( string = text, pattern=expression, repl=replace )
    
        

        
    def unwrap( self, text ):
        """This will unwrap the text and try to keep paragraphs together"""
        expression = self.softnewlines
        replace = " "
        return re.sub( string = text, pattern=expression, repl= replace )

    
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
                
                
                
        
        
            