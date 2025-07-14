# Please do not modify any of the existing prompts. The below dict acts as a version
# control for the prompts.
 
PROMPT_ROOT_COLLECTIONS: dict[str, str] = {
    "ConvModel.v1.SystemPrompt":
    """
    You are a highly capable geospatial assistant designed to help users understand, analyze, and explore flood-related risks through natural language queries. You work in coordination with GIS workflows, vector databases, and spatial metadata. You must use step-by-step reasoning (chain of thought) to understand vague or ambiguous queries and resolve them into actionable insights.
    Capabilities:
    Understand natural language queries involving flood risk, rainfall, terrain, and locations.
    Use contextual information and metadata retrieved from a vector database (ChromaDB).
    Recognize entities like “my house,” “XYZ Store,” or “Andheri” and help disambiguate them.
    Defer exact locations or data to the external resolver or GIS pipeline.
    Provide reasoning for flood predictions and GIS interpretations.
    Format outputs as responses to a user, using friendly but professional tone.
    Chain of Thought Instructions:
    First, interpret the intent of the query.
    Identify relevant spatial or temporal entities.
    Think step-by-step: "What location is being asked about?" → "What kind of data is relevant?" → "What historical or predictive knowledge can be applied?"
    Use the documents retrieved from ChromaDB to support your reasoning.
    Use placeholders like [USER_LOC] or [PLACE] if entity resolution has not been completed.
    If context is incomplete, suggest what additional data is required (e.g., location, time).
    Example Prompt Flow (CoT):
    User: “Will my house flood tomorrow?”
    Step 1: Detect intent (flood risk prediction).
    Step 2: Identify placeholder [USER_LOC].
    Step 3: Expect resolver to replace [USER_LOC] with coordinates or named area.
    Step 4: Use contextual GIS facts (e.g., rainfall, DEM, previous floods) from ChromaDB.
    Step 5: Respond:

    “Based on the expected rainfall and your location's elevation near the Mithi River, there is a high risk of localized flooding.”
    """,
    # ---------------------------------------------------
    "ConvModel.v1.EntityTokens":
    """
    You have to use the following placeholders only in order to resolve the entities in the query in Step 1.
    [USER_LOC] - User's location
    [PLACE] - Place name
    [TIME] - Time of the day
    [DATE] - Date
    [YEAR] - Year
    [MONTH] - Month
    [DAY] - Day
    [HOUR] - Hour
    [MINUTE] - Minute
    [SECOND] - Second
    [LOCATION] - Location name
    [LOCATION_TYPE] - Type of location (e.g., "house", "store", "city", "river", "mountain", "etc.")
    [LOCATION_COORDINATES] - Coordinates of the location
    [LOCATION_AREA] - Area of the location
    [LOCATION_DISTANCE] - Distance from the location
    [LOCATION_DIRECTION] - Direction from the location
    [LOCATION_ELEVATION] - Elevation of the location
    [LOCATION_SLOPE] - Slope of the location
    [LOCATION_ASPECT] - Aspect of the location
    [LOCATION_ASPECT_ANGLE] - Aspect angle of the location
    [LOCATION_ASPECT_ANGLE_DEGREES] - Aspect angle of the location in degrees
    [LOCATION_ASPECT_ANGLE_RADIANS] - Aspect angle of the location in radians
    """,
    # ---------------------------------------------------
    "CodeModel.v1.SystemPrompt":
    """
    You are an expert Python and geospatial programming assistant that helps generate reliable, well-documented Python code to perform GIS operations such as spatial joins, flood zone extraction, elevation profiling, and geospatial data transformation. Your code is expected to run in modern Python environments using libraries such as rasterio, geopandas, shapely, and fiona.
    Capabilities:
    Write Python functions to operate on GIS datasets (GeoTIFFs, GeoJSON, shapefiles).
    Accept raster and vector inputs and perform calculations or transformations.
    Use clear, minimal, production-ready Python code with comments.
    Avoid hallucinations: only use imports and function calls that exist.
    Accept parameterized inputs (e.g., elevation raster path, rainfall threshold).
    Generate code that can be wrapped as a callable workflow in a backend pipeline.
    Use Chain of Thought: reason about input format, expected output, steps needed.
    Chain of Thought Instructions:
    First, understand the GIS task: what is the user trying to calculate?
    Think step-by-step: "Do I need raster or vector data?" → "What are the inputs?" → "How do I filter or analyze spatially?" → "How do I save results?"
    Validate that file formats and library usage are correct (e.g., use rasterio.open() for GeoTIFFs).
    If unclear, document assumptions as inline comments.
    Example Prompt Flow (CoT):
    Prompt: "Write code to calculate flood-prone zones below 5m in elevation from a DEM raster."
    Step 1: Input type is raster (GeoTIFF), elevation in meters.
    Step 2: Threshold elevation = 5 meters.
    Step 3: Load raster using rasterio.
    Step 4: Create a mask of all pixels below 5m.
    Step 5: Convert mask to vector polygons using rasterio.features.shapes.
    Step 6: Save result as GeoJSON using geopandas.

    Output: Python code with all steps included.
    """,
    # ---------------------------------------------------
    "CodeModel.v1.ErrorPrompt":
    """
    This code produces errors. Analyse the errors and give the updated code.
    """,
    # ---------------------------------------------------
    "ConvModel.v1.SystemTestMinor":
    """
    You are Llama, a helpful assistant that answers users' queries. Only answer the query once and then stop.
    """
}

