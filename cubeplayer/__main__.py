import signal
from argparse import ArgumentParser, Namespace

from cubeplayer.cli import duration_type
from cubeplayer.glut_backend import GlutWindow
from cubeplayer.renderer.label import Label
from cubeplayer.video_backend import VideoRenderer
from libcube.cli.cube_builder import init_cube_args_parser, build_cube
from libcube.cli.options import formula_type, integer_type


def backend_factory(args: Namespace):
    return GlutWindow if args.video_file is None else VideoRenderer


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    arg_parser = ArgumentParser()
    arg_parser.add_argument("formula", type=formula_type, default=[], nargs="?",
                            help="turns and rotations that will be animated")
    arg_parser.add_argument("--no-ui", action="store_false", dest="show_formula_ui",
                            help="hide the sequence of actions at the bottom of a screen")

    rendering_group = arg_parser.add_argument_group("rendering options")
    rendering_group.add_argument("--resolution", metavar="W H", nargs=2, default=[854, 480],
                                 help="resolution of a frame (width, height)", type=integer_type(1))
    rendering_group.add_argument("--msaa", type=integer_type(0), default=0, metavar="N_SAMPLES",
                                 help="number of samples for multisample antialiasing (MSAA)")

    init_cube_args_parser(arg_parser)
    VideoRenderer.init_args_parser(arg_parser)

    timing_group = arg_parser.add_argument_group("timing options")
    timing_group.add_argument("--time-before", metavar="MS", type=duration_type, default=0.15,
                              help="delay before starting an animation", dest="time_before")
    timing_group.add_argument("--time-after", metavar="MS", type=duration_type, default=0.5,
                              help="delay after the end of the last animation", dest="time_after")
    timing_group.add_argument("--time-turn", metavar="MS", type=duration_type,
                              help="duration of a turn animation", dest="time_turn1")
    timing_group.add_argument("--time-turn2", metavar="MS", type=duration_type,
                              help="duration of a double turn animation", dest="time_turn2")
    timing_group.add_argument("--time-rotate", metavar="MS", type=duration_type,
                              help="duration of a 90 degrees rotation animation", dest="time_rotation1")
    timing_group.add_argument("--time-rotate2", metavar="MS", type=duration_type,
                              help="duration of a 180 degrees rotation animation", dest="time_rotation2")
    Label.init_arg_parser(arg_parser)
    args = arg_parser.parse_args()

    cube, orientation = build_cube(args)
    if args.show_formula_ui:
        formula_string = list(map(str, args.formula))
    else:
        formula_string = []
    renderer = backend_factory(args)(cube, orientation, args, formula_string, arg_parser)
    renderer.run()


if __name__ == "__main__":
    main()
