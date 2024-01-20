function addURL() {
    // Prompt the user to enter a URL
    var urlToAdd = prompt(
        "Please enter the Coursera certificate URL to verify:"
    );
    if (urlToAdd) {
        // Send the URL to the Flask app for verification
        fetch("http://127.0.0.1:5000/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ urls: [urlToAdd] }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(
                        "Network response was not ok " + response.statusText
                    );
                }
                return response.json();
            })
            .then((data) => {
                // Print the result to the screen
                document.getElementById("result").textContent = JSON.stringify(
                    data,
                    null,
                    2
                );
            })
            .catch((error) => {
                console.error(
                    "There has been a problem with your fetch operation:",
                    error
                );
                document.getElementById("result").textContent = error.message;
            });
    }
}
function getCurriculum() {
    fetch("curriculum.json")
        .then((response) => response.json())
        .then((jsonData) => {
            createExpandableList(
                jsonData,
                document.getElementById("curriculumList")
            );
        })
        .catch((error) => {
            console.error("Fetch operation error:", error);
            document.getElementById("curriculumList").textContent =
                error.message;
        });
}
function createExpandableList(data, container) {
    function createList(itemData, parentElement) {
        Object.keys(itemData).forEach((key) => {
            if (key !== "meta") {
                // Exclude 'meta' nodes
                if (
                    typeof itemData[key] === "object" &&
                    itemData[key] !== null &&
                    !Array.isArray(itemData[key])
                ) {
                    // Create section for the object
                    let section = document.createElement("div");
                    section.className = "section";

                    let sectionTitle = document.createElement("button");
                    sectionTitle.className = "section-title";
                    sectionTitle.innerText = key;
                    sectionTitle.onclick = function () {
                        this.nextElementSibling.classList.toggle("active");
                    };

                    let itemList = document.createElement("div");
                    itemList.className = "item-list";

                    // Recursively create list for nested objects
                    createList(itemData[key], itemList);

                    section.appendChild(sectionTitle);
                    section.appendChild(itemList);
                    parentElement.appendChild(section);
                } else {
                    // Create item for non-object data
                    let item = document.createElement("div");
                    item.className = "item";
                    item.innerText = key + ": " + itemData[key];
                    parentElement.appendChild(item);
                }
            }
        });
    }

    createList(data, container);
}

function addListeners(){

    document.body.addEventListener('click', function(event) {
        switch (event.target.id) {
            case 'btn-verify-certificate':
                addURL(); // Function for verifying certificate
                break;
        }
    });
}
