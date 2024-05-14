import functools

from jax.typing import ArrayLike
import jax.numpy as jnp

from .layer import Layer, SerializableLayer
from . import com

class Model:
    def __init__(self, layers: list[Layer]):
        self.layers = layers

    def infer(self, input_: ArrayLike) -> ArrayLike:
        activations_com = jnp.int16(input_ * (1 << com.FRACTION_BITS))

        for layer in self.layers:
            activations_com = layer.infer(activations_com)

        return activations_com

    def serialize(self) -> dict:
        is_serializable = lambda layer: issubclass(type(layer), SerializableLayer)
        serializable_layers = filter(is_serializable, self.layers)

        serialized_layers = list(map(lambda layer: layer.serialize(), serializable_layers))

        return {
            'layers': serialized_layers
        }
