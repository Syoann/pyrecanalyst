class Tile:
    """Represents a map tile."""
    def __init__(self, x, y, terrain, elevation):
        # X coordinate
        self.x = x

        # Y coordinate
        self.y = y

        # Terrain type ID
        self.terrain = terrain

        # Elevation level (0-7)
        self.elevation = elevation
