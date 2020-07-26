import requests as rq 
import bs4 as bs4
import re
import time

# retorna a string com o código fonte da página com varios vídeos
def download_search_page(query, page):
	url = "https://www.youtube.com/results?search_query={query}&sp=CAI%253D&p={page}"
	urll = url.format(query=query, page=page)
	response = rq.get(urll)

	return response.text

# retorn a string com o código fonte da página do vídeo
def download_video_page(link):
	url = "https://www.youtube.com{link}"
	urll = url.format(link=link)
	response = rq.get(urll)

	link_name = re.search("v=(.*)", link).group(1)

	return response.text

# obter informações sobre o vídeo
def parse_search_page(page_html):
	parsed = bs4.BeautifulSoup(page_html)

	tags = parsed.findAll("a")

	video_list = []

	for e in tags:
		if e.has_attr("aria-describedby"):
			link = e['href']
			title = e['title']
			data = {"link": link, "title": title}
			video_list.append(data)
	return video_list

def parse_video_page(page_html):
	parsed = bs4.BeautifulSoup(page_html, 'html.parser')

	class_watch = parsed.find_all(attrs={"class":re.compile(r"watch")})
	id_watch = parsed.find_all(attrs={"id":re.compile(r"watch")})
	channel = parsed.find_all("a", attrs={"href":re.compile(r"channel")})
	meta = parsed.find_all("meta")

	data = dict()

	for e in class_watch:
		colname = "_".join(e['class'])
		if "clearfix" in colname:
			continue
		data[colname] = e.text.strip()
            
	for e in id_watch:
	    colname = e["id"]
	    data[colname] = e.text.strip()
	            
	for e in meta:
	    colname = e.get("property")
	    if colname is not None:
	    	data[colname] = e["content"]
	        
	for link_num, e in enumerate(channel):
	    data["channel_link_{}".format(link_num)] = e["href"]
        

	return data

