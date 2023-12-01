from .start import router as start_router
from .admin import router as admin_router
from .funnel import router as funnel_router
from .end_message import router as end_message_router

routers = (
    start_router,
    admin_router,
    funnel_router,
    end_message_router,
)
