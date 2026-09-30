from __future__ import annotations

import importlib.util
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).with_name("find_passenger_boardings.py")
SPEC = importlib.util.spec_from_file_location("find_passenger_boardings", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FindPassengerBoardingsTest(unittest.TestCase):
    def test_api_url_supports_mounted_pocketbase(self) -> None:
        self.assertEqual(
            MODULE.pocketbase_api_url(
                "https://uat-qrverify.opsioc.com/api/", "/collections/x/records"
            ),
            "https://uat-qrverify.opsioc.com/api/api/collections/x/records",
        )

    def test_map_record(self) -> None:
        record = {
            "id": "event-1",
            "boarding_location_id": "location-1",
            "boarding_time": "2026-09-30 01:02:03Z",
            "bus_shift": "08:00",
            "user_id": "account-1",
            "created": "2026-09-30 01:02:04Z",
            "scan_failure_reason": "",
            "scan_status": "success",
            "tenant_name": "Tenant A",
            "expand": {
                "device_id": {"expand": {"bus_id": {"name": "Bus 1"}}},
                "trip_id": {"expand": {"route_id": {"name": "Route 1"}}},
            },
        }

        result = MODULE.map_record(record, "account-1", "admin@example.com")

        self.assertEqual(result["Bus Reference"], "Bus 1")
        self.assertEqual(result["Route Name"], "Route 1")
        self.assertEqual(result["Customer"], "account-1")
        self.assertEqual(result["Last Modified"], "")
        self.assertEqual(result["Modified User"], "admin@example.com")

    def test_print_table_has_header_and_row(self) -> None:
        row = {field: "" for field in MODULE.FIELD_NAMES}
        row["Event Id"] = "event-1"
        output = io.StringIO()

        with redirect_stdout(output):
            MODULE.print_table([row])

        rendered = output.getvalue()
        self.assertIn("| Boarding Location", rendered)
        self.assertIn("event-1", rendered)


if __name__ == "__main__":
    unittest.main()
