import sys
import numpy as np
import random
import pygame
import math
import random
import numpy as np
from util import flipCoin, Counter
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 4
COLUMN_COUNT = 5

EMPTY = 0

WINDOW_LENGTH = 4

def get_state(board):
	return tuple(map(tuple, board))

class Game():

	# Criar jogo
	def __init__(self):
		
		self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

		self.id1 = 1
		self.id2 = 2

		self.p1 = QLearnAgent(self, self.id1)
		self.p2 = MinMaxAgent(self, self.id2, self.id1)
		self.p3 = RandomAgent(self, self.id2)

	def reset_board(self):
		self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

	def place_piece(self, row, col, piece):
		self.board[row][col] = piece
	
	def is_valid(self, board, col):
		return board[ROW_COUNT-1][col] == 0
	
	def get_next_open_row(self, board, col):
		for r in range(ROW_COUNT):
			if board[r][col] == 0:
				return r
	
	def print_board(self):
		print(np.flip(self.board, 0))

	def get_valid_locations(self, board):
		valid_locations = []
		for col in range(COLUMN_COUNT):
			if self.is_valid(board, col):
				valid_locations.append(col)
		return valid_locations
	
	def get_board(self):
		return self.board
	
	def is_terminal(self, board):
		return self.winning_move(board, self.id1) or self.winning_move(board, self.id2) or len(self.get_valid_locations(board)) == 0

	def evaluate_window(self, window, piece):
		score = 0
		opp_piece = self.id2
		if piece == self.id2:
			opp_piece = self.id1

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
			score -= 4

		return score

	def score_position(self, board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(ROW_COUNT):
			row_array = [int(i) for i in list(board[r,:])]
			for c in range(COLUMN_COUNT-3):
				window = row_array[c:c+WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score Vertical
		for c in range(COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:,c])]
			for r in range(ROW_COUNT-3):
				window = col_array[r:r+WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score posiive sloped diagonal
		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		for r in range(ROW_COUNT-3):
			for c in range(COLUMN_COUNT-3):
				window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		return score


	def winning_move(self, board, piece):
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
					return True
				
	def draw_board(self, screen, SQUARESIZE, RADIUS, height):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
		
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):		
				if self.board[r][c] == self.id1:
					pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				elif self.board[r][c] == self.id2: 
					pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
		pygame.display.update()
		

	def run_q_vs_minmax(self, graphics=False, name="tab_final"):
		self.reset_board()
		game_over = False
		turn = random.randint(self.id1, self.id2)

		winner_id = -1

		episode_reward = 0

		if graphics:
			pygame.init()
			SQUARESIZE = 100

			width = COLUMN_COUNT * SQUARESIZE
			height = (ROW_COUNT+1) * SQUARESIZE

			size = (width, height)

			RADIUS = int(SQUARESIZE/2 - 5)

			screen = pygame.display.set_mode(size)
			self.draw_board(screen, SQUARESIZE, RADIUS, height)
			pygame.display.update()

			myfont = pygame.font.SysFont("monospace", 50)

		state = None
		next_state = None
		action = None


		while not game_over:
			reward = 0

			# Q-Learn
			if turn == self.id1:

				state = get_state(self.board) # Estado anterior da ação

				col = self.p1.choose_move(self.board)

				if self.is_valid(self.board, col):
					row = self.get_next_open_row(self.board, col)
					self.place_piece(row, col, self.id1)

					action = col # A coluna representa a ação

					if self.winning_move(self.board, self.id1):

						reward = 1  # Recompensa para vitória
						game_over = True
						winner_id = self.id1

						if graphics:
							label = myfont.render("Q-Learn wins!!", 1, RED)
							screen.blit(label, (20, 10))

						# Se vencer, atualizar com base nisso
						# state - anterior // action - col // next_state - estado após(0.0?) // 
						next_state = get_state(self.board) # Como esse estado nunca será atualizado, seu Q-Value é 0.0
						self.p1.process_move(state, action, next_state, reward)
						# Se não vencer, atualizar na iteração - 3 situações (se perdeu // se deu empate // se continua)

					if graphics:
						# self.print_board()
						self.draw_board(screen, SQUARESIZE, RADIUS, height)

					

					turn = self.id2

			# MinMax
			elif turn == self.id2:
				col = self.p2.choose_move()

				if self.is_valid(self.board, col):
					row = self.get_next_open_row(self.board, col)
					self.place_piece(row, col, self.id2)

					if self.winning_move(self.board, self.id2):
						reward = -2  # Penalidade para derrota do Q-Learn
						game_over = True
						winner_id = self.id2
						if graphics:
							label = myfont.render("MinMax wins!!", 1, YELLOW)
							screen.blit(label, (20, 10))

					if graphics:
						# self.print_board()
						self.draw_board(screen, SQUARESIZE, RADIUS, height)

					if state is not None:
						next_state = get_state(self.board)

				turn = self.id1


			if self.is_terminal(self.board):
				game_over = True
				if winner_id == -1:
					reward = -1  # Penalidade para empate
					next_state = get_state(self.board)

			if state is not None and next_state is not None:
				self.p1.process_move(state, action, next_state, reward)

			if game_over and graphics:

				# Salvar resultado da imagem
				file_name = f"{name}-w{winner_id}.jpg"
				pygame.image.save(screen, file_name)

				pygame.time.wait(2000)

			episode_reward += reward

		# print('Cheguei aqui')
		if graphics:
			self.print_board()
		return winner_id, episode_reward
	

	def run_q_vs_random(self, graphics=False, name="tab_final"):
		self.reset_board()
		game_over = False
		turn = 1

		winner_id = -1

		episode_reward = 0

		if graphics:
			pygame.init()
			SQUARESIZE = 100

			width = COLUMN_COUNT * SQUARESIZE
			height = (ROW_COUNT+1) * SQUARESIZE

			size = (width, height)

			RADIUS = int(SQUARESIZE/2 - 5)

			screen = pygame.display.set_mode(size)
			self.draw_board(screen, SQUARESIZE, RADIUS, height)
			pygame.display.update()

			myfont = pygame.font.SysFont("monospace", 50)

		state = None
		next_state = None
		action = None


		while not game_over:
			reward = 0

			# Q-Learn
			if turn == self.id1:

				state = get_state(self.board) # Estado anterior da ação
				col = self.p1.choose_move(self.board)


				if self.is_valid(self.board, col):
					row = self.get_next_open_row(self.board, col)
					self.place_piece(row, col, self.id1)

					action = col # A coluna representa a ação

					if self.winning_move(self.board, self.id1):

						reward = 1  # Recompensa para vitória
						game_over = True
						winner_id = self.id1

						if graphics:
							label = myfont.render("Q-Learn wins!!", 1, RED)
							screen.blit(label, (20, 10))

						# Se vencer, atualizar com base nisso
						# state - anterior // action - col // next_state - estado após(0.0?) // 
						next_state = get_state(self.board) # Como esse estado nunca será atualizado, seu Q-Value é 0.0
						self.p1.process_move(state, action, next_state, reward)
						# Se não vencer, atualizar na iteração - 3 situações (se perdeu // se deu empate // se continua)

					if graphics:
						# self.print_board()
						self.draw_board(screen, SQUARESIZE, RADIUS, height)

					turn = self.id2

			# Random
			elif turn == self.id2:
				col = self.p3.choose_move(self.board)

				if self.is_valid(self.board, col):
					row = self.get_next_open_row(self.board, col)
					self.place_piece(row, col, self.id2)

					if self.winning_move(self.board, self.id2):
						reward = -2  # Penalidade para derrota do Q-Learn
						game_over = True
						winner_id = self.id2
						if graphics:
							label = myfont.render("Random wins!!", 1, YELLOW)
							screen.blit(label, (20, 10))

					if graphics:
						# self.print_board()
						self.draw_board(screen, SQUARESIZE, RADIUS, height)

					if state is not None:
						next_state = get_state(self.board)

					turn = self.id1


			if self.is_terminal(self.board):
				game_over = True
				if winner_id == -1:
					reward = -1  # Penalidade para empate
					next_state = get_state(self.board)

			if state is not None and next_state is not None:
				self.p1.process_move(state, action, next_state, reward)

			if game_over and graphics:

				# Salvar resultado da imagem
				file_name = f"{name}-w{winner_id}.jpg"
				pygame.image.save(screen, file_name)

				pygame.time.wait(2000)

			episode_reward += reward

		# print('Cheguei aqui')
		if graphics:
			self.print_board()
		return winner_id, episode_reward
	

	def run_q_vs_human(self):
		graphics = True
		self.reset_board()
		game_over = False
		turn = 1

		winner_id = -1

		if graphics:
			pygame.init()
			SQUARESIZE = 100

			width = COLUMN_COUNT * SQUARESIZE
			height = (ROW_COUNT+1) * SQUARESIZE

			size = (width, height)

			RADIUS = int(SQUARESIZE/2 - 5)

			screen = pygame.display.set_mode(size)
			self.draw_board(screen, SQUARESIZE, RADIUS, height)
			pygame.display.update()

			myfont = pygame.font.SysFont("monospace", 50)

		state = None
		next_state = None
		action = None


		while not game_over:

			reward = 0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
					posx = event.pos[0]
					if turn == self.id2:
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

				pygame.display.update()


				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					#print(event.pos)
					# Ask for Player 1 Input
					if turn == self.id2:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if self.is_valid(self.board, col):
							row = self.get_next_open_row(self.board, col)
							self.place_piece(row, col, self.id2)

							if self.winning_move(self.board, self.id2):
								label = myfont.render("Human wins!!", 1, YELLOW)
								screen.blit(label, (20,10))
								reward = -5  # Penalidade para derrota do Q-Learn
								game_over = True
								winner_id = self.id2

							turn = self.id1

							# self.print_board()
							self.draw_board(screen, SQUARESIZE, RADIUS, height)

			# Q-Learn
			if turn == self.id1:

				state = get_state(self.board) # Estado anterior da ação
				col = self.p1.choose_move(self.board)


				if self.is_valid(self.board, col):
					row = self.get_next_open_row(self.board, col)
					self.place_piece(row, col, self.id1)

					action = col # A coluna representa a ação

					if self.winning_move(self.board, self.id1):

						reward = 2  # Recompensa para vitória
						game_over = True
						winner_id = self.id1

						if graphics:
							label = myfont.render("Q-Learn wins!!", 1, RED)
							screen.blit(label, (20, 10))

						# Se vencer, atualizar com base nisso
						# state - anterior // action - col // next_state - estado após(0.0?) // 
						next_state = get_state(self.board) # Como esse estado nunca será atualizado, seu Q-Value é 0.0
						self.p1.process_move(state, action, next_state, reward)
						# Se não vencer, atualizar na iteração - 3 situações (se perdeu // se deu empate // se continua)

					if graphics:
						self.print_board()
						self.draw_board(screen, SQUARESIZE, RADIUS, height)

					turn = self.id2

			if self.is_terminal(self.board):
				game_over = True
				if winner_id == -1:
					reward = -20  # Penalidade para empate
					next_state = get_state(self.board)

			if state is not None and next_state is not None:
				self.p1.process_move(state, action, next_state, reward)

			if game_over and graphics:
				pygame.time.wait(2000)

		# print('Cheguei aqui')
		self.print_board()
		return winner_id

			
	
