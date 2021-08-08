import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="tween",
  version="0.0.3",
  description="A small tweening module",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Ivar Fatland",
  author_email="fatland99@hotmail.com",
  license="MIT",
  packages=["tween"],
  zip_safe=False,
  install_requires = ["PyTweening==1.0.3"],
  url = "https://github.com/roodletoof/tween"
)
