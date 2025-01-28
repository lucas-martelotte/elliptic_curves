def get_xyz_axis(z_axis: int) -> tuple[int, int, int]:
    """Returns the xy-axis based on the z-axis following a convention."""
    if z_axis == 0:
        return (1, 2, 0)
    elif z_axis == 1:
        return (0, 2, 1)
    return (0, 1, 2)


def get_abc_axis(z_axis: int) -> tuple[int, int, int]:
    """Returns the abc-axis based on the z-axis following the convention."""
    if z_axis == 0:
        return (2, 0, 1)
    elif z_axis == 1:
        return (0, 2, 1)
    return (0, 1, 2)


def get_abc_axis_and_plane_name(z_axis: int) -> tuple[str, str]:
    if z_axis == 0:
        return "A", "BC"
    elif z_axis == 1:
        return "B", "AC"
    elif z_axis:
        return "C", "AB"
    raise ValueError("z_axis must be between 0 and 2.")
