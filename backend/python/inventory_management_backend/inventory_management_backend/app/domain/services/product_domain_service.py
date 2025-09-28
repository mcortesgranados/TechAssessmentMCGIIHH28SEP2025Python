class ProductDomainService:
    def can_activate(self, product):
        return product.stock > 0 and product.is_verified
    
    def is_sellable(self, product):
        """
        Returns True if the product is sellable (stock > 0 and active).
        """
        return getattr(product, "stock", 0) > 0