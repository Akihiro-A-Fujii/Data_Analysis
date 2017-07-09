"""
Get China Daily News Program 

	This program is to get China Daily news' title, news text
	Version 1.0
	Devloped 2015/12/06

	news titles -> china_daily_list.txt
	news contents -> ./news_contents/ 

"""
import requests
from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-



def make_soup_from(url):
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html,"lxml")
	return soup



if __name__ == "__main__":
	
	url = "http://www.chinadaily.com.cn/"
	r = requests.get(url)
	soup = BeautifulSoup(r.text.encode(r.encoding),"lxml")
	contents = soup.find_all("h2")
	
	
	
	News_keys = []
	News_title = []
	
	
	for content in contents:
		if len(content.find("a").get('href')) >= 15:
			if len(str(content.string)) >= 10:
	#			print(content.string, content.find("a").get('href')) 
	#			print(content.string)				## News Title 
	#			print(content.find("a").get('href')) 		## News website
				News_title.append(content.string)		## News Title 
				News_keys.append(content.find("a").get('href'))	## News website
	
	#			f1.write(content.string)
	#			f1.write('\n')
	
	
	
	
	n = len(News_title)
	
	news_dic = {}
	news_codes = []
	
	f1 = open('china_daily_list.txt','r') ## stmulated data
	all_data = f1.read()
	f1.close()
	
	past_news_dic = {}
	n_keys = []
	n_titles = []
	
	
	lines_d = all_data.split('\n')
	
	i = 0
	for line in lines_d:
		datas = line.split('\t')
		if len(datas) == 2:
			n_keys.append(datas[0])
			n_titles.append(datas[1])
			past_news_dic[datas[0]] = datas[1]
		elif len(datas) == 1:
			print('data end')
			pass
		else:
			print('Error code 01')
	
	#	print(past_news_dic)
	
	
	
	
	
	if   len(News_keys) != len(News_title) :
		print ('Error Code 02')
	else:	
	
		f = open('china_daily_list.txt', 'a')
		"""
		Check the news which is latest. Old news is already input in bbc_news_list.txt.
		"""
		for k in range(0,n):
			news_dic[News_keys[k]] = News_title[k]
			print(News_keys[k])
		for k in range(0,n):
			news_dic[News_keys[k]] = News_title[k]
			if not (News_keys[k] in past_news_dic):
				
				news_codes = News_keys[k].split("/")
	
				url = "http://www.chinadaily.com.cn/"+News_keys[k]
				print("NewsURL = http://www.chinadaily.com.cn/"+News_keys[k])
	
				if not (news_codes[0] ==  "travel" or news_codes[0] == "http:"):
					print(news_codes[0])
					f_name = "./news_contents/" + news_codes[-1] +".cont"
					print("title = ", news_codes[-1])
					f1 = open(f_name, 'w')
					soup = make_soup_from(url)
					#for news_code in news_codes:
					#	print(news_code)
					f.write(news_codes[-1])
					f.write('\t')
					f.write(News_title[k])
					f.write('\n')
					print("Good")
					print(news_codes[-1])
		
					#################################
					####   Date and time          ###
					#################################
#					update = soup.find("div", {"id":"Title_e"})
					update = soup.find("span", {"class":"greyTxt6 block mb15"})
					f1.write(str(update))
					f1.write('\n')
					print("Updated:", update)
		
					#################################
					####   News contents          ###
					#################################
					
					contents = soup.find_all("div",{"id":"Content"})
					for content in contents :
						f1.write(content.text)
					f1.close()
					print("output succeed")
					print('\n')
					print('\n')
	
		f.close()
	
	
