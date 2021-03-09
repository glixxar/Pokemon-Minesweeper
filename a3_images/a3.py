import random,math,re
import tkinter.font as tkFont
import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button,BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT,messagebox,simpledialog,filedialog
from PIL import Image, ImageTk
import os


TASK_ONE = 1
TASK_TWO = 2

ENTER = '7'
LEAVE = '8'

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")

POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"

dir_path = os.path.dirname(os.path.realpath(__file__))
POKEBALL_E = dir_path + '/pokeball.png'  
POKEBALL_P = dir_path + '/full_pokeball.png'    
STOPWATCH = dir_path + '/clock.png'
GRASS_U = dir_path + '/unrevealed.png'
GRASS_U_M = dir_path + '/unrevealed_moved.png'

GRASS_R_0 = dir_path + '/zero_adjacent.png'
GRASS_R_1 = dir_path + '/one_adjacent.png'
GRASS_R_2 = dir_path + '/two_adjacent.png'
GRASS_R_3 = dir_path + '/three_adjacent.png'
GRASS_R_4 = dir_path + '/four_adjacent.png'
GRASS_R_5 = dir_path + '/five_adjacent.png'
GRASS_R_6 = dir_path + '/six_adjacent.png'
GRASS_R_7 = dir_path + '/seven_adjacent.png'
GRASS_R_8 = dir_path + '/eight_adjacent.png'

GRASS_DICT = {0:GRASS_R_0, 1:GRASS_R_1, 2:GRASS_R_2, 3:GRASS_R_3, 
4:GRASS_R_4, 5:GRASS_R_5, 6:GRASS_R_6, 7:GRASS_R_7, 8:GRASS_R_8}

CHARIZARD =dir_path + '/pokemon_sprites/charizard.png'
TOGEPI =dir_path + '/pokemon_sprites/togepi.png'
CYNDAQUIL =dir_path + '/pokemon_sprites/cyndaquil.png'
PIKACHU =dir_path + '/pokemon_sprites/pikachu.png'
PSYDUCK =dir_path + '/pokemon_sprites/psyduck.png'
UMBREON =dir_path + '/pokemon_sprites/umbreon.png'

POKEMON_DICT = {0:CHARIZARD, 1:TOGEPI, 2:CYNDAQUIL, 3:PIKACHU, 4:PSYDUCK, 5:UMBREON}

