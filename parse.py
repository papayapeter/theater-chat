import os
import json
import click


def error(s: str) -> None:
    print(s)
    raise SystemExit


@click.command()
@click.argument('input', nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.argument('output', nargs=1, type=click.Path(dir_okay=False))
def parse(input: str, output: str) -> None:
    # create output directory, if it doesn't exist yet
    if outdir := os.path.dirname(output):
        os.makedirs(outdir, exist_ok=True)

    # check if input is json or txt
    # json: parse for editing
    if os.path.splitext(input)[1] == '.json':
        # check if output is of right type
        if os.path.splitext(output)[1] != '.txt':
            error('output must be textfile if input is json')

        # read json and parse lines for textfile
        with open(input) as file:
            json_object = json.load(file)

        lines = [
            f'{element["roleName"]} {element["timestamp"]}> {element["message"]}\n'
            for element in json_object
        ]

        # write textfile
        with open(output, 'w') as file:
            file.writelines(lines)

    # txt: parse to json
    elif os.path.splitext(input)[1] == '.txt':
        # check if output is of right type
        if os.path.splitext(output)[1] != '.json':
            error('output must be json if input is textfile')

        # read textfile
        with open(input) as file:
            lines = file.readlines()

        json_object = [{
            'roleName': line.split(' ', 1)[0],
            'id': index,
            'message': line.split('> ', 1)[1].strip('\n')
        } for index, line in enumerate(lines)]

        # write json
        with open(output, 'w') as file:
            json.dump(json_object, file, indent=4)

    else:
        error('input must be either textfile or json')


if __name__ == '__main__':
    parse()