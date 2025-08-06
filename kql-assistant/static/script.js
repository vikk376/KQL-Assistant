function generateKQL() {
    const prompt = document.getElementById("inputPrompt").value;
    const output = document.getElementById("kqlOutput");

    output.textContent = "Generating KQL, please wait... ⏳";

    fetch("/generate_kql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        output.textContent = data.kql;
    })
    .catch(error => {
        output.textContent = "❌ Error generating KQL.";
        console.error("Error:", error);
    });
}
