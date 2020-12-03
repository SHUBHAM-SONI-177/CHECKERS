import pygame
from copy import deepcopy
import time

BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GREEN = (0,255,0)


class State:
	def __init__(self,win,piece):
		self.win = win
		self.turn = 0
		self.winner = -1
		self.piece = piece
		self.moves = {}

	def draw_pieces(self):
		for i in range(0,8):
			for j in range(0,8):
				if self.piece[i][j][0] == WHITE or self.piece[i][j][0] == RED:
					radius = 35
					x,y = 100*i + 50, 100*j + 50
					pygame.draw.circle(self.win, BLUE, (y, x), radius + 5)
					pygame.draw.circle(self.win, self.piece[i][j][0], (y,x), radius)
					if self.piece[i][j][1]:
						self.screen.blit(self.font.render('KING', True, (0,0,0)), (y, x))

				elif self.piece[i][j][0]== GREEN:
					pygame.draw.circle(self.win, WHITE, (j*100 + 50, i*100 + 50), 15)
				
	def make_all_correct(self):
		for i in range(0,8):
			for j in range(0,8):
				if self.piece[i][j][0]==GREEN:
					self.piece[i][j]=(BLACK,False)



	def update(self,row,col):
		if self.piece[row][col][0] == GREEN:
			self.piece[self.row][self.col],self.piece[row][col]=self.piece[row][col],self.piece[self.row][self.col]
			for pos in self.moves[(row,col)]:
				xx,yy = pos
				self.piece[xx][yy]=(BLACK,False)
			self.make_all_correct()
			self.draw_pieces()
			if iSwinner(self.piece,WHITE):
				self.winner=1
			self.turn = 1
			new_piece = minimax(self.piece,3,True)[1]
			self.piece = new_piece
			self.draw_pieces()
			time.sleep(1)
			self.turn = 0
			return
			
		if self.turn == 0:
			if self.piece[row][col][0] == RED:
				self.row = row
				self.col = col
				valid_pos = get_valid_pos(self.piece,row,col)
				#print(valid_pos)
				for pos in valid_pos:
					x,y = pos
					self.piece[x][y]=(GREEN,False)
					self.moves[(x,y)]=valid_pos[pos]
		self.draw_pieces()

def get_valid_pos(piece,row,col):
	moves = {}
	if piece[row][col][0] == WHITE or piece[row][col][1]:
		if(row+1<8 and col+1<8):
			if piece[row+1][col+1][0]==BLACK:
				moves[(row+1,col+1)]=[]
			elif piece[row+1][col+1][0]!=piece[row][col][0]:
				if row+2<8 and col+2<8 and piece[row+2][col+2][0]==BLACK:
					moves[(row+2,col+2)]=[(row+1,col+1)]
		if(row+1<8 and col-1>=0):
			if piece[row+1][col-1][0]==BLACK:
				moves[(row+1,col-1)]=[]
			elif piece[row+1][col-1][0]!=piece[row][col][0]:
				if row+2<8 and col-2>=0 and piece[row+2][col-2][0]==BLACK:
					moves[(row+2,col-2)]=[(row+1,col-1)]

	if piece[row][col][0] == RED or piece[row][col][1]:
		if(row-1>=0 and col+1<8):
			if piece[row-1][col+1][0]==BLACK:
				moves[(row-1,col+1)]=[]
			elif piece[row-1][col+1][0]!=piece[row][col][0]:
				if row-2>=0 and col+2<8 and piece[row-2][col+2][0]==BLACK:
					moves[(row-2,col+2)]=[(row-1,col+1)]
		if(row-1>=0 and col-1>=0):
			if piece[row-1][col-1][0]==BLACK:
				moves[(row-1,col-1)]=[]
			elif piece[row-1][col-1][0]!=piece[row][col][0]:
				if row-2>=0 and col-2>=0 and piece[row-2][col-2][0]==BLACK:
					moves[(row-2,col-2)]=[(row-1,col-1)]
	#print(moves)
	return moves


