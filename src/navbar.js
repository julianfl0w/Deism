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

async function loadUserContent() {
    try {
        const userDetails = await getUserDetails();
        const selectedNodeText = document.getElementById('selected-node-text');
        //selectedNodeText.innerHTML = JSON.stringify(userDetails, null, 2); // Pretty print the JSON
        // Create a custom object with only user's name and picture
        const simplifiedUserDetails = {
            name: userDetails.name,
            picture: userDetails.picture
        };
        // Display user's name as a centered header and picture as a full-width image
        selectedNodeText.innerHTML = `
        <div style="text-align: center;">
            <h3>${userDetails.name}</h3>
            <img src="${userDetails.picture}" alt="${userDetails.name}'s Profile Picture" style="width: 100%; height: auto; display: block; margin: auto;">
        </div>
        `;


    } catch (error) {
        console.error('Error loading user content:', error);
        // Handle the error appropriately
    }
}


async function updateNavbarBasedOnLoginStatus() {
    const profileButton = document.getElementById('profileButton');
    const loginButton = document.getElementById('loginButton');

    // User is logged in
    if (await isUserLoggedIn()) {
        const user = await getUserDetails();
        console.log(JSON.stringify(user));
        profileButton.innerHTML = `<img src="${user.picture}" alt="User" class="navbar-profile-pic">`;
        loginButton.textContent = 'Logout';
        loginButton.removeEventListener('click', dlogin);
        loginButton.addEventListener('click', dlogout);
        profileButton.addEventListener('click', loadUserContent);

    }
    else {
        // User is not logged in
        profileButton.textContent = ''; // Clear the profile button
        loginButton.textContent = 'Login';
        loginButton.removeEventListener('click', dlogout);
        loginButton.addEventListener('click', dlogin);
        profileButton.removeEventListener('click', loadUserContent);
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
    console.log("Configure Auth0");
    let thisOrigin = window.location.origin;
    console.log(thisOrigin);
    auth0 = await createAuth0Client({
        domain: "bookofjulian.us.auth0.com",
        client_id: "rR4XKHjHUJyN7G7n9L7C7lkx7ZHJzIso",
        redirect_uri: thisOrigin // This will dynamically set the redirect URI
    });

    console.log("Checking code");
    if (window.location.search.includes("code=")) {
        await auth0.handleRedirectCallback();
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    console.log("Updating Navbar");
    updateNavbarBasedOnLoginStatus();
    console.log("Updated Navbar");
};


console.log("DOM Loaded");
fetch("julian_flare.json")
    .then((response) => response.json())
    .then((data) => {
        populatePillarSelect(data.children, data.text);
    })
    .catch((error) => {
        console.error("Error loading JSON:", error);
    });


document.getElementById('bojButton').addEventListener('click', function () {
    window.location.href = 'index.html';
});

document.getElementById('deismuButton').addEventListener('click', loadDeismUContent);

configureAuth0();
