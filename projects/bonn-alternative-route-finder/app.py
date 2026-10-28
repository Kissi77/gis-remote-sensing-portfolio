
import itertools
import math

import folium
import networkx as nx
import osmnx as ox
import streamlit as st
from streamlit_folium import st_folium


# ============================================================
# 1. APPLICATION SETTINGS
# ============================================================

st.set_page_config(
    page_title="Bonn Alternative Route Finder",
    page_icon="🗺️",
    layout="wide",
)

MAX_ROUTE_STRETCH = 1.35
MAX_SHARED_ROUTE = 0.85
MAX_CANDIDATE_PATHS = 300
MAX_ROUTES = 3

ROUTE_COLORS = ["blue", "green"]


# ============================================================
# 2. LOAD BONN'S DRIVING NETWORK
# ============================================================

@st.cache_resource(show_spinner="Loading Bonn's road network...")
def load_road_network():
    """
    Download the Bonn driving network and convert it to a
    directed graph. For parallel edges, retain the shortest
    edge between each pair of nodes.
    """
    graph = ox.graph_from_place(
        "Bonn, North Rhine-Westphalia, Germany",
        network_type="drive",
        simplify=True,
    )

    graph = ox.distance.add_edge_lengths(graph)

    directed_graph = nx.DiGraph()

    directed_graph.add_nodes_from(
        (node, attributes.copy())
        for node, attributes in graph.nodes(data=True)
    )

    for u, v, key, attributes in graph.edges(
        keys=True, data=True
    ):
        edge_attributes = attributes.copy()

        if not directed_graph.has_edge(u, v):
            directed_graph.add_edge(
                u, v, **edge_attributes
            )
        elif (
            edge_attributes.get("length", float("inf"))
            < directed_graph[u][v].get(
                "length", float("inf")
            )
        ):
            directed_graph[u][v].clear()
            directed_graph[u][v].update(edge_attributes)

    return directed_graph


# ============================================================
# 3. FIND THE SHORTEST ROUTE AND ALTERNATIVES
# ============================================================

def route_distance(graph, path):
    """Calculate route length in metres."""
    return sum(
        graph[u][v].get("length", 0)
        for u, v in zip(path[:-1], path[1:])
    )


def find_routes(graph, origin_node, destination_node):
    """
    Return the shortest-distance route and up to two
    alternatives.

    Alternatives must be within the maximum detour threshold
    and must not overlap too heavily with the shortest route.
    """
    if origin_node == destination_node:
        return []

    try:
        candidates = nx.shortest_simple_paths(
            graph,
            origin_node,
            destination_node,
            weight="length",
        )

        selected_routes = []
        shortest_distance = None
        shortest_edges = set()

        for path in itertools.islice(
            candidates, MAX_CANDIDATE_PATHS
        ):
            distance = route_distance(graph, path)

            if distance <= 0:
                continue

            if not selected_routes:
                shortest_distance = distance
                shortest_edges = set(
                    zip(path[:-1], path[1:])
                )

                selected_routes.append(
                    {"path": path, "distance": distance}
                )
                continue

            # Ignore routes that are excessively longer.
            if distance > shortest_distance * MAX_ROUTE_STRETCH:
                continue

            alternative_edges = set(
                zip(path[:-1], path[1:])
            )

            shared_ratio = (
                len(shortest_edges & alternative_edges)
                / max(len(shortest_edges), 1)
            )

            if shared_ratio >= MAX_SHARED_ROUTE:
                continue

            selected_routes.append(
                {"path": path, "distance": distance}
            )

            if len(selected_routes) >= MAX_ROUTES:
                break

        return selected_routes

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


# ============================================================
# 4. CONVERT A ROUTE INTO MAP COORDINATES
# ============================================================

