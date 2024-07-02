import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYears(self):
        years = self._model._years
        for y in years:
            self._view._DD_anno.options.append(ft.dropdown.Option(data=y, text=y, on_click=self._choice_year))
        self._view.update_page()

    def _choice_year(self, e):
        if e.control.data is None:
            self._selected_year = None
        else:
            self._selected_year = e.control.data
            self._model._clearShapes()
            self._model._fillShapes(self._selected_year)
            self.fillDDShapes()

    def fillDDShapes(self):
        shapes = self._model._shapes
        for s in shapes:
            self._view._DD_shape.options.append(ft.dropdown.Option(data=s, text=s, on_click=self._choice_shape))
        self._view.update_page()

    def _choice_shape(self, e):
        if e.control.data is None:
            self._selected_shape = None
        else:
            self._selected_shape = e.control.data



    def handleGrafo(self, e):
        self._model._crea_grafo(self._selected_shape, self._selected_year)
        nNodi, nArchi = self._model.get_dettagli_grafo()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato. Il grafo ha {nNodi} nodi e {nArchi} archi."))
        peso_nodi = self._model.peso_nodi()
        for n in peso_nodi:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]}: {n[1]}"))
        self._view._btn_percorso.disabled = False
        self._view.update_page()

    def handlePercorso(self, e):
        path, distanza = self._model._handle_percorso()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso lungo {distanza} km."))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p[0]} --> {p[1]}: weight = {p[3]}, distance = {p[2]} km"))
        self._view.update_page()

