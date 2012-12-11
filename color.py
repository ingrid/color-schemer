from flask import Flask, render_template, request, url_for
import urllib2
from bs4 import BeautifulSoup
import re
app = Flask(__name__)
app.config["DEBUG"] = True

colorReg = re.compile("#(([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})?)") 

def make_css_url(base, css):
	return base + css

def find_base_colors(urls):
	def colors(url):
		f = urllib2.urlopen(url)
		data = f.read()
		matches = re.findall(colorReg, data)
		return [m[0] for m in matches]

	all = []
	for url in urls:
		all.extend(colors(url))
	return all

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fix", methods=['POST'])
def fix():
	url = request.form['url']
	if url[-1] != '/':
		url += '/'
	f = urllib2.urlopen(url)
	data = f.read()
	soup = BeautifulSoup(data)
	styles = []
	for link in soup.find_all('link'):
		if link.has_key('href'):
			cssurl = make_css_url(url, link.get('href'))
			styles.append(cssurl)
	base_colors = find_base_colors(styles)
	return render_template('fix.html', styles=styles, body=soup.body, colors=base_colors)

if __name__ == "__main__":
    app.run()
