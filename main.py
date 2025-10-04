import tkinter as tk
from shapely.geometry import Polygon

class PolygonDrawer:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.polygons = []      # список завершённых полигонов
        self.current = []       # текущий рисуемый полигон
        self.result_ids = []    # ID линий результата

        # Кнопки
        frame = tk.Frame(master)
        frame.pack()
        tk.Button(frame, text="Union", command=lambda: self.apply_op("union")).pack(side="left")
        tk.Button(frame, text="Intersection", command=lambda: self.apply_op("intersection")).pack(side="left")
        tk.Button(frame, text="Difference", command=lambda: self.apply_op("difference")).pack(side="left")
        tk.Button(frame, text="Clear", command=self.clear).pack(side="left")

        # События мыши
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.finish_polygon)

    # Добавление точки
    def add_point(self, event):
        x, y = event.x, event.y
        self.current.append((x, y))
        if len(self.current) > 1:
            self.canvas.create_line(self.current[-2][0], self.current[-2][1],
                                    self.current[-1][0], self.current[-1][1], fill="black")
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

    # Завершение полигона
    def finish_polygon(self, event=None):
        if len(self.current) > 2:
            self.canvas.create_line(self.current[-1][0], self.current[-1][1],
                                    self.current[0][0], self.current[0][1], fill="black")
            self.polygons.append(Polygon(self.current))
        self.current = []

    # Рисование результата
    def draw_result(self, poly, color="red"):
        # Удаляем старые линии
        for rid in self.result_ids:
            self.canvas.delete(rid)
        self.result_ids = []

        if poly.is_empty:
            return

        # Поддержка Polygon и MultiPolygon
        if poly.geom_type == 'Polygon':
            polys = [poly]
        elif poly.geom_type == 'MultiPolygon':
            polys = poly.geoms
        else:
            return  # другие типы игнорируем

        for p in polys:
            coords = list(p.exterior.coords)
            for i in range(len(coords)-1):
                line_id = self.canvas.create_line(coords[i][0], coords[i][1],
                                                  coords[i+1][0], coords[i+1][1],
                                                  fill=color, width=2)
                self.result_ids.append(line_id)

    # Операции
    def apply_op(self, op):
        if not self.polygons:
            return

        color = "black"
        if op == "union":
            color = "blue"
        elif op == "intersection":
            color = "green"
        elif op == "difference":
            color = "red"

        result = self.polygons[0]
        for p in self.polygons[1:]:
            if op == "union":
                result = result.union(p)
            elif op == "intersection":
                result = result.intersection(p)
            elif op == "difference":
                result = result.difference(p)

        self.draw_result(result, color=color)


    def clear(self):
        self.canvas.delete("all")
        self.polygons = []
        self.result_ids = []

def main():
    root = tk.Tk()
    app = PolygonDrawer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
