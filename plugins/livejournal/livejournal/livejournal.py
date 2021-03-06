# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet


__version__ = u"1.3.5"


if getCurrentVersion() < Version (1, 7, 0, 670, status=StatusSet.DEV):
    print ("Livejournal plugin. OutWiker version requirement: 1.7.0.670")
else:
    from .controller import Controller
    from .i18n import set_

    class PluginLivejournal (Plugin):
        """
        Плагин, добавляющий обработку команды spoiler в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self._controller = Controller(application)


        def initialize(self):
            """
            Инициализация плагина
            """
            self._initlocale("livejournal")
            self._controller.initialize()


        def _initlocale (self, domain):
            """
            Загрузить перевод
            """
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_ (_)


        @property
        def name (self):
            return u"Livejournal"


        @property
        def description (self):
            return _(u"""Add commands (:ljuser:) and (:ljcomm:) in wiki parser.

                     <B>Usage:</B>
                     (:ljuser username:)
                     (:ljcomm communityname:)
                     """)


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/LivejournalPluginEn")


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._controller.destroy()
