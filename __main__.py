import click

from game import Match


@click.command()
@click.option('--rows', default=10, help='Number of rows.')
@click.option('--cols', default=10, help='Number of columns.')
# @click.option('-b', '--bot', required=True, multiple=True, help=('Folder bot name.'))
@click.argument('bots', nargs=-1)
def main(rows, cols, bots):
    match = Match(bots, rows, cols)
    match.play()


if __name__ == '__main__':
    main()
