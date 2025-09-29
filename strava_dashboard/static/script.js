document.getElementById('connectBtn').addEventListener('click', () => {
    window.location.href = 'http://localhost:5000/authorize';
});

async function fetchActivites() {
    try {
        const res = await fetch('http://localhost:5000/activities');
        const data = await res.json();
        const container = document.getElementById('activities');
        container.innerHTML = '<h2>Recent Activities</h2>';
        data.activites.forEach(act => {
            const div = document.createElement('div');
            div.innerHTML = `
                <p><strong>${act.type}</strong><br>
                ${act.type} - ${(act.distance / 1000).toFixed(2)} km -
                ${(act.moving_time / 60).toFixed(2)} min</p>
            `;
        });
    } catch (err) {
        console.error('Error fetching activities:', err);
    }
}

window.onload = fetchActivites;