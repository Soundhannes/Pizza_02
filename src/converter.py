class UnitConverter:
    def __init__(self):
        # Gewichtseinheiten in Gramm
        self.weight_units = {
            'g': 1,
            'kg': 1000,
            'mg': 0.001,
            'lb': 453.592,
            'oz': 28.3495,
            't': 1000000
        }
        
        # Längeneinheiten in Meter
        self.length_units = {
            'm': 1,
            'cm': 0.01,
            'mm': 0.001,
            'km': 1000,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.34
        }
    
    def convert_weight(self, value, from_unit, to_unit):
        """Konvertiert Gewichtseinheiten"""
        if from_unit not in self.weight_units or to_unit not in self.weight_units:
            raise ValueError("Ungültige Gewichtseinheit")
        
        # Konvertiere zu Gramm, dann zur Zieleinheit
        grams = value * self.weight_units[from_unit]
        result = grams / self.weight_units[to_unit]
        return result
    
    def convert_length(self, value, from_unit, to_unit):
        """Konvertiert Längeneinheiten"""
        if from_unit not in self.length_units or to_unit not in self.length_units:
            raise ValueError("Ungültige Längeneinheit")
        
        # Konvertiere zu Meter, dann zur Zieleinheit
        meters = value * self.length_units[from_unit]
        result = meters / self.length_units[to_unit]
        return result
    
    def get_available_weight_units(self):
        """Gibt verfügbare Gewichtseinheiten zurück"""
        return list(self.weight_units.keys())
    
    def get_available_length_units(self):
        """Gibt verfügbare Längeneinheiten zurück"""
        return list(self.length_units.keys())


def main():
    converter = UnitConverter()
    
    print("=== Einheiten-Umrechner ===")
    print("1. Gewicht umrechnen")
    print("2. Länge umrechnen")
    print("3. Verfügbare Einheiten anzeigen")
    print("4. Beenden")
    
    while True:
        try:
            choice = input("\nWählen Sie eine Option (1-4): ").strip()
            
            if choice == '1':
                print(f"Verfügbare Gewichtseinheiten: {', '.join(converter.get_available_weight_units())}")
                value = float(input("Wert eingeben: "))
                from_unit = input("Von Einheit: ").strip().lower()
                to_unit = input("Zu Einheit: ").strip().lower()
                
                result = converter.convert_weight(value, from_unit, to_unit)
                print(f"{value} {from_unit} = {result:.6f} {to_unit}")
                
            elif choice == '2':
                print(f"Verfügbare Längeneinheiten: {', '.join(converter.get_available_length_units())}")
                value = float(input("Wert eingeben: "))
                from_unit = input("Von Einheit: ").strip().lower()
                to_unit = input("Zu Einheit: ").strip().lower()
                
                result = converter.convert_length(value, from_unit, to_unit)
                print(f"{value} {from_unit} = {result:.6f} {to_unit}")
                
            elif choice == '3':
                print(f"Gewichtseinheiten: {', '.join(converter.get_available_weight_units())}")
                print(f"Längeneinheiten: {', '.join(converter.get_available_length_units())}")
                
            elif choice == '4':
                print("Auf Wiedersehen!")
                break
                
            else:
                print("Ungültige Auswahl. Bitte wählen Sie 1-4.")
                
        except ValueError as e:
            print(f"Fehler: {e}")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()