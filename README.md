This extension provides the default key bindings for Windows
on any platform.

Currently, these are the defaults for VSCode 1.78.2.

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

## Some problematic keybindings and workarounds

The basic goal of this extension is to allow VSCode users who are accustomed to the keybindings on Windows to use it on other platforms with the same keybindings.  However, sometimes the bindings conflict with something else on the other OS, or don't work for some other reason.

In this section I have collected together some workarounds, but be aware that I haven't personally tested all of them.

### Ctrl + Alt + Up/Down/Right

On Windows, Ctrl+Alt+Up and Ctrl+Alt+Down enter multi-column select mode, and
Ctrl+Alt+Right splits the editor pane vertically.  On some Linux distributions,
the window manager by default intercepts these key combinations.

On Ubuntu 22, to disable the offending window manager bindings and allow VSCode
to see them, run at a shell:

```
$ gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left "['']"
$ gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right "['']"
$ gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down "['']"
$ gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up "['']"
```

On Mint 20, run:

```
$ gsettings set org.cinnamon.desktop.keybindings.wm move-to-workspace-left "['']"
$ gsettings set org.cinnamon.desktop.keybindings.wm move-to-workspace-right "['']"
$ gsettings set org.cinnamon.desktop.keybindings.wm move-to-workspace-down "['']"
$ gsettings set org.cinnamon.desktop.keybindings.wm move-to-workspace-up "['']"
```

### Ctrl + Left/Right on MacOS

On Windows, Ctrl + Left/Right moves the cursor by one word to the left or right,
including in the Terminal window.  However, reportedly on MacOS, these key bindings
do not work in the Terminal.  Insert the following snippet into `keybindings.json`
(Ctrl+Shift+P to get the Command Palette, then "Open Keyboard Shortcuts (JSON)")
to add bindings that work in Terminal on MacOS:

```
[
  {
    "key":     "ctrl+left",
    "command": "workbench.action.terminal.sendSequence",
    "args":    { "text": "\u001bb" },
    "when":    "terminalFocus"
  },
  {
    "key":     "ctrl+right",
    "command": "workbench.action.terminal.sendSequence",
    "args":    { "text": "\u001bf" },
    "when":    "terminalFocus"
  },
]
```

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
