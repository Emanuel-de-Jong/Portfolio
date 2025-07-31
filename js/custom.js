
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (const [repoName, project] of Object.entries(projects)) {
        let cardHtml = `
<div class="card" data-repo-name="${repoName}">
    <div class="thumbnail">
        <img class="card-img-top" src="https://raw.githubusercontent.com/Emanuel-de-Jong/${repoName}/refs/heads/${project.branch}/${project.imgPaths[0]}">
        <p class="date">${project.date.toISOString().slice(0, 10)}</p>
    </div>
    <div class="card-body">
        <h5 class="card-title">${project.name}</h5>
        <p class="description">${project.description}</p>
        <div class="tags">
            <span class="badge text-bg-secondary">${project.madeFor}</span>`;
            
        for (pLang of project.pLangs) {
            cardHtml += `<span class="badge text-bg-primary">${pLang}</span>`;
        }

        cardHtml += `
        </div>
    </div>
</div>`;

        gridDiv.innerHTML += cardHtml;
    }
};

let cards = {}
function addLinksToCards() {
    for (const [repoName, project] of Object.entries(projects)) {
        let card = document.querySelector(`div[data-repo-name="${repoName}"]`);
        card.addEventListener("click", (e) => {
            window.open("https://github.com/Emanuel-de-Jong/" + e.currentTarget.dataset.repoName);
        });

        cards[repoName] = card;
    }
};

addProjectCards();
addLinksToCards();

const search = document.querySelector("#projects .filters .search");
const inspirationSelect = document.querySelector("#projects .filters .inspiration");
const pLangSelect = document.querySelector("#projects .filters .p-lang");
function applyFilters() {
    const searchValue = search.value.trim().toLowerCase();
    const inspirationValue = inspirationSelect.value;
    const pLangValue = pLangSelect.value;

    for (const [repoName, card] of Object.entries(cards)) {
        const project = projects[repoName];
        
        if (searchValue !== "" && !project.name.toLowerCase().includes(searchValue)) {
            card.hidden = true;
            continue;
        }
        
        if (inspirationValue !== "" && project.madeFor !== inspirationValue) {
            card.hidden = true;
            continue;
        }
        
        if (pLangValue !== "" && !project.pLangs.includes(pLangValue)) {
            card.hidden = true;
            continue;
        }
        
        card.hidden = false;
    }
};

search.addEventListener("keyup", applyFilters);
inspirationSelect.addEventListener("change", applyFilters);
pLangSelect.addEventListener("change", applyFilters);
