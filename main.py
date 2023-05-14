from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from plyer import filechooser
from kivy.clock import Clock
import pandas as pd
import math
from matplotlib import pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

Window.size=(1000,600)

class Image_btn(ButtonBehavior, Image):
    pass

class Interface(BoxLayout):
    def binder(self, checkbox, value):
        if value:
            print(self.obj_dict[checkbox], " added")
        else:
            print(self.obj_dict[checkbox], " removed")

    
    def uploader(self, dt):
        self.obj_dict=dict()
        self.column_dict = dict()
        self.file_adress= dict()
        
        self.files = filechooser.open_file(title="Choose excel files", filters =[("*.xlsx")], multiple=True)
        for file in self.files:
            file_name = file.split("\\")[-1]
            self.file_adress[file_name] = file
            box=BoxLayout(size_hint_y= None, height=50, padding=[30, 0, 0, 0])
            checkbox= CheckBox(size_hint_x = .25, color=[0, 0, 0, 2])
            checkbox.bind(active=self.binder)
            label = Label(text=f"[color=#3f51b5]{file_name}[/color]", markup=True )
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.file_placeholder.add_widget(box)
            self.obj_dict[checkbox] = file_name

        columns = pd.read_excel(self.files[0]).columns.values.tolist()
        for column in columns:
            box=BoxLayout(size_hint_y= None, height=50, padding=[30, 0, 0, 0])
            checkbox= CheckBox(size_hint_x = .25, color=[0, 0, 0, 2])            
            label = Label(text=f"[color=#3f51b5]{column}[/color]", markup=True )
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.property_placeholder.add_widget(box)
            self.column_dict[checkbox] = column
        

        self.ids.upload_btn.source="Drag.png"

    def update(self):
        flatten_axis = list()
        #Check for old plots
        children = self.ids.graph_placeholder.children
        if children:
            self.ids.graph_placeholder.remove_widget(children[0])

        #Total number of charts
        files_len=len(self.files)
        if files_len == 1:
            fig,axis = plt.subplots(1,1)
            flatten_axis.append(axis)
        elif files_len == 2:
            fig, axis = plt.subplots(2, 1)
            flatten_axis = axis.flatten().tolist()
        else:
            row_col = math.ceil(files_len/2)
            fig, axis = plt.subplots(row_col, row_col)
            flatten_axis = axis.flatten().tolist()

        #Keys
        files_checkbox=self.obj_dict.keys()
        properties_checkbox = self.column_dict.keys()
        plt.gcf().autofmt_xdate()
        for index, file_checkbox in enumerate(files_checkbox):
            y_axis = list()
            if file_checkbox.active:
                file_name = self.obj_dict[file_checkbox]
                file_address = self.file_adress[file_name]
                content = pd.read_excel(file_address)
                print(content)
                for property_checkbox in properties_checkbox:
                    if property_checkbox.active:
                        if self.column_dict[property_checkbox] == "Date":
                            x_axis = content[self.column_dict[property_checkbox]]
                        else:
                            y_axis.append(content[self.column_dict[property_checkbox]])
                for y in y_axis:
                    flatten_axis[index].plot(x_axis.to_numpy(), y.to_numpy())
        
        self.ids.graph_placeholder.add_widget(FigureCanvasKivyAgg(plt.gcf()))

                        

    def upload_menu(self):
        self.ids.upload_btn.source="Drop.png"
        Clock.schedule_once(self.uploader)

    def switching(self):
        self.ids.sm.current = "visualizer_window"

    def saving(self):
        dir = filechooser.choose_dir(title="Please Select A Location")
        plt.savefig(dir[0]+"\\Figure.png")

        

class VisualizerApp(App):
    pass

VisualizerApp().run()