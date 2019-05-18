import os
import datetime
import logging
import sys

from _game import GameOfLife
from _drawer import TableView, create_gif

BASE_PATH = os.getcwd()
TEMP_FOLDER = os.path.join(BASE_PATH, 'tmp')
TEMP_IMG_FILE_RULE = os.path.join(TEMP_FOLDER, '%d.png')
RESULT_FILENAME = f'result-{datetime.datetime.now().strftime("%d_%m_%y_%H_%M")}.gif'

GAME_TABLE_SIZE = 200
MAX_GEN_COUNT = 300

TABLE_VIEW_SIZE = 500
CELL_TABLE_VIEW_SIZE = 2.5

logging.basicConfig(
    format="%(levelname)s | %(module)s | %(asctime)s |  %(message)s",
    handlers=(logging.StreamHandler(sys.stdout),),
    level=logging.DEBUG
)


def main():
    prepare_environment_for_game()

    game = GameOfLife(GAME_TABLE_SIZE)
    view = TableView(TABLE_VIEW_SIZE, CELL_TABLE_VIEW_SIZE)

    view.save_img_table(game.table, get_name_for_tmp_file(-1))  # start

    gen_count = 0
    while gen_count < MAX_GEN_COUNT:
        game = next(game)
        view.save_img_table(game.table, get_name_for_tmp_file(gen_count))
        gen_count += 1

    create_gif([get_name_for_tmp_file(i) for i in range(-1, MAX_GEN_COUNT)], RESULT_FILENAME)

    clear_up_environment()


def prepare_environment_for_game():
    logging.debug("preparing environment")
    check_and_create_tmp_folder()


def check_and_create_tmp_folder():
    if not os.path.exists(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)


def clear_up_environment():
    logging.debug("clearing up environment")
    delete_tmp_folder()


def delete_tmp_folder():
    images_files = os.listdir(TEMP_FOLDER)

    for image_file in images_files:
        os.remove(os.path.join(TEMP_FOLDER, image_file))

    os.rmdir(TEMP_FOLDER)


def get_name_for_tmp_file(index: int):
    return TEMP_IMG_FILE_RULE % index


if __name__ == '__main__':
    logging.debug("starting new game of life generator with data: ")
    logging.debug("GAME_TABLE_SIZE | %d" % GAME_TABLE_SIZE)
    logging.debug("MAX_GEN_COUNT | %d" % MAX_GEN_COUNT)
    logging.debug("TABLE_VIEW_SIZE | %d" % TABLE_VIEW_SIZE)
    logging.debug("CELL_TABLE_VIEW_SIZE | %F" % CELL_TABLE_VIEW_SIZE)

    main()
