from typing import Optional, List
from src.models.widget import Widget


class WidgetRepository:
    def __init__(self):
        # In-memory storage for now, would be replaced with actual database
        self._widgets = {}
        self._widgets_by_key = {}
    
    def get_by_id(self, widget_id: int) -> Optional[Widget]:
        """Holt Widget anhand der ID"""
        return self._widgets.get(widget_id)
    
    def get_by_key(self, widget_key: str) -> Optional[Widget]:
        """Holt Widget anhand des eindeutigen Schlüssels"""
        return self._widgets_by_key.get(widget_key)
    
    def save(self, widget: Widget) -> Widget:
        """Speichert Widget"""
        if widget.id is None:
            widget.id = len(self._widgets) + 1
        
        self._widgets[widget.id] = widget
        self._widgets_by_key[widget.key] = widget
        return widget
    
    def get_all(self) -> List[Widget]:
        """Holt alle Widgets"""
        return list(self._widgets.values())
    
    def delete(self, widget_id: int) -> bool:
        """Löscht Widget anhand der ID"""
        widget = self._widgets.get(widget_id)
        if widget:
            del self._widgets[widget_id]
            del self._widgets_by_key[widget.key]
            return True
        return False