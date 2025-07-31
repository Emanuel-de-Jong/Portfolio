
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (project of projects) {
        let cardHtml = `
<div class="card" data-repo-name="${project.repoName}">
    <img class="card-img-top" src="https://raw.githubusercontent.com/Emanuel-de-Jong/${project.repoName}/refs/heads/${project.branch}/${project.imgPaths[0]}">
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

function addLinksToCards() {
    for (project of projects) {
        let card = document.querySelector(`div[data-repo-name="${project.repoName}"]`);
        card.addEventListener("click", (e) => {
            window.open("https://github.com/Emanuel-de-Jong/" + e.currentTarget.dataset.repoName);
        })
    }
};

addProjectCards();
addLinksToCards();
