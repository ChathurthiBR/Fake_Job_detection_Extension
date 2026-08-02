// Try to extract job info

let title = document.querySelector("h1")?.innerText || "No Title Found";
let description = document.body.innerText;

// Send to backend (Python API)
fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: title,
        description: description
    })
})
.then(res => res.json())
.then(data => {

    let resultText = `Result: ${data.prediction} \nConfidence: ${data.confidence}`;

    alert(resultText);

})
.catch(err => {
    alert("Error connecting to backend!");
});