import os
import subprocess
import time
import webbrowser
from datetime import datetime

import click

from game import Match


@click.command()
@click.option('--size', default=90, help='Board size.')
@click.argument('bots', nargs=-1)
def main(size, bots):
    match = Match(bots, size)
    match.play()
    filename = os.path.join('matches',
                            datetime.strftime(datetime.utcnow(), '%Y%m%d_%H%M%S') + '.json')
    match.save(os.path.join('www', filename))
    proc = subprocess.Popen('python -m http.server --directory www', shell=True)
    webbrowser.open_new(f'http://localhost:8000?file={filename}')
    time.sleep(2.5)  # Marco's contribution
    proc.kill()


if __name__ == '__main__':
    main()
