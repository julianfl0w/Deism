// Function to populate chapter dropdown
function populateChapterSelect(chapters, alltext) {
    const chapterDropdown = document.getElementById("chapterDropdown");
    const selectedNodeText = document.getElementById("selected-node-text");

    chapterSelect.onclick = function () {
        selectedNodeText.innerHTML = alltext;
        chapterSelect.textContent = "All Chapters";
    };
    chapterSelect.onclick();

    chapterDropdown.innerHTML = '';
    chapters.forEach((chapter) => {
        const option = document.createElement("a");
        option.textContent = chapter.name;
        option.href = "javascript:void(0);";
        option.onclick = function () {
            chapterSelect.textContent = chapter.name;
            selectedNodeText.innerHTML = chapter.text;
        };
        chapterDropdown.appendChild(option);
    });
}

function populatePillarSelect(pillars, alltext) {
    const selectedNodeText = document.getElementById("selected-node-text");
    const pillarDropdown = document.getElementById("pillarDropdown");
    const pillarSelect = document.getElementById("pillarSelect");
    const chapterDropdown = document.getElementById("chapterDropdown");
    const chapterSelect = document.getElementById("chapterSelect");

    pillarSelect.onclick = function () {
        pillarSelect.textContent = "All Pillars"
        selectedNodeText.innerHTML = alltext;
        chapterDropdown.innerHTML = '';
        chapterSelect.textContent = "All Chapters";
    };
    pillarSelect.onclick();

    pillars.forEach((pillar) => {
        const option = document.createElement("a");
        option.textContent = pillar.name;
        option.href = "javascript:void(0);";
        option.onclick = function () {
            pillarSelect.textContent = pillar.name;
            selectedNodeText.innerHTML = pillar.text;
            populateChapterSelect(pillar.children, pillar.text);
        };
        pillarDropdown.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    fetch("julian_flare.json")
        .then((response) => response.json())
        .then((data) => {
            populatePillarSelect(data.children, data.text);
        })
        .catch((error) => {
            console.error("Error loading JSON:", error);
        });

    setupEventListeners();
    configureAuth0();
});

function setupEventListeners() {
    document.getElementById('bojButton').addEventListener('click', function () {
        window.location.href = 'index.html';
    });

    document.getElementById('deismuButton').addEventListener('click', loadDeismUContent);
}

function loadDeismUContent() {
    fetch('deismu.html?_=' + new Date().getTime())
        .then(response => response.text())
        .then(html => {
            const selectedNodeText = document.getElementById('selected-node-text');
            selectedNodeText.innerHTML = html;
            addListeners();
            getCurriculum();
        })
        .catch(error => console.error('Error loading DeismU:', error));
}
function updateNavbarBasedOnLoginStatus() {
    const profileButton = document.getElementById('profileButton');
    const loginButton = document.getElementById('loginButton');

    if (isUserLoggedIn()) {
        // User is logged in
        const user = getUserDetails();
        profileButton.innerHTML = `<img src="${user.picture}" alt="User" class="navbar-profile-pic">`;
        loginButton.textContent = 'Logout';
        loginButton.removeEventListener('click', dlogin);
        loginButton.addEventListener('click', dlogout);
    } else {
        // User is not logged in
        profileButton.textContent = ''; // Clear the profile button
        loginButton.textContent = 'Login';
        loginButton.removeEventListener('click', dlogout);
        loginButton.addEventListener('click', dlogin);
    }
}

async function isUserLoggedIn() {
    return await auth0.isAuthenticated();
}

async function getUserDetails() {
    if (await isUserLoggedIn()) {
        return await auth0.getUser();
    } else {
        return null; // or handle the case where the user is not logged in
    }
}

const dlogin = async () => {
    await auth0.loginWithRedirect();
};

const dlogout = () => {
    auth0.logout({ returnTo: window.location.origin });
};

let auth0 = null;

const configureAuth0 = async () => {
    auth0 = await createAuth0Client({
        domain: "bookofjulian.us.auth0.com",
        client_id: "rR4XKHjHUJyN7G7n9L7C7lkx7ZHJzIso",
        redirect_uri: "https://bookofjulian.net/"
    });

    if (window.location.search.includes("code=")) {
        await auth0.handleRedirectCallback();
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    updateUI();
};

const updateUI = async () => {
    const isAuthenticated = await auth0.isAuthenticated();

    if (isAuthenticated) {
        const user = await auth0.getUser();
        document.getElementById("profileButton").innerHTML = JSON.stringify(user, null, 2);
    }
    updateNavbarBasedOnLoginStatus();
};
