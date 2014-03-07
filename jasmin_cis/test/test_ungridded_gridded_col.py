from nose.tools import istest, raises
import numpy
from jasmin_cis.data_io.Coord import CoordList
from jasmin_cis.col_implementations import UngriddedGriddedColocator, mean, CubeCellConstraint, \
    BinningCubeCellConstraint
from jasmin_cis.test.test_util.mock import make_dummy_ungridded_data_single_point, make_square_5x3_2d_cube, \
    make_dummy_ungridded_data_two_points_with_different_values, make_dummy_1d_ungridded_data, \
    make_dummy_1d_ungridded_data_with_invalid_standard_name


@istest
@raises(ValueError)
def test_throws_value_error_with_empty_coord_list():
    sample_cube = make_square_5x3_2d_cube()
    empty_coord_list = CoordList()

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    col.colocate(points=sample_cube, data=empty_coord_list, constraint=con, kernel=mean())[0]


@istest
def test_fill_value_for_cube_cell_constratint():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(99, 99, 0.0)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_fill_value_for_cube_cell_constratint_default_fill_value():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(99, 99, 0.0)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint()

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[float('Inf'), float('Inf'), float('Inf')],
                                   [float('Inf'), float('Inf'), float('Inf')],
                                   [float('Inf'), float('Inf'), float('Inf')],
                                   [float('Inf'), float('Inf'), float('Inf')],
                                   [float('Inf'), float('Inf'), float('Inf')]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_single_point_results_in_single_value_in_cell():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(0.5, 0.5, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_single_point_results_in_single_value_in_cell_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(0.5, 0.5, 1.2)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_two_points_in_a_cell_results_in_mean_value_in_cell():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_two_points_with_different_values(0.5, 0.5, 1.2, 1.4)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.3, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_two_points_in_a_cell_results_in_mean_value_in_cell_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_two_points_with_different_values(0.5, 0.5, 1.2, 1.4)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.3, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lat_bounday_appears_in_both_cells():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(2.5, 0.0, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lat_bounday_appears_in_both_cells_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(2.5, 0.0, 1.2)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, 1.2, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lon_bounday_appears_in_both_cells():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(0.0, 2.5, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lon_bounday_appears_in_both_cells_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(0.0, 2.5, 1.2)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lat_lon_bounday_appears_in_four_cells():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(2.5, 2.5, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_point_on_a_lat_lon_bounday_appears_in_four_cells_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(2.5, 2.5, 1.2)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, 1.2, 1.2],
                                   [-999.9, -999.9, -999.9]])

    assert numpy.allclose(out_cube.data.filled(), expected_result, atol=1.0e-15)


@istest
def test_single_point_outside_grid_is_excluded():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(99, 99, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_single_point_outside_grid_is_excluded_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(99, 99, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_single_point_on_grid_corner_is_counted_once():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(10, 5, 1.2)

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, 1.2]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_single_point_on_grid_corner_is_counted_once_using_binning():
    sample_cube = make_square_5x3_2d_cube()
    data_point = make_dummy_ungridded_data_single_point(10, 5, 1.2)

    col = UngriddedGriddedColocator()
    con = BinningCubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_point, constraint=con, kernel=mean())[0]

    expected_result = numpy.array([[-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, -999.9],
                                   [-999.9, -999.9, 1.2]])

    assert (out_cube.data.filled() == expected_result).all()


@istest
def test_data_with_no_standard_name():
    sample_cube = make_square_5x3_2d_cube()
    data_points = make_dummy_1d_ungridded_data()

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_points, constraint=con, kernel=mean())[0]


@istest
def test_data_with_invalid_standard_name():
    sample_cube = make_square_5x3_2d_cube()
    data_points = make_dummy_1d_ungridded_data_with_invalid_standard_name()

    col = UngriddedGriddedColocator()
    con = CubeCellConstraint(fill_value=-999.9)

    out_cube = col.colocate(points=sample_cube, data=data_points, constraint=con, kernel=mean())[0]

