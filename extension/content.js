// Listen for scan request
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scan_email") {
        
        // 1. Get Text
        let emailBody = document.querySelector('.a3s.aiL'); 
        let text = emailBody ? emailBody.innerText : "";
        
        // 2. Get Links (Forensic Data)
        let links = [];
        if (emailBody) {
            let anchorTags = emailBody.getElementsByTagName("a");
            for (let a of anchorTags) {
                links.push(a.href);
            }
        }

        if (!text) {
            sendResponse({status: "error", message: "No email open."});
            return;
        }

        // Send to Backend
        fetch("http://127.0.0.1:5000/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_text: text, links: links })
        })
        .then(response => response.json())
        .then(data => sendResponse({status: "success", result: data}))
        .catch(err => sendResponse({status: "error", message: "Server Offline"}));

        return true; 
    }
});