
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (const [repoName, project] of Object.entries(projects)) {
        let cardHtml = `
<div class="card" data-repo-name="${repoName}">
    <div class="thumbnail">
        <div id="${repoName}-carousel" class="carousel slide">
            <div class="carousel-inner">`;

        const imgPaths = project.imgPaths;
        for (let i = 0; i < imgPaths.length; i++) {
            const imgPath = imgPaths[i];
            const activeClass = i === 0 ? "active" : "";
            cardHtml += `
                <div class="carousel-item ${activeClass}">
                    <img src="https://raw.githubusercontent.com/Emanuel-de-Jong/${repoName}/refs/heads/${project.branch}/${imgPath}">
                </div>`;
        }

        if (imgPaths.length == 0) {
            cardHtml += `
                <div class="carousel-item active">
                    <img src="assets/imgs/No-Image.png">
                </div>`;
        }

        cardHtml += `</div>`;

        if (imgPaths.length > 1) {
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
    </div>
    <div class="card-body">
        <h5 class="card-title">${project.name}</h5>
        <p class="description">${project.description}</p>
        <div class="tags">
            <span class="badge text-bg-secondary">${project.madeFor}</span>`;
            
        for (const skill of project.skills) {
            cardHtml += `<span class="badge text-bg-primary">${skill}</span>`;
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

let skillOptions = new Set();
for (const project of Object.values(projects)) {
    for (const skill of project.skills) {
        skillOptions.add(skill);
    }
}
skillOptions = Array.from(skillOptions).sort();

let skillSelectSettings = {
    options: [],
    create: false,
    plugins: {
		remove_button:{
			title:"Remove this skill",
		}
	},
};

for (const skill of skillOptions) {
    skillSelectSettings["options"].push({ value: skill, text: skill });
}

const skillSelect = new TomSelect("#skills input", skillSelectSettings);

const orderByDefaultDirections = {
    "name": "asc",
    "workDays": "desc",
    "lastChangeDate": "desc",
    "activeDateStart": "desc",
    "activeDateEnd": "desc",
};
const orderBySelect = document.getElementById("order-by-value");
const orderByDirectionBtn = document.getElementById("order-by-direction");

let lastOrderBy = "workDays"
function orderGrid() {
    const cardArray = Object.values(cards);

    const orderBy = orderBySelect.value;
    let orderByDirection = orderByDirectionBtn.dataset.direction;
    if (orderBy !== lastOrderBy) {
        lastOrderBy = orderBy;

        if (orderByDefaultDirections[orderBy] !== orderByDirection)
        orderByDirection = toggleOrderByDirectionBtn();
    }
    
    cardArray.sort((a, b) => {
        let projectA, projectB, fallback;
        if (orderByDirection == "asc") {
            projectA = projects[a.dataset.repoName];
            projectB = projects[b.dataset.repoName];
            
            // nameAsc as fallback.
            fallback = projectA.name.localeCompare(projectB.name);
        } else {
            projectA = projects[b.dataset.repoName];
            projectB = projects[a.dataset.repoName];

            // nameAsc as fallback.
            fallback = projectB.name.localeCompare(projectA.name);
        }
        
        let diff = 0;
        switch (orderBy) {
            case "name":
                diff = projectA.name.localeCompare(projectB.name);
                break;
            case "workDays":
                diff = projectA.workDays - projectB.workDays;
                break;
            case "lastChangeDate":
                diff = projectB.lastChangeDate - projectA.lastChangeDate;
                break;
            case "activeDateStart":
                diff = projectB.activeDateStart - projectA.activeDateStart;
                break;
            case "activeDateEnd":
                diff = projectB.activeDateEnd - projectA.activeDateEnd;
                break;
        }

        return diff != 0 ? diff : fallback;
    });
    
    gridDiv.innerHTML = '';
    cardArray.forEach(card => {
        gridDiv.appendChild(card);
    });
}

const search = document.getElementById("search");
const inspirationSelect = document.getElementById("inspiration");
function applyFilters() {
    const searchValue = search.value.trim().toLowerCase();
    const inspirationValue = inspirationSelect.value;
    const skillValue = "";

    for (const [repoName, card] of Object.entries(cards)) {
        const project = projects[repoName];
        
        if (searchValue !== ""
                && !project.name.toLowerCase().includes(searchValue)
                && !project.description.toLowerCase().includes(searchValue)) {
            card.hidden = true;
            continue;
        }
        
        if (inspirationValue !== "" && project.madeFor !== inspirationValue) {
            card.hidden = true;
            continue;
        }
        
        if (skillValue !== "" && !project.skills.includes(skillValue)) {
            card.hidden = true;
            continue;
        }
        
        card.hidden = false;
    }

    updateProjectCount();
}

let visibleCountElement = document.getElementById("visible-count");
let totalCountElement = document.getElementById("total-count");
function updateProjectCount() {
    const totalCount = Object.keys(cards).length;
    const visibleCount = Object.values(cards).filter(card => !card.hidden).length;
    
    totalCountElement.textContent = totalCount;
    visibleCountElement.textContent = visibleCount;
}

function toggleOrderByDirectionBtn() {
    if (orderByDirectionBtn.dataset.direction == "asc") {
        orderByDirectionBtn.dataset.direction = "desc";
    } else {
        orderByDirectionBtn.dataset.direction = "asc";
    }

    return orderByDirectionBtn.dataset.direction;
}

orderBySelect.addEventListener("change", orderGrid);
search.addEventListener("keyup", applyFilters);
inspirationSelect.addEventListener("change", applyFilters);
orderByDirectionBtn.addEventListener("click", () => {
    toggleOrderByDirectionBtn();
    orderGrid();
});

addProjectCards();
addLinksToCards();
updateProjectCount();
orderGrid();
