# -*- coding: utf-8 -*-
# Copyright stuff
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import wordpresslib
 
class PublishToWordpressApplet(plasmascript.Applet):
  def __init__(self,parent,args=None):
    plasmascript.Applet.__init__(self,parent)
 
  def init(self):
    self.setHasConfigurationInterface(True)
    self.setAspectRatioMode(Plasma.Square)
    self.theme = Plasma.Svg(self)
    self.theme.setImagePath("widgets/background")
    self.setBackgroundHints(Plasma.Applet.DefaultBackground)
    self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
    self.conf = self.config()
    if self.conf.readEntry("username","") == "":
      self.setConfigurationRequired(True,"Configure your wordpress blog's adress.")
    

    titleLabel = Plasma.Label(self.applet)
    titleLabel.setText("Title:")
    self.layout.addItem(titleLabel)    
    
    self.titleLineEdit = Plasma.LineEdit(self.applet)
    self.layout.addItem(self.titleLineEdit)
    
    textLabel = Plasma.Label(self.applet)
    textLabel.setText("Text:")
    self.layout.addItem(textLabel)

    
    self.textTextEdit = Plasma.TextEdit(self.applet)
    self.textTextEdit.setText("Write here")
    self.layout.addItem(self.textTextEdit)
    self.connect(self.textTextEdit, SIGNAL("clicked()"),self.clearTextEdit)
    
    submitPushButton = Plasma.PushButton(self.applet)
    submitPushButton.setText("Publish")
    self.layout.addItem(submitPushButton)
    self.connect(submitPushButton, SIGNAL("clicked()"),self.publish)
    
    
    self.setLayout(self.layout)
    self.resize(400,400)
    
  def configChanged(self):
    #FIXME Confirm that all are set and that connection works.
    self.setConfigurationRequired(False,"")
    return

  def publish(self):
    publishTitle = unicode(self.titleLineEdit.text())
    publishText = unicode(self.textTextEdit.text())
    wordpress = unicode(self.conf.readEntry("wordpressurl",""))
    user = unicode(self.conf.readEntry("username",""))
    password = unicode(self.conf.readEntry("password",""))
    
    # prepare client object
    wp = wordpresslib.WordPressClient(wordpress, user, password)
    wp.selectBlog(0)
    
    post = wordpresslib.WordPressPost()
    post.title = publishTitle
    post.description = publishText
    
    idNewPost = wp.newPost(post, True)
    
    return;
    
  def clearTextEdit(self):
    if self.textTextEdit.text() == "Write here":
      textTextEdit.setText("")

def CreateApplet(parent):
    return PublishToWordpressApplet(parent)