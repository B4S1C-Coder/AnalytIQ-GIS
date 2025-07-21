from integrations.openweather import OpenWeatherAPI
from integrations.tool_integrator import ToolIntegrator

def get_prefabricated_tool_integrator() -> ToolIntegrator:
    """ A shortcut method to get a Pre-Configured ToolIntegrator. """
    return ToolIntegrator(tools=[ OpenWeatherAPI() ], suppress_warning=False)