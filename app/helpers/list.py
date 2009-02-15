def header_link(context, label, name, sort, sort_asc, path):

	icon = ''
	class_ = ''
	sort_attr = '%s-desc' % name
	
	if sort == name:
		if not sort_asc:
			class_ = 'asc'
			sort_attr = name
			icon = 'bullet_arrow_down.png'
		else:
			class_ = 'desc'
			sort_attr = '%s-desc' % name
			icon = 'bullet_arrow_up.png'
			
	context.write('''<th class="sorted %s %s" onclick="document.location.href='/%s/?s=%s'">''' % (class_, name, path, sort_attr))
	context.write('''<a href="/%s/?s=%s">%s</a>''' % (path, sort_attr, label))
	
	if icon: context.write('<img src="/shrub/images/%s"/></th>' % icon)
	return ''
	
def if_even(context, n, if_label, else_label):
	if n % 2 == 0:
		return if_label
	else:
		return else_label

