# -*- coding: utf-8 -*-
from django.template import Library
from django.template import Node, NodeList, Template, Context, Variable
from django.template.defaultfilters import stringfilter
register=Library()

PermitDict={'C':5,'A':4,'M':3,'R':2,'B':1,'N':0}
FullRights={'C':'creator','A':'admin','M':'moderator','R':'reader','B':'banned','N':'nobody'}

@register.filter
@stringfilter
def full_right(val):
    return FullRights[val]

class IfPermitNode(Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfPermitNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = str(self.var2)
        if (PermitDict[val1] >= PermitDict[val2]):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_ifpermit(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, u"%r takes two arguments" % bits[0]
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
    return do_ifpermit(parser, token)
ifpermit = register.tag(ifpermit)