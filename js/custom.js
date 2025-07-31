
let gridDiv = document.querySelector("#projects .grid");
function addProjectCards() {
    for (project of projects) {
        gridDiv.innerHTML += `
<div class="card">
    ${project.name}
</div>`
    }
};

addProjectCards();
