
import hashlib
from itertools import islice

import folium
import networkx as nx
import osmnx as ox
import streamlit as st
from streamlit_folium import st_folium


# ============================================================
# BONN INTERACTIVE ALTERNATIVE ROUTE FINDER
# ============================================================

PLACE = "Bonn, North Rhine-Westphalia, Germany"

N_ALTERNATIVES = 2
MAX_STRETCH = 1.35
MAX_SHARED = 0.85
MAX_CANDIDATES = 300

ROUTE_COLOURS = ["red", "blue", "green"]

st.set_page_config(
    page_title="Bonn Alternative Route Finder",
    page_icon="🗺️",
    layout="wide",
)

st.title("Bonn Interactive Alternative Route Finder")

st.write(
    "Select an origin and destination by clicking the map. "
    "Calculate the shortest-distance driving route and explore "
    "up to two alternative routes."
)

st.caption(
    "Routing objective: shortest distance. Road network: OpenStreetMap."
)


# ============================================================
# 1. LOAD BONN'S DRIVING ROAD NETWORK
# ============================================================

@st.cache_resource(show_spinner="Loading Bonn's road network...")
def load_graph():

    G = ox.graph_from_place(
        PLACE,
        network_type="drive",
        simplify=True,
    )

    G = ox.distance.add_edge_lengths(G)

    # Convert MultiDiGraph to DiGraph because
    # shortest_simple_paths does not support MultiDiGraph.
    H = nx.DiGraph()
    H.graph.update(G.graph)
    H.add_nodes_from(G.nodes(data=True))

    for u, v, data in G.edges(data=True):

        length = data.get("length")

        if length is None:
            continue

        if (
            not H.has_edge(u, v)
            or length < H[u][v]["length"]
        ):
            H.add_edge(u, v, **dict(data))

    return H


# ============================================================
# 2. ROUTING HELPER FUNCTIONS
# ============================================================

def route_distance(G, path):

    return sum(
        G[u][v]["length"]
        for u, v in zip(path[:-1], path[1:])
    )


def route_edges(path):

    return set(zip(path[:-1], path[1:]))


def shared_edge_ratio(candidate, shortest):

    reference_edges = route_edges(shortest)
    candidate_edges = route_edges(candidate)

    if not reference_edges:
        return 1.0

    return (
        len(reference_edges & candidate_edges)
        / len(reference_edges)
    )


def edge_coordinates(G, u, v):
    """Return actual road geometry as latitude-longitude pairs."""

    ux, uy = G.nodes[u]["x"], G.nodes[u]["y"]
    vx, vy = G.nodes[v]["x"], G.nodes[v]["y"]

    geometry = G[u][v].get("geometry")

    if geometry is None:
        return [(uy, ux), (vy, vx)]

    coords = list(geometry.coords)

    if len(coords) < 2:
        return [(uy, ux), (vy, vx)]

    start, end = coords[0], coords[-1]

    forward_error = (
        (start[0] - ux) ** 2
        + (start[1] - uy) ** 2
        + (end[0] - vx) ** 2
        + (end[1] - vy) ** 2
    )

    reverse_error = (
        (end[0] - ux) ** 2
        + (end[1] - uy) ** 2
        + (start[0] - vx) ** 2
        + (start[1] - vy) ** 2
    )

    if reverse_error < forward_error:
        coords.reverse()

    return [(lat, lon) for lon, lat in coords]


def route_geometry(G, path):

    coordinates = []

    for u, v in zip(path[:-1], path[1:]):

        segment = edge_coordinates(G, u, v)

        if not coordinates:
            coordinates.extend(segment)

        elif coordinates[-1] == segment[0]:
            coordinates.extend(segment[1:])

        else:
            coordinates.extend(segment)

    return coordinates


# ============================================================
# 3. CALCULATE SHORTEST ROUTE AND ALTERNATIVES
# ============================================================

def calculate_routes(G, origin, destination):

    source = ox.distance.nearest_nodes(
        G,
        X=origin[1],
        Y=origin[0],
    )

    target = ox.distance.nearest_nodes(
        G,
        X=destination[1],
        Y=destination[0],
    )

    if source == target:
        raise ValueError(
            "Both locations snapped to the same road node. "
            "Choose locations farther apart."
        )

    if not nx.has_path(G, source, target):
        raise nx.NetworkXNoPath(
            "No driving route exists between these locations."
        )

    path_generator = nx.shortest_simple_paths(
        G,
        source,
        target,
        weight="length",
    )

    shortest = next(path_generator)
    shortest_distance = route_distance(G, shortest)

    routes = [{
        "name": "Shortest route",
        "path": shortest,
        "distance": shortest_distance,
        "stretch": 1.0,
        "overlap": 1.0,
        "colour": ROUTE_COLOURS[0],
    }]

    for candidate in islice(
        path_generator,
        MAX_CANDIDATES,
    ):

        distance = route_distance(G, candidate)

        if shortest_distance <= 0:
            continue

        stretch = distance / shortest_distance
        overlap = shared_edge_ratio(candidate, shortest)

        if (
            stretch <= MAX_STRETCH
            and overlap < MAX_SHARED
        ):

            index = len(routes)

            routes.append({
                "name": f"Alternative {index}",
                "path": candidate,
                "distance": distance,
                "stretch": stretch,
                "overlap": overlap,
                "colour": ROUTE_COLOURS[index],
            })

        if len(routes) >= 1 + N_ALTERNATIVES:
            break

    return routes


