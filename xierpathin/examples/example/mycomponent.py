
from xierpathin.components.component import Component

class MyComponent(Component):

    def build(self, b):
        b.div(class_='myComponent')
        for component in self.components:
            component.build(b)
        b._div()

