// Function to populate chapter dropdown
function populateChapterSelect(chapters, alltext) {

    const chapterDropdown = document.getElementById("chapterDropdown");
    const selectedNodeText = document.getElementById("selected-node-text");


    // Default option for pillarSelect
    chapterSelect.onclick = function () {
        selectedNodeText.innerHTML = alltext; // Display text of the currently selected pillar
        chapterSelect.textContent = "All Chapters";
    };
    chapterSelect.onclick();


    chapterDropdown.innerHTML = ''; // start over!
    chapters.forEach((chapter) => {
        const option = document.createElement("a");
        option.textContent = chapter.name;
        option.href = "javascript:void(0);";
        option.onclick = function () {
            chapterSelect.textContent = chapter.name;
            selectedNodeText.innerHTML = chapter.text; // Chapter text
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

    // Default option for pillarSelect
    pillarSelect.onclick = function () {
        pillarSelect.textContent = "All Pillars"
        selectedNodeText.innerHTML = alltext; // Display text of the currently selected pillar
        chapterDropdown.innerHTML = ''; // Clear chapter dropdown
        chapterSelect.textContent = "All Chapters";
    };
    pillarSelect.onclick();

    pillars.forEach((pillar) => {
        const option = document.createElement("a");
        option.textContent = pillar.name;
        option.href = "javascript:void(0);";
        option.onclick = function () {
            pillarSelect.textContent = pillar.name;
            selectedNodeText.innerHTML = pillar.text; // Child text
            populateChapterSelect(pillar.children, pillar.text);

        };
        pillarDropdown.appendChild(option);
    });
}

fetch("julian_flare.json")
    .then((response) => response.json())
    .then((data) => {
        // Assuming 'data.children' and 'data.text' exist
        populatePillarSelect(data.children, data.text);
    })
    .catch((error) => {
        console.error("Error loading JSON:", error);
    });

document.getElementById('bojButton').addEventListener('click', function() {
    window.location.href = 'index.html';
});

document.getElementById('deismuButton').addEventListener('click', () => {
    fetch('deismu.html?_=' + new Date().getTime())
        .then(response => response.text())
        .then(html => {
            const selectedNodeText = document.getElementById('selected-node-text');
            selectedNodeText.innerHTML = html;

            addListeners();
            getCurriculum();
            configureAuth0();
            
        })
        .catch(error => console.error('Error loading DeismU:', error));
});
