import re

class parser:
    """Use this object to perform flow operations on text
    based upon RFC2646. The unwrap routines will take text
    formatted in RFC2646 and give back unformatted lines, perfect
    for a text control in a GUI which does its own wrapping,
    but as it can wrap, and insert quote '>' and ' ' characters
    
    where necessary, it is very good for formatting text for viewing."""
    
    #This class holds the RFC2646 ABNF Spec 
    #Define the rules with regexp
    non_sp      = "(?:[^ ^\0^\r^\n])"
    text_char   = "(?:%s| )" % non_sp
    text        = "(?:%s*)" % text_char
    quote       = "(?:[>]+)"
    sigsep      = "(?:%s?-- \n)" % quote
    stuffing    = "(?: ?)"
    stuffed     = "(?:%s? )" % (quote)
    flow_unqt   = "(?:%s?%s +\n)" % (stuffing, text)
    flow_qt     = "(?:%s?%s?%s +\n)" % (quote, stuffing, text)
    flowed_line = "(?:%s|%s)" % (flow_qt , flow_unqt)
    fixed       = "(?:%s?%s?%s%s\n)" % (quote, stuffing, text, non_sp)
    fixed_line  = "(?:%s|%s)" % (fixed, sigsep)
    paragraph   = "(?:%s+%s)" % (flowed_line, fixed_line)
    #create a match dictionary - starting with the most derived, working 
    #backwards
    matchdict = {"paragraph":re.compile(paragraph), "fixed-line":re.compile(fixed_line), 
                 "fixed":re.compile(fixed), "flowed-line":re.compile(flowed_line),
                 "flow-qt":re.compile(flow_qt), "flow-unqt":re.compile(flow_unqt),
                 "stuffing":re.compile(stuffing), "sigsep":re.compile(sigsep),
                 "quote":re.compile(quote), "text":re.compile(text),
                 "text-char":re.compile(text_char),"non-sp":re.compile(non_sp)}
                 
    def __init__( self, maxwidth = 66 ):
        """The parameter maxwidth specifies the maximum width 
        for a line. Its default is 66 as this is recommmended in
        RFC 2646 that 66 character lines are most readable"""
        self.setMaxWidth( maxwidth )
        
    anynewline = re.compile(r"((?:\r\n)|(?:\n\r)|(?:\n)|(?:\r))")
        
    def standardiseNewlines( self, text ):
        """This function turns ALL newlines into a simple \n sequence.
        Thus simplifiying our job a little"""
        replace = r"\n"
        return self.anynewline.sub( replace, text)
    
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

    def flow( self, text, debug=False ):
        """This is the real workhorse function,
        The parameter text contains the text to 
        be flowed"""
        if not isinstance( text, str ):
            raise TypeError( "Parameter to flow must be of type string" )
        return self.wrap(self.unwrap(text, debug), debug)

        
    def matches(self, rule, text):
        """matches(rule, text)
        Will return True if this text meets the requirements of the specified
        rule according to the rules from the 2646 ABNF"""
        if self.matchdict[rule].match(text):
            return True;
        return False;
    
    def getComponent(self, rule, text):
        """getComponent(rule, text)
        Will return a matching component if its rule is matched in the text
        rule according to the rules from the 2646 ABNF"""
        matchObj = self.matchdict[rule].search(text)
        if matchObj:
            return matchObj.group(0);
        return False;
    
    def bestMatch(self, text):
        """minMatch(text)
        Will return the best level of matching we can get from the ABNF
        rules for RFC2646."""
        for item in self.matchdict.iteritems():
            matchObj = item[1].match(text)
            if (matchObj and matchObj.group(0) == text):
                return item[0]
        return None
    
    def lineMatches(self, text):
        """lineMatches(text)
        Will return a list of the best matches for each line"""
        output=[]
        for line in text.splitlines(True):
            output.append(self.bestMatch(line))
        return output
    
    def unwrap(self, text, debug=False):
        """unwrap(text)
        Will uwrap a string to RFC2646 - using the BNF definition.
        Note the text passed in must be terminated with a CRLF"""
        output = []
        quotedepth = None
        lastLineFlowed = False
        for line in text.splitlines(True):
            #Simplest case - the fixed line
            currentQuote = self.getComponent("quote", line)
            if (lastLineFlowed and re.match(self.stuffed, line)):
                if debug:
                    print "Removing stuffing\n"
                #remove the stuffing
                line = re.sub("^(%s?) " % (self.quote), "\g<1>", line)                    
            if self.matches("fixed-line", line):
                if debug:
                    print "Fixed line\n"
                if currentQuote:
                    if currentQuote == quotedepth:
                        #strip the quotes if we are at depth
                        line = re.sub("^%s" % currentQuote, '', line)
                    else:
                        if lastLineFlowed:
                            line = ''.join(('\n', line))
                #Fixed lines always reset quotedepth
                quotedepth = None
                lastLineFlowed = False
            #The flowed line
            elif self.matches("flowed-line", line):
                if debug:
                    print "Flowed line\n"
                line = line[:-1]
                if quotedepth and currentQuote == quotedepth:
                    if debug:
                        print "\tQuoted at same depth\n"                    
                    #strip the quotes if we are at depth
                    line = re.sub("^%s" % currentQuote, '', line)
                #Mismatched level
                elif currentQuote:
                    if debug:
                        print "\tQuote depth changed\n"
                    quotedepth = currentQuote
                    if lastLineFlowed:
                        line = ''.join(('\n', line))
                lastLineFlowed = True
            output.append(line)
        return ''.join(output)
    
    def wrap( self, text, debug = False ):
        """This function will wrap back up a text that has previously 
           been unwrapped properly - using our current settings"""
        output = []    
        #Match a possible newline
        for line in text.splitlines(True):
            #Match the quote characters
            quoteMatchObj = re.match( "^%s" % self.quote, line )
            if quoteMatchObj:
                quote = quoteMatchObj.group( 0 )
            else:
                quote = ''
            linelength = self.maxwidth - len( quote )
            count = 0
            lastspace = 0
            outputTemp = []
            for char in line[len( quote ):]:
                count += 1
                outputTemp.append( char )
                if char==' ':
                    lastspace = count
                #Its time for a newline
                if count >= linelength and lastspace > 0:
                    #divide at last space
                    output.append( "%s%s" % ( quote, ''.join( outputTemp[:lastspace] ) ) )
                    #reset outputtemp
                    outputTemp = outputTemp[lastspace:]
                    count -= lastspace
                    lastspace = 0
            if debug:
                print "Output temp is currently '%s'\n" % ''.join(outputTemp)
            if count > 0:
                output.append( "%s%s" % ( quote, ''.join( outputTemp ) ) )
        return '\n'.join(output)
    