import re

class FormatText:
    """Use this object to perform flow operations on text
    based upon RFC2646. The unwrap routines will take text
    formatted in RFC2646 and give back unformatted lines, perfect
    for a text control in a GUI which does its own wrapping,
    but as it can wrap, and insert quote '>' and ' ' characters
    where necessary, it is very good for formatting text for viewing."""
    #Define a softnew line constant
    softnewlines = "(?<!--) \n(?=[^\n])"
    #TODO: "From " quote style as per RFC
    #The expression is an untagged group of one or more quote 
    #characters. of course - a user may tag this, or extend the group
    quotematch = "(?:[> ]+)"        
    
    def __init__( self, maxwidth = 66 ):
        """The parameter maxwidth specifies the maximum width 
        for a line. Its default is 66 as this is recommmended in
        RFC 2646 that 66 character lines are most readable"""
        self.setMaxWidth( maxwidth )
        
    def standardiseNewlines( self, text ):
        """This function turns ALL newlines into a simple \n sequence.
        Thus simplifiying our job a little"""
        anynewline = r"((?:\r\n)|(?:\n\r)|(?:\n)|(?:\r))"
        replace = r"\n"
        return re.sub( string = text, pattern=anynewline, repl=replace )
    
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

    class wrapReplaceWorker:
        """Helper class for the wrap function only"""        
        def __init__( self, debug ):
            self.quotelevel = None
            self.debug = debug
            self.firstline = True
            
        def __call__( self, matchobj ):
            if self.debug:
                print matchobj.groups()
            #Handle the simplest case
            retval = ""
            if matchobj.group( "newline" ) or self.firstline:
                if matchobj.group( "quote" ):
                    self.quotelevel = matchobj.group( "quote" )
                    retval = self.quotelevel
                else:
                    self.quotelevel = None
                self.firstline = False
            if self.quotelevel:
                return ''.join( ( retval, 
                    matchobj.group( "groupmatch" ), "\n" , self.quotelevel ) )
            else:
                return "%s\n" % matchobj.group( "groupmatch" )
    
    wrapmatch = ''.join((
         #Match a possible newline
         "(?P<newline>\n)?",
         # Match any possible quote characters
         "(?P<quote>%s)?" % quotematch,
        #Match a group named groupmatch, which may be anything that is not a 
        #newline
         "(?P<groupmatch>[^\n]",
        #And there may be between 1 and the maxwidth, but must be followed by a
        #space
        "{1,%s} )"))
        
    def wrap( self, text, debug = False ):
        """This function will wrap back up a text that has previously 
           been unwrapped properly - using our current settings"""
        #Match a possible newline
        boundarymatch = FormatText.wrapmatch % ( self.maxwidth - 1 )
        replace = FormatText.wrapReplaceWorker( debug )
        if debug:
            print "in wrap function:\n"
        return re.sub( boundarymatch, replace, text )

    class unwrapReplaceWorker:
        """This class offers a callable to be used in the callback for
            the regular expression replace. It allows persistance
            Of some variables and user parameters."""
        def __init__( self, debug ):
            self.quotelevel = None
            self.debug = debug
            
        def __call__( self, matchobj ):
            if self.debug:
                print matchobj.groups()
            if not matchobj.group( "softnewline" ):
                if self.debug:
                    print "\nNonsoft newline"
                #if we have a quote, and not after a soft new line(wrap)
                if matchobj.group( "quote" ):
                    if( self.debug ):
                        print "\nNotsoft Replacing the quotelevel object '%s'"\
                                "' with '%s'" % ( self.quotelevel, matchobj.group( "quote" ) )
                    #then set quotelevel to the new quote
                    self.quotelevel = matchobj.group( "quote" )                
                #return (with out changing anything)
                return matchobj.group( 0 )
            #We have got a soft newline
            else:
                if self.debug:
                    print "\nSoft newline matched";
                #if we have a quote pattern (after a soft break)
                if matchobj.group( "quote" ):
                    # If we have a previously stored quote level
                    #  and this one doesnt match
                    if ( self.quotelevel != matchobj.group( "quote" ) ):
                        #   reset the quote level to the new one
                        if( self.debug ):
                            print "\nReplacing the quotelevel object '%s'"\
                                "' with '%s'" % ( self.quotelevel, matchobj.group( "quote" ) )
                        self.quotelevel = matchobj.group( "quote" )
                        #   dont continue the line (less soft break)
                        return "\n%s" % matchobj.group( "quote" )
                    elif ( self.debug ):
                        print "Keeping quote level, and unwrapping"
                else:                    
                    if( self.debug ):
                        print "\nSimple unwrap - removing soft break"
                    pass;
                    #if(self.debug):
                    #    print "\nSoft Discarding quotelevel object"
                    #self.quotelevel = None
                    # join the line by returning a single space (removing the softbreak and quote)
                return " "
        
    def unwrap( self, text, debug = False ):
        """This will unwrap the text, dealing specifically with quoted stuff
        and try to keep paragraphs together"""
        text = self.standardiseNewlines( text )

        #here we must start with a softnewline match or the start of a line
        expression = "(?:(?P<softnewline>%s)|(\n|^))" % (FormatText.softnewlines)
        #Then we may (or may not) have a quotematch
        expression += "(?P<quote>%s)?" %( FormatText.quotematch )
        #either followed by something that is NOT a quotematch-making sure we 
        #dont get any more quotematches
        expression += "(?!%s)" % ( FormatText.quotematch )
        #Decision has been to go with complex pattern matcher
        replace = FormatText.unwrapReplaceWorker( debug )
        return re.sub( string = text, pattern=expression, repl=replace )

    def nonReUnwrap( self, text, debug= False ):
        output = ""
        for line in text.splitlines():
            pass
        