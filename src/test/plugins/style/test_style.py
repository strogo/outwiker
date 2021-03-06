# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeDir


class StylePluginTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "866"

        self.__createWiki()

        dirlist = [u"../plugins/style"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        removeDir (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testStyleContentParse (self):
        text = u"""Бла-бла-бла
(:style:)
body {font-size: 33px}
(:styleend:)
бла-бла-бла
"""

        validResult = u"""Бла-бла-бла

бла-бла-бла
"""
        styleresult = u"<STYLE>body {font-size: 33px}</STYLE>"

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)
        self.assertTrue (styleresult in self.parser.head)


    def testFullHtml (self):
        text = u"""Бла-бла-бла
(:style:)
body {font-size: 33px}
(:styleend:)
бла-бла-бла
"""
        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        validStyle = u"<STYLE>body {font-size: 33px}</STYLE>"

        self.assertTrue (validStyle in result, result)


    def testFullHtml2 (self):
        text = u"""Бла-бла-бла
(:style:)
body {font-size: 33px}
(:styleend:)

sdfsdf sdf

(:style:)
body {font-size: 10px}
(:styleend:)

бла-бла-бла
"""
        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        validStyle1 = u"<STYLE>body {font-size: 33px}</STYLE>"
        validStyle2 = u"<STYLE>body {font-size: 10px}</STYLE>"

        self.assertTrue (validStyle1 in result, result)
        self.assertTrue (validStyle2 in result, result)
