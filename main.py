import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, EASY, MEDIUM, HARD, GREY, BLACK
from checkers.game import Game
from minimax.algorithm import minimax, alphabeta, computerMoves

# Setting a constant FPS for the game
FPS = 60

# making the Window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#title of the game 
pygame.display.set_caption('Checkers')


#get the coordiantes of the position of the mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE  #the y axis over the total of the square size 
    col = x // SQUARE_SIZE
    return row, col

#get the 3 difficulty of the game with it's buttons
def getDiff():
    difficulty = None
    algorithm = ""
    EASY_BUTTON = pygame.Rect(340, 400, 100, 50)
    MEDIUM_BUTTON = pygame.Rect(340, 300, 100, 50)
    HARD_BUTTON = pygame.Rect(340, 200, 100, 50)
    MINIMAX_BUTTON = pygame.Rect(100, 500, 150, 50)
    ALPHABETA_BUTTON = pygame.Rect(530, 500, 150, 50)
    
    #while game is running just keep loading the game
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #in case of exiting 
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if a button was clicked
                if EASY_BUTTON.collidepoint(mouse_pos):
                    difficulty = EASY
                elif MEDIUM_BUTTON.collidepoint(mouse_pos):
                    difficulty = MEDIUM
                elif HARD_BUTTON.collidepoint(mouse_pos):
                    difficulty = HARD
                elif MINIMAX_BUTTON.collidepoint(mouse_pos):
                    algorithm = "minimax"
                elif ALPHABETA_BUTTON.collidepoint(mouse_pos):
                    algorithm = "alphabeta"
                if difficulty and algorithm != "":
                    run = False

        # Fill the background of the difficulty with color grey
        WIN.fill(GREY)
        
        # Draw the buttons
        pygame.draw.rect(WIN, WHITE, EASY_BUTTON)
        pygame.draw.rect(WIN, WHITE, MEDIUM_BUTTON)
        pygame.draw.rect(WIN, WHITE, HARD_BUTTON)
        pygame.draw.rect(WIN, WHITE, MINIMAX_BUTTON)
        pygame.draw.rect(WIN, WHITE, ALPHABETA_BUTTON)

        pygame.font.init()
        font = pygame.font.SysFont('Aerial', 32)
        label = pygame.font.SysFont('Aerial', 50)
        easy_text = font.render("Easy", True, BLACK)
        medium_text = font.render("Medium", True, BLACK)
        hard_text = font.render("Hard", True, BLACK)
        minimax_text = font.render("Minimax", True, BLACK)
        alphabeta_text = font.render("Alpha-Beta", True, BLACK)
        diffi = label.render("Choose Your Difficulity & Algorithm", True, BLACK)

        WIN.blit(easy_text, (EASY_BUTTON.x + 20, EASY_BUTTON.y + 15))
        WIN.blit(medium_text, (MEDIUM_BUTTON.x + 10, MEDIUM_BUTTON.y + 15))
        WIN.blit(hard_text, (HARD_BUTTON.x + 20, HARD_BUTTON.y + 15))
        WIN.blit(minimax_text, (MINIMAX_BUTTON.x + 30, MINIMAX_BUTTON.y + 15))
        WIN.blit(alphabeta_text, (ALPHABETA_BUTTON.x + 20, ALPHABETA_BUTTON.y + 15))
        WIN.blit(diffi, (120,75))
        
        pygame.display.update()

    return difficulty, algorithm
    


def main():
    diff, algorithm = getDiff()
    if(diff == None): #must choose a difficulty
        pygame.quit()
        return
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)



    ALPHA = float('-inf')
    BETA = float('inf')

    while run:
        clock.tick(FPS)
        
        # red ---> white >> 3 red >>  6 
        if game.turn == WHITE:
            if algorithm == "minimax": # in case of choosing the minimax
                value, new_board = minimax(game.get_board(), diff, True, game)
            else:
                value, new_board = alphabeta(game.get_board(), diff, ALPHA, BETA, True, game)
            game.ai_move(new_board) # Change Turn
        
        else:
            # new_board = computerMoves(game.get_board(), RED, game)
            value, new_board = alphabeta(game.get_board(), 3, BETA, ALPHA, False, game)
            game.ai_move(new_board) # Change Turn
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col) 
        
        #printing in the console output the winner 
        if game.winner() != None:
            print("******************************************************")
            if(game.winner() == RED):
                print("RED WINS!")
            else:
                print("WHITE WINS!")
            print("******************************************************")
            run = False
        game.update()
    pygame.quit()

main()