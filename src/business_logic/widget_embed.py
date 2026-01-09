from typing import Dict, Any, Optional
import json
import html
from src.models.widget import Widget
from src.repositories.widget_repository import WidgetRepository


class WidgetEmbedService:
    def __init__(self, widget_repository: WidgetRepository):
        self.widget_repository = widget_repository

    def generate_widget_embed_code(
        self, 
        widget_key: str, 
        domain: str,
        theme: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generiert HTML-Code zum Einbetten des Widgets
        
        Args:
            widget_key: Eindeutiger Widget-Schlüssel
            domain: Domain von der das Widget eingebettet wird
            theme: Optional theme override
            config: Optional configuration override
            
        Returns:
            HTML embed code als String
            
        Raises:
            ValueError: Wenn Widget-Key ungültig oder Domain nicht erlaubt
        """
        # Widget-Key muss eindeutig und gültig sein
        widget = self.widget_repository.get_by_key(widget_key)
        if not widget:
            raise ValueError(f"Invalid widget key: {widget_key}")
        
        # Domain-Beschränkung wird geprüft
        if not self._is_domain_allowed(widget, domain):
            raise ValueError(f"Domain not allowed: {domain}")
        
        # Theme und Konfiguration werden in Embed-Code eingebettet
        embed_theme = theme or widget.theme or 'default'
        embed_config = config or widget.config or {}
        
        # Sichere JSON-Serialisierung für HTML
        config_json = html.escape(json.dumps(embed_config))
        theme_escaped = html.escape(embed_theme)
        widget_key_escaped = html.escape(widget_key)
        
        embed_code = f'''<div id="widget-{widget_key_escaped}" class="widget-container">
    <script type="application/json" class="widget-config">
        {config_json}
    </script>
    <script>
        (function() {{
            var script = document.createElement('script');
            script.src = '/static/js/widget.js';
            script.onload = function() {{
                if (window.WidgetLoader) {{
                    window.WidgetLoader.init({{
                        key: '{widget_key_escaped}',
                        theme: '{theme_escaped}',
                        config: {config_json},
                        container: 'widget-{widget_key_escaped}'
                    }});
                }}
            }};
            document.head.appendChild(script);
        }})();
    </script>
</div>'''
        
        return embed_code
    
    def _is_domain_allowed(self, widget: Widget, domain: str) -> bool:
        """
        Prüft ob die Domain für das Widget erlaubt ist
        
        Args:
            widget: Widget-Instanz
            domain: Zu prüfende Domain
            
        Returns:
            True wenn Domain erlaubt, False sonst
        """
        if not widget.allowed_domains:
            return True  # Keine Beschränkung
        
        # Normalisiere Domain (entferne Protokoll und Port)
        normalized_domain = domain.lower()
        if '://' in normalized_domain:
            normalized_domain = normalized_domain.split('://', 1)[1]
        if ':' in normalized_domain:
            normalized_domain = normalized_domain.split(':', 1)[0]
        
        # Prüfe gegen erlaubte Domains
        for allowed_domain in widget.allowed_domains:
            allowed_normalized = allowed_domain.lower()
            
            # Exakte Übereinstimmung
            if normalized_domain == allowed_normalized:
                return True
            
            # Wildcard-Unterstützung (*.example.com)
            if allowed_normalized.startswith('*.'):
                wildcard_domain = allowed_normalized[2:]
                if normalized_domain.endswith('.' + wildcard_domain) or normalized_domain == wildcard_domain:
                    return True
        
        return False