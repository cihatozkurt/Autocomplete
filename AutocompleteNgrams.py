import csv
from AVLTree import AVLTree
import heapq


class AutocompleteNgrams:

    def __init__(self, filename: str):
        """ Initialisiert AutocompleteNgrams

        :param filename: Der Dateipfad zum csv file
        """
        self.avl_tree: AVLTree = AVLTree()
        self.hash_table = {}
        self.read_csv_file(filename)

    def read_csv_file(self, filename: str):
        """ Liest die Daten von einem csv file und fügt sie dem self.avl_tree hinzu.

        :param filename: Der Dateipfad zum csv file
        """
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            for row in csv_reader:
                ngram = row[0]  # N-Gramm ist in Spalte 1
                frequency = int(row[1])  # Häufigkeit in Spalte 2
                self.avl_tree.insert(ngram, frequency) # Übergibt N-Gramm als Key und frequency als Value
                self.hash_table[ngram] = frequency # speichern der Datensätze in Dictionary für get mit O(1) Laufzeit


    def get_from_avl_tree(self, ngram: str):
        found_node = self.avl_tree.find(ngram)
        if found_node is not None:
            return found_node.get_value()
        else:
            return None

    def get_from_hash_table(self, ngram: str):
        # Methode, um das N-gramm in der Hashtabelle zu finden
        # Konstante Zeitkomplexität
        return self.hash_table.get(ngram)

    def get(self, ngram: str, use_hash_table: bool = False):
        """
        :param ngram: Das N-gram, welches gefunden werden soll.
        :param use_hash_table: Wenn True, wird die Hashtabelle verwendet, sonst der AVL-Baum.
        :return: Wenn das ngram gefunden wurde, wird die Frequenz des N-grams zurückgegeben,
                 falls es nicht gefunden werden konnte wird None zurückgegeben.
        """
        if use_hash_table:
            return self.get_from_hash_table(ngram)
        else:
            return self.get_from_avl_tree(ngram)

    def get_k_possible_suggestions(self, input_string: str, k: int):
        """
        Gibt eine Liste der k besten Vorschläge für den gegebenen Eingabestring zurück.
        :param input_string: Der String für den Fortsetzungen vorgeschlagen werden.
        :param k: Die Anzahl an gewünschten Vorschlägen.
        :return: Eine Liste mit den k besten Vorschlägen und die Anzahl untersuchter Nodes im AVL Baum.
        """
        heap, searched_nodes = self.avl_tree.find_most_likely_ngrams(input_string)

        # Extrahiere die Top-k Elemente aus dem Heap
        suggestions = []
        while heap and len(suggestions) < k:
            frequency, ngram = heapq.heappop(heap)
            suggestions.append((ngram, -frequency))  # Umkehren der negierten Frequenz

        return suggestions, searched_nodes

