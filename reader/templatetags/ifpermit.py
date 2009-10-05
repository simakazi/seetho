# -*- coding: utf-8 -*-
from django.template import Library
from django.template import Node, NodeList, Template, Context, Variable
register=Library()

PermitDict={'C':5,'A':4,'M':3,'R':2,'B':1}

class IfPermitNode(Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfPermitNode>"

    def render(self, context):
	print self.var1,self.var2
        val1 = self.var1.resolve(context, True)
        val2 = str(self.var2)
	print val1,val2
	print PermitDict[val1]
	print PermitDict[val2]
        if (PermitDict[val1] >= PermitDict[val2]):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_ifpermit(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:                 
        raise TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]                                        
    nodelist_true = parser.parse(('else', end_tag))                  
    token = parser.next_token()                                      
    if token.contents == 'else':                                     
        nodelist_false = parser.parse((end_tag,))                    
        parser.delete_first_token()                                  
    else:                                                            
        nodelist_false = NodeList()                                  
    val1 = parser.compile_filter(bits[1])                            
    val2 = parser.compile_filter(bits[2])                            
    return IfPermitNode(val1, val2, nodelist_true, nodelist_false)

#@register.tag
def ifpermit(parser, token):
    """                    
    Outputs the contents of the block if the first arguments rights are above the second's.

    Examples::

        {% ifpermit rights M %}
            ...                              
        {% endifpermit %}                                          
    """                                         
    return do_ifpermit(parser, token)     
ifpermit = register.tag(ifpermit)   