###################################################################################################################
###################################################################################################################
###################################################################################################################

class Player():

	def __init__(self, game:Game, id):
		self.game = game
		self.id = int(id)

	def choose_move(self):
		pass

	def process_move(self):
		pass


""" UM STATE DO AGENTE REPRESENTA O MOMENTO APÓS O OPONENTE COLOCOU A PEÇA E DEVE O EFEITO QUE COLOCAR A PEÇA VAI FAZER """

class QLearnAgent(Player):
	
	def __init__(self, game, id, alpha=0.2, gamma=0.95, epsilon=0.1):

		super().__init__(game, id)

		self.alpha = float(alpha)
		self.gamma = float(gamma)
		self.epsilon = float(epsilon)

		self.q_table = Counter()

	def choose_move(self, board):

		state = get_state(board)

		actions = self.game.get_valid_locations(board)

		if flipCoin(self.epsilon):
			action = random.choice(actions)
		else:
			action = self.best_action(state)
		
		return action

	def process_move(self, state, action, nextState, reward):
		# Atualiza o valor de Q
		amostra = reward + self.gamma*self.getValue(nextState)
		newQVal = (1 - self.alpha) * self.getQValue(state, action) + self.alpha*amostra

		self.q_table[state, action] = newQVal

		# print("Atualizei")

	def best_action(self, state):
		maxValue = self.getValue(state)

		actions = self.game.get_valid_locations(self.game.board)

		for action in actions:
			if maxValue == self.getQValue(state, action):
				return action
			
	def getValue(self, state):

		actions = self.game.get_valid_locations(self.game.board)

		all_q_values = []
		# Para cada possivel acao do oponente
		for action in actions:
			all_q_values.append(self.getQValue(state, action))
			# Para cada acao a partir de um estado

		if len(all_q_values) > 0:
			return max(all_q_values)
	 
		return 0.0
	
	def getQValue(self, state, action):
		return self.q_table[(state, action)]
	
	def printQ(self):
		print(self.q_table)
	



