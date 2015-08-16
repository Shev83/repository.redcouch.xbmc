#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Shev83
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,xbmc,xbmcaddon,HTMLParser,json,os,time,datetime,binascii

h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.redcouch'
print addon_id
selfAddon = xbmcaddon.Addon(id=addon_id)
print selfAddon
addonfolder = selfAddon.getAddonInfo('path')
print addonfolder
artfolder = addonfolder + '/resources/img/'
print artfolder
base_url = 'http://www.redcouch.me/'
fanart = os.path.join(addonfolder,'fanart.jpg')
print fanart
	
def CATEGORIES():
	addDir('FILMES','http://www.redcouch.me/filmes/',1,artfolder+'categorias.png')
    addDir('Categorias','-',2,artfolder+'categorias.png')

def categorias():
	html = abrir_url(base_url)
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(html)
	for url, cat in match:
		if cat.startswith('- Filmes'): continue
		addDir(cat,url,1,artfolder + 'categorias.png')

def listar_videos(url):
    codigo_fonte = abrir_url(url)
    url_title = re.compile('<a href="(.+?)">').findall(codigo_fonte)
	img = re.compile('<img src="(.+?)" alt=".+?" class="img-poster border-2 shadow-dark7" width=".+?" height=".+?"/>').findall(codigo_fonte)
    titulo = re.compile('<img src=".+?" alt="(.+?)" class="img-poster border-2 shadow-dark7" width=".+?" height=".+?"/>').findall(codigo_fonte)
	total = len(url_title)
	
	for i in range(0,total):
	    addDir(titulo,url_title,2,img)

########################################################################################################
#FUNCOES DIRECTORIAS                                                                                   #
########################################################################################################

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
#################################################################################
#FUNCOES REQUEST's HTTP                                                         #
#################################################################################

def check_if_image_exists(url):
	try:
		f = urllib2.urlopen(urllib2.Request(url))
		deadLinkFound = False
	except:
		deadLinkFound = True
	return deadLinkFound

def abrir_url(url, encoding='utf-8'):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
    return link

def json_get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    data = json.load(urllib2.urlopen(req))
    return data

def json_post(data,url):
	data = json.dumps(data)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()

def post_page(url,user,password):
    mydata=[('login_name',user),('login_password',password),('login','submit')]
    mydata=urllib.urlencode(mydata)
    req=urllib2.Request(url, mydata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page=urllib2.urlopen(req).read()
    return page

def post_page_free(url,mydata):
	mydata=urllib.urlencode(mydata)
	req=urllib2.Request(url, mydata)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	page=urllib2.urlopen(req).read()
	return page

def exists(url):
    try:
        r = urllib2.urlopen(url)
        return True
    except: return False	
	
###############################################################################################################
# MODOS                                                                                                       #
###############################################################################################################

if mode==None or url==None or len(url)<1:
    print ""
    CATEGORIES()
elif mode==1: listar_videos(url)
elif mode==2: categorias()

xbmcplugin.endOfDirectory(int(sys.argv[1]))