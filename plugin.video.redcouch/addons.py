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

import urllib
import re
import json
import os

import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
import HTMLParser

h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.redcouch'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
base_url = 'http://www.redcouch.me/'
fanart = os.path.join(addonfolder, 'fanart.jpg')


def CATEGORIES():
    addDir('FILMES', 'http://www.redcouch.me/filmes/', 1, artfolder + 'categorias.png')
    addDir('SÉRIES', 'http://www.redcouch.me/series/', 1, artfolder + 'categorias.png')
    addDir('ANIMES', 'http://www.redcouch.me/animes/', 1, artfolder + 'categorias.png')
    addDir('Categorias', '-', 2, artfolder + 'categorias.png')


def categorias():
    html = abrir_url(base_url)
    match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(html)
    for url, cat in match:
        if not cat.startswith('<span>'):
            addDir(cat, 'http://www.redcouch.me' + url, 1, artfolder + 'categorias.png')


def listar_videos(url):
    codigo_fonte = abrir_url(url)
    match = re.compile('<div class="short-film">\n<a href="(.+?)">\n<div class="border-2">\n<img src="(.+?)" '
                       'alt="(.+?)" class="img-poster border-2 shadow-dark7" width="151" height="215"/>\n</div> \n'
                       '<div class="clr"></div>\n</a>\n</div>').findall(codigo_fonte)
    for url, img, titulo in match:
        addDir(titulo, url, 4, img)
    try:
        next = re.compile('<a href="(.+?)"><span class="pnext">.+?</span></a>').findall(codigo_fonte)[0]
        addDir('[B][COLOR white]Próxima página >>[/COLOR][/B]', next, 1, artfolder + 'next.png')
    except:
        pass

def encontrar_fontes(url):
    codigo_fonte = abrir_url(url)
    codigo_fonte_v = abrir_url(url)
    match2 = re.compile('<iframe src="(.+?)"').findall(codigo_fonte_v)
    for url_v in match2:
        print url_v
        addDir('Teste', url_v, 4, '')
        # return urlfound

def player(name, url, iconimage):
    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('RedCouch', 'A resolver link', 'Por favor aguarde...')
    mensagemprogresso.update(33)
    mensagemprogresso.update(100)
    mensagemprogresso.close()
    link = open_url(url)
    print link
    if 'openload' in link:
        olurl=re.compile('<iframe src="(.+?)"').findall(link)[0]
        print olurl
        link = open_url(olurl)
        print link
        stream_url = re.compile('<source type="video/mp4" src="(.+?)">').findall(link)[0]
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    try:
        xbmc.Player ().play(stream_url, liz, False) 
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok(" Erro:", " Impossível abrir vídeo! ")

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link = link.replace('\n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        response.close()
        return link

########################################################################################################
# FUNCOES DIRECTORIAS                                                                                   #
########################################################################################################


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
    liz.setInfo( type="video", infoLabels={ "title": name} )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDirPlayer(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
    liz.setInfo(type="Video", infoLabels={"Title": name,
                                          "OriginalTitle": name
                                          })
    cm = []
    cm.append(('Download', 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url), name)))
    liz.addContextMenuItems(cm, replaceItems=True)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addLink(name, url):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


#################################################################################
# FUNCOES REQUEST's HTTP                                                         #
#################################################################################
def url_solver(urlfinal):
    import urlresolver
    sources = []
    hosted_media = urlresolver.HostedMediaFile(url=urlfinal)
    sources.append(hosted_media)
    source = urlresolver.choose_source(sources)
    if source:
        stream_url = source.resolve()
        stream_source = source.get_host()
    else:
        stream_url = '-'
        stream_source = '-'
    return stream_url


def check_if_image_exists(url):
    try:
        f = urllib.request.urlopen(urllib2.Request(url))
        deadLinkFound = False
    except:
        deadLinkFound = True
    return deadLinkFound


def abrir_url(url, encoding='utf-8'):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
    return link


def json_get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    data = json.load(urllib2.urlopen(req))
    return data


def json_post(data, url):
    data = json.dumps(data)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()


def post_page(url, user, password):
    mydata = [('login_name', user), ('login_password', password), ('login', 'submit')]
    mydata = urllib.urlencode(mydata)
    req = urllib2.Request(url, mydata)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page = urllib2.urlopen(req).read()
    return page


def post_page_free(url, mydata):
    mydata = urllib.urlencode(mydata)
    req = urllib2.Request(url, mydata)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page = urllib2.urlopen(req).read()
    return page


def exists(url):
    try:
        r = urllib2.urlopen(url)
        return True
    except:
        return False


############################################################################################################
# NAVEGAÇÃO												   #
############################################################################################################
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'): params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
# MODOS                                                                                                       #
###############################################################################################################

if mode == None or url == None or len(url) < 1:
    CATEGORIES()
elif mode == 1:
    listar_videos(url)
elif mode == 2:
    categorias()
elif mode == 3:
    encontrar_fontes(url)
elif mode == 4:
    player(name, url, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
