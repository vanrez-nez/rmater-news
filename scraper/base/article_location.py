class ArticleLocation:
  def __init__(self, fields: dict) -> None:
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
