import signal
from argparse import ArgumentParser

from cubeplayer.glut_backend import GlutWindow
from libcube.parser import get_action_representation
from libcube.cli.cube_builder import init_cube_args_parser, build_cube
from libcube.cli.options import formula_type


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    arg_parser = ArgumentParser()
    arg_parser.add_argument("formula", type=formula_type, default=[])
    init_cube_args_parser(arg_parser)
    args = arg_parser.parse_args()

    cube, orientation = build_cube(args)

    window = GlutWindow(cube, orientation,
                        list(map(get_action_representation, args.formula)))
    for action in args.formula:
        window.cube_animator.enqueue(action)
    window.run()


if __name__ == "__main__":
    main()
