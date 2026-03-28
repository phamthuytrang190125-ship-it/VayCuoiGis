// static/js/manager.js

function openMgrTab(evt, tabName) {
    var i, x, tablinks;
    
    // Ẩn tất cả các nội dung tab
    x = document.getElementsByClassName("mgr-content");
    for (i = 0; i < x.length; i++) { 
        x[i].style.display = "none"; 
    }
    
    // Xóa class 'active' khỏi tất cả các nút tab
    tablinks = document.getElementsByClassName("mgr-tab");
    for (i = 0; i < x.length; i++) { 
        tablinks[i].className = tablinks[i].className.replace(" active", ""); 
    }
    
    // Hiện tab được chọn và thêm class 'active' cho nút đó
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Tính năng Tìm kiếm nhanh Live Search (Xịn hơn Django Admin)
function filterProducts() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchProduct");
    filter = input.value.toUpperCase(); // Chuyển chữ thường thành in hoa để tìm không phân biệt HOA/thường
    table = document.getElementById("productTable");
    tr = table.getElementsByClassName("product-row");

    // Quét qua từng hàng trong bảng
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByClassName("product-name")[0]; // Cột Tên váy cưới nằm ở đây
        if (td) {
            txtValue = td.textContent || td.innerText;
            // Nếu chữ bạn gõ khớp với tên váy thì hiện ra, không thì giấu đi
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Tính năng Tìm kiếm nhanh Cửa hàng
function filterStores() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchStore");
    filter = input.value.toUpperCase();
    table = document.getElementById("storeTable");
    tr = table.getElementsByClassName("store-row");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByClassName("store-name")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}