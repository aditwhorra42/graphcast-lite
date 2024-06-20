from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, List
from enum import Enum


class Grid2MeshEdgeCreation(str, Enum):
    """The different strategies to create grid to mesh edges."""

    K_NEAREST = "k_nearest"
    RADIUS = "radius"


class Mesh2GridEdgeCreation(str, Enum):
    """The different strategies to create mesh to grid edges."""

    CONTAINED = "contained"


class GraphLayerType(str, Enum):
    ConvGCN = "conv_gcn"
    SimpleConv = "simple_conv"


class GraphBuildingConfig(BaseModel):
    """This defines the parameters for building the graph.

    mesh_size: int
        How many refinements to do on the multi-mesh.
    grid2mesh_edge_creation: Grid2MeshEdgeCreation
        The strategy to create the Grid2Mesh edges for encoding.
    mesh2grid_edge_creation: Mesh2GridEdgeCreation
        The strategy to create the Mesh2Grid edges for decoding.
    grid2mesh_radius_query: Optional[float]
        This needs to be passed if grid2mesh_edge_creation is 'radius'.
        Scalar that will be multiplied by the
        length of the longest edge of the finest mesh to define the radius of
        connectivity to use in the Grid2Mesh graph. Reasonable values are
        between 0.6 and 1. 0.6 reduces the number of grid points feeding into
        multiple mesh nodes and therefore reduces edge count and memory use, but
        1 gives better predictions.
    grid2mesh_k: Optional[int]:
        This needs to be passed if grid2mesh_edge_creation is 'k_nearest'. Each grid node
        will be connected to the nearest grid2mesh_k mesh nodes.
    mesh_levels: List[int]
        The list of mesh levels to use for processing.

    """

    # grid-to-mesh graph configs
    mesh_size: int
    grid2mesh_edge_creation: Grid2MeshEdgeCreation
    grid2mesh_radius_query: Optional[float] = None
    grid2mesh_k: Optional[int] = None

    # mesh graph configs
    mesh_levels: List[int]
    
    # mesh-to-grid graph configs
    mesh2grid_edge_creation: Mesh2GridEdgeCreation


class MLPBlock(BaseModel):
    mlp_hidden_dims: Optional[List[int]] = None
    output_dim: int
    use_layer_norm: bool
    layer_norm_mode: Optional[str] = None


class GraphBlock(BaseModel):
    layer_type: GraphLayerType
    hidden_dims: Optional[List[int]] = None
    output_dim: Optional[int] = None
    use_layer_norm: Optional[bool] = None
    layer_norm_mode: Optional[str] = None


class ModelConfig(BaseModel):
    mlp: Optional[MLPBlock] = None
    gcn: GraphBlock


class PipelineConfig(BaseModel):
    encoder: ModelConfig
    processor: ModelConfig
    decoder: ModelConfig
    residual_output: bool = False


class DataConfig(BaseModel):
    data_directory: str
    num_latitudes: int
    num_longitudes: int
    num_features: int
    num_timesteps: int


class ExperimentConfig(BaseModel):
    batch_size: int
    learning_rate: float
    num_epochs: int
    random_seed: Optional[int] = None
    graph: GraphBuildingConfig
    pipeline: PipelineConfig
    data: DataConfig
