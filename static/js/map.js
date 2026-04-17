// static/js/map.js

// 1. CẤU HÌNH DỊCH THUẬT CHỈ ĐƯỜNG SANG TIẾNG VIỆT
var viFormatter = new L.Routing.Formatter();
viFormatter.formatInstruction = function(instr, i) {
    if (instr.text === undefined) return '';
    var t = instr.text;
    t = t.replace('northwest', 'Tây Bắc').replace('northeast', 'Đông Bắc')
         .replace('southwest', 'Tây Nam').replace('southeast', 'Đông Nam')
         .replace('north', 'Bắc').replace('south', 'Nam')
         .replace('east', 'Đông').replace('west', 'Tây');
    t = t.replace('Head', 'Đi về hướng').replace('Turn right', 'Rẽ phải').replace('Turn left', 'Rẽ trái')
         .replace('Slight right', 'Chếch sang phải').replace('Slight left', 'Chếch sang trái')
         .replace('Sharp right', 'Ngoặt sang phải').replace('Sharp left', 'Ngoặt sang trái')
         .replace('Continue', 'Tiếp tục đi thẳng').replace('Make a U-turn', 'Quay đầu xe');
    t = t.replace('Enter the traffic circle and take the', 'Đi vào vòng xuyến và rẽ ra lối thứ')
         .replace('1st exit', '1').replace('2nd exit', '2')
         .replace('3rd exit', '3').replace('4th exit', '4')
         .replace('5th exit', '5').replace('exit', '');
    t = t.replace('You have arrived at your destination, on the right', '🎉 Bạn đã đến nơi (cửa hàng ở bên phải)')
         .replace('You have arrived at your destination, on the left', '🎉 Bạn đã đến nơi (cửa hàng ở bên trái)')
         .replace('You have arrived at your destination', '🎉 Bạn đã đến nơi');
    t = t.replace(' onto ', ' vào ').replace(' on ', ' trên ');
    return t;
};

// 2. KHỞI TẠO BIẾN TOÀN CỤC
var map, shopGroup, allMarkers = [], userMarker, bufferLayer, drawnItems, routingControl = null;
var currentDestLat = null, currentDestLon = null;

var redIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
});

// 3. HÀM CẬP NHẬT VỊ TRÍ NGƯỜI DÙNG (MANUAL & TÌM KIẾM)
window.updateManualPosition = function(lat, lng) {
    document.getElementById('latInput').value = lat.toFixed(6);
    document.getElementById('lonInput').value = lng.toFixed(6);
    userLat = lat; 
    userLon = lng; 
    isDefault = false;

    if (!userMarker) {
        userMarker = L.marker([lat, lng], {icon: redIcon, zIndexOffset: 1000}).addTo(map);
    } else {
        userMarker.setLatLng([lat, lng]);
    }
    map.flyTo([lat, lng], 15);
    if(window.runGisAnalysis) runGisAnalysis();
};

// 4. HÀM VẼ ĐƯỜNG ĐI (ĐÃ TÍCH HỢP CHỌN XE)
window.focusAndRoute = function(destLat, destLon, profile = 'car') {
    if (isDefault) {
        alert("Vui lòng nhập địa chỉ, Định vị hoặc click trên bản đồ để chọn vị trí xuất phát trước nhé!");
        return;
    }

    currentDestLat = parseFloat(destLat);
    currentDestLon = parseFloat(destLon);

    map.closePopup();
    if (routingControl != null) { map.removeControl(routingControl); }
    document.body.style.cursor = 'wait';

    // Đổi màu nút phương tiện
    document.querySelectorAll('.btn-vehicle').forEach(btn => btn.classList.remove('active-vehicle'));
    var btnProfile = document.getElementById('btn-' + profile);
    if(btnProfile) btnProfile.classList.add('active-vehicle');

    // Chọn Server Routing
    var serverUrl = 'https://routing.openstreetmap.de/routed-car/route/v1';
    if (profile === 'bike') serverUrl = 'https://routing.openstreetmap.de/routed-bike/route/v1';
    else if (profile === 'foot') serverUrl = 'https://routing.openstreetmap.de/routed-foot/route/v1';

    routingControl = L.Routing.control({
        waypoints: [ L.latLng(userLat, userLon), L.latLng(currentDestLat, currentDestLon) ],
        router: L.Routing.osrmv1({ serviceUrl: serverUrl, profile: 'driving' }), 
        formatter: viFormatter,
        lineOptions: { styles: [{color: '#d88a9a', opacity: 0.9, weight: 6}] },
        addWaypoints: false, draggableWaypoints: false, show: true,
        createMarker: function() { return null; }
    })
    .on('routesfound', function(e) {
        document.body.style.cursor = 'default';
        var bounds = L.latLngBounds([userLat, userLon], [currentDestLat, currentDestLon]);
        map.fitBounds(bounds, {padding: [50, 50]});
    })
    .on('routingerror', function(e) {
        document.body.style.cursor = 'default';
        alert("Máy chủ OSM hiện đang quá tải. Vui lòng thử lại sau!");
    }).addTo(map);
};

