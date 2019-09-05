This extension provides the default key bindings for Windows.

Currently, these are the defaults for VSCode 1.37.1.

It is useful if you want to run VSCode on another platform
but continue to use the bindings that are the defaults on
Windows (e.g.,
[here](https://stackoverflow.com/questions/52726849/how-to-transfer-vscode-key-mapping-on-windows-to-ubuntu)
and
[here](https://stackoverflow.com/questions/45840945/vscode-importing-keyboard-shortcuts)).

This extension does not remove any existing bindings.  On
Windows, that means you have everything bound twice.  On
other platforms, you have that platform's default bindings
plus the Windows ones.  The bindings in this extension take
precedence over the defaults provided by VSCode.

Example screenshot running on Linux:

![Screenshot of bindings](bindings-screenshot.png)

Procedure for creating this extension:

1. Run `yo code` to make a new keybindings extension.
2. Run command "Preference: Open Default Keyboard Shortcuts (JSON)"
   from the command palette.
3. Copy the output into the `contributes.keybindings` section
   of `package.json`.
4. Tidy up `package.json` by adding `publisher`, etc.
5. Write documentation.
