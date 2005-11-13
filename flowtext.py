class FormatText:
    """Use this object to perform flow operations on text
    based upon RFC2646. The unwrap routines will take text
    formatted in RFC2646 and give back unformatted lines, perfect
    for a text control in a GUI which does its own wrapping,
    but as it can wrap, and insert quote '>' and ' ' characters
    where necessary, it is very good for formatting text for viewing."""
    
    def __init__(self, maxwidth = 66):
        """The parameter maxwidth specifies the maximum width 
        for a line. Its default is 66 as this is recommmended in
        RFC 2646 that 66 character lines are most readable"""
        self.maxwidth = maxwidth
    
    def getMaxWidth(self):
        return self.maxwidth
    
    def setMaxWidth(self, maxwidth):
        if not isinstance(maxwidth, int):
            raise TypeError("Parameter to setMaxWidth must be an integer")
        self.maxwidth = maxwidth
    
    def flow(self, text):
        """This is the real workhorse function,
        The parameter text contains the text to 
        be flowed"""
        if not isinstance(text, str):
            raise TypeError("Parameter to flow must be of type string")
        #Deal with unflowing everything, removing all soft breaks
        #unflow quoted strings (but place back in quote level)
        
        #Reflow each line
        
    def unwrap(self, text):
        """This will unwrap the text and try to keep paragraphs together"""
        whitespace = False
        newchars = ''
        for char in text:
            if not (whitespace == True and char == '\n'):
                newchars += char
            if char == ' ' or char == '\t':
                whitespace = True
            else:
                whitespace = False
                
        return newchars
                
                
                
        
        
            