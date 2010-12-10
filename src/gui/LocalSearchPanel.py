# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon May 31 21:35:59 2010

import codecs
import os.path

import wx
import core.system

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class LocalSearchPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self.imagesDir = core.system.getImagesDir()

		# begin wxGlade: LocalSearchPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.phraseTextCtrl = wx.TextCtrl(self, -1, "")
		self.nextSearchBtn = wx.BitmapButton(self, -1, wx.Bitmap("images/arrow_down.png", wx.BITMAP_TYPE_ANY))
		self.prevSearchBtn = wx.BitmapButton(self, -1, wx.Bitmap("images/arrow_up.png", wx.BITMAP_TYPE_ANY))
		self.resultLabel = wx.StaticText(self, -1, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_TEXT_ENTER, self.onNextSearch, self.phraseTextCtrl)
		self.Bind(wx.EVT_TEXT, self.onTextEnter, self.phraseTextCtrl)
		self.Bind(wx.EVT_BUTTON, self.onNextSearch, self.nextSearchBtn)
		self.Bind(wx.EVT_BUTTON, self.onPrevSearch, self.prevSearchBtn)
		# end wxGlade

		self.nextSearchBtn.SetToolTipString (_(u"Find Next") )
		self.prevSearchBtn.SetToolTipString (_(u"Find Previous") )


	def __set_properties(self):
		# begin wxGlade: LocalSearchPanel.__set_properties
		self.phraseTextCtrl.SetMinSize((250, -1))
		self.nextSearchBtn.SetSize(self.nextSearchBtn.GetBestSize())
		self.prevSearchBtn.SetSize(self.prevSearchBtn.GetBestSize())
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: LocalSearchPanel.__do_layout
		mainSizer = wx.FlexGridSizer(1, 4, 0, 0)
		mainSizer.Add(self.phraseTextCtrl, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		mainSizer.Add(self.nextSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		mainSizer.Add(self.prevSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		mainSizer.Add(self.resultLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		mainSizer.AddGrowableCol(3)
		# end wxGlade
	

	def onNextSearch(self, event): # wxGlade: LocalSearchPanel.<event_handler>
		self.nextSearch()

	
	def onPrevSearch(self, event): # wxGlade: LocalSearchPanel.<event_handler>
		self.prevSearch()

	
	def onTextEnter(self, event): # wxGlade: LocalSearchPanel.<event_handler>
		self.enterSearchPhrase()

	
	def nextSearch (self):
		"""
		Искать следующее вхождение фразы
		"""
		pass


	def prevSearch (self):
		"""
		Искать предыдущее вхождение фразы
		"""
		pass
	

	def startSearch (self):
		"""
		Начать поиск
		"""
		pass
	

	def enterSearchPhrase (self):
		pass
	

# end of class LocalSearchPanel


class SearchResult (object):
	"""
	Результат поиска по странице
	"""
	def __init__ (self, position, phrase):
		"""
		position -- начало найденного текста
		"""
		self.position = position
		self.phrase = phrase


class LocalSearcher (object):
	def __init__ (self, text, phrase):
		self.text = text.lower()
		self.phrase = phrase.lower()
		self.result = self._findAll ()


	def _findAll (self):
		result = []
		index = self.text.find (self.phrase)

		while index != -1:
			result.append (SearchResult (index, self.phrase) )
			index = self.text.find (self.phrase, index + len (self.phrase))
			#print index

		return result

