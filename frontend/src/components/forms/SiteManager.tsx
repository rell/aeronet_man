import React, {
  useEffect,
  useState,
  useRef,
  useCallback,
  ReactElement,
} from "react";
import { useMapContext } from "../MapContext";
import L from "leaflet";
import * as d3 from "d3";
import "leaflet-svg-shape-markers";
import API_BASE_URL from "../../config";
import { getCookie } from "../utils/csrf";

export interface SiteSelect {
  name: string;
}

export interface Marker {
  site: string;
  filename: string;
  date: Date;
  time: Date;
  latlng: {
    lat: number;
    lng: number;
  };
  aeronet_number: number;
  value: number;
}

interface SiteManagerProps {
  startDate: string;
  endDate: string;
  minLat?: number;
  minLng?: number;
  maxLat?: number;
  maxLng?: number;
  type: string;
  traceActive: boolean;
  selectedSites?: Set<string>;
  zoom: number;
  sitesSelected: boolean;
  refreshMarkers: boolean;
  refreshMarkerSize: boolean;
  typeChanged: boolean;
  markerSize: number;
  children: ReactElement<SiteManagerChildProps>;
  setTraceActive: (active: boolean) => void;
}

interface SiteManagerChildProps {
  sites: SiteSelect[];
  selectedSites: Set<string>;
  selectSite: (siteName: string) => void;
  selectAllSites: () => void;
  deselectAllSites: () => void;
  setSites: (sites: SiteSelect[]) => void;
}

