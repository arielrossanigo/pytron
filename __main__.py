import os
from datetime import datetime

import click

from game import Match


@click.command()
@click.option('--size', default=10, help='Board size.')
@click.argument('bots', nargs=-1)
def main(size, bots):
    match = Match(bots, size)
    match.play()
    filename = datetime.strftime(datetime.utcnow(), '%Y%m%d_%H%M%S') + '.json'
    match.save(os.path.join('www', 'matches', filename))
    print(f"Visit http://localhost:8000?file={filename}")

if __name__ == '__main__':
    main()
