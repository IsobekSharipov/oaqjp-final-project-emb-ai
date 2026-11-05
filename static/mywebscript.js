/* Submit text to the Flask emotion detector and show the response. */
function RunSentimentAnalysis() {
    const text = document.getElementById("textToAnalyze").value;
    const output = document.getElementById("system_response");
    output.textContent = "Analyzing...";

    fetch("/emotionDetector?textToAnalyze=" + encodeURIComponent(text))
        .then(async (response) => {
            const message = await response.text();
            output.textContent = message;
        })
        .catch(() => {
            output.textContent = "Unable to contact the emotion detector.";
        });
}
