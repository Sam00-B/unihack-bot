const BACKEND_URL = "https://your-backend-name.onrender.com"; 
// const BACKEND_URL = "http://127.0.0.1:8000";
document.getElementById('submit-hack-btn').addEventListener('click', async () => {
    const problem = document.getElementById('sub-problem').value.trim();
    const university = document.getElementById('sub-university').value.trim();
    const location = document.getElementById('sub-location').value.trim();
    const solution = document.getElementById('sub-solution').value.trim();
    
    let author = document.getElementById('sub-author').value.trim();
    if (!author) {
        author = "Anonymous Student";
    }

    if (!problem || !university || !location || !solution) {
        alert("Please fill out all required fields!");
        return;
    }

    const sysMsg = document.getElementById('sys-message');
    sysMsg.classList.remove('hidden');
    sysMsg.className = 'sys-message'; 
    sysMsg.innerText = "Transmitting to mainframe...";
    sysMsg.style.color = "var(--primary)";
    sysMsg.style.borderLeftColor = "var(--primary)";
    
    try {
        const response = await fetch('${BACKEND_URL}/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                problem: problem,
                university: university,
                location: location,
                solution: solution,
                author: author
            })
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        // Show Success
        sysMsg.className = 'sys-message sys-success';
        sysMsg.innerText = "Hack successfully uploaded to the database! Thank you for contributing.";
        
        // Clear the form
        document.getElementById('sub-problem').value = '';
        document.getElementById('sub-solution').value = '';

    } catch (error) {
        console.error("Error transmitting hack:", error);
        // Show Error
        sysMsg.className = 'sys-message sys-error';
        sysMsg.innerText = "Transmission failed. Ensure the backend connection is online.";
    }
});