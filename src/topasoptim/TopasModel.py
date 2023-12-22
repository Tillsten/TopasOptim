from __future__ import annotations

import dataclasses

import requests


@dataclasses.dataclass
class TopasMotor:
    name: str
    index: int
    actual_position: int
    target_position: int
    actual_position_in_units: float
    target_position_in_units: float
    unit_name: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["Title"],
            index=data["Index"],
            actual_position=data["ActualPosition"],
            target_position=data["TargetPosition"],
            actual_position_in_units=data["ActualPositionInUnits"],
            target_position_in_units=data["TargetPositionInUnits"],
            unit_name=data["UnitName"],
        )


@dataclasses.dataclass
class MotorPositionSetting:
    name: str
    comment: str
    folder: str
    GUID: str
    positions: list[tuple[int, int]]
    time_created: str

    @classmethod
    def from_dict(cls, data):
        pos = [(m["Key"], m["Value"]) for m in data["MotorPositions"]]
        return cls(
            name=data["Name"],
            comment=data["Comment"],
            folder=data["Folder"],
            GUID=data["GUID"],
            positions=pos,
            time_created=data["TimeCreated"],
        )


@dataclasses.dataclass(kw_only=True)
class TopasConnection:
    baseAddress: str

    @classmethod
    def from_info(
        cls,
        ip_address: str = "127.0.0.1",
        port: str = "8000",
        serial_number: str = "14187",
        version="v0",
    ):
        url = f"http://{ip_address}:{port}/{serial_number}/{version}/PublicAPI"
        return cls(baseAddress=url)

    def put(self, url, data):
        return requests.put(self.baseAddress + url, json=data)

    def post(self, url, data):
        return requests.post(self.baseAddress + url, json=data)

    def get(self, url):
        return requests.get(self.baseAddress + url).json()


@dataclasses.dataclass
class Topas:
    """
    OPA Model

    Attributes
    ----------
    motors : dict[str, TopasMotor]
        Dictionary of motors
    index_to_motor : dict[int, TopasMotor]
        Dictionary of motor indices to motors
    connection : TopasConnection
        Connection to the OPA
    positions : dict[str, MotorPositionSetting]
    """

    motors: dict[str, TopasMotor] = dataclasses.field(default_factory=dict)
    index_to_motor: dict[int, TopasMotor] = dataclasses.field(default_factory=dict)
    connection: TopasConnection = dataclasses.field(default_factory=TopasConnection)
    positions: dict[str, MotorPositionSetting] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.update_motors()
        self.index_to_motor = {motor.index: motor for motor in self.motors.values()}
        self.load_positions()

    def update_motors(self):
        "Update the motor information"
        data = self.connection.get("/Motors/AllProperties")["Motors"]
        self.motors = {motor["Title"]: TopasMotor.from_dict(motor) for motor in data}

    def get_actual_positions(self) -> dict[str, int]:
        "Get the actual positions of the motors"
        self.update_motor_positions()
        return {name: motor.actual_position for name, motor in self.motors.items()}

    def get_target_positions(self) -> dict[str, int]:
        "Get the target positions of the motors"
        self.update_motor_positions()
        return {name: motor.target_position for name, motor in self.motors.items()}

    def is_open(self) -> bool:
        "Get the status of the shutter"
        return self.get("/ShutterInterlock/IsShutterOpen")

    def toggle_shutter(self, shutter_open: bool):
        "Toggle the shutter"
        self.connection.put("/ShutterInterlock/OpenCloseShutter", shutter_open)

    def get_authentication_status(self) -> bool:
        "Get the authentication status of the caller"
        return self.connection.get("/CallerHasAccess")

    def update_motor_positions(self) -> None:
        "Get the motor positions"
        props = self.connection.get("/Motors/PropertiesThatChangeOften")
        for m in props:
            motor = self.index_to_motor[m["Index"]]
            motor.actual_position = m["ActualPosition"]
            motor.target_position = m["TargetPosition"]
            motor.target_position_in_units = m["TargetPositionInUnits"]
            motor.actual_position_in_units = m["ActualPositionInUnits"]

    def move_motor(self, name: str, position: int) -> None:
        "Move a motor to a position"
        motor_index = self.motors[name].index
        self.connection.put(f"/TargetPosition?id={motor_index}", int(position))

    def move_motors(self, positions: dict[str, int]) -> None:
        "Move multiple motors to positions"
        for name, position in positions.items():
            self.move_motor(name, position)

    def save_positions(self, name: str, folder: str) -> str:
        "Save the current motor positions"
        id = self.connection.post("/SaveCurrent", {"Name": name, "Folder": folder})
        self.load_positions()
        return id

    def load_positions(self) -> None:
        "Load all saved motor positions"
        data = self.connection.get("/Positions")
        self.positions = {m["GUID"]: MotorPositionSetting.from_dict(m) for m in data}

    def goto_position_by_name(self, name: str) -> None:
        """Move the motors to a saved position called `name`
        If there are multiple positions with the same name, the first one is used"""
        first_match = next(p for p in self.positions if p.name == name)
        self.goto_position_by_id(first_match.GUID)

    def goto_position_by_id(self, guid: str) -> None:
        """Move the motors to a saved position with a given GUID"""
        self.connection.put("/MoveMotorsToPosition", guid)
