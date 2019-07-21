workflow "upload to PyPI on tag" {
  on = "create"
  resolves = "upload to PyPI"
}

action "filter tag" {
  uses = "actions/bin/filter@master"
  args = "tag v*"
}

action "install dependencies" {
  uses = "gieseladev/python-actions@3.7"
  args = "pip install pytest"
}

action "test" {
  uses = "gieseladev/python-actions@3.7"
  args = "python -m pytest"
  needs = "install dependencies"
}

action "create distribution" {
  uses = "ross/python-actions/setup-py/3.7@master"
  args = "sdist"
  needs = [
    "filter tag",
    "test",
  ]
}

action "upload to PyPI" {
  uses = "ross/python-actions/twine@master"
  args = "upload ./dist/lptrack*.tar.gz"
  secrets = [
    "TWINE_USERNAME",
    "TWINE_PASSWORD",
  ]
  needs = "create distribution"
}

workflow "test on push" {
  on = "push"
  resolves = "test"
}
