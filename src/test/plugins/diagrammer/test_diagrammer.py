# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class DiagrammerTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)

        self.thumbDir = os.path.join (u"__attach", u"__thumb")
        self.thumbFullPath = os.path.join (self.testPage.path, self.thumbDir)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        removeDir (self.path)
        self.loader.clear()


    def testEmpty (self):
        text = u"(:diagram:)(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def test_simple (self):
        text = u"(:diagram:)Абырвалг -> Блаблабла(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def test_double (self):
        text = u"""(:diagram:)Абырвалг -> Блаблабла(:diagramend:)
(:diagram:)Абыр -> валг -> Блаблабла(:diagramend:)"""

        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 2)


    def test_copy (self):
        text = u"""(:diagram:)Абырвалг -> Блаблабла(:diagramend:)
(:diagram:)Абырвалг -> Блаблабла(:diagramend:)"""

        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def testError (self):
        text = u"(:diagram:)a - b(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertNotIn (validResult, result)

        # Признак ошибки
        self.assertIn (u"<b>", result)

        # Папка для превьюшек все равно создается
        self.assertTrue (os.path.exists (self.thumbFullPath))


    def testShapes_01 (self):
        template = u'a{n}[shape = {shape}]'
        shapes = [
            "actor",
            "beginpoint",
            "box",
            "circle",
            "cloud",
            "diamond",
            "dots",
            "ellipse",
            "endpoint",
            "mail",
            "minidiamond",
            "none",
            "note",
            "roundedbox",
            "square",
            "textbox",
            "flowchart.database",
            "flowchart.input",
            "flowchart.loopin",
            "flowchart.loopout",
            "flowchart.terminator",
        ]

        lines = [u"(:diagram:)"]

        for n, shape in zip (range (len (shapes)), shapes):
            lines.append (template.format (n = n, shape = shape))

        lines .append (u"(:diagramend:)")
        text = u"\n".join (lines)

        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)
        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)


    def testShapes_02 (self):
        shapes = sorted ([
            "actor",
            "beginpoint",
            "box",
            "circle",
            "cloud",
            "diamond",
            "dots",
            "ellipse",
            "endpoint",
            "mail",
            "minidiamond",
            "none",
            "note",
            "roundedbox",
            "square",
            "textbox",
            "flowchart.database",
            "flowchart.input",
            "flowchart.loopin",
            "flowchart.loopout",
            "flowchart.terminator",
        ])

        from diagrammer.diagramrender import DiagramRender
        diagramShapers = DiagramRender.shapes

        self.assertEqual (shapes, diagramShapers)
