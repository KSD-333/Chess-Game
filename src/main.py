import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH , HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            #show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                
                #for cliking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos) 

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    #if clicked square has piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        #check if its a valid piece 
                        if piece.color == game.next_player:
                            board.calc_moves(piece , clicked_row , clicked_col , bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            #shw methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                #for mouse motion 
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row , motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen) 
                        

                #for click relese 
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #create possible moves
                        initial = Square(dragger.initial_row , dragger.initial_col)
                        final = Square(released_row , released_col)
                        move = Move(initial , final)

                        #valid move..?
                        if board.valid_move(dragger.piece , move):
                            #normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece , move)

                            board.set_true_en_passant(dragger.piece)
                            #play the sound
                            game.play_sound(captured)
                            #draw show Method
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            #next turn
                            game.next_turn()

                    dragger.undrag_piece()

                #key press
                elif event.type == pygame.KEYDOWN:

                    #for changing the theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    #for restarting the game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        screen = self.screen
                        dragger = self.game.dragger
                        board = self.game.board

                #for quiting the aaplication
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  

            pygame.display.update()

main = Main()
main.mainloop()