#MandatoryImports
from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime as dt
import threading 
import sys
import AWSIoTPythonSDK.MQTTLib as awsmqtt
import json

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import  MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton

from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty

import random