import pytest

from glmpy import dimensions

def test_negative_height():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=-6,
            surface_length=40,
            surface_width=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == "height must be a positive value."
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedCone(
            height=-3,
            surface_radius=15,
            num_vals=3,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == "height must be a positive value."

def test_negative_surface_dimension():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=-40,
            surface_width=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "surface_length must be a positive value."
    )
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=40,
            surface_width=-40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "surface_width must be a positive value."
    )
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedCone(
            height=3,
            surface_radius=-15,
            num_vals=3,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == "surface_radius must be a positive value."

def test_num_vals_less_than_2():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=40,
            surface_width=40,
            num_vals=1,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
       "num_vals must be greater than or equal 2."
    )
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedCone(
            height=3,
            surface_radius=15,
            num_vals=1,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
       "num_vals must be greater than or equal 2."
    )

def test_negative_side_slope():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=40,
            surface_width=40,
            num_vals=7,
            side_slope=-1/3,
            surface_elevation=0
        )
    assert str(error.value) == "side_slope must be a positive value."
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedCone(
            height=3,
            surface_radius=15,
            num_vals=3,
            side_slope=-1/3,
            surface_elevation=0
        )
    assert str(error.value) == "side_slope must be a positive value."

def test_negative_base_length():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=10,
            surface_width=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "Invalid combination of height, surface_length, and "
        "side_slope attributes. The calculated base_length of the "
        "water body is currently <= 0. base_length is calculated by "
        "(surface_length-(height/side_slope)*2). Adjust your input "
        "attributes to calculate a positive base_length value."
    )
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedPyramid(
            height=6,
            surface_length=40,
            surface_width=10,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "Invalid combination of height, surface_width, and "
        "side_slope attributes. The calculated base_width of the "
        "water body is currently <= 0. base_width is calculated by "
        "(surface_width-(height/side_slope)*2). Adjust your input "
        "attributes to calculate a positive base_width value."
    )
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedCone(
            height=3,
            surface_radius=8,
            num_vals=3,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "Invalid combination of height, surface_radius, and "
        "side_slope attributes. The calculated base_radius of the "
        "water body is currently <= 0. base_radius is calculated by "
        "(surface_radius - (height / side_slope)). Adjust your input "
        "attributes to calculate a positive base_radius value."
    )

def test_greater_num_vals_at_0_surface_elev():
    square_reservoir = dimensions.InvertedTruncatedPyramid(
        height=6,
        surface_length=40,
        surface_width=40,
        num_vals=7,
        side_slope=1/3,
        surface_elevation=0
    )
    expected_volumes = [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
    expected_areas = [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
    expected_heights = [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
    assert square_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert square_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert square_reservoir.get_heights() == pytest.approx(expected_heights)

    circular_reservoir = dimensions.InvertedTruncatedCone(
        surface_radius=15,
        height=3,
        side_slope=1/3,
        num_vals=5,
        surface_elevation=0
    )
    expected_volumes = [
        0.0, 120.60770546672065, 328.6891313818321, 
        648.1007469585319, 1102.6990214100174
    ]
    expected_areas = [
        113.09733552923255, 213.8246499849553, 346.3605900582747, 
        510.70515574919074, 706.8583470577034
    ]
    expected_heights = [-3.0, -2.25, -1.5, -0.75, 0.0]
    assert circular_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert circular_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert circular_reservoir.get_heights() == pytest.approx(expected_heights)


def test_lower_num_vals_at_0_surface_elev():
    square_reservoir = dimensions.InvertedTruncatedPyramid(
        height=6,
        surface_length=40,
        surface_width=40,
        num_vals=4,
        side_slope=1/3,
        surface_elevation=0
    )
    expected_volumes = [0.0, 224.0, 1216.0, 3552.0]
    expected_areas = [16.0, 256.0, 784.0, 1600.0]
    expected_heights = [-6.0, -4.0, -2.0, 0.0]
    assert square_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert square_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert square_reservoir.get_heights() == pytest.approx(expected_heights)

    circular_reservoir = dimensions.InvertedTruncatedCone(
        surface_radius=15,
        height=3,
        side_slope=1/3,
        num_vals=3,
        surface_elevation=0
    )
    expected_volumes = [0.0, 328.6891313818321, 1102.6990214100174]
    expected_areas = [113.09733552923255, 346.3605900582747, 706.8583470577034]
    expected_heights = [-3.0, -1.5, 0.0]
    assert circular_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert circular_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert circular_reservoir.get_heights() == pytest.approx(expected_heights)

def test_greater_num_vals_at_neg_3_surface_elev():
    square_reservoir = dimensions.InvertedTruncatedPyramid(
        height=6,
        surface_length=40,
        surface_width=40,
        num_vals=7,
        side_slope=1/3,
        surface_elevation=-3
    )
    expected_volumes = [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
    expected_areas = [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
    expected_heights = [-9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0]
    assert square_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert square_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert square_reservoir.get_heights() == pytest.approx(expected_heights)

    circular_reservoir = dimensions.InvertedTruncatedCone(
        surface_radius=15,
        height=3,
        side_slope=1/3,
        num_vals=5,
        surface_elevation=-3
    )
    expected_volumes = [
        0.0, 120.60770546672065, 328.6891313818321, 
        648.1007469585319, 1102.6990214100174
    ]
    expected_areas = [
        113.09733552923255, 213.8246499849553, 346.3605900582747, 
        510.70515574919074, 706.8583470577034
    ]
    expected_heights = [-6.0, -5.25, -4.5, -3.75, -3.0]
    assert circular_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert circular_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert circular_reservoir.get_heights() == pytest.approx(expected_heights)

def test_lower_num_vals_at_neg_3_surface_elev():
    square_reservoir = dimensions.InvertedTruncatedPyramid(
        height=6,
        surface_length=40,
        surface_width=40,
        num_vals=4,
        side_slope=1/3,
        surface_elevation=-3
    )
    expected_volumes = [0.0, 224.0, 1216.0, 3552.0]
    expected_areas = [16.0, 256.0, 784.0, 1600.0]
    expected_heights = [-9.0, -7.0, -5.0, -3.0]
    assert square_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert square_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert square_reservoir.get_heights() == pytest.approx(expected_heights)

    circular_reservoir = dimensions.InvertedTruncatedCone(
        surface_radius=15,
        height=3,
        side_slope=1/3,
        num_vals=3,
        surface_elevation=-3
    )
    expected_volumes = [0.0, 328.6891313818321, 1102.6990214100174]
    expected_areas = [113.09733552923255, 346.3605900582747, 706.8583470577034]
    expected_heights = [-6.0, -4.5, -3.0]
    assert circular_reservoir.get_volumes() == pytest.approx(expected_volumes)
    assert circular_reservoir.get_surface_areas() == pytest.approx(
        expected_areas
    )
    assert circular_reservoir.get_heights() == pytest.approx(expected_heights)