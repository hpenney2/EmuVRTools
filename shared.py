from inquirer.themes import Theme
from blessed import Terminal

term = Terminal()


class EVRTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.bright_magenta
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.bright_magenta
        self.Checkbox.selection_icon = ">"
        self.Checkbox.selected_icon = "X"
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "o"
        self.List.selection_color = term.bright_cyan + term.bold
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.normal
