"""
Get BBC News Program 

	This program is for get BBC news' title, news text
	Version 1.4
	Devloped 2016/07/30

	news titles -> bbc_news_list.txt
	news contents -> ./news_contents/ 


	ver1.1	news code name changed.  2016/01/03
	ver1.2	relative pathname to absolute pathname	
		Output file name changed 2016/02/07 
	ver1.3  2016/07/15
		For Main PC : Ubuntu
		Datetime Modified
		file pass Modified

	ver1.4 url error modified
"""

import requests
from bs4 import BeautifulSoup
from flask import jsonify
import re
import csv
import datetime
import locale

# -*- coding: utf-8 -*-



def make_soup_from(url):
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html,"lxml")
	return soup

if __name__ == "__main__":
	
	"""
	Data Input from past stmulated data
	"""
	### file pass
	ap = '/home/akihiro-fujii/Programs'	#absolute pass
		
	
	n_data = []
	n_keys = []
	n_titles = []

	f1 = open(ap + '/Cygwin_Programs/main_programs/Datas/get_news/bbc_news_list.txt','r') ## stmulated data
	all_data = f1.read()
	f1.close()

	past_news_dic = {}

	lines_d = all_data.split('\n')
	
	i = 0
	for line in lines_d:
		datas = line.split('\t')
		if len(datas) == 2:
			n_keys.append(datas[0])
			n_titles.append(datas[1])
			past_news_dic[datas[0]] = datas[1]
		elif len(datas) == 1:
#			print('data end')
			pass
		else:
			print('Error code 01')
	
#	print("past_news_dic")
#	print(past_news_dic)
			

	"""
	Data Input from BBC latest news
	"""

	url = "http://www.bbc.com/news"
	soup = make_soup_from(url)
	News_title = []
	News_keys = []
	titles = soup.find_all("span",{"class":"title-link__title-text"})
	nids = soup.find_all("a",{"class":"title-link"})
	for opt in nids:  ### Get news codes
		code =  opt['href'].split("/")
		News_keys.append(opt['href'])


	for title in titles: ### Get news titles
		News_title.append(title.text)

	n = len(News_title)
	n2 = len(News_keys)
	news_dic = {}





	news_codes = []
#	print(n)

	if  n != n2 :
		print ('Error Code 02')
	else:	
#		for i in range(0,n):

		"""
		Check the news which is latest. Old news is already input in bbc_news_list.txt.
		"""
		for k in range(0,n):
			news_dic[News_keys[k]] = News_title[k]
#			print("News_keys[k]   :",News_keys[k])


		new_one = 0
		f = open(ap + '/Cygwin_Programs//main_programs/Datas/get_news/bbc_news_list.txt', 'a')
		for k in range(0,n):
			news_dic[News_keys[k]] = News_title[k]
			

			if not (News_keys[k] in past_news_dic):
				new_one = 1
				news_codes = News_keys[k].split("/")
				for news_code in news_codes:
					print("news_code    :",news_code)

					
				url = "http://www.bbc.com"+News_keys[k]
				error = 0
				print("url = ",url)
				try:
					r = requests.get(url)
				except:
					print("URL Error")
					error = 1
					
				if error == 0:

					print("News Page    :http://www.bbc.com"+News_keys[k])

## 					f.write(News_keys[k])    ### ver1.0
##					f.write(news_codes[2])   ### ver1.1
					f.write(News_keys[k])    ### ver1.4
#					print("news_code[2] :",news_codes[2])   ### ver1.1
					f.write('\t')
					f.write(News_title[k])
					print("News_title[k] :",News_title[k])
					f.write('\n')
#					print("News_keys[k]  :",News_keys[k])

					f_name = ap + "/Cygwin_Programs/main_programs/Datas/get_news/news_contents/bbc_" + news_codes[2] +".cont"
					print(news_codes[2])
					f1 = open(f_name, 'w')
					soup = make_soup_from(url)
		
					#################################
					####   Date and time,title    ###
					#################################
					f1.write(str(datetime.datetime.today()))
					f1.write('\n')
					main_data = soup.find("script",{"type":"application/ld+json"})
					if isinstance(main_data,type(None)) == False:
						m_datas = str(main_data).split('\n')
						n = len(m_datas)
						for i in range(0,n):
							if "datePublish" in m_datas[i] :
								j = i
						if j <=  n: 
							f1.write(m_datas[j])
						else:
							f1.write("None Datetime")
	
						f1.write('\n')
	
						f1.write(News_title[k])
					else:
						print("Contents Error")
		
					#################################
					####   News contents          ###
					#################################
					#main = soup.find("div",{"class":"story-body__inner"})
					main = soup.find("div",{"class":"story-body"})
					print(type(main))
					if isinstance(main,type(None)) == False:
						contents = main.find_all("p")
						for content in contents:
							f1.write(str(content.string))
						f1.close()
						print("output succeed")
						print('\n')
					elif isinstance(main,type(None)) == True:
						print('Contents Error')
						f1.write('Contents Error')
					else:
						print('something wrong1')

		if new_one == 0:
			print("No new ones : BBC News")
		f.close()


