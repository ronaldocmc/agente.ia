"""Baseline obrigatório sem API, gratuito e offline."""
from shared_rule import Pedido,consultar
for email in ('ana@exemplo.test','bruno@exemplo.test','carla@exemplo.test'):
    print(email,consultar(Pedido(email=email,actor=email)))
