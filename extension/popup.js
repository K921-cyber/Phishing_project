document.getElementById('scanBtn').addEventListener('click', () => {
    const verdict = document.getElementById('verdict');
    const reasonsList = document.getElementById('reasons');
    const scoreFill = document.getElementById('score-fill');
    
    verdict.innerText = "Analyzing...";
    verdict.style.color = "#333";
    reasonsList.innerHTML = "";
    scoreFill.style.width = "0%";

    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {action: "scan_email"}, (response) => {
            if (response && response.status === "success") {
                const data = response.result;
                
                // Update UI
                verdict.innerText = data.verdict;
                verdict.style.color = data.color;
                scoreFill.style.width = data.score + "%";
                scoreFill.style.backgroundColor = data.color;

                // List reasons
                data.reasons.forEach(reason => {
                    let li = document.createElement("li");
                    li.innerText = reason;
                    reasonsList.appendChild(li);
                });

            } else {
                verdict.innerText = "Error";
                let li = document.createElement("li");
                li.innerText = response ? response.message : "Ensure you are on an open Gmail email.";
                reasonsList.appendChild(li);
            }
        });
    });
});