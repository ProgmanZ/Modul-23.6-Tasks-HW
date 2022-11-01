
import keyboard

def foo():
    print('\nWorld')

keyboard.add_hotkey('1', lambda: print('\nHello'))
keyboard.add_hotkey('2', foo)

keyboard.wait('Ctrl + Q')