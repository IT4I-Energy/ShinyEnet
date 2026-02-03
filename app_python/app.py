from pathlib import Path
from shiny import ui, render, reactive, App
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from opt_func import simple_ga_optimize_pyr,objective
icon_title = "Description"
np.seterr(divide='ignore', invalid='ignore')


def bs_questionmark_icon(title: str):
    # Enhanced from https://rstudio.github.io/bsicons/ via `bsicons::bs_icon(&quot;gear&quot;, title = icon_title)`
    return ui.HTML(
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi '
        'bi-info-circle-fill" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 '
        '4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-'
        '.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 '
        '0 2"/></svg>'
    )


app_ui = ui.page_fluid(
    ui.tags.link(href="styles16.css", rel="stylesheet"),
    ui.row(
        ui.column(11,
                  ui.output_ui("jumbo_title"),
                  ),
        ui.column(1,
                  ui.div(
                      ui.input_switch("en", "EN", False),
                      style="padding:10px;background-color:#e9ecef;border-radius:5px;margin-left:-10px;"
                  ),
                  )
    ),
    ui.br(),
    ui.navset_pill(
        ui.nav_panel(ui.output_text("nav_panel_intro_title"),
                     ui.row(
                         ui.column(7,
                                   ui.br(),
                                   ui.output_ui("nav_panel_intro_text"),
                                   ui.row(
                                       ui.column(2, ),
                                       ui.column(8,
                                                 ui.card( ui.card_body( ui.output_image("scheme") ) )),
                                       ui.column(2, )
                                   ),
                                   ),
                         ui.column(5,
                                   ui.card( ui.card_body( ui.output_image("scheme_io") ) )
                                   )
                     ),
                     ),
        ui.nav_panel(ui.output_text("nav_panel_gasification_title"),
                     ui.card(
                         ui.card_header("Input Parameters"),
                         ui.card_body(
                             ui.row(
                                 ui.column(3, ui.input_slider("x1", ui.output_text("nozzle_base_constant"),
                                                              value=10,
                                                              min=5,
                                                              max=20,
                                                              step=0.1),
                                           ),
                                 ui.column(3, ui.input_slider("x2", ui.output_text("plasma_torch_power"),
                                                              value=10,
                                                              min=5,
                                                              max=15,
                                                              step=0.1),
                                           ),
                                 ui.column(3, ui.input_slider("x3", ui.output_text("filling_pressure"),
                                                              value=5,
                                                              min=3,
                                                              max=8,
                                                              step=0.1),
                                           ),
                                 ui.column(3, ui.input_slider("waste", ui.output_text("waste_input"),
                                                              value=20, min=1, max=100, step=1),
                                           ),
                             )
                         )
                     ),
                     ui.br(),
                     ui.accordion(
                         ui.accordion_panel(ui.output_text("acc_panel_plasmatron_title"),
                                            ui.row(
                                                ui.column(12,
                                                          ui.output_text("intro_plasmatron"),
                                                          ),
                                                # ui.column(3,
                                                # ui.popover(
                                                #     ui.span(
                                                #         bs_questionmark_icon(icon_title),
                                                #         style="position: relative; top: -5px;", ),
                                                #     ui.output_ui("popover_plasmatron"),
                                                # ),
                                                # ),
                                            ),
                                            ui.row(

                                                ui.column(3,
                                                          ui.br(),
                                                          ui.value_box(
                                                              title=ui.output_text("plasmatron_normalized_temperature"),
                                                              value=ui.output_text("txt_plasmatron_norm_c"))
                                                          ),
                                                ui.column(3,
                                                          ui.br(),
                                                          ui.value_box(
                                                              title=ui.output_text("plasmatron_middle_temperature_k"),
                                                              value=ui.output_text("txt_plasmatron_mid_k"))
                                                          ),
                                                ui.column(3,
                                                          ui.br(),
                                                          ui.value_box(
                                                              title=ui.output_text("plasmatron_middle_temperature_c"),
                                                              value=ui.output_text("txt_plasmatron_mid_c"))
                                                          ),
                                                ui.column(3,
                                                          ui.div(
                                                              style="height: 30vh; background-image: url('plazmatron.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ),
                                                          ),
                                            ),
                                            value="Plasmatron"),
                         ui.accordion_panel(ui.output_text("acc_panel_gasification_chamber_title"),
                                            ui.row(
                                                ui.column(8, ui.output_text("intro_gasification_chamber")),
                                                ui.column(4,
                                                          #           ui.popover(
                                                          #     ui.span(
                                                          #         bs_questionmark_icon(icon_title),
                                                          #         style="position: relative; top:-5px;", ),
                                                          #     ui.output_ui("popover_gasification_chamber"),
                                                          # ),
                                                          ),
                                            ),
                                            ui.row(
                                                ui.column(4,
                                                          ui.br(),
                                                          ui.value_box(
                                                              title=ui.output_text("gasification_chamber_normalized_"
                                                                                   "temperature"),
                                                              value=ui.output_text("txt_plasmatron_norm_c_2")),
                                                          ui.output_ui("gasification_model_select"),
                                                          # ui.output_text("model_output"),
                                                          # ui.output_text("model_select_output")
                                                          ),
                                                ui.column(4,
                                                          ui.br(),
                                                          ui.value_box(
                                                              title=ui.output_text("gasification_chamber_syngas_"
                                                                                   "produced"),
                                                              value=ui.output_text("txt_gasification_waste_m3"))
                                                          ),
                                                ui.column(4,
                                                          ui.div(
                                                              style="height: 35vh; background-image: url('gasifikace_c.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ), ),
                                            ),
                                            ui.hr(),
                                            ui.row(
                                                ui.column(4,
                                                          ui.output_plot('plot_models2', height="270px",
                                                                         click=False)
                                                          ),
                                                ui.column(4,
                                                          ui.row(
                                                              ui.column(6, ui.output_text("gasification"
                                                                                          "_chamber_table_select_text")),
                                                              ui.column(6,
                                                                        ui.output_ui("gasification_chamber_table"
                                                                                     "_select"),
                                                                        ),
                                                          ),
                                                          ui.output_data_frame('data_component_vol')
                                                          ),
                                                ui.column(4,
                                                          ui.output_plot('plot_gasification', height="270px")
                                                          ),
                                            ),
                                            value="Gasification_chamber"),
                         ui.accordion_panel(ui.output_text("hydrogen_tank_filling"),
                                            ui.output_text("intro_hydrogen_tank"),
                                            ui.br(),
                                            ui.row(
                                                ui.column(6,
                                                          ui.row(
                                                              ui.column(3,
                                                                        ui.output_text("hydrogen_tank_pressure"),
                                                                        ui.br(),
                                                                        ui.input_numeric("tank_pressure",
                                                                                         "",
                                                                                         value=200, min=100, max=500),
                                                                        ),
                                                              ui.column(1, ),
                                                              ui.column(3,
                                                                        ui.output_text("hydrogen_tank_volume"),
                                                                        ui.br(),
                                                                        ui.input_numeric("tank_volume",
                                                                                         "",
                                                                                         value=2.2, min=1, max=3,
                                                                                         step=0.1),
                                                                        ),
                                                              ui.column(1, ),
                                                              ui.column(3,
                                                                        ui.output_text("hydrogen_tank_temperature"),
                                                                        ui.br(),
                                                                        ui.input_numeric("tank_temperature",
                                                                                         "",
                                                                                         value=298, min=200, max=400),
                                                                        ),
                                                              ui.column(1, ),
                                                          ),
                                                          ),
                                                ui.column(3,
                                                          ui.value_box(
                                                              title=ui.output_text("hydrogen_tank_time"),
                                                              value=ui.output_text("txt_tank_filling")
                                                          )
                                                          ),
                                                ui.column(3,
                                                          ui.div(
                                                              style="height: 35vh; background-image: url('vodikove_lahve.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ),
                                                          ),
                                            ),
                                            value="Hydrogen_tank_fill"),
                         ui.accordion_panel(ui.output_text("acc_panel_combustion_title"),
                                            ui.output_text("intro_combustion"),
                                            ui.br(),
                                            ui.row(
                                                ui.column(3,
                                                          ui.input_slider("combustion_h2_percent",
                                                                          ui.output_text("txt_combustion_h2_percent"),
                                                                          value=0,
                                                                          min=0,
                                                                          max=100, step=1)
                                                          ),
                                            ),
                                            ui.row(
                                                ui.column(3,
                                                          ui.input_slider("combustion_efficiency",
                                                                          ui.output_text("txt_combustion_efficiency"),
                                                                          value=100,
                                                                          min=20,
                                                                          max=100, step=1)
                                                          ),
                                                ui.column(3,
                                                          ui.output_ui("combustion_select"),
                                                          ),
                                                ui.column(6,
                                                          ui.output_data_frame("data_combustion")
                                                          ),
                                            ),
                                            value="Combustion"),
                         ui.accordion_panel(ui.output_text("acc_panel_fuel_cell_title"),
                                            ui.row(
                                                ui.column(9, ui.output_text("intro_fuel_cell")),
                                                ui.column(3,
                                                          #           ui.popover(
                                                          #     ui.span(
                                                          #         bs_questionmark_icon(icon_title),
                                                          #         style="position: relative; top:-5px;", ),
                                                          #     ui.output_ui("popover_fuel_cell"),
                                                          # ),
                                                          ),
                                            ),
                                            ui.br(),
                                            ui.input_switch("fuel_cell_switch",
                                                            ui.output_text("fuel_cell_switch_text"), False),
                                            ui.hr(),
                                            ui.row(
                                                ui.column(9,
                                                          ui.row(
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.input_slider("efficiency",
                                                                                        ui.output_text(
                                                                                            "fuel_cell_efficiency"),
                                                                                        value=35,
                                                                                        min=35,
                                                                                        max=100, step=1)
                                                                        ),
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.output_ui("fuel_cell_select"),
                                                                        ),
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.value_box(
                                                                            title=ui.output_text("fuel_cell_h2"),
                                                                            value=ui.output_text("txt_h2_kg_ee"))
                                                                        ),
                                                          ),
                                                          ui.row(
                                                              ui.column(6,
                                                                        ui.value_box(
                                                                            title=ui.output_text("fuel_cell_el_energy"),
                                                                            value=ui.output_text("txt_fuel_cell")
                                                                        ),
                                                                        ),
                                                              ui.column(6,
                                                                        ui.value_box(
                                                                            title=ui.output_text("fuel_cell_ele_to_h2"),
                                                                            value=ui.output_text(
                                                                                "txt_fuel_cell_ele_to_h2")
                                                                        ),
                                                                        ),
                                                          ),
                                                          ),
                                                ui.column(3,
                                                          ui.div(
                                                              style="height: 32vh; background-image: url('palivovy_clanek_c.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ),
                                                          )
                                            ),
                                            ui.hr(),
                                            ui.row(
                                                ui.column(2,
                                                          ui.output_text("txt_fuel_cell_count"),
                                                          ui.br(),
                                                          ui.input_numeric("fuel_cell_count",
                                                                           "",
                                                                           value=5, min=1, max=100),
                                                          ),
                                                ui.column(3,
                                                          ui.input_slider("fuel_cell_power",
                                                                          ui.output_text(
                                                                              "txt_fuel_cell_power"),
                                                                          value=8, min=5,
                                                                          max=50, step=1),
                                                          ),
                                                ui.column(4,
                                                          ui.value_box(
                                                              title=ui.output_text("fuel_cell_to_grid"),
                                                              value=ui.output_text(
                                                                  "txt_fuel_cell_to_grid"))
                                                          ),
                                            ),
                                            value="Fuel_cell"),
                         ui.accordion_panel(ui.output_text("acc_panel_electrolyzer_title"),
                                            ui.row(
                                                ui.column(9, ui.output_text("intro_electrolyzer")),
                                                ui.column(3,
                                                          #           ui.popover(
                                                          #     ui.span(
                                                          #         bs_questionmark_icon(icon_title),
                                                          #         style="position: relative; top:-5px;", ),
                                                          #     ui.output_ui("popover_electrolyzer"),
                                                          # ),
                                                          ),
                                            ),
                                            ui.row(
                                                ui.column(8,
                                                          ui.row(
                                                              ui.column(6,
                                                                        ui.br(),
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "electrolyzer_kwh_to_h2_kg"),
                                                                            value=ui.output_text(
                                                                                "txt_electrolyzer_kwh_to_h2_kg")),
                                                                        ),
                                                              ui.column(6,
                                                                        ui.br(),
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "electrolyzer_h2_kg_to_kwh"),
                                                                            value=ui.output_text(
                                                                                "txt_electrolyzer_h2_kg_to_kwh")),
                                                                        ),
                                                          ),
                                                          ui.row(
                                                              ui.column(6,
                                                                        ui.input_slider(
                                                                            "photovoltaic_to_electrolyzer",
                                                                            ui.output_text(
                                                                                "txt_photovoltaic_to_electrolyzer"),
                                                                            value=14, min=10, max=20, step=1),
                                                                        ),
                                                              ui.column(6,
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "electrolyzer_from_photovoltaic"),
                                                                            value=ui.output_text(
                                                                                "txt_electrolyzer_from_photovoltaic")),
                                                                        ),
                                                          ),
                                                          ui.row(
                                                              ui.column(6,
                                                                        ui.input_slider("grid_to_electrolyzer",
                                                                                        ui.output_text(
                                                                                            "txt_grid_to_electrolyzer"),
                                                                                        value=50,
                                                                                        min=1,
                                                                                        max=100, step=1),
                                                                        ),
                                                              ui.column(6,
                                                                        ui.value_box(
                                                                            title=ui.output_text("electrolyzer_h2"),
                                                                            value=ui.output_text("txt_electrolyzer_h2"))
                                                                        ),
                                                          ),
                                                          ),
                                                ui.column(1, ),
                                                ui.column(3,
                                                          ui.div(
                                                              style="height: 32vh; background-image: url('elektrolyzer_c.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ),
                                                          ),

                                            ),
                                            value="Electrolyzer"),
                         ui.accordion_panel(ui.output_text("acc_panel_sun_wind_title"),
                                            ui.output_text("intro_fotovoltaics"),
                                            ui.row(
                                                ui.column(9,
                                                          ui.row(
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.input_slider("solar_power",
                                                                                        ui.output_text(
                                                                                            "txt_solar_power_slider"),
                                                                                        value=170,
                                                                                        min=10,
                                                                                        max=170, step=10)
                                                                        ),
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.input_slider("wind_power",
                                                                                        ui.output_text(
                                                                                            "txt_wind_power_slider"),
                                                                                        value=10,
                                                                                        min=1,
                                                                                        max=10, step=1)
                                                                        ),
                                                              ui.column(4,
                                                                        ui.br(),
                                                                        ui.input_slider("battery",
                                                                                        ui.output_text(
                                                                                            "txt_battery_slider"),
                                                                                        value=500,
                                                                                        min=400,
                                                                                        max=1000, step=100)
                                                                        ),
                                                          ),
                                                          ui.br(),
                                                          ui.row(
                                                              ui.column(8,
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "photovoltaic_wind_sum"),
                                                                            value=ui.output_text(
                                                                                "txt_photovoltaic_wind_sum")), ), ),
                                                          ui.row(
                                                              ui.column(4,
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "photovoltaic_to_electrolyzer_2"),
                                                                            value=ui.output_text(
                                                                                "txt_photovoltaic_to_electrolyzer_2"))
                                                                        ),
                                                              ui.column(4,
                                                                        ui.value_box(
                                                                            title=ui.output_text(
                                                                                "photovoltaic_to_battery_grid"),
                                                                            value=ui.output_text(
                                                                                "txt_photovoltaic_to_battery_grid"))
                                                                        ),
                                                              ui.column(4,
                                                                        ui.value_box(
                                                                            title=ui.output_text("battery_hours"),
                                                                            value=ui.output_text(
                                                                                "txt_battery_hours")),
                                                                        ),
                                                          ),
                                                          ui.row(
                                                              ui.column(8,
                                                                        ui.value_box(
                                                                            title=ui.output_text("fuel_cell_to_grid_2"),
                                                                            value=ui.output_text(
                                                                                "txt_fuel_cell_to_grid_2")),
                                                                        ),
                                                          ),
                                                          ),
                                                ui.column(3,
                                                          ui.div(
                                                              style="height: 32vh; background-image: url('solar_vitr.jpg'); "
                                                                    "background-size: 100%; background-repeat: no-repeat; "
                                                                    "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                                                          ),
                                                          ),
                                            ),
                                            value="Sun_wind"),
                         multiple=False, open=False),
                     ui.br(),
                     ui.br(),
                     ),
        ui.nav_panel(ui.output_text("nav_panel_pyrolysis_title"),
                     ui.br(),
                     ui.output_text("intro_pyrolysis"),
                     ui.row(
                         ui.column(9,
                                   ui.row(
                                       ui.column(4,
                                                 ui.br(),
                                                 ui.input_slider("energy", ui.output_text("pyrolysis_energy_kwh"),
                                                                 value=5, min=3.3,
                                                                 max=9, step=0.1),
                                                 ),
                                       ui.column(4,
                                                 ui.br(),
                                                 ui.value_box(title=ui.output_text("pyrolysis_energy_mj"),
                                                              value=ui.output_text("txt_pyrolysis_mj"))
                                                 ),
                                       ui.column(4,
                                                 ui.br(),
                                                 ui.input_slider("pyrolysis_waste",
                                                                 ui.output_text("pyrolysis_waste_slider"),
                                                                 value=3, min=2,
                                                                 max=5, step=1),
                                                 )
                                   ),
                                   ui.row(
                                       ui.column(7,
                                                 ui.br(),
                                                 ui.div(
                                                     ui.panel_absolute(
                                                         ui.value_box(title=ui.output_text("pyrolysis_temperature_c"),
                                                                      value=ui.output_text("txt_pyrolysis_temperature"),
                                                                      ),
                                                         width="32%",
                                                         height="5%",
                                                         right="24%",
                                                         top="7%",
                                                     ),
                                                     style="height: 30vh; background-image: url('pyrolysis.png'); "
                                                           "background-size: contain; background-repeat: no-repeat; "
                                                           "position: relative;",
                                                 ),
                                                 ),
                                       # ui.column(1, ),
                                       ui.column(3,
                                                 ui.br(),
                                                 ui.br(),
                                                 ui.div(ui.output_image("scheme_pyrolysis"),
                                                        style="height: 220px",
                                                        ),
                                                 )
                                   ),
                                   ),
                         ui.column(3, ui.div(
                             style="height: 50vh; background-image: url('pyrolyza.png'); "
                                   "background-size: 100%; background-repeat: no-repeat; "
                                   "position: relative; box-shadow: 0px 0px 10px 10px white inset;",
                         ), )
                     ),
                     ui.br(),
                     ui.hr(),
                     ui.row(
                         ui.column(3,
                                   ui.value_box(
                                       title=ui.output_text("pyrolysis_liquid"),
                                       value=ui.output_text(
                                           "txt_pyrolysis_liquid")),
                                   ui.value_box(
                                       title=ui.output_text("pyrolysis_gas"),
                                       value=ui.output_text(
                                           "txt_pyrolysis_gas")),
                                   ui.value_box(
                                       title=ui.output_text("pyrolysis_biochar"),
                                       value=ui.output_text(
                                           "txt_pyrolysis_biochar")),
                                   ),
                         ui.column(3,
                                   ui.output_plot("plot_pyrolysis_state", height="270px")
                                   ),
                         ui.column(6,
                                   ui.row(
                                       ui.column(6,
                                                 ui.row(
                                                     ui.column(6, ui.output_text("pyrolysis_table_"
                                                                                 "select_text")),
                                                     ui.column(6,
                                                               ui.output_ui("pyrolysis_table_select"),
                                                               ),
                                                 ),
                                                 ui.output_data_frame("pyrolysis_gas_vol")
                                                 ),
                                       ui.column(6,
                                                 ui.output_plot("plot_pyrolysis", height="270px")
                                                 )
                                   )
                                   ),
                     ),
                     ),
        ui.nav_panel(ui.output_text("nav_panel_optimization_title"),
                     ui.row(
                         ui.column(6,
                                   ui.br(),
                                   ui.output_ui("optimization_problem_select"),
                                   ui.row(
                                       ui.column(6,
                                                 ui.br(),
                                                 ui.output_text("text_opt"),
                                                 ui.br(),
                                                 ui.output_table("df_opt_h2"),
                                                 ),
                                       ui.column(6,
                                                 ui.br(),
                                                 ui.output_plot("plot_opt_gasification", height="200px"))
                                   ),
                                   ui.output_ui("ui_h2_gas_opt_options"),
                                   ),
                         ui.column(6,
                                   ui.br(),
                                   ui.br(),
                                   ui.HTML('<p style="margin-bottom:2px;"> </p>'),
                                   ui.div(ui.output_ui("ui_action_button"), id="start_opt_button")
                                   )
                     ),
                     ),
        id="tabs"),
)