const SiteManager: React.FC<SiteManagerProps> = ({
  startDate,
  endDate,
  minLat,
  minLng,
  maxLat,
  maxLng,
  type,
  zoom,
  traceActive,
  setTraceActive,
  markerSize,
  refreshMarkerSize,
  refreshMarkers,
  selectedSites,
  sitesSelected,
  typeChanged,
  children,
}) => {
  const { map } = useMapContext();
  const [markerData, setMarkerData] = useState<Marker[]>([]);
  const [refresh, setRefreshState] = useState<boolean>(false);
  const [previousMarkerData, setPreviousMarkerData] = useState<Marker[]>([]);
  const [sites, setSites] = useState<SiteSelect[]>([]);
  const [value, setValue] = useState<string>(type);
  const [colors, setColors] = useState<string[]>([]);
  const [colorDomain, setColorDomain] = useState<number[]>([]);
  const [maxValue, setMaxValue] = useState<number>();
  const prevZoom = usePrevious(zoom);
  const prevSitesSelected = usePrevious(selectedSites);
  const prevStartDate = usePrevious(startDate);
  const prevEndDate = usePrevious(endDate);
  const previousMinLat = usePrevious(minLat);
  const previousMaxLat = usePrevious(maxLat);
  const previousMinLng = usePrevious(minLng);
  const previousMaxLng = usePrevious(maxLng);
  const prevType = usePrevious(type);

  function usePrevious<T>(value: T): T | undefined {
    const ref = useRef<T>();
    useEffect(() => {
      ref.current = value;
    }, [value]);
    return ref.current;
  }

  useEffect(() => {
    setTimeout(() => {
      setDomain(type);
    }, 300);
  }, []);

  useEffect(() => {
    if (zoom) {
      updateMarkerSize(markerSize);
    }
  }, [zoom, map]);

  useEffect(() => {
    setTimeout(() => {
      setDomain(type);
    }, 300);
  }, [type]);

  useEffect(() => {
    if (refreshMarkers) {
      setDomain(type);
      fetchMarkers();
    }
  }, [refreshMarkers]);

  useEffect(() => {
    let refresh = false;
    if (prevStartDate !== startDate || prevEndDate !== endDate) {
      refresh = true;
    } else if (
      previousMaxLng !== maxLng ||
      previousMaxLat !== maxLat ||
      previousMinLng !== minLng ||
      previousMinLat !== minLat
    ) {
      refresh = true;
    }
    if (refresh) {
      fetchSites();
    }
  }, [startDate, endDate, prevStartDate, prevEndDate, maxLng, previousMaxLng]);

  const isDataDifferent = (prevData: Marker[], newData: Marker[]) => {
    return JSON.stringify(prevData) !== JSON.stringify(newData);
  };

  const setDomain = async (dataType: string) => {
    const color = [
      "blue",
      "teal",
      "green",
      "chartreuse",
      "yellow",
      "orange",
      "red",
    ];
    let domain: number[];

    if (dataType.includes("std") || dataType.includes("aod")) {
      domain = Array.from({ length: 6 }, (_, i) =>
        parseFloat((i * 0.1).toFixed(1)),
      );
    } else if (dataType.includes("water") || dataType.includes("air_mass")) {
      domain = Array.from({ length: 6 }, (_, i) => i);
    } else if (dataType.includes("angstrom")) {
      domain = Array.from({ length: 6 }, (_, i) =>
        parseFloat((i * (2 / 5)).toFixed(1)),
      );
    } else {
      domain = Array.from({ length: 6 }, (_, i) =>
        parseFloat((i / 6).toFixed(1)),
      );
    }

    setColors(color);
    setColorDomain(domain);
    setMaxValue(domain[domain.length - 1]);
  };

  const clearMarkers = () => {
    if (map) {
      map.eachLayer((layer: L.Layer) => {
        if (
          layer instanceof L.CircleMarker ||
          layer instanceof L.FeatureGroup
        ) {
          map.removeLayer(layer);
        }
      });
    }
  };

  const setColor = (value: number) => {
    if (colors.length && colorDomain.length && maxValue !== undefined) {
      const colorScale = d3
        .scaleLinear<string>()
        .domain(colorDomain)
        .range(colors);
      if (value <= maxValue && value > 0) {
        return colorScale(value); // sets weight of color based on scale
      } else if (value > maxValue) {
        return d3.color("darkred");
      } else {
        return d3.color("grey");
      }
    }
    return d3.color("grey");
  };

  const fetchMarkers = async () => {
    try {
      const params = {
        start_date: startDate,
        end_date: endDate,
        sites: selectedSites
          ? Array.from(selectedSites).map((site) => site)
          : [],
        min_lat: minLat !== undefined ? minLat.toString() : null,
        min_lng: minLng !== undefined ? minLng.toString() : null,
        max_lat: maxLat !== undefined ? maxLat.toString() : null,
        max_lng: maxLng !== undefined ? maxLng.toString() : null,
        reading: type,
      };

      const filteredParams = Object.fromEntries(
        Object.entries(params).filter(([_, v]) => v != null),
      );
      const csrfToken = getCookie("X-CSRFToken");
      const response = await fetch(
        `${API_BASE_URL}/maritimeapp/measurements/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(filteredParams),
          credentials: "include",
        },
      );

      if (!response.ok) {
        clearMarkers();
        throw new Error("Network response was not ok");
      }

      const data: Marker[] = await response.json();

      clearMarkers();

      const siteGroups: { [key: string]: L.FeatureGroup } = {};
      const sitePolylineGroups: { [key: string]: L.FeatureGroup } = {}; // To store polyline groups
      let lastClickTime: number | null = null;
      let lastClickedSite: string | null = null;

      data.forEach((markerData) => {
        const { latlng, value, date, site } = markerData;

        if (!siteGroups[site]) {
          siteGroups[site] = L.featureGroup().addTo(map);
          sitePolylineGroups[site] = L.featureGroup(); // Create a polyline group for the site
        }

        const markerColor = setColor(value);
        const fillOpacity =
          markerColor && markerColor === d3.color("grey") ? 0.6 : 0.9;
        const cruiseMarker = L.circleMarker([latlng.lat, latlng.lng], {
          color: markerColor,
          radius: markerSize,
          fillOpacity: fillOpacity,
          stroke: false,
          setFillOpacity: fillOpacity,
          interactive: true,
          value: value,
          site: site,
          date: date,
          originalColor: markerColor,
          previousSize: markerSize,
        }).addTo(siteGroups[site]);

        cruiseMarker.on("click", () => {
          const currentTime = Date.now();
          if (
            lastClickTime &&
            lastClickedSite === site &&
            currentTime - lastClickTime < 1000 // Time window to double click to reset site view
          ) {
            // Handle double-click
            clearMap();
            resetMarkerOpacity();
            lastClickTime = null;
            lastClickedSite = null;
          } else {
            // Handle single click
            updateMarkerOpacity(site);
            drawPolyline(site, data);
            lastClickTime = currentTime;
            lastClickedSite = site;
          }
        });

        cruiseMarker.on("mouseover", () => {
          cruiseMarker
            .bindPopup(
              `<b>Cruise:</b> ${cruiseMarker.options.site}<br>
                             <b>${type.toUpperCase().replace(/_/g, " ")}</b> ${cruiseMarker.options.value.toFixed(4)}<br>
                             <b>Date:</b> ${cruiseMarker.options.date}`,
            )
            .openPopup();
        });

        cruiseMarker.on("mouseout", () => {
          cruiseMarker.closePopup();
        });
      });
    } catch (error) {
      console.error("Error fetching markers:", error);
    }
  };

  const toggleTraceActive = (active: boolean) => {
    setTraceActive(active);
  };

  const updateMarkerSize = (size: number) => {
    if (map) {
      map.eachLayer((layer: L.Layer) => {
        if (layer instanceof L.CircleMarker) {
          layer.setStyle({
            radius: size,
          });
        }
      });
    }
  };

  const updateMarkerOpacity = (site: string) => {
    map.eachLayer((layer: L.Layer) => {
      if (layer.options.site !== undefined) {
        if (layer.options.site === site) {
          layer.setStyle({
            shape: "square",
            fillOpacity: 1,
            color: layer.options.originalColor,
            weight: 2,
            opacity: 1,
            interactive: true,
          });

          layer.on("mouseover", () => {
            layer
              .bindPopup(
                `<b>Cruise:</b> ${layer.options.site}<br>
                            <b>${type.toUpperCase().replace(/_/g, " ")}:</b> ${layer.options.value.toFixed(3)}<br>
                            <b>Date:</b> ${layer.options.date}`,
              )
              .openPopup();
          });

          layer.on("mouseout", () => {
            layer.closePopup();
          });
        } else {
          layer.setStyle({
            fillOpacity: 0.0,
            color: "grey",
            weight: 2,
            opacity: 0,
            interactive: false,
          });
          layer.off("mouseover");
          layer.off("mouseout");
        }
      }
    });
  };
  const drawPolyline = (site: string, markers: Marker[]) => {
    // Remove previous polyline if exists

    const sitePolylineGroups: { [key: string]: L.FeatureGroup } = {}; // To store polyline groups
    clearMap();
    setTraceActive(true);
    const oldPolylineGroup = sitePolylineGroups[site];
    if (oldPolylineGroup) {
      oldPolylineGroup.eachLayer((layer: L.Layer) => {
        if (layer instanceof L.Polyline) {
          oldPolylineGroup.removeLayer(layer);
        }
      });
      map.removeLayer(oldPolylineGroup);
      delete sitePolylineGroups[site]; // makes sure reference is also deleted
    }

    const siteMarkers = markers
      .filter((marker) => marker.site === site)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

    const latlngs = siteMarkers.map((marker) => [
      marker.latlng.lat,
      marker.latlng.lng,
    ]);

    // Define color scale
    const colorScale = d3
      .scaleLinear<string>()
      .domain([0, 1])
      .range(["rgb(255, 0, 0)", "rgb(0, 255, 0)"]);

    // Create a new polyline group
    const polylineGroup = L.featureGroup().addTo(map);

    // Draw polyline segments with color gradient
    latlngs.forEach((latlng, index) => {
      const nextLatLng = latlngs[index + 1];
      if (nextLatLng) {
        const fraction = index / latlngs.length;
        const color = colorScale(fraction);
        L.polyline([latlng, nextLatLng], {
          weight: 3,
          color: color,
          opacity: 1,
          interactive: false,
        }).addTo(polylineGroup);
      }
    });

    // Store the new polyline group
    sitePolylineGroups[site] = polylineGroup;
  };

  const resetMarkerOpacity = () => {
    //console.log("reset" + markerSize);
    map.eachLayer((layer: L.Layer) => {
      if (layer instanceof L.CircleMarker) {
        layer.setStyle({
          color: layer.options.originalColor,
          fillOpacity: layer.options.setFillOpacity,
          weight: 2,
          interactive: true,
        });

        layer.on("mouseover", () => {
          layer
            .bindPopup(
              `<b>Cruise:</b> ${layer.options.site}<br>
                        <b>${type.toUpperCase().replace(/_/g, " ")}:</b> ${layer.options.value.toFixed(3)}<br>
                        <b>Date:</b> ${layer.options.date}`,
            )
            .openPopup();
        });

        layer.on("mouseout", () => {
          layer.closePopup();
        });
      }
    });
  };

  const fetchSites = async () => {
    try {
      const params = new URLSearchParams();
      // Append the necessary parameters
      if (startDate) params.append("start_date", startDate);
      if (endDate) params.append("end_date", endDate);
      if (
        minLat !== undefined &&
        minLng !== undefined &&
        maxLat !== undefined &&
        maxLng !== undefined
      ) {
        params.append("min_lat", minLat.toString());
        params.append("min_lng", minLng.toString());
        params.append("max_lat", maxLat.toString());
        params.append("max_lng", maxLng.toString());
      }

      const response = await fetch(
        `${API_BASE_URL}/maritimeapp/measurements/sites/?${params.toString()}`,
      );
      console.log(
        `${API_BASE_URL}/maritimeapp/measurements/sites/?${params.toString()}`,
      );
      const data: SiteSelect[] = await response.json();
      setSites(data);
    } catch (error) {
      console.error("Error fetching sites:", error);
    }
  };

  const clearMap = () => {
    toggleTraceActive(false);
    for (const i in map._layers) {
      if (
        map._layers[i] instanceof L.Polyline &&
        !(map._layers[i] instanceof L.Rectangle)
      ) {
        try {
          map.removeLayer(map._layers[i]);
        } catch (e) {
          console.log("Problem with " + e + map._layers[i]);
        }
      }
    }
  };

  return React.cloneElement(children, {
    sites,
    selectedSites,
  });
};

export default SiteManager;
