import dataclasses as dc
from typing import Any, Protocol

from imgui_bundle import imgui, immapp


class DataclassProtocol(Protocol):
    __dataclass_fields__: dict
    __dataclass_params__: dict


def text_view(name: str, value: Any) -> None:
    """Create a text view of the value"""
    imgui.text(f"{name}: {value}")


def float_view(name: str, value: float) -> None:
    """Create a float view of the value"""
    imgui.text(f"{name}: {value:.3f}")


def int_view(name: str, value: int) -> None:
    """Create an int view of the value"""
    imgui.text(f"{name}: {value: d}")


def bool_view(name: str, value: bool) -> None:
    """Create a bool view of the value"""
    imgui.begin_disabled()
    imgui.checkbox(name, value)
    imgui.end_disabled()


def dataclass_view(name: str, dc: DataclassProtocol) -> None:
    imgui.begin_group()
    dc.make_view()
    imgui.end_group()


def default_view(name: str, value: Any) -> None:
    """Create a default view of the value"""
    imgui.text(f"{name}: {value}")


TYPE_MAP = {
    float: float_view,
    int: int_view,
    bool: bool_view,
    str: text_view,
}


def unique_label(name, dc: DataclassProtocol) -> str:
    """Create a unique label for the dataclass"""
    return f"{name}##{id(dc)}"


def text_edit_view(name: str, dc: DataclassProtocol) -> None:
    """Create a text edit view of the value"""
    current_val = getattr(dc, name)
    changed, new_val = imgui.input_text(unique_label(name, dc), current_val)
    if changed:
        setattr(dc, name, new_val)


def float_edit_view(name: str, dc: DataclassProtocol) -> None:
    """Create a float edit view of the value"""
    current_val = getattr(dc, name)
    changed, new_val = imgui.input_float(unique_label(name, dc), current_val)
    if changed:
        setattr(dc, name, new_val)


def int_edit_view(name: str, dc: DataclassProtocol) -> None:
    """Create an int edit view of the value"""
    current_val = getattr(dc, name)
    changed, new_val = imgui.input_int(unique_label(name, dc), current_val)
    if changed:
        setattr(dc, name, new_val)


def bool_edit_view(name: str, dc: DataclassProtocol) -> None:
    """Create a bool edit view of the value"""
    current_val = getattr(dc, name)
    changed, new_val = imgui.checkbox(unique_label(name, dc), current_val)
    if changed:
        setattr(dc, name, new_val)


def default_edit_view(name: str, dc: DataclassProtocol) -> None:
    return default_view(name, getattr(dc, name))


TYPE_EDIT_MAP = {
    float: float_edit_view,
    int: int_edit_view,
    bool: bool_edit_view,
    str: text_edit_view,
}


def register_type_map(ty, view, edit_view):
    """Register a type mapping"""
    TYPE_MAP[ty] = view
    TYPE_EDIT_MAP[ty] = edit_view


@dc.dataclass
class DataView:
    dc: DataclassProtocol = dc.field()

    def make_view(self) -> None:
        imgui.begin_group()
        for name, field in self.dc.__dataclass_fields__.items():
            view = TYPE_MAP.get(field.type, default_view)
            view(name, getattr(self.dc, name))
        imgui.end_group()

    def make_edit_view(self) -> None:
        imgui.begin_group()
        for name, field in self.dc.__dataclass_fields__.items():
            TYPE_EDIT_MAP.get(field.type, default_edit_view)(name, self.dc)
        imgui.end_group()


@dc.dataclass()
class Tester:
    test_str: str = "Hello"
    test_int: int = 1
    test_float: float = 1.0
    test_bool: bool = True


def gui_test() -> None:
    imgui.begin("Dataclass View")
    dv.make_view()
    dv.make_edit_view()
    imgui.end()


if __name__ == "__main__":
    dv = DataView(dc=Tester())
    immapp.run(gui_test)
