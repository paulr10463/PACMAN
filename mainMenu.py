from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import os

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets", "frame0")

class MainMenu:

    rectangle_position = 0
    canvas = 0
    selector = 0
    options_positions = {}
    option = -1

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)


    def on_key_press(self, event, window):
        if event.keysym == 'Up':
            self.rectangle_position = (self.rectangle_position - 1) % 3
        elif event.keysym == 'Down':
            self.rectangle_position = (self.rectangle_position + 1) % 3
        self.canvas.coords(
            self.selector, 
            290.0, 
            self.options_positions[self.rectangle_position] - 3, 
            431.0, 
            self.options_positions[self.rectangle_position] + 3)

    ###### Función para manejar las teclas presionadas ######
        # Check the current position and perform actions
        # 1 -> Play
        # 2 -> Scores
        # 3 -> Exit
        if event.keysym == 'Return':
            if self.rectangle_position == 0:
                self.option = 0
            elif self.rectangle_position == 1:
                self.option = 1
            elif self.rectangle_position == 2:
                # Action for button_4 (Add your code here)
                window.destroy()

    def setImage(self, src, x, y):
        image = PhotoImage( file=self.relative_to_assets(src) )
        self.canvas.create_image(x, y, image=image)
        return image
        
    def show(self):
        window = Tk()
        ##################################################
        window.title("Pacman")
        # Obtener dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcular coordenadas para centrar la ventana
        x_position = (screen_width - WINDOW_WIDTH) // 2
        y_position = (screen_height - WINDOW_HEIGHT) // 2

        # Establecer la geometría de la ventana
        window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}")
        window.configure(bg="#222429")

        self.canvas = Canvas(window, bg = "#222429", height = 720, width = 720, bd = 0, highlightthickness = 0, relief = "ridge")

        ################## MENU ###################

        self.canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            360.0,
            123.0,
            image=image_image_1
        )

        # -----------------------------------------------
        ####### OJO: Manejar las posiciones desde aqui #########
        x_center = self.canvas.winfo_reqwidth() / 2  # Obtenemos el ancho del canvas y dividimos por 2
        y_offset = 70.0
        # -----------------------------------------------

        # -----------------------------------------------

        Option_play_image = PhotoImage(
            file=self.relative_to_assets("Option_play.png"))
        Option_play = self.canvas.create_image(
            x_center,
            234.0 + y_offset,
            image=Option_play_image
        )

        # -----------------------------------------------
        # the python interpreter needs this values to be assigned to some variable even if this is not used? wtf
        
        scores = self.setImage("Option_scores.png", x_center, 305.0 + y_offset)
        exit = self.setImage("Option_exit.png", x_center, 376.0 + y_offset)

        ##################################################
        ##################################################

        ################## PIE DE MENU ###################

        image2 = self.setImage("image_2.png", 168.0, 633.0)
        image3 = self.setImage("image_3.png", 357.99999237060547, 627.0)
        image4 = self.setImage("image_4.png", 424.0, 627.0)
        image5 = self.setImage("image_5.png", 551.0, 627.0)
        image6 = self.setImage("image_6.png", 491.0, 627.0)


        self.canvas.create_rectangle(212.0, 626.0, 225.0, 639.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle(240.0, 626.0, 253.0, 639.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle( 268.0, 626.0, 281.0, 639.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle( 295.0, 626.0, 308.0, 639.0, fill="#D9D9D9", outline="")

        ##################################################
        ##################################################

        ########## DISEÑO SELECTOR DE OPCIONES ###########
        # Posiciones de cada

        # Define the positions of buttons
        self.options_positions = [self.canvas.coords(Option_play)[1]+20.0, self.canvas.coords(Option_play)[1]+91, self.canvas.coords(Option_play)[1]+162]

        # Draw the rectangle initially under button_2
        self.selector = self.canvas.create_rectangle(
            290.0,
            self.options_positions[self.rectangle_position] - 3,
            431.0,
            self.options_positions[self.rectangle_position] + 3,
            fill="#FFFFFF",
            outline=""
        )

        window.resizable(False, False)
        window.bind('<KeyPress>', lambda event: self.on_key_press(event, window))
        window.mainloop()
        return self.option