# ============================================================
# 4. SESSION STATE
# ============================================================

defaults = {
    "origin": None,
    "destination": None,
    "last_click": None,
    "routes": None,
    "route_error": None,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


def reset_selection():

    st.session_state.origin = None
    st.session_state.destination = None
    st.session_state.last_click = None
    st.session_state.routes = None
    st.session_state.route_error = None


# ============================================================
# 5. BUILD INTERACTIVE MAP
# ============================================================

def build_map():

    map_object = folium.Map(
        location=[50.7374, 7.0982],
        zoom_start=13,
        control_scale=True,
        tiles="OpenStreetMap",
    )

    if st.session_state.origin is not None:

        folium.Marker(
            st.session_state.origin,
            tooltip="Origin",
            popup="Origin",
            icon=folium.Icon(
                color="green",
                icon="play",
            ),
        ).add_to(map_object)

    if st.session_state.destination is not None:

        folium.Marker(
            st.session_state.destination,
            tooltip="Destination",
            popup="Destination",
            icon=folium.Icon(
                color="darkred",
                icon="flag",
            ),
        ).add_to(map_object)

    if st.session_state.routes:

        G = load_graph()

        for route in st.session_state.routes:

            coordinates = route_geometry(
                G,
                route["path"],
            )

            folium.PolyLine(
                locations=coordinates,
                color=route["colour"],
                weight=3,
                opacity=1.0,
                tooltip=(
                    f"{route['name']} — "
                    f"{route['distance'] / 1000:.2f} km"
                ),
            ).add_to(map_object)

    return map_object


# ============================================================
# 6. MAP SELECTION
# ============================================================

st.info(
    "Click once to select the origin and again to select "
    "the destination. A third click starts a new selection."
)

map_data = st_folium(
    build_map(),
    height=600,
    key="bonn_route_map",
    returned_objects=["last_clicked"],
)

clicked = map_data.get("last_clicked") if map_data else None

if clicked and "lat" in clicked and "lng" in clicked:

    lat = round(float(clicked["lat"]), 6)
    lon = round(float(clicked["lng"]), 6)

    signature = hashlib.sha1(
        f"{lat},{lon}".encode()
    ).hexdigest()

    if signature != st.session_state.last_click:

        st.session_state.last_click = signature
        st.session_state.routes = None
        st.session_state.route_error = None

        point = (lat, lon)

        if st.session_state.origin is None:

            st.session_state.origin = point

        elif st.session_state.destination is None:

            st.session_state.destination = point

        else:

            st.session_state.origin = point
            st.session_state.destination = None

        st.rerun()


# ============================================================
# 7. SHOW SELECTED LOCATIONS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.write("**Origin**")

    st.write(
        st.session_state.origin
        if st.session_state.origin
        else "Not selected"
    )

with col2:

    st.write("**Destination**")

    st.write(
        st.session_state.destination
        if st.session_state.destination
        else "Not selected"
    )


# ============================================================
# 8. ROUTE CONTROLS
# ============================================================

col_button, col_reset = st.columns([2, 1])

with col_button:

    calculate = st.button(
        "Calculate routes",
        type="primary",
        use_container_width=True,
        disabled=not (
            st.session_state.origin
            and st.session_state.destination
        ),
    )

with col_reset:

    st.button(
        "Reset selection",
        on_click=reset_selection,
        use_container_width=True,
    )


if calculate:

    try:

        G = load_graph()

        with st.spinner("Calculating routes..."):

            st.session_state.routes = calculate_routes(
                G,
                st.session_state.origin,
                st.session_state.destination,
            )

        st.session_state.route_error = None
        st.rerun()

    except Exception as error:

        st.session_state.routes = None
        st.session_state.route_error = str(error)


if st.session_state.route_error:

    st.error(st.session_state.route_error)


# ============================================================
# 9. ROUTE COMPARISON
# ============================================================

if st.session_state.routes:

    routes = st.session_state.routes

    st.subheader("Route comparison")

    columns = st.columns(len(routes))

    for column, route in zip(columns, routes):

        with column:

            detour = (
                None
                if route["name"] == "Shortest route"
                else f"{(route['stretch'] - 1) * 100:.1f}% longer"
            )

            st.metric(
                route["name"],
                f"{route['distance'] / 1000:.2f} km",
                delta=detour,
            )

            if route["name"] != "Shortest route":

                st.caption(
                    "Shared road edges: "
                    f"{route['overlap'] * 100:.1f}%"
                )

    st.caption(
        "Alternative routes are limited to a maximum 35% detour "
        "and less than 85% overlap with the shortest route. "
        "Some journeys may have fewer than two qualifying alternatives."
    )


# ============================================================
# 10. ATTRIBUTION AND LIMITATIONS
# ============================================================

st.divider()

st.caption(
    "Map data © OpenStreetMap contributors. "
    "This demonstration optimizes distance, not travel time, "
    "live traffic, road closures, or accessibility."
)
