from pygame import *
from modules.menu import *
import os
import platform

class ChessGame:
    def __init__(self):
        init()
        if platform.system() == 'Windows':
          os.environ['SDL_VIDEODRIVER'] = 'windib'    # Ensure compatability
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre game window

        self.screen = display.set_mode((600, 600))
        self.turn = 1
        self.wcastle = 0
        self.bcastle = 0
        self.selected = None
        self.moves = []
        self.captures = []
        self.wcaptured = []
        self.bcaptured = []
        self.game_board = [None for _ in range(64)]
        self.en_passant = None

        # Load images
        self.load_images()

        # Create game board
        self.create_board()

        # Initialize GUI elements
        self.init_gui()

        # Initialize menus
        self.init_menus()

    def load_images(self):
        self.king1 = image.load("assets/images/wking.png").convert_alpha()
        self.king2 = image.load("assets/images/bking.png").convert_alpha()
        self.pawn1 = image.load("assets/images/wpawn.png").convert_alpha()
        self.pawn2 = image.load("assets/images/bpawn.png").convert_alpha()
        self.rook1 = image.load("assets/images/wrook.png").convert_alpha()
        self.rook2 = image.load("assets/images/brook.png").convert_alpha()
        self.queen1 = image.load("assets/images/wqueen.png").convert_alpha()
        self.queen2 = image.load("assets/images/bqueen.png").convert_alpha()
        self.bishop1 = image.load("assets/images/wbishop.png").convert_alpha()
        self.bishop2 = image.load("assets/images/bbishop.png").convert_alpha()
        self.knight1 = image.load("assets/images/wknight.png").convert_alpha()
        self.knight2 = image.load("assets/images/bknight.png").convert_alpha()

    def create_board(self):
        self.font1 = font.Font('assets/fonts/Alido.otf',18)
        self.font2 = font.Font('assets/fonts/LCALLIG.ttf',36)

        self.win_bg = Surface((250,90))
        self.win_bg.fill((0,0,0))
        draw.rect(self.win_bg,(255,255,255),(5,5,240,80))

        self.layer_black = Surface((50,50))
        self.layer_black.fill((128,128,128))
        self.layer_hovered = Surface((50,50))
        self.layer_hovered.fill((0,0,255))
        self.layer_selected = Surface((50,50))
        self.layer_selected.fill((0,255,0))
        self.layer_is_move = Surface((50,50),SRCALPHA)
        self.layer_is_move.fill((0,0,255,85))
        self.layer_is_capture = Surface((50,50))
        self.layer_is_capture.fill((255,0,0))

        self.new_bg = Surface((100,20))
        self.new_bg.fill((255,0,0))
        self.new_bg2 = Surface((100,20))
        self.new_bg2.fill((0,0,255))

        self.promote_layer = Surface((120,120))
        self.promote_layer.fill((255,255,255))
        draw.rect(self.promote_layer,(0,0,0),(5,5,110,110))
        draw.rect(self.promote_layer,(255,255,255),(10,10,100,100))
        draw.line(self.promote_layer,(0,0,0),(10,60),(110,60),5)
        draw.line(self.promote_layer,(0,0,0),(60,10),(60,110),5)

    def init_gui(self):
        self.game_menu = make_menu((0,0,800,800),'game',0)
        open_menu(self.game_menu)

        self.board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

        for i in range(64):
            if (i+i//8)%2 == 0:
                self.board_buttons[i].add_layer(self.layer_black,(0,0),(0,))

        self.new_game = Button((2,2,50,20),'new',(0,))
        self.new_game.add_layer(self.new_bg,(0,0),(2,))
        self.new_game.add_text("Reset",self.font1,(0,0,0),(25,10),1,0,(0,))

        self.quit_button = Button((548,2,50,20),'quit',(0,))
        self.quit_button.add_layer(self.new_bg,(0,0),(2,))
        self.quit_button.add_text("Quit",self.font1,(0,0,0),(25,10),1,0,(0,))

        add_layer_multi(self.layer_hovered,(0,0),(2,-5,-6,-7),self.board_buttons)
        add_layer_multi(self.layer_selected,(0,0),(5,),self.board_buttons)
        add_layer_multi(self.layer_is_move,(0,0),(-5,6,-7),self.board_buttons)
        add_layer_multi(self.layer_is_capture,(0,0),(-5,7),self.board_buttons)

        add_objects(self.game_menu,self.board_buttons)
        add_objects(self.game_menu,(self.new_game,self.quit_button))

    def init_menus(self):           
        # Win menu
        self.win_menu = make_menu((175,270,250,90),'win',1)
        self.win_menu.add_layer(self.win_bg,(0,0),(5,6))
        self.win_menu.add_text("White wins!",self.font2,(0,0,0),(125,30),1,0,(5,))
        self.win_menu.add_text("Black wins!",self.font2,(0,0,0),(125,30),1,0,(6,))
        self.new_game2 = Button((10,60,100,20),'new',(0,))
        self.new_game2.add_layer(self.new_bg,(0,0),(2,))
        self.new_game2.add_layer(self.new_bg2,(0,0),(0,-2))
        self.new_game2.add_text("New Game",self.font1,(255,255,255),(50,10),1,0,(0,))
        self.win_menu.add_object(self.new_game2)
        self.quit2 = Button((180,60,50,20),'quit',(0,))
        self.quit2.add_layer(self.new_bg,(0,0),(2,))
        self.quit2.add_layer(self.new_bg2,(0,0),(0,-2))
        self.quit2.add_text("Quit",self.font1,(255,255,255),(25,10),1,0,(0,))
        self.win_menu.add_object(self.quit2)

        # Promotion menus
        self.wqueen_btn = Button((10,10,50,50),'Q',(0,))
        self.wknight_btn = Button((60,10,50,50),'N',(0,))
        self.wrook_btn = Button((10,60,50,50),'R',(0,))
        self.wbishop_btn = Button((60,60,50,50),'B',(0,))

        self.bqueen_btn = Button((10,10,50,50),'Q',(0,))
        self.bknight_btn = Button((60,10,50,50),'N',(0,))
        self.brook_btn = Button((10,60,50,50),'R',(0,))
        self.bbishop_btn = Button((60,60,50,50),'B',(0,))

        add_layer_multi(self.layer_hovered,(0,0),(2,),(self.wqueen_btn,self.wknight_btn,self.wrook_btn,self.wbishop_btn,
                                                  self.bqueen_btn,self.bknight_btn,self.brook_btn,self.bbishop_btn))

        self.wqueen_btn.add_layer(self.queen1,(0,0),(0,))
        self.wrook_btn.add_layer(self.rook1,(0,0),(0,))
        self.wknight_btn.add_layer(self.knight1,(0,0),(0,))
        self.wbishop_btn.add_layer(self.bishop1,(0,0),(0,))
        self.bqueen_btn.add_layer(self.queen2,(0,0),(0,))
        self.brook_btn.add_layer(self.rook2,(0,0),(0,))
        self.bknight_btn.add_layer(self.knight2,(0,0),(0,))
        self.bbishop_btn.add_layer(self.bishop2,(0,0),(0,))

        self.wpromote_menu = make_menu((240,240,120,120),'wpromote',1)
        self.wpromote_menu.add_layer(self.promote_layer,(0,0),(0,))
        add_objects(self.wpromote_menu,(self.wqueen_btn,self.wknight_btn,self.wrook_btn,self.wbishop_btn))

        self.bpromote_menu = make_menu((240,240,120,120),'bpromote',1)
        self.bpromote_menu.add_layer(self.promote_layer,(0,0),(0,))
        add_objects(self.bpromote_menu,(self.bqueen_btn,self.bknight_btn,self.brook_btn,self.bbishop_btn))

        self.reset_game()
    
    def reset_game(self):
        """Puts all of the pieces back"""
        close_menu(self.win_menu)
        self.win_menu.event_off(5)
        self.win_menu.event_off(6)
        self.deselect_piece()
        self.turn = 1
        self.wcastle = 0
        self.bcastle = 0
        self.wcaptured = []
        self.bcaptured = []
        self.game_board[0] = 'R1'; self.game_board[7] = 'R1'; self.game_board[-1] = 'R2'; self.game_board[-8] = 'R2'
        self.game_board[1] = 'N1'; self.game_board[6] = 'N1'; self.game_board[-2] = 'N2'; self.game_board[-7] = 'N2'
        self.game_board[2] = 'B1'; self.game_board[5] = 'B1'; self.game_board[-3] = 'B2'; self.game_board[-6] = 'B2'
        self.game_board[4] = 'K1'; self.game_board[3] = 'Q1'; self.game_board[-4] = 'K2'; self.game_board[-5] = 'Q2'
        for i in range(8):
            self.game_board[8+i] = 'P1'
            self.game_board[48+i] = 'P2'
        for i in range(32):
            self.game_board[16+i] = None

    def select_piece(self, location):
        """Attempts to select the piece at location"""
        # Remove illegal selections
        if self.game_board[location] == None or self.game_board[location][1] != str(self.turn):
            return

        self.selected = location
        self.moves = []
        self.captures = []

        # Pawn for player 1
        if self.game_board[self.selected] == 'P1':
            if self.game_board[self.selected+8] == None:
                self.moves.append(self.selected+8)
                if self.selected//8 == 1 and self.game_board[self.selected+16] == None:
                    self.moves.append(self.selected+16)
            if self.selected%8 != 0 and ((self.game_board[self.selected+7] != None and self.game_board[self.selected+7][1] == '2') or \
                                    (self.game_board[self.selected-1] == 'P2' and self.en_passent == self.selected-1)):
                self.captures.append(self.selected+7)
            if self.selected%8 != 7 and ((self.game_board[self.selected+9] != None and self.game_board[self.selected+9][1] == '2') or \
                                    (self.game_board[self.selected+1] == 'P2' and self.en_passent == self.selected+1)):
                self.captures.append(self.selected+9)

        # Pawn for player 2
        if self.game_board[self.selected] == 'P2':
            if self.game_board[self.selected-8] == None:
                self.moves.append(self.selected-8)
                if self.selected//8 == 6 and self.game_board[self.selected-16] == None:
                    self.moves.append(self.selected-16)
            if self.selected%8 != 7 and ((self.game_board[self.selected-7] != None and self.game_board[self.selected-7][1] == '1') or \
                                    (self.game_board[self.selected+1] == 'P1' and self.en_passent == self.selected+1)):
                self.captures.append(self.selected-7)
            if self.selected%8 != 0 and ((self.game_board[self.selected-9] != None and self.game_board[self.selected-9][1] == '1') or \
                                    (self.game_board[self.selected-1] == 'P1' and self.en_passent == self.selected-1)):
                self.captures.append(self.selected-9)

        # Rook and half of Queen for both players
        if self.game_board[self.selected][0] in 'RQ':
            x,y = self.selected%8,self.selected//8

            for i in range(x+1,8,1):
                if self.game_board[i+y*8] == None:   # Check if no blocking piece
                    self.moves.append(i+y*8)
                elif self.game_board[i+y*8][1] != str(self.turn): # Check if is attacking
                    self.captures.append(i+y*8)
                    break
                else:
                    break

            for i in range(x-1,-1,-1):
                if self.game_board[i+y*8] == None:
                    self.moves.append(i+y*8)
                elif self.game_board[i+y*8][1] != str(self.turn):
                    self.captures.append(i+y*8)
                    break
                else:
                    break

            for i in range(y+1,8,1):
                if self.game_board[x+i*8] == None:
                    self.moves.append(x+i*8)
                elif self.game_board[x+i*8][1] != str(self.turn):
                    self.captures.append(x+i*8)
                    break
                else:
                    break

            for i in range(y-1,-1,-1):
                if self.game_board[x+i*8] == None:
                    self.moves.append(x+i*8)
                elif self.game_board[x+i*8][1] != str(self.turn):
                    self.captures.append(x+i*8)
                    break
                else:
                    break

        # Bishop and other half of Queen for both players
        if self.game_board[self.selected][0] in 'BQ':

            i = self.selected+7
            while (i-7)%8 != 0 and (i-7)//8 != 7:   # Check if valid move
                if self.game_board[i] == None:   # Check if no blocking piece
                    self.moves.append(i)
                elif self.game_board[i][1] != str(self.turn): # Check if is attacking
                    self.captures.append(i)
                    break
                else:
                    break
                i += 7

            i = self.selected+9
            while (i-9)%8 != 7 and (i-9)//8 != 7:
                if self.game_board[i] == None:
                    self.moves.append(i)
                elif self.game_board[i][1] != str(self.turn):
                    self.captures.append(i)
                    break
                else:
                    break
                i += 9

            i = self.selected-7
            while (i+7)%8 != 7 and (i+7)//8 != 0:
                if self.game_board[i] == None:
                    self.moves.append(i)
                elif self.game_board[i][1] != str(self.turn):
                    self.captures.append(i)
                    break
                else:
                    break
                i -= 7

            i = self.selected-9
            while (i+9)%8 != 0 and (i+9)//8 != 0:
                if self.game_board[i] == None:
                    self.moves.append(i)
                elif self.game_board[i][1] != str(self.turn):
                    self.captures.append(i)
                    break
                else:
                    break
                i -= 9

        # Knight for both players
        if self.game_board[self.selected][0] == 'N':
            x,y = self.selected%8,self.selected//8

            if x >= 2 and y <= 6:   # Check if valid move
                if self.game_board[(x-2)+(y+1)*8] == None:   # Check if no blocking piece
                    self.moves.append((x-2)+(y+1)*8)
                elif self.game_board[(x-2)+(y+1)*8][1] != str(self.turn): # Check if is attacking
                    self.captures.append((x-2)+(y+1)*8)
            if x >= 1 and y <= 5:
                if self.game_board[(x-1)+(y+2)*8] == None:
                    self.moves.append((x-1)+(y+2)*8)
                elif self.game_board[(x-1)+(y+2)*8][1] != str(self.turn):
                    self.captures.append((x-1)+(y+2)*8)

            if x <= 6 and y <= 5:
                if self.game_board[(x+1)+(y+2)*8] == None:
                    self.moves.append((x+1)+(y+2)*8)
                elif self.game_board[(x+1)+(y+2)*8][1] != str(self.turn):
                    self.captures.append((x+1)+(y+2)*8)
            if x <= 5 and y <= 6:
                if self.game_board[(x+2)+(y+1)*8] == None:
                    self.moves.append((x+2)+(y+1)*8)
                elif self.game_board[(x+2)+(y+1)*8][1] != str(self.turn):
                    self.captures.append((x+2)+(y+1)*8)

            if x <= 5 and y >= 1:
                if self.game_board[(x+2)+(y-1)*8] == None:
                    self.moves.append((x+2)+(y-1)*8)
                elif self.game_board[(x+2)+(y-1)*8][1] != str(self.turn):
                    self.captures.append((x+2)+(y-1)*8)
            if x <= 6 and y >= 2:
                if self.game_board[(x+1)+(y-2)*8] == None:
                    self.moves.append((x+1)+(y-2)*8)
                elif self.game_board[(x+1)+(y-2)*8][1] != str(self.turn):
                    self.captures.append((x+1)+(y-2)*8)

            if x >= 1 and y >= 2:
                if self.game_board[(x-1)+(y-2)*8] == None:
                    self.moves.append((x-1)+(y-2)*8)
                elif self.game_board[(x-1)+(y-2)*8][1] != str(self.turn):
                    self.captures.append((x-1)+(y-2)*8)
            if x >= 2 and y >= 1:
                if self.game_board[(x-2)+(y-1)*8] == None:
                    self.moves.append((x-2)+(y-1)*8)
                elif self.game_board[(x-2)+(y-1)*8][1] != str(self.turn):
                    self.captures.append((x-2)+(y-1)*8)

        # King for both players
        if self.game_board[self.selected][0] == 'K':
            x,y = self.selected%8,self.selected//8
            attacked = self.attacked_spaces(1+self.turn%2,self.game_board)

            if self.selected == 3 and self.wcastle%2 == 0 and \
              self.game_board[1] == None and self.game_board[2] == None and\
              not 1 in attacked and not 2 in attacked and not 3 in attacked:
                self.moves.append(1)
            if self.selected == 3 and -1 < self.wcastle < 2 and \
              self.game_board[4] == None and self.game_board[5] == None and self.game_board[6] == None and\
              not 3 in attacked and not 4 in attacked and not 5 in attacked:
                self.moves.append(5)

            if self.selected == 59 and self.bcastle%2 == 0 and \
              self.game_board[58] == None and self.game_board[57] == None and\
              not 57 in attacked and not 58 in attacked and not 59 in attacked:
                self.moves.append(57)
            if self.selected == 59 and -1 < self.bcastle < 2 and \
              self.game_board[60] == None and self.game_board[61] == None and self.game_board[62] == None and\
              not 59 in attacked and not 60 in attacked and not 61 in attacked:
                self.moves.append(61)

            if x >= 1 and y <= 6: # Check if valid move
                if self.game_board[(x-1)+(y+1)*8] == None:   # Check if no blocking piece
                    self.moves.append((x-1)+(y+1)*8)
                elif self.game_board[(x-1)+(y+1)*8][1] != str(self.turn): # Check if is attacking
                    self.captures.append((x-1)+(y+1)*8)
            if y <= 6:
                if self.game_board[x+(y+1)*8] == None:
                    self.moves.append(x+(y+1)*8)
                elif self.game_board[x+(y+1)*8][1] != str(self.turn):
                    self.captures.append(x+(y+1)*8)
            if x <= 6 and y <= 6:
                if self.game_board[(x+1)+(y+1)*8] == None:
                    self.moves.append((x+1)+(y+1)*8)
                elif self.game_board[(x+1)+(y+1)*8][1] != str(self.turn):
                    self.captures.append((x+1)+(y+1)*8)
            if x <= 6:
                if self.game_board[(x+1)+y*8] == None:
                    self.moves.append((x+1)+y*8)
                elif self.game_board[(x+1)+y*8][1] != str(self.turn):
                    self.captures.append((x+1)+y*8)
            if x <= 6 and y >= 1:
                if self.game_board[(x+1)+(y-1)*8] == None:
                    self.moves.append((x+1)+(y-1)*8)
                elif self.game_board[(x+1)+(y-1)*8][1] != str(self.turn):
                    self.captures.append((x+1)+(y-1)*8)
            if y >= 1:
                if self.game_board[x+(y-1)*8] == None:
                    self.moves.append(x+(y-1)*8)
                elif self.game_board[x+(y-1)*8][1] != str(self.turn):
                    self.captures.append(x+(y-1)*8)
            if x >= 1 and y >= 1:
                if self.game_board[(x-1)+(y-1)*8] == None:
                    self.moves.append((x-1)+(y-1)*8)
                elif self.game_board[(x-1)+(y-1)*8][1] != str(self.turn):
                    self.captures.append((x-1)+(y-1)*8)
            if x >= 1:
                if self.game_board[(x-1)+y*8] == None:
                    self.moves.append((x-1)+y*8)
                elif self.game_board[(x-1)+y*8][1] != str(self.turn):
                    self.captures.append((x-1)+y*8)

        # Find the player's king
        for i in range(64):
            if self.game_board[i] != None and self.game_board[i][0] == 'K' and self.game_board[i][1] == str(self.turn):
                break

        # See if a move allows the king to be taken
        t_moves = list(self.moves)
        for j in t_moves:
            t_game = list(self.game_board)
            t_game[j] = t_game[self.selected]
            t_game[self.selected] = None
            if self.game_board[self.selected][0] == 'K':
                i = j
            if i in self.attacked_spaces(1+self.turn%2,t_game):
                self.moves.remove(j)

        # See if a capture allows the king to be taken
        t_captures = list(self.captures)
        for j in t_captures:
            t_game = list(self.game_board)
            t_game[j] = t_game[self.selected]
            t_game[self.selected] = None
            if self.game_board[self.selected][0] == 'K':
                i = j
            if i in self.attacked_spaces(1+self.turn%2,t_game):
                self.captures.remove(j)

        self.board_buttons[self.selected].event_on(5)
        for i in self.moves:
            self.board_buttons[i].event_on(6)
        for i in self.captures:
            self.board_buttons[i].event_on(7)

    def deselect_piece(self):
            """Deselects the selected piece"""
            if self.selected != None:
                self.board_buttons[self.selected].event_off(5)
                for i in self.moves:
                    self.board_buttons[i].event_off(6)
                for i in self.captures:
                    self.board_buttons[i].event_off(7)

                self.captures = []
                self.moves = []
                self.selected = None

    def move_piece(self, destination):
        """Moves the selected piece"""
        if self.game_board[self.selected][0] == 'P':
            # En-passent rule activation
            if abs(destination-self.selected) in (7,9) and self.en_passent != None and abs(self.en_passent-destination) == 8:
                self.game_board[self.en_passent] = None

            # En-passent rule initiation
            self.en_passent = None
            if abs(destination-self.selected) == 16:
                self.en_passent = destination

            # Open the menu to select promotion
            if destination < 8 and self.turn == 2:
                open_menu(self.wpromote_menu)
            if destination > 55 and self.turn == 1:
                open_menu(self.wpromote_menu)

        # Deny castling to moved rooks
        if self.game_board[self.selected] == 'R1':
            if self.selected == 0:
                if self.wcastle == 2: self.wcastle = -1
                else:            self.wcastle = 1
            elif self.selected == 7:
                if self.wcastle == 1: self.wcastle = -1
                else:            self.wcastle = 2
        if self.game_board[self.selected] == 'R2':
            if self.selected == 56:
                if self.bcastle == 2: self.bcastle = -1
                else:            self.bcastle = 1
            elif self.selected == 63:
                if self.bcastle == 1: self.bcastle = -1
                else:            self.bcastle = 2

        # Activate castling move
        if self.game_board[self.selected][0] == 'K' and abs(destination-self.selected) == 2:
            if destination == 1:
                self.game_board[2] = 'R1'
                self.game_board[0] = None
            elif destination == 5:
                self.game_board[4] = 'R1'
                self.game_board[7] = None
            elif destination == 61:
                self.game_board[60] = 'R2'
                self.game_board[63] = None
            elif destination == 57:
                self.game_board[58] = 'R2'
                self.game_board[56] = None

        # Deny castling to moved king
        if self.game_board[self.selected] == 'K1':
            self.wcastle = -1
        if self.game_board[self.selected] == 'K2':
            self.bcastle = -1

        # Add captured piece to list of captured pieces
        if destination in self.captures:
            if self.turn == 1:
                if self.game_board[destination] == None:
                    self.wcaptured.append("P")
                else:
                    self.wcaptured.append(self.game_board[destination][0])
                self.wcaptured = sorted(self.wcaptured,key = lambda x: "PBNRQ".find(x))
            else:
                if self.game_board[destination] == None:
                    self.bcaptured.append("P")
                else:
                    self.bcaptured.append(self.game_board[destination][0])
                self.bcaptured = sorted(self.bcaptured,key = lambda x: "PBNRQ".find(x))

        self.game_board[destination] = self.game_board[self.selected]
        self.game_board[self.selected] = None

    def attacked_spaces(self, player,board):
        """Returns which spaces a player is currently able to attack"""

        attacked = []

        for i in range(64):
            if board[i] == None:
                continue

            # Pawn for player 1
            if board[i] == 'P1' and player == 1:
                if i%8 != 0:
                    attacked.append(i+7)
                if i%8 != 7:
                    attacked.append(i+9)

            # Pawn for player 2
            if board[i] == 'P2' and player == 2:
                if i%8 != 7:
                    attacked.append(i-7)
                if i%8 != 0:
                    attacked.append(i-9)

            # Rook and half of Queen for both players
            if board[i][0] in 'RQ' and board[i][1] == str(player):
                x,y = i%8,i//8

                for j in range(x+1,8,1):
                    attacked.append(j+y*8)
                    if board[j+y*8] != None:
                        break

                for j in range(x-1,-1,-1):
                    attacked.append(j+y*8)
                    if board[j+y*8] != None:
                        break

                for j in range(y+1,8,1):
                    attacked.append(x+j*8)
                    if board[x+j*8] != None:
                        break

                for j in range(y-1,-1,-1):
                    attacked.append(x+j*8)
                    if board[x+j*8] != None:
                        break

            # Bishop and other half of Queen for both players
            if board[i][0] in 'BQ' and board[i][1] == str(player):

                j = i+7
                while (j-7)%8 != 0 and (j-7)//8 != 7:
                    attacked.append(j)
                    if board[j] != None:
                        break
                    j += 7

                j = i+9
                while (j-9)%8 != 7 and (j-9)//8 != 7:
                    attacked.append(j)
                    if board[j] != None:
                        break
                    j += 9

                j = i-7
                while (j+7)%8 != 7 and (j+7)//8 != 0:
                    attacked.append(j)
                    if board[j] != None:
                        break
                    j -= 7

                j = i-9
                while (j+9)%8 != 0 and (j+9)//8 != 0:
                    attacked.append(j)
                    if board[j] != None:
                        break
                    j -= 9

            # Knight for both players
            if board[i][0] == 'N' and board[i][1] == str(player):
                x,y = i%8,i//8

                if x >= 2 and y <= 6:
                    attacked.append((x-2)+(y+1)*8)
                if x >= 1 and y <= 5:
                    attacked.append((x-1)+(y+2)*8)

                if x <= 6 and y <= 5:
                    attacked.append((x+1)+(y+2)*8)
                if x <= 5 and y <= 6:
                    attacked.append((x+2)+(y+1)*8)

                if x <= 5 and y >= 1:
                    attacked.append((x+2)+(y-1)*8)
                if x <= 6 and y >= 2:
                    attacked.append((x+1)+(y-2)*8)

                if x >= 1 and y >= 2:
                    attacked.append((x-1)+(y-2)*8)
                if x >= 2 and y >= 1:
                    attacked.append((x-2)+(y-1)*8)

            if board[i][0] == 'K' and board[i][1] == str(player):
                x,y = i%8,i//8

                if x >= 1 and y <= 6:
                    attacked.append((x-1)+(y+1)*8)
                if y <= 6:
                    attacked.append(x+(y+1)*8)
                if x <= 6 and y <= 6:
                    attacked.append((x+1)+(y+1)*8)
                if x <= 6:
                        attacked.append((x+1)+y*8)
                if x <= 6 and y >= 1:
                    attacked.append((x+1)+(y-1)*8)
                if y >= 1:
                    attacked.append(x+(y-1)*8)
                if x >= 1 and y >= 1:
                    attacked.append((x-1)+(y-1)*8)
                if x >= 1:
                    attacked.append((x-1)+y*8)

        return attacked

    def is_checkmated(self):
        """Returns 1 if the player with the current turn to move is checkmated"""
        for i in range(64):
            self.select_piece(i)
            if self.moves+self.captures != []:
                self.deselect_piece()
                return 0
            self.deselect_piece()
        return 1

    def main_loop(self):
            self.running = 1
            while self.running:
                """ STEP 1: Get inputs """
                chars = ''
                for evnt in event.get():
                    if evnt.type == QUIT:
                        self.running = 0
                    elif evnt.type == KEYDOWN:
                        if evnt.key == K_ESCAPE:
                            self.running = 0
                        else:
                            chars += evnt.str

                lc,rc = mouse.get_pressed()[0:2]
                mx,my = mouse.get_pos()

                """ STEP 2: Handle inputs / update menus """

                update_menus(mx,my,lc,chars)

                if is_menu_open(self.wpromote_menu) or is_menu_open(self.wpromote_menu):  # Promotion menus
                    for i in self.wpromote_menu.get_pressed():   # Check selection
                        close_menu(self.wpromote_menu)
                        self.game_board[c] = i+'1'
                        self.deselect_piece()
                        self.turn = 2
                        if self.is_checkmated():
                            open_menu(self.win_menu)
                            self.win_menu.event_on(4)

                    for i in self.bpromote_menu.get_pressed():   # Check selection
                        close_menu(self.bpromote_menu)
                        self.game_board[c] = i+'2'
                        self.deselect_piece()
                        self.turn = 1
                        if self.is_checkmated():
                            open_menu(self.win_menu)
                            self.win_menu.event_on(5)

                elif is_menu_open(self.game_menu):
                    # Handle the game board and game menu
                    for c in self.game_menu.get_pressed():
                        if c == 'new':      # Reset game button
                            self.reset_game()
                        elif c == 'quit':   # Exit game button
                            self.running = 0
                        else:
                            if self.selected == None:    # Select piece that was clicked on
                                self.select_piece(c)
                            else:
                                if self.selected == c:   # Deselect currently selected piece
                                    self.deselect_piece()
                                else:
                                    if c in self.moves or c in self.captures: # If the chosen square is an option
                                        self.move_piece(c)

                                        if not is_menu_open(self.wpromote_menu) and not is_menu_open(self.wpromote_menu):
                                            self.deselect_piece()
                                            self.turn = 1+self.turn%2
                                            if self.is_checkmated():
                                                open_menu(self.win_menu)
                                                self.win_menu.event_on(5+self.turn%2)
                                        else:
                                            break

                                    else:
                                        self.deselect_piece()
                                        self.select_piece(c)

                if is_menu_open(self.win_menu):
                    for i in self.win_menu.get_pressed():
                        if i == 'quit':
                            self.running = 0
                        elif i == 'new':
                            self.reset_game()

                """ STEP 3: Draw menus """

                update_menu_images()

                if is_menu_open(self.game_menu):
                    # Show which pieces are captured
                    i = 0
                    p = 0
                    for piece in self.wcaptured:
                        if piece == "P":
                            if p == 0:
                                self.game_menu.blit(self.pawn2,(0,50))
                            p += 1
                        else:
                            i += 50
                        if piece == "B": self.game_menu.blit(self.bishop2,(0,50+i))
                        if piece == "N": self.game_menu.blit(self.knight2,(0,50+i))
                        if piece == "R": self.game_menu.blit(self.rook2,(0,50+i))
                        if piece == "Q": self.game_menu.blit(self.queen2,(0,50+i))
                    if p != 0:
                        msg = self.font1.render(str(p),1,(255,255,255))
                        self.game_menu.blit(msg,(20,68))

                    i = 0
                    p = 0
                    for piece in self.bcaptured:
                        if piece == "P":
                            if p == 0:
                                self.game_menu.blit(self.pawn1,(550,50))
                            p += 1
                        else:
                            i += 50
                        if piece == "B": self.game_menu.blit(self.bishop1,(550,50+i))
                        if piece == "N": self.game_menu.blit(self.knight1,(550,50+i))
                        if piece == "R": self.game_menu.blit(self.rook1,(550,50+i))
                        if piece == "Q": self.game_menu.blit(self.queen1,(550,50+i))
                    if p != 0:
                        msg = self.font1.render(str(p),1,(0,0,0))
                        self.game_menu.blit(msg,(570,68))

                    # Draw the pieces on the game board
                    for i in range(64):
                        if self.game_board[i] == 'P1':
                            self.game_menu.blit(self.pawn1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'P2':
                            self.game_menu.blit(self.pawn2,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'K1':
                            self.game_menu.blit(self.king1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'K2':
                            self.game_menu.blit(self.king2,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'Q1':
                            self.game_menu.blit(self.queen1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'Q2':
                            self.game_menu.blit(self.queen2,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'R1':
                            self.game_menu.blit(self.rook1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'R2':
                            self.game_menu.blit(self.rook2,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'B1':
                            self.game_menu.blit(self.bishop1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'B2':
                            self.game_menu.blit(self.bishop2,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'N1':
                            self.game_menu.blit(self.knight1,(100+(i%8)*50,450-(i//8)*50))
                        if self.game_board[i] == 'N2':
                            self.game_menu.blit(self.knight2,(100+(i%8)*50,450-(i//8)*50))

                self.screen.fill((255,255,255))
                draw.rect(self.screen,(0,0,0),(50,50,500,500))
                draw.rect(self.screen,(255,255,255),(100,100,400,400))
                draw_menus(self.screen)

                display.flip()
                time.wait(10)

if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.main_loop()
