import copy
import keras
import numpy as np
from StaSmy.data_preprocess import get_data
from timeit import default_timer as timer

model = keras.models.load_model('StaSmy/model/sudoku.model')


def norm(a):
    return (a / 9) - .5


def denorm(a):
    return (a + .5) * 9


def inference_sudoku(sample):
    # This function solve the sudoku by filling blank positions one by one.

    feat = copy.copy(sample)
    while True:
        out = model.predict(feat.reshape((1, 9, 9, 1)), verbose=0)
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9, 9)) + 1
        prob = np.around(np.max(out, axis=1).reshape((9, 9)), 2)

        feat = denorm(feat).reshape((9, 9))
        mask = (feat == 0)

        if mask.sum() == 0:
            break

        prob_new = prob * mask

        ind = np.argmax(prob_new)
        x, y = (ind // 9), (ind % 9)

        val = pred[x][y]
        feat[x][y] = val
        feat = norm(feat)

    return pred


# testing own game
def solve_sudoku(game):
    game = game.replace('\n', '')
    game = game.replace(' ', '')
    game = np.array([int(j) for j in game]).reshape((9, 9, 1))
    game = norm(game)
    game = inference_sudoku(game)
    return game


def solve_sudoku_from_npArray(game):
    game.reshape((9, 9, 1))
    game = norm(game)
    game = inference_sudoku(game)
    return game


def test_one():
    game = '''
              0 8 0 0 3 2 0 0 1
              7 0 3 0 8 0 0 0 2
              5 0 0 0 0 7 0 3 0
              0 5 0 0 0 1 9 7 0
              6 0 0 7 0 9 0 0 8
              0 4 7 2 0 0 0 5 0
              0 2 0 6 0 0 0 0 9
              8 0 0 0 9 0 3 0 5
              3 0 0 8 2 0 0 1 0
          '''

    start = timer()
    game = solve_sudoku(game)
    end = timer()

    print('solved puzzle:\n')
    print(game)
    print("columns sums")
    print(np.sum(game, axis=1))
    print("time: ", end - start)
