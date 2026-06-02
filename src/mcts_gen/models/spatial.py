from dataclasses import dataclass

@dataclass(frozen=True)
class SpatialZone:
    """Defines a 3D bounding box for spatial partitioning."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float

    def contains(self, x: float, y: float, z: float) -> bool:
        """Checks if a point (x, y, z) is within the zone."""
        return (self.x_min <= x <= self.x_max and
                self.y_min <= y <= self.y_max and
                self.z_min <= z <= self.z_max)
