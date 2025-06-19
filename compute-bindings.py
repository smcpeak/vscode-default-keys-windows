#!/usr/bin/env python3

"""
Read the default Linux and Windows key bindings files from the
`reference` directory, and output which keys have a different binding on
Windows than Linux.
"""

import argparse              # argparse
import difflib               # unified_diff
import json                  # load
import os                    # os.getenv
import re                    # re.compile
import signal                # signal.signal
import sys                   # sys.argv, sys.stderr, sys.stdin
import traceback             # traceback.print_exc

from typing import Any, Dict, List, Match, Pattern, TextIO


# -------------- BEGIN: boilerplate -------------
# These are things I add at the start of every Python program to
# allow better error reporting.

# Positive if debug is enabled, with higher values enabling more printing.
debugLevel = 0
if debugEnvVal := os.getenv("DEBUG"):
  debugLevel = int(debugEnvVal)

def debugPrint(str: str) -> None:
  """Debug printout when DEBUG >= 2."""
  if debugLevel >= 2:
    print(str)

# Ctrl-C: interrupt the interpreter instead of raising an exception.
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Error(Exception):
  """A condition to be treated as an error."""
  pass

def die(message: str) -> None:
  """Throw a fatal Error with message."""
  raise Error(message)

def exceptionMessage(e: BaseException) -> str:
  """Turn exception 'e' into a human-readable message."""
  t = type(e).__name__
  s = str(e)
  if s:
    return f"{t}: {s}"
  else:
    return f"{t}"

def call_main() -> None:
  """Call main() and catch exceptions."""
  try:
    main()

  except SystemExit as e:
    raise      # Let this one go, otherwise sys.exit gets "caught".

  except BaseException as e:
    print(f"{exceptionMessage(e)}", file=sys.stderr)
    if (debugLevel >= 1):
      traceback.print_exc(file=sys.stderr)
    sys.exit(2)
# --------------- END: boilerplate --------------


def read_file_lines(fname: str) -> List[str]:
  """Read `fname` into a list of strings, one per line, with newlines
  retained."""

  lines: List[str] = []
  with open(fname, "r") as f:
    for line in f:
      lines.append(line)
  return lines


def read_commented_json(fname: str) -> Any:
  """Read `fname` as JSON after discarding lines that begin with a
  comment character.  (This does not handle the case of a comment on
  the same line as data, but VSCode JSON does not do that.)"""

  lines = read_file_lines(fname)
  filtered_lines = [
    line
    for line in lines
    if not line.strip().startswith("//")     # `strip` removes surrounding ws
  ]
  filtered_string = "".join(filtered_lines)
  return json.loads(filtered_string)


# A VSCode binding is a dictionary that has a "key", a "command",
# possibly a "when", and a few other optional elements.  An ordered list
# of Bindings specifies how VSCode will interpret the correspinding
# keyboard key.
Binding = Dict[str, Any]


# Type of a dictionary of grouped key bindings where the overall
# dictionary key is the name of the keyboard key (as a string), and the
# value is the ordered list of Bindings for that key.
BindingDict = Dict[str, List[Binding]]


def read_bindings(fname: str) -> BindingDict:
  """Read `fname` as a VSCode key bindings file."""

  flat_bindings = read_commented_json(fname)
  if not isinstance(flat_bindings, list):
    die(f"Expected key bindings in {fname!r} to be a list.")

  grouped_bindings: BindingDict = {}
  for binding in flat_bindings:
    if not isinstance(binding, dict):
      die(f"Expected binding to be a dict: {binding!r}")
    if "key" not in binding:
      die(f"Expected binding to have a 'key': {binding!r}")

    key = binding["key"]
    grouped_bindings.setdefault(key, []).append(binding)

  return grouped_bindings


def get_indented_json(value: Any, indent_level: int) -> str:
  """Get `value` as JSON with `indent_level` of indentation spaces
  preceding all lines, and two spaces of indentation separating nested
  levels.  The final line does not have a trailing newline."""

  indent_prefix: str = " " * indent_level
  quoted: str = json.dumps(value, indent=2)
  lines: List[str] = [
    indent_prefix + line
    for line in quoted.splitlines()
  ]
  return "\n".join(lines)


def read_platform_bindings(platform: str) -> BindingDict:
  """Read the default bindings for `platform`."""

  # This relies on https://github.com/codebling/vs-code-default-keybindings,
  # which is a separate project that does its own automated extraction
  # of the vscode bindings.
  return read_bindings(f"vs-code-default-keybindings/{platform}.keybindings.json")


