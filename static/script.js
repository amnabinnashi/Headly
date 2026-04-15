console.log("JS is running");

async function analyze() {
    const url = document.getElementById("url").value;

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    document.getElementById("results").classList.add("hidden");

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        const report = data.report;

        document.getElementById("results").classList.remove("hidden");

        document.getElementById("seoScore").innerText = report.seo_score;
        document.getElementById("metaTitle").innerText = report.meta.title;
        document.getElementById("metaDesc").innerText = report.meta.description;

        document.getElementById("headings").innerText =
            `H1: ${report.stats.H1} | H2: ${report.stats.H2} | H3: ${report.stats.H3}`;

        document.getElementById("links").innerText =
            `Internal: ${report.internal_links} | External: ${report.external_links}`;

    } catch (err) {
        alert("Something went wrong");
        console.error(err);
    }
}