class MinMaxAgent(Player):

	def __init__(self, game: Game, id, oppId):
		super().__init__(game, id)
		self.oppId = int(oppId)

	def choose_move(self):
		col, _ = self.minmax(self.game.board, 5, -math.inf, math.inf, True)
		
		return col

	def minmax(self, board, depth, alpha, beta, maximizingOpp):
		valid_locations = self.game.get_valid_locations(board)
		is_terminal = self.game.is_terminal(board)
		if depth==0 or is_terminal:
			if is_terminal:
				if self.game.winning_move(board, self.id):
					return (None, 100000000000000)
				elif self.game.winning_move(board, self.oppId):
					return (None, -10000000000000)
				else:
					return (None, 0)
			else:
				return (None, self.game.score_position(board, self.id))
		if maximizingOpp:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.game.get_next_open_row(board, col)
				b_copy = board.copy()
				b_copy[row][col] = self.id
				new_score = self.minmax(b_copy, depth-1, alpha, beta, False)[1]
				if new_score > value:
					value = new_score
					column = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value
		
		else:
			value = math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.game.get_next_open_row(board, col)
				b_copy = board.copy()
				b_copy[row][col] = self.oppId
				new_score = self.minmax(b_copy, depth-1, alpha, beta, True)[1]
				if new_score < value:
					value = new_score
					column = col
				beta = min(beta, value)
				if alpha >= beta:
					break

			return column, value
		


class RandomAgent(Player):

	def __init__(self, game: Game, id):
		super().__init__(game, id)

	def choose_move(self, board):
		
		# Pegar uma posição aleatória válida
		actions = self.game.get_valid_locations(board)
		action = random.choice(actions)

		return action