class BoardModel:
    """Board Model object representing the Pokemon Game"""
    def __init__(self, grid_size, num_pokemon):
        """Construct a BoardModel object with the number of pokemon and the grid size

        Parameters:
            grid_size (int): Size of the grid.
            num_pokemon (int): Number of pokemon
        """
        self.grid_size = grid_size
        self.pokeballs = num_pokemon
        self.game = UNEXPOSED * self.grid_size ** 2
        self.num_pokemon = num_pokemon
        self.pokemon_locations = self.generate_pokemons()
        
    def generate_pokemons(self):
        """Pokemons will be generated and given a random index within the game.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = self.grid_size ** 2
        pokemon_locations = ()

        for _ in range(self.num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)
            pokemon_locations += (index,)
        return pokemon_locations
    
    def reset_game(self):
        """Resets the game string for the Board Model object

        Returns:
            None
        """
        self.game = UNEXPOSED * self.grid_size ** 2
    
    def change_game(self,game):
        """ Changes the game string for the Board Model object to 
        the new game string provided

        Parameters:
            game (str): Game string. 
        """
        for i in range(0,len(game)):
            if(game[i] == UNEXPOSED):
                self.replace_character_at_index(i,UNEXPOSED)
            elif(game[i] == POKEMON):
                self.replace_character_at_index(i,POKEMON)
            elif(game[i] == FLAG):
                self.replace_character_at_index(i,FLAG)
            else:
                self.replace_character_at_index(i,game[i])

    def get_game(self):
        """Returns an appropriate representation of the current state of the game
        board.
        
        Returns:
            game (str): Game string. 
        """
        return self.game

    def get_pokemon_locations(self):
        """Returns the indices describing all pokemon locations.
        
        Returns:
            pokemon locations (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        return self.pokemon_locations

    def get_num_attempted_catches(self):
        """Returns the number of pokeballs currently placed on
        the board.
        
        Returns:
            pokeballs (int): Number of pokeballs
        """
        return self.pokeballs
    
    def replace_pokemon_loc(self,pokemon_loc):
        """Replaces the pokemon locations for Board Model with new pokemon locations
        
        Parameters:
            pokemon_loc (string): String version of the pokemon locations tuple
        """
        self.pokemon_locations = None
        self.pokemon_locations = tuple(int(num) for num in pokemon_loc.replace('(', '').replace(')', '').replace('...', '').split(', '))

    def position_to_index(self,position):
        """Convert the row, column coordinate in the grid to the game strings index.
        
        Returns:
            index (int): index of the game string.
        """
        x, y = position
        return x * self.grid_size + y

    def replace_character_at_index(self,index,character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        
        Parameters:
            index (int): index specified to be replaced.
            character (int): character to be replaced with.
        """
        self.game = self.game[:index] + character + self.game[index + 1:]

    def neighbour_directions(self,index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours    

    def index_in_direction(self, index, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        Parameters:
            index (int): The index in the game string.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % self.grid_size
        row = index // self.grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self.grid_size and 0 <= row < self.grid_size):
            return None
        return self.position_to_index((row, col))

    def number_at_cell(self, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """

        if self.game[index] != UNEXPOSED:
            return int(self.game[index])

        number = 0
        for neighbour in self.neighbour_directions(index, self.grid_size):
            if neighbour in self.pokemon_locations:
                number += 1

        return number    

    def big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.
        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self.game[index] == FLAG:
            return queue

        number = self.number_at_cell(index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, self.grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self.game[neighbour] != FLAG:
                    number = self.number_at_cell(neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def flag_cell(self,index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.
        
        Parameter:
            index (int): Selected index to be flagged or toggled.
        """
        if self.game[index] == FLAG:
            self.game = self.game[:index] + UNEXPOSED + self.game[index + 1:]

        elif self.game[index] == UNEXPOSED:
            self.game = self.game[:index] + FLAG + self.game[index + 1:]

    def check_lose(self,index):
        """Checks if the current index is a pokemon location. Returns True if yes and replaces 
        the game string with pokemon at all pokemon locations. Returns False if index is not a pokemon location.

        Parameter:
            index (int): Currently selected index

        """
        if index in self.pokemon_locations:
            for i in self.pokemon_locations:
                self.replace_character_at_index(i, POKEMON)
            return True    
        return False
    
    def check_win(self):
        """Returns True if the every pokemon location in game string is a Flag, returns False otherwise"""
        total= len(self.pokemon_locations)
        count = 0
        for i in self.pokemon_locations:
            if self.game[i] == FLAG:
                count += 1
                if count == total:
                    return True

        return False

    def reveal_cells(self,index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        
        number = self.number_at_cell(index)
        self.replace_character_at_index(index, str(number))
        clear = self.big_fun_search(index)
            
        for i in clear:
            if self.game[i] != FLAG:
                number = self.number_at_cell(i)
                self.replace_character_at_index(i, str(number))

class PokemonGame:
    """Game application that manages communication between the status board, board view and game model."""
    def __init__(self,master, grid_size=10, num_pokemon=5,task=TASK_TWO):
        """Create a new game app within a master widget
        
        Parameters:
            grid_size (int): Size of Pokemon Game grid.
            num_pokemon (int): Number of pokemon in the game.
            task (int): Constant that tells the game to run in which mode.
        """

        self.master = master
        self.grid_size = grid_size
        self.num_pokemon = num_pokemon
        self.task = task

        #Initialises the BoardModel game object
        self.game_board = BoardModel(self.grid_size,self.num_pokemon)
        self.game = self.game_board.get_game()
        
        #Initialise BoardView game object
        self.board_view = None
        self.can_select =True
        self.draw()
        #Creates a prompt to ask whether user wishes to quit
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)
        if(self.task == TASK_TWO):
            #Draws out the Status Board if in Task Two mode
            self.selection = StatusBoard(self.master,self.game_board.get_num_attempted_catches(),self.new_game,self.restart_game)
            self.create_menu()
    
    def draw(self):
        """Draws out the grid of rectangles or grid of grass images based on the Task"""
        self.board_view = BoardView(self.master,self.grid_size,self.game,self.action_left,self.action_right,self.task,self.parse_enter_leave_event)

    def delete_window(self):
        """User messagebox for prompting whether they want to quit"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def won_dialog(self):
        """Informs the user that they have won the game and asks them if they want to quit or continue. Closes 
        game if no is clicked. Restarts game with different pokemon locations."""
        msg = tk.messagebox.askquestion('Game Over','You won! want to play again?')
        self.can_select = False
        if msg =='yes':
            self.new_game()
            self.can_select = True
        else:
            self.master.destroy()


    def lost_dialog(self):
        """Informs the user that they have lost the game and asks them if they want to quit or restart. Closes 
        game if no is clicked. Restarts game with different pokemon locations."""
        if(self.task == TASK_TWO):
            #Pauses the game timer
            self.selection.stop_timer()
            self.can_select = False
            msg = tk.messagebox.askquestion('Game Over','You lost! want to play again?')
            if msg =='yes':
                self.new_game()
                self.can_select = True
            else:
                self.master.destroy()

    def quit_game(self):
        """Asks the user if they want to quit or not. Closes 
        game if yes is clicked. Continues game if no is clicked"""
        if(self.task == TASK_TWO):
            #Pauses the game timer
            self.selection.stop_timer()
            msg = tk.messagebox.askquestion('Quit','You are quitting are you sure?')
            self.can_select = False
            if msg =='yes':
                self.master.destroy()
            else:
                self.selection.update_time()
                self.can_select = True
            
    def action_left(self,position):
        """Parses the user left click action by converting the tag of the canvas item to index.
        
        Parameter:
            position (tuple<int>): Tuple representing the tag of the canvas item.
        """
        index = self.convert_to_index(position[1],position[0])
        #Reveals all pokemon cells if the user clicked on a pokemon and not a flag
        if(self.game_board.check_lose(index) and self.game[index] != FLAG and self.can_select == True):
            self.redraw()
            #Tells user that they lost via messagebox if in Task 1 mode
            if(self.task == TASK_ONE):
                messagebox.showinfo(title="You Lost!", message="You scared away all the Pokemon!")
                self.master.destroy()        
            self.lost_dialog()
        else:
            #Reveals cells if user did not click on a flag
            if(self.game[index] != FLAG and self.can_select == True):
                self.game_board.reveal_cells(index)
                self.redraw()
        
            

    def action_right(self,position):
        """Parses the user right click action by converting the tag of the canvas item to index.
        
        Parameter:
            position (tuple<int>): Tuple representing the tag of the canvas item.
        """

        index = self.convert_to_index(position[1],position[0])
        #Parses if in task one mode and flags cell
        if(self.task== TASK_ONE):
            self.game_board.flag_cell(index)
            self.redraw()
            #Checks if the user has won and shows a messagebox if they have won
            if(self.game_board.check_win()):
                messagebox.showinfo(title="You Win!", message="You have captured all the Pokemon!")
                self.master.destroy()
        else:
            #If not in task one mode, checks to see if user still has pokeballs to throw and then flag cells
            if(self.selection.return_pokeball_left() > 0 and self.can_select == True):
                #Flag cell if cell is unexposed
                if(self.game[index] == UNEXPOSED):
                    self.selection.update_catch()
                    self.game_board.flag_cell(index)
                    self.redraw()
                #Return pokeball if cell is pokeball
                elif(self.game[index] == FLAG):
                    self.selection.update_catch("return")
                    self.game_board.flag_cell(index)
                    self.redraw()
            #Checks to see if player has won 
            if(self.game_board.check_win() and self.can_select == True):
                time = self.selection.stop_timer()
                self.file_exists = False  
                self.can_select = False
                self.parse_win(time)

    
    def parse_enter_leave_event(self,event,tag_id):
        """Highlights cells user has cursor on.
        
        Parameter:
            event: Event callable object
            tag_id (string): Tag for the canvas object to be configured
        """
        #Canvas object to be changed
        canvas = event.widget
        if(self.task == TASK_ONE):
            #Changes outline of rectangle to red on enter and black on leaving
            if event.type == ENTER:
                canvas.itemconfig(tag_id, outline="pink",width=2)
            elif event.type == LEAVE:
                canvas.itemconfig(tag_id, outline="black",width=1)

        elif(self.task == TASK_TWO):
            #Changes image to unexposed moved on enter and unexposed on leaving
            if event.type == ENTER and self.game[tag_id-1] == UNEXPOSED:
                canvas.itemconfig(tag_id, image=self.board_view.state.grass_m)
            elif event.type == LEAVE and self.game[tag_id-1] == UNEXPOSED:
                canvas.itemconfig(tag_id, image=self.board_view.state.grass_u)


                
    def redraw(self):
        """Redraw the game board by updating the images displayed in each grid"""
        self.board_view.delete()
        self.board_view.destroy()
        self.game = self.game_board.get_game()
        self.draw()

    def convert_to_index(self,x_pos,y_pos):
        """Converts the x direction and y direction in string format to index
        
        Parameters:
            x_pos (string): X direction in string format.
            y_pos (string): Y direction in string format.

        Returns:
            index (int): Index of the position.
        """
        return self.game_board.position_to_index((int(x_pos[0]),int(y_pos[1])))

    def new_game(self):
        """Creates a new BoadModel with the same grid size and number of pokemon but different pokemon locations,
        redraws the board and resets the selection board.
        """
        self.game_board = BoardModel(self.grid_size,self.num_pokemon)
        self.redraw()
        self.selection.reset(self.num_pokemon)
        

    def restart_game(self):
        """Creates a new BoadModel with the same grid size and number of pokemon, redraws the board and resets the 
        selection board.
        """
        self.game_board.reset_game()
        self.redraw()
        self.selection.reset(self.num_pokemon)
    
    def save_game(self):
        """Saves the game information to a text file with name specified by user"""
        time = self.selection.stop_timer()
        filename = filedialog.asksaveasfilename(title='Save game',defaultextension=".txt")
        if filename:
            try:
                fd = open(filename,'w',encoding='utf-8')
                fd.write(str(self.game)+'\n')
                fd.write(str((time[0]*60) + time[1]) +'\n')
                fd.write(str(self.selection.return_pokeball_left()) +'\n')
                fd.write(str(self.game_board.get_pokemon_locations()) +'\n')
                fd.close()
            except IOError:
                pass
        #Starts the timer again
        self.selection.update_time()

    def load_game(self): 
        """Loads the game information to a text file with name specified by user"""
        #Stops the timer when loading game
        self.selection.stop_timer()
        filename = filedialog.askopenfilename(title='Load game')
        
        #Loads contents of file 
        if filename:
            try:
                fd = open(filename,'r',encoding='utf-8')
                Lines = fd.readlines()
                fd.close()
                #Checks to see if text file has been tampered
                if len(Lines) == 4:
                    if(Lines[1].isnumeric and Lines[2].isnumeric):
                        #If not load game data
                        temp_game = Lines[0].strip('\n')
                        self.game_board.change_game(temp_game) 
                        self.grid_size = int(math.sqrt(len(temp_game)))
                        self.game_board.grid_size = self.grid_size
                        self.selection.change_time(int(Lines[1].strip('\n'))) 
                        self.game_board.replace_pokemon_loc(Lines[3].strip('\n'))
                        self.selection.change_pokeball_left(int(Lines[2].strip('\n')),len(self.game_board.pokemon_locations)) 
                        self.num_pokemon = len(self.game_board.pokemon_locations)
            except IOError:
                pass
        else:
            self.selection.update_time()
        

        self.redraw() 

    def close_high_score(self):
        """Closes the high score toplevel window"""
        self.high_score_window.destroy()

    def show_high_score(self):
        """Opens, reads and display the score contained in the score.txt file if it exists in a toplevel window"""
        text_lines = ""

        #Widgets for the toplevel window
        self.high_score_window =tk.Toplevel(self.master)
        self.high_score_window.wm_title('Top 3')

        #High Score banner for window
        fontStyle = tkFont.Font(family="Courier New", size=18,weight="bold")
        top = tk.Label(self.high_score_window,text="High Scores",font=fontStyle,bg="light coral",fg="white",relief='raised')
        top.pack(side=tk.TOP)

        #Label for displaying the score
        scores = tk.Label(self.high_score_window)
        scores.pack(side=tk.TOP)

        #Button for closing the toplevel window
        done_but = tk.Button(self.high_score_window,text="Done",command=self.close_high_score)
        done_but.pack(side=tk.TOP)
        
        #Error parsing for opening the score.txt file if it exists
        try:
            fd = open("c:/Users/alvin/Desktop/Python/a3_images/Score.txt",'r',encoding='utf-8')
            Lines = fd.readlines()
            fd.close()
            for x in Lines:
                text_lines += x
            self.high_score_window.geometry("160x120")
            scores.config(text=text_lines)
        except IOError:
            pass
               

    def enter_score_dialog(self,time):
        """Toplevel window for informing user to input their name to be added to the score.txt file"""
        
        #Toplevel window for informing user
        self.score_dialog = tk.Toplevel(self.master)
        self.score_dialog.wm_title('You Win!')

        #Text informing user they won with their time finished
        win_text = 'You won in {}m {}s! Enter your name:'.format(time[0],time[1])
        self.win_label = tk.Label(self.score_dialog,text=win_text)
        self.win_label.pack(side=tk.TOP)

        #Entry box for user to fill in
        self.entry = tk.Entry(self.score_dialog)
        self.entry.pack(side=tk.TOP)

        #Button for closing the toplevel window
        self.done_button = tk.Button(self.score_dialog,text='Done',command=self.score_dialog_done)
        self.done_button.pack(side=tk.BOTTOM)
        self.win_time = time

    def score_dialog_done(self): 
        """Parses how the score needs to be entered into the score text file if the file exists and creates the file if it 
        doesn't exist."""

        self.top_name = self.entry.get()
        #Checks if user enters empty or none answer
        if(self.top_name == "" or None):
            self.top_name = "Unknown"
        #Creates and writes score to file if file does not exist
        if(self.file_exists == False):
            try:
                fd = open("c:/Users/alvin/Desktop/Python/a3_images/Score.txt",'w',encoding='utf-8')
                fd.write(self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1]))
                fd.close()
            except IOError:
                pass
            self.score_dialog.destroy()
            self.won_dialog()
        #Writes to file if file exists
        elif(self.file_exists == True):
            #Inserts if score beats initial score and appends if it does not
            if(len(self.Score_Lines) == 1):
                if(self.Insert):
                    self.Score_Lines.insert(self.Insert_index,self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1]))
                elif(self.Append):
                    self.Score_Lines.append(self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1])) 
            
            #Inserts if score beats initial score and appends if it does not
            elif(len(self.Score_Lines)== 2):
                if(self.Insert):
                    self.Score_Lines.insert(self.Insert_index,self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1]))
                elif(self.Append):
                    self.Score_Lines.append(self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1]))
            
            #Replaces initial score if score beats any in list
            elif(self.change_index == True):
                self.Score_Lines[self.index_2_change] = self.top_name + ' {}m {}s'.format(self.win_time[0],self.win_time[1])
            
            #Adds new line to each score line
            for x in range(0,len(self.Score_Lines)):
                if "\n" not in self.Score_Lines[x]:
                    self.Score_Lines[x]=self.Score_Lines[x] + '\n'
            try:
                #Writes newly changed scores into Score.txt
                fd = open("c:/Users/alvin/Desktop/Python/a3_images/Score.txt",'w',encoding='utf-8')
                fd.writelines("%s" % place for place in self.Score_Lines)
                fd.close()
            except IOError:
                pass
            self.score_dialog.destroy()
            self.won_dialog()
            
    def parse_win(self,time):
        """Checks to see if the user's score is faster than the scores contained in the text file.
        
        Parameters:
            time (int): Users' win time in seconds    
        """

        #Truth statements and variables for determining whether to append or insert
        self.Insert = False
        self.Append = False
        self.change_index = False
        self.Insert_index = 0
        self.index_2_change = 0
        
        try:
            #Opens and reads the score file 
            fd = open("c:/Users/alvin/Desktop/Python/a3_images/Score.txt",'r',encoding='utf-8')
            self.Score_Lines = fd.readlines()
            fd.close()
            #Integer for checking length of score lines
            loop_int =0

            #Iterates the through the score lines
            for x in self.Score_Lines:
                #Finds all the integers in each line and adds them
                temp_int = re.findall(r'\d+', x) 
                sec_list = list(map(int, temp_int)) 
                score_time_sum = int(sec_list[0]*60) + int(sec_list[1])
                user_time_sum = int(time[0]*60) + int(time[1])

                #Checks if there is only one line in score_lines
                if(len(self.Score_Lines) == 1):
                    #Checks if the first score is longer than the new score
                    if(score_time_sum > user_time_sum):
                        self.Insert = True
                        self.Insert_index = 0
                        self.enter_score_dialog(time)
                    #Appends the new score to the empty second line
                    else:
                        self.Append = True  
                        self.enter_score_dialog(time)

                #Checks if there are two lines in score_lines         
                elif(len(self.Score_Lines) == 2):
                    #Checks if the first score is longer than the new score
                    if(score_time_sum > user_time_sum and loop_int == 0):
                        self.Insert = True
                        self.Insert_index = loop_int
                        self.enter_score_dialog(time)
                    #Checks if the second score is longer than the new score    
                    elif(score_time_sum > user_time_sum and loop_int == 1):
                        self.Insert = True
                        self.Insert_index = loop_int
                        self.enter_score_dialog(time)
                    #Appends the new score to the empty third line
                    elif(loop_int == 1):
                        self.Append = True
                        self.enter_score_dialog(time)

                #Checks if there are two lines in score_lines          
                elif(len(self.Score_Lines) == 3):
                    #Replaces the first score if longer than the new score
                    if(score_time_sum > user_time_sum and loop_int == 0):
                        self.change_index = True
                        self.index_2_change = loop_int
                        self.enter_score_dialog(time)
                    #Replaces the second score if longer than the new score    
                    elif(score_time_sum > user_time_sum and loop_int == 1 and not self.change_index):
                        self.change_index = True
                        self.index_2_change = loop_int
                        self.enter_score_dialog(time)
                    #Replaces the third score if longer than the new score    
                    elif(score_time_sum > user_time_sum and loop_int== 2 and not self.change_index):        
                        self.change_index = True
                        self.index_2_change = loop_int
                        self.enter_score_dialog(time)
                loop_int += 1

            #Shows the win dialog if the user won regardless
            if(not self.Insert and not self.Append and not self.change_index):
                self.won_dialog()
            self.file_exists = True
        except IOError:
            self.enter_score_dialog(time)
            

    def create_menu(self):
        """Creates a drop down menubar with its associated commands."""
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save game",command=self.save_game)
        filemenu.add_command(label="Load game",command=self.load_game)
        filemenu.add_command(label="Restart game",command=self.restart_game)
        filemenu.add_command(label="New game",command=self.new_game)
        filemenu.add_command(label='High Scores',command=self.show_high_score)
        filemenu.add_command(label="Quit",command=self.quit_game)

