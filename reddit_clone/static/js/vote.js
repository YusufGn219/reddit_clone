
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".vote-form").forEach((form) => {
        form.querySelectorAll(".vote-btn").forEach((btn) => {
            btn.addEventListener("click", (e) => handleVote(e, form));
        });
    });
});

async function handleVote(e, form) {
    e.preventDefault();

    const btn = e.currentTarget;
    const value = btn.dataset.value; // "up" veya "down"
    const url = form.dataset.url;
    const scoreEl = form.querySelector(".score-display");
    const upBtn = form.querySelector('[data-value="up"]');
    const downBtn = form.querySelector('[data-value="down"]');

    const csrf = getCookie("csrftoken");

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrf,
            },
            body: `value=${value}`,
        });

        if (res.status === 403 || res.redirected) {
            window.location.href = "/login/";
            return;
        }

        const data = await res.json();

        // Skoru güncelle
        scoreEl.textContent = data.score;

        // Buton durumlarını güncelle
        upBtn.classList.remove("upvoted");
        downBtn.classList.remove("downvoted");

        if (data.user_vote === 1) upBtn.classList.add("upvoted");
        if (data.user_vote === -1) downBtn.classList.add("downvoted");

    } catch (err) {
        console.error("Oy gönderilemedi:", err);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}