import tkinter as tk
from tkinter import ttk
import time


class AutocompleteGUI:

    def __init__(self, autocomplete_instance):
        self.autocomplete = autocomplete_instance
        self.root = tk.Tk()
        self.root.title("Autocomplete App")

        # Eingabefelder
        tk.Label(self.root, text="Wort:").grid(row=0, column=0)
        self.word_entry = tk.Entry(self.root)
        self.word_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Anzahl der Vorschläge (k):").grid(row=1, column=0)
        self.k_entry = tk.Entry(self.root)
        self.k_entry.grid(row=1, column=1)

        # Schaltfläche
        search_button = tk.Button(self.root, text="Suche", command=self.perform_search)
        search_button.grid(row=2, column=0, columnspan=2)

        # Ergebnisbereich
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.result_tree = ttk.Treeview(self.result_frame, columns=("Wort", "Frequenz"), show="headings")
        self.result_tree.column("Wort", width=150)
        self.result_tree.column("Frequenz", width=150)
        self.result_tree.heading("Wort", text="Wort")
        self.result_tree.heading("Frequenz", text="Frequenz")
        self.result_tree.pack(expand=True, fill="both")

        # Statusbereich
        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=4, column=0, columnspan=2)

    def perform_search(self):
        word = self.word_entry.get()
        try:
            k = int(self.k_entry.get())
        except ValueError:
            self.status_label.config(text="Bitte geben Sie eine gültige Zahl für k ein.")
            return

        # Zeitmessungen für get-Funktionen
        start_time_hash = time.perf_counter()
        get_o1_result = self.autocomplete.get_from_hash_table(word)
        time_taken_hash = time.perf_counter() - start_time_hash

        start_time_avl = time.perf_counter()
        get_ologn_result = self.autocomplete.get_from_avl_tree(word)
        time_taken_avl = time.perf_counter() - start_time_avl

        # Zeitmessung für get_k_possible_suggestions
        start_time_suggestions = time.perf_counter()
        suggestions, searched_nodes = self.autocomplete.get_k_possible_suggestions(word, k)
        time_taken_suggestions = time.perf_counter() - start_time_suggestions

        self.update_results(suggestions, searched_nodes)

        # Update GUI für get O(1), get O(log n) und get_k_possible_suggestions Ergebnisse
        self.get_o1_label.config(text=f"get O(1) Ergebnis: {get_o1_result}")
        self.get_o1_time_label.config(text=f"Laufzeit (O(1)): {time_taken_hash:.6f} Sekunden")

        self.get_ologn_label.config(text=f"get O(log n) Ergebnis: {get_ologn_result}")
        self.get_ologn_time_label.config(text=f"Laufzeit (O(log n)): {time_taken_avl:.6f} Sekunden")

        self.get_k_suggestions_time_label.config(
            text=f"Laufzeit (get_k_possible_suggestions): {time_taken_suggestions:.6f} Sekunden")

    def update_results(self, suggestions, searched_nodes):
        # Lösche alte Ergebnisse
        for i in self.result_tree.get_children():
            self.result_tree.delete(i)

        # Füge neue Ergebnisse hinzu
        for suggestion in suggestions:
            self.result_tree.insert("", "end", values=suggestion)

        # Update Status
        self.status_label.config(text=f"{len(suggestions)} Vorschläge gefunden, {searched_nodes} Knoten durchsucht.")

    def run(self):

        # Labels für get-Methoden und Laufzeiten mit zusätzlichen leeren Zeilen
        self.get_o1_label = tk.Label(self.root, text="get O(1) Ergebnis:")
        self.get_o1_label.grid(row=5, column=0, sticky="w")

        self.get_o1_time_label = tk.Label(self.root, text="Laufzeit (O(1)):")
        self.get_o1_time_label.grid(row=6, column=0, sticky="w")

        # Leere Zeile
        tk.Label(self.root, text="").grid(row=7, column=0)

        self.get_ologn_label = tk.Label(self.root, text="get O(log n) Ergebnis:")
        self.get_ologn_label.grid(row=8, column=0, sticky="w")

        self.get_ologn_time_label = tk.Label(self.root, text="Laufzeit (O(log n)):")
        self.get_ologn_time_label.grid(row=9, column=0, sticky="w")

        # Leere Zeile
        tk.Label(self.root, text="").grid(row=10, column=0)

        self.get_k_suggestions_time_label = tk.Label(self.root, text="Laufzeit (get_k_possible_suggestions):")
        self.get_k_suggestions_time_label.grid(row=11, column=0, columnspan=2, sticky="w")

        # Leere Zeile
        tk.Label(self.root, text="").grid(row=12, column=0)

        self.root.mainloop()