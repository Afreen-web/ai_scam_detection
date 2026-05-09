let mode = "LOCAL AI";

// ✅ Set mode
function setMode(selectedMode) {
    mode = selectedMode;
}

// ✅ Reset form
function resetForm() {
    document.getElementById("message").value = "";
    document.getElementById("resultText").innerText = "--";
    document.getElementById("confidenceText").innerText = "Confidence Score: 0%";
    document.getElementById("modeText").innerText = "Mode Used: --";
    document.getElementById("progressFill").style.width = "0%";

    document.getElementById("historyTable").innerHTML = "";
}

// ✅ Check message
function checkMessage() {

    let msg = document.getElementById("message").value;

    if (msg.trim() === "") {
        alert("Enter message");
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"   // ✅ FIXED
        },
        body: JSON.stringify({                  // ✅ FIXED
            message: msg,
            mode: mode
        })
    })

    .then(response => response.json())
    .then(data => {

        document.getElementById("resultText").innerText = data.result;
        document.getElementById("confidenceText").innerText =
            "Confidence Score: " + data.confidence + "%";

        document.getElementById("modeText").innerText =
            "Mode Used: " + data.mode;

        let bar = document.getElementById("progressFill");
        bar.style.width = data.confidence + "%";
        bar.style.background = data.result === "SCAM" ? "red" : "green";

        // HISTORY
        let table = document.getElementById("historyTable");
        table.innerHTML = "";

        if (data.history && data.history.length > 0) {
            data.history.forEach((item, index) => {
                table.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.message}</td>
                        <td>${item.result}</td>
                        <td>${item.confidence}%</td>
                        <td>${item.mode}</td>
                        <td>${item.time}</td>
                    </tr>
                `;
            });
        } else {
            table.innerHTML = "<tr><td colspan='6'>No history available</td></tr>";
        }

    })
    .catch(error => {
        console.error("Error:", error);
        alert("Backend not responding");
    });
}