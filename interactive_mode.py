from data_optimizer import optimize_data
from collections import (
    OrderedDict,
    namedtuple
)


class InputHandler:

    @staticmethod
    def handle_input(input_msg, error_msg, expected_type):
        while True:
            try:
                user_input = eval(input(input_msg))
                if type(user_input) != expected_type:
                    raise TypeError
                break
            except (SyntaxError, NameError, TypeError):
                print(error_msg)

        return user_input


class InteractiveMode:
    def __init__(self, optimize_func, data):
        self.data = data
        self.menu = OrderedDict()
        self.template = None
        self.optimize_data = optimize_func
        self.init_menu()

    def quit_interactive_mode(self):
        exit()

    def show_dict(self):
        print(self.data)

    def init_menu(self):
        MenuItem = namedtuple("MenuItem", "label handler")
        self.menu[1] = MenuItem('1 - Provide your data', self.provide_dict)
        self.menu[2] = MenuItem('2 - Show current data', self.show_dict)
        self.menu[3] = MenuItem('3 - Provide your template', self.provide_template)
        self.menu[4] = MenuItem('4 - Exit', self.quit_interactive_mode)

    def show_menu(self):
        for menu_item_key in self.menu.keys():
            print(self.menu[menu_item_key].label)



    def provide_dict(self):
        self.data = InputHandler.handle_input('Provide your data in dict format: ',
                                              'You should provide data in dict format.',
                                              expected_type=dict)

    def provide_template(self):
        self.template = InputHandler.handle_input('Provide your template in str format: ',
                                                  'You should provide template in str format.',
                                                  expected_type=str)
        if self.data:
            new_data = self.optimize_data(self.template, self.data)
            if new_data:
                print('Optimized data: {}'.format(new_data))
                print(self.template.format(**new_data))

    def handle_menu(self, user_input):
        menu_item = self.menu.get(user_input)
        if not menu_item:
            self.quit_interactive_mode()
        menu_item.handler()


    def interactive_loop(self):
        self.show_menu()

        while True:
            user_input = InputHandler.handle_input('Choose 1, 2, 3 or 4: ',
                                                   'You should type 1, 2, 3 or 4.',
                                                   expected_type=int)
            self.handle_menu(user_input)


if __name__ == '__main__':
    data = {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {
                'latest_version': '1.17',
                'site': 'https://rust-lang.org',
            },
        },
        'animals': ['cow', 'penguin'],
    }
    interactive_mode = InteractiveMode(optimize_data, data)
    interactive_mode.interactive_loop()