class BoardView(tk.Canvas):
    """View of the Rectangle game board"""
    def __init__(self,master, grid_size, game,  action_left=None,action_right=None,task = TASK_ONE,parse_enter_leave_event=None,board_width=600,*args, **kwargs):
        """Construct a board view from a game string and grid size.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (int): Grid size of the game board.
            action_left (callable): Callable to call when left mouse button is pressed.
            action_right (callable): Callable to call when right mouse button is pressed.
            parse_enter_leave_event (callable): Callable to call when cursor enters and leaves canvas item.
            """

        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid_size =grid_size
        self.board_width = board_width
        self.action_left = action_left
        self.action_right = action_right
        self.parse_enter_leave_event = parse_enter_leave_event
        self.interval = self.board_width//self.grid_size
        self.task = task
        #Creates ImageBoardView instead if task two
        if(self.task == TASK_TWO):
            self.state = ImageBoardView(self.master,self.grid_size,self.board_width,self.action_left,self.action_right,self.parse_enter_leave_event)
            self.state.draw_board(game)
        else:
            self.draw_board()
            self.draw_grid()
            self.draw_rec(game)

    def delete(self):
        """Deletes all content on canvas including canvas"""
        if(self.task == TASK_TWO):
            #Calls delete function in ImageBoardView if in task 2
            self.state.delete()
        else:
            self.canvas.delete('all')
            self.canvas.destroy()
            self.banner.destroy()

    def right_click_event(self,event):
        """Parses right clicked object and sends it to Pokemon Game to intepret"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        item_tag = self.canvas.gettags(item)
        self.action_right(item_tag)

    def left_click_event(self,event):
        """Parses left clicked object and sends it to Pokemon Game to intepret"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        item_tag = self.canvas.gettags(item)
        self.action_left(item_tag) 

    def enter_event(self,event,r_id):
        """Parses enter and leave event and sends it to Pokemon Game to intepret"""
        self.parse_enter_leave_event(event,r_id)
        

    def draw_board(self):
        """Draws the banner and canvas for the Board"""
        size = self.board_width//23
        fontStyle = tkFont.Font(family="Courier New", size=size,weight="bold")
        self.banner = tk.Label(self.master,text="Pokemon: Got 2 Find Them All!",font=fontStyle,bg="light coral",fg="white", relief='raised' )
        self.banner.pack(side=tk.TOP)

        self.canvas = tk.Canvas(self.master, width=self.board_width, height=self.board_width, bg='white')
        self.canvas.pack(side=tk.TOP)


    def draw_grid(self):
        """Draws the grid lines for the canvas."""
        self.canvas.delete('grid_line') 
        x_position=0
        y_position=0
        # Creates all vertical lines at intevals of 0 to grid size
        for z_counter in range(0, self.grid_size, 1): 
            self.canvas.create_line([(x_position, 0), (x_position, self.board_width)], tag='grid_line')
            x_position+=self.interval
            
        # Creates all horizontal lines at intevals of 0 to grid size
        for i_counter in range(0, self.grid_size, 1):
            self.canvas.create_line([(0, y_position), (self.board_width, y_position)], tag='grid_line')
            y_position+=self.interval



    def draw_rec(self,game):
        """Draws rectangles on the game board according to provided game string
        
        Parameters: 
            game (string): The game string for the game model
        """

        #Counting variables for positioning the rectangles and the text
        game_index = 0
        first_x_position = 0
        first_y_position = 0
        second_x_position = self.interval
        second_y_position = self.interval

        #Creates rectangles according to grid size squared
        for i in range(0,self.grid_size,1):
            for x in range(0,self.grid_size,1):
                rec_tag = (x,i)
                rec_tag = str(rec_tag)

                #Creates rectangles of different colors according to game index
                if(game[game_index] == FLAG):
                    tag = self.canvas.create_rectangle([first_x_position,first_y_position],[second_x_position,second_y_position],fill="red",tags=rec_tag)

                elif(game[game_index].isnumeric()):     
                    tag = self.canvas.create_rectangle([first_x_position,first_y_position],[second_x_position,second_y_position],fill="light green",tags=rec_tag)
                    self.canvas.create_text((self.interval//2+first_x_position,self.interval//2+first_y_position), text=game[game_index], font=("Purisa", 12))
                    
                elif(game[game_index] == POKEMON):
                    tag = self.canvas.create_rectangle([first_x_position,first_y_position],[second_x_position,second_y_position],fill="yellow",tags=rec_tag)
                else:
                    tag = self.canvas.create_rectangle([first_x_position,first_y_position],[second_x_position,second_y_position],fill="dark green",tags=rec_tag)   

                #Binds button presses and enter/leave events
                self.canvas.tag_bind(tag,'<ButtonPress-1>',self.left_click_event)  
                self.canvas.tag_bind(tag,'<ButtonPress-2>',self.right_click_event)  
                self.canvas.tag_bind(tag,'<ButtonPress-3>',self.right_click_event)  
                self.canvas.tag_bind(tag,'<Enter>', lambda event, t=tag:self.enter_event(event,t))
                self.canvas.tag_bind(tag,'<Leave>', lambda event, t=tag:self.enter_event(event,t))    
                
                #Updates the both x variables for positioning
                game_index += 1
                first_x_position += self.interval
                second_x_position += self.interval

            #Updates the both y variables for positioning    
            first_y_position += self.interval
            second_y_position += self.interval

            #Resets first x position to 0 and second position to the interval
            first_x_position = 0
            second_x_position = self.interval

class ImageBoardView(BoardView):
    """View of the Image game board"""
    def __init__(self,master,grid_size, board_width=600, action_left=None,action_right=None,parse_enter_leave_event=None,*args,**kwargs):
        """Construct a image board view from a game string and grid size.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (int): Grid size of the game board.
            action_left (callable): Callable to call when left mouse button is pressed.
            action_right (callable): Callable to call when right mouse button is pressed.
            parse_enter_leave_event (callable): Callable to call when cursor enters and leaves canvas item.
            """
        
        self.master = master
        self.grid_size = grid_size
        self.board_width = board_width
        self.interval = self.board_width//self.grid_size

        #Initialise callable to call 
        self.action_left = action_left
        self.action_right = action_right
        self.parse_enter_leave_event = parse_enter_leave_event

        #Create and import image containers
        self.grass,self.pokeball = None,None
        self.import_images()
    
    def delete(self):
        """Destroy canvas and canvas items"""
        self.canvas.delete('all')
        self.canvas.destroy()
        self.banner.destroy()
    
    def import_images(self):
        """Imports unreavealed.png, unrevealed_moved.png and pokeball.png images for display"""
        self.grass_u = ImageTk.PhotoImage(Image.open(GRASS_U).resize((self.interval,self.interval),Image.ANTIALIAS))
        self.grass_m = ImageTk.PhotoImage(Image.open(GRASS_U_M).resize((self.interval,self.interval),Image.ANTIALIAS))
        self.pokeball = ImageTk.PhotoImage(Image.open(POKEBALL_E).resize((self.interval,self.interval),Image.ANTIALIAS))

        
    def draw_board(self,game):
        """Draws rectangles on the game board according to provided game string
        
        Parameters: 
            game (string): The game string for the game model
        """        
        super().draw_board()

        #Empty lists for creating references to images
        self.images = []
        self.images_p = []

        #Counting variables for positioning the images 
        game_index  = 0
        first_x_position = 0
        first_y_position = 0

        #Creates and resizes images according to grid size squared
        for i in range(0,self.grid_size,1):
            for x in range(0,self.grid_size,1):
                
                #Random integer for choosing different pokemon to be revealed
                pokemon_int = random.randint(0,5)
                rec_tag = (x,i)
                rec_tag = str(rec_tag)

                #Creates and assigns images of according to game index
                if(game[game_index] == FLAG):
                    tag = self.canvas.create_image(self.interval//2+first_x_position,self.interval//2+first_y_position,image=self.pokeball,tags=rec_tag) 

                elif(game[game_index].isnumeric()): 
                    grass_num_ = ImageTk.PhotoImage(Image.open(GRASS_DICT[int(game[game_index])]).resize((self.interval,self.interval),Image.ANTIALIAS) )
                    self.images.append(grass_num_) #Creates a reference to the image
                    tag = self.canvas.create_image(self.interval//2+first_x_position,self.interval//2+first_y_position,image=grass_num_,tags=rec_tag)
                    
                elif(game[game_index] == POKEMON):
                    pokemon_ran = ImageTk.PhotoImage(Image.open(POKEMON_DICT[pokemon_int]).resize((self.interval,self.interval),Image.ANTIALIAS))
                    self.images_p.append(pokemon_ran)#Creates a reference to the image
                    tag = self.canvas.create_image(self.interval//2+first_x_position,self.interval//2+first_y_position,image=pokemon_ran,tags=rec_tag)

                else:
                    tag = self.canvas.create_image(self.interval//2+first_x_position,self.interval//2+first_y_position,image=self.grass_u,tags=rec_tag)   
                
                #Binds button presses and enter/leave events
                self.canvas.tag_bind(tag,'<ButtonPress-1>',self.left_click_event)  
                self.canvas.tag_bind(tag,'<ButtonPress-2>',self.right_click_event)  
                self.canvas.tag_bind(tag,'<ButtonPress-3>',self.right_click_event)  
                self.canvas.tag_bind(tag,'<Enter>', lambda event, t=tag:self.enter_event(event,t))
                self.canvas.tag_bind(tag,'<Leave>', lambda event, t=tag:self.enter_event(event,t))   

                #Increments the game index counter and first x position counter for image positioning
                game_index += 1
                first_x_position += self.interval

            #Increments the y position counter by self.interval and resets the first x position counter    
            first_y_position += self.interval
            first_x_position = 0
            

    def left_click_event(self,event):
        """Parses left clicked object and sends it to Pokemon Game to intepret"""
        super().left_click_event(event)
    
    def right_click_event(self,event):
        """Parses right clicked object and sends it to Pokemon Game to intepret"""
        super().right_click_event(event)

    def enter_event(self,event,r_id):
        """Parses enter and leave event and sends it to Pokemon Game to intepret"""
        super().enter_event(event,r_id) 

class StatusBoard(tk.Frame):
    """Status board display of the pokeballs available, time and start/restart buttons."""
    def __init__(self,master,pokeball_left=10,new_game=None,restart_game=None,attempted_catch=0,width=600):
        """
        Construct a new status board display frame.

        Parameters:
            master (tk.Widget): Widget within which to place the selection panel.
            pokeball_left (int): Amount of pokeball left in the game
            new_game (callable): Function or method to call when a new game button is pressed.
            restart_game (callable): Function or method to call when a restart button is pressed.
            attempted_catch (int): Number of catches attempted.
            width (int): Width of the frame

        """
        self.master = master
        self.width = width
        self.new_game = new_game
        self.restart_game = restart_game
        self.pokeball_left = pokeball_left 
        self.attempted_catch = attempted_catch
        #Self defined constant of how high the status board frame has to be 
        self.height = 150
        self.import_images() 
        self.draw_status_bar()

    def reset(self,num_pokemon):
        """Resets the number of pokeball left as well as their respective labels along with the timer.
        
        Parameter: 
            num_pokemon (int): Number of pokemon
        """
        self.pokeball_left = num_pokemon
        self.attempted_catch = 0
        self.seconds = 0
        
        self.a_catch.config(text=str(self.attempted_catch)+' attempted catches')
        self.r_pokeball.config(text=str(self.pokeball_left)+' pokeballs left')

        self.timer.after_cancel(self.timer_i)
        self.timer.config(text="0m 0s")
        self.timer.after(1000,self.update_time)  
        
        
    def create_timer(self):
        """Creates and intialises all labels including image which are associated with timer. Also creates and after 
        call to start the timer after 1ms."""
        t_label = tk.Label(self.selection, image=self.timer_img,borderwidth=0, highlightthickness = 0)
        t_label.place(relx=0.6, rely=   0.5, anchor='e') 

        timer_desc = tk.Label(self.selection,text='Time Elapsed',bg='white')
        timer_desc.place(relx=0.741,rely=0.42,anchor='e')
        
        self.timer= tk.Label(self.selection, text="0m 0s", bg='white')
        self.timer.place(relx=0.71,rely=0.55,anchor='e')
        self.seconds = 0
        self.timer.after(1,self.update_time)    
    
    def import_images(self):
        """Imports the pokeball.png and timer.png images."""
        self.pokeball_img = ImageTk.PhotoImage(Image.open(POKEBALL_P))
        self.timer_img = ImageTk.PhotoImage(Image.open(STOPWATCH))

    def draw_status_bar(self):
        """Creates and draws the status bar."""
        self.selection = tk.Frame(self.master,width=self.width, height=self.height,bg='white')
        self.selection.pack(side=tk.BOTTOM)

        self.draw_button()
        self.draw_catches()
        self.create_timer()


    def draw_button(self):
        """Creates the new game and restart buttons."""
        new_but = tk.Button(self.selection, text="New Game",width=8,command=self.new_game_button)
        new_but.place(relx=0.9, rely=   0.4, anchor='s')

        res_but = tk.Button(self.selection, text="Restart Game",width=10,command=self.restart_game_button)
        res_but.place(relx=0.9, rely=   0.7, anchor='s')

    def draw_catches(self):
        """Creates and places the pokeball image along with the attempted catch and pokeball left labels.
        """
        p_label = tk.Label(self.selection, image=self.pokeball_img,borderwidth=0, highlightthickness = 0)
        p_label.place(relx=0.2, rely=   0.5, anchor='e')

        self.a_catch =  tk.Label(self.selection,text=str(self.attempted_catch)+' attempted catches',bg='white')
        self.a_catch.place(relx=0.409, rely=   0.42, anchor='e')

        self.r_pokeball = tk.Label(self.selection,text=str(self.pokeball_left)+' pokeballs left',bg='white')
        self.r_pokeball.place(relx=0.36, rely=   0.55, anchor='e')

    def update_catch(self,action="catch"):
        """Updates the number of catches depending on the action provided.
        
        Parameters:
            action (string): Action to be taken to update catches.
        """
        if action == "catch":
            self.attempted_catch += 1
            self.pokeball_left -= 1
        elif action == "return":
            self.attempted_catch -= 1
            self.pokeball_left += 1

        self.a_catch.config(text=str(self.attempted_catch)+' attempted catches')
        self.r_pokeball.config(text=str(self.pokeball_left)+' pokeballs left')
        

    def update_time(self):
        """Self calling function that continually updates the timer after 1 second."""
        self.seconds += 1
        self.timer.config(text="{}m {}s".format(self.seconds//60,self.seconds%60))
        self.timer_i=self.timer.after(1000,self.update_time)
    
    def return_pokeball_left(self):
        """Returns the number of pokeballs left.
        
        Returns:
            pokeball_left (int): Number of pokeball(s) left.
        """
        return self.pokeball_left   
    
    def stop_timer(self):
        """Stops the timer and returns the time.

        Returns:
            time (tuple<int,int>): Time in minutes and seconds
        """
        self.timer.after_cancel(self.timer_i)
        return (self.seconds//60,self.seconds%60)
    
    def change_time(self,time):
        """Changes the time for the current timer to the new time.
        
        Parameters:
            time (int): Time in seconds
        """
        self.seconds = time
        self.update_time()
    
    def change_pokeball_left(self,pokeball,num_pokemon):
        """Changes and updates the number of pokeballs and attempted catches left to the new value assigned to it.
        
        Parameters:
            pokeball (int): New number of pokeballs left
            num_pokemon (int): Number of pokemons on the board
        """
        self.pokeball_left = pokeball
        self.attempted_catch = num_pokemon - pokeball
        self.a_catch.config(text=str(self.attempted_catch)+' attempted catches')
        self.r_pokeball.config(text=str(self.pokeball_left)+' pokeballs left')

    def new_game_button(self):
        """Parses new game button press and sends it to Pokemon Game to intepret"""
        self.new_game()
        self.timer.after_cancel(self.timer_i)
    
    def restart_game_button(self):
        """Parses restart game button press and sends it to Pokemon Game to intepret"""
        self.restart_game()
        self.timer.after_cancel(self.timer_i)

def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 Find Them All!")
 
    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
