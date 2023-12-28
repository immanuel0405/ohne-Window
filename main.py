from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from functools import partial


class QuizPopup(Popup):
    def __init__(self, **kwargs):
        super(QuizPopup, self).__init__(**kwargs)
        self.title = "Prüfungsfragen"
        self.current_question_index = 0
        self.score = 0
        self.questions = [
            {
                'question': 'Was ist die Hauptfunktion eines Drohnenführerscheins?',
                'options': ['Luftaufnahmen machen', 'Drohnenrennen gewinnen',
                            'Sicherheit/Gesetzeskonformität gewährleisten'],
                'correct_answer': 'Sicherheit/Gesetzeskonformität gewährleisten'
            },
            {
                'question': 'Welche Flugregeln sollten beim Betrieb einer Drohne beachtet werden?',
                'options': ['Es gibt keine Regeln', 'Je höher, desto besser',
                            'Luftraumvorschriften beachten'],
                'correct_answer': 'Luftraumvorschriften beachten'
            },
            {
                'question': 'Warum ist die Kenntnis der Drohnentechnik wichtig?',
                'options': ['Nur für Technik-Enthusiasten', 'Zum Angeben vor Freunden',
                            'Sicherer Betrieb/Steuerung der Drohne'],
                'correct_answer': 'Sicherer Betrieb/Steuerung der Drohne'
            }
        ]

        self.question_label = Label(text=self.questions[self.current_question_index]['question'], font_size=10)
        self.option_buttons = []

        for option in self.questions[self.current_question_index]['options']:
            button = Button(text=option, on_press=self.check_answer, size_hint_y=None, height=40)
            self.option_buttons.append(button)

        self.next_button = Button(text="Weiter", on_press=self.next_question, size_hint_y=None, height=40)

        self.content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.content.add_widget(self.question_label)
        for button in self.option_buttons:
            self.content.add_widget(button)
        self.content.add_widget(self.next_button)
        self.set_button_colors()

    def set_button_colors(self):
        for button, color in zip(self.option_buttons, [(0.2, 0.4, 0.8, 1), (0.4, 0.6, 1, 1), (0.6, 0.8, 1, 1)]):
            button.background_color = color

    def check_answer(self, instance):
        selected_answer = instance.text
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        if selected_answer == correct_answer:
            self.score += 1

    def next_question(self, instance):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label.text = self.questions[self.current_question_index]['question']
            for i, button in enumerate(self.option_buttons):
                button.text = self.questions[self.current_question_index]['options'][i]
        else:
            self.dismiss()
            self.show_quiz_result()

    def show_quiz_result(self):
        result_popup = Popup(title="Quiz Ergebnis", content=Label(
            text=f"Du hast {self.score} von {len(self.questions)} Fragen richtig beantwortet."),
                             size_hint=(None, None), size=(400, 400))
        result_popup.open()


class MyButtonsApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title_label = Label(text="Willkommen in unserer App", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(title_label)

        button_data = [
            ("Vorbereitung Drohnenführerschein", (0.1, 0.2, 0.6, 1)),  # Dunkles Blau
            ("Drohnenkennzahlen", (0.2, 0.4, 0.8, 1)),  # Mittelblau
            ("Bewässerungszustand", (0.4, 0.6, 1, 1)),  # Hellblau
            ("Info Hydrojet", (0.6, 0.8, 1, 1))  # Sehr helles Blau
        ]

        for name, color in button_data:
            h_box = BoxLayout(orientation='horizontal', spacing=10)

            button = Button(text=f'{name}', background_color=color, on_press=partial(self.show_popup, btn_name=name))
            h_box.add_widget(button)

            h_box.id = f'box_{name.replace(" ", "_")}'
            layout.ids[h_box.id] = h_box

            layout.add_widget(h_box)

        return layout

    def show_popup(self, instance, btn_name):
        if btn_name == "Vorbereitung Drohnenführerschein":
            self.subpopup = PreparationSubPopup()
            self.subpopup.open()
        else:
            content = None
            title = ""
            if btn_name == "Bewässerungszustand":
                content = self.create_table_content()
                title = "Bewässerungszustand"
            elif btn_name == "Info Hydrojet":
                content = self.create_hydrojet_info()
                title = "Info Hydrojet"
            elif btn_name == "Drohnenkennzahlen":
                content = self.create_drone_info()
                title = "Drohnenkennzahlen"

            if content is not None:
                popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 600))
                close_button = Button(text="zurück", on_press=lambda *args: self.dismiss_popup(popup),
                                      size_hint=(None, None), size=(80, 50), pos_hint={'top': 1, 'right': 1})
                content.add_widget(close_button)
                popup.open()

    def create_table_content(self):
        table_layout = GridLayout(cols=3, spacing=1, size_hint_y=None, pos_hint={'top': 0.95})

        header_label1 = Label(text="Felder", bold=True, font_size=8)
        header_label2 = Label(text="Zustand", bold=True, font_size=8)
        header_label3 = Label(text="zuletzt bewässert", bold=True, font_size=8)
        table_layout.add_widget(header_label1)
        table_layout.add_widget(header_label2)
        table_layout.add_widget(header_label3)

        felder = ["Nr. 1", "Nr. 2", "Nr. 3", "Nr. 4", "Nr. 5", "Nr. 6", "Nr. 7", "Nr. 8", "Nr. 9", "Nr. 10"]

        zustand = ["gut", "sehr gut", "gut", "schlecht", "sehr gut", "gut", "sehr schlecht", "gut", "sehr gut",
                   "sehr gut"]

        zuletzt_bewaessert = ["vor 2 Tagen bewässert", "heute bewässert", "vor 3 Tagen bewässert",
                              "vor 7 Tagen bewässert", "gestern bewässert", "vor 3 Tagen bewässert",
                              "vor 11 Tagen bewässert", "vor 2 Tagen bewässert", "heute bewässert", "gestern bewässert"]

        for feld, zustand_text, zuletzt_bewaessert_text in zip(felder, zustand, zuletzt_bewaessert):
            label_feld = Label(text=feld, font_size=8, size_hint_y=None, height=20)
            label_zustand = Label(text=zustand_text, font_size=8, size_hint_y=None, height=20)
            label_zuletzt_bewaessert = Label(text=zuletzt_bewaessert_text, font_size=8, size_hint_y=None, height=20)
            table_layout.add_widget(label_feld)
            table_layout.add_widget(label_zustand)
            table_layout.add_widget(label_zuletzt_bewaessert)

        return table_layout

    def create_hydrojet_info(self):
        hydrojet_info_layout = GridLayout(cols=1, spacing=12, size_hint_y=None, pos_hint={'top': 0.8})

        hydrojet_info_text = """
        HydroJet Irrigation Systems PLC (HydroJet), 
        headquartered in Kidwelly/UK, is a Welsh
        provider of drone-supported irrigation system
        solutions, which it offers as Smart Product
        Service Systems (SPSS) for smart agriculture 
        and forestry, winegrowing, vegetable and fruit
        growing, vertical farming and other professional
        gardening businesses.





        """

        label_hydrojet_info = Label(text=hydrojet_info_text, font_size=14, size_hint_y=None, height=55)
        hydrojet_info_layout.add_widget(label_hydrojet_info)

        return hydrojet_info_layout

    def create_drone_info(self):
        drone_info_layout = GridLayout(cols=2, spacing=12, size_hint_y=None, pos_hint={'top': 0.95})

        header_label1 = Label(text="Infos", bold=True, font_size=8)
        header_label2 = Label(text="verbundene Drohne", bold=True, font_size=8)
        drone_info_layout.add_widget(header_label1)
        drone_info_layout.add_widget(header_label2)

        drone_data = [
            ("Betriebszustand", "aktiv"),
            ("Akkustand", "78 Prozent"),
            ("Standort", "Feld 1"),
            ("Flugzeit", "3h 20min"),
            ("Zeit seit letzter Wartung", "7 Tage 8 Stunden")
        ]

        for label_text, value_text in drone_data:
            label = Label(text=label_text, font_size=8, size_hint_y=None, height=30)
            value = Label(text=value_text, font_size=8, size_hint_y=None, height=30)
            drone_info_layout.add_widget(label)
            drone_info_layout.add_widget(value)

        return drone_info_layout

    def dismiss_popup(self, popup):
        popup.dismiss()


