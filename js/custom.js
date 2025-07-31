
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (const [repoName, project] of Object.entries(projects)) {
        let cardHtml = `
<div class="card" data-repo-name="${repoName}">
    <img class="card-img-top" src="https://raw.githubusercontent.com/Emanuel-de-Jong/${repoName}/refs/heads/${project.branch}/${project.imgPaths[0]}">
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
        })

        cards[repoName] = card;
    }
};

addProjectCards();
addLinksToCards();

const search = document.querySelector("#projects .filters .search");
search.addEventListener("keyup", (e) => {
    const val = e.currentTarget.value.toLowerCase();
    if (val === "") {
        for (const card of Object.values(cards)) {
            card.hidden = false;
        }
    } else {
        for (const [repoName, card] of Object.entries(cards)) {
            if (!projects[repoName].name.toLowerCase().includes(val)) {
                card.hidden = true;
            }
        }
    }
});

const pLangSelect = document.querySelector("#projects .filters .p-lang");
pLangSelect.addEventListener("change", (e) => {
    const val = e.currentTarget.value;
    if (val === "") {
        for (const card of Object.values(cards)) {
            card.hidden = false;
        }
    } else {
        for (const [repoName, card] of Object.entries(cards)) {
            if (!projects[repoName].pLangs.includes(val)) {
                card.hidden = true;
            }
        }
    }
});
