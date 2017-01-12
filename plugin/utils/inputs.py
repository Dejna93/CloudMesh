
def input_validator(event):
        if event.char in '0123456789':
            pass
        elif len(event.widget.get()) == 0 and event.char in "+-":
            pass
        elif event.widget.get().count('.') == 0 and event.char == '.':
            pass
        elif len(event.widget.get()) == 0 and event.char == '-':
            pass
        elif event.keysym == "BackSpace" or event.keysym == 'Delete':
            pass
        else:
            return 'break'