// Toggle these depending on where you are testing!
const BACKEND_URL = "https://unihack-bot.onrender.com"; // We will put your real Render URL here later
// const BACKEND_URL = "http://127.0.0.1:8000";
document.getElementById('search-btn').addEventListener('click', () => {
    const problem = document.getElementById('problem').value.trim();
    const university = document.getElementById('university').value.trim();
    const location = document.getElementById('location').value.trim();

    if (!problem || !university || !location) {
        alert("Please fill out all fields!");
        return;
    }

    let rejectedAnswers = []; // Keep track of bad answers

    // We wrap the search in a function so the "No" button can call it again
    const fetchAnswer = async () => {
        const loading = document.getElementById('loading');
        const resultsArea = document.getElementById('results-area');
        const resultContent = document.getElementById('result-content');

        loading.classList.remove('hidden');
        resultsArea.classList.add('hidden');
        resultContent.innerHTML = '';

        try {
            const response = await fetch(BACKEND_URL + '/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problem: problem,
                    university: university,
                    location: location,
                    rejected_answers: rejectedAnswers
                })
            });

            if (!response.ok) throw new Error("Network response was not ok");
            const data = await response.json();
            
            loading.classList.add('hidden');
            resultsArea.classList.remove('hidden');

            // Helper to add the Yes/No buttons
            const appendFeedback = (card, solutionText, source) => {
                // Skip feedback for exhausted or error states only
                if (source === 'exhausted' || source === 'error') return;

                const isFromDB = (source === 'db');

                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'feedback-container';

                // DB results: ask if it was relevant (catches wrong-problem matches)
                // Web results: ask if it worked
                feedbackDiv.innerHTML = `
                    <span>${isFromDB ? 'Was this relevant to your problem?' : 'Did this solution work for you?'}</span>
                    <button class="feedback-btn btn-yes">Yes</button>
                    <button class="feedback-btn btn-no">No</button>
                `;

                const btnYes = feedbackDiv.querySelector('.btn-yes');
                const btnNo  = feedbackDiv.querySelector('.btn-no');

                btnYes.addEventListener('click', async () => {
                    btnYes.classList.add('active-yes');
                    btnNo.classList.remove('active-no');
                    btnYes.innerText = "Saved!";
                    btnNo.style.display = "none";
                    feedbackDiv.querySelector('span').innerText = "Great! Saving for future students...";

                    // Only save to DB if it came from web (DB results are already saved)
                    if (!isFromDB) {
                        await fetch(BACKEND_URL + '/save_answer', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ problem, university, location, solution: solutionText })
                        });
                    }
                });

                btnNo.addEventListener('click', () => {
                    // Show "Why?" options
                    feedbackDiv.innerHTML = `
                        <span>Why wasn't it helpful?</span>
                        <button class="feedback-btn btn-reason" data-reason="different_solution">1. The solution is different</button>
                        <button class="feedback-btn btn-reason" data-reason="different_problem">2. Answer to a different problem</button>
                    `;

                    feedbackDiv.querySelectorAll('.btn-reason').forEach(btn => {
                        btn.addEventListener('click', async () => {
                            const reason = btn.dataset.reason;

                            // Only report to block system if result came from DB
                            // (web answers aren't stored in Pinecone so nothing to block)
                            if (isFromDB) {
                                fetch(BACKEND_URL + '/report_feedback', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        query: problem,
                                        result_problem: solutionText,
                                        university: university,
                                        location: location,
                                        reason: reason
                                    })
                                });
                            }

                            // Add to rejected list so it won't show again this session
                            rejectedAnswers.push(solutionText);

                            if (reason === 'different_problem') {
                                feedbackDiv.innerHTML = `<span style="color: var(--primary);">// Reported. Searching again...</span>`;
                            } else {
                                feedbackDiv.innerHTML = `<span style="color: var(--primary);">// Noted. Finding a better solution...</span>`;
                            }

                            // Search DB again first, web as fallback (handled by backend)
                            setTimeout(() => fetchAnswer(), 1200);
                        });
                    });
                });

                card.appendChild(feedbackDiv);
            };

            // ✨ NEW HYBRID RENDERING BLOCK ✨
            if (data.type === "hybrid_solution") {
                // 1. Render Official AI/Verified solution card if it exists
                if (data.solution) {
                    const card = document.createElement('div');
                    card.className = 'result-card ai-card';
                    card.innerText = data.solution;
                    appendFeedback(card, data.solution, data.source);
                    resultContent.appendChild(card);
                }
                
                // 2. Render Student hacks below it if any exist
                if (data.hacks && data.hacks.length > 0) {
                    // Add a terminal-style subtitle divider for student entries
                    const hackHeader = document.createElement('div');
                    hackHeader.style.margin = "1.5rem 0 0.5rem 0";
                    hackHeader.style.color = "var(--primary)";
                    hackHeader.style.fontFamily = "'Share Tech Mono', monospace";
                    hackHeader.innerText = "// Community Mainframe Submissions:";
                    resultContent.appendChild(hackHeader);

                    data.hacks.forEach(hack => {
                        const card = document.createElement('div');
                        card.className = 'result-card student-card';
                        card.innerText = `${hack.solution}\n\n— Submitted by ${hack.author}`;
                        appendFeedback(card, hack.solution, data.source);
                        resultContent.appendChild(card);
                    });
                }
            } else {
                // Fallback for normal web searches, errors, or exhausted attempts
                const card = document.createElement('div');
                card.className = 'result-card ai-card';
                card.innerText = data.solution;
                appendFeedback(card, data.solution, data.source);
                resultContent.appendChild(card);
            }

        } catch (error) {
            console.error("Error fetching hack:", error);
            loading.classList.add('hidden');
            resultsArea.classList.remove('hidden');
            resultContent.innerHTML = '<div class="result-card" style="border-left-color: #ff4f4f; color: #ff4f4f;">Connection Error: Ensure your Python backend is running!</div>';
        }
    };

    // Trigger the first search
    fetchAnswer();
});