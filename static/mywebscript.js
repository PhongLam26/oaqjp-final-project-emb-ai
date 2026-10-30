"use strict";

function showError(message) {
    const output = document.getElementById("system_response");
    output.replaceChildren();

    const card = document.createElement("div");
    card.className = "error-state";
    card.setAttribute("role", "alert");
    card.textContent = message;
    output.append(card);
}

function showResults(message) {
    const output = document.getElementById("system_response");
    output.replaceChildren();

    const heading = document.createElement("h2");
    heading.textContent = "Emotion analysis result";
    output.append(heading);

    const result = document.createElement("p");
    result.className = "dominant-result";
    result.textContent = message;
    output.append(result);
}

async function runSentimentAnalysis(event) {
    event.preventDefault();
    const text = document.getElementById("textToAnalyze").value.trim();
    const button = document.getElementById("analyzeButton");

    if (!text) {
        showError("Invalid Input! Please try again.");
        return;
    }

    button.disabled = true;
    button.querySelector("span").textContent = "Analyzing…";
    try {
        const query = new URLSearchParams({ textToAnalyze: text });
        const response = await fetch(`/emotionDetector?${query.toString()}`);
        const message = await response.text();
        if (!response.ok || message === "Invalid Input! Please try again.") {
            showError(message || "The emotion analysis could not be completed.");
            return;
        }
        showResults(message);
    } catch (error) {
        showError("Could not contact the app. Please try again.");
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Analyze emotions";
    }
}

document.getElementById("analysisForm").addEventListener("submit", runSentimentAnalysis);
