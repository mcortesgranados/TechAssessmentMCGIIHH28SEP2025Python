from app.domain.services.product_domain_service import ProductDomainService
from app.adapters.events.product_event_service import ProductEventService
from app.adapters.repositories.product_repository_impl import ProductRepositoryImpl
from app.application.dto.product_update_dto import ProductUpdateDTO

class ProductApplicationService:
    def __init__(self, repository=None, domain_service=None, event_service=None):
        self.repository = repository or ProductRepositoryImpl()
        self.domain_service = domain_service or ProductDomainService()
        self.event_service = event_service or ProductEventService()

    def create_product(self, product_data: dict):  # <-- product_data debe ser dict
        # Create from repository
        product = self.repository.create_product(product_data)
        # Validate service domain
        if self.domain_service.is_sellable(product):
            # Publish event with infrastructure service
            self.event_service.publish_product_created(product)
        return product
    
    def update_product(self, product_id: int, update_dto: ProductUpdateDTO):
        update_data = update_dto.dict(exclude_unset=True)  # Only include provided fields
        product = self.repository.update_product(product_id, update_data)
        # Validate service domain
        if self.domain_service.is_sellable(product):
            # Publish event with infrastructure service
            self.event_service.publish_product_updated(product)
        return product    
    
    def delete_product(self, product_id: int) -> bool:
        deleted = self.repository.delete_product(product_id)
        return deleted    