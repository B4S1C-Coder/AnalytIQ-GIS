"use client";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { MapPin, Layers } from "lucide-react";
import L from "leaflet";
import { useEffect, useRef, useState } from "react";

const mumbaiCenter: [number, number] = [19.076, 72.8777];

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

export function MapPanel({
  location,
  floodZones,
  onMarkerClick,
}: {
  location?: { lat: number; lng: number; label?: string };
  floodZones?: any;
  onMarkerClick?: () => void;
}) {
  const [isClient, setIsClient] = useState(false);
  const mapRef = useRef<any>(null);
  
  useEffect(() => {
    // Ensure we're on the client side and DOM is ready
    if (typeof window !== 'undefined') {
      setIsClient(true);
    }
  }, []);

  useEffect(() => {
    if (location && mapRef.current && isClient) {
      mapRef.current.flyTo([location.lat, location.lng], 14, { duration: 1.2 });
    }
  }, [location, isClient]);

  if (!isClient) {
    return (
      <div className="relative h-full w-full bg-zinc-900 rounded-lg flex items-center justify-center">
        <div className="text-zinc-400">Loading map...</div>
      </div>
    );
  }

  return (
    <div className="relative h-full w-full">
      <MapContainer
        center={mumbaiCenter}
        zoom={12}
        scrollWheelZoom={true}
        className="h-full w-full rounded-lg z-0"
        ref={mapRef}
        style={{ background: "#2a2a2a" }}
        zoomControl={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/attributions'>CARTO</a>"
        />
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png"
          attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/attributions'>CARTO</a>"
        />
        {location && (
          <Marker position={[location.lat, location.lng]} icon={markerIcon} eventHandlers={{ click: onMarkerClick }}>
            <Popup>
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-[#d32f2f]" />
                <span>{location.label || "User Location"}</span>
              </div>
            </Popup>
          </Marker>
        )}
        {floodZones && <GeoJSON data={floodZones} style={{ color: "#ff6b6b", fillOpacity: 0.3, weight: 2 }} />}
      </MapContainer>
              <div className="absolute bottom-4 left-4 bg-zinc-800/95 text-zinc-100 rounded-lg px-3 py-2 text-xs shadow-lg border border-zinc-700">
          <div className="font-bold mb-1 text-zinc-200">Legend</div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-[#ff6b6b]" /> Flood Zone
          </div>
        </div>
                <div className="absolute top-4 right-4 bg-zinc-800/95 text-zinc-100 rounded-lg p-2 shadow-lg border border-zinc-700">
          <div className="flex flex-col gap-1">
            <button className="w-8 h-8 bg-zinc-700 hover:bg-zinc-600 rounded flex items-center justify-center text-zinc-200 hover:text-white transition-colors">
              +
            </button>
            <button className="w-8 h-8 bg-zinc-700 hover:bg-zinc-600 rounded flex items-center justify-center text-zinc-200 hover:text-white transition-colors">
              −
            </button>
          </div>
        </div>
        <div className="absolute top-4 left-4 bg-zinc-800/95 text-zinc-100 rounded-lg p-2 shadow-lg border border-zinc-700">
          <button className="w-8 h-8 bg-zinc-700 hover:bg-zinc-600 rounded flex items-center justify-center text-zinc-200 hover:text-white transition-colors">
            <Layers className="w-4 h-4" />
          </button>
        </div>
    </div>
  );
} 