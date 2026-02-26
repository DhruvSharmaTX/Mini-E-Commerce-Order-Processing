function loadProductsMenu() {
    render(`
        <h2>Products</h2>
        <button onclick="getAllProducts()">Get All Products</button>
        <button onclick="getAvailableProducts()">Get Available Products</button>
        <button onclick="showCreateProduct()">Create Product</button>
        <button onclick="showGetProduct()">Get Product</button>
        <br><br>
        <button onclick="loadHome()">Back</button>
    `);
}

async function getAllProducts() {
    const products = await apiRequest("/products/");
    let html = "<h2>All Products</h2>";
    products.forEach(product => {
        html += `
            <div class="card">
                ID: ${product.id}<br>
                Name: ${product.name}<br>
                Price: $${product.price}<br>
                Quantity: ${product.quantity}
            </div>
        `;
    });

    html += `<button onclick="loadProductsMenu()">Back</button>`;
    render(html);
}

async function getAvailableProducts() {
    const products = await apiRequest("/products/available");
    let html = "<h2>Available Products</h2>";
    products.forEach(product => {
        html += `
            <div class="card">
                ${product.name} - Quantity: ${product.quantity}
            </div>
        `;
    });
    html += `<button onclick="loadProductsMenu()">Back</button>`;
    render(html);
}

function showCreateProduct() {
    render(`
        <h2>Create Product</h2>
        <input id="pname" placeholder="Name"><br>
        <input id="price" type="number" placeholder="Price"><br>
        <input id="quantity" type="number" placeholder="Quantity"><br>
        <button onclick="createProduct()">Submit</button>
        <br><br>
        <button onclick="loadProductsMenu()">Back</button>
    `);
}

async function createProduct() {
    await apiRequest("/products/", "POST", {
        name: document.getElementById("pname").value,
        price: parseFloat(document.getElementById("price").value),
        quantity: parseInt(document.getElementById("quantity").value)
    });
    alert("Product Created");
    loadProductsMenu();
}

function showGetProduct() {
    render(`
        <h2>Get Product</h2>
        <input id="productId" placeholder="Product ID">
        <button onclick="getProduct()">Search</button>
        <br><br>
        <button onclick="loadProductsMenu()">Back</button>
    `);
}

async function getProduct() {
    const id = document.getElementById("productId").value;
    const product = await apiRequest(`/products/${id}`);
    render(`
        <h2>Product Details</h2>
        <div class="card">
            ID: ${product.id}<br>
            Name: ${product.name}<br>
            Price: $${product.price}<br>
            Quantity: ${product.quantity}
        </div>
        <button onclick="loadProductsMenu()">Back</button>
    `);
}