from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import servicios, cursos, productos, pagos, auth

router = DefaultRouter()
router.register(r'servicios', servicios.ServicioViewSet)
router.register(r'reservas', servicios.ReservaViewSet, basename='reserva')
router.register(r'cursos', cursos.CursoViewSet)
router.register(r'inscripciones', cursos.InscripcionCursoViewSet, basename='inscripcion')
router.register(r'productos', productos.ProductoViewSet)
router.register(r'pedidos', productos.PedidoProductoViewSet, basename='pedido')
router.register(r'metodos-pago', pagos.MetodoPagoViewSet)
router.register(r'bitacora-pagos', pagos.BitacoraPagoViewSet, basename='bitacora')

urlpatterns = [
    path('', include(router.urls)),
    path('iniciar-pago-paypal/', pagos.BitacoraPagoViewSet.as_view({'post': 'iniciar_pago_paypal'}), name='iniciar_pago_paypal'),
    path('confirmar-pago-paypal/', pagos.BitacoraPagoViewSet.as_view({'post': 'confirmar_pago_paypal'}), name='confirmar_pago_paypal'),
    path('register/', auth.UserRegistrationView.as_view(), name='register'),
    path('login/', auth.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', auth.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]