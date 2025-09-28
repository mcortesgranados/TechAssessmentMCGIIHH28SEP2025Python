from app.domain.services.product_domain_service import ProductDomainService
from app.adapters.events.product_event_service import ProductEventService
from app.adapters.repositories.product_repository_impl import ProductRepositoryImpl

class ProductApplicationService:
    def __init__(self, repository=None, domain_service=None, event_service=None):
        self.repository = repository or ProductRepositoryImpl()
        self.domain_service = domain_service or ProductDomainService()
        self.event_service = event_service or ProductEventService()

    def create_product(self, product_data: dict):  # <-- product_data debe ser dict
        # Crear producto en el repositorio
        product = self.repository.create_product(product_data)
        # Validar con servicio de dominio
        if self.domain_service.is_sellable(product):
            # Publicar evento con servicio de infraestructura
            self.event_service.publish_product_created(product)
        return product