def print_differences(left: Any, right: Any, ) -> None:
  """Print the differences between `left` and `right` in a `diff`-like
  report."""

  # Stringify as JSON for comparison and printing.
  left_json: List[str] = json.dumps(left, indent=2).splitlines()
  right_json: List[str] = json.dumps(right, indent=2).splitlines()

  # Compare using difflib.
  differences: List[str] = [
    line
    for line in difflib.unified_diff(left_json, right_json)
  ]

  # Discard the header that tries to give the file names.
  differences = differences[2:]

  for line in differences:
    print(line)


def should_ignore_key(key: str) -> bool:
  """Return true if `key` should be ignored, in the sense of never
  having an overriding keybinding in this extension."""

  # "escape" is weird because it has identical bindings on Windows and
  # Linux when I check in my own VSCode instances, but the
  # vs-code-default-keybindings repo shows a single anomalous
  # difference.  Even if the difference is "real", the purpose of the
  # Escape key is the same on all platforms, so this extension should
  # not need to mess with it.
  if key == "escape":
    return True

  # This one is weird because it has a "when" clause that refers to my
  # own user data directory, which of course makes no sense to publish
  # in a general purpose extension.  It's harmless because that "when"
  # will never match, but cleaner to exclude entirely.
  if key == "ctrl+k ctrl+k":
    return True

  return False


def print_key_list(keys: List[str], label: str) -> None:
  """Print `keys` after a line with `label`."""

  print(f"  {len(keys)} {label}:")
  for key in keys:
    print(f"    {key}")


def main() -> None:
  windows_keys: BindingDict = read_platform_bindings("windows")
  print(f"Windows has {len(windows_keys)} bound keys.")

  linux_keys: BindingDict = read_platform_bindings("linux")
  print(f"Linux has {len(linux_keys)} bound keys.")

  macos_keys: BindingDict = read_platform_bindings("macos")
  print(f"MacOS has {len(macos_keys)} bound keys.")

  # Bindings that we need to include in the extension definition in
  # order to make the Windows bindings work on Linux.
  override_bindings: List[Binding] = []

  # List of keys with various dispositions.
  ignored = []
  missing_linux = []
  missing_macos = []
  different_linux = []
  different_macos = []
  same = []

  # Iterate over all keys bound on Windows and compare that binding to
  # how it is bound (if at all) on Linux.
  for key in sorted(windows_keys):
    windows_bindings = windows_keys[key]

    # Ignore certain keys.
    if should_ignore_key(key):
      ignored.append(key)

    elif key not in linux_keys:
      print(f"Key {key!r} is not bound on Linux; on Windows, it is:")
      print(get_indented_json(windows_bindings, 2))

      override_bindings += windows_bindings
      missing_linux.append(key)

    elif key not in macos_keys:
      print(f"Key {key!r} is not bound on MacOS; on Windows, it is:")
      print(get_indented_json(windows_bindings, 2))

      override_bindings += windows_bindings
      missing_macos.append(key)

    else:
      linux_bindings = linux_keys[key]
      macos_bindings = macos_keys[key]

      if windows_bindings != linux_bindings:
        print(f"Bindings for {key!r} differ between Windows and Linux:")
        print_differences(windows_bindings, linux_bindings)

        override_bindings += windows_bindings
        different_linux.append(key)

      elif windows_bindings != macos_bindings:
        print(f"Bindings for {key!r} differ between Windows and MacOS:")
        print_differences(windows_bindings, macos_bindings)

        override_bindings += windows_bindings
        different_macos.append(key)

      else:
        same.append(key)

  # Summarize the comparison results.
  print(f"Of the {len(windows_keys)} keys bound on Windows:")
  print_key_list(ignored, "are ignored due to rules in this script")
  print_key_list(missing_linux, "are not bound on Linux")
  print_key_list(missing_macos, "are not bound on MacOS")
  print_key_list(different_linux, "are bound differently on Linux")
  print_key_list(different_macos, "are bound differently on MacOS")
  print_key_list(same, "are the same on all three platforms")

  # Print the override bindings to a file.  That has to then be
  # manually copied+pasted into package.json.
  with open("overrides.json", "w") as f:
    f.write(get_indented_json(override_bindings, 4) + "\n")


call_main()


# EOF
