import gettext
import locale
import os


def setup_translation():
    localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../messages')
    lang = locale.getlocale()[0]

    if lang:
        lang = lang.split('_')[0]

    translation = gettext.translation('messages', localedir, languages=[lang], fallback=True)
    translation.install()
    return translation.gettext, translation.ngettext


_, ngettext = setup_translation()
