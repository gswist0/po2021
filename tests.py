import unittest
from app import log_in_check, get_trip_title, get_user_id_from_entry, check_if_amount_correct, get_user_data_from_id

class TestAppLogic(unittest.TestCase):
    def test_log_in_check(self):
        self.assertTrue(log_in_check("matiz","matikox"))
        self.assertFalse(log_in_check("adwad","adwqda"))
        self.assertFalse(log_in_check("",""))
        self.assertFalse(log_in_check("matiz","a"))

    def test_get_trip_title(self):
        self.assertEqual(get_trip_title(0),"LipiecZakopane")
        self.assertNotEqual(get_trip_title(0),"aaaa")
        self.assertEqual(get_trip_title(5),"LutyNarty")
    
    def test_get_user_id_from_entry(self):
        self.assertEqual(get_user_id_from_entry("x;x;87;x"),87)
        self.assertEqual(get_user_id_from_entry("x;x;1;x"),1)
        self.assertNotEqual(get_user_id_from_entry("x;x;11;x"),12)
        with self.assertRaises(IndexError):
            get_user_id_from_entry("aaaaabcd2")

    def test_check_if_amount_correct(self):
        self.assertTrue(check_if_amount_correct("21"))
        self.assertTrue(check_if_amount_correct("121.33"))
        self.assertFalse(check_if_amount_correct("dwadziescia piec i pol"))
        self.assertFalse(check_if_amount_correct(""))
    
    def test_get_user_data_from_id(self):
        self.assertEqual(get_user_data_from_id(1),["abcd1","123","1","Zenon Marciniak"])
        self.assertNotEqual(get_user_data_from_id(1),["123","abcd1","1","Zenon Marciniak"])

if __name__ == "__main__":
    unittest.main()