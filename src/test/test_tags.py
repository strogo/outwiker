# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.tagscommands import(parseTagsList,
                                       appendTag,
                                       removeTag,
                                       tagBranch,
                                       appendTagsList,
                                       removeTagsFromBranch,
                                       renameTag)

from .utils import removeDir


class TagsListTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, u"page 1", [u"Метка 1", u"Метка 2"])
        factory.create(self.wikiroot, u"Страница 2", [u"Метка 1", u"Метка 3"])
        factory.create(self.wikiroot[u"Страница 2"],
                       u"Страница 3",
                       [u"Метка 2"])
        factory.create(self.wikiroot[u"Страница 2/Страница 3"],
                       u"Страница 4",
                       [u"Метка 1"])
        factory.create(self.wikiroot[u"page 1"], u"page 5", [u"Метка 4"])

    def tearDown(self):
        removeDir(self.path)

    def test1(self):
        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags), 4)

        self.assertEqual(len(tags[u"Метка 1"]), 3)
        self.assertIn(self.wikiroot[u"page 1"], tags[u"Метка 1"])
        self.assertIn(self.wikiroot[u"Страница 2"], tags[u"Метка 1"])
        self.assertIn(self.wikiroot[u"Страница 2/Страница 3/Страница 4"],
                      tags[u"Метка 1"])

    def testParseTags(self):
        tagsString = u" метка 1 , Метка 2, метка 3,, , "

        tags = parseTagsList(tagsString)

        self.assertEqual(len(tags), 3)

        self.assertIn(u"метка 1", tags)
        self.assertIn(u"Метка 2", tags)
        self.assertIn(u"метка 3", tags)

    def testAppendTag(self):
        appendTag(self.wikiroot[u"Страница 2"], u"Метка 666")

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 3)
        self.assertIn(u"Метка 666".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 1".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 3".lower(), self.wikiroot[u"Страница 2"].tags)

    def testAppendTagsList(self):
        appendTagsList(self.wikiroot[u"Страница 2"],
                       [u"Метка 111", u"Метка 222", u"Метка 333"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 5)
        self.assertIn(u"Метка 111".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 222".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 333".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 1".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 3".lower(), self.wikiroot[u"Страница 2"].tags)

    def testCopyTags(self):
        self.assertEqual(len(self.wikiroot[u"page 1"].tags), 2)

        appendTag(self.wikiroot[u"page 1"], u"Метка 1")

        self.assertEqual(len(self.wikiroot[u"page 1"].tags), 2)

    def testTagBranch(self):
        tagBranch(self.wikiroot[u"Страница 2"], [u"Метка 111", u"Метка 222"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 4)
        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 3)
        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertIn(u"Метка 111".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 111".lower(),
                      self.wikiroot[u"Страница 2/Страница 3"].tags)
        self.assertIn(u"Метка 111".lower(),
                      self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2/Страница 3"].tags)
        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags)

    def testTagRoot(self):
        tagBranch(self.wikiroot, [u"Метка 111", u"Метка 222"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 4)
        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 3)
        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertIn(u"Метка 111".lower(), self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 111".lower(),
                      self.wikiroot[u"Страница 2/Страница 3"].tags)
        self.assertIn(u"Метка 111".lower(),
                      self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2"].tags)
        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2/Страница 3"].tags)
        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn(u"Метка 222".lower(), self.wikiroot[u"page 1"].tags)
        self.assertIn(u"Метка 222".lower(),
                      self.wikiroot[u"page 1/page 5"].tags)

    def testRemoveTag1(self):
        self.assertIn(u"Метка 3".lower(),
                      self.wikiroot[u"Страница 2"].tags)
        removeTag(self.wikiroot[u"Страница 2"], u"Метка 3")
        self.assertNotIn(u"Метка 3".lower(),
                         self.wikiroot[u"Страница 2"].tags)

    def testRemoveTag2(self):
        self.assertIn(u"Метка 3".lower(),
                      self.wikiroot[u"Страница 2"].tags)
        removeTag(self.wikiroot[u"Страница 2"], u"МеТкА 3")
        self.assertNotIn(u"Метка 3".lower(),
                         self.wikiroot[u"Страница 2"].tags)

    def testRemoveNotExists(self):
        self.assertNotIn(u"Метка 333".lower(),
                         self.wikiroot[u"Страница 2"].tags)
        removeTag(self.wikiroot[u"Страница 2"], u"Метка 333")
        self.assertNotIn(u"Метка 333".lower(),
                         self.wikiroot[u"Страница 2"].tags)

    def testAppendExists(self):
        appendTag(self.wikiroot[u"Страница 2"], u"Метка 1")
        self.assertIn(u"Метка 1".lower(),
                      self.wikiroot[u"Страница 2"].tags)

        removeTag(self.wikiroot[u"Страница 2"], u"Метка 1")
        self.assertNotIn(u"Метка 1".lower(),
                         self.wikiroot[u"Страница 2"].tags)

    def testRemoveTagsFromBranch1(self):
        removeTagsFromBranch(self.wikiroot[u"Страница 2"], [u"Метка 1"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 1)
        self.assertIn(u"метка 3", self.wikiroot[u"Страница 2"].tags)

        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 1)
        self.assertIn(u"метка 2", self.wikiroot[u"Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsFromRoot(self):
        removeTagsFromBranch(self.wikiroot, [u"МеТкА 1"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 1)
        self.assertIn(u"метка 3", self.wikiroot[u"Страница 2"].tags)

        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 1)
        self.assertIn(u"метка 2", self.wikiroot[u"Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsFromBranch2(self):
        removeTagsFromBranch(self.wikiroot[u"Страница 2"],
                             [u"МеТкА 1", u"Метка 1000"])

        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 1)
        self.assertIn(u"метка 3", self.wikiroot[u"Страница 2"].tags)

        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 1)
        self.assertIn(u"метка 2", self.wikiroot[u"Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsEmpty(self):
        removeTagsFromBranch(self.wikiroot, [])

        self.assertEqual(len(self.wikiroot[u"page 1"].tags), 2)
        self.assertEqual(len(self.wikiroot[u"page 1/page 5"].tags), 1)
        self.assertEqual(len(self.wikiroot[u"Страница 2"].tags), 2)
        self.assertEqual(len(self.wikiroot[u"Страница 2/Страница 3"].tags), 1)
        self.assertEqual(
            len(self.wikiroot[u"Страница 2/Страница 3/Страница 4"].tags), 1)

    def testRenameTag(self):
        renameTag(self.wikiroot, u"МеТкА 1", u"Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags), 4)

        self.assertEqual(len(tags[u"Метка 1"]), 0)
        self.assertEqual(len(tags[u"Черная метка"]), 3)

        self.assertIn(self.wikiroot[u"page 1"], tags[u"Черная метка"])
        self.assertIn(self.wikiroot[u"Страница 2"], tags[u"Черная метка"])
        self.assertIn(self.wikiroot[u"Страница 2/Страница 3/Страница 4"],
                      tags[u"Черная метка"])

    def testRenameTagBranch(self):
        renameTag(self.wikiroot[u"Страница 2"], u"МеТкА 1", u"Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags[u"Метка 1"]), 1)
        self.assertEqual(len(tags[u"Черная метка"]), 2)

        self.assertIn(self.wikiroot[u"page 1"], tags[u"Метка 1"])
        self.assertIn(self.wikiroot[u"Страница 2"], tags[u"Черная метка"])
        self.assertIn(self.wikiroot[u"Страница 2/Страница 3/Страница 4"],
                      tags[u"Черная метка"])

    def testRenameNotExists(self):
        renameTag(self.wikiroot, u"МеТкА 666", u"Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags[u"Метка 1"]), 3)
        self.assertEqual(len(tags[u"Метка 666"]), 0)

        self.assertIn(self.wikiroot[u"page 1"], tags[u"Метка 1"])
        self.assertIn(self.wikiroot[u"Страница 2"], tags[u"Метка 1"])
        self.assertIn(self.wikiroot[u"Страница 2/Страница 3/Страница 4"],
                      tags[u"Метка 1"])
