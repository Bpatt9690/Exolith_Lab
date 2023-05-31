import unittest
from axisReset import axis_reset
from xMove import xMove
from yMove import yMove
from xyForward import xyMove


class TestXY(unittest.TestCase):
    def test_reset(self):
        # Test if elevation resets properly.
        xy = axis_reset()
        self.assertTrue(xy.x_axis_reset())
        self.assertTrue(xy.y_axis_reset())
    def test_x_movement(self):
        # Test if x motors can move x distance successfully
        self.xMove(6)
        self.xMove(-6)

    def test_y_movement(self):
        # Test if y motors can move y distance successfully
        self.yMove(6)
        self.yMove(-6)
    def test_xy_movement(self):
        # Idea 1: Simple test of just telling the x and y motors to move to one location
        # Idea 2: To test for any mechanical limitations, we should try moving the bin to each "corner
        self.xyMove(6, 6)
        self.xyMove(6, -6)
        self.xyMove(-6, 6)
        self.xyMove(-6, -6)


if __name__ == "__main__":
    unittest.main()