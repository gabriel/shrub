import cgi

def if_tag(context, item, name, html_escape=False):
	value = getattr(item, name)
	if value:
		context.write('<%s>' % (name))
		context.write(cgi.escape(value, True) if html_escape else value)
		context.write('</%s>\n' % (name))
		
	return ''

