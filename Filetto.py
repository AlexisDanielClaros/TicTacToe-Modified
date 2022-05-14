import numpy as np
import pygame
import sys

pygame.init()
pygame.font.init()

print("How much players? (max 6 players)")
PLAYERS = int(input())
# RGB COLORS
DEFAULT_CIRCLE_COLOR = (255, 0, 0)
CIRCLE_COLOR = (255, 0, 0)
RED = 255
GREEN = 255
BLUE = 0
colorLine = (50, 100, 200)
BOARD_COLOR = (50, 150, 250)
# BUILD BOARD
width = 600
length = 600
board = pygame.display.set_mode((width, length))
pygame.display.set_caption("Filetto!")
board.fill(BOARD_COLOR)
build_board = PLAYERS * 2  # i need this for the creations of the board
if (build_board < 5):
    build_board = 5
boardRows = boardColumns = build_board
matrix = np.zeros((boardRows, boardColumns))
SQUARE_SIZE = width // boardColumns
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10


def boardLines(players):
    for i in range(1, players, 1):
        pygame.draw.line(board, colorLine, (10, width / build_board * i), (width - 10, width / build_board * i), 10)
        pygame.draw.line(board, colorLine, (length / build_board * i, 10), (length / build_board * i, length - 10), 10)


def mark_position(row, column, player):
    matrix[row][column] = player


def empty_position(row, column):
    return matrix[row][column] == 0


def score_points(player):
    score = 0
    for row in range(boardRows):
        for col in range(boardColumns):

            # HORIZONTAL SCORES
            if (col + 4 < boardColumns) and matrix[row][col] == player and matrix[row][col + 1] == player and \
                    matrix[row][col + 2] == player and matrix[row][col + 3] == player and matrix[row][
                col + 4] == player:
                score += 50
            elif (col + 3 < boardColumns) and matrix[row][col] == player and matrix[row][col + 1] == player and \
                    matrix[row][col + 2] == player and matrix[row][col + 3] == player:
                score += 10
            elif (col + 2 < boardColumns) and matrix[row][col] == player and matrix[row][col + 1] == player and \
                    matrix[row][col + 2] == player:
                score += 2

            # VERTICAL SCORES
            if (row + 4 < boardRows) and matrix[row][col] == player and matrix[row + 1][col] == player and \
                    matrix[row + 2][col] == player and matrix[row + 3][col] == player and matrix[row + 4][
                col] == player:
                score += 50
            elif (row + 3 < boardRows) and matrix[row][col] == player and matrix[row + 1][col] == player and \
                    matrix[row + 2][col] == player and matrix[row + 3][col] == player:
                score += 10
            elif (row + 2 < boardRows) and matrix[row][col] == player and matrix[row + 1][col] == player and \
                    matrix[row + 2][col] == player:
                score += 2

            # DESC DIAGONAL SCORES \
            if (row + 4 < boardRows and col + 4 < boardColumns) and matrix[row][col] == player and matrix[row + 1][
                col + 1] == player and matrix[row + 2][col + 2] == player and matrix[row + 3][col + 3] == player and \
                    matrix[row + 4][col + 4] == player:
                score += 50
            elif (row + 3 < boardRows and col + 3 < boardColumns) and matrix[row][col] == player and matrix[row + 1][
                col + 1] == player and matrix[row + 2][col + 2] == player and matrix[row + 3][col + 3] == player:
                score += 10
            elif (row + 2 < boardRows and col + 2 < boardColumns) and matrix[row][col] == player and matrix[row + 1][
                col + 1] == player and matrix[row + 2][col + 2] == player:
                score += 2

            # ASC DIAGON SCORES /
            if (row + 4 < boardRows and col - 4 >= 0) and matrix[row][col] == player and matrix[row + 1][
                col - 1] == player and matrix[row + 2][col - 2] == player and matrix[row + 3][col - 3] == player and \
                    matrix[row + 4][col - 4] == player:
                score += 50
            elif (row + 3 < boardRows and col - 3 >= 0) and matrix[row][col] == player and matrix[row + 1][
                col - 1] == player and matrix[row + 2][col - 2] == player and matrix[row + 3][col - 3] == player:
                score += 10
            elif (row + 2 < boardRows and col - 2 >= 0) and matrix[row][col] == player and matrix[row + 1][
                col - 1] == player and matrix[row + 2][col - 2] == player:
                score += 2
    # print("boardRows", boardRows, "  player", player)

    print("player", player, " score is ", score)
    if score >= 50:
        match_over(player)


def full_board():
    for row in range(boardRows):
        for col in range(boardColumns):
            if matrix[row][col] == 0:
                return False
    return True


def match_over(player):
    global GAME_OVER
    GAME_OVER = True
    player = str(player)
    myfont = pygame.font.SysFont('SUNRISE', width // 10, bold=True)
    font_reset = pygame.font.SysFont('Papyrus', width // 15, bold=True)
    reset_surface = font_reset.render("Press r to restart", True, (50, 250, 100), (0, 0, 200))
    text_surface = myfont.render("The winner is player " + player + "!!!", True, (50, 250, 100), (0, 0, 200))
    text_rect = text_surface.get_rect(center=(width / 2, length / 3))
    reset_rect = reset_surface.get_rect(center=(width / 2, length / 3 + 50))
    board.blit(text_surface, text_rect)
    board.blit(reset_surface, reset_rect)


def draw_circle(player):
    for row in range(boardRows):
        for col in range(boardColumns):
            if matrix[row][col] == player:
                pygame.draw.circle(board, CIRCLE_COLOR, (
                int(col * 2 * ((length / build_board) / 2) + (length / build_board) / 2),
                int(row * 2 * ((length / build_board) / 2) + (length / build_board) / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


def next_player_turn(player):
    global CIRCLE_COLOR
    global RED, GREEN, BLUE

    player = player % PLAYERS + 1
    # RESET TO PLAYER 1
    if player == 1:
        CIRCLE_COLOR = DEFAULT_CIRCLE_COLOR
        RED = 255
        GREEN = 255
        BLUE = 0
    else:  # NEXT PLAYER
        RED -= 50
        GREEN -= 50
        BLUE += 50
        CIRCLE_COLOR = (RED, GREEN, BLUE)
    return player


def restart(build_board):
    global GAME_OVER
    board.fill(BOARD_COLOR)
    boardLines(build_board)
    GAME_OVER = False
    for row in range(boardRows):
        for col in range(boardColumns):
            matrix[row][col] = 0
    print()
    print()


# MAIN
boardLines(build_board)
player = 1
GAME_OVER = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            row_clicked = int(mouseY // (length / build_board))
            col_clicked = int(mouseX // (length / build_board))

            if empty_position(row_clicked, col_clicked):
                mark_position(row_clicked, col_clicked, player)
                score_points(player)
                draw_circle(player)
                player = next_player_turn(player)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart(build_board)
                player = next_player_turn(PLAYERS)

    pygame.display.update()
