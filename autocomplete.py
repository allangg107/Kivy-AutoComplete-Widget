from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput


class Autocomplete(TextInput):
    suggestion_index = -404
    dropdown = DropDown()
    suggestions_source = [
        'aaa', 'aab', 'aac', 'aad', 'aae',
        'aba', 'abb', 'abc', 'abd', 'abe',
        'aca', 'acb', 'acc', 'acd', 'ace',
    ]

    # Sets the Autocomplete text to the given text
    def dropdown_set_text(self, text):
        self.text = text
        self.dropdown.dismiss()

    # Determines the suggestions to show the user based on their current input and then displays those suggestions
    def give_suggestions(self):
        self.dropdown.dismiss()
        self.dropdown = DropDown()

        user_input = self.text

        suggestions = []

        # Populates the suggestions list by comparing the user input to its suggestions_source (this could be changed
        # as you see fit)
        # For demonstration purposes the logic to create the suggestions list is very simple
        # However, the suggestions list could be populated in a smarter and more efficient manner depending on how you
        # wish the suggestions to be displayed
        for word in self.suggestions_source:
            if user_input in word:
                suggestions.append(word)

        # Each suggestion that matches the user input is added as an option to select in the Autocomplete dropdown
        for option in suggestions:
            btn = Button(size_hint=(1, None), height="30dp")
            btn.text = option
            btn.bind(on_release=lambda the_btn: self.dropdown_set_text(the_btn.text))
            self.dropdown.add_widget(btn)

        # If there is at least 1 suggestion, the suggestion_index is set and the first suggestion is highlighted
        if len(self.dropdown.children[0].children) > 0:
            self.suggestion_index = len(self.dropdown.children[0].children) - 1
            self.dropdown.open(self)
            self.dropdown.children[0].children[self.suggestion_index].background_color = (2, 2, 2, 2)

    # Overrides the keyboard_on_key_down method
    # Enables the user to use the up and down arrow keys to navigate the list of suggestions
    # The enter key can be used to select a suggestion
    # The tab key can be used to select a suggestion and move to the next field
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if len(self.dropdown.children[0].children) > 0:
            if keycode[1] == 'up':
                # Check to make sure you are not going out of bounds
                if self.suggestion_index < len(self.dropdown.children[0].children) - 1:
                    # Update the index
                    self.suggestion_index = self.suggestion_index + 1
                    # Highlight and un-highlight the current and previous suggestion
                    self.dropdown.children[0].children[self.suggestion_index].background_color = (2, 2, 2, 2)
                    self.dropdown.children[0].children[self.suggestion_index - 1].background_color = (1, 1, 1, 1)
                    return True

            elif keycode[1] == 'down':
                if self.suggestion_index > 0:
                    self.suggestion_index = self.suggestion_index - 1
                    self.dropdown.children[0].children[self.suggestion_index].background_color = (2, 2, 2, 2)
                    self.dropdown.children[0].children[self.suggestion_index + 1].background_color = (1, 1, 1, 1)
                    return True

            elif keycode[1] == 'enter':
                self.dropdown_set_text(self.dropdown.children[0].children[self.suggestion_index].text)
                return True

            elif keycode[1] == 'tab':
                self.dropdown_set_text(self.dropdown.children[0].children[self.suggestion_index].text)
                # does not return True in order to keep default tab behavior of moving to next field

        return super().keyboard_on_key_down(window, keycode, text, modifiers)


_kv = Builder.load_file("autocomplete.kv")


class Demonstration(App):
    def build(self):
        return _kv


Demonstration().run()
