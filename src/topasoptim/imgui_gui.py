from OptimizerModel import OptimizerModel
from TopasModel import Topas, TopasConnection
from typing import Literal, TYPE_CHECKING
import dataclasses as dc
from imgui_bundle import imgui, immapp, implot, hello_imgui
import numpy as np
import time
import threading


@dc.dataclass
class AppState:
    """Application state"""

    last_update: float = dc.field(init=False, default=time.time())
    mode: Literal["alignment", "optimization"] = "alignment"
    wavelength: float = 689.0
    integration_time: float = 30.0
    last_x: np.ndarray = dc.field(init=False)
    last_y: np.ndarray = dc.field(init=False)

    optimizer_hist: np.ndarray = dc.field(init=False)
    optimizer_hist_x: np.ndarray = dc.field(init=False)

    stop_optimization: bool = False
    is_running: bool = True
    runner: threading.Thread = dc.field(init=False)

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

    def save_app_state(self):
        """Save the application state"""
        imgui.log_text("Saving application state")

    def start_loop(self):
        """Start the loop"""
        self.is_running = True
        self.runner = threading.Thread(
            target=self.run_loop, daemon=True).start()

    def stop_loop(self):
        """Stop the loop"""
        self.is_running = False

    def run_loop(self):
        """Run updates in a loop"""
        while self.is_running:
            self.update_xy()


app_state = AppState()


def spec_settings(app_state: AppState):
    imgui.set_next_item_open(True)
    if imgui.tree_node("Spectrometer Settings"):
        imgui.begin_disabled()
        imgui.push_item_width(200)
        if (mode := imgui.combo("Mode", current_item=0, items=["alignment", "optimization"]))[0]:

            app_state.mode = mode[0]
        if (wavelength := imgui.input_float("Wavelength [nm]", app_state.wavelength, step=5., format="%.1f"))[0]:
            app_state.wavelength = wavelength[0]
        if (integration_time := imgui.input_float("Integration Time [s]", app_state.integration_time, step=1., format="%.1f"))[0]:
            app_state.integration_time = integration_time[1]

        imgui.pop_item_width()
        imgui.end_disabled()
        imgui.tree_pop()


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

    # app_state.update_xy()
    # hello_imgui.log_gui()
    if app_state.mode == "alignment":
        imgui.columns(2, "columns1", border=True)
        imgui.set_column_width(-1, 400)
        topas_settings(app_state)
        spec_settings(app_state)
        if imgui.button("Start"):
            app_state.mode = "optimization"
        imgui.next_column()
        imgui.set_column_width(-1, imgui.get_window_width() - 400)
        if implot.begin_plot("Spectrum Plot", (-1, 400)):
            implot.setup_axes("Time", "Amplitude")
            implot.set_next_line_style(weight=5)
            implot.plot_scatter(
                "My Line Plot", app_state.last_x, app_state.last_y)
            implot.end_plot()
        if implot.begin_plot("Optimization Plot", (-1, 400)):
            implot.setup_axes("Time", "Amplitude")
            implot.plot_line("My Line Plot", app_state.last_x,
                             app_state.last_y)
            implot.end_plot()
    else:
        imgui.text("Iteration: 0")
        imgui.same_line()
        imgui.text("Evaluations: 0.0")
        imgui.same_line()
        if imgui.button("Stop"):
            app_state.mode = "alignment"

        if implot.begin_plot("Spec Plot", (-1, -1)):
            implot.setup_axes("Time", "Amplitude")
            implot.plot_line("My Line Plot", app_state.last_x,
                             app_state.last_y)
            implot.end_plot()


app_state.start_loop()
params = immapp.RunnerParams()
params.callbacks.show_gui = gui
params.callbacks.before_exit = app_state.stop_loop
params.app_window_params.window_title = "TopasOpt!"
params.fps_idling.enable_idling = False
params.fps_idling.remember_enable_idling = False


def setup_fonts():
    style = imgui.get_style()
    style.scale_all_sizes(2)
    imgui.


params.callbacks.post_init = setup_fonts

add_on_params = immapp.AddOnsParams()
add_on_params.with_implot = True
immapp.run(params, add_on_params)