class PreparationSubPopup(Popup, EventDispatcher):
    def __init__(self, **kwargs):
        super(PreparationSubPopup, self).__init__(**kwargs)
        self.title = "Vorbereitungskurs zum Drohnenführerschein"
        self.content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        subbutton_data = [
            ("Vorbereitungskurs", (0.1, 0.2, 0.6, 1)),
            ("Prüfungsfragen", (0.2, 0.4, 0.8, 1)),
            ("Hier gehts zur Prüfungsanmeldung", (0.4, 0.6, 1, 1))
        ]

        for subname, subcolor in subbutton_data:
            subbutton = Button(text=f'{subname}', background_color=subcolor,
                               on_press=partial(self.on_subbutton_press, subname))
            self.content.add_widget(subbutton)

        close_button = Button(text="zurück", on_press=lambda *args: self.dismiss(), size_hint=(None, None),
                              size=(80, 50), pos_hint={'top': 1, 'right': 0.6})
        self.content.add_widget(close_button)

    def on_subbutton_press(self, subname, *args):
        if subname == "Vorbereitungskurs":
            open_course_info_popup()
        elif subname == "Prüfungsfragen":
            quiz_popup = QuizPopup()
            quiz_popup.open()
        elif subname == "Hier gehts zur Prüfungsanmeldung":
            self.show_pruefungsanmeldung_popup()

    def show_pruefungsanmeldung_popup(self):
        pruefungsanmeldung_text = "Besuchen Sie uns gerne auf unserer Website."
        pruefungsanmeldung_popup = Popup(title="Prüfungsanmeldung", content=Label(text=pruefungsanmeldung_text),
                                         size_hint=(None, None), size=(400, 600))
        close_button = Button(text="zurück", on_press=pruefungsanmeldung_popup.dismiss,
                              size_hint=(None, None), size=(50, 30), pos_hint={'top': 0.5, 'right': 0.55})
        pruefungsanmeldung_popup.content.add_widget(close_button)
        pruefungsanmeldung_popup.open()

    def on_parent(self, widget, parent):
        if parent and isinstance(parent, Popup):
            parent.dismiss()


def open_course_info_popup():
    course_info_text = """
1. Gesetzliche Compliance sicherstellen: 
    Informieren Sie sich über die aktuellen nationalen und 
    regionalen Gesetze und Vorschriften für den Betrieb
    von Drohnen. Unsere Schulung deckt alle
    relevanten rechtlichen Anforderungen ab.

2. Teilnahme an theoretischer Schulung: Besuchen Sie 
   unsere theoretische Schulung, die alle
   notwendigen Kenntnisse abdeckt, darunter Flugregeln,
   Luftraumklassen, Datenschutzbestimmungen
   und aktuelle gesetzliche Änderungen.

3. Absolvierung der praktischen Schulung: Nehmen Sie
   an unserer praxisorientierten Schulung teil,
   die praktische Flugübungen, Navigationsszenarien 
   und reale Anwendungsfälle umfasst. Hier lernen
   Sie, die Drohne sicher zu steuern und auf 
   verschiedene Situationen zu reagieren.

4. Kenntnis der Drohnentechnik: Verstehen Sie die Technik
   Ihrer Drohne. Unsere Schulung deckt
   grundlegende technische Aspekte ab, von der Steuerung
   bis zur GPS-Navigation.
    
    """

    course_info_popup = Popup(title="Vorbereitungskurs", content=Label(text=course_info_text),
                              size_hint=(None, None), size=(400, 600))
    close_button = Button(text="zurück", on_press=course_info_popup.dismiss,
                          size_hint=(None, None), size=(50, 30), pos_hint={'top': 0.95, 'right': 1})
    course_info_popup.content.add_widget(close_button)
    course_info_popup.open()


if __name__ == '__main__':
    MyButtonsApp().run()
