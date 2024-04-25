from typing import List
from itertools import product

class URLGenerator:
  def __init__(self, template: str, static_params: dict) -> None:
    self._template = template
    self._static_params = static_params
    self.param_values = {}
    self.param_order = []

  @classmethod
  def create(cls, template: str = '', static_params: dict = {}) -> 'URLGenerator':
    return cls(template, static_params)

  def template(self, template: str) -> 'URLGenerator':
    self._template = template
    return self

  def static_params(self, static_params: dict) -> 'URLGenerator':
    self._static_params = static_params
    return self

  def each(self, values: List, name: str) -> 'URLGenerator':
    if (name in self.param_values):
      raise ValueError(f"Parameter {name} already defined")
    self.param_values[name] = values
    self.param_order.append(name)
    return self

  def generate(self) -> List[str]:
    urls = []
    # Generate the product of all parameter values in order
    for values in product(*[self.param_values[param] for param in self.param_order]):
      params = dict(zip(self.param_order, values))
      params.update(self._static_params)
      urls.append(self._template.format(**params))
    return urls