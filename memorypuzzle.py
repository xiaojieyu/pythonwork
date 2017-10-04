import random, pygame, sys
from pygame.locals import *

FPS = 3
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 2
BOARDHEIGHT =3

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have event number\
    of oxes for pairs of matches.'

XMARGIN = int((WINDOWWIDTH-(BOARDWIDTH * (BOXSIZE + GAPSIZE)))/2)
YMARGIN = int((WINDOWHEIGHT-(BOARDHEIGHT * (BOXSIZE + GAPSIZE)))/2)

GRAY =    (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE =   (255, 255, 255)
RED =     (255,   0,   0)
GREEN =   (  0, 255,   0)
BLUE =    (  0,   0, 255)
YELLOW =  (255, 255,   0)
ORANGE =  (255, 128,   0)
PURPLE =  (255,   0, 255)
CYAN =    (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board\
is too big for the number of shapes/colors defined.'

def leftTopCoordsOfBox(boxx, boxy):
  # Convert board coordinates to pixel coordinates
  left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
  top  = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
  return (left, top)

def drawIcon(shape, color, boxx, boxy):
  quarter = int(BOXSIZE * 0.25)
  half = int(BOXSIZE * 0.5)

  left, top = leftTopCoordsOfBox(boxx, boxy)

  # Draw the shapes
  if shape == DONUT:
    pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
    pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
  elif shape == SQUARE:
    pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter,
                                          BOXSIZE - half, BOXSIZE - half))
  elif shape == DIAMOND:
    pygame.draw.polygon(DISPLAYSURF, color,
                        ((left + half, top), (left + BOXSIZE - 1, top + half),
                         (left + half, top + BOXSIZE - 1), (left, top + half)))
  elif shape == LINES:
    for i in range(0, BOXSIZE, 4):
      pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
      pygame.draw.line(DISPLAYSURF, color,
                       (left + i, top + BOXSIZE - 1),
                       (left + BOXSIZE - 1, top +i))
  elif shape == OVAL:
    pygame.draw.ellipse(DISPLAYSURF, color,
                        (left, top + quarter, BOXSIZE, half))


def getRandomizedBoard():
  # Get a list of every possible shape in every possible color
  icons = []
  for color in ALLCOLORS:
    for shape in ALLSHAPES:
      icons.append((shape, color))

  random.shuffle(icons) # randomize the order of the icons list
  numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
  icons = icons[:numIconsUsed] * 2
  random.shuffle(icons)

  # create the baord data structure, with randomly placed icons.
  board = []
  for x in range(BOARDWIDTH):
    column = []
    for y in range(BOARDHEIGHT):
      column.append(icons[0])
      del icons[0]
    board.append(column)
  return board

def generateRevealedBoxesData(val):
  revealedBoxes = []
  for i in range(BOARDWIDTH):
    revealedBoxes.append([val] * BOARDHEIGHT)
  return revealedBoxes

def drawBoxCovers(board, boxes, coverage):
  # draw boxes being covered/revealed. "boxes" is a list
  # of two-item lists, which have the x &  spot of the box.
  for box in boxes:
    left, top = leftTopCoordsOfBox(box[0], box[1])
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
    shape, color = getShapeAndColor(board, box[0], box[1])
    drawIcon(shape, color, box[0], box[1])
    if coverage > 0:
      pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
  pygame.display.update()
  FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
  # Do the "box reveal" animation
  for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
    drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
  # Do the "box reveal" animation
  for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
    drawBoxCovers(board, boxesToCover, coverage)

def startGameAnimation(board):
  # Randomly reveal the boxes 8 at a time
  coveredBoxes = generateRevealedBoxesData(False)
  boxes = []
  for x in range(BOARDWIDTH):
    for y in range(BOARDHEIGHT):
      boxes.append((x, y))
  random.shuffle(boxes)
  boxGroups = splitIntoGroupsOf(8, boxes)

  drawBoard(board, coveredBoxes)
  for boxGroup in boxGroups:
    revealBoxesAnimation(board, boxGroup)
    coverBoxesAnimation(board, boxGroup)

