function loadOrdersMenu() {
    render(`
        <h2>Orders</h2>
        <button onclick="getAllOrders()">Get All Orders</button>
        <button onclick="showCreateOrder()">Create Order</button>
        <button onclick="showGetOrder()">Get Order</button>
        <button onclick="showCancelOrder()">Cancel Order</button>
        <br><br>
        <button onclick="loadHome()">Back</button>
    `);
}

async function getAllOrders() {
    const orders = await apiRequest("/orders/");

    let html = `
        <h2>All Orders</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Total</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;

    orders.forEach(order => {
        html += `
            <tr>
                <td>${order.id}</td>
                <td>${order.user_id}</td>
                <td>$${order.total_amount}</td>
                <td>${order.status}</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
        <br>
        <button onclick="loadOrdersMenu()">Back</button>
    `;

    render(html);
}

function showCreateOrder() {
    render(`
        <h2>Create Order</h2>
        <input id="userId" placeholder="User ID"><br>
        <input id="productId" placeholder="Product ID"><br>
        <input id="quantity" type="number" placeholder="Quantity"><br>
        <button onclick="createOrder()">Submit</button>
        <br><br>
        <button onclick="loadOrdersMenu()">Back</button>
    `);
}

async function createOrder() {
    await apiRequest("/orders/", "POST", {
        user_id: document.getElementById("userId").value,
        product_id: document.getElementById("productId").value,
        quantity: parseInt(document.getElementById("quantity").value)
    });
    alert("Order Created");
    loadOrdersMenu();
}

function showGetOrder() {
    render(`
        <h2>Get Order</h2>
        <input id="orderId" placeholder="Order ID">
        <button onclick="getOrder()">Search</button>
        <br><br>
        <button onclick="loadOrdersMenu()">Back</button>
    `);
}

async function getOrder() {
    const id = document.getElementById("orderId").value;
    const order = await apiRequest(`/orders/${id}`);

    render(`
        <h2>Order Details</h2>
        <div class="card">
            ID: ${order.id}<br>
            User ID: ${order.user_id}<br>
            Product ID: ${order.product_id}<br>
            Quantity: ${order.quantity}<br>
            Status: ${order.status}
        </div>
        <button onclick="loadOrdersMenu()">Back</button>
    `);
}

function showCancelOrder() {
    render(`
        <h2>Cancel Order</h2>
        <input id="cancelOrderId" placeholder="Order ID">
        <button onclick="cancelOrder()">Cancel</button>
        <br><br>
        <button onclick="loadOrdersMenu()">Back</button>
    `);
}

async function cancelOrder() {
    const id = document.getElementById("cancelOrderId").value;
    await apiRequest(`/orders/cancel/${id}`, "PUT");
    alert("Order Cancelled");
    loadOrdersMenu();
}