
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (const [repoName, project] of Object.entries(projects)) {
        let cardHtml = `
<div class="card" data-repo-name="${repoName}">
    <div class="thumbnail">
        <div id="${repoName}-carousel" class="carousel slide">
            <div class="carousel-inner">`;

        for (let i = 0; i < project.imgPaths.length; i++) {
            const imgPath = project.imgPaths[i];
            const activeClass = i === 0 ? "active" : "";
            cardHtml += `
                <div class="carousel-item ${activeClass}">
                    <img src="https://raw.githubusercontent.com/Emanuel-de-Jong/${repoName}/refs/heads/${project.branch}/${imgPath}">
                </div>`;
        }

        cardHtml += `</div>`;

        if (project.imgPaths.length > 1) {
            cardHtml += `
            <button type="button" class="carousel-control-prev" data-bs-target="#${repoName}-carousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </button>
            <button type="button" class="carousel-control-next" data-bs-target="#${repoName}-carousel" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
            </button>`;
        }
        
        cardHtml += `
        </div>
        <p class="date">${project.activeDateStart.toISOString().slice(0, 10)}</p>
    </div>
    <div class="card-body">
        <h5 class="card-title">${project.name}</h5>
        <p class="description">${project.description}</p>
        <div class="tags">
            <span class="badge text-bg-secondary">${project.madeFor}</span>`;
            
        for (const pLang of project.pLangs) {
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
        const card = document.querySelector(`div[data-repo-name="${repoName}"]`);

        const cardBody = card.querySelector(".card-body");
        cardBody.addEventListener("click", (e) => {
            window.open("https://github.com/Emanuel-de-Jong/" + e.currentTarget.parentElement.dataset.repoName);
        });

        cards[repoName] = card;
    }
};

const orderBySelect = document.querySelector("#projects .filters .order-by");
function orderGrid() {
    const orderBy = orderBySelect.value;
    const cardArray = Object.values(cards);
    
    cardArray.sort((a, b) => {
        const projectA = projects[a.dataset.repoName];
        const projectB = projects[b.dataset.repoName];
        
        switch (orderBy) {
            case "nameAsc":
                return projectA.name.localeCompare(projectB.name);
            case "nameDesc":
                return projectB.name.localeCompare(projectA.name);
            case "dateDesc":
                return projectB.activeDateStart - projectA.activeDateStart;
            case "dateAsc":
                return projectA.activeDateStart - projectB.activeDateStart;
            default:
                return 0;
        }
    });
    
    gridDiv.innerHTML = '';
    cardArray.forEach(card => {
        gridDiv.appendChild(card);
    });
}

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

orderBySelect.addEventListener("change", orderGrid);
search.addEventListener("keyup", applyFilters);
inspirationSelect.addEventListener("change", applyFilters);
pLangSelect.addEventListener("change", applyFilters);

addProjectCards();
addLinksToCards();
orderGrid();
