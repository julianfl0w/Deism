function addURL(auth0) {
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

async function getCompletedCourses(auth0) {
    try {
        // Obtain the JWT token
        const token = await auth0.getTokenSilently();

        // Set up your API endpoint
        const apiEndpoint = 'https://your-api-endpoint.com/user-courses';

        // Make the API request
        const response = await fetch(apiEndpoint, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const courses = await response.json();
        
        return courses;
    } catch (error) {
        console.error('Error fetching completed courses:', error);
        throw error;
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
            // Check if the current item has a meta dictionary with a reference list
            let hasReference = itemData[key]?.meta?.reference?.length > 0;

            if (key !== "meta") {
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

                    if (hasReference) {
                        sectionTitle.onclick = function () {
                            window.open(itemData[key].meta.reference[0], '_blank');
                        };
                        sectionTitle.style.textDecoration = "underline";
                        sectionTitle.style.cursor = "pointer";
                    } else {
                        sectionTitle.onclick = function () {
                            this.nextElementSibling.classList.toggle("active");
                        };
                    }

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

                    if (hasReference) {
                        item.onclick = function () {
                            window.open(itemData.meta.reference[0], '_blank');
                        };
                        item.style.textDecoration = "underline";
                        item.style.cursor = "pointer";
                        item.innerText = key + ": " + itemData[key];
                    } else {
                        item.innerText = key + ": " + itemData[key];
                    }

                    parentElement.appendChild(item);
                }
            }
        });
    }

    createList(data, container);
}


function addListeners(auth0){
    document.body.addEventListener('click', function(event) {
        switch (event.target.id) {
            case 'btn-verify-certificate':
                addURL(auth0); // Function for verifying certificate
                break;
        }
    });
}
