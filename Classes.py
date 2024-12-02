import json
import xml.etree.ElementTree as ET

class GraphicEditorError(Exception):
    """Базовый класс для исключений графического редактора."""
    pass

class ShapeError(GraphicEditorError):
    """Исключение для ошибок, связанных с фигурами."""
    pass

class Shape:
    def __init__(self, name):
        self.name = name

    def draw(self):
        raise NotImplementedError("Метод draw() должен быть реализован в подклассах.")

    def to_dict(self):
        return {"type": self.name}

    def to_xml(self):
        shape_elem = ET.Element(self.name)
        return shape_elem

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        if radius <= 0:
            raise ShapeError("Радиус должен быть положительным.")
        self.radius = radius

    def draw(self):
        return f"Рисуем круг с радиусом {self.radius}"

    def to_dict(self):
        return {**super().to_dict(), "radius": self.radius}

    def to_xml(self):
        shape_elem = super().to_xml()
        radius_elem = ET.SubElement(shape_elem, "radius")
        radius_elem.text = str(self.radius)
        return shape_elem

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        if width <= 0 or height <= 0:
            raise ShapeError("Ширина и высота должны быть положительными.")
        self.width = width
        self.height = height

    def draw(self):
        return f"Рисуем прямоугольник шириной {self.width} и высотой {self.height}"

    def to_dict(self):
        return {**super().to_dict(), "width": self.width, "height": self.height}

    def to_xml(self):
        shape_elem = super().to_xml()
        width_elem = ET.SubElement(shape_elem, "width")
        height_elem = ET.SubElement(shape_elem, "height")
        width_elem.text = str(self.width)
        height_elem.text = str(self.height)
        return shape_elem

class GraphicEditor:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        if not isinstance(shape, Shape):
            raise ShapeError("Объект должен быть экземпляром класса Shape.")
        self.shapes.append(shape)

    def draw_all(self):
        for shape in self.shapes:
            print(shape.draw())

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([shape.to_dict() for shape in self.shapes], f, ensure_ascii=False, indent=4)

    def save_to_xml(self, filename):
        root = ET.Element("shapes")
        for shape in self.shapes:
            root.append(shape.to_xml())
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            shapes_data = json.load(f)
            for shape_data in shapes_data:
                if shape_data["type"] == "Circle":
                    self.add_shape(Circle(shape_data["radius"]))
                elif shape_data["type"] == "Rectangle":
                    self.add_shape(Rectangle(shape_data["width"], shape_data["height"]))

    def load_from_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        for shape_elem in root:
            if shape_elem.tag == "Circle":
                radius = float(shape_elem.find("radius").text)
                self.add_shape(Circle(radius))
            elif shape_elem.tag == "Rectangle":
                width = float(shape_elem.find("width").text)
                height = float(shape_elem.find("height").text)
                self.add_shape(Rectangle(width, height))
