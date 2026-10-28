
import math

import folium
import networkx as nx
import osmnx as ox
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Bonn Alternative Route Finder",
    page_icon="🗺️",
    layout="wide",
)

st.title("Bonn Alternative Route Finder")
st.write(
    "Select a starting point and destination on the map, "
    "then compare the shortest driving route with two alternatives."
)
st.caption(
    "Uses OpenStreetMap road data. Distances are estimates; "
    "live traffic and current road closures are not included."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "origin": None,
    "destination": None,
    "click_stage": "origin",
    "route_results": [],
    "route_message": "",
    "last_processed_click": None,
    "map_version": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# LOAD BONN ROAD NETWORK
# --------------------------------------------------

@st.cache_resource(show_spinner="Loading Bonn's driving network...")
def load_road_graph():
    # OSMnx supplies road-edge lengths; no add_edge_lengths call is needed.
    return ox.graph_from_place(
        "Bonn, North Rhine-Westphalia, Germany",
        network_type="drive",
        simplify=True,
    )


# --------------------------------------------------
# ROUTE FUNCTIONS
# --------------------------------------------------

def nearest_node(graph, point):
    lat, lon = point

    return ox.distance.nearest_nodes(
        graph,
        X=lon,
        Y=lat,
    )


def get_edge(graph, u, v):
    """Choose the shortest available edge between two nodes."""
    edge_data = graph.get_edge_data(u, v)

    if not edge_data:
        return None

    return min(
        edge_data.values(),
        key=lambda data: float(data.get("length", math.inf)),
    )


def route_distance_km(graph, route):
    total_m = 0.0

    for u, v in zip(route[:-1], route[1:]):
        edge = get_edge(graph, u, v)

        if edge is not None:
            total_m += float(edge.get("length", 0.0))

    return total_m / 1000.0


def route_coordinates(graph, route):
    coordinates = []

    for u, v in zip(route[:-1], route[1:]):
        edge = get_edge(graph, u, v)

        if edge is None:
            continue

        geometry = edge.get("geometry")

        if geometry is not None:
            edge_coords = [
                (lat, lon)
                for lon, lat in geometry.coords
            ]
        else:
            edge_coords = [
                (
                    graph.nodes[u]["y"],
                    graph.nodes[u]["x"],
                ),
                (
                    graph.nodes[v]["y"],
                    graph.nodes[v]["x"],
                ),
            ]

        # Ensure coordinates follow the route's direction.
        u_xy = (
            graph.nodes[u]["x"],
            graph.nodes[u]["y"],
        )

        first_xy = (
            edge_coords[0][1],
            edge_coords[0][0],
        )

        last_xy = (
            edge_coords[-1][1],
            edge_coords[-1][0],
        )

        if math.dist(first_xy, u_xy) > math.dist(last_xy, u_xy):
            edge_coords.reverse()

        if coordinates and edge_coords:
            coordinates.extend(edge_coords[1:])
        else:
            coordinates.extend(edge_coords)

    if not coordinates:
        coordinates = [
            (
                graph.nodes[node]["y"],
                graph.nodes[node]["x"],
            )
            for node in route
        ]

    return coordinates


def calculate_routes(graph, origin, destination, max_routes=3):
    start = nearest_node(graph, origin)
    end = nearest_node(graph, destination)

    if start == end:
        raise ValueError(
            "The selected points are too close together. "
            "Choose points farther apart."
        )

    # Build a directed graph and retain the shortest parallel edge
    # between each pair of nodes.
    network = nx.DiGraph()

    for u, v, data in graph.edges(data=True):
        if data.get("length") is None:
            continue

        length = float(data["length"])
        existing = network.get_edge_data(u, v)

        if existing is None or length < existing["length"]:
            network.add_edge(u, v, length=length)

    if start not in network or end not in network:
        raise ValueError(
            "A connected driving road could not be found "
            "for one of the selected points."
        )

    paths = nx.shortest_simple_paths(
        network,
        start,
        end,
        weight="length",
    )

    results = []

    for nodes in paths:
        distance = route_distance_km(graph, nodes)
        coordinates = route_coordinates(graph, nodes)

        if distance > 0 and len(coordinates) >= 2:
            results.append(
                {
                    "nodes": nodes,
                    "distance_km": distance,
                    "coords": coordinates,
                }
            )

        # Three routes total: shortest + two alternatives.
        if len(results) >= max_routes:
            break

    if not results:
        raise ValueError(
            "No driving route could be calculated between these points."
        )

    return sorted(
        results,
        key=lambda item: item["distance_km"],
    )


# --------------------------------------------------
# PAGE LAYOUT
# --------------------------------------------------

map_col, panel_col = st.columns([2, 1])


# --------------------------------------------------
# CONTROL PANEL
# --------------------------------------------------

with panel_col:
    st.subheader("1. Choose your points")

    if st.session_state.click_stage == "origin":
        st.info("Click the map to select your starting point.")

    elif st.session_state.click_stage == "destination":
        st.info("Click the map again to select your destination.")

    else:
        st.success(
            "Both points are selected. Click Find Route below."
        )

    if st.session_state.origin:
        st.write(
            "**Start:** "
            f"{st.session_state.origin[0]:.5f}, "
            f"{st.session_state.origin[1]:.5f}"
        )
    else:
        st.write("**Start:** Not selected")

    if st.session_state.destination:
        st.write(
            "**Destination:** "
            f"{st.session_state.destination[0]:.5f}, "
            f"{st.session_state.destination[1]:.5f}"
        )
    else:
        st.write("**Destination:** Not selected")

    reset_col, clear_col = st.columns(2)

    with reset_col:
        if st.button("Reset points", use_container_width=True):
            st.session_state.origin = None
            st.session_state.destination = None
            st.session_state.click_stage = "origin"
            st.session_state.route_results = []
            st.session_state.route_message = ""
            st.session_state.last_processed_click = None
            st.session_state.map_version += 1
            st.rerun()

    with clear_col:
        if st.button("Clear routes", use_container_width=True):
            st.session_state.route_results = []
            st.session_state.route_message = ""
            st.rerun()

    st.subheader("2. Find your routes")

    if st.button(
        "Find Route",
        type="primary",
        use_container_width=True,
        disabled=not (
            st.session_state.origin
            and st.session_state.destination
        ),
    ):
        try:
            graph = load_road_graph()

            with st.spinner("Calculating the best three routes..."):
                st.session_state.route_results = calculate_routes(
                    graph,
                    st.session_state.origin,
                    st.session_state.destination,
                    max_routes=3,
                )

            st.session_state.route_message = (
                "Routes calculated successfully."
            )

        except nx.NetworkXNoPath:
            st.session_state.route_results = []
            st.session_state.route_message = (
                "No connected driving route was found."
            )

        except Exception as exc:
            st.session_state.route_results = []
            st.session_state.route_message = (
                f"Route calculation failed: {exc}"
            )

    if st.session_state.route_message:
        if st.session_state.route_results:
            st.success(st.session_state.route_message)
        else:
            st.error(st.session_state.route_message)


    # ----------------------------------------------
    # DISTANCE COMPARISON
    # ----------------------------------------------

    if st.session_state.route_results:
        st.subheader("3. Route distance comparison")

        routes = st.session_state.route_results
        shortest_km = routes[0]["distance_km"]

        st.metric(
            "Shortest route distance",
            f"{shortest_km:.2f} km",
        )

        for index, route in enumerate(routes):
            distance = route["distance_km"]
            difference = max(0.0, distance - shortest_km)

            percentage = (
                difference / shortest_km * 100
                if shortest_km > 0
                else 0.0
            )

            if index == 0:
                st.markdown("🔴 **Route 1 — Shortest route**")

                st.write(
                    f"Actual route distance: **{distance:.2f} km**"
                )

                st.write(
                    "Difference from shortest: **0.00 km (0.0%)**"
                )

            else:
                st.markdown(
                    f"**Route {index + 1} — Alternative route**"
                )

                st.write(
                    f"Actual route distance: **{distance:.2f} km**"
                )

                st.write(
                    f"Longer than shortest: **+{difference:.2f} km** "
                    f"({percentage:.1f}%)"
                )


# --------------------------------------------------
# MAP AND ROUTE DISPLAY
# --------------------------------------------------

with map_col:
    map_obj = folium.Map(
        location=[50.7374, 7.0982],
        zoom_start=13,
        control_scale=True,
    )

    routes = st.session_state.route_results

    # Draw the two alternatives first.
    alternative_colors = [
        "#2878B5",  # Blue
        "#2A9D55",  # Green
    ]

    for index, route in enumerate(routes[1:3]):
        folium.PolyLine(
            route["coords"],
            color=alternative_colors[index],
            weight=5,
            opacity=0.9,
            tooltip=(
                f"Alternative Route {index + 2}: "
                f"{route['distance_km']:.2f} km"
            ),
        ).add_to(map_obj)

    # Draw the shortest route last so it remains visible in red.
    if routes:
        shortest = routes[0]

        folium.PolyLine(
            shortest["coords"],
            color="#E31A1C",
            weight=8,
            opacity=1.0,
            tooltip=(
                f"Shortest Route: "
                f"{shortest['distance_km']:.2f} km"
            ),
        ).add_to(map_obj)

    if st.session_state.origin:
        folium.Marker(
            st.session_state.origin,
            tooltip="Starting point",
            icon=folium.Icon(
                color="green",
                icon="play",
            ),
        ).add_to(map_obj)

    if st.session_state.destination:
        folium.Marker(
            st.session_state.destination,
            tooltip="Destination",
            icon=folium.Icon(
                color="red",
                icon="flag",
            ),
        ).add_to(map_obj)

    map_data = st_folium(
        map_obj,
        height=650,
        use_container_width=True,
        key=f"bonn_route_map_{st.session_state.map_version}",
        returned_objects=["last_clicked"],
    )

    # Process each new map click once.
    click = map_data.get("last_clicked") if map_data else None

    if click:
        point = (
            float(click["lat"]),
            float(click["lng"]),
        )

        previous = st.session_state.last_processed_click

        is_new_click = (
            previous is None
            or abs(point[0] - previous[0]) > 0.00001
            or abs(point[1] - previous[1]) > 0.00001
        )

        if is_new_click:
            st.session_state.last_processed_click = point

            if st.session_state.click_stage == "origin":
                st.session_state.origin = point
                st.session_state.destination = None
                st.session_state.click_stage = "destination"
                st.session_state.route_results = []
                st.session_state.route_message = ""
                st.rerun()

            elif st.session_state.click_stage == "destination":
                st.session_state.destination = point
                st.session_state.click_stage = "ready"
                st.session_state.route_results = []
                st.session_state.route_message = ""
                st.rerun()


st.divider()

st.caption(
    "Map and road-network data: © OpenStreetMap contributors. "
    "Routes are calculated from mapped driving roads and do not "
    "account for live traffic or guarantee real-world travel times."
)
