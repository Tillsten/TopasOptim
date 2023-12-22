import topasoptim.TopasModel as tm
import json


test_props = """{
  "Motors": [
    {
      "Acceleration": 25,
      "ActualPosition": 19,
      "ActualPositionInSuperUnits": 0,
      "ActualPositionInUnits": 0,
      "Affix": 0,
      "Current": 34,
      "Factor": 0,
      "ForbiddenRanges": [
        {
          "From": 0,
          "IsEnabled": true,
          "To": 0
        },
        {
          "From": 0,
          "IsEnabled": true,
          "To": 0
        }
      ],
      "Index": 86,
      "IsHoming": false,
      "IsLeftSwitchPressed": false,
      "IsRightSwitchPressed": false,
      "MaximalPosition": 42,
      "MaximalPositionInUnits": 0,
      "MaximalVelocity": 32,
      "MinimalPositionInUnits": 0,
      "MinimalVelocity": 94,
      "NamedPositions": [
        {
          "Name": "Untitled",
          "Position": 17,
          "ShortName": ""
        },
        {
          "Name": "Untitled",
          "Position": 94,
          "ShortName": ""
        }
      ],
      "PulseDivision": 26,
      "RampDivision": 16,
      "StepDivision": 42,
      "SuperUnitsCalculator": {
        "Expression": "x",
        "ParserType": 0,
        "UnitName": "",
        "ValidUnitsRange": {
          "From": -1E+300,
          "To": 1E+300
        }
      },
      "TargetPosition": 89,
      "TargetPositionInSuperUnits": 0,
      "TargetPositionInUnits": 0,
      "Title": "Local High School Dropouts Cut in Half",
      "UnitName": "year",
      "ZeroOffset": 5
    },
    {
      "Acceleration": 35,
      "ActualPosition": 47,
      "ActualPositionInSuperUnits": 0,
      "ActualPositionInUnits": 0,
      "Affix": 0,
      "Current": 91,
      "Factor": 0,
      "ForbiddenRanges": [
        {
          "From": 0,
          "IsEnabled": true,
          "To": 0
        },
        {
          "From": 0,
          "IsEnabled": true,
          "To": 0
        }
      ],
      "Index": 95,
      "IsHoming": false,
      "IsLeftSwitchPressed": false,
      "IsRightSwitchPressed": false,
      "MaximalPosition": 44,
      "MaximalPositionInUnits": 0,
      "MaximalVelocity": 37,
      "MinimalPositionInUnits": 0,
      "MinimalVelocity": 19,
      "NamedPositions": [
        {
          "Name": "Untitled",
          "Position": 37,
          "ShortName": ""
        },
        {
          "Name": "Untitled",
          "Position": 49,
          "ShortName": ""
        }
      ],
      "PulseDivision": 9,
      "RampDivision": 95,
      "StepDivision": 81,
      "SuperUnitsCalculator": {
        "Expression": "x",
        "ParserType": 0,
        "UnitName": "",
        "ValidUnitsRange": {
          "From": -1E+300,
          "To": 1E+300
        }
      },
      "TargetPosition": 19,
      "TargetPositionInSuperUnits": 0,
      "TargetPositionInUnits": 0,
      "Title": "Officials Determine Crash Occured When Plane Hit the Ground",
      "UnitName": "cosby",
      "ZeroOffset": 53
    }
  ]
}"""

changing_props = """[
  {
    "ActualPosition": 75,
    "ActualPositionInSuperUnits": 0,
    "ActualPositionInUnits": 0,
    "Index": 38,
    "IsHoming": false,
    "IsLeftSwitchPressed": false,
    "IsRightSwitchPressed": false,
    "TargetPosition": 69,
    "TargetPositionInSuperUnits": 0,
    "TargetPositionInUnits": 0
  },
  {
    "ActualPosition": 69,
    "ActualPositionInSuperUnits": 0,
    "ActualPositionInUnits": 0,
    "Index": 23,
    "IsHoming": false,
    "IsLeftSwitchPressed": false,
    "IsRightSwitchPressed": false,
    "TargetPosition": 25,
    "TargetPositionInSuperUnits": 0,
    "TargetPositionInUnits": 0
  }
]"""


class MockConnection:
    def get(self, url):
        if url == "/Motors/AllProperties":
            return json.loads(test_props)
        elif url == "/Motors/PropertiesThatChangeOften":
            return json.loads(changing_props)
        else:
            msg = f"Unknown url: {url}"
            raise ValueError(msg)


def test_from_dict():
    """Test the from_dict method of TopasModel."""
    data = json.loads(test_props)
    tm.TopasMotor.from_dict(data["Motors"][0])


def test_update_motors():
    tm.Topas(connection=MockConnection())
