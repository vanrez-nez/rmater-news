from base.serialize import SerializableDict

class ArticleLocation(SerializableDict):

  def __init__(self, fields: dict = None) -> None:
    fields = fields or {}
    self.id = fields.get('id', 'none')
    self.place_id = fields.get('place_id')
    self.country = fields.get('country')
    self.state = fields.get('state')
    self.city = fields.get('city')
    self.county = fields.get('county')
    self.town = fields.get('town')
    self.osm_id = fields.get('osm_id')
    self.osm_type = fields.get('osm_type')
    self.rank_address = fields.get('rank_address')
    self.lat = fields.get('lat')
    self.lon = fields.get('lon')
    super().__init__(self.__dict__)

  @property
  def type(self):
    ranges = { 'country': [4, 4], 'state': [5, 9], 'county': [10, 12], 'city': [13, 16], 'town': [17, 21] }
    for key, (start, end) in ranges.items():
      if start <= self.rank_address <= end:
        return key
    return None

  @property
  def name(self) -> str:
    t = self.type
    if (t == 'country' and self.country):
      return self.country
    if (t == 'state' and self.state):
      return self.state
    if (t == 'county' and self.county):
      return self.county
    if (t == 'city' and self.city):
      return self.city
    if (t == 'town' and self.town):
      return self.town
    return self.town or self.city or self.county or self.state or self.country