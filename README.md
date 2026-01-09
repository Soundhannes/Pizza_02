# Einheiten-Umrechner

Ein Python-Programm zum Umrechnen von Gewichts- und Längenmaßen.

## Features

- Gewichtsumrechnung zwischen verschiedenen Einheiten
- Längenumrechnung zwischen verschiedenen Einheiten
- Interaktive Benutzeroberfläche
- Unterstützte Einheiten werden angezeigt

## Unterstützte Einheiten

### Gewicht
- g (Gramm)
- kg (Kilogramm)
- mg (Milligramm)
- lb (Pfund)
- oz (Unze)
- t (Tonne)

### Länge
- m (Meter)
- cm (Zentimeter)
- mm (Millimeter)
- km (Kilometer)
- in (Zoll)
- ft (Fuß)
- yd (Yard)
- mi (Meile)

## Verwendung

```bash
python src/converter.py
```

## Tests ausführen

```bash
python src/test_converter.py
```

## Beispiele

```python
from src.converter import UnitConverter

converter = UnitConverter()

# Gewicht umrechnen
result = converter.convert_weight(1, 'kg', 'g')  # 1000.0

# Länge umrechnen
result = converter.convert_length(1, 'm', 'cm')  # 100.0
```