def draw_board(win):
	win.fill(BLACK)
	for i in range(0,8):
		for j in range(i%2,8,2):
			pygame.draw.rect(win, WHITE, (i*100, j*100, 100, 100))


def heuristic(piece):
	cost = 0
	for i in range(0,8):
		for j in range(0,8):
			if piece[i][j][0] == WHITE:
				if piece[i][j][1]:
					for move in get_valid_pos(piece,i,j):
						cost+=2
				else:
					for move in get_valid_pos(piece,i,j):
						cost+=1
			elif piece[i][j][0] == RED:
				if piece[i][j][1]:
					for move in get_valid_pos(piece,i,j):
						cost-=2
				else:
					for move in get_valid_pos(piece,i,j):
						cost-=1
	return cost

def iSwinner(piece,color):
	cost =0
	for i in range(0,8):
		for j in range(0,8):
			if piece[i][j][0] == color:
				if piece[i][j][1]:
					for move in get_valid_pos(piece,i,j):
						cost+=2
				else:
					for move in get_valid_pos(piece,i,j):
						cost+=1
	if cost==0:
		return True
	else:
		return False
	


def minimax(piece,depth,maxplayer):
	piece = deepcopy(piece)

	if depth == 0 or iSwinner(piece,RED):
		return heuristic(piece),piece

	if maxplayer:
		max_val = -1000000
		best_state = None
		for i in range(0,8):
			for j in range(0,8):
				if piece[i][j][0] == WHITE:
					valid_chance = get_valid_pos(piece,i,j)
					for move in valid_chance:
						x,y = move
						piece[x][y],piece[i][j]=piece[i][j],piece[x][y]
						for pos in valid_chance[move]:
							xx,yy = pos
							piece[xx][yy]=(BLACK,False)
						state = deepcopy(piece)
						temp = minimax(piece,depth-1, False)[0]
						piece[x][y],piece[i][j]=piece[i][j],piece[x][y]
						if max_val < temp:
							max_val = temp
							best_state = state
		return max_val, best_state

	else:
		min_val = 1000000
		best_state = None
		for i in range(0,8):
			for j in range(0,8):
				if piece[i][j][0] == RED:
					valid_chance = get_valid_pos(piece,i,j)
					for move in valid_chance:
						x,y = move
						piece[x][y],piece[i][j]=piece[i][j],piece[x][y]
						for pos in valid_chance[move]:
							xx,yy = pos
							piece[xx][yy]=(BLACK,False)
						state = deepcopy(piece)
						temp = minimax(piece,depth-1, True)[0]
						piece[x][y],piece[i][j]=piece[i][j],piece[x][y]
						if min_val > temp:
							min_val = temp
							best_state = state
		return min_val, best_state






def start_game():
	win = pygame.display.set_mode((800,800))
	pygame.display.set_caption('Checkers GUI')
	
	piece =[[(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False)],
		   [(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False)],
		   [(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False),(BLACK,False),(WHITE,False)],
		   [(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False)],
		   [(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False),(BLACK,False)],
		   [(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False)],
		   [(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False)],
		   [(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False),(RED,False),(BLACK,False)]]

	state = State(win,piece)
	#print(piece)
	while True:
		draw_board(win)
		state.draw_pieces()

		if state.winner != -1:
			font = pygame.font.Font('freesansbold.ttf', 32)
			if state.winner == 1:
				text = font.render('Artificial intelligence won', True, GREEN, BLUE)
				textRect = text.get_rect()
				textRect.center = (500, 500)
				display_surface.blit(text, textRect)
			else:
				text = font.render('You won', True, GREEN, BLUE)
				textRect = text.get_rect()
				textRect.center = (500, 500)
				display_surface.blit(text, textRect)

		continue_game = True
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				continue_game = False
				break
			if event.type == pygame.MOUSEBUTTONDOWN and state.turn == 0:
				x,y = pygame.mouse.get_pos()
				state.update(y//100,x//100)

		pygame.display.update()
		if not continue_game:
			pygame.quit()
			break


start_game()