import pytest
import math
from glmpy import dimensions


def test_non_numeric_height():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height='foo',
            surface_length=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(
        error.value) == (
            f"height must be a numeric value. Got type {type('foo')}."
    )


def test_non_numeric_surface_length():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length="foo",
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(
        error.value) == (
            f"surface_length must be a numeric value. Got type {type('foo')}."
    )

def test_non_numeric_num_vals():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=40,
            num_vals="foo",
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(
        error.value) == (
            f"num_vals must be an integer value. Got type {type('foo')}."
    )

def test_non_numeric_surface_elevation():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation="foo"
        )
    assert str(
        error.value) == (
            "surface_elevation must be a numeric value. Got type "
            f"{type('foo')}."
    )

def test_non_numeric_side_slope():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=40,
            num_vals=7,
            side_slope="foo",
            surface_elevation=0
        )
    assert str(
        error.value) == (
            f"side_slope must be a numeric value. Got type {type(f'foo')}."
    )

def test_negative_height():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=-6,
            surface_length=40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == "height must be a positive value."


def test_negative_surface_length():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=-40,
            num_vals=7,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
        "surface_length must be a positive value."
    )

def test_num_vals_less_than_2():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=40,
            num_vals=1,
            side_slope=1/3,
            surface_elevation=0
        )
    assert str(error.value) == (
       "num_vals must be greater than or equal 2."
    )

def test_negative_side_slope():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=40,
            num_vals=7,
            side_slope=-1/3,
            surface_elevation=0
        )
    assert str(error.value) == "side_slope must be a positive value."


def test_negative_base_length():
    with pytest.raises(ValueError) as error:
        dimensions.InvertedTruncatedSquarePyramid(
            height=6,
            surface_length=10,
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

def test_num_vals_is_7_surface_elev_is_0():
    dam = dimensions.InvertedTruncatedSquarePyramid(
        height=6,
        surface_length=40,
        num_vals=7,
        side_slope=1/3,
        surface_elevation=0
    )
    expected_volumes = [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
    expected_areas = [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
    expected_heights = [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)
    assert dam.get_surface_areas() == pytest.approx(expected_areas)
    assert dam.get_heights() == pytest.approx(expected_heights)

def test_num_vals_is_4_surface_elev_is_0():
    dam = dimensions.InvertedTruncatedSquarePyramid(
        height=6,
        surface_length=40,
        num_vals=4,
        side_slope=1/3,
        surface_elevation=0
    )
    expected_volumes = [0.0, 224.0, 1216.0, 3552.0]
    expected_areas = [16.0, 256.0, 784.0, 1600.0]
    expected_heights = [-6.0, -4.0, -2.0, 0.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)
    assert dam.get_surface_areas() == pytest.approx(expected_areas)
    assert dam.get_heights() == pytest.approx(expected_heights)

def test_num_vals_is_7_surface_elev_is_neg_3():
    dam = dimensions.InvertedTruncatedSquarePyramid(
        height=6,
        surface_length=40,
        num_vals=7,
        side_slope=1/3,
        surface_elevation=-3
    )
    expected_volumes = [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
    expected_areas = [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
    expected_heights = [-9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)
    assert dam.get_surface_areas() == pytest.approx(expected_areas)
    assert dam.get_heights() == pytest.approx(expected_heights)

def test_num_vals_is_4_surface_elev_is_neg_3():
    dam = dimensions.InvertedTruncatedSquarePyramid(
        height=6,
        surface_length=40,
        num_vals=4,
        side_slope=1/3,
        surface_elevation=-3
    )
    expected_volumes = [0.0, 224.0, 1216.0, 3552.0]
    expected_areas = [16.0, 256.0, 784.0, 1600.0]
    expected_heights = [-9.0, -7.0, -5.0, -3.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)
    assert dam.get_surface_areas() == pytest.approx(expected_areas)
    assert dam.get_heights() == pytest.approx(expected_heights)