window.checkAndRoute = function(destLat, destLon) {
    focusAndRoute(destLat, destLon, 'car');
};

window.changeVehicle = function(profile) {
    if (currentDestLat !== null && currentDestLon !== null) {
        focusAndRoute(currentDestLat, currentDestLon, profile);
    } else {
        document.querySelectorAll('.btn-vehicle').forEach(btn => btn.classList.remove('active-vehicle'));
        document.getElementById('btn-' + profile).classList.add('active-vehicle');
    }
};

// 5. KHỞI TẠO BẢN ĐỒ KHI TRANG TẢI XONG
document.addEventListener('DOMContentLoaded', function() {
    map = L.map('map').setView([userLat, userLon], 13);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { attribution: '&copy; OpenStreetMap' }).addTo(map);

    shopGroup = L.layerGroup().addTo(map);
    drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    // ĐỔ DỮ LIỆU CỬA HÀNG VÀ TRẢ LẠI POPUP GỐC CỦA BẠN
    storesData.forEach(function(store) {
        var popupContent = `
            <div style="text-align: center; min-width: 220px; font-family: 'Quicksand', sans-serif;">
                <div style="font-weight: 700; color: #d88a9a; margin-bottom: 5px; font-size: 16px;">${store.name}</div>
                <img src="${store.image}" onerror="this.src='https://via.placeholder.com/150x100?text=Bridal+Luxury'" 
                    style="width: 100%; height: 110px; object-fit: cover; border-radius: 8px; margin: 5px 0;">
                <div style="font-size: 12px; color: #666; line-height: 1.4; text-align: left; margin-bottom: 10px;">
                    📍 <b>Địa chỉ:</b> ${store.address}<br>
                    📞 <b>Hotline:</b> ${store.phone || 'Đang cập nhật'}
                </div>
                <div style="border-top: 1px dashed #eee; padding-top: 10px; margin-bottom: 10px;">
                    <div style="color: #d88a9a; font-weight: 700; font-size: 14px;">Cách bạn: ${store.distance || '--'} km</div>
                    <div style="color: #e67e22; font-weight: 700; font-size: 14px;">
                        <i class="fa-solid fa-motorcycle"></i> Phí ship: ${store.formatted_fee || 'Miễn phí'}
                    </div>
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
    <a href="/stores/${store.id}/" style="flex: 1; background: #333; color: white; padding: 8px 5px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: bold; transition: 0.3s; display: flex; align-items: center; justify-content: center; gap: 5px;" onmouseover="this.style.background='#555'" onmouseout="this.style.background='#333'">
        <i class="fa-solid fa-shirt"></i> Xem Váy
    </a>
    
    <button class="btn-route-popup" onclick="checkAndRoute(${store.lat}, ${store.lon})" style="flex: 1; margin-top: 0; padding: 8px 5px; font-size: 12px; display: flex; align-items: center; justify-content: center; gap: 5px;">
         <i class="fa-solid fa-location-arrow"></i> Chỉ đường
    </button>
</div>
            </div>
        `;
        var marker = L.marker([store.lat, store.lon]).bindPopup(popupContent, {maxWidth: 250});
        marker.storeData = store;
        shopGroup.addLayer(marker);
        allMarkers.push(marker);
    });

    if (!isDefault) updateManualPosition(userLat, userLon);

    // Bắt sự kiện Click trên map
    map.on('click', function(e) { updateManualPosition(e.latlng.lat, e.latlng.lng); });

    // Bắt sự kiện Enter tìm địa chỉ bằng Photon API
    var searchInput = document.getElementById('custom-address-search');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                var query = this.value;
                if (!query) return;
                document.body.style.cursor = 'wait';
                fetch("https://photon.komoot.io/api/?q=" + encodeURIComponent(query + ", Việt Nam") + "&limit=1")
                    .then(res => res.json())
                    .then(data => {
                        document.body.style.cursor = 'default';
                        if (data.features && data.features.length > 0) {
                            updateManualPosition(data.features[0].geometry.coordinates[1], data.features[0].geometry.coordinates[0]);
                        } else {
                            alert("Không tìm ra địa chỉ này. Hãy thử gõ ngắn gọn lại tên đường và quận nhé!");
                        }
                    }).catch(() => { document.body.style.cursor = 'default'; });
            }
        });
    }

    // Công cụ vẽ vùng Leaflet Draw
    var drawControl = new L.Control.Draw({
        position: 'topleft',
        draw: { polygon: true, rectangle: true, circle: false, marker: false, polyline: false, circlemarker: false },
        edit: { featureGroup: drawnItems }
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (e) {
        drawnItems.clearLayers();
        if (bufferLayer) map.removeLayer(bufferLayer);
        drawnItems.addLayer(e.layer);
        var shape = e.layer.toGeoJSON();
        var count = 0;
        shopGroup.clearLayers(); 
        allMarkers.forEach(m => {
            if (turf.booleanPointInPolygon(turf.point([m.storeData.lon, m.storeData.lat]), shape)) { shopGroup.addLayer(m); count++; }
        });
        document.getElementById('gis-analysis').innerHTML = `<i class="fa-solid fa-filter"></i> Đã lọc theo vùng vẽ | Tìm thấy: <b>${count}</b> cửa hàng.`;
    });

    // 6. XỬ LÝ FOCUS TỪ TRANG KHÁC
    var urlParams = new URLSearchParams(window.location.search);
    var focusId = urlParams.get('focus_store');
    if (focusId) {
        var targetStore = storesData.find(s => s.id == focusId);
        if (targetStore) {
            map.flyTo([targetStore.lat, targetStore.lon], 16, { animate: true, duration: 1.5 });
            setTimeout(() => {
                L.popup().setLatLng([targetStore.lat, targetStore.lon])
                         .setContent("<div style='text-align:center; color: #d88a9a;'><h3 style='margin:0'>" + targetStore.name + "</h3></div>")
                         .openOn(map);
            }, 1000);
            if (!isDefault) setTimeout(() => { checkAndRoute(targetStore.lat, targetStore.lon); }, 1500);
        }
    }
});

