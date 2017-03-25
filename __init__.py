if IN[0]:
	if isinstance(IN[0], list):
		OUT = str(sum([round((x-(y/1000), 2) for x, y in zip(IN[1], IN[0]))]))
else:
	if not isinstance(IN[1], list):
		OUT = str(round(IN[1], 2))