# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from ..i18n import get_


class InsertNodeDialog (TestedDialog):
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertNodeDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                                                 title=_(u"Insert Node"))

        self.__createGui()
        self.SetSize ((500, 350))

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)


    @property
    def name (self):
        return self._name.GetValue()


    @name.setter
    def name (self, value):
        return self._name.SetValue (value)


    def __onOk (self, event):
        if len (self.name.strip()) == 0:
            MessageBox (_(u"Node name can't be empty"),
                        u"Node name is empty",
                        wx.ICON_ERROR | wx.OK)
            return

        event.Skip()


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        self.__createNameRow (mainSizer)
        self.__createOkCancelButtons (mainSizer)
        self.SetSizer (mainSizer)
        self._name.SetFocus()


    def __createNameRow (self, mainSizer):
        """
        Создать элементы для ввода имени узла
        """
        titleLabel = wx.StaticText (self, label = _(u"Node name"))
        self._name = wx.TextCtrl (self)
        self._name.SetMinSize ((250, -1))

        mainSizer.Add (titleLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 2
                       )

        mainSizer.Add (self._name,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2
                       )


    def __createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (okCancel,
                       flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                       border=4
                       )



class InsertNodeController (object):
    def __init__ (self, dialog):
        """
        dialog - экземпляр класса InsertNodeDialog
        """
        self._dialog = dialog


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает строку для создания нового узла в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        name = self._dialog.name
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return name
        else:
            return u"{}[{}];".format (name, params)


    def _getParamString (self, dialog):
        result = u""

        return result