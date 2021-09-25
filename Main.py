import pygame as p
import Engine

p.init()
WIDTH = HEIGHT = 512
screenHW = 540
DIMENSION = 8
S_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
sideFont = p.font.Font("freesansbold.ttf", 20)
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bN', "bR", 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece + '.png'), (S_SIZE, S_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((screenHW, screenHW))

    clock = p.time.Clock()
    screen.fill(p.Color('White'))
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // S_SIZE
                    row = location[1] // S_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = [] 
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((S_SIZE, S_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * S_SIZE, r * S_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * S_SIZE, move.endRow * S_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    highlightSquares(screen, gs, validMoves, sqSelected)


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('brown')]  # (133, 94, 66)
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * S_SIZE, r * S_SIZE, S_SIZE, S_SIZE))
        x = 25
        label = ['A', 'B', "C", "D", "E", "F", "G", "H"]
        y = 475
        for row in label:
            screen.blit(sideFont.render(row, True, (0, 0, 0)), (x, 520))
            x += S_SIZE
        for col in range(1, 9):
            screen.blit(sideFont.render(str(col), True, (0, 0, 0)), (520, y))
            y -= S_SIZE


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c * S_SIZE, r * S_SIZE, S_SIZE, S_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * S_SIZE, move.endRow * S_SIZE, S_SIZE, S_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(int(c * S_SIZE), int(r * S_SIZE), int(S_SIZE), int(S_SIZE)))
        p.display.flip()
        clock.tick(60)

def drawText (screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0,int(WIDTH), int(HEIGHT)).move(int(WIDTH/2) - int(textObject.get_width()/2), int(HEIGHT/2) - int(textObject.get_height()/2))
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))
if __name__ == "__main__":
    main()
