import unittest
from GPS import GPS_Data
from solarAlignment import sensorGroupCheck, azimuthLogic
from axisReset import axis_reset
from elevationTracking import elevation_tracker
from azimuthTracking import azimuth_tracker


class TestAlignment(unittest.TestCase):
    gps = GPS_Data()

    def test_sensors(self):
        self.assertTrue(sensorGroupCheck())

    def test_reset(self):
        # Test if elevation resets properly.
        ar = axis_reset()
        self.assertTrue(ar.elevation_reset())
        # self.assertTrue(ar.x_axis_reset())
        # self.assertTrue(ar.y_axis_reset())
    def test_gps(self):
        # Tests if gps gets correct location and produces correct elevation angle.
        self.gps.getCurrentCoordinates()
        self.assertAlmostEqual(int(self.gps.gps_dict["Time UTC"]), 204010, -3, "GPS UTC Time is not almost equal to true time.")
        self.assertAlmostEqual(int(self.gps.gps_dict["Lattitude"]), float(2833.2327) / 100, 4, "GPS Lattitude is not almost equal to true lattitude.")
        self.assertAlmostEqual(int(self.gps.gps_dict["Longitude"]), float(8111.11886) / 100, 4, "GPS Longitude is not almost equal to true lattitude.")
        self.assertAlmostEqual(int(self.gps.gps_dict["Alt Above Sea Level"]), 34.2, -1, "GPS angle is not almost equal to true angle.")

    def test_elev_angle(self):
        # Tests if elevation angle is accurate.
        self.assertTrue(elevation_tracker.solarElevationPositioning(45))
    def test_azim_movement(self):
        # Tests if azimuth turns as intended.
        self.assertTrue(azimuthLogic())


if __name__ == "__main__":
    unittest.main()