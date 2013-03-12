from django import template
import time
register = template.Library()

def t():
    return time.ctime()
    
register.filter(t)
