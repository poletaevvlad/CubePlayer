import signal
from argparse import ArgumentParser, Namespace
import math

from cubeplayer.cli import duration_type
from cubeplayer.glut_backend import GlutWindow
from cubeplayer.renderer.label import Label
from cubeplayer.video_backend import VideoRenderer
from cubeplayer import colors
from cubelang.cli.cube_builder import init_cube_args_parser, build_cube
from cubelang.cli.options import formula_type, integer_type
from cubeplayer.renderer.scene import Scene


def backend_factory(args: Namespace):
    return GlutWindow if args.video_file is None else VideoRenderer


def create_scene(args: Namespace, arg_parser: ArgumentParser):
    cube, orientation = build_cube(args)

    return Scene(cube,
                 args.scale, [x / 180.0 * math.pi for x in args.camera_angle],
                 list(map(str, args.formula)) if args.show_formula_ui else [],
                 args.ui_scale,
                 Label.from_arguments(args, cube, arg_parser),
                 colors.get_background_theme(args),
                 colors.get_cube_colors(args)), orientation


def init_timing_arg_parser(arg_parser: ArgumentParser):
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


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    arg_parser = ArgumentParser(description="Visualizing of twisting cube turning "
                                            "and rotation. ", prog="cubeplayer")
    arg_parser.add_argument("formula", type=formula_type, default=[], nargs="?",
                            help="turns and rotations that will be animated")
    arg_parser.add_argument("--no-ui", action="store_false", dest="show_formula_ui",
                            help="hide the sequence of actions at the bottom of a screen")
    arg_parser.add_argument("--ui-scale", type=float, dest="ui_scale",
                            help="user interface scale", default=1.0)

    rendering_group = arg_parser.add_argument_group("rendering options")
    rendering_group.add_argument("--resolution", metavar="N", nargs=2, default=[854, 480],
                                 help="resolution of a frame (width, height)", type=integer_type(1))
    rendering_group.add_argument("--scale", metavar="S", default=1.0, dest="scale",
                                 help="cube scale", type=float)
    rendering_group.add_argument("--camera-angle", metavar="D", default=[-20, 25, 0], nargs=3,
                                 dest="camera_angle", help="camera angle in degreese", type=float)
    rendering_group.add_argument("--msaa", type=integer_type(0), default=0, metavar="N_SAMPLES",
                                 help="number of samples for multisample antialiasing (MSAA)")

    init_cube_args_parser(arg_parser)
    VideoRenderer.init_args_parser(arg_parser)
    init_timing_arg_parser(arg_parser)
    Label.init_args_parser(arg_parser)
    colors.init_args_parser(arg_parser)

    args = arg_parser.parse_args()

    renderer = backend_factory(args)(lambda: create_scene(args, arg_parser), args)
    renderer.run()


if __name__ == "__main__":
    main()
