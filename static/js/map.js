// static/js/map.js

// BỘ LỌC DỊCH THUẬT TIẾNG VIỆT
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

function openTab(evt, tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// Biến điều khiển logic
var currentDestLat = null;
var currentDestLon = null;
var currentProfile = 'car'; 

// Khởi tạo bản đồ
var map = L.map('map').setView([userLat, userLon], 14);

L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap & CARTO'
}).addTo(map);

var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});

// Chỉ hiện Marker người dùng nếu đã định vị
if (!isDefault) {
    var userMarker = L.marker([userLat, userLon], {icon: redIcon}).addTo(map)
        .bindPopup("<b>Vị trí của bạn 💃</b>").openPopup();
}

// TẠO MỘT NHÓM CHỨA CÁC ĐIỂM CỬA HÀNG ĐỂ THANH TÌM KIẾM ĐỌC
var markersLayer = new L.LayerGroup();
map.addLayer(markersLayer);

// VÒNG LẶP RẢI CỬA HÀNG
stores.forEach(function(store) {
    // QUAN TRỌNG: Phải thêm {title: store.name} để kính lúp biết đường mà tìm
    var m = L.marker([store.lat, store.lon], {title: store.name});
    
    var distanceText = "";
    if (!isDefault) {
        distanceText = "<span style='color: var(--primary-color); font-weight: bold; display: block; margin-bottom: 8px; font-size: 14px;'>Cách bạn: " + store.distance + " km</span>";
    }

    var popupHTML = 
        "<div class='popup-header'><b>" + store.name + "</b></div>" +
        "<div class='popup-body' style='text-align: left; padding: 12px; background: white; border-radius: 0 0 10px 10px;'>" +
            "<img src='" + store.image + "' onerror='this.onerror=null; this.src=\"https://dummyimage.com/400x150/fff0f3/d88a9a&text=Bridal+Luxury\";' style='width: 100%; height: 130px; object-fit: cover; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>" +                    
            "<div style='font-size: 12.5px; color: #555; margin-bottom: 6px; line-height: 1.4;'>" +
                "<b>📍 Địa chỉ:</b> " + store.address +
            "</div>" +
            "<div style='font-size: 12.5px; color: #555; margin-bottom: 12px;'>" +
                "<b>📞 Hotline:</b> " + store.phone +
            "</div>" +
            "<div style='text-align: center; border-top: 1px dashed #eee; padding-top: 10px;'>" +
                distanceText +
                "<button class='btn-route-pop' style='width: 100%; padding: 8px; font-weight: bold;' onclick='showRouteTo(" + store.lat + ", " + store.lon + ", \"car\")'>🚗 Chỉ đường tới đây</button>" +
            "</div>" +
        "</div>";

    m.bindPopup(popupHTML, { minWidth: 240, className: 'custom-popup' });
    
    // Đưa marker vào nhóm thay vì đưa thẳng lên bản đồ
    markersLayer.addLayer(m);
});

// ==========================================
// THÊM THANH TÌM KIẾM (KÍNH LÚP) LÊN BẢN ĐỒ
// ==========================================
var searchControl = new L.Control.Search({
    layer: markersLayer,         // Chỉ tìm trong nhóm cửa hàng của mình
    propertyName: 'title',       // Tìm theo tên cửa hàng
    initial: false,              // Tìm kiếm theo từ khóa chứa bên trong (gõ 'H' ra 'Helen')
    zoom: 16,                    // Zoom sát vào cửa hàng khi tìm thấy
    marker: false,               // Không vẽ thêm icon rác
    textPlaceholder: '🔍 Nhập tên tiệm váy...', // Chữ hiển thị
    position: 'topleft'          // Nằm góc trên bên trái y hệt ý thầy
});

// Sự kiện: Khi tìm thấy tiệm, tự động bung cái Popup thông tin ra luôn!
searchControl.on('search:locationfound', function(e) {
    e.layer.openPopup();
});

map.addControl(searchControl);

var routingControl = null;

function showRouteTo(destLat, destLon, profile = 'car') {
    if (isDefault) {
        alert("Vui lòng bấm 'Định Vị' hoặc 'Tìm Shop Gần Đây' để xác định vị trí của bạn trước khi xem chỉ đường nhé!");
        return;
    }

    currentDestLat = parseFloat(destLat);
    currentDestLon = parseFloat(destLon);
    currentProfile = profile;

    if (routingControl !== null) {
        map.removeControl(routingControl);
        routingControl = null;
    }

    document.getElementById('vehicle-selector').style.display = 'flex';
    document.querySelectorAll('.btn-vehicle').forEach(btn => btn.classList.remove('active-vehicle'));
    document.getElementById('btn-' + profile).classList.add('active-vehicle');

    var serverUrl = 'https://routing.openstreetmap.de/routed-car/route/v1';
    if (profile === 'bike') {
        serverUrl = 'https://routing.openstreetmap.de/routed-bike/route/v1';
    } else if (profile === 'foot') {
        serverUrl = 'https://routing.openstreetmap.de/routed-foot/route/v1';
    }

    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(userLat, userLon),
            L.latLng(currentDestLat, currentDestLon)
        ],
        formatter: viFormatter,
        createMarker: function() { return null; },
        lineOptions: { styles: [{color: '#d88a9a', opacity: 0.9, weight: 6}] },
        router: L.Routing.osrmv1({
            serviceUrl: serverUrl,
            profile: 'driving'
        }),
        show: true 
    }).addTo(map);

    routingControl.on('routingerror', function(e) {
        console.error("Lỗi: ", e);
        alert("Máy chủ OSM hiện đang quá tải. Vui lòng thử lại sau!");
    });
}

function changeVehicle(profile) {
    if (currentDestLat !== null && currentDestLon !== null) {
        showRouteTo(currentDestLat, currentDestLon, profile);
    }
}

function focusAndRoute(lat, lon) {
    map.flyTo([lat, lon], 16);
    showRouteTo(lat, lon, 'car'); 
}

function forceGetLocation() {
    if (!navigator.geolocation) {
        alert("Trình duyệt không hỗ trợ GPS.");
        return;
    }
    navigator.geolocation.getCurrentPosition(function(pos) {
        document.getElementById('latInput').value = pos.coords.latitude;
        document.getElementById('lonInput').value = pos.coords.longitude;
        document.getElementById('locationForm').submit();
    }, function(error) {
        alert("Vui lòng cấp quyền vị trí cho trình duyệt web để tìm cửa hàng gần bạn nhất.");
    });
}

const urlParams = new URLSearchParams(window.location.search);
const focusId = urlParams.get('focus_store');

if (focusId) {
    const targetStore = stores.find(s => s.id == focusId);
    if (targetStore) {
        map.flyTo([targetStore.lat, targetStore.lon], 16, { animate: true, duration: 1.5 });
        setTimeout(() => {
            L.popup()
                .setLatLng([targetStore.lat, targetStore.lon])
                .setContent(`
                    <div style='text-align:center; color: #d88a9a;'>
                        <h3 style='margin:0'>${targetStore.name}</h3>
                    </div>
                `)
                .openOn(map);
        }, 1000);
        
        if (!isDefault) {
            setTimeout(() => {
                showRouteTo(targetStore.lat, targetStore.lon, 'car');
            }, 1500);
        }
    }
}