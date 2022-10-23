#MandatoryImports
from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime as dt
from threading import Thread
import sys
import AWSIoTPythonSDK.MQTTLib as awsmqtt
import json

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import  MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons

from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty