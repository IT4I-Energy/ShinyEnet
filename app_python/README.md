# Shinyenet
This repository accompanies the research paper "In-House Simulation Software for a Data-Driven Waste-to-Energy Facility: An Example from the Czech Republic" and showcases the code associated with the [Shinyenet application](https://shinyenet.vsb.cz/).

The objective of the Shinyenet application is to simulate gasification processes used to convert communal waste into valuable energy resources. Communal waste mainly consists of organic materials such as biomass, as well as combustible fractions from household and industrial sources. Through gasification, this waste is transformed into synthetic gas—syngas—whose composition depends heavily on parameters such as the gasification temperature and the characteristics of the input waste.

Hydrogen is the primary target component of syngas because it can be used to generate electrical energy through fuel cells. Syngas also contains other useful components, such as methane and carbon monoxide, which can be used for heat or electricity production through combustion.

The application additionally supports simulations of hydrogen production via electrolyzers, which generate hydrogen from electricity. This reverse-mode functionality increases the operational flexibility of the simulated facility to meet different energy demands.

Besides gasification, the application can also simulate pyrolysis, a process primarily used for producing liquid fuels.

## Gasification
The gasification module is controlled by three main parameters: nozzle base constant, plasma torch power, and filling pressure. These can be adjusted using the sliders at the top of the tab. A fourth adjustable parameter is the amount of waste introduced into the system.

### Plasmatron
This tab displays the temperature and normalized temperature calculated from the selected parameters.

### Gasification chamber
The main gasification reactions occur in the gasification chamber. This tab shows all relevant process parameters. Users can choose between symbolic regression or polynomial regression models to calculate the amount of syngas produced as well as its composition.

### Hydrogen tank filling
Hydrogen produced in the gasification chamber is stored in hydrogen tanks. Users can adjust tank pressure, volume, and temperature to simulate the time required to fill the tank.

### Combustion
Combustion provides an alternative route for producing energy from hydrogen. It operates only when fuel cells are inactive or unable to consume all available hydrogen. In this simulation, users can configure the amount of hydrogen used for combustion and specify parameters such as efficiency and heating value.

### Fuel cell
Fuel cells serve as the primary method of converting hydrogen into electrical energy. Users can modify parameters such as efficiency, heating value, number of fuel cells, and their power. The main output shown is the amount of electrical energy generated.

### Electrolyzer
Electrolyzers operate in reverse to fuel cells, producing hydrogen from water using electricity. Users can specify the amount of electrical energy supplied by photovoltaics and the grid. The resulting hydrogen output is then calculated and displayed.

### Photovoltaics and wind turbine
Photovoltaic panels and wind turbines supply electricity to the battery system and electrolyzer. Users can adjust photovoltaic power, wind turbine power, and battery capacity. The tab displays system outputs, including energy consumed by the electrolyzer, energy routed to the battery or grid, and the time required to fully charge the battery.

<br/><br/>
<img src="www/ceet_diagram_en_new_3.png" alt="diagram" height="600">

## Pyrolysis
Pyrolysis is used to produce liquid fuel within the facility. Adjustable parameters include input energy and the amount of waste fed into the system. The simulation outputs the quantities of liquid fuel, gas, and biochar produced, along with the composition of the gas byproduct.

## Optimization
In this tab, users can select one of two optimization objectives: maximizing hydrogen production during gasification or maximizing liquid fuel production during pyrolysis. For gasification, one or more of the three main parameters may be fixed at user-defined values. After clicking the Start optimization button, the optimized parameter set is displayed. Users may then apply these optimized values to the simulation or reset the optimization results.

# License
This work is licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">
