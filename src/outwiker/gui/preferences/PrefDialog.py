# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Oct 23 11:20:17 2010

import wx

import GeneralPanel
import EditorPanel
import HtmlRenderPanel
import TextPrintPanel
from pluginspanel import PluginsPanel

from outwiker.core.exceptions import PreferencesException
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.application import Application

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class PrefDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: PrefDialog.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
		wx.Dialog.__init__(self, *args, **kwds)
		self.treeBook = wx.Treebook(self, -1)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.__createPages()
		self.treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGING, self.onPageChanging)
		self.treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGED, self.onPageChanged)

		Application.onPreferencesDialogCreate (self)


	def __set_properties(self):
		# begin wxGlade: PrefDialog.__set_properties
		self.SetTitle(_("Preferences"))
		self.SetSize((800, 550))
		self.treeBook.SetMinSize((300, 400))
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: PrefDialog.__do_layout
		main_sizer = wx.FlexGridSizer(2, 1, 0, 0)
		main_sizer.Add(self.treeBook, 1, wx.ALL|wx.EXPAND, 4)
		self.SetSizer(main_sizer)
		main_sizer.AddGrowableRow(0)
		main_sizer.AddGrowableCol(0)
		self.Layout()
		# end wxGlade
		
		self._createOkCancelButtons(main_sizer)
		self.Layout()
	

	def __createPages (self):
		"""
		Создать страницы окна настроек
		"""
		self.generalPage = GeneralPanel.GeneralPanel (self.treeBook)
		self.editorPage = EditorPanel.EditorPanel (self.treeBook)
		self.htmlRenderPage = HtmlRenderPanel.HtmlRenderPanel (self.treeBook)
		self.textPrintPage = TextPrintPanel.TextPrintPanel (self.treeBook)
		self.pluginsPage = PluginsPanel (self.treeBook)

		self.treeBook.AddPage (self.generalPage, _(u"Interface"))
		self.treeBook.AddSubPage (self.generalPage, _(u"General"))
		self.treeBook.AddSubPage (self.editorPage, _(u"Editor"))
		self.treeBook.AddSubPage (self.htmlRenderPage, _(u"Preview"))
		self.treeBook.AddSubPage (self.textPrintPage, _(u"Text Printout"))
		self.treeBook.AddPage (self.pluginsPage, _(u"Plugins") )

		self._createPagesForPages()

		self.treeBook.ExpandNode (0)
		self.treeBook.SetSelection (0)

		self.generalPage.minimizeCheckBox.SetFocus()
	

	def _createPagesForPages (self):
		"""
		Создать страницы настроек для типов страниц
		"""
		# Индекс последней добавленной страницы
		pageindex = 5
		for factory in FactorySelector.factories:
			pages = factory.getPrefPanels(self.treeBook)

			if len (pages) > 0:
				pageindex += 1

				# Номер страницы, которую надо будет развернуть
				expandindex = pageindex

				self.treeBook.AddPage (pages[0][1], factory.title)

				for page in pages:
					pageindex += 1
					self.treeBook.AddSubPage (page[1], page[0])

				self.treeBook.ExpandNode (expandindex)

	

	def _createOkCancelButtons (self, sizer):
		"""
		Создать кнопки Ok / Cancel
		"""
		buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
		sizer.AddSpacer(0)
		sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 4)

		self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)
		self.Bind (wx.EVT_BUTTON, self.__onCancel, id=wx.ID_CANCEL)
		
		self.Layout()
	

	def __onOk (self, event):
		try:
			self.__saveCurrentPage()
		except PreferencesException:
			pass

		Application.onPreferencesDialogClose(self)
		self.EndModal (wx.ID_OK)


	def __onCancel (self, event):
		Application.onPreferencesDialogClose(self)
		self.EndModal(wx.ID_CANCEL)
	

	def __saveCurrentPage (self):
		selectedPage = self.treeBook.GetCurrentPage()

		if selectedPage == None:
			return

		# У страницы должен быть метод Save, который сохраняет настройки 
		# или бросает исключение outwiker.core.exceptions.PreferencesException
		selectedPage.Save()


	def onPageChanging (self, event):
		try:
			self.__saveCurrentPage()
		except PreferencesException:
			event.Veto()


	def onPageChanged (self, event):
		pageIndex = event.GetSelection()

		if pageIndex == wx.NOT_FOUND:
			return

		selectedPage = self.treeBook.GetPage (pageIndex)

		if selectedPage == None:
			return

		selectedPage.LoadState()
		selectedPage.SetFocus()


# end of class PrefDialog


