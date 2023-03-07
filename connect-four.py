import pygame, sys, copy, random
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

BLUE = (0, 50, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BGCOLOR = BLACK

DIFFICULTY = 2

BOARDWIDTH = 8
BOARDHEIGHT = 7

TOKENSIZE = 57

XMARGIN = (WINDOWWIDTH - (TOKENSIZE * BOARDWIDTH)) / 2
YMARGIN = (WINDOWHEIGHT - (TOKENSIZE * BOARDHEIGHT)) / 2

FPS = 60

BLANK = None
RED = "red"
YELLOW = "yellow"
TIE = "tie"

def runGame(isPlayingWithComputer):
    board = getBlankBoard()
    turn = RED
    result = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        if isPlayingWithComputer:
            # if you play with computer
            if turn == RED:
                # human turn, human is red
                getHumanMove(board, RED)
                if isWinner(board, RED):
                    result = RED
                    break
                turn = YELLOW
            else:
                # computer turn, computer is yellow
                getComputerMove(board)
                if isWinner(board, YELLOW):
                    result = YELLOW
                    break
                turn = RED
            if isBoardFull(board):
                result = TIE
                break
        else:
            # if you play with your friend
            if turn == RED:
                # red turn
                getHumanMove(board, RED)
                if isWinner(board, RED):
                    result = RED
                    break
                turn = YELLOW
            else:
                # yellow turn
                getHumanMove(board, YELLOW)
                if isWinner(board, YELLOW):
                    result = YELLOW
                    break
                turn = RED
            if isBoardFull(board):
                result = TIE
                break
    return showTextScreen(result.upper())

def isValidMove(board, column):
    if column >= 0 and column < BOARDWIDTH and board[0][column] == BLANK:
        return True
    else:
        return False
    
def main():
    global DISPLAYSURF, BOARD_IMAGE, RED_TOKEN_IMAGE, YELLOW_TOKEN_IMAGE
    global RED_PILE_RECT, YELLOW_PILE_RECT, CLOCK
    pygame.init()
    pygame.display.set_caption("Four in row")
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    CLOCK = pygame.time.Clock()
    RED_TOKEN_IMAGE = pygame.transform.scale(pygame.image.load("4row_red.png"), (TOKENSIZE, TOKENSIZE))
    YELLOW_TOKEN_IMAGE = pygame.transform.scale(pygame.image.load("4row_yellow.png"), (TOKENSIZE, TOKENSIZE))
    BOARD_IMAGE = pygame.transform.scale(pygame.image.load("4row_board.png"), (TOKENSIZE, TOKENSIZE))
    RED_PILE_RECT = pygame.Rect(70, WINDOWHEIGHT - 100, TOKENSIZE, TOKENSIZE)
    YELLOW_PILE_RECT = pygame.Rect(WINDOWWIDTH - 120, WINDOWHEIGHT - 100, TOKENSIZE, TOKENSIZE)
    
    isPlayingWithComputer = showTextScreen("CONNECT 4")
    while True:
        isPlayingWithComputer = runGame(isPlayingWithComputer)    

def terminate():
    pygame.quit()
    sys.exit()

def drawBoard(board, extraToken = None):
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(RED_TOKEN_IMAGE, RED_PILE_RECT)
    DISPLAYSURF.blit(YELLOW_TOKEN_IMAGE, YELLOW_PILE_RECT)

    if extraToken != None:
        if extraToken["color"] == RED:
            DISPLAYSURF.blit(RED_TOKEN_IMAGE, (extraToken["x"], extraToken["y"]))
        elif extraToken["color"] == YELLOW:
            DISPLAYSURF.blit(YELLOW_TOKEN_IMAGE, (extraToken["x"], extraToken["y"]))

    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            if board[y][x] == RED:
                DISPLAYSURF.blit(RED_TOKEN_IMAGE, (XMARGIN + x * TOKENSIZE, YMARGIN + y * TOKENSIZE))
            elif board[y][x] == YELLOW:
                DISPLAYSURF.blit(YELLOW_TOKEN_IMAGE, (XMARGIN + x * TOKENSIZE, YMARGIN + y * TOKENSIZE))
            DISPLAYSURF.blit(BOARD_IMAGE, (XMARGIN + x * TOKENSIZE, YMARGIN + y * TOKENSIZE))

def getBlankBoard():
    board = []
    for y in range(BOARDHEIGHT):
        board.append([BLANK] * BOARDWIDTH)
    return board
    
def getLowestBlankSpace(board, column):
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[y][column] == BLANK:
            return y

def makeMove(board, column, color):
    lowestBlankSpace = getLowestBlankSpace(board, column)
    board[lowestBlankSpace][column] = color

def animateDroppingToken(board, column, color):
    x = XMARGIN + TOKENSIZE * column
    y = YMARGIN - 50
    dropSpeed = 1
    lowestBlankSpace = getLowestBlankSpace(board, column)
    while lowestBlankSpace * TOKENSIZE + YMARGIN > y:
        y += int(dropSpeed)
        dropSpeed += 0.5
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board, {"x": x, "y": y, "color": color})
        pygame.display.update()
        CLOCK.tick(FPS)

