from setuptools import setup, find_packages
from pathlib import Path
import re


with open(str(Path(__file__).parents[0] / "cubeplayer" / "__init__.py")) as f:
    init_file = f.read()
    metadata = dict(re.findall(r"^__([a-z_]+)__\s*=\s*\"(.*)\"$", init_file,
                               re.MULTILINE))


setup(
    name='CubePlayer',
    version=metadata["version"],
    packages=["cubeplayer", "cubeplayer.renderer", 
              "cubeplayer.renderer.animation", "cubeplayer.renderer.engine"],
    url='https://github.com/poletaevvlad/CubePlayer',
    license='MIT',
    author=metadata["version"],
    author_email=metadata["author_email"],
    description="Visualization tool for twisting cube puzzle turns and rotations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "CubeLang",
        "PyOpenGL",
        "pillow",
        "freetype-py"
    ],
    entry_points={
        "console_scripts": [
            "cubeplayer = cubeplayer.__main__:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment :: Puzzle Games"
    ]
)
