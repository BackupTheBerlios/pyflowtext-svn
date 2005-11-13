class formattext:
    """Use this object to perform flow operations on text
    based upon RFC2646."""
    
    def init(self, maxwidth):
        """The parameter maxwidth specifies the maximum width 
        for a line"""
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
        
        
            