# -*- coding: utf-8 -*-
"""Pibooth plugin for upload pictures to ConAdmin application."""
import pluggy
import pibooth
from pbBadges import pbBadges
from pibooth.utils import LOGGER
import config

__version__ = "1.0.2"
hookspec = pluggy.HookspecMarker('pibooth')

# --- Pibooth state-independent hooks ------------------------------------------
def unescape(text):
    if (len(text)>1):
        if (text[0] == '"' and text[-1] == '"'):
            text = text[1:][:-1]
    return text

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Actions performed after loading of the configuration file or when the
    plugin is enabled for the first time. The ``cfg`` object is an instance
    of :py:class:`ConfigParser` class.

    :param cfg: application configuration
    """
    """Declare the new configuration options"""
    cfg.add_option(config.SECTION, config.BTMIX_FILE , config.BTMIX_FILE_DEFAULT ,
                   config.BTMIX_FILE,
                   config.BTMIX_FILE , config.BTMIX_FILE_DEFAULT )
    cfg.add_option(config.SECTION, config.BADGES_IMG_FOLDER , config.BADGES_IMG_FOLDER_DEFAULT ,
                   config.BADGES_IMG_FOLDER,
                   config.BADGES_IMG_FOLDER , config.BADGES_IMG_FOLDER_DEFAULT )
    cfg.add_option(config.SECTION, config.BADGES_DEFAULT_IMG , config.BADGES_DEFAULT_IMG_FILE ,
                   config.BADGES_DEFAULT_IMG,
                   config.BADGES_DEFAULT_IMG , config.BADGES_DEFAULT_IMG_FILE )
    
    LOGGER.debug("pibooth_rfid - Configure options added" )
    

@pibooth.hookimpl
def pibooth_startup(cfg, app):
    """Actions performed at the startup of pibooth or when the plugin is enabled
    for the first time.

    :param cfg: application configuration
    :param app: application instance
    """
    LOGGER.info("pibooth_rfid - Hello from pibooth_rfid plugin")
    app.pbBadges = pbBadges(unescape(cfg.get(config.SECTION, config.BTMIX_FILE )),
                            unescape(cfg.get(config.SECTION, config.BADGES_IMG_FOLDER )),
                            unescape(cfg.get(config.SECTION, config.BADGES_DEFAULT_IMG ))
                            )



    

@pibooth.hookimpl
def state_finish_enter(cfg, app, win):
    """Actions performed when application enter in Finish state.
    """

@pibooth.hookimpl
def state_wait_enter(cfg, app, win):
    """Actions performed when application enter in Choose state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    """
    app.pbImgMetaData = {}
    app.pbBadges.startAdding(win)

@pibooth.hookimpl
def state_wait_do(cfg, app, win, events):
    """Actions performed when application is in Wait state.
    This hook is called in a loop until the application can switch
    to the next state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    :param events: pygame events generated since last call
    """
    
        

@pibooth.hookimpl
def state_wait_validate(cfg, app, win, events):
    """Return the next state name if application can switch to it
    else return None.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    :param events: pygame events generated since last call
    """
    showLogo = True
    if hasattr(app,"plugin_gallery"):
            if app.plugin_gallery["active"]:
                showLogo = False
    
    if app.pbBadges.do(showLogo):
        return "choose" #jump to choose state


@pibooth.hookimpl
def state_choose_enter(cfg, app, win):
    """Actions performed when application enter in Choose state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    """
    app.pbBadges.redraw()
    # app.pbImgMetaData = {}
    # app.pbBadges.startAdding(win)
 

@pibooth.hookimpl
def state_choose_do(cfg, app, win, events):
    """Actions performed when application is in Choose state.
    This hook is called in a loop until the application can switch
    to the next state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    :param events: pygame events generated since last call
    """
        

    app.pbBadges.do()

@pibooth.hookimpl
def state_choose_exit(cfg, app, win):
    """Actions performed when application exit Choose state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    """
    app.pbBadges.exitAdding()

