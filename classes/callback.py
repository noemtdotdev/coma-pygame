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
        
        elif button_label == "Level 1":
            level_1(main_screen)

        elif button_label == "Level 2":
            level_2(main_screen)

        elif button_label == "Level 3":
            level_3(main_screen)

        elif button_label == "Level 4":
            level_4(main_screen)

        elif button_label == "Level 5":
            level_5(main_screen)

        elif button_label == "Level 6":
            level_6(main_screen)

        elif button_label == "Level 7":
            level_7(main_screen)

        elif button_label == "Level 8":
            level_8(main_screen)
        
        elif button_label == "Level 9":
            level_9(main_screen)

        else:
            print(f"Button {button_label} was clicked.")
            

    