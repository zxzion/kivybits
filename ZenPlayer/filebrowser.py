"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from os.path import exists


Builder.load_string('''
<ZenFileBrowser>:
    filechooser: filechooser
    label_sel: label_sel

    BoxLayout:
        orientation: 'vertical'
        #FileChooserIconView:
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.1
            Label:
                text: "Select the file or folder"
                canvas:
                    Color:
                        rgba: 0.25, 0.25, 0.75, 0.5
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                id: label_sel
                text: "Selection - None"
        FileChooserListView:
            id: filechooser
            size_hint_y: 0.8
            dirselect: True
            on_selection: label_sel.text = "Selection - " + str(self.selection)
            #TODO: Remove
            #path: '/media/Zen320/Zen/Music'
        BoxLayout:
            orientation: 'horizontal'
            padding: 10, 10, 10, 10
            size_hint_y: 0.1
            Button:
                text: 'Back'
                on_release: root.sm.current = "main"
            Button:
                text: "Add and replace"
                on_release: root.add_replace()
            Button:
                text: "Add"
                on_release: root.add_files()
''')


class ZenFileBrowser(Screen):
    """
    Displays a file browsing screen for ZenPlayer
    """
    filechooser = ObjectProperty()

    def __init__(self, sm, playlist, **kwargs):
        self.sm = sm
        self.playlist = playlist
        self.initailized = False
        super(ZenFileBrowser, self).__init__(**kwargs)

    def add_files(self):
        """ Add any selected files/folders to the playlist"""
        for filefolder in self.filechooser.selection:
            self.playlist.add_files(filefolder)

    def add_replace(self):
        """ Add amy selected files/folders to the playlist removing any that
        already exist """
        self.playlist.clear_files()
        self.add_files()

    def on_enter(self):
        """ The filebrowser screen is being opened """
        if not self.initailized:
            self.initailized = True
            store = JsonStore("zenplayer.json")
            if store.exists("filebrowser"):
                if "path" in store.get("filebrowser").keys():
                    file_path = store.get("filebrowser")["path"]
                    if exists(file_path):
                        self.filechooser.path = file_path

    def on_leave(self):
        """ The filebrowser screen is being closed """
        if len(self.filechooser.selection) > 0:
            store = JsonStore("zenplayer.json")
            store.put("filebrowser", path=self.filechooser.selection[0])
