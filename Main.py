from AutocompleteNgrams import AutocompleteNgrams
from AutocompleteGUI import AutocompleteGUI
import time


def main():

    start_time = time.time()
    autocomplete: AutocompleteNgrams = AutocompleteNgrams(
        "C:\\Users\\cihat\\OneDrive\\Masaüstü\\Modulen\\ALgo\\Praktikum1_AutoComplete\\StudentTask\\1_gram.csv")
    end_time = time.time()
    print(f"Ausführungszeit Initialisierung: {end_time - start_time} Sekunden")

    gui = AutocompleteGUI(autocomplete)
    gui.run()


if __name__ == "__main__":
    main()




    """
    Alternativer Test ohne GUI:
    while True:
        test_string = input("Geben Sie einen Wortanfang ein (oder 'exit' zum Beenden): ")
        if test_string.lower() == 'exit':
            break

        k = int(input("Wie viele Vorschläge möchten Sie erhalten? "))

        suggestions, searched_nodes = autocomplete.get_k_possible_suggestions(test_string, k)
        print(f"Top {k} suggestions: {suggestions}")
        print(f"Anzahl der durchsuchten Knoten: {searched_nodes}\n")
    """