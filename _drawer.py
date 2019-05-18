import logging

from PIL import ImageDraw, Image, ImageColor
import imageio


class TableView:
    ACTIVE_COLOR = ImageColor.getrgb('#DC143C')
    DEAD_COLOR = ImageColor.getrgb('#FFFFFF')

    def __init__(self, size_table: int, size_cell: int):
        assert size_table * size_table % size_cell * size_cell == 0, ('Table size is square and cell size '
                                                                      'must contains it')
        self._size_cell = size_cell
        self.image = Image.new('RGB', (size_table, size_table), color='white')
        self.drawer = ImageDraw.Draw(self.image)

    def save_img_table(self, table, filename: str):

        for (count_row, row) in enumerate(range(len(table)), 1):
            for (count_col, col) in enumerate(range(len(table[row])), 1):

                if table[row][col] == 1:
                    color = self.ACTIVE_COLOR
                else:
                    color = self.DEAD_COLOR

                x_start = self._size_cell * (count_col - 1)
                y_start = self._size_cell * (count_row - 1)
                x_end = x_start + self._size_cell
                y_end = y_start + self._size_cell
                self.drawer.rectangle(((x_start, y_start), (x_end, y_end)), fill=color)

        logging.debug("saving new img %s " % filename)
        self.image.save(filename)
        self._clear_img()

    def _clear_img(self):
        self.image = Image.new('RGB', self.image.size, color='white')
        self.drawer = ImageDraw.Draw(self.image)


def create_gif(filenames_images: list, gif_filename: str):
    logging.debug("creating %s " % gif_filename)
    images = [imageio.imread(filename) for filename in filenames_images]
    imageio.mimsave(gif_filename, images)
