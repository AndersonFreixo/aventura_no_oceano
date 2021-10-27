import pygame
from time import sleep

BUTTON_COLOR = 100, 180, 255        #Light blue
OVER_BUTTON_COLOR =  0, 130, 255    #A darker blue
TXT_COLOR = 255,255,255             #White

TXT_SIZE = 25
TXT_FONT = None
TXT_NAME = None

from pygame.locals import *

class Widget:
    def __init__(self):
        self.type = None                #'button' or 'text box'
        self.normal_surface = None
        self.cursor_over_surface = None
        self.focus = False              #For text boxes
        self.is_cursor_over = False
        self.text = ""                  #For text boxes
        self.position = None
        self.max_text = 0
class MiniGui:
    def __init__(self):
        #Widgets implemented so far: button, text
        self.widgets = dict() 
        self.active = dict()
        self.txt_font = pygame.font.Font(TXT_NAME, TXT_SIZE)
        self.active_textboxes = dict()

    def is_cursor_over_widget(self, name):
        return Rect((self.active[name].position), self.widgets[name].normal_surface.get_size()).collidepoint(pygame.mouse.get_pos())
    def set_focus(self, name):
        """Turn off the focus of all widgets, then turn on the focus of the especified widget"""
        for wid in self.active.values():
            wid.focus = False
        if name in self.active.keys():
            self.active[name].focus = True
    
    def process(self, game_events):

        events = []
        #Detect if cursor moved onto a button
        for name in self.active.keys():
            if self.is_cursor_over_widget(name):
                if self.active[name].type == "button":
                    if self.active[name].is_cursor_over == False:
                        self.active[name].is_cursor_over = True
                        events.append(("cursor-over", name))
            else:
                self.active[name].is_cursor_over = False

        #Check for clicks and keystrokes
        for event in game_events:
            if event.type == QUIT:
                events.append(("quit", None))

            #Clicks may fire a button or put focus on a text box
            if event.type == MOUSEBUTTONDOWN:
                clicked = self.what_is_clicked()
                if clicked:
                    #If the player clicked on a button, add to game_events
                    if self.active[clicked].type == "button":
                        events.append(("clicked", clicked))
                    #If the player clicked on a text box, set it's focus to true
                    elif self.active[clicked].type == "textbox":
                        self.active[clicked].focus = True            
                
                #If the player clicked outside of any widget
                #then any possible text box with focus loses its focus
                else:
                    for widget in self.active.values():
                        widget.focus = False
            #On keypress check if there's an active textbox with focus
            #and add character keys to its text attribute. 
            if event.type == KEYDOWN:
                active_textbox = None
                
                for widget in self.active.values():
                    if widget.type == "textbox" and widget.focus:
                        active_textbox = widget
                        break
                if active_textbox:
                    if event.key >= ord('a') and event.key <= ord('z'):
                        if active_textbox.max_text > len(active_textbox.text):
                            active_textbox.text += chr(event.key)
                    if event.key == pygame.K_BACKSPACE:
                        active_textbox.text = active_textbox.text[:-1]
                    if event.key == pygame.K_RETURN:
                        events.append(("submit", active_textbox.text))
        return events
    def render(self, surface):
        """This method renders all active buttons."""

        for widget in self.active.values():
            
            if widget.type == "button":
                if widget.is_cursor_over:
                    
                    surface.blit(widget.cursor_over_surface, widget.position)
                else:
                    surface.blit(widget.normal_surface, widget.position)
            if widget.type == "textbox":
                    surface.blit(widget.normal_surface, widget.position)
                    text_surface = self.get_text(widget.text, color = (0,0,0))
                    surface.blit(text_surface, widget.position)

    def remove_widget(self, name):
        self.active.pop(name)
        
    def what_is_clicked(self):

        for name, widget in self.active.items():
            if Rect((widget.position, self.active[name].normal_surface.get_size())).collidepoint(pygame.mouse.get_pos()):
                return name
    def create_textbox(self, name, size, max_text = 10):
        textbox = pygame.Surface((size, 30))
        textbox.fill((255, 255, 255))
        widget = Widget()
        widget.type = "textbox"
        widget.max_text = max_text
        widget.normal_surface = widget.cursor_over_surface = textbox
        self.widgets[name] = widget

    def create_button(self, name, text_str, size):

        """This method is used to create a button generating two surfaces to be used depending if the mouse is
            over the surface or not"""
        button = pygame.Surface(size)
        button_over = pygame.Surface(size)

        button.fill(BUTTON_COLOR)
        button_over.fill(OVER_BUTTON_COLOR)

        text = self.get_text(text_str, TXT_COLOR)
        text_size = text.get_size()

        button.blit(text, ((size[0]-text_size[0])/2, (size[1]-text_size[1])/2))
        button_over.blit(text, ((size[0]-text_size[0])/2, (size[1]-text_size[1])/2))
        widget = Widget()
        widget.type = "button"
        widget.normal_surface = button
        widget.cursor_over_surface = button_over

        self.widgets[name] = widget

    def put_widget(self, name, position):
        if self.widgets[name].type == "textbox":
            self.widgets[name].text = ""
        self.active[name] =  self.widgets[name]
        self.active[name].position = position


    def get_text(self, text_str, color = TXT_COLOR):

        return self.txt_font.render(text_str, 1, color)
    
    def get_widget(self, name):

        return self.widgets[name]
    
    def get_txt_size(self, str):
        return self.txt_font.size(str)
        
        