def route_coordinates(graph, path):
    """
    Convert graph edges into Folium coordinates (latitude,
    longitude), preserving road geometries when available.
    """
    coordinates = []

    for u, v in zip(path[:-1], path[1:]):
        start_node = graph.nodes[u]
        end_node = graph.nodes[v]

        start_xy = (
            start_node["x"],
            start_node["y"],
        )
        end_xy = (
            end_node["x"],
            end_node["y"],
        )

        edge = graph[u][v]
        geometry = edge.get("geometry")

        if geometry is not None:
            edge_coords = list(geometry.coords)

            # Ensure the geometry follows the route direction.
            first_xy = edge_coords[0]
            last_xy = edge_coords[-1]

            forward_error = (
                math.dist(first_xy, start_xy)
                + math.dist(last_xy, end_xy)
            )

            reverse_error = (
                math.dist(last_xy, start_xy)
                + math.dist(first_xy, end_xy)
            )

            if reverse_error < forward_error:
                edge_coords.reverse()

            segment = [
                (lat, lon)
                for lon, lat in edge_coords
            ]

        else:
            segment = [
                (start_xy[1], start_xy[0]),
                (end_xy[1], end_xy[0]),
            ]

        for coordinate in segment:
            if (
                not coordinates
                or coordinate != coordinates[-1]
            ):
                coordinates.append(coordinate)

    return coordinates


# ============================================================
# 5. APPLICATION HEADER
# ============================================================

st.title("🗺️ Bonn Interactive Alternative Route Finder")

st.write(
    "Select an origin and destination on the map to "
    "calculate the shortest-distance driving route and "
    "explore alternative routes in Bonn, Germany."
)

st.info(
    "Click once to set your origin and a second time to "
    "set your destination. A third click starts a new "
    "journey. Routes are optimized by distance, not live "
    "travel time."
)

with st.expander("How to use the map"):
    st.markdown(
        """
        1. Click a location on the map to select the origin.
        2. Click another location to select the destination.
        3. Compare the shortest route with available alternatives.
        4. Click again to begin another journey.
        """
    )


# ============================================================
# 6. SESSION STATE
# ============================================================

if "origin" not in st.session_state:
    st.session_state.origin = None

if "destination" not in st.session_state:
    st.session_state.destination = None

if "last_processed_click" not in st.session_state:
    st.session_state.last_processed_click = None


# ============================================================
# 7. LOAD GRAPH AND PREPARE MAP
# ============================================================

try:
    G = load_road_network()

except Exception as error:
    st.error(
        "The Bonn road network could not be loaded. "
        "Please refresh the application and try again."
    )

    with st.expander("Technical details"):
        st.code(str(error))

    st.stop()


bonn_center = [50.7374, 7.0982]

route_map = folium.Map(
    location=bonn_center,
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True,
)

folium.Marker(
    bonn_center,
    tooltip="Bonn, Germany",
    icon=folium.Icon(color="cadetblue", icon="info-sign"),
).add_to(route_map)


# ============================================================
# 8. PROCESS ORIGIN AND DESTINATION
# ============================================================

# st_folium returns the most recent map click.
# Only process a click when its coordinates have changed.

# Routes are calculated below, after a destination is selected.
# The map is displayed again after route layers are added.


# ============================================================
# 9. SNAP LOCATIONS TO THE ROAD NETWORK
# ============================================================

def nearest_road_node(graph, location):
    """Find the nearest graph node to a clicked map location."""
    latitude, longitude = location

    return ox.distance.nearest_nodes(
        graph,
        X=longitude,
        Y=latitude,
    )


# ============================================================
# 10. DRAW ROUTES
# ============================================================

def add_route_to_map(
    route_map,
    graph,
    route,
    color,
    weight,
    label,
    show_on_top=False,
):
    """Draw one route using its road geometry."""
    coordinates = route_coordinates(
        graph, route["path"]
    )

    if len(coordinates) < 2:
        return

    folium.PolyLine(
        locations=coordinates,
        color=color,
        weight=weight,
        opacity=1.0,
        tooltip=(
            f"{label}: "
            f"{route['distance'] / 1000:.2f} km"
        ),
        smooth_factor=1,
    ).add_to(route_map)


# ============================================================
# 11. MAP DISPLAY AND CLICK HANDLING
# ============================================================

# Add origin and destination markers, when available.

