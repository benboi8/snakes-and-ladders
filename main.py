import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


playerColors = {
	"0": "Red",
	"1": "Light Blue",
	"2": "Green",
	"3": "Yellow",
}


class Board:
	player = 0

	player_label = Label((0, 0, 250, 150), (lightBlack, darkWhite), text=f"It is {playerColors['0']}'s turn", textData={"alignText": "top"})

	rect = [width // 2 - 70 * 5, height // 2 - 70 * 5, 70, 70]
	board = []
	y = 0
	x = 0
	for i in range(1, 101):
		if y // rect[3] % 2 == 0:
			txt = str(101 - i)
		else:
			match x // rect[2]:
				case 0:
					a = 9
				case 1:
					a = 7
				case 2:
					a = 5
				case 3:
					a = 3
				case 4:
					a = 1
				case 5:
					a = -1
				case 6:
					a = -3
				case 7:
					a = -5
				case 8:
					a = -7
				case 9:
					a = -9

			txt = str(101 - a - i) 

		board.append((
			Box((rect[0] + x, rect[1] + y, rect[2], rect[3]), (lightBlack, darkWhite),  lists=[]),
			Label((rect[0] + x - rect[2] // 2 + 15, rect[1] + y - rect[3] // 2 + 15, rect[2], rect[3]), (lightBlack, darkWhite), text=txt, drawData={"drawBorder":False, "drawBackground":False}, textData={"fontSize": 16}, lists=[])
			))
		
		x += rect[2]
		if i % 10 == 0:
			y += rect[3]
			x = 0


	# len(board) - 1 - desired board square = index
	#           4  14    9  31    20  38    28  84    40  59    51  67    63  81    71  91
	ladders = [(6, 13), (1, 30), (19, 37), (22, 86), (39, 58), (50, 63), (67, 89), (70, 90)]
	#          17  7    62  19    87  24    54  34    64  60    93  73    95  75    99  78
	snakes = [(16, 3), (68, 18), (83, 26), (53, 33), (66, 59), (92, 72), (94, 74), (98, 77)]

	def Draw():
		w = 5

		for cell in Board.board:
			cell[0].Draw()

		for ladder in Board.ladders:
			start = Board.board[len(Board.board) - 1 - ladder[0]][0].rect
			end = Board.board[len(Board.board) - 1 - ladder[1]][0].rect
			pg.draw.line(screen, green.ChangeBrightness(80), (start.x + start.w // 2, start.y + start.h // 2), (end.x + end.w // 2, end.y + end.h // 2), w)

		for snake in Board.snakes:
			start = Board.board[len(Board.board) - 1 - snake[0]][0].rect
			end = Board.board[len(Board.board) - 1 - snake[1]][0].rect
			pg.draw.line(screen, red.ChangeBrightness(80), (start.x + start.w // 2, start.y + start.h // 2), (end.x + end.w // 2, end.y + end.h // 2), w)

		for cell in Board.board:
			cell[1].Draw()

	def RollDice():
		r = randint(3, 3)
		if Board.player + 1 > 3:
			nextPlayer = playerColors['0']
		else:
			nextPlayer = playerColors[str(Board.player + 1)]

		Board.player_label.UpdateText(f"{playerColors[str(Board.player)]} rolled a {r}\n\nIt is now {nextPlayer}'s\nturn")
		
		player = Player.allPlayers[Board.player]
		for i in range(r):

			player.Step()
			
			DrawLoop()
			t.sleep(0.2)

		for ladder in Board.ladders:
			if Board.board[len(Board.board) - 1 - ladder[0]][0].rect.colliderect(player.rect):
				player.MoveTo(Board.board[len(Board.board) - 1 - ladder[1]][0].rect)
				break

		for snake in Board.snakes:
			if Board.board[len(Board.board) - 1 - snake[0]][0].rect.colliderect(player.rect):
				player.MoveTo(Board.board[len(Board.board) - 1 - snake[1]][0].rect)
				break

		if Board.player + 1 > 3:
			Board.player = 0
		else:
			Board.player += 1

		pg.event.clear()



class Player(Box):
	allPlayers = []

	def __init__(self, color, i):

		self._id = i

		rect = (Board.rect[0] + (16 * i) + 3, Board.rect[1] + Board.rect[2] * 10 - 37, 14, 34)

		super().__init__(rect, (color, color))

		self.reverseX = False
		self.changeY = False
		self.mult = 1
		self.won = False

		Player.allPlayers.append(self)

	def Step(self):
		if not self.won:
			if self.changeY:
				self.rect.y -= Board.rect[3]
				self.changeY = False
			else:
				self.rect.x += Board.rect[2] * self.mult

				if self.rect.x // Board.rect[2] - 4 in (9, 0):
					self.mult *= -1
					self.changeY = True

		if self.rect.colliderect(Board.rect):
			self.won = True

	def MoveTo(self, rect):
		self.rect.x = rect.x + 3 + (self.rect.w * self._id + 1 * self._id)
		self.rect.y = rect.y + (Board.rect[3] - 37)
		
		if self.rect.y // Board.rect[3] % 2 == 0:
			self.mult = -1
		else:
			self.mult = 1



def DrawLoop():
	screen.fill(darkGray)

	Board.Draw()

	DrawAllGUIObjects()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	if event.type == pg.KEYDOWN:
		if event.key == pg.K_SPACE:
			Board.RollDice()


Player(red, 0)
Player(lightBlue, 1)
Player(green, 2)
Player(yellow, 3)

while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	DrawLoop()
