# Este archivo hace que el directorio views sea un paquete de Python
from .dashboard_view import DashboardView
from .registration_view import RegistrationView
from .search_view import SearchView

__all__ = ['DashboardView', 'RegistrationView', 'SearchView'] 