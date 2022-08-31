This extension provides the default key bindings for Windows
on any platform.

Currently, these are the defaults for VSCode 1.70.2.

This is useful if you want to run VSCode on another platform
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

## Installation

From within VSCode, go to extensions (Ctrl+Shift+X),
search for "Windows Default Keybindings", click on it, then
click on Install.  The new bindings should be active immediately.

Alternatively, install it from the
[Marketplace page](https://marketplace.visualstudio.com/items?itemName=smcpeak.default-keys-windows),
or download the VSIX file from the
[Github releases page](https://github.com/smcpeak/vscode-default-keys-windows/releases)
and then use "Install from VSIX..." menu option from the "..." menu in
the Extensions page.

## How it was created

For the curious or adventurous, the procedure I used to create this
extension is:

1. Run `yo code` to make a new keybindings extension.
2. Disable all non-default extensions (within the workspace) so their
   entries do not appear in the output from the next command.
3. Run command "Preference: Open Default Keyboard Shortcuts (JSON)"
   from the command palette.
4. Copy the output into the `contributes.keybindings` section
   of `package.json`.
5. Tidy up `package.json` by adding `publisher`, etc.
6. Write documentation.
