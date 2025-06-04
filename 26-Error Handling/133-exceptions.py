from fastapi import FastAPI, HTTPException, Request, Response, status


class FastShipError(Exception):
    """Base exception for all exceptions in fastship api"""
    # status_code to be returned for this exception
    # when it is handled
    status = status.HTTP_400_BAD_REQUEST


class EntityNotFound(FastShipError):
    """Entity not found in database"""

    status = status.HTTP_404_NOT_FOUND


class ClientNotAuthorized(FastShipError):
    """Client is not authorized to perform the action"""

    status = status.HTTP_401_UNAUTHORIZED


class ClientNotVerified(FastShipError):
    """Client is not verified"""

    status = status.HTTP_401_UNAUTHORIZED


class NothingToUpdate(FastShipError):
    """No data provided to update"""


class BadCredentials(FastShipError):
    """User email or password is incorrect"""

    status = status.HTTP_401_UNAUTHORIZED


class InvalidToken(FastShipError):
    """Access token is invalid or expired"""

    status = status.HTTP_401_UNAUTHORIZED


class DeliveryPartnerNotAvailable(FastShipError):
    """Delivery partner/s do not service the destination"""

    status = status.HTTP_406_NOT_ACCEPTABLE


class DeliveryPartnerCapacityExceeded(FastShipError):
    """Delivery partner has reached their max handling capacity"""

    status = status.HTTP_406_NOT_ACCEPTABLE


def _get_handler(status: int, detail: str):
    # Define
    def handler(request: Request, exception: Exception) -> Response:
        # DEBUG PRINT STATEMENT 👇
        from rich import print, panel
        print(
            panel.Panel(
                exception.__class__.__name__,
                title="Handled Exception",
                border_style="red",
            ),
        )
        # DEBUG PRINT STATEMENT 👆
        
        # Raise HTTPException with given status and detail
        # can return JSONResponse as well
        raise HTTPException(
            status_code=status,
            detail=detail,
        )
    # Return ExceptionHandler required with given
    # status and detail for HTTPExcetion above
    return handler


def add_exception_handlers(app: FastAPI):
    # Get all subclass of 👇, our custom exceptions
    exception_classes = FastShipError.__subclasses__()

    for exception_class in exception_classes:
        # Add exception handler
        app.add_exception_handler(
            # Custom exception class
            exception_class,
            # Get handler function
            _get_handler(
                status=exception_class.status,
                detail=exception_class.__doc__,
            ),
        )
