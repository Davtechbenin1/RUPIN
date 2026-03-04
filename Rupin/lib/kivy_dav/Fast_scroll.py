from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock


class FastStackLayout(StackLayout):
    pass


class FastScroll(ScrollView):
    container = ObjectProperty(None)
    all_widgets = ListProperty([])
    buffer_zone = NumericProperty(50)  # marge pour pré-chargement autour

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = FastStackLayout(size_hint=(None, None))
        self.container.bind(minimum_height=self._update_height,
                            minimum_width=self._update_width)
        self.add_widget(self.container)

        self.scroll_type = ['bars', 'content']
        self.bar_width = 10
        self.effect_cls = 'ScrollEffect'

        self.bind(scroll_y=self._on_scroll, scroll_x=self._on_scroll)
        Clock.schedule_once(lambda dt: self.update_visible_widgets(), 1)

    def add_widget_to_stack(self, widget):
        self.all_widgets.append(widget)
        self.container.add_widget(widget)

    def _update_height(self, instance, value):
        self.container.height = value

    def _update_width(self, instance, value):
        self.container.width = value

    def _on_scroll(self, *args):
        Clock.schedule_once(lambda dt: self.update_visible_widgets(), 0)

    def update_visible_widgets(self):
        # Pour l'instant on ne fait pas de suppression : on affiche tout
        # (optimisation avancée possible avec calculs de coordonnées)
        pass  # À implémenter plus tard si besoin de très gros volumes


class TestApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        scroll = FastScroll(size_hint=(1, 1), do_scroll_y=True, do_scroll_x=True)

        # Génère des widgets complexes (ici boutons) à scroller
        for i in range(1000):
            b = Button(text=f'Bouton {i}', size_hint=(None, None), size=(150, 100))
            scroll.add_widget_to_stack(b)

        root.add_widget(scroll)
        return root


if __name__ == '__main__':
    TestApp().run()