// 7. CÁC HÀM TIỆN ÍCH KHÁC
window.runGisAnalysis = function() {
    var radius = parseFloat(document.getElementById('radiusInput').value) || 5;
    if (drawnItems) drawnItems.clearLayers(); 
    var buffered = turf.buffer(turf.point([userLon, userLat]), radius, {units: 'kilometers'});
    if (bufferLayer) map.removeLayer(bufferLayer);
    bufferLayer = L.geoJSON(buffered, {style: { color: '#d88a9a', weight: 2, fillColor: '#ffc1cc', fillOpacity: 0.25 }}).addTo(map);
    var count = 0;
    shopGroup.clearLayers(); 
    allMarkers.forEach(m => {
        if (turf.booleanPointInPolygon(turf.point([m.storeData.lon, m.storeData.lat]), buffered)) { shopGroup.addLayer(m); count++; }
    });
    document.getElementById('gis-analysis').innerHTML = `<i class="fa-solid fa-location-dot"></i> Bán kính: ${radius}km | Tìm thấy: <b>${count}</b> cửa hàng.`;
};

window.forceGetLocation = function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => { updateManualPosition(pos.coords.latitude, pos.coords.longitude); }, 
        () => { alert("Không thể truy cập GPS. Hãy tự chọn vị trí trên bản đồ!"); });
    }
}

window.openTab = function(evt, tabName) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}