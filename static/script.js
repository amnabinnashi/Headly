async function analyze() {
    const url = document.getElementById("url").value;

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("results").classList.add("hidden");

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    document.getElementById("loading").classList.add("hidden");

    if (data.error) {
        alert(data.error);
        return;
    }

    const report = data.report;

    document.getElementById("results").classList.remove("hidden");

    // SEO score
    document.getElementById("seoScore").innerText = report.seo_score;
    document.getElementById("progressBar").style.width = report.seo_score + "%";

    // meta
    document.getElementById("metaTitle").innerText = report.meta.title || "Missing";
    document.getElementById("metaDesc").innerText = report.meta.description || "Missing";

    // headings
    document.getElementById("headings").innerText =
        `H1: ${report.stats.H1} | H2: ${report.stats.H2} | H3: ${report.stats.H3}`;

    // links
    document.getElementById("links").innerText =
        `Internal: ${report.internal_links} | External: ${report.external_links}`;

    // data
    document.getElementById("data").innerText =
        `Images: ${report.data.images} | Scripts: ${report.data.scripts}`;

    // suggestions
    const suggestions = [];

    if (!report.meta.title) suggestions.push("Add a meta title");
    if (!report.meta.description) suggestions.push("Add a meta description");
    if (report.stats.H1 === 0) suggestions.push("Add at least one H1 heading");
    if (report.internal_links < 3) suggestions.push("Add more internal links");

    const list = document.getElementById("suggestions");
    list.innerHTML = "";

    suggestions.forEach(item => {
        const li = document.createElement("li");
        li.innerText = item;
        list.appendChild(li);
    });
}
