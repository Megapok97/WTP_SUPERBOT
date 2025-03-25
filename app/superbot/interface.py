class Button:
    def __init__(self, name: str, icon: str = None, command: str = None):
        self.name = name
        self.icon = icon
        self.command = command

        text_parts = [self.icon, self.name]
        self.text = ' '.join([s for s in text_parts if s is not None])

        messages = self.text, self.name, self.command
        self.messages = {*[m for m in messages if m is not None]}


class Keyboard:
    def __init__(self, name: str, layout: list[list[Button]]):
        self.name = name
        self.layout = layout

        self.buttons = set()
        self.messages = set()

        self.width = 0
        self.height = len(layout)

        for buttons_row in self.layout:
            self.width = max(self.width, len(buttons_row))

            for button in buttons_row:
                self.buttons.add(button)
                self.messages |= button.messages
