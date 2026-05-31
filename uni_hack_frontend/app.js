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
            const response = await fetch('http://127.0.0.1:8000/ask', {
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
                // If it came from the DB, it's already verified, no need to ask
                if (source === 'db' || source === 'exhausted' || source === 'error') return;

                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'feedback-container';
                feedbackDiv.innerHTML = `
                    <span>Did this solution work for you?</span>
                    <button class="feedback-btn btn-yes">Yes</button>
                    <button class="feedback-btn btn-no">No</button>
                `;
                
                const btnYes = feedbackDiv.querySelector('.btn-yes');
                const btnNo = feedbackDiv.querySelector('.btn-no');

                btnYes.addEventListener('click', async () => {
                    btnYes.classList.add('active-yes');
                    btnNo.classList.remove('active-no');
                    btnYes.innerText = "Saved!";
                    btnNo.style.display = "none";
                    feedbackDiv.querySelector('span').innerText = "Great! Saving for future students...";
                    
                    // Tell backend to save it to the DB!
                    await fetch('http://127.0.0.1:8000/save_answer', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ problem, university, location, solution: solutionText })
                    });
                });

                btnNo.addEventListener('click', () => {
                    // Add this bad answer to our list
                    rejectedAnswers.push(solutionText);
                    // Search again!
                    fetchAnswer(); 
                });

                card.appendChild(feedbackDiv);
            };

            if (data.type === "student_hacks") {
                data.hacks.forEach(hack => {
                    const card = document.createElement('div');
                    card.className = 'result-card student-card';
                    card.innerText = `${hack.solution}\n\n— Submitted by ${hack.author}`;
                    appendFeedback(card, hack.solution, data.source);
                    resultContent.appendChild(card);
                });
            } else {
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