async function analyze() {
    const url = document.getElementById("url").value;

    if (!url) {
        alert("اكتب رابط");
        return;
    }

    const res = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    });

    const data = await res.json();

    document.getElementById("results").classList.remove("hidden");

    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("score").innerText = data.score;
    document.getElementById("title").innerText = data.title;
    document.getElementById("desc").innerText = data.description;
    document.getElementById("headings").innerText =
        `H1: ${data.h1} | H2: ${data.h2} | H3: ${data.h3}`;
    document.getElementById("links").innerText =
        `Internal: ${data.internal_links} | External: ${data.external_links}`;

    document.getElementById("suggestions").innerHTML =
        data.suggestions.map(s => "• " + s).join("<br>");
}
