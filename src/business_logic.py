from datetime import datetime, timedelta
from typing import Dict, Any

def calculate_timing_schedule(recipe_data: Dict[str, Any], target_finish_time: datetime) -> Dict[str, datetime]:
    """
    Berechnet den Zeitplan für die Teigzubereitung basierend auf dem gewünschten Fertigstellungszeitpunkt.
    
    Args:
        recipe_data: Dictionary mit Rezeptdaten inklusive Zeiten für verschiedene Schritte
        target_finish_time: Gewünschter Fertigstellungszeitpunkt
    
    Returns:
        Dictionary mit Zeitpunkten für jeden Arbeitsschritt
    """
    # Zeiten aus den Rezeptdaten extrahieren (in Minuten)
    knet_zeit = recipe_data.get('knet_zeit', 10)  # Standard: 10 Minuten
    stockgare_zeit = recipe_data.get('stockgare_zeit', 120)  # Standard: 2 Stunden
    portionier_zeit = recipe_data.get('portionier_zeit', 15)  # Standard: 15 Minuten
    stueckgare_zeit = recipe_data.get('stueckgare_zeit', 60)  # Standard: 1 Stunde
    back_zeit = recipe_data.get('back_zeit', 30)  # Standard: 30 Minuten
    
    # Rückwärts vom Fertigstellungszeitpunkt rechnen
    schedule = {}
    
    # Fertigstellung
    schedule['fertigstellung'] = target_finish_time
    
    # Backende (Backzeit vor Fertigstellung)
    schedule['back_ende'] = target_finish_time
    schedule['back_start'] = target_finish_time - timedelta(minutes=back_zeit)
    
    # Stückgare Ende (beginnt nach dem Portionieren, endet beim Backstart)
    schedule['stueckgare_ende'] = schedule['back_start']
    schedule['stueckgare_start'] = schedule['stueckgare_ende'] - timedelta(minutes=stueckgare_zeit)
    
    # Portionieren (vor Stückgare)
    schedule['portionier_ende'] = schedule['stueckgare_start']
    schedule['portionier_start'] = schedule['portionier_ende'] - timedelta(minutes=portionier_zeit)
    
    # Stockgare Ende (beginnt nach dem Kneten, endet beim Portionieren)
    schedule['stockgare_ende'] = schedule['portionier_start']
    schedule['stockgare_start'] = schedule['stockgare_ende'] - timedelta(minutes=stockgare_zeit)
    
    # Kneten (vor Stockgare)
    schedule['knet_ende'] = schedule['stockgare_start']
    schedule['knet_start'] = schedule['knet_ende'] - timedelta(minutes=knet_zeit)
    
    # Startzeit der gesamten Produktion
    schedule['produktion_start'] = schedule['knet_start']
    
    return schedule