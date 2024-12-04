from callbacks.information import show_information
from callbacks.level_1 import level_1
from callbacks.level_2 import level_2
from callbacks.level_3 import level_3
from callbacks.level_4 import level_4
from callbacks.level_5 import level_5
from callbacks.level_6 import level_6
from callbacks.level_7 import level_7
from callbacks.level_8 import level_8
from callbacks.level_9 import level_9

class Callback:
    def __init__(self, button_label, main_screen):
        if button_label == "Informationen":
            show_information(main_screen)

        if "Level" in button_label:
            globals()[button_label.lower().replace(" ", "_")](main_screen)

        else:
            print(f"Button {button_label} was clicked.")
            

    