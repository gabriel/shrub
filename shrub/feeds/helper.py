import cgi

def if_tag(context, item, name, html_escape=False):  
  value = getattr(item, name)
  if value:
    context.write('<%s>' % name)
    if html_escape:
      context.write(cgi.escape(value, True))
    else:
      context.write(value)
    context.write('</%s>\n' % name)
    
  return ''
