import sys, random

try:
    import bext
except ImportError:
    print('This program requires the bext module, which')
    print('can be installed with "pip install bext".')
    sys.exit()
# Setup the constants
MIN_X_INCREASE = 6
MAX_X_INCREASE = 16
MIN_Y_INCREASE = 3
MAX_Y_INCREASE = 6
WHITE = 'white'
BLACK = 'black'
RED = 'red'
YELLOW = 'yellow'
BLUE = 'blue'

# Setup the screen
width, height = bext.size()
# maybe need this correction?
width -= 1
height -= 3

while True:
    # 1. Prepopulate canvas with blank spaces
    canvas = {}
    for x in range(width):
        for y in range(height):
            canvas[(x,y)] = WHITE
    # 2. Generate verticle lines
    numberOfSegmentsToDelete = 0
    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    while x < width - MIN_X_INCREASE:
        numberOfSegmentsToDelete += 1
        for y in range(height):
            canvas[(x,y)] = BLACK
        x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    # 2. Generate horizontal lines
    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    while y < height - MIN_Y_INCREASE:
        numberOfSegmentsToDelete += 1
        for x in range(width):
            canvas[(x,y)] = BLACK
        y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    numberOfRectanglesToPaint = numberOfSegmentsToDelete - 3
    numberOfSegmentsToDelete = int(numberOfSegmentsToDelete * 1.5)

    # 3. Randomly select points and try to remove them
    for i in range(numberOfSegmentsToDelete):
        while True:
            # Get random start point on an existing segment
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)
            if canvas[(startx, starty)] == WHITE:
                continue
            # Find out if we are on vertical or horizontal segment
            if (canvas[(startx-1, starty)] == WHITE and canvas[(startx + 1, starty)] == WHITE):
                orientation = 'vertical'
            elif (canvas[(startx, starty-1)] == WHITE and canvas[(startx, starty+1)] == WHITE):
                orientation = 'horizontal'
            else:
                # The start point is at an intersection, resample
                continue
            
            pointsToDelete = [(startx, starty)]
            canDeleteSegment = True
            if orientation == 'vertical':
                # Go up one path from the start point and see if we can remove this segment
                for changey in (-1, 1):
                    y = starty
                    while 0 < y < height - 1:
                        y += changey
                        if (canvas[(startx - 1, y)] == BLACK and canvas[(startx + 1, y)] == BLACK):
                            # We found a 4 way intersection
                            break
                        elif ((canvas[(startx - 1, y)] == WHITE and canvas[(startx + 1, y)] == BLACK) or (canvas[(startx - 1, y)] == BLACK and canvas[(startx + 1, y)] == WHITE)):
                            # We found a T-intersection, we cant delete this
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((startx, y))
            elif orientation == 'horizontal':
                # Go side to side one path from start point and see if we can delete
                for changex in (-1, 1):
                    x = startx
                    while 0 < x < width - 1:
                        x += changex
                        if (canvas[(x, starty - 1)] == BLACK and canvas[(x, starty + 1)] == BLACK):
                            # 4 way intersection
                            break
                        elif ((canvas[(x, starty - 1)] == WHITE and canvas[(x, starty + 1)] == BLACK) or (canvas[(x, starty - 1)] == BLACK and canvas[(x, starty + 1)] == WHITE)):
                            # We found T-intersection, cant delete
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((x, starty))
            if not canDeleteSegment:
                continue # Get new random point
            break
        # If we can delete this segment, set all points to WHITE
        for x, y in pointsToDelete:
            canvas[(x, y)] = WHITE
    
    # 4. Add border lines
    # for x in range(width):
    #     canvas[(x, 0)] = BLACK # top
    #     canvas[(x, height - 1)] = BLACK # bottom
    # for y in range(height):
    #     canvas[(0, y)] = BLACK # left
    #     canvas[(width - 1, y)] # right
    
    # 5. Paint the rectangles
    for i in range(numberOfRectanglesToPaint):
        while True:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)

            if canvas[(startx, starty)] != WHITE:
                continue
            else:
                break
        # Floodfill algorithm
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([(startx, starty)])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            canvas[(x, y)] = colorToPaint
            try:
                if canvas[(x - 1, y)] == WHITE:
                    pointsToPaint.add((x - 1, y))
                if canvas[(x + 1, y)] == WHITE:
                    pointsToPaint.add((x + 1, y))
                if canvas[(x, y - 1)] == WHITE:
                    pointsToPaint.add((x, y - 1))
                if canvas[(x, y + 1)] == WHITE:
                    pointsToPaint.add((x, y + 1))
            except:
                pass
    # 1. Draw the canvas
    # for y in range(height):
    #     for x in range(width):
    #         bext.bg(canvas[(x,y)])
    #         print(' ', end='')
    #     print()
    print('\n')
    for x in range(width):
        for y in range(height):
            bext.bg(canvas[(x,y)])
            print(' ', end='')
            print('\n')
    
    # 1. Prompt user to create new one
        try:
            input('Press ENTER for another work of art, or Crtl-C to quit.')
        except KeyboardInterrupt:
            sys.exit()