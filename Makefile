push:
	git add .
	git commit -m 'update'
	git push origin master

run:
	python app.py data output