if st.session_state.origin is not None:
    folium.Marker(
        st.session_state.origin,
        tooltip="Origin",
        popup="Origin",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(route_map)

if st.session_state.destination is not None:
    folium.Marker(
        st.session_state.destination,
        tooltip="Destination",
        popup="Destination",
        icon=folium.Icon(color="darkred", icon="flag"),
    ).add_to(route_map)


# Calculate routes if both locations have been selected.

routes = []

if (
    st.session_state.origin is not None
    and st.session_state.destination is not None
):
    try:
        origin_node = nearest_road_node(
            G, st.session_state.origin
        )

        destination_node = nearest_road_node(
            G, st.session_state.destination
        )

        routes = find_routes(
            G, origin_node, destination_node
        )

        if not routes:
            st.warning(
                "No suitable route was found between these "
                "locations. Try selecting different points."
            )

        else:
            # Draw alternatives FIRST, so the shortest route
            # will be drawn last and remain visible on overlaps.

            for index, route in enumerate(routes[1:]):
                color = ROUTE_COLORS[
                    index % len(ROUTE_COLORS)
                ]

                add_route_to_map(
                    route_map,
                    G,
                    route,
                    color=color,
                    weight=4,
                    label=f"Alternative {index + 1}",
                )

            # Draw the shortest route LAST, in red.
            # The thicker line helps it stand out where routes
            # share the same road segments.

            add_route_to_map(
                route_map,
                G,
                routes[0],
                color="red",
                weight=7,
                label="Shortest route",
                show_on_top=True,
            )

    except Exception as error:
        st.error(
            "An error occurred while calculating the routes."
        )

        with st.expander("Technical details"):
            st.code(str(error))


# ============================================================
# 12. DISPLAY THE MAP
# ============================================================

map_output = st_folium(
    route_map,
    height=620,
    use_container_width=True,
    returned_objects=["last_clicked"],
    key="bonn_route_map",
)

clicked = map_output.get("last_clicked")

if clicked:
    click_location = (
        round(clicked["lat"], 6),
        round(clicked["lng"], 6),
    )

    if click_location != st.session_state.last_processed_click:
        st.session_state.last_processed_click = click_location

        if st.session_state.origin is None:
            st.session_state.origin = click_location
            st.session_state.destination = None

        elif st.session_state.destination is None:
            st.session_state.destination = click_location

        else:
            # Third click: start a new journey.
            st.session_state.origin = click_location
            st.session_state.destination = None

        st.rerun()


# ============================================================
# 13. ROUTE COMPARISON
# ============================================================

if routes:
    st.subheader("Route Comparison")

    shortest_distance = routes[0]["distance"]

    columns = st.columns(len(routes))

    for index, route in enumerate(routes):
        distance_km = route["distance"] / 1000

        if index == 0:
            title = "🔴 Shortest Route"
            detour = 0.0

        else:
            title = f"Alternative {index}"
            detour = (
                (route["distance"] - shortest_distance)
                / shortest_distance
            ) * 100

        with columns[index]:
            st.markdown(f"**{title}**")

            st.metric(
                label="Road distance",
                value=f"{distance_km:.2f} km",
            )

            if index == 0:
                st.caption("Shortest-distance option")
            else:
                st.caption(f"{detour:.1f}% longer than shortest")

    st.caption(
        "Distances are calculated from the mapped road network. "
        "They are not live travel-time estimates."
    )


# ============================================================
# 14. SELECTED LOCATIONS AND DATA ATTRIBUTION
# ============================================================

with st.expander("Selected coordinates"):
    if st.session_state.origin is not None:
        st.write(
            "Origin (latitude, longitude):",
            st.session_state.origin,
        )

    if st.session_state.destination is not None:
        st.write(
            "Destination (latitude, longitude):",
            st.session_state.destination,
        )

st.divider()

st.caption(
    "Road network data © OpenStreetMap contributors. "
    "Routing uses OSMnx and NetworkX."
)

st.caption(
    "This application does not include live traffic, "
    "temporary road closures, or travel-time optimization."
)
