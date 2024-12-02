from Classes import Circle, Rectangle, GraphicEditor, ShapeError, GraphicEditorError

def main():
    editor = GraphicEditor()

    try:
        # Создание фигур
        circle = Circle(5)
        rectangle = Rectangle(10, 20)

        # Добавление фигур в редактор
        editor.add_shape(circle)
        editor.add_shape(rectangle)

        # Рисование всех фигур
        editor.draw_all()

        # Сохранение в JSON
        editor.save_to_json("shapes.json")
        print("Фигуры сохранены в shapes.json")

        # Сохранение в XML
        editor.save_to_xml("shapes.xml")
        print("Фигуры сохранены в shapes.xml")

        # Загрузка из JSON
        new_editor = GraphicEditor()
        new_editor.load_from_json("shapes.json")
        print("\nЗагруженные фигуры из JSON:")
        new_editor.draw_all()

        # Загрузка из XML
        another_editor = GraphicEditor()
        another_editor.load_from_xml("shapes.xml")
        print("\nЗагруженные фигуры из XML:")
        another_editor.draw_all()

    except ShapeError as e:
        print(f"Ошибка: {e}")
    except GraphicEditorError as e:
        print(f"Ошибка графического редактора: {e}")

if __name__ == "__main__":
    main()
