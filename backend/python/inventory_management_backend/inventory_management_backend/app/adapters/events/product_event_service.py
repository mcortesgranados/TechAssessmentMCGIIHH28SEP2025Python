class ProductEventService:
    """
    Service responsible for publishing product-related events to the event broker.

    Methods
    -------
    publish_product_created(product)
        Publishes an event indicating that a new product has been created.

    publish_product_updated(product)
        Publishes an event indicating that an existing product has been updated.
    """

    def publish_product_created(self, product):
        """
        Publish a 'product created' event to the event broker.

        Parameters
        ----------
        product : Product
            The product instance that has been created.
        """
        # Publish event to broker
        pass

    def publish_product_updated(self, product):
        """
        Publish a 'product updated' event to the event broker.

        Parameters
        ----------
        product : Product
            The product instance that has been updated.
        """
        # Publish event to broker
        pass    