def getShapeAndColor(board, boxx, boxy):
  # shape value for x, y spot is stored in board[x][y][0]
  # color value for x, y spot is stored in board[x][y][1]
  return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoard(board, revealed):
  # draws all of the boxes in their covered or revealed state.
  for boxx in range(BOARDWIDTH):
    for boxy in range(BOARDHEIGHT):
      left, top = leftTopCoordsOfBox(boxx, boxy)
      if not revealed[boxx][boxy]:
        # draw a covered box.
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
      else:
        # draw the (revealed) icon.
        shape, color = getShapeAndColor(board, boxx, boxy)
        drawIcon(shape, color, boxx, boxy)

def splitIntoGroupsOf(groupSize, theList):
  # splits a list into a list of lists, where the inner lists have at
  # most groupSize number of items.
  result = []
  for i in range(0, len(theList), groupSize):
    result.append(theList[i : i + groupSize])
  return result

def getBoxAtPixel(x, y):
  for boxx in range(BOARDWIDTH):
    for boxy in range(BOARDHEIGHT):
      left, top = leftTopCoordsOfBox(boxx, boxy)
      boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
      if boxRect.collidepoint(x, y):
        return (boxx, boxy)
  return (None, None)

def drawHighlightBox(boxx, boxy):
  left, top = leftTopCoordsOfBox(boxx, boxy)
  pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                   (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def hasWon(revealedBoxes):
  # Returns True if all the boxes have been revealed, otherwise False
  for i in revealedBoxes:
    if False in i:
      return False
  return True

def gameWonAnimation(board):
  # flash the background color when the player has won
  coveredBoxes = generateRevealedBoxesData(True)
  color1 = LIGHTBGCOLOR
  color2 = BGCOLOR

  for i in range(13):
    color1, color2 = color2, color1
    DISPLAYSURF.fill(color1)
    drawBoard(board, coveredBoxes)
    pygame.display.update()
    pygame.time.wait(300)

def main():
  global FPSCLOCK, DISPLAYSURF
  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

  mousex = 0
  mousey = 0
  pygame.display.set_caption('Memory Game')

  mainBoard = getRandomizedBoard()
  revealedBoxes = generateRevealedBoxesData(False)
  DISPLAYSURF.fill(BGCOLOR)

  firstSelection = None

  while True:
    mouseClicked = False
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard, revealedBoxes)

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEMOTION:
        mousex, mousey = event.pos
      elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        mouseClicked = True

    boxx, boxy = getBoxAtPixel(mousex, mousey)
    if boxx != None and boxy != None:
      print("box:", boxx, boxy)
      print ("first:", firstSelection)
      if not revealedBoxes[boxx][boxy]:
        drawHighlightBox(boxx, boxy)
      if not revealedBoxes[boxx][boxy] and mouseClicked:
        revealBoxesAnimation(mainBoard, [(boxx, boxy)])
        revealedBoxes[boxx][boxy] = True # set the box as "revealed"
        if firstSelection == None: # the current box was the first box clicked
          firstSelection = (boxx, boxy)
          print (firstSelection)
        else: # the current box was the second box clicked
              # check if there is a match between two icons
          icon1shape, icon1color = getShapeAndColor(mainBoard,
                                                    firstSelection[0],
                                                    firstSelection[1])
          icon2shape, icon2color = getShapeAndColor(mainBoard,
                                                    boxx,
                                                    boxy)

          if icon1shape != icon2shape or icon1color != icon2color:
            # Icons don't match. Re-cover up both selections.
            pygame.time.wait(1000)
            coverBoxesAnimation(mainBoard, [(firstSelection[0],
                                             firstSelection[1]),
                                            (boxx, boxy)])
            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
            revealedBoxes[boxx][boxy] = False
          elif hasWon(revealedBoxes): # check if all pairs found
            gameWonAnimation(mainBoard)
            pygame.time.wait(2000)

            #reset the board
            mainBoard = getRandomizedBoard()
            revealedBoxes = generateRevealedBoxesData(False)

            # show the fully unrevealed board for a second.
            drawBoard(mainBoard, revealedBoxes)
            pygame.display.update()
            pygame.time.wait(1000)

            startGameAnimation(mainBoard)

          firstSelection = None

    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
  main()
