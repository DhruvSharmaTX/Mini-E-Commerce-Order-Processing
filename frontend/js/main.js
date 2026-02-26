const content = document.getElementById("content");

function render(html) {
    content.innerHTML = html;
}

function loadHome() {
    render(`
        <h2>Home</h2>
        <button onclick="loadUsersMenu()">Users</button>
        <button onclick="loadProductsMenu()">Products</button>
        <button onclick="loadOrdersMenu()">Orders</button>
    `);
}

loadHome();