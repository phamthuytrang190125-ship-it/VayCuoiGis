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

// 2. HÀM CHUYỂN ĐỔI TAB (CỬA HÀNG / VÁY CƯỚI)
function openTab(evt, tabId) {
    // Ẩn tất cả nội dung tab
    var tabContents = document.querySelectorAll('.tab-content');
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    // Xóa màu đỏ của các nút tab
    var tabBtns = document.querySelectorAll('.tab-btn');
    for (var j = 0; j < tabBtns.length; j++) {
        tabBtns[j].classList.remove('active');
    }
    
    // Hiện tab được chọn lên
    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// 3. KHỞI TẠO BẢN ĐỒ VÀ CÁC BIẾN TOÀN CỤC
var currentDestLat = null;
var currentDestLon = null;
var currentProfile = 'car'; 

var map = L.map('map').setView([userLat, userLon], 14);

// Nền bản đồ (Base Map)
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap & CARTO'
}).addTo(map);

// Tạo icon màu đỏ cho vị trí người dùng
var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});

// Nếu đã định vị thì cắm cờ đỏ lên bản đồ
if (!isDefault) {
    var userMarker = L.marker([userLat, userLon], {icon: redIcon}).addTo(map);
    userMarker.bindPopup("<b>Vị trí của bạn 💃</b>").openPopup();
}

// 4. HIỂN THỊ CÁC CỬA HÀNG LÊN BẢN ĐỒ
var markersLayer = new L.LayerGroup();
map.addLayer(markersLayer);

// Dùng vòng lặp for truyền thống rải từng cửa hàng
for (var k = 0; k < stores.length; k++) {
    var store = stores[k];
    var m = L.marker([store.lat, store.lon], {title: store.name});
    
    // Xử lý hiển thị Khoảng cách và Phí ship nếu đã định vị
    var distanceText = "";
    var shippingFeeText = "";
    
    if (!isDefault) {
        distanceText = "<p style='color: #d88a9a; font-weight: bold; margin-bottom: 5px; font-size: 14px;'>Cách bạn: " + store.distance + " km</p>";
        shippingFeeText = "<p style='color: #e67e22; font-weight: bold; font-size: 14px; margin-top: 0; margin-bottom: 15px;'>🛵 Phí ship: " + store.formatted_fee + "</p>";
    }

    // Nối chuỗi HTML để tạo Popup (Code kiểu sinh viên hay dùng)
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
                shippingFeeText + 
                "<button class='btn-route-pop' style='width: 100%; padding: 8px; font-weight: bold;' onclick='showRouteTo(" + store.lat + ", " + store.lon + ", \"car\")'>🚗 Chỉ đường tới đây</button>" +
            "</div>" +
        "</div>";

    m.bindPopup(popupHTML, { minWidth: 240, className: 'custom-popup' });
    markersLayer.addLayer(m);
}

// 5. THANH TÌM KIẾM CỬA HÀNG
var searchControl = new L.Control.Search({
    layer: markersLayer,         
    propertyName: 'title',       
    initial: false,              
    zoom: 16,                    
    marker: false,               
    textPlaceholder: '🔍 Nhập tên tiệm váy...', 
    position: 'topleft'          
});

searchControl.on('search:locationfound', function(e) {
    e.layer.openPopup();
});
map.addControl(searchControl);

// 6. CHỨC NĂNG CHỈ ĐƯỜNG (ROUTING)
var routingControl = null;

function showRouteTo(destLat, destLon, profile) {
    // Nếu quên truyền phương tiện thì mặc định là xe hơi
    if (profile === undefined) {
        profile = 'car';
    }

    if (isDefault) {
        alert("Vui lòng bấm 'Định Vị' hoặc 'Tìm Shop Gần Đây' để xác định vị trí của bạn trước khi xem chỉ đường nhé!");
        return;
    }

    currentDestLat = parseFloat(destLat);
    currentDestLon = parseFloat(destLon);
    currentProfile = profile;

    // Xóa đường vẽ cũ đi (nếu có)
    if (routingControl !== null) {
        map.removeControl(routingControl);
        routingControl = null;
    }

    // Hiện thanh chọn phương tiện
    document.getElementById('vehicle-selector').style.display = 'flex';
    var vehicleBtns = document.querySelectorAll('.btn-vehicle');
    for (var v = 0; v < vehicleBtns.length; v++) {
        vehicleBtns[v].classList.remove('active-vehicle');
    }
    document.getElementById('btn-' + profile).classList.add('active-vehicle');

    // Chọn máy chủ chỉ đường tương ứng
    var serverUrl = 'https://routing.openstreetmap.de/routed-car/route/v1';
    if (profile === 'bike') {
        serverUrl = 'https://routing.openstreetmap.de/routed-bike/route/v1';
    } else if (profile === 'foot') {
        serverUrl = 'https://routing.openstreetmap.de/routed-foot/route/v1';
    }

    // Vẽ đường đi mới
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

// Hàm đổi phương tiện khi bấm nút Ô tô / Xe máy / Đi bộ
function changeVehicle(profile) {
    if (currentDestLat !== null && currentDestLon !== null) {
        showRouteTo(currentDestLat, currentDestLon, profile);
    }
}

// 7. XỬ LÝ SỰ KIỆN BẤM TỪ BÊN NGOÀI
function focusAndRoute(lat, lon) {
    map.flyTo([lat, lon], 16);
    showRouteTo(lat, lon, 'car'); 
}

// Hàm lấy GPS tự động của người dùng
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

// Xử lý khi người dùng bấm "Xem bản đồ" từ trang khác chuyển tới
var urlParams = new URLSearchParams(window.location.search);
var focusId = urlParams.get('focus_store');

if (focusId) {
    var targetStore = null;
    // Tìm cửa hàng theo ID (kiểu sinh viên)
    for (var s = 0; s < stores.length; s++) {
        if (stores[s].id == focusId) {
            targetStore = stores[s];
            break;
        }
    }

    if (targetStore !== null) {
        map.flyTo([targetStore.lat, targetStore.lon], 16, { animate: true, duration: 1.5 });
        
        setTimeout(function() {
            L.popup()
                .setLatLng([targetStore.lat, targetStore.lon])
                .setContent("<div style='text-align:center; color: #d88a9a;'><h3 style='margin:0'>" + targetStore.name + "</h3></div>")
                .openOn(map);
        }, 1000);
        
        if (!isDefault) {
            setTimeout(function() {
                showRouteTo(targetStore.lat, targetStore.lon, 'car');
            }, 1500);
        }
    }
}