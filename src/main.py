import config
import window
from data import Data

if __name__ == '__main__':
    config.current_theme = config.get_dark_theme()
    Data.load()
    main = window.MainWindow((512, 360))
