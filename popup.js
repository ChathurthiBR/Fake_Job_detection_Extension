document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("checkBtn").addEventListener("click", async () => {

        try {
            const [tab] = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: getJobText
            }, async (results) => {

                try {
                    let jobText = results[0].result;

                    let response = await fetch("http://127.0.0.1:5000/predict", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            description: jobText
                        })
                    });

                    let data = await response.json();

                    console.log("Backend Response:", data);

                    let result = data.result || "Unknown";
                    let confidence = data.confidence || 0;

                    document.getElementById("result").innerText =
                        `Result: ${result} (${confidence}%)`;

                } catch (error) {
                    console.error(error);
                    document.getElementById("result").innerText =
                        "Error fetching result";
                }
            });

        } catch (error) {
            console.error(error);
        }
    });
});

// SMART TEXT EXTRACTION
function getJobText() {

    let title = document.querySelector("h1")?.innerText || "";

    let description =
        document.querySelector(".jobs-description")?.innerText ||
        document.querySelector(".description")?.innerText ||
        document.body.innerText.substring(0, 1500);

    return title + " " + description;
}