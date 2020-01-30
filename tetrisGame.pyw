import pygame, random, sys
colours = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 150, 0),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0,   255)
    ]
config = {
    "maxfps":60,
    "rows":22,
    "columns":10,
    "cellsize":20,
    "delay":250
    }
tetrominoes = {
    "O":[
        [1, 1],
        [1, 1]
        ],
    "I":[
        [2, 2, 2, 2]
        ],
    "J":[
        [0, 3],
        [0, 3],
        [3, 3]
        ],
    "L":[
        [4, 0],
        [4, 0],
        [4, 4]
        ],
    "S":[
        [5, 0],
        [5, 5],
        [0, 5]
        ],
    "Z":[
        [0, 6],
        [6, 6],
        [6, 0]
        ],
    "T":[
        [7, 0],
        [7, 7],
        [7, 0]
        ]
    }

def joinMatrices(mat1, mat2, offset):
    for m1y, m1row in enumerate(mat1):
        for m1x, m1column in enumerate(m1row):
            if m1column != 0:
                mat2[offset[1] + m1y][offset[0] + m1x] = m1column
    return mat2
def rotMat(mat, clockwise = False):
    tempMat = [[0 for _ in range(len(mat))] for _ in range(len(mat[0]))]
    newMat = tempMat
    for y, row in enumerate(mat):
        for x, column in enumerate(row):
            tempMat[x][y] = mat[y][x]
    
    if clockwise:
        for y, row in enumerate(tempMat):
            t = tempMat[y][0]
            u = tempMat[y][-1]
            newMat[y][0] = u
            newMat[y][-1] = t
    else:
        t = tempMat[0]
        y = tempMat[-1]
        newMat = tempMat
        newMat[0] = y
        newMat[-1] = t
    return newMat
def checkCollision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False
def TetrisGame():
    pygame.init()
    score = 0
    lastClear = 0
    font = pygame.font.Font('freesansbold.ttf', 12)
    DISPLAYSURF = pygame.display.set_mode((config["columns"] * config["cellsize"], config["rows"] * config["cellsize"]))
    pygame.display.set_caption("Tetris")
    board = [[0 for _ in range(config["columns"])] for _ in range(config["rows"])]
    clock = pygame.time.Clock()
    tetromino = random.choice(["S", "Z", "O", "I", "J", "L", "T"])
    tetromino = tetrominoes[tetromino]
    last = pygame.time.get_ticks()
    offset = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tetromino = rotMat(tetromino, 1)
                    if checkCollision(board, tetromino, offset):
                        tetromino = rotMat(tetromino)
                if event.key == pygame.K_LEFT:
                    tetromino = rotMat(tetromino)
                    if checkCollision(board, tetromino, offset):
                        tetromino = rotMat(tetromino, 1)
                if event.key == pygame.K_a:
                    offset[0] -= 1
                    if offset[0] < 0:
                        offset[0] = 0
                    if checkCollision(board, tetromino, offset):
                        offset[0] += 1
                if event.key == pygame.K_d:
                    offset[0] += 1
                    if offset[0] > len(board[0]) - len(tetromino[0]):
                        offset[0] = len(board[0]) - len(tetromino[0])
                    if checkCollision(board, tetromino, offset):
                        offset[0] -= 1
        now = pygame.time.get_ticks()
        if now - last > config["delay"]:
            last = now
            offset[1] += 1
            if checkCollision(board, tetromino, offset):
                offset[1] -= 1
                board = joinMatrices(tetromino, board, offset)
                tetromino = random.choice(["S", "Z", "O", "I", "J", "L", "T"])
                tetromino = tetrominoes[tetromino]
                offset = [0, 0]
        for y, row in enumerate(board):
            for x, column in enumerate(row):
                pygame.draw.rect(DISPLAYSURF, colours[column], (x * config["cellsize"], y * config["cellsize"], config["cellsize"], config["cellsize"]))
        for y, row in enumerate(tetromino):
            for x, column in enumerate(row):
                if column != 0 and (offset[1] + y >= 2):
                    pygame.draw.rect(DISPLAYSURF, colours[column], ((x + offset[0]) * config["cellsize"], (y + offset[1]) * config["cellsize"], config["cellsize"], config["cellsize"]))
        cleared = 0
        for y, row in enumerate(board):
            full = True
            for each in row:
                if not each:
                    full = False
            if full:
                del board[y]
                board.insert(0, [0 for _ in range(config["columns"])])
                cleared += 1
        if cleared == 1:
            score += 100
        elif cleared == 2:
            score += 250
        elif cleared == 3:
            score += 500
        elif cleared == 4:
            if lastClear == 4:
                score += 2000
            else:
                score += 1000
        if cleared != 0:
            lastClear = cleared
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (0, 0, config["cellsize"] * config["columns"], config["cellsize"] * 2))
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (0, 2 * config["cellsize"]), (config["cellsize"] * config["columns"], config["cellsize"] * 2))
        
        clock.tick(config["maxfps"])
        sText = font.render("Score: " + str(score), False, (255, 255, 255))
        sRect = sText.get_rect()
        DISPLAYSURF.blit(sText, (10, 10, 30, 30))
        pygame.display.update()
        dead = False
        for each in board[0]:
            if each:
                dead = True
        if dead:
            break
    sText = font.render("Score: " + str(score), False, (255, 255, 255))
    sRect = sText.get_rect()
    sRect.center = (config["columns"] * config["cellsize"] // 2, config["rows"] * config["cellsize"] // 2)
    DISPLAYSURF.blit(sText, (sRect))
    pygame.display.update()
        
TetrisGame()