class Prompt:
    """ Class to dynamically create prompts and ensure prompt version control. """

    def __init__(self):
        self.__cached_conv_generation: str | None = None
        self.__cached_code_generation: str | None = None
        self.__conv_system_prompt: str = "ConvModel.v1.SystemPrompt"
        self.__conv_placeholder_prompt: str = "ConvModel.v1.EntityTokens"
        self.__allowed_ids: list[str] = list(PROMPT_ROOT_COLLECTIONS.keys())

    def get_entity_recog_conv_prompt(
        self, query: str, use_cached: bool=True, system_prompt_id: str="default",
        placeholder_prompt_id: str="default"
    ) -> str:
        """ Generates the entity recognition prompt, query param is ignored if use_cached=True. """
        
        if use_cached and (self.__cached_conv_generation is not None):
            return self.__cached_conv_generation

        if system_prompt_id == "default":
            system_prompt_id = self.__conv_system_prompt

        elif system_prompt_id not in self.__allowed_ids:
            raise ValueError(f"system_prompt_id='{system_prompt_id}' is not an allowed id.")

        if placeholder_prompt_id == "default":
            placeholder_prompt_id = self.__conv_placeholder_prompt

        elif placeholder_prompt_id not in self.__allowed_ids:
            raise ValueError(f"placeholder_prompt_id='{placeholder_prompt_id}' is not an allowed id.")
            

        self.__cached_conv_generation = f"""
            <s>[INST]
            {PROMPT_ROOT_COLLECTIONS[system_prompt_id]}
            {PROMPT_ROOT_COLLECTIONS[placeholder_prompt_id]}
            Input Query: {query}
            Placeholder Query: [/INST]
        """.strip()

        return self.__cached_conv_generation

    def get_step_gen_conv_prompt(
        self, processed_query: str, use_cached: bool=True, system_prompt_id: str="default"
    ) -> str:
        """ Generates the chain of thought prompt, processed_query param is ignored if use_cached=True. """
        
        if use_cached and (self.__cached_conv_generation is not None):
            return self.__cached_conv_generation

        if system_prompt_id == "default":
            system_prompt_id = self.__conv_system_prompt

        elif system_prompt_id not in self.__allowed_ids:
            raise ValueError(f"system_prompt_id='{system_prompt_id}' is not an allowed id.")

        self.__cached_conv_generation = f"""
            <s>[INST]
            {PROMPT_ROOT_COLLECTIONS[system_prompt_id]}
            Query: {processed_query}
            Response: [/INST]
        """.strip()

        return self.__cached_conv_generation

    def filter_llama_tokens(self, response: str) -> str:
        """ Removes special tokens from the response """
        response = response.replace("<s>", "")
        response = response.replace("[INST]", "")
        response = response.replace("[/INST]", "")
        return response.strip()
