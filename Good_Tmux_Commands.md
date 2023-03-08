# Good Tmux Commands

Created: July 31, 2022 5:09 PM
Modified: March 8, 2023 12:54 AM

<aside>
🎯 USE BetterTouchTool to customize more commands.

</aside>

<aside>
🎯 NOTE: Hold option to copy/select!
ctrl + d to exit terminals

</aside>

Note my prefix is ctrl + a (default is ctrl + b) 

- [ ]  todo: tmux net speed (kinda interesting, and can specify specific interfaces)

[https://github.com/tmux-plugins/tmux-net-speed](https://github.com/tmux-plugins/tmux-net-speed)

## References

[Tmux Cheat Sheet & Quick Reference](https://tmuxcheatsheet.com/)

Plugins: https://github.com/tmux-plugins/tpm

# synchronize panes

```python
<prefix> then type `:setw synchronize-panes`
```

Swap panes, move it around `prefix + {`

# toggle full-screen (zoom)

Note indicator in bottom right 

```python
ctrl +a + z
```

![Untitled](Good%20Tmux%20Commands%2041330b4917b04eaab3d42159e2eaa0d8/Untitled.png)

# Sessions

- Rename session `prefix + $`

## Window Management

- `prefix + c` — create new window
- `,` - rename window
- `w` - list all windows
- `f` - find window by name
- `.` - move window to another session (promt)
- `:movew` - move window to next unused number

### Breakout pane into new window

`prefix + !` — super handy

Rename windows (tabs at bottom) `prefix + ,`

or spell it out: `tmux rename-session $(echo testsession)`

### cycle thru sessions

`prefix` + `)`         (and the other paren way)

## Kill sessions

`tmux kill-server`  — nuclear reset

`prefix + shift + X`   —  kill pane  (`bind-key X kill-pane`)

# resize panes

<prefix>

- `ctrl + o` cycle clockwise
- `{` — move pane clockwise.

Mouse works! 

`prefix` + `HOLD option` + `arrow arrow arrow` (to iteratively expand! super nice)

### Cycle thru windows

`prefix + n / w`  — cycle forward and backwards

`prefix + <window number>` — switch to specific window