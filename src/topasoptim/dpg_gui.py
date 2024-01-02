from OptimizerModel import OptimizerModel
from TopasModel import Topas, TopasConnection
from typing import Literal, TYPE_CHECKING
import dataclasses as dc
from imgui_bundle import imgui, immapp, implot
import numpy as np
import time

imgui_ctx = imgui_bundle.imgui_ctx


@dc.dataclass
class AppState:
    """Application state"""

    last_update: float = dc.field(init=False, default=time.time())
    mode: Literal["alignment", "optimization"] = "optimization"
    wavelength: float = 689.0
    integration_time: float = 30.0
    last_x: np.ndarray = dc.field(init=False)
    last_y: np.ndarray = dc.field(init=False)

    def __post_init__(self):
        self.update_xy()

    def update_xy(self):
        """Update the x and y values"""
        self.last_x = np.linspace(0, 10, 100)
        self.last_y = np.sin(self.last_x+time.time()) + \
            np.random.randn(100)*0.1
        cur_time = time.time()
        self.last_update = cur_time

    def update_motors(self):
        """Update the motor information"""
        imgui.log_text("Updating motors")

    def load_positions(self):
        """Load the positions"""
        imgui.log_text("Loading positions")


app_state = AppState()


def spec_settings(app_state: AppState):
    imgui.set_next_item_open(True)
    with imgui_ctx.tree_node("Spectrometer Settings"):
        with imgui_ctx.begin_disabled():

            imgui.push_item_width(200)
            if (mode := imgui.combo("Mode", current_item=0, items=["alignment", "optimization"]))[0]:

                app_state.mode = mode[0]
            if (wavelength := imgui.input_float("Wavelength [nm]", app_state.wavelength, step=5., format="%.1f"))[0]:
                app_state.wavelength = wavelength[0]
            if (integration_time := imgui.input_float("Integration Time [s]", app_state.integration_time, step=1., format="%.1f"))[0]:
                app_state.integration_time = integration_time[1]

            imgui.pop_item_width()


def topas_settings(app_state: AppState):
    imgui.set_next_item_open(True)
    if imgui.tree_node("Topas Settings"):
        if imgui.button("Update Motors"):
            app_state.update_motors()
        if imgui.button("Load Positions"):
            app_state.load_positions()
        imgui.tree_pop()
    return
    for topas_motor in app_state.topas.motors.values():
        imgui.set_next_item_open(True)
        if imgui.tree_node(topas_motor.title):
            imgui.begin_disabled()
            imgui.push_item_width(200)
            imgui.text(f"Index: {topas_motor.index}")
            imgui.text(f"Actual Position: {topas_motor.actual_position}")
            imgui.text(f"Target Position: {topas_motor.target_position}")
            imgui.pop_item_width()
            imgui.end_disabled()
            imgui.tree_pop()
        imgui.tree_pop()


def gui():
    """The GUI function"""

    app_state.update_xy()

    imgui.columns(2, "columns1", border=True)
    imgui.set_column_width(-1, 400)
    topas_settings(app_state)

    spec_settings(app_state)

    imgui.next_column()
    imgui.set_column_width(-1, imgui.get_window_width() - 400)
    if implot.begin_plot("Spectrum Plot", (-1, 400)):
        implot.setup_axes("Time", "Amplitude")
        implot.set_next_line_style(weight=5)
        implot.plot_scatter("My Line Plot", app_state.last_x, app_state.last_y)
        implot.end_plot()
    if implot.begin_plot("Optimization Plot", (-1, 400)):
        implot.setup_axes("Time", "Amplitude")
        implot.plot_line("My Line Plot", app_state.last_x, app_state.last_y)
        implot.end_plot()
    imgui.log()


immapp.run(
    gui_function=gui,  # The Gui function to run
    window_title="TopasOpt!",  # the window title
    window_size_auto=True,  # Auto size the application window given its widgets
    # Uncomment the next line to restore window position and size from previous run
    window_restore_previous_geometry=True,
    fps_idle=-1,
    with_implot=True,
)
