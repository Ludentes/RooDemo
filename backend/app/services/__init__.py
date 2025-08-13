# Define __all__ to make classes available for dependency injection
# Use lazy imports to avoid circular dependencies

__all__ = [
    "TransactionService",
    "TransactionValidator",
    "TransactionBatchProcessor",
    "TransactionQueryService"
]

# Import functions to get the classes when needed
def get_transaction_service():
    from app.services.transaction_service import TransactionService
    return TransactionService

def get_transaction_validator():
    from app.services.transaction_validator import TransactionValidator
    return TransactionValidator

def get_transaction_batch_processor():
    from app.services.transaction_batch_processor import TransactionBatchProcessor
    return TransactionBatchProcessor

def get_transaction_query_service():
    from app.services.transaction_query_service import TransactionQueryService
    return TransactionQueryService