def isWinner(board, color):
    for y in range(BOARDHEIGHT - 3):
        for x in range(BOARDWIDTH):
            if board[y + 1][x] == color and board[y][x] == color and board[y + 2][x] == color and board[y + 3][x] == color:
                return True
            
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[y][x] == color and board[y][x + 1] == color and board[y][x + 2] == color and board[y][x + 3] == color:
                return True
            
    for y in range(BOARDHEIGHT - 3):
        for x in range(BOARDWIDTH - 3):
            if board[y][x] == color and board[y + 1][x + 1] == color and board[y + 2][x + 2] == color and board[y + 3][x + 3] == color:
                return True

    for y in range(4):
        for x in range(3, BOARDWIDTH):
            if board[y][x] == color and board[y + 1][x - 1] == color and board[y + 2][x - 2] == color and board[y + 3][x - 3] == color:
                return True
            
    return False

def isBoardFull(board):
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            if board[y][x] == BLANK:
                return False
    return True

def makeText(text, fontSize, color):
    font = pygame.font.SysFont("Arial", fontSize, bold=True)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect()
    return textSurf, textRect

def animateComputerMove(board, column):
    x = YELLOW_PILE_RECT.left
    y = YELLOW_PILE_RECT.top
    speed = 1

    while y > YMARGIN - 50:
        y -= speed
        speed += 1
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board, {"x": x, "y": y, "color":  YELLOW})
        pygame.display.update()
        CLOCK.tick(FPS)

    speed = 1
    while x > XMARGIN + TOKENSIZE * column:
        x -= speed
        speed += 1
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board, {"x": x, "y": y, "color":  YELLOW})
        pygame.display.update()
        CLOCK.tick(FPS)

    animateDroppingToken(board, column, YELLOW)

def findBestMove(board):
    potentialMoves = getPotentialMoves(board, YELLOW, DIFFICULTY)
    bestMoveFitness = -1
    for i in range(BOARDWIDTH):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)

def getPotentialMoves(board, tile, lookAhead):
    if lookAhead == 0 or isBoardFull(board):
        return [0] * BOARDWIDTH

    if tile == RED:
        enemyTile = YELLOW
    else:
        enemyTile = RED

    potentialMoves = [0] * BOARDWIDTH
    for firstMove in range(BOARDWIDTH):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, firstMove):
            continue
        makeMove(dupeBoard, firstMove, tile)
        if isWinner(dupeBoard, tile):
            potentialMoves[firstMove] = 1
            break 
        else:
            if isBoardFull(dupeBoard):
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(BOARDWIDTH):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    makeMove(dupeBoard2, counterMove, enemyTile)
                    if isWinner(dupeBoard2, enemyTile):
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves 

def getComputerMove(board):
    bestMove = findBestMove(board)
    animateComputerMove(board, bestMove)
    makeMove(board, bestMove, YELLOW)
    drawBoard(board)

def showTextScreen(text):
    alpha = 128
    r, g, b = BLACK
    surf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    surf = surf.convert_alpha()
    surf.fill((r, g, b, alpha))

    titleSurf, titleRect = makeText(text, 60, WHITE)
    onePlayerSurf, onePlayerRect = makeText("ONE  PLAYER", 30, WHITE)
    twoPlayersSurf, twoPlayersRect = makeText("TWO  PLAYERS", 30, WHITE)

    titleRect.center = (WINDOWWIDTH / 2, 200)
    onePlayerRect.center = (WINDOWWIDTH / 2, 320)
    twoPlayersRect.center = (WINDOWWIDTH / 2, 390)
    
    DISPLAYSURF.blit(surf, (0, 0))
    DISPLAYSURF.blit(titleSurf, titleRect)
    DISPLAYSURF.blit(onePlayerSurf, onePlayerRect)
    DISPLAYSURF.blit(twoPlayersSurf, twoPlayersRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONUP:
                if twoPlayersRect.collidepoint(event.pos):
                    return False
                if onePlayerRect.collidepoint(event.pos):
                    return True
            
        pygame.display.update()
        CLOCK.tick(FPS)
    
def getHumanMove(board, turn):
    draggingToken = False
    tokenx, tokeny = None, None
    draggedTokenColor = RED if turn == RED else YELLOW

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken:
                if (turn == RED and RED_PILE_RECT.collidepoint(event.pos)) or (turn == YELLOW and YELLOW_PILE_RECT.collidepoint(event.pos)):
                    draggingToken = True
                    tokenx, tokeny = event.pos

            elif event.type == MOUSEMOTION and draggingToken:
                tokenx, tokeny = event.pos

            elif event.type == MOUSEBUTTONUP and draggingToken:
                if tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN and tokeny > 0 and tokeny < YMARGIN:
                    column = int((tokenx - XMARGIN) / TOKENSIZE)
                    if  isValidMove(board, column):
                        LowestBlankSpace = getLowestBlankSpace(board, column)
                        animateDroppingToken(board, column, draggedTokenColor)
                        board[LowestBlankSpace][column] = draggedTokenColor
                        drawBoard(board)
                        pygame.display.update()
                        return  
                draggingToken = False 
        if draggingToken:
            drawBoard(board, {"x": tokenx - TOKENSIZE / 2, "y": tokeny - TOKENSIZE / 2, "color": draggedTokenColor})
        else:
            drawBoard(board)
        pygame.display.update()
        CLOCK.tick(FPS)

main()