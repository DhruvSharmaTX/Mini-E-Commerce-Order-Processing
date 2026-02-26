function loadUsersMenu() {
    render(`
        <h2>Users</h2>
        <button onclick="getAllUsers()">Get All Users</button>
        <button onclick="showCreateUser()">Create User</button>
        <button onclick="showGetUser()">Get User</button>
        <br><br>
        <button onclick="loadHome()">Back</button>
    `);
}

async function getAllUsers() {
    const users = await apiRequest("/users/");

    let html = `
        <h2>All Users</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
    `;

    users.forEach(user => {
        html += `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
        <br>
        <button onclick="loadUsersMenu()">Back</button>
    `;

    render(html);
}

function showCreateUser() {
    render(`
        <h2>Create User</h2>
        <input id="name" placeholder="Name">
        <input id="email" placeholder="Email">
        <button onclick="createUser()">Submit</button>
        <button onclick="loadUsersMenu()">Back</button>
    `);
}

async function createUser() {
    await apiRequest("/users/", "POST", {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value
    });
    alert("User Created");
    loadUsersMenu();
}

function showGetUser() {
    render(`
        <h2>Get User</h2>
        <input id="userId" placeholder="User ID">
        <button onclick="getUser()">Search</button>
        <button onclick="loadUsersMenu()">Back</button>
    `);
}

async function getUser() {
    const id = document.getElementById("userId").value;
    const user = await apiRequest(`/users/${id}`);
    render(`
        <h2>User Details</h2>
        <div class="card">
            ${user.id} - ${user.name} - ${user.email}
        </div>
        <button onclick="loadUsersMenu()">Back</button>
    `);
}