def server(input, output, session):
    waste_coefficient = 0.88
    volume_1_mol_normal_cond = 0.0224
    mm_h2 = 2
    mm_co2 = 44
    mm_co = 28
    mm_ch4 = 16
    mm_n2 = 28
    low_heat_value_const = 33
    high_heat_value_const = 39.38
    kwh_for_1_kg_h2 = 52
    r_const = 8.31446
    default_model_select = reactive.Value('poly')
    default_heating_value_select = reactive.Value('low')
    default_efficiency = reactive.Value(35)

    @reactive.Effect
    @reactive.event(input.model_select)
    def _():
        default_model_select.set(input.model_select())

    @reactive.Effect
    @reactive.event(input.heating_value_select)
    def _():
        default_heating_value_select.set(input.heating_value_select())

    @reactive.Effect
    @reactive.event(input.efficiency)
    def _():
        default_efficiency.set(input.efficiency())

    @output
    @render.ui
    def jumbo_title():
        if input.en() is True:
            return ui.HTML(
                """
                      <div class="jumbotron" style="background-color: #EBEBEB">
                      <h4 class='jumbotron-heading' style='margin-bottom:0px;margin-top:0px;margin-left:10px;padding:5px;
                      background-color: #e9ecef;'>
                      <img src="logo.png" style="text-align:left;height:70px;margin-right:20px;"/>
                      CEET: Software tool with implemented optimization algorithms for SCS
                      </h4>
                      </div>
                      """
            )
        else:
            return ui.HTML(
                """
                      <div class="jumbotron" style="background-color: #EBEBEB">
                      <h4 class='jumbotron-heading' style='margin-bottom:0px;margin-top:0px;margin-left:5px;padding:5px;
                      background-color: #e9ecef;'>
                      <img src="logo_cz.png" style="text-align:left;height:70px"/>
                      CEET: Softwarový nástroj s implementovanými optimalizačními algoritmy pro SCS
                      </h4>
                      </div>
                      """
            )

    @output
    @render.text
    def nav_panel_intro_title():
        if input.en() is True:
            return "Introduction"
        else:
            return "Úvod"

    @output
    @render.ui
    def nav_panel_intro_text():
        if input.en() is True:
            return ui.HTML("""
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            The objective of this application is to simulate the gasification processes involved in converting communal 
            waste into valuable resources. Communal waste primarily comprises organic materials like biomass and 
            combustibles from both household and industrial sources. Through gasification, this waste is transformed 
            into synthetic gas, known as syngas. The composition of syngas is heavily influenced by factors such as the
             temperature within the gasification chamber and the makeup of the waste materials.</div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            The primary target within syngas production is hydrogen, a versatile resource capable of generating 
            electrical energy via fuel cells. Additionally, syngas contains other valuable components such as methane 
            and carbon monoxide, which can serve various purposes. These include direct combustion for heating or 
            electricity generation. </div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            Moreover, it's imperative for the facility to incorporate a reverse mode capability. This means having the 
            capacity to produce hydrogen from electricity through an electrolyzer, thereby enhancing operational 
            flexibility and meeting diverse energy demands. </div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            In addition to gasification, the application can simulate the process of pyrolysis, which is mainly used 
            for the production of liquid fuel. </div>
            """)
        else:
            return ui.HTML("""
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            Cílem této aplikace je zejména simulovat procesy zplyňování (gasifikace) při přeměně komunálního odpadu
            na cenné zdroje. Komunální odpad obsahuje především organické materiály, jako je biomasa a
            hořlaviny z domácích i průmyslových zdrojů. Zplyňováním se tento odpad přeměňuje
            na syntetický plyn, známý jako syngas. Složení syngasu je silně ovlivněno faktory, jako je
            teplota ve zplyňovací komoře a složení odpadních materiálů.</div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            Hlavním cílem při výrobě syngasu je vodík, všestranný zdroj schopný generovat
            elektrickou energii prostřednictvím palivových článků. Syngas navíc obsahuje další cenné složky, jako je 
            metan a oxid uhelnatý, který může sloužit různým účelům - například k přímému spalování pro vytápění nebo k
            výrobě elektřiny. </div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            Kromě toho je nezbytné, aby zařízení mělo schopnost zpětného režimu, tzn. mít
            kapacity produkovat vodík z elektřiny prostřednictvím elektrolyzéru, čímž se zvyšuje provozní
            flexibilita a splnění různých energetických požadavků. </div>
            <div style="text-align: justify; padding-right: 30px; padding-left:20px"> 
            Kromě gasifikace je možné v aplikaci simulovat proces pyrolýzy, která slouží zejména k výrobě kapalného 
            paliva. </div>
            """)

    @output
    @render.image
    def scheme_io():
        if input.en() is True:
            img = {"src": www_dir / "ceet_diagram_en_new_3.png", "height": "660px"}
        else:
            img = {"src": www_dir / "ceet_diagram_cz_new_4.png", "height": "660px"}
        return img

    @output
    @render.image
    def scheme_pyrolysis():
        if input.en() is True:
            img = {"src": www_dir / "pyrolysis_scheme_en.png", "height": "220px"}
        else:
            img = {"src": www_dir / "pyrolysis_scheme_cz.png", "height": "220px"}
        return img

    @output
    @render.image
    def scheme():
        if input.en() is True:
            img = {"src": www_dir / "ceet_scheme_new_en.png", "height": "270px"}
        else:
            img = {"src": www_dir / "ceet_scheme_new_cz_2.png", "height": "270px"}
        return img

    @output
    @render.text
    def nav_panel_gasification_title():
        if input.en() is True:
            return "Gasification"
        else:
            return "Gasifikace"

    @output
    @render.text
    def nozzle_base_constant():
        if input.en() is True:
            return "Nozzle base constant [no units]:"
        else:
            return "Základní konstanta trysky [-]:"

    @output
    @render.text
    def plasma_torch_power():
        if input.en() is True:
            return "Plasma torch power [kW]:"
        else:
            return "Výkon plazmového hořáku [kW]:"

    @output
    @render.text
    def filling_pressure():
        if input.en() is True:
            return "Filling pressure [bar]:"
        else:
            return "Plnící tlak [bar]:"

    @output
    @render.text
    def waste_input():
        if input.en() is True:
            return "Waste input [kg/hour]:"
        else:
            return "Přísun odpadu [kg/h]:"

    @output
    @render.text
    def acc_panel_plasmatron_title():
        if input.en() is True:
            return "Plasmatron"
        else:
            return "Plazmatron"

    @output
    @render.text
    def acc_panel_gasification_chamber_title():
        if input.en() is True:
            return "Gasification chamber"
        else:
            return "Gasifikační komora"

    @output
    @render.text
    def acc_panel_combustion_title():
        if input.en() is True:
            return "Combustion"
        else:
            return "Spalování"

    @output
    @render.text
    def acc_panel_fuel_cell_title():
        if input.en() is True:
            return "Fuel cell"
        else:
            return "Palivové články"

    @output
    @render.text
    def acc_panel_electrolyzer_title():
        if input.en() is True:
            return "Electrolyzer"
        else:
            return "Elektrolyzér"

    @output
    @render.text
    def acc_panel_sun_wind_title():
        if input.en() is True:
            return "Photovoltaics and wind turbine"
        else:
            return "Fotovoltaika a větrné turbíny"

    @output
    @render.text
    def photovoltaic_wind_sum():
        if input.en() is True:
            return "Energy from photovoltaics and wind turbine [kWh]:"
        else:
            return "Energie z fotovoltaiky a větrné turbíny [kWh]:"

    @output
    @render.text
    def txt_photovoltaic_wind_sum():
        return "{:.0f}".format(input.solar_power() + input.wind_power())

    @output
    @render.text
    def intro_plasmatron():
        if input.en() is True:
            return ("The plasma torch gives the middle temperature of plasma stream in [K] and [°C] and normalized "
                    "temperature in plasma reactor in [°C], which is filled-in with waste [kg/hour].")
        else:
            return ("Plazmový hořák udává střední teplotu proudu plazmy v [K] a [°C] a normalizovanou teplotu v "
                    "plazmovém reaktoru v [°C], který je naplněn odpadem [kg/hod].")

    @output
    @render.ui
    def popover_plasmatron():
        if input.en() is True:
            return ui.HTML("""
                            <div style="text-align: justify"> 
                            The Plasmatron, also known as a plasma torch, serves as a crucial device for generating 
                            the necessary heat to gasify waste materials. To estimate the median temperature of the 
                            plasma torch, various parameters from the utilized direct current (DC) plasmatron are taken
                             into account. These parameters include:
                            <ul>
                            <li>the base constant of the nozzle, </li>
                            <li>the required power of the plasma torch, </li>
                            <li>and the filling pressure.</li>
                            </ul>
                            In this study, a DC plasma torch is employed. This device operates by conducting direct 
                            current between a cathode and an anode, thereby generating a potent electric field. This 
                            electric field, in turn, catalyzes the ionization of the gas situated between the cathode 
                            and anode, resulting in the formation of low-temperature plasma.
                            </div>
                            <div style="text-align: justify"> 
                            The plasmatron used in this application boasts an output power of 15 kW. Ambient air, 
                            pressurized to a maximum of 10 bar through a compressor station, serves as the medium 
                            between the electrodes. This pressurized air is carefully directed through nozzles to 
                            maintain the flow of plasma and to prevent any electrical short circuits between the anode 
                            and cathode. Additionally, the voltage of the electric arc of the plasma is 
                            measured for further analysis.
                            </div>
                             """)
        else:
            return ui.HTML("""
                            <div style="text-align: justify"> 
                            Plazmatron, známý také jako plazmový hořák, slouží jako klíčové zařízení pro generování 
                            potřebného tepla ke zplynování odpadních materiálů. K odhadu střední hodnoty teploty 
                            uvažujeme o těchto parametrech plazmového hořáku:
                            <ul>
                            <li>základní konstanta trysky, </li>
                            <li>výkon plazmového hořáku, </li>
                            <li>a plnící tlak. </li>
                            </ul> V experimentech, ze kterých tato aplikace vychází, je použit stejnosměrný plazmový
                            hořák. Funkce tohoto zařízení spočívá ve vedení stejnosměrného proudu mezi katodou a anodou, 
                            čímž generuje silné elektrické pole. Toto elektrické pole naopak katalyzuje ionizace 
                            plynu umístěného mezi katodou a anodou, což má za následek tvorbu nízkoteplotní plazma.
                            </div>
                            <div style="text-align: justify"> 
                            Plasmatron použitý v této aplikaci disponuje výstupním výkonem 15 kW. Okolní vzduch, pod 
                            tlakem maximálně 10 barů přes kompresorovou stanici, slouží jako médium mezi elektrodami. 
                            Tento stlačený vzduch je pečlivě nasměrován tryskami, aby se zachoval tok plazmy a aby se 
                            zabránilo jakémukoli elektrickému zkratu mezi anodou a katodou. Navíc je pro další analýzu 
                            měřeno napětí elektrického oblouku plazmy.
                            </div>
                             """)

    @output
    @render.text
    def plasmatron_normalized_temperature():
        if input.en() is True:
            return "Normalized temperature [°C]:"
        else:
            return "Normalizovaná teplota [°C]:"

    @output
    @render.text
    def plasmatron_middle_temperature_k():
        if input.en() is True:
            return "Middle temperature [K]:"
        else:
            return "Střední teplota [K]:"

    @output
    @render.text
    def plasmatron_middle_temperature_c():
        if input.en() is True:
            return "Middle temperature [°C]:"
        else:
            return "Střední teplota [°C]:"

    @output
    @render.text
    def intro_gasification_chamber():
        if input.en() is True:
            return ("In the gasification reactor, syngas is produced in [m\u00B3/hour] and we can see its volumetric "
                    "composition in [%].")
        else:
            return ("Ve zplyňovacím reaktoru se výrobí syngas v [m\u00B3/hod] a můžeme sledovat jeho objemové složení "
                    "v [%].")

    @output
    @render.ui
    def popover_gasification_chamber():
        if input.en() is True:
            return ui.HTML("""
                            <div style="text-align: justify">
                             Gasification occurs within a controlled chamber environment, typically maintained at 
                             temperatures ranging from 750°C to 1100°C. Leveraging advanced computational techniques 
                             such as symbolic and polynomial regression, 
                             we construct a continuous mathematical model to predict the
                             volumetric composition of the five predominant gases within syngas as a function of
                             temperature in the gasification chamber. This modeling process integrates tools like
                             Al-Feynman and PySR for accurate analysis and prediction.
                             </div>
                             <div style="text-align: justify">
                             The input of waste materials for gasification is estimated at 20 kg per hour, yielding
                             approximately 17.6 - 18.33 normal cubic meters of syngas. This estimation is derived from
                             the observation that 100 kg of waste typically generates around 88 normal cubic meters
                             of syngas.
                             </div>
                             <br>
                             """)
        else:
            return ui.HTML("""
                            <div style="text-align: justify">
                            Zplyňování probíhá v prostředí řízené komory, typicky udržované při teplotě od 750°C do 
                            1100°C.Využití pokročilých výpočetních technik jako je symbolická a polynomiální regrese, 
                            konstruujeme spojitý matematický model pro předpovídání
                            objemového složení pěti převládajících plynů v syngasu v závislosti na
                            teplotě ve zplyňovací komoře. Tento proces modelování integruje nástroje jako
                            Al-Feynman a PySR pro přesnou analýzu a předpověď.
                            </div>
                            <div style="text-align: justify">
                            Vstup odpadních materiálů pro zplyňování se odhaduje na 20 kg za hodinu, s výnosem
                            přibližně 17,6 - 18,33 běžných metrů krychlových syngasu. Tento odhad je odvozen z
                            pozorování, že 100 kg odpadu obvykle vytváří přibližně 88 běžných metrů krychlových
                            syngasu.
                            </div>
                            <br>
                            """)

    @output
    @render.text
    def gasification_chamber_normalized_temperature():
        if input.en() is True:
            return "Normalized temperature [°C]:"
        else:
            return "Normalizovaná teplota [°C]:"

    @output
    @render.text
    def gasification_chamber_syngas_produced():
        if input.en() is True:
            return "Syngas produced [m\u00B3/hour]:"
        else:
            return "Produkce syngasu [m\u00B3/h]:"

    @output
    @render.text
    def gasification_chamber_table_select_text():
        if input.en() is True:
            return "Select an option:"
        else:
            return "Zvolte možnost:"

    @output
    @render.text
    def pyrolysis_table_select_text():
        if input.en() is True:
            return "Select an option:"
        else:
            return "Zvolte možnost:"

    @output
    @render.ui
    def gasification_chamber_table_select():
        if input.en() is True:
            return ui.input_select(
                "gasification_select",
                "",
                {"Volume [%]": "Volume [%]",
                 "Volume [m\u00B3]": "Volume [m\u00B3]",
                 "Moles": "Moles",
                 "Mass [%]": "Mass [%]",
                 "Mass [g]": "Mass [g]",
                 "Mass [kg]": "Mass [kg]"}
            )
        else:
            return ui.input_select(
                "gasification_select",
                "",
                {"Volume [%]": "Objem [%]",
                 "Volume [m\u00B3]": "Objem [m\u00B3]",
                 "Moles": "Látkové množství [mol]",
                 "Mass [%]": "Hmotnost [%]",
                 "Mass [g]": "Hmotnost [g]",
                 "Mass [kg]": "Hmotnost [kg]"}
            )

    @output
    @render.ui
    def pyrolysis_table_select():
        if input.en() is True:
            return ui.input_select(
                "pyrolysis_select",
                "",
                {"Volume [%]": "Volume [%]",
                 "Volume [m\u00B3]": "Volume [m\u00B3]",
                 "Moles": "Moles",
                 "Mass [%]": "Mass [%]",
                 "Mass [g]": "Mass [g]",
                 "Mass [kg]": "Mass [kg]"}
            )
        else:
            return ui.input_select(
                "pyrolysis_select",
                "",
                {"Volume [%]": "Objem [%]",
                 "Volume [m\u00B3]": "Objem [m\u00B3]",
                 "Moles": "Látkové množství [mol]",
                 "Mass [%]": "Hmotnost [%]",
                 "Mass [g]": "Hmotnost [g]",
                 "Mass [kg]": "Hmotnost [kg]"}
            )

    @output
    @render.text
    def hydrogen_tank_filling():
        if input.en() is True:
            return "Hydrogen tank filling"
        else:
            return "Plnění vodíkové láhve"

    @output
    @render.text
    def hydrogen_tank_pressure():
        if input.en() is True:
            return "Pressure [bar]:"
        else:
            return "Tlak [bar]:"

    @output
    @render.text
    def hydrogen_tank_volume():
        if input.en() is True:
            return "Volume [m\u00B3]:"
        else:
            return "Objem [m\u00B3]:"

    @output
    @render.text
    def hydrogen_tank_temperature():
        if input.en() is True:
            return "Temperature [K]:"
        else:
            return "Teplota [K]:"

    @output
    @render.text
    def hydrogen_tank_time():
        if input.en() is True:
            return "Time to fill up the tank [hours]:"
        else:
            return "Čas k naplnění láhve [h]:"

    @output
    @render.text
    def txt_combustion_h2_percent():
        if input.en() is True:
            return "H\u2082 used in combustion [%]:"
        else:
            return "H\u2082 využito ve spalování [%]:"

    @output
    @render.text
    def txt_combustion_efficiency():
        if input.en() is True:
            return "Efficiency [%]:"
        else:
            return "Účinnost [%]:"

    @output
    @render.ui
    def combustion_select():
        if input.en() is True:
            return ui.input_select(
                "comb_heating_value_select",
                "Select a heating value:",
                {"low": "Lower heating values",
                 "high": "Higher heating values"})
        else:
            return ui.input_select(
                "comb_heating_value_select",
                "Vyberte hodnotu výhřevnosti:",
                {"low": "Nízké hodnoty výhřevnosti",
                 "high": "Vysoké hodnoty výhřevnosti"})

    @output
    @render.text
    def intro_hydrogen_tank():
        if input.en() is True:
            return "The hydrogen produced in the gasification chamber is stored in hydrogen tanks."
        else:
            return "Vodík získaný v gasifikační komoře je následně uložen ve vodíkových lahvích."

    @output
    @render.text
    def intro_combustion():
        if input.en() is True:
            return ("Combustion is an alternative process and it operates only when production of electricity in fuel "
                    "cells is closed.")
        else:
            return ("Spalování je alternativní proces, který funguje pouze při ukončení výroby elektřiny v palivových "
                    "článcích.")

    @output
    @render.text
    def intro_fuel_cell():
        if input.en() is True:
            return ("Producing energy in the fuel cell is a main process (if it operates then hydrogen is not used "
                    "in combustion).")
        else:
            return (
                "Výroba energie v palivovém článku je hlavním procesem (pokud je v provozu, vodík se nevyužívá "
                "v procesu spalování).")

    @output
    @render.ui
    def popover_fuel_cell():
        if input.en() is True:
            return ui.HTML("""
                         <div style="text-align: justify"> 
                         In a fuel cell with 100% efficiency, 1 kg of hydrogen can produce 33 kWh of 
                         electrical energy, considering the lower heating value for high-temperature fuel cells 
                         if the product is steam. On the other hand, for low-temperature fuel cells, where the 
                         product is liquid water, higher heating value can be considered, leading 1 kg hydrogen to
                         produce 39.38 kWh of electrical energy. In a low-temperature fuel cell, where the product 
                         is liquid water, the higher heating value should be used in efficiency calculations, 
                         while for high-temperature fuel cells, it may be acceptable to use the lower heating value,
                         considering the produced steam is used up efficiently. 
                         </div>
                         <br>
                         """)
        else:
            return ui.HTML("""
                           <div style="text-align: justify"> 
                           V palivovém článku se 100% účinností může 1 kg vodíku vyrobit 33 kWh
                           elektrické energie s ohledem na nižší výhřevnost u vysokoteplotních palivových článků
                           pokud je produktem pára. Na druhou stranu u nízkoteplotních palivových článků, kde
                           produktem je pára, lze uvažovat o vyšší výhřevnosti. To vedek tomu, že 1 kg vodíku
                           vyrobí 39,38 kWh elektrické energie. V nízkoteplotním palivovém článku by se při výpočtech 
                           účinnosti měla použít vyšší výhřevnost, zatímco u vysokoteplotních palivových článků může 
                           být přijatelné použít nižší výhřevnost, pokud je vyrobená pára využita efektivně.
                           </div>
                           <br>
                           """)

    @output
    @render.text
    def intro_electrolyzer():
        if input.en() is True:
            return ("The electrolyer works in reverse compared to fuel cells – it produces hydrogen from water and "
                    "electricity.")
        else:
            return ("Elektrolyzér funguje ve srovnání s palivovými články obráceně – vyrábí vodík z vody a elektřiny.")

    @output
    @render.ui
    def popover_electrolyzer():
        if input.en() is True:
            return ui.HTML("""
                             <div style="text-align: justify"> 
                             It takes 52 kWh to produce 1 kg of 
                             hydrogen. The implemented model makes it possible to simulate the conversion of electricity
                              - hydrogen - electricity, which takes into account the use of hydrogen as an energy storage.
                             It was shown that 22.21% of hydrogen can be recovered. The model shows that 1 kWh of 
                             electricity corresponds to approx. 0.02 kg of hydrogen that was produced in the electrolyser. 
                             In contrast, 1 kWh of electricity corresponds, in the worst case, to approx. 0.087 kg of 
                             hydrogen produced in the fuel cell. 
                             </div>
                             <br>
                             """)
        else:
            return ui.HTML("""
                               <div style="text-align: justify"> 
                               Na výrobu 1 kg vodíku je potřeba 52 kWh
                               elektrické energie. Implementovaný model umožňuje simulovat přeměnu elektrické energie
                                - vodík - elektřina, která zohledňuje využití vodíku jako úložiště energie.
                               Ukázalo se, že lze získat 22,21 % vodíku. Model ukazuje, že 1 kWh
                               elektřiny odpovídá cca. 0,02 kg vodíku, který byl vyroben v elektrolyzéru.
                               Naproti tomu 1 kWh elektřiny odpovídá v nejhorším případě cca. 0,087 kg
                               vodíku produkovaného v palivovém článku.
                               </div>
                               <br>
                               """)

    @output
    @render.text
    def intro_fotovoltaics():
        if input.en() is True:
            return ("Photovoltaic panels and wind turbines provide electricity to the battery and electrolyzer.")
        else:
            return ("Fotovoltaické panely a větrné turbíny dodávají elektřinu baterii a elektrolyzéru.")

    @output
    @render.text
    def fuel_cell_switch_text():
        if input.en() is True:
            return "Fuel cells out of order"
        else:
            return "Palivové články mimo provoz"

    @output
    @render.text
    def fuel_cell_efficiency():
        if input.en() is True:
            return "Efficiency [%]:"
        else:
            return "Účinnost [%]:"

    @output
    @render.ui
    def fuel_cell_select():
        if input.en() is True:
            return ui.input_select(
                "heating_value_select",
                "Select a heating value:",
                {"low": "Lower heating value: 33",
                 "high": "Higher heating value: 39.38"})
        else:
            return ui.input_select(
                "heating_value_select",
                "Vyberte hodnotu výhřevnosti:",
                {"low": "Nízká hodnota výhřevnosti: 33",
                 "high": "Vysoká hodnota výhřevnosti: 39.38"})

    @output
    @render.text
    def fuel_cell_h2():
        if input.en() is True:
            return "The amount of H\u2082 [kg]:"
        else:
            return "Množství H\u2082 [kg]:"

    @output
    @render.text
    def fuel_cell_el_energy():
        if input.en() is True:
            return "Electrical energy obtained from fuel cells [kWh]:"
        else:
            return "Elektrická energie získaná z palivových článků [kWh]:"

    @output
    @render.text
    def electrolyzer_fuel_cell_el_energy():
        if input.en() is True:
            return "Electrical energy obtained from fuel cells [kWh]:"
        else:
            return "Elektrická energie získaná z palivových článků [kWh]:"

    @output
    @render.text
    def fuel_cell_ele_to_h2():
        if input.en() is True:
            return "Amount of H\u2082 equivalent to 1 kWh of electricity [kg]:"
        else:
            return "Množství H\u2082 ekvivalentní 1 kWh elektřiny [kg]:"

    @output
    @render.text
    def txt_fuel_cell_ele_to_h2():
        if calc_fuel_cell() == 0:
            return "-"
        else:
            return "{:.2f}".format(h2_kg() / calc_fuel_cell())

    @output
    @render.text
    def txt_fuel_cell_count():
        if input.en() is True:
            return "Number of fuel cells:"
        else:
            return "Počet palivových článků:"

    @output
    @render.text
    def txt_fuel_cell_power():
        if input.en() is True:
            return "Power of fuel cells [kW]:"
        else:
            return "Výkon palivových článků [kW]:"

    @output
    @render.text
    def electrolyzer_h2():
        if input.en() is True:
            return "H\u2082 produced using electricity from grid [kg]:"
        else:
            return "H\u2082 vyprodukováno z energie ze sítě [kg]:"

    @output
    @render.text
    def txt_grid_to_electrolyzer():
        if input.en() is True:
            return "Energy from grid [kWh]:"
        else:
            return "Energie ze sítě [kWh]:"

    @output
    @render.text
    def electrolyzer_h2_kg_to_kwh():
        if input.en() is True:
            return "H\u2082 produced from 1 kWh of electricity [kg]:"
        else:
            return "H\u2082 vyrobeno z 1 kWh elektrické energie [kg]:"

    @output
    @render.text
    def txt_electrolyzer_h2_kg_to_kwh():
        return "{:.2f}".format(1 / kwh_for_1_kg_h2)

    @output
    @render.text
    def electrolyzer_kwh_to_h2_kg():
        if input.en() is True:
            return "Energy required to produce 1 kg of H\u2082 [kWh]:"
        else:
            return "Energie potřebná k výrobě 1 kg H\u2082 [kWh]:"

    @output
    @render.text
    def txt_electrolyzer_kwh_to_h2_kg():
        return "{:.0f}".format(kwh_for_1_kg_h2)

    @output
    @render.text
    def txt_photovoltaic_to_electrolyzer():
        if input.en() is True:
            return "Energy obtained from photovoltaics and wind [kWh]:"
        else:
            return "Energie z fotovoltaiky a větrné turbíny [kWh]:"

    @output
    @render.text
    def photovoltaic_to_electrolyzer_2():
        if input.en() is True:
            return "Energy used by the electrolyzer [kWh]:"
        else:
            return "Energie využita elektrolyzérem [kWh]:"

    @output
    @render.text
    def txt_photovoltaic_to_electrolyzer_2():
        return "{:.0f}".format(input.photovoltaic_to_electrolyzer())

    @output
    @render.text
    def photovoltaic_to_battery_grid():
        if input.en() is True:
            return "Energy sent to battery or grid [kWh]:"
        else:
            return "Energie posílaná do baterie / sítě [kWh]:"

    @output
    @render.text
    def txt_photovoltaic_to_battery_grid():
        return "{:.0f}".format(input.solar_power() + input.wind_power() - input.photovoltaic_to_electrolyzer())

    @output
    @render.text
    def electrolyzer_from_photovoltaic():
        if input.en() is True:
            return ("H\u2082 using electricity from photovoltaics and "
                    "wind [kg/hour]:")
        else:
            return "H\u2082 z energie fotovoltaiky a větrné turbíny [kg/h]:"

    @output
    @render.text
    def txt_electrolyzer_from_photovoltaic():
        return "{:.2f}".format(input.photovoltaic_to_electrolyzer() / kwh_for_1_kg_h2)

    @output
    @render.text
    def txt_solar_power_slider():
        if input.en() is True:
            return "Installed photovoltaics power [kW]:"
        else:
            return "Instalovaný výkon fotovoltaiky [kW]:"

    @output
    @render.text
    def txt_wind_power_slider():
        if input.en() is True:
            return "Installed power of wind turbine [kW]:"
        else:
            return "Instalovaný výkon větrné turbíny [kW]:"

    @output
    @render.text
    def txt_battery_slider():
        if input.en() is True:
            return "Battery capacity [kWh]:"
        else:
            return "Kapacita baterie [kWh]:"

    @output
    @render.text
    def battery_hours():
        if input.en() is True:
            return "Time to fill up the battery [hours]:"
        else:
            return "Čas k dobití baterie [h]:"

    @output
    @render.text
    def txt_battery_hours():
        return "{:.1f}".format(
            input.battery() / (input.solar_power() + input.wind_power() - input.photovoltaic_to_electrolyzer()))

    @output
    @render.text
    def fuel_cell_to_grid():
        if input.en() is True:
            return "Installed power of fuel cells [kW]:"
        else:
            return "Instalovaný výkon palivových článků [kW]:"

    @reactive.Calc
    def fuel_cell_grid():
        return input.fuel_cell_count() * input.fuel_cell_power()

    @output
    @render.text
    def txt_fuel_cell_to_grid():
        return "{:.0f}".format(fuel_cell_grid())

    @output
    @render.text
    def fuel_cell_to_grid_2():
        if input.en() is True:
            return "Energy sent to grid from fuel cells [kWh]:"
        else:
            return "Energie posílaná do sítě z palivových článků [kWh]:"

    @output
    @render.text
    def txt_fuel_cell_to_grid_2():
        return "{:.0f}".format(fuel_cell_grid())

    @output
    @render.text
    def nav_panel_pyrolysis_title():
        if input.en() is True:
            return "Pyrolysis"
        else:
            return "Pyrolýza"

    @output
    @render.text
    def intro_pyrolysis():
        if input.en() is True:
            return ("The main product of pyrolysis is liquid fuel - pyrolysis oil.")
        else:
            return ("Hlavním produktem pyrolýzy je kapalné palivo – pyrolýzní olej.")

    @output
    @render.text
    def pyrolysis_energy_kwh():
        if input.en() is True:
            return "Energy [kWh]:"
        else:
            return "Energie [kWh]:"

    @output
    @render.text
    def pyrolysis_waste_slider():
        if input.en() is True:
            return "Waste input [kg/hour]:"
        else:
            return "Přísun odpadu [kg/h]:"

    @output
    @render.text
    def pyrolysis_energy_mj():
        if input.en() is True:
            return "Energy [MJ]:"
        else:
            return "Energie [MJ]:"

    @output
    @render.text
    def pyrolysis_temperature_c():
        if input.en() is True:
            return "Temperature [°C]:"
        else:
            return "Teplota [°C]:"

    @output
    @render.text
    def nav_panel_optimization_title():
        if input.en() is True:
            return "Optimization"
        else:
            return "Optimalizace"

    @output
    @render.ui
    def optimization_problem_select():
        if input.en() is True:
            return ui.input_select(
                "select_opt",
                "Select a variable to maximize:",
                {"h2_gas": "Volume of H\u2082 [%] in gasification",
                 "liq_pyr": "Liquid fuel [kg] in pyrolysis"},
            )
        else:
            return ui.input_select(
                "select_opt",
                "Zvolte veličinu k maximalizaci:",
                {"h2_gas": "Objem H\u2082 [%] - gasifikace",
                 "liq_pyr": "Kapalné palivo [kg] - pyrolýza"},
            )

    @reactive.Calc
    def middle_temp_k():
        return 700 + 19050 * input.x2() / (input.x1() * input.x3())

    @reactive.Calc
    def middle_temp_c():
        return middle_temp_k() - 273.15

    @reactive.Calc
    def normal_temp_c():
        return middle_temp_c() * 0.01917 + 726.59

    @output
    @render.text
    def txt_plasmatron_mid_k():
        return "{:.1f}".format(middle_temp_k())

    @output
    @render.text
    def txt_plasmatron_mid_c():
        return "{:.1f}".format(middle_temp_c())

    @output
    @render.text
    def txt_plasmatron_norm_c():
        return "{:.1f}".format(normal_temp_c())

    @output
    @render.text
    def txt_plasmatron_norm_c_2():
        return "{:.1f}".format(normal_temp_c())

    @output
    @render.ui
    def gasification_model_select():
        if input.en() is True:
            return ui.input_select(
                "model_select",
                "Choose which model to use:",
                {#"sr": "Symbolic regression",
                 "poly": "Polynomial regression"}
            )
        else:
            return ui.input_select(
                "model_select",
                "Vyberte, který modely chcete použít:",
                {#"sr": "Symbolická regrese",
                 "poly": "Polynomiální regrese"}
            )

    @output
    @render.text
    def model_select_output():
        return input.model_select()

    @reactive.Calc
    def h2_vol():
        if default_model_select.get() == 'sr':
            return np.log(np.abs(0.000677729241918855 * normal_temp_c() ** 2 * np.abs(np.log(np.abs(
                0.0010822109 * normal_temp_c()) + 0.00000001)) ** (-2.6401255)) + 0.00000001)
        elif default_model_select.get() == 'poly':
            return 8.64427756e+02 + 0.00000000e+00 * normal_temp_c() + (
                -1.11535475e-02) * normal_temp_c() ** 2 + 2.50417715e-05 * normal_temp_c() ** 3 + (
                -2.08318518e-08) * normal_temp_c() ** 4 + 6.09290570e-12 * normal_temp_c() ** 5

    @reactive.Calc
    def co2_vol():
        if default_model_select.get() == 'sr':
            return np.log(
                np.abs(-0.060511474 * normal_temp_c() ** 2 + 44.81684 * normal_temp_c()) + 0.00000001) + 2.0503674
        elif default_model_select.get() == 'poly':
            return 7.88262261e+01 + 0.00000000e+00 * normal_temp_c() + (
                -1.42644743e-03) * normal_temp_c() ** 2 + 3.66824063e-06 * normal_temp_c() ** 3 + (
                -3.38728167e-09) * normal_temp_c() ** 4 + 1.07816591e-12 * normal_temp_c() ** 5

    @reactive.Calc
    def co_vol():
        if default_model_select.get() == 'sr':
            return 0.7548879 * normal_temp_c() / (0.07978012 * normal_temp_c() - 40.459797)
        elif default_model_select.get() == 'poly':
            return -7.75058073e+02 + 0.00000000e+00 * normal_temp_c() + (1.12213487e-02) * normal_temp_c() ** 2 + (
                -2.59664968e-05) * normal_temp_c() ** 3 + (2.22417149e-08) * normal_temp_c() ** 4 + (
                -6.70159810e-12) * normal_temp_c() ** 5

    @reactive.Calc
    def ch4_vol():
        if default_model_select.get() == 'sr':
            return np.abs(3.6089828 - 3679.8438 / (normal_temp_c() - 300.00784))
        elif default_model_select.get() == 'poly':
            return -1.35270631e+02 + 0.00000000e+00 * normal_temp_c() + 1.76696155e-03 * normal_temp_c() ** 2 + (
                -3.88540841e-06) * normal_temp_c() ** 3 + (3.15797384e-09) * normal_temp_c() ** 4 + (
                -9.02717242e-13) * normal_temp_c() ** 5

    @reactive.Calc
    def n2_vol():
        if default_model_select.get() == 'sr':
            return np.abs(0.000001013 * normal_temp_c() - 0.0017925174) ** (-0.5535527)
        elif default_model_select.get() == 'poly':
            return -1.92588105e+02 + 0.00000000e+00 * normal_temp_c() + 3.07852112e-03 * normal_temp_c() ** 2 + (
                -6.98410588e-06) * normal_temp_c() ** 3 + (5.91052625e-09) * normal_temp_c() ** 4 + (
                -1.75956783e-12) * normal_temp_c() ** 5

    @output
    @render.plot
    def plot_gasification():
        labels = ['H\u2082', 'CO\u2082', 'CO', 'CH\u2084', 'N\u2082']
        if input.gasification_select() in ['Volume [%]', 'Volume [m\u00B3]', 'Moles']:
            value = [h2_vol(), co2_vol(), co_vol(), ch4_vol(), n2_vol()]
        elif input.gasification_select() in ['Mass [g]', 'Mass [kg]', 'Mass [%]']:
            value = [h2_kg(), co2_kg(), co_kg(), ch4_kg(), n2_kg()]
        colors = ["#00524C", "#007A72", "#00A499", "#00CCBE", "#66E7DE"]
        fig, ax = plt.subplots()
        ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        fig.tight_layout()

    @output
    @render.plot
    def plot_models():
        x = np.linspace(746, 1100, 3541)
        y_h2 = np.log(
            np.abs(0.000677729241918855 * x ** 2 * np.abs(
                np.log(np.abs(0.0010822109 * x) + 0.00000001)) ** (-2.6401255)) + 0.00000001)
        y_co2 = (np.log(np.abs(-0.060511474 * x ** 2 + 44.81684 * x) + 0.00000001)
                 + 2.0503674)
        y_co = 0.7548879 * x / (0.07978012 * x - 40.459797)
        y_ch4 = np.abs(3.6089828 - 3679.8438 / (x - 300.00784))
        y_n2 = np.abs(0.000001013 * x - 0.0017925174) ** (-0.5535527)
        t = ((700 + 19050 * input.x2() / (input.x1() * input.x3())) - 273.15) * 0.01917 + 726.59
        fig, ax = plt.subplots()
        ax.plot(x, y_h2, label='H\u2082', color="#00524C")
        ax.plot(x, y_co2, label='CO\u2082', color="#007A72")
        ax.plot(x, y_co, label='CO', color="#00A499")
        ax.plot(x, y_ch4, label='CH\u2084', color="#00CCBE")
        ax.plot(x, y_n2, label='N\u2082', color="#66E7DE")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.axvline(x=t, color='#BABABA', linestyle='dashed')
        fig.tight_layout()

    @output
    @render.plot
    def plot_models2():
        x = np.linspace(746, 1100, 3541)
        if default_model_select.get() == 'sr':
            y_h2 = np.log(
                np.abs(0.000677729241918855 * x ** 2 * np.abs(
                    np.log(np.abs(0.0010822109 * x) + 0.00000001)) ** (-2.6401255)) + 0.00000001)
            y_co2 = (np.log(np.abs(-0.060511474 * x ** 2 + 44.81684 * x) + 0.00000001)
                     + 2.0503674)
            y_co = 0.7548879 * x / (0.07978012 * x - 40.459797)
            y_ch4 = np.abs(3.6089828 - 3679.8438 / (x - 300.00784))
            y_n2 = np.abs(0.000001013 * x - 0.0017925174) ** (-0.5535527)
        elif default_model_select.get() == 'poly':
            y_h2 = 8.64427756e+02 + 0.00000000e+00 * x + (
                -1.11535475e-02) * x ** 2 + 2.50417715e-05 * x ** 3 + (
                       -2.08318518e-08) * x ** 4 + 6.09290570e-12 * x ** 5
            y_co2 = 7.88262261e+01 + 0.00000000e+00 * x + (
                -1.42644743e-03) * x ** 2 + 3.66824063e-06 * x ** 3 + (
                        -3.38728167e-09) * x ** 4 + 1.07816591e-12 * x ** 5
            y_co = -7.75058073e+02 + 0.00000000e+00 * x + 1.12213487e-02 * x ** 2 + (
                -2.59664968e-05) * x ** 3 + 2.22417149e-08 * x ** 4 + (
                       -6.70159810e-12) * x ** 5
            y_ch4 = -1.35270631e+02 + 0.00000000e+00 * x + 1.76696155e-03 * x ** 2 + (
                -3.88540841e-06) * x ** 3 + 3.15797384e-09 * x ** 4 + (
                        -9.02717242e-13) * x ** 5
            y_n2 = -1.92588105e+02 + 0.00000000e+00 * x + 3.07852112e-03 * x ** 2 + (
                -6.98410588e-06) * x ** 3 + (5.91052625e-09) * x ** 4 + (
                       -1.75956783e-12) * x ** 5
        t = ((700 + 19050 * input.x2() / (input.x1() * input.x3())) - 273.15) * 0.01917 + 726.59
        fig, ax = plt.subplots()
        ax.plot(x, y_h2, label='H\u2082', color="#00524C")
        ax.plot(x, y_co2, label='CO\u2082', color="#007A72")
        ax.plot(x, y_co, label='CO', color="#00A499")
        ax.plot(x, y_ch4, label='CH\u2084', color="#00CCBE")
        ax.plot(x, y_n2, label='N\u2082', color="#66E7DE")
        if input.en() is True:
            ax.set(xlabel='temperature', ylabel='volume [%]')
        else:
            ax.set(xlabel='teplota', ylabel='objem [%]')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.axvline(x=t, color='#BABABA', linestyle='dashed')
        # plt.legend(loc='upper left', bbox_to_anchor=(1.04, 1), frameon=False)
        plt.text(1103, 9, 'H\u2082', color="#00524C")
        plt.text(1103, 12.5, 'CO\u2082', color="#007A72")
        plt.text(1103, 17, 'CO', color="#00A499")
        plt.text(1103, 0, 'CH\u2084', color="#00CCBE")
        plt.text(1103, 57, 'N\u2082', color="#66E7DE")
        fig.tight_layout()

    @reactive.effect
    @reactive.event(input.plot_models_click)
    def _():
        m = ui.modal(ui.output_plot("plot_models2"),
                     size='l',
                     easy_close=True,
                     footer=None,
                     )
        ui.modal_show(m)

    @reactive.Calc
    def waste_volume():
        return input.waste() * waste_coefficient

    @output
    @render.text
    def txt_gasification_waste_m3():
        return "{:.1f}".format(waste_volume())

    @reactive.Calc
    def h2_m3():
        return h2_vol() * waste_volume() / 100

    @reactive.Calc
    def co2_m3():
        return co2_vol() * waste_volume() / 100

    @reactive.Calc
    def co_m3():
        return co_vol() * waste_volume() / 100

    @reactive.Calc
    def ch4_m3():
        return ch4_vol() * waste_volume() / 100

    @reactive.Calc
    def n2_m3():
        return n2_vol() * waste_volume() / 100

    @reactive.Calc
    def h2_n():
        return h2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def co2_n():
        return co2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def co_n():
        return co_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def ch4_n():
        return ch4_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def n2_n():
        return n2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def h2_kg():
        return h2_n() * mm_h2 / 1000

    @reactive.Calc
    def co2_kg():
        return co2_n() * mm_co2 / 1000

    @reactive.Calc
    def co_kg():
        return co_n() * mm_co / 1000

    @reactive.Calc
    def ch4_kg():
        return ch4_n() * mm_ch4 / 1000

    @reactive.Calc
    def n2_kg():
        return n2_n() * mm_n2 / 1000

    @reactive.Calc
    def sum_kg():
        return h2_kg() + co2_kg() + co_kg() + ch4_kg() + n2_kg()

    @output
    @render.data_frame
    def data_component_vol():
        sum = h2_vol() + co2_vol() + co_vol() + ch4_vol() + n2_vol()
        data_comp_vol = [
            ['H\u2082', "{:.1f}".format(h2_vol() / sum * 100), "{:.1f}".format(h2_m3()), "{:.4f}".format(h2_n()),
             "{:.1f}".format(h2_kg() * 1000),
             "{:.2f}".format(h2_kg()), "{:.1f}".format(h2_kg() / sum_kg() * 100)],
            ['CO\u2082', "{:.1f}".format(co2_vol() / sum * 100), "{:.1f}".format(co2_m3()), "{:.4f}".format(co2_n()),
             "{:.1f}".format(co2_kg() * 1000),
             "{:.2f}".format(co2_kg()), "{:.1f}".format(co2_kg() / sum_kg() * 100)],
            ['CO', "{:.1f}".format(co_vol() / sum * 100), "{:.1f}".format(co_m3()), "{:.4f}".format(co_n()),
             "{:.1f}".format(co_kg() * 1000),
             "{:.2f}".format(co_kg()), "{:.1f}".format(co_kg() / sum_kg() * 100)],
            ['CH\u2084', "{:.1f}".format(ch4_vol() / sum * 100), "{:.1f}".format(ch4_m3()), "{:.4f}".format(ch4_n()),
             "{:.1f}".format(ch4_kg() * 1000),
             "{:.2f}".format(ch4_kg()), "{:.1f}".format(ch4_kg() / sum_kg() * 100)],
            ["N\u2082", "{:.1f}".format(n2_vol() / sum * 100), "{:.1f}".format(n2_m3()), "{:.4f}".format(n2_n()),
             "{:.1f}".format(n2_kg() * 1000),
             "{:.2f}".format(n2_kg()), "{:.1f}".format(n2_kg() / sum_kg() * 100)],
            ['Sum',
             "{:.1f}".format(sum / sum * 100),
             "{:.1f}".format(h2_m3() + co2_m3() + co_m3() + ch4_m3() + n2_m3()),
             "{:.4f}".format(h2_n() + co2_n() + co_n() + ch4_n() + n2_n()),
             "{:.1f}".format(sum_kg() * 1000),
             "{:.1f}".format(sum_kg()),
             "{:.1f}".format(
                 (h2_kg() / sum_kg() * 100) + (co2_kg() / sum_kg() * 100) + (co_kg() / sum_kg() * 100)
                 + (ch4_kg() / sum_kg() * 100) + (n2_kg() / sum_kg() * 100))]]
        col_dict = {'Gas': 'Plyn',
                    'Volume [%]': 'Objem [%]',
                    'Volume [m\u00B3]': 'Objem [m\u00B3]',
                    'Moles': 'Látkové množství [mol]',
                    'Mass [g]': 'Hmotnost [g]',
                    'Mass [kg]': 'Hmotnost [kg]',
                    'Mass [%]': 'Hmotnost [%]'}
        if input.en() is True:
            col_names = ['Gas', 'Volume [%]', 'Volume [m\u00B3]', 'Moles', 'Mass [g]', 'Mass [kg]', 'Mass [%]']
            df_comp_vol = pd.DataFrame(data_comp_vol, columns=col_names)
            df_show = df_comp_vol[['Gas', input.gasification_select()]]
        else:
            col_names = ['Plyn', 'Objem [%]', 'Objem [m\u00B3]', 'Látkové množství [mol]', 'Hmotnost [g]',
                         'Hmotnost [kg]',
                         'Hmotnost [%]']
            df_comp_vol = pd.DataFrame(data_comp_vol, columns=col_names)
            df_show = df_comp_vol[['Plyn', col_dict[input.gasification_select()]]]
        return render.DataGrid(df_show, width="100%")

    @reactive.Calc
    def tank_fill():
        moles = input.tank_pressure() * 100000 * input.tank_volume() / (input.tank_temperature() * r_const)
        kg_h2 = moles * 2 / 1000
        return kg_h2 / h2_kg()

    @output
    @render.text
    def txt_tank_filling():
        return "{}".format(round(tank_fill()))

    @reactive.Calc
    def combustion_h2_kg():
        return h2_kg() * input.combustion_h2_percent() / 100

    @output
    @render.data_frame
    def data_combustion():
        if input.comb_heating_value_select() == "high":
            h2_hv = 142.081
            co_hv = 10.16
            ch4_hv = 55.384
        elif input.comb_heating_value_select() == "low":
            h2_hv = 120.087
            co_hv = 10.16
            ch4_hv = 49.853
        kwh_constant = 0.2777777778
        eff = input.combustion_efficiency() / 100
        data_comb = [
            ['H\u2082', "{:.2f}".format(combustion_h2_kg()), "{:.2f}".format(combustion_h2_kg() * h2_hv * eff),
             "{:.2f}".format(combustion_h2_kg() * h2_hv * eff * kwh_constant)],
            ['CO', "{:.2f}".format(co_kg()), "{:.2f}".format(co_kg() * co_hv * eff),
             "{:.2f}".format(co_kg() * co_hv * eff * kwh_constant)],
            ['CH\u2084', "{:.2f}".format(ch4_kg()), "{:.2f}".format(ch4_kg() * ch4_hv * eff),
             "{:.2f}".format(ch4_kg() * ch4_hv * eff * kwh_constant)]]
        # data_comb = [
        #     ['H\u2082', "{:.2f}".format(h2_kg()), "{:.2f}".format(h2_kg()*6*6),
        #      "{:.2f}".format(h2_kg()*65*6*636)],
        #     ['CO', "{:.2f}".format(co_kg()), "{:.2f}".format(co_kg()*7*7),
        #      "{:.2f}".format(co_kg()*6*4*1)],
        #     ['CH\u2084', "{:.2f}".format(ch4_kg()), "{:.2f}".format(ch4_kg()*1*7),
        #      "{:.2f}".format(ch4_kg()*3*4*5)]]
        if input.en() is True:
            col_names = ['Gas', 'Production [kg/hour]', 'Energy [MJ/hour]', 'Energy [kWh/hour]']
            df_comb = pd.DataFrame(data_comb, columns=col_names)
        else:
            col_names = ['Plyn', 'Produkce [kg/h]', 'Energie [MJ/h]', 'Energie [kWh/h]']
            df_comb = pd.DataFrame(data_comb, columns=col_names)
        return render.DataGrid(df_comb, width="100%")

    @reactive.Calc
    def fuel_cell_h2_kg():
        return h2_kg() - combustion_h2_kg()

    @output
    @render.text
    def txt_h2_kg_ee():
        return "{:.2f}".format(fuel_cell_h2_kg())

    @reactive.Calc
    def ee_low():
        return fuel_cell_h2_kg() * low_heat_value_const

    @reactive.Calc
    def ee_high():
        return fuel_cell_h2_kg() * high_heat_value_const

    @reactive.Calc
    def ee_eff_low():
        return ee_low() * default_efficiency.get() / 100

    @reactive.Calc
    def ee_eff_high():
        return ee_high() * default_efficiency.get() / 100

    @reactive.Calc
    def calc_fuel_cell():
        if default_heating_value_select.get() == "low":
            return (fuel_cell_h2_kg() * low_heat_value_const) * default_efficiency.get() / 100
        if default_heating_value_select.get() == "high":
            return (fuel_cell_h2_kg() * high_heat_value_const) * default_efficiency.get() / 100

    @output
    @render.text
    def txt_fuel_cell():
        if input.fuel_cell_switch() is True:
            return "0"
        else:
            return "{:.1f}".format(calc_fuel_cell())

    @output
    @render.text
    def txt_electrolyzer_fuel_cell():
        return "{:.1f}".format(calc_fuel_cell())

    @output
    @render.text
    def txt_electrolyzer_kwh():
        return "{:.1f}".format(calc_fuel_cell())

    @output
    @render.text
    def txt_electrolyzer_h2():
        return "{:.2f}".format(input.grid_to_electrolyzer() / kwh_for_1_kg_h2)

    @output
    @render.text
    def txt_pyrolysis_mj():
        return "{:.1f}".format(input.energy() * 3.6)

    @reactive.Calc
    def pyrolysis_temperature():
        return (input.energy() * 3.6 + 1.5591) / 0.0425

    @output
    @render.text
    def txt_pyrolysis_temperature():
        return "{:.1f}".format(pyrolysis_temperature())

    @reactive.Calc
    def pyrolysis_co_vol():
        return 71.64571 - 0.18489 * pyrolysis_temperature() + 0.00018 * pyrolysis_temperature() ** 2

    @reactive.Calc
    def pyrolysis_co2_vol():
        return 76.631 - 0.0309 * pyrolysis_temperature() - 0.000070876 * pyrolysis_temperature() ** 2

    @reactive.Calc
    def pyrolysis_ch4_vol():
        return -35.957 + 0.1855 * pyrolysis_temperature() - 0.00014 * pyrolysis_temperature() ** 2

    @reactive.Calc
    def pyrolysis_h2_vol():
        return -10.5349 + 0.0235 * pyrolysis_temperature() + 0.0000336 * pyrolysis_temperature() ** 2

    @reactive.Calc
    def pyrolysis_m3_per_waste():
        return 0.612 * input.pyrolysis_waste()

    @reactive.Calc
    def pyrolysis_liquid_percent():
        return 30.2507 + 0.0246 * pyrolysis_temperature() - 0.000057833 * pyrolysis_temperature() ** 2

    @reactive.Calc
    def pyrolysis_m3_gas():
        return pyrolysis_m3_per_waste() * (11.3943 + 0.059 * pyrolysis_temperature()) / 100

    @reactive.Calc
    def pyrolysis_co_m3():
        return pyrolysis_m3_gas() * pyrolysis_co_vol() / 100

    @reactive.Calc
    def pyrolysis_co2_m3():
        return pyrolysis_m3_gas() * pyrolysis_co2_vol() / 100

    @reactive.Calc
    def pyrolysis_ch4_m3():
        return pyrolysis_m3_gas() * pyrolysis_ch4_vol() / 100

    @reactive.Calc
    def pyrolysis_h2_m3():
        return pyrolysis_m3_gas() * pyrolysis_h2_vol() / 100

    @reactive.Calc
    def pyrolysis_co_n():
        return pyrolysis_co_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def pyrolysis_co2_n():
        return pyrolysis_co2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def pyrolysis_ch4_n():
        return pyrolysis_ch4_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def pyrolysis_h2_n():
        return pyrolysis_h2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def pyrolysis_co_g():
        return pyrolysis_co_n() * mm_co

    @reactive.Calc
    def pyrolysis_co2_g():
        return pyrolysis_co2_n() * mm_co2

    @reactive.Calc
    def pyrolysis_ch4_g():
        return pyrolysis_ch4_n() * mm_ch4

    @reactive.Calc
    def pyrolysis_h2_g():
        return pyrolysis_h2_n() * mm_h2

    @reactive.Calc
    def pyrolysis_co_kg():
        return pyrolysis_co_n() * mm_co / 1000

    @reactive.Calc
    def pyrolysis_co2_kg():
        return pyrolysis_co2_n() * mm_co2 / 1000

    @reactive.Calc
    def pyrolysis_ch4_kg():
        return pyrolysis_ch4_n() * mm_ch4 / 1000

    @reactive.Calc
    def pyrolysis_h2_kg():
        return pyrolysis_h2_n() * mm_h2 / 1000

    @reactive.Calc
    def pyrolysis_kg_sum():
        return pyrolysis_co_kg() + pyrolysis_co2_kg() + pyrolysis_ch4_kg() + pyrolysis_h2_kg()

    @reactive.Calc
    def pyrolysis_co_kg_percent():
        return pyrolysis_co_kg() / pyrolysis_kg_sum() * 100

    @reactive.Calc
    def pyrolysis_co2_kg_percent():
        return pyrolysis_co2_kg() / pyrolysis_kg_sum() * 100

    @reactive.Calc
    def pyrolysis_ch4_kg_percent():
        return pyrolysis_ch4_kg() / pyrolysis_kg_sum() * 100

    @reactive.Calc
    def pyrolysis_h2_kg_percent():
        return pyrolysis_h2_kg() / pyrolysis_kg_sum() * 100

    @output
    @render.data_frame
    def pyrolysis_gas_vol():
        sum = pyrolysis_co2_vol() + pyrolysis_co_vol() + pyrolysis_ch4_vol() + pyrolysis_h2_vol()
        data = [['CO\u2082', "{:.1f}".format(pyrolysis_co2_vol() / sum * 100),
                 "{:.1f}".format(pyrolysis_co2_m3()),
                 "{:.4f}".format(pyrolysis_co2_n()),
                 "{:.1f}".format(pyrolysis_co2_g()),
                 "{:.2f}".format(pyrolysis_co2_kg()),
                 "{:.1f}".format(pyrolysis_co2_kg_percent())],
                ['CO', "{:.1f}".format(pyrolysis_co_vol() / sum * 100),
                 "{:.1f}".format(pyrolysis_co_m3()),
                 "{:.4f}".format(pyrolysis_co_n()),
                 "{:.1f}".format(pyrolysis_co_g()),
                 "{:.2f}".format(pyrolysis_co_kg()),
                 "{:.1f}".format(pyrolysis_co_kg_percent())],
                ['CH\u2084', "{:.1f}".format(pyrolysis_ch4_vol() / sum * 100),
                 "{:.1f}".format(pyrolysis_ch4_m3()),
                 "{:.4f}".format(pyrolysis_ch4_n()),
                 "{:.1f}".format(pyrolysis_ch4_g()),
                 "{:.2f}".format(pyrolysis_ch4_kg()),
                 "{:.1f}".format(pyrolysis_ch4_kg_percent())],
                ['H\u2082', "{:.1f}".format(pyrolysis_h2_vol() / sum * 100),
                 "{:.1f}".format(pyrolysis_h2_m3()),
                 "{:.4f}".format(pyrolysis_h2_n()),
                 "{:.1f}".format(pyrolysis_h2_g()),
                 "{:.2f}".format(pyrolysis_h2_kg()),
                 "{:.1f}".format(pyrolysis_h2_kg_percent())],
                ['Sum', "{:.1f}".format((pyrolysis_co2_vol() + pyrolysis_co_vol() + pyrolysis_ch4_vol() +
                                         pyrolysis_h2_vol()) / sum * 100),
                 "{:.1f}".format(pyrolysis_co2_m3() + pyrolysis_co_m3() + pyrolysis_ch4_m3() + pyrolysis_h2_m3()),
                 "{:.4f}".format(pyrolysis_co2_n() + pyrolysis_co_n() + pyrolysis_ch4_n() + pyrolysis_h2_n()),
                 "{:.1f}".format(pyrolysis_co2_g() + pyrolysis_co_g() + pyrolysis_ch4_g() + pyrolysis_h2_g()),
                 "{:.2f}".format(pyrolysis_co2_kg() + pyrolysis_co_kg() + pyrolysis_ch4_kg() + pyrolysis_h2_kg()),
                 "{:.1f}".format(pyrolysis_co2_kg_percent() + pyrolysis_co_kg_percent() + pyrolysis_ch4_kg_percent()
                                 + pyrolysis_h2_kg_percent())]]
        col_dict = {'Gas': 'Plyn',
                    'Volume [%]': 'Objem [%]',
                    'Volume [m\u00B3]': 'Objem [m\u00B3]',
                    'Moles': 'Látkové množství [mol]',
                    'Mass [g]': 'Hmotnost [g]',
                    'Mass [kg]': 'Hmotnost [kg]',
                    'Mass [%]': 'Hmotnost [%]'}
        if input.en() is True:
            col_names = ['Gas', 'Volume [%]', 'Volume [m\u00B3]', 'Moles', 'Mass [g]', 'Mass [kg]', 'Mass [%]']
            df_comp_vol = pd.DataFrame(data, columns=col_names)
            df_show = df_comp_vol[['Gas', input.pyrolysis_select()]]
        else:
            col_names = ['Plyn', 'Objem [%]', 'Objem [m\u00B3]', 'Látkové množství [mol]', 'Hmotnost [g]',
                         'Hmotnost [kg]',
                         'Hmotnost [%]']
            df_comp_vol = pd.DataFrame(data, columns=col_names)
            df_show = df_comp_vol[['Plyn', col_dict[input.pyrolysis_select()]]]
        return render.DataGrid(df_show, width="100%")

    @output
    @render.plot
    def plot_pyrolysis():
        labels = ['CO\u2082', 'CO', 'CH\u2084', "H\u2082"]
        if input.pyrolysis_select() in ['Volume [%]', 'Volume [m\u00B3]', 'Moles']:
            value = [pyrolysis_co2_vol(), pyrolysis_co_vol(), pyrolysis_ch4_vol(), pyrolysis_h2_vol()]
        elif input.pyrolysis_select() in ['Mass [g]', 'Mass [kg]', 'Mass [%]']:
            value = [pyrolysis_co2_kg(), pyrolysis_co_kg(), pyrolysis_ch4_kg(), pyrolysis_h2_kg()]
        colors = ["#00CCBE", "#00A499", "#007A72", "#00524C"]
        fig, ax = plt.subplots()
        ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        fig.tight_layout()

    @output
    @render.text
    def pyrolysis_gas():
        if input.en() is True:
            return "Gas [kg]:"
        else:
            return "Plyn [kg]:"

    @output
    @render.text
    def txt_pyrolysis_gas():
        return "{:.2f}".format(pyrolysis_kg_sum())

    @output
    @render.text
    def pyrolysis_liquid():
        if input.en() is True:
            return "Liquid fuel [kg]:"
        else:
            return "Kapalné palivo [kg]:"

    @output
    @render.text
    def txt_pyrolysis_liquid():
        return "{:.2f}".format(input.pyrolysis_waste() * pyrolysis_liquid_percent() / 100)

    @output
    @render.text
    def pyrolysis_biochar():
        if input.en() is True:
            return "Biochar [kg]:"
        else:
            return "Biouhel [kg]:"

    @output
    @render.text
    def txt_pyrolysis_biochar():
        return "{:.2f}".format(input.pyrolysis_waste() - pyrolysis_kg_sum() - (
                input.pyrolysis_waste() * pyrolysis_liquid_percent() / 100))

    @output
    @render.plot
    def plot_pyrolysis_state():
        if input.en() is True:
            labels = ['Liquid fuel', 'Gas', 'Biochar']
        else:
            labels = ['Kapalné palivo', 'Plyn', 'Biouhel']
        value = [pyrolysis_m3_per_waste() * pyrolysis_liquid_percent() / 100, pyrolysis_kg_sum(),
                 input.pyrolysis_waste() - pyrolysis_kg_sum() - (
                         pyrolysis_m3_per_waste() * pyrolysis_liquid_percent() / 100)]
        colors = ["#00CCBE", "#00A499", "#007A72"]
        fig, ax = plt.subplots()
        ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        fig.tight_layout()

    @render.text  # to check the select opt
    def check_select():
        return input.select_opt()

    @output
    @render.text
    def text_opt():
        if input.en() is True:
            return "The current choice of parameters: "
        else:
            return "Stávající parametry: "

    @output
    @render.table
    def df_opt_h2():
        if input.select_opt() == "h2_gas":
            if input.en() is True:
                params_now = [["Nozzle base constant", "{:.1f}".format(input.x1())],
                              ["Plasma torch power [kW] ", "{:.1f}".format(input.x2())],
                              ["Filling pressure [bar]", "{:.1f}".format(input.x3())],
                              ["Volume of H\u2082 [%]", "{:.2f}".format(h2_vol() / (h2_vol() + co2_vol() + co_vol() +
                                                                                    ch4_vol() + n2_vol()) * 100)]]
                df_params_now = pd.DataFrame(params_now, columns=['Parameter', 'Value'])
                return df_params_now.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
            else:
                params_now = [["Základní konstanta trysky", "{:.1f}".format(input.x1())],
                              ["Výkon plazmového hořáku [kW] ", "{:.1f}".format(input.x2())],
                              ["Plnící tlak [bar]", "{:.1f}".format(input.x3())],
                              ["Objem H\u2082 [%]", "{:.2f}".format(h2_vol() / (h2_vol() + co2_vol() + co_vol() +
                                                                                ch4_vol() + n2_vol()) * 100)]]
                df_params_now = pd.DataFrame(params_now, columns=['Parametr', 'Hodnota'])
                return df_params_now.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
        elif input.select_opt() == "liq_pyr":
            if input.en() is True:
                params_now = [["Energy [kW]", "{:.1f}".format(input.energy())],
                              ["Liquid fuel [kg]", "{:.2f}".format(input.pyrolysis_waste() *
                                                                   pyrolysis_liquid_percent() / 100)]]
                df_params_now = pd.DataFrame(params_now, columns=['Parameter', 'Value'])
                return df_params_now.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
            else:
                params_now = [["Energie [kW]", "{:.1f}".format(input.energy())],
                              ["Kapalné palivo [kg]", "{:.2f}".format(input.pyrolysis_waste() *
                                                                      pyrolysis_liquid_percent() / 100)]]
                df_params_now = pd.DataFrame(params_now, columns=['Parametr', 'Hodnota'])
                return df_params_now.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])

    @output
    @render.ui
    def ui_h2_gas_opt_options():
        if input.select_opt() == "h2_gas":
            if input.en() is True:
                return ui.div(
                    ui.br(),
                    "Optionally, choose a parameter and its value to be fixed during the "
                    "optimization process:",
                    ui.br(),
                    ui.br(),
                    ui.row(ui.column(6,
                                     ui.input_checkbox("fix_nozzle",
                                                       "Base constant of the nozzle",
                                                       False)
                                     ),
                           ui.column(6, ui.output_ui("ui_checkbox_nozzle")
                                     )
                           ),
                    ui.row(ui.column(6,
                                     ui.input_checkbox("fix_plasma_torch",
                                                       "Power of the plasma torch",
                                                       False),
                                     ),
                           ui.column(6,
                                     ui.output_ui("ui_checkbox_plasma_torch"),
                                     )
                           ),
                    ui.row(
                        ui.column(6,
                                  ui.input_checkbox("fix_pressure",
                                                    "Filling pressure",
                                                    False)
                                  ),
                        ui.column(6,
                                  ui.output_ui("ui_checkbox_pressure")
                                  )
                    ))
            else:
                return ui.div(
                    ui.br(),
                    "Vyberte volitelné parametry, kterých hodnotu chcete zachovat:",
                    ui.br(),
                    ui.br(),
                    ui.row(ui.column(6,
                                     ui.input_checkbox("fix_nozzle",
                                                       "Základní konstanta trysky",
                                                       False)
                                     ),
                           ui.column(6, ui.output_ui("ui_checkbox_nozzle")
                                     )
                           ),
                    ui.row(ui.column(6,
                                     ui.input_checkbox("fix_plasma_torch",
                                                       "Výkon plazmového hořáku",
                                                       False),
                                     ),
                           ui.column(6,
                                     ui.output_ui("ui_checkbox_plasma_torch"),
                                     )
                           ),
                    ui.row(
                        ui.column(6,
                                  ui.input_checkbox("fix_pressure",
                                                    "Plnící tlak",
                                                    False)
                                  ),
                        ui.column(6,
                                  ui.output_ui("ui_checkbox_pressure")
                                  )
                    ))

    @render.ui
    def ui_checkbox_nozzle():
        if input.select_opt() == "h2_gas" and input.fix_nozzle():
            return ui.input_slider("fix_nozzle_value", "", value=10, min=5,
                                   max=20,
                                   step=0.1)

    @render.ui
    def ui_checkbox_plasma_torch():
        if input.select_opt() == "h2_gas" and input.fix_plasma_torch():
            return ui.input_slider("fix_plasma_torch_value", "", value=10,
                                   min=5,
                                   max=15,
                                   step=0.1)

    @render.ui
    def ui_checkbox_pressure():
        if input.select_opt() == "h2_gas" and input.fix_pressure():
            return ui.input_slider("fix_pressure_value", "", value=5, min=3, max=8,
                                   step=0.1)

    @render.ui
    def ui_action_button():
        if input.select_opt() in ["h2_gas", "liq_pyr"]:
            if input.en() is True:
                return ui.input_action_button("start_opt", "Start optimization")
            else:
                return ui.input_action_button("start_opt", "Začít optimalizaci")

    @output
    @render.plot
    def plot_opt_gasification():
        if input.select_opt() == "h2_gas":
            labels = ['H\u2082', 'CO\u2082', 'CO', 'CH\u2084', "N\u2082"]
            value = [h2_vol(), co2_vol(), co_vol(), ch4_vol(), n2_vol()]
            colors = ["#00524C", "#007A72", "#00A499", "#00CCBE", "#66E7DE"]
            fig, ax = plt.subplots()
            ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        elif input.select_opt() == "liq_pyr":
            if input.en() is True:
                labels = ['Liquid fuel', 'Gas', 'Biochar']
            else:
                labels = ['Kapalné palivo', 'Plyn', 'Biouhel']
            value = [input.pyrolysis_waste() * pyrolysis_liquid_percent() / 100, pyrolysis_kg_sum(),
                     input.pyrolysis_waste() - pyrolysis_kg_sum() - (
                             pyrolysis_m3_per_waste() * pyrolysis_liquid_percent() / 100)]
            colors = ["#00CCBE", "#00A499", "#007A72"]
            fig, ax = plt.subplots()
            ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
            fig.tight_layout()

    h2_opt_res_x1 = reactive.Value(0.00)
    h2_opt_res_x2 = reactive.Value(0.00)
    h2_opt_res_x3 = reactive.Value(0.00)
    h2_opt_res_fmax = reactive.Value(0.00)
    h2_opt_pyr_e = reactive.Value(0.00)
    h2_opt_pyr_res = reactive.Value(0.00)
    counter = reactive.Value(0)

    @reactive.Effect
    @reactive.event(input.start_opt)
    def _():
        if input.en() is True:
            message = "Calculation in progress"
        else:
            message = "Probíhá optimalizace"
        if input.select_opt() == "h2_gas":

            def h2_vol_opt(x, y, z):
                if default_model_select.get() == 'sr':
                    return -(np.log(
                        np.abs(
                            0.000677729241918855 * (((700 + (19050 * y) / (x * z)) - 273.15) * 0.01917 + 726.59) ** 2 *
                            np.abs(
                                np.log(
                                    np.abs(0.0010822109 * (((700 + (19050 * y) / (x * z)) - 273.15) * 0.01917 + 726.59))
                                    + 0.00000001)) ** (-2.6401255)) + 0.00000001))
                elif default_model_select.get() == 'poly':
                    return -(8.64427756e+02 + (-1.11535475e-02) * (
                            (((700 + (19050 * y) / (x * z)) - 273.15) * 0.01917 + 726.59) ** 2) + 2.50417715e-05 * (
                                     (((700 + (19050 * y) / (x * z)) - 273.15) * 0.01917 + 726.59) ** 3) + (
                                 -2.08318518e-08) * (
                                     (((700 + (19050 * y) / (
                                             x * z)) - 273.15) * 0.01917 + 726.59) ** 4) + 6.09290570e-12 * (
                                     (((700 + (19050 * y) / (x * z)) - 273.15) * 0.01917 + 726.59) ** 5))

            if counter.get() == 0:
                xl = np.array([5, 5, 3]).astype(float)
                xu = np.array([20, 15, 8]).astype(float)
                if input.fix_nozzle():
                    xl[0] = xu[0] = input.fix_nozzle_value()
                if input.fix_plasma_torch():
                    xl[1] = xu[1] = input.fix_plasma_torch_value()
                if input.fix_pressure():
                    xl[2] = xu[2] = input.fix_pressure_value()

                def wrapped_h2_vol_opt(x_vec):
                    """Wrapper so the function accepts a vector instead of 3 scalars"""
                    return h2_vol_opt(x_vec[0], x_vec[1], x_vec[2])

                def update_progress(gen):
                        p.set(gen)

                max_gen = 100

                from scipy.optimize import minimize
                from scipy.optimize import differential_evolution
                from scipy import optimize

                # Prepare bounds – assuming xl and xu are arrays/lists of length 3

                bounds_list = [(xl[i], xu[i]) for i in range(3)]
                bounds = np.array(bounds_list)

                initial_guess = xl
                minimizer_kwargs = {"method": "BFGS"}
                def print_fun(x, f, accepted):
                    print("at minimum %.4f accepted %d" % (f, int(accepted)))

                # result = optimize.basinhopping(wrapped_h2_vol_opt, x0 = xl,niter=500,minimizer_kwargs=minimizer_kwargs,callback=print_fun)
                # print(result)
                # print("-----",result.fun)
                # # Show results
                # X = result.x
                # print(X[0])
                # h2_opt_res_x1.set(X[0].round(1))
                # h2_opt_res_x2.set(X[1].round(1))
                # h2_opt_res_x3.set(X[2].round(1))
                #
                # max_val = result.fun.round(2)
                # h2_opt_res_fmax.set(-max_val)



# --------------------------------------------------------------------------------------
                # with ui.Progress(min=0, max=max_gen) as p:
                #     p.set(message=message)
                #     result = differential_evolution(
                #             wrapped_h2_vol_opt,
                #             bounds,
                #             # init = 'sobol',
                #             maxiter=max_gen, popsize=50, tol=1e-13)
                #     print(result)
                #     # Show results
                #     X = result.x
                #     h2_opt_res_x1.set(X[0])
                #     h2_opt_res_x2.set(X[1])
                #     h2_opt_res_x3.set(X[2])
                #
                #     max_val = result.fun
                #     h2_opt_res_fmax.set(-max_val)


#----------------------------------------------------------------------------
                with ui.Progress(min=0, max=max_gen) as p:

                    p.set(message=message)

                    best_x, best_f = simple_ga_optimize_pyr(
                        wrapped_h2_vol_opt,
                        bounds=bounds_list,
                        progress_callback=update_progress
                    )
                    print(best_x)

                    # Show results
                    h2_opt_res_x1.set(best_x[0])
                    h2_opt_res_x2.set(best_x[1])
                    h2_opt_res_x3.set(best_x[2])

                    max_val = wrapped_h2_vol_opt(best_x)
                    h2_opt_res_fmax.set(-max_val)

        elif input.select_opt() == "liq_pyr":
            def liquid_opt_pyr(e):
                return -(30.2507 + 0.0246 * ((e * 3.6 + 1.5591) / 0.0425) - 0.000057833 * (
                        (e * 3.6 + 1.5591) / 0.0425) ** 2)

            if counter.get() == 0:
                def update_progress(gen):
                        p.set(gen)

                max_gen = 200

                with ui.Progress(min=0, max=max_gen) as p:
                    p.set(message=message)

                    best_x, best_f = simple_ga_optimize_pyr(
                        liquid_opt_pyr,
                        bounds=[(3.3, 9.0)],
                        progress_callback=update_progress
                    )
                    max_e = best_x[0]
                    max_val = liquid_opt_pyr(max_e)
                    h2_opt_pyr_e.set(max_e)
                    h2_opt_pyr_res.set(-max_val)  # since maximizing

    @render.table
    def h2_vol_opt_results():
        if input.select_opt() == "h2_gas":
            if input.en() is True:
                opt_results = [["Nozzle base constant", "{:.1f}".format(h2_opt_res_x1.get())],
                               ["Plasma torch power [kW]", "{:.1f}".format(h2_opt_res_x2.get())],
                               ["Filling pressure [bar]", "{:.1f}".format(h2_opt_res_x3.get())],
                               ["Volume of H\u2082 [%]", "{:.2f}".format(h2_opt_res_fmax.get() /
                                                                         (opt_h2_vol() + opt_co2_vol() + opt_co_vol() +
                                                                          opt_ch4_vol() + opt_n2_vol()) * 100)]]
                df_opt_result = pd.DataFrame(opt_results, columns=['Parameter', 'Value'])
                return df_opt_result.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
            else:
                opt_results = [["Základní konstanta trysky", "{:.1f}".format(h2_opt_res_x1.get())],
                               ["Výkon plazmového hořáku [kW]", "{:.1f}".format(h2_opt_res_x2.get())],
                               ["Plnící tlak [bar]", "{:.1f}".format(h2_opt_res_x3.get())],
                               ["Objem H\u2082 [%]", "{:.2f}".format(h2_opt_res_fmax.get() /
                                                                     (opt_h2_vol() + opt_co2_vol() + opt_co_vol() +
                                                                      opt_ch4_vol() + opt_n2_vol()) * 100)]]
                df_opt_result = pd.DataFrame(opt_results, columns=['Parametr', 'Hodnota'])
                return df_opt_result.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
        elif input.select_opt() == "liq_pyr":
            if input.en() is True:
                opt_results = [["Energy [kW]", "{:.1f}".format(h2_opt_pyr_e.get())],
                               ["Liquid fuel [kg]", "{:.2f}".format(opt_pyrolysis_liquid_fuel())]]
                df_opt_result = pd.DataFrame(opt_results, columns=['Parameter', 'Value'])
                return df_opt_result.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])
            else:
                opt_results = [["Energie [kW]", "{:.1f}".format(h2_opt_pyr_e.get())],
                               ["Kapalné palivo [kg]", "{:.2f}".format(opt_pyrolysis_liquid_fuel())]]
                df_opt_result = pd.DataFrame(opt_results, columns=['Parametr', 'Hodnota'])
                return df_opt_result.style.hide(axis="index").set_table_styles(
                    [dict(selector="th", props=[("width", "25000000px")])])

    @reactive.Calc
    def opt_middle_temp_k():
        return 700 + 19050 * h2_opt_res_x2.get() / (h2_opt_res_x1.get() * h2_opt_res_x3.get())

    @reactive.Calc
    def opt_middle_temp_c():
        return opt_middle_temp_k() - 273.15

    @reactive.Calc
    def opt_normal_temp_c():
        return opt_middle_temp_c() * 0.01917 + 726.59

    @reactive.Calc
    def opt_h2_vol():
        if default_model_select.get() == 'sr':
            return np.log(np.abs(0.000677729241918855 * opt_normal_temp_c() ** 2 * np.abs(np.log(np.abs(
                0.0010822109 * opt_normal_temp_c()) + 0.00000001)) ** (-2.6401255)) + 0.00000001)
        elif default_model_select.get() == 'poly':
            return 8.64427756e+02 + 0.00000000e+00 * opt_normal_temp_c() + (
                -1.11535475e-02) * opt_normal_temp_c() ** 2 + 2.50417715e-05 * opt_normal_temp_c() ** 3 + (
                -2.08318518e-08) * opt_normal_temp_c() ** 4 + 6.09290570e-12 * opt_normal_temp_c() ** 5

    @reactive.Calc
    def opt_co2_vol():
        if default_model_select.get() == 'sr':
            return np.log(
                np.abs(
                    -0.060511474 * opt_normal_temp_c() ** 2 + 44.81684 * opt_normal_temp_c()) + 0.00000001) + 2.0503674
        elif default_model_select.get() == 'poly':
            return 7.88262261e+01 + 0.00000000e+00 * opt_normal_temp_c() + (
                -1.42644743e-03) * opt_normal_temp_c() ** 2 + 3.66824063e-06 * opt_normal_temp_c() ** 3 + (
                -3.38728167e-09) * opt_normal_temp_c() ** 4 + 1.07816591e-12 * opt_normal_temp_c() ** 5

    @reactive.Calc
    def opt_co_vol():
        if default_model_select.get() == 'sr':
            return 0.7548879 * opt_normal_temp_c() / (0.07978012 * opt_normal_temp_c() - 40.459797)
        elif default_model_select.get() == 'poly':
            return -7.75058073e+02 + 0.00000000e+00 * opt_normal_temp_c() + (
                1.12213487e-02) * opt_normal_temp_c() ** 2 + (
                -2.59664968e-05) * opt_normal_temp_c() ** 3 + (2.22417149e-08) * opt_normal_temp_c() ** 4 + (
                -6.70159810e-12) * opt_normal_temp_c() ** 5

    @reactive.Calc
    def opt_ch4_vol():
        if default_model_select.get() == 'sr':
            return np.abs(3.6089828 - 3679.8438 / (opt_normal_temp_c() - 300.00784))
        elif default_model_select.get() == 'poly':
            return -1.35270631e+02 + 0.00000000e+00 * opt_normal_temp_c() + 1.76696155e-03 * opt_normal_temp_c() ** 2 + (
                -3.88540841e-06) * opt_normal_temp_c() ** 3 + (3.15797384e-09) * opt_normal_temp_c() ** 4 + (
                -9.02717242e-13) * opt_normal_temp_c() ** 5

    @reactive.Calc
    def opt_n2_vol():
        if default_model_select.get() == 'sr':
            return np.abs(0.000001013 * opt_normal_temp_c() - 0.0017925174) ** (-0.5535527)
        elif default_model_select.get() == 'poly':
            return -1.92588105e+02 + 0.00000000e+00 * opt_normal_temp_c() + 3.07852112e-03 * opt_normal_temp_c() ** 2 + (
                -6.98410588e-06) * opt_normal_temp_c() ** 3 + (5.91052625e-09) * opt_normal_temp_c() ** 4 + (
                -1.75956783e-12) * opt_normal_temp_c() ** 5

    @reactive.Calc
    def opt_pyrolysis_temperature():
        return (h2_opt_pyr_e.get() * 3.6 + 1.5591) / 0.0425

    @reactive.Calc
    def opt_pyrolysis_co_vol():
        return 71.64571 - 0.18489 * opt_pyrolysis_temperature() + 0.00018 * opt_pyrolysis_temperature() ** 2

    @reactive.Calc
    def opt_pyrolysis_co2_vol():
        return 76.631 - 0.0309 * opt_pyrolysis_temperature() - 0.000070876 * opt_pyrolysis_temperature() ** 2

    @reactive.Calc
    def opt_pyrolysis_ch4_vol():
        return -35.957 + 0.1855 * opt_pyrolysis_temperature() - 0.00014 * opt_pyrolysis_temperature() ** 2

    @reactive.Calc
    def opt_pyrolysis_h2_vol():
        return -10.5349 + 0.0235 * opt_pyrolysis_temperature() + 0.0000336 * opt_pyrolysis_temperature() ** 2

    @reactive.Calc
    def opt_pyrolysis_liquid_percent():
        return 30.2507 + 0.0246 * opt_pyrolysis_temperature() - 0.000057833 * opt_pyrolysis_temperature() ** 2

    @reactive.Calc
    def opt_pyrolysis_m3_gas():
        return pyrolysis_m3_per_waste() * (11.3943 + 0.059 * opt_pyrolysis_temperature()) / 100

    @reactive.Calc
    def opt_pyrolysis_co_m3():
        return opt_pyrolysis_m3_gas() * opt_pyrolysis_co_vol() / 100

    @reactive.Calc
    def opt_pyrolysis_co2_m3():
        return opt_pyrolysis_m3_gas() * opt_pyrolysis_co2_vol() / 100

    @reactive.Calc
    def opt_pyrolysis_ch4_m3():
        return opt_pyrolysis_m3_gas() * opt_pyrolysis_ch4_vol() / 100

    @reactive.Calc
    def opt_pyrolysis_h2_m3():
        return opt_pyrolysis_m3_gas() * opt_pyrolysis_h2_vol() / 100

    @reactive.Calc
    def opt_pyrolysis_co_n():
        return opt_pyrolysis_co_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def opt_pyrolysis_co2_n():
        return opt_pyrolysis_co2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def opt_pyrolysis_ch4_n():
        return opt_pyrolysis_ch4_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def opt_pyrolysis_h2_n():
        return opt_pyrolysis_h2_m3() / volume_1_mol_normal_cond

    @reactive.Calc
    def opt_pyrolysis_co_g():
        return opt_pyrolysis_co_n() * mm_co

    @reactive.Calc
    def opt_pyrolysis_co2_g():
        return opt_pyrolysis_co2_n() * mm_co2

    @reactive.Calc
    def opt_pyrolysis_ch4_g():
        return opt_pyrolysis_ch4_n() * mm_ch4

    @reactive.Calc
    def opt_pyrolysis_h2_g():
        return opt_pyrolysis_h2_n() * mm_h2

    @reactive.Calc
    def opt_pyrolysis_co_kg():
        return opt_pyrolysis_co_n() * mm_co / 1000

    @reactive.Calc
    def opt_pyrolysis_co2_kg():
        return opt_pyrolysis_co2_n() * mm_co2 / 1000

    @reactive.Calc
    def opt_pyrolysis_ch4_kg():
        return opt_pyrolysis_ch4_n() * mm_ch4 / 1000

    @reactive.Calc
    def opt_pyrolysis_h2_kg():
        return opt_pyrolysis_h2_n() * mm_h2 / 1000

    @reactive.Calc
    def opt_pyrolysis_kg_sum():
        return opt_pyrolysis_co_kg() + opt_pyrolysis_co2_kg() + opt_pyrolysis_ch4_kg() + opt_pyrolysis_h2_kg()

    @reactive.Calc
    def opt_pyrolysis_liquid_fuel():
        return input.pyrolysis_waste() * opt_pyrolysis_liquid_percent() / 100

    @reactive.Calc
    def opt_pyrolysis_gas():
        return opt_pyrolysis_kg_sum()

    @reactive.Calc
    def opt_pyrolysis_biochar():
        return input.pyrolysis_waste() - opt_pyrolysis_kg_sum() - opt_pyrolysis_liquid_fuel()

    @output
    @render.plot
    def plot_h2_vol_opt_results():
        if input.select_opt() == "h2_gas":
            labels = ['H\u2082', 'CO\u2082', 'CO', 'CH\u2084', "N\u2082"]
            value = [opt_h2_vol(), opt_co2_vol(), opt_co_vol(), opt_ch4_vol(), opt_n2_vol()]
            colors = ["#00524C", "#007A72", "#00A499", "#00CCBE", "#66E7DE"]
            fig, ax = plt.subplots()
            ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        elif input.select_opt() == "liq_pyr":
            if input.en() is True:
                labels = ['Liquid fuel', 'Gas', 'Biochar']
            else:
                labels = ['Kapalné palivo', 'Plyn', 'Biouhel']
            value = [opt_pyrolysis_liquid_fuel(), opt_pyrolysis_gas(), opt_pyrolysis_biochar()]
            colors = ["#00CCBE", "#00A499", "#007A72"]
            fig, ax = plt.subplots()
            ax.pie(value, labels=labels, colors=colors, wedgeprops={"linewidth": 1, "edgecolor": "white"})

    @reactive.Effect
    @reactive.event(input.start_opt)
    def _():
        if counter.get() == 0:
            ui.insert_ui(
                ui.div(ui.row(
                    ui.column(6,
                              ui.br(),
                              ui.output_text("opt_results_intro_text"),
                              ui.br(),
                              ui.output_table("h2_vol_opt_results"),
                              ),
                    ui.column(6,
                              ui.HTML('<p style="margin-bottom:3px;"> </p>'),
                              ui.br(),
                              ui.output_plot("plot_h2_vol_opt_results", height="200px")
                              )
                ),
                    ui.br(),
                    ui.br(),
                    ui.br(),
                    ui.br(),
                    ui.br(),
                    ui.br(),
                    ui.row(
                        ui.column(6,
                                  ui.output_ui("use_opt_vals_button")),
                        ui.column(6,
                                  ui.output_ui("reset_opt_button")))
                    ,
                    id="result_div"),
                selector="#start_opt",
                where="afterEnd",
            )
            counter.set(counter.get() + 1)

    @output
    @render.text
    def opt_results_intro_text():
        if input.en() is True:
            return "The optimization results:"
        else:
            return "Výsledky optimalizace:"

    @output
    @render.ui
    def use_opt_vals_button():
        if input.en() is True:
            return ui.input_action_button("opt_values", "Use the optimized values")
        else:
            return ui.input_action_button("opt_values", "Použít parametry")

    @output
    @render.ui
    def reset_opt_button():
        if input.en() is True:
            return ui.input_action_button("reset_opt", "Reset the optimization")
        else:
            return ui.input_action_button("reset_opt", "Resetovat optimalizaci")

    @reactive.Effect
    @reactive.event(input.opt_values)
    def _():
        if input.select_opt() == "h2_gas":
            ui.update_slider("x1", value=h2_opt_res_x1.get())
            ui.update_slider("x2", value=h2_opt_res_x2.get())
            ui.update_slider("x3", value=h2_opt_res_x3.get())
            ui.remove_ui(selector="div#result_div")
            counter.set(0)
            ui.update_checkbox("fix_nozzle", value=False)
            ui.update_checkbox("fix_plasma_torch", value=False)
            ui.update_checkbox("fix_pressure", value=False)
        elif input.select_opt() == "liq_pyr":
            ui.update_slider("energy", value=h2_opt_pyr_e.get())
            ui.remove_ui(selector="div#result_div")
            counter.set(0)

    @reactive.Effect
    @reactive.event(input.reset_opt)
    def _():
        ui.remove_ui(selector="div#result_div")
        counter.set(0)
        ui.update_checkbox("fix_nozzle", value=False)
        ui.update_checkbox("fix_plasma_torch", value=False)
        ui.update_checkbox("fix_pressure", value=False)

    @reactive.Effect
    @reactive.event(input.select_opt)
    def _():
        counter.set(0)

    @reactive.Effect
    @reactive.event(input.en)
    def _():
        counter.set(0)

    @reactive.Effect
    @reactive.event(input.fuel_cell_switch)
    def _():
        if input.fuel_cell_switch() is True:
            ui.update_slider("combustion_h2_percent", value=100)
        else:
            ui.update_slider("combustion_h2_percent", value=0)


www_dir = Path(__file__).parent / "www"
# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server, static_assets=www_dir)
