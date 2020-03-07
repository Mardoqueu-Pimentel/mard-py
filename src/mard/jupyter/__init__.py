from string import Template

view_template = Template("""
<div style="float:left; width:$percentage;">
	$obj
</div>
""".strip())

b64_pdf_template = Template("""
<object 
	width="$width" height="$height" 
	data="data:application/pdf;base64,$pdf" 
	type="application/pdf" class="internal"
>
</object>
""".strip())


def split_view(*objs):
	return '\n'.join(
		view_template.safe_substitute(percentage=f'{100 // len(objs)}%', obj=obj)
		for obj in objs
	)


def b64_pdf(pdf: bytes, width='100%', height=1080):
	return b64_pdf_template.safe_substitute(
		width=width, height=height, pdf=pdf
	)
