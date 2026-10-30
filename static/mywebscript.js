"use strict";

const emotionNames = ["anger", "disgust", "fear", "joy", "sadness"];

function showError(message) {
    const output = document.getElementById("system_response");
    output.replaceChildren();

    const card = document.createElement("div");
    card.className = "error-state";
    card.setAttribute("role", "alert");
    card.textContent = message;
    output.append(card);
}

function showResults(result) {
    const output = document.getElementById("system_response");
    output.replaceChildren();

    const heading = document.createElement("h2");
    heading.textContent = "Emotion scores";
    output.append(heading);

    const list = document.createElement("dl");
    list.className = "score-list";
    for (const name of emotionNames) {
        const label = document.createElement("dt");
        label.textContent = name[0].toUpperCase() + name.slice(1);
        const score = document.createElement("dd");
        score.textContent = Number(result[name]).toFixed(4);
        list.append(label, score);
    }
    output.append(list);

    const dominant = document.createElement("p");
    dominant.className = "dominant-result";
    dominant.textContent = `Dominant emotion: ${result.dominant_emotion}`;
    output.append(dominant);
}

async function runSentimentAnalysis(event) {
    event.preventDefault();
    const text = document.getElementById("textToAnalyze").value.trim();
    const button = document.getElementById("analyzeButton");

    if (!text) {
        showError("Please enter some text before analyzing.");
        return;
    }

    button.disabled = true;
    button.querySelector("span").textContent = "Analyzing…";
    try {
        const query = new URLSearchParams({ textToAnalyze: text });
        const response = await fetch(`/emotionDetector?${query.toString()}`, {
            headers: { Accept: "application/json" },
        });
        const result = await response.json();
        if (!response.ok || result.error) {
            showError(result.error?.message || "The emotion analysis could not be completed.");
            return;
        }
        showResults(result);
    } catch (error) {
        showError("Could not contact the app. Please try again.");
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Analyze emotions";
    }
}

document.getElementById("analysisForm").addEventListener("submit", runSentimentAnalysis);
