import subprocess
from argparse import ArgumentParser
from libcube.cli.options import integer_type
from OpenGL.GL import *
from OpenGL.GLUT import *

from .backend import RenderingBackend
from os.path import expanduser


class VideoRenderer(RenderingBackend):
    @staticmethod
    def init_args_parser(parser: ArgumentParser):
        group = parser.add_argument_group("video output options")
        group.add_argument("--video", help="path to the output video file",
                           metavar="FILE", dest="video_file")
        group.add_argument("--video-fps", help="frame rate of the video", type=integer_type(1),
                           metavar="FPS", dest="video_frame_rate", default=30)
        group.add_argument("--ffmpeg", help="path to a ffmpeg executable",
                           metavar="PATH", dest="ffmpeg_path", default="/usr/bin/ffmpeg")
        group.add_argument("--ffmpeg-out", help="show output generated by ffmpeg", action="store_true",
                           dest="ffmpeg_show_output")

    def init_gl(self):
        self.create_glut_window("", False)
        glutHideWindow()

    def run(self):
        # noinspection PyBroadException
        try:
            process = subprocess.Popen(
                [self.args.ffmpeg_path,
                 "-f", "rawvideo",
                 "-pix_fmt", "rgb24",
                 "-s", "x".join(map(str, self.args.resolution)),
                 "-r", str(self.args.video_frame_rate),
                 "-i", "pipe:",
                 "-y",
                 "-vf", "vflip",
                 "-r", str(self.args.video_frame_rate),
                 expanduser(self.args.video_file)
                 ],
                stdin=subprocess.PIPE,
                stderr=sys.stderr if self.args.ffmpeg_show_output else subprocess.DEVNULL)
        except Exception as e:
            print("An error has occurred while trying to start ffmpeg. Make sure it is installed.\n"
                  f"Error message: {e}\n\n"
                  "If ffmpeg is not installed under its default location, please, specify the path to the executable "
                  "via `--ffmpeg` argument.")
            sys.exit(1)

        try:
            over = False

            def finished_callback():
                nonlocal over
                over = True

            self.cube_animator.finish_callback = finished_callback
            while not over:
                self.scene.render(*self.args.resolution)
                glPixelStorei(GL_PACK_ALIGNMENT, 1)
                data = glReadPixels(0, 0, *self.args.resolution, GL_RGB, GL_UNSIGNED_BYTE)
                process.stdin.write(data)
                self.animator.run(1.0 / self.args.video_frame_rate)
            process.stdin.close()
            code = process.wait()
        except BrokenPipeError:
            code = 1

        if code != 0:
            message = "An error has occurred while generating a video."
            if not self.args.ffmpeg_show_output:
                message += " Please, see `--ffmpeg-out` option for more details"
            print(message, file=sys.stderr)
            sys.exit(1)
