def calculate_dough_ingredients(num_balls, ball_weight, hydration_percent):
    """
    Berechnet alle Zutatenmengen basierend auf Rezept-Parametern.
    
    Args:
        num_balls (int): Anzahl der Teigkugeln
        ball_weight (float): Gewicht pro Teigkugel in Gramm
        hydration_percent (float): Hydration in Prozent (z.B. 65.0 für 65%)
    
    Returns:
        dict: Dictionary mit Zutatenmengen
            - flour (float): Mehlmenge in Gramm
            - water (float): Wassermenge in Gramm
            - salt (float): Salzanteil in Gramm
    """
    # Gesamtmehlmenge wird aus Anzahl Kugeln und Kugelgewicht berechnet
    total_dough_weight = num_balls * ball_weight
    
    # Berechnung der Mehlmenge basierend auf Hydration und Salzanteil
    # Gesamtgewicht = Mehl + Wasser + Salz
    # Wasser = Mehl * (hydration_percent / 100)
    # Salz = Mehl * 0.02
    # total_dough_weight = Mehl + Mehl * (hydration_percent / 100) + Mehl * 0.02
    # total_dough_weight = Mehl * (1 + hydration_percent / 100 + 0.02)
    
    flour = total_dough_weight / (1 + hydration_percent / 100 + 0.02)
    
    # Wassermenge wird basierend auf Hydration-Prozentsatz berechnet
    water = flour * (hydration_percent / 100)
    
    # Salzanteil ist standardmäßig 2% der Mehlmenge
    salt = flour * 0.02
    
    return {
        'flour': flour,
        'water': water,
        'salt': salt
    }